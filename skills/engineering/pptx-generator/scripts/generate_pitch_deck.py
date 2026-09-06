from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- THEME CONFIGURATION (Light Theme) ---
BG_COLOR = RGBColor(248, 250, 252)      # #F8FAFC
TEXT_PRIMARY = RGBColor(31, 41, 55)     # #1F2937
TEXT_SECONDARY = RGBColor(75, 85, 99)   # #4B5563
ACCENT_PRIMARY = RGBColor(99, 102, 241) # #6366F1
CARD_BG = RGBColor(224, 242, 254)       # #E0F2FE (Light Blue)
CARD_BG_PRO = RGBColor(96, 165, 250)    # #60A5FA (Blue)
WHITE = RGBColor(255, 255, 255)

def create_presentation():
    prs = Presentation()
    
    # Set slide size to 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    def add_slide(layout_index=6): # 6 is usually blank
        slide = prs.slides.add_slide(prs.slide_layouts[layout_index])
        
        # Set background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR
        return slide

    def add_title(slide, text, font_size=40, top=Inches(0.5)):
        textbox = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.73), Inches(1))
        tf = textbox.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.name = "Arial"  # Fallback for Inter
        p.font.bold = True
        p.font.color.rgb = TEXT_PRIMARY
        return p

    def add_subtitle(slide, text, top=Inches(1.3)):
        textbox = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.73), Inches(0.5))
        tf = textbox.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(20)
        p.font.name = "Arial"
        p.font.color.rgb = TEXT_SECONDARY
        return p

    def add_card(slide, left, top, width, height, color=CARD_BG):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = ACCENT_PRIMARY
        shape.line.width = Pt(1) # Thin border
        shape.adjustments[0] = 0.05 # Roundness
        return shape

    def add_text_in_box(slide, left, top, width, height, text, size=18, color=TEXT_PRIMARY, bold=False):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        tf = textbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.name = "Arial"
        p.font.color.rgb = color
        p.font.bold = bold
        return tf

    # ==========================================
    # SLIDE 1: TITLE
    # ==========================================
    slide = add_slide()
    
    # Logo
    add_text_in_box(slide, Inches(0.8), Inches(2.5), Inches(4), Inches(1), "RentalLife", 48, ACCENT_PRIMARY, True)
    
    # Title
    t_frame = add_text_in_box(slide, Inches(0.8), Inches(3.5), Inches(10), Inches(2), "Превращаем квартиры пенсионеров в доходный портфель", 44, TEXT_PRIMARY, True)
    
    # Subtitle
    add_text_in_box(slide, Inches(0.8), Inches(5.0), Inches(10), Inches(1), "Платформа пожизненной ренты с equity-sharing моделью", 24, TEXT_SECONDARY)
    
    # Stats Card
    bg = add_card(slide, Inches(6), Inches(2.5), Inches(6.5), Inches(3), CARD_BG)
    add_text_in_box(slide, Inches(6.5), Inches(3), Inches(2), Inches(1), "35.6М\nпожилых в РФ", 20, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(8.5), Inches(3), Inches(2), Inches(1), "~40К\nдефицит/мес", 20, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(10.5), Inches(3), Inches(2), Inches(1), "IRR 95%\nдля инвестора", 20, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(6.5), Inches(4.5), Inches(6), Inches(0.5), "Pitch Deck • Февраль 2026 • Seed Round: 4.4M ₽", 14, TEXT_SECONDARY)

    # ==========================================
    # SLIDE 2: HISTORY
    # ==========================================
    slide = add_slide()
    add_title(slide, "История бизнеса")
    add_subtitle(slide, "Как мы пришли к решению, которое нужно миллионам")
    
    # Timeline
    y = 2.5
    events = [
        ("2019-2022", "Исследование", "5+ лет в elderly care. Изучение модели ренты в Испании и Германии"),
        ("2023", "Валидация", "100+ лидов квалифицировано. Юридическая модель проверена"),
        ("2024", "Пилот", "3 контракта подписано. MVP CRM. Доход уже идёт. Конверсия 3.3%"),
        ("2025-2026", "Масштабирование", "Seed Round 4.4M ₽. AI голосовые агенты. 100 контрактов Year 1")
    ]
    
    x = 0.8
    for year, title, desc in events:
        add_card(slide, Inches(x), Inches(y), Inches(2.8), Inches(3), WHITE)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+0.2), Inches(2.4), Inches(0.5), year, 18, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+0.6), Inches(2.4), Inches(0.5), title, 16, TEXT_PRIMARY, True)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+1.0), Inches(2.4), Inches(1.5), desc, 12, TEXT_SECONDARY)
        x += 3.1

    # ==========================================
    # SLIDE 3: PROBLEM
    # ==========================================
    slide = add_slide()
    add_title(slide, "Проблема: кризис достойной старости")
    
    # Stats
    stats = [
        ("35.6М", "людей 60+ (Росстат)"),
        ("~25К", "средняя пенсия в МО"),
        ("40-110К", "пансионат/мес"),
        ("−40К", "дефицит ежемесячно")
    ]
    
    y_stat = 2.0
    for val, lbl in stats:
        add_text_in_box(slide, Inches(0.8), Inches(y_stat), Inches(5), Inches(0.8), f"{val} - {lbl}", 20, TEXT_PRIMARY)
        y_stat += 0.8

    # Highlight Card
    add_card(slide, Inches(6), Inches(2), Inches(6.5), Inches(4), CARD_BG)
    add_text_in_box(slide, Inches(6.5), Inches(2.5), Inches(5.5), Inches(1), "~80% пожилых владеют жильём", 24, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(6.5), Inches(3.5), Inches(5.5), Inches(2), "Квартира 10-25M ₽ — лежит мёртвым грузом, пока пенсионер не может себе позволить уход.\n\nВыбор: достойный уход ИЛИ своя квартира", 18, TEXT_PRIMARY)

    # ==========================================
    # SLIDE 4: PRODUCT
    # ==========================================
    slide = add_slide()
    add_title(slide, "Продукт: Equity-Sharing платформа")
    add_subtitle(slide, "Win-Win: бабушка получает уход, инвестор получает доходную недвижимость")
    
    # Diagram simulation
    x_flow = 1
    flows = [
        ("👵 Пенсионер", "Передаёт 50% доли → Получает 50% аренды (~40K/мес)"),
        ("→", ""),
        ("🏢 RentalLife", "Управление + Пансионат + AI лидген"),
        ("→", ""),
        ("💼 Инвестор", "50% доли → 35K/мес net → IRR ~95%")
    ]
    
    for title, desc in flows:
        width = 3 if desc else 1
        if desc:
            add_card(slide, Inches(x_flow), Inches(3), Inches(width), Inches(2), WHITE)
            add_text_in_box(slide, Inches(x_flow+0.2), Inches(3.2), Inches(width-0.4), Inches(0.5), title, 16, ACCENT_PRIMARY, True)
            add_text_in_box(slide, Inches(x_flow+0.2), Inches(3.8), Inches(width-0.4), Inches(1), desc, 12, TEXT_SECONDARY)
        else:
            add_text_in_box(slide, Inches(x_flow), Inches(4), Inches(1), Inches(1), "→", 30, TEXT_PRIMARY)
        x_flow += width + 0.2

    # Stats footer
    add_text_in_box(slide, Inches(1), Inches(6), Inches(10), Inches(1), "LTV/CAC: 28x  •  LTV: 9.6M  •  Payback: 10 мес", 18, TEXT_PRIMARY, True)

    # ==========================================
    # SLIDE 5: MARKET
    # ==========================================
    slide = add_slide()
    add_title(slide, "Размер рынка")
    
    # Stats
    market_stats = [
        ("TAM (все 60+)", "~10.7 трлн ₽/год"),
        ("SAM (одинокие + квартира)", "~4.4 трлн ₽/год"),
        ("SOM Year 1 (50 контрактов)", "480M ₽")
    ]
    y_m = 2.0
    for lbl, val in market_stats:
        add_text_in_box(slide, Inches(0.8), Inches(y_m), Inches(5), Inches(0.5), lbl, 16, TEXT_SECONDARY)
        add_text_in_box(slide, Inches(0.8), Inches(y_m+0.4), Inches(5), Inches(0.5), val, 24, ACCENT_PRIMARY, True)
        y_m += 1.5

    # Trend card
    add_card(slide, Inches(6), Inches(2), Inches(6.5), Inches(4), CARD_BG)
    add_text_in_box(slide, Inches(6.5), Inches(2.5), Inches(5.5), Inches(1), "Тренд: доля 60+ → 25.4% к 2030", 22, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(6.5), Inches(3.5), Inches(5.5), Inches(2), "Минздрав РФ прогнозирует рост. Нет ни одной платформенной компании — только частные сделки.\n\nТаргет: Элитный сегмент МО, квартиры 10-25M ₽", 16, TEXT_PRIMARY)

    # ==========================================
    # SLIDE 6: CLIENTS
    # ==========================================
    slide = add_slide()
    add_title(slide, "Кто наш клиент")
    
    # Pensioner Card
    add_card(slide, Inches(0.8), Inches(2), Inches(5.5), Inches(4.5), WHITE)
    add_text_in_box(slide, Inches(1), Inches(2.2), Inches(5), Inches(0.5), "👵 Получатель ренты", 20, ACCENT_PRIMARY, True)
    add_text_in_box(slide, Inches(1), Inches(2.8), Inches(5), Inches(0.5), "Одинокий пенсионер 75+, Москва/МО", 14, TEXT_PRIMARY, True)
    client_list = "• Пенсия ~25K ₽, квартира 10-25M ₽\n• Нуждается в уходе (40-65K/мес)\n• Квартира — единственный актив\n• Боится мошенников"
    add_text_in_box(slide, Inches(1), Inches(3.5), Inches(5), Inches(2), client_list, 14, TEXT_SECONDARY)
    add_text_in_box(slide, Inches(1), Inches(5.8), Inches(5), Inches(0.5), "Решение: И уход, и доход от квартиры", 14, TEXT_PRIMARY, True)

    # Investor Card
    add_card(slide, Inches(6.8), Inches(2), Inches(5.5), Inches(4.5), CARD_BG)
    add_text_in_box(slide, Inches(7), Inches(2.2), Inches(5), Inches(0.5), "💼 Инвестор", 20, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(7), Inches(2.8), Inches(5), Inches(0.5), "HNW индивид / Family Office, 35-55 лет", 14, TEXT_PRIMARY, True)
    inv_list = "• Свободный капитал от 5M ₽\n• Ищет альтернативу депозитам\n• Готов к горизонту 5-7 лет\n• Ценит прозрачность"
    add_text_in_box(slide, Inches(7), Inches(3.5), Inches(5), Inches(2), inv_list, 14, TEXT_PRIMARY)
    add_text_in_box(slide, Inches(7), Inches(5.8), Inches(5), Inches(0.5), "Решение: IRR ~95% + актив (квартира)", 14, TEXT_PRIMARY, True)

    # ==========================================
    # SLIDE 7: MOAT
    # ==========================================
    slide = add_slide()
    add_title(slide, "Конкуренты и наше отличие")
    add_subtitle(slide, "Нечестное конкурентное преимущество (MOAT)")
    
    moats = [
        ("🔗 Вертикальная интеграция", "Недвижимость + уход + финтех = 3-в-1"),
        ("🤖 AI лидогенерация", "Голосовые агенты: 300 лидов/мес, конверсия 3.3%"),
        ("🤝 Партнёрская сеть", "100+ пансионатов, юристы, нотариусы"),
        ("🛡️ Юридическая защита", "Видеофиксация, Telegram-отчёты, нотариус")
    ]
    
    x_moat = 0.8
    for title, desc in moats:
        add_card(slide, Inches(x_moat), Inches(2.5), Inches(2.8), Inches(3), WHITE)
        add_text_in_box(slide, Inches(x_moat+0.2), Inches(2.7), Inches(2.4), Inches(0.8), title, 16, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(x_moat+0.2), Inches(3.6), Inches(2.4), Inches(1.5), desc, 14, TEXT_SECONDARY)
        x_moat += 3.1

    add_text_in_box(slide, Inches(0.8), Inches(6), Inches(12), Inches(0.8), "Конкуренты: частные сделки, чёрные риелторы. RentalLife — первая платформенная компания.", 16, TEXT_PRIMARY)

    # ==========================================
    # SLIDE 8: UNIT ECONOMICS
    # ==========================================
    slide = add_slide()
    add_title(slide, "Unit Economics (1 контракт)")

    # Left col
    add_text_in_box(slide, Inches(0.8), Inches(2), Inches(5), Inches(0.5), "Ежемесячный Cash Flow", 18, TEXT_PRIMARY, True)
    ue_rows = [
        "Аренда от жильца: 80 000 ₽",
        "Бабушке (50%): −40 000 ₽",
        "Операционка: −5 000 ₽",
        "NET (RentalLife): 35 000 ₽"
    ]
    y_ue = 2.7
    for row in ue_rows:
        add_text_in_box(slide, Inches(0.8), Inches(y_ue), Inches(5), Inches(0.4), row, 16, TEXT_PRIMARY)
        y_ue += 0.6

    # Right col
    add_text_in_box(slide, Inches(6.5), Inches(2), Inches(5), Inches(0.5), "Ключевые метрики", 18, TEXT_PRIMARY, True)
    metrics = [
        "CAC: 340K ₽ (ремонт + юристы)",
        "LTV (5 лет): 9.6M ₽ (аренда + exit)",
        "LTV/CAC: 28x (benchmark: 3x)",
        "Payback: 10 мес",
        "Gross Margin: 44%",
        "IRR (5 лет): ~95%"
    ]
    y_met = 2.7
    for row in metrics:
        add_text_in_box(slide, Inches(6.5), Inches(y_met), Inches(6), Inches(0.4), row, 16, TEXT_PRIMARY)
        y_met += 0.6

    # ==========================================
    # SLIDE 9: ROADMAP
    # ==========================================
    slide = add_slide()
    add_title(slide, "Бизнес-цели на 3 года")
    
    roadmap = [
        ("Year 1: Валидация", "50 контрактов • AUM: 0.75 млрд • MRR: 1.75M"),
        ("Year 2: Масштаб", "150 контрактов • AUM: 2.25 млрд • MRR: 5.25M • Series A"),
        ("Year 3: Exit", "300 контрактов • AUM: 4.5 млрд • Валюация 5-10 млрд • IPO/M&A")
    ]
    
    x_rm = 0.8
    for year, desc in roadmap:
        add_card(slide, Inches(x_rm), Inches(2.5), Inches(3.8), Inches(3), WHITE)
        add_text_in_box(slide, Inches(x_rm+0.2), Inches(2.7), Inches(3.4), Inches(0.5), year, 18, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(x_rm+0.2), Inches(3.3), Inches(3.4), Inches(2), desc, 14, TEXT_SECONDARY)
        x_rm += 4.1

    add_text_in_box(slide, Inches(0.8), Inches(6), Inches(6), Inches(1), "52x Seed → 5yr multiple\n88M EBITDA Year 3", 20, TEXT_PRIMARY, True)

    # ==========================================
    # SLIDE 10: AI STACK
    # ==========================================
    slide = add_slide()
    add_title(slide, "AI-стек: нечестное преимущество")
    add_subtitle(slide, "Автоматизация снижает CAC и повышает качество обслуживания")
    
    ai_items = [
        ("🤖 Голосовой обзвон", "ElevenLabs + GPT-4o\n300 лидов → 10 контрактов"),
        ("📊 Риск-скоринг", "ML модель (Python)\nAccuracy 94%"),
        ("📸 Оценка квартир", "API ЦИАН + CV\nАвтоматическая оценка м²"),
        ("📱 Авто-отчёты", "GPT + Telegram Bot\nPDF для семей ежемесячно")
    ]
    
    x_ai = 0.8
    for title, desc in ai_items:
        add_card(slide, Inches(x_ai), Inches(2.5), Inches(2.8), Inches(3.5), WHITE)
        add_text_in_box(slide, Inches(x_ai+0.2), Inches(2.7), Inches(2.4), Inches(0.8), title, 16, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(x_ai+0.2), Inches(3.6), Inches(2.4), Inches(2), desc, 14, TEXT_SECONDARY)
        x_ai += 3.1

    # ==========================================
    # SLIDE 11: TRENDS
    # ==========================================
    slide = add_slide()
    add_title(slide, "Тренды: идеальный шторм")
    
    trends = [
        "👴 Старение населения\nДоля 60+ → 25.4% к 2030",
        "🏠 Рынок аренды взрывается\n+20-25% за год",
        "💰 Рента набирает обороты\nРезкий рост предложений",
        "📈 Высокая ставка ЦБ\nИпотека недоступна"
    ]
    
    x_tr = 0.8
    for item in trends:
        add_card(slide, Inches(x_tr), Inches(2.5), Inches(2.8), Inches(2), WHITE)
        add_text_in_box(slide, Inches(x_tr+0.2), Inches(2.7), Inches(2.4), Inches(1.6), item, 14, TEXT_PRIMARY)
        x_tr += 3.1

    add_card(slide, Inches(3), Inches(5), Inches(7.33), Inches(1.5), CARD_BG)
    add_text_in_box(slide, Inches(3.2), Inches(5.2), Inches(7), Inches(1), "Наш IRR ~95% >> депозит ~20% — инвесторы ищут альтернативы", 18, TEXT_PRIMARY, True)

    # ==========================================
    # SLIDE 12: TEAM
    # ==========================================
    slide = add_slide()
    add_title(slide, "Команда")
    
    team = [
        ("Founder — CEO", "9+ лет в digital-продуктах\n5+ лет в elderly care\nЭкс-Газпромбанк, OZON"),
        ("Вадим — CTO", "5+ лет в финтехе\nТакси CRM, PayPeople\n3 успешных финтех-проекта"),
        ("Advisory Board", "Демограф (Росстат)\nБанкир (экс-Сбер)\nЮрист (estate law)")
    ]
    
    x_tm = 0.8
    for title, desc in team:
        add_card(slide, Inches(x_tm), Inches(2.5), Inches(3.8), Inches(3.5), WHITE)
        add_text_in_box(slide, Inches(x_tm+0.2), Inches(2.7), Inches(3.4), Inches(0.5), title, 18, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(x_tm+0.2), Inches(3.4), Inches(3.4), Inches(2.4), desc, 14, TEXT_SECONDARY)
        x_tm += 4.1

    # ==========================================
    # SLIDE 13: RISKS
    # ==========================================
    slide = add_slide()
    add_title(slide, "Риски и митигация")
    
    risks = [
        "Долгожительство (35%): Модель 50/50: больше живёт = больше cash flow",
        "Оспаривание (20%): Видеозапись нотариуса, отчёты",
        "Ликвидность (15%): Фокус элитный сегмент МО",
        "Регуляция (10%): Прозрачность, НКО структура"
    ]
    y_r = 2.5
    for r in risks:
        add_text_in_box(slide, Inches(0.8), Inches(y_r), Inches(11), Inches(0.5), "• " + r, 18, TEXT_PRIMARY)
        y_r += 0.8

    # ==========================================
    # SLIDE 14: SEED ROUND
    # ==========================================
    slide = add_slide()
    add_title(slide, "Seed Round: 4.4M ₽")
    
    # Use of funds
    add_text_in_box(slide, Inches(0.8), Inches(2), Inches(5), Inches(0.5), "Использование средств", 18, TEXT_PRIMARY, True)
    funds = [
        "Дефицит финансирования: 2.4M (55%)",
        "Маркетинг + PR: 0.8M (18%)",
        "Юридическое оформление: 0.5M (11%)",
        "AI/Tech разработка: 0.2M (5%)"
    ]
    y_f = 2.7
    for f in funds:
        add_text_in_box(slide, Inches(0.8), Inches(y_f), Inches(5), Inches(0.4), f, 16, TEXT_PRIMARY)
        y_f += 0.6

    # Terms
    add_card(slide, Inches(6.5), Inches(2), Inches(6), Inches(4), CARD_BG)
    add_text_in_box(slide, Inches(6.8), Inches(2.2), Inches(5.4), Inches(0.5), "Условия для инвестора", 20, TEXT_PRIMARY, True)
    terms = "• Вадиму: 40% доля\n• Founder: 60% доля\n• IRR ~95% за 5 лет\n• Multiple: 52x на Seed\n• Exit: 3-5 лет (IPO / стратег)"
    add_text_in_box(slide, Inches(6.8), Inches(3), Inches(5.4), Inches(2.5), terms, 16, TEXT_PRIMARY)

    # ==========================================
    # SLIDE 15: QUESTIONS
    # ==========================================
    slide = add_slide()
    add_title(slide, "Вопросы к Клубу менторов")
    add_subtitle(slide, "Мы ищем экспертизу, а не только капитал")
    
    questions = [
        "⚖️ Юридическая структура: Оптимальный формат?",
        "🏛️ REIT регистрация: Как структурировать?",
        "🗺️ Масштабирование: Москва first или +СПб?",
        "🛡️ PR-стратегия: Как не ассоциироваться с «чёрными риелторами»?",
        "🎯 Exit стратегия: Кто покупатель?"
    ]
    
    y_q = 2.5
    for q in questions:
        add_text_in_box(slide, Inches(0.8), Inches(y_q), Inches(11), Inches(0.5), q, 18, TEXT_PRIMARY)
        y_q += 0.8

    # ==========================================
    # SLIDE 16: CTA
    # ==========================================
    slide = add_slide()
    
    # Centered Logo & Title
    add_text_in_box(slide, Inches(1), Inches(1), Inches(11.33), Inches(1), "RentalLife", 60, ACCENT_PRIMARY, True)
    textbox = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(11.33), Inches(1.5))
    p = textbox.text_frame.paragraphs[0]
    p.text = "Первая платформа, которая превращает недвижимость пожилых в доходные инвестиции"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(28)
    p.font.name = "Arial"
    p.font.color.rgb = TEXT_PRIMARY

    # Stats
    s_x = 2
    cta_stats = [
        ("35.6M", "пожилых"),
        ("~95%", "IRR"),
        ("4.4M", "Seed Round")
    ]
    for val, lbl in cta_stats:
        add_text_in_box(slide, Inches(s_x), Inches(4), Inches(2.5), Inches(0.5), val, 24, ACCENT_PRIMARY, True)
        add_text_in_box(slide, Inches(s_x), Inches(4.5), Inches(2.5), Inches(0.5), lbl, 16, TEXT_SECONDARY)
        s_x += 3.5

    # Link
    textbox = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(11.33), Inches(1))
    p = textbox.text_frame.paragraphs[0]
    p.text = "Telegram @rentallife • Февраль 2026"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.name = "Arial"
    p.font.color.rgb = ACCENT_PRIMARY

    # Save
    prs.save('/Users/asmadey/PersonalOS/RentalLife_PitchDeck.pptx')
    print("Presentation saved successfully.")

if __name__ == "__main__":
    create_presentation()
