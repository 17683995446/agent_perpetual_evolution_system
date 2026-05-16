"""
Agent 永续自进化系统 - 健康检查与看门狗模块
提供服务健康检查、看门狗监控功能
"""
import os
import sys
import time
import threading
import psutil
import requests
from datetime import datetime
from typing import Optional, Dict, List, Callable, Any
from collections import deque


class HealthChecker:
    """
    健康检查器
    提供多种健康检查方法
    """
    
    @staticmethod
    def check_process_alive(pid: int) -> bool:
        """
        检查进程是否存活
        :param pid: 进程ID
        :return: 是否存活
        """
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            return False
    
    @staticmethod
    def check_process_cpu(pid: int, threshold: float = 90.0) -> bool:
        """
        检查进程CPU使用率
        :param pid: 进程ID
        :param threshold: 阈值(百分比)
        :return: 是否超过阈值
        """
        try:
            process = psutil.Process(pid)
            cpu_percent = process.cpu_percent(interval=0.1)
            return cpu_percent <= threshold
        except Exception:
            return False
    
    @staticmethod
    def check_process_memory(pid: int, threshold_mb: float = 1024.0) -> bool:
        """
        检查进程内存使用
        :param pid: 进程ID
        :param threshold_mb: 阈值(MB)
        :return: 是否超过阈值
        """
        try:
            process = psutil.Process(pid)
            mem_mb = process.memory_info().rss / (1024 * 1024)
            return mem_mb <= threshold_mb
        except Exception:
            return False
    
    @staticmethod
    def check_http_endpoint(url: str, timeout: int = 5) -> bool:
        """
        检查HTTP端点健康
        :param url: 端点URL
        :param timeout: 超时时间(秒)
        :return: 是否健康
        """
        try:
            response = requests.get(url, timeout=timeout)
            return 200 <= response.status_code < 300
        except Exception:
            return False
    
    @staticmethod
    def check_disk_usage(path: str, threshold: float = 90.0) -> bool:
        """
        检查磁盘使用率
        :param path: 挂载点路径
        :param threshold: 阈值(百分比)
        :return: 是否健康
        """
        try:
            usage = psutil.disk_usage(path)
            return usage.percent <= threshold
        except Exception:
            return False
    
    @staticmethod
    def check_memory_usage(threshold: float = 90.0) -> bool:
        """
        检查系统内存使用率
        :param threshold: 阈值(百分比)
        :return: 是否健康
        """
        try:
            memory = psutil.virtual_memory()
            return memory.percent <= threshold
        except Exception:
            return False


class Watchdog:
    """
    看门狗类
    监控服务健康状态，异常时触发恢复
    """
    
    def __init__(
        self,
        name: str,
        health_check: Callable[[], bool],
        check_interval: float = 10.0,
        max_failures: int = 3,
        recovery_action: Optional[Callable] = None,
        alert_callback: Optional[Callable[[str], None]] = None
    ):
        """
        初始化看门狗
        :param name: 服务名称
        :param health_check: 健康检查函数
        :param check_interval: 检查间隔(秒)
        :param max_failures: 最大连续失败次数
        :param recovery_action: 恢复动作
        :param alert_callback: 告警回调
        """
        self.name = name
        self.health_check = health_check
        self.check_interval = check_interval
        self.max_failures = max_failures
        self.recovery_action = recovery_action
        self.alert_callback = alert_callback
        
        self.failures = 0
        self.recoveries = 0
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # 健康状态历史
        self.health_history = deque(maxlen=100)
    
    def _alert(self, message: str):
        """
        发送告警
        :param message: 告警消息
        """
        print(f"[{self.name}] {message}")
        if self.alert_callback:
            self.alert_callback(message)
    
    def _check(self):
        """
        执行健康检查
        """
        try:
            is_healthy = self.health_check()
            
            timestamp = datetime.now().isoformat()
            self.health_history.append({
                "timestamp": timestamp,
                "healthy": is_healthy
            })
            
            if is_healthy:
                if self.failures > 0:
                    self._alert(f"服务已恢复 (之前失败次数: {self.failures})")
                    self.failures = 0
            else:
                self.failures += 1
                self._alert(f"健康检查失败 (失败次数: {self.failures}/{self.max_failures})")
                
                if self.failures >= self.max_failures:
                    self._alert("达到最大失败次数，执行恢复动作...")
                    self._recover()
                    
        except Exception as e:
            self._alert(f"健康检查异常: {e}")
    
    def _recover(self):
        """
        执行恢复动作
        """
        if self.recovery_action:
            try:
                self._alert("正在执行恢复动作...")
                self.recovery_action()
                self.recoveries += 1
                self.failures = 0
                self._alert("恢复动作执行完成")
            except Exception as e:
                self._alert(f"恢复动作失败: {e}")
        else:
            self._alert("未配置恢复动作")
    
    def start(self):
        """
        启动看门狗
        """
        if self.is_running:
            return
        
        print(f"[{self.name}] 启动看门狗")
        self.is_running = True
        self.stop_event.clear()
        
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """
        运行看门狗
        """
        while not self.stop_event.is_set():
            self._check()
            self.stop_event.wait(self.check_interval)
    
    def stop(self):
        """
        停止看门狗
        """
        print(f"[{self.name}] 停止看门狗")
        self.is_running = False
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
    
    def get_status(self) -> Dict:
        """
        获取看门狗状态
        :return: 状态字典
        """
        return {
            "name": self.name,
            "is_running": self.is_running,
            "failures": self.failures,
            "recoveries": self.recoveries,
            "health_history": list(self.health_history),
            "timestamp": datetime.now().isoformat()
        }


class HealthCheckManager:
    """
    健康检查管理器
    管理多个健康检查和看门狗
    """
    
    def __init__(self):
        self.watchdogs: Dict[str, Watchdog] = {}
        self.statuses: Dict[str, Dict] = {}
    
    def add_watchdog(
        self,
        name: str,
        health_check: Callable[[], bool],
        **kwargs
    ):
        """
        添加看门狗
        :param name: 名称
        :param health_check: 健康检查函数
        :param kwargs: 其他参数
        """
        watchdog = Watchdog(name, health_check, **kwargs)
        self.watchdogs[name] = watchdog
        return watchdog
    
    def start_all(self):
        """
        启动所有看门狗
        """
        for watchdog in self.watchdogs.values():
            watchdog.start()
    
    def stop_all(self):
        """
        停止所有看门狗
        """
        for watchdog in self.watchdogs.values():
            watchdog.stop()
    
    def get_all_status(self) -> Dict[str, Dict]:
        """
        获取所有看门狗状态
        :return: 状态字典
        """
        return {name: wd.get_status() for name, wd in self.watchdogs.items()}


if __name__ == "__main__":
    # 演示：使用看门狗
    print("健康检查与看门狗演示")
    
    # 创建健康检查管理器
    manager = HealthCheckManager()
    
    # 添加一个简单的看门狗（总是返回True）
    manager.add_watchdog(
        "demo-service",
        lambda: True,
        check_interval=5
    )
    
    # 启动所有看门狗
    manager.start_all()
    
    try:
        print("看门狗已启动，按Ctrl+C停止...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止...")
        manager.stop_all()
