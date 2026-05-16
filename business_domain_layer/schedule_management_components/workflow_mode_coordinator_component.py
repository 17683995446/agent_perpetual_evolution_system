"""
Workflow Mode Coordinator Component - 工作流模式协调器组件
负责协调和切换不同的工作流执行模式
"""

from typing import Dict, Any, Optional
from enum import Enum

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class WorkflowExecutionMode(Enum):
    """
    Workflow Execution Mode - 工作流执行模式
    """
    SEQUENTIAL = 'sequential'
    PARALLEL = 'parallel'
    ADAPTIVE = 'adaptive'
    BATCH = 'batch'


class WorkflowModeCoordinatorComponent:
    """
    Workflow Mode Coordinator Component - 工作流模式协调器组件
    
    负责协调和切换不同的工作流执行模式
    根据任务特性和系统状态选择最优的执行策略
    """
    
    def __init__(self, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Workflow Mode Coordinator Component - 初始化工作流模式协调器组件
        
        Args:
            logger_backend: 日志后端实例
        """
        self.logger_backend = logger_backend
        self.current_mode = WorkflowExecutionMode.SEQUENTIAL
        self.mode_history = []
    
    def determine_optimal_execution_mode(self, task_metadata: Dict[str, Any]) -> WorkflowExecutionMode:
        """
        Determine Optimal Execution Mode - 确定最优执行模式
        
        Args:
            task_metadata: 任务元数据
            
        Returns:
            推荐的工作流执行模式
        """
        self.logger_backend.log_debug_message(
            'WorkflowModeCoordinatorComponent',
            'Analyzing task metadata to determine optimal execution mode',
            task_metadata=task_metadata
        )
        
        # 简单的决策逻辑
        subtask_count = task_metadata.get('subtask_count', 0)
        has_dependencies = task_metadata.get('has_dependencies', False)
        
        if subtask_count > 10 and not has_dependencies:
            recommended_mode = WorkflowExecutionMode.PARALLEL
        elif subtask_count > 50:
            recommended_mode = WorkflowExecutionMode.BATCH
        elif has_dependencies and subtask_count > 5:
            recommended_mode = WorkflowExecutionMode.ADAPTIVE
        else:
            recommended_mode = WorkflowExecutionMode.SEQUENTIAL
        
        self.logger_backend.log_information_message(
            'WorkflowModeCoordinatorComponent',
            f'Recommended execution mode: {recommended_mode.value}',
            mode=recommended_mode.value
        )
        
        return recommended_mode
    
    def switch_execution_mode(self, new_mode: WorkflowExecutionMode) -> bool:
        """
        Switch Execution Mode - 切换执行模式
        
        Args:
            new_mode: 新的工作流执行模式
            
        Returns:
            bool: 切换是否成功
        """
        old_mode = self.current_mode
        
        if old_mode == new_mode:
            self.logger_backend.log_debug_message(
                'WorkflowModeCoordinatorComponent',
                f'Already in mode: {new_mode.value}',
                mode=new_mode.value
            )
            return True
        
        self.mode_history.append({
            'timestamp': str(__import__('datetime').datetime.now()),
            'old_mode': old_mode.value,
            'new_mode': new_mode.value
        })
        
        self.current_mode = new_mode
        
        self.logger_backend.log_information_message(
            'WorkflowModeCoordinatorComponent',
            f'Switched execution mode from {old_mode.value} to {new_mode.value}',
            old_mode=old_mode.value,
            new_mode=new_mode.value
        )
        
        return True
    
    def get_current_execution_mode(self) -> WorkflowExecutionMode:
        """
        Get Current Execution Mode - 获取当前执行模式
        
        Returns:
            当前工作流执行模式
        """
        return self.current_mode
    
    def get_mode_transition_history(self, limit: int = 10) -> list:
        """
        Get Mode Transition History - 获取模式转换历史
        
        Args:
            limit: 返回历史记录的数量限制
            
        Returns:
            模式转换历史列表
        """
        return self.mode_history[-limit:]


__all__ = ['WorkflowModeCoordinatorComponent', 'WorkflowExecutionMode']
