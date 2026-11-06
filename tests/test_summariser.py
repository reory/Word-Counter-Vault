from hypothesis import given
from hypothesis import strategies as st

from counter.services.summariser import generate_summary


def test_generate_summary_empty_text():
    """Verify empty input returns empty summary data."""

    result = generate_summary("")

    assert result["summary"] == ""
    assert result["bullets"] == []
    assert result["topics"] == []


def test_generate_summary_uses_first_two_sentences():
    """Verify the summary contains the first two sentences."""

    text = (
        "Sentence one. "
        "Sentence two. "
        "Sentence three."
    )

    result = generate_summary(text)

    assert result["summary"] == "Sentence one. Sentence two."


def test_generate_summary_generates_bullets():
    """Verify bullet points contain the first four sentences."""

    text = (
        "One. "
        "Two. "
        "Three. "
        "Four. "
        "Five."
    )

    result = generate_summary(text)

    assert result["bullets"] == [
        "One.",
        "Two.",
        "Three.",
        "Four.",
    ]


def test_generate_summary_extracts_topics():
    """Verify common non-stop words are extracted as topics."""

    text = (
        "python python python "
        "django django "
        "testing coverage"
    )

    result = generate_summary(text)

    assert "python" in result["topics"]
    assert "django" in result["topics"]





@given(st.text())
def test_generate_summary_returns_expected_structure(text):
    """Verify summary generation always returns the expected keys."""

    result = generate_summary(text)

    assert isinstance(result, dict)

    assert "summary" in result
    assert "bullets" in result
    assert "topics" in result