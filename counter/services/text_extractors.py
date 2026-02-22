from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_txt(file) -> str:
    
    # Read the raw file bytes, then convert them into a readable string.
    return file.read().decode("utf-8", errors="ignore")

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = []
    
    # Loop through every page in the PDF document.
    for page in reader.pages:
        page_text = page.extract_text()
        # Save the page to the [] list if the page contains text.
        if page_text:
            text.append(page_text)

    return "\n".join(text)
    
def extract_text_from_docx(file) -> str:
    """Pull plain text from a Word document."""

    # Load the uploaded file into a Word document object.
    document = Document(file)
    # Extract text from each paragraph, Skip any that are empty or have spaces.
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    # # Merge the list of paragrapns into a string, seperated by newlines.
    return "\n".join(paragraphs)

def get_text_from_uploaded_file(uploaded_file):
    """Acts as a central gateway to extract text regardless of file type"""

    filename = uploaded_file.name.lower()

    if filename.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    elif filename.endswith('pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith('docx'):
        return extract_text_from_docx(uploaded_file)
    
    return None # Returns None if the file type is not supported.
    