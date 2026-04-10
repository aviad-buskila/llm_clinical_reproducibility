from __future__ import annotations

import re
from difflib import SequenceMatcher

import pandas as pd


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


def token_f1(prediction: str, gold: str) -> float:
    pred_tokens = normalize_text(prediction).split()
    gold_tokens = normalize_text(gold).split()
    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0

    pred_counts: dict[str, int] = {}
    gold_counts: dict[str, int] = {}
    for tok in pred_tokens:
        pred_counts[tok] = pred_counts.get(tok, 0) + 1
    for tok in gold_tokens:
        gold_counts[tok] = gold_counts.get(tok, 0) + 1

    common = 0
    for tok, n_pred in pred_counts.items():
        n_gold = gold_counts.get(tok, 0)
        common += min(n_pred, n_gold)

    if common == 0:
        return 0.0
    precision = common / len(pred_tokens)
    recall = common / len(gold_tokens)
    return (2 * precision * recall) / (precision + recall)


def score_deterministic(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["normalized_response"] = out["response_text"].astype(str).map(normalize_text)
    out["normalized_gold"] = out["gold_answer"].astype(str).map(normalize_text)
    out["exact_match"] = (out["response_text"].astype(str) == out["gold_answer"].astype(str)).astype(float)
    out["normalized_exact_match"] = (out["normalized_response"] == out["normalized_gold"]).astype(float)
    out["token_f1"] = [
        token_f1(pred, gold)
        for pred, gold in zip(out["response_text"].astype(str), out["gold_answer"].astype(str), strict=True)
    ]
    out["string_similarity"] = [
        SequenceMatcher(None, pred, gold).ratio()
        for pred, gold in zip(out["normalized_response"], out["normalized_gold"], strict=True)
    ]
    return out
