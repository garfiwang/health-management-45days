import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_micro_actions_slide(bg_image_path="generated/slide09_micro_actions_raw.jpg"):
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
        base_img = Image.new("RGBA", (w, h), (10, 16, 28, 255))

    # 2. 左側平滑暗角漸層（Smoothstep Scrim），無框溶字
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fade_end = int(w * 0.58) # 約 890px
    grad_pixels = gradient.load()

    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 252 * factor
        else:
            base_alpha = 0

        for y in range(h):
            if y > int(h * 0.65):
                alpha = int(min(255, base_alpha * 1.08))
            else:
                alpha = int(base_alpha)
            # 深石板夜藍底 (8, 14, 24)
            grad_pixels[x, y] = (8, 14, 24, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 3. 文字與陰影排版
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 26)
    font_title = ImageFont.truetype(font_path, 98)
    font_sub = ImageFont.truetype(font_path, 34)
    font_action_badge = ImageFont.truetype(font_path, 30)
    font_action_core = ImageFont.truetype(font_path, 28)
    font_action_desc = ImageFont.truetype(font_path, 23)
    font_punchline = ImageFont.truetype(font_path, 24)

    start_x = 85
    start_y = 62

    # 3.1 眉標
    eng_tag = "A C T   V I I   :   R E T U R N   W I T H   T H E   E L I X I R   ｜   微 行 動 地 圖"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 3.2 核心主標（98 pt 完美雙行對仗：7字 ✕ 7字）
    line1 = "健管一點都不難！"
    line2 = "送你兩個微行動"

    y_line1 = start_y + 44
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 112
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3.3 衝擊副標（34 pt 紐崔萊琥珀金）
    sub_title = "不用挨餓、不用算卡路里，只要兩個生活好習慣！"
    y_sub = y_line2 + 130
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 3.4 兩大微行動排版
    # --- 微行動 1 ---
    y_act1 = y_sub + 68
    act1_badge = "微行動 ① 💧【把水喝足】"
    act1_core = "每天喝足「體重 × 40cc」好水"
    act1_desc = "→ 水是燃脂最便宜也最強大的燃料！啟動全身代謝大循環"

    draw_shadow.text((start_x, y_act1), act1_badge, font=font_action_badge, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_act1), act1_badge, font=font_action_badge, fill=(224, 242, 254, 255))
    bw1 = draw_text.textlength(act1_badge, font=font_action_badge)
    
    draw_shadow.text((start_x + bw1 + 10, y_act1 + 1), act1_core, font=font_action_core, fill=(0, 0, 0, 240))
    draw_text.text((start_x + bw1 + 10, y_act1 + 1), act1_core, font=font_action_core, fill=(253, 224, 71, 255)) # 金黃高亮

    draw_shadow.text((start_x + 24, y_act1 + 42), act1_desc, font=font_action_desc, fill=(0, 0, 0, 240))
    draw_text.text((start_x + 24, y_act1 + 42), act1_desc, font=font_action_desc, fill=(186, 230, 253, 230))

    # --- 微行動 2 ---
    y_act2 = y_act1 + 92
    act2_badge = "微行動 ② 🍽️【順序吃對】"
    act2_core = "先喝水 → 先吃肉 → 再吃菜 → 最後碰澱粉"
    act2_desc = "→ 穩定胰島素不飆升，下午大腦精神滿格、再也不昏睡！"

    draw_shadow.text((start_x, y_act2), act2_badge, font=font_action_badge, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_act2), act2_badge, font=font_action_badge, fill=(224, 242, 254, 255))
    bw2 = draw_text.textlength(act2_badge, font=font_action_badge)

    draw_shadow.text((start_x + 24, y_act2 + 42), act2_core, font=font_action_core, fill=(0, 0, 0, 240))
    draw_text.text((start_x + 24, y_act2 + 42), act2_core, font=font_action_core, fill=(253, 224, 71, 255))

    draw_shadow.text((start_x + 24, y_act2 + 82), act2_desc, font=font_action_desc, fill=(0, 0, 0, 240))
    draw_text.text((start_x + 24, y_act2 + 82), act2_desc, font=font_action_desc, fill=(186, 230, 253, 230))

    # 3.5 壓軸共鳴金句
    y_punch = y_act2 + 138
    punch_text = "「什麼事情都可以放下，唯獨不能放下筷子；把筷子拿穩，健康就回來了！」"
    draw_shadow.text((start_x, y_punch), punch_text, font=font_punchline, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_punch), punch_text, font=font_punchline, fill=(252, 211, 77, 255)) # 溫暖暖金

    # 4. 模糊陰影與圖層合成
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))

    final_img = Image.alpha_composite(comp_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    output_path = "generated/slide09_micro_actions_preview.png"
    final_img.convert("RGB").save(output_path, quality=95)
    print(f"Rendered Slide: {output_path}")
    return output_path

if __name__ == "__main__":
    render_micro_actions_slide()
