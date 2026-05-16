"""
Custom Exception Classes - 自定义异常类
定义系统中使用的所有自定义异常类型
"""


class AgentEvolutionSystemException(Exception):
    """基础异常类"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
    
    def to_dict(self) -> dict:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details
        }


class StorageException(AgentEvolutionSystemException):
    """存储相关异常"""
    
    def __init__(self, message: str, operation: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="STORAGE_ERROR",
            details=details
        )
        self.operation = operation


class LoggerException(AgentEvolutionSystemException):
    """日志相关异常"""
    
    def __init__(self, message: str, logger_name: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="LOGGER_ERROR",
            details=details
        )
        self.logger_name = logger_name


class TaskWorkflowException(AgentEvolutionSystemException):
    """任务工作流相关异常"""
    
    def __init__(self, message: str, task_id: str = None, workflow_state: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="TASK_WORKFLOW_ERROR",
            details=details
        )
        self.task_id = task_id
        self.workflow_state = workflow_state


class TaskAnalysisException(AgentEvolutionSystemException):
    """任务分析相关异常"""
    
    def __init__(self, message: str, analysis_phase: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="TASK_ANALYSIS_ERROR",
            details=details
        )
        self.analysis_phase = analysis_phase


class TaskExecutionException(AgentEvolutionSystemException):
    """任务执行相关异常"""
    
    def __init__(self, message: str, task_id: str = None, step_number: int = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="TASK_EXECUTION_ERROR",
            details=details
        )
        self.task_id = task_id
        self.step_number = step_number


class SchedulerException(AgentEvolutionSystemException):
    """调度器相关异常"""
    
    def __init__(self, message: str, queue_state: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="SCHEDULER_ERROR",
            details=details
        )
        self.queue_state = queue_state


class ConfigurationException(AgentEvolutionSystemException):
    """配置相关异常"""
    
    def __init__(self, message: str, config_key: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            details=details
        )
        self.config_key = config_key


class ValidationException(AgentEvolutionSystemException):
    """验证相关异常"""
    
    def __init__(self, message: str, field_name: str = None, invalid_value: any = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )
        self.field_name = field_name
        self.invalid_value = invalid_value


class LearningException(AgentEvolutionSystemException):
    """学习模块相关异常"""
    
    def __init__(self, message: str, experience_id: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="LEARNING_ERROR",
            details=details
        )
        self.experience_id = experience_id


class CheckpointException(AgentEvolutionSystemException):
    """检查点相关异常"""
    
    def __init__(self, message: str, checkpoint_id: str = None, task_id: str = None, details: dict = None):
        super().__init__(
            message=message,
            error_code="CHECKPOINT_ERROR",
            details=details
        )
        self.checkpoint_id = checkpoint_id
        self.task_id = task_id


__all__ = [
    'AgentEvolutionSystemException',
    'StorageException',
    'LoggerException',
    'TaskWorkflowException',
    'TaskAnalysisException',
    'TaskExecutionException',
    'SchedulerException',
    'ConfigurationException',
    'ValidationException',
    'LearningException',
    'CheckpointException',
]
