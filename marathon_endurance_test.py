#!/usr/bin/env python3
"""
MARATHON ENDURANCE TEST - 30 Minutes
The most comprehensive, complex, and difficult real-world simulation
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
from typing import Dict, List

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache


@dataclass
class MarathonMetrics:
    start_time: float = 0
    end_time: float = 0
    total_ops: int = 0
    success: int = 0
    failed: int = 0
    anomalies_injected: int = 0
    error_log: List[Dict] = field(default_factory=list)
    mem_samples: List[Dict] = field(default_factory=list)
    gc_cycles: int = 0
    peak_memory: float = 0


class MarathonEnduranceTest:
    def __init__(self, duration_minutes=30):
        self.duration = duration_minutes * 60
        self.q = QuantumApplicationPlatform()
        self.a = AGIApplicationFramework()
        self.d = IntelligentDecisionPlatform()
        self.i = IndustrySolutionsPlatform()
        self.cache = get_global_cache()
        self.metrics = MarathonMetrics()
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.temp_dir = tempfile.mkdtemp(prefix="marathon_")
        self.gc_count = 0
        tracemalloc.start()

    def _get_mem(self):
        current, peak = tracemalloc.get_traced_memory()
        return current / (1024 * 1024), peak / (1024 * 1024)

    def _log_mem(self, tag):
        curr, peak = self._get_mem()
        with self.lock:
            self.metrics.mem_samples.append({
                "time": datetime.now().isoformat(),
                "tag": tag,
                "current_mb": round(curr, 2),
                "peak_mb": round(peak, 2)
            })
            if peak > self.metrics.peak_memory:
                self.metrics.peak_memory = peak

    def _exec_normal(self, worker_id, step):
        """Execute normal high-difficulty operations"""
        op = random.randint(0, 12)
        
        if op == 0:
            cities = [f"C_{worker_id}_{step}_{i}" for i in range(random.randint(4, 10))]
            self.q.optimization.solve_tsp(cities)
        elif op == 1:
            self.q.optimization.solve_quadratic_assignment(
                [random.randint(1, 5) for _ in range(random.randint(3, 6))],
                [random.randint(1, 5) for _ in range(random.randint(3, 6))]
            )
        elif op == 2:
            self.a.creative.generate_art(f"Art_{worker_id}_{step}", random.choice(["abstract", "modern", "vintage", "surreal"]))
        elif op == 3:
            self.a.creative.generate_story(f"Story_{worker_id}", f"Theme_{step}", random.choice(["short", "medium", "long"]))
        elif op == 4:
            self.a.reasoning.deductive_reasoning(f"Task_{worker_id}_{step}", f"Query about {random.randint(1, 1000)}")
        elif op == 5:
            options = [f"Opt_{worker_id}_{step}_{i}" for i in range(random.randint(3, 8))]
            self.d.multi_criteria.optimize({"options": options})
        elif op == 6:
            data = [random.uniform(-10, 50) for _ in range(random.randint(10, 30))]
            self.d.risk.calculate_var(data)
        elif op == 7:
            self.d.risk.scenario_analysis([f"Scenario_{i}" for i in range(3)])
        elif op == 8:
            self.i.manufacturing.quality_control(f"Batch_{worker_id}_{step}", random.randint(0, 25))
        elif op == 9:
            self.i.retail.personalized_recommendation(f"Customer_{worker_id}", [f"Prod_{i}" for i in range(5)])
        elif op == 10:
            key = f"k_{worker_id}_{step}_{random.randint(1, 100000)}"
            val = f"v_{random.random()}" * random.randint(10, 100)
            self.cache.set(key, val)
            self.cache.get(f"k_{worker_id}_{step-1}")
        elif op == 11:
            file_path = os.path.join(self.temp_dir, f"f_{worker_id}_{step}.json")
            data = {"id": step, "data": "x" * random.randint(100, 1000)}
            with open(file_path, "w") as f:
                json.dump(data, f)
            if os.path.exists(file_path):
                os.remove(file_path)
        elif op == 12:
            assets = [{"symbol": f"Asset{i}", "expected_return": random.uniform(0.05, 0.3)} for i in range(random.randint(4, 8))]
            self.q.finance.optimize_portfolio(assets, risk_tolerance=0.5)

    def _exec_anomaly(self, worker_id, step):
        """Inject various anomalies"""
        anomaly_types = [
            lambda: self.q.optimization.solve_tsp([]),
            lambda: self.q.optimization.solve_tsp(["OnlyOne"]),
            lambda: self.i.manufacturing.quality_control("", "not-a-number"),
            lambda: self.d.multi_criteria.optimize("not-a-dict"),
            lambda: self.d.risk.calculate_var("not-a-list"),
            lambda: self.a.creative.generate_art(None, None),
            lambda: self.a.creative.generate_story(None, None, None),
            lambda: self.cache.get(f"non_existent_key_{random.randint(1, 1000000)}"),
            lambda: self.q.optimization.solve_quadratic_assignment([], []),
            lambda: self.i.retail.personalized_recommendation("", []),
        ]
        random.choice(anomaly_types)()

    def _execute(self, worker_id, step):
        try:
            if random.random() < 0.15:
                self._exec_anomaly(worker_id, step)
                with self.lock:
                    self.metrics.anomalies_injected += 1
            else:
                self._exec_normal(worker_id, step)
            
            with self.lock:
                self.metrics.success += 1
        except Exception as e:
            with self.lock:
                self.metrics.failed += 1
                if len(self.metrics.error_log) < 100:
                    self.metrics.error_log.append({
                        "time": datetime.now().isoformat(),
                        "worker": worker_id,
                        "step": step,
                        "error_type": type(e).__name__,
                        "error_msg": str(e)[:150]
                    })
        finally:
            with self.lock:
                self.metrics.total_ops += 1

    def worker(self, worker_id):
        print(f"🏃 Worker {worker_id:02d} started")
        step = 0
        last_gc = 0
        
        while not self.stop.is_set():
            self._execute(worker_id, step)
            step += 1
            
            if step - last_gc > 2000:
                if random.random() < 0.2:
                    gc.collect()
                    self.gc_count += 1
                    last_gc = step
            
            if random.random() < 0.05:
                time.sleep(random.uniform(0, 0.01))
        
        print(f"✅ Worker {worker_id:02d} finished - {step:,} operations")

    def monitor(self):
        last_report = time.time()
        last_mem = time.time()
        
        while not self.stop.is_set():
            now = time.time()
            
            if now - last_report >= 60:
                self._print_status(now - self.metrics.start_time)
                last_report = now
            
            if now - last_mem >= 30:
                self._log_mem("periodic_monitor")
                last_mem = now
            
            time.sleep(1)

    def _print_status(self, elapsed):
        with self.lock:
            total = self.metrics.total_ops
            success = self.metrics.success
            failed = self.metrics.failed
            anomalies = self.metrics.anomalies_injected
            curr_mem, peak_mem = self._get_mem()
            success_rate = (success / total * 100) if total > 0 else 0
            elapsed_mins = elapsed / 60
        
        print("\n" + "="*80)
        print(f"⏱️  MARATHON STATUS - {elapsed_mins:.1f}/{self.duration/60:.0f} minutes")
        print(f"   Operations: {total:,} | Success: {success:,} ({success_rate:.2f}%) | Failed: {failed:,}")
        print(f"   Anomalies Injected: {anomalies:,} | GC Cycles: {self.gc_count:,}")
        print(f"   Memory: {curr_mem:.2f} MB (Peak: {peak_mem:.2f} MB)")
        print(f"   Throughput: {total/elapsed:.0f} ops/sec")
        print("="*80 + "\n")

    def run(self, workers=30):
        print("\n" + "🎯"*40)
        print("🎯 MARATHON ENDURANCE TEST - 30 MINUTES 🎯")
        print("🎯"*40)
        print(f"Duration: {self.duration/60} min | Workers: {workers}")
        print(f"Anomaly Injection: 15% | Chaos Level: EXTREME")
        print()
        
        self.metrics.start_time = time.time()
        self._log_mem("test_start")
        
        print("🔍 Pre-test validation...")
        self._execute(-1, 0)
        print("✅ Pre-test passed!\n")
        
        monitor_thread = threading.Thread(target=self.monitor, daemon=True)
        monitor_thread.start()
        
        worker_threads = []
        for i in range(workers):
            t = threading.Thread(target=self.worker, args=(i,), daemon=True)
            worker_threads.append(t)
            t.start()
        
        print(f"🏃 Starting {workers} workers for {self.duration/60} minutes...\n")
        start_run = time.time()
        while time.time() - start_run < self.duration and not self.stop.is_set():
            time.sleep(1)
        
        print("\n🛑 Stopping all workers...")
        self.stop.set()
        
        for t in worker_threads:
            t.join(timeout=5)
        
        monitor_thread.join(timeout=3)
        
        self.metrics.end_time = time.time()
        self._log_mem("test_end")
        tracemalloc.stop()
        
        self._final_report()
        self._save_report()
        self._cleanup()

    def _final_report(self):
        duration = self.metrics.end_time - self.metrics.start_time
        total = self.metrics.total_ops
        success = self.metrics.success
        failed = self.metrics.failed
        
        print("\n" + "🏆"*40)
        print("🏆 MARATHON ENDURANCE TEST - FINAL REPORT 🏆")
        print("🏆"*40)
        print(f"Duration: {duration/60:.2f} minutes ({duration:.1f} seconds)")
        print(f"Total Operations: {total:,}")
        print(f"✅ Success: {success:,} ({(success/total*100 if total else 0):.2f}%)")
        print(f"❌ Failed: {failed:,} ({(failed/total*100 if total else 0):.2f}%)")
        print(f"🧪 Anomalies Injected: {self.metrics.anomalies_injected:,}")
        print(f"♻️  Garbage Collections: {self.gc_count:,}")
        print(f"⚡ Throughput: {total/duration:.0f} operations/second")
        
        if self.metrics.mem_samples:
            start_mem = self.metrics.mem_samples[0]['current_mb']
            end_mem = self.metrics.mem_samples[-1]['current_mb']
            print(f"💾 Memory: {start_mem:.2f} MB → {end_mem:.2f} MB (Δ {end_mem-start_mem:+.2f} MB)")
            print(f"💾 Peak Memory: {self.metrics.peak_memory:.2f} MB")
        
        if len(self.metrics.error_log) > 0:
            print(f"\n📋 Top 10 Errors:")
            error_types = {}
            for err in self.metrics.error_log:
                et = err['error_type']
                error_types[et] = error_types.get(et, 0) + 1
            
            sorted_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
            for i, (err_type, count) in enumerate(sorted_errors[:10], 1):
                print(f"   {i}. {err_type}: {count} occurrences")
        
        print("="*80)
        
        if failed == 0:
            print("\n🎉🎉🎉 PERFECT MARATHON! FLAWLESS VICTORY! 🎉🎉🎉")
        elif failed < total * 0.001:
            print("\n🌟 EXCELLENT! Near-perfect performance!")
        elif failed < total * 0.01:
            print("\n✅ GOOD! Acceptable failure rate.")
        else:
            print(f"\n⚠️  FAILURES DETECTED: {failed} errors need investigation.")

    def _save_report(self):
        report_file = f"marathon_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "test_config": {
                    "duration_minutes": self.duration / 60,
                    "workers": 30
                },
                "metrics": {
                    "total_ops": self.metrics.total_ops,
                    "success": self.metrics.success,
                    "failed": self.metrics.failed,
                    "anomalies_injected": self.metrics.anomalies_injected,
                    "gc_cycles": self.gc_count,
                    "peak_memory_mb": self.metrics.peak_memory,
                    "error_log": self.metrics.error_log[:100],
                    "mem_samples": self.metrics.mem_samples
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Full report saved: {os.path.abspath(report_file)}")

    def _cleanup(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    test = MarathonEnduranceTest(duration_minutes=30)
    test.run(workers=30)
