"""
Infrastructure Adapter Layer - Structured Logger Implementation
基础设施适配层 - 结构化日志框架实现

使用structlog库实现的日志记录器
支持多种输出格式和结构化日志
支持控制台、文件等多个输出目标
"""

from typing import Optional
import structlog
import sys

from ...core_abstraction_layer.interfaces.logging_interface_contract import (
    CoreLoggerInterfaceContract,
)


class StructuredLoggerFrameworkImplementation(CoreLoggerInterfaceContract):
    """
    Structured Logger Framework Implementation - 结构化日志框架实现
    
    使用structlog库实现的日志记录器
    支持多种输出格式和结构化日志
    支持控制台、文件等多个输出目标
    """
    
    def __init__(self, storage_backend=None):
        """
        Initialize Structured Logger Framework Implementation - 初始化结构化日志框架实现
        
        Args:
            storage_backend: 可选的存储后端，用于持久化日志
        """
        self.storage_backend = storage_backend
        self._configure_structlog_system()
    
    def _configure_structlog_system(self):
        """
        Configure Structlog System - 配置structlog系统
        """
        # 使用数值日志级别避免版本兼容性问题
        INFO_LOG_LEVEL = 20  # structlog.INFO = 20
        
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer() if sys.stderr.isatty() else structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(INFO_LOG_LEVEL),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    
    def log_information_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Information Message - 记录信息日志消息
        """
        structlog.get_logger().info(message_text, module=module_name, **kwargs)
    
    def log_warning_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Warning Message - 记录警告日志消息
        """
        structlog.get_logger().warning(message_text, module=module_name, **kwargs)
    
    def log_error_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Error Message - 记录错误日志消息
        """
        structlog.get_logger().error(message_text, module=module_name, **kwargs)
    
    def log_debug_message(self, module_name: str, message_text: str, **kwargs):
        """
        Log Debug Message - 记录调试日志消息
        """
        structlog.get_logger().debug(message_text, module=module_name, **kwargs)


__all__ = ['StructuredLoggerFrameworkImplementation']
