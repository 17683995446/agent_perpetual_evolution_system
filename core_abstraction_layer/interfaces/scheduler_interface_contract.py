"""
Scheduler Interface Contract - 调度器接口契约
定义所有调度器实现必须遵循的标准接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class CoreSchedulerInterfaceContract(ABC):
    """
    Core Scheduler Interface Contract - 核心调度器接口契约
    
    定义所有调度器实现必须实现的标准方法
    支持多种调度策略：优先级、时间驱动、事件驱动
    """
    
    @abstractmethod
    def add_task_to_schedule_queue(self, task, priority: int = 1) -> str:
        """
        Add Task To Schedule Queue - 将任务添加到调度队列
        
        Args:
            task: 要调度的任务对象
            priority: 任务优先级（数字越大优先级越高）
            
        Returns:
            str: 任务调度标识符
        """
        pass
    
    @abstractmethod
    def retrieve_next_scheduled_task(self):
        """
        Retrieve Next Scheduled Task - 获取下一个待调度任务
        
        Returns:
            下一个任务对象或 None
        """
        pass
    
    @abstractmethod
    def update_schedule_task_priority(self, task_id: str, new_priority: int) -> bool:
        """
        Update Schedule Task Priority - 更新调度任务优先级
        
        Args:
            task_id: 任务标识符
            new_priority: 新的优先级值
            
        Returns:
            bool: 更新是否成功
        """
        pass
    
    @abstractmethod
    def get_current_schedule_queue_status(self) -> Dict[str, Any]:
        """
        Get Current Schedule Queue Status - 获取当前调度队列状态
        
        Returns:
            调度队列状态字典
        """
        pass
    
    @abstractmethod
    def pause_schedule_queue_processing(self) -> bool:
        """
        Pause Schedule Queue Processing - 暂停调度队列处理
        
        Returns:
            bool: 操作是否成功
        """
        pass
    
    @abstractmethod
    def resume_schedule_queue_processing(self) -> bool:
        """
        Resume Schedule Queue Processing - 恢复调度队列处理
        
        Returns:
            bool: 操作是否成功
        """
        pass


__all__ = ['CoreSchedulerInterfaceContract']
