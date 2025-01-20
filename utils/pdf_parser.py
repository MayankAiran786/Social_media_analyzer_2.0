from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_bytes):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PdfReader(pdf_bytes)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None