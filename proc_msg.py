# 屎山, 但不准备重构, 能跑就行

from get_config import bot_config
from log import log_msg
from command import do as do_cmd
import re

def check(msg: dict) -> bool:
    if msg.get("message_type") is None:
        return False
    if bot_config.group_mode == "whitelist":
        if msg.get('message_type') == 'group' and msg.get('group_id') in bot_config.group_list:
            log_msg("DEBUG", f"消息 {msg.get('message_id')} 在白名单内, 验证通过")
            return True
    elif bot_config.group_mode == "blacklist":
        if msg.get('message_type') == 'group' and msg.get('group_id') not in bot_config.group_list:
            log_msg("DEBUG", f"消息 {msg.get('message_id')} 不在黑名单内, 验证通过")
            return True
    elif bot_config.group_mode == "all":
        if msg.get('message_type') == 'group':
            log_msg("DEBUG", f"消息 {msg.get('message_id')} 是群消息, 验证通过")
            return True
    return False

def is_commamd(raw_msg, self_id):
    global cleaned_raw
    cleaned_raw = re.sub(r'^\[CQ:reply,[^\]]*\]', '', raw_msg)
    prefixes = [f"[CQ:at,qq={self_id}]", "#"]
    if any(cleaned_raw.startswith(prefix) for prefix in prefixes):
        return True
    else:
        return False

def split_command(command, self_id):
    # 剔除出现的第一个"#"或f"[CQ:at,qq={self_id}]"
    if command.startswith("#"):
        command = command[1:]
    elif command.startswith(f"[CQ:at,qq={self_id}]"):
        command = command[len(f"[CQ:at,qq={self_id}]"):]
    # 剔除开头与结尾多余的空格和换行
    command = command.strip()
    # 判断剩下的str中是否存在空格且存在其它字符
    if ' ' in command and len(command.strip()) > 0:
        # 返回command为第一个出现的空格之前内容，data为之后的内容
        command, data = command.split(' ', 1)
        return command, data
    elif len(command.strip()) > 0:
        # 返回command为整个字符串，data为None
        return command, None
    else:
        # 字符串为空或全是空格，返回command为None，data为None
        return None, None

def proc(msg):
    if check(msg):
        global self_id
        bot_self_id = msg["self_id"]
        if is_commamd(raw_msg=msg["raw_message"], self_id=bot_self_id):
            log_msg("DEBUG", f"接收到指令消息: {cleaned_raw}")
            command, data = split_command(command=cleaned_raw, self_id=bot_self_id)
            if command and command.startswith("#"): command = command[1:]
            log_msg("INFO", f"指令: {command}, 参数: {data}")
            do_cmd(command, data, msg)
            
