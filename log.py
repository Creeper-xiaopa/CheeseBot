# 日志模块

# 不会添加对于日志的配置选项, 因为该项目主要为了自己使用
# 当然你也可以通过修改代码来修改选项
# Creeper_xiaopa
# 2025/02/03 20:47:11

# 完全由 DeepSeek V3 671B 生成

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 定义日志级别对应的颜色
LOG_COLORS = {
    'DEBUG': '\033[94m',    # 蓝色
    'INFO': '\033[92m',     # 绿色
    'WARNING': '\033[93m',  # 黄色
    'ERROR': '\033[91m',    # 红色
    'CRITICAL': '\033[95m'  # 紫色
}

# 重置颜色
RESET_COLOR = '\033[0m'

# 创建日志文件夹
log_folder = 'log'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 获取当前时间作为日志文件名
start_time = datetime.now().strftime('%y-%m-%d %H-%M-%S')
log_file = os.path.join(log_folder, f'{start_time}.log')

# 配置日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器，将日志写入文件，并设置编码为UTF-8
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# 创建一个控制台处理器，将日志输出到控制台
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s', datefmt='%y/%m/%d %H:%M:%S')
file_handler.setFormatter(formatter)

# 自定义控制台日志格式，添加颜色和压缩日志级别
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_level = record.levelname
        # 将日志级别映射为4个字符的缩写
        log_level_short = {
            'DEBUG': 'DEBG',
            'INFO': 'INFO',
            'WARNING': 'WARN',
            'ERROR': 'ERRR',
            'CRITICAL': 'CRIT'
        }.get(log_level, log_level)
        msg = super().format(record)
        # 替换日志级别为缩写
        msg = msg.replace(log_level, log_level_short)
        return f"{LOG_COLORS.get(log_level, '')}{msg}{RESET_COLOR}"

console_handler.setFormatter(ColoredFormatter('[%(levelname)s] %(asctime)s %(message)s', datefmt='%y/%m/%d %H:%M:%S'))

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_message(level, body):
    # 将字符串日志级别映射到 logging 模块的常量
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    log_level = log_levels.get(level.upper())
    if log_level is not None:
        logger.log(log_level, body)
    else:
        raise ValueError(f"Invalid log level: {level}")