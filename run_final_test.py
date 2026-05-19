#!/usr/bin/env python3
"""Run the final endurance test"""

import sys
import os

# Disable output buffering
sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from long_term_endurance_test import LongTermEnduranceTest

if __name__ == "__main__":
    print("🚀=" * 30)
    print("🚀 AGENT PERPETUAL EVOLUTION - LONG TERM ENDURANCE TEST")
    print("🚀=" * 30)
    
    tester = LongTermEnduranceTest(test_duration_minutes=1.5, log_interval_seconds=10)
    metrics = tester.run_test(num_workers=10)
    
    print("\n" + "="*60)
    if len(metrics.error_log) == 0:
        print("🎉 PERFECT TEST!")
    else:
        print(f"⚠️ Test completed with {len(metrics.error_log)} errors")
