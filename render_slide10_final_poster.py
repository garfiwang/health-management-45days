import os
import glob
from PIL import Image, ImageDraw, ImageFont

def render_slide10_poster(bg_image_path=None):
    w, h = 1536, 864  # 真實 16:9

    # 若未指定背景，自動搜尋最新的 slide10_richman_openai
    if not bg_image_path or not os.path.exists(bg_image_path):
        candidates = sorted(glob.glob("generated/slide10_richman_openai*.png"))
        if candidates:
            bg_image_path = candidates[-1]
        else:
            # 備援使用使用者上傳的 IP 參考圖
            bg_image_path = "/Users/garfiwang/.gemini/antigravity/brain/5a31b131-0cdf-466b-be7c-38835e8014bc/.user_uploaded/media_1793321019564_78f40c6a.jpg"

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

    # 2. 左側平滑暗角漸層（Smoothstep Scrim），左側 58% 保留給文字，平滑溶入右側自然光影
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    # 起始暗角 x 0~620 為深海軍藍黑，x 620~950 為 smoothstep 漸層褪去
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
    font_hero_1 = ImageFont.truetype(font_path, 66)
    font_gold = ImageFont.truetype(font_path, 34)
    font_quote = ImageFont.truetype(font_path, 22)
    font_card_lead = ImageFont.truetype(font_path, 22)
    font_card_punch = ImageFont.truetype(font_path, 24)
    font_ack_title = ImageFont.truetype(font_path, 19)
    font_farewell = ImageFont.truetype(font_path, 26)

    left_x = 75

    # 3. 頂部徽章
    draw.rounded_rectangle([(left_x, 42), (left_x + 560, 82)], radius=6, fill=(16, 185, 129, 230))
    draw.text((left_x + 18, 50), "ACT VIII / FINALE : THE RETURN & MASTERY ｜ 英雄謝幕", font=font_badge, fill=(255, 255, 255, 255))

    # 4. 核心主標題（130+ pt 視覺重量，分行疊加呈現）
    draw.text((left_x, 112), "什麼事情都可以放下", font=font_hero_1, fill=(255, 255, 255, 255))
    draw.text((left_x, 198), "唯獨不能放下筷子！", font=font_hero_1, fill=(255, 255, 255, 255))

    # 5. 紐崔萊琥珀金衝擊副標
    draw.text((left_x, 298), "好好拿穩筷子、吃對營養 ｜ 48 歲贏回人生主控權！", font=font_gold, fill=(245, 158, 11, 255))

    # 6. 心法與身體覺察金句（冰晶亮藍白 ＋ 警示粉紅）
    draw.text((left_x, 362), "健管從來不是叫我們放下筷子挨餓節食，而是好好吃對每一口營養；", font=font_quote, fill=(224, 242, 254, 255))
    draw.text((left_x, 398), "所有開心的、不開心的事情，任何忙碌都可以放下，請好好覺察身體的警訊！", font=font_quote, fill=(224, 242, 254, 255))
    draw.text((left_x, 434), "千萬不要等身體開始罷工了才發現，那就真的來不及了！", font=font_quote, fill=(254, 202, 202, 255))

    # 7. 48 歲逆生長昇華卡片
    card_w, card_h = 790, 110
    card_y = 485
    draw.rounded_rectangle([(left_x, card_y), (left_x + card_w, card_y + card_h)], radius=12, fill=(15, 23, 42, 210), outline=(56, 189, 248, 170), width=1)
    draw.text((left_x + 24, card_y + 18), "45 天前，我以為我只是在管理體重；45 天後，我發現我贏回了人生的主控權。", font=font_card_lead, fill=(224, 242, 254, 255))
    draw.text((left_x + 24, card_y + 58), "48 歲，這絕不是下坡路，而是人生下半場最精彩的黃金起點！", font=font_card_punch, fill=(56, 189, 248, 255))

    # 8. 溫暖致謝與結尾祝福
    draw.text((left_x, 625), "衷心感謝：最佳戰友 Carolyn ｜ 推薦人 沛璇 ｜ 麥淑媛教練 ｜ 寰宇南京中心全體夥伴", font=font_ack_title, fill=(148, 163, 184, 255))
    draw.text((left_x, 665), "謝謝大家，祝各位 Live Better ! Better Life !", font=font_farewell, fill=(52, 211, 153, 255))

    out_path = "generated/slide10_grand_finale_poster.png"
    comp.convert("RGB").save(out_path, quality=95)
    print(f"Rendered Slide 10 Grand Finale Poster: {out_path}")
    return out_path

if __name__ == "__main__":
    render_slide10_poster()
