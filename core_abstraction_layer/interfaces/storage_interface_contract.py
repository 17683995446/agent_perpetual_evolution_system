"""
Core Abstraction Layer - Storage Interface Contract
核心抽象层 - 存储接口契约

定义所有存储后端必须遵循的标准接口
支持多种存储实现（内存、关系型数据库、NoSQL等）
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime


class CoreStorageInterfaceContract(ABC):
    """
    Core Storage Interface Contract - 核心存储接口契约
    
    定义所有存储后端必须实现的标准方法
    支持多种存储类型：内存、SQLite、Redis等
    """
    
    @abstractmethod
    def save_single_task_record(self, task) -> bool:
        """
        Save Single Task Record - 保存单个任务记录
        
        Args:
            task: 要保存的任务对象
        
        Returns:
            bool: 保存是否成功
        """
        pass
    
    @abstractmethod
    def retrieve_task_by_identifier(self, task_id: str):
        """
        Retrieve Task By Identifier - 根据标识符获取任务
        
        Args:
            task_id: 任务唯一标识符
            
        Returns:
            找到的任务对象，或None
        """
        pass
    
    @abstractmethod
    def update_task_status_value(self, task_id: str, new_status, **kwargs) -> bool:
        """
        Update Task Status Value - 更新任务状态值
        
        Args:
            task_id: 任务ID
            new_status: 新的状态值
            **kwargs: 其他要更新的属性
            
        Returns:
            bool: 更新是否成功
        """
        pass
    
    @abstractmethod
    def get_list_of_pending_tasks(self, limit_count: int = 100) -> List:
        """
        Get List Of Pending Tasks - 获取待处理任务列表
        
        Args:
            limit_count: 返回的最大数量
            
        Returns:
            待处理任务列表
        """
        pass
    
    @abstractmethod
    def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform Health Check - 执行健康检查
        
        Returns:
            健康状态字典
        """
        pass


__all__ = [
    'CoreStorageInterfaceContract',
]
