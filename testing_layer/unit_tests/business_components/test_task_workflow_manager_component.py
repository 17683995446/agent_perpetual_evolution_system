"""
Unit Tests for Task Workflow Manager Component - 任务工作流管理器组件单元测试
测试任务工作流管理器组件的完整功能
"""

import pytest
from unittest.mock import Mock
from ...business_domain_layer.task_processing_components.task_workflow_manager_component import TaskWorkflowManagerComponent


class TestTaskWorkflowManagerComponent:
    """
    Test Task Workflow Manager Component - 任务工作流管理器组件测试
    验证任务工作流管理器组件的基本功能
    """
    
    @pytest.fixture
    def mock_storage_backend(self):
        """Mock Storage Backend - 模拟存储后端"""
        return Mock()
    
    @pytest.fixture
    def mock_logger_backend(self):
        """Mock Logger Backend - 模拟日志后端"""
        return Mock()
    
    @pytest.fixture
    def task_workflow_manager_component(self, mock_storage_backend, mock_logger_backend):
        """Task Workflow Manager Component Instance - 任务工作流管理器组件实例"""
        return TaskWorkflowManagerComponent(mock_storage_backend, mock_logger_backend)
    
    def test_task_workflow_manager_component_can_be_instantiated(
        self, mock_storage_backend, mock_logger_backend
    ):
        """
        Test Task Workflow Manager Component Can Be Instantiated - 测试任务工作流管理器组件可以实例化
        """
        manager = TaskWorkflowManagerComponent(mock_storage_backend, mock_logger_backend)
        assert manager is not None
        assert manager.storage_backend == mock_storage_backend
        assert manager.logger_backend == mock_logger_backend
    
    def test_create_new_task_workflow_returns_task(
        self, task_workflow_manager_component, mock_storage_backend, mock_logger_backend
    ):
        """
        Test Create New Task Workflow Returns Task - 测试创建新任务工作流返回任务
        """
        task = task_workflow_manager_component.create_new_task_workflow(
            raw_input_text="Test task input",
            priority_level=2
        )
        
        assert task is not None
        assert hasattr(task, 'task_id')
        assert hasattr(task, 'raw_input')
        assert task.raw_input == "Test task input"
        assert task.priority == 2
        assert task.status == "PENDING"
    
    def test_create_new_task_workflow_saves_to_storage(
        self, task_workflow_manager_component, mock_storage_backend
    ):
        """
        Test Create New Task Workflow Saves To Storage - 测试创建新任务工作流保存到存储
        """
        task_workflow_manager_component.create_new_task_workflow("Test input")
        mock_storage_backend.save_single_task_record.assert_called_once()
    
    def test_create_new_task_workflow_logs_info(
        self, task_workflow_manager_component, mock_logger_backend
    ):
        """
        Test Create New Task Workflow Logs Info - 测试创建新任务工作流记录信息日志
        """
        task_workflow_manager_component.create_new_task_workflow("Test input")
        mock_logger_backend.log_information_message.assert_called()
    
    def test_retrieve_task_by_identifier_found(
        self, task_workflow_manager_component, mock_storage_backend
    ):
        """
        Test Retrieve Task By Identifier Found - 测试根据标识符检索找到的任务
        """
        mock_task = Mock()
        mock_task.task_id = "test_123"
        mock_storage_backend.retrieve_task_by_identifier.return_value = mock_task
        
        result = task_workflow_manager_component.retrieve_task_by_identifier("test_123")
        assert result == mock_task
    
    def test_retrieve_task_by_identifier_not_found(
        self, task_workflow_manager_component, mock_storage_backend, mock_logger_backend
    ):
        """
        Test Retrieve Task By Identifier Not Found - 测试根据标识符检索未找到的任务
        """
        mock_storage_backend.retrieve_task_by_identifier.return_value = None
        
        result = task_workflow_manager_component.retrieve_task_by_identifier("nonexistent")
        assert result is None
        mock_logger_backend.log_warning_message.assert_called()
    
    def test_list_all_pending_task_workflows(
        self, task_workflow_manager_component, mock_storage_backend
    ):
        """
        Test List All Pending Task Workflows - 测试列出所有待处理任务
        """
        mock_tasks = [Mock(), Mock(), Mock()]
        mock_storage_backend.get_list_of_pending_tasks.return_value = mock_tasks
        
        result = task_workflow_manager_component.list_all_pending_task_workflows(limit_count=10)
        assert len(result) == 3
        mock_storage_backend.get_list_of_pending_tasks.assert_called_once_with(limit_count=10)
    
    def test_update_task_workflow_status_success(
        self, task_workflow_manager_component, mock_storage_backend, mock_logger_backend
    ):
        """
        Test Update Task Workflow Status Success - 测试更新任务工作流状态成功
        """
        mock_storage_backend.update_task_status_value.return_value = True
        
        result = task_workflow_manager_component.update_task_workflow_status(
            "task_123",
            "COMPLETED"
        )
        
        assert result is True
        mock_logger_backend.log_information_message.assert_called()
    
    def test_update_task_workflow_status_failure(
        self, task_workflow_manager_component, mock_storage_backend, mock_logger_backend
    ):
        """
        Test Update Task Workflow Status Failure - 测试更新任务工作流状态失败
        """
        mock_storage_backend.update_task_status_value.return_value = False
        
        result = task_workflow_manager_component.update_task_workflow_status(
            "nonexistent",
            "COMPLETED"
        )
        
        assert result is False
        mock_logger_backend.log_error_message.assert_called()
    
    def test_get_task_workflow_statistics(
        self, task_workflow_manager_component, mock_storage_backend
    ):
        """
        Test Get Task Workflow Statistics - 测试获取任务工作流统计
        """
        mock_task_1 = Mock()
        mock_task_1.priority = 1
        mock_task_2 = Mock()
        mock_task_2.priority = 2
        mock_task_3 = Mock()
        mock_task_3.priority = 1
        
        mock_storage_backend.get_list_of_pending_tasks.return_value = [
            mock_task_1, mock_task_2, mock_task_3
        ]
        
        statistics = task_workflow_manager_component.get_task_workflow_statistics()
        
        assert 'pending_task_count' in statistics
        assert 'priority_distribution' in statistics
        assert statistics['pending_task_count'] == 3
        assert statistics['priority_distribution']['1'] == 2
        assert statistics['priority_distribution']['2'] == 1
