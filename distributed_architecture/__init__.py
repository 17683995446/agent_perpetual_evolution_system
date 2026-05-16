"""
Distributed Architecture Module - 分布式架构模块
提供分布式任务队列、负载均衡、数据一致性等功能
"""

from .distributed_components import (
    LoadBalancingStrategy,
    DistributedTaskNode,
    DistributedTaskQueue,
    LoadBalancer,
    DataConsistencyManager,
    ServiceRegistry
)

__version__ = "1.0.0"

__all__ = [
    "LoadBalancingStrategy",
    "DistributedTaskNode",
    "DistributedTaskQueue",
    "LoadBalancer",
    "DataConsistencyManager",
    "ServiceRegistry"
]
