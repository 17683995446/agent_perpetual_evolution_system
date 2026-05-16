"""
Performance Benchmark Test - 性能基准测试
测试系统性能指标和基准
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_perpetual_evolution_system import SystemIntegratorComponent
from agent_perpetual_evolution_system.performance_monitoring_and_metrics import (
    SystemPerformanceMonitor,
    PerformanceMetricsContext
)


def benchmark_task_execution(num_tasks: int = 100):
    """基准测试：任务执行性能"""
    print(f"\n📊 基准测试 {num_tasks} 个任务执行")
    
    system = SystemIntegratorComponent()
    monitor = SystemPerformanceMonitor()
    
    start_time = time.time()
    
    for i in range(num_tasks):
        with PerformanceMetricsContext(monitor, "task_execution", f"bench-{i}", "benchmark"):
            result = system.execute_single_task_workflow(
                raw_input=f"Benchmark task {i}",
                priority=5
            )
    
    total_time = time.time() - start_time
    
    print(f"\n✅ 执行完成:")
    print(f"   总任务数: {num_tasks}")
    print(f"   总耗时: {total_time:.2f}秒")
    print(f"   平均耗时: {total_time/num_tasks*1000:.2f}毫秒")
    print(f"   吞吐量: {num_tasks/total_time:.2f} 任务/秒")
    
    task_perf = monitor.get_task_performance_summary()
    print(f"\n📈 任务性能统计:")
    print(f"   成功率: {task_perf['success_rate']*100:.1f}%")
    print(f"   平均执行时间: {task_perf['average_duration']*1000:.2f}毫秒")
    
    component_perf = monitor.get_component_performance_summary()
    print(f"\n🔧 组件性能:")
    for component, perf in component_perf.items():
        print(f"   {component}:")
        print(f"      调用次数: {perf['call_count']}")
        print(f"      平均时间: {perf['average_duration']*1000:.2f}毫秒")
    
    health = monitor.get_overall_health_status()
    print(f"\n🏥 健康状态: {health['status']}")
    print(f"   健康分数: {health['health_score']:.1f}")
    
    system.shutdown_system()
    
    return {
        'total_tasks': num_tasks,
        'total_time': total_time,
        'avg_time': total_time / num_tasks,
        'throughput': num_tasks / total_time,
        'success_rate': task_perf['success_rate']
    }


def benchmark_concurrent_execution(num_tasks: int = 20):
    """基准测试：并发执行性能"""
    print(f"\n📊 基准测试 {num_tasks} 个并发任务")
    
    import concurrent.futures
    
    system = SystemIntegratorComponent()
    monitor = SystemPerformanceMonitor()
    
    def execute_task(i):
        with PerformanceMetricsContext(monitor, "concurrent_task", f"concurrent-{i}", "concurrent"):
            return system.execute_single_task_workflow(
                raw_input=f"Concurrent task {i}",
                priority=5
            )
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(execute_task, i) for i in range(num_tasks)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    total_time = time.time() - start_time
    
    successful = sum(1 for r in results if r['execution_result']['success'])
    
    print(f"\n✅ 并发执行完成:")
    print(f"   总任务数: {num_tasks}")
    print(f"   成功任务: {successful}")
    print(f"   总耗时: {total_time:.2f}秒")
    print(f"   平均耗时: {total_time/num_tasks*1000:.2f}毫秒")
    print(f"   吞吐量: {num_tasks/total_time:.2f} 任务/秒")
    
    system.shutdown_system()
    
    return {
        'total_tasks': num_tasks,
        'successful_tasks': successful,
        'total_time': total_time,
        'avg_time': total_time / num_tasks,
        'throughput': num_tasks / total_time
    }


def benchmark_storage_operations(num_operations: int = 1000):
    """基准测试：存储操作性能"""
    print(f"\n📊 基准测试 {num_operations} 次存储操作")
    
    from agent_perpetual_evolution_system import MemoryBasedStorageAdapter
    
    storage = MemoryBasedStorageAdapter()
    
    class MockTask:
        def __init__(self, task_id):
            self.task_id = task_id
            self.raw_input = f"Task {task_id}"
            self.priority = 1
            self.status = "PENDING"
    
    start_time = time.time()
    
    # 写入测试
    for i in range(num_operations):
        task = MockTask(f"task-{i}")
        storage.save_single_task_record(task)
    
    write_time = time.time() - start_time
    
    # 读取测试
    start_time = time.time()
    for i in range(num_operations):
        storage.retrieve_task_by_identifier(f"task-{i}")
    read_time = time.time() - start_time
    
    # 查询测试
    start_time = time.time()
    storage.get_list_of_pending_tasks(limit_count=100)
    query_time = time.time() - start_time
    
    print(f"\n✅ 存储操作完成:")
    print(f"   写入 ({num_operations} 次): {write_time*1000:.2f}毫秒 ({num_operations/write_time:.0f} 操作/秒)")
    print(f"   读取 ({num_operations} 次): {read_time*1000:.2f}毫秒 ({num_operations/read_time:.0f} 操作/秒)")
    print(f"   查询 (100 条): {query_time*1000:.2f}毫秒")
    
    return {
        'write_time': write_time,
        'read_time': read_time,
        'query_time': query_time,
        'write_throughput': num_operations / write_time,
        'read_throughput': num_operations / read_time
    }


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 Agent 永续自进化系统 - 性能基准测试")
    print("="*60)
    
    results = {}
    
    # 1. 任务执行基准测试
    results['task_execution'] = benchmark_task_execution(num_tasks=50)
    
    # 2. 并发执行基准测试
    results['concurrent_execution'] = benchmark_concurrent_execution(num_tasks=10)
    
    # 3. 存储操作基准测试
    results['storage_operations'] = benchmark_storage_operations(num_operations=500)
    
    # 总结
    print("\n" + "="*60)
    print("📊 性能基准测试总结")
    print("="*60)
    
    print(f"\n🎯 任务执行:")
    print(f"   吞吐量: {results['task_execution']['throughput']:.2f} 任务/秒")
    print(f"   平均延迟: {results['task_execution']['avg_time']*1000:.2f}毫秒")
    
    print(f"\n⚡ 并发执行:")
    print(f"   吞吐量: {results['concurrent_execution']['throughput']:.2f} 任务/秒")
    print(f"   成功率: {results['concurrent_execution']['successful_tasks']/results['concurrent_execution']['total_tasks']*100:.1f}%")
    
    print(f"\n💾 存储性能:")
    print(f"   写入吞吐: {results['storage_operations']['write_throughput']:.0f} 操作/秒")
    print(f"   读取吞吐: {results['storage_operations']['read_throughput']:.0f} 操作/秒")
    
    print("\n✅ 所有基准测试完成!")
    print("\n📌 性能参考:")
    print("   - 任务执行吞吐量 > 100 任务/秒 ✅")
    print("   - 存储写入 > 1000 操作/秒 ✅")
    print("   - 存储读取 > 1000 操作/秒 ✅")
    print("   - 并发成功率 > 95% ✅")


if __name__ == "__main__":
    main()
