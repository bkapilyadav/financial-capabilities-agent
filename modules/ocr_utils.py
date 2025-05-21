import pytesseract
from PIL import Image
import fitz  # PyMuPDF

def extract_text_from_image(uploaded_file):
    img = Image.open(uploaded_file)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(uploaded_pdf):
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
