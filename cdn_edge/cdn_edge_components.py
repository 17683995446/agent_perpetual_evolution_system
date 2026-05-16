"""
Agent 永续自进化系统 - CDN与边缘计算核心组件 (v7.0.0)
优化点：8个（CDN与边缘计算）
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
import uuid
import random
from collections import defaultdict, deque


@dataclass
class CDNNode:
    """CDN节点"""
    node_id: str
    region: str
    city: str
    capacity_gbps: float
    current_load: float
    latency_ms: float
    status: str = "healthy"
    last_ping: datetime = field(default_factory=datetime.now)
    cached_items: int = 0


class GlobalCDN:
    """优化点28：全球CDN节点管理（50+节点）"""
    
    CDN_REGIONS = [
        "us-east-1", "us-west-2", "eu-west-1", "eu-central-1",
        "ap-northeast-1", "ap-southeast-1", "sa-east-1", "ap-southeast-2",
        "me-south-1", "af-south-1", "ca-central-1", "us-south-1"
    ]
    
    def __init__(self):
        self.nodes: Dict[str, CDNNode] = {}
        self._initialize_global_nodes()
        self.routing_table: Dict[str, List[str]] = defaultdict(list)
        print(f"🌐 Global CDN initialized with {len(self.nodes)} nodes")
    
    def _initialize_global_nodes(self):
        """初始化50+个全球节点"""
        for i in range(55):
            region = self.CDN_REGIONS[i % len(self.CDN_REGIONS)]
            node_id = f"cdn-{region}-{i}"
            self.nodes[node_id] = CDNNode(
                node_id=node_id,
                region=region,
                city=self._get_city_for_region(region),
                capacity_gbps=random.uniform(10, 100),
                current_load=random.uniform(0.1, 0.6),
                latency_ms=random.uniform(10, 80)
            )
    
    def _get_city_for_region(self, region: str) -> str:
        """获取区域对应城市"""
        cities = {
            "us-east-1": "Virginia",
            "us-west-2": "Oregon",
            "eu-west-1": "Ireland",
            "eu-central-1": "Frankfurt",
            "ap-northeast-1": "Tokyo",
            "ap-southeast-1": "Singapore",
            "sa-east-1": "São Paulo",
            "ap-southeast-2": "Sydney",
            "me-south-1": "Dubai",
            "af-south-1": "Johannesburg",
            "ca-central-1": "Toronto",
            "us-south-1": "Texas"
        }
        return cities.get(region, "Unknown")
    
    def find_optimal_node(self, user_region: str) -> Optional[CDNNode]:
        """优化点22：智能负载均衡节点选择"""
        candidate_nodes = [
            node for node in self.nodes.values()
            if user_region in node.region and node.status == "healthy"
        ]
        
        if not candidate_nodes:
            # 找不到同区域节点，寻找最近的健康节点
            candidate_nodes = [
                node for node in self.nodes.values()
                if node.status == "healthy"
            ]
        
        if not candidate_nodes:
            return None
        
        # 选择延迟最低且负载最轻的节点
        return min(candidate_nodes, key=lambda x: (x.latency_ms, x.current_load))
    
    def get_cdn_status(self) -> Dict:
        """获取CDN状态"""
        healthy = sum(1 for n in self.nodes.values() if n.status == "healthy")
        total = len(self.nodes)
        total_capacity = sum(n.capacity_gbps for n in self.nodes.values())
        avg_load = sum(n.current_load for n in self.nodes.values()) / total if total > 0 else 0
        
        return {
            "total_nodes": total,
            "healthy_nodes": healthy,
            "unhealthy_nodes": total - healthy,
            "total_capacity_gbps": round(total_capacity, 1),
            "avg_load_percent": round(avg_load * 100, 1),
            "node_distribution": self._get_distribution()
        }
    
    def _get_distribution(self) -> Dict[str, int]:
        """获取节点分布"""
        dist = defaultdict(int)
        for node in self.nodes.values():
            dist[node.region] += 1
        return dict(dist)


class EdgeComputePlatform:
    """优化点29：边缘计算平台"""
    
    class EdgeFunction(Enum):
        IMAGE_RESIZING = auto()
        AB_TESTING = auto()
        SECURITY_SCAN = auto()
        PERSONALIZATION = auto()
        GEO_IP_LOOKUP = auto()
        REQUEST_TRANSFORM = auto()
    
    def __init__(self):
        self.active_functions: Dict[str, Dict] = {}
        self.function_metrics: Dict[str, Dict] = defaultdict(lambda: {
            "invocations": 0,
            "avg_execution_ms": 0,
            "errors": 0
        })
        self.deployed_regions: List[str] = []
        self._setup_default_functions()
    
    def _setup_default_functions(self):
        """设置默认边缘函数"""
        for func in self.EdgeFunction:
            self.active_functions[func.name.lower()] = {
                "status": "enabled",
                "version": "v1.0",
                "regions": ["us-east-1", "eu-west-1", "ap-southeast-1"]
            }
    
    def invoke_edge_function(self, func_name: str, data: Any) -> Dict:
        """调用边缘函数"""
        if func_name not in self.active_functions:
            return {"status": "error", "message": "Function not found"}
        
        # 模拟执行
        exec_time = random.uniform(1, 20)
        self.function_metrics[func_name]["invocations"] += 1
        
        if random.random() < 0.01:
            self.function_metrics[func_name]["errors"] += 1
            return {"status": "error", "message": "Function execution failed"}
        
        return {
            "status": "success",
            "execution_ms": round(exec_time, 2),
            "result": self._simulate_function_result(func_name, data)
        }
    
    def _simulate_function_result(self, func_name: str, data: Any) -> Any:
        """模拟函数结果"""
        if func_name == "image_resizing":
            return {"resized": True, "new_size": "512x512"}
        elif func_name == "a/b_testing":
            return {"variant": random.choice(["A", "B"])}
        elif func_name == "geo_ip_lookup":
            return {"country": "US", "city": "New York", "lat": 40.7, "long": -74.0}
        return {"processed": True}


class IntelligentCache:
    """优化点30：智能缓存策略"""
    
    class CacheStrategy(Enum):
        LRU = "LRU"
        LFU = "LFU"
        ARC = "ARC"
        ADAPTIVE = "ADAPTIVE"
    
    def __init__(self, max_size_mb: int = 10000):
        self.max_size_mb = max_size_mb
        self.current_size_mb: float = 0
        self.cache: Dict[str, Any] = {}
        self.access_log: deque = deque(maxlen=1000)
        self.cache_metrics: Dict[str, int] = defaultdict(int)
        self.strategy = IntelligentCache.CacheStrategy.ADAPTIVE
        self.hit_rate_history: List[float] = []
        print(f"🧠 Intelligent Cache initialized with {max_size_mb}MB, strategy: {self.strategy.value}")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存内容"""
        if key in self.cache:
            self.cache_metrics["hits"] += 1
            self.access_log.append((key, datetime.now()))
            return self.cache[key]
        
        self.cache_metrics["misses"] += 1
        return None
    
    def set(self, key: str, value: Any, size_kb: float = 100) -> bool:
        """设置缓存"""
        required_mb = size_kb / 1024
        
        # 智能驱逐策略
        while self.current_size_mb + required_mb > self.max_size_mb:
            self._evict_one()
        
        self.cache[key] = value
        self.current_size_mb += required_mb
        self.cache_metrics["sets"] += 1
        
        self._update_hit_rate()
        return True
    
    def _evict_one(self):
        """智能驱逐一个缓存项"""
        if not self.cache:
            return
        
        if self.strategy == IntelligentCache.CacheStrategy.LRU:
            # 最简单的LRU实现
            self.cache.pop(next(iter(self.cache.keys())))
        else:
            # 其他策略类似
            self.cache.pop(next(iter(self.cache.keys())))
    
    def _update_hit_rate(self):
        """更新命中率"""
        total = self.cache_metrics["hits"] + self.cache_metrics["misses"]
        if total > 0:
            hit_rate = self.cache_metrics["hits"] / total
            self.hit_rate_history.append(hit_rate)
            if len(self.hit_rate_history) > 100:
                self.hit_rate_history.pop(0)
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        total = self.cache_metrics["hits"] + self.cache_metrics["misses"]
        hit_rate = (self.cache_metrics["hits"] / total) * 100 if total > 0 else 0
        
        return {
            "total_items": len(self.cache),
            "size_mb": round(self.current_size_mb, 1),
            "max_size_mb": self.max_size_mb,
            "hits": self.cache_metrics["hits"],
            "misses": self.cache_metrics["misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "strategy": self.strategy.value,
            "avg_recent_hit_rate": round(sum(self.hit_rate_history[-20:]) * 100, 2) if self.hit_rate_history else 0
        }


class EdgeSecurity:
    """优化点33：边缘安全防护"""
    
    class ThreatType(Enum):
        SQL_INJECTION = "sql_injection"
        XSS_ATTACK = "xss"
        DDOS = "ddos"
        MALICIOUS_PAYLOAD = "malicious_payload"
        BOT_ATTACK = "bot_attack"
    
    def __init__(self):
        self.threat_history: List[Dict] = []
        self.waf_rules: List[Dict] = []
        self.ip_blacklist: Set[str] = set()
        self._setup_default_waf()
        print("🔒 Edge Security initialized")
    
    def _setup_default_waf(self):
        """设置默认WAF规则"""
        self.waf_rules = [
            {"rule": "sqli", "enabled": True, "description": "SQL injection protection"},
            {"rule": "xss", "enabled": True, "description": "XSS protection"},
            {"rule": "rate_limit", "enabled": True, "description": "Rate limiting"}
        ]
    
    def scan_request(self, request_data: Dict, client_ip: str) -> Dict:
        """扫描请求是否有威胁"""
        threats = []
        
        if client_ip in self.ip_blacklist:
            threats.append({"type": "blocked_ip", "severity": "high"})
        
        # 模拟威胁检测
        if random.random() < 0.02:  # 2%的模拟威胁概率
            threat_type = random.choice(list(self.ThreatType))
            threat = {
                "type": threat_type.value,
                "severity": "high" if threat_type == self.ThreatType.DDOS else "medium",
                "action_taken": "blocked"
            }
            threats.append(threat)
            self.threat_history.append(threat)
        
        return {
            "safe": len(threats) == 0,
            "threats_detected": threats,
            "scan_time_ms": round(random.uniform(0.1, 2), 3)
        }


class CDNEdgePlatform:
    """CDN边缘平台 - 整合所有功能"""
    
    def __init__(self):
        self.cdn = GlobalCDN()
        self.edge_compute = EdgeComputePlatform()
        self.cache = IntelligentCache()
        self.security = EdgeSecurity()
        
        print("🚀 CDN & Edge Platform initialized (v7.0.0)")
    
    def process_request(self, path: str, client_ip: str, region: str = "us-east-1") -> Dict:
        """完整的边缘处理流程"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "client_ip": client_ip
        }
        
        # 1. 安全扫描
        security_result = self.security.scan_request({"path": path}, client_ip)
        result["security"] = security_result
        
        if not security_result["safe"]:
            result["status"] = "blocked"
            return result
        
        # 2. CDN缓存查找
        cache_key = path
        cached_content = self.cache.get(cache_key)
        if cached_content:
            result["cache_status"] = "hit"
            result["content"] = cached_content
        else:
            result["cache_status"] = "miss"
            cached_content = f"Generated content for {path}"
            self.cache.set(cache_key, cached_content)
            result["content"] = cached_content
        
        # 3. 最优节点路由
        optimal_node = self.cdn.find_optimal_node(region)
        if optimal_node:
            result["cdn_node"] = {
                "id": optimal_node.node_id,
                "region": optimal_node.region,
                "latency_ms": round(optimal_node.latency_ms, 1)
            }
        
        # 4. 边缘函数处理
        edge_result = self.edge_compute.invoke_edge_function("geo_ip_lookup", {})
        result["edge_function"] = edge_result
        
        return result
    
    def get_platform_dashboard(self) -> Dict:
        """获取平台仪表盘"""
        return {
            "cdn": self.cdn.get_cdn_status(),
            "cache": self.cache.get_cache_stats(),
            "edge_functions": {
                "active": len(self.edge_compute.active_functions),
                "metrics": dict(self.edge_compute.function_metrics)
            },
            "security": {
                "threats_blocked": len(self.security.threat_history),
                "blacklist_size": len(self.security.ip_blacklist)
            }
        }


print("✅ CDN & Edge module loaded (v7.0.0 - Phase 7)")
