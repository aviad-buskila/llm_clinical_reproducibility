from __future__ import annotations

import time
from typing import Any

import requests

from clinical_eval_pipeline.config import GenerationConfig


class OllamaRequestError(RuntimeError):
    """Structured error for failed Ollama generate requests."""


class OllamaClient:
    def __init__(self, base_url: str, generation_config: GenerationConfig) -> None:
        self.base_url = base_url.rstrip("/")
        self.generation_config = generation_config

    def generate(
        self,
        model: str,
        prompt: str,
        seed: int | None = None,
        system: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.generation_config.temperature,
                "top_p": self.generation_config.top_p,
                "num_predict": self.generation_config.max_tokens,
            },
        }
        if seed is not None:
            payload["options"]["seed"] = seed
        if system:
            payload["system"] = system

        url = f"{self.base_url}/api/generate"
        retries = self.generation_config.retries
        last_error: Exception | None = None

        for attempt in range(retries + 1):
            try:
                resp = requests.post(
                    url,
                    json=payload,
                    timeout=self.generation_config.timeout_seconds,
                )
                if resp.status_code >= 400:
                    body = resp.text.strip()
                    raise RuntimeError(
                        f"Ollama HTTP {resp.status_code} for model '{model}' at {url}. "
                        f"Response: {body}"
                    )
                data = resp.json()
                data["model"] = model
                data["prompt"] = prompt
                return data
            except Exception as exc:  # broad on purpose for retry safety
                last_error = exc
                print(
                    f"[ollama][warn] attempt={attempt + 1}/{retries + 1} model={model} "
                    f"failed: {exc}",
                    flush=True,
                )
                if attempt < retries:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                break

        prompt_preview = prompt.strip().replace("\n", " ")[:160]
        raise OllamaRequestError(
            f"Ollama request failed after retries model={model} url={url} "
            f"prompt_preview='{prompt_preview}' last_error={last_error}"
        ) from last_error
