import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_opening_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    slide = prs.slides.add_slide(blank_layout)
    
    # 1. Full-bleed background image
    img_path = "generated/slide01_hero_opening_sunrise_20261029_013934.png"
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        
    # 2. Subtle gradient / frosted container on the left for maximum readability
    # Left container card (frosted dark slate with soft opacity)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(6.8), Inches(5.1))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card.line.color.rgb = RGBColor(5, 150, 105) # Emerald border
    card.line.width = Pt(1.5)
    
    # Accent emerald bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.7), Inches(0.12), Inches(4.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(5, 150, 105)
    bar.line.fill.background()
    
    # Typography
    tb = slide.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(5.8), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    # Tag
    p_tag = tf.paragraphs[0]
    p_tag.text = "HERO'S JOURNEY ｜ 健管 45 天"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(14)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(16, 185, 129) # Emerald 500
    p_tag.space_after = Pt(14)
    
    # Main Title
    p_title = tf.add_paragraph()
    p_title.text = "45 天的\n蛻變歷程"
    p_title.font.name = "Microsoft JhengHei"
    p_title.font.size = Pt(46)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.space_after = Pt(14)
    
    # Subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = "重啟 48 歲的身體主控權"
    p_sub.font.name = "Microsoft JhengHei"
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(245, 158, 11) # Amber 500
    p_sub.space_after = Pt(20)
    
    # Speaker Line
    p_speaker = tf.add_paragraph()
    p_speaker.text = "分享者：王執定（Rich）"
    p_speaker.font.name = "Microsoft JhengHei"
    p_speaker.font.size = Pt(16)
    p_speaker.font.color.rgb = RGBColor(203, 213, 225) # Slate 300
    
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
