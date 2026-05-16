"""
Adaptive System Module - 自适应系统模块
提供系统自适应、故障恢复、性能优化等功能
"""

import uuid
import time
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque

from ..core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class AdaptiveSystemController:
    """
    自适应系统控制器 - 自动调整系统参数和策略
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.current_parameters = {
            "max_workers": 4,
            "timeout": 300,
            "retry_count": 3,
            "batch_size": 10,
            "queue_size": 100,
            "cache_size": 1000
        }
        self.baseline_metrics = {}
        self.adjustment_history = deque(maxlen=100)
        self.health_history = deque(maxlen=1000)
    
    def initialize_baseline(self, metrics: Dict[str, Any]):
        """初始化基线指标"""
        self.baseline_metrics = metrics.copy()
        self.logger and self.logger.log_information_message(
            "AdaptiveSystemController",
            "Baseline metrics initialized",
            metrics=list(metrics.keys())
        )
    
    def analyze_and_adjust(self, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """分析指标并调整参数"""
        adjustments = []
        
        error_rate = current_metrics.get("error_rate", 0)
        if error_rate > 0.1:
            retry_count = self.current_parameters["retry_count"]
            new_retry = min(retry_count + 1, 5)
            adjustments.append({
                "parameter": "retry_count",
                "old_value": retry_count,
                "new_value": new_retry,
                "reason": f"High error rate: {error_rate:.2%}"
            })
            self.current_parameters["retry_count"] = new_retry
        
        latency = current_metrics.get("avg_latency", 0.1)
        baseline_latency = self.baseline_metrics.get("avg_latency", 0.1)
        if latency > baseline_latency * 1.5:
            workers = self.current_parameters["max_workers"]
            new_workers = min(workers + 2, 16)
            adjustments.append({
                "parameter": "max_workers",
                "old_value": workers,
                "new_value": new_workers,
                "reason": f"High latency: {latency:.3f}s vs baseline {baseline_latency:.3f}s"
            })
            self.current_parameters["max_workers"] = new_workers
        
        throughput = current_metrics.get("throughput", 0)
        if throughput < 10:
            batch_size = self.current_parameters["batch_size"]
            new_batch = min(batch_size + 5, 50)
            adjustments.append({
                "parameter": "batch_size",
                "old_value": batch_size,
                "new_value": new_batch,
                "reason": f"Low throughput: {throughput:.1f}/s"
            })
            self.current_parameters["batch_size"] = new_batch
        
        if adjustments:
            for adj in adjustments:
                self.adjustment_history.append({
                    **adj,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.logger and self.logger.log_information_message(
                "AdaptiveSystemController",
                f"Made {len(adjustments)} parameter adjustments"
            )
        
        return {
            "adjustments": adjustments,
            "current_parameters": self.current_parameters.copy(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_current_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        return self.current_parameters.copy()
    
    def rollback_adjustment(self, adjustment_id: int) -> bool:
        """回滚调整"""
        if 0 <= adjustment_id < len(self.adjustment_history):
            adj = list(self.adjustment_history)[adjustment_id]
            param = adj["parameter"]
            self.current_parameters[param] = adj["old_value"]
            self.logger and self.logger.log_information_message(
                "AdaptiveSystemController",
                f"Rolled back adjustment: {param}"
            )
            return True
        return False
    
    def get_adjustment_history(self) -> List[Dict[str, Any]]:
        """获取调整历史"""
        return list(self.adjustment_history)


class FaultRecoveryManager:
    """
    故障恢复管理器 - 检测和恢复系统故障
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.fault_history = deque(maxlen=100)
        self.checkpoint_data = {}
        self.recovery_strategies = {}
        self.active_faults = {}
    
    def register_recovery_strategy(self, fault_type: str, strategy: Callable):
        """注册恢复策略"""
        self.recovery_strategies[fault_type] = strategy
        self.logger and self.logger.log_information_message(
            "FaultRecoveryManager",
            f"Recovery strategy registered for: {fault_type}"
        )
    
    def detect_fault(
        self,
        fault_type: str,
        severity: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """检测故障"""
        fault_id = str(uuid.uuid4())
        
        fault = {
            "fault_id": fault_id,
            "fault_type": fault_type,
            "severity": severity,
            "details": details,
            "detected_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.active_faults[fault_id] = fault
        self.fault_history.append(fault)
        
        self.logger and self.logger.log_warning_message(
            "FaultRecoveryManager",
            f"Fault detected: {fault_type}",
            fault_id=fault_id,
            severity=severity
        )
        
        return fault
    
    def attempt_recovery(self, fault_id: str) -> Dict[str, Any]:
        """尝试恢复"""
        if fault_id not in self.active_faults:
            return {"success": False, "error": "Fault not found"}
        
        fault = self.active_faults[fault_id]
        fault_type = fault["fault_type"]
        
        strategy = self.recovery_strategies.get(fault_type)
        if not strategy:
            return {"success": False, "error": f"No recovery strategy for {fault_type}"}
        
        try:
            result = strategy(fault)
            fault["status"] = "resolved"
            fault["resolved_at"] = datetime.now().isoformat()
            
            self.logger and self.logger.log_information_message(
                "FaultRecoveryManager",
                f"Fault resolved: {fault_id}",
                fault_type=fault_type
            )
            
            return {
                "success": True,
                "fault_id": fault_id,
                "recovery_result": result
            }
            
        except Exception as e:
            fault["status"] = "failed"
            fault["error"] = str(e)
            
            self.logger and self.logger.log_error_message(
                "FaultRecoveryManager",
                f"Recovery failed: {fault_id}",
                error=str(e)
            )
            
            return {"success": False, "error": str(e)}
    
    def save_checkpoint(self, checkpoint_id: str, data: Dict[str, Any]) -> bool:
        """保存检查点"""
        self.checkpoint_data[checkpoint_id] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.logger and self.logger.log_debug_message(
            "FaultRecoveryManager",
            f"Checkpoint saved: {checkpoint_id}"
        )
        return True
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """加载检查点"""
        checkpoint = self.checkpoint_data.get(checkpoint_id)
        if checkpoint:
            self.logger and self.logger.log_information_message(
                "FaultRecoveryManager",
                f"Checkpoint loaded: {checkpoint_id}"
            )
        return checkpoint
    
    def get_fault_summary(self) -> Dict[str, Any]:
        """获取故障摘要"""
        total = len(self.fault_history)
        resolved = sum(1 for f in self.fault_history if f.get("status") == "resolved")
        failed = sum(1 for f in self.fault_history if f.get("status") == "failed")
        
        fault_types = defaultdict(int)
        for fault in self.fault_history:
            fault_types[fault["fault_type"]] += 1
        
        return {
            "total_faults": total,
            "resolved_faults": resolved,
            "failed_recoveries": failed,
            "active_faults": len(self.active_faults),
            "fault_type_distribution": dict(fault_types)
        }


class SystemHealthMonitor:
    """
    系统健康监控器 - 监控和管理系统健康状态
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.health_metrics = deque(maxlen=1000)
        self.alert_thresholds = {
            "cpu_percent": 90,
            "memory_percent": 85,
            "error_rate": 0.1,
            "latency_ms": 1000
        }
        self.alerts = deque(maxlen=100)
    
    def check_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """检查健康状态"""
        status = HealthStatus.HEALTHY
        issues = []
        
        cpu_percent = metrics.get("cpu_percent", 0)
        if cpu_percent > self.alert_thresholds["cpu_percent"]:
            status = HealthStatus.DEGRADED
            issues.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        memory_percent = metrics.get("memory_percent", 0)
        if memory_percent > self.alert_thresholds["memory_percent"]:
            status = HealthStatus.DEGRADED
            issues.append(f"High memory usage: {memory_percent:.1f}%")
        
        error_rate = metrics.get("error_rate", 0)
        if error_rate > self.alert_thresholds["error_rate"]:
            status = HealthStatus.UNHEALTHY
            issues.append(f"High error rate: {error_rate:.2%}")
        
        latency_ms = metrics.get("latency_ms", 0)
        if latency_ms > self.alert_thresholds["latency_ms"]:
            status = HealthStatus.UNHEALTHY
            issues.append(f"High latency: {latency_ms}ms")
        
        if len(issues) >= 3:
            status = HealthStatus.CRITICAL
        
        health_record = {
            "timestamp": datetime.now().isoformat(),
            "status": status.value,
            "metrics": metrics,
            "issues": issues
        }
        
        self.health_metrics.append(health_record)
        
        if issues:
            self.alerts.append({
                "timestamp": datetime.now().isoformat(),
                "status": status.value,
                "issues": issues
            })
        
        self.logger and self.logger.log_debug_message(
            "SystemHealthMonitor",
            f"Health check: {status.value}",
            issues_count=len(issues)
        )
        
        return {
            "status": status.value,
            "issues": issues,
            "timestamp": health_record["timestamp"]
        }
    
    def get_health_trend(self, duration_minutes: int = 30) -> Dict[str, Any]:
        """获取健康趋势"""
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        
        recent_metrics = [
            m for m in self.health_metrics
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]
        
        if not recent_metrics:
            return {"status": "no_data"}
        
        status_counts = defaultdict(int)
        for m in recent_metrics:
            status_counts[m["status"]] += 1
        
        return {
            "total_checks": len(recent_metrics),
            "status_distribution": dict(status_counts),
            "health_score": self._calculate_health_score(status_counts),
            "period_minutes": duration_minutes
        }
    
    def _calculate_health_score(self, status_counts: Dict[str, int]) -> float:
        """计算健康分数"""
        total = sum(status_counts.values())
        if total == 0:
            return 100.0
        
        weights = {
            "healthy": 100,
            "degraded": 70,
            "unhealthy": 40,
            "critical": 10
        }
        
        weighted_sum = sum(count * weights.get(status, 0) for status, count in status_counts.items())
        return weighted_sum / total
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近告警"""
        return list(self.alerts)[-limit:]


class CircuitBreaker:
    """
    断路器模式 - 防止故障级联
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"
    
    def call(self, func: Callable, *args, **kwargs):
        """执行函数"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """成功处理"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self):
        """失败处理"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
    
    def _should_attempt_reset(self) -> bool:
        """是否应该尝试重置"""
        if self.last_failure_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout_seconds
    
    def get_state(self) -> Dict[str, Any]:
        """获取断路器状态"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "threshold": self.failure_threshold,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }


__all__ = [
    "HealthStatus",
    "AdaptiveSystemController",
    "FaultRecoveryManager",
    "SystemHealthMonitor",
    "CircuitBreaker"
]
