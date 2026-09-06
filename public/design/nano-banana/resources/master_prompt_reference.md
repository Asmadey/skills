# Nano Banana - Master JSON Prompt Reference Guide

Данное руководство определяет единую JSON-схему для промптинга модели **Nano Banana (Google Gemini 3 Pro Image / Gemini 3.1)**. Структурированный формат гарантирует повторяемость, устранение пластикового вида («AI-slop») и максимальную детализацию.

---

## 1. Схема JSON-промпта

```json
{
  "prompt": "string - Плотное описательное повествование: объект, текстура, окружение, физика камеры, освещение. Используйте нелестные, конкретные термины для реализма (visible pores, uneven skin tone, mild redness, fine wrinkles, 85mm lens, f/1.8, ISO 200, direct flash).",
  "negative_prompt": "string - Список блокаторов: blurry, low resolution, distorted face, extra fingers, overexposed, heavy makeup, unrealistic skin, cartoon, CGI, oversaturated colors, anatomy normalization, datasets-average body, plastic skin, airbrushed, beautified, perfectly symmetrical.",
  "settings": {
    "resolution": "string - '1K', '2K', или '4K'",
    "aspect_ratio": "string - '1:1', '16:9', '9:16', '4:5', '3:4', '4:3'",
    "style": "string - 'documentary realism', 'candid amateur', 'editorial photography', 'analog 35mm film'",
    "lighting": "string - поведение света, например: 'direct on-camera flash creating sharp specular highlights, hard falloff'",
    "camera": "string - фокусное расстояние, апертура, ISO: '85mm f/1.8 ISO 200'",
    "imperfections": "string - 'visible skin pores, peach fuzz, subtle blemishes, uncombed hair, asymmetrical features'"
  }
}
```

---

## 2. Две парадигмы промптинга

### Парадигма 1: Dense Narrative (Плотный связный текст)
Идеально подходит для единичных фотореалистичных портретов, предметной съемки и кинематографичных сцен:
- Явная физика оптики (`85mm lens, f/2.0, ISO 200`).
- Описание реального поведения света (`direct harsh sunlight causing hard dark shadows`).
- Принудительные дефекты реального мира (`mild acne marks, dry lips, lint on clothing, dust motes`).
- Запреты прямо внутри позитивного промпта (`Do not beautify, do not smooth skin, unretouched raw documentary photograph`).

### Парадигма 2: Deep Grid (Многопанельная сетка 2x2)
Используется, когда необходимо сгенерировать коллаж из 4 связанных кадров (один персонаж в разных ракурсах, серия фотографий продукта):
```json
{
  "task": "2x2_candid_portrait_grid",
  "output": {
    "layout": "2x2_grid",
    "aspect_ratio": "1:1",
    "camera_style": "smartphone_front_camera_candid"
  },
  "subject": {
    "appearance": {
      "skin_texture": "realistic unretouched skin, visible pores, peach fuzz",
      "expression": "series of 4 candid facial expressions: thoughtful, laughing, neutral, surprised"
    }
  },
  "grid_panels": [
    {"panel": "top_left", "pose": "close-up candid smile, direct gaze"},
    {"panel": "top_right", "pose": "looking away, side lighting"},
    {"panel": "bottom_left", "pose": "laughing mid-motion, slight motion blur"},
    {"panel": "bottom_right", "pose": "relaxed neutral expression"}
  ]
}
```

---

## 3. Image-to-Image и композиция (до 14 изображений)

Флагманская модель Gemini 3 Pro поддерживает передачу до 14 изображений в одном запросе:
- **Перенос стиля:** передайте исходную фотографию и референс стиля с промптом *"Apply the 35mm film grain, muted color grading and lighting of image 2 to the subject in image 1"*.
- **Замена объектов / Inpainting:** *"Keep everything in the image identical, but replace the sunglasses with classic reading glasses"*.
- **Композиция нескольких объектов:** передайте фото персонажа + фото фона + фото одежды и укажите правила сборки.
