from counter.services.quality_insights import (
    analyse_quality,
    count_syllables,
    get_basic_metrics,
)


def test_count_syllables_short_word():
    """Verify short words are treated as a single syllable."""

    assert count_syllables("cat") == 1


def test_count_syllables_common_word():
    """Verify common multi-syllable words are counted correctly."""

    assert count_syllables("testing") >= 2


def test_count_syllables_multiple_syllables():
    """Verify words with multiple syllables return a value greater than one."""

    assert count_syllables("computer") >= 2


def test_count_syllables_never_returns_zero():
    """Verify the function always returns at least one syllable."""

    assert count_syllables("") == 1


def test_get_basic_metrics():
    """Verify basic text statistics and reading time are calculated."""

    text = "Hello World.\n\nThis is a test."

    result = get_basic_metrics(text)

    assert result["word_count"] == 6
    assert result["sentence_count"] == 2
    assert result["paragraph_count"] == 2
    assert result["reading_time"] == 1


def test_analyse_quality_empty_text():
    """Verify empty text returns default readability metrics."""

    result = analyse_quality("")

    assert result["longest_sentence"] == ""
    assert result["ttr"] == 0
    assert result["passive_count"] == 0
    assert result["flesch_score"] == 0.0
    assert result["gunning_fog"] == 0.0


def test_analyse_quality_longest_sentence():
    """Verify the longest sentence is correctly identified."""

    text = (
        "Short sentence. "
        "This is a longer sentence than the first one up above."
    )

    result = analyse_quality(text)

    assert result["longest_sentence"].startswith(
        "This is a longer sentence than the first one up above."
    )


def test_analyse_quality_ttr():
    """Verify type-token ratio is calculated correctly."""

    text = "apple apple banana"

    result = analyse_quality(text)

    assert result["ttr"] == 0.667


def test_analyse_quality_overused_words():
    """Verify frequently repeated words are detected as overused."""

    text = ("python python python python python hello code code")

    result = analyse_quality(text)

    assert ("python", 5) in result["overused"]


def test_analyse_quality_passive_voice():
    """Verify passive voice patterns are identified and counted."""

    text = "The report was completed. The task was finished."

    result = analyse_quality(text)

    assert result["passive_count"] == 2