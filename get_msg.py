import uvicorn
from fastapi import FastAPI, Request
from typing import List
from queue import Queue
from threading import Lock
from get_config import bot_config

# 消息队列, 用于存储接收到的消息
rx_msg = Queue()
# 线程锁, 用于保护消息队列
_lock = Lock()

# 创建FastAPI应用实例
app = FastAPI()

@app.post("/")
async def root(request: Request):
    # 接收 POST 请求并存储进队列
    data = await request.json()
    with _lock:
        rx_msg.put(data)

def has_new() -> bool:
    # 检查是否有新消息
    return not rx_msg.empty()

def get_new() -> List[dict]:
    # 返回所有新消息
    with _lock:
        msgs = []
        while not rx_msg.empty():
            msgs.append(rx_msg.get())
        return msgs

def server():
    # 启动 WebHook 服务器
    uvicorn.run(app, host=bot_config.webhook_host, port=bot_config.webhook_port)