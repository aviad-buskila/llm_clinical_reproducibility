# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.401 |                   0.157 |             0.000 |      0.120 |         0.292 |              0.899 |             0.800 |             0.401 |                      0.157 |                0.000 |         0.120 |            0.292 |                 0.899 |                0.800 |
| medaibase/medgemma1.5:4b |          0.390 |                   0.177 |             0.000 |      0.132 |         0.353 |              0.897 |             0.800 |             0.390 |                      0.177 |                0.000 |         0.132 |            0.353 |                 0.897 |                0.800 |
| gemma3:12b               |          0.345 |                   0.155 |             0.000 |      0.111 |         0.276 |              0.891 |             0.750 |             0.345 |                      0.155 |                0.000 |         0.111 |            0.276 |                 0.891 |                0.750 |
| gpt-oss:20b              |          0.332 |                   0.145 |             0.000 |      0.116 |         0.253 |              0.885 |             0.750 |             0.332 |                      0.145 |                0.000 |         0.116 |            0.253 |                 0.885 |                0.750 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            1.000 |                                 1.000 |
| gpt-oss:20b              |                            1.000 |                                 1.000 |
| llama3.1:8b              |                            1.000 |                                 1.000 |
| medaibase/medgemma1.5:4b |                            1.000 |                                 1.000 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| gemma3:12b               | q1            |        1 |                            1.000 |                                 1.000 |
| gemma3:12b               | q2            |        1 |                            1.000 |                                 1.000 |
| gpt-oss:20b              | q1            |        1 |                            1.000 |                                 1.000 |
| gpt-oss:20b              | q2            |        1 |                            1.000 |                                 1.000 |
| llama3.1:8b              | q1            |        1 |                            1.000 |                                 1.000 |
| llama3.1:8b              | q2            |        1 |                            1.000 |                                 1.000 |
| medaibase/medgemma1.5:4b | q1            |        1 |                            1.000 |                                 1.000 |
| medaibase/medgemma1.5:4b | q2            |        1 |                            1.000 |                                 1.000 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.