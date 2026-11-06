from io import BytesIO
from unittest.mock import Mock, patch

from counter.services.exporters import (
    generate_docx_report,
    generate_pdf_report,
    generate_word_frequency_chart_image,
    get_export_data,
)


def test_get_export_data_uses_session_data():
    """Verify export data falls back to session storage."""

    session = {
        "analysis_text": "Hello World",
        "summary": "Summary text",
        "word_count": 2,
    }

    result = get_export_data(
        user=None,
        session=session,
    )

    assert result["text"] == "Hello World"
    assert result["summary"] == "Summary text"
    assert result["word_count"] == 2


def test_get_export_data_handles_none_session():
    """Verify missing session data is handled safely."""

    result = get_export_data(
        user=None,
        session=None,
    )

    assert result["text"] is None


@patch("counter.services.exporters.word_selectors.get_record_for_user")
def test_get_export_data_from_record(mock_record):
    """Verify export data is populated from a saved record."""

    record = Mock()

    record.original_text = "Text"
    record.summary = "Summary"
    record.topics = ["python"]

    record.word_count = 10
    record.bullets = []
    record.longest_sentence = "Long sentence"

    record.ttr = 0.5
    record.overused = []
    record.passive_count = 0

    record.flesch_score = 75.0
    record.gunning_fog = 8.0

    mock_record.return_value = record

    result = get_export_data(
        user="user",
        pk=1,
    )

    assert result["text"] == "Text"
    assert result["summary"] == "Summary"


@patch("counter.services.exporters.HTML")
@patch("counter.services.exporters.render_to_string")
@patch("counter.services.exporters.get_word_frequencies")
def test_generate_pdf_report(
    mock_freq,
    mock_render,
    mock_html,
):
    """Verify PDF reports are generated."""

    mock_freq.return_value = [("python", 5)]

    mock_render.return_value = "<html></html>"

    mock_html.return_value.write_pdf.return_value = b"pdf"

    result = generate_pdf_report(
        {"text": "python python"}
    )

    assert result == b"pdf"


@patch("counter.services.exporters.HTML")
@patch("counter.services.exporters.render_to_string")
def test_generate_pdf_report_without_text(
    mock_render,
    mock_html,
):
    """Verify PDF generation works without source text."""

    mock_render.return_value = "<html></html>"
    mock_html.return_value.write_pdf.return_value = b"pdf"

    result = generate_pdf_report({})

    assert result == b"pdf"



@patch("counter.services.exporters.get_word_frequencies")
def test_generate_word_frequency_chart_image(
    mock_freq,
):
    """Verify chart images are generated."""

    mock_freq.return_value = [
        ("python", 5),
        ("django", 3),
    ]

    result = generate_word_frequency_chart_image(
        "python django"
    )

    assert result is not None
    assert result.getbuffer().nbytes > 0


@patch(
    "counter.services.exporters.generate_word_frequency_chart_image"
)
@patch("counter.services.exporters.Document")
def test_generate_docx_report(
    mock_document,
    mock_chart,
):
    """Verify Word reports are generated."""

    doc = Mock()
    doc.paragraphs = [Mock()]

    mock_document.return_value = doc
    mock_chart.return_value = BytesIO(b"chart")

    result = generate_docx_report(
        {
            "text": "sample",
            "summary": "summary",
            "word_count": 5,
            "bullets": ["one"],
            "overused": [("python", 4)],
        }
    )

    assert result is not None

    doc.add_heading.assert_called()


@patch(
    "counter.services.exporters.generate_word_frequency_chart_image"
)
@patch("counter.services.exporters.Document")
def test_generate_docx_report_without_overused_words(
    mock_document,
    mock_chart,
):
    """Verify empty overused-word lists are handled."""

    doc = Mock()
    doc.paragraphs = [Mock()]

    mock_document.return_value = doc
    mock_chart.return_value = BytesIO(b"chart")

    generate_docx_report(
        {
            "text": "sample",
            "overused": [],
        }
    )

    doc.add_paragraph.assert_any_call(
        "No significant overused detected."
    )