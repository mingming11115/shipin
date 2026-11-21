import React from "react";
import {
  AbsoluteFill,
  Img,
  Sequence,
  staticFile,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const seeded = (i: number) => ((i * 9301 + 49297) % 233280) / 233280;
const YA = "Microsoft YaHei, PingFang SC, sans-serif";

/* ---------- S1 逐字母弹簧标题 ---------- */
const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const letters = "Harness2".split("");
  const sub = interpolate(frame, [32, 52], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{
        position: "absolute", width: 520, height: 520, borderRadius: "50%",
        border: "3px dashed #30363d", transform: `rotate(${frame * 0.7}deg)`,
      }} />
      <div style={{
        position: "absolute", width: 660, height: 660, borderRadius: "50%",
        border: "1px solid #21262d", transform: `rotate(${-frame * 0.35}deg)`,
      }} />
      <div style={{ display: "flex", marginTop: -40 }}>
        {letters.map((ch, i) => {
          const pop = spring({ frame: frame - i * 4, fps, config: { damping: 11 } });
          return (
            <span key={i} style={{
              fontSize: 170, fontWeight: 800, color: "#e6edf3", fontFamily: YA,
              transform: `translateY(${(1 - pop) * 130}px) scale(${0.7 + pop * 0.3})`,
              opacity: pop,
              textShadow: "0 0 40px rgba(56,139,253,.35)",
            }}>{ch}</span>
          );
        })}
      </div>
      <div style={{
        fontSize: 42, color: "#8b949e", marginTop: 30, fontFamily: YA,
        letterSpacing: 6, opacity: sub,
        transform: `translateY(${(1 - sub) * 24}px)`,
      }}>Recursive Agent Harnessing</div>
    </AbsoluteFill>
  );
};

/* ---------- S2 八组件环绕 Model ---------- */
const COMPONENTS = ["System Prompt", "Memory", "Tools", "Skills", "Sub-agents", "Middleware", "Plugins", "Context"];
const ACCENTS = ["#58a6ff", "#bc8cff", "#3fb950", "#d29922", "#f85149", "#58a6ff", "#bc8cff", "#3fb950"];

const ComponentsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cx = 960, cy = 520, R = 400;
  const model = spring({ frame, fps, config: { damping: 12 } });
  const spin = frame * 0.15;
  return (
    <AbsoluteFill>
      {COMPONENTS.map((name, i) => {
        const appear = spring({ frame: frame - 12 - i * 6, fps, config: { damping: 13 } });
        const a = (i / COMPONENTS.length) * Math.PI * 2 - Math.PI / 2 + spin;
        const x = cx + Math.cos(a) * R;
        const y = cy + Math.sin(a) * R * 0.66;
        const fx = interpolate(appear, [0, 1], [x < cx ? -350 : 2270, x]);
        const fy = interpolate(appear, [0, 1], [y < cy ? -250 : 1330, y]);
        const lineP = interpolate(appear, [0.5, 1], [0, 1], clamp);
        return (
          <React.Fragment key={i}>
            <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
              <line x1={cx} y1={cy} x2={x} y2={y}
                stroke={ACCENTS[i]} strokeWidth={2} opacity={lineP * 0.5}
                strokeDasharray="8 8" />
            </svg>
            <div style={{
              position: "absolute", left: fx, top: fy,
              transform: `translate(-50%,-50%) scale(${appear})`,
              padding: "16px 30px", borderRadius: 14,
              background: "#161b22", border: `2px solid ${ACCENTS[i]}`,
              color: "#e6edf3", fontSize: 30, fontWeight: 700, fontFamily: YA,
              boxShadow: `0 0 30px ${ACCENTS[i]}33`,
              whiteSpace: "nowrap",
            }}>{name}</div>
          </React.Fragment>
        );
      })}
      <div style={{
        position: "absolute", left: cx, top: cy,
        transform: `translate(-50%,-50%) scale(${0.4 + model * 0.6})`,
        width: 280, height: 170, borderRadius: 22,
        background: "linear-gradient(135deg,#1f6feb,#388bfd)",
        display: "flex", justifyContent: "center", alignItems: "center",
        color: "#fff", fontWeight: 800, fontSize: 48, fontFamily: YA,
        boxShadow: "0 0 80px rgba(56,139,253,.5)",
      }}>Model</div>
      <div style={{
        position: "absolute", left: 0, right: 0, top: 930, textAlign: "center",
        color: "#8b949e", fontSize: 36, fontFamily: YA, fontWeight: 600,
        opacity: interpolate(frame, [55, 70], [0, 1], clamp),
      }}>Harness = 包在模型外的 8 类可编辑组件</div>
    </AbsoluteFill>
  );
};

/* ---------- S3 真实页面 + 星数爆发 ---------- */
const StarScene: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [8, 66], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const num = Math.round(24623 * p);
  const cardIn = interpolate(frame, [4, 16], [0, 1], clamp);
  const ringA = interpolate(frame, [62, 72], [0, 1], clamp) * (0.72 + 0.28 * Math.sin(frame / 3.5));
  const burst = frame > 66;
  return (
    <AbsoluteFill>
      <Img src={staticFile("gh_repo_top.png")} style={{
        position: "absolute", inset: 0, width: "100%", height: "100%",
        objectFit: "cover", filter: `brightness(${0.55 + 0.35 * cardIn})`,
      }} />
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(13,17,23,.25), rgba(13,17,23,.75))" }} />
      {/* 红圈套真实 Star 按钮 */}
      <div style={{
        position: "absolute", left: "79.8%", top: "18.7%",
        width: 200, height: 96, transform: "translate(-50%,-50%)",
        border: "6px solid #f85149", borderRadius: 999,
        opacity: ringA,
        boxShadow: `0 0 ${20 + 14 * Math.sin(frame / 3.5)}px rgba(248,81,73,.7)`,
      }} />
      {/* 星数大字卡 */}
      <div style={{
        position: "absolute", left: "50%", top: "26%", transform: `translate(-50%,-50%) scale(${0.8 + cardIn * 0.2})`,
        opacity: cardIn, textAlign: "center",
      }}>
        <div style={{ fontSize: 34, color: "#e6edf3", fontWeight: 700, letterSpacing: 8, fontFamily: YA, marginBottom: 8 }}>
          GITHUB STARS
        </div>
        <div style={{
          fontSize: 150, fontWeight: 800, color: "#ffd943", fontFamily: YA,
          textShadow: "0 0 50px rgba(255,217,67,.45)",
        }}>★ {num.toLocaleString("en-US")}</div>
        <div style={{
          fontSize: 36, color: "#e6edf3", fontFamily: YA, marginTop: 6,
          opacity: burst ? 1 : 0, transition: "opacity .3s",
        }}>一个多月 · 平均每天 600+ · 真实数据 api.github.com</div>
      </div>
      {/* 星星粒子 */}
      {Array.from({ length: 26 }).map((_, i) => {
        const start = 66 + i * 2;
        if (frame < start) return null;
        const life = frame - start;
        const prog = life / 50;
        if (prog > 1) return null;
        const r1 = seeded(i), r2 = seeded(i + 100), r3 = seeded(i + 200);
        return (
          <div key={i} style={{
            position: "absolute",
            left: `${68 + r1 * 24}%`, top: `${30 + r2 * 22}%`,
            fontSize: 14 + r3 * 22, color: "#ffd943",
            opacity: (1 - prog) * 0.95,
            transform: `translateY(${-prog * 180}px) rotate(${prog * 40 - 20}deg) scale(${0.6 + prog * 0.5})`,
          }}>★</div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------- S4 收尾卡 ---------- */
const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 12 } });
  const sweep = interpolate(frame, [16, 40], [0, 1], clamp);
  const glowX = interpolate(frame, [0, 60], [-400, 2200]);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", overflow: "hidden" }}>
      <div style={{
        position: "absolute", left: glowX, top: 300, width: 500, height: 500,
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(56,139,253,.35), transparent 65%)",
        filter: "blur(30px)",
      }} />
      <div style={{
        fontSize: 110, fontWeight: 800, color: "#e6edf3", fontFamily: YA,
        transform: `scale(${0.7 + pop * 0.3})`,
      }}>用 React 代码做视频</div>
      <div style={{
        width: 700, height: 8, borderRadius: 4, marginTop: 36,
        background: "linear-gradient(90deg,#1f6feb,#ffd943)",
        transform: `scaleX(${sweep})`, transformOrigin: "center",
      }} />
      <div style={{
        fontSize: 38, color: "#8b949e", fontFamily: YA, marginTop: 30,
        opacity: interpolate(frame, [30, 45], [0, 1], clamp),
      }}>Remotion · 300 帧 · 逐帧精确控制</div>
    </AbsoluteFill>
  );
};

/* 场景渐入渐出包装（在 Sequence 内部取局部帧号） */
const Fader: React.FC<{ outAt: number; children: React.ReactNode }> = ({ outAt, children }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 8], [0, 1], clamp)
    * (1 - interpolate(frame, [outAt, outAt + 10], [0, 1], clamp));
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

/* ---------- 主合成：4 场景接力 ---------- */
export const Showcase: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOut = interpolate(frame, [288, 300], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "#0d1117" }}>
      <Sequence from={0} durationInFrames={82}>
        <Fader outAt={70}><TitleScene /></Fader>
      </Sequence>
      <Sequence from={78} durationInFrames={82}>
        <Fader outAt={72}><ComponentsScene /></Fader>
      </Sequence>
      <Sequence from={156} durationInFrames={92}>
        <Fader outAt={82}><StarScene /></Fader>
      </Sequence>
      <Sequence from={244} durationInFrames={56}>
        <EndCard />
      </Sequence>
      <AbsoluteFill style={{ background: "#000", opacity: globalOut * 0.9, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
