from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["question", "answer"]


def load_gold_csv(path: str | Path) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Gold data CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Gold data CSV missing required columns: {missing}. "
            f"Required: {REQUIRED_COLUMNS}"
        )

    out = pd.DataFrame(
        {
            "id": [f"q{i + 1}" for i in range(len(df))],
            "question": df["question"].astype(str),
            "gold_answer": df["answer"].astype(str),
            "category": "",
        }
    )
    return out
