import os
from PIL import Image, ImageDraw, ImageFont

def render_preview():
    bg_path = "generated/slide01_hero_opening_sunrise_20261029_013934.png"
    if not os.path.exists(bg_path):
        print("Missing background image")
        return
        
    img = Image.open(bg_path).convert("RGBA")
    w, h = img.size # 1536 x 1024
    
    # Overlay layer
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Card coordinates
    card_x1 = int(w * 0.06)
    card_y1 = int(h * 0.16)
    card_x2 = int(w * 0.54)
    card_y2 = int(h * 0.84)
    radius = 24
    
    # Draw dark frosted container with 88% opacity
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=radius, fill=(15, 23, 42, 225), outline=(5, 150, 105, 255), width=3)
    
    # Draw vertical emerald bar
    bar_x = card_x1 + 36
    bar_y1 = card_y1 + 48
    bar_y2 = card_y2 - 48
    draw.rectangle([bar_x, bar_y1, bar_x + 8, bar_y2], fill=(16, 185, 129, 255))
    
    # Font loading
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_tag = ImageFont.truetype(font_path, 22)
        font_title = ImageFont.truetype(font_path, 64)
        font_sub = ImageFont.truetype(font_path, 32)
        font_author = ImageFont.truetype(font_path, 24)
    except Exception as e:
        print(f"Font load error: {e}")
        font_tag = font_title = font_sub = font_author = ImageFont.load_default()
        
    text_x = bar_x + 36
    
    # Tag
    draw.text((text_x, bar_y1 + 10), "HERO'S JOURNEY ｜ 健管 45 天", font=font_tag, fill=(52, 211, 153, 255))
    
    # Title
    draw.text((text_x, bar_y1 + 60), "45 天的", font=font_title, fill=(255, 255, 255, 255))
    draw.text((text_x, bar_y1 + 140), "蛻變歷程", font=font_title, fill=(255, 255, 255, 255))
    
    # Subtitle
    draw.text((text_x, bar_y1 + 250), "重啟 48 歲的身體主控權", font=font_sub, fill=(245, 158, 11, 255))
    
    # Author
    draw.text((text_x, bar_y1 + 320), "分享者：王執定（Rich）", font=font_author, fill=(203, 213, 225, 255))
    draw.text((text_x, bar_y1 + 365), "45天減重 5.7kg・腰圍 -8cm・身體年齡 -6歲", font=font_tag, fill=(148, 163, 184, 255))
    
    final_img = Image.alpha_composite(img, overlay)
    out_path = "generated/slide01_opening_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered preview saved to {out_path}")

if __name__ == "__main__":
    render_preview()
