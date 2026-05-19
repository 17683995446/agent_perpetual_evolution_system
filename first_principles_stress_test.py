#!/usr/bin/env python3
"""
FIRST PRINCIPLES STRESS TEST - 第一性原理压力测试
从系统核心架构层开始，测试底层实现的极限和缺陷
"""

import sys
import os
import time
import random
import threading
import gc
import json
import tempfile
import tracemalloc
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any

sys.stdout.reconfigure(line_buffering=True)

# Add the agent_perpetual_evolution_system to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class FirstPrinciplesMetrics:
    """第一性原理测试指标"""
    start_time: float = 0
    end_time: float = 0
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    connection_leaks_detected: int = 0
    memory_leak_samples: List[Dict] = field(default_factory=list)
    thread_safety_violations: int = 0
    error_log: List[Dict] = field(default_factory=list)
    peak_memory: float = 0


class FirstPrinciplesStressTest:
    """
    第一性原理压力测试
    从系统核心架构的基本组件开始测试
    """

    def __init__(self, duration_minutes: int = 30):
        self.duration = duration_minutes * 60
        self.metrics = FirstPrinciplesMetrics()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.temp_dir = tempfile.mkdtemp(prefix="first_principles_test_")
        self.db_path = os.path.join(self.temp_dir, "test_system.db")
        tracemalloc.start()

    def _create_test_task(self, task_id: str = None):
        """创建一个测试任务对象"""
        if task_id is None:
            task_id = f"test_task_{random.randint(1, 1000000)}"
        task_obj = type('Task', (), {
            'task_id': task_id,
            'raw_input': f"Test input for {task_id}",
            'priority': random.randint(1, 10),
            'status': 'PENDING',
            'created_at': datetime.now()
        })()
        return task_obj

    def _log_sample(self, tag: str):
        """记录内存样本"""
        current, peak = tracemalloc.get_traced_memory()
        with self.lock:
            self.metrics.memory_leak_samples.append({
                'time': datetime.now().isoformat(),
                'tag': tag,
                'current_mb': current / (1024 * 1024),
                'peak_mb': peak / (1024 * 1024)
            })
            if peak > self.metrics.peak_memory * 1024 * 1024:
                self.metrics.peak_memory = peak / (1024 * 1024)

    def _execute_storage_operations(self, thread_id: int):
        """
        执行存储操作 - 测试第一性原理的核心存储接口
        """
        from infrastructure_adapter_layer.storage_backends.sqlite_based_storage_adapter import SQLiteBasedStorageAdapter
        storage = SQLiteBasedStorageAdapter(database_path=self.db_path)
        
        while not self.stop_event.is_set():
            try:
                # 随机执行存储操作
                op_type = random.randint(0, 10)
                
                if op_type == 0:
                    # Save task
                    task = self._create_test_task()
                    success = storage.save_single_task_record(task)
                    with self.lock:
                        if success:
                            self.metrics.successful_operations += 1
                        else:
                            self.metrics.failed_operations += 1
                
                elif op_type == 1:
                    # Retrieve task
                    task_id = f"test_task_{random.randint(1, 1000)}"
                    result = storage.retrieve_task_by_identifier(task_id)
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                elif op_type == 2:
                    # Update task status
                    task_id = f"test_task_{random.randint(1, 1000)}"
                    new_status = random.choice(['RUNNING', 'COMPLETED', 'FAILED'])
                    success = storage.update_task_status_value(task_id, new_status)
                    with self.lock:
                        if success:
                            self.metrics.successful_operations += 1
                        else:
                            self.metrics.failed_operations += 1
                
                elif op_type == 3:
                    # Get pending tasks
                    tasks = storage.get_list_of_pending_tasks(limit_count=random.randint(1, 50))
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                elif op_type == 4:
                    # Save experience
                    exp_id = f"exp_{thread_id}_{random.randint(1, 1000000)}"
                    task_id = f"test_task_{random.randint(1, 1000)}"
                    success = storage.save_execution_experience(
                        experience_id=exp_id,
                        task_id=task_id,
                        execution_result={'result': random.random()},
                        execution_plan={'steps': ['step1', 'step2']},
                        success=random.choice([True, False]),
                        duration_seconds=random.uniform(0.1, 10.0)
                    )
                    with self.lock:
                        if success:
                            self.metrics.successful_operations += 1
                        else:
                            self.metrics.failed_operations += 1
                
                elif op_type == 5:
                    # Save checkpoint
                    cp_id = f"cp_{thread_id}_{random.randint(1, 1000000)}"
                    task_id = f"test_task_{random.randint(1, 1000)}"
                    success = storage.save_execution_checkpoint(
                        checkpoint_id=cp_id,
                        task_id=task_id,
                        current_step="step3",
                        context={'data': f"context_{thread_id}"}
                    )
                    with self.lock:
                        if success:
                            self.metrics.successful_operations += 1
                        else:
                            self.metrics.failed_operations += 1
                
                elif op_type == 6:
                    # Get latest checkpoint
                    task_id = f"test_task_{random.randint(1, 1000)}"
                    storage.get_latest_checkpoint_record(task_id)
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                elif op_type == 7:
                    # Health check
                    health = storage.perform_health_check()
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                elif op_type == 8:
                    # Random operations in sequence
                    task = self._create_test_task()
                    storage.save_single_task_record(task)
                    storage.retrieve_task_by_identifier(task.task_id)
                    storage.update_task_status_value(task.task_id, 'RUNNING')
                    storage.update_task_status_value(task.task_id, 'COMPLETED')
                    with self.lock:
                        self.metrics.successful_operations += 4
                
                elif op_type == 9:
                    # Memory pressure - create and delete large objects
                    for i in range(random.randint(1, 5)):
                        task = self._create_test_task(f"heavy_task_{thread_id}_{i}")
                        storage.save_single_task_record(task)
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                elif op_type == 10:
                    # Extreme concurrency simulation - multiple saves in quick successions
                    for i in range(random.randint(1, 10)):
                        task = self._create_test_task(f"rapid_task_{thread_id}_{i}")
                        storage.save_single_task_record(task)
                    with self.lock:
                        self.metrics.successful_operations += 1
                
                # Increment total count
                with self.lock:
                    self.metrics.total_operations += 1
            
            except Exception as e:
                with self.lock:
                    self.metrics.failed_operations += 1
                    self.metrics.total_operations += 1
                    if len(self.metrics.error_log) < 500:
                        self.metrics.error_log.append({
                            'time': datetime.now().isoformat(),
                            'thread': thread_id,
                            'error_type': type(e).__name__,
                            'error_msg': str(e)[:300]
                        })
            
            if random.random() < 0.1:
                time.sleep(random.uniform(0, 0.01))

    def _execute_abnormal_operations(self, thread_id: int):
        """
        执行异常操作 - 边界和异常情况
        """
        from infrastructure_adapter_layer.storage_backends.sqlite_based_storage_adapter import SQLiteBasedStorageAdapter
        storage = SQLiteBasedStorageAdapter(database_path=self.db_path)
        
        while not self.stop_event.is_set():
            try:
                op_type = random.randint(0, 8)
                
                if op_type == 0:
                    # None task
                    storage.save_single_task_record(None)
                
                elif op_type == 1:
                    # Empty task ID
                    task = self._create_test_task("")
                    storage.save_single_task_record(task)
                
                elif op_type == 2:
                    # Retrieve None task
                    storage.retrieve_task_by_identifier(None)
                
                elif op_type == 3:
                    # Empty task ID retrieve
                    storage.retrieve_task_by_identifier("")
                
                elif op_type == 4:
                    # Update with None
                    storage.update_task_status_value(None, None)
                
                elif op_type == 5:
                    # Negative limit
                    storage.get_list_of_pending_tasks(limit_count=-100)
                
                elif op_type == 6:
                    # Zero limit
                    storage.get_list_of_pending_tasks(limit_count=0)
                
                elif op_type == 7:
                    # Save invalid experience
                    storage.save_execution_experience(
                        experience_id=None,
                        task_id=None,
                        execution_result=None,
                        execution_plan=None,
                        success=None,
                        duration_seconds=None
                    )
                
                elif op_type == 8:
                    # Rapid connections and disconnections
                    for i in range(3):
                        temp_storage = SQLiteBasedStorageAdapter(
                            database_path=self.db_path
                        )
                        temp_storage.perform_health_check()
                        if hasattr(temp_storage, 'close'):
                            temp_storage.close()
                
                with self.lock:
                    self.metrics.successful_operations += 1
                    self.metrics.total_operations += 1
            
            except Exception as e:
                with self.lock:
                    self.metrics.failed_operations += 1
                    self.metrics.total_operations += 1
                    if len(self.metrics.error_log) < 500:
                        self.metrics.error_log.append({
                            'time': datetime.now().isoformat(),
                            'thread': thread_id,
                            'error_type': type(e).__name__,
                            'error_msg': str(e)[:300],
                            'context': 'ABNORMAL'
                        })
            
            if random.random() < 0.1:
                time.sleep(random.uniform(0, 0.01))

    def _print_status(self, elapsed: float):
        """打印测试状态"""
        with self.lock:
            total = self.metrics.total_operations
            success = self.metrics.successful_operations
            failed = self.metrics.failed_operations
            curr_mem, peak_mem = self._get_mem()
            success_rate = (success / total * 100) if total > 0 else 0
            elapsed_mins = elapsed / 60
        
        print(f"\n{'=' * 100}")
        print(f"⏱️  FIRST PRINCIPLES STRESS TEST - {elapsed_mins:.1f} min / {self.duration / 60:.0f} min")
        print(f"🔢 Total: {total:,} | ✅ Success: {success:,} ({success_rate:.2f}%) | ❌ Failed: {failed:,}")
        print(f"💾 Mem: {curr_mem:.2f} MB | Peak: {peak_mem:.2f} MB | Errors: {len(self.metrics.error_log)}")
        print(f"{'=' * 100}\n")

    def _get_mem(self):
        return tracemalloc.get_traced_memory()

    def monitor_thread(self):
        """监控线程"""
        last_report = time.time()
        last_sample = time.time()
        
        while not self.stop_event.is_set():
            now = time.time()
            
            if now - last_report >= 60:
                elapsed = now - self.metrics.start_time
                self._print_status(elapsed)
                last_report = now
            
            if now - last_sample >= 15:
                self._log_sample('monitor')
                last_sample = now
            
            time.sleep(0.1)

    def run(self):
        """运行第一性原理压力测试"""
        print("\n" + "🔥" * 60)
        print("🔥 FIRST PRINCIPLES STRESS TEST - 第一性原理压力测试 🔥")
        print("🔥" * 60)
        print(f"Duration: {self.duration / 60} min | Focus: Core Storage Infrastructure")
        print()

        self.metrics.start_time = time.time()
        self._log_sample('start')

        print("📋 Starting monitor thread...")
        monitor = threading.Thread(target=self.monitor_thread, daemon=True)
        monitor.start()

        print("📋 Starting normal operation threads...")
        normal_threads = []
        for i in range(15):
            t = threading.Thread(
                target=self._execute_storage_operations,
                args=(i,),
                daemon=True
            )
            normal_threads.append(t)
            t.start()

        print("📋 Starting abnormal operation threads...")
        abnormal_threads = []
        for i in range(10):
            t = threading.Thread(
                target=self._execute_abnormal_operations,
                args=(i,),
                daemon=True
            )
            abnormal_threads.append(t)
            t.start()

        print("\n🚀 Test running for", self.duration, "seconds...\n")
        
        start_wait = time.time()
        while time.time() - start_wait < self.duration and not self.stop_event.is_set():
            time.sleep(1)

        print("\n🛑 Stopping test...")
        self.stop_event.set()

        print("\n📋 Joining normal threads...")
        for t in normal_threads:
            t.join(timeout=10)
        
        print("\n📋 Joining abnormal threads...")
        for t in abnormal_threads:
            t.join(timeout=10)

        monitor.join(timeout=5)
        
        self.metrics.end_time = time.time()
        self._log_sample('end')
        tracemalloc.stop()

        self._final_report()
        self._save_report()
        self._cleanup()

    def _final_report(self):
        """生成最终报告"""
        duration = self.metrics.end_time - self.metrics.start_time
        total = self.metrics.total_operations
        success = self.metrics.successful_operations
        failed = self.metrics.failed_operations

        print("\n" + "=" * 100)
        print("📊 FIRST PRINCIPLES STRESS TEST - FINAL REPORT")
        print("=" * 100)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Operations: {total:,}")
        print(f"✅ Successful: {success:,} ({(success / total * 100) if total else 0:.2f}%)")
        print(f"❌ Failed: {failed:,} ({(failed / total * 100) if total else 0:.2f}%)")
        print(f"⚠️ Errors Logged: {len(self.metrics.error_log)}")
        print(f"💾 Peak Memory: {self.metrics.peak_memory:.2f} MB")
        print(f"⚡ Throughput: {total / duration:.0f} ops/sec")

        if self.metrics.error_log:
            print("\n📋 TOP ERROR TYPES:")
            error_counts = {}
            for err in self.metrics.error_log:
                err_type = err['error_type']
                error_counts[err_type] = error_counts.get(err_type, 0) + 1
            
            sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
            for err_type, count in sorted_errors[:10]:
                print(f"  {err_type}: {count} occurrences")

            print("\n📋 SAMPLE ERRORS:")
            for i, err in enumerate(self.metrics.error_log[:10]):
                print(f"  {i+1}. [{err['time']}] {err['error_type']}: {err['error_msg']}")

        print("\n" + "=" * 100)
        if failed == 0:
            print("🎉🎉🎉 PERFECT VICTORY! NO ISSUES DETECTED! 🎉🎉🎉")
        elif failed < total * 0.001:
            print("🌟 EXCELLENT! MINIMAL FAILURES!")
        else:
            print("⚠️ ISSUES DETECTED! NEEDS ANALYSIS!")

    def _save_report(self):
        """保存报告"""
        report_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"first_principles_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        report_data = {
            'start_time': datetime.fromtimestamp(self.metrics.start_time).isoformat(),
            'end_time': datetime.fromtimestamp(self.metrics.end_time).isoformat(),
            'duration_seconds': self.metrics.end_time - self.metrics.start_time,
            'metrics': {
                'total_operations': self.metrics.total_operations,
                'successful_operations': self.metrics.successful_operations,
                'failed_operations': self.metrics.failed_operations,
                'peak_memory_mb': self.metrics.peak_memory,
                'error_log': self.metrics.error_log
            }
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Report saved to: {os.path.abspath(report_path)}")

    def _cleanup(self):
        """清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        print(f"\n🧹 Cleanup complete.")


if __name__ == '__main__':
    print("=" * 100)
    print("STARTING FIRST PRINCIPLES STRESS TEST")
    print("=" * 100)
    
    test = FirstPrinciplesStressTest(duration_minutes=15)
    test.run()
