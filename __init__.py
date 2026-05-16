"""
Agent Perpetual Evolution System - Main Package
Agent永续自进化运行系统 - 主包

高度模块化的架构，清晰的层次
更长更清晰的文件名，至少4个单词
"""

__version__ = "3.0.0"

# 导入各层，简化使用
from .core_abstraction_layer import (
    CoreStorageInterfaceContract,
    CoreLoggerInterfaceContract,
    CoreSchedulerInterfaceContract,
)

from .configuration_management_layer import (
    ApplicationGlobalSettings,
    get_application_global_settings,
)

from .infrastructure_adapter_layer import (
    MemoryBasedStorageAdapter,
    StorageBackendFactoryBuilder,
    create_storage_backend,
    StructuredLoggerFrameworkImplementation,
)

from .business_domain_layer import (
    TaskAnalyzerPlannerComponent,
    TaskStepExecutorComponent,
    TaskWorkflowManagerComponent,
    WorkflowModeCoordinatorComponent,
    WorkflowExecutionMode,
    PriorityQueueManagerComponent,
    ExecutionCheckpointSaverComponent,
    ExperienceLearningManagerComponent,
    FeedbackGenerationReporterComponent,
    SystemIntegratorComponent,
)

from .data_model_definition_layer import (
    TaskProcessingDataModel,
    TaskStatusTypeEnum,
    TaskPriorityLevelEnum,
)

from .api_presentation_layer import (
    fastapi_application,
    health_router,
    task_router,
)

from .cli_application_layer import (
    InteractiveCommandLineInterface,
    run_interactive_command_line_interface,
)

__all__ = [
    # 核心抽象层
    "CoreStorageInterfaceContract",
    "CoreLoggerInterfaceContract",
    "CoreSchedulerInterfaceContract",
    
    # 配置管理层
    "ApplicationGlobalSettings",
    "get_application_global_settings",
    
    # 基础设施层
    "MemoryBasedStorageAdapter",
    "StorageBackendFactoryBuilder",
    "create_storage_backend",
    "StructuredLoggerFrameworkImplementation",
    
    # 业务领域层
    "TaskAnalyzerPlannerComponent",
    "TaskStepExecutorComponent",
    "TaskWorkflowManagerComponent",
    "WorkflowModeCoordinatorComponent",
    "WorkflowExecutionMode",
    "PriorityQueueManagerComponent",
    "ExecutionCheckpointSaverComponent",
    "ExperienceLearningManagerComponent",
    "FeedbackGenerationReporterComponent",
    "SystemIntegratorComponent",
    
    # 数据模型层
    "TaskProcessingDataModel",
    "TaskStatusTypeEnum",
    "TaskPriorityLevelEnum",
    
    # API展示层
    "fastapi_application",
    "health_router",
    "task_router",
    
    # CLI应用层
    "InteractiveCommandLineInterface",
    "run_interactive_command_line_interface",
]
