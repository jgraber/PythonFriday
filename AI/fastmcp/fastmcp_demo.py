from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def ip() -> str:
    """What is my IP address?"""
    return "0.0.1.2.3"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)