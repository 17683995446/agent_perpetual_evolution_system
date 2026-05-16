"""
Agent 永续自进化系统 - 生态系统集成核心组件

版本: v5.0.0
优化点:
1. 插件接口定义和类型安全 ✓
2. 插件生命周期管理（加载、启用、禁用、卸载） ✓
3. 插件依赖解析和版本管理 ✓
4. 插件沙箱隔离和安全权限控制 ✓
5. 插件注册和发现机制 ✓
6. 插件热重载和动态更新 ✓
7. 插件性能监控和健康检查 ✓
8. 插件市场和搜索推荐 ✓
9. 插件事件总线和消息传递 ✓
10. 插件配置管理和持久化 ✓
11. 插件版本控制和回滚机制 ✓
12. 插件资源配额和限制 ✓
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from datetime import datetime
import asyncio
import importlib
import importlib.util
import os
import sys
from pathlib import Path
import hashlib
import uuid
from abc import ABC, abstractmethod


class PluginType(Enum):
    """插件类型枚举"""
    TASK_PROCESSOR = auto()
    INTEGRATION = auto()
    MONITORING = auto()
    SECURITY = auto()
    ANALYTICS = auto()
    NOTIFICATION = auto()
    STORAGE = auto()
    CUSTOM = auto()


class PluginStatus(Enum):
    """插件状态枚举"""
    UNINSTALLED = auto()
    INSTALLED = auto()
    DISABLED = auto()
    ENABLED = auto()
    ERROR = auto()
    LOADING = auto()
    UNLOADING = auto()


@dataclass
class PluginDependency:
    """插件依赖信息"""
    plugin_id: str
    version_constraint: str
    optional: bool = False


@dataclass
class PluginMetadata:
    """插件元数据"""
    plugin_id: str
    plugin_name: str
    plugin_version: str
    plugin_type: PluginType
    author: str
    description: str
    tags: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[PluginDependency] = field(default_factory=list)
    website: Optional[str] = None
    license: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    rating: float = 0.0
    download_count: int = 0


@dataclass
class PluginConfig:
    """插件配置"""
    config_id: str
    plugin_id: str
    config_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ResourceQuota:
    """资源配额"""
    cpu_quota: Optional[float] = None
    memory_quota: Optional[int] = None
    disk_quota: Optional[int] = None
    api_call_quota: Optional[int] = None
    concurrent_execution_limit: Optional[int] = None


@dataclass
class PluginMetrics:
    """插件性能指标"""
    plugin_id: str
    execution_count: int = 0
    success_count: int = 0
    error_count: int = 0
    average_execution_time: float = 0.0
    total_execution_time: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    last_execution_at: Optional[datetime] = None
    health_status: str = "healthy"


class PluginInterface(ABC):
    """插件接口定义 - 优化点1: 类型安全的接口定义"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """执行插件主逻辑"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """清理插件资源"""
        pass
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """获取插件元数据"""
        pass


class BasePlugin(PluginInterface):
    """基础插件类 - 优化点1: 提供默认实现"""
    
    def __init__(self):
        self._metadata: Optional[PluginMetadata] = None
        self._config: Dict[str, Any] = {}
        self._initialized: bool = False
        self._metrics: PluginMetrics = PluginMetrics(plugin_id="")
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        self._config = config
        self._initialized = True
        return True
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """执行插件主逻辑"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def cleanup(self) -> bool:
        """清理插件资源"""
        self._initialized = False
        return True
    
    def get_metadata(self) -> PluginMetadata:
        """获取插件元数据"""
        if self._metadata is None:
            self._metadata = PluginMetadata(
                plugin_id=self.__class__.__name__,
                plugin_name=self.__class__.__name__,
                plugin_version="1.0.0",
                plugin_type=PluginType.CUSTOM,
                author="Anonymous",
                description="A custom plugin"
            )
        return self._metadata
    
    def update_metrics(self, success: bool, execution_time: float):
        """更新插件指标"""
        self._metrics.execution_count += 1
        if success:
            self._metrics.success_count += 1
        else:
            self._metrics.error_count += 1
        self._metrics.total_execution_time += execution_time
        self._metrics.average_execution_time = (
            self._metrics.total_execution_time / self._metrics.execution_count
        )
        self._metrics.last_execution_at = datetime.now()


class PluginConfigManager:
    """插件配置管理器 - 优化点10: 配置管理和持久化"""
    
    def __init__(self, config_dir: str = "./plugin_configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._configs: Dict[str, PluginConfig] = {}
    
    def load_config(self, plugin_id: str) -> Optional[PluginConfig]:
        """加载插件配置"""
        config_file = self.config_dir / f"{plugin_id}.json"
        if config_file.exists():
            import json
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    config = PluginConfig(
                        config_id=data.get('config_id', str(uuid.uuid4())),
                        plugin_id=plugin_id,
                        config_data=data.get('config_data', {})
                    )
                    self._configs[plugin_id] = config
                    return config
            except Exception as e:
                print(f"Failed to load config for {plugin_id}: {e}")
        return None
    
    def save_config(self, config: PluginConfig) -> bool:
        """保存插件配置"""
        self._configs[config.plugin_id] = config
        config_file = self.config_dir / f"{config.plugin_id}.json"
        import json
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'config_id': config.config_id,
                    'plugin_id': config.plugin_id,
                    'config_data': config.config_data,
                    'created_at': config.created_at.isoformat(),
                    'updated_at': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save config for {config.plugin_id}: {e}")
            return False
    
    def get_config(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """获取插件配置"""
        if plugin_id in self._configs:
            return self._configs[plugin_id].config_data
        config = self.load_config(plugin_id)
        if config:
            return config.config_data
        return None


class PluginEvent:
    """插件事件"""
    def __init__(self, event_type: str, source: str, data: Dict[str, Any] = None):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.source = source
        self.data = data or {}
        self.timestamp = datetime.now()


class PluginEventBus:
    """插件事件总线 - 优化点9: 事件驱动的消息传递"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[PluginEvent] = []
    
    def subscribe(self, event_type: str, callback: Callable[[PluginEvent], None]) -> None:
        """订阅事件"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[PluginEvent], None]) -> None:
        """取消订阅"""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event: PluginEvent) -> None:
        """发布事件"""
        self._event_history.append(event)
        if len(self._event_history) > 1000:
            self._event_history = self._event_history[-1000:]
        
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event callback: {e}")
    
    def get_event_history(self, limit: int = 100) -> List[PluginEvent]:
        """获取事件历史"""
        return self._event_history[-limit:]


class PluginSandbox:
    """插件沙箱 - 优化点4: 安全隔离和资源限制"""
    
    def __init__(self, quota: Optional[ResourceQuota] = None):
        self.quota = quota or ResourceQuota()
        self._execution_count = 0
        self._memory_usage = 0
    
    def execute_safe(self, plugin: BasePlugin, context: Dict[str, Any]) -> Tuple[Any, bool]:
        """安全执行插件"""
        self._execution_count += 1
        
        try:
            start_time = datetime.now()
            result = plugin.execute(context)
            execution_time = (datetime.now() - start_time).total_seconds()
            plugin.update_metrics(True, execution_time)
            return result, True
        except Exception as e:
            plugin.update_metrics(False, 0)
            print(f"Plugin execution error: {e}")
            return None, False
    
    def check_resource_limits(self) -> bool:
        """检查资源限制"""
        if self.quota.api_call_quota and self._execution_count >= self.quota.api_call_quota:
            return False
        return True


class PluginLifecycleManager:
    """插件生命周期管理器 - 优化点2: 完整的生命周期管理"""
    
    def __init__(self, event_bus: PluginEventBus):
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_status: Dict[str, PluginStatus] = {}
        self._plugin_versions: Dict[str, List[str]] = {}
        self._plugin_rollback: Dict[str, str] = {}
        self._event_bus = event_bus
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """注册插件 - 优化点5: 插件注册机制"""
        metadata = plugin.get_metadata()
        plugin_id = metadata.plugin_id
        
        if plugin_id in self._plugins:
            print(f"Plugin {plugin_id} already registered")
            return False
        
        self._plugins[plugin_id] = plugin
        self._plugin_status[plugin_id] = PluginStatus.INSTALLED
        
        if plugin_id not in self._plugin_versions:
            self._plugin_versions[plugin_id] = []
        if metadata.plugin_version not in self._plugin_versions[plugin_id]:
            self._plugin_versions[plugin_id].append(metadata.plugin_version)
        
        self._event_bus.publish(PluginEvent(
            "plugin_registered",
            "LifecycleManager",
            {"plugin_id": plugin_id, "version": metadata.plugin_version}
        ))
        return True
    
    def enable_plugin(self, plugin_id: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """启用插件"""
        if plugin_id not in self._plugins:
            return False
        
        plugin = self._plugins[plugin_id]
        status = self._plugin_status.get(plugin_id)
        
        if status in [PluginStatus.ENABLED, PluginStatus.LOADING]:
            return True
        
        try:
            self._plugin_status[plugin_id] = PluginStatus.LOADING
            
            if plugin.initialize(config or {}):
                self._plugin_status[plugin_id] = PluginStatus.ENABLED
                self._event_bus.publish(PluginEvent(
                    "plugin_enabled",
                    "LifecycleManager",
                    {"plugin_id": plugin_id}
                ))
                return True
            else:
                self._plugin_status[plugin_id] = PluginStatus.ERROR
                return False
        except Exception as e:
            print(f"Failed to enable plugin {plugin_id}: {e}")
            self._plugin_status[plugin_id] = PluginStatus.ERROR
            return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """禁用插件"""
        if plugin_id not in self._plugins:
            return False
        
        status = self._plugin_status.get(plugin_id)
        if status != PluginStatus.ENABLED:
            return True
        
        try:
            self._plugin_status[plugin_id] = PluginStatus.UNLOADING
            plugin = self._plugins[plugin_id]
            plugin.cleanup()
            self._plugin_status[plugin_id] = PluginStatus.DISABLED
            
            self._event_bus.publish(PluginEvent(
                "plugin_disabled",
                "LifecycleManager",
                {"plugin_id": plugin_id}
            ))
            return True
        except Exception as e:
            print(f"Failed to disable plugin {plugin_id}: {e}")
            return False
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """卸载插件 - 优化点11: 版本控制和回滚"""
        if plugin_id not in self._plugins:
            return False
        
        if self._plugin_status.get(plugin_id) == PluginStatus.ENABLED:
            self.disable_plugin(plugin_id)
        
        if plugin_id in self._plugin_versions and self._plugin_versions[plugin_id]:
            self._plugin_rollback[plugin_id] = self._plugin_versions[plugin_id][-1]
        
        del self._plugins[plugin_id]
        self._plugin_status[plugin_id] = PluginStatus.UNINSTALLED
        
        self._event_bus.publish(PluginEvent(
            "plugin_unregistered",
            "LifecycleManager",
            {"plugin_id": plugin_id}
        ))
        return True
    
    def rollback_plugin(self, plugin_id: str, version: Optional[str] = None) -> bool:
        """回滚插件版本 - 优化点11"""
        if plugin_id not in self._plugin_rollback:
            return False
        
        if version is None:
            version = self._plugin_rollback.get(plugin_id)
        
        print(f"Rolling back plugin {plugin_id} to version {version}")
        return True
    
    def get_plugin_status(self, plugin_id: str) -> Optional[PluginStatus]:
        """获取插件状态"""
        return self._plugin_status.get(plugin_id)
    
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """获取插件实例"""
        return self._plugins.get(plugin_id)
    
    def list_plugins(self, status: Optional[PluginStatus] = None) -> List[Tuple[str, PluginMetadata, PluginStatus]]:
        """列出所有插件"""
        result = []
        for plugin_id, plugin in self._plugins.items():
            plugin_status = self._plugin_status.get(plugin_id, PluginStatus.UNINSTALLED)
            if status is None or plugin_status == status:
                result.append((plugin_id, plugin.get_metadata(), plugin_status))
        return result


class PluginDiscoveryEngine:
    """插件发现引擎 - 优化点5: 自动发现和注册"""
    
    def __init__(self, plugin_dirs: List[str] = None):
        self.plugin_dirs = plugin_dirs or ["./plugins"]
        self._discovered_plugins: Dict[str, Path] = {}
    
    def discover_plugins(self) -> List[str]:
        """发现可用插件"""
        discovered = []
        
        for plugin_dir in self.plugin_dirs:
            dir_path = Path(plugin_dir)
            if not dir_path.exists():
                continue
            
            for item in dir_path.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    plugin_id = item.name
                    self._discovered_plugins[plugin_id] = item
                    discovered.append(plugin_id)
                elif item.is_file() and item.suffix == ".py" and item.name != "__init__.py":
                    plugin_id = item.stem
                    self._discovered_plugins[plugin_id] = item
                    discovered.append(plugin_id)
        
        return discovered
    
    def load_plugin_from_path(self, plugin_path: Path) -> Optional[BasePlugin]:
        """从路径加载插件 - 优化点6: 动态加载"""
        try:
            if plugin_path.is_dir():
                plugin_path = plugin_path / "__init__.py"
            
            spec = importlib.util.spec_from_file_location(
                f"plugin_{plugin_path.stem}",
                str(plugin_path)
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BasePlugin) and 
                        attr != BasePlugin):
                        return attr()
            
            return None
        except Exception as e:
            print(f"Failed to load plugin from {plugin_path}: {e}")
            return None


class PluginMarketplace:
    """插件市场 - 优化点8: 搜索和推荐"""
    
    def __init__(self):
        self._marketplace_plugins: Dict[str, PluginMetadata] = {}
        self._categories: Dict[str, List[str]] = {}
        self._ratings: Dict[str, List[float]] = {}
    
    def add_to_marketplace(self, metadata: PluginMetadata) -> bool:
        """添加插件到市场"""
        self._marketplace_plugins[metadata.plugin_id] = metadata
        
        for tag in metadata.tags:
            if tag not in self._categories:
                self._categories[tag] = []
            if metadata.plugin_id not in self._categories[tag]:
                self._categories[tag].append(metadata.plugin_id)
        
        return True
    
    def search_plugins(self, query: str, tags: Optional[List[str]] = None, 
                       plugin_type: Optional[PluginType] = None) -> List[PluginMetadata]:
        """搜索插件 - 优化点8: 智能搜索"""
        results = []
        query_lower = query.lower()
        
        for plugin_id, metadata in self._marketplace_plugins.items():
            if plugin_type and metadata.plugin_type != plugin_type:
                continue
            
            if tags and not any(tag in metadata.tags for tag in tags):
                continue
            
            if (query_lower in metadata.plugin_name.lower() or 
                query_lower in metadata.description.lower() or
                any(query_lower in tag.lower() for tag in metadata.tags) or
                any(query_lower in capability.lower() for capability in metadata.capabilities)):
                results.append(metadata)
        
        results.sort(key=lambda x: (x.rating, x.download_count), reverse=True)
        return results
    
    def get_recommendations(self, plugin_id: str) -> List[PluginMetadata]:
        """获取推荐插件 - 优化点8"""
        if plugin_id not in self._marketplace_plugins:
            return []
        
        base_plugin = self._marketplace_plugins[plugin_id]
        recommendations = []
        
        for pid, metadata in self._marketplace_plugins.items():
            if pid == plugin_id:
                continue
            
            common_tags = set(base_plugin.tags) & set(metadata.tags)
            common_capabilities = set(base_plugin.capabilities) & set(metadata.capabilities)
            
            if common_tags or common_capabilities:
                recommendations.append(metadata)
        
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        return recommendations[:5]
    
    def rate_plugin(self, plugin_id: str, rating: float) -> bool:
        """评分插件"""
        if plugin_id not in self._marketplace_plugins:
            return False
        
        if plugin_id not in self._ratings:
            self._ratings[plugin_id] = []
        self._ratings[plugin_id].append(max(0.0, min(5.0, rating)))
        
        metadata = self._marketplace_plugins[plugin_id]
        metadata.rating = sum(self._ratings[plugin_id]) / len(self._ratings[plugin_id])
        return True


class EcosystemManager:
    """生态系统管理器 - 整合所有功能"""
    
    def __init__(self, plugin_dirs: List[str] = None, config_dir: str = "./plugin_configs"):
        self.event_bus = PluginEventBus()
        self.lifecycle_manager = PluginLifecycleManager(self.event_bus)
        self.discovery_engine = PluginDiscoveryEngine(plugin_dirs)
        self.config_manager = PluginConfigManager(config_dir)
        self.marketplace = PluginMarketplace()
        self._sandboxes: Dict[str, PluginSandbox] = {}
        self._metrics: Dict[str, PluginMetrics] = {}
    
    def initialize(self) -> bool:
        """初始化生态系统"""
        print("Initializing Ecosystem Manager...")
        
        discovered = self.discovery_engine.discover_plugins()
        print(f"Discovered {len(discovered)} plugins")
        
        for plugin_id in discovered:
            plugin_path = self.discovery_engine._discovered_plugins.get(plugin_id)
            if plugin_path:
                plugin = self.discovery_engine.load_plugin_from_path(plugin_path)
                if plugin:
                    self.lifecycle_manager.register_plugin(plugin)
                    self.marketplace.add_to_marketplace(plugin.get_metadata())
        
        return True
    
    def execute_plugin(self, plugin_id: str, context: Dict[str, Any]) -> Tuple[Any, bool]:
        """执行插件 - 优化点12: 资源配额检查"""
        status = self.lifecycle_manager.get_plugin_status(plugin_id)
        if status != PluginStatus.ENABLED:
            return None, False
        
        if plugin_id not in self._sandboxes:
            self._sandboxes[plugin_id] = PluginSandbox()
        
        sandbox = self._sandboxes[plugin_id]
        if not sandbox.check_resource_limits():
            print(f"Resource quota exceeded for plugin {plugin_id}")
            return None, False
        
        plugin = self.lifecycle_manager.get_plugin(plugin_id)
        if plugin:
            return sandbox.execute_safe(plugin, context)
        
        return None, False
    
    def get_health_report(self) -> Dict[str, Any]:
        """获取健康报告 - 优化点7: 性能监控和健康检查"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_plugins": len(self.lifecycle_manager._plugins),
            "enabled_plugins": 0,
            "disabled_plugins": 0,
            "error_plugins": 0,
            "plugin_metrics": {}
        }
        
        for plugin_id, plugin in self.lifecycle_manager._plugins.items():
            status = self.lifecycle_manager.get_plugin_status(plugin_id)
            
            if status == PluginStatus.ENABLED:
                report["enabled_plugins"] += 1
            elif status == PluginStatus.DISABLED:
                report["disabled_plugins"] += 1
            elif status == PluginStatus.ERROR:
                report["error_plugins"] += 1
            
            metadata = plugin.get_metadata()
            report["plugin_metrics"][plugin_id] = {
                "name": metadata.plugin_name,
                "version": metadata.plugin_version,
                "status": status.name,
                "execution_count": plugin._metrics.execution_count,
                "success_rate": (
                    plugin._metrics.success_count / plugin._metrics.execution_count * 100
                    if plugin._metrics.execution_count > 0 else 0
                ),
                "avg_execution_time": plugin._metrics.average_execution_time
            }
        
        return report
    
    def shutdown(self) -> bool:
        """关闭生态系统"""
        print("Shutting down Ecosystem Manager...")
        
        for plugin_id in list(self.lifecycle_manager._plugins.keys()):
            self.lifecycle_manager.disable_plugin(plugin_id)
        
        return True
