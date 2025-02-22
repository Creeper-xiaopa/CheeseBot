# Copyright (c) 2021 - Present Creeper_xiaopa
# Licensed under the MIT License. See the LICENSE file in the project root for details.


import uvicorn
import env
from typing import List
from fastapi import FastAPI, Request
import asyncio

# 用于存储消息的异步队列
rx_msg_queue = asyncio.Queue()

app = FastAPI()


@app.post("/")
async def root(request: Request):
    """接收 POST 请求并将数据放入异步队列。"""
    data = await request.json()
    await rx_msg_queue.put(data)


def check() -> bool:
    """检查队列中是否有新消息。"""
    return not rx_msg_queue.empty()


def get_new() -> List[dict]:
    """从队列中获取所有新消息并清空队列。"""
    msgs = []
    while not rx_msg_queue.empty():
        msgs.append(rx_msg_queue.get_nowait())
    return msgs


host = str(env.get("WebHook.host", "0.0.0.0"))
port = int(env.get("WebHook.port", 8080))


def server():
    """启动 FastAPI 服务器。"""
    uvicorn.run(app, host=host, port=port, log_level="critical")
