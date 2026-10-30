import os
from PIL import Image, ImageDraw, ImageFont

def create_slide10_wireframe():
    w, h = 1536, 864  # 真實 16:9
    img = Image.new("RGBA", (w, h), (11, 19, 36, 255))  # 頂級深海軍藍黑底
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_large_title = ImageFont.truetype(font_path, 36)
    font_sec = ImageFont.truetype(font_path, 28)
    font_body = ImageFont.truetype(font_path, 22)
    font_sub = ImageFont.truetype(font_path, 18)
    font_hero_big = ImageFont.truetype(font_path, 64)
    font_gold = ImageFont.truetype(font_path, 30)

    # 1. 畫布外框與 16:9 比例安全邊距
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=(51, 65, 85, 255), width=2)
    split_x = int(w * 0.58)  # 890px，左側文字 58%，右側人物 42%

    # 分割虛線（標記黃金比例切分）
    for y in range(40, h - 40, 16):
        draw.line([(split_x, y), (split_x, y + 8)], fill=(71, 85, 105, 255), width=2)

    # ==========================================
    # 2. 左側：無框電影大字漸層排版區 (58%)
    # ==========================================
    draw.text((60, 42), "【 區塊 A：左側 58% 視覺空間 ｜ 無框電影海報漸層溶字區 】", font=font_large_title, fill=(56, 189, 248, 255))

    # A1. 終極幕眉標
    draw.rectangle([(60, 95), (split_x - 60, 140)], outline=(52, 211, 153, 200), width=1)
    draw.text((75, 105), "ACT VIII / FINALE : THE RETURN & MASTERY（亮青綠色 24pt）", font=font_sub, fill=(52, 211, 153, 255))

    # A2. 核心主標區 (130+ pt 視覺層次)
    draw.rectangle([(60, 155), (split_x - 60, 430)], outline=(255, 255, 255, 220), width=2)
    draw.text((75, 170), "【核心主標題】純白無襯線粗體，130+ pt（大會場超遠距震撼可讀）", font=font_sub, fill=(203, 213, 225, 255))
    draw.text((75, 215), "什麼事情都可以放下", font=font_hero_big, fill=(255, 255, 255, 255))
    draw.text((75, 305), "唯獨不能放下筷子！", font=font_hero_big, fill=(255, 255, 255, 255))
    draw.text((75, 395), "（平滑暗角漸層背景，文字裸放浮現，無色塊方框壓迫感）", font=font_sub, fill=(148, 163, 184, 255))

    # A3. 衝擊副標區 (48 pt 琥珀金)
    draw.rectangle([(60, 445), (split_x - 60, 535)], outline=(245, 158, 11, 200), width=1)
    draw.text((75, 458), "【衝擊副標】紐崔萊琥珀金，48 pt", font=font_sub, fill=(245, 158, 11, 255))
    draw.text((75, 488), "好好拿穩筷子、吃對營養 ｜ 48 歲贏回人生主控權！", font=font_gold, fill=(245, 158, 11, 255))

    # A4. 靈魂心法與身體覺察金句 (30 pt 冰晶亮藍白)
    draw.rectangle([(60, 550), (split_x - 60, 680)], outline=(224, 242, 254, 200), width=1)
    draw.text((75, 562), "【靈魂金句與深層覺察】高對比冰晶亮藍白，28~30 pt", font=font_sub, fill=(224, 242, 254, 255))
    draw.text((75, 595), "「健管不是挨餓，而是覺察身體警訊，吃對每一口營養！」", font=font_body, fill=(224, 242, 254, 255))
    draw.text((75, 635), "「48 歲不是下坡路，而是人生下半場最精彩的黃金起點！」", font=font_body, fill=(186, 230, 253, 255))

    # A5. 致謝與謝幕祝福區
    draw.rectangle([(60, 695), (split_x - 60, 785)], outline=(110, 231, 183, 180), width=1)
    draw.text((75, 708), "【致謝與謝幕】溫暖翡翠薄荷綠，22 pt", font=font_sub, fill=(110, 231, 183, 255))
    draw.text((75, 735), "衷心感謝：最佳戰友 Carolyn ｜ 推薦人 沛璇 ｜ 麥淑媛教練 ｜ 寰宇南京中心", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((75, 758), "謝謝大家，祝各位 Live Better ! Better Life ✨", font=font_body, fill=(52, 211, 153, 255))

    # ==========================================
    # 3. 右側：Richman 金融男神 IP 英雄謝幕焦點 (42%)
    # ==========================================
    char_rect = [(split_x + 30, 80), (w - 40, h - 80)]
    draw.rectangle(char_rect, outline=(234, 179, 8, 220), width=2)
    draw.text((split_x + 45, 42), "【 區塊 B：右側 42% 角色焦點 ｜ 英雄歸來・自信謝幕 】", font=font_large_title, fill=(251, 191, 36, 255))

    # 人物繪製示意（頭部、身形、西裝、手勢）
    cx = split_x + int((w - split_x) * 0.5)  # 中心 x 約 1210
    
    # 紐崔萊晨曦破曉金光輪廓 (Rim Light 示意)
    draw.arc([(cx - 160, 80), (cx + 160, 400)], start=180, end=0, fill=(253, 224, 71, 160), width=4)
    draw.text((cx - 80, 95), "紐崔萊晨曦金光 (Rim Light)", font=font_sub, fill=(253, 224, 71, 255))

    # 頭部
    draw.ellipse([(cx - 75, 140), (cx + 75, 290)], outline=(255, 255, 255, 220), width=2)
    draw.text((cx - 65, 195), "Richman 48歲\n成熟型男・知性眼鏡\n從容自信感恩微笑", font=font_sub, fill=(255, 255, 255, 255))

    # 西裝身形（倒三角 Slim-fit 腰圍瘦 8cm）
    draw.polygon([(cx - 140, 310), (cx + 140, 310), (cx + 175, 730), (cx - 175, 730)], outline=(148, 163, 184, 200), width=2)
    draw.text((cx - 60, 340), "Slim-fit 深海軍藍西裝\n微解領扣・精實腰身", font=font_sub, fill=(148, 163, 184, 255))

    # 姿態動作與筷子亮點
    draw.rectangle([(split_x + 45, 420), (w - 55, 710)], outline=(59, 130, 246, 160), width=1)
    action_notes = [
        "● 核心手勢姿態（二選一或融合）：",
        "  方案甲：一手瀟灑插西裝褲口袋，另一手自信向觀眾致意，",
        "          身形挺拔、站姿 45 度，散發健康男神氣場。",
        "  方案乙：一手優雅拿著精緻筷子（呼應核心金句），",
        "          另一手溫暖放在心口或向全場致謝，象徵好好吃飯。",
        "",
        "● 視覺環境與氣氛：",
        "  背後透出紐崔萊有機農場破曉晨光，象徵穿越 45 天試煉後",
        "  迎來璀璨人生下半場，充滿生命力與希望。",
        "",
        "● 三大神隊友彩蛋：",
        "  畫面右下角可巧妙點綴 3D 公仔（巧巧、沛沛、麥麥）",
        "  微笑揮手致意，象徵一群人走得遠的圓滿結局！"
    ]
    cur_ny = 430
    for line in action_notes:
        draw.text((split_x + 60, cur_ny), line, font=font_sub, fill=(219, 234, 254, 255))
        cur_ny += 25

    # 底部狀態列
    draw.text((60, 810), "📐 畫布比例：16:9（1536 x 864）｜ 嚴禁拉伸 ｜ 提案一無框電影漸層排版 ｜ 劇場級 130+ pt 主標", font=font_sub, fill=(100, 116, 139, 255))

    out_path = "generated/slide10_wireframe_mockup.png"
    img.save(out_path)
    print(f"Wireframe mockup created: {out_path}")
    return out_path

if __name__ == "__main__":
    create_slide10_wireframe()
