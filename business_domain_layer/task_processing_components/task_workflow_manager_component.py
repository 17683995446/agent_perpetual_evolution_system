"""
Task Workflow Manager Component - 任务工作流管理器组件
负责任务的创建、查询、更新和完整生命周期管理
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class TaskWorkflowManagerComponent:
    """
    Task Workflow Manager Component - 任务工作流管理器组件
    
    负责任务的完整生命周期管理
    包括任务创建、状态流转、查询统计等
    """
    
    def __init__(self, storage_backend: CoreStorageInterfaceContract, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Task Workflow Manager Component - 初始化任务工作流管理器组件
        
        Args:
            storage_backend: 存储后端实例
            logger_backend: 日志后端实例
        """
        self.storage_backend = storage_backend
        self.logger_backend = logger_backend
    
    def create_new_task_workflow(
        self,
        raw_input_text: str,
        priority_level: int = 1,
        timeout_duration: Optional[int] = None
    ) -> object:
        """
        Create New Task Workflow - 创建新任务工作流
        
        Args:
            raw_input_text: 任务原始输入文本
            priority_level: 任务优先级级别
            timeout_duration: 可选的过期时间
            
        Returns:
            创建的任务对象
        """
        task_id = str(uuid.uuid4())
        
        # 创建任务对象
        task = type('Task', (object,), {
            'task_id': task_id,
            'raw_input': raw_input_text,
            'priority': priority_level,
            'status': 'PENDING',
            'created_at': datetime.now(),
            'started_at': None,
            'completed_at': None,
            'timeout_seconds': timeout_duration,
        })()
        
        # 保存到存储
        self.storage_backend.save_single_task_record(task)
        
        # 记录日志
        self.logger_backend.log_information_message(
            'TaskWorkflowManagerComponent',
            f'New task workflow created: {task_id}',
            task_id=task_id,
            priority_level=priority_level
        )
        
        return task
    
    def retrieve_task_by_identifier(self, task_id: str) -> Optional[object]:
        """
        Retrieve Task By Identifier - 根据标识符获取任务
        
        Args:
            task_id: 任务唯一标识符
            
        Returns:
            找到的任务对象，或None
        """
        task = self.storage_backend.retrieve_task_by_identifier(task_id)
        
        if not task:
            self.logger_backend.log_warning_message(
                'TaskWorkflowManagerComponent',
                f'Task not found by identifier: {task_id}',
                task_id=task_id
            )
        
        return task
    
    def list_all_pending_task_workflows(self, limit_count: int = 100) -> List[object]:
        """
        List All Pending Task Workflows - 列出所有待处理任务
        
        Args:
            limit_count: 返回的最大数量
            
        Returns:
            待处理任务列表
        """
        return self.storage_backend.get_list_of_pending_tasks(limit_count=limit_count)
    
    def update_task_workflow_status(
        self,
        task_id: str,
        new_status: str,
        **additional_kwargs
    ) -> bool:
        """
        Update Task Workflow Status - 更新任务工作流状态
        
        Args:
            task_id: 任务ID
            new_status: 新状态
            **additional_kwargs: 其他要更新的属性
            
        Returns:
            bool: 更新是否成功
        """
        success = self.storage_backend.update_task_status_value(
            task_id, 
            new_status, 
            **additional_kwargs
        )
        
        if success:
            self.logger_backend.log_information_message(
                'TaskWorkflowManagerComponent',
                f'Task workflow status updated: {task_id} -> {new_status}',
                task_id=task_id,
                new_status=new_status
            )
        else:
            self.logger_backend.log_error_message(
                'TaskWorkflowManagerComponent',
                f'Failed to update task workflow status: {task_id}',
                task_id=task_id
            )
        
        return success
    
    def get_task_workflow_statistics(self) -> Dict[str, Any]:
        """
        Get Task Workflow Statistics - 获取任务工作流统计
        
        Returns:
            任务统计字典
        """
        pending_tasks = self.storage_backend.get_list_of_pending_tasks(limit_count=1000)
        
        statistics = {
            'pending_task_count': len(pending_tasks),
            'priority_distribution': {}
        }
        
        for task in pending_tasks:
            priority_key = str(getattr(task, 'priority', 1))
            if priority_key not in statistics['priority_distribution']:
                statistics['priority_distribution'][priority_key] = 0
            statistics['priority_distribution'][priority_key] += 1
        
        return statistics


__all__ = ['TaskWorkflowManagerComponent']
