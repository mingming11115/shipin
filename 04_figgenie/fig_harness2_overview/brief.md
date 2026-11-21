# Brief — Harness2 Figure 1（方法总览图）

## 1. 这是什么图

Harness2 论文（arXiv 预印本，单栏 A4，文本宽约 469 pt，按 AI 顶会单栏图 396–454 pt 处理，取 420 pt）的 **Figure 1 式方法总览图**，放在 §1/§2，展示"递归智能体框架自优化"的两级耦合递归。 kinds：**concept-schematic + stage-pipeline**（概念示意为主、任务级递归内部是一条 Propose–Probe–Compose 流水线），子领域 **agents**（次级 llm-nlp）。

## 2. 组件

顶部背景带 —— **任务流 q₁ … q_N**（open-world 任务流，无 ground-truth 标注；existing/设定）。

**Agent = Model + Harness 卡片**（左上，概念锚点）：
- **Frozen Model**（雪花标记，frozen；existing）
- **Execution Harness H**（8 个组件文件的堆叠小卡片示意：system prompt / memory / skills / tools …；existing，可 elide 为一个图标堆）

**Task-Level Recursion 面板**（主体，横向流水线，论文贡献，accent）：
- **Agent Executor**（用当前 harness 执行任务 q_t → Trajectory + Deliverable，即参考执行 e⁰）
- **Harness Editor**（Propose：产出两个候选——**Invariant candidate**（跨领域通病：planning / tool use / context / delegation）与 **Domain-specific candidate**（本领域知识/流程/约束）；各是一份可执行的 harness 副本）
- **Candidate Probes**（Probe：两个候选在同一任务上执行，与参考执行形成 **behavioral contrast**（行为对比，非正确性判定））
- **Harness Composer**（Compose：读参考 + 候选 diff + 全部执行证据，选择性合并/修订/采纳/保留 → **Final Harness H′** 并执行产出 e′）
- 可选小徽章：**budget k**（parallel / sequential 两种任务级递归形式，只画一个小注记，不展开成面板）

**Harnessing-Level Recursion 面板**（右侧/下方，论文贡献，第二 accent）：
- **Reflector**（任务结束后复盘整个改进记录 D_t）
- **Improvement Harness R** 及其 **Harness Improvement Library**（存放 adopted harnesses + lessons；在任务级递归期间保持 fixed（雪花），每任务后 Update）

## 3. 流程与主路径

主路径（任务级，编号 ①–④）：
① q_t + H → Agent Executor：参考执行（trajectory + deliverable）
② Executor 证据 + Library → Harness Editor：提出 invariant 与 domain 两个候选
③ 两个候选 → Candidate Probes：同任务执行，与 e⁰ 形成行为对比
④ Probes 证据 → Harness Composer：合成 Final Harness H′（交付 deliverable）

框架级（虚线/弧线，跨任务）：
⑤ H′ + 改进记录 D_t → Reflector：提炼 lessons 与 adopted harnesses → Update Improvement Harness Library（虚线弧，"Update"）
⑥ Library → 下一个任务的 Editor / Composer（虚线，"inform future proposals"；配合 "Move to the next task" 弧线 q_t → q_t+1 回到 ①）

关键语义：改进框架 R 在任务级递归中**固定**（画雪花），只在任务间被更新——这是两级递归耦合的论点。

## 4. 图论证的一点

**两级递归互相咬合**：内环（任务级）在没有 ground-truth 的情况下用"行为对比"改进当前 harness；外环（框架级）把每次改进的*经验*沉淀为库，让下一次改进更聪明。视线从任务流进入内环 ①→④，再顺虚线弧看到外环回到下一个任务。

## 5. 版式与风格意图

- **排布**：bands/hub 混合——上半部任务级递归画成 4 段横向流水线（大面板、重色），右下角框架级递归画成较小的面板 + 一条大的回环弧（"Move to the next task" / "Update"），顶带任务流。面板字母/标题命名，两个 recursion 面板用各自淡色底。
- **示例图候选**：见 `exemplar_sheet.png`（10 张，用户挑 2–4 张作为观感强偏好）。已看 `neurips25-0016_fig1`（循环+镜像泳道）、`aaai25-0120_fig1`（两级 tinted zones）、`neurips25-0367_fig1`（按角色着色的智能体环）。
- **配色**：office-pastel 家族（粉彩，贴近论文自带 Figure 3 的观感）；执行流水线蓝色系，框架级/库紫色系，accent 给 Final Harness H′ 与 Update 弧；frozen 统一雪花图标。颜色语义 = 面板归属，legend 一枚（frozen ❄ / 提议 △ / 对比 ◇ 之类的小 key）。
- **idioms**：agent 机器人头像（parts library）、harness 文件堆卡片、chat/trajectory 小卡、雪花 frozen 标记。
- 步骤编号用 ①②③④（主路径）+ 虚线弧标 Update / Next task。图内不放标题。

## 6. 假设待确认（已确认 2026-11-21）

a) ✅ 定位为**新的 Figure 1 概念总览**。
b) ✅ Parallel / Sequential recursion 只画成 budget-k 小注记。
c) ✅ Harness 的 8 个组件画成一个小文件堆示意。
d) ✅ 单栏宽（约 420 pt）。
e) ✅ 粉彩底色 + 规范线稿 + 局部小机器人图标点缀（不模仿手绘吉祥物）。观感示例：用户不挑，AI 按语料习惯自定（内部参照 #1 循环泳道、#6 两级 tinted 大区、#5 编号步骤徽章）。

## 7. Caption 草稿

**Figure 1 | Harness2: recursive agent harnessing as two coupled recursion levels.** For each open-world task q_t, task-level recursion ① executes the current harness for a reference trajectory, ② the Harness Editor proposes invariant and domain-specific candidate harnesses, ③ probes them on the same task to obtain behavioral contrasts, and ④ composes a final harness H′ — without any ground-truth verifier. Harnessing-level recursion ⑤ then reflects on the improvement record to update the improvement harness's library, ⑥ which informs future proposals for subsequent tasks. The frozen model and the fixed improvement harness are the only invariant parts; everything around them improves recursively.
