#!/usr/bin/env python3
"""
调试发现的缺陷
"""
import sys
import random
import traceback

sys.path.insert(0, '/workspace/agent_perpetual_evolution_system')

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache

print("=== 开始调试缺陷 ===")

quantum = QuantumApplicationPlatform()
agi = AGIApplicationFramework()
decision = IntelligentDecisionPlatform()
industry = IndustrySolutionsPlatform()
cache = get_global_cache()

chaos_inputs = [
    None, [], {}, 123, "invalid", ["City", None], [None],
    [1, 2, "3", None], {"a": None, "b": []}, True, False,
    float('inf'), float('-inf'), float('nan'),
    "", "   ", "\x00\x00\x00",
    [None, None, None], [[[[[]]]]],
    {"nested": {"deep": {"value": None}}},
    list(range(1000)), "a" * 10000
]

print("\n--- 测试行业解决方案 ---")

print("\n1. 测试 industry.retail.personalized_recommendation:")
try:
    result = industry.retail.personalized_recommendation(random.choice(chaos_inputs), random.choice(chaos_inputs))
    print(f"   结果: {result}")
except Exception as e:
    print(f"   错误: {type(e).__name__}: {e}")
    print(f"   堆栈:\n{traceback.format_exc()}")

print("\n2. 测试 industry.manufacturing.quality_control:")
try:
    result = industry.manufacturing.quality_control(random.choice(chaos_inputs), random.choice(chaos_inputs))
    print(f"   结果: {result}")
except Exception as e:
    print(f"   错误: {type(e).__name__}: {e}")
    print(f"   堆栈:\n{traceback.format_exc()}")

print("\n3. 测试 decision.multi_criteria.optimize:")
try:
    result = decision.multi_criteria.optimize({"options": random.choice(chaos_inputs)})
    print(f"   结果: {result}")
except Exception as e:
    print(f"   错误: {type(e).__name__}: {e}")
    print(f"   堆栈:\n{traceback.format_exc()}")

print("\n4. 测试 decision.risk.scenario_analysis:")
try:
    result = decision.risk.scenario_analysis(random.choice(chaos_inputs))
    print(f"   结果: {result}")
except Exception as e:
    print(f"   错误: {type(e).__name__}: {e}")
    print(f"   堆栈:\n{traceback.format_exc()}")

print("\n5. 测试 quantum.optimization.solve_quadratic_assignment:")
try:
    result = quantum.optimization.solve_quadratic_assignment(
        random.choice(chaos_inputs), random.choice(chaos_inputs), random.choice(chaos_inputs)
    )
    print(f"   结果: {result}")
except Exception as e:
    print(f"   错误: {type(e).__name__}: {e}")
    print(f"   堆栈:\n{traceback.format_exc()}")
