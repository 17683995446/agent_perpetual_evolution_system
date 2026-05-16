# Agent 永续自进化系统 - 持续运行完整指南

## 概述

本指南提供了确保 Agent 永续自进化系统持续稳定运行的完整方案，包括：

- **进程守护**：确保服务崩溃时自动重启
- **Systemd 服务**：Linux 标准服务管理，支持开机自启
- **健康检查**：监控服务健康状态
- **看门狗机制**：异常时自动恢复
- **告警通知**：及时通知管理员问题
- **最佳实践**：生产环境部署建议

## 快速开始

### 1. 使用进程守护模块

最简单的方式是使用我们的进程守护模块：

```bash
# 守护一个 Python 脚本
python3 service_daemon.py \
  --command "python3 demo_v9_quantum_agi_application.py" \
  --work-dir /workspace/agent_perpetual_evolution_system \
  --max-restarts 10 \
  --restart-delay 5 \
  --health-check-interval 10
```

### 2. 使用 Systemd 服务（推荐）

```bash
# 1. 复制服务文件
sudo cp agent_perpetual_evolution.service /etc/systemd/system/

# 2. 修改服务配置（根据需要）
sudo vi /etc/systemd/system/agent_perpetual_evolution.service

# 3. 重新加载配置
sudo systemctl daemon-reload

# 4. 启动服务
sudo systemctl start agent_perpetual_evolution

# 5. 查看服务状态
sudo systemctl status agent_perpetual_evolution

# 6. 设置开机自启
sudo systemctl enable agent_perpetual_evolution

# 7. 查看服务日志
sudo journalctl -u agent_perpetual_evolution -f
```

## 模块说明

### 1. service_daemon.py - 进程守护与自动重启

**功能**：
- 监控目标进程运行状态
- 进程异常时自动重启
- 支持日志重定向
- 优雅的信号处理

**用法示例**：

```python
from service_daemon import ProcessDaemon, MultiServiceDaemon

# 守护单个服务
daemon = ProcessDaemon(
    command="python3 demo_v9_quantum_agi_application.py",
    work_dir="/workspace/agent_perpetual_evolution_system",
    max_restarts=10,
    restart_delay=5,
    health_check_interval=10,
    log_file="/var/log/agent_service.log"
)
daemon.start()

# 同时守护多个服务
multi_daemon = MultiServiceDaemon()
multi_daemon.add_service(
    name="api-service",
    command="python3 api_gateway.py"
)
multi_daemon.add_service(
    name="worker-service",
    command="python3 worker.py"
)
multi_daemon.start_all()
```

### 2. agent_perpetual_evolution.service - Systemd 服务配置

**关键配置**：
- `Restart=always`：总是重启
- `RestartSec=5`：重启延迟 5 秒
- `LimitNOFILE=65536`：文件描述符限制
- `StandardOutput=append:`：日志重定向

**常用 Systemd 命令**：

```bash
# 启动服务
sudo systemctl start agent_perpetual_evolution

# 停止服务
sudo systemctl stop agent_perpetual_evolution

# 重启服务
sudo systemctl restart agent_perpetual_evolution

# 查看服务状态
sudo systemctl status agent_perpetual_evolution

# 启用开机自启
sudo systemctl enable agent_perpetual_evolution

# 禁用开机自启
sudo systemctl disable agent_perpetual_evolution

# 查看实时日志
sudo journalctl -u agent_perpetual_evolution -f

# 重新加载服务配置
sudo systemctl daemon-reload
```

### 3. health_check.py - 健康检查与看门狗

**功能**：
- 进程存活检查
- CPU/内存使用监控
- HTTP 端点健康检查
- 磁盘和系统资源检查
- 看门狗自动恢复

**用法示例**：

```python
from health_check import HealthCheckManager, HealthChecker

manager = HealthCheckManager()

# 添加一个看门狗
manager.add_watchdog(
    name="api-service",
    health_check=lambda: HealthChecker.check_http_endpoint("http://localhost:8080/health"),
    check_interval=10,
    max_failures=3,
    recovery_action=lambda: print("执行恢复操作...")
)

manager.start_all()

# 获取所有状态
status = manager.get_all_status()
print(status)
```

### 4. alerts.py - 告警通知系统

**功能**：
- 多级别告警（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 多种告警通道：控制台、文件、邮件、Webhook
- 告警历史记录

**用法示例**：

```python
from alerts import AlertManager, ConsoleAlertChannel, FileAlertChannel, EmailAlertChannel

manager = AlertManager()

# 添加控制台告警
manager.add_channel(ConsoleAlertChannel())

# 添加文件告警
manager.add_channel(FileAlertChannel("/var/log/agent_alerts.log"))

# 添加邮件告警
manager.add_channel(EmailAlertChannel(
    smtp_server="smtp.example.com",
    smtp_port=587,
    username="user@example.com",
    password="password",
    sender="alert@example.com",
    recipients=["admin@example.com"]
))

# 发送告警
manager.info("服务启动", "系统已成功启动")
manager.warning("资源警告", "内存使用率超过80%")
manager.error("API失败", "请求超时")
manager.critical("服务崩溃", "主进程异常退出")
```

## 高可用架构建议

### 单机部署（最小化）

```
[Application]
    ↓
[Process Daemon / Systemd]
    ↓
[Health Check + Watchdog]
    ↓
[Alert Notification]
```

### 生产环境部署（推荐）

```
                    [Load Balancer]
                         ↓
        ┌────────────────┴────────────────┐
        ↓                                 ↓
    [Node 1]                          [Node 2]
        ↓                                 ↓
[Application]                       [Application]
[Systemd Service]                   [Systemd Service]
[Health Check]                      [Health Check]
        ↓                                 ↓
    └────────────────┬────────────────┘
                     ↓
            [Monitoring & Alerting]
```

## 监控建议

### 1. 系统资源监控

监控以下指标：
- CPU 使用率
- 内存使用率
- 磁盘 I/O 和使用率
- 网络流量
- 文件描述符数量

### 2. 应用层监控

- 服务响应时间
- 请求成功率
- 业务错误率
- 系统吞吐量

### 3. 日志收集

建议使用：
- ELK Stack (Elasticsearch + Logstash + Kibana)
- Grafana + Prometheus
- 或者其他商业 APM 工具

## 故障排查

### 服务频繁重启

1. 检查服务日志：`sudo journalctl -u agent_perpetual_evolution`
2. 查看资源限制是否足够
3. 检查依赖服务是否正常
4. 确认代码中是否有未捕获的异常

### 内存泄漏

1. 使用 `psutil` 监控内存使用
2. 启用 gc 调试
3. 考虑使用内存分析工具（如 memory-profiler）

### 高 CPU 使用率

1. 使用 `top`、`htop` 查看进程
2. 使用 `py-spy` 等工具分析性能瓶颈
3. 检查是否有死循环或密集计算

## 最佳实践

1. **使用 Systemd 管理服务**：生产环境推荐使用 Systemd
2. **配置合适的资源限制**：避免服务耗尽系统资源
3. **完善的健康检查**：不仅仅检查进程存活，还要检查业务功能
4. **多级告警**：不同级别问题采用不同通知方式
5. **日志轮转**：避免日志文件无限增长
6. **定期备份**：重要数据定期备份
7. **灰度发布**：更新时先在小范围验证
8. **灾难恢复预案**：提前准备好应对严重问题的方案

## 相关文件

- `service_daemon.py` - 进程守护模块
- `agent_perpetual_evolution.service` - Systemd 服务配置
- `health_check.py` - 健康检查与看门狗
- `alerts.py` - 告警通知系统
- `system_optimization.py` - 系统优化工具
