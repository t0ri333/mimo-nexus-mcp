# MiMo-Nexus

<p align="center">
  <strong>Lightweight MCP intelligent gateway for token-efficient AI coding</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="README_zh.md">中文</a> •
  <a href="README_ja.md">日本語</a>
</p>

---

## Overview

MiMo-Nexus is a lightweight MCP (Model Context Protocol) gateway that intercepts large codebase analysis requests from AI coding assistants (Claude Code, Cursor, etc.) and offloads them to Xiaomi's MiMo 2.5 Pro API.

**The problem:** When AI assistants read large projects, they consume massive amounts of tokens, leading to expensive API bills and context overflow.

**The solution:** MiMo-Nexus acts as a smart proxy - it scans your local code, packages it efficiently, sends it to MiMo 2.5 Pro's 1M context window (at ~$1/M tokens), and returns concise analysis results back to your AI assistant.

**Result:** Save 60-95% on token costs while getting deeper code analysis.

## Features

- **Token-Efficient Analysis** - Offload entire codebase analysis to MiMo 2.5 Pro's 1M context window
- **OpenAI-Compatible API** - Uses standard OpenAI SDK for seamless integration
- **Thinking Model Support** - Access MiMo 2.5 Omni's reasoning chain via Gemini format
- **Voice Feedback** - Generate spoken build notifications using MiMo TTS
- **Smart File Filtering** - Automatically skips .git, node_modules, binaries, and other irrelevant files
- **MCP Protocol** - Works with any MCP-compatible AI assistant out of the box

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- MiMo API key from [platform.xiaomimimo.com](https://platform.xiaomimimo.com)

### Install with uv (Recommended)

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

### Install from PyPI (When Published)

```bash
pip install mimo-nexus-mcp
```

## Quick Start

### 1. Configure Your API Key

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API key
# Get your key at: https://platform.xiaomimimo.com
XIAOMI_MIMO_API_KEY=your_key_here
```

### 2. Register with Claude Code

```bash
# Register the MCP server globally
claude mcp add \
  --env XIAOMI_MIMO_API_KEY=$XIAOMI_MIMO_API_KEY \
  --transport stdio \
  mimo-nexus \
  -- uv run server.py
```

### 3. Use in Your Workflow

In Claude Code, simply ask:

```
Analyze the authentication module in this project and identify potential security vulnerabilities.
```

Claude Code will automatically call MiMo-Nexus, which:
1. Scans your local source files
2. Packages them into a structured payload
3. Sends to MiMo 2.5 Pro for deep analysis
4. Returns a concise report (saving you thousands of tokens)

## API Reference

### MCP Tools

#### `mimo_global_repo_analyzer`

Analyze an entire codebase by offloading to MiMo 2.5 Pro's 1M context.

**Parameters:**
- `directory_path` (str): Absolute path to the project directory
- `architectural_query` (str): The specific question or focus for analysis
- `model` (str, optional): Model ID (default: `mimo-v2.5-pro`)
- `use_thinking` (bool, optional): Enable thinking mode for `mimo-v2.5-omni`

**Returns:** Detailed analysis report with file references and specific recommendations.

#### `mimo_code_query`

Quick query about the codebase without full analysis.

**Parameters:**
- `question` (str): The specific question about the code
- `directory_path` (str, optional): Project root directory (default: `.`)
- `model` (str, optional): Model ID (default: `mimo-v2.5-pro`)

**Returns:** Concise answer based on project structure.

#### `mimo_voice_broadcaster`

Generate spoken audio feedback using MiMo TTS.

**Parameters:**
- `report_text` (str): Text content to convert to speech
- `vibe_style` (str, optional): Emotional tone preset
  - `professional_engineer`: Calm, precise senior engineer
  - `urgent_warning`: Anxious system admin warning
  - `calm_success`: Warm satisfaction after successful build
  - `hacker_cyberpunk`: Fast-talking cyberpunk hacker

**Returns:** Dict with `audio_path` (local file path) and `metadata`.

## Supported Models

| Model | ID | Format | Context | Use Case |
|-------|-----|--------|---------|----------|
| MiMo 2.5 Pro | `mimo-v2.5-pro` | OpenAI | 1M tokens | Code analysis, architecture review |
| MiMo 2.5 | `mimo-v2.5` | OpenAI | 1M tokens | Lightweight queries |
| MiMo 2.5 Omni | `mimo-v2.5-omni` | OpenAI / Gemini | 1M tokens | Thinking mode with reasoning chain |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `XIAOMI_MIMO_API_KEY` | Yes | Your MiMo API key |

### Inference Parameters

The gateway uses optimized parameters per MiMo's official recommendations:

| Parameter | Standard Models | Thinking Model |
|-----------|----------------|----------------|
| Temperature | 0.3 | 1.0 |
| Top P | 0.95 | 0.95 |

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Code    │────▶│  MiMo-Nexus      │────▶│  MiMo 2.5 Pro   │
│  (Local AI)     │◀────│  MCP Gateway     │◀────│  API (Cloud)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        │                   ┌────┴────┐
        │                   │ Local   │
        │                   │ Files   │
        │                   └─────────┘
        ▼
  Concise results (300 tokens)
  instead of raw code (80,000 tokens)
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) for MCP protocol handling
- Powered by [Xiaomi MiMo 2.5 Pro](https://platform.xiaomimimo.com) for cloud inference
- Inspired by [headroom](https://github.com/anthropics/headroom) for token optimization concepts
