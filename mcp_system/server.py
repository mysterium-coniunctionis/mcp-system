from mcp.server.fastmcp import FastMCP, Context, Image
import sqlite3
import json
from typing import Any, Dict, List, Optional

# Create our MCP server instance
mcp = FastMCP("System Monitor & Analytics")

# Database helper
def get_db():
    conn = sqlite3.connect("system_data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Resource: System Schema
@mcp.resource("schema://system")
def get_schema() -> str:
    """Get the current system database schema"""
    conn = get_db()
    schema = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(f"Table {table['name']}:\n{table['sql']}" for table in schema)

# Resource: System Metrics
@mcp.resource("metrics://{component}")
def get_metrics(component: str) -> str:
    """Get metrics for a specific system component"""
    conn = get_db()
    metrics = conn.execute(
        "SELECT * FROM metrics WHERE component = ? ORDER BY timestamp DESC LIMIT 10", 
        (component,)
    ).fetchall()
    return json.dumps([dict(m) for m in metrics], indent=2)

# Tool: Query System Data
@mcp.tool()
def query_system(sql: str, ctx: Context) -> str:
    """Execute a SQL query against the system database"""
    conn = get_db()
    try:
        ctx.info(f"Executing query: {sql}")
        result = conn.execute(sql).fetchall()
        return json.dumps([dict(row) for row in result], indent=2)
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Tool: Monitor Component
@mcp.tool()
async def monitor_component(component: str, duration: int, ctx: Context) -> str:
    """Monitor a system component for a specified duration"""
    try:
        for i in range(duration):
            # Simulate monitoring updates
            ctx.info(f"Monitoring {component}: {i+1}/{duration}")
            await ctx.report_progress(i, duration)
        return f"Completed monitoring {component} for {duration} intervals"
    except Exception as e:
        return f"Error monitoring component: {str(e)}"

# Tool: Generate System Report
@mcp.tool()
def generate_report(components: List[str]) -> Dict[str, Any]:
    """Generate a comprehensive system report for specified components"""
    conn = get_db()
    report = {}
    
    for component in components:
        metrics = conn.execute(
            "SELECT * FROM metrics WHERE component = ? ORDER BY timestamp DESC LIMIT 5",
            (component,)
        ).fetchall()
        report[component] = [dict(m) for m in metrics]
    
    return report

if __name__ == "__main__":
    mcp.run()