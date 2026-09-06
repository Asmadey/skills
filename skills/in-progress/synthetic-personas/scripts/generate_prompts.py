import json
import argparse
import os

def generate_synthetic_prompts(persona_card):
    """
    Генерирует паттерны промптов на основе Persona Card.
    В продакшн-версии здесь вызывается LLM. 
    Этот скрипт подготавливает "Запрос к модели" для имитации поведения.
    """
    
    jtbd = persona_card.get("jtbd", "")
    constraints = persona_card.get("constraints", [])
    vocabulary = persona_card.get("vocabulary", [])
    success_metric = persona_card.get("success_metric", "")

    # Шаблоны интентов на основе статьи
    prompt_templates = [
        "Как {jtbd} учитывая {constraint}",
        "{vocabulary_word} руководство для {jtbd}",
        "Лучший способ {jtbd} чтобы {success_metric}",
        "Сравнение инструментов для {jtbd} с поддержкой {vocabulary_word}",
        "Как исправить {jtbd} если мешает {constraint}"
    ]

    prompts = []
    # Смешиваем поля для генерации разнообразия
    for i, template in enumerate(prompt_templates):
        const = constraints[i % len(constraints)] if constraints else "ограничения"
        vocab = vocabulary[i % len(vocabulary)] if vocabulary else "инструмент"
        
        prompt = template.format(
            jtbd=jtbd.lower(),
            constraint=const.lower(),
            vocabulary_word=vocab,
            success_metric=success_metric.lower()
        )
        prompts.append(prompt)

    return prompts

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic prompts from a Persona Card')
    parser.add_argument('--file', type=str, help='Path to persona JSON file')
    args = parser.parse_args()

    if not args.file:
        # Пример данных, если файл не указан
        persona_data = {
            "name": "Александр (Авторазбор)",
            "jtbd": "Оцифровать склад и автоматизировать выгрузку на Авито",
            "constraints": ["нет времени на долгое обучение", "страх потери данных"],
            "vocabulary": ["штрих-код", "адресное хранение", "выгрузка"],
            "success_metric": "видеть остатки в телефоне в реальном времени"
        }
    else:
        with open(args.file, 'r', encoding='utf-8') as f:
            persona_data = json.load(f)

    print(f"\n👤 Персонаж: {persona_data.get('name')}")
    print("-" * 30)
    
    generated = generate_synthetic_prompts(persona_data)
    
    print("🚀 Сгенерированные промпты для отслеживания:")
    for i, p in enumerate(generated, 1):
        print(f"{i}. {p}")

if __name__ == "__main__":
    main()
