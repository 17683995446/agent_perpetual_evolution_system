"""
Performance Optimization Utilities - 性能优化工具
提供缓存、懒加载、性能分析等优化功能
"""

import time
import functools
import threading
from typing import Any, Callable, Optional, Dict
from collections import OrderedDict
from datetime import datetime, timedelta


class LRUCache:
    """
    LRU (Least Recently Used) Cache - 最近最少使用缓存
    
    提供线程安全的 LRU 缓存实现
    """
    
    def __init__(self, max_size: int = 128, ttl_seconds: Optional[float] = None):
        """
        Initialize LRU Cache - 初始化 LRU 缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl_seconds: 缓存过期时间（秒），None 表示永不过期
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache = OrderedDict()
        self._timestamps = {}
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get Value From Cache - 从缓存获取值
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            缓存的值或默认值
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return default
            
            # 检查过期
            if self.ttl_seconds is not None:
                timestamp = self._timestamps.get(key)
                if timestamp and (time.time() - timestamp) > self.ttl_seconds:
                    del self._cache[key]
                    del self._timestamps[key]
                    self._misses += 1
                    return default
            
            # 移到末尾（最近使用）
            self._cache.move_to_end(key)
            self._hits += 1
            return self._cache[key]
    
    def set(self, key: str, value: Any):
        """
        Set Value In Cache - 设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self.max_size:
                    # 删除最旧的条目
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                    del self._timestamps[oldest_key]
                
                self._cache[key] = value
            
            self._timestamps[key] = time.time()
    
    def delete(self, key: str):
        """
        Delete Value From Cache - 从缓存删除值
        
        Args:
            key: 缓存键
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]
    
    def clear(self):
        """Clear All Cache - 清空所有缓存"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
            self._hits = 0
            self._misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get Cache Statistics - 获取缓存统计
        
        Returns:
            缓存统计字典
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0.0
            
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': hit_rate,
                'ttl_seconds': self.ttl_seconds
            }


def cached(
    max_size: int = 128,
    ttl_seconds: Optional[float] = None,
    key_func: Optional[Callable] = None
):
    """
    Cached Decorator - 缓存装饰器
    
    Args:
        max_size: 最大缓存数
        ttl_seconds: 缓存过期时间
        key_func: 自定义键生成函数
        
    Returns:
        装饰器函数
    """
    cache = LRUCache(max_size=max_size, ttl_seconds=ttl_seconds)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            
            return result
        
        # 添加缓存属性
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.get_stats
        
        return wrapper
    
    return decorator


def timed(max_calls: Optional[int] = None):
    """
    Timed Decorator - 计时装饰器
    
    Args:
        max_calls: 最大调用次数，超过后输出警告
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        func._call_count = 0
        func._total_time = 0.0
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            func._call_count += 1
            func._total_time += duration
            
            # 检查最大调用次数
            if max_calls and func._call_count > max_calls:
                print(f"⚠️  Warning: {func.__name__} called {func._call_count} times (max: {max_calls})")
            
            # 添加执行时间到结果
            if isinstance(result, dict):
                result['_execution_time'] = duration
            
            return result
        
        wrapper.get_stats = lambda: {
            'call_count': func._call_count,
            'total_time': func._total_time,
            'average_time': func._total_time / func._call_count if func._call_count > 0 else 0
        }
        
        return wrapper
    
    return decorator


def lazy_property(func: Callable) -> property:
    """
    Lazy Property Decorator - 懒加载属性装饰器
    
    属性只在首次访问时计算一次，之后缓存结果
    
    Returns:
        属性对象
    """
    attr_name = f'_lazy_{func.__name__}'
    
    @property
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return wrapper


class LazyInitializer:
    """
    Lazy Initializer - 懒加载初始化器
    
    延迟初始化耗时的资源
    """
    
    def __init__(self, initializer: Callable, *args, **kwargs):
        """
        Initialize Lazy Initializer - 初始化懒加载初始化器
        
        Args:
            initializer: 初始化函数
            *args: 位置参数
            **kwargs: 关键字参数
        """
        self._initializer = initializer
        self._args = args
        self._kwargs = kwargs
        self._instance = None
        self._initialized = False
        self._lock = threading.RLock()
    
    def get_instance(self):
        """
        Get Instance - 获取实例
        
        如果尚未初始化，则执行初始化
        
        Returns:
            初始化后的实例
        """
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._instance = self._initializer(*self._args, **self._kwargs)
                    self._initialized = True
        
        return self._instance
    
    def reset(self):
        """Reset - 重置初始化状态"""
        with self._lock:
            self._instance = None
            self._initialized = False


class PerformanceProfiler:
    """
    Performance Profiler - 性能分析器
    
    提供函数级别的性能分析
    """
    
    def __init__(self):
        self._profiles = {}
        self._lock = threading.RLock()
    
    def profile(self, func: Callable) -> Callable:
        """
        Profile Decorator - 分析装饰器
        
        Args:
            func: 要分析的函数
            
        Returns:
            装饰后的函数
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            with self._lock:
                if func.__name__ not in self._profiles:
                    self._profiles[func.__name__] = {
                        'count': 0,
                        'total_time': 0.0,
                        'min_time': float('inf'),
                        'max_time': 0.0
                    }
                
                profile = self._profiles[func.__name__]
                profile['count'] += 1
                profile['total_time'] += duration
                profile['min_time'] = min(profile['min_time'], duration)
                profile['max_time'] = max(profile['max_time'], duration)
            
            return result
        
        return wrapper
    
    def get_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        Get Profiles - 获取所有分析结果
        
        Returns:
            分析结果字典
        """
        with self._lock:
            results = {}
            for name, profile in self._profiles.items():
                results[name] = {
                    **profile,
                    'avg_time': profile['total_time'] / profile['count'] if profile['count'] > 0 else 0
                }
            return results
    
    def reset(self):
        """Reset - 重置所有分析数据"""
        with self._lock:
            self._profiles.clear()


__all__ = [
    'LRUCache',
    'cached',
    'timed',
    'lazy_property',
    'LazyInitializer',
    'PerformanceProfiler',
]
