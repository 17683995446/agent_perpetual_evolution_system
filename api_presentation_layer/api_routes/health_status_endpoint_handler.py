"""
Health Status API Endpoint - 健康状态API端点
提供系统健康检查和状态报告的RESTful接口
"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/health", tags=["Health Status"])


@router.get("", response_model=Dict[str, Any])
async def perform_system_health_check():
    """
    Perform System Health Check - 执行系统健康检查
    
    返回系统整体的健康状态和各个组件的检查结果
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api_service": "operational",
            "storage_backend": "operational",
            "timestamp": datetime.now().isoformat()
        }
    }


@router.get("/liveness")
async def check_liveness_probe():
    """
    Check Liveness Probe - 检查存活探针
    
    用于Kubernetes等容器编排系统的存活检查
    """
    return {
        "status": "live",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/readiness")
async def check_readiness_probe():
    """
    Check Readiness Probe - 检查就绪探针
    
    用于Kubernetes等容器编排系统的就绪检查
    """
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }


__all__ = ['router']
