# Agent 永续自进化系统 - API 文档

## 📚 目录

1. [核心组件 API](#1-核心组件-api)
2. [存储后端 API](#2-存储后端-api)
3. [日志系统 API](#3-日志系统-api)
4. [任务管理 API](#4-任务管理-api)
5. [调度管理 API](#5-调度管理-api)
6. [学习系统 API](#6-学习系统-api)
7. [系统集成 API](#7-系统集成-api)

---

## 1. 核心组件 API

### 1.1 TaskWorkflowManagerComponent

任务工作流管理器组件

#### 初始化

```python
from agent_perpetual_evolution_system import TaskWorkflowManagerComponent

component = TaskWorkflowManagerComponent(
    storage_backend,  # CoreStorageInterfaceContract
    logger_backend    # CoreLoggerInterfaceContract
)
```

#### 方法

##### `create_new_task_workflow()`

创建新任务工作流

```python
task = component.create_new_task_workflow(
    raw_input_text: str,           # 任务输入文本
    priority_level: int = 1,       # 优先级（1-10）
    timeout_duration: int = None    # 超时时间（秒）
) -> object
```

**返回值**: 任务对象

**示例**:

```python
task = workflow_manager.create_new_task_workflow(
    raw_input_text="分析代码质量",
    priority_level=5,
    timeout_duration=300
)
print(f"创建任务: {task.task_id}")
```

##### `retrieve_task_by_identifier()`

根据 ID 获取任务

```python
task = component.retrieve_task_by_identifier(
    task_id: str  # 任务 ID
) -> Optional[object]
```

##### `list_all_pending_task_workflows()`

列出所有待处理任务

```python
tasks = component.list_all_pending_task_workflows(
    limit_count: int = 100  # 返回数量限制
) -> List[object]
```

##### `update_task_workflow_status()`

更新任务状态

```python
success = component.update_task_workflow_status(
    task_id: str,
    new_status: str,
    **additional_kwargs  # 其他属性
) -> bool
```

##### `get_task_workflow_statistics()`

获取任务统计信息

```python
stats = component.get_task_workflow_statistics() -> Dict[str, Any]
```

---

### 1.2 TaskAnalyzerPlannerComponent

任务分析规划器组件

#### 初始化

```python
component = TaskAnalyzerPlannerComponent(
    logger_backend  # CoreLoggerInterfaceContract
)
```

#### 方法

##### `analyze_and_generate_execution_plan()`

分析任务并生成执行计划

```python
execution_plan = component.analyze_and_generate_execution_plan(
    task_object  # 任务对象
) -> Dict[str, Any]
```

**返回值**:

```python
{
    'task_id': str,
    'identified_intent': str,
    'task_goal': str,
    'generated_subtasks': List[Dict],
    'execution_order_path': List[str],
    'dependencies_valid': bool
}
```

**示例**:

```python
plan = analyzer.analyze_and_generate_execution_plan(task)
print(f"子任务数: {len(plan['generated_subtasks'])}")
print(f"执行路径: {plan['execution_order_path']}")
```

---

### 1.3 TaskStepExecutorComponent

任务步骤执行器组件

#### 初始化

```python
component = TaskStepExecutorComponent(
    storage_backend,  # CoreStorageInterfaceContract
    logger_backend    # CoreLoggerInterfaceContract
)
```

#### 方法

##### `execute_task_execution_plan()`

执行任务执行计划

```python
result = component.execute_task_execution_plan(
    task_object,       # 任务对象
    execution_plan: Dict[str, Any]  # 执行计划
) -> Dict[str, Any]
```

**返回值**:

```python
{
    'success': bool,
    'subtask_execution_results': List[Dict],
    'total_steps_executed': int,
    'total_duration_seconds': float
}
```

---

## 2. 存储后端 API

### 2.1 CoreStorageInterfaceContract

核心存储接口契约（抽象基类）

#### 抽象方法

##### `save_single_task_record()`

保存单个任务记录

```python
success = storage.save_single_task_record(
    task  # 任务对象
) -> bool
```

##### `retrieve_task_by_identifier()`

根据 ID 检索任务

```python
task = storage.retrieve_task_by_identifier(
    task_id: str  # 任务 ID
)
```

##### `update_task_status_value()`

更新任务状态

```python
success = storage.update_task_status_value(
    task_id: str,
    new_status,
    **kwargs
) -> bool
```

##### `get_list_of_pending_tasks()`

获取待处理任务列表

```python
tasks = storage.get_list_of_pending_tasks(
    limit_count: int = 100
) -> List
```

##### `perform_health_check()`

执行健康检查

```python
health = storage.perform_health_check() -> Dict[str, Any]
```

### 2.2 MemoryBasedStorageAdapter

内存存储适配器

#### 初始化

```python
adapter = MemoryBasedStorageAdapter()
```

#### 方法

继承自 `CoreStorageInterfaceContract` 的所有方法

#### 示例

```python
from agent_perpetual_evolution_system import MemoryBasedStorageAdapter

storage = MemoryBasedStorageAdapter()

# 保存任务
task = create_task()
storage.save_single_task_record(task)

# 查询任务
task = storage.retrieve_task_by_identifier("task-123")

# 健康检查
health = storage.perform_health_check()
print(f"状态: {health['status']}")
```

### 2.3 StorageBackendFactoryBuilder

存储后端工厂构建器

#### 方法

##### `create_storage_backend_instance()`

创建存储后端实例

```python
storage = StorageBackendFactoryBuilder.create_storage_backend_instance(
    backend_type: str = "memory"  # 存储类型
) -> CoreStorageInterfaceContract
```

**示例**:

```python
# 创建内存存储
memory_storage = StorageBackendFactoryBuilder.create_storage_backend_instance("memory")

# 创建 SQLite 存储（如果实现了）
sqlite_storage = StorageBackendFactoryBuilder.create_storage_backend_instance("sqlite")
```

---

## 3. 日志系统 API

### 3.1 CoreLoggerInterfaceContract

核心日志接口契约（抽象基类）

#### 抽象方法

##### `log_information_message()`

记录信息日志

```python
logger.log_information_message(
    module_name: str,
    message_text: str,
    **kwargs
)
```

##### `log_warning_message()`

记录警告日志

```python
logger.log_warning_message(
    module_name: str,
    message_text: str,
    **kwargs
)
```

##### `log_error_message()`

记录错误日志

```python
logger.log_error_message(
    module_name: str,
    message_text: str,
    **kwargs
)
```

##### `log_debug_message()`

记录调试日志

```python
logger.log_debug_message(
    module_name: str,
    message_text: str,
    **kwargs
)
```

### 3.2 StructuredLoggerFrameworkImplementation

结构化日志框架实现

#### 初始化

```python
logger = StructuredLoggerFrameworkImplementation(
    app_name: str = "AgentSystem",      # 应用名称
    log_level: str = "INFO",           # 日志级别
    json_format: bool = True            # JSON 格式输出
)
```

#### 方法

继承自 `CoreLoggerInterfaceContract` 的所有方法

#### 示例

```python
from agent_perpetual_evolution_system import StructuredLoggerFrameworkImplementation

logger = StructuredLoggerFrameworkImplementation(
    app_name="MyApp",
    log_level="DEBUG"
)

logger.log_information_message(
    "TaskManager",
    "Task created successfully",
    task_id="123",
    priority=5
)

# 输出:
# {"module": "TaskManager", "event": "Task created successfully", "task_id": "123", "priority": 5, ...}
```

---

## 4. 任务管理 API

### 4.1 PriorityQueueManagerComponent

优先级队列管理器组件

#### 初始化

```python
component = PriorityQueueManagerComponent(
    logger_backend  # CoreLoggerInterfaceContract
)
```

#### 方法

##### `enqueue_task()`

将任务加入队列

```python
queue_item_id = component.enqueue_task(
    task_object,        # 任务对象
    priority_level: int = 1  # 优先级
) -> str
```

##### `dequeue_task()`

从队列取出任务

```python
task = component.dequeue_task() -> Optional[object]
```

##### `update_task_priority()`

更新任务优先级

```python
success = component.update_task_priority(
    queue_item_id: str,
    new_priority: int
) -> bool
```

##### `get_queue_statistics()`

获取队列统计

```python
stats = component.get_queue_statistics() -> Dict[str, Any]
```

##### `stop_queue_processing()`

停止队列处理

```python
component.stop_queue_processing()
```

#### 示例

```python
queue_manager = PriorityQueueManagerComponent(logger)

# 添加任务
task = create_task()
queue_id = queue_manager.enqueue_task(task, priority=3)

# 取出任务
next_task = queue_manager.dequeue_task()

# 获取统计
stats = queue_manager.get_queue_statistics()
print(f"队列大小: {stats['queue_size']}")
```

---

## 5. 调度管理 API

### 5.1 WorkflowModeCoordinatorComponent

工作流模式协调器组件

#### 初始化

```python
component = WorkflowModeCoordinatorComponent(
    logger_backend  # CoreLoggerInterfaceContract
)
```

#### 方法

##### `determine_optimal_execution_mode()`

确定最优执行模式

```python
mode = component.determine_optimal_execution_mode(
    task_metadata: Dict[str, Any]
) -> WorkflowExecutionMode
```

##### `switch_execution_mode()`

切换执行模式

```python
success = component.switch_execution_mode(
    new_mode: WorkflowExecutionMode
) -> bool
```

##### `get_current_execution_mode()`

获取当前执行模式

```python
mode = component.get_current_execution_mode() -> WorkflowExecutionMode
```

##### `get_mode_transition_history()`

获取模式转换历史

```python
history = component.get_mode_transition_history(
    limit: int = 10
) -> list
```

#### WorkflowExecutionMode 枚举

```python
from agent_perpetual_evolution_system import WorkflowExecutionMode

# 可用模式
WorkflowExecutionMode.SEQUENTIAL  # 顺序执行
WorkflowExecutionMode.PARALLEL    # 并行执行
WorkflowExecutionMode.ADAPTIVE    # 自适应执行
WorkflowExecutionMode.BATCH       # 批量执行
```

### 5.2 ExecutionCheckpointSaverComponent

执行检查点保存器组件

#### 初始化

```python
component = ExecutionCheckpointSaverComponent(
    storage_backend,  # CoreStorageInterfaceContract
    logger_backend    # CoreLoggerInterfaceContract
)
```

#### 方法

##### `save_execution_checkpoint()`

保存执行检查点

```python
checkpoint_id = component.save_execution_checkpoint(
    task_id: str,
    execution_state: Dict[str, Any],
    step_number: int,
    metadata: Dict[str, Any] = None
) -> str
```

##### `load_latest_checkpoint()`

加载最新检查点

```python
checkpoint = component.load_latest_checkpoint(
    task_id: str
) -> Optional[Dict[str, Any]]
```

##### `load_checkpoint_by_id()`

根据 ID 加载检查点

```python
checkpoint = component.load_checkpoint_by_id(
    checkpoint_id: str
) -> Optional[Dict[str, Any]]
```

##### `delete_checkpoint()`

删除检查点

```python
success = component.delete_checkpoint(
    checkpoint_id: str
) -> bool
```

##### `save_checkpoint()`

保存检查点（简单版）

```python
success = component.save_checkpoint() -> bool
```

---

## 6. 学习系统 API

### 6.1 ExperienceLearningManagerComponent

经验学习管理器组件

#### 初始化

```python
component = ExperienceLearningManagerComponent(
    storage_backend,  # CoreStorageInterfaceContract
    logger_backend    # CoreLoggerInterfaceContract
)
```

#### 方法

##### `record_execution_experience()`

记录执行经验

```python
experience_id = component.record_execution_experience(
    task_id: str,
    execution_result: Dict[str, Any],
    execution_plan: Dict[str, Any],
    metadata: Dict[str, Any] = None
) -> str
```

##### `extract_and_store_experience()`

提取并存储经验

```python
experience = component.extract_and_store_experience(
    task_id: str,
    execution_result: Dict[str, Any]
) -> Optional[Dict[str, Any]]
```

##### `find_similar_execution_experiences()`

查找相似的执行经验

```python
similar = component.find_similar_execution_experiences(
    task_metadata: Dict[str, Any],
    limit: int = 5
) -> List[Dict[str, Any]]
```

##### `get_learning_insights()`

获取学习洞察

```python
insights = component.get_learning_insights() -> Dict[str, Any]
```

##### `get_experience_by_id()`

根据 ID 获取经验

```python
experience = component.get_experience_by_id(
    experience_id: str
) -> Optional[Dict[str, Any]]
```

#### 示例

```python
learning_manager = ExperienceLearningManagerComponent(storage, logger)

# 记录经验
exp_id = learning_manager.record_execution_experience(
    task_id="task-123",
    execution_result={'success': True, 'duration': 1.5},
    execution_plan={'steps': ['analyze', 'execute', 'verify']}
)

# 获取洞察
insights = learning_manager.get_learning_insights()
print(f"总经验数: {insights['total_experiences']}")
print(f"成功率: {insights['success_rate']}")

# 查找相似经验
similar = learning_manager.find_similar_execution_experiences(
    {'task_type': 'analysis'},
    limit=3
)
```

---

### 6.2 FeedbackGenerationReporterComponent

反馈生成报告器组件

#### 初始化

```python
component = FeedbackGenerationReporterComponent(
    logger_backend  # CoreLoggerInterfaceContract
)
```

#### 方法

##### `generate_execution_feedback()`

生成执行反馈

```python
feedback = component.generate_execution_feedback(
    task_id: str,
    execution_result: Dict[str, Any],
    execution_plan: Dict[str, Any]
) -> Dict[str, Any]
```

##### `generate_improvement_suggestions()`

生成改进建议

```python
suggestions = component.generate_improvement_suggestions(
    execution_data: Dict[str, Any]
) -> List[str]
```

##### `generate_performance_report()`

生成性能报告

```python
report = component.generate_performance_report(
    task_id: str,
    metrics: Dict[str, Any]
) -> Dict[str, Any]
```

---

## 7. 系统集成 API

### 7.1 SystemIntegratorComponent

系统集成器组件（主入口）

#### 初始化

```python
system = SystemIntegratorComponent(
    custom_storage=None,  # 可选：自定义存储后端
    custom_logger=None    # 可选：自定义日志后端
)
```

#### 方法

##### `execute_single_task_workflow()`

执行单个任务工作流

```python
result = system.execute_single_task_workflow(
    raw_input: str,
    priority: int = 1
) -> Dict[str, Any]
```

**返回值**:

```python
{
    'task_id': str,
    'execution_result': {
        'success': bool,
        'subtask_execution_results': List[Dict],
        'total_steps_executed': int,
        'total_duration_seconds': float
    },
    'experience': List[Dict]
}
```

##### `get_system_status()`

获取系统状态

```python
status = system.get_system_status() -> Dict[str, Any]
```

**返回值**:

```python
{
    'initialized': bool,
    'version': str,
    'components': {
        'storage_backend': {...},
        'workflow_mode_coordinator': {...},
        'priority_queue': {...}
    }
}
```

##### `shutdown_system()`

关闭系统

```python
system.shutdown_system()
```

#### 属性

##### `task_workflow_manager`

任务工作流管理器

```python
workflow_manager = system.task_workflow_manager  # TaskWorkflowManagerComponent
```

##### `task_analyzer_planner`

任务分析规划器

```python
analyzer = system.task_analyzer_planner  # TaskAnalyzerPlannerComponent
```

##### `task_step_executor`

任务步骤执行器

```python
executor = system.task_step_executor  # TaskStepExecutorComponent
```

##### `priority_queue_manager`

优先级队列管理器

```python
queue_manager = system.priority_queue_manager  # PriorityQueueManagerComponent
```

##### `experience_learning_manager`

经验学习管理器

```python
learning_manager = system.experience_learning_manager  # ExperienceLearningManagerComponent
```

#### 示例

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

# 初始化系统
system = SystemIntegratorComponent()

# 执行任务
result = system.execute_single_task_workflow(
    raw_input="分析项目代码质量",
    priority=5
)

print(f"任务ID: {result['task_id']}")
print(f"成功: {result['execution_result']['success']}")
print(f"执行步骤: {result['execution_result']['total_steps_executed']}")
print(f"经验数: {len(result['experience'])}")

# 获取系统状态
status = system.get_system_status()
print(f"版本: {status['version']}")
print(f"初始化: {status['initialized']}")

# 关闭系统
system.shutdown_system()
```

---

## 配置 API

### ApplicationGlobalSettings

应用程序全局设置

#### 初始化

```python
from agent_perpetual_evolution_system import ApplicationGlobalSettings

settings = ApplicationGlobalSettings(
    APPLICATION_NAME="MyApp",
    DEBUG_MODE_ENABLED=True,
    LOGGING_LEVEL="DEBUG"
)
```

#### 获取单例

```python
from agent_perpetual_evolution_system import get_application_global_settings

settings = get_application_global_settings()
```

#### 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `APPLICATION_NAME` | str | "Agent Evolution System" | 应用名称 |
| `APPLICATION_VERSION` | str | "3.0.0" | 应用版本 |
| `DEBUG_MODE_ENABLED` | bool | False | 调试模式 |
| `API_SERVER_HOST` | str | "0.0.0.0" | API 主机 |
| `API_SERVER_PORT` | int | 8000 | API 端口 |
| `STORAGE_BACKEND_TYPE` | str | "memory" | 存储类型 |
| `DATABASE_FILE_PATH` | str | "data/agent_system.db" | 数据库路径 |
| `LOGGING_LEVEL` | str | "INFO" | 日志级别 |
| `LOG_TO_FILE_ENABLED` | bool | False | 日志文件输出 |
| `LOG_FILE_PATH` | str | "logs/agent_system.log" | 日志文件路径 |

---

## 异常类 API

### 自定义异常

所有异常类都继承自 `AgentEvolutionSystemException`

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import (
    AgentEvolutionSystemException,
    StorageException,
    TaskWorkflowException,
    TaskAnalysisException,
    TaskExecutionException,
    SchedulerException,
    ConfigurationException,
    ValidationException,
    LearningException,
    CheckpointException,
)
```

#### 使用示例

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import TaskWorkflowException

try:
    # 执行任务操作
    pass
except TaskWorkflowException as e:
    print(f"任务工作流错误: {e.message}")
    print(f"任务ID: {e.task_id}")
    print(f"错误码: {e.error_code}")
```

---

## 工具函数 API

### 错误处理工具

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import (
    handle_exceptions,
    safe_execute,
    validate_and_raise,
    ErrorContext,
    RetryExecutor,
)
```

#### 示例

```python
from agent_perpetual_evolution_system.common_utilities_and_helpers import handle_exceptions

@handle_exceptions(default_return=None, log_errors=True)
def risky_function(x):
    # 可能抛出异常的操作
    return 10 / x

# 使用
result = risky_function(0)  # 返回 None，不会崩溃
```

---

**API 文档版本**: 3.0.0  
**最后更新**: 2026-05-16
