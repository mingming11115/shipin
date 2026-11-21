import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const Demo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 12 } });
  const opacity = interpolate(frame, [0, 20], [0, 1]);
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 30, durationInFrames],
    [1, 0]
  );

  return (
    <AbsoluteFill
      style={{
        background: "#0d1117",
        justifyContent: "center",
        alignItems: "center",
        opacity: opacity * fadeOut,
      }}
    >
      <h1
        style={{
          fontFamily: "Microsoft YaHei, sans-serif",
          fontWeight: 800,
          fontSize: 130,
          color: "white",
          transform: `scale(${0.6 + pop * 0.4})`,
          margin: 0,
        }}
      >
        Harness2
      </h1>
      <p
        style={{
          fontFamily: "Microsoft YaHei, sans-serif",
          fontSize: 52,
          color: "#8b949e",
          marginTop: 30,
          transform: `translateY(${pop * 40}px)`,
        }}
      >
        Remotion 就绪 · 用 React 代码做视频
      </p>
    </AbsoluteFill>
  );
};
