import os
import pptx
from pptx.util import Inches

def build_opening_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    slide = prs.slides.add_slide(blank_layout)
    
    # 1. Use the full cinematic composite image directly (Proposal 1: Seamless gradient, zero card boxes)
    cinematic_img = "generated/slide01_proposal1_cinematic_preview.png"
    if os.path.exists(cinematic_img):
        slide.shapes.add_picture(cinematic_img, 0, 0, width=prs.slide_width, height=prs.slide_height)
    
    # Speaker notes
    slide.notes_slide.notes_text_frame.text = (
        "【開場｜預計 30 秒】\n"
        "大家好，我是 Rich。\n"
        "今天要來和大家分享 45 天的蛻變歷程。"
    )
    
    output_path = "健管45天圖片簡報-王執定.pptx"
    prs.save(output_path)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    build_opening_slide()
