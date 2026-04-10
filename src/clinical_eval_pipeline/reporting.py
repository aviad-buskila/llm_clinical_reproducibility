from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from clinical_eval_pipeline.scoring.deterministic import normalize_text


def _df_to_markdown_or_fallback(df: pd.DataFrame, **kwargs) -> str:
    try:
        return df.to_markdown(**kwargs)
    except ImportError:
        # Fallback keeps report generation working even if tabulate is missing.
        return df.to_string(index=kwargs.get("index", True))


def _pairwise_model_similarity(scored_df: pd.DataFrame) -> pd.DataFrame:
    df = scored_df.copy()
    if "normalized_response" not in df.columns:
        df["normalized_response"] = df["response_text"].astype(str).map(normalize_text)

    aligned = df.pivot_table(
        index=["question_id", "run_index"],
        columns="model",
        values="normalized_response",
        aggfunc="first",
    )
    models = aligned.columns.tolist()
    matrix = pd.DataFrame(1.0, index=models, columns=models, dtype=float)

    for model_a in models:
        for model_b in models:
            a_vals = aligned[model_a]
            b_vals = aligned[model_b]
            mask = a_vals.notna() & b_vals.notna()
            if mask.sum() == 0:
                sim = 0.0
            else:
                sim = float((a_vals[mask] == b_vals[mask]).mean())
            matrix.loc[model_a, model_b] = sim

    return matrix


def generate_figures(scored_df: pd.DataFrame, aggregate_df: pd.DataFrame, output_dir: str | Path) -> None:
    out_dir = Path(output_dir)
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 5))
    sns.barplot(data=scored_df, x="model", y="token_f1", errorbar="sd")
    plt.title("Average Token F1 by Model")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(fig_dir / "model_token_f1_bar.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=scored_df, x="model", y="string_similarity")
    plt.title("String Similarity Distribution by Model")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(fig_dir / "string_similarity_boxplot.png", dpi=160)
    plt.close()

    heatmap_data = aggregate_df.pivot_table(
        index="model",
        columns="question_id",
        values="token_f1_mean",
        aggfunc="mean",
    )
    plt.figure(figsize=(12, 5))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Token F1 Heatmap (Model x Question)")
    plt.tight_layout()
    plt.savefig(fig_dir / "token_f1_heatmap.png", dpi=160)
    plt.close()

    pairwise_similarity = _pairwise_model_similarity(scored_df)
    plt.figure(figsize=(10, 8))
    sns.heatmap(pairwise_similarity, annot=True, fmt=".2f", cmap="mako", vmin=0.0, vmax=1.0)
    plt.title("Pairwise Model Similarity (Normalized Output Exact Match)")
    plt.tight_layout()
    plt.savefig(fig_dir / "pairwise_model_similarity_heatmap.png", dpi=160)
    plt.close()


def write_markdown_report(
    scored_df: pd.DataFrame,
    aggregate_df: pd.DataFrame,
    output_dir: str | Path,
) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.md"

    quality_cols = [
        "token_f1",
        "string_similarity",
        "exact_match",
        "bleu",
        "rouge_l",
        "bertscore_f1",
        "judge_score",
    ]
    quality_cols = [c for c in quality_cols if c in scored_df.columns]
    model_quality_mean = scored_df.groupby("model", dropna=False)[quality_cols].mean()
    model_quality_median = scored_df.groupby("model", dropna=False)[quality_cols].median()
    quality_table = model_quality_mean.join(
        model_quality_median,
        lsuffix="_avg",
        rsuffix="_median",
    )
    if "token_f1_avg" in quality_table.columns:
        quality_table = quality_table.sort_values("token_f1_avg", ascending=False)

    reproducibility_cols = [
        "normalized_self_agreement_rate",
        "normalized_response_uniqueness_rate",
    ]
    reproducibility_cols = [c for c in reproducibility_cols if c in aggregate_df.columns]
    reproducibility_by_model = (
        aggregate_df.groupby("model", dropna=False)[reproducibility_cols]
        .mean()
        .reset_index()
    )
    if "normalized_self_agreement_rate" in reproducibility_by_model.columns:
        reproducibility_by_model = reproducibility_by_model.sort_values(
            "normalized_self_agreement_rate", ascending=False
        )

    per_question_repro_cols = [
        "model",
        "question_id",
        "n_runs",
        "normalized_self_agreement_rate",
        "normalized_response_uniqueness_rate",
    ]
    per_question_repro_cols = [c for c in per_question_repro_cols if c in aggregate_df.columns]
    reproducibility_by_model_question = aggregate_df[per_question_repro_cols].copy()
    if "normalized_self_agreement_rate" in reproducibility_by_model_question.columns:
        reproducibility_by_model_question = reproducibility_by_model_question.sort_values(
            ["normalized_self_agreement_rate", "normalized_response_uniqueness_rate"],
            ascending=[True, False],
        )

    # Global model comparison (ignores question_id granularity).
    global_model_cols = [c for c in ["model", "normalized_response", "response_text"] if c in scored_df.columns]
    global_model_comparison = (
        scored_df[global_model_cols]
        .groupby("model", dropna=False)
        .agg(
            total_outputs=("response_text", "count"),
            unique_outputs=("response_text", "nunique"),
            unique_normalized_outputs=("normalized_response", "nunique"),
        )
        .reset_index()
    )
    global_model_comparison["global_response_uniqueness_rate"] = (
        global_model_comparison["unique_outputs"] / global_model_comparison["total_outputs"]
    )
    global_model_comparison["global_normalized_uniqueness_rate"] = (
        global_model_comparison["unique_normalized_outputs"] / global_model_comparison["total_outputs"]
    )
    global_model_comparison = global_model_comparison.sort_values(
        "global_normalized_uniqueness_rate", ascending=True
    )
    pairwise_similarity = _pairwise_model_similarity(scored_df)

    lines: list[str] = [
        "# Clinical Reproducibility Evaluation Report",
        "",
        "## Part 1 - Model-vs-Gold Quality (Average and Median)",
        "",
        "Higher values indicate better alignment to gold answers.",
        "",
        _df_to_markdown_or_fallback(quality_table, floatfmt=".3f"),
        "",
        "## Part 2 - Within-Model Reproducibility (Ignoring Gold)",
        "",
        "- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).",
        "- `normalized_response_uniqueness_rate`: lower is better (less variability).",
        "",
        _df_to_markdown_or_fallback(
            reproducibility_by_model,
            index=False, floatfmt=".3f"
        ),
        "",
        "## Part 3 - Reproducibility by Model and Question",
        "",
        "Rows at the top are least reproducible and should be inspected first.",
        "",
        _df_to_markdown_or_fallback(
            reproducibility_by_model_question.head(20),
            index=False,
            floatfmt=".3f",
        ),
        "",
        "## Part 4 - Global Model Comparison (Ignoring Question ID)",
        "",
        "This section compares model output variability across all runs/questions together.",
        "",
        _df_to_markdown_or_fallback(
            global_model_comparison,
            index=False,
            floatfmt=".3f",
        ),
        "",
        "## Part 5 - Pairwise Model Similarity Matrix",
        "",
        "Cell value = fraction of aligned `(question_id, run_index)` pairs where two models "
        "produced the exact same normalized output.",
        "",
        _df_to_markdown_or_fallback(pairwise_similarity, floatfmt=".3f"),
        "",
        "## Reading Guide",
        "- Use Part 1 to compare clinical answer quality versus gold.",
        "- Use Part 2 to compare model stability across repeated runs.",
        "- Use Part 3 to find specific unstable model/question pairs.",
        "- Use Part 4 to compare overall model variability without question-level grouping.",
        "- Use Part 5 to compare direct model-to-model behavioral overlap.",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
