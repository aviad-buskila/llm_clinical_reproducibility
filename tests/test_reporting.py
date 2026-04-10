from pathlib import Path

import pandas as pd

from clinical_eval_pipeline.reporting import _pairwise_model_similarity, write_markdown_report


def _sample_scored_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "model": "m1",
                "question_id": "q1",
                "run_index": 0,
                "response_text": "Alpha",
                "normalized_response": "alpha",
                "token_f1": 0.5,
                "string_similarity": 0.5,
                "exact_match": 0.0,
                "bleu": 0.4,
                "rouge_l": 0.4,
                "bertscore_f1": 0.8,
                "judge_score": 0.7,
            },
            {
                "model": "m2",
                "question_id": "q1",
                "run_index": 0,
                "response_text": "Alpha",
                "normalized_response": "alpha",
                "token_f1": 0.6,
                "string_similarity": 0.6,
                "exact_match": 0.0,
                "bleu": 0.5,
                "rouge_l": 0.5,
                "bertscore_f1": 0.85,
                "judge_score": 0.8,
            },
        ]
    )


def _sample_aggregate_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "model": "m1",
                "question_id": "q1",
                "n_runs": 1,
                "normalized_self_agreement_rate": 1.0,
                "normalized_response_uniqueness_rate": 1.0,
            },
            {
                "model": "m2",
                "question_id": "q1",
                "n_runs": 1,
                "normalized_self_agreement_rate": 1.0,
                "normalized_response_uniqueness_rate": 1.0,
            },
        ]
    )


def test_pairwise_model_similarity_identity_and_match() -> None:
    matrix = _pairwise_model_similarity(_sample_scored_df())
    assert matrix.loc["m1", "m1"] == 1.0
    assert matrix.loc["m2", "m2"] == 1.0
    assert matrix.loc["m1", "m2"] == 1.0


def test_write_markdown_report_includes_all_parts(tmp_path: Path) -> None:
    report_path = write_markdown_report(_sample_scored_df(), _sample_aggregate_df(), tmp_path)
    content = report_path.read_text(encoding="utf-8")
    assert "## Part 1 - Model-vs-Gold Quality (Average and Median)" in content
    assert "## Part 2 - Within-Model Reproducibility (Ignoring Gold)" in content
    assert "## Part 3 - Reproducibility by Model and Question" in content
    assert "## Part 4 - Global Model Comparison (Ignoring Question ID)" in content
    assert "## Part 5 - Pairwise Model Similarity Matrix" in content
