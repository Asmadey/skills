# Пример Графа Работ: Прием нового товара (Bazon)

Этот пример показывает, как применить AJTBD к процессу приемки товара на складе (Аватар 4).

## Контекст
Руководитель склада хочет оприходовать новую партию запчастей (бамперы, фары), чтобы быстрее выставить их на продажу.

## Анализ
1.  **Meta Job:** Заработать деньги на продаже запчастей.
2.  **Core Job:** Оприходовать товар на склад.
3.  **Micro-Jobs (Steps):**
    -   Найти накладную.
    -   Вбить название детали.
    -   Определить, от какой машины (по году/кузову).
    -   Оценить состояние (дефекты).
    -   Сфотографировать.
    -   Назначить цену.
4.  **Проблемы (Tax Jobs):**
    -   Ручной ввод длинных названий (Ошибки, Время).
    -   Поиск в интернете, чтобы понять, от какой машины деталь (Потеря фокуса).
    -   Вспоминание цены закупки (Нагрузка на память).

## Решение (Value Creation)
-   **Automate:** Распознавание детали и авто по фото.
-   **Kill:** Ручной ввод названия.
-   **Delegate:** Оценку рыночной цены (ИИ подсказывает среднюю по рынку).

## Визуализация (Mermaid)

```mermaid
graph TD
    %% Стили
    classDef value fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000;
    classDef job fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000;
    classDef problem fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000;
    classDef solution fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px,color:#000;

    %% Иерархия
    Sell("💸 Заработать на продаже"):::value
    Receive("📦 Оприходовать товар"):::job
    
    %% Процесс AS IS (Как есть)
    TypeData("⌨️ Вбить название и авто"):::job
    Google("🔍 Гуглить совместимость"):::problem
    Assess("👀 Оценить дефекты"):::job
    Price("🏷 Назначить цену"):::job
    
    %% Проблемы
    Error1("⚡️ Опечатки и ошибки"):::problem
    TimeLoss("⏳ Потеря 15 мин/деталь"):::problem
    
    %% Решение TO BE (Как будет)
    AI_Vision("🤖 Bazon Vision<br/>(Распознавание по фото)"):::solution
    AutoPrice("📊 Авто-прайсинг"):::solution

    %% Связи
    Sell --> Receive
    Receive --> TypeData
    Receive --> Assess
    Receive --> Price
    
    TypeData --> Google
    TypeData --> Error1
    Google --> TimeLoss
    
    %% Трансформация
    AI_Vision --"KILL (Убивает ручной ввод)"--> TypeData
    AI_Vision --"AUTOMATE (Сама определяет авто)"--> Google
    AutoPrice --"DELEGATE (Подсказывает цену)"--> Price
```
