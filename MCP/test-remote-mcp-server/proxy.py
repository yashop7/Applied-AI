from fastmcp.server import create_proxy

# Create a proxy to your remote FastMCP Cloud server
# FastMCP Cloud uses Streamable HTTP (default), so just use the /mcp URL
mcp = create_proxy(
    "https://silky-maroon-pheasant.fastmcp.app/mcp",  # Standard FastMCP Cloud URL
    name="YASH FASTMCP SERVER"
)

if __name__ == "__main__":
    # This runs via STDIO, which Claude Desktop can connect to
    mcp.run()
