"""Slide 6（第四幕・試煉與盟友）：保留原版畫面與文字不變，
於左下角空白處放入三個獨立的 3D Q 版神隊友公仔（OpenAI 生成，完整全身不裁切）。"""
import glob
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "generated/slide05_allies_base_original.png"   # 原版 Slide 6（a8ff3f3）
OUT = "generated/slide05_allies_preview.png"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

DOLLS = [
    ("doll_chiao", "巧巧", "備餐戰友 雅雯", (134, 239, 172, 255)),
    ("doll_pei",   "沛沛", "營養導師 沛璇", (192, 132, 252, 255)),
    ("doll_mai",   "麥麥", "健管教練 淑媛", (251, 113, 133, 255)),
]


def latest(prefix):
    files = sorted(glob.glob(f"generated/{prefix}*.png"))
    files = [f for f in files if not f.endswith("_cut.png")]
    return files[-1]


def remove_white_bg(img, tol=6):
    """從四邊 flood-fill 去除純白背景，保留公仔內部的白色（白袍、廚師帽）。"""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, _ = px[x, y]
        if 255 - min(r, g, b) <= tol:
            ap[x, y] = 0
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                    q.append((nx, ny))
    # 再清除被包圍的純白空隙（例如雙腿之間），只處理面積較大的純白連通區塊
    for sy in range(0, h, 2):
        for sx in range(0, w, 2):
            i0 = sy * w + sx
            if seen[i0]:
                continue
            r, g, b, _ = px[sx, sy]
            if min(r, g, b) < 252:
                continue
            comp, cq = [], deque([(sx, sy)])
            seen[i0] = 1
            while cq:
                x, y = cq.popleft()
                comp.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                        rr, gg, bb, _ = px[nx, ny]
                        if min(rr, gg, bb) >= 252:
                            seen[ny * w + nx] = 1
                            cq.append((nx, ny))
            if len(comp) > 400:
                for x, y in comp:
                    ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    img.putalpha(alpha)
    return img.crop(img.getbbox())


def main():
    slide = Image.open(BASE).convert("RGBA")
    font_name = ImageFont.truetype(FONT, 20)
    font_role = ImageFont.truetype(FONT, 15)

    # 左下角安全區：文字最低到 y≈640；公仔區 y 660～850、x 110～700
    area_x0, area_x1 = 110, 700
    doll_h = 152
    label_gap = 6
    bottom = 850 - 44            # 預留兩行標籤
    slot_w = (area_x1 - area_x0) // 3

    layer = Image.new("RGBA", slide.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", slide.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ds = ImageDraw.Draw(shadow)

    for i, (prefix, name, role, color) in enumerate(DOLLS):
        cut = remove_white_bg(Image.open(latest(prefix)))
        cut.save(f"generated/{prefix}_cut.png")
        s = doll_h / cut.height
        if cut.width * s > slot_w - 10:
            s = (slot_w - 10) / cut.width
        cut = cut.resize((int(cut.width * s), int(cut.height * s)), Image.Resampling.LANCZOS)
        cx = area_x0 + slot_w * i + slot_w // 2
        x = cx - cut.width // 2
        y = bottom - cut.height
        # 地面柔光陰影
        ds.ellipse([(cx - cut.width * 0.38, bottom - 8), (cx + cut.width * 0.38, bottom + 6)], fill=(0, 0, 0, 170))
        layer.alpha_composite(cut, (x, y))
        # 名字＋角色
        tw = d.textlength(name, font=font_name)
        d.text((cx - tw / 2, bottom + label_gap), name, font=font_name, fill=color)
        rw = d.textlength(role, font=font_role)
        d.text((cx - rw / 2, bottom + label_gap + 24), role, font=font_role, fill=(203, 213, 225, 235))

    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    out = Image.alpha_composite(Image.alpha_composite(slide, shadow), layer)
    out.convert("RGB").save(OUT, quality=95)
    print("Rendered:", OUT)


if __name__ == "__main__":
    main()
