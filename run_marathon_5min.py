#!/usr/bin/env python3
"""Run 5-minute marathon validation"""

import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marathon_endurance_test import MarathonEnduranceTest

if __name__ == "__main__":
    test = MarathonEnduranceTest(duration_minutes=5)
    test.run(workers=25)
