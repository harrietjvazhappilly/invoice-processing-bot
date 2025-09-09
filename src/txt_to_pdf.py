from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

# Paths
data_dir = Path("../data")          # points to data folder
txt_file = data_dir / "invoice2.txt"   # your existing txt file
pdf_file = data_dir / "invoice2.pdf"   # new pdf file

# Read content from txt
with open(txt_file, "r") as f:
    content = f.read()

# Create PDF
c = canvas.Canvas(str(pdf_file), pagesize=letter)
textobject = c.beginText(40, 750)   # starting position (x=40, y=750 on page)
textobject.setFont("Helvetica", 12)

# Write each line into the PDF
for line in content.splitlines():
    textobject.textLine(line)

c.drawText(textobject)
c.save()

print(f"Converted {txt_file.name} → {pdf_file.name}")
