import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_threshold_slide(bg_image_path=None):
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
    font_title = ImageFont.truetype(font_path, 132)
    font_sub = ImageFont.truetype(font_path, 48)
    font_body = ImageFont.truetype(font_path, 28)

    start_x = 110
    start_y = 100

    # 1. 眉標
    eng_tag = "A C T  I I I  :  C R O S S I N G  T H E  T H R E S H O L D"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 2. 核心主標（132 pt）
    line1 = "不見棺材不掉淚"
    line2 = "關鍵在「城隍爺」！"

    y_line1 = start_y + 60
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 155
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3. 衝擊副標（48 pt 紐崔萊琥珀金）
    sub_title = "以往批流年「小心開車」，今年竟批出「小心頭部疾病」！"
    y_sub = y_line2 + 180
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 4. 現場爆笑與破釜行動路徑（28 pt 冰晶亮藍白）
    joke_path = "追問竟被神明肅穆搖頭 ➔ 腦補中風頭爆炸 ➔ 火速找沛璇老師排健管！"
    y_joke = y_sub + 90
    draw_shadow.text((start_x, y_joke), joke_path, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_joke), joke_path, font=font_body, fill=(224, 242, 254, 255))

    # 模糊陰影
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    # 合成
    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide04_threshold_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered slide: {out_path}")
    return out_path

if __name__ == "__main__":
    render_threshold_slide()
