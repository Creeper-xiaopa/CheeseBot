# Copyright (c) 2021 - Present Creeper_xiaopa
# Licensed under the MIT License. See the LICENSE file in the project root for details.


from loguru import logger
import sys
import env


def init():
    """
    初始化日志配置
    自定义日志级别缩写和日志格式，并根据环境变量配置日志级别
    """
    # 自定义日志级别缩写
    _custom_levels = {
        "TRACE": "TRAC",
        "DEBUG": "DBUG",
        "INFO": "INFO",
        "SUCCESS": "SUCC",
        "WARNING": "WARN",
        "ERROR": "ERRR",
        "CRITICAL": "CRIT",
    }

    # 自定义日志格式，使用 extra 中的 abbrev_level 字段
    _log_format = "[<level>{extra[abbrev_level]}</level>] " "<level>{message}</level>"

    # 移除默认的日志处理器
    logger.remove(0)

    # 定义 patcher 函数来动态生成缩写
    def _patcher(record):
        record["extra"]["abbrev_level"] = _custom_levels.get(
            record["level"].name, record["level"].name
        )

    # 应用 patcher
    logger.configure(patcher=_patcher)

    # 处理日志级别配置
    try:
        log_level = env.get("LOG_LEVEL").upper()
    except:
        log_level = "INFO"

    # 添加处理器
    logger.add(sys.stderr, format=_log_format, level=log_level)


"""为每一级别的日志添加调用函数"""


def trace(*args, **kwargs):
    logger.trace(*args, **kwargs)


def debug(*args, **kwargs):
    logger.debug(*args, **kwargs)


def info(*args, **kwargs):
    logger.info(*args, **kwargs)


def success(*args, **kwargs):
    logger.success(*args, **kwargs)


def warning(*args, **kwargs):
    logger.warning(*args, **kwargs)


def error(*args, **kwargs):
    logger.error(*args, **kwargs)


def critical(*args, **kwargs):
    logger.critical(*args, **kwargs)
