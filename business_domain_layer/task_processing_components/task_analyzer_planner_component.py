"""
Task Analyzer Planner Component - 任务分析规划器组件
负责分析输入任务并生成详细的执行计划
"""

from typing import Dict, Any, List
from datetime import datetime
import uuid

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class TaskAnalyzerPlannerComponent:
    """
    Task Analyzer Planner Component - 任务分析规划器组件
    
    负责分析输入任务并生成详细的执行计划
    包括子任务分解、依赖关系分析、执行顺序规划等
    """
    
    def __init__(self, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Task Analyzer Planner Component - 初始化任务分析规划器组件
        
        Args:
            logger_backend: 日志后端实例
        """
        self.logger_backend = logger_backend
    
    def analyze_and_generate_execution_plan(self, task_object) -> Dict[str, Any]:
        """
        Analyze And Generate Execution Plan - 分析并生成执行计划
        
        Args:
            task_object: 输入任务对象
            
        Returns:
            完整的执行计划字典
        """
        self.logger_backend.log_information_message(
            'TaskAnalyzerPlannerComponent',
            f'Analyzing task for execution plan: {task_object.task_id}',
            task_id=task_object.task_id
        )
        
        # 分析任务意图
        identified_intent = self._extract_task_intent_from_input(task_object.raw_input)
        
        # 确定所需工具
        required_tool_list = self._identify_required_tools_list(task_object.raw_input)
        
        # 生成子任务
        generated_subtasks = self._generate_subtask_list(task_object, identified_intent, required_tool_list)
        
        # 确定执行顺序
        execution_order_path = self._determine_execution_order_path(generated_subtasks)
        
        # 创建执行计划
        execution_plan = {
            'task_id': task_object.task_id,
            'identified_intent': identified_intent,
            'task_goal': self._extract_task_goal_description(task_object.raw_input),
            'generated_subtasks': generated_subtasks,
            'execution_order_path': execution_order_path,
            'dependencies_valid': True
        }
        
        self.logger_backend.log_information_message(
            'TaskAnalyzerPlannerComponent',
            f'Execution plan generated for task: {task_object.task_id}',
            task_id=task_object.task_id,
            subtask_count=len(generated_subtasks)
        )
        
        return execution_plan
    
    def _extract_task_intent_from_input(self, raw_input: str) -> str:
        """
        Extract Task Intent From Input - 从输入中提取任务意图
        
        Args:
            raw_input: 任务原始输入
            
        Returns:
            识别的任务意图
        """
        raw_input_lower = raw_input.lower()
        
        if any(keyword in raw_input_lower for keyword in ['search', 'find', 'look']):
            return 'search_operation_intent'
        elif any(keyword in raw_input_lower for keyword in ['create', 'make', 'build']):
            return 'creation_operation_intent'
        elif any(keyword in raw_input_lower for keyword in ['update', 'modify', 'change']):
            return 'update_operation_intent'
        elif any(keyword in raw_input_lower for keyword in ['delete', 'remove']):
            return 'deletion_operation_intent'
        elif any(keyword in raw_input_lower for keyword in ['analyze', 'examine', 'check']):
            return 'analysis_operation_intent'
        else:
            return 'general_operation_intent'
    
    def _identify_required_tools_list(self, raw_input: str) -> List[str]:
        """
        Identify Required Tools List - 识别所需工具列表
        
        Args:
            raw_input: 任务原始输入
            
        Returns:
            所需工具列表
        """
        tool_list = []
        raw_input_lower = raw_input.lower()
        
        if 'file' in raw_input_lower:
            tool_list.append('file_handling_tool')
        if 'web' in raw_input_lower or 'http' in raw_input_lower:
            tool_list.append('web_request_tool')
        if 'database' in raw_input_lower or 'sql' in raw_input_lower:
            tool_list.append('database_access_tool')
        if 'api' in raw_input_lower:
            tool_list.append('api_calling_tool')
        if 'code' in raw_input_lower or 'programming' in raw_input_lower:
            tool_list.append('code_execution_tool')
        
        return tool_list if tool_list else ['default_execution_tool']
    
    def _extract_task_goal_description(self, raw_input: str) -> str:
        """
        Extract Task Goal Description - 提取任务目标描述
        
        Args:
            raw_input: 任务原始输入
            
        Returns:
            任务目标描述
        """
        return raw_input[:100] + ('...' if len(raw_input) > 100 else '')
    
    def _generate_subtask_list(
        self, 
        task_object, 
        identified_intent: str, 
        required_tool_list: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate Subtask List - 生成子任务列表
        
        Args:
            task_object: 主任务对象
            identified_intent: 识别的意图
            required_tool_list: 所需工具列表
            
        Returns:
            子任务列表
        """
        subtask_list = []
        
        # 第一步：分析和理解任务需求
        subtask_step_1 = {
            'subtask_id': str(uuid.uuid4()),
            'parent_task_id': task_object.task_id,
            'description': 'Analyze and understand task requirements',
            'dependencies': [],
            'status': 'PENDING'
        }
        subtask_list.append(subtask_step_1)
        
        # 第二步：如果需要特殊工具，准备工具
        if required_tool_list and required_tool_list != ['default_execution_tool']:
            subtask_step_2 = {
                'subtask_id': str(uuid.uuid4()),
                'parent_task_id': task_object.task_id,
                'description': f'Prepare required tools: {", ".join(required_tool_list)}',
                'dependencies': [subtask_step_1['subtask_id']],
                'status': 'PENDING'
            }
            subtask_list.append(subtask_step_2)
        
        # 第三步：执行主要操作
        main_dependencies = [subtask_step_1['subtask_id']]
        if len(subtask_list) > 1:
            main_dependencies.append(subtask_list[1]['subtask_id'])
        
        subtask_step_3 = {
            'subtask_id': str(uuid.uuid4()),
            'parent_task_id': task_object.task_id,
            'description': f'Execute {identified_intent} operation',
            'dependencies': main_dependencies,
            'status': 'PENDING'
        }
        subtask_list.append(subtask_step_3)
        
        # 第四步：验证执行结果
        subtask_step_4 = {
            'subtask_id': str(uuid.uuid4()),
            'parent_task_id': task_object.task_id,
            'description': 'Verify execution results and quality',
            'dependencies': [subtask_step_3['subtask_id']],
            'status': 'PENDING'
        }
        subtask_list.append(subtask_step_4)
        
        return subtask_list
    
    def _determine_execution_order_path(self, subtask_list: List[Dict[str, Any]]) -> List[str]:
        """
        Determine Execution Order Path - 确定执行顺序路径
        
        Args:
            subtask_list: 子任务列表
            
        Returns:
            子任务ID的执行顺序列表
        """
        execution_path = []
        remaining_subtasks = subtask_list.copy()
        
        while remaining_subtasks:
            for index, subtask in enumerate(remaining_subtasks):
                all_dependencies_satisfied = all(
                    dep_id in execution_path 
                    for dep_id in subtask['dependencies']
                )
                if all_dependencies_satisfied:
                    execution_path.append(subtask['subtask_id'])
                    remaining_subtasks.pop(index)
                    break
            else:
                execution_path.append(remaining_subtasks[0]['subtask_id'])
                remaining_subtasks.pop(0)
        
        return execution_path


__all__ = ['TaskAnalyzerPlannerComponent']
