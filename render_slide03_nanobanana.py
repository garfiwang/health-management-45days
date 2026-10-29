import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_slide03_nanobanana():
    raw_path = "generated/slide03_nanobanana_concept_raw.jpg"
    if not os.path.exists(raw_path):
        print("Missing raw image")
        return

    raw_img = Image.open(raw_path).convert("RGBA")
    rw, rh = raw_img.size # 1376 x 768

    # 1. 精準對齊 16:9
    # 目標標準 16:9 尺寸：1536 x 864
    # 目前 1376 x 768，長寬比為 1.7916。標準 16:9 是 1.777778
    # 768 * (16/9) = 1365.333 -> 左右微修剪 10px (1376 - 1365 = 11px)
    target_w_src = int(rh * 16 / 9) # 1365
    crop_x = (rw - target_w_src) // 2
    cropped_src = raw_img.crop((crop_x, 0, crop_x + target_w_src, rh))

    # 高品質放大至 1536 x 864
    w, h = 1536, 864
    base_img = cropped_src.resize((w, h), Image.Resampling.LANCZOS)
    print(f"Resized & Cropped to exact 16:9: {w} x {h}, ratio = {w/h:.6f}")

    # 2. 左側平滑暗角漸層（Smoothstep Scrim），無卡片框線，自然光影融入
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

    # 3. 排版文字圖層（大字規範）
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 32)
    font_title = ImageFont.truetype(font_path, 136)
    font_sub = ImageFont.truetype(font_path, 52)
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

    # C. 衝擊副標（紐崔萊琥珀金 52 pt）
    sub_title = "半夜膝蓋痛到發瘋，自創 168 差點休克"
    y_sub = y_line2 + 180
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

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
