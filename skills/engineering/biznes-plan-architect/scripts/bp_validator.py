#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business Plan Validator (PersonalOS)
Автоматический аудит бизнес-плана на соответствие структуре и отсутствие 6 методологических ошибок.
"""

import sys
import os
import re
from typing import Dict, List, Tuple, Any

REQUIRED_SECTIONS = [
    ("Резюме проекта", [r"резюме", r"executive summary"]),
    ("Концепция и описание продукта/услуг", [r"описание\s+услуг", r"описание\s+продукц", r"существо\s+предлагаемого\s+проекта", r"концепция"]),
    ("Анализ рынка и конкурентов", [r"анализ\s+рынка", r"оценка\s+рынка\s+сбыта", r"конкуренц"]),
    ("Маркетинговый план и сбыт", [r"план\s+маркетинга", r"маркетинговый\s+план", r"стратегия\s+продвижения"]),
    ("Производственный/Операционный план", [r"производственный\s+план", r"операционный\s+план", r"технологическ"]),
    ("Организационный план и график запуска", [r"организационный\s+план", r"календарный\s+план", r"график\s+подготовки"]),
    ("Финансовый план (CAPEX, OPEX, P&L, Cash Flow)", [r"финансовый\s+план", r"план\s+прибылей\s+и\s+убытков", r"cash\s*flow", r"движение\s+денежных"]),
    ("Инвестиционная эффективность (NPV, IRR, Срок окупаемости)", [r"npv", r"irr", r"срок\s+окупаемости", r"эффективность\s+инвестиций"]),
    ("Точка безубыточности (BEP)", [r"точка\s+безубыточности", r"анализ\s+безубыточности", r"порог\s+рентабельности"]),
    ("Анализ рисков и SWOT", [r"анализ\s+рисков", r"оценка\s+риск", r"swot"])
]

GUARDRAIL_CHECKS = [
    {
        "id": "ERR_1_OWN_FUNDS",
        "name": "Ошибка №1: Отсутствие собственного капитала инициатора (перекладывание риска)",
        "patterns": [r"собственн\w+\s+(средств|капитал|вклад)", r"доля\s+собственн\w+", r"equity"],
        "critical": True,
        "recommendation": "Укажите долю собственного капитала инициатора (рекомендуется не менее 20–30% от общей сметы CAPEX)."
    },
    {
        "id": "ERR_2_CLEAR_INVESTMENT_TERMS",
        "name": "Ошибка №2: Неопределенность условий финансирования и графика возврата",
        "patterns": [r"срок\s+(возврата|окупаемости|кредита)", r"ставка", r"график\s+(платежей|погашения|транш)"],
        "critical": True,
        "recommendation": "Четко зафиксируйте объем заемных средств, срок, процентную ставку / доходность инвестора и помесячный/поквартальный график возврата."
    },
    {
        "id": "ERR_3_LEGAL_FRAMEWORK",
        "name": "Ошибка №3: Пробелы в организационно-правовой базе и налоговом режиме",
        "patterns": [r"(ооо|ип|товарищество|ао)", r"(усн|осно|патент|налог)", r"(договор\s+аренды|право\s+собственности|лицензи)"],
        "critical": True,
        "recommendation": "Опишите организационно-правовую форму (ООО/ИП), налоговый режим (УСН 6%, 15% или ОСНО) и статус прав на помещение/землю/оборудование."
    },
    {
        "id": "ERR_4_TECH_SPECIFICATIONS",
        "name": "Ошибка №4: Отсутствие экспертно-технологического обоснования",
        "patterns": [r"оборудовани", r"технологическ\w+\s+(процесс|карта|решени)", r"(гост|санпин|снип|спецификаци)"],
        "critical": False,
        "recommendation": "Приведите технические характеристики оборудования, поставщиков и ссылки на технологические нормативы."
    },
    {
        "id": "ERR_5_HIDDEN_COSTS",
        "name": "Ошибка №5: Забытые операционные расходы (налоги на ФОТ, эквайринг, логистика)",
        "patterns": [r"(взносы|страхов\w+\s+фонд|30%|15%)", r"(коммунал|аренд)", r"(непредвиден|проч)"],
        "critical": True,
        "recommendation": "Убедитесь, что в OPEX учтены страховые взносы на ФОТ (30% или 15%), коммунальные платежи, комиссии эквайринга, маркетинг и резерв на непредвиденные расходы (2–5%)."
    },
    {
        "id": "ERR_6_RISK_DEPTH",
        "name": "Ошибка №6: Формальный анализ рисков и отсутствие мер снижения",
        "patterns": [r"(swot|матрица\s+рисков)", r"(меры\s+по\s+снижению|страховани|компенсаци|минимизаци)"],
        "critical": True,
        "recommendation": "Не ограничивайтесь фразой 'риски минимальны'. Составьте матрицу рисков (вероятность / ущерб) и регламент превентивных действий."
    }
]

def validate_business_plan_text(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    score = 100
    section_results = []
    missing_sections = []

    for name, patterns in REQUIRED_SECTIONS:
        found = any(re.search(p, text_lower) for p in patterns)
        section_results.append((name, found))
        if not found:
            missing_sections.append(name)
            score -= 5

    guardrail_results = []
    failed_guardrails = []

    for check in GUARDRAIL_CHECKS:
        found = any(re.search(p, text_lower) for p in check["patterns"])
        guardrail_results.append((check["name"], found, check["recommendation"]))
        if not found:
            failed_guardrails.append(check)
            deduction = 8 if check["critical"] else 4
            score -= deduction

    score = max(0, min(100, score))
    status = "PASSED" if score >= 80 and not any(g["critical"] for g in failed_guardrails) else "NEEDS_REVISION"

    return {
        "status": status,
        "score": score,
        "section_results": section_results,
        "missing_sections": missing_sections,
        "guardrail_results": guardrail_results,
        "failed_guardrails": failed_guardrails
    }

def print_audit_report(res: Dict[str, Any]):
    print("\n" + "="*70)
    print(f"ОТЧЕТ АУДИТА БИЗНЕС-ПЛАНА (Score: {res['score']}/100 | Status: {res['status']})")
    print("="*70)

    print("\n1. Проверка структуры (Обязательные разделы):")
    for name, found in res["section_results"]:
        status_icon = "✅" if found else "❌"
        print(f"  {status_icon} {name}")

    print("\n2. Проверка защиты от 6 критических ошибок инвестора:")
    for name, found, rec in res["guardrail_results"]:
        status_icon = "✅" if found else "⚠️ "
        print(f"  {status_icon} {name}")
        if not found:
            print(f"     💡 Рекомендация: {rec}")

    print("\n" + "-"*70)
    if res["status"] == "PASSED":
        print("🎉 Бизнес-план соответствует институциональным стандартам качества.")
    else:
        print("⚠️  Бизнес-план требует доработки перед передачей инвесторам или кредиторам.")
    print("="*70 + "\n")


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 bp_validator.py <path_to_business_plan.md>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Ошибка: Файл {path} не найден.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    results = validate_business_plan_text(text)
    print_audit_report(results)
    if results["status"] != "PASSED":
        sys.exit(2)

if __name__ == "__main__":
    main()
