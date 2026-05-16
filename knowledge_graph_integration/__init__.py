"""
Knowledge Graph Integration Module - 知识图谱集成模块
提供知识图谱、经验提取、任务关系分析等知识管理功能
"""

from .knowledge_graph_components import (
    NodeType,
    RelationshipType,
    KnowledgeGraphNode,
    KnowledgeGraphEdge,
    KnowledgeGraph,
    ExperienceKnowledgeExtractor,
    TaskRelationAnalyzer,
    IntelligentRecommendationEngine
)

__version__ = "1.0.0"

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
