import os
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_celebrity_crisis_slide(bg_image_path=None):
    w, h = 1536, 864 # 真實 16:9
    
    # 1. 準備背景
    if bg_image_path and os.path.exists(bg_image_path):
        raw_bg = Image.open(bg_image_path).convert("RGBA")
        rw, rh = raw_bg.size
        # 精準 16:9 裁切
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
        # 深石板夜色漸層底
        base_img = Image.new("RGBA", (w, h), (10, 15, 26, 255))

    # 暗角遮罩（確保文字極度清晰）
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scrim_pixels = scrim.load()
    for y in range(h):
        for x in range(w):
            # 頂部與底部加深
            factor_y = 0.65
            if y < 180:
                factor_y = 0.85
            elif y > h - 140:
                factor_y = 0.88
            scrim_pixels[x, y] = (5, 9, 18, int(220 * factor_y))

    comp_img = Image.alpha_composite(base_img, scrim)

    # 2. 建立卡片與文字圖層
    cards_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    draw_cards = ImageDraw.Draw(cards_layer)
    draw_text = ImageDraw.Draw(text_layer)
    draw_shadow = ImageDraw.Draw(shadow_layer)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_bold_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    
    font_eyebrow = ImageFont.truetype(font_path, 22)
    font_main_title = ImageFont.truetype(font_bold_path, 64)
    font_subtitle = ImageFont.truetype(font_path, 28)
    
    font_tag = ImageFont.truetype(font_bold_path, 18)
    font_card_title = ImageFont.truetype(font_bold_path, 32)
    font_sub_info = ImageFont.truetype(font_path, 20)
    font_body = ImageFont.truetype(font_path, 21)
    font_highlight = ImageFont.truetype(font_bold_path, 22)
    font_quote = ImageFont.truetype(font_bold_path, 26)

    # ---------------- 頂部標題區 ----------------
    top_y = 45
    # 眉標
    eyebrow = "S H O C K I N G   R E A L I T Y   :   T H E   S I L E N T   K I L L E R"
    draw_text.text((80, top_y), eyebrow, font=font_eyebrow, fill=(239, 68, 68, 255)) # 警示紅

    # 主標題
    title_text = "名人猝逝震撼彈：隱形殺手不挑人"
    draw_shadow.text((80, top_y + 35), title_text, font=font_main_title, fill=(0, 0, 0, 240))
    draw_text.text((80, top_y + 35), title_text, font=font_main_title, fill=(255, 255, 255, 255))

    # 副標題
    subtitle_text = "無論是「拼命三郎」還是「自律養生」—— 都在人生黃金期驟然離世"
    draw_text.text((80, top_y + 115), subtitle_text, font=font_subtitle, fill=(245, 158, 11, 255)) # 琥珀金

    # ---------------- 雙欄對比卡片區 ----------------
    card_y = 230
    card_h = 490
    card_w = 660
    
    card1_x = 80
    card2_x = 796

    # 卡片 1 背景 (左：戴俊郎)
    draw_cards.rounded_rectangle([(card1_x, card_y), (card1_x + card_w, card_y + card_h)], radius=16, fill=(15, 23, 42, 215), outline=(239, 68, 68, 160), width=2)
    
    # 卡片 2 背景 (右：廖國宏)
    draw_cards.rounded_rectangle([(card2_x, card_y), (card2_x + card_w, card_y + card_h)], radius=16, fill=(15, 23, 42, 215), outline=(168, 85, 247, 160), width=2)

    # === 左卡內容（案例一：拼命三郎型） ===
    # 標籤
    tag1_w = 200
    tag1_h = 32
    draw_cards.rounded_rectangle([(card1_x + 30, card_y + 30), (card1_x + 30 + tag1_w, card_y + 30 + tag1_h)], radius=6, fill=(220, 38, 38, 240))
    draw_text.text((card1_x + 42, card_y + 35), "過勞高壓 ✕ 心血管猝逝", font=font_tag, fill=(255, 255, 255, 255))

    # 人物名與年齡
    draw_text.text((card1_x + 30, card_y + 75), "承億文旅創辦人 戴俊郎", font=font_card_title, fill=(255, 255, 255, 255))
    draw_text.text((card1_x + 420, card_y + 82), "享年 54 歲", font=font_sub_info, fill=(252, 165, 165, 255))

    # 身份身家
    draw_text.text((card1_x + 30, card_y + 125), "▪ 台灣最大文創旅店集團推手，事業如日中天", font=font_sub_info, fill=(148, 163, 184, 255))

    # 分隔線
    draw_cards.line([(card1_x + 30, card_y + 160), (card1_x + card_w - 30, card_y + 160)], fill=(51, 65, 85, 200), width=1)

    # 事實點
    bullets1 = [
        "● 被業界視為事業上的【拼命三郎】，常年高壓拚搏",
        "● 近年罹患心血管疾病，並持續服藥控制多年",
        "● 母親節前夕於工作室失聯，發現時已無生命跡象",
        "● 死因：突發多發性腦溢血，各界震驚痛惜"
    ]
    cur_y = card_y + 185
    for b in bullets1:
        draw_text.text((card1_x + 30, cur_y), b, font=font_body, fill=(241, 245, 249, 255))
        cur_y += 42

    # 警示框小結
    draw_cards.rounded_rectangle([(card1_x + 30, card_y + 380), (card1_x + card_w - 30, card_y + 450)], radius=8, fill=(30, 41, 59, 230), outline=(239, 68, 68, 100), width=1)
    draw_text.text((card1_x + 50, card_y + 395), "⚠️ 警訊破除：以為「有吃藥控制」就沒事？", font=font_highlight, fill=(248, 113, 113, 255))
    draw_text.text((card1_x + 50, card_y + 422), "長期過勞與睡眠不足，血管隨時可能發生致命撕裂！", font=font_sub_info, fill=(203, 213, 225, 255))

    # === 右卡內容（案例二：自律養生型） ===
    # 標籤
    tag2_w = 210
    tag2_h = 32
    draw_cards.rounded_rectangle([(card2_x + 30, card_y + 30), (card2_x + 30 + tag2_w, card_y + 30 + tag2_h)], radius=6, fill=(147, 51, 234, 240))
    draw_text.text((card2_x + 42, card_y + 35), "茹素運動 ✕ 突發腦栓塞", font=font_tag, fill=(255, 255, 255, 255))

    # 人物名與年齡
    draw_text.text((card2_x + 30, card_y + 75), "福華飯店第三代 廖國宏", font=font_card_title, fill=(255, 255, 255, 255))
    draw_text.text((card2_x + 420, card_y + 82), "享年 55 歲", font=font_sub_info, fill=(216, 180, 254, 255))

    # 身份身家
    draw_text.text((card2_x + 30, card_y + 125), "▪ 掌舵福華核心管理、熱心國際公益，青壯有為", font=font_sub_info, fill=(148, 163, 184, 255))

    # 分隔線
    draw_cards.line([(card2_x + 30, card_y + 160), (card2_x + card_w - 30, card_y + 160)], fill=(51, 65, 85, 200), width=1)

    # 事實點
    bullets2 = [
        "● 【長期茹素、不抽菸、不喝酒】，生活極端自律注重養生",
        "● 規律維持【每天健走、打網球】等高強度運動習慣",
        "● 8/15 返台剛下機突發抽搐，緊急取出腦血栓",
        "● 因出血位於【腦幹無法開刀】，搶救 10 多天不幸離世"
    ]
    cur_y = card_y + 185
    for b in bullets2:
        draw_text.text((card2_x + 30, cur_y), b, font=font_body, fill=(241, 245, 249, 255))
        cur_y += 42

    # 警示框小結
    draw_cards.rounded_rectangle([(card2_x + 30, card_y + 380), (card2_x + card_w - 30, card_y + 450)], radius=8, fill=(30, 41, 59, 230), outline=(168, 85, 247, 100), width=1)
    draw_text.text((card2_x + 50, card_y + 395), "⚠️ 迷思打破：以為「吃素運動不菸不酒」就免疫？", font=font_highlight, fill=(192, 132, 252, 255))
    draw_text.text((card2_x + 50, card_y + 422), "忽略深層代謝發炎與內皮斑塊，隱形腦血栓依舊無聲致命！", font=font_sub_info, fill=(203, 213, 225, 255))

    # ---------------- 底部靈魂拷問區 ----------------
    bottom_y = 750
    quote_text = "「猝死從來不挑人！你還以為自己有積福報、很健康，身體就不會抗議嗎？」"
    draw_shadow.text((80, bottom_y), quote_text, font=font_quote, fill=(0, 0, 0, 240))
    draw_text.text((80, bottom_y), quote_text, font=font_quote, fill=(224, 242, 254, 255)) # 冰晶亮藍白

    # 陰影模糊並合成
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=6))
    final_img = Image.alpha_composite(comp_img, cards_layer)
    final_img = Image.alpha_composite(final_img, shadow_blurred)
    final_img = Image.alpha_composite(final_img, text_layer)

    out_path = "generated/slide_celebrity_sudden_death_preview.png"
    final_img.convert("RGB").save(out_path, quality=95)
    print(f"Rendered slide: {out_path}")
    return out_path

if __name__ == "__main__":
    render_celebrity_crisis_slide()
