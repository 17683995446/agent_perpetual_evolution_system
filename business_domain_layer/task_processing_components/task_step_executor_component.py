"""
Task Step Executor Component - 任务步骤执行器组件
负责按照执行计划执行任务及其子任务
"""

from typing import Dict, Any, List
from datetime import datetime
import time

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class TaskStepExecutorComponent:
    """
    Task Step Executor Component - 任务步骤执行器组件
    
    负责任务执行计划的实际执行
    按计划顺序执行各子任务，收集执行结果
    """
    
    def __init__(self, storage_backend: CoreStorageInterfaceContract, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Task Step Executor Component - 初始化任务步骤执行器组件
        
        Args:
            storage_backend: 存储后端实例
            logger_backend: 日志后端实例
        """
        self.storage_backend = storage_backend
        self.logger_backend = logger_backend
    
    def execute_task_execution_plan(self, task_object, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Task Execution Plan - 执行任务执行计划
        
        Args:
            task_object: 要执行的任务对象
            execution_plan: 执行计划字典
            
        Returns:
            执行结果字典
        """
        start_time = time.time()
        
        self.logger_backend.log_information_message(
            'TaskStepExecutorComponent',
            f'Starting task execution plan: {task_object.task_id}',
            task_id=task_object.task_id
        )
        
        # 更新任务状态为运行中
        self.storage_backend.update_task_status_value(
            task_object.task_id,
            'RUNNING',
            started_at=datetime.now()
        )
        
        execution_result = {
            'success': True,
            'subtask_execution_results': [],
            'total_steps_executed': 0
        }
        
        try:
            # 按执行路径顺序执行每个步骤
            for step_id in execution_plan.get('execution_order_path', []):
                subtask = self._find_subtask_by_id_in_list(
                    execution_plan.get('generated_subtasks', []), 
                    step_id
                )
                
                if subtask:
                    step_execution_result = self._execute_single_subtask_step(subtask)
                    execution_result['subtask_execution_results'].append(step_execution_result)
                    execution_result['total_steps_executed'] += 1
                    
                    if not step_execution_result.get('success', False):
                        execution_result['success'] = False
                        execution_result['error_message'] = step_execution_result.get('error')
                        break
            
            # 更新任务最终状态
            final_status = 'COMPLETED' if execution_result['success'] else 'FAILED'
            self.storage_backend.update_task_status_value(
                task_object.task_id,
                final_status,
                completed_at=datetime.now()
            )
            
        except Exception as e:
            execution_result['success'] = False
            execution_result['error_message'] = str(e)
            
            self.storage_backend.update_task_status_value(
                task_object.task_id,
                'FAILED',
                completed_at=datetime.now()
            )
            
            self.logger_backend.log_error_message(
                'TaskStepExecutorComponent',
                f'Task execution plan failed: {task_object.task_id}',
                task_id=task_object.task_id,
                error=str(e)
            )
        
        execution_result['total_duration_seconds'] = time.time() - start_time
        
        self.logger_backend.log_information_message(
            'TaskStepExecutorComponent',
            f'Task execution plan completed: {task_object.task_id}',
            task_id=task_object.task_id,
            success=execution_result['success'],
            duration=execution_result['total_duration_seconds']
        )
        
        return execution_result
    
    def _execute_single_subtask_step(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Single Subtask Step - 执行单个子任务步骤
        
        Args:
            subtask: 子任务字典
            
        Returns:
            子任务执行结果
        """
        step_start_time = time.time()
        
        try:
            # 模拟子任务执行
            # 在实际实现中，这里会根据子任务描述执行相应操作
            
            execution_result = {
                'subtask_id': subtask['subtask_id'],
                'description': subtask['description'],
                'success': True,
                'output_message': f'Successfully executed: {subtask["description"]}',
                'duration_seconds': time.time() - step_start_time
            }
            
            self.logger_backend.log_debug_message(
                'TaskStepExecutorComponent',
                f'Subtask step completed: {subtask["subtask_id"]}',
                subtask_id=subtask['subtask_id']
            )
            
            return execution_result
            
        except Exception as e:
            return {
                'subtask_id': subtask['subtask_id'],
                'description': subtask['description'],
                'success': False,
                'error': str(e),
                'duration_seconds': time.time() - step_start_time
            }
    
    def _find_subtask_by_id_in_list(
        self, 
        subtask_list: List[Dict[str, Any]], 
        subtask_id: str
    ) -> Dict[str, Any]:
        """
        Find Subtask By ID In List - 在列表中根据ID查找子任务
        
        Args:
            subtask_list: 子任务列表
            subtask_id: 子任务ID
            
        Returns:
            找到的子任务字典，或None
        """
        for subtask in subtask_list:
            if subtask['subtask_id'] == subtask_id:
                return subtask
        return None


__all__ = ['TaskStepExecutorComponent']
