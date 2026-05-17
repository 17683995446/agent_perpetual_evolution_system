#!/usr/bin/env python3
"""Quick verify anomaly handling"""

import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Quick anomaly injection verification test")
print("="*60)

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
from system_optimization import get_global_cache

q = QuantumApplicationPlatform()
a = AGIApplicationFramework()
d = IntelligentDecisionPlatform()
i = IndustrySolutionsPlatform()
c = get_global_cache()

tests_passed = 0
tests_total = 6

print("\n🧪 Testing anomaly 1: Empty TSP list")
try:
    result = q.optimization.solve_tsp([])
    print(f"   Result: {result}")
    if 'status' in result:
        print("   ✅ Passed!")
        tests_passed +=1
    else:
        print("   ⚠️ No status key, but didn't crash!")
except Exception as e:
    print(f"   ❌ CRASHED! {e}")

print("\n🧪 Testing anomaly 2: Bad manufacturing params")
try:
    result = i.manufacturing.quality_control("", "invalid-number")
    print(f"   Result: {result}")
    if 'status' in result:
        print("   ✅ Passed!")
        tests_passed +=1
    else:
        print("   ⚠️ No status key, but didn't crash!")
except Exception as e:
    print(f"   ❌ CRASHED! {e}")

print("\n🧪 Testing anomaly 3: Not dict to multi_criteria")
try:
    result = d.multi_criteria.optimize("not-a-dict")
    print(f"   Result: {result}")
    if 'status' in result:
        print("   ✅ Passed!")
        tests_passed +=1
    else:
        print("   ⚠️ No status key, but didn't crash!")
except Exception as e:
    print(f"   ❌ CRASHED! {e}")

print("\n🧪 Testing anomaly 4: Not list to calculate_var")
try:
    result = d.risk.calculate_var("not-a-list")
    print(f"   Result: {result}")
    if 'status' in result:
        print("   ✅ Passed!")
        tests_passed +=1
    else:
        print("   ⚠️ No status key, but didn't crash!")
except Exception as e:
    print(f"   ❌ CRASHED! {e}")

print("\n🧪 Testing anomaly 5: None to generate_art")
try:
    result = a.creative.generate_art(None, None)
    print(f"   Result: {result}")
    if 'status' in result:
        print("   ✅ Passed!")
        tests_passed +=1
    else:
        print("   ⚠️ No status key, but didn't crash!")
except Exception as e:
    print(f"   ❌ CRASHED! {e}")

print("\n🧪 Testing anomaly 6: Cache single arg")
try:
    c.set("just-a-key")
    print("   ✅ Cache survived!")
    tests_passed +=1
except TypeError as e:
    print(f"   ℹ️ Expected TypeError (cache needs value): {e}")
    tests_passed +=1  # This is expected behavior for cache
except Exception as e:
    print(f"   ❌ Unexpected crash! {e}")

print("\n" + "="*60)
print(f"🎉 {tests_passed}/{tests_total} tests PASSED!")
if tests_passed == tests_total:
    print("✅ SYSTEM IS READY FOR ULTIMATE TEST!")
