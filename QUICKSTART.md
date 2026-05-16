# Agent 永续自进化系统 - 快速启动指南

## 📦 安装

### 基础安装

```bash
pip install -e .
```

### 完整安装（包含 API 和开发工具）

```bash
pip install -e ".[all]"
```

### 仅安装核心依赖

```bash
pip install pydantic>=2.0.0 pydantic-settings>=2.0.0 structlog>=23.0.0
```

## 🚀 快速开始

### 1. 基础使用

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

# 初始化系统
system = SystemIntegratorComponent()

# 执行单个任务
result = system.execute_single_task_workflow(
    raw_input="分析项目代码结构",
    priority=1
)

print(f"任务ID: {result['task_id']}")
print(f"执行结果: {result['execution_result']}")

# 获取系统状态
status = system.get_system_status()
print(f"系统状态: {status}")

# 关闭系统
system.shutdown_system()
```

### 2. 使用 API 服务器

```python
from agent_perpetual_evolution_system.api_presentation_layer import fastapi_application

# 启动 API 服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_application, host="0.0.0.0", port=8000)
```

API 端点：

- `GET /health` - 健康检查
- `POST /tasks` - 创建新任务
- `GET /tasks/{task_id}` - 获取任务状态
- `GET /tasks` - 列出所有任务
- `GET /status` - 系统状态

### 3. 使用命令行界面

```bash
# 启动交互式 CLI
python -m agent_perpetual_evolution_system.cli_application_layer

# 或者直接运行
agent-evolution
```

## 🏗️ 核心概念

### 1. 系统架构

系统采用 8 层架构设计：

```
┌─────────────────────────────────────────┐
│         API 展示层 (05)                  │
│   FastAPI + RESTful 接口                 │
├─────────────────────────────────────────┤
│         CLI 应用层 (06)                  │
│   交互式命令行界面                       │
├─────────────────────────────────────────┤
│         测试层 (07)                      │
│   单元测试 + 集成测试                    │
├─────────────────────────────────────────┤
│       业务领域层 (03)                    │
│   任务处理 + 调度 + 学习 + 反馈          │
├─────────────────────────────────────────┤
│       数据模型层 (04)                    │
│   数据结构定义                           │
├─────────────────────────────────────────┤
│     基础设施层 (02)                      │
│   存储 + 日志                            │
├─────────────────────────────────────────┤
│       配置层 (01)                        │
│   全局配置管理                           │
├─────────────────────────────────────────┤
│       核心层 (00)                       │
│   接口契约定义                           │
└─────────────────────────────────────────┘
```

### 2. 核心组件

| 组件 | 说明 |
|------|------|
| `TaskWorkflowManagerComponent` | 任务工作流管理器 |
| `TaskAnalyzerPlannerComponent` | 任务分析规划器 |
| `TaskStepExecutorComponent` | 任务步骤执行器 |
| `PriorityQueueManagerComponent` | 优先级队列管理器 |
| `WorkflowModeCoordinatorComponent` | 工作流模式协调器 |
| `ExperienceLearningManagerComponent` | 经验学习管理器 |
| `FeedbackGenerationReporterComponent` | 反馈生成报告器 |
| `SystemIntegratorComponent` | 系统集成器 |

### 3. 任务生命周期

```
创建 → 分析 → 规划 → 调度 → 执行 → 学习 → 完成
  ↓      ↓      ↓      ↓      ↓      ↓
  └──────┴──────┴──────┴──────┴──────┘
              状态更新
```

## 📝 使用示例

### 示例 1: 基本任务处理

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 创建并执行任务
result = system.execute_single_task_workflow(
    raw_input="分析 Python 项目结构",
    priority=5
)

print(f"任务完成: {result['task_id']}")
print(f"成功: {result['execution_result']['success']}")
print(f"经验: {len(result['experience'])} 条")

system.shutdown_system()
```

### 示例 2: 批量任务处理

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

tasks = [
    {"input": "代码审查", "priority": 5},
    {"input": "性能分析", "priority": 3},
    {"input": "安全扫描", "priority": 4},
]

results = []
for task in tasks:
    result = system.execute_single_task_workflow(
        raw_input=task["input"],
        priority=task["priority"]
    )
    results.append(result)

# 统计
successful = sum(1 for r in results if r['execution_result']['success'])
print(f"成功率: {successful}/{len(results)}")

system.shutdown_system()
```

### 示例 3: 自定义存储后端

```python
from agent_perpetual_evolution_system import (
    SystemIntegratorComponent,
    MemoryBasedStorageAdapter,
    StructuredLoggerFrameworkImplementation
)

# 创建自定义存储和日志
storage = MemoryBasedStorageAdapter()
logger = StructuredLoggerFrameworkImplementation()

# 初始化系统
system = SystemIntegratorComponent(
    custom_storage=storage,
    custom_logger=logger
)

# 执行任务
result = system.execute_single_task_workflow(
    raw_input="使用自定义存储",
    priority=1
)

system.shutdown_system()
```

### 示例 4: 访问系统组件

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 直接访问组件
workflow_manager = system.task_workflow_manager
analyzer_planner = system.task_analyzer_planner
executor = system.task_step_executor

# 使用单个组件
task = workflow_manager.create_new_task_workflow(
    raw_input_text="独立使用组件",
    priority_level=3
)

plan = analyzer_planner.analyze_and_generate_execution_plan(task)
result = executor.execute_task_execution_plan(task, plan)

print(f"独立执行结果: {result['success']}")

system.shutdown_system()
```

### 示例 5: 查询系统状态

```python
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 获取完整状态
status = system.get_system_status()
print(f"版本: {status['version']}")
print(f"初始化: {status['initialized']}")

# 组件状态
components = status['components']
print(f"存储状态: {components['storage_backend']['status']}")
print(f"队列大小: {components['priority_queue']['queue_size']}")

# 获取任务统计
task_stats = system.task_workflow_manager.get_task_workflow_statistics()
print(f"待处理任务: {task_stats['pending_task_count']}")

system.shutdown_system()
```

## ⚙️ 配置

### 环境变量

创建 `.env` 文件：

```env
# 应用配置
APPLICATION_NAME=Agent Evolution System
APPLICATION_VERSION=3.0.0
DEBUG_MODE_ENABLED=false

# API 服务器
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8000

# 存储配置
STORAGE_BACKEND_TYPE=memory
DATABASE_FILE_PATH=data/agent_system.db

# 日志配置
LOGGING_LEVEL=INFO
LOG_TO_FILE_ENABLED=false
```

### 程序化配置

```python
from agent_perpetual_evolution_system import (
    ApplicationGlobalSettings,
    get_application_global_settings
)

# 方式1: 使用全局单例
settings = get_application_global_settings()
print(f"版本: {settings.APPLICATION_VERSION}")

# 方式2: 创建自定义配置
custom_settings = ApplicationGlobalSettings(
    APPLICATION_NAME="Custom System",
    DEBUG_MODE_ENABLED=True,
    LOGGING_LEVEL="DEBUG"
)
```

## 🧪 测试

### 运行所有测试

```bash
pytest agent_perpetual_evolution_system/testing_layer/ -v
```

### 运行单元测试

```bash
pytest agent_perpetual_evolution_system/testing_layer/unit_tests/ -v
```

### 运行集成测试

```bash
pytest agent_perpetual_evolution_system/testing_layer/integration_tests/ -v
```

### 运行 API 测试

```bash
pytest agent_perpetual_evolution_system/testing_layer/api_tests/ -v
```

## 🛠️ 开发

### 代码格式化

```bash
# 使用 Black
black agent_perpetual_evolution_system/

# 使用 Ruff
ruff check agent_perpetual_evolution_system/ --fix
```

### 类型检查

```bash
mypy agent_perpetual_evolution_system/
```

### 代码检查

```bash
ruff check agent_perpetual_evolution_system/
```

### 测试覆盖率

```bash
pytest agent_perpetual_evolution_system/testing_layer/ --cov=agent_perpetual_evolution_system
```

## 📚 学习资源

### API 文档

详细的 API 文档请参考：[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

### 架构文档

系统架构说明请参考：[ARCHITECTURE.md](./ARCHITECTURE.md)

### 示例代码

更多示例请参考：[EXAMPLES.md](./EXAMPLES.md)

## 🐛 常见问题

### Q1: 如何处理大型项目？

```python
# 使用批量处理
from agent_perpetual_evolution_system import SystemIntegratorComponent

system = SystemIntegratorComponent()

# 分批处理
batch_size = 100
for i in range(0, len(large_project_list), batch_size):
    batch = large_project_list[i:i+batch_size]
    for item in batch:
        system.execute_single_task_workflow(item, priority=5)
```

### Q2: 如何扩展存储后端？

```python
from agent_perpetual_evolution_system import CoreStorageInterfaceContract

class CustomStorageAdapter(CoreStorageInterfaceContract):
    # 实现所有抽象方法
    pass

# 使用自定义存储
storage = CustomStorageAdapter()
system = SystemIntegratorComponent(custom_storage=storage)
```

### Q3: 如何添加新的学习策略？

```python
from agent_perpetual_evolution_system import ExperienceLearningManagerComponent

# 扩展现有组件
class EnhancedExperienceManager(ExperienceLearningManagerComponent):
    def advanced_learning_strategy(self, task_data):
        # 实现高级学习策略
        pass
```

## 🎯 最佳实践

1. **错误处理**: 使用 `try-except` 包裹关键操作
2. **资源管理**: 使用 `contextlib` 管理资源
3. **日志记录**: 使用结构化日志记录关键事件
4. **配置管理**: 使用环境变量进行配置
5. **测试覆盖**: 为新功能编写测试

## 📞 支持

- 📧 邮箱: support@example.com
- 🐛 GitHub Issues: [链接](https://github.com/example/agent-perpetual-evolution-system/issues)
- 📖 文档: [链接](https://agent-perpetual-evolution-system.readthedocs.io)

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

**版本**: 3.0.0  
**最后更新**: 2026-05-16  
**快速入门完成!** 🎉
