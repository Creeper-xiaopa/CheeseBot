# Copyright (c) 2021 - Present Creeper_xiaopa
# Licensed under the MIT License. See the LICENSE file in the project root for details.

from art import text2art
import log
import msg
import threading
import time
import traceback
import sys

# 缓存 ASCII 艺术字
WELCOME_ART = text2art("CheeseBot", font="Small Slant")


def log_welcome():
    """欢迎信息"""
    log.info("---------------------------------------------")
    for line in WELCOME_ART.splitlines():
        if line.strip():  # 检查该行是否为空
            log.info(f"\033[94m{line}\033[0m")  # ASCII 艺术字
    log.info("\033[94m感谢使用 CheeseBot! 求给项目一个 Star\033[0m")
    log.info("\033[94mGitHub: https://github.com/Creeper-xiaopa/CheeseBot\033[0m")
    log.info("---------------------------------------------")


def server_thread():
    server_thread = threading.Thread(target=msg.server)
    server_thread.daemon = True  # 设为守护进程
    server_thread.start()
    log.success(f"在 {msg.host}:{msg.port} 开始监听消息")
    return server_thread


def main_loop():
    if msg.check():
        msgs = msg.get_new()
        log.debug(f"收到 {len(msgs)} 条新消息")
        for message in msgs:
            log.trace(f"消息内容: {message}")


def main():
    try:
        log.init()  # 初始化日志系统
        log_welcome()  # 打印欢迎信息
        server_thread_instance = server_thread()  # 启动服务器线程

        # 主循环
        while True:
            main_loop()
            time.sleep(1)

    except KeyboardInterrupt:
        log.info("\033[94m正在退出 CheeseBot...\033[0m")
        # 等待服务器线程退出
        if server_thread_instance.is_alive():
            server_thread_instance.join(timeout=1)  # 等待线程退出，最多等待1秒
        log.info("\033[94m感谢使用 CheeseBot!\033[0m")
        log.info("\033[94m程序已退出\033[0m")
        sys.exit(0)
    except Exception:
        error_msg = traceback.format_exc()
        log.critical("致命错误:\n")
        for line in error_msg.strip().split("\n"):
            log.critical(line)
        log.critical("程序因异常退出!")
        sys.exit(1)


if __name__ == "__main__":
    main()
