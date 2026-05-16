"""
SQLite Based Storage Adapter - SQLite 存储适配器
提供基于 SQLite 数据库的持久化存储实现
"""

import sqlite3
import json
import threading
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from ...core_abstraction_layer.interfaces.storage_interface_contract import CoreStorageInterfaceContract
from ...core_abstraction_layer.interfaces.logging_interface_contract import CoreLoggerInterfaceContract


class SQLiteBasedStorageAdapter(CoreStorageInterfaceContract):
    """
    SQLite Based Storage Adapter - SQLite 存储适配器
    
    提供基于 SQLite 的持久化存储
    支持任务、经验、检查点等多种数据的持久化
    """
    
    def __init__(
        self,
        database_path: str = "data/agent_system.db",
        logger_backend: Optional[CoreLoggerInterfaceContract] = None
    ):
        """
        Initialize SQLite Based Storage Adapter - 初始化 SQLite 存储适配器
        
        Args:
            database_path: 数据库文件路径
            logger_backend: 日志后端（可选）
        """
        self.database_path = database_path
        self.logger_backend = logger_backend
        
        # 确保目录存在
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 线程锁
        self._lock = threading.RLock()
        
        # 初始化数据库
        self._initialize_database()
        
        self.logger_backend and self.logger_backend.log_information_message(
            'SQLiteBasedStorageAdapter',
            f'SQLite storage adapter initialized with database: {database_path}'
        )
    
    def _initialize_database(self):
        """初始化数据库表结构"""
        with self._lock:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # 创建任务表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    raw_input TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    timeout_seconds INTEGER,
                    metadata TEXT
                )
            """)
            
            # 创建经验表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    experience_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    execution_result TEXT,
                    execution_plan TEXT,
                    metadata TEXT,
                    success INTEGER DEFAULT 0,
                    duration_seconds REAL DEFAULT 0,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
                )
            """)
            
            # 创建检查点表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    step_number INTEGER NOT NULL,
                    execution_state TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_experiences_task ON experiences(task_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkpoints_task ON checkpoints(task_id)")
            
            conn.commit()
            conn.close()
    
    def save_single_task_record(self, task) -> bool:
        """
        Save Single Task Record - 保存单个任务记录
        
        Args:
            task: 任务对象
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                # 将任务对象转换为字典
                task_dict = {
                    'task_id': task.task_id,
                    'raw_input': getattr(task, 'raw_input', ''),
                    'priority': getattr(task, 'priority', 1),
                    'status': getattr(task, 'status', 'PENDING'),
                    'created_at': getattr(task, 'created_at', datetime.now()),
                    'started_at': getattr(task, 'started_at', None),
                    'completed_at': getattr(task, 'completed_at', None),
                    'timeout_seconds': getattr(task, 'timeout_seconds', None),
                    'metadata': json.dumps(getattr(task, '__dict__', {}))
                }
                
                cursor.execute("""
                    INSERT OR REPLACE INTO tasks 
                    (task_id, raw_input, priority, status, created_at, started_at, completed_at, timeout_seconds, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task_dict['task_id'],
                    task_dict['raw_input'],
                    task_dict['priority'],
                    task_dict['status'],
                    task_dict['created_at'],
                    task_dict['started_at'],
                    task_dict['completed_at'],
                    task_dict['timeout_seconds'],
                    task_dict['metadata']
                ))
                
                conn.commit()
                conn.close()
                
                self.logger_backend and self.logger_backend.log_debug_message(
                    'SQLiteBasedStorageAdapter',
                    f'Task saved: {task.task_id}'
                )
                
                return True
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to save task: {str(e)}',
                task_id=getattr(task, 'task_id', 'unknown')
            )
            return False
    
    def retrieve_task_by_identifier(self, task_id: str):
        """
        Retrieve Task By Identifier - 根据标识符获取任务
        
        Args:
            task_id: 任务唯一标识符
            
        Returns:
            找到的任务对象，或 None
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    # 将数据库行转换为任务对象
                    task = type('Task', (), {
                        'task_id': row[0],
                        'raw_input': row[1],
                        'priority': row[2],
                        'status': row[3],
                        'created_at': datetime.fromisoformat(row[4]) if row[4] else None,
                        'started_at': datetime.fromisoformat(row[5]) if row[5] else None,
                        'completed_at': datetime.fromisoformat(row[6]) if row[6] else None,
                        'timeout_seconds': row[7],
                        'metadata': json.loads(row[8]) if row[8] else {}
                    })()
                    
                    self.logger_backend and self.logger_backend.log_debug_message(
                        'SQLiteBasedStorageAdapter',
                        f'Task retrieved: {task_id}'
                    )
                    
                    return task
                
                return None
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to retrieve task: {str(e)}',
                task_id=task_id
            )
            return None
    
    def update_task_status_value(self, task_id: str, new_status, **kwargs) -> bool:
        """
        Update Task Status Value - 更新任务状态值
        
        Args:
            task_id: 任务ID
            new_status: 新的状态值
            **kwargs: 其他要更新的属性
            
        Returns:
            bool: 更新是否成功
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                # 构建更新语句
                update_fields = ['status = ?']
                update_values = [new_status]
                
                if 'started_at' in kwargs:
                    update_fields.append('started_at = ?')
                    update_values.append(kwargs['started_at'])
                
                if 'completed_at' in kwargs:
                    update_fields.append('completed_at = ?')
                    update_values.append(kwargs['completed_at'])
                
                update_values.append(task_id)
                
                cursor.execute(
                    f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = ?",
                    update_values
                )
                
                conn.commit()
                affected = cursor.rowcount
                conn.close()
                
                self.logger_backend and self.logger_backend.log_debug_message(
                    'SQLiteBasedStorageAdapter',
                    f'Task status updated: {task_id} -> {new_status}',
                    affected_rows=affected
                )
                
                return affected > 0
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to update task status: {str(e)}',
                task_id=task_id
            )
            return False
    
    def get_list_of_pending_tasks(self, limit_count: int = 100) -> List:
        """
        Get List Of Pending Tasks - 获取待处理任务列表
        
        Args:
            limit_count: 返回的最大数量
            
        Returns:
            待处理任务列表
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM tasks 
                    WHERE status IN ('PENDING', 'RUNNING')
                    ORDER BY priority DESC, created_at ASC
                    LIMIT ?
                """, (limit_count,))
                
                rows = cursor.fetchall()
                conn.close()
                
                tasks = []
                for row in rows:
                    task = type('Task', (), {
                        'task_id': row[0],
                        'raw_input': row[1],
                        'priority': row[2],
                        'status': row[3],
                        'created_at': datetime.fromisoformat(row[4]) if row[4] else None,
                        'started_at': datetime.fromisoformat(row[5]) if row[5] else None,
                        'completed_at': datetime.fromisoformat(row[6]) if row[6] else None,
                        'timeout_seconds': row[7]
                    })()
                    tasks.append(task)
                
                return tasks
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to get pending tasks: {str(e)}'
            )
            return []
    
    def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform Health Check - 执行健康检查
        
        Returns:
            健康状态字典
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                # 检查数据库连接
                cursor.execute("SELECT 1")
                
                # 获取统计信息
                cursor.execute("SELECT COUNT(*) FROM tasks")
                total_tasks = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'PENDING'")
                pending_tasks = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'COMPLETED'")
                completed_tasks = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM experiences")
                total_experiences = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM checkpoints")
                total_checkpoints = cursor.fetchone()[0]
                
                conn.close()
                
                health_info = {
                    'status': 'healthy',
                    'storage_type': 'sqlite',
                    'database_path': self.database_path,
                    'total_tasks': total_tasks,
                    'pending_tasks': pending_tasks,
                    'completed_tasks': completed_tasks,
                    'total_experiences': total_experiences,
                    'total_checkpoints': total_checkpoints
                }
                
                return health_info
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'storage_type': 'sqlite',
                'database_path': self.database_path,
                'error': str(e)
            }
    
    def save_execution_experience(
        self,
        experience_id: str,
        task_id: str,
        execution_result: Dict[str, Any],
        execution_plan: Dict[str, Any],
        success: bool,
        duration_seconds: float
    ) -> bool:
        """
        Save Execution Experience - 保存执行经验
        
        Args:
            experience_id: 经验ID
            task_id: 任务ID
            execution_result: 执行结果
            execution_plan: 执行计划
            success: 是否成功
            duration_seconds: 执行时长（秒）
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO experiences 
                    (experience_id, task_id, execution_result, execution_plan, success, duration_seconds)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    experience_id,
                    task_id,
                    json.dumps(execution_result),
                    json.dumps(execution_plan),
                    1 if success else 0,
                    duration_seconds
                ))
                
                conn.commit()
                conn.close()
                
                self.logger_backend and self.logger_backend.log_debug_message(
                    'SQLiteBasedStorageAdapter',
                    f'Experience saved: {experience_id}'
                )
                
                return True
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to save experience: {str(e)}',
                experience_id=experience_id
            )
            return False
    
    def save_execution_checkpoint(
        self,
        checkpoint_id: str,
        task_id: str,
        current_step: str,
        context: Dict[str, Any]
    ) -> bool:
        """
        Save Execution Checkpoint - 保存执行检查点
        
        Args:
            checkpoint_id: 检查点ID
            task_id: 任务ID
            current_step: 当前步骤
            context: 执行上下文
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO checkpoints 
                    (checkpoint_id, task_id, step_number, execution_state)
                    VALUES (?, ?, ?, ?)
                """, (
                    checkpoint_id,
                    task_id,
                    0,  # 可以从context中提取
                    json.dumps(context)
                ))
                
                conn.commit()
                conn.close()
                
                self.logger_backend and self.logger_backend.log_debug_message(
                    'SQLiteBasedStorageAdapter',
                    f'Checkpoint saved: {checkpoint_id}'
                )
                
                return True
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to save checkpoint: {str(e)}',
                checkpoint_id=checkpoint_id
            )
            return False
    
    def get_latest_checkpoint_record(self, task_id: str):
        """
        Get Latest Checkpoint Record - 获取最新检查点记录
        
        Args:
            task_id: 任务ID
            
        Returns:
            最新的检查点对象，或 None
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM checkpoints 
                    WHERE task_id = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (task_id,))
                
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    checkpoint = type('Checkpoint', (), {
                        'checkpoint_id': row[0],
                        'task_id': row[1],
                        'step_number': row[2],
                        'execution_state': json.loads(row[3]) if row[3] else {},
                        'created_at': datetime.fromisoformat(row[4]) if row[4] else None
                    })()
                    return checkpoint
                
                return None
                
        except Exception as e:
            self.logger_backend and self.logger_backend.log_error_message(
                'SQLiteBasedStorageAdapter',
                f'Failed to get latest checkpoint: {str(e)}',
                task_id=task_id
            )
            return None
    
    def close(self):
        """关闭数据库连接"""
        self.logger_backend and self.logger_backend.log_information_message(
            'SQLiteBasedStorageAdapter',
            'SQLite storage adapter closed'
        )


__all__ = ['SQLiteBasedStorageAdapter']
