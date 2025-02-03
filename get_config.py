import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Literal

def readonly_property(name):
    # 生成只读属性访问私有变量
    private_name = f'_{name}'
    return property(lambda self: getattr(self, private_name))

@dataclass
class BotConfig:
    _config_version: int
    _webhook_host: str
    _webhook_port: int
    _onebot_addr: str
    _onebot_token: str
    _group_mode: Literal["all", "whitelist", "blacklist"]
    _group_list: List[int]
    _ai_base_url: str
    _ai_api_key: str
    _ai_model: str
    _ai_temperature: float

    # 自动生成只读属性
    config_version = readonly_property('config_version')
    webhook_host = readonly_property('webhook_host')
    webhook_port = readonly_property('webhook_port')
    onebot_addr = readonly_property('onebot_addr')
    onebot_token = readonly_property('onebot_token')
    group_mode = readonly_property('group_mode')
    group_list = readonly_property('group_list')
    ai_base_url = readonly_property('ai_base_url')
    ai_api_key = readonly_property('ai_api_key')
    ai_model = readonly_property('ai_model')
    ai_temperature = readonly_property('ai_temperature')

    @classmethod
    def from_dict(cls, data: dict) -> "BotConfig":

        # 从字典构造配置对象
        return cls(
            _config_version=data.get("config_version", 1),
            _webhook_host=data.get("webhook_service", {}).get("host", "0.0.0.0"),
            _webhook_port=data.get("webhook_service", {}).get("port", 8080),
            _onebot_addr=data.get("onebot_server", {}).get("address", ""),
            _onebot_token=data.get("onebot_server", {}).get("token", ""),
            _group_mode=data.get("group_management", {}).get("mode", "whitelist"),
            _group_list=data.get("group_management", {}).get("group_list", []),
            _ai_base_url=data.get("ai", {}).get("base_url", ""),
            _ai_api_key=data.get("ai", {}).get("api_key", ""),
            _ai_model=data.get("ai", {}).get("model", ""),
            _ai_temperature=data.get("ai", {}).get("temperature", 0.7),
        )

    def validate(self) -> None:
        # 验证配置项有效性，无效时抛出ValueError
        errors = []

        # 验证配置版本
        if self._config_version != 1:
            errors.append(f"配置版本 {self._config_version} 不支持, 请使用当前版本1")

        # 验证webhook服务配置
        if not self._webhook_host:
            errors.append("WebHook服务主机不能为空")
        if not (1 <= self._webhook_port <= 65535):
            errors.append(f"无效WebHook端口 {self._webhook_port} (应为1-65535)")

        # 验证OneBot服务器配置
        if not self._onebot_addr.startswith(("http://", "https://")):
            errors.append(f"错误的OneBot地址 {self._onebot_addr} (应以 http(s):// 开头)")

        # 验证群组管理模式
        valid_modes = ["all", "whitelist", "blacklist"]
        if self._group_mode not in valid_modes:
            errors.append(f"无效的群组模式 {self._group_mode} 无效")
        if not isinstance(self._group_list, list):
            errors.append("错误的群组列表")
        else:
            for g in self._group_list:
                if not isinstance(g, int) or g <= 0:
                    errors.append(f"群号 {g} 无效 (必须为正整数)")

        # 验证AI配置
        if not self._ai_base_url:
            errors.append("AI服务地址不能为空")
        if not self._ai_api_key:
            errors.append("AI API密钥不能为空")
        if not self._ai_model:
            errors.append("AI模型名称不能为空")
        if not (0.0 <= self._ai_temperature <= 2.0):
            errors.append(f"AI温度参数无效: {self._ai_temperature} (范围0.0-2.0)")

        if errors:
            error_msg = "配置验证失败:\n  " + "\n  ".join(errors)
            raise ValueError(error_msg)

bot_config: BotConfig = None

def load(config_path: str = 'config.yml') -> BotConfig:
    # 加载并验证配置文件
    global bot_config
    try:
        path = Path(config_path).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"配置文件 {path} 不存在")
        
        with path.open(encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}
        
        config = BotConfig.from_dict(config_data)
        config.validate()
        bot_config = config
        return config
    except Exception as e:
        raise RuntimeError(e) from e

if __name__ == "__main__":
    try:
        load()
    except RuntimeError as e:
        print(e)
        exit(1)