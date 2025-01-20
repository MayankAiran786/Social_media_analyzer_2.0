from PIL import Image
import pytesseract
import io  # Import the 'io' module

def perform_ocr(image_bytes):
    """Performs OCR on an image."""
    try:
        img = Image.open(io.BytesIO(image_bytes))  # Use io.BytesIO() to create an in-memory file
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return None