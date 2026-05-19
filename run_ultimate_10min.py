#!/usr/bin/env python3
"""Run 10-minute ultimate stress test validation"""

import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ultimate_stress_test import UltimateStressTest

if __name__ == "__main__":
    test = UltimateStressTest(duration_minutes=10)
    test.run(workers=45)
