# -*- coding: utf-8 -*-
"""edge-tts 生成 9 段旁白并输出时长表"""
import asyncio, os, json
import edge_tts

OUT = r"C:\Users\sunshuting\Desktop\shipin\06_video\tts"
os.makedirs(OUT, exist_ok=True)
VOICE = "zh-CN-YunxiNeural"

LINES = [
    "先问一个问题：同一个模型，为什么有的agent很能干，有的就笨手笨脚？",
    "差别往往不在模型，在harness。就是包在模型外面的那套提示词、记忆、工具和流程。",
    "今天要讲的这篇论文，就是让agent自己改这套东西的。论文叫Harness2：Recursive Agent Harnessing for an Open World，10月12号挂在arXiv上。",
    "一作是西北大学的Ruiyao Xu，其余八位作者全部来自Google Cloud AI Research。",
    "也就是说，这是大厂研究团队拿自家agent产品线的问题，做的一次相当认真的方法学尝试。",
    "代码开源在Google Research的GitHub上，仓库10月6号创建，到今天一个多月。",
    "已经涨到两万四千六百多个star，两千四百多个fork，一百八十多个issue在讨论。",
    "什么概念：平均每天三四百个star。而且社区里已经冒出好几个第三方移植，有人把它接进别的agent框架，有人拿它做红队实验。一个多月就有这个生态速度，在研究型仓库里，算非常罕见的。",
    "为什么这么火？因为它戳中了所有做agent的人共同的痛。下面进入正题。",
]

async def gen(i, text):
    mp3 = os.path.join(OUT, f"n{i}.mp3")
    tts = edge_tts.Communicate(text, VOICE, rate="+10%")
    await tts.save(mp3)
    return mp3

async def main():
    for i, t in enumerate(LINES, 1):
        await gen(i, t)
        print("done", i)

asyncio.run(main())

# 测时长：用 imageio-ffmpeg 解码为 wav，读 wav 长度
import imageio_ffmpeg, subprocess, wave, contextlib
FF = imageio_ffmpeg.get_ffmpeg_exe()
durs = {}
for i in range(1, len(LINES) + 1):
    mp3 = os.path.join(OUT, f"n{i}.mp3")
    wav = os.path.join(OUT, f"n{i}.wav")
    subprocess.run([FF, "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav],
                   capture_output=True)
    with contextlib.closing(wave.open(wav)) as w:
        durs[i] = w.getnframes() / w.getframerate()
print(json.dumps(durs, ensure_ascii=False))
json.dump(durs, open(os.path.join(OUT, "durs.json"), "w"))
