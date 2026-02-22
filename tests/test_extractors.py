import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from counter.services.text_extractors import get_text_from_uploaded_file

def test_extract_text_from_simple_text():

    # Create a fake .txt file with some content.
    file_content = b"Hello, this is a test for the word counter."
    fake_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

    # Run the service function.
    extracted_text = get_text_from_uploaded_file(fake_file)

    # Assertions
    assert extracted_text is not None
    assert "word counter" in extracted_text

def test_extract_text_from_unsupported_file():

    # Create a fake image file.
    fake_file = SimpleUploadedFile(
        'virus.exe', 
        b'fake_binary_data', content_type='application/x-msdownload'
    )

    extracted_text = get_text_from_uploaded_file(fake_file)

    # This confirms the else logic in the view will trigger correctly.
    assert extracted_text == '' or extracted_text is None
