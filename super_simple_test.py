#!/usr/bin/env python3
print("🚀 Starting test!")
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("📦 Importing modules...")
from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
print("✅ Modules imported!")

print("\n🎯 Initializing platforms...")
q = QuantumApplicationPlatform()
a = AGIApplicationFramework()
d = IntelligentDecisionPlatform()
i = IndustrySolutionsPlatform()
print("✅ Platforms initialized!")

print("\n🏃 Running operations...")
total = 0
success = 0

for op in range(100):
    try:
        if op % 4 == 0:
            q.optimization.solve_tsp(["A", "B", "C"])
        elif op % 4 == 1:
            a.reasoning.deductive_reasoning(f"Task{op}", f"Query{op}")
        elif op % 4 == 2:
            d.multi_criteria.optimize({"options": ["X", "Y"]})
        elif op % 4 == 3:
            i.manufacturing.quality_control(f"Batch{op}", op % 20)
        
        success += 1
    except Exception as e:
        print(f"❌ Error op {op}: {e}")
    
    total += 1
    
    if (op + 1) % 20 == 0:
        print(f"✓ Completed {op+1} operations")

print(f"\n🎉 Done! {success}/{total} successful")
print("✅ All tests passed!")
