"""
Machine Learning Integration Module - 机器学习集成模块
提供任务预测、策略学习、异常检测等智能功能
"""

import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import random

from ..core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class TaskExecutionDataCollector:
    """
    任务执行数据收集器 - 收集和管理任务执行数据
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.execution_data = []
        self.max_history_size = 10000
    
    def record_execution(
        self,
        task_id: str,
        task_input: str,
        priority: int,
        duration: float,
        success: bool,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """记录一次任务执行"""
        record = {
            "record_id": str(uuid.uuid4()),
            "task_id": task_id,
            "task_input": task_input,
            "priority": priority,
            "duration": duration,
            "success": success,
            "error_message": error_message,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.execution_data.append(record)
        
        if len(self.execution_data) > self.max_history_size:
            self.execution_data = self.execution_data[-self.max_history_size:]
        
        self.logger and self.logger.log_debug_message(
            "TaskExecutionDataCollector",
            f"Recorded execution: {task_id}, success={success}"
        )
    
    def get_training_data(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取训练数据"""
        data = self.execution_data[-limit:] if limit else self.execution_data
        return data
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取数据统计"""
        total = len(self.execution_data)
        if total == 0:
            return {"total": 0}
        
        success_count = sum(1 for d in self.execution_data if d["success"])
        durations = [d["duration"] for d in self.execution_data]
        
        return {
            "total_executions": total,
            "success_count": success_count,
            "failure_count": total - success_count,
            "success_rate": success_count / total,
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations)
        }


class TaskFeatureExtractor:
    """
    任务特征提取器 - 从任务中提取特征用于机器学习
    """
    
    @staticmethod
    def extract_features(task_input: str, priority: int, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """提取任务特征"""
        features = {
            "input_length": len(task_input),
            "word_count": len(task_input.split()),
            "priority": priority,
            "has_special_chars": any(c in task_input for c in ["!", "?", "*"]),
            "uppercase_ratio": sum(1 for c in task_input if c.isupper()) / len(task_input) if task_input else 0,
            "digit_count": sum(1 for c in task_input if c.isdigit()),
            "special_keyword_count": sum(1 for kw in ["analyze", "create", "update", "delete", "search"] if kw in task_input.lower())
        }
        
        if metadata:
            features.update(metadata)
        
        return features
    
    @staticmethod
    def extract_time_features() -> Dict[str, float]:
        """提取时间特征"""
        now = datetime.now()
        return {
            "hour": now.hour,
            "day_of_week": now.weekday(),
            "day_of_month": now.day,
            "is_weekend": now.weekday() >= 5,
            "is_business_hours": 9 <= now.hour <= 17
        }


class TaskSuccessPredictor:
    """
    任务成功率预测器 - 基于历史数据预测任务成功率
    """
    
    def __init__(self, data_collector: TaskExecutionDataCollector, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.data_collector = data_collector
        self.logger = logger
        self.model_weights = self._initialize_model()
    
    def _initialize_model(self) -> Dict[str, float]:
        """初始化简单的加权模型"""
        return {
            "priority_weight": 0.2,
            "duration_weight": 0.1,
            "input_length_weight": 0.15,
            "time_weight": 0.25,
            "history_weight": 0.3
        }
    
    def predict_success_probability(
        self,
        task_input: str,
        priority: int,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """预测任务成功概率"""
        features = TaskFeatureExtractor.extract_features(task_input, priority, metadata)
        time_features = TaskFeatureExtractor.extract_time_features()
        
        history_stats = self.data_collector.get_statistics()
        history_rate = history_stats.get("success_rate", 0.5)
        
        score = 0.5
        score += (priority / 10) * self.model_weights["priority_weight"]
        score += min(len(task_input) / 100, 1.0) * self.model_weights["input_length_weight"]
        score += time_features["is_business_hours"] * self.model_weights["time_weight"]
        score += history_rate * self.model_weights["history_weight"]
        
        probability = max(0.0, min(1.0, score))
        
        risk_level = "low" if probability > 0.8 else "medium" if probability > 0.5 else "high"
        
        return {
            "success_probability": probability,
            "risk_level": risk_level,
            "confidence": 0.7,
            "features": {**features, **time_features},
            "model_version": "v1.0"
        }
    
    def update_model(self, actual_success: bool):
        """基于实际结果更新模型"""
        pass
    
    def get_feature_importance(self) -> Dict[str, float]:
        """获取特征重要性"""
        return self.model_weights.copy()


class ExecutionStrategyLearner:
    """
    执行策略学习器 - 学习最优执行策略
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.strategies = {
            "sequential": {"name": "Sequential", "success_rate": 0.0, "usage_count": 0},
            "parallel": {"name": "Parallel", "success_rate": 0.0, "usage_count": 0},
            "batch": {"name": "Batch", "success_rate": 0.0, "usage_count": 0}
        }
        self.total_success = defaultdict(int)
        self.total_attempts = defaultdict(int)
    
    def select_best_strategy(self, task_metadata: Dict[str, Any]) -> str:
        """选择最佳策略"""
        if not task_metadata:
            return "sequential"
        
        priority = task_metadata.get("priority", 5)
        input_length = task_metadata.get("input_length", 50)
        
        if priority >= 8:
            best_strategy = "parallel"
        elif input_length > 100:
            best_strategy = "batch"
        else:
            best_strategy = "sequential"
        
        self.strategies[best_strategy]["usage_count"] += 1
        
        return best_strategy
    
    def record_strategy_result(self, strategy: str, success: bool):
        """记录策略执行结果"""
        self.total_attempts[strategy] += 1
        if success:
            self.total_success[strategy] += 1
        
        if self.total_attempts[strategy] > 0:
            self.strategies[strategy]["success_rate"] = self.total_success[strategy] / self.total_attempts[strategy]
    
    def get_strategy_recommendations(self) -> Dict[str, Any]:
        """获取策略推荐"""
        recommendations = []
        for strategy, stats in self.strategies.items():
            recommendations.append({
                "strategy": strategy,
                "name": stats["name"],
                "success_rate": stats["success_rate"],
                "usage_count": stats["usage_count"],
                "recommendation": "recommended" if stats["success_rate"] > 0.8 else "use_with_caution"
            })
        
        return {
            "strategies": recommendations,
            "best_strategy": max(self.strategies.items(), key=lambda x: x[1]["success_rate"])[0]
        }


class AnomalyDetector:
    """
    异常检测器 - 检测系统异常和性能问题
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.baseline_metrics = {
            "avg_duration": 0.1,
            "max_duration": 1.0,
            "error_rate": 0.05,
            "success_rate": 0.95
        }
        self.anomaly_history = []
        self.max_history = 100
    
    def detect_task_anomaly(self, duration: float, success: bool) -> Dict[str, Any]:
        """检测任务异常"""
        is_anomaly = False
        anomaly_type = None
        severity = "normal"
        
        if duration > self.baseline_metrics["max_duration"] * 3:
            is_anomaly = True
            anomaly_type = "high_duration"
            severity = "high"
        elif not success:
            is_anomaly = True
            anomaly_type = "task_failure"
            severity = "medium"
        elif duration > self.baseline_metrics["avg_duration"] * 2:
            is_anomaly = True
            anomaly_type = "slow_execution"
            severity = "low"
        
        result = {
            "is_anomaly": is_anomaly,
            "anomaly_type": anomaly_type,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        
        if is_anomaly:
            self.anomaly_history.append(result)
            if len(self.anomaly_history) > self.max_history:
                self.anomaly_history = self.anomaly_history[-self.max_history:]
            
            self.logger and self.logger.log_warning_message(
                "AnomalyDetector",
                f"Anomaly detected: {anomaly_type}",
                severity=severity
            )
        
        return result
    
    def detect_system_anomaly(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """检测系统级异常"""
        anomalies = []
        
        cpu_percent = metrics.get("cpu", {}).get("percent", 0)
        if cpu_percent > 90:
            anomalies.append({
                "type": "high_cpu_usage",
                "severity": "high",
                "value": cpu_percent,
                "threshold": 90
            })
        
        memory_percent = metrics.get("memory", {}).get("percent", 0)
        if memory_percent > 85:
            anomalies.append({
                "type": "high_memory_usage",
                "severity": "high",
                "value": memory_percent,
                "threshold": 85
            })
        
        return {
            "has_anomalies": len(anomalies) > 0,
            "anomalies": anomalies,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_anomaly_summary(self) -> Dict[str, Any]:
        """获取异常摘要"""
        if not self.anomaly_history:
            return {"total_anomalies": 0, "types": {}}
        
        type_counts = defaultdict(int)
        severity_counts = defaultdict(int)
        
        for anomaly in self.anomaly_history:
            type_counts[anomaly["anomaly_type"]] += 1
            severity_counts[anomaly["severity"]] += 1
        
        return {
            "total_anomalies": len(self.anomaly_history),
            "types": dict(type_counts),
            "severity_distribution": dict(severity_counts),
            "recent_anomalies": self.anomaly_history[-10:]
        }


class AdaptiveParameterTuner:
    """
    自适应参数调整器 - 自动调整系统参数
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.parameters = {
            "max_workers": 4,
            "timeout": 300,
            "retry_count": 3,
            "batch_size": 10,
            "queue_size": 100
        }
        self.parameter_history = []
    
    def get_current_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        return self.parameters.copy()
    
    def suggest_parameter_adjustment(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """建议参数调整"""
        suggestions = []
        
        throughput = performance_metrics.get("throughput", 0)
        error_rate = performance_metrics.get("error_rate", 0)
        latency = performance_metrics.get("avg_latency", 0.1)
        
        if error_rate > 0.1:
            suggestions.append({
                "parameter": "retry_count",
                "current_value": self.parameters["retry_count"],
                "suggested_value": min(self.parameters["retry_count"] + 1, 5),
                "reason": "High error rate detected"
            })
        
        if latency > 1.0:
            suggestions.append({
                "parameter": "timeout",
                "current_value": self.parameters["timeout"],
                "suggested_value": max(self.parameters["timeout"] - 30, 60),
                "reason": "High latency detected"
            })
        
        if throughput < 10:
            suggestions.append({
                "parameter": "max_workers",
                "current_value": self.parameters["max_workers"],
                "suggested_value": min(self.parameters["max_workers"] + 1, 16),
                "reason": "Low throughput, increase workers"
            })
        
        return {
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
    
    def apply_parameter_adjustment(self, parameter: str, value: Any) -> bool:
        """应用参数调整"""
        if parameter in self.parameters:
            old_value = self.parameters[parameter]
            self.parameters[parameter] = value
            
            self.parameter_history.append({
                "parameter": parameter,
                "old_value": old_value,
                "new_value": value,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger and self.logger.log_information_message(
                "AdaptiveParameterTuner",
                f"Parameter adjusted: {parameter} = {old_value} -> {value}"
            )
            
            return True
        
        return False
    
    def get_adjustment_history(self) -> List[Dict[str, Any]]:
        """获取调整历史"""
        return self.parameter_history.copy()


__all__ = [
    "TaskExecutionDataCollector",
    "TaskFeatureExtractor",
    "TaskSuccessPredictor",
    "ExecutionStrategyLearner",
    "AnomalyDetector",
    "AdaptiveParameterTuner"
]
