from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "data"

pdf_files = list(data_dir.glob("*.pdf"))
if not pdf_files:
    raise FileNotFoundError("No PDF files found in 'data' folder.")

for pdf_path in pdf_files:
    print(f" Processing {pdf_path.name}...")

    pages = convert_from_path(str(pdf_path), poppler_path=r"C:\Users\user\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin")
    print(f"Converted {len(pages)} pages")

    all_text = ""
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page)
        all_text += f"\n---- Page {i} ----\n{text}\n"

    txt_path = pdf_path.with_suffix(".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"Saved OCR text → {txt_path.name}")

print("All PDFs processed!")
