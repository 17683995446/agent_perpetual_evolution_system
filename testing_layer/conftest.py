"""
Test Configuration - 测试配置
pytest配置文件，提供测试夹具和配置
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_storage_backend():
    """
    Mock Storage Backend Fixture - 模拟存储后端夹具
    """
    from unittest.mock import Mock
    
    mock_storage = Mock()
    mock_storage.save_single_task_record.return_value = True
    mock_storage.update_task_status_value.return_value = True
    mock_storage.retrieve_task_by_identifier.return_value = None
    mock_storage.get_list_of_pending_tasks.return_value = []
    mock_storage.perform_health_check.return_value = {
        "status": "healthy",
        "storage_type": "mock",
        "task_count": 0
    }
    
    return mock_storage


@pytest.fixture
def mock_logger_backend():
    """
    Mock Logger Backend Fixture - 模拟日志后端夹具
    """
    from unittest.mock import Mock
    
    mock_logger = Mock()
    
    return mock_logger


@pytest.fixture
def sample_task_data():
    """
    Sample Task Data Fixture - 示例任务数据夹具
    """
    return {
        "task_id": "test_task_001",
        "raw_input": "Test task input text",
        "priority": 1,
        "status": "PENDING"
    }
