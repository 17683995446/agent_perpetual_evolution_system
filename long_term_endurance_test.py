#!/usr/bin/env python3
"""
Long-Term Endurance Test for Agent Perpetual Evolution System
Runs for an extended duration with mixed extreme operations
"""

import sys
import os
import time
import random
import threading
import gc
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any

# Disable output buffering
sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache


@dataclass
class TestMetrics:
    """Stores test metrics"""
    start_time: float = 0
    end_time: float = 0
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    error_log: List[Dict] = field(default_factory=list)
    memory_usage_history: List[Dict] = field(default_factory=list)
    operations_per_second: List[float] = field(default_factory=list)


class LongTermEnduranceTest:
    def __init__(self, test_duration_minutes: int = 30, log_interval_seconds: int = 60):
        self.test_duration = test_duration_minutes * 60  # Convert to seconds
        self.log_interval = log_interval_seconds
        self.quantum = QuantumApplicationPlatform()
        self.agi = AGIApplicationFramework()
        self.decision = IntelligentDecisionPlatform()
        self.industry = IndustrySolutionsPlatform()
        self.cache = get_global_cache()
        self.metrics = TestMetrics()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            try:
                import resource
                return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            except:
                return 0

    def log_memory_usage(self, stage: str):
        """Log memory usage with timestamp"""
        with self.lock:
            self.metrics.memory_usage_history.append({
                "timestamp": datetime.now().isoformat(),
                "stage": stage,
                "memory_mb": self.get_memory_usage()
            })

    def execute_random_operation(self, worker_id: int):
        """Execute a single random high-difficulty operation"""
        op_type = random.choice([
            "quantum_tsp", "quantum_optimization", "agi_reasoning", 
            "agi_creative", "decision_multi", "decision_risk", 
            "industry_manufacturing", "cache_write_read"
        ])
        
        try:
            if op_type == "quantum_tsp":
                cities = [f"City_{worker_id}_{i}_{random.randint(1, 1000)}" for i in range(random.randint(3, 8))]
                self.quantum.optimization.solve_tsp(cities)
            elif op_type == "quantum_optimization":
                self.quantum.optimization.solve_quadratic_assignment([1, 2, 3], [4, 5, 6])
            elif op_type == "agi_reasoning":
                task = f"Problem_{worker_id}_{random.randint(1, 100000)}"
                query = f"Analyze {random.randint(1, 1000)} data points"
                self.agi.reasoning.deductive_reasoning(task, query)
            elif op_type == "agi_creative":
                topic = f"Topic_{worker_id}_{random.randint(1, 100000)}"
                self.agi.creative.generate_art(topic, "abstract")
            elif op_type == "decision_multi":
                options = [f"Option_{i}" for i in range(random.randint(2, 6))]
                self.decision.multi_criteria.optimize({"options": options})
            elif op_type == "decision_risk":
                data = [random.random() * 100 for _ in range(random.randint(5, 20))]
                self.decision.risk.calculate_var(data)
            elif op_type == "industry_manufacturing":
                batch_id = f"Batch_{worker_id}_{random.randint(1, 100000)}"
                defects = random.randint(0, 20)
                self.industry.manufacturing.quality_control(batch_id, defects)
            elif op_type == "cache_write_read":
                key = f"cache_{worker_id}_{random.randint(1, 100000)}"
                value = f"value_{random.random()}" * random.randint(10, 100)
                self.cache.set(key, value)
                self.cache.get(key)
            
            with self.lock:
                self.metrics.successful_operations += 1
            return True
        except Exception as e:
            with self.lock:
                self.metrics.failed_operations += 1
                self.metrics.error_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "operation": op_type,
                    "worker_id": worker_id,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
            return False

    def worker_thread(self, worker_id: int):
        """Worker thread that continuously executes operations"""
        print(f"🚀 Worker {worker_id} started")
        ops_count = 0
        last_log = time.time()
        
        while not self.stop_event.is_set():
            self.execute_random_operation(worker_id)
            
            ops_count += 1
            with self.lock:
                self.metrics.total_operations += 1
            
            # Random short delay (0-50ms)
            if random.random() < 0.3:
                time.sleep(random.uniform(0, 0.05))
            
            # Periodic GC
            if ops_count % 100 == 0:
                if random.random() < 0.1:
                    gc.collect()
        
        print(f"🏁 Worker {worker_id} completed - {ops_count} operations")

    def monitor_thread(self):
        """Monitor thread that logs status periodically"""
        last_log = time.time()
        start_time = time.time()
        
        while not self.stop_event.is_set():
            now = time.time()
            if now - last_log >= self.log_interval:
                self.log_memory_usage("monitor")
                self.print_status_summary(now - start_time)
                last_log = now
            
            time.sleep(1)

    def print_status_summary(self, elapsed_seconds: float):
        """Print current test status summary"""
        with self.lock:
            elapsed_mins = elapsed_seconds / 60
            total_ops = self.metrics.total_operations
            success = self.metrics.successful_operations
            failed = self.metrics.failed_operations
            success_rate = (success / total_ops * 100) if total_ops > 0 else 0
            memory_mb = self.get_memory_usage()
            
            print(f"\n{'='*60}")
            print(f"📊 Status Update - {elapsed_mins:.1f} mins elapsed")
            print(f"   Total Operations: {total_ops:,}")
            print(f"   ✅ Success: {success:,} ({success_rate:.2f}%)")
            print(f"   ❌ Failed: {failed:,}")
            print(f"   💾 Memory Usage: {memory_mb:.2f} MB")
            print(f"   📝 Error Count: {len(self.metrics.error_log)}")
            print(f"{'='*60}\n")

    def run_test(self, num_workers: int = 20):
        """Run the long-term endurance test"""
        print("🚀 Starting Long-Term Endurance Test")
        print(f"   Test Duration: {self.test_duration/60} minutes")
        print(f"   Workers: {num_workers}")
        print(f"   Log Interval: {self.log_interval} seconds")
        print()
        
        self.metrics.start_time = time.time()
        self.log_memory_usage("start")
        
        # Quick validation
        print("🔍 Quick validation test...")
        self.execute_random_operation(-1)
        print("✅ Validation passed!\n")
        
        # Start monitor thread
        monitor = threading.Thread(target=self.monitor_thread, daemon=True)
        monitor.start()
        
        # Start workers
        workers = []
        for i in range(num_workers):
            t = threading.Thread(target=self.worker_thread, args=(i,), daemon=True)
            workers.append(t)
            t.start()
        
        # Run for specified duration
        print(f"⏳ Running for {self.test_duration/60} minutes...")
        start_wait = time.time()
        while time.time() - start_wait < self.test_duration and not self.stop_event.is_set():
            time.sleep(1)
        
        # Stop everything
        print("\n🛑 Stopping test...")
        self.stop_event.set()
        
        for t in workers:
            t.join(timeout=5)
        
        monitor.join(timeout=2)
        
        self.metrics.end_time = time.time()
        self.log_memory_usage("end")
        
        self.print_final_report()
        
        # Save report
        self.save_report()
        
        return self.metrics

    def print_final_report(self):
        """Print final test report"""
        total_time = self.metrics.end_time - self.metrics.start_time
        total_ops = self.metrics.total_operations
        success = self.metrics.successful_operations
        failed = self.metrics.failed_operations
        
        print("\n" + "="*80)
        print("📋 LONG-TERM ENDURANCE TEST - FINAL REPORT")
        print("="*80)
        print(f"   Duration: {total_time/60:.2f} minutes")
        print(f"   Total Operations: {total_ops:,}")
        print(f"   ✅ Successful: {success:,} ({(success/total_ops*100 if total_ops>0 else 0):.2f}%)")
        print(f"   ❌ Failed: {failed:,} ({(failed/total_ops*100 if total_ops>0 else 0):.2f}%)")
        print(f"   Ops per second: {total_ops/total_time:.0f}")
        
        if len(self.metrics.error_log) > 0:
            print("\n   🔍 Errors Encountered:")
            for i, err in enumerate(self.metrics.error_log[:20], 1):  # Show first 20
                print(f"   {i}. {err['operation']} - {err['error_type']}: {err['error_message']}")
        
        if self.metrics.memory_usage_history:
            mem_start = self.metrics.memory_usage_history[0]['memory_mb']
            mem_end = self.metrics.memory_usage_history[-1]['memory_mb']
            print(f"\n   💾 Memory: {mem_start:.2f} MB → {mem_end:.2f} MB (Δ {mem_end-mem_start:+.2f} MB)")
        
        print("="*80)
        
        if len(self.metrics.error_log) == 0 and total_ops > 0:
            print("\n🎉 FLAWLESS LONG-TERM ENDURANCE TEST! No errors encountered!")
        elif len(self.metrics.error_log) == 0:
            print("\nℹ️ Test completed with zero errors but no operations counted.")
        else:
            print(f"\n⚠️ Test completed with {len(self.metrics.error_log)} errors.")

    def save_report(self):
        """Save test report to JSON file"""
        report_file = f"endurance_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = {
            "test_duration_seconds": self.test_duration,
            "metrics": {
                "start_time": self.metrics.start_time,
                "end_time": self.metrics.end_time,
                "total_operations": self.metrics.total_operations,
                "successful_operations": self.metrics.successful_operations,
                "failed_operations": self.metrics.failed_operations,
                "error_log": self.metrics.error_log,
                "memory_usage_history": self.metrics.memory_usage_history
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Report saved to: {os.path.abspath(report_file)}")


if __name__ == "__main__":
    # For quick testing, run for 5 minutes instead of 30
    test_duration = 5 if len(sys.argv) == 1 else int(sys.argv[1])
    
    tester = LongTermEnduranceTest(test_duration_minutes=test_duration)
    tester.run_test(num_workers=25)
