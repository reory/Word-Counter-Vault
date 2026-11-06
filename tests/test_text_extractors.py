from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from hypothesis import given
from hypothesis import strategies as st

from counter.services.text_extractors import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_txt,
    get_text_from_uploaded_file,
)


def test_extract_text_from_txt():
    """Verify plain text is decoded correctly."""

    uploaded = SimpleUploadedFile(
        "test.txt",
        b"hello world",
        content_type="text/plain",
    )

    assert extract_text_from_txt(uploaded) == "hello world"


@patch("counter.services.text_extractors.PdfReader")
def test_extract_text_from_pdf(mock_reader):
    """Verify text is extracted from PDF pages."""

    page = Mock()
    page.extract_text.return_value = "Hello PDF"

    mock_reader.return_value.pages = [page]

    result = extract_text_from_pdf(Mock())

    assert result == "Hello PDF"


@patch("counter.services.text_extractors.PdfReader")
def test_extract_text_from_pdf_ignores_empty_pages(mock_reader):
    """Verify blank PDF pages are ignored."""

    page = Mock()
    page.extract_text.return_value = None

    mock_reader.return_value.pages = [page]

    result = extract_text_from_pdf(Mock())

    assert result == ""


@patch("counter.services.text_extractors.Document")
def test_extract_text_from_docx(mock_document):
    """Verify paragraph text is extracted from Word documents."""

    p1 = Mock(text="First paragraph")
    p2 = Mock(text="Second paragraph")

    mock_document.return_value.paragraphs = [p1, p2]

    result = extract_text_from_docx(Mock())

    assert result == "First paragraph\nSecond paragraph"


@patch("counter.services.text_extractors.Document")
def test_extract_text_from_docx_skips_empty_paragraphs(mock_document):
    """Verify empty paragraphs are ignored."""

    p1 = Mock(text="First paragraph")
    p2 = Mock(text="")
    p3 = Mock(text="   ")

    mock_document.return_value.paragraphs = [p1, p2, p3]

    result = extract_text_from_docx(Mock())

    assert result == "First paragraph"


@given(st.text())
def test_extract_text_from_txt_hypothesis(text):
    """Verify text extraction never corrupts UTF-8 text."""

    uploaded = SimpleUploadedFile(
        "test.txt",
        text.encode("utf-8"),
        content_type="text/plain",
    )

    assert get_text_from_uploaded_file(uploaded) == text