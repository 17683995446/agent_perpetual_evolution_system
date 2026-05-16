"""
Knowledge Graph Integration Module - 知识图谱集成模块
提供知识图谱、经验提取、任务关系分析等知识管理功能
"""

import uuid
import time
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime
from enum import Enum
from collections import defaultdict, deque

from ..core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class NodeType(Enum):
    """图谱节点类型"""
    TASK = "task"
    AGENT = "agent"
    EXPERIENCE = "experience"
    CONCEPT = "concept"
    RESOURCE = "resource"


class RelationshipType(Enum):
    """关系类型"""
    DEPENDS_ON = "depends_on"
    SIMILAR_TO = "similar_to"
    EXECUTES = "executes"
    LEARNS_FROM = "learns_from"
    REQUIRES = "requires"
    PRODUCE = "produce"
    SUCCEEDED_BY = "succeeded_by"


class KnowledgeGraphNode:
    """
    知识图谱节点 - 表示图谱中的实体
    """
    
    def __init__(
        self,
        node_id: str,
        node_type: NodeType,
        name: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        self.node_id = node_id
        self.node_type = node_type
        self.name = name
        self.properties = properties or {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.embedding = None
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "name": self.name,
            "properties": self.properties,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class KnowledgeGraphEdge:
    """
    知识图谱边 - 表示节点之间的关系
    """
    
    def __init__(
        self,
        edge_id: str,
        source_node_id: str,
        target_node_id: str,
        relationship_type: RelationshipType,
        weight: float = 1.0,
        properties: Optional[Dict[str, Any]] = None
    ):
        self.edge_id = edge_id
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id
        self.relationship_type = relationship_type
        self.weight = weight
        self.properties = properties or {}
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "edge_id": self.edge_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "relationship_type": self.relationship_type.value,
            "weight": self.weight,
            "properties": self.properties,
            "created_at": self.created_at
        }


class KnowledgeGraph:
    """
    知识图谱 - 管理知识节点和关系
    """
    
    def __init__(self, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.logger = logger
        self.nodes: Dict[str, KnowledgeGraphNode] = {}
        self.edges: List[KnowledgeGraphEdge] = []
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adjacency: Dict[str, List[str]] = defaultdict(list)
        self.node_index: Dict[str, List[str]] = defaultdict(list)
    
    def add_node(self, node: KnowledgeGraphNode) -> bool:
        """添加节点"""
        if node.node_id in self.nodes:
            self.logger and self.logger.log_warning_message(
                "KnowledgeGraph",
                f"Node {node.node_id} already exists"
            )
            return False
        
        self.nodes[node.node_id] = node
        self.node_index[node.node_type.value].append(node.node_id)
        
        self.logger and self.logger.log_information_message(
            "KnowledgeGraph",
            f"Node added: {node.node_id}"
        )
        return True
    
    def add_edge(self, edge: KnowledgeGraphEdge) -> bool:
        """添加边"""
        if edge.source_node_id not in self.nodes or edge.target_node_id not in self.nodes:
            self.logger and self.logger.log_error_message(
                "KnowledgeGraph",
                "Cannot add edge: node not found"
            )
            return False
        
        self.edges.append(edge)
        self.adjacency_list[edge.source_node_id].append(edge.target_node_id)
        self.reverse_adjacency[edge.target_node_id].append(edge.source_node_id)
        
        self.logger and self.logger.log_information_message(
            "KnowledgeGraph",
            f"Edge added: {edge.source_node_id} -> {edge.target_node_id}"
        )
        return True
    
    def get_node(self, node_id: str) -> Optional[KnowledgeGraphNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_neighbors(self, node_id: str, relationship_type: Optional[RelationshipType] = None) -> List[KnowledgeGraphNode]:
        """获取邻居节点"""
        if node_id not in self.nodes:
            return []
        
        neighbors = []
        for edge in self.edges:
            if edge.source_node_id == node_id:
                if relationship_type is None or edge.relationship_type == relationship_type:
                    neighbor = self.nodes.get(edge.target_node_id)
                    if neighbor:
                        neighbors.append(neighbor)
        
        return neighbors
    
    def find_path(self, start_node_id: str, end_node_id: str) -> Optional[List[str]]:
        """查找路径（BFS）"""
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            return None
        
        queue = deque([(start_node_id, [start_node_id])])
        visited = {start_node_id}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end_node_id:
                return path
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_subgraph(self, node_id: str, depth: int = 2) -> Dict[str, Any]:
        """获取子图"""
        if node_id not in self.nodes:
            return {}
        
        visited = {node_id}
        queue = deque([(node_id, 0)])
        subgraph_nodes = [node_id]
        subgraph_edges = []
        
        while queue:
            current, current_depth = queue.popleft()
            
            if current_depth >= depth:
                continue
            
            for edge in self.edges:
                if edge.source_node_id == current and edge.target_node_id not in visited:
                    visited.add(edge.target_node_id)
                    subgraph_nodes.append(edge.target_node_id)
                    subgraph_edges.append(edge)
                    queue.append((edge.target_node_id, current_depth + 1))
                
                if edge.target_node_id == current and edge.source_node_id not in visited:
                    visited.add(edge.source_node_id)
                    subgraph_nodes.append(edge.source_node_id)
                    subgraph_edges.append(edge)
                    queue.append((edge.source_node_id, current_depth + 1))
        
        return {
            "nodes": subgraph_nodes,
            "edges": [e.edge_id for e in subgraph_edges],
            "depth": depth
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取图谱统计"""
        node_types = defaultdict(int)
        relationship_types = defaultdict(int)
        
        for node in self.nodes.values():
            node_types[node.node_type.value] += 1
        
        for edge in self.edges:
            relationship_types[edge.relationship_type.value] += 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": dict(node_types),
            "relationship_types": dict(relationship_types),
            "avg_degree": len(self.edges) * 2 / len(self.nodes) if self.nodes else 0
        }


class ExperienceKnowledgeExtractor:
    """
    经验知识提取器 - 从执行历史中提取知识
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.knowledge_graph = knowledge_graph
        self.logger = logger
        self.pattern_cache = deque(maxlen=1000)
    
    def extract_from_execution(
        self,
        task_id: str,
        task_input: str,
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """从执行结果中提取知识"""
        task_node = KnowledgeGraphNode(
            node_id=task_id,
            node_type=NodeType.TASK,
            name=f"Task: {task_input[:50]}",
            properties={
                "input": task_input,
                "success": execution_result.get("success", False),
                "duration": execution_result.get("duration", 0)
            }
        )
        self.knowledge_graph.add_node(task_node)
        
        concepts = self._extract_concepts(task_input)
        concept_nodes = []
        for concept in concepts:
            concept_id = f"concept_{uuid.uuid4().hex[:8]}"
            concept_node = KnowledgeGraphNode(
                node_id=concept_id,
                node_type=NodeType.CONCEPT,
                name=concept,
                properties={"source": "extraction", "task_id": task_id}
            )
            self.knowledge_graph.add_node(concept_node)
            concept_nodes.append(concept_node)
            
            edge = KnowledgeGraphEdge(
                edge_id=str(uuid.uuid4()),
                source_node_id=task_id,
                target_node_id=concept_id,
                relationship_type=RelationshipType.LEARNS_FROM
            )
            self.knowledge_graph.add_edge(edge)
        
        self.pattern_cache.append({
            "task_id": task_id,
            "concepts": concepts,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "task_node": task_node.to_dict(),
            "concept_nodes": [n.to_dict() for n in concept_nodes],
            "concepts": concepts
        }
    
    def _extract_concepts(self, text: str) -> List[str]:
        """提取概念（简单实现）"""
        keywords = [
            "analyze", "create", "update", "delete", "search",
            "process", "execute", "manage", "optimize", "review"
        ]
        
        text_lower = text.lower()
        found_concepts = [kw for kw in keywords if kw in text_lower]
        
        if not found_concepts:
            found_concepts = ["general"]
        
        return found_concepts
    
    def find_similar_experiences(self, task_input: str, limit: int = 5) -> List[Dict[str, Any]]:
        """查找相似的经验"""
        current_concepts = set(self._extract_concepts(task_input))
        
        similarities = []
        for pattern in self.pattern_cache:
            pattern_concepts = set(pattern.get("concepts", []))
            if not pattern_concepts:
                continue
            
            intersection = len(current_concepts & pattern_concepts)
            union = len(current_concepts | pattern_concepts)
            similarity = intersection / union if union > 0 else 0
            
            similarities.append({
                "task_id": pattern["task_id"],
                "similarity": similarity,
                "concepts": pattern.get("concepts", []),
                "timestamp": pattern["timestamp"]
            })
        
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:limit]


class TaskRelationAnalyzer:
    """
    任务关系分析器 - 分析任务间的关系
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.knowledge_graph = knowledge_graph
        self.logger = logger
    
    def calculate_similarity(self, task1_input: str, task2_input: str) -> float:
        """计算两个任务的相似度"""
        words1 = set(task1_input.lower().split())
        words2 = set(task2_input.lower().split())
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_dependencies(self, task_id: str) -> List[str]:
        """查找任务依赖"""
        dependencies = []
        
        for edge in self.knowledge_graph.edges:
            if edge.target_node_id == task_id and edge.relationship_type == RelationshipType.DEPENDS_ON:
                dependencies.append(edge.source_node_id)
        
        return dependencies
    
    def suggest_execution_order(self, task_ids: List[str]) -> List[str]:
        """建议执行顺序"""
        graph = self.knowledge_graph
        
        in_degree = defaultdict(int)
        for task_id in task_ids:
            in_degree[task_id] = 0
        
        for edge in graph.edges:
            if edge.source_node_id in task_ids and edge.target_node_id in task_ids:
                if edge.relationship_type == RelationshipType.DEPENDS_ON:
                    in_degree[edge.target_node_id] += 1
        
        queue = deque([tid for tid in task_ids if in_degree[tid] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in graph.adjacency_list.get(current, []):
                if neighbor in task_ids:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        
        return result if len(result) == len(task_ids) else task_ids


class IntelligentRecommendationEngine:
    """
    智能推荐引擎 - 基于知识图谱提供智能推荐
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph, logger: Optional[CoreLoggerInterfaceContract] = None):
        self.knowledge_graph = knowledge_graph
        self.logger = logger
        self.recommendation_history = deque(maxlen=1000)
    
    def recommend_next_task(self, completed_task_id: str) -> Optional[Dict[str, Any]]:
        """推荐下一个任务"""
        neighbors = self.knowledge_graph.get_neighbors(
            completed_task_id,
            RelationshipType.SUCCEEDED_BY
        )
        
        if not neighbors:
            similar_tasks = self._find_similar_tasks(completed_task_id)
            if similar_tasks:
                return {
                    "type": "similar_task",
                    "recommendation": similar_tasks[0],
                    "confidence": 0.7
                }
            return None
        
        best_next = max(neighbors, key=lambda n: n.properties.get("success_rate", 0.5))
        
        return {
            "type": "recommended_next",
            "task_id": best_next.node_id,
            "task_name": best_next.name,
            "confidence": 0.85,
            "reason": "Based on workflow pattern"
        }
    
    def recommend_optimization(self, task_id: str) -> List[Dict[str, Any]]:
        """推荐优化策略"""
        recommendations = []
        
        task_node = self.knowledge_graph.get_node(task_id)
        if not task_node:
            return recommendations
        
        dependencies = self.knowledge_graph.get_neighbors(task_id, RelationshipType.DEPENDS_ON)
        if len(dependencies) > 5:
            recommendations.append({
                "type": "dependency_optimization",
                "message": "Too many dependencies, consider parallelizing",
                "priority": "high"
            })
        
        neighbors = self.knowledge_graph.get_neighbors(task_id, RelationshipType.SIMILAR_TO)
        if len(neighbors) > 0:
            avg_duration = sum(n.properties.get("duration", 0) for n in neighbors) / len(neighbors)
            if task_node.properties.get("duration", 0) > avg_duration * 1.5:
                recommendations.append({
                    "type": "performance_optimization",
                    "message": "Task duration is higher than similar tasks",
                    "priority": "medium",
                    "avg_duration": avg_duration
                })
        
        return recommendations
    
    def _find_similar_tasks(self, task_id: str) -> List[Dict[str, Any]]:
        """查找相似任务"""
        task_node = self.knowledge_graph.get_node(task_id)
        if not task_node:
            return []
        
        similar_tasks = []
        for node in self.knowledge_graph.nodes.values():
            if node.node_type == NodeType.TASK and node.node_id != task_id:
                similarity = self.knowledge_graph.calculate_similarity(
                    task_node.properties.get("input", ""),
                    node.properties.get("input", "")
                )
                if similarity > 0.5:
                    similar_tasks.append({
                        "task_id": node.node_id,
                        "name": node.name,
                        "similarity": similarity
                    })
        
        similar_tasks.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_tasks[:3]


__all__ = [
    "NodeType",
    "RelationshipType",
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "KnowledgeGraph",
    "ExperienceKnowledgeExtractor",
    "TaskRelationAnalyzer",
    "IntelligentRecommendationEngine"
]
