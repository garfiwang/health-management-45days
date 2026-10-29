import os
import pptx
from pptx.util import Inches

def append_slide05():
    pptx_path = "健管45天圖片簡報-王執定.pptx"
    slide05_img = "generated/slide04_threshold_preview.png"

    if not os.path.exists(pptx_path):
        print("Missing pptx")
        return

    prs = pptx.Presentation(pptx_path)
    blank_layout = prs.slide_layouts[6]

    s5 = prs.slides.add_slide(blank_layout)
    s5.shapes.add_picture(slide05_img, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 內嵌演講者備忘講稿
    s5.notes_slide.notes_text_frame.text = (
        "【第三幕・跨越門檻｜預計 55 秒】\n\n"
        "所以像我這樣鐵齒的人，通常最適合用哪一句成語來形容？\n"
        "『不見棺材不掉淚』！\n\n"
        "到底是因為什麼事情發生，我才終於肯啟動健管呢？\n"
        "關鍵在——城隍爺！對，你沒聽錯，就是掌管地府的城隍爺！\n\n"
        "原來是這樣，我每年都會去城隍爺前面『批流年』。\n"
        "以往城隍爺給我的提醒都是：『小心開車』、『早點睡覺』。\n"
        "但是今年他給我的提醒，竟然是：『小心頭部的疾病』！\n\n"
        "請問大家，你如果聽到掌管地府的神明這樣跟你講，你會不會覺得很恐怖？（～會吧～）\n"
        "那我就再追問城隍爺：『請問是什麼頭部疾病呀？』\n"
        "結果祂就——搖、搖、頭……（學神明搖頭動作）\n\n"
        "我看祂一搖頭，我就自己瘋狂腦補：天啊！掌管生死的老闆對著我搖頭，我是不是要中風？然後頭要爆炸？！\n"
        "那該怎麼辦？！——『健管！』\n\n"
        "所以我馬上請我的引薦人沛璇老師趕快安排健管教練，營養品趕快買一買，立刻執行！"
    )

    prs.save(pptx_path)
    print(f"Updated {pptx_path} with Slide 5. Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    append_slide05()
