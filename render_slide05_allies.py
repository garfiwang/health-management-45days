import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_allies_slide(bg_image_path=None):
    w, h = 1536, 864 # 真實 16:9

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

    # 左側平滑暗角漸層（Smoothstep Scrim），無框溶字
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

    # 文字與陰影
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 32)
    font_title = ImageFont.truetype(font_path, 128)
    font_sub = ImageFont.truetype(font_path, 48)
    font_body = ImageFont.truetype(font_path, 28)
    font_small = ImageFont.truetype(font_path, 23)

    start_x = 110
    start_y = 100

    # 1. 眉標
    eng_tag = "A C T   I V   :   T E S T S ,   A L L I E S   &   E N E M I E S"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 2. 核心主標（128 pt）
    line1 = "一個人走得快"
    line2 = "一群人走得遠"

    y_line1 = start_y + 60
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 150
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3. 衝擊副標（48 pt 紐崔萊琥珀金）
    sub_title = "謝謝我的神隊友雅雯，謝謝沛璇老師與淑媛教練"
    y_sub = y_line2 + 175
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 4. 核心心法金句（28 pt 冰晶亮藍白）
    mindset_text = "打破「少吃就會瘦」迷思 ➔ 吃對順序、補足營養，減重自然發生！"
    y_mindset = y_sub + 85
    draw_shadow.text((start_x, y_mindset), mindset_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_mindset), mindset_text, font=font_body, fill=(224, 242, 254, 255))

    # 5. 神隊友成績亮點（小字補述）
    carolyn_stats = "（神隊友雅雯並肩作戰：減掉整整 1.6kg 純脂肪，肌肉量逆勢上升！）"
    y_stats = y_mindset + 48
    draw_shadow.text((start_x, y_stats), carolyn_stats, font=font_small, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_stats), carolyn_stats, font=font_small, fill=(186, 230, 253, 230))

    # 模糊陰影
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    # 合成
    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide05_allies_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered slide 6: {out_path}")
    return out_path

if __name__ == "__main__":
    render_allies_slide()
