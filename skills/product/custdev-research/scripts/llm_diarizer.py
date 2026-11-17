#!/usr/bin/env python3
"""
llm_diarizer.py — Context-aware LLM speaker diarization, v2.

Что изменилось относительно v1 (окна по 30 сегментов + по-сегментный JSON):
  * окна планируются по ТОКЕН-БЮДЖЕТУ (~4000 токенов prompt), а не по числу сегментов:
    один вызов покрывает 100-150 сегментов, поэтому system prompt амортизируется
    (в v1 он съедал ~42% расхода: 800 токенов × 11 окон на одну часть встречи);
  * ответ приходит ПРОГОНАМИ подряд идущих реплик
    ({"runs": [["Глеб", 3], ["Интервьюер (JGGL)", 1]]}) — в групповой встрече это
    ~55 записей вместо 303, выход дешевеет примерно в 4 раза;
  * перехлёст отправляется как КОНТЕКСТ и не оплачивается дважды;
  * в каждом окне проверяется полнота (сумма прогонов == число сегментов) с авто-
    восстановлением: хвостовой срез → повтор по индексам → деление окна пополам;
  * все вызовы идут через skills/product/custdev-research/scripts/groq_keys.py, поэтому ключ, упёршийся в
    дневной лимит, заменяется следующим, а не роняет пайплайн.

Совместимость: diarize_transcript(...) сохраняет прежнюю сигнатуру, а поля
transcript_data (timeline / interviewer / respondent / speakers) — прежний вид.
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent))
from groq_keys import KEYRING, AllKeysExhausted, classify  # noqa: E402  multi-key rotation

# --------------------------------------------------------------------------- config

MODEL_CHAIN = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]

# Русский текст в токенайзере o200k ≈ 2.5 символа на токен (замерено на реальном
# окне: 30 сегментов ≈ 773 токена prompt). Оценка нужна только для раскладки окон.
CHARS_PER_TOKEN = 2.5

# TPM на free-тире Groq = 8000 токенов/мин на запрос → держим prompt около 4k,
# чтобы вход + выход одного окна уверенно влезали в лимит.
TOKEN_BUDGET = int(os.getenv("DIARIZER_TOKEN_BUDGET", "4000"))
OVERLAP_SEGMENTS = int(os.getenv("DIARIZER_OVERLAP", "8"))
MIN_TARGET = 20          # меньше — окно вырождается, лучше дотянуть предыдущее
HALVE_TO = 8             # ниже этого порога окно не дробим, ставим дефолт
GAP_MARKER_SEC = 1.0     # пауза → вероятная смена говорящего
MAX_TRUSTED_RUN = int(os.getenv("DIARIZER_MAX_RUN", "20"))  # прогон длиннее — перепроверяем
VERIFY_RUNS = os.getenv("DIARIZER_VERIFY_RUNS", "0") not in ("", "0", "false", "no")
VERIFY_SHARE = 0.2       # доля окна, которую разрешено перепроверять (контроль расхода)


class WindowTooLarge(Exception):
    """Модель отвергла запрос по размеру (её TPM меньше, чем у gpt-oss-120b)."""


def is_diarized(transcript_data: dict) -> bool:
    """Уже размечено? Нужно, чтобы не платить за повторную диаризацию.

    Признаки: есть v2-метка `diarization`, либо (файлы старой версии) в timeline
    большинство сегментов имеют настоящего спикера, а не SPEAKER_UNKNOWN.
    """
    if transcript_data.get("diarization"):
        return True
    timeline = transcript_data.get("timeline") or []
    if not timeline:
        return False
    placeholders = {"SPEAKER_UNKNOWN", "SPEAKER_0", "SPEAKER_1", "SPEAKER_2", "UNKNOWN", ""}
    known = sum(1 for seg in timeline
                if seg.get("speaker") and str(seg["speaker"]).upper() not in placeholders)
    return known >= 0.9 * len(timeline)


def get_groq_client(api_key: str = None):
    """Backward-compatible accessor (v1 API). New code uses KEYRING directly."""
    return KEYRING.client()


# --------------------------------------------------------------------------- prompt

def _build_system_prompt(labels, speaker_hints=None):
    """Компактный system prompt для 2..N спикеров (labels[0] — интервьюер).

    Профиль респондента описывается ОДИН раз, а не повторяется дословно под каждым
    именем (в v1 это дублировало ~250 символов на участника × каждое окно). Имена
    и известные факты сохраняются — они нужны, чтобы модель привязывала реплики
    и «авто-метки» к конкретным людям.
    """
    hints = speaker_hints or {}
    interviewer = labels[0]
    respondents = list(labels[1:])

    lines = [
        "Ты эксперт по семантической диаризации кастдев-интервью и UX-тестирования "
        "мобильного приложения JGGL. Размечаешь спикеров по смыслу реплик.",
        "",
        "Роли:",
        f'- "{interviewer}" — интервьюер / ведущий: задаёт вопросы, ставит задачи, ведёт по '
        'приложению, фасилитирует, подводит итоги ("Слышно меня?", "Давай перейдём…", '
        '"Как думаешь, что значит эта кнопка?", "Кто хочет начать?").',
        "- Респонденты: отвечают на вопросы, описывают экран и свои привычки, жалуются на UX "
        '("я обратил(а) внимание…", "непонятно, где…", "я обычно слушаю на YouTube", "вот здесь зависает").',
        "",
        "Участники:",
    ]
    for i, label in enumerate(labels[1:], start=2):
        hint = hints.get(label)
        lines.append(f'{i}. "{label}"' + (f" — {hint}" if hint else ""))

    if len(respondents) > 1:
        lines += [
            "",
            "Разметка групповой сессии: респонденты перебивают друг друга и соглашаются короткими "
            'репликами ("да, плюс один", "согласен"). Такую реплику относи тому, к кому обращаются, '
            "или тому, кто говорил последним по той же мысли, — не ведущему.",
        ]

    lines += [
        "",
        'Пол — сильнейший сигнал: "я хотел / сказал / понял / сделал" — мужчина, '
        '"я хотела / сказала / поняла / сделала" — женщина.',
        "",
        'Если у сегмента указана "авто-метка" (автоматическая диаризация по голосу), используй её как '
        "подсказку: обычно она верна по голосу, но путает короткие реплики и границы смены говорящего. "
        "При явном противоречии со смыслом реплики доверяй смыслу.",
    ]
    return "\n".join(lines)


def _segment_line(idx, seg, prev=None, with_auto=True):
    """Компактная строка сегмента: индекс + маркеры границы реплики + текст.

    Таймкоды заменены на два дешёвых маркера, которых достаточно для определения
    смены говорящего: '⇄' — перебивание (сегмент начался до конца предыдущего),
    '⏸' — пауза >= 1 c (вероятная смена реплики). Это ~60% короче пары таймкодов
    при том же сигнале о границах.
    """
    flags = ""
    if prev is not None:
        if seg.get("start", 0) < prev.get("end", 0) - 0.05:
            flags += " ⇄"
        elif seg.get("start", 0) - prev.get("end", 0) >= GAP_MARKER_SEC:
            flags += " ⏸"
    auto = ""
    if with_auto and seg.get("auto_speaker"):
        auto = f' (авто: {seg["auto_speaker"]})'
    return f'[{idx}]{flags}{auto}: "{seg.get("text", "").strip()}"'


def _est_tokens(text):
    return max(1, int(len(text) / CHARS_PER_TOKEN))


def _labels_list(labels):
    return "/".join(labels)


def _runs_prompt(labels, lines_ctx, lines_target, target_start, count):
    parts = [
        f"Размечай сегменты [{target_start}]..[{target_start + count - 1}] — ровно {count} шт."
    ]
    if lines_ctx:
        parts += ["", "Контекст ДО (только для понимания диалога, размечать НЕ нужно):", *lines_ctx]
    parts += ["", "Сегменты:", *lines_target, ""]
    parts += [
        "Верни СТРОГО JSON: {\"runs\": [[\"метка\", сколько_подряд], ...]}.",
        f"Склеивай подряд идущие реплики одного спикера. Сумма всех количеств = {count}.",
        f"Метки строго из списка: {_labels_list(labels)}.",
    ]
    return "\n".join(parts)


def _index_prompt(labels, lines_ctx, lines_target, target_start, count):
    parts = [
        f"Размечай сегменты [{target_start}]..[{target_start + count - 1}] — ровно {count} шт."
    ]
    if lines_ctx:
        parts += ["", "Контекст ДО (размечать НЕ нужно):", *lines_ctx]
    parts += ["", "Сегменты:", *lines_target, ""]
    parts += [
        "Верни СТРОГО JSON объект: ключ — индекс сегмента, значение — метка спикера, "
        f"индексы подряд от {target_start} до {target_start + count - 1}, без пропусков.",
        f"Метки строго из списка: {_labels_list(labels)}.",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- parsing

def _normalise_label(raw, labels):
    """Модель иногда возвращает 'Глеб' вместо полной метки — приводим к канону."""
    if not isinstance(raw, str):
        return None
    value = raw.strip().strip('"\'')
    if value in labels:
        return value
    low = value.lower()
    for label in labels:
        if label.lower() == low:
            return label
    for label in labels:
        if low and (low in label.lower() or label.lower() in low):
            return label
    return None


def _expand_runs(data, count, labels):
    """Достаёт последовательность меток длины count из ответа модели.

    Понимает три формата: {"runs": [["метка", n], ...]}, {"runs": ["метка", ...]} и
    {"<индекс>": "метка", ...} (старый формат v1, если модель его всё же выдала).
    Возвращает список меток или None, если длина не совпала.
    """
    runs = data.get("runs")
    if runs is None:
        flat = []
        for key, value in data.items():
            if str(key).isdigit():
                label = _normalise_label(value, labels)
                if label:
                    flat.append(label)
        return flat if len(flat) == count else None

    seq = []
    if isinstance(runs, dict):                      # {"Глеб": 3, ...}
        for label, n in runs.items():
            canon = _normalise_label(label, labels)
            if canon is None:
                return None
            seq.extend([canon] * int(n))
    elif isinstance(runs, list):
        for item in runs:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                canon = _normalise_label(item[0], labels)
                if canon is None:
                    return None
                seq.extend([canon] * int(item[1]))
            elif isinstance(item, str):             # плоский список меток
                canon = _normalise_label(item, labels)
                if canon is None:
                    return None
                seq.append(canon)
            elif isinstance(item, dict):
                label = item.get("speaker") or item.get("label") or item.get("метка")
                n = item.get("count") or item.get("n") or item.get("количество") or 1
                canon = _normalise_label(label, labels)
                if canon is None:
                    return None
                seq.extend([canon] * int(n))
            else:
                return None
    else:
        return None

    if len(seq) < count:
        return None
    if len(seq) > count:
        # Модель разметила и контекст тоже — берём хвост, относящийся к цели.
        seq = seq[-count:]
    return seq


# --------------------------------------------------------------------------- LLM call

def _ask(system_prompt, user_prompt, labels, count, window_label, want_runs=True, skip_models=()):
    """Один вызов с фолбэком по моделям и ротацией ключей. -> (labels_list, model, usage)"""
    for model_name in MODEL_CHAIN:
        if model_name in skip_models:
            continue
        try:
            resp = KEYRING.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=model_name,
                est_tokens=_est_tokens(system_prompt) + _est_tokens(user_prompt),
                temperature=0.0,
                response_format={"type": "json_object"},
            )
        except AllKeysExhausted as err:
            print(f"  Warning: {model_name}: {err}")
            continue
        except Exception as err:
            verdict, _, msg = classify(err)
            if verdict == "too_large":
                # Это не проблема ключа и не повод менять модель: окно слишком
                # большое для TPM этой модели — пусть вызывающий его уменьшит.
                raise WindowTooLarge(f"{model_name}: {msg[:180]}") from err
            brief = str(err).split("'")[0][:110]
            print(f"  Warning: {model_name} failed on {window_label}: {brief}")
            continue

        usage = getattr(resp, "usage", None)
        try:
            data = json.loads(resp.choices[0].message.content.strip())
        except Exception:
            print(f"  Warning: {model_name} returned non-JSON on {window_label}")
            continue

        seq = _expand_runs(data, count, labels)
        spent = (getattr(usage, "prompt_tokens", 0) or 0,
                 getattr(usage, "completion_tokens", 0) or 0)
        if seq:
            kind = "runs" if "runs" in data else "map"
            if kind != ("runs" if want_runs else "map"):
                kind += "/fallback"
            print(f"  {window_label} resolved via {model_name} ✅ ({kind}, {count} segs)")
            return seq, model_name, spent
        got = len(data.get("runs") or []) if isinstance(data.get("runs"), list) else "?"
        print(f"  Warning: {model_name} gave incomplete answer on {window_label} "
              f"(runs={got}, expected {count} segs)")
    return None, None, (0, 0)


# --------------------------------------------------------------------------- windows

def _plan_windows(timeline, system_prompt, token_budget, overlap, max_segments=None):
    """Раскладка окон по токен-бюджету. -> [(ctx_start, target_start, end), ...]

    ctx_start..target_start — перехлёст, отправляется только как контекст.
    """
    lines_tokens, prev = [], None
    for idx, seg in enumerate(timeline):
        lines_tokens.append(_est_tokens(_segment_line(idx, seg, prev)))
        prev = seg

    overhead = _est_tokens(system_prompt) + 120        # boilerplate инструкции
    text_budget = max(600, token_budget - overhead)

    windows, i, n = [], 0, len(timeline)
    while i < n:
        ctx_start = max(0, i - overlap)
        ctx_cost = sum(lines_tokens[ctx_start:i])
        budget = max(1, text_budget - ctx_cost)

        acc, j = 0, i
        while j < n and (acc + lines_tokens[j] <= budget or j == i):
            acc += lines_tokens[j]
            j += 1
        if max_segments:
            j = min(j, i + max_segments)
        # Не оставляем «сиротский» хвост из 1-2 сегментов — приклеиваем к окну.
        if 0 < n - j < MIN_TARGET and n - j <= MIN_TARGET:
            j = n
        windows.append((ctx_start, i, j))
        i = j
    return windows


def _long_runs(seq, max_run):
    """Границы прогонов длиннее max_run: длинная склейка может быть ошибкой модели."""
    found, i = [], 0
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and seq[j + 1] == seq[i]:
            j += 1
        if j - i + 1 > max_run:
            found.append((i, j + 1))
        i = j + 1
    return found


def _verify_long_runs(timeline, system_prompt, labels, target_start, seq, dead_models):
    """Перепроверяет подозрительно длинные прогоны по-индексно и правит их.

    Не включено по умолчанию (VERIFY_RUNS): в реальных кастдевах сегменты короткие
    и прогоны по 20-30 реплик — норма (монолог интервьюера), так что проверка
    срабатывала бы почти всегда и удваивала расход. Включать точечно, когда
    есть подозрение на склейку, через DIARIZER_VERIFY_RUNS=1.
    """
    fixed, spent = 0, [0, 0]
    budget = max(12, int(len(seq) * VERIFY_SHARE))
    suspects = sorted(_long_runs(seq, MAX_TRUSTED_RUN), key=lambda r: r[1] - r[0], reverse=True)
    for a, b in suspects:
        if b - a > budget:
            continue                      # не влезает в лимит проверки — пропускаем
        budget -= b - a
        abs_a, abs_b = target_start + a, target_start + b
        lines_ctx, lines_target, prev = [], [], None
        ctx_start = max(0, abs_a - OVERLAP_SEGMENTS)
        for idx in range(ctx_start, abs_b):
            line = _segment_line(idx, timeline[idx], prev)
            (lines_target if idx >= abs_a else lines_ctx).append(line)
            prev = timeline[idx]
        sub, _, used = _ask(
            system_prompt,
            _index_prompt(labels, lines_ctx, lines_target, abs_a, abs_b - abs_a),
            labels, abs_b - abs_a, f"Verify [{abs_a}..{abs_b - 1}]",
            want_runs=False, skip_models=dead_models,
        )
        spent[0] += used[0]
        spent[1] += used[1]
        if sub and len(sub) == abs_b - abs_a:
            seq[a:b] = sub
            fixed += 1
    return seq, fixed, tuple(spent)


def _resolve_window(timeline, system_prompt, labels, ctx_start, target_start, end,
                    dead_models=frozenset(), verify_runs=None):
    """Разметка одного окна: runs → per-index → деление пополам. -> (seq, model, tokens, verified)"""
    count = end - target_start
    window_label = f"Batch [{target_start}..{end - 1}]"
    verify_runs = VERIFY_RUNS if verify_runs is None else verify_runs

    lines_ctx, lines_target, prev = [], [], None
    for idx in range(ctx_start, end):
        seg = timeline[idx]
        line = _segment_line(idx, seg, prev)
        (lines_target if idx >= target_start else lines_ctx).append(line)
        prev = seg

    try:
        seq, model_name, used = _ask(
            system_prompt,
            _runs_prompt(labels, lines_ctx, lines_target, target_start, count),
            labels, count, window_label, want_runs=True, skip_models=dead_models,
        )
        if seq is None:
            # Второй заход: по-индексный формат (иногда модель лучше держит индексы).
            print(f"  ↳ retry {window_label} as per-index map")
            seq, model_name, extra = _ask(
                system_prompt,
                _index_prompt(labels, lines_ctx, lines_target, target_start, count),
                labels, count, window_label, want_runs=False, skip_models=dead_models,
            )
            used = (used[0] + extra[0], used[1] + extra[1])
    except WindowTooLarge as err:
        print(f"  ↳ {window_label}: запрос велик для модели ({str(err)[:90]}) — делю")
        return _halve(timeline, system_prompt, labels, ctx_start, target_start, end,
                      dead_models, verify_runs)

    if seq:
        verified = 0
        if verify_runs:
            seq, verified, extra = _verify_long_runs(
                timeline, system_prompt, labels, target_start, seq, dead_models)
            used = (used[0] + extra[0], used[1] + extra[1])
        return seq, model_name, used, verified

    return _halve(timeline, system_prompt, labels, ctx_start, target_start, end,
                  dead_models, verify_runs)


def _halve(timeline, system_prompt, labels, ctx_start, target_start, end,
           dead_models, verify_runs):
    count = end - target_start
    if count <= HALVE_TO:
        return None, None, (0, 0), 0
    mid = target_start + count // 2
    print(f"  ↳ splitting Batch [{target_start}..{end - 1}] into halves and retrying")
    head = _resolve_window(timeline, system_prompt, labels, ctx_start, target_start, mid,
                           dead_models, verify_runs)
    tail = _resolve_window(timeline, system_prompt, labels, target_start, mid, end,
                           dead_models, verify_runs)
    if not head[0] and not tail[0]:
        return None, None, (0, 0), 0
    head_seq = head[0] if head[0] else [None] * (mid - target_start)
    tail_seq = tail[0] if tail[0] else [None] * (end - mid)
    tokens = (head[2][0] + tail[2][0], head[2][1] + tail[2][1])
    return head_seq + tail_seq, (head[1] or tail[1]), tokens, head[3] + tail[3]


# --------------------------------------------------------------------------- entry point

def diarize_transcript(transcript_data: dict, interviewer_name: str = "Влад JGGL",
                       respondent_name: str = "Респондент", client=None,
                       batch_size: int = None, overlap: int = None,
                       speakers=None, speaker_hints=None,
                       token_budget: int = None, verify_runs: bool = None):
    """
    Семантическая диаризация стенограммы.

    speakers      — явный список меток (первая = интервьюер), нужен для групповых сессий;
    speaker_hints — {метка: "27 лет, нейродизайнер"};
    token_budget  — сколько токенов prompt допускать на окно (по умолчанию 4000);
    batch_size    — устаревший параметр v1: если задан, дополнительно ограничивает
                    число сегментов в окне;
    overlap       — сколько сегментов предыдущего окна отправлять как контекст (8).
    """
    timeline = transcript_data.get("timeline", [])
    if not timeline:
        return transcript_data

    labels = list(speakers) if speakers else [interviewer_name, respondent_name]
    budget = token_budget or TOKEN_BUDGET
    overlap = OVERLAP_SEGMENTS if overlap is None else overlap

    system_prompt = _build_system_prompt(labels, speaker_hints)
    windows = _plan_windows(timeline, system_prompt, budget, overlap, max_segments=batch_size)

    print(f"👥 LLM Diarization: {len(timeline)} сегментов, {len(windows)} окно(ок) "
          f"(budget≈{budget} tok, ctx={overlap}), спикеры: {', '.join(labels)}")
    print(f"   system prompt ≈ {_est_tokens(system_prompt)} токенов")

    started = time.time()
    resolved = [None] * len(timeline)
    models_used: dict[str, int] = {}
    tokens_in = tokens_out = 0
    verified_runs = 0
    dead_models: set[str] = set()          # модели без суточного бюджета — не трогаем больше

    for ctx_start, target_start, end in windows:
        seq, model_name, used, verified = _resolve_window(
            timeline, system_prompt, labels, ctx_start, target_start, end,
            dead_models=dead_models, verify_runs=verify_runs,
        )
        tokens_in += used[0]
        tokens_out += used[1]
        verified_runs += verified
        if model_name:
            models_used[model_name] = models_used.get(model_name, 0) + 1

        if not seq:
            print(f"  Fallback: [{target_start}..{end - 1}] без ответа — ставлю авто-метку/дефолт")
            for idx in range(target_start, end):
                auto = timeline[idx].get("auto_speaker")
                resolved[idx] = auto if auto in labels else labels[0]
            continue

        for offset, label in enumerate(seq):
            idx = target_start + offset
            if idx >= len(timeline):
                break
            resolved[idx] = label if label in labels else labels[0]

    # Ни один индекс не должен остаться пустым
    missing = [i for i, value in enumerate(resolved) if value is None]
    if missing:
        print(f"  Warning: {len(missing)} сегмент(ов) без метки — дефолт "
              f"'{labels[0]}' для {missing[:5]}{'…' if len(missing) > 5 else ''}")
        for idx in missing:
            resolved[idx] = labels[0]

    for idx, seg in enumerate(timeline):
        seg["speaker"] = resolved[idx]

    counts: dict[str, int] = {}
    for label in resolved:
        counts[label] = counts.get(label, 0) + 1
    elapsed = time.time() - started

    transcript_data["timeline"] = timeline
    transcript_data["interviewer"] = labels[0]
    transcript_data["respondent"] = ", ".join(labels[1:]) if len(labels) > 2 else labels[-1]
    transcript_data["speakers"] = labels
    transcript_data["diarization"] = {
        "engine": "llm-semantic-v2",
        "windows": len(windows),
        "token_budget": budget,
        "context_segments": overlap,
        "models": models_used,
        "verified_runs": verified_runs,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "seconds": round(elapsed, 1),
        "speaker_counts": counts,
    }

    print(f"✅ Готово за {elapsed:.1f}s: " + ", ".join(f"{k} {v}" for k, v in counts.items())
          + f" | tokens in/out: {tokens_in}/{tokens_out}"
          + (f" | модели: {', '.join(f'{m}×{c}' for m, c in models_used.items())}" if models_used else ""))
    return transcript_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 llm_diarizer.py <input_json> [interviewer] [respondent] [output_json]")
        sys.exit(1)

    in_file = sys.argv[1]
    interviewer = sys.argv[2] if len(sys.argv) > 2 else "Влад JGGL"
    respondent = sys.argv[3] if len(sys.argv) > 3 else "Респондент"
    out_file = sys.argv[4] if len(sys.argv) > 4 else in_file

    with open(in_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = diarize_transcript(data, interviewer, respondent)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Diarization saved to {out_file}")
