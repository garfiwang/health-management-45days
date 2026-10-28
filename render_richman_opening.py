import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_richman_opening_super_large():
    bg_path = "generated/slide01_richman_ip_opening_20261029_015510.png"
    if not os.path.exists(bg_path):
        print(f"Error: {bg_path} not found")
        return

    base_img = Image.open(bg_path).convert("RGBA")
    w, h = base_img.size # 1536 x 1024

    # 1. Enhanced Dark Scrim Gradient
    # Extend fade_end to 60% of width, and ensure lower-left has deep contrast
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.60) # ~921px

    grad_pixels = gradient.load()
    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            # smoothstep: 3*t^2 - 2*t^3
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 245 * factor # deeper dark on left (max 245)
        else:
            base_alpha = 0
            
        for y in range(h):
            # Give extra dark backing to bottom area where stats text sits
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
    
    # 再放大兩級 (Enlarge 2 more levels)
    # Title: 110 -> 142 pt (Massive Keynote Impact)
    # Sub: 48 -> 58 pt
    # Author: 34 -> 42 pt
    # Stats: 26 -> 32 pt (High-contrast pure white/cyan)
    # Tag: 28 -> 34 pt
    try:
        font_eng = ImageFont.truetype(font_path, 34)
        font_title = ImageFont.truetype(font_path, 142)
        font_sub = ImageFont.truetype(font_path, 58)
        font_author = ImageFont.truetype(font_path, 42)
        font_stats = ImageFont.truetype(font_path, 32)
        font_stats_bold = ImageFont.truetype(font_path, 34)
    except Exception as e:
        print("Font error:", e)
        font_eng = font_title = font_sub = font_author = font_stats = font_stats_bold = ImageFont.load_default()

    # Layout Coordinates
    start_x = int(w * 0.075) # x = ~115
    y_eng = int(h * 0.12)    # y = ~123

    y_title1 = y_eng + 65    # y = 188
    y_title2 = y_title1 + 160 # y = 348
    y_sub = y_title2 + 185   # y = 533
    y_author = y_sub + 115   # y = 648
    y_stats = y_author + 80   # y = 728

    eng_tag = "T H E   H E R O ' S   J O U R N E Y"
    title_line1 = "45 天的"
    title_line2 = "蛻變歷程"
    sub_title = "重啟 48 歲的身體主控權"
    author_text = "主講人：王執定（Rich） ｜ 金融男神"
    stats_text = "45 天累減 5.7kg ｜ 腰圍大瘦 8cm ｜ 身體年齡年輕 6 歲"

    # Cinematic Strong Drop Shadow
    s_offset = 4
    s_color = (0, 0, 0, 210) # deeper shadow for maximum legibility
    draw_shadow.text((start_x + s_offset, y_eng + s_offset), eng_tag, font=font_eng, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title1 + s_offset), title_line1, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_title2 + s_offset), title_line2, font=font_title, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_sub + s_offset), sub_title, font=font_sub, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_author + s_offset), author_text, font=font_author, fill=s_color)
    draw_shadow.text((start_x + s_offset, y_stats + s_offset), stats_text, font=font_stats, fill=s_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))

    # Forefront Typography
    # 1. Tag (Emerald Neon Green)
    draw_text.text((start_x, y_eng), eng_tag, font=font_eng, fill=(52, 211, 153, 255))
    
    # 2. Main Title (Crisp Pure White 142pt)
    draw_text.text((start_x, y_title1), title_line1, font=font_title, fill=(255, 255, 255, 255))
    draw_text.text((start_x, y_title2), title_line2, font=font_title, fill=(255, 255, 255, 255))
    
    # 3. Subtitle (Vibrant Nutrilite Amber Sunburst 58pt)
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(251, 191, 36, 255))
    
    # 4. Author line (Bright Crisp White 42pt)
    draw_text.text((start_x, y_author), author_text, font=font_author, fill=(255, 255, 255, 255))
    
    # 5. Bottom Stats: ADJUSTED TO HIGH-CONTRAST LUMINOUS ICE-CYAN / CRISP WHITE
    # Instead of dull grey, use glowing crisp light cyan-white (224, 242, 254) with 100% opacity
    draw_text.text((start_x, y_stats), stats_text, font=font_stats, fill=(224, 242, 254, 255))

    final = Image.alpha_composite(comp_img, shadow_layer)
    final = Image.alpha_composite(final, text_layer)

    out_path = "generated/slide01_richman_ip_opening_preview.png"
    final.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_path} with 2 more levels enlarged typography and high-contrast bottom stats!")

if __name__ == "__main__":
    render_richman_opening_super_large()
