"""
Core Abstraction Layer - Logging Interface Contract
核心抽象层 - 日志接口契约

定义所有日志实现必须遵循的标准接口
支持结构化日志和多种输出目标（控制台、文件、远程等）
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class CoreLoggerInterfaceContract(ABC):
    """
    Core Logger Interface Contract - 核心日志接口契约
    
    定义所有日志实现必须实现的标准方法
    支持结构化日志和多种输出目标
    """
    
    @abstractmethod
    def log_information_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Information Message - 记录信息日志消息
        
        Args:
            module_name: 产生日志的模块名称
            message_text: 日志消息文本
            **kwargs: 额外的结构化字段
        """
        pass
    
    @abstractmethod
    def log_warning_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Warning Message - 记录警告日志消息
        """
        pass
    
    @abstractmethod
    def log_error_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Error Message - 记录错误日志消息
        """
        pass
    
    @abstractmethod
    def log_debug_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Debug Message - 记录调试日志消息
        """
        pass


__all__ = [
    'CoreLoggerInterfaceContract',
]
