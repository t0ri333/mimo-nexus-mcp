"""MiMo-Nexus MCP Server entry point.

Run with: uv run server.py
Or register with Claude Code:
  claude mcp add --transport stdio mimo-nexus -- uv run server.py
"""

from src.mimo_nexus.server import main

if __name__ == "__main__":
    main()
