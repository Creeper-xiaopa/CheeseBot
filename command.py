from log import log_msg
from datetime import datetime 
import send_request
import yaml
import platform
import psutil
import time

def cmd_help(data, msg):
    send_request.send_group_msg(group_id=msg["group_id"], msg=f"[CQ:reply,id={msg["message_id"]}]{open('help.txt', 'r', encoding='utf-8').read()}")

def cmd_echo(data, msg):
    send_request.send_group_msg(group_id=msg["group_id"], msg=str(data))

def cmd_status(data, msg):
    cpu_usage = f"{psutil.cpu_percent(interval=1)}%"
    mem = psutil.virtual_memory()
    mem_usage = f"{mem.used/1024**3:.2f}GiB/{mem.total/1024**3:.2f}GiB"
    system_v = f"{platform.system()} {platform.machine()} {platform.version()}"
    current_time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    net_io_start = psutil.net_io_counters()
    time.sleep(1)
    net_io_end = psutil.net_io_counters()
    upload_speed = (net_io_end.bytes_sent - net_io_start.bytes_sent) * 8 / 1024 / 1024
    download_speed = (net_io_end.bytes_recv - net_io_start.bytes_recv) * 8 / 1024 / 1024
    upload = f"{upload_speed:.1f}Mbps"
    download = f"{download_speed:.1f}Mbps"
    message = f"""
[CheeseBot 状态]
版本: v0.1.0
系统: {system_v}
时间: {current_time}
CPU: {cpu_usage}
内存: {mem_usage}
网络: {upload}↑ {download}↓
""".strip()
    send_request.send_group_msg(group_id=msg["group_id"], msg=f"[CQ:reply,id={msg["message_id"]}]{message}")

def do(command, data, msg):
    # 从 YAML 文件中读取配置
    try:
        command_alias = yaml.safe_load(open("command_alias.yml", 'r', encoding='utf-8'))
    except FileNotFoundError:
        log_msg("ERROR", "找不到命令别名文件 command_alias.yml")
        raise
    except yaml.YAMLError as e:
        log_msg("ERROR", f"解析 command_alias.yml 文件时出错:\n{e}")
        raise
    # 遍历所有大项
    for main_cmd, aliases in command_alias.items():
        # 如果命令在某个大项的别名列表中
        if command in aliases:
            # 构造对应的函数名
            func_name = f"cmd_{main_cmd}"
            # 获取函数对象
            func = globals().get(func_name)
            # 如果函数存在，则执行
            if func:
                func(data=data, msg=msg)
                return
    # 如果没有找到对应的命令，则返回错误信息
    log_msg("INFO", f"未知命令: {command}")
    send_request.send_group_msg(group_id=msg["group_id"], msg=f"[CQ:reply,id={msg["message_id"]}]未知命令: {command}, 使用 help 获取帮助")