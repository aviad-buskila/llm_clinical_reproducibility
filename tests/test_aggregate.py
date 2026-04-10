import pandas as pd

from clinical_eval_pipeline.aggregate import compute_aggregates


def test_compute_aggregates_contains_reproducibility_columns() -> None:
    scored_df = pd.DataFrame(
        [
            {
                "model": "m1",
                "question_id": "q1",
                "run_index": 0,
                "response_text": "Ibuprofen is an NSAID.",
                "gold_answer": "Ibuprofen is an NSAID.",
                "exact_match": 1.0,
                "normalized_exact_match": 1.0,
                "token_f1": 1.0,
                "string_similarity": 1.0,
                "bleu": 1.0,
                "rouge_l": 1.0,
                "bertscore_precision": 0.9,
                "bertscore_recall": 0.9,
                "bertscore_f1": 0.9,
            },
            {
                "model": "m1",
                "question_id": "q1",
                "run_index": 1,
                "response_text": "Ibuprofen is an NSAID",
                "gold_answer": "Ibuprofen is an NSAID.",
                "exact_match": 0.0,
                "normalized_exact_match": 1.0,
                "token_f1": 1.0,
                "string_similarity": 1.0,
                "bleu": 1.0,
                "rouge_l": 1.0,
                "bertscore_precision": 0.9,
                "bertscore_recall": 0.9,
                "bertscore_f1": 0.9,
            },
        ]
    )

    agg = compute_aggregates(scored_df)
    assert len(agg) == 1
    row = agg.iloc[0]
    assert row["n_runs"] == 2
    assert "normalized_self_agreement_rate" in agg.columns
    assert "normalized_response_uniqueness_rate" in agg.columns
    # After normalization, both responses should match exactly.
    assert row["normalized_self_agreement_rate"] == 1.0
