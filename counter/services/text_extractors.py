from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_txt(file) -> str:

    return file.read().decode("utf-8", errors="ignore")

def extract_text_from_pdf(file) -> str: #type:ignore
    reader = PdfReader(file)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

        return "\n".join(text)
    
def extract_text_from_docx(file) -> str:
    document = Document(file)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)