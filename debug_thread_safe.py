#!/usr/bin/env python3
"""调试线程安全测试的读操作问题"""

import sys
import random
import traceback

sys.path.insert(0, '/workspace/agent_perpetual_evolution_system')

from quantum_applications import QuantumApplicationPlatform
from agi_applications import AGIApplicationFramework
from intelligent_decision import IntelligentDecisionPlatform
from system_optimization import get_global_cache

print("=== 调试线程安全测试的读操作问题 ===\n")

quantum = QuantumApplicationPlatform()
decision = IntelligentDecisionPlatform()
agi_reader = AGIApplicationFramework()
cache = get_global_cache()

cache.clear()

print("--- 测试单个读操作 ---")

try:
    # 先写一个测试 key
    test_key = "writer_0_key_0"
    cache.set(test_key, "test_value")
    print(f"✅ 设置了测试 key: {test_key}")
    
    # 测试缓存读取
    val = cache.get(test_key, "default")
    print(f"✅ 缓存读取成功: {val}")
    
    # 测试 AGI 推理
    result = agi_reader.reasoning.deductive_reasoning("R0", "Q0")
    print(f"✅ AGI 推理成功: {result}")
    
    print("\n🎉 单个读操作完全正常！")
    
    # 现在测试多个连续操作
    print("\n--- 测试多个连续读操作 ---")
    success = 0
    errors = 0
    for i in range(100):
        try:
            key = f"writer_{random.randint(0, 49)}_key_{random.randint(0, 100)}"
            cache.get(key, "default")
            agi_reader.reasoning.deductive_reasoning(f"R{i}", f"Q{i}")
            success += 1
        except Exception as e:
            errors += 1
            print(f"❌ 错误 {i}: {type(e).__name__}: {e}")
            print(traceback.format_exc())
            break
    
    print(f"\n📊 测试结果: {success} 成功, {errors} 错误")
    
    if errors == 0:
        print("🎉 单个线程下的读操作完全正常！")
except Exception as e:
    print(f"\n❌ 整体错误: {type(e).__name__}: {e}")
    print(traceback.format_exc())
