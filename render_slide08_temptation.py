import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_temptation_slide():
    w, h = 1536, 864 # 真實 16:9
    base_img = Image.new("RGBA", (w, h), (8, 14, 24, 255)) # 極致深石板夜色底

    # 1. 照片圖層與陰影圖層
    cards_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cards_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_cards = ImageDraw.Draw(cards_layer)
    draw_cshadow = ImageDraw.Draw(cards_shadow)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_tag = ImageFont.truetype(font_path, 18)
    font_caption = ImageFont.truetype(font_path, 16)
    font_sub_caption = ImageFont.truetype(font_path, 14)

    p1 = "generated/food_temptation_shrimp_feast.jpg"
    p2 = "generated/food_temptation_chicken_soup.jpg"
    p3 = "generated/food_temptation_brownie_dessert.jpg"

    # 頂部紅色警示膠囊（純文字，絕無特殊 emoji）
    tag_x, tag_y = 870, 75
    tag_w, tag_h = 596, 38
    draw_cshadow.rounded_rectangle([(tag_x - 3, tag_y - 3), (tag_x + tag_w + 3, tag_y + tag_h + 3)], radius=10, fill=(0, 0, 0, 160))
    draw_cards.rounded_rectangle([(tag_x, tag_y), (tag_x + tag_w, tag_y + tag_h)], radius=8, fill=(220, 38, 38, 220), outline=(248, 113, 113, 240), width=1)
    draw_cards.text((tag_x + 20, tag_y + 9), "【誘惑實錄】朋友聚餐吃大餐 ｜ 健管嚴格忌口", font=font_tag, fill=(255, 255, 255, 255))

    # 輔助函式：裁切並繪製圓角卡片
    def place_food_card(img_path, cx, cy, cw, ch, title, subtitle=None):
        if not os.path.exists(img_path):
            return
        raw = Image.open(img_path).convert("RGBA")
        rw, rh = raw.size
        scale = max(cw / rw, ch / rh)
        nw, nh = int(rw * scale), int(rh * scale)
        resized = raw.resize((nw, nh), Image.Resampling.LANCZOS)
        crop_x = (nw - cw) // 2
        crop_y = (nh - ch) // 2
        cropped = resized.crop((crop_x, crop_y, crop_x + cw, crop_y + ch))

        # 陰影
        draw_cshadow.rounded_rectangle([(cx - 6, cy - 6), (cx + cw + 6, cy + ch + 6)], radius=18, fill=(0, 0, 0, 190))

        # 圓角遮罩貼上圖片
        mask = Image.new("L", (cw, ch), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([(0, 0), (cw, ch)], radius=14, fill=255)
        cards_layer.paste(cropped, (cx, cy), mask)

        # 卡片外框（警示橙紅/琥珀金色調）
        draw_cards.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=14, outline=(245, 158, 11, 200), width=2)

        # 底部標籤條（半透明漸層黑底）
        bar_h = 36 if subtitle else 32
        bar_layer = Image.new("RGBA", (cw, bar_h), (0, 0, 0, 210))
        cards_layer.paste(bar_layer, (cx, cy + ch - bar_h))

        # 標籤文字（純中文，無 emoji 與特殊符號）
        draw_cards.text((cx + 12, cy + ch - bar_h + 8), title, font=font_caption, fill=(254, 240, 138, 255))
        if subtitle:
            sw = draw_cards.textlength(subtitle, font=font_sub_caption)
            draw_cards.text((cx + cw - sw - 12, cy + ch - bar_h + 9), subtitle, font=font_sub_caption, fill=(252, 165, 165, 255))

    # 主卡 1：蝦鬆烤雞大餐
    place_food_card(p1, 870, 128, 596, 325, "滿桌油條蝦鬆與香酥烤雞大餐", "高油高精緻碳水")

    # 下方左卡 2：砂鍋老母雞濃湯
    place_food_card(p2, 870, 470, 290, 275, "砂鍋老母雞濃湯", "極致濃郁高普林")

    # 下方右卡 3：冰淇淋布朗尼甜點
    place_food_card(p3, 1176, 470, 290, 275, "熔岩冰淇淋布朗尼", "高糖高飽和脂肪")

    # 底部提醒文字（純中文）
    draw_cards.text((875, 762), "每到用餐就像走鋼索 —— 身邊大魚大肉，我們堅持到底！", font=font_caption, fill=(251, 113, 133, 230))

    # 2. 左側文字與陰影圖層
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_eng = ImageFont.truetype(font_path, 30)
    font_title = ImageFont.truetype(font_path, 122)
    font_sub = ImageFont.truetype(font_path, 42)
    font_punchline = ImageFont.truetype(font_path, 32)
    font_body = ImageFont.truetype(font_path, 24)
    font_small = ImageFont.truetype(font_path, 21)

    start_x = 90
    start_y = 80

    # 2.1 眉標
    eng_tag = "A C T   V I   :   T E M P T A T I O N   &   D I S C I P L I N E"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 2.2 核心主標（122 pt 純白超大字）
    line1 = "素食齋戒 7 天"
    line2 = "心靈與自律考驗"

    y_line1 = start_y + 58
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 142
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 2.3 衝擊副標（42 pt 紐崔萊琥珀金）
    sub_title = "朋友吃雞腿喝雞湯，我吃生菜豆腐毛豆喝蛋白素"
    y_sub = y_line2 + 168
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 2.4 震撼核心金句（32 pt 冰晶亮藍白，全場核心哲學）
    punchline_text = "你有多大的自律，就換來多大的自由！"
    y_punch = y_sub + 78
    draw_shadow.text((start_x, y_punch), punchline_text, font=font_punchline, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_punch), punchline_text, font=font_punchline, fill=(224, 242, 254, 255))

    # 2.5 奇蹟回報小字（24 pt 淺天藍白）
    miracle_text = "（7天葷食歸零：腸道順暢乾淨、身體好輕盈、褲頭大鬆找回年輕！）"
    y_miracle = y_punch + 50
    draw_shadow.text((start_x, y_miracle), miracle_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_miracle), miracle_text, font=font_body, fill=(186, 230, 253, 230))

    # 2.6 打氣金句小語（標準引號）
    cheer_text = "每天和 Carolyn 彼此打氣：「再撐三天！再撐一天！脂肪不見了！」"
    y_cheer = y_miracle + 42
    draw_shadow.text((start_x, y_cheer), cheer_text, font=font_small, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_cheer), cheer_text, font=font_small, fill=(253, 230, 138, 220))

    # 3. 陰影模糊與合成
    cards_shadow_blurred = cards_shadow.filter(ImageFilter.GaussianBlur(radius=10))
    text_shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    final_img = Image.alpha_composite(base_img, cards_shadow_blurred)
    final_img = Image.alpha_composite(final_img, cards_layer)
    final_img = Image.alpha_composite(final_img, text_shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide07_temptation_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered Slide 8 cleanly: {out_path}")
    return out_path

if __name__ == "__main__":
    render_temptation_slide()
