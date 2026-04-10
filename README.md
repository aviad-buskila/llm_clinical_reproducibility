# Ollama Clinical Reproducibility Pipeline

Evaluate multiple Ollama-hosted text models on repeated short clinical prompts, compare against gold answers, and generate reproducibility metrics plus visual reports.

## What This Pipeline Does

- Runs the same prompt many times per model (`models x prompts x runs_per_prompt`).
- Stores all raw outputs for traceability.
- Scores outputs with deterministic metrics (exact match, normalized exact match, token F1, similarity).
- Optionally applies an LLM judge rubric (also through Ollama).
- Produces aggregates, figures, and a Markdown report.

## Project Layout

- `configs/pipeline.yaml` - models, run count, generation and output settings.
- `data/questions_gold.md` - editable Markdown table containing clinical prompts and gold answers.
- `src/clinical_eval_pipeline/` - pipeline implementation.
- `outputs/` - generated artifacts (ignored by git).

## Prerequisites

- Python 3.10+
- Local Ollama server running at `http://localhost:11434`
- Required models pulled locally, e.g.:

  - `ollama pull llama3`
  - `ollama pull gemma3`
  - `ollama pull gemma4`
  - `ollama pull medgemma:1.5` (or whichever model tag you use)

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Input Data Format (Markdown Table)

Edit `data/questions_gold.md` and keep at least these required columns:

- `id`
- `question`
- `gold_answer`

Optional columns:

- `gold_keywords`
- `category`
- `notes`

## Configure Models and Runs

Edit `configs/pipeline.yaml`:

- `models`: list of Ollama model names/tags.
- `shared_instruction`: common instruction sent to all models as system guidance.
- `runs_per_prompt`: default number of repeats for every prompt/model.
- Optional per-model override: `runs_per_prompt` under each model entry.
- `judge.enabled`: enable hybrid scoring with LLM-as-judge.
- `resume`: when `true`, skip already completed stages if artifacts exist.

Prompting behavior:

- The user prompt is exactly the `question` field from `data/questions_gold.md`.
- `shared_instruction` is added separately as shared system instruction for every model call.

## Run the Pipeline

Run full pipeline:

```bash
clinical-eval all --config-path configs/pipeline.yaml
```

Resume from existing artifacts (skip completed phases):

```bash
clinical-eval all --resume
```

Or step-by-step:

```bash
clinical-eval run --config-path configs/pipeline.yaml
clinical-eval score --config-path configs/pipeline.yaml
clinical-eval report --config-path configs/pipeline.yaml
```

`--resume/--no-resume` is also supported on `run`, `score`, `report`, and `all`.
`--sample N` is supported on `run` and `all` to use only the first `N` questions from the gold file (default: all questions).

## Outputs

Generated under `outputs/`:

- `raw_responses.jsonl`, `raw_responses.csv`, `raw_responses.parquet`
- `scored_responses.csv`, `scored_responses.parquet`
- `aggregates.csv`
- `report.md`
- `figures/*.png`

## Reproducibility Notes

- Set `deterministic_mode: true` and `random_seed` in config for stable repeated runs.
- Keep `temperature: 0.0` for reduced randomness when measuring consistency.
- Record model tags explicitly (e.g., `model:version`) to avoid drift.
