"""
Configuration Validation and Type Safety - 配置验证和类型安全
提供配置验证和类型安全增强功能
"""

from typing import Any, Callable, Type, Union, Optional
from enum import Enum

from ...common_utilities_and_helpers.custom_exception_classes import ConfigurationException


class ConfigurationValidator:
    """
    Configuration Validator - 配置验证器
    
    提供配置项的验证功能
    """
    
    @staticmethod
    def validate_required(value: Any, field_name: str) -> None:
        """
        Validate Required Field - 验证必填字段
        
        Args:
            value: 字段值
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果字段值为空
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ConfigurationException(
                message=f"Required field '{field_name}' is missing or empty",
                config_key=field_name
            )
    
    @staticmethod
    def validate_type(value: Any, expected_type: Type, field_name: str) -> None:
        """
        Validate Type - 验证类型
        
        Args:
            value: 字段值
            expected_type: 期望的类型
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果类型不匹配
        """
        if not isinstance(value, expected_type):
            raise ConfigurationException(
                message=f"Field '{field_name}' must be of type {expected_type.__name__}, got {type(value).__name__}",
                config_key=field_name,
                details={
                    'expected_type': expected_type.__name__,
                    'actual_type': type(value).__name__
                }
            )
    
    @staticmethod
    def validate_range(
        value: Union[int, float],
        min_value: Union[int, float],
        max_value: Union[int, float],
        field_name: str
    ) -> None:
        """
        Validate Range - 验证数值范围
        
        Args:
            value: 字段值
            min_value: 最小值
            max_value: 最大值
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果值不在范围内
        """
        if not (min_value <= value <= max_value):
            raise ConfigurationException(
                message=f"Field '{field_name}' must be between {min_value} and {max_value}, got {value}",
                config_key=field_name,
                details={
                    'min_value': min_value,
                    'max_value': max_value,
                    'actual_value': value
                }
            )
    
    @staticmethod
    def validate_enum(value: Any, enum_class: Type[Enum], field_name: str) -> None:
        """
        Validate Enum - 验证枚举值
        
        Args:
            value: 字段值
            enum_class: 枚举类
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果值不是有效的枚举值
        """
        if not isinstance(value, enum_class):
            valid_values = [e.value for e in enum_class]
            raise ConfigurationException(
                message=f"Field '{field_name}' must be one of {valid_values}, got {value}",
                config_key=field_name,
                details={
                    'valid_values': valid_values,
                    'actual_value': value
                }
            )
    
    @staticmethod
    def validate_choice(value: Any, choices: list, field_name: str) -> None:
        """
        Validate Choice - 验证选项
        
        Args:
            value: 字段值
            choices: 可选值列表
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果值不在选项列表中
        """
        if value not in choices:
            raise ConfigurationException(
                message=f"Field '{field_name}' must be one of {choices}, got {value}",
                config_key=field_name,
                details={
                    'valid_choices': choices,
                    'actual_value': value
                }
            )
    
    @staticmethod
    def validate_pattern(value: str, pattern: str, field_name: str) -> None:
        """
        Validate Pattern - 验证正则表达式
        
        Args:
            value: 字段值
            pattern: 正则表达式模式
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果值不匹配模式
        """
        import re
        if not re.match(pattern, str(value)):
            raise ConfigurationException(
                message=f"Field '{field_name}' does not match pattern {pattern}",
                config_key=field_name,
                details={
                    'pattern': pattern,
                    'actual_value': value
                }
            )
    
    @staticmethod
    def validate_callable(value: Any, field_name: str) -> None:
        """
        Validate Callable - 验证可调用对象
        
        Args:
            value: 字段值
            field_name: 字段名称
            
        Raises:
            ConfigurationException: 如果值不是可调用对象
        """
        if not callable(value):
            raise ConfigurationException(
                message=f"Field '{field_name}' must be callable, got {type(value).__name__}",
                config_key=field_name
            )


class TypeSafeWrapper:
    """
    Type Safe Wrapper - 类型安全包装器
    
    提供类型安全的值包装和转换
    """
    
    @staticmethod
    def to_string(value: Any, default: str = "") -> str:
        """转换为字符串"""
        if value is None:
            return default
        return str(value)
    
    @staticmethod
    def to_int(value: Any, default: int = 0) -> int:
        """转换为整数"""
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def to_float(value: Any, default: float = 0.0) -> float:
        """转换为浮点数"""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def to_bool(value: Any, default: bool = False) -> bool:
        """转换为布尔值"""
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        return bool(value)
    
    @staticmethod
    def to_list(value: Any, default: list = None) -> list:
        """转换为列表"""
        if value is None:
            return default or []
        if isinstance(value, list):
            return value
        if isinstance(value, (tuple, set)):
            return list(value)
        return [value]
    
    @staticmethod
    def to_dict(value: Any, default: dict = None) -> dict:
        """转换为字典"""
        if value is None:
            return default or {}
        if isinstance(value, dict):
            return value
        return default or {}


def validate_configuration(config_dict: dict, schema: dict) -> tuple[bool, list]:
    """
    Validate Configuration Against Schema - 根据模式验证配置
    
    Args:
        config_dict: 配置字典
        schema: 配置模式
        
    Returns:
        tuple[bool, list]: (是否有效, 错误列表)
    """
    errors = []
    
    for field_name, rules in schema.items():
        value = config_dict.get(field_name)
        
        # 必填检查
        if rules.get('required', False):
            try:
                ConfigurationValidator.validate_required(value, field_name)
            except ConfigurationException as e:
                errors.append(e)
        
        # 类型检查
        if 'type' in rules and value is not None:
            try:
                ConfigurationValidator.validate_type(value, rules['type'], field_name)
            except ConfigurationException as e:
                errors.append(e)
        
        # 范围检查
        if 'min' in rules or 'max' in rules:
            try:
                min_val = rules.get('min', float('-inf'))
                max_val = rules.get('max', float('inf'))
                ConfigurationValidator.validate_range(value, min_val, max_val, field_name)
            except ConfigurationException as e:
                errors.append(e)
        
        # 选项检查
        if 'choices' in rules:
            try:
                ConfigurationValidator.validate_choice(value, rules['choices'], field_name)
            except ConfigurationException as e:
                errors.append(e)
    
    return len(errors) == 0, errors


__all__ = [
    'ConfigurationValidator',
    'TypeSafeWrapper',
    'validate_configuration',
]
