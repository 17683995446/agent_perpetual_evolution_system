"""
Error Handler Utilities - 错误处理工具
提供统一的错误处理和异常管理功能
"""

import traceback
import functools
from typing import Callable, Any, Optional, Type, Union
from .custom_exception_classes import AgentEvolutionSystemException


def handle_exceptions(
    default_return: Any = None,
    exception_types: Optional[Union[Type[Exception], tuple]] = None,
    log_errors: bool = True,
    reraise: bool = False
):
    """
    异常处理装饰器
    
    Args:
        default_return: 发生异常时返回的默认值
        exception_types: 要捕获的异常类型，默认捕获所有异常
        log_errors: 是否记录错误日志
        reraise: 是否重新抛出异常
    
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if exception_types and not isinstance(e, exception_types):
                    raise
                
                error_info = {
                    'function': func.__name__,
                    'args': str(args)[:100],
                    'kwargs': str(kwargs)[:100],
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
                
                if log_errors:
                    print(f"[ERROR] {func.__name__}: {e}")
                    traceback.print_exc()
                
                if reraise:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    exception_types: Optional[Union[Type[Exception], tuple]] = None,
    **kwargs
) -> Any:
    """
    安全执行函数
    
    Args:
        func: 要执行的函数
        *args: 位置参数
        default_return: 发生异常时返回的默认值
        exception_types: 要捕获的异常类型
        **kwargs: 关键字参数
    
    Returns:
        函数执行结果或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if exception_types and not isinstance(e, exception_types):
            raise
        
        print(f"[ERROR] {func.__name__}: {e}")
        traceback.print_exc()
        return default_return


def validate_and_raise(
    condition: bool,
    exception_class: Type[AgentEvolutionSystemException],
    message: str,
    **kwargs
):
    """
    验证条件并在不满足时抛出异常
    
    Args:
        condition: 要验证的条件
        exception_class: 异常类
        message: 错误消息
        **kwargs: 传递给异常类的参数
    """
    if not condition:
        raise exception_class(message=message, **kwargs)


class ErrorContext:
    """
    错误上下文管理器
    
    用于捕获和记录代码块的错误信息
    """
    
    def __init__(self, context_name: str, log_errors: bool = True):
        self.context_name = context_name
        self.log_errors = log_errors
        self.error_occurred = False
        self.error_message = None
        self.error_traceback = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.error_occurred = True
            self.error_message = str(exc_val)
            self.error_traceback = traceback.format_exception(exc_type, exc_val, exc_tb)
            
            if self.log_errors:
                print(f"[ERROR] {self.context_name}: {exc_val}")
                traceback.print_exc()
            
            return False  # 不抑制异常
        
        return True


class RetryExecutor:
    """
    重试执行器
    
    用于在失败时自动重试操作
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        exponential_backoff: bool = False,
        exceptions: Optional[tuple] = None
    ):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.exponential_backoff = exponential_backoff
        self.exceptions = exceptions or (Exception,)
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        执行函数并在失败时重试
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            函数执行结果
        """
        import time
        
        last_exception = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    if self.log_errors:
                        print(f"[RETRY] {func.__name__} failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                    
                    time.sleep(delay)
                    
                    if self.exponential_backoff:
                        delay *= 2
                else:
                    if self.log_errors:
                        print(f"[ERROR] {func.__name__} failed after {self.max_retries} retries: {e}")
        
        raise last_exception
    
    @property
    def log_errors(self) -> bool:
        return True


__all__ = [
    'handle_exceptions',
    'safe_execute',
    'validate_and_raise',
    'ErrorContext',
    'RetryExecutor',
]
