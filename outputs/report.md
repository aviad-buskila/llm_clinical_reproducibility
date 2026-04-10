# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.277 |                   0.075 |             0.000 |      0.032 |         0.176 |              0.852 |             0.592 |             0.274 |                      0.045 |                0.000 |         0.013 |            0.167 |                 0.849 |                0.600 |
| medaibase/medgemma1.5:4b |          0.249 |                   0.066 |             0.000 |      0.024 |         0.161 |              0.848 |             0.459 |             0.233 |                      0.040 |                0.000 |         0.010 |            0.146 |                 0.856 |                0.400 |
| gemma3:12b               |          0.239 |                   0.065 |             0.000 |      0.020 |         0.150 |              0.847 |             0.600 |             0.218 |                      0.041 |                0.000 |         0.010 |            0.135 |                 0.858 |                0.700 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            0.198 |                                 0.868 |
| medaibase/medgemma1.5:4b |                            0.146 |                                 0.936 |
| llama3.1:8b              |                            0.122 |                                 0.974 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model       | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| gemma3:12b  | q10308        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q10686        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q11564        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q12291        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q13241        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q13275        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q15174        |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q3145         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q3555         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q4227         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q4448         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q5470         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q5780         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q8526         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q8618         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q9144         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q9257         |       10 |                            0.100 |                                 1.000 |
| gemma3:12b  | q931          |       10 |                            0.100 |                                 1.000 |
| llama3.1:8b | q10254        |       10 |                            0.100 |                                 1.000 |
| llama3.1:8b | q10308        |       10 |                            0.100 |                                 1.000 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |             500 |              434 |                         434 |                             0.868 |                               0.868 |
| medaibase/medgemma1.5:4b |             500 |              468 |                         468 |                             0.936 |                               0.936 |
| llama3.1:8b              |             500 |              487 |                         487 |                             0.974 |                               0.974 |

## Part 5 - Pairwise Model Similarity Matrix

Cell value = fraction of aligned `(question_id, run_index)` pairs where two models produced the exact same normalized output.

|                          |   gemma3:12b |   llama3.1:8b |   medaibase/medgemma1.5:4b |
|:-------------------------|-------------:|--------------:|---------------------------:|
| gemma3:12b               |        1.000 |         0.000 |                      0.000 |
| llama3.1:8b              |        0.000 |         1.000 |                      0.000 |
| medaibase/medgemma1.5:4b |        0.000 |         0.000 |                      1.000 |

## Part 6 - Performance (Model Level)

Per-run latency and output token throughput, aggregated at model level.

| model                    |   latency_ms_avg |   output_tokens_avg |   tokens_per_second_avg |   latency_ms_median |   output_tokens_median |   tokens_per_second_median |
|:-------------------------|-----------------:|--------------------:|------------------------:|--------------------:|-----------------------:|---------------------------:|
| llama3.1:8b              |         2534.837 |             109.230 |                  43.012 |            2526.519 |                108.500 |                     43.099 |
| medaibase/medgemma1.5:4b |         3074.574 |              88.356 |                  28.706 |            2985.106 |                 86.000 |                     28.770 |
| gemma3:12b               |         4024.542 |             102.582 |                  25.494 |            3973.639 |                101.000 |                     25.575 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.
- Use Part 4 to compare overall model variability without question-level grouping.
- Use Part 5 to compare direct model-to-model behavioral overlap.
- Use Part 6 to compare speed and token output characteristics across models.