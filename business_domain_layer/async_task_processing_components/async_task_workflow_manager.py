"""
Async Task Processing Framework - 异步任务处理框架
提供高性能的异步任务队列、执行和管理
"""

import asyncio
import time
import uuid
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from collections import deque

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class AsyncTaskQueue:
    """
    异步任务队列 - 用于管理待处理的异步任务
    """
    
    def __init__(self, max_size: int = 1000):
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._size: int = 0
    
    async def put(self, task_data: Dict[str, Any]) -> None:
        """放入任务到队列"""
        await self._queue.put(task_data)
        self._size += 1
    
    async def get(self) -> Dict[str, Any]:
        """从队列获取任务"""
        task_data = await self._queue.get()
        self._size -= 1
        return task_data
    
    def qsize(self) -> int:
        """队列大小"""
        return self._size
    
    def empty(self) -> bool:
        """是否为空"""
        return self._queue.empty()
    
    def full(self) -> bool:
        """是否已满"""
        return self._queue.full()


class AsyncTaskExecutor:
    """
    异步任务执行器 - 负责执行异步任务
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self._running = False
        self._worker_tasks = []
    
    async def start_workers(self, num_workers: int = 4) -> None:
        """启动工作线程"""
        self._running = True
        self._worker_tasks = []
        for i in range(num_workers):
            worker_task = asyncio.create_task(self._worker_loop())
            self._worker_tasks.append(worker_task)
        
        if self.logger:
            self.logger.log_information_message(
                "AsyncTaskExecutor",
                f"Started {num_workers} async workers"
            )
    
    async def stop_workers(self) -> None:
        """停止工作线程"""
        self._running = False
        for task in self._worker_tasks:
            task.cancel()
        
        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        
        if self.logger:
            self.logger.log_information_message(
                "AsyncTaskExecutor",
                "Async workers stopped"
            )
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个任务"""
        try:
            start_time = time.time()
            
            # 模拟任务执行
            await asyncio.sleep(0.01)  # 模拟 IO
            
            execution_result = {
                "task_id": task.get("task_id", str(uuid.uuid4())),
                "success": True,
                "duration": time.time() - start_time,
                "started_at": start_time,
                "completed_at": time.time()
            }
            
            if self.logger:
                self.logger.log_information_message(
                    "AsyncTaskExecutor",
                    f"Task executed successfully: {execution_result['task_id']}"
                )
            
            return execution_result
        
        except Exception as e:
            if self.logger:
                self.logger.log_error_message(
                    "AsyncTaskExecutor",
                    f"Task execution failed: {str(e)}"
                )
            
            return {
                "task_id": task.get("task_id", str(uuid.uuid4())),
                "success": False,
                "error": str(e),
                "duration": 0
            }
    
    async def _worker_loop(self):
        """工作线程循环"""
        while self._running:
            try:
                await asyncio.sleep(0.001)
            except Exception:
                if self.logger:
                    self.logger.log_information_message(
                        "AsyncTaskExecutor",
                        "Worker loop exiting"
                    )
                break


class AsyncTaskWorkflowManager:
    """
    异步任务工作流管理器 - 管理异步任务的完整生命周期
    """
    
    def __init__(
        self,
        storage: CoreStorageInterfaceContract,
        logger: Optional[CoreLoggerInterfaceContract] = None,
        max_workers: int = 4
    ):
        self.storage = storage
        self.logger = logger
        self.task_queue = AsyncTaskQueue()
        self.executor = AsyncTaskExecutor(logger=logger)
        self._max_workers = max_workers
        self._running = False
    
    async def initialize(self) -> None:
        """初始化异步管理器"""
        self._running = True
        await self.executor.start_workers(self._max_workers)
        
        if self.logger:
            self.logger.log_information_message(
                "AsyncTaskWorkflowManager",
                f"Initialized {self._max_workers} async workers"
            )
    
    async def create_and_execute_task(
        self,
        raw_input: str,
        priority: int = 1,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """创建并执行单个异步任务"""
        
        task_id = str(uuid.uuid4())
        task_data = {
            "task_id": task_id,
            "raw_input": raw_input,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        if self.logger:
            self.logger.log_information_message(
                "AsyncTaskWorkflowManager",
                f"Creating async task: {task_id}"
            )
        
        execution_result = await self.executor.execute_task(task_data)
        
        return {
            "task_id": task_id,
            "execution_result": execution_result,
            "experience": {
                "task_id": task_id,
                "success": execution_result["success"],
                "duration": execution_result.get("duration", 0)
            }
        }
    
    async def get_queue_statistics(self) -> Dict[str, Any]:
        """获取队列统计信息"""
        return {
            "queue_size": self.task_queue.qsize(),
            "is_full": self.task_queue.full(),
            "is_empty": self.task_queue.empty(),
            "max_workers": self._max_workers
        }
    
    async def shutdown(self) -> None:
        """关闭异步管理器"""
        self._running = False
        await self.executor.stop_workers()
        
        if self.logger:
            self.logger.log_information_message(
                "AsyncTaskWorkflowManager",
                "Async workflow manager shutdown"
            )


__all__ = [
    "AsyncTaskQueue",
    "AsyncTaskExecutor",
    "AsyncTaskWorkflowManager"
]
