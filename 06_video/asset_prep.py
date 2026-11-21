# -*- coding: utf-8 -*-
"""论文首页/作者行裁切 + GitHub 截图关键区域裁切验证"""
import fitz, os
from PIL import Image

BASE = r"C:\Users\sunshuting\Desktop\shipin"
OUT = os.path.join(BASE, "06_video", "shots")
SHOTS = os.path.join(OUT)

doc = fitz.open(os.path.join(BASE, "00_source", "harness2.pdf"))
page = doc[0]

# 1) 论文首页整页（zoom 2.2）
pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
pix.save(os.path.join(OUT, "paper_page1.png"))
print("page1", pix.width, pix.height)

# 2) 作者行裁切：定位 Ruiyao Xu 与 Google Cloud AI Research
r1 = page.search_for("Ruiyao Xu")
r2 = page.search_for("Google Cloud AI Research")
print("ruiyao:", r1[:1], "google:", r2[:1])
rects = [r for r in (r1 + r2) if r]
if rects:
    y0 = min(r.y0 for r in rects) - 18
    y1 = max(r.y1 for r in rects) + 18
    x0 = 40
    x1 = page.rect.width - 40
    clip = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip)
    pix.save(os.path.join(OUT, "paper_authors.png"))
    print("authors", pix.width, pix.height)

# 3) GitHub 关键区域裁切（normalized coords on 3840x2160 shots）
top = Image.open(os.path.join(SHOTS, "gh_repo_top.png"))
W, H = top.size
print("top size", W, H)
def crop_norm(img, box):
    w, h = img.size
    return img.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h)))

# Star/Fork 按钮行（右上）
crop_norm(top, (0.68, 0.075, 0.85, 0.135)).save(os.path.join(OUT, "test_btnrow.png"))
# 标题行 google-research / harness2
crop_norm(top, (0.15, 0.14, 0.45, 0.21)).save(os.path.join(OUT, "test_title.png"))
# Issues 45 标签
crop_norm(top, (0.04, 0.09, 0.30, 0.14)).save(os.path.join(OUT, "test_issues.png"))

scrolled = Image.open(os.path.join(SHOTS, "gh_repo_scrolled.png"))
crop_norm(scrolled, (0.60, 0.40, 0.90, 0.62)).save(os.path.join(OUT, "test_about.png"))

search = Image.open(os.path.join(SHOTS, "gh_search.png"))
crop_norm(search, (0.10, 0.10, 0.75, 0.60)).save(os.path.join(OUT, "test_search.png"))

# 拼贴目检
tiles = ["test_btnrow.png", "test_title.png", "test_issues.png", "test_about.png", "test_search.png", "paper_authors.png"]
imgs = [Image.open(os.path.join(OUT, t)) for t in tiles]
tw = 900
scaled = []
for im in imgs:
    r = tw / im.width
    scaled.append(im.resize((tw, max(1, int(im.height*r)))))
th = sum(im.height for im in scaled) + 10*len(scaled)
sheet = Image.new("RGB", (tw, th), "white")
y = 0
for im in scaled:
    sheet.paste(im, (0, y)); y += im.height + 10
sheet.save(os.path.join(OUT, "contact_sheet.png"))
print("sheet saved")
