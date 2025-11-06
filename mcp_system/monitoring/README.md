# MCP System Monitoring

This module provides monitoring capabilities for the MCP system using Prometheus metrics.

## Features

- Server metrics (uptime, memory usage, active connections)
- Request tracking (count and latency)
- MCP-specific metrics (command executions and errors)
- Prometheus integration

## Usage

### Basic Metrics Collection

```python
from mcp_system.monitoring.metrics import track_request

# Track request metrics using decorator
@track_request(method='POST', endpoint='/execute')
async def handle_request():
    # Request handling logic
    pass

# Track command execution
from mcp_system.monitoring.metrics import track_command_execution
track_command_execution('analyze_data')
```

### System Metrics

System metrics are automatically updated periodically. You can also manually update them:

```python
from mcp_system.monitoring.metrics import update_system_metrics
update_system_metrics()
```

## Monitoring Dashboard

The monitoring dashboard is available at `/metrics` endpoint in Prometheus format.

## Installation

1. Install required dependencies:
   ```bash
   pip install prometheus_client psutil
   ```

2. Configure Prometheus to scrape the `/metrics` endpoint

3. (Optional) Set up Grafana for visualization

## Metrics Reference

### Server Metrics
- `mcp_server_uptime_seconds`: Server uptime in seconds
- `mcp_active_connections`: Number of active connections
- `mcp_memory_usage_bytes`: Current memory usage in bytes

### Request Metrics
- `mcp_requests_total`: Total request count by method and endpoint
- `mcp_request_latency_seconds`: Request latency histogram

### MCP-specific Metrics
- `mcp_command_executions_total`: Command execution count by type
- `mcp_command_errors_total`: Command errors by type
