import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_stairwell_slide(bg_image_path="generated/slide06_stairwell_trial_v2_raw.jpg"):
    w, h = 1536, 864 # 真實 16:9

    # 1. 處理背景圖，精準裁切為 16:9 (1536x864)
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

    # 3. 文字與陰影排版
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
    start_y = 85

    # 3.1 眉標
    eng_tag = "A C T   V   :   T H E   I N M O S T   C A V E   &   O R D E A L"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 3.2 核心主標（124 pt 超大震撼純白）
    line1 = "一口氣爬到 8 樓"
    line2 = "跌到 5 樓就大休息"

    y_line1 = start_y + 58
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 145
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3.3 衝擊副標（44 pt 紐崔萊琥珀金）
    sub_title = "撞牆期的小劇場：熱量不夠？好累不想動，該停了嗎？！"
    y_sub = y_line2 + 168
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 3.4 破局心法金句（28 pt 冰晶亮藍白，使用標準 → 箭頭）
    mindset_text = "教練定海神針 →「不是減重，是調體質！補足蛋白素與水分！」"
    y_mindset = y_sub + 80
    draw_shadow.text((start_x, y_mindset), mindset_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_mindset), mindset_text, font=font_body, fill=(224, 242, 254, 255))

    # 3.5 數據亮點（小字補述）
    stats_text = "（前 2 週蜜月期亮眼：體重累減 3kg ｜ 體脂降 1% ｜ 骨骼肌率逆勢 +0.3%）"
    y_stats = y_mindset + 46
    draw_shadow.text((start_x, y_stats), stats_text, font=font_small, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_stats), stats_text, font=font_small, fill=(186, 230, 253, 230))

    # 4. 模糊陰影與圖層合成
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide06_stairwell_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered Slide 7: {out_path}")
    return out_path

if __name__ == "__main__":
    render_stairwell_slide()
