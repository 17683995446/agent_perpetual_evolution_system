"""
Unit Tests for Task Analyzer Planner Component - 任务分析规划器组件单元测试
测试任务分析规划器组件的完整功能
"""

import pytest
from unittest.mock import Mock
from ...business_domain_layer.task_processing_components.task_analyzer_planner_component import TaskAnalyzerPlannerComponent


class TestTaskAnalyzerPlannerComponent:
    """
    Test Task Analyzer Planner Component - 任务分析规划器组件测试
    验证任务分析规划器组件的基本功能
    """
    
    @pytest.fixture
    def mock_logger_backend(self):
        """Mock Logger Backend - 模拟日志后端"""
        return Mock()
    
    @pytest.fixture
    def task_analyzer_planner_component(self, mock_logger_backend):
        """Task Analyzer Planner Component Instance - 任务分析规划器组件实例"""
        return TaskAnalyzerPlannerComponent(mock_logger_backend)
    
    def test_task_analyzer_planner_component_can_be_instantiated(self, mock_logger_backend):
        """
        Test Task Analyzer Planner Component Can Be Instantiated - 测试任务分析规划器组件可以实例化
        """
        planner = TaskAnalyzerPlannerComponent(mock_logger_backend)
        assert planner is not None
        assert planner.logger_backend == mock_logger_backend
    
    def test_analyze_and_generate_execution_plan_returns_plan(self, task_analyzer_planner_component):
        """
        Test Analyze And Generate Execution Plan Returns Plan - 测试分析并生成执行计划返回计划
        """
        mock_task = Mock()
        mock_task.task_id = "test_task_001"
        mock_task.raw_input = "Search for information about Python"
        
        plan = task_analyzer_planner_component.analyze_and_generate_execution_plan(mock_task)
        
        assert plan is not None
        assert 'task_id' in plan
        assert 'identified_intent' in plan
        assert 'generated_subtasks' in plan
        assert 'execution_order_path' in plan
        assert plan['task_id'] == "test_task_001"
    
    def test_analyze_and_generate_execution_plan_logs_info(self, task_analyzer_planner_component):
        """
        Test Analyze And Generate Execution Plan Logs Info - 测试分析并生成执行计划记录日志
        """
        mock_task = Mock()
        mock_task.task_id = "test_task_002"
        mock_task.raw_input = "Create a new file"
        
        task_analyzer_planner_component.analyze_and_generate_execution_plan(mock_task)
        task_analyzer_planner_component.logger_backend.log_information_message.assert_called()
    
    def test_extract_search_intent(self, task_analyzer_planner_component):
        """
        Test Extract Search Intent - 测试提取搜索意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("search for python") == "search_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("find information") == "search_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("look up details") == "search_operation_intent"
    
    def test_extract_creation_intent(self, task_analyzer_planner_component):
        """
        Test Extract Creation Intent - 测试提取创建意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("create a file") == "creation_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("make a document") == "creation_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("build a project") == "creation_operation_intent"
    
    def test_extract_update_intent(self, task_analyzer_planner_component):
        """
        Test Extract Update Intent - 测试提取更新意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("update the config") == "update_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("modify settings") == "update_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("change the value") == "update_operation_intent"
    
    def test_extract_deletion_intent(self, task_analyzer_planner_component):
        """
        Test Extract Deletion Intent - 测试提取删除意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("delete the file") == "deletion_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("remove the entry") == "deletion_operation_intent"
    
    def test_extract_analysis_intent(self, task_analyzer_planner_component):
        """
        Test Extract Analysis Intent - 测试提取分析意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("analyze the data") == "analysis_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("examine the code") == "analysis_operation_intent"
        assert task_analyzer_planner_component._extract_task_intent_from_input("check the logs") == "analysis_operation_intent"
    
    def test_extract_general_intent(self, task_analyzer_planner_component):
        """
        Test Extract General Intent - 测试提取通用意图
        """
        assert task_analyzer_planner_component._extract_task_intent_from_input("do something") == "general_operation_intent"
    
    def test_identify_file_tool(self, task_analyzer_planner_component):
        """
        Test Identify File Tool - 测试识别文件工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("process this file")
        assert 'file_handling_tool' in tools
    
    def test_identify_web_tool(self, task_analyzer_planner_component):
        """
        Test Identify Web Tool - 测试识别网络工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("fetch from web")
        assert 'web_request_tool' in tools
    
    def test_identify_database_tool(self, task_analyzer_planner_component):
        """
        Test Identify Database Tool - 测试识别数据库工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("query database")
        assert 'database_access_tool' in tools
    
    def test_identify_api_tool(self, task_analyzer_planner_component):
        """
        Test Identify API Tool - 测试识别API工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("call the api")
        assert 'api_calling_tool' in tools
    
    def test_identify_code_tool(self, task_analyzer_planner_component):
        """
        Test Identify Code Tool - 测试识别代码工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("execute code")
        assert 'code_execution_tool' in tools
    
    def test_identify_default_tool(self, task_analyzer_planner_component):
        """
        Test Identify Default Tool - 测试识别默认工具
        """
        tools = task_analyzer_planner_component._identify_required_tools_list("do something")
        assert 'default_execution_tool' in tools
    
    def test_extract_task_goal_description(self, task_analyzer_planner_component):
        """
        Test Extract Task Goal Description - 测试提取任务目标描述
        """
        short_input = "Short task"
        long_input = "A" * 150
        
        short_desc = task_analyzer_planner_component._extract_task_goal_description(short_input)
        long_desc = task_analyzer_planner_component._extract_task_goal_description(long_input)
        
        assert short_desc == "Short task"
        assert len(long_desc) == 103  # 100 chars + "..."
    
    def test_generate_subtask_list_structure(self, task_analyzer_planner_component):
        """
        Test Generate Subtask List Structure - 测试生成子任务列表结构
        """
        mock_task = Mock()
        mock_task.task_id = "task_001"
        
        subtasks = task_analyzer_planner_component._generate_subtask_list(
            mock_task,
            "search_operation_intent",
            ["file_handling_tool"]
        )
        
        assert len(subtasks) >= 4
        for subtask in subtasks:
            assert 'subtask_id' in subtask
            assert 'parent_task_id' in subtask
            assert 'description' in subtask
            assert 'dependencies' in subtask
            assert 'status' in subtask
    
    def test_determine_execution_order_path(self, task_analyzer_planner_component):
        """
        Test Determine Execution Order Path - 测试确定执行顺序路径
        """
        subtasks = [
            {'subtask_id': 's1', 'dependencies': []},
            {'subtask_id': 's2', 'dependencies': ['s1']},
            {'subtask_id': 's3', 'dependencies': ['s1']},
            {'subtask_id': 's4', 'dependencies': ['s2', 's3']}
        ]
        
        path = task_analyzer_planner_component._determine_execution_order_path(subtasks)
        
        assert path[0] == 's1'
        assert path.index('s2') > path.index('s1')
        assert path.index('s3') > path.index('s1')
        assert path.index('s4') > path.index('s2')
        assert path.index('s4') > path.index('s3')
