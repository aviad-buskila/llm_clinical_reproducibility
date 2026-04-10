# Clinical Reproducibility Evaluation Report

## Model-level Means

| model                    |   token_f1 |   string_similarity |   exact_match |
|:-------------------------|-----------:|--------------------:|--------------:|
| medaibase/medgemma1.5:4b |      0.400 |               0.265 |         0.000 |
| llama3.1:8b              |      0.325 |               0.080 |         0.000 |
| gemma3:12b               |      0.311 |               0.210 |         0.000 |

## Top Model/Question Results (Token F1 Mean)

| model                    | question_id   |   token_f1_mean |   string_similarity_mean |
|:-------------------------|:--------------|----------------:|-------------------------:|
| medaibase/medgemma1.5:4b | q1            |           0.400 |                    0.265 |
| llama3.1:8b              | q1            |           0.325 |                    0.080 |
| gemma3:12b               | q1            |           0.311 |                    0.210 |

## Notes
- This report aggregates repeated runs for reproducibility analysis.
- Inspect `outputs/figures/` for visualization artifacts.