import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_slide01_openai_16_9():
    bg_path = "generated/slide01_richman_openai_16_9_20261030_080024.png"
    out_path = "generated/slide01_openai_16_9_rendered.png"

    if not os.path.exists(bg_path):
        print(f"Error: {bg_path} not found")
        return

    base_img = Image.open(bg_path).convert("RGBA")
    w, h = base_img.size  # 1536 x 864

    # 1. Left-to-right smooth dark scrim gradient
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.58)  # ~890px
    grad_pixels = gradient.load()
    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 245 * factor
        else:
            base_alpha = 0
            
        for y in range(h):
            if y > int(h * 0.55):
                alpha = int(min(255, base_alpha * 1.08))
            else:
                alpha = int(base_alpha)
            grad_pixels[x, y] = (8, 14, 24, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 2. Typography Layers
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_eng = ImageFont.truetype(font_path, 32)
        font_title = ImageFont.truetype(font_path, 136)
        font_sub = ImageFont.truetype(font_path, 54)
        font_author = ImageFont.truetype(font_path, 38)
        font_stats = ImageFont.truetype(font_path, 30)
    except Exception as e:
        print("Font error:", e)
        font_eng = font_title = font_sub = font_author = font_stats = ImageFont.load_default()

    # Layout Coordinates
    start_x = int(w * 0.075)  # x = ~115
    y_eng = int(h * 0.10)     # y = ~86

    y_title1 = y_eng + 58     # y = 144
    y_title2 = y_title1 + 150  # y = 294
    y_sub = y_title2 + 175    # y = 469
    y_author = y_sub + 105    # y = 574
    y_stats = y_author + 75    # y = 649

    eng_tag = "T H E   H E R O ' S   J O U R N E Y"
    title_line1 = "45 天的"
    title_line2 = "蛻變歷程"
    sub_title = "重啟 48 歲的身體主控權"
    author_text = "主講人：王執定 Rich ｜ 金融界理財講師"
    stats_text = "45 天累減 5.7kg ｜ 腰圍大瘦 8cm ｜ 身體年齡年輕 6 歲"

    # Soft Drop Shadow
    s_offset = 4
    s_color = (0, 0, 0, 215)
    draw_shadow.text((start_x + s_offset, y_eng + s_offset), eng_tag, font=font_eng, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title1 + s_offset), title_line1, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title2 + s_offset), title_line2, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_sub + s_offset), sub_title, font=font_sub, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_author + s_offset), author_text, font=font_author, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_stats + s_offset), stats_text, font=font_stats, fill=s_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))

    # Forefront Typography
    draw_text.text((start_x, y_eng), eng_tag, font=font_eng, fill=(52, 211, 153, 255))  # Emerald Green
    draw_text.text((start_x, y_title1), title_line1, font=font_title, fill=(255, 255, 255, 255))  # Pure Bold White
    draw_text.text((start_x, y_title2), title_line2, font=font_title, fill=(255, 255, 255, 255))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(251, 191, 36, 255))  # Amber Gold
    draw_text.text((start_x, y_author), author_text, font=font_author, fill=(255, 255, 255, 255))  # Crisp White
    draw_text.text((start_x, y_stats), stats_text, font=font_stats, fill=(224, 242, 254, 255))  # Luminous Ice-Cyan White

    final = Image.alpha_composite(comp_img, shadow_layer)
    final = Image.alpha_composite(final, text_layer)
    final.convert("RGB").save(out_path, quality=95)
    print(f"Successfully rendered: {out_path} ({w}x{h})")

if __name__ == "__main__":
    render_slide01_openai_16_9()
