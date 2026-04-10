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


def _bleu_score(normalized_pred: str, normalized_gold: str) -> float:
    from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

    pred_tokens = normalized_pred.split()
    gold_tokens = normalized_gold.split()
    if not pred_tokens or not gold_tokens:
        return 0.0
    smoother = SmoothingFunction().method1
    return float(sentence_bleu([gold_tokens], pred_tokens, smoothing_function=smoother))


def _rouge_l_f1(normalized_pred: str, normalized_gold: str) -> float:
    from rouge_score import rouge_scorer

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    score = scorer.score(normalized_gold, normalized_pred)["rougeL"]
    return float(score.fmeasure)


def _bert_scores(
    predictions: list[str],
    references: list[str],
    model_type: str,
    batch_size: int,
) -> tuple[list[float], list[float], list[float]]:
    from bert_score import score as bertscore_score

    p_tensor, r_tensor, f1_tensor = bertscore_score(
        predictions,
        references,
        model_type=model_type,
        lang="en",
        verbose=False,
        batch_size=batch_size,
    )
    return (
        [float(x) for x in p_tensor.tolist()],
        [float(x) for x in r_tensor.tolist()],
        [float(x) for x in f1_tensor.tolist()],
    )


def score_deterministic(
    df: pd.DataFrame,
    bertscore_model: str = "roberta-base",
    bertscore_batch_size: int = 8,
) -> pd.DataFrame:
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
    out["bleu"] = [
        _bleu_score(pred, gold)
        for pred, gold in zip(out["normalized_response"], out["normalized_gold"], strict=True)
    ]
    out["rouge_l"] = [
        _rouge_l_f1(pred, gold)
        for pred, gold in zip(out["normalized_response"], out["normalized_gold"], strict=True)
    ]

    bert_p, bert_r, bert_f1 = _bert_scores(
        out["response_text"].astype(str).tolist(),
        out["gold_answer"].astype(str).tolist(),
        model_type=bertscore_model,
        batch_size=bertscore_batch_size,
    )
    out["bertscore_precision"] = bert_p
    out["bertscore_recall"] = bert_r
    out["bertscore_f1"] = bert_f1
    return out
