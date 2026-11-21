# -*- coding: utf-8 -*-
"""Harness2 开场视频渲染：8 场景 / 90 秒 / 1920x1080@30fps
素材：真实 GitHub 页面截图(4x) + star_history 曲线 + 论文 PDF 裁切 + 口播稿 TTS
"""
import os, math, wave, subprocess, contextlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"C:\Users\sunshuting\Desktop\shipin"
V = os.path.join(BASE, "06_video")
SH = os.path.join(V, "shots")
TTS = os.path.join(V, "tts")
OUT_MP4 = os.path.join(V, "Harness2_开场90秒.mp4")

W, H, FPS = 1920, 1080, 30
DARK = (13, 17, 23)          # GitHub 深色
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_R = r"C:\Windows\Fonts\msyh.ttc"
def fb(sz): return ImageFont.truetype(FONT_B, sz)
def fr(sz): return ImageFont.truetype(FONT_R, sz)

import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

# ---------------- 素材 ----------------
repo4x   = Image.open(os.path.join(SH, "gh_repo_top_4x.png")).convert("RGB")
repo2x   = Image.open(os.path.join(SH, "gh_repo_top.png")).convert("RGB")
search2x = Image.open(os.path.join(SH, "gh_search.png")).convert("RGB")
fig2     = Image.open(os.path.join(BASE, "05_output/figures/fig2.png")).convert("RGB")
overview = Image.open(os.path.join(BASE, "04_figgenie/fig_harness2_overview/fig.png")).convert("RGB")
stars    = Image.open(os.path.join(V, "star_history.png")).convert("RGB")
paper1   = Image.open(os.path.join(SH, "paper_page1.png")).convert("RGB")
authors  = Image.open(os.path.join(SH, "paper_authors.png")).convert("RGB")

# ---------------- 通用工具 ----------------
def ease(t):  # smoothstep
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def kb(img, t, dur, kfs):
    """Ken Burns：kfs=[(tn, cx, cy, zoom), ...]，zoom=1 为 cover 铺满"""
    tn = t / dur
    for i in range(len(kfs) - 1):
        a, b = kfs[i], kfs[i + 1]
        if a[0] <= tn <= b[0] or i == len(kfs) - 2:
            p = ease((tn - a[0]) / max(1e-6, b[0] - a[0]))
            cx = a[1] + (b[1] - a[1]) * p
            cy = a[2] + (b[2] - a[2]) * p
            z  = a[3] + (b[3] - a[3]) * p
            break
    w, h = img.size
    scale = max(W / w, H / h) * z
    cw, ch = W / scale, H / scale
    x0 = min(max(cx * w - cw / 2, 0), w - cw)
    y0 = min(max(cy * h - ch / 2, 0), h - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS).convert("RGBA"), (x0, y0, cw, ch)

def map_pt(src_pt, crop):
    """源图坐标 -> 输出画面坐标"""
    x0, y0, cw, ch = crop
    sx, sy = src_pt
    return ((sx - x0) / cw * W, (sy - y0) / ch * H)

def draw_ring(frame, cx, cy, rx, ry, alpha, width=10):
    if alpha <= 0: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    a = int(alpha * 255)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(255, 60, 60, a), width=width)
    frame.alpha_composite(ov)

def pop_text(frame, text, cx, cy, alpha, size=110, fill=(255,255,255), stroke=(0,0,0), star_color=None):
    if alpha <= 0: return
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    f = fb(size)
    a = int(alpha * 255)
    if star_color:
        d.text((cx, cy), text, font=f, fill=star_color + (a,), anchor="rm",
               stroke_width=6, stroke_fill=stroke + (a,))
    else:
        d.text((cx, cy), text, font=f, fill=fill + (a,), anchor="mm",
               stroke_width=6, stroke_fill=stroke + (a,))
    frame.alpha_composite(ov)

def chip(frame, text, alpha, pos=(60, 46), accent=(88, 166, 255)):
    if alpha <= 0: return
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    f = fb(40)
    tw = d.textlength(text, font=f)
    x0, y0 = pos
    a = int(alpha * 255)
    d.rounded_rectangle([x0, y0, x0 + tw + 44, y0 + 64], 14, fill=(30, 36, 46, a))
    d.rounded_rectangle([x0, y0, x0 + 10, y0 + 64], 5, fill=accent + (a,))
    d.text((x0 + 26, y0 + 30), text, font=f, fill=(235, 240, 245, a), anchor="lm")
    frame.alpha_composite(ov)

def wrap(text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if f.getlength(cur + ch) > maxw:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur: lines.append(cur)
    return lines

def subtitle(frame, text, alpha):
    if alpha <= 0 or not text: return
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    f = fr(42)
    lines = wrap(text, f, 1760)
    lh = 58
    bh = len(lines) * lh + 34
    y0 = H - bh - 36
    a = int(alpha * 255)
    d.rounded_rectangle([70, y0, W - 70, H - 36], 16, fill=(10, 12, 16, int(alpha * 200)))
    ty = y0 + 17
    for ln in lines:
        d.text((W/2, ty + lh/2), ln, font=f, fill=(240, 243, 246, a), anchor="mm")
        ty += lh
    frame.alpha_composite(ov)

def card(frame, box, title, sub, accent, alpha):
    if alpha <= 0: return
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ov)
    a = int(alpha * 255)
    d.rounded_rectangle(box, 18, fill=(28, 33, 42, a), outline=accent + (a,), width=3)
    cx = (box[0] + box[2]) / 2
    d.text((cx, box[1] + 52), title, font=fb(48), fill=(240,243,246,a), anchor="mm")
    d.text((cx, box[1] + 118), sub, font=fr(36), fill=accent + (a,), anchor="mm")
    frame.alpha_composite(ov)

def fade(frame, t, dur, fin=0.3, fout=0.35):
    """首尾黑场过渡"""
    a = 0.0
    if t < fin: a = 1 - t / fin
    if dur - t < fout: a = max(a, 1 - (dur - t) / fout)
    if a > 0:
        black = Image.new("RGBA", (W, H), (0, 0, 0, int(a * 255)))
        frame.alpha_composite(black)

def new_frame():
    return Image.new("RGBA", (W, H), DARK + (255,))

# ---------------- 场景时间轴 ----------------
SC = []
def scene(dur, render):
    SC.append({"dur": dur, "render": render})
starts = {}
def compute_starts():
    t = 0.0
    for i, s in enumerate(SC):
        starts[i] = t
        t += s["dur"]
    return t
TOTAL_DUR = compute_starts()

# ---------- S1 黑场提问 7s ----------
def s1(t):
    f = new_frame(); d = ImageDraw.Draw(f)
    a1 = ease(t / 0.8)
    s = 1 + 0.04 * ease(t / 7)
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    do = ImageDraw.Draw(ov)
    do.text((W/2, H/2 - 90), "同一个模型", font=fb(150), fill=(255,255,255,int(a1*255)), anchor="mm")
    f.alpha_composite(ov)
    if t > 2.3:
        a2 = ease((t - 2.3) / 0.7)
        d.text((W/2, H/2 + 70), "为什么有的 agent 很能干，有的就笨手笨脚？",
               font=fr(58), fill=(200, 208, 216, int(a2*255)), anchor="mm")
    if t > 4.3:
        a3 = ease((t - 4.3) / 0.5)
        card(f, [250, 690, 880, 860], "能干 ✔", "harness 好", (63, 185, 80), a3)
        card(f, [1040, 690, 1670, 860], "笨手笨脚 ✘", "harness 差", (248, 81, 73), a3)
    fade(f, t, 7)
    return f
scene(7.0, s1)

# ---------- S2 fig2 八组件 10s ----------
def s2(t):
    f = new_frame()
    s = 1.0 + 0.20 * ease(t / 10)
    fw = 1650 * s
    fh = fw * fig2.height / fig2.width
    fg = fig2.resize((int(fw), int(fh)), Image.LANCZOS)
    sh = Image.new("RGBA", fg.size, (0,0,0,0))
    f.paste(fg, (int((W - fw)/2), int((H - fh)/2)))
    chip(f, "Harness = 包在模型外的 8 类组件", ease(t / 0.6))
    subtitle(f, "差别不在模型，在 harness——提示词、记忆、工具、流程", ease((t - 0.3) / 0.5) * (1 - ease((t - 9.3) / 0.6)))
    fade(f, t, 10)
    return f
scene(10.0, s2)

# ---------- S3 论文首页 + 印章 13.1s ----------
def s3(t):
    f = new_frame()
    s = 1.0 + 0.06 * ease(t / 13.1)
    ph = 980 * s
    pw = ph * paper1.width / paper1.height
    pg = paper1.resize((int(pw), int(ph)), Image.LANCZOS)
    px, py = int((W - pw)/2), int((H - ph)/2)
    f.paste(pg, (px, py))
    # 标题带高亮
    if t > 2.5:
        a = ease((t - 2.5) / 0.6)
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        d = ImageDraw.Draw(ov)
        bx0 = px + pw * 0.10; by0 = py + ph * 0.085
        bx1 = px + pw * 0.90; by1 = py + ph * 0.175
        d.rectangle([bx0, by0, bx1, by1], fill=(255, 214, 0, int(a*70)))
        f.alpha_composite(ov)
    # arXiv 印章
    if t > 6.0:
        a = ease((t - 6.0) / 0.5)
        sc = 1.6 - 0.6 * ease((t - 6.0) / 0.5)
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        d = ImageDraw.Draw(ov)
        st = Image.new("RGBA", (760, 240), (0,0,0,0))
        ds = ImageDraw.Draw(st)
        aa = int(a*255)
        ds.rounded_rectangle([6, 6, 754, 234], 24, outline=(218, 54, 51, aa), width=8)
        ds.text((380, 92), "arXiv:2610.14224", font=fb(74), fill=(218, 54, 51, aa), anchor="mm")
        ds.text((380, 172), "2026-10-12 · OPEN WORLD", font=fr(38), fill=(218, 54, 51, aa), anchor="mm")
        st = st.resize((int(760*sc), int(240*sc))).rotate(-7, expand=True, resample=Image.BICUBIC)
        f.alpha_composite(st, (int(W*0.62), int(H*0.62)))
    chip(f, "Harness2 · Recursive Agent Harnessing", ease(t / 0.6))
    subtitle(f, "10 月 12 号挂在 arXiv 上", ease((t - 7.5) / 0.5) * (1 - ease((t - 12.3) / 0.6)))
    fade(f, t, 13.1)
    return f
scene(13.1, s3)

# ---------- S4 作者行（两阶段）16.4s ----------
STAGE_B = 7.7
def s4(t):
    f = new_frame()
    if t < STAGE_B:
        # 阶段 A：镜头横移到一作（幅度小，保证 Ruiyao Xu 始终在画面内）
        sw = 2600
        sh_ = sw * authors.height / authors.width
        strip = authors.resize((int(sw), int(sh_)), Image.LANCZOS)
        cw = 1920
        prog = ease(t / STAGE_B)
        x0 = prog * 70  # 轻微右移
        cy = (H - sh_) / 2 + 60
        f.paste(strip, (int(-x0), int(cy)))
        if t > 1.0:
            a = ease((t - 1.0) / 0.5)
            cx = 0.075 * sw - x0
            draw_ring(f, cx, cy + sh_/2, 180, 100, a * (0.7 + 0.3 * math.sin(t * 5)))
        card(f, [180, 760, 900, 950], "Ruiyao Xu · 一作", "Northwestern University 西北大学",
             (188, 140, 255), ease((t - 0.6) / 0.5))
        chip(f, "论文作者行 · 第 1 页", ease(t / 0.6))
    else:
        tb = t - STAGE_B
        strip = authors.resize((1920, int(1920 * authors.height / authors.width)), Image.LANCZOS)
        f.paste(strip, (0, int(H/2 - strip.height/2)))
        card(f, [560, 740, 1360, 940], "Google Cloud AI Research", "其余 8 位作者 · Google 云 AI 研究团队",
             (88, 166, 255), ease(tb / 0.5))
        chip(f, "作者全名单", ease(tb / 0.6))
    subtitle(f, "一作是西北大学的 Ruiyao Xu" if t < STAGE_B else "其余八位作者，全部来自 Google Cloud AI Research",
             ease((t - 0.3) / 0.5) * (1 - ease((t - 15.6) / 0.6)))
    fade(f, t, 16.4)
    return f
scene(16.4, s4)

# ---------- S5 仓库页缓推 + 星标 7.5s ----------
STAR_PT = (0.798, 0.187)   # star 按钮中心（源图归一化）
def s5(t):
    f, crop = kb(repo4x, t, 7.5, [(0, 0.50, 0.42, 1.02), (1, 0.72, 0.30, 1.5)])
    if t > 5.0:
        a = ease((t - 5.0) / 0.5) * (0.7 + 0.3 * math.sin(t * 5))
        sx, sy = STAR_PT[0] * repo4x.width, STAR_PT[1] * repo4x.height
        cx, cy = map_pt((sx, sy), crop)
        k = crop[2] and (W / crop[2])
        draw_ring(f, cx, cy, 150, 85, a)
    chip(f, "github.com/google-research/harness2 · 真实页面", ease(t / 0.6))
    subtitle(f, "代码开源在 Google Research 的 GitHub 上，到今天一个多月",
             ease((t - 0.3) / 0.5) * (1 - ease((t - 6.8) / 0.6)))
    fade(f, t, 7.5)
    return f
scene(7.5, s5)

# ---------- S6 星星三连放大 10s ----------
def s6(t):
    f = new_frame()
    segs = [
        (0.0, 4.2, 0.798, 0.187, "★ 24,623", (255, 198, 60)),
        (4.2, 7.0, 0.735, 0.187, "Fork 2,463", (137, 208, 255)),
        (7.0, 10.0, 0.088, 0.128, "Issues 185", (255, 137, 137)),
    ]
    for i, (t0, t1, cxn, cyn, label, col) in enumerate(segs):
        if not (t0 <= t < t1 or (i == 2 and t >= t0)): continue
        lt = t - t0; ld = t1 - t0
        z0 = 4.0 if i < 2 else 3.2
        z1 = 6.2 if i < 2 else 5.0
        f, crop = kb(repo4x, lt, ld, [(0, cxn, cyn, z0), (1, cxn, cyn, z1)])
        a = ease(lt / 0.3)
        sx, sy = cxn * repo4x.width, cyn * repo4x.height
        cx, cy = map_pt((sx, sy), crop)
        draw_ring(f, cx, cy, 190, 110, a * (0.75 + 0.25 * math.sin(t * 6)), width=12)
        pop_text(f, label, W/2, 150, ease((lt - 0.8) / 0.4), size=130 if i == 0 else 100,
                 star_color=(255, 198, 60) if i == 0 else None)
        break
    chip(f, ["Star 特写", "Fork 特写", "Issues 特写"][min(2, int(t / 4.2) if t < 7 else 2)], ease(t / 0.4),
         accent=(248, 81, 73))
    subtitle(f, "两万四千六百多个 star，两千四百多个 fork，一百八十多个 issue 在讨论",
             ease((t - 0.3) / 0.5) * (1 - ease((t - 9.2) / 0.6)))
    fade(f, t, 10)
    return f
scene(10.0, s6)

# ---------- S7 曲线 + 第三方移植 17s ----------
CURVE_END = 11.5
def s7(t):
    f = new_frame()
    if t < CURVE_END:
        lt = t
        imh = 860
        imw = imh * stars.width / stars.height
        st = stars.resize((int(imw), int(imh)), Image.LANCZOS)
        x0, y0 = (W - imw) // 2, (H - imh) // 2 - 20
        reveal = int(imw * ease(lt / 9.0))
        if reveal > 0:
            f.paste(st.crop((0, 0, reveal, imh)), (int(x0), int(y0)))
            d = ImageDraw.Draw(f)
            if reveal < imw:
                d.line([x0 + reveal, y0, x0 + reveal, y0 + imh], fill=(248, 81, 73), width=4)
        d = ImageDraw.Draw(f)
        d.rounded_rectangle([x0, y0, x0 + imw, y0 + imh], 8, outline=(60, 68, 80), width=2)
        if t > 8.5:
            a = ease((t - 8.5) / 0.4)
            pop_text(f, "上线两周 +17k ★", x0 + imw * 0.72, y0 + 110, a, size=72,
                     fill=(255, 255, 255), stroke=(200, 40, 40), star_color=(255, 198, 60))
        chip(f, "真实 Star 增长曲线 · star-history.com", ease(t / 0.6), accent=(63, 185, 80))
    else:
        lt = t - CURVE_END
        f, crop = kb(search2x, lt, 5.5, [(0, 0.45, 0.42, 1.05), (1, 0.45, 0.40, 1.35)])
        chip(f, "GitHub 搜索 harness2 → 第三方移植", ease(lt / 0.5), accent=(63, 185, 80))
    subtitle(f, "平均每天三四百个 star，社区已经冒出好几个第三方移植",
             ease((t - 0.3) / 0.5) * (1 - ease((t - 16.2) / 0.6)))
    fade(f, t, 17)
    return f
scene(17.0, s7)

# ---------- S9 结尾 9s ----------
END_SPLIT = 4.0
def s8(t):
    f = new_frame()
    if t < END_SPLIT:
        d = ImageDraw.Draw(f)
        a = ease(t / 0.8)
        s = 1 + 0.03 * ease(t / END_SPLIT)
        d.text((W/2, H/2), "模型卷到头了，增量在哪？", font=fb(110),
               fill=(255, 255, 255, int(a * 255)), anchor="mm")
    else:
        tb = t - END_SPLIT
        fw = min(1720, W - 120)
        fh = fw * overview.height / overview.width
        if fh > 900:
            fh = 900; fw = fh * overview.width / overview.height
        ov = overview.resize((int(fw), int(fh)), Image.LANCZOS)
        a = ease(tb / 0.6)
        frame2 = new_frame()
        frame2.paste(ov, (int((W - fw)/2), int((H - fh)/2)))
        f = Image.blend(f, frame2, a)
        chip(f, "Harness2 · 任务级递归 × 框架级递归 → Final Harness H′", ease((tb - 0.4) / 0.5))
    subtitle(f, "为什么这么火？它戳中了所有做 agent 的人共同的痛",
             ease((t - 4.5) / 0.5) * (1 - ease((t - 8.2) / 0.6)))
    fade(f, t, 9)
    return f
scene(9.0, s8)

TOTAL_DUR = compute_starts()
N_FRAMES = int(TOTAL_DUR * FPS)
print(f"scenes={[round(s['dur'],1) for s in SC]} total={TOTAL_DUR:.1f}s frames={N_FRAMES}")

# ---------------- 预览模式 ----------------
import sys
if "--preview" in sys.argv:
    probes = [(0, 3.5), (1, 5.0), (2, 8.0), (3, 3.0), (3, 12.0), (4, 6.0),
              (5, 2.0), (5, 5.5), (5, 8.5), (6, 6.0), (6, 14.0), (7, 2.0), (7, 6.5)]
    tiles = []
    for si, lt in probes:
        img = SC[si]["render"](lt).convert("RGB").resize((640, 360))
        d = ImageDraw.Draw(img)
        d.text((10, 6), f"S{si+1} t={lt}s", font=fb(26), fill=(255, 80, 80))
        tiles.append(img)
    cols = 2
    rows = (len(tiles) + 1) // cols
    sheet = Image.new("RGB", (cols * 650, rows * 370), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 650 + 5, (i // cols) * 370 + 5))
    sheet.save(os.path.join(V, "preview_sheet.png"))
    print("preview saved")
    sys.exit(0)

# ---------------- 音频合成 ----------------
SR = 24000
def load_wav(path):
    with contextlib.closing(wave.open(path)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return data

# 旁白时间点（与场景对齐）
NARR = [
    (starts[0] + 0.5, "n1"), (starts[1] + 0.4, "n2"), (starts[2] + 0.4, "n3"),
    (starts[3] + 0.4, "n4"), (starts[3] + 7.7, "n5"), (starts[4] + 0.4, "n6"),
    (starts[5] + 0.4, "n7"), (starts[6] + 0.5, "n8"), (starts[7] + 0.5, "n9"),
]
total_n = int((TOTAL_DUR + 1.0) * SR)
mix = np.zeros(total_n)
for off, name in NARR:
    a = load_wav(os.path.join(TTS, name + ".wav"))
    i0 = int(off * SR)
    n = min(len(a), total_n - i0)
    seg = a[:n]
    fade_n = int(0.08 * SR)
    if n > 2 * fade_n:
        seg[:fade_n] *= np.linspace(0, 1, fade_n)
        seg[-fade_n:] *= np.linspace(1, 0, fade_n)
    mix[i0:i0 + n] += seg

# BGM：96BPM 轻鼓点
bpm = 96; beat = 60.0 / bpm
kick_len = int(0.16 * SR); hat_len = int(0.05 * SR)
kick = np.sin(2 * np.pi * 55 * np.arange(kick_len) / SR) * np.exp(-np.arange(kick_len) / (0.05 * SR))
rng = np.random.default_rng(7)
hat = rng.standard_normal(hat_len) * np.exp(-np.arange(hat_len) / (0.012 * SR)) * 0.5
bgm = np.zeros(total_n)
t_i = 0
bi = 0
while True:
    tb = bi * beat
    i0 = int(tb * SR)
    if i0 + kick_len >= total_n: break
    if bi % 2 == 0:
        bgm[i0:i0 + kick_len] += kick * 0.5
    for k in range(2):
        j0 = i0 + int(k * beat / 2 * SR)
        if j0 + hat_len < total_n:
            bgm[j0:j0 + hat_len] += hat * (0.25 if k else 0.15)
    bi += 1
mix += bgm * 0.18
peak = np.max(np.abs(mix))
if peak > 0.95: mix *= 0.95 / peak
wav_path = os.path.join(V, "final_mix.wav")
with contextlib.closing(wave.open(wav_path, "w")) as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("audio ok", TOTAL_DUR)

# ---------------- 视频管道 ----------------
cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
       "-i", "-", "-i", wav_path, "-c:v", "libx264", "-preset", "medium", "-crf", "19",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", OUT_MP4]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for i in range(N_FRAMES):
    t = i / FPS
    # 找当前场景
    for si, s in enumerate(SC):
        if t < starts[si] + s["dur"] or si == len(SC) - 1:
            lt = t - starts[si]
            frame = s["render"](max(0.0, lt))
            break
    proc.stdin.write(frame.convert("RGB").tobytes())
    if i % 150 == 0:
        print(f"frame {i}/{N_FRAMES} t={t:.1f}s scene={si}")
proc.stdin.close()
proc.wait()
print("DONE", OUT_MP4, os.path.getsize(OUT_MP4))
