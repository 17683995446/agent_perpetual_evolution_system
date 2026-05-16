#!/usr/bin/env python3
"""
调试混沌猴子攻击，找出具体是哪些方法调用有问题
"""
import sys
import random
import traceback

sys.path.insert(0, '/workspace/agent_perpetual_evolution_system')

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform

print("=== 调试混沌猴子攻击 ===\n")

quantum = QuantumApplicationPlatform()
agi = AGIApplicationFramework()
decision = IntelligentDecisionPlatform()
industry = IndustrySolutionsPlatform()

chaos_inputs = [
    None, [], {}, 123, "invalid", ["City", None], [None],
    [1, 2, "3", None], {"a": None, "b": []}, True, False,
    float('inf'), float('-inf'), float('nan'),
    "", "   ", "\x00\x00\x00",
    [None, None, None], [[[[[]]]]],
    {"nested": {"deep": {"value": None}}},
    list(range(1000)), "a" * 10000
]

attack_methods = [
    ("quantum_tsp", quantum.optimization.solve_tsp),
    ("quantum_resource", quantum.optimization.solve_resource_scheduling),
    ("agi_deductive", agi.reasoning.deductive_reasoning),
    ("agi_creative_art", agi.creative.generate_art),
    ("agi_creative_story", agi.creative.generate_story),
    ("decision_multi", decision.multi_criteria.optimize),
    ("decision_risk", decision.risk.calculate_var),
    ("decision_scenario", decision.risk.scenario_analysis),
    ("healthcare_diagnose", industry.healthcare.diagnose_disease),
    ("finance_portfolio", industry.finance.portfolio_optimization),
    ("manufacturing_quality", industry.manufacturing.quality_control),
    ("retail_recommend", industry.retail.personalized_recommendation)
]

print(f"准备测试 {len(attack_methods)} 个方法...\n")

for method_name, method in attack_methods:
    print(f"--- 测试方法: {method_name} ---")
    
    crashes = 0
    graceful_errors = 0
    successes = 0
    
    for _ in range(100):
        try:
            if method_name == "quantum_tsp":
                args = [random.choice(chaos_inputs)]
            elif method_name == "quantum_resource":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "agi_deductive":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "agi_creative_art":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "agi_creative_story":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "healthcare_diagnose":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "finance_portfolio":
                args = [random.randint(-1000000, 1000000), random.choice(["high", "low", None, 123])]
            elif method_name == "manufacturing_quality":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "retail_recommend":
                args = [random.choice(chaos_inputs), random.choice(chaos_inputs)]
            elif method_name == "decision_multi":
                args = [{"options": random.choice(chaos_inputs)}]
            elif method_name == "decision_risk":
                args = [random.choice(chaos_inputs)]
            elif method_name == "decision_scenario":
                args = [random.choice(chaos_inputs)]
            else:
                num_args = random.randint(0, 3)
                args = [random.choice(chaos_inputs) for _ in range(num_args)]
            
            result = method(*args)
            
            if isinstance(result, dict) and result.get("status") == "error":
                graceful_errors += 1
            else:
                successes += 1
                
        except Exception as e:
            crashes += 1
            if crashes <= 3:
                print(f"  崩溃! 错误类型: {type(e).__name__}, 信息: {str(e)}")
                print(f"  参数: {args}")
                print(f"  堆栈:\n{traceback.format_exc()}")
    
    print(f"  结果: {successes} 成功, {graceful_errors} 优雅错误, {crashes} 崩溃\n")
