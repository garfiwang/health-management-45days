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
    fade_end = int(w * 0.60) # 約 920px
    grad_pixels = gradient.load()

    for x in range(w):
        if x < fade_end:
            t = x / fade_end
            factor = 1.0 - (3 * (t**2) - 2 * (t**3))
            base_alpha = 250 * factor
        else:
            base_alpha = 0

        for y in range(h):
            if y > int(h * 0.65):
                alpha = int(min(255, base_alpha * 1.08))
            else:
                alpha = int(base_alpha)
            # 深石板夜藍底 (7, 13, 24)
            grad_pixels[x, y] = (7, 13, 24, alpha)

    comp_img = Image.alpha_composite(base_img, gradient)

    # 3. 文字與陰影排版
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_eng = ImageFont.truetype(font_path, 28)
    font_title = ImageFont.truetype(font_path, 118)
    font_sub = ImageFont.truetype(font_path, 42)
    font_action_title = ImageFont.truetype(font_path, 32)
    font_action_body = ImageFont.truetype(font_path, 26)
    font_punchline = ImageFont.truetype(font_path, 26)

    start_x = 90
    start_y = 65

    # 3.1 眉標
    eng_tag = "A C T   V I I   :   R E T U R N   W I T H   T H E   E L I X I R"
    draw_shadow.text((start_x, start_y), eng_tag, font=font_eng, fill=(0, 0, 0, 220))
    draw_text.text((start_x, start_y), eng_tag, font=font_eng, fill=(52, 211, 153, 255)) # 亮青綠色

    # 3.2 核心主標（118 pt 超大震撼純白）
    line1 = "健管從來不繁瑣！"
    line2 = "明天啟動兩個「微行動」"

    y_line1 = start_y + 48
    draw_shadow.text((start_x, y_line1), line1, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line1), line1, font=font_title, fill=(255, 255, 255, 255))

    y_line2 = y_line1 + 132
    draw_shadow.text((start_x, y_line2), line2, font=font_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_line2), line2, font=font_title, fill=(255, 255, 255, 255))

    # 3.3 衝擊副標（42 pt 紐崔萊琥珀金）
    sub_title = "不用挨餓、不用算卡路里，只要兩個習慣，血糖穩定告別昏睡！"
    y_sub = y_line2 + 150
    draw_shadow.text((start_x, y_sub), sub_title, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_sub), sub_title, font=font_sub, fill=(245, 158, 11, 255))

    # 3.4 兩大微行動（32 pt 標題 + 26 pt 內文，冰晶亮藍白與薄荷綠標記）
    # 微行動 1
    y_act1 = y_sub + 78
    act1_title = "微行動 ①【把水喝足】每天喝足「體重 × 40cc」好水"
    act1_desc = "→ 脂肪燃燒最便宜也最強大的燃料！啟動全身代謝大循環"
    
    draw_shadow.text((start_x, y_act1), act1_title, font=font_action_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_act1), act1_title, font=font_action_title, fill=(224, 242, 254, 255)) # 冰晶亮藍白
    
    draw_shadow.text((start_x + 30, y_act1 + 42), act1_desc, font=font_action_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x + 30, y_act1 + 42), act1_desc, font=font_action_body, fill=(186, 230, 253, 230))

    # 微行動 2
    y_act2 = y_act1 + 95
    act2_title = "微行動 ②【順序吃對】一口水 → 一口肉 → 再吃菜 → 最後碰澱粉"
    act2_desc = "→ 穩定胰島素不飆升，下午精神飽滿、再也不會昏睡當機！"

    draw_shadow.text((start_x, y_act2), act2_title, font=font_action_title, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_act2), act2_title, font=font_action_title, fill=(224, 242, 254, 255)) # 冰晶亮藍白

    draw_shadow.text((start_x + 30, y_act2 + 42), act2_desc, font=font_action_body, fill=(0, 0, 0, 240))
    draw_text.text((start_x + 30, y_act2 + 42), act2_desc, font=font_action_body, fill=(186, 230, 253, 230))

    # 3.5 壓軸共鳴金句
    y_punch = y_act2 + 96
    punch_text = "「什麼事情都可以放下，唯獨不能放下筷子；把筷子拿穩，健康就回來了！」"
    draw_shadow.text((start_x, y_punch), punch_text, font=font_punchline, fill=(0, 0, 0, 240))
    draw_text.text((start_x, y_punch), punch_text, font=font_punchline, fill=(253, 224, 71, 255)) # 亮黃金字

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
