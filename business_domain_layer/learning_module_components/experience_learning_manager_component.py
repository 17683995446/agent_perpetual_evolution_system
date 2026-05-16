"""
Experience Learning Manager Component - 经验学习管理器组件
负责收集、存储和利用任务执行经验
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import json

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class ExperienceLearningManagerComponent:
    """
    Experience Learning Manager Component - 经验学习管理器组件
    
    负责收集、存储和利用任务执行经验
    支持经验记录、相似度匹配和学习改进
    """
    
    def __init__(self, storage_backend: CoreStorageInterfaceContract, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Experience Learning Manager Component - 初始化经验学习管理器组件
        
        Args:
            storage_backend: 存储后端实例
            logger_backend: 日志后端实例
        """
        self.storage_backend = storage_backend
        self.logger_backend = logger_backend
        self.experience_cache = {}
    
    def record_execution_experience(
        self,
        task_id: str,
        execution_result: Dict[str, Any],
        execution_plan: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record Execution Experience - 记录执行经验
        
        Args:
            task_id: 任务ID
            execution_result: 执行结果
            execution_plan: 执行计划
            metadata: 可选的元数据
            
        Returns:
            经验记录ID
        """
        experience_id = str(uuid.uuid4())
        
        experience_record = {
            'experience_id': experience_id,
            'task_id': task_id,
            'execution_result': execution_result,
            'execution_plan': execution_plan,
            'metadata': metadata or {},
            'recorded_at': datetime.now(),
            'success': execution_result.get('success', False),
            'duration_seconds': execution_result.get('total_duration_seconds', 0)
        }
        
        # 保存经验记录
        self._store_experience(experience_id, experience_record)
        
        # 缓存经验
        self.experience_cache[experience_id] = experience_record
        
        self.logger_backend.log_information_message(
            'ExperienceLearningManagerComponent',
            f'Execution experience recorded for task: {task_id}',
            task_id=task_id,
            experience_id=experience_id,
            success=experience_record['success']
        )
        
        return experience_id
    
    def find_similar_execution_experiences(
        self,
        task_metadata: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find Similar Execution Experiences - 查找相似的执行经验
        
        Args:
            task_metadata: 任务元数据
            limit: 返回结果数量限制
            
        Returns:
            相似经验列表
        """
        self.logger_backend.log_debug_message(
            'ExperienceLearningManagerComponent',
            'Searching for similar execution experiences',
            task_metadata=task_metadata
        )
        
        # 获取所有经验记录
        all_experiences = self._get_all_experiences()
        
        # 简单的相似度匹配
        similar_experiences = []
        for exp in all_experiences:
            similarity_score = self._calculate_similarity_score(task_metadata, exp)
            if similarity_score > 0:
                exp['similarity_score'] = similarity_score
                similar_experiences.append(exp)
        
        # 按相似度排序
        similar_experiences.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        result = similar_experiences[:limit]
        
        self.logger_backend.log_information_message(
            'ExperienceLearningManagerComponent',
            f'Found {len(result)} similar execution experiences',
            count=len(result)
        )
        
        return result
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get Learning Insights - 获取学习洞察
        
        Returns:
            学习洞察字典
        """
        all_experiences = self._get_all_experiences()
        
        total_experiences = len(all_experiences)
        successful = sum(1 for exp in all_experiences if exp.get('success', False))
        failed = total_experiences - successful
        
        avg_duration = 0
        if total_experiences > 0:
            avg_duration = sum(exp.get('duration_seconds', 0) for exp in all_experiences) / total_experiences
        
        insights = {
            'total_experiences': total_experiences,
            'successful_count': successful,
            'failed_count': failed,
            'success_rate': successful / total_experiences if total_experiences > 0 else 0,
            'average_duration_seconds': avg_duration,
            'generated_at': datetime.now()
        }
        
        self.logger_backend.log_information_message(
            'ExperienceLearningManagerComponent',
            'Learning insights generated',
            insights=insights
        )
        
        return insights
    
    def get_experience_by_id(self, experience_id: str) -> Optional[Dict[str, Any]]:
        """
        Get Experience By ID - 根据ID获取经验
        
        Args:
            experience_id: 经验ID
            
        Returns:
            经验记录，如果没有则返回None
        """
        # 先查缓存
        if experience_id in self.experience_cache:
            return self.experience_cache[experience_id]
        
        # 从存储获取
        experience = self._retrieve_experience(experience_id)
        if experience:
            self.experience_cache[experience_id] = experience
        
        return experience
    
    def _calculate_similarity_score(self, task_metadata: Dict[str, Any], experience: Dict[str, Any]) -> float:
        """
        Calculate Similarity Score - 计算相似度分数
        
        Args:
            task_metadata: 任务元数据
            experience: 经验记录
            
        Returns:
            相似度分数 (0-1)
        """
        # 简化的相似度计算
        score = 0.0
        
        # 匹配成功经验
        if experience.get('success', False):
            score += 0.3
        
        # 可以根据更多特征计算相似度
        # 这里简化处理
        
        return score
    
    def _store_experience(self, experience_id: str, experience_data: Dict[str, Any]):
        """
        Store Experience - 存储经验数据
        """
        # 在实际实现中，这里会使用存储后端保存数据
        # 这里简化处理
        pass
    
    def _retrieve_experience(self, experience_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve Experience - 检索经验数据
        """
        # 在实际实现中，这里会从存储后端获取数据
        # 这里简化处理
        return None
    
    def _get_all_experiences(self) -> List[Dict[str, Any]]:
        """
        Get All Experiences - 获取所有经验数据
        """
        # 在实际实现中，这里会查询存储后端
        # 这里简化处理
        return list(self.experience_cache.values())
    
    def extract_and_store_experience(self, task_id: str, execution_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract And Store Experience - 提取并存储经验
        
        Args:
            task_id: 任务ID
            execution_result: 执行结果
            
        Returns:
            经验字典，如果没有提取到则返回None
        """
        if not execution_result:
            return None
        
        experience = {
            'task_id': task_id,
            'success': execution_result.get('success', False),
            'duration': execution_result.get('total_duration_seconds', 0),
            'subtask_count': execution_result.get('total_steps_executed', 0),
            'extracted_at': datetime.now().isoformat()
        }
        
        experience_id = self.record_execution_experience(
            task_id=task_id,
            execution_result=execution_result,
            execution_plan={}
        )
        
        experience['experience_id'] = experience_id
        
        self.logger_backend.log_information_message(
            'ExperienceLearningManagerComponent',
            f'Experience extracted and stored for task: {task_id}',
            task_id=task_id,
            experience_id=experience_id
        )
        
        return experience


__all__ = ['ExperienceLearningManagerComponent']
