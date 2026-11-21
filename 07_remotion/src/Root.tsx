import { Composition } from "remotion";
import { Demo } from "./Demo";
import { Showcase } from "./Showcase";
import { StyleBoard } from "./StyleBoard";

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="Demo"
        component={Demo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Showcase10s"
        component={Showcase}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="StyleBoard"
        component={StyleBoard}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
