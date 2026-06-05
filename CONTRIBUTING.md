# Contributing to MiMo-Nexus

Thank you for your interest in contributing to MiMo-Nexus! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/mimo-nexus-mcp.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with a clear message
7. Push and create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/t0ri333/mimo-nexus-mcp.git
cd mimo-nexus-mcp

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your API key
# XIAOMI_MIMO_API_KEY=your_key_here
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for public functions
- Keep functions focused and small

## Testing

Before submitting a PR, ensure:
1. The MCP server starts without errors: `uv run server.py`
2. All imports work correctly
3. No syntax errors

## Pull Request Process

1. Update the README if needed
2. Add tests for new features
3. Ensure all tests pass
4. Request a review from maintainers

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
