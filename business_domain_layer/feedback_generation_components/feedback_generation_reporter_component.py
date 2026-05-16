"""
Feedback Generation Reporter Component - 反馈生成报告器组件
负责生成任务执行反馈和报告
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class FeedbackGenerationReporterComponent:
    """
    Feedback Generation Reporter Component - 反馈生成报告器组件
    
    负责生成任务执行反馈和报告
    支持多种报告格式和详细程度
    """
    
    def __init__(self, logger_backend: CoreLoggerInterfaceContract):
        """
        Initialize Feedback Generation Reporter Component - 初始化反馈生成报告器组件
        
        Args:
            logger_backend: 日志后端实例
        """
        self.logger_backend = logger_backend
    
    def generate_execution_feedback(
        self,
        task_id: str,
        execution_result: Dict[str, Any],
        execution_plan: Dict[str, Any],
        detail_level: str = 'standard'
    ) -> Dict[str, Any]:
        """
        Generate Execution Feedback - 生成执行反馈
        
        Args:
            task_id: 任务ID
            execution_result: 执行结果
            execution_plan: 执行计划
            detail_level: 详细程度 ('brief', 'standard', 'detailed')
            
        Returns:
            反馈数据字典
        """
        feedback_id = str(uuid.uuid4())
        
        self.logger_backend.log_information_message(
            'FeedbackGenerationReporterComponent',
            f'Generating execution feedback for task: {task_id}',
            task_id=task_id,
            detail_level=detail_level
        )
        
        # 基础反馈信息
        feedback = {
            'feedback_id': feedback_id,
            'task_id': task_id,
            'generated_at': datetime.now(),
            'success': execution_result.get('success', False),
            'detail_level': detail_level
        }
        
        # 根据详细程度添加不同的信息
        if detail_level in ['standard', 'detailed']:
            feedback['duration_seconds'] = execution_result.get('total_duration_seconds', 0)
            feedback['steps_executed'] = execution_result.get('total_steps_executed', 0)
        
        if detail_level == 'detailed':
            feedback['execution_plan'] = execution_plan
            feedback['execution_result'] = execution_result
            feedback['recommendations'] = self._generate_recommendations(execution_result, execution_plan)
        
        self.logger_backend.log_information_message(
            'FeedbackGenerationReporterComponent',
            f'Execution feedback generated: {feedback_id}',
            feedback_id=feedback_id
        )
        
        return feedback
    
    def generate_summary_report(
        self,
        task_results: List[Dict[str, Any]],
        time_range: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """
        Generate Summary Report - 生成摘要报告
        
        Args:
            task_results: 任务结果列表
            time_range: 可选的时间范围
            
        Returns:
            摘要报告字典
        """
        self.logger_backend.log_information_message(
            'FeedbackGenerationReporterComponent',
            'Generating summary report',
            task_count=len(task_results)
        )
        
        total_tasks = len(task_results)
        successful = sum(1 for res in task_results if res.get('success', False))
        failed = total_tasks - successful
        
        total_duration = sum(res.get('total_duration_seconds', 0) for res in task_results)
        avg_duration = total_duration / total_tasks if total_tasks > 0 else 0
        
        report = {
            'report_id': str(uuid.uuid4()),
            'generated_at': datetime.now(),
            'summary': {
                'total_tasks': total_tasks,
                'successful_count': successful,
                'failed_count': failed,
                'success_rate': successful / total_tasks if total_tasks > 0 else 0,
                'total_duration_seconds': total_duration,
                'average_duration_seconds': avg_duration
            },
            'time_range': time_range
        }
        
        self.logger_backend.log_information_message(
            'FeedbackGenerationReporterComponent',
            f'Summary report generated: {report["report_id"]}',
            report_id=report['report_id']
        )
        
        return report
    
    def format_feedback_for_display(
        self,
        feedback: Dict[str, Any],
        format_type: str = 'text'
    ) -> str:
        """
        Format Feedback For Display - 格式化反馈用于显示
        
        Args:
            feedback: 反馈数据
            format_type: 格式类型 ('text', 'json', 'html')
            
        Returns:
            格式化的反馈字符串
        """
        if format_type == 'json':
            import json
            return json.dumps(feedback, indent=2, default=str)
        elif format_type == 'html':
            return self._format_as_html(feedback)
        else:
            return self._format_as_text(feedback)
    
    def _generate_recommendations(
        self,
        execution_result: Dict[str, Any],
        execution_plan: Dict[str, Any]
    ) -> List[str]:
        """
        Generate Recommendations - 生成改进建议
        
        Args:
            execution_result: 执行结果
            execution_plan: 执行计划
            
        Returns:
            建议列表
        """
        recommendations = []
        
        # 基于执行结果生成建议
        if not execution_result.get('success', False):
            recommendations.append("Review the error details and retry the task")
            recommendations.append("Check dependencies and prerequisites")
        
        duration = execution_result.get('total_duration_seconds', 0)
        if duration > 60:  # 超过1分钟
            recommendations.append("Consider optimizing the execution plan for faster performance")
        
        steps = execution_result.get('total_steps_executed', 0)
        if steps > 20:
            recommendations.append("Consider breaking down the task into smaller subtasks")
        
        return recommendations
    
    def _format_as_text(self, feedback: Dict[str, Any]) -> str:
        """
        Format As Text - 格式化为文本
        
        Args:
            feedback: 反馈数据
            
        Returns:
            文本格式的反馈
        """
        lines = []
        lines.append(f"=== Execution Feedback - {feedback['feedback_id']} ===")
        lines.append(f"Task ID: {feedback['task_id']}")
        lines.append(f"Generated At: {feedback['generated_at']}")
        lines.append(f"Success: {'✓ Yes' if feedback['success'] else '✗ No'}")
        
        if 'duration_seconds' in feedback:
            lines.append(f"Duration: {feedback['duration_seconds']:.2f}s")
        
        if 'steps_executed' in feedback:
            lines.append(f"Steps Executed: {feedback['steps_executed']}")
        
        if 'recommendations' in feedback and feedback['recommendations']:
            lines.append("\nRecommendations:")
            for rec in feedback['recommendations']:
                lines.append(f"  - {rec}")
        
        return '\n'.join(lines)
    
    def _format_as_html(self, feedback: Dict[str, Any]) -> str:
        """
        Format As HTML - 格式化为HTML
        
        Args:
            feedback: 反馈数据
            
        Returns:
            HTML格式的反馈
        """
        html_parts = []
        html_parts.append(f"<div class='feedback-report'>")
        html_parts.append(f"<h2>Execution Feedback</h2>")
        html_parts.append(f"<p><strong>Feedback ID:</strong> {feedback['feedback_id']}</p>")
        html_parts.append(f"<p><strong>Task ID:</strong> {feedback['task_id']}</p>")
        html_parts.append(f"<p><strong>Generated At:</strong> {feedback['generated_at']}</p>")
        html_parts.append(f"<p><strong>Success:</strong> {'Yes' if feedback['success'] else 'No'}</p>")
        html_parts.append("</div>")
        
        return '\n'.join(html_parts)


__all__ = ['FeedbackGenerationReporterComponent']
