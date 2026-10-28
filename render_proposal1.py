import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_cinematic_proposal1():
    bg_path = "generated/slide01_hero_opening_sunrise_20261029_013934.png"
    if not os.path.exists(bg_path):
        print(f"Error: {bg_path} not found")
        return

    base_img = Image.open(bg_path).convert("RGBA")
    w, h = base_img.size # 1536 x 1024

    # 1. Create seamless Left-to-Right Dark Scrim Gradient
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.65) # fade ends at 65% of screen width

    # Build gradient image row by row / column by column
    grad_pixels = gradient.load()
    for x in range(w):
        if x < fade_end:
            # Smoothstep curve for natural photographic falloff
            t = x / fade_end
            # smoothstep: 3*t^2 - 2*t^3
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            alpha = int(220 * factor) # Max alpha 220 (86% opacity) on far left, down to 0
        else:
            alpha = 0
            
        for y in range(h):
            grad_pixels[x, y] = (10, 18, 30, alpha) # Deep cinematic slate dark tone

    # Composite the gradient onto the base image
    comp_img = Image.alpha_composite(base_img, gradient)

    # 2. Text Drawing Layer
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    # Font loading
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

    # Text positioning (Left margin with generous breathing room)
    start_x = int(w * 0.08) # x = ~123
    start_y = int(h * 0.22) # y = ~225

    # Text Content
    eng_tag = "T H E   H E R O ' S   J O U R N E Y"
    title_line1 = "45 天的"
    title_line2 = "蛻變歷程"
    sub_title = "重啟 48 歲的身體主控權"
    author_text = "主講人：王執定（Rich）"
    stats_text = "45 天累減 5.7kg ｜ 腰圍大瘦 8cm ｜ 身體年齡年輕 6 歲"

    # Positions
    y_eng = start_y
    y_title1 = y_eng + 45
    y_title2 = y_title1 + 90
    y_sub = y_title2 + 120
    y_author = y_sub + 75
    y_stats = y_author + 45

    # Draw Subtle Cinematic Drop Shadow on shadow_layer
    s_offset = 3
    s_color = (0, 0, 0, 160)
    draw_shadow.text((start_x + s_offset, y_eng + s_offset), eng_tag, font=font_eng, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title1 + s_offset), title_line1, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title2 + s_offset), title_line2, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_sub + s_offset), sub_title, font=font_sub, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_author + s_offset), author_text, font=font_author, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_stats + s_offset), stats_text, font=font_stats, fill=s_color)

    # Blur the shadow slightly for movie poster softness
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))

    # Draw Crisp Forefront Text
    # 1. English Tag (soft emerald gold)
    draw_text.text((start_x, y_eng), eng_tag, font=font_eng, fill=(52, 211, 153, 255))
    
    # 2. Main Title (Pure crisp white with massive weight)
    draw_text.text((start_x, y_title1), title_line1, font=font_title, fill=(255, 255, 255, 255))
    draw_text.text((start_x, y_title2), title_line2, font=font_title, fill=(255, 255, 255, 255))

    # 3. Subtitle (Warm Nutrilite Amber Sunburst)
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(251, 191, 36, 255))

    # 4. Author line (Clean Off-White)
    draw_text.text((start_x, y_author), author_text, font=font_author, fill=(241, 245, 249, 255))

    # 5. Stats line (Soft Slate Grey)
    draw_text.text((start_x, y_stats), stats_text, font=font_stats, fill=(148, 163, 184, 255))

    # Final Composite
    final = Image.alpha_composite(comp_img, shadow_layer)
    final = Image.alpha_composite(final, text_layer)

    out_path = "generated/slide01_proposal1_cinematic_preview.png"
    final.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    create_cinematic_proposal1()
