# Copyright (c) 2021 - Present Creeper_xiaopa
# Licensed under the MIT License. See the LICENSE file in the project root for details.


import dotenv
import os


_cache = {}


def get(env_name, deafult=None):
    """获取环境变量"""
    if env_name not in _cache:  # 检测是否包含在缓存中
        dotenv.load_dotenv(verbose=True)
        _cache[env_name] = os.getenv(env_name)

    # 如果环境变量为None，返回默认值
    return _cache[env_name] if _cache[env_name] is not None else deafult
    return _cache[env_name]


def flush():
    """清除缓存"""
    _cache.clear()
