from counter.services.comparisons import compare_texts, get_comparison_insights


def test_reports_text_a_has_greater_lexical_diversity():
    """Text A should be identified as having greater lexical diversity."""

    # Text A has the higher TTR score.
    quality_a = {
        "ttr": 0.8,
        "passive_count": 2,
        "flesch_score": 50,
    }

    quality_b = {
        "ttr": 0.4,
        "passive_count": 2,
        "flesch_score": 50,
    }

    insights = get_comparison_insights(quality_a, quality_b)

    assert "Text A shows greater lexical diversity." in insights


def test_reports_text_b_has_greater_lexical_diversity():
    """Text B should be identified as having greater lexical diversity."""

    # Text B has the higher TTR score.
    quality_a = {
        "ttr": 0.4,
        "passive_count": 2,
        "flesch_score": 50,
    }

    quality_b = {
        "ttr": 0.8,
        "passive_count": 2,
        "flesch_score": 50,
    }

    insights = get_comparison_insights(quality_a, quality_b)

    assert "Text B shows greater lexical diversity." in insights


def test_reports_text_a_uses_less_passive_voice():
    """Text A should be flagged as using less passive voice."""

    # Lower passive voice count should be preferred.
    quality_a = {
        "ttr": 0.5,
        "passive_count": 1,
        "flesch_score": 50,
    }

    quality_b = {
        "ttr": 0.5,
        "passive_count": 5,
        "flesch_score": 50,
    }

    insights = get_comparison_insights(quality_a, quality_b)

    assert "Text A uses less passive voice." in insights


def test_compare_texts_returns_expected_structure(monkeypatch):
    """Compare two texts and return a complete comparison payload."""

    # Mock baseline metrics generation.
    monkeypatch.setattr(
        "counter.services.comparisons.get_basic_metrics",
        lambda text: {"word_count": 3},
    )

    # Mock quality analysis.
    monkeypatch.setattr(
        "counter.services.comparisons.analyse_quality",
        lambda text: {
            "ttr": 0.5,
            "passive_count": 1,
            "flesch_score": 60,
        },
    )

    # Mock summary generation.
    monkeypatch.setattr(
        "counter.services.comparisons.generate_summary",
        lambda text: "Mock summary",
    )

    # Mock vocabulary extraction.
    def mock_frequencies(text, limit=2000):
        if text == "text a":
            return [("python", 2), ("django", 1)]

        return [("python", 1), ("pytest", 1)]

    monkeypatch.setattr(
        "counter.services.comparisons.get_word_frequencies",
        mock_frequencies,
    )

    result = compare_texts(
        "text a",
        "text b",
    )

    # Verify top-level sections exist.
    assert "text_a" in result
    assert "text_b" in result
    assert "comparison" in result

    # Verify shared vocabulary.
    assert result["comparison"]["shared_words"] == ["python"]

    # Verify unique vocabulary.
    assert result["comparison"]["unique_to_a"] == ["django"]
    assert result["comparison"]["unique_to_b"] == ["pytest"]

    # Verify overlap percentage is calculated.
    assert result["comparison"]["vocabulary_overlap"] == 33.33


def test_compare_texts_returns_zero_overlap_for_empty_vocab(monkeypatch):
    """Return zero overlap when neither text contains vocabulary."""

    # Mock baseline metrics to isolate comparison logic.
    monkeypatch.setattr(
        "counter.services.comparisons.get_basic_metrics",
        lambda text: {},
    )

    # Mock quality analysis with neutral values.
    monkeypatch.setattr(
        "counter.services.comparisons.analyse_quality",
        lambda text: {
            "ttr": 0,
            "passive_count": 0,
            "flesch_score": 0,
        },
    )

    # Mock summary generation.
    monkeypatch.setattr(
        "counter.services.comparisons.generate_summary",
        lambda text: "",
    )

    # Return an empty vocabulary for both texts.
    monkeypatch.setattr(
        "counter.services.comparisons.get_word_frequencies",
        lambda text, limit=2000: [],
    )

    # Compare two empty text submissions.
    result = compare_texts("", "")

    # Ensure division-by-zero protection returns 0.0%.
    assert result["comparison"]["vocabulary_overlap"] == 0.0