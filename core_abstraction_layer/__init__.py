"""
Agent Perpetual Evolution System - Core Abstraction Layer
Agent永续自进化运行系统 - 核心抽象层

定义系统核心接口契约
"""

from .interfaces.storage_interface_contract import (
    CoreStorageInterfaceContract,
)
from .interfaces.logging_interface_contract import (
    CoreLoggerInterfaceContract,
)
from .interfaces.scheduler_interface_contract import (
    CoreSchedulerInterfaceContract,
)

__version__ = "3.0.0"

__all__ = [
    "CoreStorageInterfaceContract",
    "CoreLoggerInterfaceContract",
    "CoreSchedulerInterfaceContract",
]
