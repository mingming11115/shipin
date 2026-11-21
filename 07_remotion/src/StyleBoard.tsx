import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* 每种风格渲染同一内容：标题 Harness2 + star 数据 + 一句副标题，便于公平对比 */

/* ---------- 1. GitHub 终端风 ---------- */
const S1: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 10, fps, config: { damping: 12 } });
  return (
    <AbsoluteFill style={{ background: "#0d1117", fontFamily: "Consolas, monospace", padding: 70 }}>
      <div style={{ color: "#8b949e", fontSize: 26 }}>$ npx harness2 --explain</div>
      <div style={{ color: "#3fb950", fontSize: 26, marginTop: 12 }}>✓ repo cloned · 24,623 stars fetched</div>
      <div style={{
        marginTop: 60, fontSize: 96, fontWeight: 800, color: "#e6edf3",
        transform: `scale(${pop})`, transformOrigin: "left center",
      }}>Harness2<span style={{ color: "#58a6ff" }}>_</span></div>
      <div style={{ marginTop: 30, fontSize: 34, color: "#8b949e" }}>
        Recursive Agent Harnessing <span style={{ color: "#f85149" }}>· arXiv:2610.14224</span>
      </div>
      <div style={{
        marginTop: 50, display: "inline-block", border: "2px solid #30363d", borderRadius: 12,
        padding: "18px 36px", background: "#161b22", color: "#ffd943", fontSize: 40, fontWeight: 700,
      }}>★ 24,623 <span style={{ color: "#8b949e", fontWeight: 400, fontSize: 28 }}>/ fork 2,463</span></div>
      <div style={{ position: "absolute", bottom: 60, left: 70, color: "#30363d", fontSize: 22 }}>
        ── 38 days ──────────────────────────
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 2. 学术论文白 ---------- */
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const a = interpolate(f, [5, 25], [0, 1], clamp);
  const a2 = interpolate(f, [15, 35], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "#fdfdfa", padding: 90, fontFamily: "Georgia, serif" }}>
      <div style={{ borderBottom: "3px double #1a1a1a", paddingBottom: 24 }}>
        <div style={{ fontSize: 74, color: "#111", fontWeight: 700, letterSpacing: 1 }}>Harness2: Recursive Agent Harnessing</div>
        <div style={{ fontSize: 30, color: "#555", marginTop: 14, fontStyle: "italic" }}>
          Ruiyao Xu (Northwestern) · Google Cloud AI Research × 8
        </div>
      </div>
      <div style={{ marginTop: 50, display: "flex", gap: 40, opacity: a }}>
        <div style={{ flex: 1, borderLeft: "4px solid #a40f13", paddingLeft: 24 }}>
          <div style={{ fontSize: 62, color: "#a40f13", fontWeight: 700 }}>24,623</div>
          <div style={{ fontSize: 26, color: "#444", marginTop: 6 }}>GitHub Stars（38 天）</div>
        </div>
        <div style={{ flex: 1, borderLeft: "4px solid #a40f13", paddingLeft: 24 }}>
          <div style={{ fontSize: 62, color: "#a40f13", fontWeight: 700 }}>+17k</div>
          <div style={{ fontSize: 26, color: "#444", marginTop: 6 }}>上线两周增量</div>
        </div>
        <div style={{ flex: 1, borderLeft: "4px solid #a40f13", paddingLeft: 24 }}>
          <div style={{ fontSize: 62, color: "#a40f13", fontWeight: 700 }}>2 级</div>
          <div style={{ fontSize: 26, color: "#444", marginTop: 6 }}>任务级 × 框架级递归</div>
        </div>
      </div>
      <div style={{
        position: "absolute", right: 90, top: 250, border: "3px solid #a40f13", color: "#a40f13",
        padding: "10px 22px", fontSize: 28, fontWeight: 700, transform: "rotate(-6deg)", opacity: a2,
        background: "#fdfdfa",
      }}>arXiv:2610.14224</div>
      <div style={{ position: "absolute", bottom: 70, left: 90, fontSize: 24, color: "#888", fontStyle: "italic" }}>
        Figure 1 · 概念总览（手绘风插图与正文同源）
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 3. 科技蓝玻璃拟态 ---------- */
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - 8, fps, config: { damping: 14 } });
  const glow = Math.sin(f / 8) * 20;
  return (
    <AbsoluteFill style={{
      background: "radial-gradient(1200px 800px at 30% 20%, #123a7a 0%, #0a1230 55%, #060a1c 100%)",
      justifyContent: "center", alignItems: "center",
    }}>
      <div style={{
        width: 1100, padding: "70px 80px", borderRadius: 28,
        background: "rgba(255,255,255,0.06)",
        border: "1px solid rgba(140,180,255,0.35)",
        backdropFilter: "blur(20px)",
        boxShadow: `0 0 ${60 + glow}px rgba(56,139,253,.35)`,
        transform: `scale(${0.9 + pop * 0.1})`,
      }}>
        <div style={{ fontSize: 30, color: "#7fb0ff", letterSpacing: 8, fontWeight: 600 }}>PAPER DECODED</div>
        <div style={{ fontSize: 100, fontWeight: 800, color: "#fff", marginTop: 14, fontFamily: "Microsoft YaHei" }}>
          Harness2 <span style={{ fontSize: 40, color: "#9ab8ff", fontWeight: 400 }}>论文深读</span>
        </div>
        <div style={{ display: "flex", gap: 28, marginTop: 44 }}>
          {[["★ 24,623", "#ffd943"], ["+17k / 2 周", "#3fb950"], ["8 位作者 · Google", "#58a6ff"]].map(([t, c], i) => (
            <div key={i} style={{
              padding: "16px 30px", borderRadius: 14, fontSize: 34, fontWeight: 700,
              color: c, background: "rgba(255,255,255,0.07)", border: `1px solid ${c}55`,
            }}>{t}</div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 4. Kinetic 大字报 ---------- */
const S4: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f, fps, config: { damping: 10, stiffness: 120 } });
  const slide = interpolate(f, [10, 30], [1920, 0], { ...clamp, easing: undefined });
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center", alignItems: "center", overflow: "hidden" }}>
      <div style={{
        fontSize: 230, fontWeight: 900, color: "#fff", fontFamily: "Arial Black, Microsoft YaHei",
        transform: `scale(${pop}) skewX(-6deg)`, letterSpacing: -6,
      }}>24,623</div>
      <div style={{
        position: "absolute", bottom: 300, left: slide, background: "#ffd900", color: "#000",
        fontSize: 60, fontWeight: 900, padding: "8px 40px", transform: "skewX(-6deg)",
        fontFamily: "Microsoft YaHei",
      }}>STARS IN 38 DAYS ★</div>
      <div style={{
        position: "absolute", top: 120, left: 80, fontSize: 44, color: "#fff", fontWeight: 900,
        transform: "rotate(-3deg)", border: "6px solid #ff3b30", padding: "6px 20px",
        fontFamily: "Microsoft YaHei",
      }}>Harness2</div>
    </AbsoluteFill>
  );
};

/* ---------- 5. 手绘白板风（与论文总览图同源） ---------- */
const S5: React.FC = () => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [5, 40], [0, 1], clamp);
  const bounce = Math.sin(f / 6) * 4;
  return (
    <AbsoluteFill style={{ background: "#fffdf5", padding: 80 }}>
      <div style={{ position: "absolute", inset: 30, border: "3px solid #2b2b2b", borderRadius: 18, opacity: 0.12 }} />
      <div style={{
        fontSize: 88, fontWeight: 800, color: "#1f1f1f", fontFamily: "Microsoft YaHei",
        transform: `rotate(-1.5deg)`, marginTop: 30,
      }}>Harness2 画给你看 ✏️</div>
      <svg width={1760} height={480} style={{ marginTop: 40 }}>
        <path d="M 60 300 Q 400 220 760 290 T 1400 270" fill="none" stroke="#e4572e"
          strokeWidth={7} strokeLinecap="round"
          strokeDasharray={1600} strokeDashoffset={1600 * (1 - draw)} />
        <circle cx={1400} cy={270} r={54} fill="none" stroke="#2b6cb0" strokeWidth={8}
          strokeDasharray={340} strokeDashoffset={340 * (1 - draw)} />
        <text x={1370} y={288} fontSize={44} fontWeight={800} fill="#2b6cb0"
          fontFamily="Microsoft YaHei">+17k</text>
        <text x={70} y={250} fontSize={38} fill="#666" fontFamily="Microsoft YaHei">上线两周爆发 →</text>
        <text x={1150} y={130} fontSize={38} fill="#666" fontFamily="Microsoft YaHei">真实曲线 ↑</text>
      </svg>
      <div style={{
        fontSize: 40, color: "#1f1f1f", fontWeight: 700, fontFamily: "Microsoft YaHei",
        marginTop: 30, transform: `translateY(${bounce}px)`,
      }}>▶ 手绘曲线 + 荧光笔标注，跟论文总览图一个画风</div>
    </AbsoluteFill>
  );
};

/* ---------- 6. 数据杂志风 ---------- */
const S6: React.FC = () => {
  const f = useCurrentFrame();
  const a = interpolate(f, [5, 22], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "#f4f1ea", padding: "80px 90px", fontFamily: "Microsoft YaHei" }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 20, borderBottom: "2px solid #1a1a1a", paddingBottom: 18 }}>
        <div style={{ fontSize: 40, fontWeight: 900, color: "#1a1a1a" }}>HARNESS2</div>
        <div style={{ fontSize: 26, color: "#666", letterSpacing: 4 }}>WEEKLY PAPER · VOL.42</div>
        <div style={{ marginLeft: "auto", fontSize: 26, color: "#a40f13", fontWeight: 700 }}>深度 10 分钟</div>
      </div>
      <div style={{ display: "flex", marginTop: 50, gap: 60, opacity: a }}>
        <div style={{ flex: 1.2 }}>
          <div style={{ fontSize: 60, fontWeight: 900, color: "#1a1a1a", lineHeight: 1.25 }}>
            一个 GitHub 仓库，<br />38 天 24,623 星
          </div>
          <div style={{ fontSize: 30, color: "#555", marginTop: 26, lineHeight: 1.7 }}>
            Google Cloud AI Research 的 agent 自改进方法学，<br />
            为什么突然成了社区最热的论文？
          </div>
        </div>
        <div style={{ flex: 1, borderLeft: "1px solid #999", paddingLeft: 50 }}>
          {[["STAR 增速", "600+/天"], ["FORK", "2,463"], ["ISSUES", "185 在讨论"], ["作者", "9 人 · 2 机构"]].map(([k, v], i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "14px 0", borderBottom: "1px solid #ccc4" }}>
              <span style={{ fontSize: 26, color: "#666" }}>{k}</span>
              <span style={{ fontSize: 30, fontWeight: 800, color: "#a40f13" }}>{v}</span>
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const STYLES = [S1, S2, S3, S4, S5, S6];
const PER = 30;

export const StyleBoard: React.FC = () => {
  const f = useCurrentFrame();
  const idx = Math.min(5, Math.floor(f / PER));
  const Style = STYLES[idx];
  return <Style />;
};
