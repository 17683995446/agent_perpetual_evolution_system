"""
Infrastructure Adapter Layer - Storage Backend Factory Builder
基础设施适配层 - 存储后端工厂构建器

根据配置创建合适的存储后端实例
支持多种存储类型：内存、SQLite、Redis等
"""

from typing import Type, Dict

from ...core_abstraction_layer.interfaces.storage_interface_contract import (
    CoreStorageInterfaceContract,
)
from ...configuration_management_layer.application_global_settings import (
    get_application_global_settings,
)
from .memory_based_storage_adapter import (
    MemoryBasedStorageAdapter,
)
from .sqlite_based_storage_adapter import (
    SQLiteBasedStorageAdapter,
)


class StorageBackendFactoryBuilder:
    """
    Storage Backend Factory Builder - 存储后端工厂构建器
    
    根据配置创建合适的存储后端实例
    支持多种存储类型：内存、SQLite、Redis等
    """
    
    # 存储后端注册表
    _storage_backend_registry: Dict[str, Type[CoreStorageInterfaceContract]] = {
        "memory": MemoryBasedStorageAdapter,
        "sqlite": SQLiteBasedStorageAdapter,
    }
    
    @classmethod
    def create_storage_backend_instance(cls) -> CoreStorageInterfaceContract:
        """
        Create Storage Backend Instance - 创建存储后端实例
        
        根据配置创建合适的存储后端
        
        Returns:
            CoreStorageInterfaceContract: 存储接口实例
        """
        settings = get_application_global_settings()
        backend_type = settings.STORAGE_BACKEND_TYPE.lower()
        
        if backend_type not in cls._storage_backend_registry:
            # 默认回退到内存存储
            backend_type = "memory"
        
        storage_class = cls._storage_backend_registry[backend_type]
        
        if backend_type == "sqlite":
            # SQLite 存储需要额外参数
            return storage_class(database_path=settings.DATABASE_FILE_PATH)
        else:
            # 其他存储（如内存）不需要参数
            return storage_class()
    
    @classmethod
    def register_new_storage_backend(cls, backend_name: str, backend_class: Type[CoreStorageInterfaceContract]):
        """
        Register New Storage Backend - 注册新的存储后端
        
        Args:
            backend_name: 后端名称
            backend_class: 后端实现类
        """
        cls._storage_backend_registry[backend_name.lower()] = backend_class


# 便捷函数
def create_storage_backend() -> CoreStorageInterfaceContract:
    """
    Create Storage Backend - 创建存储后端
    
    便捷函数，直接调用工厂创建存储后端
    
    Returns:
        CoreStorageInterfaceContract: 存储接口实例
    """
    return StorageBackendFactoryBuilder.create_storage_backend_instance()


__all__ = [
    'StorageBackendFactoryBuilder',
    'create_storage_backend',
]
