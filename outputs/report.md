# Clinical Reproducibility Evaluation Report

## Part 1 - Model-vs-Gold Quality (Average and Median)

Higher values indicate better alignment to gold answers.

| model                    |   token_f1_avg |   string_similarity_avg |   exact_match_avg |   bleu_avg |   rouge_l_avg |   bertscore_f1_avg |   judge_score_avg |   token_f1_median |   string_similarity_median |   exact_match_median |   bleu_median |   rouge_l_median |   bertscore_f1_median |   judge_score_median |
|:-------------------------|---------------:|------------------------:|------------------:|-----------:|--------------:|-------------------:|------------------:|------------------:|---------------------------:|---------------------:|--------------:|-----------------:|----------------------:|---------------------:|
| llama3.1:8b              |          0.241 |                   0.005 |             0.000 |      0.044 |         0.133 |              0.826 |             0.200 |             0.236 |                      0.005 |                0.000 |         0.044 |            0.137 |                 0.825 |                0.000 |
| gemma3:12b               |          0.233 |                   0.015 |             0.000 |      0.042 |         0.159 |              0.828 |             0.400 |             0.241 |                      0.015 |                0.000 |         0.042 |            0.167 |                 0.827 |                0.000 |
| medaibase/medgemma1.5:4b |          0.213 |                   0.008 |             0.000 |      0.043 |         0.142 |              0.840 |             0.380 |             0.221 |                      0.008 |                0.000 |         0.042 |            0.138 |                 0.839 |                0.000 |

## Part 2 - Within-Model Reproducibility (Ignoring Gold)

- `normalized_self_agreement_rate`: higher is better (same normalized answer repeated).
- `normalized_response_uniqueness_rate`: lower is better (less variability).

| model                    |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|---------------------------------:|--------------------------------------:|
| gemma3:12b               |                            0.200 |                                 1.000 |
| llama3.1:8b              |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b |                            0.200 |                                 1.000 |

## Part 3 - Reproducibility by Model and Question

Rows at the top are least reproducible and should be inspected first.

| model                    | question_id   |   n_runs |   normalized_self_agreement_rate |   normalized_response_uniqueness_rate |
|:-------------------------|:--------------|---------:|---------------------------------:|--------------------------------------:|
| gemma3:12b               | q9980         |        5 |                            0.200 |                                 1.000 |
| llama3.1:8b              | q9980         |        5 |                            0.200 |                                 1.000 |
| medaibase/medgemma1.5:4b | q9980         |        5 |                            0.200 |                                 1.000 |

## Part 4 - Global Model Comparison (Ignoring Question ID)

This section compares model output variability across all runs/questions together.

| model                    |   total_outputs |   unique_outputs |   unique_normalized_outputs |   global_response_uniqueness_rate |   global_normalized_uniqueness_rate |
|:-------------------------|----------------:|-----------------:|----------------------------:|----------------------------------:|------------------------------------:|
| gemma3:12b               |               5 |                5 |                           5 |                             1.000 |                               1.000 |
| llama3.1:8b              |               5 |                5 |                           5 |                             1.000 |                               1.000 |
| medaibase/medgemma1.5:4b |               5 |                5 |                           5 |                             1.000 |                               1.000 |

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
| medaibase/medgemma1.5:4b |         4610.803 |              98.800 |                  24.528 |            4010.289 |                 92.000 |                     27.679 |
| llama3.1:8b              |         4871.193 |             193.800 |                  40.935 |            4442.354 |                190.000 |                     44.047 |
| gemma3:12b               |         5564.324 |             120.400 |                  23.268 |            4896.401 |                124.000 |                     26.110 |

## Reading Guide
- Use Part 1 to compare clinical answer quality versus gold.
- Use Part 2 to compare model stability across repeated runs.
- Use Part 3 to find specific unstable model/question pairs.
- Use Part 4 to compare overall model variability without question-level grouping.
- Use Part 5 to compare direct model-to-model behavioral overlap.
- Use Part 6 to compare speed and token output characteristics across models.