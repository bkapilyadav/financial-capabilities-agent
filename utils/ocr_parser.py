from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def extract_text_from_file(uploaded_file):
    text_list = []

    try:
        # If PDF
        if uploaded_file.type == "application/pdf":
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    text = page.get_text()
                    if text.strip():
                        text_list.append(text)
        else:
            # If Image
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            text_list.append(text)

    except Exception as e:
        text_list.append(f"[OCR Error]: {str(e)}")

    return text_list
