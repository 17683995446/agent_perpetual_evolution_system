"""
Integration Tests for API Endpoints - API端点集成测试
测试FastAPI应用程序的完整API端点功能
"""

import pytest
from fastapi.testclient import TestClient
from ...api_presentation_layer.fastapi_application_entry import fastapi_application


class TestRootEndpoint:
    """
    Test Root Endpoint - 根端点测试
    验证应用程序根端点的响应
    """
    
    @pytest.fixture
    def client(self):
        """Test Client - 测试客户端"""
        return TestClient(fastapi_application)
    
    def test_root_endpoint_returns_welcome_message(self, client):
        """
        Test Root Endpoint Returns Welcome Message - 测试根端点返回欢迎消息
        """
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "application_name" in data
        assert data["application_name"] == "Agent Evolution System"
    
    def test_root_endpoint_contains_version_info(self, client):
        """
        Test Root Endpoint Contains Version Info - 测试根端点包含版本信息
        """
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "application_version" in data
    
    def test_root_endpoint_contains_documentation_url(self, client):
        """
        Test Root Endpoint Contains Documentation URL - 测试根端点包含文档URL
        """
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "documentation_url" in data


class TestHealthEndpoint:
    """
    Test Health Endpoint - 健康检查端点测试
    验证健康检查端点的功能
    """
    
    @pytest.fixture
    def client(self):
        """Test Client - 测试客户端"""
        return TestClient(fastapi_application)
    
    def test_health_endpoint_returns_healthy_status(self, client):
        """
        Test Health Endpoint Returns Healthy Status - 测试健康端点返回健康状态
        """
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_health_endpoint_contains_timestamp(self, client):
        """
        Test Health Endpoint Contains Timestamp - 测试健康端点包含时间戳
        """
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
    
    def test_liveness_endpoint_returns_live(self, client):
        """
        Test Liveness Endpoint Returns Live - 测试存活探针端点返回存活状态
        """
        response = client.get("/health/liveness")
        
        assert response.status_code == 200
        data = response.json()
    
    def test_readiness_endpoint_returns_ready(self, client):
        """
        Test Readiness Endpoint Returns Ready - 测试就绪探针端点返回就绪状态
        """
        response = client.get("/health/readiness")
        
        assert response.status_code == 200
        data = response.json()


class TestMetricsEndpoint:
    """
    Test Metrics Endpoint - 指标端点测试
    验证指标端点的功能
    """
    
    @pytest.fixture
    def client(self):
        """Test Client - 测试客户端"""
        return TestClient(fastapi_application)
    
    def test_metrics_endpoint_returns_metrics(self, client):
        """
        Test Metrics Endpoint Returns Metrics - 测试指标端点返回指标
        """
        response = client.get("/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert "metrics_timestamp" in data
    
    def test_metrics_endpoint_contains_version(self, client):
        """
        Test Metrics Endpoint Contains Version - 测试指标端点包含版本
        """
        response = client.get("/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert "application_version" in data


class TestTaskEndpoints:
    """
    Test Task Endpoints - 任务端点测试
    验证任务管理API端点的功能
    """
    
    @pytest.fixture
    def client(self):
        """Test Client - 测试客户端"""
        return TestClient(fastapi_application)
    
    def test_list_tasks_endpoint(self, client):
        """
        Test List Tasks Endpoint - 测试列出任务端点
        """
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == 200


class TestAPIDocumentation:
    """
    Test API Documentation - API文档测试
    验证API文档端点的可用性
    """
    
    @pytest.fixture
    def client(self):
        """Test Client - 测试客户端"""
        return TestClient(fastapi_application)
    
    def test_openapi_endpoint_available(self, client):
        """
        Test OpenAPI Endpoint Available - 测试OpenAPI端点可用
        """
        response = client.get("/api/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
    
    def test_swagger_ui_endpoint_available(self, client):
        """
        Test Swagger UI Endpoint Available - 测试Swagger UI端点可用
        """
        response = client.get("/api/documentation")
        
        assert response.status_code == 200
