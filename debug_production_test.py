#!/usr/bin/env python3
"""调试生产场景测试失败的部分"""

import sys
import traceback
import random

sys.path.insert(0, '/workspace/agent_perpetual_evolution_system')

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache

print("=== 初始化平台 ===")
quantum = QuantumApplicationPlatform()
agi = AGIApplicationFramework()
decision = IntelligentDecisionPlatform()
industry = IndustrySolutionsPlatform()
cache = get_global_cache()

print("\n=== 1. 调试随机延迟和超时模拟 ===")
try:
    for i in range(10):
        print(f"\n  尝试操作 {i}...")
        delay = random.uniform(0, 0.01)
        import time
        time.sleep(delay)
        op_type = random.choice(["tsp", "art", "decision", "quality", "finance"])
        print(f"  选择操作: {op_type}")
        
        if op_type == "tsp":
            result = quantum.optimization.solve_tsp([f"City{i}A", f"City{i}B", f"City{i}C"])
            print(f"  TSP 结果: {result}")
        elif op_type == "art":
            result = agi.creative.generate_art(f"Art{i}", "abstract")
            print(f"  Art 结果: {result}")
        elif op_type == "decision":
            result = decision.multi_criteria.optimize({"options": [f"Opt{i}1", f"Opt{i}2"]})
            print(f"  Decision 结果: {result}")
        elif op_type == "quality":
            result = industry.manufacturing.quality_control(f"Batch{i}", random.randint(0, 10))
            print(f"  Quality 结果: {result}")
        elif op_type == "finance":
            result = quantum.finance.portfolio_optimization([0.1, 0.2, 0.3, 0.4])
            print(f"  Finance 结果: {result}")
except Exception as e:
    print(f"❌ 错误: {type(e).__name__}: {e}")
    print(traceback.format_exc())

print("\n=== 2. 调试内存压力与垃圾回收 ===")
try:
    import gc
    gc.collect()
    print("  GC 完成")
    
    for _ in range(5):
        print(f"\n  循环 {_}...")
        large_list = [{"id": i, "data": "x"*100} for i in range(100)]
        print(f"  列表长度: {len(large_list)}")
        
        for obj in large_list:
            if obj["id"] % 10 == 0:
                result = agi.language.text_generation(f"MemoryTest{obj['id']}")
                print(f"  文本生成: {result['status'] if isinstance(result, dict) else result}")
        
        print("  删除列表")
        del large_list
        
        if _ % 2 == 0:
            gc.collect()
            print("  触发 GC")
    
    print("✅ 内存测试成功")
except Exception as e:
    print(f"❌ 错误: {type(e).__name__}: {e}")
    print(traceback.format_exc())

print("\n=== 3. 调试混合场景中的各个功能 ===")
test_cases = [
    ("plan_generation", lambda: decision.strategic.plan_generation("TestPlan")),
    ("image_analysis", lambda: agi.vision.image_analysis("TestImage")),
    ("optimize_inventory", lambda: quantum.supply_chain.optimize_inventory([1, 2, 3]))
]

for name, func in test_cases:
    try:
        print(f"\n  测试 {name}...")
        result = func()
        print(f"  ✅ 结果: {result}")
    except Exception as e:
        print(f"  ❌ {name} 错误: {type(e).__name__}: {e}")
        print(traceback.format_exc())
