from __future__ import annotations

import re

import pandas as pd

from clinical_eval_pipeline.config import JudgeConfig, PipelineConfig
from clinical_eval_pipeline.ollama_client import OllamaClient


def _extract_score(text: str) -> float | None:
    match = re.search(r"score\s*=\s*([0-9]*\.?[0-9]+)", text.lower())
    if match:
        score = float(match.group(1))
        return max(0.0, min(1.0, score))

    # Fallback: take first standalone float between 0 and 1 from the judge output.
    fallback = re.search(r"\b(0(?:\.\d+)?|1(?:\.0+)?)\b", text.lower())
    if fallback:
        score = float(fallback.group(1))
        return max(0.0, min(1.0, score))
    return None


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
    parse_failures = 0

    for _, row in out.iterrows():
        judge_prompt = (
            f"{judge_cfg.rubric_prompt}\n\n"
            f"QUESTION: {row['question']}\n"
            f"GOLD_ANSWER: {row['gold_answer']}\n"
            f"MODEL_ANSWER: {row['response_text']}\n"
        )
        result = client.generate(model=judge_cfg.model, prompt=judge_prompt)
        judge_text = str(result.get("response", "")).strip()
        parsed = _extract_score(judge_text)
        if parsed is None:
            parse_failures += 1
            snippet = judge_text.replace("\n", " ")[:220]
            print(
                f"[judge][warn] could not parse score for model={row['model']} "
                f"question_id={row['question_id']} output='{snippet}'",
                flush=True,
            )
        judge_scores.append(parsed)
        judge_rationales.append(judge_text)

    out["judge_score"] = judge_scores
    out["judge_rationale"] = judge_rationales
    print(
        f"[judge] completed rows={len(out)} parsed_scores={len(out) - parse_failures} "
        f"parse_failures={parse_failures}",
        flush=True,
    )
    return out
