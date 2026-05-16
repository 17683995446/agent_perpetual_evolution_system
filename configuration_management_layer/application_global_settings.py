"""
Configuration Management Layer - Application Global Settings
配置管理层 - 应用程序全局设置

使用Pydantic管理应用程序的所有配置
支持环境变量加载和类型安全的配置管理
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class ApplicationGlobalSettings(BaseSettings):
    """
    Application Global Settings - 应用程序全局设置
    
    使用Pydantic管理应用程序的所有配置
    支持环境变量加载和类型安全
    """
    
    # 应用程序基本设置
    APPLICATION_NAME: str = "Agent Perpetual Evolution System"
    APPLICATION_VERSION: str = "3.0.0"
    DEBUG_MODE_ENABLED: bool = False
    
    # API服务器设置
    API_SERVER_HOST: str = "0.0.0.0"
    API_SERVER_PORT: int = 8000
    
    # 存储后端设置
    STORAGE_BACKEND_TYPE: str = "memory"  # 可选: memory, sqlite, redis
    DATABASE_FILE_PATH: str = "data/agent_system.db"
    DATA_DIRECTORY_PATH: str = "data"
    
    # 日志设置
    LOGGING_LEVEL: str = "INFO"
    LOG_TO_FILE_ENABLED: bool = False
    LOG_FILE_PATH: str = "logs/agent_system.log"
    
    class Config:
        """
        Config Class - 配置类
        """
        env_file = ".env"
        case_sensitive = True


# 全局单例设置
_application_settings_instance = None


def get_application_global_settings() -> ApplicationGlobalSettings:
    """
    Get Application Global Settings - 获取应用程序全局设置
    
    Returns:
        应用程序全局设置实例
    """
    global _application_settings_instance
    if _application_settings_instance is None:
        _application_settings_instance = ApplicationGlobalSettings()
        # 确保目录存在
        Path(_application_settings_instance.DATA_DIRECTORY_PATH).mkdir(
            parents=True, exist_ok=True
        )
    return _application_settings_instance


__all__ = [
    'ApplicationGlobalSettings',
    'get_application_global_settings',
]
