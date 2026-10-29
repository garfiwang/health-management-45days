import os
import pptx
from pptx.util import Inches

def update_presentation():
    pptx_path = "健管45天圖片簡報-王執定.pptx"
    slide02_img = "generated/slide02_richman_ordinary_world_preview.png"
    
    if not os.path.exists(pptx_path):
        print(f"Error: {pptx_path} not found")
        return
    
    prs = pptx.Presentation(pptx_path)
    
    # 檢查是否已經有 Slide 2，如果超過 1 頁，先保留第 1 頁
    if len(prs.slides) > 1:
        # 重建或添加
        pass
    
    blank_layout = prs.slide_layouts[6]
    slide2 = prs.slides.add_slide(blank_layout)
    
    # 加入第 2 頁全圖（16:9 無變形，13.333 x 7.5 英吋）
    if os.path.exists(slide02_img):
        slide2.shapes.add_picture(slide02_img, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # 加入演講者備忘講稿
    slide2.notes_slide.notes_text_frame.text = (
        "【第一幕・平凡世界｜預計 60 秒】\n\n"
        "別人都是朝九晚五，而我平常的工作是『朝五晚九』。\n\n"
        "什麼叫做朝五晚九呢？大家有聽過 BNI 商會嗎？應該有聽過吧。BNI 是不是都要很早起床？沒有錯。\n\n"
        "我有兩個 BNI 商會，一個是我自己創立的長輝分會，另一個是我輔導的金佑分會。所以我平常都很早起來開會，開完會之後要整理財經資料，下午要拜訪客戶或是接受客戶諮詢，有的時候會有演講，晚上也常常會有應酬和飯局。\n\n"
        "所以，可能 5 點就要起床，一路忙到晚上九點。\n\n"
        "剛退伍的時候，可以拜訪客戶到晚上 12 點，第二天早上 8 點一樣準時進公司開會。\n"
        "到了 30 歲以後，早上就會需要喝一杯咖啡來提神。\n"
        "到了 40 歲以後，喝一杯咖啡可能不夠了，要喝到三杯咖啡，還會睡過頭爬不起來。"
    )
    
    prs.save(pptx_path)
    print(f"Successfully added Slide 2 to {pptx_path}. Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    update_presentation()
