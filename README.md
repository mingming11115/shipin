# Harness 2 技术视频 · 工作区

目标：论文 → Markdown → 补图 → 对着 MD 讲解（先出 MD，视频形式后定）。

原文：https://arxiv.org/abs/2610.14224

## 目录约定

```
00_source/      论文 PDF（唯一来源，改稿从这里重跑）
01_md/          harness2.md —— 主稿，讲解和录屏都看这一份
02_images/
  raw/          从 PDF 里裁切的原始 figure（fig1–fig8，未改动）
  gen/          自绘 SVG 示意图（g1 两层递归、g2 主结果对比；改字改数据直接编辑源文件）
    渲染预览: chrome --headless=new --screenshot=xx.png --window-size=1000,500 file:///<svg路径>
03_present/     build_present.py 产出的投屏 HTML，录屏用这个
04_script/      逐段讲解稿（口播词、停顿点、切图时机）
build_present.py  01_md/*.md → 03_present/*.html
```

## 用法

```bash
cd harness2
python build_present.py 01_md/harness2.md
# → 03_present/harness2.html，双击可离线打开
```

产物是**单文件自包含**的：图片以 base64 内嵌，拷到任何机器/发给人都不丢图（约 870 KB）。

阅读页操作：`←/→` 按章节翻页，`C` 切连续滚动，`T` 回顶部，`F` 全屏，点图放大。

## MD 写作约定

技术论文直译不好念，MD 按「能讲出来」的标准写，不是按论文结构抄：

1. **每个 `##` 是一个镜头**（一个讲解段落，60–120 秒能讲完），标题写成人话，不写 "3.2 Method"。
2. 段落控制在 3–5 行。太长就拆，念稿时会喘不上气。
3. 公式：必须保留的用行内 `` ` `` 或代码块写清楚的等价形式，不硬塞 LaTeX（离线环境没有 KaTeX，`$...$` 会原样显示）。讲的时候用语言复述一遍。
4. 表格只留讲得着的几列，实验表只保留结论性对比。
5. 图统一用 `![图注](../02_images/raw/fig3.png)`，图注写「这张图在说什么」，不写 "Figure 3"。
6. 每节末尾留一行 `> 口播提示：……`，写这一节要强调什么、可以跳过什么。

## 当前状态

- [x] 目录结构、MD→投屏页工具链（已用样例验证）
- [ ] 拿到 PDF（外网当前不通，待用户提供）
- [ ] 正文抽取 + MD 初稿
- [ ] 抽原图 / 补示意图
- [ ] 讲解稿
