# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.274 |                   0.063 |             0.000 |      0.028 |         0.164 |              0.846 |             0.499 |             0.271 |                      0.048 |                0.000 |         0.009 |            0.159 |                 0.846 |                0.400 |
| gemma3:12b               |          0.230 |                   0.042 |             0.000 |      0.011 |         0.134 |              0.842 |             0.579 |             0.231 |                      0.047 |                0.000 |         0.003 |            0.123 |                 0.836 |                0.600 |
| medaibase/medgemma1.5:4b |          0.229 |                   0.045 |             0.000 |      0.010 |         0.135 |              0.835 |             0.557 |             0.230 |                      0.046 |                0.000 |         0.004 |            0.134 |                 0.845 |                0.750 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            0.154 |                                 0.582 |
| medaibase/medgemma1.5:4b |                            0.126 |                                 0.716 |
| llama3.1:8b              |                            0.028 |                                 0.904 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| llama3.1:8b              | q7803         |      100 |                            0.010 |                                 1.000 |
| llama3.1:8b              | q9360         |      100 |                            0.010 |                                 1.000 |
| llama3.1:8b              | q11493        |      100 |                            0.020 |                                 0.990 |
| medaibase/medgemma1.5:4b | q9360         |      100 |                            0.030 |                                 0.920 |
| llama3.1:8b              | q10741        |      100 |                            0.030 |                                 0.890 |
| gemma3:12b               | q11493        |      100 |                            0.050 |                                 0.910 |
| medaibase/medgemma1.5:4b | q7803         |      100 |                            0.050 |                                 0.860 |
| medaibase/medgemma1.5:4b | q11493        |      100 |                            0.070 |                                 0.880 |
| llama3.1:8b              | q2009         |      100 |                            0.070 |                                 0.640 |
| gemma3:12b               | q9360         |      100 |                            0.090 |                                 0.710 |
| gemma3:12b               | q7803         |      100 |                            0.090 |                                 0.640 |
| gemma3:12b               | q2009         |      100 |                            0.090 |                                 0.470 |
| medaibase/medgemma1.5:4b | q2009         |      100 |                            0.240 |                                 0.530 |
| medaibase/medgemma1.5:4b | q10741        |      100 |                            0.240 |                                 0.390 |
| gemma3:12b               | q10741        |      100 |                            0.450 |                                 0.180 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |             500 |              296 |                         291 |                             0.592 |                               0.582 |
| medaibase/medgemma1.5:4b |             500 |              359 |                         358 |                             0.718 |                               0.716 |
| llama3.1:8b              |             500 |              453 |                         452 |                             0.906 |                               0.904 |

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
| llama3.1:8b              |         3327.061 |             143.156 |                  43.199 |            3244.847 |                139.500 |                     43.546 |
| gemma3:12b               |         4451.418 |             111.058 |                  24.944 |            4278.436 |                107.000 |                     24.993 |
| medaibase/medgemma1.5:4b |         4489.626 |             131.722 |                  29.182 |            3088.841 |                 90.000 |                     29.169 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.
- Use Part 4 to compare overall model variability without question-level grouping.
- Use Part 5 to compare direct model-to-model behavioral overlap.
- Use Part 6 to compare speed and token output characteristics across models.