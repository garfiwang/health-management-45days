import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_slide03_nanobanana(raw_path=None):
    if raw_path is None:
        raw_path = "generated/slide03_nanobanana_concept_raw.jpg"
        
    if not os.path.exists(raw_path):
        print("Missing raw image:", raw_path)
        return False

    raw_img = Image.open(raw_path).convert("RGBA")
    rw, rh = raw_img.size

    # 1. 精準對齊 16:9（1536 x 864）
    target_w_src = int(rh * 16 / 9)
    if rw >= target_w_src:
        crop_x = (rw - target_w_src) // 2
        cropped_src = raw_img.crop((crop_x, 0, crop_x + target_w_src, rh))
    else:
        # 高度裁切
        target_h_src = int(rw * 9 / 16)
        crop_y = (rh - target_h_src) // 2
        cropped_src = raw_img.crop((0, crop_y, rw, crop_y + target_h_src))

    w, h = 1536, 864
    base_img = cropped_src.resize((w, h), Image.Resampling.LANCZOS)
    print(f"Resized & Cropped to exact 16:9: {w} x {h}, ratio = {w/h:.6f}")

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

    # 3. 排版文字圖層（依 Rich 要求精準改字）
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 32)
    font_title = ImageFont.truetype(font_path, 136)
    font_sub = ImageFont.truetype(font_path, 46) # 依 25 字副標優雅縮放
    font_body = ImageFont.truetype(font_path, 28)

    start_x = 110
    start_y = 100

    # A. 眉標（ACT II : THE CALL TO ADVENTURE）
    eng_tag = "A C T  I I  :  T H E  C A L L  T O  A D V E N T U R E"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # B. 核心主標（純白無襯線粗體 136 pt）
    line1 = "身體的兩記重擊"
    line2 = "痛風與血壓 160"

    y_line1 = start_y + 60
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 155
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # C. 衝擊副標（改字：血壓飆到 160 心跳加速差點昏倒）
    sub_title = "半夜膝蓋痛到發瘋，血壓飆到 160 心跳加速差點昏倒"
    y_sub = y_line2 + 180
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255)) # 琥珀金

    # D. 現場鐵齒笑點金句（高對比冰晶亮藍白 28 pt）
    joke_text = "「痛風？！不可能！我平常有做好事、積福報，怎麼可能出事？！」"
    y_joke = y_sub + 90
    draw_shadow.text((start_x, y_joke), joke_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_joke), joke_text, font=font_body, fill=(224, 242, 254, 255))

    # 陰影模糊
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    # 合成
    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_preview = "generated/slide03_richman_crisis_preview.png"
    final_img.convert("RGB").save(out_preview, quality=95)
    print(f"Successfully generated Slide 03 preview: {out_preview}")
    return out_preview

if __name__ == "__main__":
    render_slide03_nanobanana()
