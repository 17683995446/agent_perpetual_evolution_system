"""
Prometheus Monitoring Integration - Prometheus 监控集成
提供系统指标的收集、暴露和监控
"""

import time
import uuid
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class SimplePrometheusClient:
    """
    简单 Prometheus 客户端 - 收集和暴露系统指标
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self._counters = defaultdict(int)
        self._gauges = {}
        self._histograms = defaultdict(list)
        self._start_time = time.time()
        
        if self.logger:
            self.logger.log_information_message(
                "PrometheusMonitoring",
                "Prometheus monitoring initialized"
            )
    
    def increment_counter(self, metric_name: str, labels: Dict[str, str] = None, value: int = 1) -> None:
        """
        增加计数器指标
        """
        key = f"{metric_name}-{str(labels)}"
        self._counters[key] += value
    
    def set_gauge(self, metric_name: str, value: float, labels: Dict[str, str] = None) -> None:
        """
        设置仪表盘指标
        """
        key = f"{metric_name}-{str(labels)}"
        self._gauges[key] = value
    
    def observe_histogram(self, metric_name: str, value: float, labels: Dict[str, str] = None) -> None:
        """
        观察直方图指标
        """
        key = f"{metric_name}-{str(labels)}"
        self._histograms[key].append(value)
        
        if len(self._histograms[key]) > 1000:
            self._histograms[key] = self._histograms[key][-1000:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        获取所有指标
        """
        return {
            "counters": dict(self._counters),
            "gauges": self._gauges,
            "histograms": {
                k: {
                    "count": len(v),
                    "mean": sum(v) / len(v) if v else 0,
                    "min": min(v) if v else 0,
                    "max": max(v) if v else 0
                }
                for k, v in self._histograms.items()
            },
            "uptime": time.time() - self._start_time
        }
    
    def format_prometheus_text(self) -> str:
        """
        格式化为 Prometheus 文本格式
        """
        lines = []
        
        for key, value in self._counters.items():
            metric_name = key.split("-")[0]
            lines.append(f"# HELP {metric_name} Counter metric")
            lines.append(f"# TYPE {metric_name} counter")
            lines.append(f"{metric_name} {value}")
        
        for key, value in self._gauges.items():
            metric_name = key.split("-")[0]
            lines.append(f"# HELP {metric_name} Gauge metric")
            lines.append(f"# TYPE {metric_name} gauge")
            lines.append(f"{metric_name} {value}")
        
        for key, data in self._histograms.items():
            metric_name = key.split("-")[0]
            lines.append(f"# HELP {metric_name} Histogram metric")
            lines.append(f"# TYPE {metric_name} histogram")
            lines.append(f"{metric_name}_count {data['count']}")
            lines.append(f"{metric_name}_sum {data['mean'] * data['count']}")
        
        return "\n".join(lines)


class SystemMetricsCollector:
    """
    系统指标收集器 - 收集系统级别的指标
    """
    
    def __init__(self, prometheus_client: SimplePrometheusClient):
        self.prometheus = prometheus_client
        self._task_execution_times = []
    
    def record_task_execution(self, task_type: str, success: bool, duration: float) -> None:
        """
        记录任务执行指标
        """
        labels = {"task_type": task_type, "success": str(success)}
        self.prometheus.increment_counter("agent_tasks_total", labels)
        self.prometheus.observe_histogram("agent_task_duration_seconds", duration, labels)
        
        if not success:
            self.prometheus.increment_counter("agent_task_failures_total", labels)
    
    def record_queue_depth(self, queue_size: int) -> None:
        """
        记录队列深度
        """
        self.prometheus.set_gauge("agent_queue_depth", queue_size)
    
    def record_worker_count(self, active_workers: int, total_workers: int) -> None:
        """
        记录工作线程数
        """
        self.prometheus.set_gauge("agent_active_workers", active_workers)
        self.prometheus.set_gauge("agent_total_workers", total_workers)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        获取指标摘要
        """
        metrics = self.prometheus.get_metrics()
        
        total_tasks = metrics.get("counters", {}).get("agent_tasks_total-{}", 0)
        task_failures = metrics.get("counters", {}).get("agent_task_failures_total-{}", 0)
        success_rate = (total_tasks - task_failures) / total_tasks if total_tasks > 0 else 1.0
        
        return {
            "total_tasks": total_tasks,
            "failed_tasks": task_failures,
            "success_rate": success_rate,
            "uptime_seconds": metrics.get("uptime", 0)
        }


class MetricsMiddleware:
    """
    指标中间件 - 用于 API 端点的指标收集
    """
    
    def __init__(self, prometheus_client: SimplePrometheusClient):
        self.prometheus = prometheus_client
        self._request_times = []
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float) -> None:
        """
        记录请求指标
        """
        labels = {
            "method": method,
            "endpoint": endpoint,
            "status_code": str(status_code)
        }
        
        self.prometheus.increment_counter("http_requests_total", labels)
        self.prometheus.observe_histogram("http_request_duration_seconds", duration, labels)
        
        if status_code >= 400:
            self.prometheus.increment_counter("http_errors_total", labels)
    
    def get_request_summary(self) -> Dict[str, Any]:
        """
        获取请求摘要
        """
        metrics = self.prometheus.get_metrics()
        
        total_requests = metrics.get("counters", {}).get("http_requests_total-{}", 0)
        total_errors = metrics.get("counters", {}).get("http_errors_total-{}", 0)
        
        return {
            "total_requests": total_requests,
            "error_count": total_errors,
            "error_rate": total_errors / total_requests if total_requests > 0 else 0
        }


__all__ = [
    "SimplePrometheusClient",
    "SystemMetricsCollector",
    "MetricsMiddleware"
]
