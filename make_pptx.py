from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
import copy

# Colors
YELLOW  = RGBColor(0xFF, 0xCD, 0x11)
DARK    = RGBColor(0x0F, 0x10, 0x13)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BLACK   = RGBColor(0x00, 0x00, 0x00)
GRAY_BG = RGBColor(0xF5, 0xF5, 0xF4)
GRAY_TX = RGBColor(0x4E, 0x49, 0x49)
DARK_CARD = RGBColor(0x1A, 0x1C, 0x20)

W = Inches(20)
H = Inches(11.25)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

blank_layout = prs.slide_layouts[6]  # blank

def add_slide(bg_color=None):
    slide = prs.slides.add_slide(blank_layout)
    if bg_color:
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
    return slide

def tb(slide, text, x, y, w, h, size=16, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
       italic=False, wrap=True):
    txb = slide.shapes.add_textbox(x, y, w, h)
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Inter"
    return txb

def rect(slide, x, y, w, h, fill, radius=Inches(0.15)):
    from pptx.util import Emu
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        x, y, w, h
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    # round corners via XML
    sp = shape.element
    prstGeom = sp.find(qn('p:spPr')).find(qn('a:prstGeom'))
    if prstGeom is None:
        from lxml import etree
        spPr = sp.find(qn('p:spPr'))
        prstGeom = etree.SubElement(spPr, qn('a:prstGeom'))
    prstGeom.set('prst', 'roundRect')
    avLst = prstGeom.find(qn('a:avLst'))
    if avLst is None:
        from lxml import etree
        avLst = etree.SubElement(prstGeom, qn('a:avLst'))
    from lxml import etree
    # clear existing
    for gd in avLst.findall(qn('a:gd')):
        avLst.remove(gd)
    gd = etree.SubElement(avLst, qn('a:gd'))
    gd.set('name', 'adj')
    gd.set('fmla', 'val 20000')
    return shape

def card(slide, x, y, w, h, bg, num_text, title_text, desc_text,
         num_color=None, title_color=WHITE, desc_color=None):
    rect(slide, x, y, w, h, bg)
    nc = num_color or (RGBColor(0x80,0x80,0x80) if bg != DARK and bg != DARK_CARD else RGBColor(0x55,0x55,0x55))
    dc = desc_color or (GRAY_TX if bg == GRAY_BG or bg == WHITE else RGBColor(0xAA,0xAA,0xAA))
    if bg == YELLOW:
        nc = RGBColor(0x66,0x55,0x00)
        title_color = BLACK
        dc = RGBColor(0x44,0x33,0x00)
    pad = Inches(0.3)
    tb(slide, num_text, x+pad, y+pad, w-2*pad, Pt(20), size=10, color=nc)
    tb(slide, title_text, x+pad, y+h-Inches(1.8), w-2*pad, Inches(0.5),
       size=18, bold=True, color=title_color)
    tb(slide, desc_text, x+pad, y+h-Inches(1.3), w-2*pad, Inches(1.2),
       size=12, color=dc, wrap=True)

def pill(slide, text, x, y, color=BLACK, bg=None, size=10):
    w = Inches(len(text)*0.09 + 0.5)
    h = Inches(0.42)
    if bg:
        r = rect(slide, x, y, w, h, bg)
    txb = slide.shapes.add_textbox(x + Inches(0.18), y + Inches(0.1),
                                   w - Inches(0.36), h - Inches(0.2))
    tf = txb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = color
    run.font.name = "Inter"
    return w

def copyright(slide, color=RGBColor(0x88,0x88,0x88)):
    tb(slide, "© 2026 WINCARS. ВСЕ ПРАВА ЗАЩИЩЕНЫ",
       W - Inches(3.5), Inches(0.4), Inches(3.3), Inches(0.3),
       size=8, color=color, align=PP_ALIGN.RIGHT)

# ─── SLIDE 01 — Cover ─────────────────────────────────────────
s = add_slide(YELLOW)
# gradient-like overlay (lighter yellow rect)
rect(slide=s, x=W//2, y=Inches(0), w=W//2, h=H, fill=RGBColor(0xFF,0xDE,0x64))
# hide the overlay behind – just use solid yellow bg and add a subtle lighter shape
tb(s, "WINCARS", Inches(0.7), Inches(0.55), Inches(2.5), Inches(0.6),
   size=30, bold=True, color=BLACK)
pill(s, "ONBOARDING", Inches(3.5), Inches(0.6), color=WHITE, bg=DARK, size=10)
pill(s, "ДЛЯ НОВЫХ СОТРУДНИКОВ", W-Inches(4.2), Inches(0.6), color=BLACK, bg=None, size=10)
tb(s, "Привет!\nДобро пожаловать\nв команду",
   Inches(0.7), Inches(2.0), Inches(9), Inches(4.5),
   size=72, bold=True, color=BLACK)
tb(s, "Этот документ — твой главный проводник по нашей атмосфере,\nправилам и внутреннему коду Wincars. Пристегни ремни, погнали!",
   Inches(0.7), Inches(6.5), Inches(8), Inches(1.2),
   size=16, color=RGBColor(0x33,0x2A,0x00), wrap=True)
# bottom strip
rect(s, Inches(0.7), Inches(8.8), W-Inches(1.4), Pt(1), BLACK)
for i, (label, val) in enumerate([
    ("КОМПАНИЯ", "Wincars Sp. z o.o."),
    ("ОСНОВАНО", "2022 год"),
    ("ГЕОГРАФИЯ", "Польша · Болгария · Румыния · Молдова · Сальвадор"),
]):
    x = Inches(0.7 + i * 6.2)
    tb(s, label, x, Inches(9.0), Inches(6), Inches(0.28), size=9, color=RGBColor(0x33,0x2A,0x00))
    tb(s, val,   x, Inches(9.35), Inches(6), Inches(0.4),  size=14, bold=True, color=BLACK)

# ─── SLIDE 02 — Table of Contents ─────────────────────────────
s = add_slide(WHITE)
tb(s, "Содержание", Inches(0.7), Inches(6.5), Inches(6), Inches(1.2),
   size=64, bold=True, color=BLACK)
tb(s, "онбординга", Inches(0.7), Inches(7.7), Inches(6), Inches(1.2),
   size=64, bold=True, color=YELLOW)
# dark panel
rect(s, Inches(8.5), Inches(0.6), Inches(11.1), Inches(10.0), DARK)
sections = [
    ("SECTION 1", "Кто мы такие", "(01)"),
    ("SECTION 2", "Ценности Wincars", "(02)"),
    ("SECTION 3", "Условия и соцпакет", "(03)"),
    ("SECTION 4", "Первый месяц: Тест-драйв", "(04)"),
    ("SECTION 5", "Ритм, дисциплина и вайб", "(05)"),
    ("SECTION 6", "Команда и структура", "(06)"),
]
for i, (sec, name, num) in enumerate(sections):
    y = Inches(1.1 + i * 1.5)
    pill(s, sec, Inches(9.0), y + Inches(0.1), color=WHITE, bg=None, size=9)
    tb(s, name, Inches(11.5), y + Inches(0.1), Inches(6.5), Inches(0.55),
       size=17, bold=True, color=WHITE)
    tb(s, num, Inches(18.8), y + Inches(0.15), Inches(0.8), Inches(0.4),
       size=13, color=RGBColor(0x66,0x66,0x66), align=PP_ALIGN.RIGHT)
    if i < 5:
        rect(s, Inches(9.0), y + Inches(0.7), Inches(10.2), Pt(1),
             RGBColor(0x33,0x33,0x33))

# ─── SLIDE 03 — Section 1 ─────────────────────────────────────
def section_slide(num_str, pill_label, heading, desc):
    s = add_slide(DARK)
    pill(s, pill_label, Inches(0.7), Inches(0.55), color=WHITE, bg=None, size=10)
    copyright(s, RGBColor(0x55,0x55,0x55))
    tb(s, num_str, W - Inches(5.5), Inches(0.2), Inches(5), Inches(4.5),
       size=240, bold=True, color=WHITE)
    tb(s, heading, Inches(0.7), Inches(5.8), Inches(9), Inches(4),
       size=72, bold=True, color=WHITE)
    tb(s, desc, W - Inches(4.5), Inches(7.8), Inches(4.0), Inches(2.8),
       size=14, color=RGBColor(0xAA,0xAA,0xAA), wrap=True)
    return s

section_slide("01", "SECTION 1", "Кто мы\nтакие →",
    "Wincars — международная компания, основанная в 2022 году. Мы импортируем автомобили из США, Канады и Южной Кореи и строим команду, которой гордимся.")

# ─── SLIDE 04 — About Company ─────────────────────────────────
s = add_slide(WHITE)
pill(s, "О КОМПАНИИ", Inches(0.7), Inches(0.55), color=BLACK, size=10)
copyright(s)
tb(s, "Мы меняем правила игры\nна вторичном рынке",
   Inches(0.7), Inches(1.5), Inches(8.5), Inches(2.5),
   size=38, bold=True, color=YELLOW)
tb(s, "Wincars — международная компания, основанная в 2022 году, которая занимается импортом автомобилей из США, Канады и Южной Кореи. Мы активно растём и развиваемся, открывая филиалы по всему миру.",
   Inches(0.7), Inches(4.2), Inches(8.5), Inches(1.5),
   size=13, color=GRAY_TX, wrap=True)
tb(s, "Наша цель — стереть границу между покупкой б/у авто и выездом из премиального автосалона, окружая каждого клиента безупречным сервисом и заботой.",
   Inches(0.7), Inches(5.8), Inches(8.5), Inches(1.5),
   size=13, color=GRAY_TX, wrap=True)
stats = [
    (GRAY_BG, "2022", "год основания"),
    (GRAY_BG, "5 стран", "с филиалами"),
    (GRAY_BG, "3 офиса", "в Варшаве"),
    (YELLOW,  "USA / CA / KR", "источники авто"),
]
for i, (bg, val, lbl) in enumerate(stats):
    y = Inches(0.7 + i * 2.55)
    rect(s, Inches(10.2), y, Inches(9.4), Inches(2.3), bg)
    tc = BLACK if bg == YELLOW else BLACK
    tb(s, val, Inches(13.5), y + Inches(0.5), Inches(5.5), Inches(1.0),
       size=36, bold=True, color=tc)
    tb(s, lbl, Inches(13.5), y + Inches(1.5), Inches(5.5), Inches(0.5),
       size=13, color=RGBColor(0x55,0x55,0x55) if bg != YELLOW else RGBColor(0x33,0x22,0x00))

# ─── SLIDE 05 — Section 2 ─────────────────────────────────────
section_slide("02", "SECTION 2", "Ценности\nWincars →",
    "Мы не просто доставляем автомобили. Мы создаём компанию, которой гордимся — и вот столпы, на которых держится всё, что мы делаем.")

# ─── SLIDE 06 — Values ────────────────────────────────────────
s = add_slide(WHITE)
pill(s, "НАША ДНК", Inches(0.7), Inches(0.55), color=BLACK, size=10)
copyright(s)
tb(s, "Пять принципов, на которых держится Wincars",
   Inches(0.7), Inches(1.3), Inches(16), Inches(0.7),
   size=28, bold=True, color=BLACK)

cw = Inches(6.1)
ch = Inches(3.5)
gap = Inches(0.15)
cx = Inches(0.7)
cy = Inches(2.3)
values = [
    (DARK, "(01) ↗", "Открытость",
     "Работаем честно и «в белую». Все условия и тарифы абсолютно прозрачны. Платим налоги и выполняем обязательства."),
    (GRAY_BG, "(02) ↗", "Постоянное развитие",
     "Wincars всегда в движении. Внедряем новые решения, учимся у лучших и поддерживаем тех, кто предлагает и пробует."),
    (GRAY_BG, "(03) ↗", "Клиент в центре",
     "Создаём сервис, который хочется рекомендовать друзьям. Думаем о деталях и стремимся превзойти ожидания."),
]
for i, (bg, num, title, desc) in enumerate(values):
    card(s, cx + i*(cw+gap), cy, cw, ch, bg, num, title, desc)

# bottom row — wider cards
bottom_values = [
    (YELLOW, "(04)", "Командный дух",
     "У каждого своя зона ответственности, но за спиной всегда команда, готовая помочь. Ценим умение играть вместе."),
    (DARK, "(05) ↗", "Проактивность и креативность",
     "Мы не ждём, пока мир изменится — мы меняем его сами. Видишь, как сделать лучше — предлагай и создавай!"),
]
bw = [Inches(9.15), Inches(9.45)]
for i, (bg, num, title, desc) in enumerate(bottom_values):
    x = cx if i == 0 else cx + bw[0] + gap
    card(s, x, cy + ch + gap, bw[i], ch, bg, num, title, desc)

# ─── SLIDE 07 — Section 3 ─────────────────────────────────────
section_slide("03", "SECTION 3", "Условия\nи соцпакет →",
    "Заботимся о том, чтобы тебе было максимально комфортно: официальное оформление, оплачиваемый отпуск, полное техническое обеспечение и прозрачная мотивация.")

# ─── SLIDE 08 — Conditions ────────────────────────────────────
s = add_slide(WHITE)
pill(s, "ТВОИ УСЛОВИЯ", Inches(0.7), Inches(0.55), color=BLACK, size=10)
copyright(s)
tb(s, "Комфорт, стабильность и забота",
   Inches(0.7), Inches(1.3), Inches(14), Inches(0.7),
   size=28, bold=True, color=BLACK)

half_w = Inches(9.7)
row_h  = Inches(3.9)
row2_h = Inches(3.6)
gap = Inches(0.15)
top_y = Inches(2.3)
bot_y = top_y + row_h + gap

# top 2 big cards
card(s, Inches(0.7), top_y, half_w, row_h, GRAY_BG,
     "(01) ↘", "Защищённость и стабильность",
     "Официальное оформление, полностью оплачиваемый отпуск и больничный. Отпуск — это святое, мы всегда даём отдохнуть.")
card(s, Inches(0.7)+half_w+gap, top_y, half_w, row_h, GRAY_BG,
     "(02) ↘", "Полное обеспечение",
     "Предоставляем весь необходимый инструмент — корпоративный компьютер, мобильный телефон, а также стильный фирменный мерч компании.")

# bottom 4 small cards
small_w = Inches(4.7)
bot_cards = [
    (YELLOW,     "(04) ↗", "Локация — 3 офиса в Варшаве",
     "Wola al. Solidarności 163; Mokotów Fort Piłsudskiego 26; Mokotów Fort Piłsudskiego 2."),
    (DARK, "(04) ↗", "График работы",
     "Понедельник – пятница, с 10:00 до 18:00. Будь готов, что клиенты могут звонить до и после 18:00."),
    (DARK, "(05) ↗", "Забота в офисе",
     "Вкусный кофе, чай и сладости всегда в твоём распоряжении."),
    (DARK, "(06) ↗", "Система мотивации",
     "Прозрачная система мотивации и дополнительные бонусы за отличные результаты."),
]
for i, (bg, num, title, desc) in enumerate(bot_cards):
    card(s, Inches(0.7) + i*(small_w+gap), bot_y, small_w, row2_h, bg, num, title, desc)

# ─── SLIDE 09 — Section 4 ─────────────────────────────────────
section_slide("04", "SECTION 4", "Первый месяц:\nтест-драйв →",
    "Испытательный срок длится 1 месяц — время, чтобы мы присмотрелись друг к другу, а ты понял, что Wincars — это твоё место силы.")

# ─── SLIDE 10 — Test Drive Details ────────────────────────────
s = add_slide(WHITE)
pill(s, "ИСПЫТАТЕЛЬНЫЙ СРОК", Inches(0.7), Inches(0.55), color=BLACK, size=10)
copyright(s)
# giant faded "1"
tb(s, "1", Inches(0.5), Inches(0.8), Inches(2.5), Inches(3.5),
   size=220, bold=True, color=RGBColor(0xEE,0xEE,0xEE))
tb(s, "МЕСЯЦ — ТВОЙ ТЕСТ-ДРАЙВ",
   Inches(2.8), Inches(2.6), Inches(8), Inches(0.6),
   size=20, bold=True, color=BLACK)
col_w = Inches(6.1)
col_h = Inches(6.5)
col_y = Inches(4.0)
# Col 1 — dark
rect(s, Inches(0.7), col_y, col_w, col_h, RGBColor(0x18,0x14,0x0A))
tb(s, "🏎", Inches(0.7)+Inches(2.5), col_y+Inches(2), Inches(1.5), Inches(1.5), size=60)
tb(s, "(01)", Inches(1.0), col_y+Inches(0.3), col_w-Inches(0.6), Inches(0.4),
   size=11, color=RGBColor(0x80,0x70,0x30))
tb(s, "Тест в деле", Inches(1.0), col_y+col_h-Inches(0.8), col_w-Inches(0.6), Inches(0.6),
   size=17, bold=True, color=WHITE)
# Col 2 — yellow
rect(s, Inches(0.7)+col_w+Inches(0.15), col_y, col_w, col_h, YELLOW)
tb(s, "(02)", Inches(0.7)+col_w+Inches(0.45), col_y+Inches(0.3), col_w-Inches(0.6), Inches(0.4),
   size=11, color=RGBColor(0x66,0x55,0x00))
tb(s, "Первые две недели —\nобучение",
   Inches(0.7)+col_w+Inches(0.45), col_y+col_h-Inches(2.2), col_w-Inches(0.6), Inches(1.0),
   size=20, bold=True, color=BLACK)
tb(s, "Время активного погружения. Ты будешь плотно учиться у коллег и получишь нашу фирменную методичку — выжимку важных знаний, процессов и лайфхаков.",
   Inches(0.7)+col_w+Inches(0.45), col_y+col_h-Inches(1.2), col_w-Inches(0.6), Inches(1.0),
   size=12, color=RGBColor(0x44,0x33,0x00), wrap=True)
# Col 3 — dark
rect(s, Inches(0.7)+2*(col_w+Inches(0.15)), col_y, col_w, col_h, DARK)
tb(s, "(03)", Inches(0.7)+2*(col_w+Inches(0.15))+Inches(0.3), col_y+Inches(0.3),
   col_w-Inches(0.6), Inches(0.4), size=11, color=RGBColor(0x55,0x55,0x55))
tb(s, "Юридическая безопасность — NDA",
   Inches(0.7)+2*(col_w+Inches(0.15))+Inches(0.3), col_y+col_h-Inches(2.2),
   col_w-Inches(0.6), Inches(1.0), size=20, bold=True, color=WHITE)
tb(s, "После успешного прохождения испытательного срока ты получишь на подпись документ о неразглашении (NDA). Так мы юридически защищаем коммерческие данные компании.",
   Inches(0.7)+2*(col_w+Inches(0.15))+Inches(0.3), col_y+col_h-Inches(1.2),
   col_w-Inches(0.6), Inches(1.0), size=12, color=RGBColor(0xAA,0xAA,0xAA), wrap=True)

# ─── SLIDE 11 — Section 5 ─────────────────────────────────────
section_slide("05", "SECTION 5", "Ритм,\nдисциплина\nи вайб →",
    "Чтобы вся система Wincars работала как швейцарские часы, мы придерживаемся простых правил — и умеем отдыхать на максималках.")

# ─── SLIDE 12 — Rhythm & Vibe ─────────────────────────────────
s = add_slide(DARK)
pill(s, "РИТМ И КОРПОРАТИВНЫЙ ВАЙБ", Inches(0.7), Inches(0.55), color=WHITE, size=10)
copyright(s, RGBColor(0x55,0x55,0x55))
tb(s, "Работаем чётко. Отдыхаем на полную.",
   Inches(0.7), Inches(1.3), Inches(16), Inches(0.7),
   size=28, bold=True, color=WHITE)
rw = Inches(6.1)
rh = Inches(3.6)
gap = Inches(0.15)
ry = Inches(2.3)
rhythm = [
    (YELLOW,     "(01) ↗", "Пунктуальность",
     "Опоздания без предупреждения лидера заранее — недопустимы. Мы глубоко ценим время друг друга."),
    (DARK_CARD, "(02) ↗", "Старт дня",
     "Каждое утро начинается с общего сбора команды: планёрка и обязательная зарядка — заряжаем тело и мозг."),
    (DARK_CARD, "(03) ↗", "Перезагрузка в обед",
     "Настольный теннис и PlayStation прямо в офисе. Присоединяйся к баттлам!"),
]
for i, (bg, num, title, desc) in enumerate(rhythm):
    card(s, Inches(0.7)+i*(rw+gap), ry, rw, rh, bg, num, title, desc)
# bottom row
bot_rhythm = [
    (DARK_CARD, "(04) ↗", "Питание",
     "Когда вся команда выполняет недельный план — бесплатные обеды за счёт компании."),
    (YELLOW,    "(05) ↗", "Развлечения",
     "За крутые результаты — дрифт, пейнтбол, барбекю, поездки на Мазуры или в Закопане, посещение выставок и событий."),
]
bw2 = [Inches(6.1), Inches(12.55)]
for i, (bg, num, title, desc) in enumerate(bot_rhythm):
    x = Inches(0.7) if i == 0 else Inches(0.7)+bw2[0]+gap
    card(s, x, ry+rh+gap, bw2[i], rh, bg, num, title, desc)

# ─── SLIDE 13 — Section 6 ─────────────────────────────────────
section_slide("06", "SECTION 6", "Команда\nи порядок →",
    "В Wincars нет глухих стен — мы все общаемся на «ты». А ещё наш офис — это наш второй дом, поэтому порядок и чистота важны для каждого из нас.")

# ─── SLIDE 14 — Team ──────────────────────────────────────────
s = add_slide(WHITE)
pill(s, "КТО ЕСТЬ КТО", Inches(0.7), Inches(0.55), color=BLACK, size=10)
copyright(s)
tb(s, "Люди, с которыми ты будешь постоянно пересекаться",
   Inches(0.7), Inches(1.3), Inches(16), Inches(0.7),
   size=24, bold=True, color=YELLOW)

tw = Inches(4.45)
th = Inches(3.9)
gap = Inches(0.15)
ty = Inches(2.3)
team = [
    (GRAY_BG, "👤  Твой Лидер",
     "Главный ментор, наставник и первый человек, к которому идти с любым вопросом."),
    (GRAY_BG, "👤  Ваня — CEO",
     "Руководитель компании, определяющий глобальную стратегию развития Wincars и подписывающий ключевые документы."),
    (GRAY_BG, "👤  Женя — маркетинг-директор",
     "Отвечает за стратегию бренда, имидж компании, рекламу и привлечение клиентов."),
    (GRAY_BG, "👤  Лиза — SMM",
     "Ведёт социальные сети компании, создаёт яркий контент и общается с аудиторией бренда."),
    (DARK,    "👤  Дима — афтер-сейл",
     "Заботится о клиентах после сделки, решает спорные моменты и собирает отзывы о работе."),
    (DARK,    "👥  Команда менеджеров по продажам",
     "Твои дружелюбные коллеги, всегда готовые подсказать по рабочим процессам и офисному быту."),
]
for i, (bg, name, desc) in enumerate(team):
    col = i % 3
    row = i // 3
    x = Inches(0.7) + col*(tw+gap)
    y = ty + row*(th+gap)
    rect(s, x, y, tw, th, bg)
    tc = WHITE if bg == DARK else BLACK
    dc = RGBColor(0xAA,0xAA,0xAA) if bg == DARK else GRAY_TX
    tb(s, name, x+Inches(0.3), y+Inches(0.4), tw-Inches(0.6), Inches(0.7),
       size=16, bold=True, color=tc)
    tb(s, desc, x+Inches(0.3), y+Inches(1.3), tw-Inches(0.6), Inches(2.3),
       size=12, color=dc, wrap=True)
# yellow panel
yp_x = Inches(0.7) + 3*(tw+gap)
rect(s, yp_x, ty, Inches(5.45), 2*th+gap, YELLOW)
tb(s, "Чистота и уважение", yp_x+Inches(0.3), ty+Inches(0.3), Inches(4.8), Inches(0.7),
   size=20, bold=True, color=BLACK)
for j, (title, desc) in enumerate([
    ("Бережливость", "Аккуратно относимся к вещам компании — от рабочего стола до общих зон."),
    ("Чистота", "Есть очередь на дежурство в офисе, но каждый поддерживает порядок на своём уровне."),
    ("Библиотека", "Крутая внутренняя библиотека для развития. Не держи книгу дольше недели — она нужна другим."),
]):
    yy = ty + Inches(1.2) + j*Inches(2.3)
    tb(s, title, yp_x+Inches(0.3), yy, Inches(4.8), Inches(0.45),
       size=15, bold=True, color=BLACK)
    tb(s, desc, yp_x+Inches(0.3), yy+Inches(0.5), Inches(4.8), Inches(1.0),
       size=12, color=RGBColor(0x33,0x2A,0x00), wrap=True)

# ─── SLIDE 15 — Ending ────────────────────────────────────────
s = add_slide(YELLOW)
rect(s, W//2, Inches(0), W//2, H, RGBColor(0xFF,0xDE,0x64))
tb(s, "WINCARS", Inches(0.7), Inches(0.55), Inches(2.5), Inches(0.6),
   size=30, bold=True, color=BLACK)
pill(s, "ONBOARDING", Inches(3.5), Inches(0.6), color=WHITE, bg=DARK, size=10)
pill(s, "ДОБРО ПОЖАЛОВАТЬ НА БОРТ", W-Inches(5.0), Inches(0.6), color=BLACK, bg=None, size=10)
tb(s, "Ты готов?",
   Inches(1), Inches(3.5), W-Inches(2), Inches(3.5),
   size=108, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
tb(s, "Мы верим, что у тебя всё получится, и ты быстро станешь своим.\nДобро пожаловать на борт Wincars — погнали!",
   Inches(2), Inches(7.2), W-Inches(4), Inches(1.5),
   size=18, color=RGBColor(0x33,0x2A,0x00), align=PP_ALIGN.CENTER, wrap=True)
tb(s, "© 2026 WINCARS. ВСЕ ПРАВА ЗАЩИЩЕНЫ",
   Inches(0.7), H-Inches(0.6), Inches(5), Inches(0.4),
   size=9, color=RGBColor(0x55,0x44,0x00))

# ─── Save ─────────────────────────────────────────────────────
import os
os.makedirs("/home/user/Wincars/presentation", exist_ok=True)
prs.save("/home/user/Wincars/presentation/wincars_onboarding.pptx")
print("Saved!")
