"""
Infrastructure Adapter Layer - Memory Based Storage Adapter
基础设施适配层 - 基于内存的存储适配器

完全基于内存的存储实现
适用于测试、开发和轻量级部署场景
线程安全，支持并发访问
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import threading

from ...core_abstraction_layer.interfaces.storage_interface_contract import (
    CoreStorageInterfaceContract,
)


class MemoryBasedStorageAdapter(CoreStorageInterfaceContract):
    """
    Memory Based Storage Adapter - 基于内存的存储适配器
    
    完全基于内存的存储实现
    适用于测试、开发和轻量级部署场景
    线程安全，支持并发访问
    """
    
    def __init__(self):
        """
        Initialize Memory Based Storage Adapter - 初始化基于内存的存储适配器
        """
        self._task_storage_dictionary: Dict[str, object] = {}
        self._thread_safe_lock_object = threading.RLock()
    
    def save_single_task_record(self, task) -> bool:
        """
        Save Single Task Record - 保存单个任务记录
        """
        with self._thread_safe_lock_object:
            if hasattr(task, 'task_id'):
                self._task_storage_dictionary[task.task_id] = task
            return True
    
    def retrieve_task_by_identifier(self, task_id: str):
        """
        Retrieve Task By Identifier - 根据标识符获取任务
        """
        with self._thread_safe_lock_object:
            return self._task_storage_dictionary.get(task_id)
    
    def update_task_status_value(self, task_id: str, new_status, **kwargs) -> bool:
        """
        Update Task Status Value - 更新任务状态值
        """
        with self._thread_safe_lock_object:
            task = self._task_storage_dictionary.get(task_id)
            if task:
                task.status = new_status
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return True
            return False
    
    def get_list_of_pending_tasks(self, limit_count: int = 100) -> List:
        """
        Get List Of Pending Tasks - 获取待处理任务列表
        """
        with self._thread_safe_lock_object:
            return list(self._task_storage_dictionary.values())[:limit_count]
    
    def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform Health Check - 执行健康检查
        """
        with self._thread_safe_lock_object:
            return {
                "status": "healthy",
                "storage_type": "in_memory",
                "task_count": len(self._task_storage_dictionary)
            }


__all__ = ['MemoryBasedStorageAdapter']
