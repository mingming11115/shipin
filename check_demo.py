"""每隔 3 分钟检查桌面上的 demo.txt，不存在则新建，并持续循环。"""

import time
from datetime import datetime
from pathlib import Path

CHECK_INTERVAL = 3 * 60  # 3 分钟（秒）
DEMO_FILE = Path.home() / "Desktop" / "demo.txt"


def log(message: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}", flush=True)


def main() -> None:
    log(f"开始监控：{DEMO_FILE}，每 {CHECK_INTERVAL // 60} 分钟检查一次。按 Ctrl+C 退出。")
    try:
        while True:
            if DEMO_FILE.exists():
                log(f"已存在：{DEMO_FILE}")
            else:
                DEMO_FILE.write_text("demo\n", encoding="utf-8")
                log(f"未找到，已新建：{DEMO_FILE}")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        log("已停止监控。")


if __name__ == "__main__":
    main()
