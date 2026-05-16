"""
Phase 3 Integration Test - 第三阶段集成测试
验证异步任务、调度、监控等新功能
"""

import sys
import asyncio
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_perpetual_evolution_system import SystemIntegratorComponent
from agent_perpetual_evolution_system.business_domain_layer.async_task_processing_components import (
    AsyncTaskQueue,
    AsyncTaskExecutor,
    AsyncTaskWorkflowManager
)
from agent_perpetual_evolution_system.business_domain_layer.schedule_management_components import (
    SimpleScheduledTaskScheduler
)
from agent_perpetual_evolution_system.performance_monitoring_and_metrics import (
    SystemPerformanceMonitor,
    SimplePrometheusClient,
    SystemMetricsCollector
)


def test_async_task_framework():
    """测试异步任务框架"""
    print("\n" + "="*60)
    print("🧪 测试异步任务框架")
    print("="*60)
    
    try:
        queue = AsyncTaskQueue()
        print(f"✓ 异步任务队列创建成功")
        
        executor = AsyncTaskExecutor()
        print(f"✓ 异步任务执行器创建成功")
        
        print(f"\n✅ 异步任务框架测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 异步任务框架测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scheduled_task_scheduler():
    """测试定时任务调度器"""
    print("\n" + "="*60)
    print("🧪 测试定时任务调度器")
    print("="*60)
    
    try:
        scheduler = SimpleScheduledTaskScheduler()
        print(f"✓ 定时任务调度器创建成功")
        
        # 添加一个简单任务
        task_id = scheduler.add_scheduled_task(
            cron_expression="* * * * *",
            task_function=lambda: print("Scheduled task executed"),
            task_name="test-task"
        )
        print(f"✓ 定时任务添加成功: {task_id}")
        
        # 立即触发任务
        result = scheduler.trigger_task_now(task_id)
        print(f"✓ 定时任务立即触发成功: {result['success']}")
        
        # 列出任务
        tasks = scheduler.list_scheduled_tasks()
        print(f"✓ 列出 {len(tasks)} 个定时任务")
        
        # 获取执行历史
        history = scheduler.get_execution_history()
        print(f"✓ 执行历史: {len(history)} 条")
        
        # 获取状态
        status = scheduler.get_scheduler_status()
        print(f"✓ 调度器状态: {status}")
        
        print(f"\n✅ 定时任务调度器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 定时任务调度器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prometheus_monitoring():
    """测试 Prometheus 监控集成"""
    print("\n" + "="*60)
    print("🧪 测试 Prometheus 监控")
    print("="*60)
    
    try:
        prometheus = SimplePrometheusClient()
        print(f"✓ Prometheus 客户端创建成功")
        
        metrics_collector = SystemMetricsCollector(prometheus)
        print(f"✓ 指标收集器创建成功")
        
        # 记录一些指标
        prometheus.increment_counter("test_counter", {}, 1)
        prometheus.set_gauge("test_gauge", 1.0)
        prometheus.observe_histogram("test_histogram", 0.1)
        print(f"✓ 指标记录成功")
        
        # 记录任务执行
        metrics_collector.record_task_execution("test", True, 0.5)
        print(f"✓ 任务执行指标记录成功")
        
        # 记录队列深度
        metrics_collector.record_queue_depth(10)
        print(f"✓ 队列深度记录成功")
        
        # 获取指标
        metrics = prometheus.get_metrics()
        print(f"✓ 获取指标成功: {len(metrics['counters'])} counters")
        
        # 获取指标摘要
        summary = metrics_collector.get_metrics_summary()
        print(f"✓ 指标摘要: {summary}")
        
        # 格式化为 Prometheus 文本
        prometheus_text = prometheus.format_prometheus_text()
        print(f"✓ Prometheus 文本格式成功: {len(prometheus_text)} chars")
        
        print(f"\n✅ Prometheus 监控测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Prometheus 监控测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance_monitoring():
    """测试性能监控"""
    print("\n" + "="*60)
    print("🧪 测试性能监控")
    print("="*60)
    
    try:
        monitor = SystemPerformanceMonitor()
        print(f"✓ 性能监控器创建成功")
        
        # 记录任务执行
        monitor.record_task_execution("test-1", 0.1, True)
        monitor.record_task_execution("test-2", 0.2, True)
        monitor.record_task_execution("test-3", 0.3, False)
        print(f"✓ 任务执行记录成功")
        
        # 获取任务性能摘要
        task_summary = monitor.get_task_performance_summary()
        print(f"✓ 任务性能摘要: {task_summary}")
        
        # 获取系统指标
        system_metrics = monitor.collect_system_metrics()
        print(f"✓ 系统指标收集成功: {len(system_metrics)} keys")
        
        # 获取健康状态
        health = monitor.get_overall_health_status()
        print(f"✓ 健康状态: {health['status']}")
        
        print(f"\n✅ 性能监控测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 性能监控测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_integration():
    """测试系统集成"""
    print("\n" + "="*60)
    print("🧪 测试系统集成")
    print("="*60)
    
    try:
        system = SystemIntegratorComponent()
        print(f"✓ 系统集成器初始化成功")
        
        # 执行任务
        result = system.execute_single_task_workflow("Integration test", priority=5)
        print(f"✓ 任务执行成功: {result['execution_result']['success']}")
        
        # 获取系统状态
        status = system.get_system_status()
        print(f"✓ 系统状态获取成功: {status['initialized']}")
        
        # 关闭系统
        system.shutdown_system()
        print(f"✓ 系统关闭成功")
        
        print(f"\n✅ 系统集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 系统集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 Agent 永续自进化系统 - 第三阶段测试")
    print("="*60)
    
    tests = []
    
    tests.append(("异步任务框架", test_async_task_framework()))
    tests.append(("定时任务调度器", test_scheduled_task_scheduler()))
    tests.append(("Prometheus 监控", test_prometheus_monitoring()))
    tests.append(("性能监控", test_performance_monitoring()))
    tests.append(("系统集成", test_system_integration()))
    
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    for test_name, test_passed in tests:
        status = "✅ 通过" if test_passed else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    total = len(tests)
    passed = sum(1 for _, p in tests if p)
    
    print(f"\n🎯 总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统第三阶段实施成功！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查")
        return 1


if __name__ == "__main__":
    sys.exit(main())
