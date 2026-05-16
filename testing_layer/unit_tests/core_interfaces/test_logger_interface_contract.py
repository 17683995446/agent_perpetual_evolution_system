"""
Unit Tests for Logger Interface Contract - 日志接口契约单元测试
测试CoreLoggerInterfaceContract抽象接口的契约定义
"""

import pytest
from abc import ABC
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class TestLoggerInterfaceContract:
    """
    Test Logger Interface Contract - 日志接口契约测试
    验证接口是抽象基类且定义了所有必需方法
    """
    
    def test_logger_interface_is_abstract_base_class(self):
        """
        Test Logger Interface Is Abstract Base Class - 测试日志接口是抽象基类
        """
        assert issubclass(CoreLoggerInterfaceContract, ABC)
    
    def test_logger_interface_has_info_method(self):
        """
        Test Logger Interface Has Info Method - 测试日志接口有信息方法
        """
        assert hasattr(CoreLoggerInterfaceContract, 'log_information_message')
    
    def test_logger_interface_has_warning_method(self):
        """
        Test Logger Interface Has Warning Method - 测试日志接口有警告方法
        """
        assert hasattr(CoreLoggerInterfaceContract, 'log_warning_message')
    
    def test_logger_interface_has_error_method(self):
        """
        Test Logger Interface Has Error Method - 测试日志接口有错误方法
        """
        assert hasattr(CoreLoggerInterfaceContract, 'log_error_message')
    
    def test_logger_interface_has_debug_method(self):
        """
        Test Logger Interface Has Debug Method - 测试日志接口有调试方法
        """
        assert hasattr(CoreLoggerInterfaceContract, 'log_debug_message')


class MockLoggerImplementation(CoreLoggerInterfaceContract):
    """
    Mock Logger Implementation - 模拟日志实现
    用于测试接口契约的完整实现
    """
    
    def __init__(self):
        self.log_messages = []
    
    def log_information_message(self, module_name: str, message_text: str, **kwargs):
        self.log_messages.append({
            "level": "INFO",
            "module": module_name,
            "message": message_text,
            "extra": kwargs
        })
    
    def log_warning_message(self, module_name: str, message_text: str, **kwargs):
        self.log_messages.append({
            "level": "WARNING",
            "module": module_name,
            "message": message_text,
            "extra": kwargs
        })
    
    def log_error_message(self, module_name: str, message_text: str, **kwargs):
        self.log_messages.append({
            "level": "ERROR",
            "module": module_name,
            "message": message_text,
            "extra": kwargs
        })
    
    def log_debug_message(self, module_name: str, message_text: str, **kwargs):
        self.log_messages.append({
            "level": "DEBUG",
            "module": module_name,
            "message": message_text,
            "extra": kwargs
        })


class TestMockLoggerImplementation:
    """
    Test Mock Logger Implementation - 模拟日志实现测试
    验证接口实现的正确性
    """
    
    def test_mock_logger_can_be_instantiated(self):
        """
        Test Mock Logger Can Be Instantiated - 测试模拟日志可以实例化
        """
        mock_logger = MockLoggerImplementation()
        assert mock_logger is not None
        assert isinstance(mock_logger, CoreLoggerInterfaceContract)
    
    def test_mock_logger_info_logging(self):
        """
        Test Mock Logger Info Logging - 测试模拟日志信息记录
        """
        mock_logger = MockLoggerImplementation()
        mock_logger.log_information_message("TestModule", "Test message", key="value")
        
        assert len(mock_logger.log_messages) == 1
        log_entry = mock_logger.log_messages[0]
        assert log_entry["level"] == "INFO"
        assert log_entry["module"] == "TestModule"
        assert log_entry["message"] == "Test message"
        assert log_entry["extra"]["key"] == "value"
    
    def test_mock_logger_warning_logging(self):
        """
        Test Mock Logger Warning Logging - 测试模拟日志警告记录
        """
        mock_logger = MockLoggerImplementation()
        mock_logger.log_warning_message("TestModule", "Warning message")
        
        assert len(mock_logger.log_messages) == 1
        assert mock_logger.log_messages[0]["level"] == "WARNING"
    
    def test_mock_logger_error_logging(self):
        """
        Test Mock Logger Error Logging - 测试模拟日志错误记录
        """
        mock_logger = MockLoggerImplementation()
        mock_logger.log_error_message("TestModule", "Error message")
        
        assert len(mock_logger.log_messages) == 1
        assert mock_logger.log_messages[0]["level"] == "ERROR"
    
    def test_mock_logger_debug_logging(self):
        """
        Test Mock Logger Debug Logging - 测试模拟日志调试记录
        """
        mock_logger = MockLoggerImplementation()
        mock_logger.log_debug_message("TestModule", "Debug message")
        
        assert len(mock_logger.log_messages) == 1
        assert mock_logger.log_messages[0]["level"] == "DEBUG"
