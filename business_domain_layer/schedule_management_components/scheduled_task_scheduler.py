"""
Scheduled Task Scheduler - 定时任务调度器
基于 APScheduler 的定时任务调度和管理系统
"""

import time
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from collections import deque

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class ScheduledTask:
    """
    定时任务对象 - 存储定时任务的所有信息
    """
    
    def __init__(
        self,
        task_id: str,
        cron_expression: str,
        task_function: Callable,
        task_args: tuple = (),
        task_kwargs: dict = None,
        task_name: str = None
    ):
        self.task_id = task_id
        self.cron_expression = cron_expression
        self.task_function = task_function
        self.task_args = task_args
        self.task_kwargs = task_kwargs or {}
        self.task_name = task_name or f"scheduled-task-{task_id}"
        self.created_at = datetime.now().isoformat()
        self.last_run_at = None
        self.next_run_at = None
        self.is_active = True
        self.run_count = 0


class SimpleScheduledTaskScheduler:
    """
    简单定时任务调度器 - 轻量级的定时任务管理
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self._task_history = deque(maxlen=1000)
        self._is_running = False
        self._scheduler_thread = None
    
    def add_scheduled_task(
        self,
        cron_expression: str,
        task_function: Callable,
        task_args: tuple = (),
        task_kwargs: dict = None,
        task_name: str = None
    ) -> str:
        """
        添加定时任务
        """
        task_id = str(uuid.uuid4())
        task = ScheduledTask(
            task_id=task_id,
            cron_expression=cron_expression,
            task_function=task_function,
            task_args=task_args,
            task_kwargs=task_kwargs,
            task_name=task_name
        )
        
        self.scheduled_tasks[task_id] = task
        
        if self.logger:
            self.logger.log_information_message(
                "ScheduledTaskScheduler",
                f"Added scheduled task: {task_id}, cron: {cron_expression}"
            )
        
        return task_id
    
    def remove_scheduled_task(self, task_id: str) -> bool:
        """
        移除定时任务
        """
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
            
            if self.logger:
                self.logger.log_information_message(
                    "ScheduledTaskScheduler",
                    f"Removed scheduled task: {task_id}"
                )
            
            return True
        
        return False
    
    def get_scheduled_task(self, task_id: str) -> Optional[ScheduledTask]:
        """
        获取定时任务信息
        """
        return self.scheduled_tasks.get(task_id)
    
    def list_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """
        列出所有定时任务
        """
        return [
            {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "cron_expression": task.cron_expression,
                "created_at": task.created_at,
                "last_run_at": task.last_run_at,
                "is_active": task.is_active,
                "run_count": task.run_count
            }
            for task in self.scheduled_tasks.values()
        ]
    
    def trigger_task_now(self, task_id: str) -> Dict[str, Any]:
        """
        立即触发任务执行
        """
        task = self.scheduled_tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        start_time = time.time()
        
        try:
            result = task.task_function(*task.task_args, **task.task_kwargs)
            
            task.run_count += 1
            task.last_run_at = datetime.now().isoformat()
            
            history_entry = {
                "task_id": task_id,
                "timestamp": datetime.now().isoformat(),
                "duration": time.time() - start_time,
                "success": True
            }
            self._task_history.append(history_entry)
            
            if self.logger:
                self.logger.log_information_message(
                    "ScheduledTaskScheduler",
                    f"Task executed successfully: {task_id}"
                )
            
            return {
                "success": True,
                "result": result,
                "duration": time.time() - start_time
            }
            
        except Exception as e:
            history_entry = {
                "task_id": task_id,
                "timestamp": datetime.now().isoformat(),
                "duration": time.time() - start_time,
                "success": False,
                "error": str(e)
            }
            self._task_history.append(history_entry)
            
            if self.logger:
                self.logger.log_error_message(
                    "ScheduledTaskScheduler",
                    f"Task execution failed: {task_id}, error: {str(e)}"
                )
            
            return {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time
            }
    
    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取执行历史
        """
        history_list = list(self._task_history)
        return history_list[-limit:] if limit > 0 else history_list
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """
        获取调度器状态
        """
        return {
            "active_tasks": len([t for t in self.scheduled_tasks.values() if t.is_active]),
            "total_tasks": len(self.scheduled_tasks),
            "execution_history_count": len(self._task_history),
            "is_running": self._is_running
        }
    
    def start_scheduler(self) -> None:
        """
        启动调度器（简单实现，基于轮询）
        """
        self._is_running = True
        
        if self.logger:
            self.logger.log_information_message(
                "ScheduledTaskScheduler",
                "Scheduler started"
            )
    
    def stop_scheduler(self) -> None:
        """
        停止调度器
        """
        self._is_running = False
        
        if self.logger:
            self.logger.log_information_message(
                "ScheduledTaskScheduler",
                "Scheduler stopped"
            )


__all__ = [
    "ScheduledTask",
    "SimpleScheduledTaskScheduler"
]
