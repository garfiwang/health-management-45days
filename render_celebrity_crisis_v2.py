import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_celebrity_crisis_v2(img1_path=None, img2_path=None):
    w, h = 1536, 864 # 真實 16:9
    base_img = Image.new("RGBA", (w, h), (8, 12, 22, 255)) # 極致深石板藍黑底

    cards_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    illus_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    draw_cards = ImageDraw.Draw(cards_layer)
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    
    font_eyebrow = ImageFont.truetype(font_path, 20)
    font_main_title = ImageFont.truetype(font_path, 60)
    font_subtitle = ImageFont.truetype(font_path, 26)
    
    font_tag = ImageFont.truetype(font_path, 17)
    font_card_title = ImageFont.truetype(font_path, 28)
    font_sub_info = ImageFont.truetype(font_path, 18)
    font_body = ImageFont.truetype(font_path, 19)
    font_highlight = ImageFont.truetype(font_path, 20)
    font_punchline = ImageFont.truetype(font_path, 36) # 震撼金句 36pt

    # 1. 頂部標題
    top_y = 35
    eyebrow = "S H O C K I N G   R E A L I T Y   :   T H E   S I L E N T   K I L L E R"
    draw_text.text((70, top_y), eyebrow, font=font_eyebrow, fill=(239, 68, 68, 255))

    title_text = "名人猝逝震撼彈：隱形殺手不挑人"
    draw_shadow.text((70, top_y + 30), title_text, font=font_main_title, fill=(0, 0, 0, 240))
    draw_text.text((70, top_y + 30), title_text, font=font_main_title, fill=(255, 255, 255, 255))

    subtitle_text = "無論是「拼命三郎」還是「自律養生」—— 都在人生黃金期驟然離世"
    draw_text.text((70, top_y + 105), subtitle_text, font=font_subtitle, fill=(245, 158, 11, 255))

    # 2. 雙欄卡片佈局
    card_y = 190
    card_h = 540
    card_w = 675
    
    card1_x = 70
    card2_x = 791

    # 卡片背景（高級暗藍半透明磨砂）
    draw_cards.rounded_rectangle([(card1_x, card_y), (card1_x + card_w, card_y + card_h)], radius=16, fill=(15, 23, 42, 230), outline=(239, 68, 68, 180), width=2)
    draw_cards.rounded_rectangle([(card2_x, card_y), (card2_x + card_w, card_y + card_h)], radius=16, fill=(15, 23, 42, 230), outline=(168, 85, 247, 180), width=2)

    # 3. 嵌入具象示意圖（卡片上半部，高 175px，寬 635px）
    illus_w = card_w - 40 # 635
    illus_h = 175
    illus1_pos = (card1_x + 20, card_y + 20)
    illus2_pos = (card2_x + 20, card_y + 20)

    # 插圖 1
    if img1_path and os.path.exists(img1_path):
        i1 = Image.open(img1_path).convert("RGBA")
        # 裁剪為 illus_w x illus_h
        scale = max(illus_w / i1.width, illus_h / i1.height)
        new_w, new_h = int(i1.width * scale), int(i1.height * scale)
        i1_resized = i1.resize((new_w, new_h), Image.Resampling.LANCZOS)
        crop_x = (new_w - illus_w) // 2
        crop_y = (new_h - illus_h) // 2
        i1_cropped = i1_resized.crop((crop_x, crop_y, crop_x + illus_w, crop_y + illus_h))
        
        # 圓角遮罩
        mask = Image.new("L", (illus_w, illus_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (illus_w, illus_h)], radius=10, fill=255)
        illus_layer.paste(i1_cropped, illus1_pos, mask)

    # 插圖 2
    if img2_path and os.path.exists(img2_path):
        i2 = Image.open(img2_path).convert("RGBA")
        scale = max(illus_w / i2.width, illus_h / i2.height)
        new_w, new_h = int(i2.width * scale), int(i2.height * scale)
        i2_resized = i2.resize((new_w, new_h), Image.Resampling.LANCZOS)
        crop_x = (new_w - illus_w) // 2
        crop_y = (new_h - illus_h) // 2
        i2_cropped = i2_resized.crop((crop_x, crop_y, crop_x + illus_w, crop_y + illus_h))
        
        mask = Image.new("L", (illus_w, illus_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (illus_w, illus_h)], radius=10, fill=255)
        illus_layer.paste(i2_cropped, illus2_pos, mask)

    # 4. 卡片下半部文字資訊
    info_y = card_y + illus_h + 35

    # === 左卡文字 ===
    # 標籤
    draw_cards.rounded_rectangle([(card1_x + 20, info_y), (card1_x + 230, info_y + 28)], radius=6, fill=(220, 38, 38, 255))
    draw_text.text((card1_x + 30, info_y + 4), "象徵：過勞高壓 ✕ 心血管猝逝", font=font_tag, fill=(255, 255, 255, 255))

    # 人物名與年齡
    draw_text.text((card1_x + 20, info_y + 38), "承億文旅創辦人 戴俊郎", font=font_card_title, fill=(255, 255, 255, 255))
    draw_text.text((card1_x + 390, info_y + 45), "享年 54 歲", font=font_sub_info, fill=(252, 165, 165, 255))

    # 事實重點
    bullets1 = [
        "● 業界公認【拼命三郎】，台灣文創旅店龍頭推手",
        "● 近年罹患心血管疾病，持續服藥控制多年",
        "● 母親節前夕於工作室失聯，突發多發性腦溢血驟逝",
        "⚠️ 警訊：以為「有吃藥控制」就沒事？血管早已不堪重負！"
    ]
    by = info_y + 80
    for b in bullets1:
        if "⚠️" in b:
            draw_text.text((card1_x + 20, by), b, font=font_highlight, fill=(248, 113, 113, 255))
        else:
            draw_text.text((card1_x + 20, by), b, font=font_body, fill=(241, 245, 249, 255))
        by += 32

    # === 右卡文字 ===
    # 標籤
    draw_cards.rounded_rectangle([(card2_x + 20, info_y), (card2_x + 240, info_y + 28)], radius=6, fill=(147, 51, 234, 255))
    draw_text.text((card2_x + 30, info_y + 4), "象徵：茹素運動 ✕ 突發腦栓塞", font=font_tag, fill=(255, 255, 255, 255))

    # 人物名與年齡
    draw_text.text((card2_x + 20, info_y + 38), "福華飯店第三代 廖國宏", font=font_card_title, fill=(255, 255, 255, 255))
    draw_text.text((card2_x + 390, info_y + 45), "享年 55 歲", font=font_sub_info, fill=(216, 180, 254, 255))

    # 事實重點
    bullets2 = [
        "● 【長期茹素、不抽菸、不喝酒】，極端自律注重養生",
        "● 規律維持【每天健走、打網球】，體態精實事業有成",
        "● 返台下機突發抽搐，腦血栓合併腦幹出血無法開刀",
        "⚠️ 警訊：以為「吃素運動」就免疫？隱形腦血栓依然無聲致命！"
    ]
    by2 = info_y + 80
    for b in bullets2:
        if "⚠️" in b:
            draw_text.text((card2_x + 20, by2), b, font=font_highlight, fill=(192, 132, 252, 255))
        else:
            draw_text.text((card2_x + 20, by2), b, font=font_body, fill=(241, 245, 249, 255))
        by2 += 32

    # 5. 底部震撼金句（依 Rich 指定改為：「猝死從來不挑人！身體直接停機登出！」）
    punchline = "「猝死從來不挑人！身體直接停機登出！」"
    py = 770
    draw_shadow.text((70, py), punchline, font=font_punchline, fill=(0, 0, 0, 255))
    draw_text.text((70, py), punchline, font=font_punchline, fill=(224, 242, 254, 255)) # 冰晶亮藍白超大字

    # 陰影模糊與圖層合成
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))
    
    final_img = Image.alpha_composite(base_img, cards_layer)
    final_img = Image.alpha_composite(final_img, illus_layer)
    final_img = Image.alpha_composite(final_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide_celebrity_sudden_death_v2.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered V2 slide: {out_path}")
    return out_path

if __name__ == "__main__":
    render_celebrity_crisis_v2()
