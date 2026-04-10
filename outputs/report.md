# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.401 |                   0.157 |             0.000 |      0.120 |         0.292 |              0.899 |             0.915 |             0.401 |                      0.157 |                0.000 |         0.120 |            0.292 |                 0.899 |                0.925 |
| medaibase/medgemma1.5:4b |          0.390 |                   0.177 |             0.000 |      0.132 |         0.353 |              0.897 |             0.900 |             0.390 |                      0.177 |                0.000 |         0.132 |            0.353 |                 0.897 |                0.900 |
| gemma3:12b               |          0.345 |                   0.155 |             0.000 |      0.111 |         0.276 |              0.891 |             0.900 |             0.345 |                      0.155 |                0.000 |         0.111 |            0.276 |                 0.891 |                0.900 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            1.000 |                                 0.200 |
| llama3.1:8b              |                            1.000 |                                 0.200 |
| medaibase/medgemma1.5:4b |                            1.000 |                                 0.200 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| gemma3:12b               | q1            |        5 |                            1.000 |                                 0.200 |
| gemma3:12b               | q2            |        5 |                            1.000 |                                 0.200 |
| llama3.1:8b              | q1            |        5 |                            1.000 |                                 0.200 |
| llama3.1:8b              | q2            |        5 |                            1.000 |                                 0.200 |
| medaibase/medgemma1.5:4b | q1            |        5 |                            1.000 |                                 0.200 |
| medaibase/medgemma1.5:4b | q2            |        5 |                            1.000 |                                 0.200 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |              10 |                2 |                           2 |                             0.200 |                               0.200 |
| llama3.1:8b              |              10 |                2 |                           2 |                             0.200 |                               0.200 |
| medaibase/medgemma1.5:4b |              10 |                2 |                           2 |                             0.200 |                               0.200 |

## Part 5 - Pairwise Model Similarity Matrix

Cell value = fraction of aligned `(question_id, run_index)` pairs where two models produced the exact same normalized output.

|                          |   gemma3:12b |   llama3.1:8b |   medaibase/medgemma1.5:4b |
|:-------------------------|-------------:|--------------:|---------------------------:|
| gemma3:12b               |        1.000 |         0.000 |                      0.000 |
| llama3.1:8b              |        0.000 |         1.000 |                      0.000 |
| medaibase/medgemma1.5:4b |        0.000 |         0.000 |                      1.000 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.
- Use Part 4 to compare overall model variability without question-level grouping.
- Use Part 5 to compare direct model-to-model behavioral overlap.