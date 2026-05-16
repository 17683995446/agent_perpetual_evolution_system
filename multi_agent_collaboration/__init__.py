"""
Multi-Agent Collaboration Framework - 多智能体协作框架
提供智能体定义、通信、协作和任务分配功能
"""

from .multi_agent_framework import (
    AgentStatus,
    MessageType,
    BaseAgent,
    AgentMessage,
    AgentCommunicationProtocol,
    TaskAllocationAlgorithm,
    CollaborativeExecutionEngine
)

__version__ = "1.0.0"

__all__ = [
    "AgentStatus",
    "MessageType",
    "BaseAgent",
    "AgentMessage",
    "AgentCommunicationProtocol",
    "TaskAllocationAlgorithm",
    "CollaborativeExecutionEngine"
]
