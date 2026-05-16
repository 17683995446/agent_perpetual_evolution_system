"""
Distributed Architecture Module - 分布式架构模块
提供分布式任务队列、负载均衡、数据一致性等功能
"""

import uuid
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
from collections import defaultdict, deque
import random

from ..core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class LoadBalancingStrategy(Enum):
    """负载均衡策略"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    WEIGHTED = "weighted"
    RANDOM = "random"


class DistributedTaskNode:
    """
    分布式任务节点 - 表示分布式系统中的节点
    """
    
    def __init__(
        self,
        node_id: str,
        node_name: str,
        host: str,
        port: int,
        weight: int = 1,
        capabilities: Optional[List[str]] = None
    ):
        self.node_id = node_id
        self.node_name = node_name
        self.host = host
        self.port = port
        self.weight = weight
        self.capabilities = capabilities or []
        self.status = "active"
        self.connections = 0
        self.total_requests = 0
        self.failed_requests = 0
        self.avg_response_time = 0.0
        self.last_health_check = datetime.now().isoformat()
        self.created_at = datetime.now().isoformat()
    
    def get_endpoint(self) -> str:
        """获取节点端点"""
        return f"{self.host}:{self.port}"
    
    def update_stats(self, response_time: float, success: bool):
        """更新统计信息"""
        self.total_requests += 1
        if not success:
            self.failed_requests += 1
        
        self.avg_response_time = (
            (self.avg_response_time * (self.total_requests - 1) + response_time) / self.total_requests
        )
    
    def is_healthy(self) -> bool:
        """检查节点是否健康"""
        if self.status != "active":
            return False
        
        error_rate = self.failed_requests / self.total_requests if self.total_requests > 0 else 0
        return error_rate < 0.1


class DistributedTaskQueue:
    """
    分布式任务队列 - 管理分布式任务
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.queues: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.queue_priorities: Dict[str, int] = {}
        self.task_metadata: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()
        self.task_results: Dict[str, Any] = {}
    
    def enqueue(
        self,
        task_id: str,
        task_data: Any,
        priority: int = 5,
        queue_name: str = "default",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """入队任务"""
        with self.lock:
            self.queues[queue_name].append({
                "task_id": task_id,
                "task_data": task_data,
                "priority": priority,
                "queued_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            })
            
            self.task_metadata[task_id] = {
                "queue_name": queue_name,
                "priority": priority,
                "status": "queued"
            }
            
            self.logger and self.logger.log_debug_message(
                "DistributedTaskQueue",
                f"Task enqueued: {task_id}",
                queue=queue_name,
                priority=priority
            )
            
            return True
    
    def dequeue(self, queue_name: str = "default", timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """出队任务"""
        with self.lock:
            if not self.queues[queue_name]:
                return None
            
            tasks = list(self.queues[queue_name])
            if not tasks:
                return None
            
            sorted_tasks = sorted(tasks, key=lambda t: t["priority"], reverse=True)
            task = sorted_tasks[0]
            
            self.queues[queue_name].remove(task)
            
            task_id = task["task_id"]
            self.task_metadata[task_id]["status"] = "dequeued"
            self.task_metadata[task_id]["dequeued_at"] = datetime.now().isoformat()
            
            return task
    
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """获取任务结果"""
        return self.task_results.get(task_id)
    
    def set_task_result(self, task_id: str, result: Any):
        """设置任务结果"""
        self.task_results[task_id] = {
            "result": result,
            "completed_at": datetime.now().isoformat()
        }
        if task_id in self.task_metadata:
            self.task_metadata[task_id]["status"] = "completed"
    
    def get_queue_stats(self, queue_name: str = "default") -> Dict[str, Any]:
        """获取队列统计"""
        with self.lock:
            tasks = list(self.queues[queue_name])
            return {
                "queue_name": queue_name,
                "size": len(tasks),
                "priorities": [t["priority"] for t in tasks]
            }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """获取所有队列统计"""
        return {
            queue_name: self.get_queue_stats(queue_name)
            for queue_name in self.queues.keys()
        }


class LoadBalancer:
    """
    负载均衡器 - 在多个节点间分配负载
    """
    
    def __init__(
        self,
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
        logger: Optional[CoreLoggerInterfaceContract] = None
    ):
        self.strategy = strategy
        self.logger = logger
        self.nodes: Dict[str, DistributedTaskNode] = {}
        self.round_robin_index = 0
        self.lock = threading.RLock()
    
    def add_node(self, node: DistributedTaskNode) -> bool:
        """添加节点"""
        with self.lock:
            if node.node_id in self.nodes:
                self.logger and self.logger.log_warning_message(
                    "LoadBalancer",
                    f"Node {node.node_id} already exists"
                )
                return False
            
            self.nodes[node.node_id] = node
            self.logger and self.logger.log_information_message(
                "LoadBalancer",
                f"Node added: {node.node_id}",
                endpoint=node.get_endpoint()
            )
            return True
    
    def remove_node(self, node_id: str) -> bool:
        """移除节点"""
        with self.lock:
            if node_id in self.nodes:
                del self.nodes[node_id]
                self.logger and self.logger.log_information_message(
                    "LoadBalancer",
                    f"Node removed: {node_id}"
                )
                return True
            return False
    
    def select_node(self, client_ip: Optional[str] = None) -> Optional[DistributedTaskNode]:
        """选择节点"""
        with self.lock:
            healthy_nodes = [n for n in self.nodes.values() if n.is_healthy()]
            
            if not healthy_nodes:
                return None
            
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                node = healthy_nodes[self.round_robin_index % len(healthy_nodes)]
                self.round_robin_index += 1
            
            elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
                node = min(healthy_nodes, key=lambda n: n.connections)
            
            elif self.strategy == LoadBalancingStrategy.WEIGHTED:
                total_weight = sum(n.weight for n in healthy_nodes)
                r = random.uniform(0, total_weight)
                cumsum = 0
                node = healthy_nodes[0]
                for n in healthy_nodes:
                    cumsum += n.weight
                    if cumsum >= r:
                        node = n
                        break
            
            elif self.strategy == LoadBalancingStrategy.IP_HASH:
                if client_ip:
                    hash_value = hash(client_ip) % len(healthy_nodes)
                    node = healthy_nodes[hash_value]
                else:
                    node = healthy_nodes[0]
            
            else:  # RANDOM
                node = random.choice(healthy_nodes)
            
            node.connections += 1
            return node
    
    def release_node(self, node_id: str, response_time: float, success: bool):
        """释放节点连接"""
        with self.lock:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                node.connections = max(0, node.connections - 1)
                node.update_stats(response_time, success)
    
    def get_nodes_status(self) -> List[Dict[str, Any]]:
        """获取所有节点状态"""
        with self.lock:
            return [
                {
                    "node_id": n.node_id,
                    "node_name": n.node_name,
                    "endpoint": n.get_endpoint(),
                    "status": n.status,
                    "connections": n.connections,
                    "total_requests": n.total_requests,
                    "failed_requests": n.failed_requests,
                    "error_rate": n.failed_requests / n.total_requests if n.total_requests > 0 else 0,
                    "avg_response_time": n.avg_response_time,
                    "is_healthy": n.is_healthy()
                }
                for n in self.nodes.values()
            ]


class DataConsistencyManager:
    """
    数据一致性管理器 - 管理分布式数据一致性
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.locks: Dict[str, Dict[str, Any]] = {}
        self.replicas: Dict[str, List[Any]] = defaultdict(list)
        self.lock = threading.RLock()
    
    def acquire_lock(
        self,
        resource_id: str,
        owner_id: str,
        timeout: float = 30.0
    ) -> bool:
        """获取分布式锁"""
        with self.lock:
            if resource_id not in self.locks:
                self.locks[resource_id] = {
                    "owner_id": owner_id,
                    "acquired_at": datetime.now().isoformat()
                }
                self.logger and self.logger.log_debug_message(
                    "DataConsistencyManager",
                    f"Lock acquired: {resource_id}",
                    owner=owner_id
                )
                return True
            
            lock_info = self.locks[resource_id]
            if lock_info["owner_id"] == owner_id:
                return True
            
            return False
    
    def release_lock(self, resource_id: str, owner_id: str) -> bool:
        """释放分布式锁"""
        with self.lock:
            if resource_id in self.locks:
                if self.locks[resource_id]["owner_id"] == owner_id:
                    del self.locks[resource_id]
                    self.logger and self.logger.log_debug_message(
                        "DataConsistencyManager",
                        f"Lock released: {resource_id}"
                    )
                    return True
            return False
    
    def replicate_data(
        self,
        data_id: str,
        data: Any,
        replicas_count: int = 3
    ) -> bool:
        """复制数据"""
        with self.lock:
            self.replicas[data_id] = [data] * replicas_count
            self.logger and self.logger.log_information_message(
                "DataConsistencyManager",
                f"Data replicated: {data_id}",
                replicas=replicas_count
            )
            return True
    
    def get_replicated_data(self, data_id: str) -> Optional[Any]:
        """获取复制的数据"""
        with self.lock:
            replicas = self.replicas.get(data_id, [])
            if replicas:
                return replicas[0]
            return None
    
    def verify_consistency(self, data_id: str) -> Dict[str, Any]:
        """验证数据一致性"""
        with self.lock:
            replicas = self.replicas.get(data_id, [])
            
            if not replicas:
                return {"status": "no_data", "consistent": None}
            
            all_same = all(r == replicas[0] for r in replicas)
            
            return {
                "status": "consistent" if all_same else "inconsistent",
                "consistent": all_same,
                "replicas_count": len(replicas),
                "checked_at": datetime.now().isoformat()
            }


class ServiceRegistry:
    """
    服务注册中心 - 管理服务实例注册和发现
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.services: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.lock = threading.RLock()
    
    def register_service(
        self,
        service_name: str,
        service_id: str,
        host: str,
        port: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """注册服务"""
        with self.lock:
            service_info = {
                "service_id": service_id,
                "host": host,
                "port": port,
                "metadata": metadata or {},
                "registered_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat()
            }
            
            existing = [
                i for i, s in enumerate(self.services[service_name])
                if s["service_id"] == service_id
            ]
            
            if existing:
                self.services[service_name][existing[0]] = service_info
            else:
                self.services[service_name].append(service_info)
            
            self.logger and self.logger.log_information_message(
                "ServiceRegistry",
                f"Service registered: {service_name}",
                service_id=service_id
            )
            return True
    
    def unregister_service(self, service_name: str, service_id: str) -> bool:
        """注销服务"""
        with self.lock:
            self.services[service_name] = [
                s for s in self.services[service_name]
                if s["service_id"] != service_id
            ]
            self.logger and self.logger.log_information_message(
                "ServiceRegistry",
                f"Service unregistered: {service_name}",
                service_id=service_id
            )
            return True
    
    def discover_services(self, service_name: str) -> List[Dict[str, Any]]:
        """发现服务"""
        with self.lock:
            return self.services.get(service_name, []).copy()
    
    def heartbeat(self, service_name: str, service_id: str) -> bool:
        """发送心跳"""
        with self.lock:
            for service in self.services[service_name]:
                if service["service_id"] == service_id:
                    service["last_heartbeat"] = datetime.now().isoformat()
                    return True
            return False


__all__ = [
    "LoadBalancingStrategy",
    "DistributedTaskNode",
    "DistributedTaskQueue",
    "LoadBalancer",
    "DataConsistencyManager",
    "ServiceRegistry"
]
