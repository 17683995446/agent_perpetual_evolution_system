"""
Machine Learning Integration Module - 机器学习集成模块
提供任务预测、策略学习、异常检测等智能功能
"""

from .machine_learning_components import (
    TaskExecutionDataCollector,
    TaskFeatureExtractor,
    TaskSuccessPredictor,
    ExecutionStrategyLearner,
    AnomalyDetector,
    AdaptiveParameterTuner
)

__version__ = "1.0.0"

__all__ = [
    "TaskExecutionDataCollector",
    "TaskFeatureExtractor",
    "TaskSuccessPredictor",
    "ExecutionStrategyLearner",
    "AnomalyDetector",
    "AdaptiveParameterTuner"
]
