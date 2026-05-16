"""
Agent Perpetual Evolution System - Infrastructure Adapter Layer
Agent永续自进化运行系统 - 基础设施适配层

提供存储、日志等基础设施的实现
"""

from .storage_backends.memory_based_storage_adapter import (
    MemoryBasedStorageAdapter,
)
from .storage_backends.storage_backend_factory_builder import (
    StorageBackendFactoryBuilder,
    create_storage_backend,
)
from .logging_framework.structured_logger_framework_implementation import (
    StructuredLoggerFrameworkImplementation,
)

__all__ = [
    'MemoryBasedStorageAdapter',
    'StorageBackendFactoryBuilder',
    'create_storage_backend',
    'StructuredLoggerFrameworkImplementation',
]
