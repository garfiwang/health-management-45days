import os
from PIL import Image, ImageDraw, ImageFont

def render_slide10_draft_preview():
    w, h = 1536, 864
    bg_path = "generated/slide10_nanobanana_sketch_draft.png"
    if os.path.exists(bg_path):
        base = Image.open(bg_path).convert("RGBA")
    else:
        base = Image.new("RGBA", (w, h), (11, 19, 36, 255))

    # 左側 58% 平滑暗角漸層（Smoothstep Scrim），確保左側文字極致清晰
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    for x in range(w):
        if x < int(w * 0.42):
            alpha = 230
        elif x < int(w * 0.62):
            t = (x - int(w * 0.42)) / (int(w * 0.62) - int(w * 0.42))
            alpha = int(230 * (1 - (3 * t**2 - 2 * t**3)))
        else:
            alpha = 0
        scrim_draw.line([(x, 0), (x, h)], fill=(11, 19, 36, alpha))

    comp = Image.alpha_composite(base, scrim)
    draw = ImageDraw.Draw(comp)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_badge = ImageFont.truetype(font_path, 22)
    font_hero = ImageFont.truetype(font_path, 68)
    font_gold = ImageFont.truetype(font_path, 34)
    font_quote = ImageFont.truetype(font_path, 23)
    font_body = ImageFont.truetype(font_path, 21)
    font_meta = ImageFont.truetype(font_path, 19)

    left_x = 75

    # 1. 頂部徽章標籤
    badge_text = "ACT VIII / FINALE : THE RETURN & MASTERY ｜ 英雄謝幕"
    draw.rounded_rectangle([(left_x, 48), (left_x + 580, 88)], radius=6, fill=(16, 185, 129, 210))
    draw.text((left_x + 18, 56), badge_text, font=font_badge, fill=(255, 255, 255, 255))

    # 2. 核心主標題 (130+ pt 視覺重量)
    draw.text((left_x, 125), "什麼事情都可以放下", font=font_hero, fill=(255, 255, 255, 255))
    draw.text((left_x, 215), "唯獨不能放下筷子！", font=font_hero, fill=(255, 255, 255, 255))

    # 3. 紐崔萊琥珀金衝擊副標
    draw.text((left_x, 325), "好好拿穩筷子、吃對營養 ｜ 48 歲贏回人生主控權！", font=font_gold, fill=(245, 158, 11, 255))

    # 4. 黑色幽默與警訊破除（冰晶亮藍白）
    draw.text((left_x, 395), "健管從來不是挨餓節食，而是好好覺察身體的每一聲微小警訊；", font=font_quote, fill=(224, 242, 254, 255))
    draw.text((left_x, 435), "所有開心的、不開心的、任何忙碌都可以放下，請注意聽身體的聲音！", font=font_quote, fill=(224, 242, 254, 255))
    draw.text((left_x, 475), "千萬不要等身體開始罷工了，才驚覺來不及！", font=font_quote, fill=(254, 202, 202, 255))

    # 5. 48 歲逆生長昇華金句
    draw.rounded_rectangle([(left_x, 530), (left_x + 780, 625)], radius=10, fill=(15, 23, 42, 190), outline=(56, 189, 248, 160), width=1)
    draw.text((left_x + 22, 545), "45 天前，我以為我只是在管理體重；45 天後，我發現我贏回了主控權。", font=font_body, fill=(224, 242, 254, 255))
    draw.text((left_x + 22, 582), "48 歲，這絕不是下坡路，而是人生下半場最精彩的黃金起點！", font=font_body, fill=(56, 189, 248, 255))

    # 6. 致謝與結尾祝福
    draw.text((left_x, 660), "衷心感謝：最佳戰友 Carolyn ｜ 推薦人 沛璇 ｜ 麥淑媛教練 ｜ 寰宇南京中心", font=font_meta, fill=(148, 163, 184, 255))
    draw.text((left_x, 705), "謝謝大家，祝各位 Live Better ! Better Life ✨", font=ImageFont.truetype(font_path, 28), fill=(52, 211, 153, 255))

    out_p = "generated/slide10_concept_preview_with_text.png"
    comp.convert("RGB").save(out_p, quality=95)
    print("Rendered Draft Preview with Text:", out_p)
    return out_p

if __name__ == "__main__":
    render_slide10_draft_preview()
