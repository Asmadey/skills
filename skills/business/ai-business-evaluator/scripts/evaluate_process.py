#!/usr/bin/env python3
"""
AI Process Evaluator CLI (v2.0 - 4 Buckets & YaP/Varick Methodology)
Оценивает бизнес-процесс:
- Touch Time vs. Elapsed Time
- Распределение по 4 корзинам:
  0. Eliminate (Удалить полностью - лишние звенья)
  1. Deterministic (Обычный код/скрипты/интеграции)
  2. Agentic (ИИ-агенты)
  3. HITL (Human-in-the-Loop)
- Расчет сжатия времени цикла (Cycle Time) и устранения Handoffs
"""

import sys
import json
import argparse
from typing import List, Dict, Any

def evaluate_process(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_touch_minutes = 0.0
    total_elapsed_hours = 0.0
    
    bucket_counts = {
        "eliminate": 0,
        "deterministic": 0,
        "agentic": 0,
        "hitl": 0,
        "unclassified": 0
    }
    handoff_count = 0
    eliminated_handoffs = 0
    
    for step in steps:
        touch = float(step.get("touch_minutes", 0))
        elapsed = float(step.get("elapsed_hours", 0))
        bucket = step.get("bucket", "unclassified").lower()
        is_handoff = step.get("is_handoff", False)
        
        total_touch_minutes += touch
        total_elapsed_hours += elapsed
        
        if bucket in bucket_counts:
            bucket_counts[bucket] += 1
        else:
            bucket_counts["unclassified"] += 1
            
        if is_handoff:
            handoff_count += 1
            if bucket in ("eliminate", "deterministic", "agentic"):
                eliminated_handoffs += 1

    total_steps = len(steps)
    if total_steps == 0:
        return {"error": "Нет данных о шагах процесса"}

    # Расчет времени после реинжиниринга:
    # Eliminate: 0 часов
    # Deterministic: секунды (0.01 ч)
    # Agentic: минуты (0.05 ч)
    # HITL: сжатие до 30 мин за счет готового досье
    estimated_new_elapsed_hours = (
        (bucket_counts["eliminate"] * 0.0) +
        (bucket_counts["deterministic"] * 0.01) +
        (bucket_counts["agentic"] * 0.05) +
        (bucket_counts["hitl"] * 0.5)
    )
    
    time_reduction_pct = max(0.0, ((total_elapsed_hours - estimated_new_elapsed_hours) / total_elapsed_hours * 100)) if total_elapsed_hours > 0 else 0

    return {
        "summary": {
            "total_steps_as_is": total_steps,
            "total_steps_to_be": total_steps - bucket_counts["eliminate"],
            "eliminated_useless_steps": bucket_counts["eliminate"],
            "total_handoffs_as_is": handoff_count,
            "eliminated_handoffs": eliminated_handoffs,
            "current_touch_time_hours": round(total_touch_minutes / 60, 2),
            "current_elapsed_time_days": round(total_elapsed_hours / 24, 1),
            "estimated_new_elapsed_time_days": round(estimated_new_elapsed_hours / 24, 2),
            "cycle_time_reduction_pct": round(time_reduction_pct, 1),
        },
        "four_buckets_distribution": {
            "0_eliminate": f"{bucket_counts['eliminate']} ({round(bucket_counts['eliminate'] / total_steps * 100)}%)",
            "1_deterministic": f"{bucket_counts['deterministic']} ({round(bucket_counts['deterministic'] / total_steps * 100)}%)",
            "2_agentic": f"{bucket_counts['agentic']} ({round(bucket_counts['agentic'] / total_steps * 100)}%)",
            "3_hitl": f"{bucket_counts['hitl']} ({round(bucket_counts['hitl'] / total_steps * 100)}%)",
        },
        "diagnosis": (
            f"Выявлен колоссальный разрыв: Touch Time = {round(total_touch_minutes / 60, 1)} ч. "
            f"против Elapsed Time = {round(total_elapsed_hours / 24, 1)} дн. "
            f"Ликвидация {bucket_counts['eliminate']} лишних звеньев и автоматизация {eliminated_handoffs} передач "
            f"сократят время процесса на {round(time_reduction_pct)}%."
        )
    }

def demo():
    # Демо-кейс B2B: Заведение продукции в торговые сети
    demo_steps = [
        {"name": "Сбор требований сети и формата спецификации", "touch_minutes": 120, "elapsed_hours": 48, "bucket": "agentic", "is_handoff": True},
        {"name": "Ручное дублирование номенклатуры во внутренний промежуточный отчет", "touch_minutes": 60, "elapsed_hours": 24, "bucket": "eliminate", "is_handoff": True},
        {"name": "Сведение карточек товаров и валидация квантов/штрихкодов", "touch_minutes": 180, "elapsed_hours": 24, "bucket": "deterministic", "is_handoff": False},
        {"name": "Расчет цен, промо-скидок и ретро-бонусов", "touch_minutes": 60, "elapsed_hours": 72, "bucket": "agentic", "is_handoff": True},
        {"name": "Формирование презентации новинки и обоснования", "touch_minutes": 180, "elapsed_hours": 48, "bucket": "agentic", "is_handoff": False},
        {"name": "Вычитка договора юристом на предмет скрытых штрафов", "touch_minutes": 90, "elapsed_hours": 96, "bucket": "agentic", "is_handoff": True},
        {"name": "Утверждение коммерческих условий коммерческим директором", "touch_minutes": 15, "elapsed_hours": 24, "bucket": "hitl", "is_handoff": True},
        {"name": "Отправка в личный кабинет сети и контроль статуса", "touch_minutes": 30, "elapsed_hours": 120, "bucket": "deterministic", "is_handoff": True},
    ]
    res = evaluate_process(demo_steps)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Анализатор процессов по методологии 4 корзин (YaP & Varick)")
    parser.add_argument("--demo", action="store_true", help="Запустить демо-оценку")
    parser.add_argument("file", nargs="?", help="JSON файл с шагами")
    
    args = parser.parse_args()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
            steps = data.get("steps", data)
            print(json.dumps(evaluate_process(steps), indent=2, ensure_ascii=False))
    else:
        demo()
