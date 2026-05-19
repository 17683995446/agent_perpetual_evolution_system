#!/usr/bin/env python3
"""
Additional API diagnostic test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from industry_solutions import IndustrySolutionsPlatform
from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework

i = IndustrySolutionsPlatform()
q = QuantumApplicationPlatform()
a = AGIApplicationFramework()

test_cases = [
    ("Agriculture", lambda: i.agriculture.precision_planting({"field_size": 100}, "Wheat")),
    ("Logistics", lambda: i.logistics.route_optimization("origin", "dest", ["wp1"])),
    ("Environment", lambda: i.environment.pollution_monitoring("station", ["PM2.5"])),
    ("Education", lambda: i.education.personalized_learning("student", "Science")),
    ("Finance", lambda: i.finance.portfolio_optimization(100000, "medium")),
    ("SupplyChain", lambda: q.supply_chain.optimize_inventory([{"id": 1, "name": "P1"}], [100])),
    ("Traffic", lambda: q.traffic.optimize_traffic_light_timing(["I1"], {"rush": True})),
    ("Robotics", lambda: a.robotics.plan_motion([0,0,0], [10,10,10])),
]

print("=" * 80)
print("ADDITIONAL API DIAGNOSTIC TEST")
print("=" * 80)

errors = []
for name, func in test_cases:
    try:
        result = func()
        status = "✅ OK"
    except Exception as e:
        status = f"❌ ERROR: {type(e).__name__}: {str(e)[:100]}"
        errors.append((name, type(e).__name__, str(e)))

print(f"\nTotal Tests: {len(test_cases)}")
print(f"Passed: {len(test_cases) - len(errors)}")
print(f"Failed: {len(errors)}")

if errors:
    print("\n" + "=" * 80)
    print("ERRORS FOUND:")
    print("=" * 80)
    for name, err_type, msg in errors:
        print(f"\n{name}:")
        print(f"  Type: {err_type}")
        print(f"  Message: {msg}")
else:
    print("\n🎉 ALL TESTS PASSED!")
