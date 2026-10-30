import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_rich_final_report():
    w, h = 1536, 864 # 真實 16:9

    # 1. 底圖處理：採用 OpenAI 生成的紐崔萊有機農場晨曦大景
    bg_path = "generated/nutrilite_bg_clean_20261030_081407.png"
    if os.path.exists(bg_path):
        raw_bg = Image.open(bg_path).convert("RGBA")
        rw, rh = raw_bg.size
        target_w = int(rh * 16 / 9)
        if rw >= target_w:
            cx = (rw - target_w) // 2
            cropped = raw_bg.crop((cx, 0, cx + target_w, rh))
        else:
            th = int(rw * 9 / 16)
            cy = (rh - th) // 2
            cropped = raw_bg.crop((0, cy, rw, cy + th))
        base_img = cropped.resize((w, h), Image.Resampling.LANCZOS)
    else:
        base_img = Image.new("RGBA", (w, h), (245, 247, 245, 255))

    # 加上一層溫潤清透的紐崔萊晨曦柔光白玉遮罩，確保文字與卡片具備極致可讀性
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 115))
    base_comp = Image.alpha_composite(base_img, overlay)

    # 建立圖層
    cards_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    draw_cards = ImageDraw.Draw(cards_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)
    draw_text = ImageDraw.Draw(text_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    
    font_header_title = ImageFont.truetype(font_path, 24)
    font_name = ImageFont.truetype(font_path, 32)
    font_meta = ImageFont.truetype(font_path, 19)

    font_sec_title = ImageFont.truetype(font_path, 21)
    font_badge = ImageFont.truetype(font_path, 16)
    font_row_label = ImageFont.truetype(font_path, 19)
    font_row_val = ImageFont.truetype(font_path, 18)
    font_row_diff = ImageFont.truetype(font_path, 20)

    font_stat_box_title = ImageFont.truetype(font_path, 19)
    font_stat_box_num = ImageFont.truetype(font_path, 20)
    font_stat_box_body = ImageFont.truetype(font_path, 15)
    font_footer_punch = ImageFont.truetype(font_path, 21)

    # ==========================================
    # 2. 頂部 Header 欄（白玉磨砂浮雕條）
    # ==========================================
    head_x, head_y = 45, 20
    head_w, head_h = 1446, 82
    draw_shadow.rounded_rectangle([(head_x, head_y + 3), (head_x + head_w, head_y + head_h + 3)], radius=12, fill=(0, 0, 0, 50))
    draw_cards.rounded_rectangle([(head_x, head_y), (head_x + head_w, head_y + head_h)], radius=12, fill=(255, 255, 255, 242), outline=(16, 185, 129, 140), width=1)

    draw_text.text((head_x + 25, head_y + 11), "寰宇南京中心 ｜ 健管45天成果報告", font=font_header_title, fill=(5, 150, 105, 255))
    draw_text.text((head_x + 25, head_y + 42), "學員：王執定（Rich）", font=font_name, fill=(15, 23, 42, 255))

    meta_str = "年齡：48 歲   ｜   推薦人：江沛璇   ｜   健管教練：麥淑媛"
    mw = draw_text.textlength(meta_str, font=font_meta)
    draw_text.text((head_x + head_w - mw - 25, head_y + 30), meta_str, font=font_meta, fill=(51, 65, 85, 255))

    # ==========================================
    # 3. 左半部：BEFORE & AFTER 身材對照卡
    # ==========================================
    left_x, left_y = 45, 115
    left_w, left_h = 600, 720
    draw_shadow.rounded_rectangle([(left_x, left_y + 4), (left_x + left_w, left_y + left_h + 4)], radius=14, fill=(0, 0, 0, 60))
    draw_cards.rounded_rectangle([(left_x, left_y), (left_x + left_w, left_y + left_h)], radius=14, fill=(255, 255, 255, 242), outline=(226, 232, 240, 200), width=1)

    draw_cards.rounded_rectangle([(left_x + 18, left_y + 14), (left_x + left_w - 18, left_y + 50)], radius=8, fill=(240, 253, 244, 255))
    draw_text.text((left_x + 30, left_y + 20), "【體態紀錄】45天 真實體態蛻變全紀錄", font=font_sec_title, fill=(5, 150, 105, 255))

    p_before = "generated/extracted_rich_img_11.jpg"
    p_after = "generated/extracted_rich_img_10.jpg"

    photo_y = left_y + 64
    photo_w = 270
    photo_h = 575

    def paste_photo(p_path, px, py, pw, ph, tag_text, tag_color):
        if not os.path.exists(p_path):
            return
        im = Image.open(p_path).convert("RGBA")
        iw, ih = im.size
        scale = max(pw / iw, ph / ih)
        nw, nh = int(iw * scale), int(ih * scale)
        res = im.resize((nw, nh), Image.Resampling.LANCZOS)
        cx = (nw - pw) // 2
        cy = (nh - ph) // 2
        cropped = res.crop((cx, cy, cx + pw, cy + ph))

        mask = Image.new("L", (pw, ph), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([(0, 0), (pw, ph)], radius=10, fill=255)
        cards_layer.paste(cropped, (px, py), mask)
        draw_cards.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=10, outline=(203, 213, 225, 255), width=1)

        bw = 145
        bh = 30
        bx = px + (pw - bw) // 2
        by = py + 10
        draw_cards.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=6, fill=tag_color)
        tw = draw_text.textlength(tag_text, font=font_badge)
        draw_text.text((bx + (bw - tw) // 2, by + 6), tag_text, font=font_badge, fill=(255, 255, 255, 255))

    paste_photo(p_before, left_x + 20, photo_y, photo_w, photo_h, "BEFORE 健管前", (220, 38, 38, 230))
    paste_photo(p_after, left_x + 310, photo_y, photo_w, photo_h, "AFTER 健管後", (16, 185, 129, 230))

    draw_cards.rounded_rectangle([(left_x + 20, left_y + left_h - 60), (left_x + left_w - 20, left_y + left_h - 15)], radius=8, fill=(236, 253, 245, 255))
    draw_text.text((left_x + 35, left_y + left_h - 50), "腰圍緊縮 8 公分！現在穿褲子皮帶多退三格！", font=font_footer_punch, fill=(4, 120, 87, 255))

    # ==========================================
    # 4. 右半部上：45 天核心身體指標驗收表格卡
    # ==========================================
    right_x, right_y = 665, 115
    right_w, right_h = 825, 345
    draw_shadow.rounded_rectangle([(right_x, right_y + 4), (right_x + right_w, right_y + right_h + 4)], radius=14, fill=(0, 0, 0, 60))
    draw_cards.rounded_rectangle([(right_x, right_y), (right_x + right_w, right_y + right_h)], radius=14, fill=(255, 255, 255, 242), outline=(226, 232, 240, 200), width=1)

    draw_cards.rounded_rectangle([(right_x + 18, right_y + 14), (right_x + right_w - 18, right_y + 50)], radius=8, fill=(240, 253, 244, 255))
    draw_text.text((right_x + 30, right_y + 20), "【數據結算】45 天核心身體數據成果表", font=font_sec_title, fill=(5, 150, 105, 255))

    headers = ["測量項目", "開始日 (初始)", "結束日 (結案)", "45天總成效", "評比亮點"]
    rows = [
        ("體重 (kg)", "68.7 kg", "63.0 kg", "-5.7 kg", "達標率 165.7% 超標完成！"),
        ("體脂率 (%)", "23.5 %", "21.7 %", "-1.8 %", "體態精實收腰，腹肌浮現"),
        ("純脂肪重 (kg)", "16.1 kg", "13.6 kg", "-2.5 kg", "甩掉純脂肪，不減骨骼肌"),
        ("內臟脂肪", "9 級 (警訊)", "7 級 (標準)", "-2 級", "遠離心血管與脂肪肝威脅"),
        ("身體年齡", "48 歲", "42 歲", "-6 歲", "逆生長！找回 6 年青春活力"),
    ]

    col_x = [right_x + 25, right_x + 180, right_x + 340, right_x + 490, right_x + 625]
    row_y0 = right_y + 65
    row_gap = 48

    draw_cards.rounded_rectangle([(right_x + 18, row_y0), (right_x + right_w - 18, row_y0 + 35)], radius=6, fill=(241, 245, 249, 255))
    for c_idx, h_title in enumerate(headers):
        draw_text.text((col_x[c_idx], row_y0 + 8), h_title, font=font_row_label, fill=(71, 85, 105, 255))

    for r_idx, r_data in enumerate(rows):
        cur_y = row_y0 + 42 + r_idx * row_gap
        if r_idx % 2 == 1:
            draw_cards.rounded_rectangle([(right_x + 18, cur_y - 4), (right_x + right_w - 18, cur_y + 36)], radius=6, fill=(248, 250, 252, 255))
        draw_text.text((col_x[0], cur_y + 4), r_data[0], font=font_row_label, fill=(15, 23, 42, 255))
        draw_text.text((col_x[1], cur_y + 4), r_data[1], font=font_row_val, fill=(100, 116, 139, 255))
        draw_text.text((col_x[2], cur_y + 4), r_data[2], font=font_row_val, fill=(15, 23, 42, 255))
        draw_text.text((col_x[3], cur_y + 2), r_data[3], font=font_row_diff, fill=(5, 150, 105, 255))
        draw_text.text((col_x[4], cur_y + 5), r_data[4], font=font_row_val, fill=(180, 83, 9, 255) if r_idx==0 else (71, 85, 105, 255))

    # ==========================================
    # 5. 右半部下：改善狀況與關鍵健康突破卡
    # ==========================================
    bot_y = 475
    bot_h = 360
    draw_shadow.rounded_rectangle([(right_x, bot_y + 4), (right_x + right_w, bot_y + bot_h + 4)], radius=14, fill=(0, 0, 0, 60))
    draw_cards.rounded_rectangle([(right_x, bot_y), (right_x + right_w, bot_y + bot_h)], radius=14, fill=(255, 255, 255, 242), outline=(226, 232, 240, 200), width=1)

    draw_cards.rounded_rectangle([(right_x + 18, bot_y + 14), (right_x + right_w - 18, bot_y + 50)], radius=8, fill=(254, 243, 199, 255))
    draw_text.text((right_x + 30, bot_y + 20), "【成效突破】關鍵改善的狀況與健康奇蹟", font=font_sec_title, fill=(180, 83, 9, 255))

    box_w = 385
    box_h = 132
    b_x1 = right_x + 20
    b_x2 = b_x1 + box_w + 16
    b_y1 = bot_y + 62
    b_y2 = b_y1 + box_h + 12

    boxes_data = [
        (
            b_x1, b_y1,
            "【肌肉增長】骨骼肌率 逆勢增加",
            "31.1%  →  31.7%（+0.6%）",
            "減重期間肌肉逆勢增加！證明減掉的",
            "完全是多餘油水，科學調體質更精實！",
            (240, 253, 244, 255), (16, 185, 129, 255), (5, 150, 105, 255)
        ),
        (
            b_x2, b_y1,
            "【血壓指標】重返完美標準",
            "140/100  →  120/80 mmHg",
            "從高血壓飆破 160 昏眩危險警訊，",
            "徹底回復到健康黃金血壓 120/80！",
            (254, 242, 242, 255), (239, 68, 68, 255), (185, 28, 28, 255)
        ),
        (
            b_x1, b_y2,
            "【圍度雕塑】大幅緊實縮小",
            "腰圍 90 → 82 cm（大瘦 8 cm）",
            "臀圍減 7 cm，腹部贅肉全消！原本緊繃",
            "的西裝褲變得無比寬鬆，重現自信男神腰身！",
            (245, 243, 255, 255), (168, 85, 247, 255), (126, 34, 206, 255)
        ),
        (
            b_x2, b_y2,
            "【體質新生】精神與味蕾煥發",
            "精神飽滿充沛 ｜ 味蕾更加敏銳",
            "擺脫咖啡重度依賴，下午不再疲勞昏睡；",
            "享受原型食物天然甘甜，找回年輕！",
            (254, 249, 195, 255), (234, 179, 8, 255), (161, 98, 7, 255)
        )
    ]

    for (bx, by, b_title, b_num, l1, l2, bg_col, b_border, b_text_col) in boxes_data:
        draw_cards.rounded_rectangle([(bx, by), (bx + box_w, by + box_h)], radius=10, fill=bg_col, outline=b_border, width=1)
        draw_text.text((bx + 14, by + 12), b_title, font=font_stat_box_title, fill=b_text_col)
        draw_text.text((bx + 14, by + 38), b_num, font=font_stat_box_num, fill=(15, 23, 42, 255))
        draw_text.text((bx + 14, by + 74), l1, font=font_stat_box_body, fill=(71, 85, 105, 255))
        draw_text.text((bx + 14, by + 98), l2, font=font_stat_box_body, fill=(71, 85, 105, 255))

    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    final_img = Image.alpha_composite(base_comp, shadow_blurred)
    final_img = Image.alpha_composite(final_img, cards_layer)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide08_rich_report_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered Clean Rich Final Report Slide: {out_path}")
    return out_path

if __name__ == "__main__":
    render_rich_final_report()
