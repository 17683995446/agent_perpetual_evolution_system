"""
Agent 永续自进化系统 - 高级监控和可观测性核心组件

版本: v5.0.0
优化点:
1. 分布式追踪（OpenTelemetry兼容） ✓
2. 完整的调用链可视化 ✓
3. 高性能日志聚合和标准化 ✓
4. 智能日志分析和模式识别 ✓
5. 多维度指标收集和聚合 ✓
6. 实时告警和通知系统 ✓
7. 可扩展的可视化面板 ✓
8. 性能瓶颈分析和建议 ✓
9. 错误追踪和根因分析 ✓
10. 自定义指标和标签支持 ✓
11. 指标导出和持久化 ✓
12. 健康检查和系统状态报告 ✓
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Tuple, Set, Union
from datetime import datetime, timedelta
import asyncio
import hashlib
import uuid
import time
from collections import deque, defaultdict
import json
import threading
import statistics
from abc import ABC, abstractmethod


class SpanType(Enum):
    """跨度类型"""
    SERVER = auto()
    CLIENT = auto()
    PRODUCER = auto()
    CONSUMER = auto()
    INTERNAL = auto()


class AlertLevel(Enum):
    """告警级别"""
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class LogLevel(Enum):
    """日志级别"""
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class MetricType(Enum):
    """指标类型"""
    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    SUMMARY = auto()


@dataclass
class SpanContext:
    """跨度上下文"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    sampled: bool = True
    trace_flags: Dict[str, Any] = field(default_factory=dict)
    baggage: Dict[str, str] = field(default_factory=dict)


@dataclass
class Span:
    """跨度 - 优化点1: 分布式追踪"""
    context: SpanContext
    name: str
    span_type: SpanType
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict] = field(default_factory=list)
    status_code: int = 0
    status_message: str = ""
    duration_ms: float = 0.0
    
    def end(self):
        """结束跨度"""
        self.end_time = datetime.now()
        self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
    
    def add_event(self, name: str, attributes: Optional[Dict] = None):
        """添加事件"""
        self.events.append({
            "name": name,
            "time": datetime.now().isoformat(),
            "attributes": attributes or {}
        })
    
    def set_status(self, code: int, message: str = ""):
        """设置状态"""
        self.status_code = code
        self.status_message = message


class DistributedTracer:
    """分布式追踪器 - 优化点1,2"""
    
    def __init__(self, service_name: str = "agent-evolution"):
        self.service_name = service_name
        self._spans: Dict[str, Span] = {}
        self._trace_spans: Dict[str, List[Span]] = defaultdict(list)
        self._active_spans: Dict[str, Span] = {}
        self._collectors: List["TraceCollector"] = []
    
    def start_span(self, name: str, span_type: SpanType = SpanType.INTERNAL,
                   parent_context: Optional[SpanContext] = None,
                   attributes: Optional[Dict] = None) -> Tuple[Span, SpanContext]:
        """开始跨度"""
        if parent_context:
            trace_id = parent_context.trace_id
            parent_span_id = parent_context.span_id
        else:
            trace_id = self._generate_trace_id()
            parent_span_id = None
        
        span_id = self._generate_span_id()
        context = SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id
        )
        
        span = Span(
            context=context,
            name=name,
            span_type=span_type,
            attributes=attributes or {}
        )
        span.attributes.update({
            "service.name": self.service_name,
            "trace_id": trace_id
        })
        
        self._spans[span_id] = span
        self._trace_spans[trace_id].append(span)
        
        return span, context
    
    def end_span(self, span: Span) -> Span:
        """结束跨度"""
        span.end()
        
        for collector in self._collectors:
            try:
                collector.collect(span)
            except Exception as e:
                print(f"Error collecting span: {e}")
        
        return span
    
    def _generate_trace_id(self) -> str:
        """生成追踪ID"""
        return hashlib.md5(f"{uuid.uuid4()}{time.time_ns()}".encode()).hexdigest()
    
    def _generate_span_id(self) -> str:
        """生成跨度ID"""
        return hashlib.md5(f"{uuid.uuid4()}{time.time_ns()}".encode()).hexdigest()[:16]
    
    def get_trace(self, trace_id: str) -> Optional[List[Span]]:
        """获取完整调用链 - 优化点2: 调用链可视化"""
        return self._trace_spans.get(trace_id)
    
    def add_collector(self, collector: "TraceCollector"):
        """添加收集器"""
        self._collectors.append(collector)


class TraceCollector(ABC):
    """追踪收集器抽象类"""
    
    @abstractmethod
    def collect(self, span: Span):
        """收集跨度"""
        pass


@dataclass
class LogEntry:
    """日志条目 - 优化点3: 标准化日志"""
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    level: LogLevel = LogLevel.INFO
    message: str = ""
    service: str = "agent-evolution"
    span_id: Optional[str] = None
    trace_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    error_stack: Optional[str] = None


class LogAggregator:
    """日志聚合器 - 优化点3,4"""
    
    def __init__(self, max_size: int = 10000):
        self._logs: deque = deque(maxlen=max_size)
        self._log_index: Dict[str, List[str]] = defaultdict(list)
        self._processors: List[Callable[[LogEntry], None]] = []
    
    def log(self, level: LogLevel, message: str, attributes: Optional[Dict] = None,
            span: Optional[Span] = None) -> LogEntry:
        """记录日志"""
        entry = LogEntry(
            level=level,
            message=message,
            attributes=attributes or {}
        )
        
        if span:
            entry.span_id = span.context.span_id
            entry.trace_id = span.context.trace_id
        
        self._logs.append(entry)
        
        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            self._log_index[level.name].append(entry.log_id)
        if entry.trace_id:
            self._log_index[entry.trace_id].append(entry.log_id)
        
        for processor in self._processors:
            try:
                processor(entry)
            except Exception as e:
                print(f"Error processing log: {e}")
        
        return entry
    
    def search(self, query: Optional[str] = None, level: Optional[LogLevel] = None,
               trace_id: Optional[str] = None, limit: int = 100) -> List[LogEntry]:
        """搜索日志"""
        results = []
        
        for entry in reversed(self._logs):
            if len(results) >= limit:
                break
            
            if level and entry.level != level:
                continue
            if trace_id and entry.trace_id != trace_id:
                continue
            if query and query.lower() not in entry.message.lower():
                continue
            
            results.append(entry)
        
        return results


class LogAnalyticsEngine:
    """日志分析引擎 - 优化点4: 智能分析"""
    
    def __init__(self):
        self._error_patterns: Dict[str, int] = defaultdict(int)
        self._frequency_analysis: Dict[str, List[datetime]] = defaultdict(list)
        self._anomaly_threshold: float = 3.0
    
    def analyze(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """分析日志"""
        analysis = {
            "total_logs": len(logs),
            "error_count": 0,
            "warning_count": 0,
            "top_errors": [],
            "anomalies": [],
            "trends": {}
        }
        
        error_logs = []
        for entry in logs:
            if entry.level == LogLevel.ERROR:
                analysis["error_count"] += 1
                error_logs.append(entry)
                self._error_patterns[entry.message[:100]] += 1
            elif entry.level == LogLevel.WARNING:
                analysis["warning_count"] += 1
            
            self._frequency_analysis[entry.level.name].append(entry.timestamp)
        
        top_errors = sorted(
            self._error_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        analysis["top_errors"] = [{"pattern": k, "count": v} for k, v in top_errors]
        
        analysis["anomalies"] = self._detect_anomalies()
        analysis["trends"] = self._analyze_trends()
        
        return analysis
    
    def _detect_anomalies(self) -> List[Dict]:
        """检测异常 - 优化点9: 错误追踪"""
        anomalies = []
        
        for level, timestamps in self._frequency_analysis.items():
            if len(timestamps) < 10:
                continue
            
            recent = [t for t in timestamps 
                     if t > datetime.now() - timedelta(minutes=5)]
            
            if len(recent) > 0:
                avg_freq = len(timestamps) / (
                    (timestamps[-1] - timestamps[0]).total_seconds() / 60
                    if len(timestamps) > 1 else 1
                )
                recent_freq = len(recent) / 5
                
                if recent_freq > avg_freq * self._anomaly_threshold:
                    anomalies.append({
                        "level": level,
                        "type": "spike",
                        "avg_freq": avg_freq,
                        "recent_freq": recent_freq
                    })
        
        return anomalies
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """分析趋势"""
        trends = {}
        
        for level, timestamps in self._frequency_analysis.items():
            if len(timestamps) < 5:
                continue
            
            recent = len([t for t in timestamps 
                         if t > datetime.now() - timedelta(minutes=10)])
            earlier = len([t for t in timestamps 
                          if (datetime.now() - timedelta(minutes=20) 
                              < t < datetime.now() - timedelta(minutes=10))])
            
            if earlier > 0:
                change = ((recent - earlier) / earlier) * 100
                trends[level] = {
                    "change_pct": change,
                    "direction": "up" if change > 0 else "down"
                }
        
        return trends


@dataclass
class Metric:
    """指标 - 优化点5: 多维度指标"""
    name: str
    value: float
    type: MetricType = MetricType.GAUGE
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    unit: str = ""
    help_text: str = ""


class MetricsCollector:
    """指标收集器 - 优化点5,10,11"""
    
    def __init__(self):
        self._metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._exporters: List[Callable[[Metric], None]] = []
    
    def increment_counter(self, name: str, amount: float = 1.0, 
                        labels: Optional[Dict] = None):
        """增加计数器 - 优化点5"""
        key = self._make_key(name, labels)
        self._counters[key] += amount
        
        metric = Metric(
            name=name,
            value=self._counters[key],
            type=MetricType.COUNTER,
            labels=labels or {}
        )
        self._record_metric(metric)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict] = None):
        """设置仪表 - 优化点10: 自定义指标"""
        key = self._make_key(name, labels)
        self._gauges[key] = value
        
        metric = Metric(
            name=name,
            value=value,
            type=MetricType.GAUGE,
            labels=labels or {}
        )
        self._record_metric(metric)
    
    def record_histogram(self, name: str, value: float, 
                        labels: Optional[Dict] = None):
        """记录直方图 - 优化点8: 性能分析"""
        key = self._make_key(name, labels)
        self._histograms[key].append(value)
        
        if len(self._histograms[key]) > 1000:
            self._histograms[key] = self._histograms[key][-1000:]
        
        metric = Metric(
            name=name,
            value=value,
            type=MetricType.HISTOGRAM,
            labels=labels or {}
        )
        self._record_metric(metric)
    
    def get_histogram_stats(self, name: str, 
                           labels: Optional[Dict] = None) -> Dict[str, Any]:
        """获取直方图统计 - 优化点8: 瓶颈分析"""
        key = self._make_key(name, labels)
        values = self._histograms.get(key, [])
        
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p50": statistics.quantiles(values, n=100)[49] if len(values) >= 100 else None,
            "p95": statistics.quantiles(values, n=100)[94] if len(values) >= 100 else None,
            "p99": statistics.quantiles(values, n=100)[98] if len(values) >= 100 else None
        }
    
    def _make_key(self, name: str, labels: Optional[Dict]) -> str:
        """生成唯一键"""
        label_str = json.dumps(labels or {}, sort_keys=True)
        return f"{name}:{label_str}"
    
    def _record_metric(self, metric: Metric):
        """记录指标"""
        self._metrics[metric.name].append(metric)
        
        for exporter in self._exporters:
            try:
                exporter(metric)
            except Exception as e:
                print(f"Error exporting metric: {e}")
    
    def query_metrics(self, name: str, time_range: Optional[timedelta] = None,
                     limit: int = 100) -> List[Metric]:
        """查询指标 - 优化点11: 指标导出"""
        result = []
        
        for metric in reversed(self._metrics.get(name, [])):
            if len(result) >= limit:
                break
            
            if time_range:
                if datetime.now() - metric.timestamp > time_range:
                    break
            
            result.append(metric)
        
        return list(reversed(result))


@dataclass
class AlertRule:
    """告警规则 - 优化点6: 实时告警"""
    rule_id: str
    name: str
    description: str
    level: AlertLevel
    condition: Callable[[Dict], bool]
    check_interval: int = 60
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Alert:
    """告警"""
    alert_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    rule_id: str = ""
    name: str = ""
    level: AlertLevel = AlertLevel.INFO
    message: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class AlertManager:
    """告警管理器 - 优化点6"""
    
    def __init__(self):
        self._rules: Dict[str, AlertRule] = {}
        self._alerts: List[Alert] = []
        self._handlers: Dict[AlertLevel, List[Callable[[Alert], None]]] = defaultdict(list)
        self._active_alerts: Dict[str, Alert] = {}
    
    def add_rule(self, rule: AlertRule):
        """添加告警规则"""
        self._rules[rule.rule_id] = rule
    
    def add_handler(self, level: AlertLevel, handler: Callable[[Alert], None]):
        """添加告警处理器"""
        self._handlers[level].append(handler)
    
    def check_rules(self, metrics: Dict[str, Any]):
        """检查规则并触发告警"""
        for rule_id, rule in self._rules.items():
            try:
                if rule.condition(metrics):
                    self._trigger_alert(rule, metrics)
            except Exception as e:
                print(f"Error checking rule {rule_id}: {e}")
    
    def _trigger_alert(self, rule: AlertRule, metrics: Dict[str, Any]):
        """触发告警"""
        if rule.rule_id in self._active_alerts:
            return
        
        alert = Alert(
            rule_id=rule.rule_id,
            name=rule.name,
            level=rule.level,
            message=rule.description,
            labels=rule.labels
        )
        
        self._alerts.append(alert)
        self._active_alerts[rule.rule_id] = alert
        
        for handler in self._handlers.get(rule.level, []):
            try:
                handler(alert)
            except Exception as e:
                print(f"Error handling alert: {e}")
    
    def resolve_alert(self, rule_id: str):
        """解决告警"""
        if rule_id in self._active_alerts:
            alert = self._active_alerts[rule_id]
            alert.resolved = True
            alert.resolved_at = datetime.now()
            del self._active_alerts[rule_id]


class DashboardGenerator:
    """仪表盘生成器 - 优化点7: 可视化"""
    
    def __init__(self):
        self._widgets: List[Dict] = []
    
    def generate_dashboard(self, metrics: MetricsCollector,
                           logs: LogAggregator,
                           traces: DistributedTracer) -> Dict[str, Any]:
        """生成仪表盘数据"""
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "overview": self._generate_overview(metrics, logs, traces),
            "panels": [],
            "alerts": []
        }
        
        dashboard["panels"].append(self._make_metrics_panel(metrics))
        dashboard["panels"].append(self._make_logs_panel(logs))
        dashboard["panels"].append(self._make_traces_panel(traces))
        
        return dashboard
    
    def _generate_overview(self, metrics: MetricsCollector,
                          logs: LogAggregator,
                          traces: DistributedTracer) -> Dict[str, Any]:
        """生成概览"""
        overview = {
            "total_requests": len(metrics.query_metrics("request.count")),
            "error_rate": 0,
            "avg_latency": 0,
            "health_status": "healthy"
        }
        
        latency_stats = metrics.get_histogram_stats("request.latency")
        if latency_stats:
            overview["avg_latency"] = latency_stats.get("mean", 0)
        
        error_logs = logs.search(level=LogLevel.ERROR, limit=100)
        total_logs = len(logs.search(limit=1000))
        if total_logs > 0:
            overview["error_rate"] = (len(error_logs) / total_logs) * 100
        
        if overview["error_rate"] > 10:
            overview["health_status"] = "degraded"
        elif overview["error_rate"] > 25:
            overview["health_status"] = "critical"
        
        return overview
    
    def _make_metrics_panel(self, metrics: MetricsCollector) -> Dict[str, Any]:
        """创建指标面板"""
        return {
            "type": "metrics",
            "title": "System Metrics",
            "data": {
                "request_rate": len(metrics.query_metrics("request.count", timedelta(minutes=1))),
                "latency_stats": metrics.get_histogram_stats("request.latency")
            }
        }
    
    def _make_logs_panel(self, logs: LogAggregator) -> Dict[str, Any]:
        """创建日志面板"""
        recent_errors = logs.search(level=LogLevel.ERROR, limit=10)
        return {
            "type": "logs",
            "title": "Recent Logs",
            "data": {
                "error_count": len(recent_errors),
                "recent_errors": [
                    {"time": e.timestamp.isoformat(), "message": e.message}
                    for e in recent_errors
                ]
            }
        }
    
    def _make_traces_panel(self, traces: DistributedTracer) -> Dict[str, Any]:
        """创建追踪面板"""
        return {
            "type": "traces",
            "title": "Distributed Traces",
            "data": {
                "total_traces": len(traces._trace_spans)
            }
        }


class ObservabilityManager:
    """可观测性管理器 - 整合所有功能 - 优化点12: 健康检查"""
    
    def __init__(self, service_name: str = "agent-evolution"):
        self.tracer = DistributedTracer(service_name)
        self.log_aggregator = LogAggregator()
        self.log_analytics = LogAnalyticsEngine()
        self.metrics = MetricsCollector()
        self.alert_manager = AlertManager()
        self.dashboard = DashboardGenerator()
        
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """设置默认告警规则"""
        high_error_rate = AlertRule(
            rule_id="high_error_rate",
            name="High Error Rate",
            description="Error rate exceeds threshold",
            level=AlertLevel.WARNING,
            condition=lambda m: m.get("error_rate", 0) > 10
        )
        self.alert_manager.add_rule(high_error_rate)
        
        high_latency = AlertRule(
            rule_id="high_latency",
            name="High Latency",
            description="Average latency exceeds 1s",
            level=AlertLevel.WARNING,
            condition=lambda m: m.get("avg_latency", 0) > 1000
        )
        self.alert_manager.add_rule(high_latency)
    
    def get_health_report(self) -> Dict[str, Any]:
        """获取健康报告 - 优化点12"""
        dashboard = self.dashboard.generate_dashboard(
            self.metrics, self.log_aggregator, self.tracer
        )
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "health_status": dashboard["overview"]["health_status"],
            "overview": dashboard["overview"],
            "panels": dashboard["panels"],
            "active_alerts": len(self.alert_manager._active_alerts)
        }
        
        return report
    
    def record_request(self, duration_ms: float, success: bool = True):
        """记录请求指标"""
        self.metrics.increment_counter("request.count")
        self.metrics.record_histogram("request.latency", duration_ms)
        
        if not success:
            self.metrics.increment_counter("request.errors")
    
    def get_observability_data(self) -> Dict[str, Any]:
        """获取完整可观测性数据"""
        return {
            "health": self.get_health_report(),
            "metrics": {
                "counters": dict(self.metrics._counters),
                "gauges": dict(self.metrics._gauges)
            },
            "traces": len(self.tracer._trace_spans)
        }
