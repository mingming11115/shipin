#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 01_md/*.md 转成适合录屏讲解的单文件 HTML（无外部依赖，可离线打开）。

用法:
    python build_present.py 01_md/harness2.md
    python build_present.py 01_md/harness2.md -o 03_present/harness2.html

交互:
    ← / → / PgUp / PgDn   按 "章节(##)" 前后翻页
    C                     切换 分页 / 长滚动
    T                     回到顶部目录
    F                     全屏
"""

import argparse
import base64
import html
import mimetypes
import os
import re
import sys

# ---------------- Markdown 解析 ----------------

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def inline(text: str) -> str:
    """行内元素。先转义，再按占位符保护代码片段。"""
    stash = []

    def keep(s):
        stash.append(s)
        return "\x00%d\x00" % (len(stash) - 1)

    text = IMG.sub(lambda m: keep(
        '<img src="%s" alt="%s">' % (html.escape(m.group(2)), html.escape(m.group(1)))
    ), text)
    text = INLINE_CODE.sub(lambda m: keep("<code>%s</code>" % html.escape(m.group(1))), text)

    text = html.escape(text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    text = LINK.sub(lambda m: '<a href="%s" target="_blank">%s</a>' % (m.group(2), m.group(1)), text)

    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def split_row(line: str):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_table_sep(line: str) -> bool:
    s = line.strip()
    if not s.startswith("|") and "|" not in s:
        return False
    return bool(re.fullmatch(r"[\s|:\-]+", s)) and "-" in s


def parse(md: str):
    """返回 (toc, blocks)。blocks 是 (level, html) 列表，level 为 'h1'/'h2'/... 或 'body'。"""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    toc = []
    i = 0
    buf = []

    def flush():
        if buf:
            body = "\n".join(buf).strip()
            if body:
                out.append(("body", "<p>%s</p>" % inline(body)))
            buf.clear()

    while i < len(lines):
        line = lines[i]

        # 代码块
        fence = re.match(r"^```(\w*)\s*$", line)
        if fence:
            flush()
            lang = fence.group(1)
            i += 1
            code = []
            while i < len(lines) and not re.match(r"^```\s*$", lines[i]):
                code.append(lines[i])
                i += 1
            i += 1
            cls = ' class="lang-%s"' % lang if lang else ""
            out.append(("body", "<pre%s><code>%s</code></pre>"
                        % (cls, html.escape("\n".join(code)))))
            continue

        # 标题
        h = re.match(r"^(#{1,4})\s+(.*)$", line)
        if h:
            flush()
            level = len(h.group(1))
            title = h.group(2).strip()
            anchor = "s%d" % len(toc)
            if level == 1:
                out.append(("h1", "<h1>%s</h1>" % inline(title)))
            else:
                toc.append((level, title, anchor))
                out.append(("h%d" % level,
                            '<h%d id="%s">%s</h%d>' % (level, anchor, inline(title), level)))
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r"(\*{3,}|-{3,}|_{3,})", line.strip()):
            flush()
            out.append(("body", "<hr>"))
            i += 1
            continue

        # 表格
        if "|" in line and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            flush()
            head = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append(("body", "".join(t)))
            continue

        # 引用
        if line.strip().startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(("body", "<blockquote>%s</blockquote>" % inline(" ".join(q))))
            continue

        # 列表
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            flush()
            ordered = bool(re.match(r"^\s*\d+[.)]\s+", line))
            items = []
            while i < len(lines) and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(("body", "<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % inline(x) for x in items), tag)))
            continue

        # 空行
        if not line.strip():
            flush()
            i += 1
            continue

        buf.append(line)
        i += 1

    flush()
    return toc, out


# ---------------- 组装 HTML ----------------

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#fbfaf7; --fg:#1c1a17; --dim:#6b655c; --line:#e2ddd3;
  --accent:#c2410c; --code-bg:#f2efe8; --maxw:900px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font-family:"Source Han Serif SC","Noto Serif SC",Georgia,"Songti SC",serif;
  font-size:20px; line-height:1.85; -webkit-font-smoothing:antialiased;
}
#toc{
  position:fixed; top:0; left:0; width:280px; height:100vh; overflow:auto;
  padding:28px 20px; border-right:1px solid var(--line); background:#f6f3ec;
  font-size:14px; line-height:1.6;
}
#toc .t{font-family:-apple-system,"Segoe UI",sans-serif;font-size:12px;letter-spacing:.12em;
  color:var(--dim);text-transform:uppercase;margin-bottom:14px}
#toc a{display:block;color:var(--fg);text-decoration:none;padding:6px 10px;border-radius:6px;
  border-left:2px solid transparent}
#toc a:hover{background:#ece7dc}
#toc a.lv2{padding-left:10px}
#toc a.lv3{padding-left:24px;color:var(--dim);font-size:13px}
#toc a.on{background:#e8e2d5;border-left-color:var(--accent);color:var(--accent)}
main{margin-left:280px;padding:52px 56px 40vh;max-width:calc(var(--maxw) + 112px)}
h1{font-size:2.1em;line-height:1.3;margin:.2em 0 .9em;letter-spacing:-.01em}
h2{font-size:1.55em;line-height:1.4;margin:2.2em 0 .7em;padding-top:.4em;border-top:1px solid var(--line)}
h3{font-size:1.2em;margin:1.6em 0 .5em;color:#3a352e}
h4{font-size:1.05em;margin:1.3em 0 .4em;color:var(--dim)}
p{margin:0 0 1.05em}
ul,ol{margin:0 0 1.05em;padding-left:1.5em}
li{margin:.3em 0}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid #e8bda6}
a:hover{border-bottom-color:var(--accent)}
code{font-family:"JetBrains Mono",Consolas,"SF Mono",monospace;font-size:.86em;
  background:var(--code-bg);padding:.12em .38em;border-radius:4px}
pre{background:var(--code-bg);padding:18px 20px;border-radius:10px;overflow:auto;
  border:1px solid var(--line);margin:1.2em 0}
pre code{background:none;padding:0;font-size:.84em;line-height:1.65}
blockquote{margin:1.2em 0;padding:.6em 1.2em;border-left:3px solid var(--accent);
  background:#f7f2e9;color:#3a352e;border-radius:0 8px 8px 0}
table{border-collapse:collapse;width:100%;margin:1.3em 0;font-size:.88em;
  font-family:-apple-system,"Segoe UI","PingFang SC",sans-serif}
th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
th{background:#f0ece2;font-weight:600}
img{max-width:100%;display:block;margin:1.4em auto;border-radius:8px;
  border:1px solid var(--line);background:#fff;cursor:zoom-in}
hr{border:0;border-top:1px solid var(--line);margin:2.4em 0}
.kbd{position:fixed;right:20px;bottom:16px;font-family:ui-monospace,monospace;font-size:12px;
  color:var(--dim);background:#f6f3ec;border:1px solid var(--line);border-radius:8px;padding:8px 12px}
.kbd b{color:var(--fg)}
#rail{position:fixed;top:0;left:280px;right:0;height:3px;background:transparent;z-index:9}
#rail i{display:block;height:100%;width:0;background:var(--accent);transition:width .25s}
body.reveal main{opacity:0}
@media (max-width:1100px){
  #toc{position:static;width:auto;height:auto;border-right:0;border-bottom:1px solid var(--line)}
  main{margin-left:0;padding:32px 24px 30vh}
  #rail{left:0}
}
@media print{
  #toc,.kbd,#rail{display:none}
  main{margin:0;padding:0;max-width:none}
  body{font-size:12pt}
}
</style>
</head>
<body>
<nav id="toc"><div class="t">__TOC_TITLE__</div>__TOC__</nav>
<div id="rail"><i></i></div>
<main>__BODY__</main>
<div class="kbd"><b>← →</b> 翻章 &nbsp; <b>C</b> 连续 &nbsp; <b>F</b> 全屏</div>
<script>
(function(){
  var links = [].slice.call(document.querySelectorAll('#toc a'));
  var rail = document.querySelector('#rail i');
  var marks = links.map(function(a){ return document.getElementById(a.dataset.id); });
  var idx = 0;

  function paint(){
    var y = window.scrollY, best = 0;
    marks.forEach(function(m, i){ if (m && m.getBoundingClientRect().top <= 120) best = i; });
    idx = best;
    links.forEach(function(a, i){ a.classList.toggle('on', i === idx); });
    var h = document.documentElement.scrollHeight - window.innerHeight;
    rail.style.width = (h > 0 ? (y / h * 100) : 0) + '%';
  }
  window.addEventListener('scroll', paint, {passive:true});

  links.forEach(function(a){
    a.addEventListener('click', function(e){
      e.preventDefault();
      var el = document.getElementById(a.dataset.id);
      if (el) window.scrollTo({top: el.offsetTop - 24, behavior:'smooth'});
    });
  });

  document.addEventListener('keydown', function(e){
    if (e.key === 'ArrowRight' || e.key === 'PageDown') {
      e.preventDefault();
      var n = links[Math.min(idx + 1, links.length - 1)];
      if (n) window.scrollTo({top: document.getElementById(n.dataset.id).offsetTop - 24, behavior:'smooth'});
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      var p = links[Math.max(idx - 1, 0)];
      if (p) window.scrollTo({top: document.getElementById(p.dataset.id).offsetTop - 24, behavior:'smooth'});
    } else if (e.key.toLowerCase() === 'c') {
      document.body.classList.toggle('wide');
      var m = document.querySelector('main');
      m.style.maxWidth = document.body.classList.contains('wide') ? 'none' : '';
    } else if (e.key.toLowerCase() === 't') {
      window.scrollTo({top:0, behavior:'smooth'});
    } else if (e.key.toLowerCase() === 'f') {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }
  });

  // 点图放大
  document.querySelectorAll('main img').forEach(function(img){
    img.addEventListener('click', function(){
      if (img.dataset.zoom) { img.dataset.zoom = ''; img.style.maxWidth = '100%'; return; }
      img.dataset.zoom = '1'; img.style.maxWidth = 'none';
      img.scrollIntoView({block:'center', behavior:'smooth'});
    });
  });

  paint();
})();
</script>
</body>
</html>
"""


def inline_images(text: str, base_dir: str) -> str:
    """把本地图片改写成 base64 data URI，让 HTML 成为可直接打开的独立文件。"""
    missing = []

    def repl(m):
        src = m.group(1)
        if src.startswith(("data:", "http://", "https://", "//")):
            return m.group(0)
        path = src if os.path.isabs(src) else os.path.normpath(os.path.join(base_dir, src))
        if not os.path.exists(path):
            missing.append(src)
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or "image/png"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return 'src="data:%s;base64,%s"' % (mime, b64)

    out = re.sub(r'src="([^"]+)"', repl, text)
    if missing:
        print("WARN  图片未找到，保留原路径: %s" % ", ".join(missing))
    return out


def build(md_path: str, out_path: str):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()

    toc, blocks = parse(md)

    title = "文档"
    m = re.search(r"^#\s+(.+)$", md, re.M)
    if m:
        title = m.group(1).strip()

    body = []
    opened = False
    for kind, frag in blocks:
        if kind == "h2":
            if opened:
                body.append("</section>")
            body.append('<section class="sec">%s' % frag)
            opened = True
        else:
            body.append(frag)
    if opened:
        body.append("</section>")

    toc_html = []
    for level, text, anchor in toc:
        if level > 3:
            continue
        toc_html.append('<a class="lv%d" data-id="%s" href="#%s">%s</a>'
                        % (level, anchor, anchor, text))

    html_out = (TEMPLATE
                .replace("__TITLE__", html.escape(title))
                .replace("__TOC_TITLE__", html.escape(title[:20]))
                .replace("__TOC__", "\n".join(toc_html) or "<span></span>")
                .replace("__BODY__", "\n".join(body)))

    html_out = inline_images(html_out, os.path.dirname(os.path.abspath(md_path)))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    n_img = html_out.count("data:image")
    print("OK  %s  ->  %s  (%d 个章节, %d 张图内嵌, %.1f KB)"
          % (md_path, out_path, len(toc_html), n_img, len(html_out.encode("utf-8")) / 1024))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    md_path = os.path.abspath(a.md)
    out = a.out or os.path.join(
        os.path.dirname(md_path), "..", "03_present",
        os.path.splitext(os.path.basename(md_path))[0] + ".html")
    build(md_path, os.path.abspath(out))


if __name__ == "__main__":
    sys.exit(main())
