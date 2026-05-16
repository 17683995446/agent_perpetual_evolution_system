"""
Unit Tests for Memory Based Storage Adapter - 基于内存的存储适配器单元测试
测试基于内存的存储适配器的完整功能
"""

import pytest
import threading
import time
from ...infrastructure_adapter_layer.storage_backends.memory_based_storage_adapter import MemoryBasedStorageAdapter


class MockTask:
    """Mock Task - 模拟任务对象"""
    
    def __init__(self, task_id: str, status: str = "PENDING"):
        self.task_id = task_id
        self.status = status
        self.raw_input = "test input"
        self.priority = "MEDIUM"


class TestMemoryBasedStorageAdapter:
    """
    Test Memory Based Storage Adapter - 基于内存的存储适配器测试
    验证存储适配器的基本功能
    """
    
    def test_adapter_can_be_instantiated(self):
        """
        Test Adapter Can Be Instantiated - 测试适配器可以实例化
        """
        adapter = MemoryBasedStorageAdapter()
        assert adapter is not None
    
    def test_adapter_save_single_task_record(self):
        """
        Test Adapter Save Single Task Record - 测试适配器保存单个任务记录
        """
        adapter = MemoryBasedStorageAdapter()
        task = MockTask("task_001")
        
        result = adapter.save_single_task_record(task)
        assert result is True
    
    def test_adapter_retrieve_task_by_identifier(self):
        """
        Test Adapter Retrieve Task By Identifier - 测试适配器根据标识符检索任务
        """
        adapter = MemoryBasedStorageAdapter()
        task = MockTask("task_002")
        adapter.save_single_task_record(task)
        
        retrieved = adapter.retrieve_task_by_identifier("task_002")
        assert retrieved is not None
        assert retrieved.task_id == "task_002"
    
    def test_adapter_retrieve_nonexistent_task(self):
        """
        Test Adapter Retrieve Nonexistent Task - 测试适配器检索不存在的任务
        """
        adapter = MemoryBasedStorageAdapter()
        retrieved = adapter.retrieve_task_by_identifier("nonexistent_id")
        assert retrieved is None
    
    def test_adapter_update_task_status_value(self):
        """
        Test Adapter Update Task Status Value - 测试适配器更新任务状态值
        """
        adapter = MemoryBasedStorageAdapter()
        task = MockTask("task_003", "PENDING")
        adapter.save_single_task_record(task)
        
        result = adapter.update_task_status_value("task_003", "COMPLETED")
        assert result is True
        assert task.status == "COMPLETED"
    
    def test_adapter_update_task_with_extra_kwargs(self):
        """
        Test Adapter Update Task With Extra Kwargs - 测试适配器使用额外参数更新任务
        """
        adapter = MemoryBasedStorageAdapter()
        task = MockTask("task_004", "PENDING")
        adapter.save_single_task_record(task)
        
        result = adapter.update_task_status_value(
            "task_004",
            "RUNNING",
            started_at=time.time()
        )
        assert result is True
        assert task.status == "RUNNING"
    
    def test_adapter_update_nonexistent_task_returns_false(self):
        """
        Test Adapter Update Nonexistent Task Returns False - 测试更新不存在任务返回False
        """
        adapter = MemoryBasedStorageAdapter()
        result = adapter.update_task_status_value("nonexistent", "COMPLETED")
        assert result is False
    
    def test_adapter_get_list_of_pending_tasks(self):
        """
        Test Adapter Get List Of Pending Tasks - 测试适配器获取待处理任务列表
        """
        adapter = MemoryBasedStorageAdapter()
        
        for i in range(5):
            task = MockTask(f"task_{i:03d}")
            adapter.save_single_task_record(task)
        
        pending_tasks = adapter.get_list_of_pending_tasks()
        assert len(pending_tasks) == 5
    
    def test_adapter_get_list_with_limit(self):
        """
        Test Adapter Get List With Limit - 测试适配器获取带限制的任务列表
        """
        adapter = MemoryBasedStorageAdapter()
        
        for i in range(10):
            task = MockTask(f"task_{i:03d}")
            adapter.save_single_task_record(task)
        
        pending_tasks = adapter.get_list_of_pending_tasks(limit_count=3)
        assert len(pending_tasks) == 3
    
    def test_adapter_perform_health_check(self):
        """
        Test Adapter Perform Health Check - 测试适配器执行健康检查
        """
        adapter = MemoryBasedStorageAdapter()
        task = MockTask("task_health")
        adapter.save_single_task_record(task)
        
        health_result = adapter.perform_health_check()
        
        assert "status" in health_result
        assert "storage_type" in health_result
        assert "task_count" in health_result
        assert health_result["status"] == "healthy"
        assert health_result["storage_type"] == "in_memory"
        assert health_result["task_count"] == 1


class TestMemoryBasedStorageAdapterConcurrency:
    """
    Test Memory Based Storage Adapter Concurrency - 基于内存的存储适配器并发测试
    验证存储适配器的线程安全性
    """
    
    def test_adapter_thread_safe_concurrent_saves(self):
        """
        Test Adapter Thread Safe Concurrent Saves - 测试适配器线程安全并发保存
        """
        adapter = MemoryBasedStorageAdapter()
        errors = []
        
        def save_tasks(start_id: int, count: int):
            try:
                for i in range(count):
                    task = MockTask(f"concurrent_task_{start_id + i}")
                    adapter.save_single_task_record(task)
            except Exception as e:
                errors.append(e)
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=save_tasks, args=(i * 10, 10))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0
        health = adapter.perform_health_check()
        assert health["task_count"] == 50
    
    def test_adapter_thread_safe_concurrent_reads(self):
        """
        Test Adapter Thread Safe Concurrent Reads - 测试适配器线程安全并发读取
        """
        adapter = MemoryBasedStorageAdapter()
        
        for i in range(20):
            task = MockTask(f"read_task_{i}")
            adapter.save_single_task_record(task)
        
        errors = []
        
        def read_tasks(task_id: str):
            try:
                for _ in range(100):
                    adapter.retrieve_task_by_identifier(task_id)
            except Exception as e:
                errors.append(e)
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=read_tasks, args=(f"read_task_{i}",))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0
