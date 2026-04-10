from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["id", "question", "gold_answer"]
OPTIONAL_COLUMNS = ["gold_keywords", "category", "notes"]


def _parse_markdown_table(md_text: str) -> list[dict[str, str]]:
    lines = [ln.strip() for ln in md_text.splitlines() if ln.strip()]
    table_lines = [ln for ln in lines if ln.startswith("|") and ln.endswith("|")]
    if len(table_lines) < 2:
        raise ValueError("No markdown table found. Expected header and rows.")

    headers = [h.strip() for h in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []

    for ln in table_lines[2:]:
        parts = [p.strip() for p in ln.strip("|").split("|")]
        if len(parts) != len(headers):
            raise ValueError(f"Malformed markdown row: {ln}")
        rows.append(dict(zip(headers, parts, strict=True)))

    return rows


def load_questions_markdown(path: str | Path) -> pd.DataFrame:
    md_path = Path(path)
    if not md_path.exists():
        raise FileNotFoundError(f"Question markdown file not found: {md_path}")

    text = md_path.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text)
    df = pd.DataFrame(rows)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Markdown table missing required columns: {missing}. "
            f"Required: {REQUIRED_COLUMNS}"
        )

    selected_cols = REQUIRED_COLUMNS + [c for c in OPTIONAL_COLUMNS if c in df.columns]
    df = df[selected_cols].copy()
    df["id"] = df["id"].astype(str)
    df["question"] = df["question"].astype(str)
    df["gold_answer"] = df["gold_answer"].astype(str)

    if df["id"].duplicated().any():
        dupes = df.loc[df["id"].duplicated(), "id"].tolist()
        raise ValueError(f"Duplicate question ids found: {dupes}")

    return df
