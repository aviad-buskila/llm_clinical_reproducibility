from clinical_eval_pipeline.scoring.deterministic import normalize_text, token_f1


def test_normalize_text_basic_rules() -> None:
    text = " Hello, WORLD!!  Celiac-disease\t\n"
    normalized = normalize_text(text)
    assert normalized == "hello world celiacdisease"


def test_token_f1_identical_is_one() -> None:
    assert token_f1("ibuprofen reduces pain", "ibuprofen reduces pain") == 1.0


def test_token_f1_no_overlap_is_zero() -> None:
    assert token_f1("ibuprofen", "celiac") == 0.0
