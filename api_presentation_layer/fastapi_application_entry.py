"""
FastAPI Application Main - FastAPI应用主入口
整合所有路由和中间件的FastAPI应用程序
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import structlog

from ..configuration_management_layer import get_application_global_settings
from .api_routes import health_router, task_router

# 获取应用配置
application_settings = get_application_global_settings()

# 配置结构化日志
INFO_LOG_LEVEL_VALUE = 20  # structlog.INFO = 20
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(INFO_LOG_LEVEL_VALUE),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

# 获取日志实例
application_logger = structlog.get_logger()

# 创建FastAPI应用实例
fastapi_application = FastAPI(
    title="Agent Evolution System API",
    description="高度模块化的Agent永续自进化运行系统 - 产品级API服务",
    version=application_settings.APPLICATION_VERSION,
    docs_url="/api/documentation",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 添加CORS中间件
fastapi_application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有API路由
fastapi_application.include_router(health_router)
fastapi_application.include_router(task_router)


@fastapi_application.on_event("startup")
async def application_startup_event():
    """
    Application Startup Event - 应用程序启动事件
    """
    application_logger.info("api_application_starting", version=application_settings.APPLICATION_VERSION)
    print(f"🚀 Agent Evolution System API starting... Version: {application_settings.APPLICATION_VERSION}")


@fastapi_application.on_event("shutdown")
async def application_shutdown_event():
    """
    Application Shutdown Event - 应用程序关闭事件
    """
    application_logger.info("api_application_shutting_down")
    print("👋 Agent Evolution System API shutting down...")


@fastapi_application.get("/")
async def root_endpoint():
    """
    Root Endpoint - 根端点
    """
    return {
        "application_name": "Agent Evolution System",
        "application_version": application_settings.APPLICATION_VERSION,
        "description": "高度模块化的Agent永续自进化运行系统",
        "documentation_url": "/api/documentation",
        "health_check_url": "/health"
    }


@fastapi_application.get("/metrics")
async def metrics_endpoint():
    """
    Metrics Endpoint - 指标端点
    """
    return {
        "metrics_timestamp": datetime.now().isoformat(),
        "application_version": application_settings.APPLICATION_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "agent_perpetual_evolution_system.api_presentation_layer.fastapi_application_entry:fastapi_application",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )


__all__ = ['fastapi_application']
