from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _df_to_markdown_or_fallback(df: pd.DataFrame, **kwargs) -> str:
    try:
        return df.to_markdown(**kwargs)
    except ImportError:
        # Fallback keeps report generation working even if tabulate is missing.
        return df.to_string(index=kwargs.get("index", True))


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


def write_markdown_report(
    scored_df: pd.DataFrame,
    aggregate_df: pd.DataFrame,
    output_dir: str | Path,
) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.md"

    summary_cols = [
        "token_f1",
        "string_similarity",
        "exact_match",
        "bleu",
        "rouge_l",
        "bertscore_f1",
    ]
    summary_cols = [c for c in summary_cols if c in scored_df.columns]
    model_summary = scored_df.groupby("model", dropna=False)[summary_cols].mean().sort_values(
        "token_f1", ascending=False
    )
    top_rows = aggregate_df.sort_values("token_f1_mean", ascending=False).head(10)

    lines: list[str] = [
        "# Clinical Reproducibility Evaluation Report",
        "",
        "## Model-level Means",
        "",
        _df_to_markdown_or_fallback(model_summary, floatfmt=".3f"),
        "",
        "## Top Model/Question Results (Token F1 Mean)",
        "",
        _df_to_markdown_or_fallback(
            top_rows[["model", "question_id", "token_f1_mean", "string_similarity_mean"]],
            index=False, floatfmt=".3f"
        ),
        "",
        "## Notes",
        "- This report aggregates repeated runs for reproducibility analysis.",
        "- Inspect `outputs/figures/` for visualization artifacts.",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
