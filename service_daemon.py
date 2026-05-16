"""
Agent 永续自进化系统 - 进程守护与自动重启模块
确保系统持续运行，在崩溃时自动重启
"""
import os
import sys
import time
import signal
import subprocess
import threading
from datetime import datetime
from typing import Optional, Callable, Dict, List
from collections import defaultdict


class ProcessDaemon:
    """
    进程守护类
    监控和管理目标进程，确保其持续运行
    """
    
    def __init__(
        self,
        command: str,
        work_dir: str = None,
        max_restarts: int = 10,
        restart_delay: float = 5.0,
        health_check_interval: float = 30.0,
        log_file: str = None
    ):
        """
        初始化进程守护
        :param command: 要执行的命令
        :param work_dir: 工作目录
        :param max_restarts: 最大重启次数
        :param restart_delay: 重启延迟(秒)
        :param health_check_interval: 健康检查间隔(秒)
        :param log_file: 日志文件路径
        """
        self.command = command
        self.work_dir = work_dir or os.getcwd()
        self.max_restarts = max_restarts
        self.restart_delay = restart_delay
        self.health_check_interval = health_check_interval
        self.log_file = log_file
        
        self.process: Optional[subprocess.Popen] = None
        self.restart_count = 0
        self.is_running = False
        self.should_stop = False
        self.start_time = None
        self.health_status = {
            "total_restarts": 0,
            "last_restart_time": None,
            "status": "stopped"
        }
        
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """
        设置信号处理器
        处理终止信号，优雅关闭
        """
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        
    def _handle_signal(self, signum, frame):
        """
        信号处理函数
        :param signum: 信号编号
        :param frame: 堆栈帧
        """
        print(f"\n收到信号 {signum}，正在停止服务...")
        self.stop()
    
    def _redirect_output(self):
        """
        重定向输出到日志文件
        """
        if self.log_file:
            try:
                os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
                return open(self.log_file, 'a')
            except Exception as e:
                print(f"无法打开日志文件 {self.log_file}: {e}")
        return sys.stdout
    
    def _start_process(self) -> bool:
        """
        启动目标进程
        :return: 是否成功启动
        """
        try:
            print(f"正在启动进程: {self.command}")
            self.start_time = datetime.now()
            
            # 启动进程
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                cwd=self.work_dir,
                stdout=self._redirect_output(),
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid
            )
            
            self.is_running = True
            self.health_status["status"] = "running"
            print(f"进程已启动 (PID: {self.process.pid})")
            return True
        except Exception as e:
            print(f"启动进程失败: {e}")
            return False
    
    def _check_process(self) -> bool:
        """
        检查进程是否还在运行
        :return: 进程是否存活
        """
        if self.process is None:
            return False
        return self.process.poll() is None
    
    def _restart_process(self):
        """
        重启目标进程
        """
        if self.restart_count >= self.max_restarts:
            print(f"已达到最大重启次数 {self.max_restarts}，停止重启")
            self.stop()
            return
        
        # 先尝试终止旧进程
        self._terminate_process()
        
        # 延迟后重启
        print(f"等待 {self.restart_delay} 秒后重启...")
        time.sleep(self.restart_delay)
        
        # 重启
        if self._start_process():
            self.restart_count += 1
            self.health_status["total_restarts"] = self.restart_count
            self.health_status["last_restart_time"] = datetime.now().isoformat()
            print(f"进程已重启 (第 {self.restart_count} 次)")
    
    def _terminate_process(self):
        """
        终止目标进程
        """
        if self.process is None:
            return
        try:
            # 发送SIGTERM信号
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            # 等待进程结束
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                    # 超时后使用SIGKILL
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    self.process.wait()
            print("进程已终止")
        except Exception as e:
            print(f"终止进程时出错: {e}")
    
    def _health_check(self):
        """
        健康检查线程
        定期检查进程健康状态
        """
        while not self.should_stop:
            if self.is_running:
                if not self._check_process():
                    print("检测到进程异常，准备重启...")
                    self._restart_process()
            
            time.sleep(self.health_check_interval)
    
    def start(self):
        """
        启动守护进程
        """
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S') - 启动进程守护")
        
        self.should_stop = False
        
        # 启动目标进程
        if not self._start_process():
            print("初始启动失败")
            return
        
        # 启动健康检查线程
        self.health_thread = threading.Thread(
            target=self._health_check,
            daemon=True
        )
        self.health_thread.start()
        
        # 主循环
        try:
            while not self.should_stop:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到中断信号")
        finally:
            self.stop()
    
    def stop(self):
        """
        停止守护进程
        """
        print("正在停止进程守护...")
        self.should_stop = True
        self.is_running = False
        self.health_status["status"] = "stopped"
        
        # 终止目标进程
        self._terminate_process()
        print("进程守护已停止")
    
    def get_status(self) -> Dict:
        """
        获取服务状态
        :return: 状态字典
        """
        return {
            "command": self.command,
            "is_running": self.is_running,
            "restart_count": self.restart_count,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "health_status": self.health_status,
            "timestamp": datetime.now().isoformat()
        }


class MultiServiceDaemon:
    """
    多服务守护类
    同时监控和管理多个服务
    """
    
    def __init__(self):
        self.services: Dict[str, ProcessDaemon] = {}
        self.threads: Dict[str, threading.Thread] = {}
    
    def add_service(
        self,
        name: str,
        command: str,
        **kwargs
    ):
        """
        添加服务
        :param name: 服务名称
        :param command: 服务命令
        :param kwargs: 其他参数
        """
        daemon = ProcessDaemon(command, **kwargs)
        self.services[name] = daemon
    
    def start_all(self):
        """
        启动所有服务
        """
        print("正在启动所有服务...")
        for name, daemon in self.services.items():
            thread = threading.Thread(
                target=daemon.start,
                daemon=True
            )
            thread.start()
            self.threads[name] = thread
            time.sleep(1)  # 错开启动时间
    
    def stop_all(self):
        """
        停止所有服务
        """
        print("正在停止所有服务...")
        for name, daemon in self.services.items():
            daemon.stop()
    
    def get_all_status(self) -> Dict[str, Dict]:
        """
        获取所有服务状态
        :return: 状态字典
        """
        return {name: daemon.get_status() for name, daemon in self.services.items()}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent 永续自进化系统 - 进程守护")
    parser.add_argument("--command", required=True, help="要守护的命令")
    parser.add_argument("--work-dir", help="工作目录")
    parser.add_argument("--max-restarts", type=int, default=10, help="最大重启次数")
    parser.add_argument("--restart-delay", type=float, default=5.0, help="重启延迟(秒)")
    parser.add_argument("--health-check-interval", type=float, default=30.0, help="健康检查间隔(秒)")
    parser.add_argument("--log-file", help="日志文件路径")
    
    args = parser.parse_args()
    
    daemon = ProcessDaemon(
        command=args.command,
        work_dir=args.work_dir,
        max_restarts=args.max_restarts,
        restart_delay=args.restart_delay,
        health_check_interval=args.health_check_interval,
        log_file=args.log_file
    )
    
    try:
        daemon.start()
    except KeyboardInterrupt:
        print("\n进程守护已停止")
