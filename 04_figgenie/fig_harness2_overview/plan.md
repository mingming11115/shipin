# Plan — Harness2 Figure 1 概念总览

Canvas: `viewBox="0 0 454 288"` pt（ACL 单栏全宽 454；高 288，AI 族允许 130–320）。
Palette: office-pastel（蓝 #3c78d8 主 accent；任务级带底 #eaf2fb/边 #9dc3e6；框架级带底 #f3eefa/边 #b4a7d6；白画布）。字体 helvetica，标签 6.5–7pt，小注 6pt，粗细 0.56/1.1 两档。circled 步骤 ①–④（disc r≈4.5，白底描边）。

## 纵向分区

| 区 | y 范围 | 内容 |
|---|---|---|
| 任务流条 | 8–42 | 左侧两行灰色小标 "Open-world task stream / (no ground-truth verifier)"（x14 起）；任务卡 q₁(x125–149) q₂(158–182) ⋯(≈196) q_N(206–230)，y 24–38，白底灰边；next-task 虚线弧 qN 顶(218,24)→apex(177,8)→q₁ 顶(137,24)，标签 "move to the next task" 6pt 斜体灰 at (238, 12) |
| Band A 任务级 | 52–190 | 淡蓝圆角带；标题 + 副题；主管线行 y 86–152；边标签行 y 155–163；budget pill y 168–184 |
| 通道 | 190–206 | 两条跨任务虚线箭头 |
| Band B 框架级 | 206–280 | 淡紫圆角带；Reflector + Improvement Harness 盒 + 图例 |

## Band A 内部（x 12–442）

- 标题 "Task-Level Recursion" 7pt bold (22, 64)；副题 6pt 灰 "improve the execution harness for the current task" (22, 75)（宽≈110，止于 x132，避开 x137 竖箭头）。
- 主管线（盒 y 86–152，66 高；箭头在 y 119 中线）：
  - **agent-anchor** x 20–102：上 "Model M ❄" 芯片 (28–94, 92–106)，中 3 文件堆 (30–92, 110–138)（system prompt / memory / skills 各一条），下 6pt 标 "Agent = Model + Harness" (61, 147)。
  - **executor** x 112–162 (c137)：机器人头 icon (137, 100) r9；"Agent Executor" 7pt y 122；"runs q_t with H" 6pt 灰 y 131。
  - **editor 容器** x 172–240 (c206)：头 icon (206, 97) r8；"Harness Editor" 7pt y 115；"Propose" 6pt 灰 y 123；内嵌两张迷你卡 x 178–234：inv y 127–138（"Invariant candidate" 6pt + 无副行，空间不够 → 卡内一行主名 + 6pt 灰副行 "planning · tools · context"…测宽 93>56 → 副行省略号 "planning · tools · …"），dom y 141–152 同构（"domain knowledge · …"）。
  - **probes** x 250–316 (c283)：框 y 86–152；"Candidate Probes" 7pt y 114；"re-run each on q_t" 6pt 灰 y 124；"◇ contrast vs e⁰" 6pt y 140（菱形小标）。
  - **composer** x 326–378 (c352)：头 icon；"Harness Composer" 7pt y 122；"Compose" 6pt 灰 y 131。
  - **final** x 386–438 (c412)：饱和蓝 accent 盒白字 "Final Harness" 7pt bold y 118、"H′" y 129。
- 箭头（solid 1.1pt 主路径 #3c78d8，箭头头 marker）：
  - run-task ①: (137,42)→(137,86)；标签 "q_t + H" 6pt at (143, 78) 左对齐。
  - mount: (102,119)→(112,119) 细灰 0.56。
  - to-editor ②disc(167,119): (162,119)→(172,119)；标签 "trajectory + deliverable e⁰" 6pt 灰 at x118–200, y 160。
  - to-probes ③disc(245,119): (240,119)→(250,119)。
  - to-composer ④disc(321,119): (316,119)→(326,119)；标签 "contrasts + diffs" at c321±27, y 160。
  - compose: (378,119)→(386,119)；标签 "selective merge" 6pt 灰 at (356–408, 160)。与上一标签间隔 8pt ✓。
- budget pill: 圆角 x 24–190 y 168–184，边虚？实线细；6pt 文 "budget k → parallel / sequential recursion (Fig. 4)"（宽121，盒 166 ✓）。

## 通道（y 190–206）

- to-reflector 虚线 1.1pt 紫 #8e7cc3: (412,152)↓(412,200)←(316,200)↓(316,228 箭头进 reflector 顶)；标签 "improvement record Dₜ" 6.5pt at (170–246, y 196)（横线上方）。
- inform 虚线: (60,250)←(22,250)↑(22,166)→(206,166)↑(206,152 箭头进 editor 底)；标签 "inform future proposals" 6.5pt at (16–90, y 163)（横线上方左端）。

## Band B 内部（x 12–442）

- 标题 "Harnessing-Level Recursion" 7pt bold (22, 219)；副题 6pt 灰 "improve how future harnesses are improved" (140, 219)。
- **improvement-harness 盒** x 60–262 y 226–272 白底圆角：标题行 "Improvement Harness Rₜ · Improvement Library" 6.5pt bold (161, 238)（宽≈128 ✓）；槽位行 y 242–257：两格 "adopted harnesses" x 72–160 / "lessons" x 168–250（6pt，淡紫底 #ece4f5）；snowflake 行 "❄ fixed during a task, updated after each task" 6pt 灰 (161, 266)（宽≈114 ✓）。
- **reflector** x 288–344 (c316) y 228–272：头 icon (316, 240) r9（放大镜 prop）；"Reflector" 7pt y 258；"Reflect on Dₜ" 6pt 灰 y 267。
- update 实线箭头 (262,250)→(288,250)；标签 "Update" 6.5pt at (275, 244)。
- **legend** x 356–436 y 228–272：无框，"Legend" 6pt bold (358, 236)；行1 snowflake 符号 + "frozen: fixed during a task"（两行 6pt: "frozen: fixed during" / "a task"？宽 66 → x 372–438 = 66 ✓ 单行放得下 "frozen: fixed during a task" ≈75 → 溢出 2pt，改 "frozen = fixed during a task" 仍 75。用两行：y 246 "❄ frozen — fixed" y 254 "during a task"？丑。改行文 "❄ = frozen" + 下行小注不必要，caption 会讲。**决定**: 行1 "❄ frozen (fixed during a task)" 拆两行 6pt y 246/253 x 372 起；行2 虚线样本 + "cross-task flow" y 262；行3 粗实线 + "main path" y 270。

## 颜色语义（唯一编码）

蓝 = 任务级递归/主路径；紫 = 跨任务（框架级/虚线）；白 = 容器；灰 = 次要文字。饱和填充仅 final 盒一处。

## 自检清单（check.py 后逐项看 PNG）

1. ①–④ 徽章顺序沿主路径可读，无压线。
2. x137 竖箭头不穿 Band A 标题/副题文字。
3. "trajectory…" / "inform…" / budget pill 三者互不相交（y 155–184 区）。
4. 两条虚线跨带箭头在通道 y 190–206 内走线，不穿 Band A/B 边框文字。
5. final 盒是全图唯一饱和色；对比一下是否最响。
6. 任务卡、编辑器迷你卡、库槽位文字 ≥6pt 且不溢出盒。
7. next-task 弧不与任务卡/标签相交；apex 处标签清晰。
8. 图例三项与图中语义一致（❄出现两处：anchor 芯片、improvement 盒行）。
9. 所有盒间距均匀（主行 5 盒 gap 10–14pt 一致感）。
10. 反模式 §3：无渐变/阴影；虚线只有"跨任务"一种含义。

## 已知偏离（记录）

- 18 个标注盒高于语料 q3=13：scope-overview 中位数 24，本图为总览型，可接受；紧凑手段=候选卡内嵌 editor、库槽位合并。
- 论文原 Figure 3 为左 pipeline+右库+下方回环；本图为上下双带（单栏宽下 4 段管线需要全宽），brief §5 允许"下方"。
