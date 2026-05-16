"""
Agent 永续自进化系统 - 告警通知模块
提供多种告警方式：日志、邮件、HTTP、Webhook等
"""
import os
import sys
import smtplib
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List, Callable, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AlertLevel:
    """告警级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Alert:
    """告警信息"""
    
    def __init__(
        self,
        level: str,
        title: str,
        message: str,
        source: str = None,
        metadata: Dict = None
    ):
        self.level = level
        self.title = title
        self.message = message
        self.source = source or "agent_system"
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "level": self.level,
            "title": self.title,
            "message": self.message,
            "source": self.source,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class AlertChannel:
    """告警通道基类"""
    
    def send(self, alert: Alert) -> bool:
        """
        发送告警
        :param alert: 告警信息
        :return: 是否成功
        """
        raise NotImplementedError


class ConsoleAlertChannel(AlertChannel):
    """控制台告警通道"""
    
    def __init__(self, min_level: str = AlertLevel.INFO):
        self.min_level = min_level
        self.level_orders = {
            AlertLevel.DEBUG: 0,
            AlertLevel.INFO: 1,
            AlertLevel.WARNING: 2,
            AlertLevel.ERROR: 3,
            AlertLevel.CRITICAL: 4
        }
    
    def _should_send(self, level: str) -> bool:
        return self.level_orders[level] >= self.level_orders[self.min_level]
    
    def send(self, alert: Alert) -> bool:
        if not self._should_send(alert.level):
            return True
        
        level_color = {
            AlertLevel.DEBUG: "\033[94m",
            AlertLevel.INFO: "\033[92m",
            AlertLevel.WARNING: "\033[93m",
            AlertLevel.ERROR: "\033[91m",
            AlertLevel.CRITICAL: "\033[95m"
        }
        
        reset = "\033[0m"
        color = level_color.get(alert.level, reset)
        
        print(f"{color}[{alert.level}] {alert.title}: {alert.message}{reset}")
        return True


class FileAlertChannel(AlertChannel):
    """文件告警通道"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    def send(self, alert: Alert) -> bool:
        try:
            with open(self.file_path, "a") as f:
                f.write(json.dumps(alert.to_dict(), ensure_ascii=False) + "\n")
            return True
        except Exception as e:
            print(f"写入告警文件失败: {e}")
            return False


class EmailAlertChannel(AlertChannel):
    """邮件告警通道"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        sender: str,
        recipients: List[str],
        use_tls: bool = True
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender = sender
        self.recipients = recipients
        self.use_tls = use_tls
    
    def send(self, alert: Alert) -> bool:
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = ", ".join(self.recipients)
            msg["Subject"] = f"[{alert.level}] {alert.title}"
            
            body = f"""
时间: {alert.timestamp}
级别: {alert.level}
来源: {alert.source}
标题: {alert.title}
消息: {alert.message}

元数据:
{json.dumps(alert.metadata, indent=2, ensure_ascii=False)}
"""
            
            msg.attach(MIMEText(body, "plain", "utf-8"))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.sender, self.recipients, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"发送邮件告警失败: {e}")
            return False


class WebhookAlertChannel(AlertChannel):
    """Webhook告警通道"""
    
    def __init__(self, url: str, headers: Dict = None):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
    
    def send(self, alert: Alert) -> bool:
        try:
            response = requests.post(
                self.url,
                json=alert.to_dict(),
                headers=self.headers,
                timeout=10
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            print(f"发送Webhook告警失败: {e}")
            return False


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.channels: List[AlertChannel] = []
        self.alert_history: List[Alert] = []
        self.max_history = 1000
    
    def add_channel(self, channel: AlertChannel):
        """
        添加告警通道
        :param channel: 告警通道
        """
        self.channels.append(channel)
    
    def send_alert(
        self,
        level: str,
        title: str,
        message: str,
        source: str = None,
        metadata: Dict = None
    ):
        """
        发送告警
        :param level: 告警级别
        :param title: 标题
        :param message: 消息
        :param source: 来源
        :param metadata: 元数据
        """
        alert = Alert(level, title, message, source, metadata)
        
        # 记录历史
        self.alert_history.append(alert)
        if len(self.alert_history) > self.max_history:
            self.alert_history = self.alert_history[-self.max_history:]
        
        # 发送到所有通道
        for channel in self.channels:
            try:
                channel.send(alert)
            except Exception as e:
                print(f"发送告警到通道失败: {e}")
    
    def debug(self, title: str, message: str, **kwargs):
        """发送DEBUG级别告警"""
        self.send_alert(AlertLevel.DEBUG, title, message, **kwargs)
    
    def info(self, title: str, message: str, **kwargs):
        """发送INFO级别告警"""
        self.send_alert(AlertLevel.INFO, title, message, **kwargs)
    
    def warning(self, title: str, message: str, **kwargs):
        """发送WARNING级别告警"""
        self.send_alert(AlertLevel.WARNING, title, message, **kwargs)
    
    def error(self, title: str, message: str, **kwargs):
        """发送ERROR级别告警"""
        self.send_alert(AlertLevel.ERROR, title, message, **kwargs)
    
    def critical(self, title: str, message: str, **kwargs):
        """发送CRITICAL级别告警"""
        self.send_alert(AlertLevel.CRITICAL, title, message, **kwargs)
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """
        获取告警历史
        :param limit: 限制数量
        :return: 告警历史列表
        """
        return [alert.to_dict() for alert in self.alert_history[-limit:]]


# 创建默认告警管理器
default_alert_manager = AlertManager()
default_alert_manager.add_channel(ConsoleAlertChannel())


if __name__ == "__main__":
    # 演示：使用告警系统
    print("告警通知系统演示")
    
    manager = AlertManager()
    manager.add_channel(ConsoleAlertChannel(min_level=AlertLevel.DEBUG))
    manager.add_channel(FileAlertChannel("/tmp/agent_alerts.log"))
    
    manager.debug("系统启动", "Agent 永续自进化系统已启动")
    manager.info("服务状态", "所有服务正常运行")
    manager.warning("资源警告", "内存使用率超过80%")
    manager.error("API请求失败", "请求超时")
    manager.critical("服务崩溃", "主进程异常退出")
    
    print(f"\n最近5条告警:")
    for alert in manager.get_history(5):
        print(f"  [{alert['level']}] {alert['title']}")
