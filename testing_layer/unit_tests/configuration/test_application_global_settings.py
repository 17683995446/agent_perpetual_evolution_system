"""
Unit Tests for Application Global Settings - 配置管理单元测试
测试应用程序全局设置的配置管理功能
"""

import pytest
import os
from pathlib import Path
from ...configuration_management_layer.application_global_settings import (
    ApplicationGlobalSettings,
    get_application_global_settings
)


class TestApplicationGlobalSettings:
    """
    Test Application Global Settings - 应用程序全局设置测试
    验证配置类的默认设置和功能
    """
    
    def test_default_application_name(self):
        """
        Test Default Application Name - 测试默认应用程序名称
        """
        settings = ApplicationGlobalSettings()
        assert settings.APPLICATION_NAME == "Agent Perpetual Evolution System"
    
    def test_default_application_version(self):
        """
        Test Default Application Version - 测试默认应用程序版本
        """
        settings = ApplicationGlobalSettings()
        assert settings.APPLICATION_VERSION == "3.0.0"
    
    def test_default_debug_mode_disabled(self):
        """
        Test Default Debug Mode Disabled - 测试默认调试模式关闭
        """
        settings = ApplicationGlobalSettings()
        assert settings.DEBUG_MODE_ENABLED is False
    
    def test_default_api_server_host(self):
        """
        Test Default API Server Host - 测试默认API服务器主机
        """
        settings = ApplicationGlobalSettings()
        assert settings.API_SERVER_HOST == "0.0.0.0"
    
    def test_default_api_server_port(self):
        """
        Test Default API Server Port - 测试默认API服务器端口
        """
        settings = ApplicationGlobalSettings()
        assert settings.API_SERVER_PORT == 8000
    
    def test_default_storage_backend_type(self):
        """
        Test Default Storage Backend Type - 测试默认存储后端类型
        """
        settings = ApplicationGlobalSettings()
        assert settings.STORAGE_BACKEND_TYPE == "memory"
    
    def test_default_database_file_path(self):
        """
        Test Default Database File Path - 测试默认数据库文件路径
        """
        settings = ApplicationGlobalSettings()
        assert settings.DATABASE_FILE_PATH == "data/agent_system.db"
    
    def test_default_logging_level(self):
        """
        Test Default Logging Level - 测试默认日志级别
        """
        settings = ApplicationGlobalSettings()
        assert settings.LOGGING_LEVEL == "INFO"
    
    def test_settings_can_be_customized(self):
        """
        Test Settings Can Be Customized - 测试设置可以自定义
        """
        settings = ApplicationGlobalSettings(
            APPLICATION_NAME="Custom Agent System",
            APPLICATION_VERSION="4.0.0",
            DEBUG_MODE_ENABLED=True,
            API_SERVER_PORT=9000
        )
        
        assert settings.APPLICATION_NAME == "Custom Agent System"
        assert settings.APPLICATION_VERSION == "4.0.0"
        assert settings.DEBUG_MODE_ENABLED is True
        assert settings.API_SERVER_PORT == 9000


class TestApplicationGlobalSettingsFromEnv:
    """
    Test Application Global Settings From Env - 从环境变量加载配置测试
    验证环境变量覆盖功能
    """
    
    def test_environment_variable_override(self):
        """
        Test Environment Variable Override - 测试环境变量覆盖
        """
        os.environ["APPLICATION_NAME"] = "Env Override App"
        os.environ["API_SERVER_PORT"] = "8888"
        
        settings = ApplicationGlobalSettings(_env_file=".env")
        
        assert settings.APPLICATION_NAME == "Env Override App"
        assert settings.API_SERVER_PORT == 8888
        
        del os.environ["APPLICATION_NAME"]
        del os.environ["API_SERVER_PORT"]


class TestGetApplicationGlobalSettings:
    """
    Test Get Application Global Settings - 获取应用程序全局设置测试
    验证单例模式的实现
    """
    
    def test_get_settings_returns_singleton(self):
        """
        Test Get Settings Returns Singleton - 测试获取设置返回单例
        """
        settings1 = get_application_global_settings()
        settings2 = get_application_global_settings()
        assert settings1 is settings2
    
    def test_get_settings_returns_correct_type(self):
        """
        Test Get Settings Returns Correct Type - 测试获取设置返回正确类型
        """
        settings = get_application_global_settings()
        assert isinstance(settings, ApplicationGlobalSettings)
    
    def test_get_settings_has_all_required_fields(self):
        """
        Test Get Settings Has All Required Fields - 测试获取设置具有所有必需字段
        """
        settings = get_application_global_settings()
        
        required_fields = [
            'APPLICATION_NAME',
            'APPLICATION_VERSION',
            'DEBUG_MODE_ENABLED',
            'API_SERVER_HOST',
            'API_SERVER_PORT',
            'STORAGE_BACKEND_TYPE',
            'DATABASE_FILE_PATH',
            'LOGGING_LEVEL'
        ]
        
        for field in required_fields:
            assert hasattr(settings, field)
