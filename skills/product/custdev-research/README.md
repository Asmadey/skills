# custdev-research

Разбор записей кастдев-интервью и UX-тестирования в карточку исследования: стенограмма с
атрибуцией спикеров, профили респондентов, продуктовые боли с привязкой к говорящему, фоллоуап,
DOCX и строка в реестре.

Полное описание и рабочие процессы — в [SKILL.md](./SKILL.md).

```bash
pip install -r requirements.txt          # + системный ffmpeg
export GROQ_API_KEYS="gsk_ключ1,gsk_ключ2"

python3 scripts/process_custdev.py --audio "Meets/audio/Алиса.webm" \
  --interviewer "Влад JGGL" --respondent "Алиса" --title "Кастдев — Алиса"

python3 scripts/process_group_custdev.py --files part1.webm part2.webm \
  --respondents "Глеб" "Камиль" "Стас" --slug "группа_12.11"
```

Что внутри:

- семантическая диаризация спикеров v2 — окна по токен-бюджету, ответ прогонами, валидация полноты
  (−50…−60% токенов против окон по 30 сегментов);
- кольцо ключей Groq с ротацией на дневных лимитах, учётом расхода и pre-flight проверкой бюджета;
- кэш: повторный прогон уже разобранной встречи не тратит токенов (`--force` для пересчёта).

Подробности — [references/groq-limits.md](./references/groq-limits.md),
[references/registry-format.md](./references/registry-format.md),
[examples/quickstart.md](./examples/quickstart.md).
