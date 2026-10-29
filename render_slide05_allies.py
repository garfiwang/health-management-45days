import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_allies_slide(bg_image_path="generated/slide05_allies_kitchen_raw.jpg", dolls_image_path="generated/teammates_3d_dolls_concept_draft.jpg"):
    w, h = 1536, 864 # 真實 16:9

    # 1. 處理背景廚房中島備餐圖
    if bg_image_path and os.path.exists(bg_image_path):
        raw_bg = Image.open(bg_image_path).convert("RGBA")
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
        base_img = Image.new("RGBA", (w, h), (10, 15, 26, 255))

    # 2. 左側平滑暗角漸層（Smoothstep Scrim），無框溶字
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.58) # 約 890px
    grad_pixels = gradient.load()

    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 248 * factor
        else:
            base_alpha = 0

        for y in range(h):
            if y > int(h * 0.65):
                alpha = int(min(255, base_alpha * 1.06))
            else:
                alpha = int(base_alpha)
            # 深石板夜色底 (8, 14, 24)
            grad_pixels[x, y] = (8, 14, 24, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 3. 左側文字與陰影排版
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 30)
    font_title = ImageFont.truetype(font_path, 124)
    font_sub = ImageFont.truetype(font_path, 44)
    font_body = ImageFont.truetype(font_path, 28)
    font_small = ImageFont.truetype(font_path, 22)

    start_x = 95
    start_y = 75

    # 3.1 眉標
    eng_tag = "A C T   I V   :   T E S T S ,   A L L I E S   &   E N E M I E S"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 3.2 核心主標（124 pt 超大字）
    line1 = "一個人走得快"
    line2 = "一群人走得遠"

    y_line1 = start_y + 56
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 142
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3.3 衝擊副標（44 pt 紐崔萊琥珀金）
    sub_title = "謝謝我的神隊友雅雯，謝謝沛璇老師與淑媛教練"
    y_sub = y_line2 + 165
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 3.4 核心心法金句（28 pt 冰晶亮藍白）
    mindset_text = "打破「少吃就會瘦」迷思 ➔ 吃對順序、補足營養，減重自然發生！"
    y_mindset = y_sub + 76
    draw_shadow.text((start_x, y_mindset), mindset_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_mindset), mindset_text, font=font_body, fill=(224, 242, 254, 255))

    # 3.5 神隊友成績亮點（小字補述）
    carolyn_stats = "（神隊友雅雯並肩作戰：減掉整整 1.6kg 純脂肪，肌肉量逆勢上升！）"
    y_stats = y_mindset + 44
    draw_shadow.text((start_x, y_stats), carolyn_stats, font=font_small, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_stats), carolyn_stats, font=font_small, fill=(186, 230, 253, 230))

    # 4. 製作【左下角空白處】「縮小版健管神隊友 3D Q版潮玩 IP 展示卡」
    card_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_card = ImageDraw.Draw(card_layer)
    draw_cshadow = ImageDraw.Draw(card_shadow)

    card_x = 95
    card_y = 620
    card_w = 486
    card_h = 192
    radius = 14

    # 陰影
    draw_cshadow.rounded_rectangle([(card_x - 5, card_y - 5), (card_x + card_w + 5, card_y + card_h + 5)], radius=radius+3, fill=(0, 0, 0, 180))

    # 卡片主體（高雅深海軍藍石板磨砂半透明）
    draw_card.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=radius, fill=(11, 19, 35, 230), outline=(52, 211, 153, 190), width=1)

    font_card_head = ImageFont.truetype(font_path, 17)
    font_card_sub = ImageFont.truetype(font_path, 14)
    font_role = ImageFont.truetype(font_path, 13)

    # 卡片頂部欄（小巧精緻）
    draw_card.text((card_x + 16, card_y + 10), "🌟 健管神隊友 3D Q版潮玩 IP", font=font_card_head, fill=(255, 255, 255, 255))
    draw_card.text((card_x + card_w - 150, card_y + 12), "巧巧 ✕ 沛沛 ✕ 麥麥", font=font_card_sub, fill=(245, 158, 11, 255))

    # 嵌入縮小版 3D 公仔特寫縮圖
    thumb_w = card_w - 28 # 458px
    thumb_h = 118 # 118px
    if dolls_image_path and os.path.exists(dolls_image_path):
        dolls_raw = Image.open(dolls_image_path).convert("RGBA")
        dw, dh = dolls_raw.size
        # 裁切公仔精華主體（三人上半身至全身）
        crop_d = dolls_raw.crop((90, 80, dw - 90, int(dh * 0.85)))
        
        scale = max(thumb_w / crop_d.width, thumb_h / crop_d.height)
        nw, nh = int(crop_d.width * scale), int(crop_d.height * scale)
        d_resized = crop_d.resize((nw, nh), Image.Resampling.LANCZOS)
        cx = (nw - thumb_w) // 2
        cy = (nh - thumb_h) // 2
        d_cropped = d_resized.crop((cx, cy, cx + thumb_w, cy + thumb_h))

        # 圓角遮罩
        mask = Image.new("L", (thumb_w, thumb_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([(0, 0), (thumb_w, thumb_h)], radius=8, fill=255)
        
        card_layer.paste(d_cropped, (card_x + 14, card_y + 36), mask)

    # 角色對照小標籤（底部微型排版）
    tag_y = card_y + 36 + thumb_h + 8
    draw_card.text((card_x + 18, tag_y), "👩‍🍳 巧巧 (備餐・雅雯)", font=font_role, fill=(134, 239, 172, 255))
    draw_card.text((card_x + 175, tag_y), "👩‍⚕️ 沛沛 (營養・沛璇)", font=font_role, fill=(192, 132, 252, 255))
    draw_card.text((card_x + 332, tag_y), "🏃‍♀️ 麥麥 (動力・淑媛)", font=font_role, fill=(251, 113, 133, 255))

    # 5. 陰影模糊與圖層合成
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))
    card_shadow_blurred = card_shadow.filter(ImageFilter.GaussianBlur(radius=8))

    final_img = Image.alpha_composite(comp_img, card_shadow_blurred)
    final_img = Image.alpha_composite(final_img, card_layer)
    final_img = Image.alpha_composite(final_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide05_allies_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered slide 6 with mini 3D dolls at left bottom: {out_path}")
    return out_path

if __name__ == "__main__":
    render_allies_slide()
