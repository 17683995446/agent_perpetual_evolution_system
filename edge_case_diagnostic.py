#!/usr/bin/env python3
"""
Edge case diagnostic test - check what parameter combinations fail
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform
import random

q = QuantumApplicationPlatform()
a = AGIApplicationFramework()
d = IntelligentDecisionPlatform()
i = IndustrySolutionsPlatform()

edge_cases = [
    # Test with empty lists
    ("TSP empty", lambda: q.optimization.solve_tsp([])),
    ("TSP one item", lambda: q.optimization.solve_tsp(["A"])),
    ("TSP None", lambda: q.optimization.solve_tsp(None)),

    # Test with edge values
    ("Weather 0 days", lambda: q.weather.predict_weather("loc", 0)),
    ("Weather -1 days", lambda: q.weather.predict_weather("loc", -1)),
    ("Weather 100 days", lambda: q.weather.predict_weather("loc", 100)),

    # Test with unusual parameters
    ("Chemistry 0 electrons", lambda: q.chemistry.simulate_molecule("H2O", 0)),
    ("Chemistry -1 electrons", lambda: q.chemistry.simulate_molecule("H2O", -1)),
    ("Chemistry large electrons", lambda: q.chemistry.simulate_molecule("H2O", 1000)),

    # Test various combinations
    ("QC negative defects", lambda: i.manufacturing.quality_control("batch", -1)),
    ("QC large defects", lambda: i.manufacturing.quality_control("batch", 999)),

    ("Strategic 0 months", lambda: d.strategic_planner.create_strategic_plan("v", 0, [])),
    ("Strategic negative months", lambda: d.strategic_planner.create_strategic_plan("v", -1, [])),

    ("Risk empty list", lambda: d.risk.calculate_var([])),
    ("Risk single item", lambda: d.risk.calculate_var([1])),
    ("Risk large list", lambda: d.risk.calculate_var([1] * 10000)),

    ("Scenario empty", lambda: d.risk.scenario_analysis([])),

    ("Multi-criteria empty", lambda: d.multi_criteria.optimize({"options": []})),
    ("Multi-criteria None", lambda: d.multi_criteria.optimize({"options": None})),

    # Test the new operations with edge cases
    ("Agri empty dict", lambda: i.agriculture.precision_planting({}, "Wheat")),
    ("Agri empty crop", lambda: i.agriculture.precision_planting({"size": 100}, "")),

    ("Logistics empty", lambda: i.logistics.route_optimization("", "", [])),
    ("Logistics None", lambda: i.logistics.route_optimization(None, None, None)),

    ("Env empty station", lambda: i.environment.pollution_monitoring("", ["PM2.5"])),
    ("Env empty pollutants", lambda: i.environment.pollution_monitoring("station", [])),

    ("Edu empty student", lambda: i.education.personalized_learning("", "Science")),
    ("Edu empty topic", lambda: i.education.personalized_learning("student", "")),

    ("Finance 0", lambda: i.finance.portfolio_optimization(0, "medium")),
    ("Finance negative", lambda: i.finance.portfolio_optimization(-100, "medium")),

    ("SupplyChain empty", lambda: q.supply_chain.optimize_inventory([], [])),
    ("SupplyChain None", lambda: q.supply_chain.optimize_inventory(None, None)),

    ("Traffic empty", lambda: q.traffic.optimize_traffic_light_timing([], {})),
    ("Traffic None", lambda: q.traffic.optimize_traffic_light_timing(None, None)),

    ("Robotics empty", lambda: a.robotics.plan_motion([], [])),
    ("Robotics None", lambda: a.robotics.plan_motion(None, None)),
]

print("=" * 80)
print("EDGE CASE DIAGNOSTIC TEST")
print("=" * 80)

errors = []
for name, func in edge_cases:
    try:
        result = func()
        status = "✅ OK"
    except Exception as e:
        status = f"❌ {type(e).__name__}: {str(e)[:80]}"
        errors.append((name, type(e).__name__, str(e)))

print(f"\nTotal Edge Cases: {len(edge_cases)}")
print(f"Passed: {len(edge_cases) - len(errors)}")
print(f"Failed: {len(errors)}")

if errors:
    print("\n" + "=" * 80)
    print("EDGE CASE ERRORS:")
    print("=" * 80)
    for name, err_type, msg in errors:
        print(f"\n{name}:")
        print(f"  {err_type}: {msg}")
