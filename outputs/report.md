# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| medaibase/medgemma1.5:4b |          0.390 |                   0.180 |             0.000 |      0.124 |         0.349 |              0.897 |             0.880 |             0.400 |                      0.181 |                0.000 |         0.132 |            0.356 |                 0.897 |                0.900 |
| llama3.1:8b              |          0.361 |                   0.146 |             0.000 |      0.111 |         0.287 |              0.893 |             0.920 |             0.378 |                      0.144 |                0.000 |         0.120 |            0.286 |                 0.890 |                0.925 |
| gemma3:12b               |          0.350 |                   0.161 |             0.000 |      0.118 |         0.277 |              0.891 |             0.920 |             0.365 |                      0.167 |                0.000 |         0.125 |            0.286 |                 0.893 |                0.925 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| medaibase/medgemma1.5:4b |                            0.800 |                                 0.400 |
| gemma3:12b               |                            0.700 |                                 0.400 |
| llama3.1:8b              |                            0.500 |                                 0.700 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| llama3.1:8b              | q2            |        5 |                            0.200 |                                 1.000 |
| gemma3:12b               | q2            |        5 |                            0.400 |                                 0.600 |
| medaibase/medgemma1.5:4b | q2            |        5 |                            0.600 |                                 0.600 |
| llama3.1:8b              | q1            |        5 |                            0.800 |                                 0.400 |
| gemma3:12b               | q1            |        5 |                            1.000 |                                 0.200 |
| medaibase/medgemma1.5:4b | q1            |        5 |                            1.000 |                                 0.200 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |              10 |                4 |                           4 |                             0.400 |                               0.400 |
| medaibase/medgemma1.5:4b |              10 |                4 |                           4 |                             0.400 |                               0.400 |
| llama3.1:8b              |              10 |                7 |                           7 |                             0.700 |                               0.700 |

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