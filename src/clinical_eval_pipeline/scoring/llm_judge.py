from __future__ import annotations

import re

import pandas as pd

from clinical_eval_pipeline.config import JudgeConfig, PipelineConfig
from clinical_eval_pipeline.ollama_client import OllamaClient


def _extract_score(text: str) -> float | None:
    match = re.search(r"score\s*=\s*([0-9]*\.?[0-9]+)", text.lower())
    if not match:
        return None
    score = float(match.group(1))
    return max(0.0, min(1.0, score))


def apply_llm_judge(scored_df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    if not config.judge.enabled:
        out = scored_df.copy()
        out["judge_score"] = None
        out["judge_rationale"] = ""
        return out

    judge_cfg: JudgeConfig = config.judge
    if not judge_cfg.model:
        raise ValueError("Judge is enabled but no judge model is configured.")

    client = OllamaClient(config.ollama_base_url, config.generation)
    out = scored_df.copy()
    judge_scores: list[float | None] = []
    judge_rationales: list[str] = []

    for _, row in out.iterrows():
        judge_prompt = (
            f"{judge_cfg.rubric_prompt}\n\n"
            f"QUESTION: {row['question']}\n"
            f"GOLD_ANSWER: {row['gold_answer']}\n"
            f"MODEL_ANSWER: {row['response_text']}\n"
        )
        result = client.generate(model=judge_cfg.model, prompt=judge_prompt)
        judge_text = str(result.get("response", "")).strip()
        judge_scores.append(_extract_score(judge_text))
        judge_rationales.append(judge_text)

    out["judge_score"] = judge_scores
    out["judge_rationale"] = judge_rationales
    return out
