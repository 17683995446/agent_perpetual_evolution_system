# Agent Perpetual Evolution System

高度模块化的Agent永续自进化运行系统 - 产品级架构

## 架构概述

本系统采用清晰的分层架构设计，从底层抽象到上层应用，确保代码的模块化、可维护性和可扩展性。

### 分层架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    06. CLI应用层                             │
│                 (交互式命令行界面)                            │
├─────────────────────────────────────────────────────────────┤
│                    05. API展示层                             │
│              (FastAPI应用、路由管理)                          │
├─────────────────────────────────────────────────────────────┤
│                    04. 数据模型层                             │
│               (任务处理数据模型定义)                          │
├─────────────────────────────────────────────────────────────┤
│                    03. 业务领域层                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │任务处理  │ │调度管理  │ │学习模块  │ │反馈生成  │      │
│  │  组件   │ │  组件   │ │  组件   │ │  组件   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │         系统集成组件 (System Integrator)         │      │
│  └──────────────────────────────────────────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                    02. 基础设施适配层                         │
│  ┌──────────────────┐ ┌──────────────────┐                  │
│  │存储后端适配器    │ │日志框架实现      │                  │
│  └──────────────────┘ └──────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                    01. 配置管理层                             │
│               (应用全局设置、环境变量)                        │
├─────────────────────────────────────────────────────────────┤
│                    00. 核心抽象层                             │
│  ┌──────────────────┐ ┌──────────────────┐ ┌───────────┐  │
│  │存储接口契约      │ │日志接口契约      │ │调度接口   │  │
│  └──────────────────┘ └──────────────────┘ └───────────┘  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    07. 测试层                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │单元测试  │ │集成测试  │ │API测试    │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
agent_perpetual_evolution_system/
├── __init__.py
├── 00_core_abstraction_layer/          # 核心抽象层
│   ├── __init__.py
│   └── interfaces/
│       ├── __init__.py
│       ├── logging_interface_contract.py
│       ├── scheduler_interface_contract.py
│       └── storage_interface_contract.py
├── 01_configuration_management_layer/   # 配置管理层
│   ├── __init__.py
│   └── application_global_settings.py
├── 02_infrastructure_adapter_layer/     # 基础设施适配层
│   ├── __init__.py
│   ├── logging_framework/
│   │   ├── __init__.py
│   │   └── structured_logger_framework_implementation.py
│   └── storage_backends/
│       ├── __init__.py
│       ├── memory_based_storage_adapter.py
│       └── storage_backend_factory_builder.py
├── 03_business_domain_layer/            # 业务领域层
│   ├── __init__.py
│   ├── feedback_generation_components/
│   │   ├── __init__.py
│   │   └── feedback_generation_reporter_component.py
│   ├── learning_module_components/
│   │   ├── __init__.py
│   │   └── experience_learning_manager_component.py
│   ├── schedule_management_components/
│   │   ├── __init__.py
│   │   ├── execution_checkpoint_saver_component.py
│   │   ├── priority_queue_manager_component.py
│   │   └── workflow_mode_coordinator_component.py
│   ├── system_integration_components/
│   │   ├── __init__.py
│   │   └── system_integrator_component.py
│   └── task_processing_components/
│       ├── __init__.py
│       ├── task_analyzer_planner_component.py
│       ├── task_step_executor_component.py
│       └── task_workflow_manager_component.py
├── 04_data_model_definition_layer/      # 数据模型定义层
│   ├── __init__.py
│   └── task_processing_models.py
├── 05_api_presentation_layer/           # API展示层
│   ├── __init__.py
│   ├── api_routes/
│   │   ├── __init__.py
│   │   ├── health_status_endpoint_handler.py
│   │   └── task_management_endpoint_handler.py
│   └── fastapi_application_entry.py
├── 06_cli_application_layer/            # CLI应用层
│   ├── __init__.py
│   └── interactive_command_line_interface.py
└── 07_testing_layer/                    # 测试层
    ├── __init__.py
    ├── conftest.py
    ├── pytest_configuration.ini
    ├── api_tests/
    │   ├── __init__.py
    │   └── test_api_endpoints.py
    ├── integration_tests/
    │   ├── __init__.py
    │   └── test_system_integrator_component.py
    └── unit_tests/
        ├── __init__.py
        ├── business_components/
        │   ├── __init__.py
        │   ├── test_task_analyzer_planner_component.py
        │   └── test_task_workflow_manager_component.py
        ├── configuration/
        │   ├── __init__.py
        │   └── test_application_global_settings.py
        ├── core_interfaces/
        │   ├── __init__.py
        │   ├── test_logger_interface_contract.py
        │   └── test_storage_interface_contract.py
        └── infrastructure_adapters/
            ├── __init__.py
            ├── test_memory_based_storage_adapter.py
            └── test_structured_logger_framework_implementation.py
```

## 各层详细说明

### 00. 核心抽象层 (Core Abstraction Layer)

**职责**：定义系统核心接口契约，确保各层解耦

**关键组件**：
- `CoreStorageInterfaceContract`: 存储接口抽象，定义所有存储实现必须遵守的方法
- `CoreLoggerInterfaceContract`: 日志接口抽象，定义日志系统标准方法
- `SchedulerInterfaceContract`: 调度器接口抽象

**设计原则**：
- 使用抽象基类(ABC)定义接口
- 定义标准方法签名
- 确保所有适配器实现相同契约

### 01. 配置管理层 (Configuration Management Layer)

**职责**：管理应用全局配置，支持环境变量覆盖

**关键组件**：
- `ApplicationGlobalSettings`: 使用Pydantic的配置类
- `get_application_global_settings()`: 单例获取函数

**特性**：
- 类型安全的配置管理
- 支持环境变量覆盖
- 自动创建数据目录

### 02. 基础设施适配层 (Infrastructure Adapter Layer)

**职责**：实现核心抽象层定义的接口，提供具体的基础设施能力

**关键组件**：
- `MemoryBasedStorageAdapter`: 基于内存的存储实现（线程安全）
- `StructuredLoggerFrameworkImplementation`: 使用structlog的结构化日志实现
- `StorageBackendFactoryBuilder`: 存储后端工厂

**特性**：
- 多种存储实现可选（内存、未来可扩展SQLite、Redis等）
- 结构化日志支持
- 线程安全设计

### 03. 业务领域层 (Business Domain Layer)

**职责**：实现核心业务逻辑和领域模型

**子模块**：

#### 任务处理组件
- `TaskWorkflowManagerComponent`: 任务生命周期管理
- `TaskAnalyzerPlannerComponent`: 任务分析和执行计划生成
- `TaskStepExecutorComponent`: 任务步骤执行器

#### 调度管理组件
- `PriorityQueueManagerComponent`: 优先级队列管理
- `WorkflowModeCoordinatorComponent`: 工作流模式协调
- `ExecutionCheckpointSaverComponent`: 执行检查点保存

#### 学习模块组件
- `ExperienceLearningManagerComponent`: 经验学习和知识重用

#### 反馈生成组件
- `FeedbackGenerationReporterComponent`: 执行反馈生成

#### 系统集成组件
- `SystemIntegratorComponent`: 所有组件的协调节点，提供统一入口

### 04. 数据模型定义层 (Data Model Definition Layer)

**职责**：定义系统数据模型和数据结构

**关键组件**：
- `TaskProcessingModels`: 任务处理相关数据模型

### 05. API展示层 (API Presentation Layer)

**职责**：提供HTTP API接口，处理请求路由

**关键组件**：
- `FastAPI应用入口`: 主应用实例
- `健康状态端点处理`: /health, /health/liveness, /health/readiness
- `任务管理端点处理`: /api/v1/tasks

**特性**：
- RESTful API设计
- 自动API文档生成（Swagger/ReDoc）
- CORS支持

### 06. CLI应用层 (CLI Application Layer)

**职责**：提供命令行交互界面

**关键组件**：
- `InteractiveCommandLineInterface`: 交互式CLI界面

### 07. 测试层 (Testing Layer)

**职责**：提供完整的测试覆盖

**测试分类**：

#### 单元测试
- 核心接口契约测试
- 基础设施适配器测试
- 业务组件测试
- 配置管理测试

#### 集成测试
- 系统集成器组件测试

#### API测试
- API端点集成测试

**测试框架**：
- pytest作为测试运行器
- 使用Mock隔离依赖
- 清晰的测试夹具管理

## 文件名约定

### 后缀命名规则

- `*_contract.py`: 接口契约文件
- `*_implementation.py`: 实现文件
- `*_adapter.py`: 适配器文件
- `*_component.py`: 业务组件文件
- `*_handler.py`: 处理器文件
- `*_manager.py`: 管理器文件
- `*_settings.py`: 设置文件
- `*_models.py`: 模型文件
- `*_entry.py`: 入口文件
- `*_interface.py`: 接口文件

## 使用方法

### 运行API服务器

```bash
cd /workspace/agent_perpetual_evolution_system
python -m agent_perpetual_evolution_system.05_api_presentation_layer.fastapi_application_entry
```

或使用uvicorn直接运行：

```bash
uvicorn agent_perpetual_evolution_system.05_api_presentation_layer.fastapi_application_entry:fastapi_application --reload
```

### 运行测试

```bash
cd /workspace/agent_perpetual_evolution_system
pytest 07_testing_layer/ -c 07_testing_layer/pytest_configuration.ini -v
```

运行特定测试类别：
```bash
# 单元测试
pytest 07_testing_layer/unit_tests/ -v

# 集成测试
pytest 07_testing_layer/integration_tests/ -v

# API测试
pytest 07_testing_layer/api_tests/ -v
```

### 使用系统集成器

```python
from agent_perpetual_evolution_system.03_business_domain_layer.system_integration_components.system_integrator_component import SystemIntegratorComponent
from agent_perpetual_evolution_system.02_infrastructure_adapter_layer.storage_backends.memory_based_storage_adapter import MemoryBasedStorageAdapter
from agent_perpetual_evolution_system.02_infrastructure_adapter_layer.logging_framework.structured_logger_framework_implementation import StructuredLoggerFrameworkImplementation

# 初始化组件
storage = MemoryBasedStorageAdapter()
logger = StructuredLoggerFrameworkImplementation()
system = SystemIntegratorComponent(storage, logger)

# 处理任务
result = system.process_task("分析Python代码库的架构", priority=2)
print(result)

# 获取系统状态
status = system.get_system_status()
print(status)
```

## 架构设计原则

### 1. 依赖倒置原则 (DIP)
- 高层模块不依赖低层模块，都依赖抽象
- 抽象不依赖细节，细节依赖抽象

### 2. 开闭原则 (OCP)
- 对扩展开放，对修改关闭
- 通过添加新适配器/组件来扩展功能

### 3. 单一职责原则 (SRP)
- 每个类/模块只有一个改变的理由
- 清晰的职责划分

### 4. 接口隔离原则 (ISP)
- 定义最小必要接口
- 避免胖接口

### 5. 里氏替换原则 (LSP)
- 子类可以替换父类而不破坏程序正确性

## 扩展性说明

### 添加新的存储后端
1. 在`00_core_abstraction_layer/interfaces/`确保接口契约已定义
2. 在`02_infrastructure_adapter_layer/storage_backends/`创建新的适配器类
3. 实现所有契约方法
4. 在工厂类中注册新后端

### 添加新的业务组件
1. 在`03_business_domain_layer/`适当子目录创建组件类
2. 在`SystemIntegratorComponent`中集成新组件
3. 添加相应的单元测试

### 添加新的API端点
1. 在`05_api_presentation_layer/api_routes/`创建端点处理器
2. 在主应用中注册路由
3. 添加API集成测试

## 技术栈

- **Web框架**: FastAPI
- **日志库**: structlog
- **配置管理**: Pydantic Settings
- **测试框架**: pytest
- **ASGI服务器**: uvicorn
- **类型提示**: Python 3.8+ 类型注解

## 开发建议

1. 始终从抽象层开始，先定义接口再实现
2. 保持各层之间的单向依赖（上层依赖下层）
3. 为所有新代码添加相应的测试
4. 使用类型注解提高代码质量
5. 保持文件名和类名的一致性

## 版本历史

- **v3.0.0**: 完整的分层架构重构，组件化设计，完整测试覆盖
