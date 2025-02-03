import get_msg
import threading
import time
from get_config import bot_config
from log import log_msg

def start_webhook(): 
    get_msg.server(host=bot_config.webhook_host, port=bot_config.webhook_port)

def start_webhook_daemon():
    server_thread = threading.Thread(target=start_webhook)
    server_thread.daemon = True # 设为时候进程
    server_thread.start()

def main():
    start_webhook_daemon()
    while True:
        time.sleep(1)


if __name__ == '__main__':
    log_msg('INFO', '开始记录日志')
    main()