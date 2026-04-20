
import os
from pathlib import Path
from typing import Dict, Optional, Any
from dotenv import load_dotenv


import threading

class Config:
    """配置管理类，使用单例模式"""
    
    _instance: Optional['Config'] = None
    _initialized: bool = False
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, env_file: Optional[str] = None):
        if self._initialized:
            return
            
        self._config = {}
        self._load_env(env_file)
        self._initialized = True
    
    def _load_env(self, env_file: Optional[str] = None):
        """加载环境变量"""
        if env_file is None:
            env_file = Path(__file__).parent / '.env'
        
        if env_file.exists():
            load_dotenv(env_file)
        
        self._config = {
            'DB_HOST': os.getenv('DB_HOST', 'localhost'),
            'DB_PORT': int(os.getenv('DB_PORT', '3306')),
            'DB_USER': os.getenv('DB_USER', 'root'),
            'DB_PASSWORD': os.getenv('DB_PASSWORD', ''),
            'DB_NAME': os.getenv('DB_NAME', 'pomodoro_db'),
            'DB_CHARSET': os.getenv('DB_CHARSET', 'utf8mb4'),
            'APP_NAME': os.getenv('APP_NAME', '考研番茄钟'),
            'APP_VERSION': os.getenv('APP_VERSION', '1.0.0'),
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'BASE_DIR': Path(__file__).parent,
        }
    
    def get(self, key: str, default=None):
        """获取配置项"""
        return self._config.get(key, default)
    
    def set(self, key: str, value):
        """设置配置项（运行时）"""
        self._config[key] = value
    
    def all(self):
        """获取所有配置"""
        return self._config.copy()
    
    @property
    def db_url(self):
        """获取数据库连接URL"""
        return self.get_database_url()
    
    def get_database_url(self):
        """获取数据库连接URL"""
        return (
            f"mysql+mysqlconnector://{self.get('DB_USER')}:{self.get('DB_PASSWORD')}"
            f"@{self.get('DB_HOST')}:{self.get('DB_PORT')}/{self.get('DB_NAME')}"
            f"?charset={self.get('DB_CHARSET')}"
        )


config = Config()


def get_config(key: str, default=None):
    """
    安全获取配置项，自动处理导入异常

    Args:
        key: 配置键
        default: 默认值，当配置不存在或导入失败时返回

    Returns:
        配置值或默认值
    """
    try:
        return config.get(key, default)
    except (ImportError, AttributeError):
        return default
