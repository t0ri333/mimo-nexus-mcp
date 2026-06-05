"""MiMo Cloud Gateway - Async API client for Xiaomi MiMo models.

API format overview:
- OpenAI-compatible (https://api.xiaomimimo.com/v1): chat completions, TTS
- Gemini format (https://api.xiaomimimo.com/v1beta/models): thinking model
"""

import httpx
from openai import AsyncOpenAI

from .config import (
    MiMoConfig,
    MODEL_STANDARD,
    MODEL_THINKING,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    THINKING_TEMPERATURE,
    THINKING_TOP_P,
)


class MiMoClient:
    """Async client for Xiaomi MiMo API."""

    def __init__(self, config: MiMoConfig | None = None):
        self.config = config or MiMoConfig()
        self.config.validate()

        # OpenAI-compatible client for standard models
        self._openai = AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.openai_base_url,
        )

        # Raw httpx client for Gemini-format thinking model
        self._httpx = httpx.AsyncClient(
            base_url=self.config.gemini_base_url,
            headers={
                "x-goog-api-key": self.config.api_key,
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(300.0, connect=10.0),
        )

    async def chat(
        self,
        prompt: str,
        system: str = "",
        model: str = MODEL_STANDARD,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int = 8192,
    ) -> str:
        """Send a chat completion request using OpenAI-compatible format.

        Used for: mimo-v2.5-pro, mimo-v2.5
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await self._openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature or self.config.temperature,
            top_p=top_p or self.config.top_p,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def think(
        self,
        prompt: str,
        system: str = "",
        model: str = MODEL_THINKING,
        max_tokens: int = 8192,
    ) -> tuple[str, str]:
        """Send a request to the thinking model using Gemini format.

        Used for: mimo-v2.5-omni (thinking model)

        Returns:
            (thinking_text, response_text) tuple
        """
        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
            contents.append({"role": "model", "parts": [{"text": "Understood."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": THINKING_TEMPERATURE,
                "topP": THINKING_TOP_P,
                "maxOutputTokens": max_tokens,
                "thinkingConfig": {
                    "includeThoughts": True,
                },
            },
        }

        resp = await self._httpx.post(
            f"/{model}:generateContent",
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

        # Parse Gemini response format
        thinking_text = ""
        response_text = ""

        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if part.get("thought"):
                    thinking_text += part.get("text", "")
                else:
                    response_text += part.get("text", "")

        return thinking_text, response_text

    async def tts(
        self,
        text: str,
        voice_style: str = "professional_engineer",
    ) -> bytes:
        """Generate speech audio using MiMo TTS API (OpenAI-compatible endpoint).

        Args:
            text: Text to synthesize
            voice_style: Emotion/style preset for voice generation

        Returns:
            Raw audio bytes (mp3)
        """
        style_prompts = {
            "professional_engineer": "A calm, confident senior software engineer with a clear and precise voice",
            "urgent_warning": "An urgent, slightly anxious system administrator warning about a critical failure",
            "calm_success": "A warm, satisfied engineer announcing a successful build",
            "hacker_cyberpunk": "A fast-talking cyberpunk hacker with a deep, raspy voice",
        }

        voice_description = style_prompts.get(voice_style, style_prompts["professional_engineer"])

        # TTS uses OpenAI-compatible endpoint at /v1/audio/speech
        async with httpx.AsyncClient(
            base_url=self.config.openai_base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
        ) as client:
            resp = await client.post(
                "/audio/speech",
                json={
                    "model": "mimo-v2.5-tts-voicedesign",
                    "input": text,
                    "voice": voice_description,
                    "response_format": "mp3",
                },
            )
            resp.raise_for_status()
            return resp.content

    async def close(self) -> None:
        """Clean up HTTP clients."""
        await self._openai.close()
        await self._httpx.aclose()
