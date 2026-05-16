"""
Adaptive System Module - 自适应系统模块
提供系统自适应、故障恢复、性能优化等功能
"""

from .adaptive_system_components import (
    HealthStatus,
    AdaptiveSystemController,
    FaultRecoveryManager,
    SystemHealthMonitor,
    CircuitBreaker
)

__version__ = "1.0.0"

__all__ = [
    "HealthStatus",
    "AdaptiveSystemController",
    "FaultRecoveryManager",
    "SystemHealthMonitor",
    "CircuitBreaker"
]
