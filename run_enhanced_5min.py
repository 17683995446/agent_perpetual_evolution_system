#!/usr/bin/env python3
"""Run 5-minute enhanced marathon validation"""

import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_marathon_test import EnhancedMarathonTest

if __name__ == "__main__":
    test = EnhancedMarathonTest(duration_minutes=5)
    test.run(workers=35)
