"""
System Quick Test - 系统快速测试
验证系统核心功能是否正常工作
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_perpetual_evolution_system import SystemIntegratorComponent


def test_system_initialization():
    """测试系统初始化"""
    print("\n" + "="*60)
    print("🧪 测试 1: 系统初始化")
    print("="*60)
    
    try:
        system = SystemIntegratorComponent()
        print("✅ 系统初始化成功")
        
        # 获取状态
        status = system.get_system_status()
        print(f"   - 版本: {status['version']}")
        print(f"   - 初始化: {status['initialized']}")
        print(f"   - 存储类型: {status['components']['storage_backend']['storage_type']}")
        
        return True, system
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_task_workflow_creation(system):
    """测试任务工作流创建"""
    print("\n" + "="*60)
    print("🧪 测试 2: 任务工作流创建")
    print("="*60)
    
    try:
        # 创建任务
        result = system.execute_single_task_workflow(
            raw_input="测试任务工作流创建",
            priority=5
        )
        
        print(f"✅ 任务创建成功")
        print(f"   - 任务ID: {result['task_id']}")
        print(f"   - 成功: {result['execution_result']['success']}")
        print(f"   - 执行步骤: {result['execution_result']['total_steps_executed']}")
        print(f"   - 经验数: {len(result['experience'])}")
        
        return True
    except Exception as e:
        print(f"❌ 任务创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_tasks(system):
    """测试多任务处理"""
    print("\n" + "="*60)
    print("🧪 测试 3: 多任务处理")
    print("="*60)
    
    tasks = [
        "代码结构分析",
        "性能优化建议",
        "安全问题扫描"
    ]
    
    results = []
    try:
        for i, task_input in enumerate(tasks, 1):
            result = system.execute_single_task_workflow(
                raw_input=task_input,
                priority=3
            )
            results.append(result)
            print(f"✅ 任务 {i}: {task_input} - {result['task_id'][:8]}...")
        
        successful = sum(1 for r in results if r['execution_result']['success'])
        print(f"\n📊 结果统计:")
        print(f"   - 总任务数: {len(results)}")
        print(f"   - 成功: {successful}")
        print(f"   - 失败: {len(results) - successful}")
        
        return True
    except Exception as e:
        print(f"❌ 多任务处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_components(system):
    """测试系统组件访问"""
    print("\n" + "="*60)
    print("🧪 测试 4: 系统组件访问")
    print("="*60)
    
    try:
        components = [
            ("task_workflow_manager", system.task_workflow_manager),
            ("task_analyzer_planner", system.task_analyzer_planner),
            ("task_step_executor", system.task_step_executor),
            ("priority_queue_manager", system.priority_queue_manager),
            ("workflow_mode_coordinator", system.workflow_mode_coordinator),
            ("experience_learning_manager", system.experience_learning_manager),
            ("feedback_generation_reporter", system.feedback_generation_reporter),
        ]
        
        print("✅ 所有组件成功访问:")
        for name, component in components:
            print(f"   - {name}: {component.__class__.__name__}")
        
        return True
    except Exception as e:
        print(f"❌ 组件访问失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics(system):
    """测试统计功能"""
    print("\n" + "="*60)
    print("🧪 测试 5: 统计功能")
    print("="*60)
    
    try:
        # 任务统计
        task_stats = system.task_workflow_manager.get_task_workflow_statistics()
        print(f"✅ 任务统计:")
        print(f"   - 待处理任务: {task_stats['pending_task_count']}")
        print(f"   - 优先级分布: {task_stats['priority_distribution']}")
        
        # 队列统计
        queue_stats = system.priority_queue_manager.get_queue_statistics()
        print(f"✅ 队列统计:")
        print(f"   - 队列大小: {queue_stats['queue_size']}")
        print(f"   - 总数: {queue_stats['total_queued']}")
        
        # 学习洞察
        insights = system.experience_learning_manager.get_learning_insights()
        print(f"✅ 学习洞察:")
        print(f"   - 总经验: {insights['total_experiences']}")
        print(f"   - 成功率: {insights['success_rate']:.2%}")
        
        return True
    except Exception as e:
        print(f"❌ 统计功能失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_shutdown(system):
    """测试系统关闭"""
    print("\n" + "="*60)
    print("🧪 测试 6: 系统关闭")
    print("="*60)
    
    try:
        system.shutdown_system()
        print("✅ 系统关闭成功")
        return True
    except Exception as e:
        print(f"❌ 系统关闭失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 Agent 永续自进化系统 - 快速测试")
    print("="*60)
    
    tests = []
    system = None
    
    # 运行所有测试
    test1_pass, system = test_system_initialization()
    tests.append(("系统初始化", test1_pass))
    
    if system:
        test2_pass = test_task_workflow_creation(system)
        tests.append(("任务工作流创建", test2_pass))
        
        test3_pass = test_multiple_tasks(system)
        tests.append(("多任务处理", test3_pass))
        
        test4_pass = test_system_components(system)
        tests.append(("系统组件访问", test4_pass))
        
        test5_pass = test_statistics(system)
        tests.append(("统计功能", test5_pass))
        
        test6_pass = test_system_shutdown(system)
        tests.append(("系统关闭", test6_pass))
    
    # 打印测试结果总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查系统")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
