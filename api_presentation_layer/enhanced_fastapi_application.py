"""
Enhanced FastAPI Application - 增强版 FastAPI 应用
集成异步、监控、定时任务等功能的完整 API 应用
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
import uuid
from datetime import datetime

from ...business_domain_layer.system_integration_components import SystemIntegratorComponent
from ...business_domain_layer.schedule_management_components import ScheduledTask, SimpleScheduledTaskScheduler
from ...performance_monitoring_and_metrics import (
    SystemPerformanceMonitor,
    SimplePrometheusClient,
    SystemMetricsCollector,
    MetricsMiddleware
)
from ...common_utilities_and_helpers import ConfigurationValidator, validate_configuration


class TaskRequest(BaseModel):
    """任务请求模型"""
    raw_input: str
    priority: int = 1
    timeout: Optional[int] = None


class TaskResponse(BaseModel):
    """任务响应模型"""
    task_id: str
    execution_result: Dict[str, Any]
    experience: Dict[str, Any]


class ScheduledTaskRequest(BaseModel):
    """定时任务请求模型"""
    cron_expression: str
    task_input: str
    task_name: Optional[str] = None


app = FastAPI(
    title="Agent Perpetual Evolution System API",
    description="Agent 永续自进化系统 API",
    version="3.2.0"
)

system_integrator: Optional[SystemIntegratorComponent] = None
performance_monitor: Optional[SystemPerformanceMonitor] = None
prometheus_client: Optional[SimplePrometheusClient] = None
metrics_collector: Optional[SystemMetricsCollector] = None
scheduler: Optional[SimpleScheduledTaskScheduler] = None


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    global system_integrator, performance_monitor, prometheus_client, metrics_collector, scheduler
    
    system_integrator = SystemIntegratorComponent()
    
    performance_monitor = SystemPerformanceMonitor(logger_backend=system_integrator.logger_backend)
    
    prometheus_client = SimplePrometheusClient(logger_backend=system_integrator.logger_backend)
    
    metrics_collector = SystemMetricsCollector(prometheus_client)
    
    scheduler = SimpleScheduledTaskScheduler(logger_backend=system_integrator.logger_backend)
    
    print("🚀 Agent Perpetual Evolution System API started!")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    if scheduler:
        scheduler.stop_scheduler()
    
    if system_integrator:
        system_integrator.shutdown_system()
    
    print("🔄 System shutdown completed")


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    start_time = time.time()
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": time.time() - start_time
    }
    
    if prometheus_client:
        health_status["metrics"] = prometheus_client.get_metrics()
    
    if performance_monitor:
        health_status["performance"] = performance_monitor.get_overall_health_status()
    
    return health_status


@app.get("/metrics", tags=["Monitoring"], response_class=PlainTextResponse)
async def get_metrics():
    """获取 Prometheus 指标"""
    if prometheus_client:
        return prometheus_client.format_prometheus_text()
    
    return "# No metrics available"


@app.post("/api/tasks", tags=["Tasks"], status_code=status.HTTP_201_CREATED)
async def create_and_execute_task(task_request: TaskRequest):
    """创建并执行任务"""
    start_time = time.time()
    
    if not system_integrator:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    try:
        result = system_integrator.execute_single_task_workflow(
            raw_input=task_request.raw_input,
            priority=task_request.priority
        )
        
        if performance_monitor:
            performance_monitor.record_task_execution(
                result["task_id"],
                result["execution_result"]["success"],
                "general"
            )
        
        if metrics_collector:
            metrics_collector.record_task_execution(
                "general",
                result["execution_result"]["success"],
                result["execution_result"].get("total_duration_seconds", 0)
            )
        
        return TaskResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{task_id}", tags=["Tasks"])
async def get_task_status(task_id: str):
    """获取任务状态"""
    if not system_integrator:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    task = system_integrator.task_workflow_manager.retrieve_task_by_identifier(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_id": task_id, "status": getattr(task, "status", "unknown")}


@app.get("/api/tasks", tags=["Tasks"])
async def list_tasks(limit: int = 100):
    """列出任务"""
    if not system_integrator:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    try:
        pending_tasks = system_integrator.task_workflow_manager.list_all_pending_task_workflows(limit_count=limit)
        return {
            "pending_tasks_count": len(pending_tasks),
            "tasks": [{"task_id": task.task_id, "status": getattr(task, "status", "unknown")} for task in pending_tasks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scheduled-tasks", tags=["Scheduled Tasks"], status_code=status.HTTP_201_CREATED)
async def create_scheduled_task(scheduled_request: ScheduledTaskRequest):
    """创建定时任务"""
    if not scheduler or not system_integrator:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    def task_function():
        return system_integrator.execute_single_task_workflow(
            raw_input=scheduled_request.task_input,
            priority=1
        )
    
    task_id = scheduler.add_scheduled_task(
        cron_expression=scheduled_request.cron_expression,
        task_function=task_function,
        task_name=scheduled_request.task_name
    )
    
    return {"task_id": task_id, "message": "Scheduled task created"}


@app.get("/api/scheduled-tasks", tags=["Scheduled Tasks"])
async def list_scheduled_tasks():
    """列出定时任务"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    return {
        "scheduled_tasks": scheduler.list_scheduled_tasks()
    }


@app.get("/api/system/status", tags=["System"])
async def get_system_status():
    """获取系统状态"""
    if not system_integrator or not performance_monitor:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    return {
        "system_status": system_integrator.get_system_status(),
        "performance_status": performance_monitor.get_overall_health_status(),
        "task_statistics": performance_monitor.get_task_performance_summary()
    }


@app.get("/api/metrics/summary", tags=["Monitoring"])
async def get_metrics_summary():
    """获取指标摘要"""
    if not metrics_collector:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    return metrics_collector.get_metrics_summary()


__all__ = ["app"]
