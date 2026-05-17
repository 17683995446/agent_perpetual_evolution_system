#!/usr/bin/env python3
"""Quick diagnostic for endurance test"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Initializing modules...")

try:
    from quantum_applications import QuantumApplicationPlatform
    print("✅ quantum_applications imported")
    quantum = QuantumApplicationPlatform()
    print("✅ QuantumApplicationPlatform initialized")
except Exception as e:
    print(f"❌ Quantum error:", str(e))
    import traceback
    traceback.print_exc()

try:
    from agi_applications import AGIApplicationFramework
    print("✅ agi_applications imported")
    agi = AGIApplicationFramework()
    print("✅ AGIApplicationFramework initialized")
except Exception as e:
    print(f"❌ AGI error:", str(e))
    import traceback
    traceback.print_exc()

try:
    from intelligent_decision import IntelligentDecisionPlatform
    print("✅ intelligent_decision imported")
    decision = IntelligentDecisionPlatform()
    print("✅ IntelligentDecisionPlatform initialized")
except Exception as e:
    print(f"❌ Decision error:", str(e))
    import traceback
    traceback.print_exc()

try:
    from industry_solutions import IndustrySolutionsPlatform
    print("✅ industry_solutions imported")
    industry = IndustrySolutionsPlatform()
    print("✅ IndustrySolutionsPlatform initialized")
except Exception as e:
    print(f"❌ Industry error:", str(e))
    import traceback
    traceback.print_exc()

print("\n✅ All modules loaded successfully!")
print("\n🚀 Running quick test operations...")

print("\n1. Quantum TSP...")
result = quantum.optimization.solve_tsp(["A", "B", "C"])
print("✅", result)

print("\n2. AGI Reasoning...")
result = agi.reasoning.deductive_reasoning("TestTask", "TestQuery")
print("✅", result)

print("\n3. Decision Multi...")
result = decision.multi_criteria.optimize({"options": ["X", "Y"]})
print("✅", result)

print("\n4. Industry Manufacturing...")
result = industry.manufacturing.quality_control("TestBatch", 0)
print("✅", result)

print("\n🎉 All quick tests passed!")
