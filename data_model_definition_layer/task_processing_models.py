"""
Data Model Definition Layer - Task Processing Models
数据模型定义层 - 任务处理模型

定义任务的完整数据结构和类型
包括任务状态、优先级、时间戳等完整信息
"""

from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatusTypeEnum(str, Enum):
    """
    Task Status Type Enum - 任务状态类型枚举
    """
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    
    # 保持向后兼容性
    PENDING_STATUS = "PENDING"
    RUNNING_STATUS = "RUNNING"
    COMPLETED_STATUS = "COMPLETED"
    FAILED_STATUS = "FAILED"
    TIMEOUT_STATUS = "TIMEOUT"


class TaskPriorityLevelEnum(str, Enum):
    """
    Task Priority Level Enum - 任务优先级级别枚举
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"
    
    # 保持向后兼容性
    LOW_PRIORITY = "LOW"
    MEDIUM_PRIORITY = "MEDIUM"
    HIGH_PRIORITY = "HIGH"
    URGENT_PRIORITY = "URGENT"


class TaskProcessingDataModel:
    """
    Task Processing Data Model - 任务处理数据模型
    
    定义任务的完整数据结构
    包括基本信息、状态、优先级、时间戳等
    """
    
    def __init__(
        self,
        task_id: str,
        raw_input_text: str,
        priority_level: TaskPriorityLevelEnum = TaskPriorityLevelEnum.MEDIUM,
        status: TaskStatusTypeEnum = TaskStatusTypeEnum.PENDING,
        created_at: Optional[datetime] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        timeout_duration_seconds: Optional[int] = None
    ):
        """
        Initialize Task Processing Data Model - 初始化任务处理数据模型
        
        Args:
            task_id: 任务唯一标识符
            raw_input_text: 任务原始输入文本
            priority_level: 任务优先级级别
            status: 任务状态
            created_at: 创建时间戳
            started_at: 开始执行时间戳
            completed_at: 完成时间戳
            timeout_duration_seconds: 超时时长（秒）
        """
        self.task_id = task_id
        self.raw_input = raw_input_text
        self.priority = priority_level
        self.status = status
        self.created_at = created_at or datetime.now()
        self.started_at = started_at
        self.completed_at = completed_at
        self.timeout_seconds = timeout_duration_seconds
    
    def to_dictionary(self) -> dict:
        """
        To Dictionary - 转换为字典
        
        Returns:
            任务数据字典
        """
        return {
            'task_id': self.task_id,
            'raw_input': self.raw_input,
            'priority': self.priority.value if hasattr(self.priority, 'value') else self.priority,
            'status': self.status.value if hasattr(self.status, 'value') else self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'timeout_seconds': self.timeout_seconds
        }
    
    @classmethod
    def from_dictionary(cls, data_dict: dict) -> 'TaskProcessingDataModel':
        """
        From Dictionary - 从字典创建
        
        Args:
            data_dict: 任务数据字典
            
        Returns:
            TaskProcessingDataModel实例
        """
        return cls(
            task_id=data_dict['task_id'],
            raw_input_text=data_dict['raw_input'],
            priority_level=TaskPriorityLevelEnum(data_dict.get('priority', 'MEDIUM')),
            status=TaskStatusTypeEnum(data_dict.get('status', 'PENDING')),
            created_at=datetime.fromisoformat(data_dict['created_at']) if data_dict.get('created_at') else None,
            started_at=datetime.fromisoformat(data_dict['started_at']) if data_dict.get('started_at') else None,
            completed_at=datetime.fromisoformat(data_dict['completed_at']) if data_dict.get('completed_at') else None,
            timeout_duration_seconds=data_dict.get('timeout_seconds')
        )


__all__ = ['TaskProcessingDataModel', 'TaskStatusTypeEnum', 'TaskPriorityLevelEnum']
