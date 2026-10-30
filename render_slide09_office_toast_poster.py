import os
import glob
from PIL import Image, ImageDraw, ImageFont

def render_slide09_office_toast_poster(bg_image_path=None):
    w, h = 1536, 864  # 真實 16:9

    if not bg_image_path or not os.path.exists(bg_image_path):
        candidates = sorted(glob.glob("generated/slide09_office_toast_openai*.png"))
        if candidates:
            bg_image_path = candidates[-1]
        else:
            print("Background image not found yet.")
            return None

    print(f"Using background image: {bg_image_path}")
    raw_bg = Image.open(bg_image_path).convert("RGBA")
    rw, rh = raw_bg.size

    # 1. 精準裁切為真實 16:9（1.777778），絕不拉伸
    target_ratio = 16.0 / 9.0
    cur_ratio = rw / rh
    if cur_ratio > target_ratio:
        tw = int(rh * target_ratio)
        cx = (rw - tw) // 2
        cropped = raw_bg.crop((cx, 0, cx + tw, rh))
    else:
        th = int(rw / target_ratio)
        cy = (rh - th) // 2
        cropped = raw_bg.crop((0, cy, rw, cy + th))

    base_img = cropped.resize((w, h), Image.Resampling.LANCZOS)

    # 2. 左側平滑暗角漸層（Smoothstep Scrim），左側 58% 保留給文字，平滑溶入右側辦公室天光
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    x0, x1 = int(w * 0.40), int(w * 0.62)
    for x in range(w):
        if x < x0:
            alpha = 240
        elif x < x1:
            t = (x - x0) / (x1 - x0)
            st = 3 * t**2 - 2 * t**3
            alpha = int(240 * (1 - st))
        else:
            alpha = 0
        scrim_draw.line([(x, 0), (x, h)], fill=(7, 11, 20, alpha))

    comp = Image.alpha_composite(base_img, scrim)
    draw = ImageDraw.Draw(comp)

    # 字型載入
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_badge = ImageFont.truetype(font_path, 21)
    font_hero = ImageFont.truetype(font_path, 66)
    font_gold = ImageFont.truetype(font_path, 34)
    
    font_action_title = ImageFont.truetype(font_path, 34)
    font_action_core = ImageFont.truetype(font_path, 28)
    font_action_desc = ImageFont.truetype(font_path, 21)

    left_x = 75

    # 3. 頂部徽章
    draw.rounded_rectangle([(left_x, 46), (left_x + 580, 86)], radius=6, fill=(16, 185, 129, 230))
    draw.text((left_x + 18, 54), "ACT VII : RETURN WITH THE ELIXIR ｜ 微行動地圖", font=font_badge, fill=(255, 255, 255, 255))

    # 4. 核心主標題（110+ pt 視覺重量，純白無襯線粗體）
    draw.text((left_x, 118), "健管一點都不難！", font=font_hero, fill=(255, 255, 255, 255))
    draw.text((left_x, 202), "送你兩個微行動", font=font_hero, fill=(255, 255, 255, 255))

    # 5. 紐崔萊琥珀金衝擊副標
    draw.text((left_x, 305), "不用挨餓、不用算卡路里，只要兩個生活好習慣！", font=font_gold, fill=(245, 158, 11, 255))

    # 6. 微行動 ① 【把水喝足】
    card1_y = 375
    draw.text((left_x, card1_y), "微行動 ① 【把水喝足】", font=font_action_title, fill=(224, 242, 254, 255))
    draw.text((left_x + 30, card1_y + 48), "每天喝足「體重 × 40cc」好水", font=font_action_core, fill=(253, 224, 71, 255))
    draw.text((left_x + 30, card1_y + 92), "→ 水是燃脂最便宜也最強大的燃料！啟動全身代謝大循環", font=font_action_desc, fill=(186, 230, 253, 255))

    # 7. 微行動 ② 【順序吃對】
    card2_y = 550
    draw.text((left_x, card2_y), "微行動 ② 【順序吃對】", font=font_action_title, fill=(224, 242, 254, 255))
    draw.text((left_x + 30, card2_y + 48), "先喝水 → 先吃肉 → 再吃菜 → 最後碰澱粉", font=font_action_core, fill=(253, 224, 71, 255))
    draw.text((left_x + 30, card2_y + 92), "→ 穩定胰島素不飆升，下午大腦精神滿格、再也不昏睡當機！", font=font_action_desc, fill=(186, 230, 253, 255))

    # 底部精神標注
    draw.text((left_x, 725), "告別午後疲憊昏睡 ｜ 啟動大腦巔峰效能 ｜ 隨時隨地輕鬆實踐", font=ImageFont.truetype(font_path, 21), fill=(52, 211, 153, 255))

    out_path = "generated/slide09_office_toast_poster.png"
    comp.convert("RGB").save(out_path, quality=95)
    print(f"Rendered Slide 09 Office Toast Poster: {out_path}")
    return out_path

if __name__ == "__main__":
    render_slide09_office_toast_poster()
