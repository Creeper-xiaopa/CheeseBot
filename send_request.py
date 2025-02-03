import requests
from get_config import bot_config
from log import log_msg

# 基础结构
def send_request(addr, body):
    try:
        response = requests.post(
            url = f"{bot_config.onebot_addr}/{addr}",
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bot_config.onebot_token}"
            },
            json = body,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_msg("ERROR", f"请求失败: {str(e)}")
        return e
    
# 点赞
def send_like(user_id, times=1):
    status = send_request(
        addr = "send_like",
        body = {"user_id": str(user_id),
                "times": times
        }
    )
    return status

# 获取账号信息
def get_user_info(user_id):
    status = send_request(
        addr = "get_stranger_info",
        body = {"user_id": str(user_id)}
    )
    return status

# 获取用户在线状态
def get_user_status(user_id):
    status = send_request(
        addr = "nc_get_user_status",
        body = {"user_id": str(user_id)}
    )
    return status

# 发送群消息
def send_group_msg(group_id, msg):
    status = send_request(
        addr = "send_group_msg",
        body = {"group_id": group_id,
                "message": msg}
        )

# 获取版本信息
def get_version_info():
    status = send_request(
        addr = "get_version_info",
        body={}
    )
    return status
