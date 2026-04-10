# Clinical Reproducibility Evaluation Report

## Model-level Means

| model                    |   token_f1 |   string_similarity |   exact_match |
|:-------------------------|-----------:|--------------------:|--------------:|
| gemma3:12b               |      0.400 |               0.196 |         0.000 |
| medaibase/medgemma1.5:4b |      0.400 |               0.197 |         0.000 |
| llama3.1:8b              |      0.378 |               0.206 |         0.000 |
| gpt-oss:20b              |      0.306 |               0.196 |         0.000 |

## Top Model/Question Results (Token F1 Mean)

| model                    | question_id   |   token_f1_mean |   string_similarity_mean |
|:-------------------------|:--------------|----------------:|-------------------------:|
| gemma3:12b               | q1            |           0.400 |                    0.196 |
| medaibase/medgemma1.5:4b | q1            |           0.400 |                    0.197 |
| llama3.1:8b              | q1            |           0.378 |                    0.206 |
| gpt-oss:20b              | q1            |           0.306 |                    0.196 |

## Notes
- This report aggregates repeated runs for reproducibility analysis.
- Inspect `outputs/figures/` for visualization artifacts.