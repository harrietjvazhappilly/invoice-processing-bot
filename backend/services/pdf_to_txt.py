from pathlib import Path
import pytesseract
from pdf2image import convert_from_path

def pdf_to_text(pdf_path: str):

    pdf_path = Path(pdf_path)
    txt_output = pdf_path.with_suffix(".txt")

    images = convert_from_path(pdf_path)

    full_text = ""

    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"

    with open(txt_output, "w", encoding="utf-8") as f:
        f.write(full_text)

    return str(txt_output)