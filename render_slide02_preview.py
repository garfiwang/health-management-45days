import os
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_slide02():
    # 尋找最新產生的 slide02 圖片
    candidates = glob.glob("generated/slide02_richman_ordinary_world_*.png")
    if not candidates:
        print("Waiting for raw image generation...")
        return False
    
    candidates.sort()
    raw_path = candidates[-1]
    print(f"Processing raw image: {raw_path}")

    raw_img = Image.open(raw_path).convert("RGBA")
    rw, rh = raw_img.size # 1536 x 1024 (3:2)

    # 1. 精準 16:9 裁切 (1536 x 864)
    # 1024 - 864 = 160px。從頂部剪 40px 保留天空與頂部空間，底部剪 120px
    crop_top = 40
    crop_bottom = crop_top + 864
    base_img = raw_img.crop((0, crop_top, 1536, crop_bottom))
    w, h = base_img.size
    print(f"Cropped to exact 16:9: {w} x {h}, ratio = {w/h:.6f}")

    # 2. 左側平滑暗角漸層（Smoothstep Scrim）
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.58) # 約 890px
    grad_pixels = gradient.load()

    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            # smoothstep 曲線
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 248 * factor
        else:
            base_alpha = 0
            
        for y in range(h):
            # 底部略深，確保底部白色字極致清晰
            if y > int(h * 0.65):
                alpha = int(min(255, base_alpha * 1.06))
            else:
                alpha = int(base_alpha)
            # 深藍夜色底 (8, 14, 24)
            grad_pixels[x, y] = (8, 14, 24, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 3. 排版文字圖層（劇場級大字規範）
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 32)
    font_title = ImageFont.truetype(font_path, 136)
    font_sub = ImageFont.truetype(font_path, 54)
    font_body = ImageFont.truetype(font_path, 30)

    start_x = 110
    start_y = 110

    # A. 眉標（ACT I : THE ORDINARY WORLD）
    eng_tag = "A C T  I  :  T H E  O R D I N A R Y  W O R L D"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 翡翠亮綠

    # B. 核心主標（大字 136 pt）
    # 第一行：別人朝九晚五
    # 第二行：我「朝五晚九」
    line1 = "別人朝九晚五"
    line2 = "我「朝五晚九」"
    
    y_line1 = start_y + 60
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 155
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # C. 衝擊副標（琥珀金 54 pt）
    sub_title = "剛退伍拚到半夜，如今三杯咖啡爬不起來"
    y_sub = y_line2 + 185
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255)) # 紐崔萊琥珀金

    # D. 高壓日常路徑（高對比冰晶亮藍白 30 pt）
    path_text = "清晨 5:00 BNI 開會  |  整理財經資料  |  下午諮詢演講  |  晚間應酬"
    y_path = y_sub + 95
    draw_shadow.text((start_x, y_path), path_text, font=font_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_path), path_text, font=font_body, fill=(224, 242, 254, 255)) # 冰晶亮藍白

    # 模糊陰影
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    # 合成所有圖層
    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    # 儲存預覽圖與完美 16:9 底圖
    out_preview_path = "generated/slide02_richman_ordinary_world_preview.png"
    final_img.convert("RGB").save(out_preview_path, quality=95)
    print(f"Successfully generated Slide 02 preview: {out_preview_path}")
    return out_preview_path

if __name__ == "__main__":
    render_slide02()
