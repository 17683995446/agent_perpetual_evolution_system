"""
Agent永续自进化系统 v9.0.0 - 系统优化与改进模块

包含：
- 输入校验与异常处理
- 性能优化（缓存机制）
- 线程安全机制
- 限流保护
- 日志与监控
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import time
import threading
import functools
from collections import OrderedDict


class InputValidator:
    """输入校验器 - 增强系统健壮性"""
    
    @staticmethod
    def validate_not_none(value, param_name: str):
        """校验参数不为None"""
        if value is None:
            raise ValueError(f"参数 '{param_name}' 不能为None")
    
    @staticmethod
    def validate_list_not_empty(items: List, param_name: str, min_length: int = 1):
        """校验列表不为空且满足最小长度"""
        InputValidator.validate_not_none(items, param_name)
        
        if not isinstance(items, list):
            raise TypeError(f"参数 '{param_name}' 必须是列表类型，当前类型: {type(items)}")
        
        if len(items) < min_length:
            raise ValueError(f"参数 '{param_name}' 长度至少为 {min_length}，当前长度: {len(items)}")
    
    @staticmethod
    def safe_list(items, default: List = None):
        """安全的列表处理 - 遇到异常返回默认值"""
        if default is None:
            default = []
        
        if items is None:
            return default
        
        if isinstance(items, list):
            return items
        
        try:
            return list(items)
        except:
            return default


class LRUCache:
    """LRU缓存机制 - 提升性能"""
    
    def __init__(self, maxsize: int = 1000, ttl_seconds: int = 300):
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.ttl_seconds = ttl_seconds
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self.lock:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            # 检查是否过期
            if (datetime.now() - timestamp).total_seconds() > self.ttl_seconds:
                del self.cache[key]
                return None
            
            # 移到末尾（最近使用）
            self.cache.move_to_end(key)
            return value
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            elif len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
            
            self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()

    def delete(self, key: str) -> bool:
        """删除指定键的缓存"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False


class ThreadSafeCounter:
    """线程安全计数器 - 用于限流"""
    
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.counter += 1
            return self.counter
    
    def get(self):
        with self.lock:
            return self.counter


class RateLimiter:
    """限流保护 - 防止系统过载"""
    
    def __init__(self, max_requests: int = 1000, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.counter = ThreadSafeCounter()
        self.window_start = datetime.now()
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            now = datetime.now()
            
            # 检查是否需要重置窗口
            if (now - self.window_start).total_seconds() > self.window_seconds:
                self.counter = ThreadSafeCounter()
                self.window_start = now
            
            count = self.counter.increment()
            return count <= self.max_requests


def with_retry(max_attempts: int = 3, delay_seconds: float = 0.1):
    """重试装饰器 - 提高请求成功率"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    if attempts < max_attempts:
                        time.sleep(delay_seconds * (2 ** (attempts - 1)))
            
            raise last_exception
        return wrapper
    return decorator


def with_validation(validator_func):
    """输入校验装饰器 - 简化参数检查"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validator_func(*args, **kwargs)
            except Exception as validation_error:
                raise ValueError(f"参数校验失败: {validation_error}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def with_cache(cache: LRUCache, key_func: Callable = lambda *args, **kwargs: str(args) + str(kwargs)):
    """缓存装饰器 - 自动缓存结果"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator


class SystemMonitor:
    """系统监控器 - 收集性能数据"""
    
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
    
    def record_metric(self, name: str, value: float):
        """记录一个指标"""
        with self.lock:
            self.metrics[name] = {
                "value": value,
                "timestamp": datetime.now()
            }
    
    def get_metrics(self) -> Dict[str, Dict]:
        """获取所有指标"""
        with self.lock:
            return dict(self.metrics)
    
    def report(self) -> str:
        """生成报告"""
        metrics = self.get_metrics()
        report_lines = [
            "="*60,
            "📊 系统性能监控报告",
            "="*60
        ]
        
        for name, data in metrics.items():
            report_lines.append(f"  {name}: {data['value']} (at {data['timestamp']})")
        
        report_lines.append("="*60)
        return "\n".join(report_lines)


# 全局优化对象
_global_cache = LRUCache(maxsize=500)
_global_rate_limiter = RateLimiter(max_requests=1000, window_seconds=60)
_global_monitor = SystemMonitor()


def get_global_cache() -> LRUCache:
    """获取全局缓存"""
    return _global_cache


def get_global_rate_limiter() -> RateLimiter:
    """获取全局限流器"""
    return _global_rate_limiter


def get_global_monitor() -> SystemMonitor:
    """获取全局监控器"""
    return _global_monitor


print("✅ 系统优化模块加载完成！")
