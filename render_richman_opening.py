import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_richman_opening():
    bg_path = "generated/slide01_richman_ip_opening_20261029_015510.png"
    if not os.path.exists(bg_path):
        print(f"Error: {bg_path} not found")
        return

    base_img = Image.open(bg_path).convert("RGBA")
    w, h = base_img.size # 1536 x 1024

    # 1. Left-to-Right Dark Scrim Gradient (Left 55% only, keeping Richman on the right 100% bright)
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.55) # Smoothly fades out before reaching Richman on the right

    grad_pixels = gradient.load()
    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            # Smoothstep curve: 3*t^2 - 2*t^3
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            alpha = int(210 * factor) # Max 210 on the far left, down to 0 at x=55%
        else:
            alpha = 0
            
        for y in range(h):
            grad_pixels[x, y] = (10, 18, 30, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 2. Typography Layers
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_eng = ImageFont.truetype(font_path, 20)
        font_title = ImageFont.truetype(font_path, 76)
        font_sub = ImageFont.truetype(font_path, 34)
        font_author = ImageFont.truetype(font_path, 24)
        font_stats = ImageFont.truetype(font_path, 20)
    except Exception as e:
        print("Font error:", e)
        font_eng = font_title = font_sub = font_author = font_stats = ImageFont.load_default()

    # Layout Position (Left 50% area)
    start_x = int(w * 0.08) # x = ~123
    start_y = int(h * 0.22) # y = ~225

    eng_tag = "T H E   H E R O ' S   J O U R N E Y"
    title_line1 = "45 天的"
    title_line2 = "蛻變歷程"
    sub_title = "重啟 48 歲的身體主控權"
    author_text = "主講人：王執定（Rich） ｜ 金融男神"
    stats_text = "45 天累減 5.7kg ｜ 腰圍大瘦 8cm ｜ 身體年齡年輕 6 歲"

    y_eng = start_y
    y_title1 = y_eng + 45
    y_title2 = y_title1 + 90
    y_sub = y_title2 + 120
    y_author = y_sub + 75
    y_stats = y_author + 45

    # Cinematic Drop Shadow
    s_offset = 3
    s_color = (0, 0, 0, 160)
    draw_shadow.text((start_x + s_offset, y_eng + s_offset), eng_tag, font=font_eng, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title1 + s_offset), title_line1, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title2 + s_offset), title_line2, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_sub + s_offset), sub_title, font=font_sub, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_author + s_offset), author_text, font=font_author, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_stats + s_offset), stats_text, font=font_stats, fill=s_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))

    # Forefront Typography
    draw_text.text((start_x, y_eng), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # Emerald Green
    draw_text.text((start_x, y_title1), title_line1, font=font_title, fill=(255, 255, 255, 255)) # Pure White
    draw_text.text((start_x, y_title2), title_line2, font=font_title, fill=(255, 255, 255, 255))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(251, 191, 36, 255)) # Amber Gold
    draw_text.text((start_x, y_author), author_text, font=font_author, fill=(241, 245, 249, 255)) # Slate White
    draw_text.text((start_x, y_stats), stats_text, font=font_stats, fill=(148, 163, 184, 255)) # Muted Silver

    final = Image.alpha_composite(comp_img, shadow_layer)
    final = Image.alpha_composite(final, text_layer)

    out_path = "generated/slide01_richman_ip_opening_preview.png"
    final.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    render_richman_opening()
