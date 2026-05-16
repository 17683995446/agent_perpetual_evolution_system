"""
Unit Tests for Structured Logger Framework Implementation - 结构化日志框架实现单元测试
测试结构化日志记录器的功能
"""

import pytest
import io
import sys
from ...infrastructure_adapter_layer.logging_framework.structured_logger_framework_implementation import StructuredLoggerFrameworkImplementation


class TestStructuredLoggerFrameworkImplementation:
    """
    Test Structured Logger Framework Implementation - 结构化日志框架实现测试
    验证日志记录器的基本功能
    """
    
    def test_logger_can_be_instantiated(self):
        """
        Test Logger Can Be Instantiated - 测试日志记录器可以实例化
        """
        logger = StructuredLoggerFrameworkImplementation()
        assert logger is not None
    
    def test_logger_with_storage_backend(self):
        """
        Test Logger With Storage Backend - 测试带存储后端的日志记录器
        """
        mock_storage = {"logs": []}
        logger = StructuredLoggerFrameworkImplementation(storage_backend=mock_storage)
        assert logger.storage_backend == mock_storage
    
    def test_logger_info_message(self):
        """
        Test Logger Info Message - 测试日志记录器信息消息
        """
        logger = StructuredLoggerFrameworkImplementation()
        logger.log_information_message("TestModule", "Test info message")
    
    def test_logger_warning_message(self):
        """
        Test Logger Warning Message - 测试日志记录器警告消息
        """
        logger = StructuredLoggerFrameworkImplementation()
        logger.log_warning_message("TestModule", "Test warning message")
    
    def test_logger_error_message(self):
        """
        Test Logger Error Message - 测试日志记录器错误消息
        """
        logger = StructuredLoggerFrameworkImplementation()
        logger.log_error_message("TestModule", "Test error message")
    
    def test_logger_debug_message(self):
        """
        Test Logger Debug Message - 测试日志记录器调试消息
        """
        logger = StructuredLoggerFrameworkImplementation()
        logger.log_debug_message("TestModule", "Test debug message")
    
    def test_logger_message_with_extra_kwargs(self):
        """
        Test Logger Message With Extra Kwargs - 测试带额外参数的消息
        """
        logger = StructuredLoggerFrameworkImplementation()
        logger.log_information_message(
            "TestModule",
            "Message with extra data",
            key1="value1",
            key2=123
        )


class TestStructuredLoggerOutput:
    """
    Test Structured Logger Output - 结构化日志输出测试
    验证日志输出到不同的目标
    """
    
    def test_logger_outputs_to_console(self):
        """
        Test Logger Outputs To Console - 测试日志输出到控制台
        """
        logger = StructuredLoggerFrameworkImplementation()
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            logger.log_information_message("ConsoleModule", "Console test message")
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        
        assert len(output) > 0
