"""MiMo-Nexus MCP Server entry point.

Run with: uv run main.py
Or register with Claude Code:
  claude mcp add --transport stdio mimo-nexus -- uv run main.py
"""

from src.mimo_nexus.server import main

if __name__ == "__main__":
    main()
