"""LLM service for generating comparison summaries.

Uses Strategy pattern with multiple LLM providers.
Supports: Qwen (default), ChatGPT, Claude, Gemini, DeepSeek.
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Type

from models.entities import ComparisonResult
from services.industry_strategy import ComparisonStrategy


def _build_prompt(result: ComparisonResult, strategy: ComparisonStrategy) -> str:
    """Build the comparison prompt (shared across all providers)."""
    feature_rows = "\n".join(
        f"| {f.name} | {va} | {vb} |"
        for f, va, vb, _w in result.feature_comparisons
    )
    expert_context = "\n".join(
        f"- {ea.author}: {ea.advice_text}"
        for ea in result.expert_advice_list
    )
    return f"""You are a database technology analyst. Compare {result.product_a.name} vs {result.product_b.name} for the "{result.industry.name}" use case.

{strategy.get_llm_context_prompt()}

Feature comparison data:
| Feature | {result.product_a.name} | {result.product_b.name} |
|---------|----------|----------|
{feature_rows}

Expert advice from the field:
{expert_context if expert_context else "No expert advice available."}

Provide:
1. A 2-3 sentence executive summary of which product is stronger for this industry and why.
2. 3-5 bullet points highlighting key differentiators.
3. A recommendation with caveats.

Keep the tone professional and balanced. Be specific, cite the feature data above."""


# ---------------------------------------------------------------------------
# Strategy pattern: LLM providers
# ---------------------------------------------------------------------------

class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def call(self, prompt: str) -> str:
        ...


class QwenProvider(LLMProvider):
    """Alibaba Qwen via DashScope OpenAI-compatible API."""

    def call(self, prompt: str) -> str:
        import json
        import urllib.request
        url = "https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions"
        data = json.dumps({
            "model": "qwen3.5-plus",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('DASHSCOPE_API_KEY', '')}",
        })
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read())
        return body["choices"][0]["message"]["content"]


class ChatGPTProvider(LLMProvider):
    """OpenAI ChatGPT."""

    def call(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        resp = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content


class ClaudeProvider(LLMProvider):
    """Anthropic Claude."""

    def call(self, prompt: str) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text


class GeminiProvider(LLMProvider):
    """Google Gemini via OpenAI-compatible API."""

    def call(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("GEMINI_API_KEY", ""),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        resp = client.chat.completions.create(
            model="gemini-2.0-flash",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content


class DeepSeekProvider(LLMProvider):
    """DeepSeek via OpenAI-compatible API."""

    def call(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
            base_url="https://api.deepseek.com",
        )
        resp = client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

class LLMProviderFactory:
    """Factory for creating LLM provider instances."""

    _registry: Dict[str, Type[LLMProvider]] = {
        "Qwen": QwenProvider,
        "ChatGPT": ChatGPTProvider,
        "Claude": ClaudeProvider,
        "Gemini": GeminiProvider,
        "DeepSeek": DeepSeekProvider,
    }

    # Environment variable name for each provider's API key
    ENV_KEYS: Dict[str, str] = {
        "Qwen": "DASHSCOPE_API_KEY",
        "ChatGPT": "OPENAI_API_KEY",
        "Claude": "ANTHROPIC_API_KEY",
        "Gemini": "GEMINI_API_KEY",
        "DeepSeek": "DEEPSEEK_API_KEY",
    }

    DEFAULT = "Qwen"

    @classmethod
    def provider_names(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, name: str) -> LLMProvider:
        provider_cls = cls._registry.get(name)
        if not provider_cls:
            raise ValueError(f"Unknown LLM provider: {name}")
        return provider_cls()


# ---------------------------------------------------------------------------
# Service facade (public API unchanged)
# ---------------------------------------------------------------------------

class LLMService:
    """Generates comparison summaries using a selectable LLM provider."""

    def __init__(self, provider_name: str = None):
        self._provider_name = provider_name or LLMProviderFactory.DEFAULT
        self._provider = LLMProviderFactory.create(self._provider_name)

    def generate_comparison_summary(
        self, result: ComparisonResult, strategy: ComparisonStrategy
    ) -> str:
        env_key = LLMProviderFactory.ENV_KEYS.get(self._provider_name, "")
        if env_key and not os.environ.get(env_key):
            return (
                f"LLM analysis unavailable. Please set the {env_key} "
                f"environment variable to enable {self._provider_name} summaries."
            )
        try:
            prompt = _build_prompt(result, strategy)
            return self._provider.call(prompt)
        except Exception as e:
            return f"LLM analysis failed ({self._provider_name}): {e}"
