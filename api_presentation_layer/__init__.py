"""
Agent Perpetual Evolution System - 05 API Presentation Layer
Agent永续自进化运行系统 - 05 API展示层

提供FastAPI RESTful接口
"""

from .fastapi_application_entry import fastapi_application
from .api_routes import health_router, task_router

__all__ = [
    'fastapi_application',
    'health_router',
    'task_router'
]
