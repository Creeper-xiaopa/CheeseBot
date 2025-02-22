# Copyright (c) 2021 - Present Creeper_xiaopa
# Licensed under the MIT License. See the LICENSE file in the project root for details.


from art import text2art
import log


def log_welcome():
    """欢迎信息"""
    log.info("---------------------------------------------")
    for line in text2art("CheeseBot", font="Small Slant").splitlines():  # type: ignore
        if line.strip():  # 检查该行是否为空
            log.info(f"\033[94m{line}\033[0m")  # ASCII 艺术字
    log.info("\033[94m感谢使用 CheeseBot! 求给项目一个 Star\033[0m")
    log.info("\033[94mGitHub: https://github.com/Creeper-xiaopa/CheeseBot\033[0m")
    log.info("---------------------------------------------")


def main():
    log.init()  # 初始化日志系统
    log_welcome()  # 打印欢迎信息


if __name__ == "__main__":
    main()
