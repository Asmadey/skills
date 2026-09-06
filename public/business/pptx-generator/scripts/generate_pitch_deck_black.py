from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- THEME CONFIGURATION (Black Theme) ---
# From Brand/black.md
BG_COLOR = RGBColor(15, 23, 42)         # #0F172A (Dark Navy)
TEXT_PRIMARY = RGBColor(249, 250, 251)  # #F9FAFB
TEXT_SECONDARY = RGBColor(209, 213, 219)# #D1D5DB
TEXT_ACCENT = RGBColor(129, 140, 248)   # #818CF8 (Primary Purple/Indigo)
PRICE_COLOR = RGBColor(255, 255, 255)   # #FFFFFF

# Card Colors (Simulated Gradients)
CARD_BG_BASIC = RGBColor(30, 41, 59)    # #1E293B (Dark Blue/Gray)
CARD_BG_PRO = RGBColor(59, 130, 246)    # #3B82F6 (Blue - for highlights)
CARD_BORDER = RGBColor(255, 255, 255)   # Border (will use transparency if possible, else light gray)
CARD_BORDER_COLOR = RGBColor(55, 65, 81) # #374151 (Dark Gray for discrete borders)

FONT_HEAD = "Inter"
FONT_BODY = "Inter"

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

    def add_title(slide, text, font_size=48, top=Inches(0.5)):
        textbox = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.73), Inches(1))
        tf = textbox.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.name = FONT_HEAD
        p.font.bold = True
        p.font.color.rgb = TEXT_PRIMARY
        p.alignment = PP_ALIGN.CENTER
        return p

    def add_subtitle(slide, text, top=Inches(1.3)):
        textbox = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.73), Inches(0.5))
        tf = textbox.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(16)
        p.font.name = FONT_BODY
        p.font.color.rgb = TEXT_SECONDARY
        p.alignment = PP_ALIGN.CENTER
        return p

    def add_card(slide, left, top, width, height, color=CARD_BG_BASIC):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = CARD_BORDER_COLOR
        shape.line.width = Pt(1) 
        # shape.shadow... (PPTX python lib support for shadows is partial/complex)
        return shape

    def add_text_in_box(slide, left, top, width, height, text, size=16, color=TEXT_PRIMARY, bold=False, align=PP_ALIGN.LEFT):
        textbox = slide.shapes.add_textbox(left, top, width, height)
        tf = textbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.name = FONT_BODY
        p.font.color.rgb = color
        p.font.bold = bold
        p.alignment = align
        return tf

    # ==========================================
    # SLIDE 1: TITLE
    # ==========================================
    slide = add_slide()
    
    # Logo / Title
    add_text_in_box(slide, Inches(0.8), Inches(2.5), Inches(11.73), Inches(1), "RentalLife", 60, TEXT_ACCENT, True, PP_ALIGN.CENTER)
    
    # Subtitle
    add_text_in_box(slide, Inches(0.8), Inches(3.8), Inches(11.73), Inches(1), "Превращаем квартиры пенсионеров в доходный портфель", 32, TEXT_PRIMARY, True, PP_ALIGN.CENTER)
    
    add_text_in_box(slide, Inches(0.8), Inches(5.0), Inches(11.73), Inches(1), "Платформа пожизненной ренты с equity-sharing моделью", 20, TEXT_SECONDARY, False, PP_ALIGN.CENTER)
    
    # Highlights / Tags (Simulating Pills)
    y_p = 6.0
    x_p = 3.5
    for tag in ["Seed Round: 4.4M ₽", "IRR 95%", "Market: 10T ₽"]:
        shape = add_card(slide, Inches(x_p), Inches(y_p), Inches(2.5), Inches(0.6), CARD_BG_BASIC)
        shape.adjustments[0] = 1 # Full round (pill)
        add_text_in_box(slide, Inches(x_p), Inches(y_p+0.1), Inches(2.5), Inches(0.4), tag, 14, TEXT_ACCENT, True, PP_ALIGN.CENTER)
        x_p += 2.8

    # ==========================================
    # SLIDE 2: HISTORY
    # ==========================================
    slide = add_slide()
    add_title(slide, "История бизнеса")
    add_subtitle(slide, "Выверенная стратегия с 2019 года")
    
    # Timeline Cards
    y = 2.5
    events = [
        ("2019-2022", "Исследование", "5+ лет expertise в elderly care. Анализ рынков ЕС."),
        ("2023", "Валидация", "Юридическая модель. 100+ лидов. Product-Market Fit."),
        ("2024", "Пилот", "3 контракта. MVP. Первые выплаты. Конверсия 3.3%."),
        ("2025-2026", "Масштаб", "Seed Round. AI Agents. 100 контрактов.")
    ]
    
    x = 0.8
    for year, title, desc in events:
        add_card(slide, Inches(x), Inches(y), Inches(2.8), Inches(3.5), CARD_BG_BASIC)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+0.2), Inches(2.4), Inches(0.5), year, 14, TEXT_ACCENT, True)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+0.6), Inches(2.4), Inches(0.5), title, 18, TEXT_PRIMARY, True)
        add_text_in_box(slide, Inches(x+0.2), Inches(y+1.2), Inches(2.4), Inches(1.5), desc, 14, TEXT_SECONDARY)
        x += 3.1

    # ==========================================
    # SLIDE 3: PROBLEM
    # ==========================================
    slide = add_slide()
    add_title(slide, "Проблема")
    add_subtitle(slide, "Кризис достойной старости")
    
    # Left: Stats
    x_left = 1.0
    y_stat = 2.5
    stats = [
        ("35.6М", "человек 60+"),
        ("~20К", "пенсия"),
        ("-40К", "дефицит/мес")
    ]
    for val, lbl in stats:
        sh = add_card(slide, Inches(x_left), Inches(y_stat), Inches(3), Inches(1.2), CARD_BG_BASIC)
        add_text_in_box(slide, Inches(x_left), Inches(y_stat+0.1), Inches(3), Inches(0.5), val, 24, PRICE_COLOR, True, PP_ALIGN.CENTER)
        add_text_in_box(slide, Inches(x_left), Inches(y_stat+0.6), Inches(3), Inches(0.4), lbl, 14, TEXT_SECONDARY, False, PP_ALIGN.CENTER)
        y_stat += 1.5

    # Right: Insight
    add_card(slide, Inches(5), Inches(2.5), Inches(7.5), Inches(4.2), CARD_BG_BASIC)
    add_text_in_box(slide, Inches(5.5), Inches(3.0), Inches(6.5), Inches(1), "Парадокс: 'Богатство в бетоне'", 28, TEXT_PRIMARY, True)
    add_text_in_box(slide, Inches(5.5), Inches(4.2), Inches(6.5), Inches(2), "80% пенсионеров владеют квартирой (15М+ ₽), но живут в нищете.\n\nПродать нельзя - жить негде.\nСдавать нельзя - жить негде.\n\nРента — единственный выход.", 18, TEXT_SECONDARY)

    # ==========================================
    # SLIDE 4: SOLUTION
    # ==========================================
    slide = add_slide()
    add_title(slide, "Решение: Equity-Sharing")
    add_subtitle(slide, "Win-Win модель")

    # Flow Diagram
    x_flow = 1.0
    y_flow = 3.0
    
    # 1. Pensioner
    add_card(slide, Inches(x_flow), Inches(y_flow), Inches(3), Inches(3), CARD_BG_BASIC)
    add_text_in_box(slide, Inches(x_flow), Inches(y_flow+0.2), Inches(3), Inches(0.5), "👵 Пенсионер", 20, TEXT_PRIMARY, True, PP_ALIGN.CENTER)
    add_text_in_box(slide, Inches(x_flow+0.2), Inches(y_flow+1), Inches(2.6), Inches(1.5), "Продает 50% доли\nПолучает +40К/мес\nОстается жить дома", 14, TEXT_SECONDARY, False, PP_ALIGN.CENTER)
    
    x_flow += 3.2
    add_text_in_box(slide, Inches(x_flow), Inches(y_flow+1), Inches(0.5), Inches(0.5), "→", 24, TEXT_ACCENT, True)
    x_flow += 0.8
    
    # 2. Platform
    add_card(slide, Inches(x_flow), Inches(y_flow), Inches(3), Inches(3), CARD_BG_PRO) # Highlight
    add_text_in_box(slide, Inches(x_flow), Inches(y_flow+0.2), Inches(3), Inches(0.5), "🏢 RentalLife", 20, PRICE_COLOR, True, PP_ALIGN.CENTER)
    add_text_in_box(slide, Inches(x_flow+0.2), Inches(y_flow+1), Inches(2.6), Inches(1.5), "Организует уход\nУправляет активом\nГарант сделки", 14, RGBColor(220, 230, 255), False, PP_ALIGN.CENTER)

    x_flow += 3.2
    add_text_in_box(slide, Inches(x_flow), Inches(y_flow+1), Inches(0.5), Inches(0.5), "→", 24, TEXT_ACCENT, True)
    x_flow += 0.8
    
    # 3. Investor
    add_card(slide, Inches(x_flow), Inches(y_flow), Inches(3), Inches(3), CARD_BG_BASIC)
    add_text_in_box(slide, Inches(x_flow), Inches(y_flow+0.2), Inches(3), Inches(0.5), "💼 Инвестор", 20, TEXT_PRIMARY, True, PP_ALIGN.CENTER)
    add_text_in_box(slide, Inches(x_flow+0.2), Inches(y_flow+1), Inches(2.6), Inches(1.5), "Покупает 50% дисконт\nДоходность 95%\nБезопасный актив", 14, TEXT_SECONDARY, False, PP_ALIGN.CENTER)

    # ==========================================
    # SLIDE 5: MARKET
    # ==========================================
    slide = add_slide()
    add_title(slide, "Рынок")
    add_subtitle(slide, "Огромный неосвоенный океан")
    
    # Stats Grid
    grid = [
        ("TAM", "10.7 Трлн ₽", "Все пенсионеры с жильем"),
        ("SAM", "4.4 Трлн ₽", "Одинокие в городах-миллионниках"),
        ("SOM", "480 Млн ₽", "Цель на 1 год (Москва)")
    ]
    
    x_g = 1.0
    for lbl, val, desc in grid:
        add_card(slide, Inches(x_g), Inches(2.5), Inches(3.5), Inches(3), CARD_BG_BASIC)
        add_text_in_box(slide, Inches(x_g), Inches(2.8), Inches(3.5), Inches(0.5), lbl, 18, TEXT_SECONDARY, True, PP_ALIGN.CENTER)
        add_text_in_box(slide, Inches(x_g), Inches(3.4), Inches(3.5), Inches(0.8), val, 32, PRICE_COLOR, True, PP_ALIGN.CENTER)
        add_text_in_box(slide, Inches(x_g), Inches(4.5), Inches(3.5), Inches(0.8), desc, 14, TEXT_SECONDARY, False, PP_ALIGN.CENTER)
        x_g += 3.8

    # ==========================================
    # SLIDE 6: AI ADVANTAGE
    # ==========================================
    slide = add_slide()
    add_title(slide, "Technology Stack")
    add_subtitle(slide, "AI drastically reduces CAC")
    
    techs = [
        ("Voice AI Agents", "ElevenLabs + GPT-4o для обзвона базы. Стоимость минуты: 5₽."),
        ("Scoring ML", "Автоматическая оценка рисков объекта и здоровья рентополучателя."),
        ("Auto-Reporting", "Генерация отчетов для родственников и опеки.")
    ]
    
    y_t = 2.5
    for title, desc in techs:
        add_card(slide, Inches(2), Inches(y_t), Inches(9.33), Inches(1.2), CARD_BG_BASIC)
        add_text_in_box(slide, Inches(2.2), Inches(y_t+0.1), Inches(9), Inches(0.5), title, 18, TEXT_ACCENT, True)
        add_text_in_box(slide, Inches(2.2), Inches(y_t+0.6), Inches(9), Inches(0.5), desc, 14, TEXT_SECONDARY)
        y_t += 1.5

    # ==========================================
    # SLIDE 7: ASK
    # ==========================================
    slide = add_slide()
    add_title(slide, "Investment Opportunity")
    add_subtitle(slide, "Seed Round Open")
    
    # Big Numbers
    add_card(slide, Inches(3), Inches(2.5), Inches(7.33), Inches(3), CARD_BG_BASIC)
    
    add_text_in_box(slide, Inches(3), Inches(2.8), Inches(7.33), Inches(1), "4.4M ₽", 60, PRICE_COLOR, True, PP_ALIGN.CENTER)
    add_text_in_box(slide, Inches(3), Inches(4.0), Inches(7.33), Inches(0.5), "Smart Money / Angel Round", 20, TEXT_PRIMARY, True, PP_ALIGN.CENTER)
    
    # Bottom details
    details = "Valuation: Cap 50M • Instrument: SAFE / Convertible • Use of funds: Marketing & Tech"
    add_text_in_box(slide, Inches(1), Inches(6.0), Inches(11.33), Inches(1), details, 16, TEXT_SECONDARY, False, PP_ALIGN.CENTER)

    # Save
    prs.save('/Users/asmadey/PersonalOS/RentalLife_PitchDeck_Black.pptx')
    print("Black Theme Presentation saved successfully: /Users/asmadey/PersonalOS/RentalLife_PitchDeck_Black.pptx")

if __name__ == "__main__":
    create_presentation()
