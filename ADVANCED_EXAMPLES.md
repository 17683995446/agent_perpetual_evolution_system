# Agent 永续自进化系统 - 高级使用示例

## 📚 示例目录

1. [基础任务处理](#1-基础任务处理)
2. [使用 SQLite 持久化](#2-使用-sqlite-持久化)
3. [性能监控示例](#3-性能监控示例)
4. [错误处理最佳实践](#4-错误处理最佳实践)
5. [自定义存储后端](#5-自定义存储后端)
6. [批量任务处理](#6-批量任务处理)
7. [高级配置验证](#7-高级配置验证)
8. [组件组合使用](#8-组件组合使用)

---

## 1. 基础任务处理

### 示例 1.1: 最简单的使用

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

# 初始化系统
system = SystemIntegratorComponent()

# 执行任务
result = system.execute_single_task_workflow(
    raw_input="分析项目代码质量",
    priority=5
)

print(f"✅ 任务完成!")
print(f"   任务ID: {result['task_id']}")
print(f"   成功: {result['execution_result']['success']}")
print(f"   执行时间: {result['execution_result']['total_duration_seconds']:.3f}秒")

# 关闭系统
system.shutdown_system()
```

### 示例 1.2: 批量任务处理

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 定义任务列表
tasks = [
    {"input": "代码审查", "priority": 5},
    {"input": "性能分析", "priority": 4},
    {"input": "安全扫描", "priority": 3},
    {"input": "文档生成", "priority": 2},
]

# 执行批量任务
results = []
for task in tasks:
    result = system.execute_single_task_workflow(
        raw_input=task["input"],
        priority=task["priority"]
    )
    results.append(result)
    print(f"✅ {task['input']}: {result['task_id'][:8]}...")

# 统计结果
successful = sum(1 for r in results if r['execution_result']['success'])
failed = len(results) - successful

print(f"\n📊 统计结果:")
print(f"   总任务数: {len(results)}")
print(f"   成功: {successful}")
print(f"   失败: {failed}")
print(f"   成功率: {successful/len(results)*100:.1f}%")

system.shutdown_system()
```

---

## 2. 使用 SQLite 持久化

### 示例 2.1: 启用 SQLite 存储

```python
import os
from agent_perpetual_evolution_system import SystemIntegratorComponent

# 设置环境变量
os.environ['STORAGE_BACKEND_TYPE'] = 'sqlite'

# 初始化系统（自动使用 SQLite）
system = SystemIntegratorComponent()

# 执行任务
result = system.execute_single_task_workflow(
    raw_input="使用 SQLite 持久化存储",
    priority=5
)

# 检查存储健康
health = system.storage_backend.perform_health_check()
print(f"\n📦 存储状态:")
print(f"   类型: {health['storage_type']}")
print(f"   总任务: {health['total_tasks']}")
print(f"   待处理: {health['pending_tasks']}")
print(f"   已完成: {health['completed_tasks']}")
print(f"   总经验: {health['total_experiences']}")

system.shutdown_system()
```

### 示例 2.2: 直接使用 SQLite 存储

```python
from agent_perpetual_evolution_system.infrastructure_adapter_layer import SQLiteBasedStorageAdapter

# 创建 SQLite 存储
storage = SQLiteBasedStorageAdapter(
    database_path="data/my_app.db"
)

# 创建任务
class MockTask:
    task_id = "test-123"
    raw_input = "Test task"
    priority = 1
    status = "PENDING"

# 保存任务
task = MockTask()
success = storage.save_single_task_record(task)
print(f"任务保存: {'成功' if success else '失败'}")

# 检索任务
retrieved = storage.retrieve_task_by_identifier("test-123")
print(f"任务检索: {retrieved is not None}")

# 健康检查
health = storage.perform_health_check()
print(f"健康状态: {health['status']}")

storage.close()
```

---

## 3. 性能监控示例

### 示例 3.1: 启用性能监控

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent
from agent_perpetual_evolution_system.performance_monitoring_and_metrics import SystemPerformanceMonitor

# 创建性能监控器
monitor = SystemPerformanceMonitor()

# 初始化系统
system = SystemIntegratorComponent()

# 执行多个任务
tasks = [f"Task {i}" for i in range(10)]
for task_input in tasks:
    result = system.execute_single_task_workflow(task_input, priority=3)

# 获取性能摘要
task_perf = monitor.get_task_performance_summary()
print(f"\n📊 任务性能:")
print(f"   总任务: {task_perf['total_tasks']}")
print(f"   成功: {task_perf['successful_tasks']}")
print(f"   失败: {task_perf['failed_tasks']}")
print(f"   成功率: {task_perf['success_rate']*100:.1f}%")
print(f"   平均执行时间: {task_perf['average_duration']*1000:.2f}ms")

# 获取组件性能
component_perf = monitor.get_component_performance_summary()
print(f"\n🔧 组件性能:")
for component, perf in component_perf.items():
    print(f"   {component}:")
    print(f"      调用次数: {perf['call_count']}")
    print(f"      平均时间: {perf['average_duration']*1000:.2f}ms")

# 获取健康状态
health = monitor.get_overall_health_status()
print(f"\n🏥 健康状态: {health['status']}")
print(f"   健康分数: {health['health_score']:.1f}")

system.shutdown_system()
```

### 示例 3.2: 使用性能上下文管理器

```python
from agent_perpetual_evolution_system.performance_monitoring_and_metrics import (
    SystemPerformanceMonitor,
    PerformanceMetricsContext
)

# 创建监控器
monitor = SystemPerformanceMonitor()

# 使用上下文管理器自动记录性能
with PerformanceMetricsContext(monitor, "database_operation", "task-123", "io") as ctx:
    # 模拟数据库操作
    import time
    time.sleep(0.1)
    
    # 如果发生异常，会自动记录为失败
    # ctx.success = False

print(f"✅ 操作完成")
print(f"   执行时间: {ctx.duration*1000:.2f}ms")
print(f"   成功: {ctx.success}")

# 获取性能摘要
perf = monitor.get_task_performance_summary()
print(f"   任务成功率: {perf['success_rate']*100:.1f}%")
```

---

## 4. 错误处理最佳实践

### 示例 4.1: 使用异常处理装饰器

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import (
    handle_exceptions,
    TaskWorkflowException
)

@handle_exceptions(default_return=None, log_errors=True)
def risky_task_operation(task_id, user_input):
    if not task_id:
        raise TaskWorkflowException(
            message="Task ID is required",
            task_id=None
        )
    
    if not user_input:
        raise ValueError("User input cannot be empty")
    
    # 业务逻辑
    return {"status": "success", "task_id": task_id}

# 调用
result = risky_task_operation(None, "test")
print(f"结果: {result}")  # None，不会崩溃

result = risky_task_operation("123", "test")
print(f"结果: {result}")  # {"status": "success", "task_id": "123"}
```

### 示例 4.2: 使用验证工具

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import (
    validate_and_raise,
    ValidationException
)

def create_user(username, age, email):
    # 验证用户名
    validate_and_raise(
        len(username) >= 3,
        ValidationException,
        "Username must be at least 3 characters",
        field_name="username"
    )
    
    # 验证年龄
    validate_and_raise(
        0 < age < 150,
        ValidationException,
        "Age must be between 0 and 150",
        field_name="age"
    )
    
    # 验证邮箱
    validate_and_raise(
        "@" in email and "." in email,
        ValidationException,
        "Invalid email format",
        field_name="email"
    )
    
    return {"username": username, "age": age, "email": email}

# 测试
try:
    user = create_user("john", 25, "john@example.com")
    print(f"✅ 用户创建成功: {user}")
except ValidationException as e:
    print(f"❌ 验证失败: {e.message}")
```

### 示例 4.3: 使用错误上下文管理器

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import ErrorContext

def process_data(data):
    with ErrorContext("data_processing", log_errors=True) as ctx:
        # 可能失败的操作
        result = some_operation(data)
        
        if result is None:
            raise ValueError("Operation returned None")
        
        # 更多操作
        final_result = another_operation(result)
        
        return final_result

# 使用
try:
    result = process_data("test")
    print(f"✅ 处理成功: {result}")
except Exception as e:
    print(f"❌ 处理失败: {e}")
```

---

## 5. 自定义存储后端

### 示例 5.1: 实现自定义存储

```python
from agent_perpetual_evolution_system import CoreStorageInterfaceContract
from typing import Dict, Any, List

class CustomStorageAdapter(CoreStorageInterfaceContract):
    """自定义存储适配器"""
    
    def __init__(self):
        self.storage = {}  # 使用字典作为存储
    
    def save_single_task_record(self, task) -> bool:
        self.storage[task.task_id] = task
        return True
    
    def retrieve_task_by_identifier(self, task_id: str):
        return self.storage.get(task_id)
    
    def update_task_status_value(self, task_id: str, new_status, **kwargs) -> bool:
        if task_id in self.storage:
            self.storage[task_id].status = new_status
            return True
        return False
    
    def get_list_of_pending_tasks(self, limit_count: int = 100) -> List:
        return [
            task for task in self.storage.values()
            if task.status in ('PENDING', 'RUNNING')
        ][:limit_count]
    
    def perform_health_check(self) -> Dict[str, Any]:
        return {
            'status': 'healthy',
            'storage_type': 'custom',
            'total_tasks': len(self.storage)
        }

# 使用自定义存储
from agent_perpetual_evolution_system import SystemIntegratorComponent

storage = CustomStorageAdapter()
system = SystemIntegratorComponent(custom_storage=storage)

result = system.execute_single_task_workflow(
    raw_input="使用自定义存储",
    priority=5
)

print(f"✅ 任务执行成功: {result['task_id']}")

system.shutdown_system()
```

---

## 6. 批量任务处理

### 示例 6.1: 并行任务处理

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent
import concurrent.futures

system = SystemIntegratorComponent()

def execute_task(task_input):
    return system.execute_single_task_workflow(task_input, priority=3)

# 定义任务
tasks = [f"Task {i}" for i in range(20)]

# 使用线程池并行执行
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(execute_task, task) for task in tasks]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

# 统计结果
successful = sum(1 for r in results if r['execution_result']['success'])
print(f"✅ 并行处理完成:")
print(f"   总任务: {len(results)}")
print(f"   成功: {successful}")
print(f"   成功率: {successful/len(results)*100:.1f}%")

system.shutdown_system()
```

### 示例 6.2: 优先级任务队列

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 创建不同优先级的任务
tasks_with_priority = [
    ("紧急修复 bug", 10),      # 最高优先级
    ("重要功能开发", 8),
    ("普通优化", 5),
    ("文档完善", 3),           # 最低优先级
]

# 按优先级顺序执行
for task_input, priority in tasks_with_priority:
    result = system.execute_single_task_workflow(task_input, priority)
    print(f"✅ [{priority}] {task_input}: {result['task_id'][:8]}...")

# 查看队列状态
queue_stats = system.priority_queue_manager.get_queue_statistics()
print(f"\n📊 队列状态: {queue_stats}")

system.shutdown_system()
```

---

## 7. 高级配置验证

### 示例 7.1: 配置模式验证

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import (
    ConfigurationValidator,
    validate_configuration
)

# 定义配置模式
schema = {
    'APP_NAME': {
        'required': True,
        'type': str
    },
    'MAX_WORKERS': {
        'required': True,
        'type': int,
        'min': 1,
        'max': 100
    },
    'DEBUG_MODE': {
        'required': False,
        'type': bool
    },
    'LOG_LEVEL': {
        'required': True,
        'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    }
}

# 测试配置
valid_config = {
    'APP_NAME': 'MyApp',
    'MAX_WORKERS': 10,
    'DEBUG_MODE': True,
    'LOG_LEVEL': 'INFO'
}

invalid_config = {
    'MAX_WORKERS': 200,  # 超出范围
    'LOG_LEVEL': 'INVALID'  # 无效选项
}

# 验证配置
is_valid, errors = validate_configuration(valid_config, schema)
print(f"有效配置: {is_valid}")

is_valid, errors = validate_configuration(invalid_config, schema)
print(f"无效配置: {not is_valid}")
if errors:
    for error in errors:
        print(f"   ❌ {error.message}")
```

### 示例 7.2: 类型安全包装器

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import TypeSafeWrapper

# 测试各种类型转换
test_values = [
    ("123", int, 123),
    ("45.67", float, 45.67),
    ("true", bool, True),
    ("0", bool, False),
    (None, str, "default"),
]

for value, target_type, expected in test_values:
    if target_type == int:
        result = TypeSafeWrapper.to_int(value)
    elif target_type == float:
        result = TypeSafeWrapper.to_float(value)
    elif target_type == bool:
        result = TypeSafeWrapper.to_bool(value)
    else:
        result = TypeSafeWrapper.to_string(value)
    
    status = "✅" if result == expected else "❌"
    print(f"{status} {target_type.__name__}({value!r}) = {result!r} (期望: {expected!r})")
```

---

## 8. 组件组合使用

### 示例 8.1: 直接使用组件

```python
from agent_perpetual_evolution_system import (
    TaskWorkflowManagerComponent,
    TaskAnalyzerPlannerComponent,
    TaskStepExecutorComponent,
    MemoryBasedStorageAdapter,
    StructuredLoggerFrameworkImplementation
)

# 创建存储和日志
storage = MemoryBasedStorageAdapter()
logger = StructuredLoggerFrameworkImplementation(app_name="MyApp")

# 创建组件
workflow_manager = TaskWorkflowManagerComponent(storage, logger)
analyzer = TaskAnalyzerPlannerComponent(logger)
executor = TaskStepExecutorComponent(storage, logger)

# 直接使用组件
task = workflow_manager.create_new_task_workflow(
    raw_input_text="自定义工作流",
    priority_level=5
)
print(f"✅ 任务创建: {task.task_id}")

plan = analyzer.analyze_and_generate_execution_plan(task)
print(f"📋 执行计划: {len(plan['generated_subtasks'])} 个子任务")

result = executor.execute_task_execution_plan(task, plan)
print(f"🎯 执行结果: {'成功' if result['success'] else '失败'}")
```

### 示例 8.2: 组件生命周期管理

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 获取系统状态
status = system.get_system_status()
print(f"🚀 系统版本: {status['version']}")
print(f"📦 初始化状态: {status['initialized']}")

# 执行任务
result = system.execute_single_task_workflow(
    raw_input="测试组件生命周期",
    priority=5
)

# 再次获取状态
new_status = system.get_system_status()
print(f"📈 任务统计: {new_status['components']['priority_queue']['total_queued']} 个待处理")

# 优雅关闭
system.shutdown_system()
print(f"✅ 系统已关闭")
```

---

## 🎓 更多资源

- [快速开始指南](./QUICKSTART.md) - 5分钟快速上手
- [API 文档](./API_DOCUMENTATION.md) - 完整的 API 参考
- [项目 README](./README.md) - 项目概述

---

**版本**: 3.0.0  
**最后更新**: 2026-05-16
