from prometheus_client import Counter, Gauge, Histogram
from functools import wraps
import time
import psutil

# Server metrics
UPTIME = Gauge('mcp_server_uptime_seconds', 'Server uptime in seconds')
ACTIVE_CONNECTIONS = Gauge('mcp_active_connections', 'Number of active connections')
MEMORY_USAGE = Gauge('mcp_memory_usage_bytes', 'Current memory usage in bytes')

# Request metrics
REQUEST_COUNT = Counter('mcp_requests_total', 'Total request count', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('mcp_request_latency_seconds', 'Request latency in seconds',
                           ['method', 'endpoint'])

# MCP-specific metrics
COMMAND_EXECUTIONS = Counter('mcp_command_executions_total', 'Total command executions',
                            ['command_type'])
COMMAND_ERRORS = Counter('mcp_command_errors_total', 'Total command execution errors',
                         ['command_type', 'error_type'])

def track_request(method, endpoint):
    """Decorator to track request metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint)\
                    .observe(duration)
        return wrapper
    return decorator

def update_system_metrics():
    """Update system-level metrics"""
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
    # Add more system metrics as needed

def track_command_execution(command_type):
    """Track MCP command execution"""
    COMMAND_EXECUTIONS.labels(command_type=command_type).inc()

def track_command_error(command_type, error_type):
    """Track MCP command execution errors"""
    COMMAND_ERRORS.labels(command_type=command_type, error_type=error_type).inc()
