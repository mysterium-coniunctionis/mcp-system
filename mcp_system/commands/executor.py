from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
import asyncio
import logging
from ..monitoring.metrics import track_command_execution, track_command_error

logger = logging.getLogger(__name__)

@dataclass
class CommandContext:
    """Context information for command execution"""
    command_id: str
    parameters: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class CommandResult:
    """Represents the result of a command execution"""
    def __init__(self, success: bool, data: Any = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error

class Command(ABC):
    """Base class for all MCP commands"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, context: CommandContext) -> CommandResult:
        """Execute the command with given context"""
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate command parameters"""
        pass

class CommandExecutor:
    """Handles execution of MCP commands"""
    def __init__(self):
        self._commands: Dict[str, Command] = {}
        self._active_executions: Dict[str, asyncio.Task] = {}

    def register_command(self, command: Command) -> None:
        """Register a new command"""
        if command.name in self._commands:
            raise ValueError(f"Command {command.name} already registered")
        self._commands[command.name] = command
        logger.info(f"Registered command: {command.name}")

    async def execute_command(self, context: CommandContext) -> CommandResult:
        """Execute a command with given context"""
        command = self._commands.get(context.command_id)
        if not command:
            error_msg = f"Command {context.command_id} not found"
            track_command_error(context.command_id, "command_not_found")
            return CommandResult(False, error=error_msg)

        try:
            if not command.validate_parameters(context.parameters):
                track_command_error(context.command_id, "invalid_parameters")
                return CommandResult(False, error="Invalid parameters")

            track_command_execution(context.command_id)
            task = asyncio.create_task(command.execute(context))
            self._active_executions[context.command_id] = task
            
            result = await task
            return result

        except Exception as e:
            error_msg = f"Error executing command {context.command_id}: {str(e)}"
            track_command_error(context.command_id, "execution_error")
            logger.exception(error_msg)
            return CommandResult(False, error=error_msg)

        finally:
            self._active_executions.pop(context.command_id, None)

    async def cancel_command(self, command_id: str) -> bool:
        """Cancel an active command execution"""
        task = self._active_executions.get(command_id)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            track_command_error(command_id, "cancelled")
            return True
        return False

    def get_active_executions(self) -> List[str]:
        """Get list of currently executing command IDs"""
        return list(self._active_executions.keys())
