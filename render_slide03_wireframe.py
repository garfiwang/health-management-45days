import os
from PIL import Image, ImageDraw, ImageFont

def create_wireframe():
    w, h = 1536, 864 # 真實 16:9
    img = Image.new("RGBA", (w, h), (15, 23, 42, 255)) # 深石板藍底
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    font_large = ImageFont.truetype(font_path, 42)
    font_title = ImageFont.truetype(font_path, 32)
    font_text = ImageFont.truetype(font_path, 24)
    font_desc = ImageFont.truetype(font_path, 20)

    # 1. 畫出 16:9 外框與中心/黃金比例輔助線
    draw.rectangle([(20, 20), (w-20, h-20)], outline=(51, 65, 85, 255), width=2)
    split_x = int(w * 0.56) # 860px，左側文字 56%，右側人物 44%

    # 分割虛線
    for y in range(40, h-40, 15):
        draw.line([(split_x, y), (split_x, y+8)], fill=(71, 85, 105, 255), width=2)

    # 2. 左側：無框電影大字排版區 (56%)
    draw.text((60, 45), "【 區塊 A：左側 56% 視覺空間 ｜ 無框電影大字溶字區 】", font=font_title, fill=(56, 189, 248, 255))

    # A1. 眉標區
    draw.rectangle([(60, 100), (split_x - 60, 145)], outline=(52, 211, 153, 180), width=1)
    draw.text((75, 110), "ACT II : THE CALL TO ADVENTURE（亮青綠色 30pt）", font=font_desc, fill=(52, 211, 153, 255))

    # A2. 核心主標區 (130+ pt)
    draw.rectangle([(60, 165), (split_x - 60, 470)], outline=(255, 255, 255, 200), width=2)
    draw.text((75, 180), "核心主標題（純白無襯線粗體，130+ pt）", font=font_title, fill=(255, 255, 255, 255))
    draw.text((75, 240), "身體的兩記重擊", font=ImageFont.truetype(font_path, 68), fill=(255, 255, 255, 255))
    draw.text((75, 330), "痛風與血壓 160", font=ImageFont.truetype(font_path, 68), fill=(255, 255, 255, 255))
    draw.text((75, 430), "（左側 58% 平滑暗角溶字，大螢幕遠距 100% 震撼辨識）", font=font_desc, fill=(148, 163, 184, 255))

    # A3. 衝擊副標區 (52 pt)
    draw.rectangle([(60, 490), (split_x - 60, 590)], outline=(245, 158, 11, 200), width=1)
    draw.text((75, 505), "衝擊副標題（紐崔萊琥珀金，52 pt）", font=font_text, fill=(245, 158, 11, 255))
    draw.text((75, 540), "半夜膝蓋痛到發瘋，自創 168 差點休克", font=ImageFont.truetype(font_path, 30), fill=(245, 158, 11, 255))

    # A4. 黑色幽默金句區 (30 pt)
    draw.rectangle([(60, 610), (split_x - 60, 750)], outline=(224, 242, 254, 200), width=1)
    draw.text((75, 625), "鐵齒心態與現場笑點（高對比冰晶亮藍白，30 pt）", font=font_text, fill=(224, 242, 254, 255))
    draw.text((75, 665), "「痛風？！不可能！我平常有做好事、積福報！」", font=ImageFont.truetype(font_path, 26), fill=(224, 242, 254, 255))
    draw.text((75, 705), "「血壓 160？！不用管，我多喝水上健身房就好！」", font=ImageFont.truetype(font_path, 26), fill=(186, 230, 253, 255))

    # 3. 右側：Richman IP 人物與情境主體 (44%)
    char_rect = [(split_x + 30, 80), (w - 40, h - 80)]
    draw.rectangle(char_rect, outline=(239, 68, 68, 200), width=2)
    draw.text((split_x + 50, 45), "【 區塊 B：右側 44% 角色焦點 ｜ 危機與震撼 】", font=font_title, fill=(248, 113, 113, 255))

    # 人物繪製示意（頭部、身體、動作標籤）
    cx = split_x + int((w - split_x) * 0.5) # 中心 x 約 1200
    # 頭部
    draw.ellipse([(cx - 70, 150), (cx + 70, 290)], outline=(255, 255, 255, 200), width=2)
    draw.text((cx - 55, 205), "Richman\n成熟知性", font=font_desc, fill=(255, 255, 255, 255))

    # 身體與西裝
    draw.polygon([(cx - 130, 310), (cx + 130, 310), (cx + 160, 720), (cx - 160, 720)], outline=(148, 163, 184, 180), width=2)
    
    # 動作標註說明
    draw.text((split_x + 50, 340), "● 動作姿態：\n  一手輕扶額頭/太陽穴（眩暈感）\n  一手撐在桌緣或拿著紅字報告", font=font_text, fill=(254, 202, 202, 255))
    draw.text((split_x + 50, 460), "● 神態表情：\n  知性眼鏡後眼神震驚、錯愕\n  嘴硬鐵齒與身體重擊的強烈反差", font=font_text, fill=(254, 202, 202, 255))
    draw.text((split_x + 50, 580), "● 背景環境：\n  暗調辦公室 / 診所血壓計\n  電子螢幕隱約亮著紅色警示「160」", font=font_text, fill=(254, 202, 202, 255))

    # 底部狀態列
    draw.text((60, 800), "📐 畫布比例：16:9（1536 x 864）｜ 嚴格杜絕畫面拉扁變形 ｜ 提案一無框電影漸層排版", font=font_desc, fill=(100, 116, 139, 255))

    out_path = "generated/slide03_wireframe_mockup.png"
    img.save(out_path)
    print(f"Wireframe mockup created: {out_path}")

if __name__ == "__main__":
    create_wireframe()
