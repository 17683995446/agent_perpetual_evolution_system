#!/usr/bin/env python3
"""
Quick API diagnostic test to identify failures
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from industry_solutions import IndustrySolutionsPlatform

q = QuantumApplicationPlatform()
a = AGIApplicationFramework()
d = IntelligentDecisionPlatform()
i = IndustrySolutionsPlatform()

test_cases = [
    ("Quantum TSP", lambda: q.optimization.solve_tsp(["A", "B", "C"])),
    ("Quantum QAP", lambda: q.optimization.solve_quadratic_assignment([1,2,3], [4,5,6])),
    ("Creative Art", lambda: a.creative.generate_art("abstract", "modern")),
    ("Creative Story", lambda: a.creative.generate_story("genre", "theme", "medium")),
    ("Reasoning", lambda: a.reasoning.deductive_reasoning("task", "rule")),
    ("Language", lambda: a.language.generate_text("prompt")),
    ("Multi-Criteria", lambda: d.multi_criteria.optimize({"options": ["A", "B"]})),
    ("Risk VAR", lambda: d.risk.calculate_var([1,2,3,4,5])),
    ("Risk Scenario", lambda: d.risk.scenario_analysis(["S1", "S2"])),
    ("Strategic", lambda: d.strategic_planner.create_strategic_plan("vision", 24, [])),
    ("Manufacturing QC", lambda: i.manufacturing.quality_control("batch", 10)),
    ("Retail Rec", lambda: i.retail.personalized_recommendation("customer", ["b1", "b2"])),
    ("Finance Portfolio", lambda: q.finance.optimize_portfolio([{"symbol": "A", "expected_return": 0.1}], 0.5)),
    ("Weather", lambda: q.weather.predict_weather("location", 7)),
    ("Scheduling", lambda: q.scheduling.schedule_tasks([{"task_id": "T1", "estimated_hours": 5}], ["W1"])),
    ("Drug Discovery", lambda: q.drug_discovery.molecular_docking("mol", "protein")),
    ("Drug Design", lambda: q.drug_discovery.design_drug_candidates("protein", {})),
    ("Vision", lambda: a.vision.recognize_objects("image")),
    ("Audio", lambda: a.audio.recognize_speech("audio")),
    ("Realtime Opt", lambda: d.realtime_optimizer.optimize("system")),
    ("Healthcare", lambda: i.healthcare.diagnose_disease("patient", ["S1", "S2"])),
    ("Energy", lambda: i.energy.load_forecasting("grid", 24)),
    ("Chemistry", lambda: q.chemistry.simulate_molecule("H2O", 10)),
    # New operations (likely the source of errors)
    ("Agriculture", lambda: i.agriculture.precision_planting({"field_size": 100}, "Wheat")),
    ("Transport", lambda: i.transportation.congestion_prediction("location", "rush_hour")),
    ("Environment", lambda: i.environment.pollution_monitoring("station", ["PM2.5"])),
    ("Education", lambda: i.education.personalized_learning("student", "Science")),
    ("Finance Port Opt", lambda: i.finance.portfolio_optimization(100000, "medium")),
    ("Supply Chain", lambda: q.supply_chain.optimize_inventory([{"id": 1, "name": "P1"}], [100])),
    ("Traffic", lambda: q.traffic.optimize_traffic_light_timing(["I1"], {"rush": True})),
    ("Robotics", lambda: a.robotics.plan_motion([0,0,0], [10,10,10])),
]

print("=" * 80)
print("API DIAGNOSTIC TEST")
print("=" * 80)

errors = []
for name, func in test_cases:
    try:
        result = func()
        status = "✅ OK"
    except Exception as e:
        status = f"❌ ERROR: {type(e).__name__}: {str(e)[:80]}"
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
