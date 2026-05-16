"""
Multi-Agent Collaboration Framework - 多智能体协作框架
提供智能体定义、通信、协作和任务分配功能
"""

import uuid
import time
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
from collections import defaultdict, deque

from ..core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class AgentStatus(Enum):
    """智能体状态"""
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class MessageType(Enum):
    """消息类型"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    HEARTBEAT = "heartbeat"
    COORDINATION = "coordination"
    TERMINATION = "termination"


class BaseAgent:
    """
    基础智能体 - 所有智能体的基类
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        capabilities: List[str],
        logger: Optional[CoreLoggerInterfaceContract] = None
    ):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.logger = logger
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_execution_time": 0.0,
            "success_rate": 1.0
        }
        self.metadata = {}
        self.created_at = datetime.now().isoformat()
    
    def get_status(self) -> Dict[str, Any]:
        """获取智能体状态"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "performance_metrics": self.performance_metrics
        }
    
    def update_performance(self, success: bool, execution_time: float):
        """更新性能指标"""
        total = self.performance_metrics["tasks_completed"] + self.performance_metrics["tasks_failed"]
        
        if success:
            self.performance_metrics["tasks_completed"] += 1
        else:
            self.performance_metrics["tasks_failed"] += 1
        
        total = self.performance_metrics["tasks_completed"] + self.performance_metrics["tasks_failed"]
        if total > 0:
            self.performance_metrics["success_rate"] = self.performance_metrics["tasks_completed"] / total
        
        current_avg = self.performance_metrics["avg_execution_time"]
        count = self.performance_metrics["tasks_completed"] + self.performance_metrics["tasks_failed"]
        self.performance_metrics["avg_execution_time"] = (
            (current_avg * (count - 1) + execution_time) / count if count > 0 else execution_time
        )
    
    def has_capability(self, capability: str) -> bool:
        """检查是否具有某项能力"""
        return capability in self.capabilities


class AgentMessage:
    """
    智能体消息 - 智能体间通信的消息格式
    """
    
    def __init__(
        self,
        message_id: str,
        sender_id: str,
        receiver_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: int = 5
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type
        self.content = content
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
        self.delivered = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type.value,
            "content": self.content,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "delivered": self.delivered
        }


class AgentCommunicationProtocol:
    """
    智能体通信协议 - 管理智能体间的消息传递
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.message_queue = deque(maxlen=10000)
        self.agents: Dict[str, BaseAgent] = {}
        self.message_handlers: Dict[MessageType, List[Callable]] = defaultdict(list)
    
    def register_agent(self, agent: BaseAgent) -> bool:
        """注册智能体"""
        if agent.agent_id in self.agents:
            self.logger and self.logger.log_warning_message(
                "AgentCommunicationProtocol",
                f"Agent {agent.agent_id} already registered"
            )
            return False
        
        self.agents[agent.agent_id] = agent
        self.logger and self.logger.log_information_message(
            "AgentCommunicationProtocol",
            f"Agent registered: {agent.agent_id}"
        )
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """注销智能体"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger and self.logger.log_information_message(
                "AgentCommunicationProtocol",
                f"Agent unregistered: {agent_id}"
            )
            return True
        return False
    
    def send_message(self, message: AgentMessage) -> bool:
        """发送消息"""
        self.message_queue.append(message)
        self.logger and self.logger.log_debug_message(
            "AgentCommunicationProtocol",
            f"Message sent: {message.message_id}",
            sender=message.sender_id,
            receiver=message.receiver_id
        )
        return True
    
    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """获取某智能体的消息"""
        messages = [
            msg for msg in self.message_queue
            if msg.receiver_id == agent_id and not msg.delivered
        ]
        for msg in messages:
            msg.delivered = True
        return messages
    
    def broadcast_message(self, sender_id: str, message_type: MessageType, content: Dict[str, Any]):
        """广播消息给所有智能体"""
        for agent_id in self.agents:
            if agent_id != sender_id:
                message = AgentMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id=sender_id,
                    receiver_id=agent_id,
                    message_type=message_type,
                    content=content
                )
                self.send_message(message)


class TaskAllocationAlgorithm:
    """
    任务分配算法 - 智能分配任务给合适的智能体
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
    
    def allocate_by_capability(
        self,
        task_requirements: List[str],
        available_agents: List[BaseAgent]
    ) -> Optional[BaseAgent]:
        """基于能力分配任务"""
        capable_agents = [
            agent for agent in available_agents
            if agent.status == AgentStatus.IDLE
            and all(agent.has_capability(req) for req in task_requirements)
        ]
        
        if not capable_agents:
            return None
        
        return min(capable_agents, key=lambda a: a.performance_metrics["tasks_completed"])
    
    def allocate_by_load(
        self,
        available_agents: List[BaseAgent]
    ) -> Optional[BaseAgent]:
        """基于负载分配任务"""
        idle_agents = [a for a in available_agents if a.status == AgentStatus.IDLE]
        
        if not idle_agents:
            return None
        
        return min(idle_agents, key=lambda a: a.performance_metrics["tasks_completed"])
    
    def allocate_by_success_rate(
        self,
        available_agents: List[BaseAgent]
    ) -> Optional[BaseAgent]:
        """基于成功率分配任务"""
        idle_agents = [a for a in available_agents if a.status == AgentStatus.IDLE]
        
        if not idle_agents:
            return None
        
        return max(idle_agents, key=lambda a: a.performance_metrics["success_rate"])
    
    def allocate_balanced(
        self,
        task_requirements: List[str],
        available_agents: List[BaseAgent]
    ) -> Optional[BaseAgent]:
        """平衡分配策略"""
        capable_agents = [
            agent for agent in available_agents
            if agent.status == AgentStatus.IDLE
            and all(agent.has_capability(req) for req in task_requirements)
        ]
        
        if not capable_agents:
            capable_agents = [
                agent for agent in available_agents
                if agent.status == AgentStatus.IDLE
            ]
        
        if not capable_agents:
            return None
        
        scores = []
        for agent in capable_agents:
            success_score = agent.performance_metrics["success_rate"] * 0.4
            load_score = (1.0 - agent.performance_metrics["tasks_completed"] / 100) * 0.3
            speed_score = (1.0 / (agent.performance_metrics["avg_execution_time"] + 0.01)) * 0.3
            total_score = success_score + load_score + speed_score
            scores.append((agent, total_score))
        
        return max(scores, key=lambda x: x[1])[0]


class CollaborativeExecutionEngine:
    """
    协作执行引擎 - 管理多智能体协作执行
    """
    
    def __init__(
        self,
        communication: AgentCommunicationProtocol,
        task_allocator: TaskAllocationAlgorithm,
        logger: Optional[CoreLoggerInterfaceContract] = None
    ):
        self.communication = communication
        self.task_allocator = task_allocator
        self.logger = logger
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_results: Dict[str, Dict[str, Any]] = {}
    
    def submit_collaborative_task(
        self,
        task_id: str,
        task_input: str,
        requirements: List[str],
        collaborators_needed: int = 1
    ) -> Dict[str, Any]:
        """提交协作任务"""
        available_agents = list(self.communication.agents.values())
        
        selected_agents = []
        for _ in range(collaborators_needed):
            agent = self.task_allocator.allocate_balanced(requirements, available_agents)
            if agent:
                selected_agents.append(agent)
                available_agents.remove(agent)
        
        if not selected_agents:
            return {
                "success": False,
                "error": "No available agents"
            }
        
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "task_input": task_input,
            "requirements": requirements,
            "assigned_agents": [a.agent_id for a in selected_agents],
            "status": "in_progress",
            "started_at": datetime.now().isoformat()
        }
        
        for agent in selected_agents:
            agent.status = AgentStatus.BUSY
            message = AgentMessage(
                message_id=str(uuid.uuid4()),
                sender_id="coordinator",
                receiver_id=agent.agent_id,
                message_type=MessageType.TASK_REQUEST,
                content={
                    "task_id": task_id,
                    "task_input": task_input,
                    "collaborators": [a.agent_id for a in selected_agents if a.agent_id != agent.agent_id]
                }
            )
            self.communication.send_message(message)
        
        return {
            "success": True,
            "task_id": task_id,
            "assigned_agents": [a.agent_id for a in selected_agents],
            "collaborator_count": len(selected_agents)
        }
    
    def receive_task_result(
        self,
        task_id: str,
        agent_id: str,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """接收任务结果"""
        if task_id not in self.active_tasks:
            return {"success": False, "error": "Task not found"}
        
        agent = self.communication.agents.get(agent_id)
        if agent:
            agent.status = AgentStatus.IDLE
        
        if task_id not in self.task_results:
            self.task_results[task_id] = {
                "task_id": task_id,
                "results": [],
                "completed_agents": []
            }
        
        self.task_results[task_id]["results"].append({
            "agent_id": agent_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        self.task_results[task_id]["completed_agents"].append(agent_id)
        
        if len(self.task_results[task_id]["completed_agents"]) >= len(self.active_tasks[task_id]["assigned_agents"]):
            self.active_tasks[task_id]["status"] = "completed"
        
        return {
            "success": True,
            "task_id": task_id,
            "progress": f"{len(self.task_results[task_id]['completed_agents'])}/{len(self.active_tasks[task_id]['assigned_agents'])}"
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)
    
    def get_collaboration_summary(self) -> Dict[str, Any]:
        """获取协作摘要"""
        total_tasks = len(self.active_tasks)
        completed_tasks = sum(1 for t in self.active_tasks.values() if t["status"] == "completed")
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": total_tasks - completed_tasks,
            "total_results_received": len(self.task_results),
            "active_agents": sum(1 for a in self.communication.agents.values() if a.status == AgentStatus.BUSY)
        }


__all__ = [
    "AgentStatus",
    "MessageType",
    "BaseAgent",
    "AgentMessage",
    "AgentCommunicationProtocol",
    "TaskAllocationAlgorithm",
    "CollaborativeExecutionEngine"
]
