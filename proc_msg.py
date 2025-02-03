from get_config import bot_config
from log import log_msg

def check(msg: dict) -> bool:
    if msg.get("message_type") is None:
        log_msg("INFO", f"消息 {msg.get('message_id')} 非法, 跳过验证")
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
    log_msg("DEBUG", f"消息 {msg.get('message_id')} 不符合群组验证条件, 验证失败")
    return False