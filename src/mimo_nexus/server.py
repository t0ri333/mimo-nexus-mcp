"""MiMo-Nexus MCP Server - Smart gateway for token-efficient AI coding.

Exposes MCP tools that intercept large codebase analysis requests,
delegate them to Xiaomi MiMo 2.5 Pro's 1M context window, and return
concise results to save 60-95% of token costs.
"""

import asyncio
import os
import time
from pathlib import Path

from fastmcp import FastMCP

from .config import MiMoConfig, MODEL_STANDARD
from .mimo_client import MiMoClient
from .context_builder import scan_directory, build_context_payload

# Initialize MCP server
mcp = FastMCP("MiMo-Nexus-Gateway")

# Lazy-initialized client (created on first use to avoid import-time API key check)
_client: MiMoClient | None = None


def _get_client() -> MiMoClient:
    global _client
    if _client is None:
        _client = MiMoClient(MiMoConfig())
    return _client


@mcp.tool()
async def mimo_global_repo_analyzer(
    directory_path: str,
    architectural_query: str,
    model: str = MODEL_STANDARD,
    use_thinking: bool = False,
) -> str:
    """Analyze an entire codebase by offloading to MiMo 2.5 Pro's 1M context.

    Scans all source files in the given directory, packages them into a
    structured payload, and sends to MiMo for deep analysis. Returns a
    concise report instead of raw code, saving massive token costs.

    Args:
        directory_path: Absolute path to the project directory to analyze
        architectural_query: The specific question or focus for the analysis
        model: MiMo model to use (mimo-v2.5-pro, mimo-v2.5, mimo-v2.5-omni)
        use_thinking: Enable thinking mode for mimo-v2.5-omni (shows reasoning chain)
    """
    client = _get_client()

    # Step 1: Scan local files
    files = scan_directory(directory_path)
    if not files:
        return f"No source files found in {directory_path}"

    # Step 2: Build context payload
    payload = build_context_payload(files, architectural_query)

    system_prompt = (
        "You are a senior software architect and code reviewer. "
        "Analyze the provided codebase thoroughly and answer the user's question. "
        "Be specific: reference file paths, line numbers, variable names, and "
        "concrete code changes. Structure your response with clear sections."
    )

    # Step 3: Send to MiMo cloud
    if use_thinking and "omni" in model.lower():
        thinking, response = await client.think(
            prompt=payload,
            system=system_prompt,
            model=model,
        )
        if thinking:
            return f"## Thinking Process\n{thinking}\n\n## Analysis Report\n{response}"
        return response
    else:
        response = await client.chat(
            prompt=payload,
            system=system_prompt,
            model=model,
        )
        return response


@mcp.tool()
async def mimo_voice_broadcaster(
    report_text: str,
    vibe_style: str = "professional_engineer",
) -> dict:
    """Generate spoken audio feedback using MiMo TTS.

    Converts a text report into natural speech with the specified emotional
    tone. Useful for hands-free notifications about build status, errors,
    or analysis results.

    Args:
        report_text: The text content to convert to speech
        vibe_style: Emotional tone preset. Options:
            - professional_engineer: Calm, precise senior engineer
            - urgent_warning: Anxious system admin warning
            - calm_success: Warm satisfaction after successful build
            - hacker_cyberpunk: Fast-talking cyberpunk hacker

    Returns:
        Dict with 'audio_path' (local file path) and 'metadata' (generation info)
    """
    client = _get_client()

    # Generate audio
    audio_bytes = await client.tts(text=report_text, voice_style=vibe_style)

    # Save to local audio log directory
    audio_dir = Path(".mimo_audio_logs")
    audio_dir.mkdir(exist_ok=True)

    timestamp = int(time.time())
    safe_style = vibe_style.replace(" ", "_")
    filename = f"{safe_style}_{timestamp}.mp3"
    filepath = audio_dir / filename

    filepath.write_bytes(audio_bytes)

    return {
        "audio_path": str(filepath.resolve()),
        "metadata": {
            "style": vibe_style,
            "duration_estimate_sec": len(audio_bytes) / 16000,  # rough estimate
            "file_size_bytes": len(audio_bytes),
        },
    }


@mcp.tool()
async def mimo_code_query(
    question: str,
    directory_path: str = ".",
    model: str = MODEL_STANDARD,
) -> str:
    """Quick query about the codebase without full analysis.

    A lighter alternative to mimo_global_repo_analyzer. Scans the project
    structure (file tree only) plus any explicitly referenced files, then
    asks MiMo a focused question.

    Args:
        question: The specific question about the code
        directory_path: Project root directory (defaults to current dir)
        model: MiMo model to use
    """
    client = _get_client()

    # Build a lightweight context: just the file tree
    root = Path(directory_path).resolve()
    tree_lines: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {
            ".git", "node_modules", ".venv", "__pycache__", ".mypy_cache",
        }]
        level = Path(dirpath).relative_to(root).parts
        indent = "  " * len(level)
        tree_lines.append(f"{indent}{Path(dirpath).name}/")
        for f in sorted(filenames):
            tree_lines.append(f"{indent}  {f}")

    file_tree = "\n".join(tree_lines)

    prompt = f"""## Project Structure
```
{file_tree}
```

## Question
{question}

Based on the project structure above, answer the question. If you need
to see specific files to give a better answer, list which files should
be examined."""

    return await client.chat(
        prompt=prompt,
        system="You are a helpful senior developer. Answer concisely.",
        model=model,
    )


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
