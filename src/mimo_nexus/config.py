"""Configuration management for MiMo-Nexus gateway."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

# MiMo API base URLs
MIMO_OPENAI_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_GEMINI_BASE_URL = "https://api.xiaomimimo.com/v1beta/models"

# Model IDs
MODEL_STANDARD = "mimo-v2.5-pro"
MODEL_LIGHTWEIGHT = "mimo-v2.5"
MODEL_THINKING = "mimo-v2.5-omni"

# Recommended inference parameters (per MiMo official docs)
DEFAULT_TEMPERATURE = 0.3
DEFAULT_TOP_P = 0.95
THINKING_TEMPERATURE = 1.0
THINKING_TOP_P = 0.95

# File scanning defaults
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    "dist", "build", ".next", ".nuxt", "target",
    ".idea", ".vscode", ".DS_Store",
}

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".webp",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".flac",
    ".zip", ".tar", ".gz", ".rar", ".7z", ".bz2",
    ".exe", ".dll", ".so", ".dylib", ".o", ".a",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".woff", ".woff2", ".ttf", ".eot",
    ".sqlite", ".db", ".sqlite3",
    ".pyc", ".pyo", ".class", ".beam",
}

MAX_FILE_SIZE = 512 * 1024  # 512KB per file


@dataclass
class MiMoConfig:
    """MiMo API configuration."""
    api_key: str = field(default_factory=lambda: os.getenv("XIAOMI_MIMO_API_KEY", ""))
    openai_base_url: str = MIMO_OPENAI_BASE_URL
    gemini_base_url: str = MIMO_GEMINI_BASE_URL
    default_model: str = MODEL_STANDARD
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError(
                "XIAOMI_MIMO_API_KEY not set. "
                "Get your key at https://platform.xiaomimimo.com"
            )
