import psutil
from mcp.server.fastmcp import FastMCP

# Create the MCP server
# host='0.0.0.0' allows external connections; port=8000 is the default
mcp = FastMCP('server-health', host='0.0.0.0', port=8000)


@mcp.tool()
def get_cpu() -> str:
    """Returns current CPU usage percentage"""
    return f"CPU usage: {psutil.cpu_percent(interval=1)}%"


@mcp.tool()
def get_memory() -> str:
    """Returns RAM usage percentage and GB used"""
    mem = psutil.virtual_memory()
    return (
        f"Memory usage: {mem.percent}%  |  "
        f"Used: {mem.used / (1024**3):.1f} GB  |  "
        f"Total: {mem.total / (1024**3):.1f} GB"
    )


@mcp.tool()
def get_disk() -> str:
    """Returns disk usage percentage for root filesystem"""
    disk = psutil.disk_usage('/')
    return (
        f"Disk usage: {disk.percent}%  |  "
        f"Used: {disk.used / (1024**3):.1f} GB  |  "
        f"Total: {disk.total / (1024**3):.1f} GB"
    )


if __name__ == "__main__":
    # SSE transport is required for Claude.ai remote connector
    mcp.run(transport='sse')
