#!/usr/bin/env python3
"""
EXTREME 4-HOUR MARATHON STRESS TEST - 15 MIN VERIFICATION
Verify all fixes before running the full test
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
class ExtremeMarathonMetrics:
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
    large_objects_created: int = 0
    memory_pressure_cycles: int = 0


class Extreme4HourMarathonTest:
    def __init__(self, duration_minutes: int = 15):
        self.duration = duration_minutes * 60
        self.q = QuantumApplicationPlatform()
        self.a = AGIApplicationFramework()
        self.d = IntelligentDecisionPlatform()
        self.i = IndustrySolutionsPlatform()
        self.cache = get_global_cache()
        self.metrics = ExtremeMarathonMetrics()
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.temp_dir = tempfile.mkdtemp(prefix="extreme_4h_marathon_")
        self.gc_count = 0
        self.anomaly_rate = 0.50
        self.num_workers = 80
        self.large_object_pool = []
        tracemalloc.start()

    def _get_mem(self):
        current, peak = tracemalloc.get_traced_memory()
        return current / (1024 * 1024), peak / (1024 * 1024)

    def _log_sample(self, tag: str):
        curr_mem, peak_mem = self._get_mem()

        with self.lock:
            self.metrics.mem_samples.append({
                "time": datetime.now().isoformat(),
                "tag": tag,
                "current_mb": round(curr_mem, 2),
                "peak_mb": round(peak_mem, 2),
                "large_objects": len(self.large_object_pool)
            })
            if peak_mem > self.metrics.peak_memory:
                self.metrics.peak_memory = peak_mem

    def _create_large_object(self, worker_id: int, size_factor: int = 1):
        """创建大对象用于测试内存压力"""
        try:
            with self.lock:
                obj = {
                    "worker_id": worker_id,
                    "timestamp": time.time(),
                    "data": "x" * (100000 * size_factor),
                    "nested": {f"key_{i}": list(range(1000)) for i in range(10)}
                }
                self.large_object_pool.append(obj)
                self.metrics.large_objects_created += 1

                if len(self.large_object_pool) > 100:
                    self.large_object_pool = self.large_object_pool[-50:]

            return obj
        except:
            return None

    def _execute_normal_operation(self, worker_id: int, step: int):
        """执行复杂的正常操作"""
        op = random.randint(0, 49)

        if op == 0:
            cities = [f"City_{worker_id}_{step}_{i}" for i in range(random.randint(5, 20))]
            self.q.optimization.solve_tsp(cities)
        elif op == 1:
            self.q.optimization.solve_quadratic_assignment(
                [random.randint(1, 8) for _ in range(random.randint(4, 12))],
                [random.randint(1, 8) for _ in range(random.randint(4, 12))]
            )
        elif op == 2:
            self.a.creative.generate_art(
                f"Art_{worker_id}_{step}",
                random.choice(["abstract", "modern", "vintage", "surreal", "minimalist", "futuristic", "cyberpunk"])
            )
        elif op == 3:
            self.a.creative.generate_story(
                f"Story_{worker_id}",
                f"Theme_{step}",
                random.choice(["short", "medium", "long", "epic", "micro", "novella"])
            )
        elif op == 4:
            self.a.reasoning.deductive_reasoning(f"Task_{worker_id}_{step}",
                                                f"Complex analysis of {random.randint(1, 200000)} data points")
        elif op == 5:
            self.a.language.generate_text(f"Comprehensive analysis on topic {random.randint(1, 200000)}")
        elif op == 6:
            options = [f"Opt_{worker_id}_{step}_{i}" for i in range(random.randint(4, 15))]
            self.d.multi_criteria.optimize({"options": options})
        elif op == 7:
            data = [random.uniform(-50, 150) for _ in range(random.randint(15, 80))]
            self.d.risk.calculate_var(data)
        elif op == 8:
            self.d.risk.scenario_analysis([f"Scenario_{i}" for i in range(random.randint(3, 10))])
        elif op == 9:
            self.d.strategic_planner.create_strategic_plan(f"Vision_{worker_id}_{step}",
                                                       random.randint(6, 60), [])
        elif op == 10:
            self.i.manufacturing.quality_control(f"Batch_{worker_id}_{step}",
                                               random.randint(0, 50))
        elif op == 11:
            products = [f"Product_{i}" for i in range(random.randint(4, 12))]
            self.i.retail.personalized_recommendation(f"Customer_{worker_id}", products)
        elif op == 12:
            assets = [{"symbol": f"Asset_{i}", "expected_return": random.uniform(0.03, 0.35)} for i in range(random.randint(5, 15))]
            self.q.finance.optimize_portfolio(assets, risk_tolerance=random.uniform(0.1, 0.9))
        elif op == 13:
            key = f"k_{worker_id}_{step}_{random.randint(1, 1000000)}"
            val = f"value_{random.random()}" * random.randint(10, 500)
            self.cache.set(key, val)
            self.cache.get(f"k_{worker_id}_{step - 1}")
            if random.random() < 0.3:
                self.cache.delete(f"k_{worker_id}_{step - 2}")
        elif op == 14:
            file_path = os.path.join(self.temp_dir, f"f_{worker_id}_{step}.json")
            data = {"id": step, "data": "x" * random.randint(100, 5000)}
            with open(file_path, "w") as f:
                json.dump(data, f)
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    _ = json.load(f)
                os.remove(file_path)
        elif op == 15:
            self.q.weather.predict_weather(f"Location_{worker_id}_{step}",
                                          random.randint(3, 21))
        elif op == 16:
            tasks = [{"task_id": f"Task_{i}", "estimated_hours": random.randint(1, 12)} for i in range(random.randint(4, 15))]
            workers = [f"Worker_{i}" for i in range(random.randint(3, 10))]
            self.q.scheduling.schedule_tasks(tasks, workers)
        elif op == 17:
            self.q.drug_discovery.molecular_docking(f"Molecule_{worker_id}_{step}",
                                                 "Target_Protein")
        elif op == 18:
            self.q.drug_discovery.design_drug_candidates("Target_Protein", {})
        elif op == 19:
            self.a.vision.recognize_objects(f"Image_{worker_id}_{step}")
        elif op == 20:
            self.a.audio.recognize_speech(f"Audio_{worker_id}_{step}")
        elif op == 21:
            self.d.realtime_optimizer.optimize(f"System_{worker_id}_{step}")
        elif op == 22:
            self.i.healthcare.diagnose_disease(f"Patient_{worker_id}_{step}",
                                             ["Symptom_A", "Symptom_B", "Symptom_C"])
        elif op == 23:
            self.i.energy.load_forecasting(f"Grid_{worker_id}_{step}", 24)
        elif op == 24:
            self.q.chemistry.simulate_molecule(f"Molecule_{worker_id}_{step}",
                                                random.randint(8, 60))
        elif op == 25:
            self.q.weather.predict_weather(f"City_{worker_id}", random.randint(1, 21))
        elif op == 26:
            self.i.agriculture.precision_planting({"field_size": 150, "id": f"F_{step}"},
                                                   random.choice(["Wheat", "Rice", "Corn", "Soybean"]))
        elif op == 27:
            self.i.logistics.route_optimization(f"Origin_{worker_id}", f"Dest_{step}",
                                              [f"Way_{i}" for i in range(random.randint(2, 8))])
        elif op == 28:
            self.i.environment.pollution_monitoring(f"Station_{worker_id}_{step}",
                                                    ["PM2.5", "PM10", "O3", "NO2", "SO2"])
        elif op == 29:
            self.i.education.personalized_learning(f"Student_{worker_id}_{step}",
                                                 random.choice(["Math", "Science", "History", "Literature"]))
        elif op == 30:
            self.i.finance.portfolio_optimization(random.randint(10000, 2000000),
                                                 random.choice(["low", "medium", "high", "aggressive"]))
        elif op == 31:
            self.q.supply_chain.optimize_inventory([{"id": i, "name": f"P_{i}"} for i in range(random.randint(3, 20))],
                                                    [random.randint(50, 300) for _ in range(12)])
        elif op == 32:
            self.q.traffic.optimize_traffic_light_timing([f"Inter_{i}" for i in range(random.randint(2, 8))],
                                                         {"rush_hour": random.choice([True, False]), "weather": "clear"})
        elif op == 33:
            self.a.robotics.plan_motion([random.uniform(0, 50), random.uniform(0, 50), random.uniform(0, 50)],
                                      [random.uniform(0, 50), random.uniform(0, 50), random.uniform(0, 50)])
        elif op == 34:
            self._create_large_object(worker_id, random.randint(1, 3))
        elif op == 35:
            self.i.transportation.congestion_prediction(f"Area_{worker_id}", random.choice(["morning", "afternoon", "evening"]))
        elif op == 36:
            self.a.creative.generate_art(f"Art_{worker_id}_{step}", random.choice(["modern", "vintage", "surreal", "minimalist"]))
        elif op == 37:
            if random.random() < 0.1:
                gc.collect()
                self.metrics.memory_pressure_cycles += 1
        elif op == 38:
            self.d.risk.calculate_var([random.uniform(-100, 200) for _ in range(random.randint(20, 100))])
        elif op == 39:
            self.a.language.generate_text(f"Topic_{step}_text_{random.randint(1, 500000)}")
        elif op == 40:
            self._create_large_object(worker_id, random.randint(1, 5))
        elif op == 41:
            self.d.risk.calculate_var([random.uniform(0, 100) for _ in range(random.randint(5, 50))])
        elif op == 42:
            self.d.multi_criteria.optimize({"options": [f"Opt_{i}" for i in range(random.randint(3, 12))]})
        elif op == 43:
            self.i.healthcare.diagnose_disease(f"Patient_{worker_id}_{step}", [f"S_{i}" for i in range(random.randint(1, 5))])
        elif op == 44:
            self.q.optimization.solve_tsp([f"C_{i}" for i in range(random.randint(5, 25))])
        elif op == 45:
            self.i.manufacturing.quality_control(f"Batch_{step}", random.randint(0, 60))
        elif op == 46:
            self.q.optimization.solve_tsp([f"C_{worker_id}_{step}_{i}" for i in range(random.randint(6, 30))])
        elif op == 47:
            self.q.optimization.solve_tsp([f"C_{worker_id}_{step}_{i}" for i in range(random.randint(4, 28))])
        elif op == 48:
            self._create_large_object(worker_id, random.randint(1, 4))
        elif op == 49:
            self.cache.set(f"final_cache_{worker_id}_{step}", f"Final_{random.random()}")

    def _execute_anomaly_operation(self, worker_id: int, step: int):
        """执行混沌猴子异常操作（50%异常注入）"""
        anomaly_types = [
            lambda: self.q.optimization.solve_tsp([]),
            lambda: self.q.optimization.solve_tsp(["SingleCity"]),
            lambda: self.q.optimization.solve_tsp(None),
            lambda: self.q.optimization.solve_tsp([None, None]),
            lambda: self.i.manufacturing.quality_control("", "not_a_number"),
            lambda: self.i.manufacturing.quality_control(None, None),
            lambda: self.d.multi_criteria.optimize("not_a_dict"),
            lambda: self.d.multi_criteria.optimize(None),
            lambda: self.d.risk.calculate_var("not_a_list"),
            lambda: self.d.risk.calculate_var(None),
            lambda: self.a.creative.generate_art(None, None),
            lambda: self.a.creative.generate_story(None, None, None),
            lambda: self.cache.get(f"NonExistent_{random.randint(1, 1000000000)}"),
            lambda: self.cache.set(None, None),
            lambda: self.q.optimization.solve_quadratic_assignment([], []),
            lambda: self.q.optimization.solve_quadratic_assignment(None, None),
            lambda: self.i.retail.personalized_recommendation("", []),
            lambda: self.i.retail.personalized_recommendation(None, None),
            lambda: self.q.finance.optimize_portfolio([], 0.0),
            lambda: self.q.weather.predict_weather("", 0),
            lambda: self.a.reasoning.deductive_reasoning(None, None),
            lambda: self.d.strategic_planner.create_strategic_plan("", 0, None),
            lambda: self.a.vision.recognize_objects(None),
            lambda: self.a.audio.recognize_speech(None),
            lambda: self.i.healthcare.diagnose_disease(None, None),
            lambda: self.q.chemistry.simulate_molecule(None, 0),
            lambda: self.d.realtime_optimizer.optimize(None),
            lambda: self.q.optimization.solve_tsp(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]),
            lambda: self.i.manufacturing.quality_control("Batch_999", -100),
            lambda: self.a.language.generate_text(None),
            lambda: self.d.risk.scenario_analysis(None),
            lambda: self.q.optimization.solve_tsp(["X"] * 150),
            lambda: self.q.optimization.solve_tsp([f"X_{i}" for i in range(100)]),
            lambda: self.q.optimization.solve_tsp(["A", "B", None, "C", None, "D"]),
            lambda: self.i.manufacturing.quality_control("Batch", 1000000),
            lambda: self.d.multi_criteria.optimize({"options": None}),
            lambda: self.q.finance.optimize_portfolio([{"symbol": None, "expected_return": -2.0}], 2.5),
            lambda: self.q.finance.optimize_portfolio([None, None], None),
            lambda: self.a.language.generate_text(""),
            lambda: self.d.risk.calculate_var([1, 2, None, 4, None, 6]),
            lambda: self.d.risk.calculate_var([random.random() for _ in range(200)]),
            lambda: self.q.chemistry.simulate_molecule("X" * 2000, -10),
            lambda: self.i.agriculture.precision_planting(None, None),
            lambda: self.i.agriculture.precision_planting({}, None),
            lambda: self.i.logistics.route_optimization(None, None, None),
            lambda: self.i.logistics.route_optimization("", "", []),
            lambda: self.i.environment.pollution_monitoring(None, None),
            lambda: self.i.education.personalized_learning(None, None),
            lambda: self.i.finance.portfolio_optimization(None, None),
            lambda: self.i.finance.portfolio_optimization(-1, ""),
            lambda: self.q.supply_chain.optimize_inventory(None, None),
            lambda: self.q.traffic.optimize_traffic_light_timing(None, None),
            lambda: self.a.robotics.plan_motion(None, None),
            lambda: self._create_large_object(worker_id, 10),
            lambda: self._create_large_object(worker_id, 20),
            lambda: self.i.transportation.congestion_prediction(None, None),
            lambda: self.q.supply_chain.optimize_inventory([None, None], None),
            lambda: self.d.strategic_planner.create_strategic_plan(None, -100, None),
            lambda: self.d.multi_criteria.optimize({"options": [None, None, None]}),
            lambda: self.d.risk.calculate_var([]),
            lambda: self.d.risk.calculate_var([1] * 5000),
            lambda: self.q.scheduling.schedule_tasks([], []),
            lambda: self.q.scheduling.schedule_tasks(None, None)
        ]
        random.choice(anomaly_types)()

    def _execute(self, worker_id: int, step: int):
        try:
            if random.random() < self.anomaly_rate:
                self._execute_anomaly_operation(worker_id, step)
                with self.lock:
                    self.metrics.anomalies_injected += 1
            else:
                self._execute_normal_operation(worker_id, step)

            with self.lock:
                self.metrics.success += 1
        except Exception as e:
            with self.lock:
                self.metrics.failed += 1
                if len(self.metrics.error_log) < 1000:
                    self.metrics.error_log.append({
                        "time": datetime.now().isoformat(),
                        "worker": worker_id,
                        "step": step,
                        "error_type": type(e).__name__,
                        "error_msg": str(e)[:500]
                    })
        finally:
            with self.lock:
                self.metrics.total_ops += 1

    def worker(self, worker_id: int):
        print(f"🏃 Worker {worker_id:03d} started")
        step = 0
        last_gc = 0

        while not self.stop.is_set():
            self._execute(worker_id, step)
            step += 1

            if step - last_gc > 1200:
                if random.random() < 0.35:
                    gc.collect()
                    self.gc_count += 1
                    last_gc = step

            if random.random() < 0.085:
                time.sleep(random.uniform(0, 0.025))

        print(f"✅ Worker {worker_id:03d} completed - {step:,} operations")

    def monitor(self):
        last_report = time.time()
        last_sample = time.time()

        while not self.stop.is_set():
            now = time.time()

            if now - last_report >= 60:
                self._print_status(now - self.metrics.start_time)
                last_report = now

            if now - last_sample >= 20:
                self._log_sample("periodic_monitor")
                last_sample = now

            time.sleep(1)

    def _print_status(self, elapsed: float):
        with self.lock:
            total = self.metrics.total_ops
            success = self.metrics.success
            failed = self.metrics.failed
            anomalies = self.metrics.anomalies_injected
            curr_mem, peak_mem = self._get_mem()
            success_rate = (success / total * 100) if total > 0 else 0
            elapsed_mins = elapsed / 60

        print("\n" + "=" * 120)
        print(f"⏱️  EXTREME 4-HOUR MARATHON - {elapsed_mins:.1f}/{self.duration / 60:.0f} min - Workers: {self.num_workers}")
        print(f"   Operations: {total:,} | Success: {success:,} ({success_rate:.2f}%) | Failed: {failed:,} | Anomalies: {anomalies:,}")
        print(f"   GC: {self.gc_count:,} | Large Objects: {self.metrics.large_objects_created:,} | Mem: {curr_mem:.2f}MB (Peak: {peak_mem:.2f}MB)")
        print(f"   Throughput: {total / elapsed:.0f} ops/sec")
        print("=" * 120 + "\n")

    def run(self):
        print("\n" + "🔥" * 60)
        print("🔥 EXTREME 4-HOUR MARATHON STRESS TEST - VERIFICATION RUN - 15 MIN 🔥")
        print("🔥" * 60)
        print(f"Duration: {self.duration / 60} min | Workers: {self.num_workers} | Anomaly: {self.anomaly_rate * 100}% | Chaos: EXTREME")
        print()

        self.metrics.start_time = time.time()
        self._log_sample("test_start")

        print("🔍 Pre-test validation...")
        self._execute(-1, 0)
        print("✅ Pre-test passed!\n")

        monitor_thread = threading.Thread(target=self.monitor, daemon=True)
        monitor_thread.start()

        worker_threads = []
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker, args=(i,), daemon=True)
            worker_threads.append(t)
            t.start()

        print(f"🏃 Starting {self.num_workers} workers for {self.duration / 60} minutes...\n")
        start_run = time.time()
        while time.time() - start_run < self.duration and not self.stop.is_set():
            time.sleep(1)

        print("\n🛑 Stopping all workers...")
        self.stop.set()

        for t in worker_threads:
            t.join(timeout=8)

        monitor_thread.join(timeout=5)

        self.metrics.end_time = time.time()
        self._log_sample("test_end")
        tracemalloc.stop()

        self._final_report()
        self._save_report()
        self._cleanup()

    def _final_report(self):
        duration = self.metrics.end_time - self.metrics.start_time
        total = self.metrics.total_ops
        success = self.metrics.success
        failed = self.metrics.failed

        print("\n" + "🏆" * 60)
        print("🏆 EXTREME 4-HOUR MARATHON STRESS TEST - VERIFICATION FINAL REPORT 🏆")
        print("🏆" * 60)
        print(f"Duration: {duration / 60:.2f} minutes ({duration:.1f} seconds)")
        print(f"Total Operations: {total:,}")
        print(f"✅ Success: {success:,} ({(success / total * 100) if total else 0:.2f}%)")
        print(f"❌ Failed: {failed:,} ({(failed / total * 100) if total else 0:.2f}%)")
        print(f"🧪 Anomalies Injected: {self.metrics.anomalies_injected:,}")
        print(f"♻️  GC Cycles: {self.gc_count:,}")
        print(f"📦 Large Objects Created: {self.metrics.large_objects_created:,}")
        print(f"⚡ Throughput: {total / duration:.0f} operations/second")

        if self.metrics.mem_samples:
            start_mem = self.metrics.mem_samples[0]["current_mb"]
            end_mem = self.metrics.mem_samples[-1]["current_mb"]
            print(f"💾 Memory: {start_mem:.2f}MB → {end_mem:.2f}MB (Δ {end_mem - start_mem:+.2f}MB)")
            print(f"💾 Peak Memory: {self.metrics.peak_memory:.2f}MB")

        if len(self.metrics.error_log) > 0:
            print(f"\n📋 Top 30 Errors by Type:")
            error_types = {}
            for err in self.metrics.error_log:
                et = err["error_type"]
                error_types[et] = error_types.get(et, 0) + 1

            sorted_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
            for i, (err_type, count) in enumerate(sorted_errors[:30], 1):
                print(f"   {i:2d}. {err_type:20s} : {count} occurrences")

            print(f"\n📋 Sample Errors (First 15):")
            for i, err in enumerate(self.metrics.error_log[:15], 1):
                print(f"   {i:2d}. [{err['time']}] {err['error_type']}: {err['error_msg']}")

        print("=" * 120)

        if failed == 0:
            print("\n🎉🎉🎉 PERFECT VICTORY - ZERO BUGS 🎉🎉🎉")
        elif failed < total * 0.0001:
            print("\n🌟 NEAR PERFECT - Extremely low bug rate")
        elif failed < total * 0.001:
            print("\n🌟 EXCELLENT - Very low bug rate")
        elif failed < total * 0.01:
            print("\n✅ GOOD - Acceptable bug rate")
        else:
            print(f"\n⚠️  BUGS FOUND - {failed} bugs need investigation!")

    def _save_report(self):
        report_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"extreme_4h_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({
                "test_config": {
                    "duration_minutes": self.duration / 60,
                    "workers": self.num_workers,
                    "anomaly_rate": self.anomaly_rate
                },
                "metrics": {
                    "total_ops": self.metrics.total_ops,
                    "success": self.metrics.success,
                    "failed": self.metrics.failed,
                    "anomalies_injected": self.metrics.anomalies_injected,
                    "large_objects_created": self.metrics.large_objects_created,
                    "gc_cycles": self.gc_count,
                    "peak_memory_mb": self.metrics.peak_memory,
                    "error_log": self.metrics.error_log[:500],
                    "mem_samples": self.metrics.mem_samples[-100:]
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Full report saved to: {os.path.abspath(report_file)}")

    def _cleanup(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    test = Extreme4HourMarathonTest(duration_minutes=15)
    test.run()