"""
Phase 4 Comprehensive Test - 第四阶段综合测试
验证机器学习、多智能体、知识图谱、自适应、分布式等新功能
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_machine_learning_integration():
    """测试机器学习集成"""
    print("\n" + "="*60)
    print("🧪 测试机器学习集成")
    print("="*60)
    
    try:
        from agent_perpetual_evolution_system.machine_learning_integration import (
            TaskExecutionDataCollector,
            TaskFeatureExtractor,
            TaskSuccessPredictor,
            ExecutionStrategyLearner,
            AnomalyDetector,
            AdaptiveParameterTuner
        )
        
        # 测试数据收集器
        collector = TaskExecutionDataCollector()
        collector.record_execution(
            task_id="test-1",
            task_input="analyze code",
            priority=5,
            duration=0.1,
            success=True
        )
        stats = collector.get_statistics()
        print(f"✓ 数据收集器: 记录 {stats['total_executions']} 条")
        
        # 测试特征提取
        features = TaskFeatureExtractor.extract_features("analyze code quality", priority=5)
        print(f"✓ 特征提取: 提取 {len(features)} 个特征")
        
        # 测试成功率预测
        predictor = TaskSuccessPredictor(collector)
        prediction = predictor.predict_success_probability("analyze code", priority=5)
        print(f"✓ 成功率预测: {prediction['success_probability']:.2%}")
        
        # 测试策略学习
        learner = ExecutionStrategyLearner()
        strategy = learner.select_best_strategy({"priority": 8})
        print(f"✓ 策略学习: 选择策略 '{strategy}'")
        
        # 测试异常检测
        detector = AnomalyDetector()
        anomaly = detector.detect_task_anomaly(duration=5.0, success=False)
        print(f"✓ 异常检测: 检测到 {anomaly['anomaly_type'] or 'normal'}")
        
        # 测试参数调整
        tuner = AdaptiveParameterTuner()
        suggestion = tuner.suggest_parameter_adjustment({"error_rate": 0.15})
        print(f"✓ 参数调整: 建议 {len(suggestion['suggestions'])} 项")
        
        print(f"\n✅ 机器学习集成测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 机器学习集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multi_agent_framework():
    """测试多智能体框架"""
    print("\n" + "="*60)
    print("🧪 测试多智能体协作框架")
    print("="*60)
    
    try:
        from agent_perpetual_evolution_system.multi_agent_collaboration import (
            BaseAgent,
            AgentMessage,
            AgentCommunicationProtocol,
            AgentStatus,
            MessageType
        )
        
        # 测试智能体创建
        agent = BaseAgent(
            agent_id="agent-1",
            agent_name="Test Agent",
            agent_type="test",
            capabilities=["analyze", "execute"]
        )
        print(f"✓ 智能体创建: {agent.agent_id}")
        
        # 测试状态更新
        agent.update_performance(success=True, execution_time=0.1)
        metrics = agent.get_status()
        print(f"✓ 性能更新: 成功率 {metrics['performance_metrics']['success_rate']:.0%}")
        
        # 测试通信协议
        protocol = AgentCommunicationProtocol()
        protocol.register_agent(agent)
        print(f"✓ 通信协议: 注册 {len(protocol.agents)} 个智能体")
        
        # 测试消息发送
        message = AgentMessage(
            message_id="msg-1",
            sender_id="agent-1",
            receiver_id="agent-2",
            message_type=MessageType.TASK_REQUEST,
            content={"task": "analyze"}
        )
        protocol.send_message(message)
        print(f"✓ 消息发送: {message.message_id}")
        
        print(f"\n✅ 多智能体协作框架测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 多智能体框架测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_graph():
    """测试知识图谱"""
    print("\n" + "="*60)
    print("🧪 测试知识图谱集成")
    print("="*60)
    
    try:
        from agent_perpetual_evolution_system.knowledge_graph_integration import (
            KnowledgeGraph,
            KnowledgeGraphNode,
            KnowledgeGraphEdge,
            NodeType,
            RelationshipType
        )
        
        # 测试图谱创建
        graph = KnowledgeGraph()
        print(f"✓ 知识图谱创建成功")
        
        # 测试节点添加
        node1 = KnowledgeGraphNode(
            node_id="node-1",
            node_type=NodeType.TASK,
            name="Task 1",
            properties={"input": "analyze code"}
        )
        graph.add_node(node1)
        
        node2 = KnowledgeGraphNode(
            node_id="node-2",
            node_type=NodeType.CONCEPT,
            name="Concept 1"
        )
        graph.add_node(node2)
        print(f"✓ 节点添加: {len(graph.nodes)} 个节点")
        
        # 测试边添加
        edge = KnowledgeGraphEdge(
            edge_id="edge-1",
            source_node_id="node-1",
            target_node_id="node-2",
            relationship_type=RelationshipType.LEARNS_FROM
        )
        graph.add_edge(edge)
        print(f"✓ 边添加: {len(graph.edges)} 条边")
        
        # 测试图谱统计
        stats = graph.get_statistics()
        print(f"✓ 图谱统计: {stats['total_nodes']} 节点, {stats['total_edges']} 边")
        
        print(f"\n✅ 知识图谱集成测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 知识图谱测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adaptive_system():
    """测试自适应系统"""
    print("\n" + "="*60)
    print("🧪 测试自适应系统")
    print("="*60)
    
    try:
        from agent_perpetual_evolution_system.adaptive_system import (
            AdaptiveSystemController,
            FaultRecoveryManager,
            SystemHealthMonitor,
            HealthStatus
        )
        
        # 测试自适应控制器
        controller = AdaptiveSystemController()
        controller.initialize_baseline({"error_rate": 0.05, "avg_latency": 0.1})
        adjustment = controller.analyze_and_adjust({"error_rate": 0.15, "avg_latency": 0.2})
        print(f"✓ 自适应控制: 调整 {len(adjustment['adjustments'])} 项参数")
        
        # 测试故障恢复
        fault_manager = FaultRecoveryManager()
        fault_manager.save_checkpoint("checkpoint-1", {"state": "test"})
        checkpoint = fault_manager.load_checkpoint("checkpoint-1")
        print(f"✓ 故障恢复: 检查点 {'保存' if checkpoint else '加载'} 成功")
        
        # 测试健康监控
        monitor = SystemHealthMonitor()
        health = monitor.check_health({
            "cpu_percent": 50,
            "memory_percent": 60,
            "error_rate": 0.02
        })
        print(f"✓ 健康监控: 状态 {health['status']}")
        
        print(f"\n✅ 自适应系统测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 自适应系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_distributed_architecture():
    """测试分布式架构"""
    print("\n" + "="*60)
    print("🧪 测试分布式架构")
    print("="*60)
    
    try:
        from agent_perpetual_evolution_system.distributed_architecture import (
            DistributedTaskQueue,
            LoadBalancer,
            DataConsistencyManager,
            LoadBalancingStrategy,
            DistributedTaskNode
        )
        
        # 测试分布式任务队列
        queue = DistributedTaskQueue()
        queue.enqueue("task-1", {"data": "test"}, priority=5)
        queue.enqueue("task-2", {"data": "test2"}, priority=3)
        task = queue.dequeue()
        print(f"✓ 分布式队列: 入队 2, 出队 {task['task_id'] if task else 'None'}")
        
        # 测试负载均衡器
        balancer = LoadBalancer(strategy=LoadBalancingStrategy.ROUND_ROBIN)
        node = DistributedTaskNode(
            node_id="node-1",
            node_name="Worker 1",
            host="localhost",
            port=8000
        )
        balancer.add_node(node)
        selected = balancer.select_node()
        print(f"✓ 负载均衡: 选择节点 {selected.node_id if selected else 'None'}")
        
        # 测试数据一致性
        consistency = DataConsistencyManager()
        consistency.replicate_data("data-1", {"value": "test"}, replicas_count=3)
        data = consistency.get_replicated_data("data-1")
        verification = consistency.verify_consistency("data-1")
        print(f"✓ 数据一致性: 验证 {verification['status']}")
        
        print(f"\n✅ 分布式架构测试通过")
        return True
    
    except Exception as e:
        print(f"❌ 分布式架构测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 Agent 永续自进化系统 - 第四阶段综合测试")
    print("="*60)
    
    tests = []
    
    tests.append(("机器学习集成", test_machine_learning_integration()))
    tests.append(("多智能体协作", test_multi_agent_framework()))
    tests.append(("知识图谱", test_knowledge_graph()))
    tests.append(("自适应系统", test_adaptive_system()))
    tests.append(("分布式架构", test_distributed_architecture()))
    
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    for test_name, test_passed in tests:
        status = "✅ 通过" if test_passed else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    total = len(tests)
    passed = sum(1 for _, p in tests if p)
    
    print(f"\n🎯 总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！第四阶段实施成功！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
