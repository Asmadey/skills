# Примеры прогонов

## 1. Интервью 1-на-1

```bash
export GROQ_API_KEYS="gsk_ключ1,gsk_ключ2"
python3 scripts/process_custdev.py \
  --audio "Meets/audio/Алиса.webm" \
  --interviewer "Влад JGGL" --respondent "Алиса" \
  --title "Кастдев и UX-тестирование JGGL — Алиса" \
  --output-docx "Meets/Стенограмма_и_Фоллоуап_Алиса.docx"
```

Ожидаемый вывод:

```
💰 Бюджет Groq (по локальному учёту за текущие UTC-сутки):
   #1 …a1b2 [openai/gpt-oss-120b]: 12 340/200 000 токенов (6%), сброс через 7h12m | влезает
🚀 Starting CustDev Pipeline for 1 file(s)
--- [Part 1/1] 1. Transcription (Алиса.webm) ---
🎙 Transcribing chunk 1/4 (9.1 MB, offset: 0.0s, model: whisper-large-v3)...
👥 LLM Diarization: 220 сегментов, 2 окно(ок) (budget≈4000 tok, ctx=8), спикеры: Влад JGGL, Алиса
   Batch [0..131] resolved via openai/gpt-oss-120b ✅ (runs, 132 segs)
   Batch [132..219] resolved via openai/gpt-oss-120b ✅ (runs, 88 segs)
✅ Готово за 41.2s: Влад JGGL 96, Алиса 124 | tokens in/out: 7412/418
--- [Part 1/1] 3. Extracting Insights & Profile ---
💾 Saved transcript to: Meets/transcripts/алиса_Алиса.json
```

## 2. Групповая сессия из двух частей

```bash
python3 scripts/process_group_custdev.py \
  --files "part1.webm" "part2.webm" \
  --interviewer "Интервьюер (JGGL)" \
  --respondents "Глеб" "Камиль" "Стас" \
  --hint "Глеб: 27 лет, нейродизайнер" \
  --hint "Камиль: 24 года, архитектор-дизайнер" \
  --hint "Стас: 23 года, нейродизайнер" \
  --title "Групповой кастдев и UX-тестирование JGGL" \
  --slug "группа_12.11" \
  --raw-json raw1.json raw2.json \
  --output-docx "Meets/Стенограмма_и_Фоллоуап_Группа.docx"
```

`--raw-json` — уже сохранённые расшифровки: шаг с whisper пропускается (записи могут быть
удалены с диска, пайплайн продолжит на JSON).

## 3. Повторный прогон (кэш)

```bash
# вторая команда с теми же аргументами ничего не потратит:
♻️  Уже обработано ранее: группа_12.11_ч1.json (303 сегментов, llm-semantic-v2) — пропускаю диаризацию
♻️  Инсайты уже извлекались — беру из кэша (20 пунктов)

# переделать заново (после смены промпта, модели или состава спикеров):
python3 scripts/process_group_custdev.py ... --force
```

## 4. Готовая расшифровка (текст)

```bash
python3 scripts/process_text_custdev.py \
  --input "transcript.txt" \
  --interviewer "Влад JGGL" --respondent "Алекс" \
  --title "Кастдев и UX-тестирование JGGL — Алекс"
```

Формат входа терпимый: `[00:04:43] Спикер 2: текст` или `Имя: текст`.

## 5. Диагностика ключей и бюджета

```bash
python3 scripts/groq_keys.py check    # живы ли ключи, какие у них реальные лимиты
python3 scripts/groq_keys.py status   # что сожжено за сутки и сколько осталось
python3 scripts/groq_keys.py usage 7  # расход за неделю по локальному логу
```
