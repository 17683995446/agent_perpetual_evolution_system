"""
Priority Queue Manager Component - 优先级队列管理器组件
负责管理任务的优先级队列和调度
"""

from typing import List, Dict, Any, Optional
from heapq import heappush, heappop
from datetime import datetime
import uuid

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class PriorityQueueManagerComponent:
    """
    Priority Queue Manager Component - 优先级队列管理器组件
    
    负责管理任务的优先级队列
    提供任务入队、出队、优先级调整等功能
    """
    
    def __init__(self, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Priority Queue Manager Component - 初始化优先级队列管理器组件
        
        Args:
            logger_backend: 日志后端实例
        """
        self.logger_backend = logger_backend
        self.priority_queue = []
        self.queue_counter = 0
        self.task_map = {}
    
    def enqueue_task(self, task_object, priority_level: int = 1) -> str:
        """
        Enqueue Task - 将任务加入队列
        
        Args:
            task_object: 任务对象
            priority_level: 优先级级别，数字越小优先级越高
            
        Returns:
            队列项ID
        """
        queue_item_id = str(uuid.uuid4())
        self.queue_counter += 1
        
        # 使用 (priority, counter, queue_item_id, task_object) 来确保稳定性
        heappush(
            self.priority_queue,
            (priority_level, self.queue_counter, queue_item_id, task_object)
        )
        
        self.task_map[queue_item_id] = {
            'task': task_object,
            'priority': priority_level,
            'enqueued_at': datetime.now(),
            'status': 'QUEUED'
        }
        
        self.logger_backend.log_information_message(
            'PriorityQueueManagerComponent',
            f'Task enqueued with priority {priority_level}: {task_object.task_id}',
            task_id=task_object.task_id,
            queue_item_id=queue_item_id,
            priority=priority_level
        )
        
        return queue_item_id
    
    def dequeue_task(self) -> Optional[object]:
        """
        Dequeue Task - 从队列中取出最高优先级的任务
        
        Returns:
            任务对象，如果队列为空则返回None
        """
        if not self.priority_queue:
            self.logger_backend.log_debug_message(
                'PriorityQueueManagerComponent',
                'Priority queue is empty'
            )
            return None
        
        priority, counter, queue_item_id, task_object = heappop(self.priority_queue)
        
        if queue_item_id in self.task_map:
            self.task_map[queue_item_id]['status'] = 'DEQUEUED'
            self.task_map[queue_item_id]['dequeued_at'] = datetime.now()
        
        self.logger_backend.log_information_message(
            'PriorityQueueManagerComponent',
            f'Task dequeued: {task_object.task_id}',
            task_id=task_object.task_id,
            priority=priority
        )
        
        return task_object
    
    def update_task_priority(self, queue_item_id: str, new_priority: int) -> bool:
        """
        Update Task Priority - 更新任务优先级
        
        Args:
            queue_item_id: 队列项ID
            new_priority: 新的优先级
            
        Returns:
            bool: 更新是否成功
        """
        if queue_item_id not in self.task_map:
            self.logger_backend.log_warning_message(
                'PriorityQueueManagerComponent',
                f'Queue item not found: {queue_item_id}'
            )
            return False
        
        old_priority = self.task_map[queue_item_id]['priority']
        self.task_map[queue_item_id]['priority'] = new_priority
        
        # 重新构建队列
        self._rebuild_priority_queue()
        
        self.logger_backend.log_information_message(
            'PriorityQueueManagerComponent',
            f'Task priority updated from {old_priority} to {new_priority}',
            queue_item_id=queue_item_id,
            old_priority=old_priority,
            new_priority=new_priority
        )
        
        return True
    
    def get_queue_statistics(self) -> Dict[str, Any]:
        """
        Get Queue Statistics - 获取队列统计信息
        
        Returns:
            队列统计字典
        """
        queued_count = sum(
            1 for item in self.task_map.values() 
            if item['status'] == 'QUEUED'
        )
        
        priority_distribution = {}
        for item in self.task_map.values():
            if item['status'] == 'QUEUED':
                prio = str(item['priority'])
                if prio not in priority_distribution:
                    priority_distribution[prio] = 0
                priority_distribution[prio] += 1
        
        return {
            'total_queued': queued_count,
            'priority_distribution': priority_distribution,
            'queue_size': len(self.priority_queue)
        }
    
    def _rebuild_priority_queue(self):
        """
        Rebuild Priority Queue - 重建优先级队列
        """
        self.priority_queue = []
        self.queue_counter = 0
        
        for queue_item_id, item_info in self.task_map.items():
            if item_info['status'] == 'QUEUED':
                self.queue_counter += 1
                heappush(
                    self.priority_queue,
                    (
                        item_info['priority'],
                        self.queue_counter,
                        queue_item_id,
                        item_info['task']
                    )
                )
    
    def stop_queue_processing(self):
        """
        Stop Queue Processing - 停止队列处理
        """
        self.logger_backend.log_information_message(
            'PriorityQueueManagerComponent',
            'Priority queue processing stopped'
        )


__all__ = ['PriorityQueueManagerComponent']
