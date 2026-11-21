# -*- coding: utf-8 -*-
"""采集真实 GitHub 页面高清截图（deviceScaleFactor=2，无痕、无登录框风险）"""
import asyncio, os
from playwright.async_api import async_playwright

OUT = r"C:\Users\sunshuting\Desktop\shipin\06_video\shots"
os.makedirs(OUT, exist_ok=True)

REPO = "https://github.com/google-research/harness2"
SEARCH = "https://github.com/search?q=harness2&type=repositories"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
            locale="en-US",
        )
        page = await ctx.new_page()

        # 1) 仓库顶部（Star 按钮入画）
        await page.goto(REPO, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2500)
        await page.screenshot(path=os.path.join(OUT, "gh_repo_top.png"))
        print("shot1 ok")

        # 2) 缓慢滚到 About 栏可见（右侧 stars/forks/watching）
        await page.mouse.wheel(0, 300)
        await page.wait_for_timeout(1200)
        await page.screenshot(path=os.path.join(OUT, "gh_repo_scrolled.png"))
        print("shot2 ok")

        # 3) 再滚一点，文件列表 + README 开头
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(1200)
        await page.screenshot(path=os.path.join(OUT, "gh_repo_readme.png"))
        print("shot3 ok")

        # 4) 搜索结果页（第三方移植）
        await page.goto(SEARCH, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2500)
        await page.screenshot(path=os.path.join(OUT, "gh_search.png"))
        print("shot4 ok")

        await browser.close()

asyncio.run(main())
