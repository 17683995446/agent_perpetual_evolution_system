#!/usr/bin/env python3
"""
简单的调试测试，帮助我们找到具体的异常来源！
"""
import sys
import random
import traceback
from pprint import pprint

sys.path.insert(0, '/workspace/agent_perpetual_evolution_system')

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform

quantum = QuantumApplicationPlatform()
agi = AGIApplicationFramework()
decision = IntelligentDecisionPlatform()
industry = IndustrySolutionsPlatform()

bad_inputs = [None, [], {}, 123, "invalid", ["City", None], [None]]

print("\n=== 开始调试测试 ===\n")
crashes = 0

for i in range(100):
    choice = random.randint(0, 8)
    try:
        if choice == 0:
            print(f"[{i}] 调用 solve_tsp")
            result = quantum.optimization.solve_tsp(random.choice(bad_inputs))
            print(f"    结果: {result.get('status', 'ok')}")
        elif choice == 1:
            print(f"[{i}] 调用 deductive_reasoning")
            result = agi.reasoning.deductive_reasoning("", "")
            print(f"    结果: {result.get('status', 'ok')}")
        elif choice == 2:
            print(f"[{i}] 调用 optimize (多准则)")
            result = decision.multi_criteria.optimize({"options": random.choice(bad_inputs)})
            print(f"    结果: {result.get('status', 'ok')}")
        elif choice == 3:
            print(f"[{i}] 调用 diagnose_disease")
            result = industry.healthcare.diagnose_disease(random.choice(bad_inputs), {})
            print(f"    结果: {result.get('status', 'ok')}")
        elif choice == 4:
            print(f"[{i}] 调用 portfolio_optimization")
            result = industry.finance.portfolio_optimization(100000, "high")
            print(f"    结果: ok")
        elif choice == 5:
            print(f"[{i}] 调用 quality_control")
            result = industry.manufacturing.quality_control("Batch_001", 3)
            print(f"    结果: ok")
        elif choice == 6:
            print(f"[{i}] 调用 solve_resource_scheduling")
            result = quantum.optimization.solve_resource_scheduling(
                random.choice(bad_inputs), ["Res1", "Res2"]
            )
            print(f"    结果: {result.get('status', 'ok')}")
        elif choice == 7:
            print(f"[{i}] 调用 personalized_recommendation")
            result = industry.retail.personalized_recommendation("User_001", ["Beh1", "Beh2"])
            print(f"    结果: ok")
        elif choice == 8:
            print(f"[{i}] 调用 calculate_var")
            result = decision.risk.calculate_var(random.choice(bad_inputs))
            print(f"    结果: {result.get('status', 'ok')}")
    except Exception as e:
        crashes += 1
        print(f"\n❌ 崩溃发生在第 {i} 次迭代!")
        print(f"   异常类型: {type(e).__name__}")
        print(f"   异常信息: {str(e)}")
        print(f"   堆栈:\n{traceback.format_exc()}\n")

print(f"\n调试结束! 总崩溃数: {crashes}/100")

if crashes == 0:
    print("✅ 完美! 没有发现崩溃!")
else:
    print(f"⚠️  需要修复的崩溃数: {crashes}")
