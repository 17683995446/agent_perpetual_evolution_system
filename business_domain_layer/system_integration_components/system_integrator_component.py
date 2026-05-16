"""
System Integrator Component - 系统集成器组件
负责协调和集成所有业务领域组件
"""

from typing import Dict, Any, Optional
from datetime import datetime

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract

from ..task_processing_components.task_analyzer_planner_component import TaskAnalyzerPlannerComponent
from ..task_processing_components.task_step_executor_component import TaskStepExecutorComponent
from ..task_processing_components.task_workflow_manager_component import TaskWorkflowManagerComponent
from ..schedule_management_components.workflow_mode_coordinator_component import WorkflowModeCoordinatorComponent
from ..schedule_management_components.priority_queue_manager_component import PriorityQueueManagerComponent
from ..schedule_management_components.execution_checkpoint_saver_component import ExecutionCheckpointSaverComponent
from ..learning_module_components.experience_learning_manager_component import ExperienceLearningManagerComponent
from ..feedback_generation_components.feedback_generation_reporter_component import FeedbackGenerationReporterComponent


class SystemIntegratorComponent:
    """
    System Integrator Component - 系统集成器组件
    
    负责协调和集成所有业务领域组件
    提供统一的任务处理入口和系统协调功能
    """
    
    def __init__(self, custom_storage=None, custom_logger=None):
        """
        Initialize System Integrator Component - 初始化系统集成器组件
        
        Args:
            custom_storage: 自定义存储后端（可选）
            custom_logger: 自定义日志后端（可选）
        """
        from ...configuration_management_layer import get_application_global_settings
        from ...infrastructure_adapter_layer import (
            StorageBackendFactoryBuilder,
            StructuredLoggerFrameworkImplementation
        )
        
        self.settings = get_application_global_settings()
        
        # 初始化基础设施层组件
        self.storage_backend = custom_storage or StorageBackendFactoryBuilder.create_storage_backend_instance()
        self.logger_backend = custom_logger or StructuredLoggerFrameworkImplementation()
        
        # 初始化所有组件
        # 首先初始化不依赖其他组件的组件
        self.priority_queue_manager = PriorityQueueManagerComponent(self.logger_backend)
        self.execution_checkpoint_saver = ExecutionCheckpointSaverComponent(self.storage_backend, self.logger_backend)
        self.task_analyzer_planner = TaskAnalyzerPlannerComponent(self.logger_backend)
        self.feedback_generation_reporter = FeedbackGenerationReporterComponent(self.logger_backend)
        
        # 然后初始化依赖其他组件的组件
        self.workflow_mode_coordinator = WorkflowModeCoordinatorComponent(
            self.logger_backend
        )
        self.task_step_executor = TaskStepExecutorComponent(self.storage_backend, self.logger_backend)
        self.task_workflow_manager = TaskWorkflowManagerComponent(self.storage_backend, self.logger_backend)
        self.experience_learning_manager = ExperienceLearningManagerComponent(self.storage_backend, self.logger_backend)
        
        self.is_initialized = True
        
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            'System integrator initialized with all components'
        )
    
    def process_task(self, raw_input: str, priority: int = 1) -> Dict[str, Any]:
        """
        Process Task - 处理任务的完整流程
        
        Args:
            raw_input: 原始任务输入
            priority: 任务优先级
            
        Returns:
            处理结果字典
        """
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            'Starting task processing',
            raw_input=raw_input[:50] + '...' if len(raw_input) > 50 else raw_input
        )
        
        # 1. 创建任务工作流
        task = self.task_workflow_manager.create_new_task_workflow(raw_input, priority)
        task_id = task.task_id
        
        # 2. 分析任务并生成执行计划
        execution_plan = self.task_analyzer_planner.analyze_and_generate_execution_plan(task)
        
        # 3. 确定最佳执行模式
        task_metadata = {
            'subtask_count': len(execution_plan.get('generated_subtasks', [])),
            'has_dependencies': True
        }
        optimal_mode = self.workflow_mode_coordinator.determine_optimal_execution_mode(task_metadata)
        self.workflow_mode_coordinator.switch_execution_mode(optimal_mode)
        
        # 4. 将任务加入优先级队列
        queue_item_id = self.priority_queue_manager.enqueue_task(task, priority)
        
        # 5. 执行任务
        execution_result = self.task_step_executor.execute_task_execution_plan(task, execution_plan)
        
        # 6. 保存检查点（如果成功）
        if execution_result.get('success', False):
            self.execution_checkpoint_saver.save_execution_checkpoint(
                task_id,
                execution_result,
                len(execution_plan.get('generated_subtasks', []))
            )
        
        # 7. 记录执行经验
        self.experience_learning_manager.record_execution_experience(
            task_id,
            execution_result,
            execution_plan
        )
        
        # 8. 生成反馈
        feedback = self.feedback_generation_reporter.generate_execution_feedback(
            task_id,
            execution_result,
            execution_plan
        )
        
        result = {
            'task_id': task_id,
            'queue_item_id': queue_item_id,
            'execution_result': execution_result,
            'feedback': feedback,
            'processed_at': datetime.now()
        }
        
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            f'Task processing completed: {task_id}',
            task_id=task_id,
            success=execution_result.get('success', False)
        )
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get System Status - 获取系统状态
        
        Returns:
            系统状态字典
        """
        return {
            'initialized': self.is_initialized,
            'version': self.settings.APPLICATION_VERSION,
            'components': {
                'storage_backend': self.storage_backend.perform_health_check(),
                'workflow_mode_coordinator': {
                    'current_mode': self.workflow_mode_coordinator.get_current_execution_mode().value
                },
                'priority_queue': self.priority_queue_manager.get_queue_statistics()
            }
        }
    
    def execute_single_task_workflow(self, raw_input: str, priority: int = 1) -> Dict[str, Any]:
        """
        Execute Single Task Workflow - 执行单个任务工作流
        
        Args:
            raw_input: 任务原始输入
            priority: 任务优先级
            
        Returns:
            执行结果字典
        """
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            'Starting single task workflow execution',
            raw_input_length=len(raw_input),
            priority_level=priority
        )
        
        task = self.task_workflow_manager.create_new_task_workflow(
            raw_input_text=raw_input,
            priority_level=priority
        )
        
        execution_plan = self.task_analyzer_planner.analyze_and_generate_execution_plan(task)
        
        execution_result = self.task_step_executor.execute_task_execution_plan(task, execution_plan)
        
        experience = self.experience_learning_manager.extract_and_store_experience(
            task.task_id,
            execution_result
        )
        
        return {
            'task_id': task.task_id,
            'execution_result': execution_result,
            'experience': experience
        }
    
    def shutdown_system(self):
        """
        Shutdown System - 关闭系统
        """
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            'Shutting down system'
        )
        
        self.priority_queue_manager.stop_queue_processing()
        self.execution_checkpoint_saver.save_checkpoint()
        
        self.is_initialized = False
        
        self.logger_backend.log_information_message(
            'SystemIntegratorComponent',
            'System shutdown complete'
        )
    
    def find_similar_tasks_and_reuse(self, raw_input: str) -> Optional[Dict[str, Any]]:
        """
        Find Similar Tasks And Reuse - 查找相似任务并重用经验
        
        Args:
            raw_input: 原始任务输入
            
        Returns:
            相似任务和建议，如果没有则返回None
        """
        task_metadata = {
            'raw_input': raw_input
        }
        
        similar_experiences = self.experience_learning_manager.find_similar_execution_experiences(
            task_metadata
        )
        
        if similar_experiences:
            return {
                'similar_experiences': similar_experiences,
                'recommendation': 'Consider using insights from similar successful tasks'
            }
        
        return None


__all__ = ['SystemIntegratorComponent']
