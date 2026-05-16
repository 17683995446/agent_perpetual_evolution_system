"""
Unit Tests for Storage Interface Contract - 存储接口契约单元测试
测试CoreStorageInterfaceContract抽象接口的契约定义
"""

import pytest
from abc import ABC
from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract


class TestStorageInterfaceContract:
    """
    Test Storage Interface Contract - 存储接口契约测试
    验证接口是抽象基类且定义了所有必需方法
    """
    
    def test_storage_interface_is_abstract_base_class(self):
        """
        Test Storage Interface Is Abstract Base Class - 测试存储接口是抽象基类
        """
        assert issubclass(CoreStorageInterfaceContract, ABC)
    
    def test_storage_interface_has_save_method(self):
        """
        Test Storage Interface Has Save Method - 测试存储接口有保存方法
        """
        assert hasattr(CoreStorageInterfaceContract, 'save_single_task_record')
    
    def test_storage_interface_has_retrieve_method(self):
        """
        Test Storage Interface Has Retrieve Method - 测试存储接口有检索方法
        """
        assert hasattr(CoreStorageInterfaceContract, 'retrieve_task_by_identifier')
    
    def test_storage_interface_has_update_method(self):
        """
        Test Storage Interface Has Update Method - 测试存储接口有更新方法
        """
        assert hasattr(CoreStorageInterfaceContract, 'update_task_status_value')
    
    def test_storage_interface_has_list_method(self):
        """
        Test Storage Interface Has List Method - 测试存储接口有列表方法
        """
        assert hasattr(CoreStorageInterfaceContract, 'get_list_of_pending_tasks')
    
    def test_storage_interface_has_health_check_method(self):
        """
        Test Storage Interface Has Health Check Method - 测试存储接口有健康检查方法
        """
        assert hasattr(CoreStorageInterfaceContract, 'perform_health_check')


class MockStorageImplementation(CoreStorageInterfaceContract):
    """
    Mock Storage Implementation - 模拟存储实现
    用于测试接口契约的完整实现
    """
    
    def __init__(self):
        self._storage = {}
    
    def save_single_task_record(self, task) -> bool:
        if hasattr(task, 'task_id'):
            self._storage[task.task_id] = task
            return True
        return False
    
    def retrieve_task_by_identifier(self, task_id: str):
        return self._storage.get(task_id)
    
    def update_task_status_value(self, task_id: str, new_status, **kwargs) -> bool:
        task = self._storage.get(task_id)
        if task:
            task.status = new_status
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            return True
        return False
    
    def get_list_of_pending_tasks(self, limit_count: int = 100):
        return list(self._storage.values())[:limit_count]
    
    def perform_health_check(self):
        return {"status": "healthy", "storage_type": "mock", "task_count": len(self._storage)}


class TestMockStorageImplementation:
    """
    Test Mock Storage Implementation - 模拟存储实现测试
    验证接口实现的正确性
    """
    
    def test_mock_storage_can_be_instantiated(self):
        """
        Test Mock Storage Can Be Instantiated - 测试模拟存储可以实例化
        """
        mock_storage = MockStorageImplementation()
        assert mock_storage is not None
        assert isinstance(mock_storage, CoreStorageInterfaceContract)
    
    def test_mock_storage_save_and_retrieve(self):
        """
        Test Mock Storage Save And Retrieve - 测试模拟存储保存和检索
        """
        mock_storage = MockStorageImplementation()
        
        class MockTask:
            task_id = "test_task_001"
            status = "PENDING"
        
        task = MockTask()
        result = mock_storage.save_single_task_record(task)
        assert result is True
        
        retrieved = mock_storage.retrieve_task_by_identifier("test_task_001")
        assert retrieved is not None
        assert retrieved.task_id == "test_task_001"
    
    def test_mock_storage_update_status(self):
        """
        Test Mock Storage Update Status - 测试模拟存储更新状态
        """
        mock_storage = MockStorageImplementation()
        
        class MockTask:
            task_id = "test_task_002"
            status = "PENDING"
        
        task = MockTask()
        mock_storage.save_single_task_record(task)
        
        result = mock_storage.update_task_status_value("test_task_002", "COMPLETED")
        assert result is True
        assert task.status == "COMPLETED"
    
    def test_mock_storage_health_check(self):
        """
        Test Mock Storage Health Check - 测试模拟存储健康检查
        """
        mock_storage = MockStorageImplementation()
        health_result = mock_storage.perform_health_check()
        
        assert "status" in health_result
        assert "storage_type" in health_result
        assert "task_count" in health_result
        assert health_result["status"] == "healthy"
