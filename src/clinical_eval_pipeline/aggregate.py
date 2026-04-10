from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from clinical_eval_pipeline.scoring.deterministic import normalize_text


def compute_aggregates(scored_df: pd.DataFrame) -> pd.DataFrame:
    df = scored_df.copy()
    if "normalized_response" not in df.columns:
        df["normalized_response"] = df["response_text"].astype(str).map(normalize_text)
    if "normalized_gold" not in df.columns:
        df["normalized_gold"] = df["gold_answer"].astype(str).map(normalize_text)

    df["response_len"] = df["response_text"].astype(str).str.len()
    df["is_unique_response"] = (
        df.groupby(["model", "question_id"])["response_text"].transform("nunique")
        / df.groupby(["model", "question_id"])["response_text"].transform("size")
    )
    df["is_unique_normalized_response"] = (
        df.groupby(["model", "question_id"])["normalized_response"].transform("nunique")
        / df.groupby(["model", "question_id"])["normalized_response"].transform("size")
    )

    metrics = [
        "exact_match",
        "normalized_exact_match",
        "token_f1",
        "string_similarity",
        "bleu",
        "rouge_l",
        "bertscore_precision",
        "bertscore_recall",
        "bertscore_f1",
    ]
    metrics = [m for m in metrics if m in df.columns]
    if "judge_score" in df.columns:
        metrics.append("judge_score")

    grouped = df.groupby(["model", "question_id"], dropna=False)
    agg = grouped[metrics].agg(["mean", "median", "std", "min", "max"]).reset_index()
    agg.columns = ["_".join([c for c in col if c]).rstrip("_") for col in agg.columns.to_flat_index()]

    extra = grouped.agg(
        n_runs=("run_index", "count"),
        unique_responses=("response_text", "nunique"),
        unique_normalized_responses=("normalized_response", "nunique"),
        avg_response_length=("response_len", "mean"),
    ).reset_index()
    extra["response_uniqueness_rate"] = extra["unique_responses"] / extra["n_runs"].replace(0, np.nan)
    extra["normalized_response_uniqueness_rate"] = (
        extra["unique_normalized_responses"] / extra["n_runs"].replace(0, np.nan)
    )
    modal_counts = (
        df.groupby(["model", "question_id", "normalized_response"], dropna=False)
        .size()
        .reset_index(name="count")
        .groupby(["model", "question_id"], dropna=False)["count"]
        .max()
        .reset_index(name="modal_normalized_response_count")
    )
    extra = extra.merge(modal_counts, on=["model", "question_id"], how="left")
    extra["normalized_self_agreement_rate"] = (
        extra["modal_normalized_response_count"] / extra["n_runs"].replace(0, np.nan)
    )

    return agg.merge(extra, on=["model", "question_id"], how="left")


def save_aggregates(aggregate_df: pd.DataFrame, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "aggregates.csv"
    aggregate_df.to_csv(path, index=False)
    return path
