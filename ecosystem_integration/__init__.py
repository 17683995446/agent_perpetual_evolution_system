"""
Agent 永续自进化系统 - 生态系统集成模块

版本: v5.0.0
模块: 生态系统集成
包含: 插件系统、插件市场、沙箱隔离、热重载等功能
"""

from .ecosystem_components import (
    PluginInterface,
    PluginType,
    PluginStatus,
    PluginMetadata,
    BasePlugin,
    PluginLifecycleManager,
    PluginSandbox,
    PluginDiscoveryEngine,
    PluginMarketplace,
    PluginEventBus,
    PluginConfigManager,
    EcosystemManager,
)

__all__ = [
    "PluginInterface",
    "PluginType",
    "PluginStatus",
    "PluginMetadata",
    "BasePlugin",
    "PluginLifecycleManager",
    "PluginSandbox",
    "PluginDiscoveryEngine",
    "PluginMarketplace",
    "PluginEventBus",
    "PluginConfigManager",
    "EcosystemManager",
]
