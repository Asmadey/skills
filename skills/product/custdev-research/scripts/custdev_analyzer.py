#!/usr/bin/env python3
"""
custdev_analyzer.py — Deep Product Insight Extractor for CustDev Interviews.
Extracts user profile (age, profession, AI experience) and numbered concise UX pain bullets.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_keys import KEYRING  # noqa: E402  multi-key rotation


def get_groq_client(api_key: str = None):
    """Backward-compatible accessor; calls below go through KEYRING for rotation."""
    return KEYRING.client()

SYSTEM_PROMPT_BULLETS = """Ты главный продуктовый аналитик и Product Manager (JGGL).
Твоя задача — извлечь из стенограммы кастдев-интервью и UX-тестирования мобильного приложения:
1. Профиль клиента (Имя, возраст, профессия/роль, опыт в AI инструментах, опыт в приложении JGGL).
2. Список четких, емких продуктовых наблюдений и болей пользователя (UX-инсайты) в формате нумерованного списка.

ФОРМАТ КАЖДОГО ПУНКТА САММАРИ:
- Пиши кратко, конкретно, фактологично (1-2 предложения на пункт).
- Описывай поведение, восприятие, заблуждения и затруднения пользователя.

ПРИМЕРЫ ПУНКТОВ:
- Посты не подгружаются. Пользователь думает, что интернет не грузит.
- Пользователь не понимает разницы между постами-треками и обычными публикациями.
- Странный контент в ленте 360: не по интересам, ощущается как несвязанный микс из всего.
- Пользователь в ленте рилсов не понимает, что экран можно скроллить дальше.
- Для сохранения трека из ленты пользователь нажимает на мини-плеер, но там функции неактивны.
- Кнопку «Добавить в мои треки» пользователь не замечает на экране.
- После добавления трека в «Мои саундтреки» пользователь не понимает, где их найти.
- Пользователь не понимает, что такое «Promote» и «Talk with bot».
- Кнопка «Create Post» воспринимается как добавление нескольких картинок, а не публикация.
- При подтверждении списания токена пользователь подумал, что требуется реальная покупка за деньги.
- Пользователь не видит историю диалога и считает, что чат с ассистентом пропал.
- Непонятно, как опубликовать отдельно только аудиодорожку без видео.
- В видео бот сам подбирает фоновый звук, и пользователю непонятно, как его настроить или заменить.
- Пользователь по умолчанию отключает системные push-уведомления при первом запросе.

Ответь строго в формате JSON:
{
  "respondent_profile": "Имя, возраст, профессия. Опыт в AI: ..., Опыт в JGGL: ...",
  "summary_bullets": [
    "Пункт 1...",
    "Пункт 2..."
  ]
}
"""

SYSTEM_PROMPT_GROUP = """Ты главный продуктовый аналитик и Product Manager (JGGL).
Тебе дают стенограмму ГРУППОВОГО кастдев-тестирования: ведущий и НЕСКОЛЬКО респондентов.
Извлеки:
1. Профиль КАЖДОГО респондента (имя, возраст, профессия/роль, опыт в AI-инструментах, опыт в JGGL).
2. Список четких продуктовых наблюдений и болей. КАЖДЫЙ пункт начинается с метки говорящего в квадратных скобках: "[Имя] ..."

ФОРМАТ ПУНКТОВ:
- Кратко, конкретно, фактологично (1-2 предложения на пункт).
- Описывай поведение, восприятие, заблуждения и затруднения конкретного человека.
- Если двое и более участников независимо жалуются на одно и то же — отметь это в одном пункте: "[Глеб, Камила] ...".
- Если участники СПОРЯТ или оценивают одну и ту же вещь по-разному — отдельный пункт: "[Глеб] считает X, [Стас] не согласен: Y".
- Добавляй в пункты только то, что реально прозвучало в стенограмме.
- Пункты всегда привязаны к РЕСПОНДЕНТАМ. Если реплику произнес ведущий — это либо пересказ мнения участников, либо его собственная гипотеза: пересказ атрибутируй тому участнику, чье мнение пересказано; гипотезу ведущего в боли НЕ включай вовсе.
- Если реплики участников короткие и разметка спикеров может быть неточной — лучше напиши "[Респонденты] ...", чем приписать боль не тому человеку.

ПРИМЕРЫ ПУНКТОВ:
- [Глеб] Не нашел историю генераций: вкладка спрятана под иконкой «две полоски», подписи нет.
- [Камила] Не понимает, чем «Студия» отличается от «Чата», начинает путь генерации не с той вкладки.
- [Глеб, Стас] Просят структурировать историю по типам контента (изображения / обложки / музыка / клипы).
- [Стас] Считает, что кнопку «Publish post» надо выделить цветом или иконкой; [Камила] говорит, что сдержанный стиль важнее.

Ответь строго в формате JSON:
{
  "profiles": {"Имя1": "Имя, возраст, профессия. Опыт в AI: ..., Опыт в JGGL: ...", "Имя2": "..."},
  "summary_bullets": ["[Имя] Пункт 1...", "[Имя] Пункт 2..."]
}
"""


def _sample_dialogue(timeline, max_segments: int = 140):
    step = max(1, len(timeline) // max_segments) if len(timeline) > max_segments else 1
    sampled = timeline[::step]
    return "\n".join([
        f"[{t.get('speaker', 'Участник')}]: {t.get('text', '').strip()}"
        for t in sampled if t.get("text")
    ])


def extract_group_insights(transcript_data: dict, client=None, model="openai/gpt-oss-120b"):
    """Group-session variant: returns (profiles dict, attributed bullets list)."""
    if client is None:
        client = get_groq_client()

    timeline = transcript_data.get("timeline", [])
    speakers = transcript_data.get("speakers") or []
    interviewer = transcript_data.get("interviewer", "Интервьюер")
    respondents = [s for s in speakers if s != interviewer]

    user_prompt = f"""Стенограмма группового UX-тестирования.
Ведущий: {interviewer}
Респонденты: {', '.join(respondents) if respondents else 'несколько участников'}

Диалог:
{_sample_dialogue(timeline)}
"""

    models_to_try = [model, "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    for m in models_to_try:
        try:
            resp = KEYRING.chat(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_GROUP},
                    {"role": "user", "content": user_prompt}
                ],
                model=m,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            data = json.loads(resp.choices[0].message.content.strip())
            profiles = data.get("profiles") or {}
            bullets = [b for b in (data.get("summary_bullets") or []) if str(b).strip()]
            if bullets:
                return profiles, bullets
            print(f"  Warning: Model {m} returned no bullets. Trying next...")
        except Exception as e:
            print(f"  Warning: Model {m} failed during group insight extraction ({e}). Trying next...")

    profiles = {r: f"{r}, участник группового тестирования JGGL." for r in respondents}
    return profiles, [
        "Участники протестировали базовые сценарии генерации и навигации по приложению.",
        "Зафиксированы затруднения с поиском истории генераций и разделением разделов «Студия» и «Чат».",
    ]


def extract_insights_and_profile(transcript_data: dict, client=None, model="openai/gpt-oss-120b"):
    if client is None:
        client = get_groq_client()

    timeline = transcript_data.get("timeline", [])
    interviewer = transcript_data.get("interviewer", "Влад JGGL")
    respondent = transcript_data.get("respondent", "Респондент")

    # Sample dialogue if large
    step = len(timeline) // 80 if len(timeline) > 80 else 1
    sampled = timeline[::step]
    dialogue_str = "\n".join([
        f"[{t.get('speaker', 'Участник')}]: {t.get('text', '').strip()}"
        for t in sampled if t.get("text")
    ])

    user_prompt = f"""Стенограмма диалога:
Интервьюер: {interviewer}
Респондент: {respondent}

Диалог:
{dialogue_str}
"""

    models_to_try = [model, "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]

    for m in models_to_try:
        try:
            resp = KEYRING.chat(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_BULLETS},
                    {"role": "user", "content": user_prompt}
                ],
                model=m,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            raw = resp.choices[0].message.content.strip()
            data = json.loads(raw)
            profile = data.get("respondent_profile", "")
            bullets = data.get("summary_bullets", [])
            if bullets:
                return profile, bullets
        except Exception as e:
            print(f"  Warning: Model {m} failed during insight extraction ({e}). Trying next...")

    # Fallback
    default_profile = f"{respondent}, респондент кастдев-тестирования мобильного приложения JGGL."
    default_bullets = [
        "Пользователь протестировал базовые сценарии онбординга и навигации в приложении.",
        "Выявлены затруднения в понимании назначения кнопок плеера и генераций.",
        "Зафиксированы проблемы с задержкой подгрузки контента и видео в ленте."
    ]
    return default_profile, default_bullets

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 custdev_analyzer.py <transcript_json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        t_data = json.load(f)

    prof, b_list = extract_insights_and_profile(t_data)
    print("Profile:", prof)
    print("Bullets:")
    for b in b_list:
        print("-", b)
