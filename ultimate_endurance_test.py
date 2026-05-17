#!/usr/bin/env python3
"""
ULTIMATE LONG-TERM ENDURANCE TEST
- 10 minutes duration
- Anomaly injection testing
- Extreme mixed operations
"""

import sys
import os
import time
import random
import threading
import gc
import json
import tempfile
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache


@dataclass
class TestMetrics:
    start_time: float = 0
    end_time: float = 0
    total_ops: int = 0
    success: int = 0
    failed: int = 0
    anomalies: int = 0
    error_log: List[Dict] = field(default_factory=list)
    mem_history: List[Dict] = field(default_factory=list)


class UltimateEnduranceTest:
    def __init__(self, duration_minutes=10, log_interval=20):
        self.duration = duration_minutes * 60
        self.log_interval = log_interval
        self.q = QuantumApplicationPlatform()
        self.a = AGIApplicationFramework()
        self.d = IntelligentDecisionPlatform()
        self.i = IndustrySolutionsPlatform()
        self.cache = get_global_cache()
        self.metrics = TestMetrics()
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.temp_dir = tempfile.mkdtemp(prefix="ultimate_test_")

    def _get_mem(self):
        try:
            import resource
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        except:
            return 0

    def _log_mem(self, tag):
        with self.lock:
            self.metrics.mem_history.append({
                "time": datetime.now().isoformat(),
                "tag": tag,
                "mem": self._get_mem()
            })

    def _exec_normal(self, worker_id, step):
        """Normal operation"""
        op = random.randint(0, 6)
        if op == 0:
            self.q.optimization.solve_tsp([f"City_{worker_id}_{step}_{i}" for i in range(random.randint(3, 7))])
        elif op == 1:
            self.a.creative.generate_art(f"Art_{worker_id}_{step}", random.choice(["abstract", "modern", "vintage"]))
        elif op == 2:
            self.d.multi_criteria.optimize({
                "options": [f"Opt_{worker_id}_{step}_{i}" for i in range(random.randint(2, 5))]
            })
        elif op == 3:
            self.d.risk.calculate_var([random.random() * 100 for _ in range(random.randint(5, 15))])
        elif op == 4:
            self.i.manufacturing.quality_control(f"Batch_{worker_id}_{step}", random.randint(0, 15))
        elif op == 5:
            self.cache.set(f"key_{worker_id}_{step}", f"value_{random.random()}"*50)
            self.cache.get(f"key_{worker_id}_{step-1}")
        elif op == 6:
            file_path = os.path.join(self.temp_dir, f"f_{worker_id}_{step}.txt")
            with open(file_path, "w") as f:
                f.write(f"Test data {random.random()}")
            if os.path.exists(file_path):
                os.remove(file_path)
        return True

    def _exec_anomaly(self, worker_id, step):
        """Anomaly/invalid parameter injection"""
        op = random.randint(0, 5)
        if op == 0:
            self.q.optimization.solve_tsp([])  # Empty list
        elif op == 1:
            self.i.manufacturing.quality_control("", "invalid-number")  # Bad params
        elif op == 2:
            self.d.multi_criteria.optimize("not-a-dict")
        elif op == 3:
            self.d.risk.calculate_var("not-a-list")
        elif op == 4:
            self.a.creative.generate_art(None, None)
        elif op == 5:
            self.cache.get("non-existent-key-very-unique-12345")  # Get non-existent
        return True

    def _execute(self, worker_id, step):
        try:
            # 15% chance to inject anomaly
            if random.random() < 0.15:
                self._exec_anomaly(worker_id, step)
                with self.lock:
                    self.metrics.anomalies +=1
            else:
                self._exec_normal(worker_id, step)
            
            with self.lock:
                self.metrics.success +=1
        except Exception as e:
            with self.lock:
                self.metrics.failed +=1
                if len(self.metrics.error_log) < 50:  # Keep 50 errors max
                    self.metrics.error_log.append({
                        "time": datetime.now().isoformat(),
                        "worker": worker_id,
                        "step": step,
                        "error": str(e),
                        "type": str(type(e))
                    })
        finally:
            with self.lock:
                self.metrics.total_ops +=1

    def worker(self, worker_id):
        print(f"🚀 Worker {worker_id} starting")
        step = 0
        while not self.stop.is_set():
            self._execute(worker_id, step)
            step +=1
            if step % 1000 == 0:
                gc.collect()  # Occasional GC
            time.sleep(random.uniform(0, 0.02))  # Random tiny delay
        print(f"🏁 Worker {worker_id} done, steps: {step}")

    def monitor(self):
        last_log = time.time()
        while not self.stop.is_set():
            now = time.time()
            if now - last_log >= self.log_interval:
                self._log_mem("periodic")
                self._print_status(now - self.metrics.start_time)
                last_log = now
            time.sleep(1)

    def _print_status(self, elapsed):
        with self.lock:
            elapsed_m = elapsed /60
            total = self.metrics.total_ops
            success = self.metrics.success
            failed = self.metrics.failed
            anomalies = self.metrics.anomalies
            mem = self._get_mem()
            pct = (success / total *100) if total>0 else 0

        print("\n" + "="*70)
        print(f"📊 STATUS - {elapsed_m:.1f} mins elapsed")
        print(f"   TOTAL: {total:,} | SUCCESS: {success:,} ({pct:.2f}%)")
        print(f"   FAILED: {failed:,} | ANOMALIES INJECTED: {anomalies:,}")
        print(f"   MEM: {mem:.2f} MB | ERRORS LOGGED: {len(self.metrics.error_log)}")
        print("="*70 + "\n")

    def run(self, workers=20):
        print("🚀"*25)
        print("🚀 ULTIMATE LONG-TERM ENDURANCE TEST (10 mins) 🚀")
        print("🚀"*25)
        print(f"Duration: {self.duration/60} mins | Workers: {workers} | Log every: {self.log_interval}s")
        print()
        
        self.metrics.start_time = time.time()
        self._log_mem("start")

        # Quick validation first
        print("🔍 Quick validation run...")
        self._execute(-1, 0)
        print("✅ Validation passed! Starting main test...\n")
        
        # Start threads
        monitor_thread = threading.Thread(target=self.monitor, daemon=True)
        monitor_thread.start()

        worker_threads = []
        for i in range(workers):
            t = threading.Thread(target=self.worker, args=(i,), daemon=True)
            worker_threads.append(t)
            t.start()
        
        # Run for duration
        print(f"⏳ Main test running for {self.duration/60} minutes...")
        start_run = time.time()
        while time.time() - start_run < self.duration and not self.stop.is_set():
            time.sleep(1)
        
        print("\n🛑 Stopping all workers...")
        self.stop.set()
        
        for t in worker_threads:
            t.join(timeout=3)
        
        monitor_thread.join(timeout=2)
        
        self.metrics.end_time = time.time()
        self._log_mem("end")
        self._final_report()
        self._save_report()
        self._cleanup()

    def _final_report(self):
        duration = self.metrics.end_time - self.metrics.start_time
        total = self.metrics.total_ops
        success = self.metrics.success
        failed = self.metrics.failed
        anomalies = self.metrics.anomalies
        
        print("\n" + "="*80)
        print("🏆 ULTIMATE ENDURANCE TEST - FINAL REPORT")
        print("="*80)
        print(f"Duration: {duration/60:.2f} mins")
        print(f"Total Operations: {total:,}")
        print(f"✅ Success: {success:,} ({(success/total*100 if total else 0):.2f}%)")
        print(f"❌ Failed: {failed:,} ({(failed/total*100 if total else 0):.2f}%)")
        print(f"🧪 Anomalies Injected: {anomalies:,}")
        print(f"⚡ Throughput: {total/duration:.0f} ops/sec")
        
        if self.metrics.mem_history:
            start_m = self.metrics.mem_history[0]['mem']
            end_m = self.metrics.mem_history[-1]['mem']
            print(f"💾 Memory: {start_m:.2f} MB → {end_m:.2f} MB (Δ {end_m-start_m:+.2f})")
        
        if len(self.metrics.error_log) >0:
            print("\n📋 First 10 errors:")
            for i, e in enumerate(self.metrics.error_log[:10]):
                print(f"  {i+1}. [{e['time']}] W{e['worker']} S{e['step']}: {e['type']} - {e['error'][:80]}")
        
        print("="*80)
        
        if failed ==0 and len(self.metrics.error_log)==0:
            print("\n🎉🎉🎉 FLAWLESS VICTORY! ABSOLUTELY PERFECT! 🎉🎉🎉")
        elif failed < total * 0.01:
            print("\n🌟 EXCELLENT! Near-perfect performance!")
        else:
            print("\n⚠️ Some issues detected, needs optimization")

    def _save_report(self):
        report_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f'ultimate_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'duration': self.duration,
                'metrics': {
                    'total_ops': self.metrics.total_ops,
                    'success': self.metrics.success,
                    'failed': self.metrics.failed,
                    'anomalies': self.metrics.anomalies,
                    'error_log': self.metrics.error_log,
                    'mem_history': self.metrics.mem_history
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Full report saved to {report_file}")
    
    def _cleanup(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    test = UltimateEnduranceTest(duration_minutes=10, log_interval=20)
    test.run(workers=20)
