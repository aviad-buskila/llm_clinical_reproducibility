from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def compute_aggregates(scored_df: pd.DataFrame) -> pd.DataFrame:
    df = scored_df.copy()
    df["response_len"] = df["response_text"].astype(str).str.len()
    df["is_unique_response"] = (
        df.groupby(["model", "question_id"])["response_text"].transform("nunique")
        / df.groupby(["model", "question_id"])["response_text"].transform("size")
    )

    metrics = ["exact_match", "normalized_exact_match", "token_f1", "string_similarity"]
    if "judge_score" in df.columns:
        metrics.append("judge_score")

    grouped = df.groupby(["model", "question_id"], dropna=False)
    agg = grouped[metrics].agg(["mean", "median", "std", "min", "max"]).reset_index()
    agg.columns = ["_".join([c for c in col if c]).rstrip("_") for col in agg.columns.to_flat_index()]

    extra = grouped.agg(
        n_runs=("run_index", "count"),
        unique_responses=("response_text", "nunique"),
        avg_response_length=("response_len", "mean"),
    ).reset_index()
    extra["response_uniqueness_rate"] = extra["unique_responses"] / extra["n_runs"].replace(0, np.nan)

    return agg.merge(extra, on=["model", "question_id"], how="left")


def save_aggregates(aggregate_df: pd.DataFrame, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "aggregates.csv"
    aggregate_df.to_csv(path, index=False)
    return path
