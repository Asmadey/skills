# Правила промптинга и 13 правил гиперреализма (Anti-AI-Slop)

Модели генерации изображений имеют склонность к усреднению (бьютификация, идеальная симметрия, восковая пластиковая кожа). Для получения живых фотографий студийного и документального качества следуйте этим правилам.

---

## 1. Контрольный список 13 правил фотореализма

1. **Текстура кожи:** Принудительно указывайте микродетали: `visible pores, uneven skin tone, micro-wrinkles, asymmetric freckles, subtle skin imperfections`.
2. **Запрет AI-фильтров:** Явно требуйте: `no AI beauty filters, unretouched, raw sensor data, non-commercial candid photograph`.
3. **Оптика и дисторсия:** Указывайте объектив: `85mm f/1.8 lens, subtle barrel distortion (35mm), micro-chromatic aberration at high contrast edges`.
4. **Текстуры ткани:** Описывайте складки, текстуру волокон, нитки: `rough denim weave, fraying edges, cotton lint, natural fabric wrinkles`.
5. **Хаос окружающей среды:** Реальный мир не стерилен: `mild dust motes, subtle background clutter, realistic indoor lighting imperfections`.
6. **Глубина резкости (Bokeh):** `shallow depth of field, natural circular optical bokeh, sharp focus on the iris`.
7. **Цифровой и пленочный шум:** `visible sensor grain (ISO 400/800), slight motion blur on moving hands, realistic exposure latitude`.
8. **Аналоговые характеристики:** `35mm film stock, slight halation around bright light sources, natural color saturation`.
9. **Асимметрия лица:** Человеческие лица не симметричны: `subtle facial asymmetry, slightly crooked smile, natural eyebrow irregularity`.
10. **Поведение света:** Не называйте свет абстрактно, описывайте его действие: `harsh overhead fluorescent lighting causing hard shadows under cheekbones and chin`.
11. **Живая поза (Candid):** Избегайте поз манекенов: `candid posture, caught mid-movement, off-center framing, relaxed shoulders`.
12. **Волосы:** Волосы не лежат идеальным шлемом: `flyaway hairs, frizzy strands, uncombed texture, wisps blowing in the breeze`.
13. **Нефокусные элементы фона:** `subtly blurred background lights, ambient room reflection on surfaces`.

---

## 2. Базовый негативный стек (Negative Stack)

При генерации реалистичных людей и объектов используйте следующий проверенный стек блокаторов:

```
blurry, low resolution, distorted face, extra fingers, malformed hands, overexposed, heavy makeup, unrealistic skin, cartoon, CGI, 3D render, oversaturated colors, anatomy normalization, datasets-average body, plastic skin, airbrushed, wax figure, beautified, perfectly symmetrical face, stock photo look.
```

---

## 3. Протокол повторной генерации (Rectification Loop)

Если предыдущее сгенерированное изображение не прошло визуальный контроль (например, слишком гладкая кожа или неправильная кисть руки), новый промпт обязан начинаться с формулы исправления:

```
Rectification of failed artifact: Correcting [ТОЧНАЯ_ПРИЧИНА_ОШИБКИ, например: artificial smooth plastic skin replaced with raw unretouched skin pores and uneven tone]...
```
Модели внимания Gemini чувствительны к этой формуле и приоритетно исправляют указанный дефект.
