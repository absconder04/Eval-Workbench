"""Phase 0: the smallest possible MCP server, with one tool."""
import logging

from mcp.server.mcpserver import MCPServer

# IMPORTANT: never use print() in this file. Claude Desktop talks to the
# server through the same channel print() writes to, so a print breaks the
# connection. Write log messages with logging instead.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("workbench")

mcp = MCPServer("eval-workbench")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two whole numbers and return the sum.

    Use this whenever the user asks to add two numbers.
    """
    log.info("add called with a=%s b=%s", a, b)
    return a + b


if __name__ == "__main__":
    mcp.run()