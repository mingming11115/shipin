# -*- coding: utf-8 -*-
"""第二轮修正裁切坐标"""
import fitz, os
from PIL import Image

BASE = r"C:\Users\sunshuting\Desktop\shipin"
OUT = os.path.join(BASE, "06_video", "shots")

# 作者行紧凑裁切：只取姓名行 + 脚注行 (y 145~192pt)
doc = fitz.open(os.path.join(BASE, "00_source", "harness2.pdf"))
page = doc[0]
clip = fitz.Rect(40, 143, page.rect.width - 40, 194)
pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip)
pix.save(os.path.join(OUT, "paper_authors.png"))
print("authors", pix.width, pix.height)

top = Image.open(os.path.join(OUT, "gh_repo_top.png"))
scrolled = Image.open(os.path.join(OUT, "gh_repo_scrolled.png"))
def crop_norm(img, box, name):
    w, h = img.size
    img.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h))).save(os.path.join(OUT, name))

crop_norm(top, (0.60, 0.155, 0.87, 0.22), "test_btnrow.png")      # Notifications/Fork/Star 行
crop_norm(top, (0.02, 0.07, 0.30, 0.13), "test_breadcrumb.png")   # google-research / harness2
crop_norm(top, (0.02, 0.085, 0.32, 0.145), "test_issues.png")     # Issues 45 标签
crop_norm(scrolled, (0.62, 0.42, 0.84, 0.60), "test_about.png")   # stars/watching/forks

tiles = ["test_btnrow.png", "test_breadcrumb.png", "test_issues.png", "test_about.png", "paper_authors.png"]
imgs = [Image.open(os.path.join(OUT, t)) for t in tiles]
tw = 900
scaled = []
for im in imgs:
    r = tw / im.width
    scaled.append(im.resize((tw, max(1, int(im.height*r)))))
th = sum(im.height for im in scaled) + 10*len(scaled)
sheet = Image.new("RGB", (tw, th), (240,240,240))
y = 0
for im in scaled:
    sheet.paste(im, (0, y)); y += im.height + 10
sheet.save(os.path.join(OUT, "contact_sheet2.png"))
print("sheet2 saved")
