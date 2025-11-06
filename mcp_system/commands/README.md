# MCP Command Execution Framework

This module provides the core command execution capabilities for the MCP system.

## Overview

The command execution framework consists of:

1. **Command Interface**: Base class for implementing MCP commands
2. **Command Executor**: Manages command registration and execution
3. **Built-in Commands**: Basic commands included with the system

## Usage

### Creating a Custom Command

```python
from mcp_system.commands.executor import Command, CommandContext, CommandResult

class MyCustomCommand(Command):
    def __init__(self):
        super().__init__("my_command", "Description of my command")

    async def execute(self, context: CommandContext) -> CommandResult:
        # Command implementation
        return CommandResult(True, data={"result": "success"})

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        # Parameter validation
        return True
```

### Using the Command Executor

```python
from mcp_system.commands.executor import CommandExecutor

# Create executor
executor = CommandExecutor()

# Register commands
executor.register_command(MyCustomCommand())

# Execute command
result = await executor.execute_command(CommandContext(
    command_id="my_command",
    parameters={"param": "value"}
))
```

## Monitoring Integration

The command execution framework automatically integrates with the monitoring system:

- Command execution counts
- Error tracking
- Execution duration metrics

## Built-in Commands

1. `EchoCommand`: Simple echo functionality for testing
2. `SystemInfoCommand`: Returns system resource information

## Error Handling

The framework provides comprehensive error handling:

- Parameter validation
- Execution error tracking
- Command cancellation
- Resource cleanup

## Best Practices

1. Always implement parameter validation
2. Use async/await properly
3. Clean up resources in finally blocks
4. Include proper error messages
5. Add monitoring instrumentation
