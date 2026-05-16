"""
System Performance Monitor - 系统性能监控器
提供系统性能监控和指标收集功能
"""

import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque

# 可选导入 psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class SystemPerformanceMonitor:
    """
    System Performance Monitor - 系统性能监控器
    
    提供实时性能监控和指标收集功能
    包括 CPU、内存、任务执行时间等指标
    """
    
    def __init__(self, logger_backend: Optional[CoreLoggerInterfaceContract] = None):
        """
        Initialize System Performance Monitor - 初始化系统性能监控器
        
        Args:
            logger_backend: 日志后端（可选）
        """
        self.logger_backend = logger_backend
        
        # 性能指标
        self.task_execution_times = deque(maxlen=1000)
        self.task_success_counts = defaultdict(int)
        self.task_failure_counts = defaultdict(int)
        self.component_call_counts = defaultdict(int)
        self.component_execution_times = defaultdict(list)
        
        # 系统指标
        self.system_metrics_history = deque(maxlen=100)
        
        # 线程锁
        self._lock = threading.RLock()
        
        # 启动时间
        self.start_time = time.time()
        
        self.logger_backend and self.logger_backend.log_information_message(
            'SystemPerformanceMonitor',
            'Performance monitor initialized'
        )
    
    def record_task_execution(
        self,
        task_id: str,
        duration_seconds: float,
        success: bool,
        task_type: str = "general"
    ):
        """
        Record Task Execution - 记录任务执行
        
        Args:
            task_id: 任务ID
            duration_seconds: 执行时长（秒）
            success: 是否成功
            task_type: 任务类型
        """
        with self._lock:
            # 记录执行时间
            self.task_execution_times.append({
                'task_id': task_id,
                'duration': duration_seconds,
                'success': success,
                'task_type': task_type,
                'timestamp': datetime.now()
            })
            
            # 更新成功/失败计数
            if success:
                self.task_success_counts[task_type] += 1
            else:
                self.task_failure_counts[task_type] += 1
            
            self.logger_backend and self.logger_backend.log_debug_message(
                'SystemPerformanceMonitor',
                f'Task execution recorded: {task_id}',
                duration=duration_seconds,
                success=success
            )
    
    def record_component_call(
        self,
        component_name: str,
        duration_seconds: float
    ):
        """
        Record Component Call - 记录组件调用
        
        Args:
            component_name: 组件名称
            duration_seconds: 执行时长（秒）
        """
        with self._lock:
            self.component_call_counts[component_name] += 1
            self.component_execution_times[component_name].append(duration_seconds)
            
            # 限制历史记录大小
            if len(self.component_execution_times[component_name]) > 1000:
                self.component_execution_times[component_name] = self.component_execution_times[component_name][-1000:]
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """
        Collect System Metrics - 收集系统指标
        
        Returns:
            系统指标字典
        """
        try:
            metrics = {
                'timestamp': datetime.now(),
                'uptime_seconds': time.time() - self.start_time
            }
            
            if PSUTIL_AVAILABLE:
                try:
                    # CPU 使用率
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    cpu_count = psutil.cpu_count()
                    
                    # 内存使用
                    memory = psutil.virtual_memory()
                    
                    metrics['cpu'] = {
                        'percent': cpu_percent,
                        'count': cpu_count
                    }
                    metrics['memory'] = {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent,
                        'used': memory.used
                    }
                    
                    try:
                        # 进程信息
                        process = psutil.Process()
                        process_memory = process.memory_info()
                        metrics['process'] = {
                            'memory_rss': process_memory.rss,
                            'num_threads': process.num_threads()
                        }
                    except Exception:
                        pass
                        
                except Exception:
                    pass
            
            # 保存历史记录
            with self._lock:
                self.system_metrics_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SystemPerformanceMonitor',
                f'Failed to collect system metrics: {str(e)}'
            )
            return {'error': str(e)}
    
    def get_task_performance_summary(self) -> Dict[str, Any]:
        """
        Get Task Performance Summary - 获取任务性能摘要
        
        Returns:
            任务性能摘要字典
        """
        with self._lock:
            if not self.task_execution_times:
                return {
                    'total_tasks': 0,
                    'successful_tasks': 0,
                    'failed_tasks': 0,
                    'success_rate': 0.0,
                    'average_duration': 0.0
                }
            
            total = len(self.task_execution_times)
            successful = sum(1 for t in self.task_execution_times if t['success'])
            failed = total - successful
            
            avg_duration = sum(t['duration'] for t in self.task_execution_times) / total if total > 0 else 0
            
            # 按任务类型统计
            by_type = {}
            for task_data in self.task_execution_times:
                task_type = task_data['task_type']
                if task_type not in by_type:
                    by_type[task_type] = {
                        'count': 0,
                        'successful': 0,
                        'failed': 0,
                        'total_duration': 0
                    }
                by_type[task_type]['count'] += 1
                by_type[task_type]['total_duration'] += task_data['duration']
                if task_data['success']:
                    by_type[task_type]['successful'] += 1
                else:
                    by_type[task_type]['failed'] += 1
            
            # 计算每个类型的平均时间
            for task_type, data in by_type.items():
                data['average_duration'] = data['total_duration'] / data['count'] if data['count'] > 0 else 0
            
            return {
                'total_tasks': total,
                'successful_tasks': successful,
                'failed_tasks': failed,
                'success_rate': successful / total if total > 0 else 0.0,
                'average_duration': avg_duration,
                'by_task_type': by_type,
                'recent_window': list(self.task_execution_times)[-10:]  # 最近10个任务
            }
    
    def get_component_performance_summary(self) -> Dict[str, Any]:
        """
        Get Component Performance Summary - 获取组件性能摘要
        
        Returns:
            组件性能摘要字典
        """
        with self._lock:
            summary = {}
            
            for component_name, times in self.component_execution_times.items():
                if not times:
                    continue
                
                count = self.component_call_counts[component_name]
                avg_time = sum(times) / len(times) if times else 0
                min_time = min(times) if times else 0
                max_time = max(times) if times else 0
                
                summary[component_name] = {
                    'call_count': count,
                    'average_duration': avg_time,
                    'min_duration': min_time,
                    'max_duration': max_time,
                    'total_duration': sum(times)
                }
            
            return summary
    
    def get_overall_health_status(self) -> Dict[str, Any]:
        """
        Get Overall Health Status - 获取整体健康状态
        
        Returns:
            健康状态字典
        """
        try:
            # 收集系统指标
            metrics = self.collect_system_metrics()
            
            # 获取任务性能
            task_perf = self.get_task_performance_summary()
            
            # 计算健康分数
            health_score = 100.0
            
            # 扣分项
            if metrics.get('cpu', {}).get('percent', 0) > 80:
                health_score -= 20
            
            if metrics.get('memory', {}).get('percent', 0) > 85:
                health_score -= 25
            
            if task_perf.get('success_rate', 1.0) < 0.8:
                health_score -= 30
            
            # 确定健康状态
            if health_score >= 90:
                status = "excellent"
            elif health_score >= 70:
                status = "good"
            elif health_score >= 50:
                status = "warning"
            else:
                status = "critical"
            
            return {
                'status': status,
                'health_score': max(0, health_score),
                'timestamp': datetime.now(),
                'system_metrics': metrics,
                'task_performance': task_perf
            }
            
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SystemPerformanceMonitor',
                f'Failed to get health status: {str(e)}'
            )
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    def reset_metrics(self):
        """重置所有指标"""
        with self._lock:
            self.task_execution_times.clear()
            self.task_success_counts.clear()
            self.task_failure_counts.clear()
            self.component_call_counts.clear()
            self.component_execution_times.clear()
            self.system_metrics_history.clear()
            self.start_time = time.time()
            
            self.logger_backend and self.logger_backend.log_information_message(
                'SystemPerformanceMonitor',
                'All metrics reset'
            )
    
    def export_metrics(self) -> Dict[str, Any]:
        """
        Export All Metrics - 导出所有指标
        
        Returns:
            所有指标字典
        """
        with self._lock:
            return {
                'task_performance': self.get_task_performance_summary(),
                'component_performance': self.get_component_performance_summary(),
                'health_status': self.get_overall_health_status(),
                'system_metrics_history': list(self.system_metrics_history),
                'exported_at': datetime.now()
            }


class PerformanceMetricsContext:
    """
    Performance Metrics Context - 性能指标上下文管理器
    
    用于自动记录函数执行时间和性能指标
    """
    
    def __init__(
        self,
        monitor: SystemPerformanceMonitor,
        component_name: str,
        task_id: str = None,
        task_type: str = "general"
    ):
        self.monitor = monitor
        self.component_name = component_name
        self.task_id = task_id
        self.task_type = task_type
        self.start_time = None
        self.success = False
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.success = exc_type is None
        
        # 记录组件调用
        self.monitor.record_component_call(self.component_name, duration)
        
        # 如果是任务，记录任务执行
        if self.task_id:
            self.monitor.record_task_execution(
                self.task_id,
                duration,
                self.success,
                self.task_type
            )
        
        return False  # 不抑制异常


__all__ = [
    'SystemPerformanceMonitor',
    'PerformanceMetricsContext',
]
