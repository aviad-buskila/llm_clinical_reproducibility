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

    def _post_with_retries(
        self,
        *,
        url: str,
        payload: dict[str, Any],
        model: str,
        input_preview: str,
    ) -> dict[str, Any]:
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
                return resp.json()
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

        raise OllamaRequestError(
            f"Ollama request failed after retries model={model} url={url} "
            f"input_preview='{input_preview}' last_error={last_error}"
        ) from last_error

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

        prompt_preview = prompt.strip().replace("\n", " ")[:160]
        url = f"{self.base_url}/api/generate"
        data = self._post_with_retries(
            url=url,
            payload=payload,
            model=model,
            input_preview=prompt_preview,
        )
        data["model"] = model
        data["prompt"] = prompt
        return data

    def chat(
        self,
        model: str,
        user_message: str,
        system: str | None = None,
    ) -> dict[str, Any]:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user_message})
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.generation_config.temperature,
                "top_p": self.generation_config.top_p,
                "num_predict": self.generation_config.max_tokens,
            },
        }
        url = f"{self.base_url}/api/chat"
        preview = user_message.strip().replace("\n", " ")[:160]
        data = self._post_with_retries(
            url=url,
            payload=payload,
            model=model,
            input_preview=preview,
        )
        content = str(data.get("message", {}).get("content", ""))
        return {"model": model, "response": content, "raw": data}
