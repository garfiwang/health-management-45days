import os
from PIL import Image, ImageDraw, ImageFont

def create_slide09_wireframe():
    w, h = 1536, 864  # 真實 16:9
    img = Image.new("RGBA", (w, h), (11, 19, 36, 255))  # 深海軍藍底
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_large_title = ImageFont.truetype(font_path, 34)
    font_sec = ImageFont.truetype(font_path, 28)
    font_body = ImageFont.truetype(font_path, 22)
    font_sub = ImageFont.truetype(font_path, 18)
    font_hero_big = ImageFont.truetype(font_path, 60)
    font_gold = ImageFont.truetype(font_path, 30)

    # 1. 畫布外框與 16:9 比例安全邊距
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=(51, 65, 85, 255), width=2)
    split_x = int(w * 0.58)  # 890px，左側文字 58%，右側人物 42%

    # 分割虛線（黃金比例切分線）
    for y in range(40, h - 40, 16):
        draw.line([(split_x, y), (split_x, y + 8)], fill=(71, 85, 105, 255), width=2)

    # ==========================================
    # 2. 左側：文字排版區 (58%)
    # ==========================================
    draw.text((60, 40), "【 區塊 A：左側 58% 視覺空間 ｜ 無框電影海報漸層溶字區 】", font=font_large_title, fill=(56, 189, 248, 255))

    # A1. 頂部徽章
    draw.rectangle([(60, 90), (split_x - 60, 135)], outline=(52, 211, 153, 200), width=1)
    draw.text((75, 100), "ACT VII : RETURN WITH THE ELIXIR ｜ 微行動地圖（亮青綠色 22pt）", font=font_sub, fill=(52, 211, 153, 255))

    # A2. 核心主標區 (110+ pt 視覺重量)
    draw.rectangle([(60, 150), (split_x - 60, 375)], outline=(255, 255, 255, 220), width=2)
    draw.text((75, 165), "【核心主標題】純白無襯線粗體，110+ pt", font=font_sub, fill=(203, 213, 225, 255))
    draw.text((75, 205), "健管一點都不難！", font=font_hero_big, fill=(255, 255, 255, 255))
    draw.text((75, 280), "送你兩個微行動", font=font_hero_big, fill=(255, 255, 255, 255))

    # A3. 琥珀金副標區
    draw.rectangle([(60, 390), (split_x - 60, 460)], outline=(245, 158, 11, 200), width=1)
    draw.text((75, 402), "【衝擊副標】紐崔萊琥珀金，32 pt", font=font_sub, fill=(245, 158, 11, 255))
    draw.text((75, 424), "不用挨餓、不用算卡路里，只要兩個生活好習慣！", font=font_gold, fill=(245, 158, 11, 255))

    # A4. 微行動 ① 卡片
    draw.rounded_rectangle([(60, 475), (split_x - 60, 615)], radius=10, outline=(56, 189, 248, 220), width=2)
    draw.text((75, 490), "微行動 ① 【把水喝足】（冰晶亮藍 32pt 放大級）", font=font_sec, fill=(56, 189, 248, 255))
    draw.text((75, 532), "每天喝足「體重 × 40cc」好水", font=ImageFont.truetype(font_path, 25), fill=(253, 224, 71, 255))
    draw.text((75, 572), "→ 水是燃脂最便宜也最強大的燃料！啟動全身代謝大循環", font=font_sub, fill=(224, 242, 254, 255))

    # A5. 微行動 ② 卡片
    draw.rounded_rectangle([(60, 630), (split_x - 60, 775)], radius=10, outline=(52, 211, 153, 220), width=2)
    draw.text((75, 645), "微行動 ② 【順序吃對】（翡翠薄荷綠 32pt 放大級）", font=font_sec, fill=(52, 211, 153, 255))
    draw.text((75, 687), "先喝水 → 先吃肉 → 再吃菜 → 最後碰澱粉", font=ImageFont.truetype(font_path, 25), fill=(253, 224, 71, 255))
    draw.text((75, 727), "→ 穩定胰島素不飆升，下午大腦精神滿格、再也不昏睡當機！", font=font_sub, fill=(224, 242, 254, 255))

    # ==========================================
    # 3. 右側：新場景與新動作 方案構想規劃區 (42%)
    # ==========================================
    char_rect = [(split_x + 30, 80), (w - 40, h - 80)]
    draw.rectangle(char_rect, outline=(234, 179, 8, 220), width=2)
    draw.text((split_x + 45, 40), "【 區塊 B：右側 42% 角色新場景與新動作規劃 】", font=font_large_title, fill=(251, 191, 36, 255))

    cx = split_x + int((w - split_x) * 0.5)

    # 方案一：現代極簡廚房中島
    draw.rounded_rectangle([(split_x + 45, 95), (w - 55, 305)], radius=8, outline=(56, 189, 248, 180), width=1)
    draw.text((split_x + 60, 108), "【提案一・首選】現代極簡中島・手持水杯示範（生活大師）", font=font_body, fill=(56, 189, 248, 255))
    draw.text((split_x + 60, 142), "● 場景：大理石極簡開放式廚房中島，晨光透過玻璃灑落", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 172), "● 動作：Richman 側身微倚中島，右手端著高透明大水杯剛剛喝下一口，", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 202), "        左手自然比出「OK/讚/輕鬆指引」手勢，神采奕奕直視觀眾", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 232), "● 道具：中島檯面擺放精緻原形食物盤（西蘭花、雞肉、水），呼應兩大微行動", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 262), "● 氛圍：溫暖親切、日常生活易於實踐，徹底消除戶外擺拍的刻意感", font=font_sub, fill=(253, 224, 71, 255))

    # 方案二：高樓行政總裁辦公室
    draw.rounded_rectangle([(split_x + 45, 325), (w - 55, 535)], radius=8, outline=(168, 85, 247, 180), width=1)
    draw.text((split_x + 60, 338), "【提案二】高樓明亮辦公室・精力充沛職場男神", font=font_body, fill=(192, 132, 252, 255))
    draw.text((split_x + 60, 372), "● 場景：俯瞰城市天際線的現代高樓辦公室落地窗旁", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 402), "● 動作：一手插西裝口袋，另一手端起大水杯自信向觀眾敬酒（Toast 姿態），", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 432), "        站姿挺拔俐落，眼神專注知性，微風微動髮絲", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 462), "● 意象：打破「下午昏睡需要靠三杯咖啡」的狼狽，", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 492), "        展現「靠喝好水與順序吃，下午大腦全滿格」的商務男神狀態", font=font_sub, fill=(253, 224, 71, 255))

    # 方案三：純色舞台光影極簡特寫
    draw.rounded_rectangle([(split_x + 45, 555), (w - 55, 755)], radius=8, outline=(52, 211, 153, 180), width=1)
    draw.text((split_x + 60, 568), "【提案三】演講舞台光影・自信致敬（演講家風範）", font=font_body, fill=(52, 211, 153, 255))
    draw.text((split_x + 60, 602), "● 場景：純淨深藍色背景，右後方有紐崔萊破曉晨光輪廓金光（Rim Light）", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 632), "● 動作：48歲成熟男神半身微仰角，雙手自然攤開或一手指引向前，", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 662), "        如同在舞台上親切與觀眾互動：「跟我一起做，就是這麼簡單！」", font=font_sub, fill=(226, 232, 240, 255))
    draw.text((split_x + 60, 692), "● 優點：畫面無多餘雜物，人物神情與左側微行動字句具備最強烈視覺張力", font=font_sub, fill=(253, 224, 71, 255))

    # 底部狀態列
    draw.text((60, 810), "📐 畫布比例：16:9（1536 x 864）｜ 嚴格遵守「只給線圖草圖，不淮直接生圖」｜ 請確認新場景與動作方案", font=font_sub, fill=(148, 163, 184, 255))

    out_path = "generated/slide09_wireframe_sketch.png"
    img.save(out_path)
    print(f"Wireframe sketch created: {out_path}")
    return out_path

if __name__ == "__main__":
    create_slide09_wireframe()
