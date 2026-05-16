"""
Agent Perpetual Evolution System - 01 Configuration Management Layer
Agent永续自进化运行系统 - 01配置管理层

管理应用程序的所有配置设置
"""

from .application_global_settings import (
    ApplicationGlobalSettings,
    get_application_global_settings,
)

__all__ = [
    'ApplicationGlobalSettings',
    'get_application_global_settings',
]
