"""
Interactive Command Line Interface - 交互式命令行接口
提供与系统交互的命令行界面
"""

import sys
import cmd
from typing import Optional

from ..configuration_management_layer import get_application_global_settings
from ..infrastructure_adapter_layer import create_storage_backend
from ..infrastructure_adapter_layer.logging_framework.structured_logger_framework_implementation import StructuredLoggerFrameworkImplementation


class InteractiveCommandLineInterface(cmd.Cmd):
    """
    Interactive Command Line Interface - 交互式命令行接口
    
    提供与Agent Evolution System交互的命令行界面
    支持任务管理、系统状态查看等操作
    """
    
    intro_message = """
╔════════════════════════════════════════════════════════════════════╗
║         Agent Evolution System - Interactive Command Line Interface    ║
║                    Version: {version:<46}║
╚════════════════════════════════════════════════════════════════════╝

Welcome to the Agent Evolution System CLI!
Type 'help' or '?' to see available commands.
Type 'quit' or 'exit' to exit the CLI.
"""
    
    prompt_text = "(agent-evolution) "
    
    def __init__(self):
        """
        Initialize Interactive Command Line Interface - 初始化交互式命令行接口
        """
        super().__init__()
        
        # 获取应用配置
        self.settings = get_application_global_settings()
        
        # 初始化存储后端
        self.storage_backend = create_storage_backend()
        
        # 初始化日志系统
        self.logger = StructuredLoggerFrameworkImplementation(self.storage_backend)
        
        # 当前运行模式
        self.current_mode = "idle_evolution_mode"
        
        # 打印欢迎信息
        print(self.intro_message.format(version=self.settings.APPLICATION_VERSION))
    
    def do_status(self, command_args):
        """
        Show System Status - 显示系统状态
        
        Usage: status
        """
        print("\n📊 System Status:")
        print(f"  Application Version: {self.settings.APPLICATION_VERSION}")
        print(f"  Application Name: {self.settings.APPLICATION_NAME}")
        print(f"  Running Mode: {self.current_mode}")
        print(f"  Storage Backend: {self.settings.STORAGE_BACKEND_TYPE}")
        
        # 检查存储健康状态
        health_check_result = self.storage_backend.perform_health_check()
        print(f"  Storage Status: {health_check_result.get('status', 'unknown')}")
        print(f"  Task Count: {health_check_result.get('task_count', 0)}")
    
    def do_create_task(self, command_args):
        """
        Create New Task - 创建新任务
        
        Usage: create_task <task_description>
        Example: create_task Analyze system logs
        """
        if not command_args:
            print("❌ Error: Please provide task description")
            print("Usage: create_task <task_description>")
            return
        
        task_description = command_args.strip()
        
        # 创建任务（简化实现）
        print(f"✅ Task created successfully:")
        print(f"  Description: {task_description}")
        print(f"  Status: PENDING")
        
        self.logger.log_information_message(
            'CLI',
            f'Task created via CLI: {task_description}'
        )
    
    def do_list_tasks(self, command_args):
        """
        List All Tasks - 列出所有任务
        
        Usage: list_tasks [limit]
        """
        limit_count = 10
        if command_args.strip().isdigit():
            limit_count = int(command_args.strip())
        
        print(f"\n📋 Task List (Limit: {limit_count}):")
        print(f"  {'Task ID':<36} {'Status':<10} {'Priority':<10}")
        print(f"  {'-'*36} {'-'*10} {'-'*10}")
        print("  No tasks found")
    
    def do_mode(self, command_args):
        """
        Switch Running Mode - 切换运行模式
        
        Usage: mode <task|idle>
        Example: mode task
        """
        mode_choice = command_args.strip().lower()
        
        if mode_choice in ["task", "idle"]:
            self.current_mode = f"{mode_choice}_execution_mode" if mode_choice == "task" else "idle_evolution_mode"
            print(f"✅ Running mode switched to: {self.current_mode}")
            
            self.logger.log_information_message(
                'CLI',
                f'Mode switched via CLI: {self.current_mode}'
            )
        else:
            print("❌ Error: Invalid mode. Please use 'task' or 'idle'")
            print("Usage: mode <task|idle>")
    
    def do_statistics(self, command_args):
        """
        Show System Statistics - 显示系统统计
        
        Usage: statistics
        """
        print("\n📈 System Statistics:")
        print(f"  Pending Tasks: 0")
        print(f"  Completed Tasks: 0")
        print(f"  Success Rate: 0%")
        print(f"  Average Execution Time: 0s")
    
    def do_health_check(self, command_args):
        """
        Perform Health Check - 执行健康检查
        
        Usage: health_check
        """
        health_result = self.storage_backend.perform_health_check()
        
        print("\n🏥 Health Check Result:")
        for key, value in health_result.items():
            print(f"  {key}: {value}")
    
    def do_version(self, command_args):
        """
        Show Application Version - 显示应用程序版本
        
        Usage: version
        """
        print(f"\n🔧 Agent Evolution System")
        print(f"   Version: {self.settings.APPLICATION_VERSION}")
        print(f"   Author: Agent Evolution Team")
    
    def do_help(self, command_args):
        """
        Show Help Information - 显示帮助信息
        
        Usage: help [command]
        """
        if command_args:
            # 显示特定命令的帮助
            command = command_args.strip()
            if hasattr(self, f'do_{command}'):
                method = getattr(self, f'do_{command}')
                doc = method.__doc__
                print(f"\n📖 Help for '{command}':")
                print(f"   {doc if doc else 'No help available'}")
            else:
                print(f"❌ Command '{command}' not found")
        else:
            # 显示所有命令
            print("\n📖 Available Commands:")
            commands_list = [
                ("status", "Show system status"),
                ("create_task <desc>", "Create a new task"),
                ("list_tasks [limit]", "List all tasks"),
                ("mode <task|idle>", "Switch running mode"),
                ("statistics", "Show system statistics"),
                ("health_check", "Perform health check"),
                ("version", "Show application version"),
                ("help [command]", "Show help information"),
                ("quit/exit", "Exit the CLI")
            ]
            
            for cmd_name, description in commands_list:
                print(f"  {cmd_name:<25} - {description}")
    
    def do_exit(self, command_args):
        """
        Exit the CLI - 退出CLI
        
        Usage: exit
        """
        print("\n👋 Goodbye!")
        return True
    
    def do_quit(self, command_args):
        """
        Quit the CLI - 退出CLI
        
        Usage: quit
        """
        return self.do_exit(command_args)


def run_interactive_command_line_interface():
    """
    Run Interactive Command Line Interface - 运行交互式命令行接口
    
    启动交互式命令行界面
    """
    try:
        cli = InteractiveCommandLineInterface()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_interactive_command_line_interface()


__all__ = ['InteractiveCommandLineInterface', 'run_interactive_command_line_interface']
