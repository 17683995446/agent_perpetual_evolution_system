#!/usr/bin/env python3
"""Run 3 minutes version of ultimate endurance test"""

import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ultimate_endurance_test import UltimateEnduranceTest

if __name__ == "__main__":
    test = UltimateEnduranceTest(duration_minutes=3, log_interval=10)
    test.run(workers=15)
