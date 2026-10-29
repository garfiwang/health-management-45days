import os
import pptx
from pptx.util import Inches

def append_slide06():
    pptx_path = "健管45天圖片簡報-王執定.pptx"
    slide06_img = "generated/slide05_allies_preview.png"

    if not os.path.exists(pptx_path):
        print("Missing pptx")
        return

    prs = pptx.Presentation(pptx_path)
    blank_layout = prs.slide_layouts[6]

    s6 = prs.slides.add_slide(blank_layout)
    s6.shapes.add_picture(slide06_img, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # 內嵌演講者備忘講稿
    s6.notes_slide.notes_text_frame.text = (
        "【第四幕・試煉與盟友｜預計 55 秒】\n\n"
        "有句話這麼說：『一個人走得快，一群人走得遠。』\n\n"
        "我要謝謝我的另一半神隊友——雅雯。謝謝妳每天幫我準備健管餐！（大家知道嗎？我老婆也跟著我一起做健管，她這次也減掉了整整 1.6 公斤的純脂肪，而且肌肉量還逆勢上升喔！）\n\n"
        "同時，我更要謝謝沛璇老師和淑媛教練。在整個健管期間，她們一直在身邊提醒我、教我正確的飲食方式。\n"
        "徹底打破了我過去『少吃就會瘦』的錯誤迷思，教我們『吃對順序、補足營養』。\n\n"
        "原來，當身體的營養真正補足了，那麼減重就是自然而然發生的事！"
    )

    prs.save(pptx_path)
    print(f"Updated {pptx_path} with Slide 6. Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    append_slide06()
