from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime
import random


def _register_cjk_font():
    """Try common macOS Chinese fonts and fall back to Helvetica."""
    font_candidates = [
        ("PingFangSC", "/System/Library/Fonts/PingFang.ttc"),
        ("STHeiti", "/System/Library/Fonts/STHeiti Light.ttc"),
        ("HiraginoSansGB", "/System/Library/Fonts/Hiragino Sans GB.ttc"),
    ]

    for font_name, font_path in font_candidates:
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return font_name
        except Exception:
            continue

    return "Helvetica"


def create_word_pdf(filename):
    word_bank = [
        ("苹果", "apple"), ("香蕉", "banana"), ("橙子", "orange"), ("葡萄", "grape"), ("西瓜", "watermelon"),
        ("草莓", "strawberry"), ("桃子", "peach"), ("梨", "pear"), ("菠萝", "pineapple"), ("芒果", "mango"),
        ("米饭", "rice"), ("面包", "bread"), ("牛奶", "milk"), ("鸡蛋", "egg"), ("鱼", "fish"),
        ("鸡肉", "chicken"), ("牛肉", "beef"), ("猪肉", "pork"), ("汤", "soup"), ("面条", "noodles"),
        ("猫", "cat"), ("狗", "dog"), ("鸟", "bird"), ("兔子", "rabbit"), ("马", "horse"),
        ("牛", "cow"), ("羊", "sheep"), ("鸭", "duck"), ("母鸡", "hen"), ("老虎", "tiger"),
        ("狮子", "lion"), ("熊", "bear"), ("猴子", "monkey"), ("大象", "elephant"), ("熊猫", "panda"),
        ("红色", "red"), ("蓝色", "blue"), ("绿色", "green"), ("黄色", "yellow"), ("黑色", "black"),
        ("白色", "white"), ("紫色", "purple"), ("粉色", "pink"), ("棕色", "brown"), ("灰色", "gray"),
        ("太阳", "sun"), ("月亮", "moon"), ("星星", "star"), ("天空", "sky"), ("云", "cloud"),
        ("妈妈", "mother"), ("爸爸", "father"), ("哥哥", "brother"), ("姐姐", "sister"), ("爷爷", "grandfather"),
        ("奶奶", "grandmother"), ("朋友", "friend"), ("老师", "teacher"), ("学生", "student"), ("医生", "doctor"),
        ("头", "head"), ("眼睛", "eye"), ("耳朵", "ear"), ("鼻子", "nose"), ("嘴巴", "mouth"),
        ("桌子", "table"), ("椅子", "chair"), ("床", "bed"), ("门", "door"), ("窗户", "window"),
        ("书", "book"), ("钢笔", "pen"), ("铅笔", "pencil"), ("橡皮", "eraser"), ("尺子", "ruler"),
        ("书包", "schoolbag"), ("电脑", "computer"), ("手机", "phone"), ("手表", "watch"), ("钥匙", "key"),
        ("跑", "run"), ("走", "walk"), ("跳", "jump"), ("看", "look"), ("听", "listen"),
        ("说", "speak"), ("读", "read"), ("写", "write"), ("吃", "eat"), ("喝", "drink"),
        ("大", "big"), ("小", "small"), ("快", "fast"), ("慢", "slow"), ("热", "hot"),
        ("冷", "cold"), ("今天", "today"), ("明天", "tomorrow"), ("昨天", "yesterday"), ("学校", "school"),
        ("城市", "city"), ("村庄", "village"), ("国家", "country"), ("地图", "map"), ("道路", "road"),
        ("桥", "bridge"), ("河流", "river"), ("湖", "lake"), ("海洋", "ocean"), ("山", "mountain"),
        ("森林", "forest"), ("花", "flower"), ("树", "tree"), ("草", "grass"), ("叶子", "leaf"),
        ("雨", "rain"), ("雪", "snow"), ("风", "wind"), ("天气", "weather"), ("春天", "spring"),
        ("夏天", "summer"), ("秋天", "autumn"), ("冬天", "winter"), ("早晨", "morning"), ("夜晚", "night"),
        ("游泳", "swim"), ("唱歌", "sing"), ("跳舞", "dance"), ("画画", "draw"), ("学习", "study"),
        ("工作", "work"), ("睡觉", "sleep"), ("醒来", "wake"), ("打开", "open"), ("关闭", "close"),
        ("开始", "start"), ("结束", "finish"), ("买", "buy"), ("卖", "sell"), ("发送", "send"),
        ("收到", "receive"), ("帮助", "help"), ("等待", "wait"), ("寻找", "search"), ("找到", "find"),
        ("洗", "wash"), ("打扫", "clean"), ("烹饪", "cook"), ("练习", "practice"), ("准备", "prepare"),
        ("高", "tall"), ("矮", "short"), ("年轻", "young"), ("年老", "old"), ("开心", "happy"),
        ("难过", "sad"), ("容易", "easy"), ("困难", "difficult"), ("干净", "neat"), ("脏", "dirty"),
        ("安静", "quiet"), ("吵闹", "noisy"), ("明亮", "bright"), ("黑暗", "dark"), ("重要", "important"),
        ("安全", "safe"), ("危险", "dangerous"), ("正确", "correct"), ("错误", "wrong"), ("特别", "special"),
        ("便宜", "cheap"), ("昂贵", "expensive"), ("新", "new"), ("旧", "old"), ("简单", "simple"),
        ("自行车", "bicycle"), ("汽车", "car"), ("公交车", "bus"), ("火车", "train"), ("飞机", "airplane"),
        ("船", "boat"), ("机场", "airport"), ("车站", "station"), ("票", "ticket"), ("钱包", "wallet"),
        ("帽子", "hat"), ("鞋", "shoes"), ("袜子", "socks"), ("衬衫", "shirt"), ("裤子", "pants"),
        ("外套", "coat"), ("裙子", "dress"), ("雨伞", "umbrella"), ("礼物", "gift"), ("照片", "photo"),
        ("超市", "supermarket"), ("医院", "hospital"), ("公园", "park"), ("图书馆", "library"), ("餐厅", "restaurant"),
    ]

    if len(word_bank) < 100:
        raise ValueError("词库至少需要 100 组词")

    words = random.sample(word_bank, 100)

    words_ch = [ch for ch, _ in words]
    words_en = [en for _, en in words]

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    left_margin = 14 * mm
    right_margin = 14 * mm
    top_margin = 16 * mm
    bottom_margin = 14 * mm
    col_gap = 5 * mm
    col_count = 4
    row_count = 25
    per_page = row_count * col_count

    content_width = width - left_margin - right_margin
    col_width = (content_width - (col_count - 1) * col_gap) / col_count

    header_band = 24 * mm
    list_top_y = height - top_margin - header_band
    available_height = list_top_y - bottom_margin
    row_height = available_height / row_count
    rows_per_col = 25

    font_name = _register_cjk_font()
    title_size = 17
    subtitle_size = 10.5
    body_size = 10
    c.setTitle("中译英100词练习")

    # 练习页: 标题区
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(font_name, title_size)
    c.drawString(left_margin, height - top_margin - 7 * mm, "中译英单词练习（100词）")
    c.setFont(font_name, subtitle_size)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(left_margin, height - top_margin - 14 * mm, "姓名：____________    日期：____________")
    c.setStrokeColor(colors.HexColor("#D1D5DB"))
    c.setLineWidth(0.6)
    c.line(left_margin, height - top_margin - 17 * mm, width - right_margin, height - top_margin - 17 * mm)

    # 练习页: 四列框
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.5)
    for col in range(col_count):
        box_x = left_margin + col * (col_width + col_gap)
        c.roundRect(box_x, bottom_margin, col_width, available_height, 2 * mm, stroke=1, fill=0)

    c.setFont(font_name, body_size)
    c.setFillColor(colors.HexColor("#111827"))
    for i, word in enumerate(words_ch):
        page_index = i
        col = page_index // row_count
        row = page_index % row_count
        x = left_margin + col * (col_width + col_gap) + 2.2 * mm
        y = list_top_y - (row + 1) * row_height + 2.8 * mm
        label = f"{i + 1:02d}. {word}"
        c.drawString(x, y, label)
        label_w = pdfmetrics.stringWidth(label, font_name, body_size)
        line_x1 = x + label_w + 1.2 * mm
        line_x2 = left_margin + col * (col_width + col_gap) + col_width - 2.2 * mm
        c.setStrokeColor(colors.HexColor("#9CA3AF"))
        c.setLineWidth(0.4)
        if line_x2 > line_x1:
            c.line(line_x1, y - 0.8 * mm, line_x2, y - 0.8 * mm)
    if len(words_ch) != per_page:
        raise ValueError("当前版式固定一页4列共100题，请保持 100 个单词")

    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont(font_name, 9)
    c.drawRightString(width - right_margin, 8 * mm, "第 1 页 / 2")

    c.showPage()

    # 答案页: 标题区
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(font_name, title_size)
    c.drawString(left_margin, height - top_margin - 7 * mm, "中译英单词答案（100词）")
    c.setFont(font_name, subtitle_size)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(left_margin, height - top_margin - 14 * mm, "按练习页序号对应核对")
    c.setStrokeColor(colors.HexColor("#D1D5DB"))
    c.setLineWidth(0.6)
    c.line(left_margin, height - top_margin - 17 * mm, width - right_margin, height - top_margin - 17 * mm)

    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.5)
    for col in range(col_count):
        box_x = left_margin + col * (col_width + col_gap)
        c.roundRect(box_x, bottom_margin, col_width, available_height, 2 * mm, stroke=1, fill=0)

    c.setFillColor(colors.HexColor("#111827"))
    c.setFont(font_name, body_size)
    for i, (ch_word, en_word) in enumerate(zip(words_ch, words_en)):
        page_index = i
        col = page_index // row_count
        row = page_index % row_count
        x = left_margin + col * (col_width + col_gap) + 2.2 * mm
        y = list_top_y - (row + 1) * row_height + 2.8 * mm
        c.drawString(x, y, f"{i + 1:02d}. {ch_word} - {en_word}")

    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont(font_name, 9)
    c.drawRightString(width - right_margin, 8 * mm, "第 2 页 / 2")

    c.save()


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"中译英单词_{timestamp}.pdf"
create_word_pdf(output_filename)
print(f"已生成: {output_filename}")
