# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.239 |                   0.046 |             0.000 |      0.023 |         0.142 |              0.835 |             0.580 |             0.226 |                      0.046 |                0.000 |         0.009 |            0.135 |                 0.829 |                0.600 |
| medaibase/medgemma1.5:4b |          0.218 |                   0.042 |             0.000 |      0.023 |         0.126 |              0.838 |             0.450 |             0.235 |                      0.035 |                0.000 |         0.004 |            0.120 |                 0.822 |                0.400 |
| gemma3:12b               |          0.200 |                   0.040 |             0.000 |      0.017 |         0.124 |              0.835 |             0.735 |             0.193 |                      0.042 |                0.000 |         0.008 |            0.117 |                 0.833 |                0.850 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            0.240 |                                 0.960 |
| llama3.1:8b              |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b |                            0.200 |                                 1.000 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| gemma3:12b               | q13114        |        5 |                            0.200 |                                 1.000 |
| gemma3:12b               | q4199         |        5 |                            0.200 |                                 1.000 |
| gemma3:12b               | q6039         |        5 |                            0.200 |                                 1.000 |
| gemma3:12b               | q9076         |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q11715        |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q13114        |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q4199         |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q6039         |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q9076         |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q11715        |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q13114        |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q4199         |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q6039         |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q9076         |        5 |                            0.200 |                                 1.000 |
| gemma3:12b               | q11715        |        5 |                            0.400 |                                 0.800 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |              25 |               24 |                          24 |                             0.960 |                               0.960 |
| llama3.1:8b              |              25 |               25 |                          25 |                             1.000 |                               1.000 |
| medaibase/medgemma1.5:4b |              25 |               25 |                          25 |                             1.000 |                               1.000 |

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
| llama3.1:8b              |         2980.454 |             125.120 |                  42.924 |            2954.582 |                129.000 |                     43.992 |
| medaibase/medgemma1.5:4b |         3475.675 |              94.400 |                  28.014 |            3153.806 |                 91.000 |                     28.761 |
| gemma3:12b               |         3916.278 |              98.400 |                  25.273 |            3884.826 |                100.000 |                     25.793 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.
- Use Part 4 to compare overall model variability without question-level grouping.
- Use Part 5 to compare direct model-to-model behavioral overlap.
- Use Part 6 to compare speed and token output characteristics across models.