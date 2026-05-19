#!/usr/bin/env python3
"""Run custom endurance test"""

from long_term_endurance_test import LongTermEnduranceTest

if __name__ == "__main__":
    tester = LongTermEnduranceTest(test_duration_minutes=2, log_interval_seconds=15)
    tester.run_test(num_workers=15)
