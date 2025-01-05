from typing import Dict, Any
from .executor import Command, CommandContext, CommandResult

class EchoCommand(Command):
    """Simple echo command for testing"""
    def __init__(self):
        super().__init__("echo", "Echo back the input message")

    async def execute(self, context: CommandContext) -> CommandResult:
        message = context.parameters.get("message", "")
        return CommandResult(True, data={"message": message})

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return "message" in parameters

class SystemInfoCommand(Command):
    """Return system information"""
    def __init__(self):
        super().__init__("system_info", "Get system information")

    async def execute(self, context: CommandContext) -> CommandResult:
        import psutil
        info = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory()._asdict(),
            "disk_usage": psutil.disk_usage("/")._asdict()
        }
        return CommandResult(True, data=info)

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return True  # No parameters needed
