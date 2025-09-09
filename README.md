## Invoice Processing Bot (RPA + OCR)

An automated invoice processing solution leveraging **Python**, **OCR**, and **RPA principles** to extract key invoice data and generate structured reports efficiently. Designed to reduce manual effort, minimize errors, and provide actionable insights from invoices.

---

## Features

- **Automated OCR Processing:** Extract text from PDF invoices using Tesseract  
- **Data Extraction:** Automatically parses Vendor, Date, and Amount using regex  
- **Report Generation:** Produces `invoices.csv` (detailed) and `daily_report.csv` (summary)  
- **Supports PDF & Text Files:** Flexible input formats  
- **End-to-End Automation:** Drop invoice → OCR → parsing → CSV summary  

---

## Tech Stack

- **Python Libraries:** pandas, pdf2image, pytesseract, reportlab, PyPDF2  
- **OCR Engine:** Tesseract  
- **PDF Conversion:** Poppler  

---

## Prerequisites

- Python 3.13  
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and added to PATH  
- [Poppler](http://blog.alivate.com.au/poppler-windows/) installed and added to PATH  
- Python dependencies: run `pip install -r requirements.txt`  

---

## Installation

1. Clone the repository:

`git clone https://github.com/harrietjvazhappilly/invoice-processing-bot.git
cd invoice-processing-bot`

2.Install dependencies:
`pip install -r requirements.txt`

---

###Usage

Convert PDFs to text (OCR):
   `python src/pdf_to_txt.py`

Parse OCR text and generate reports:
   `python src/parse_ocr_invoices.py`

Check the outputs:

`reports/invoices.csv` → Detailed invoice data

`reports/daily_report.csv` → Summary per vendor

## Demo Output

## invoices.csv 

|   Vendor      |   Date    | Amount | Source       |
|---------------|-----------|--------|--------------| 
| ABC Supplies  | 09/09/2025| 150.0  | invoice1.txt | 
| XYZ Traders   | 08/09/2025| 200.0  | invoice2.txt | 

## daily_report.csv

|   Vendor     | Total_Amount | Invoice_Count |
|--------------|--------------|---------------|
| ABC Supplies |   150.0      |       1       |
| XYZ Traders  |   200.0      |       1       |

---

##Author

Harriet .J. Vazhappilly

GitHub: github.com/harrietjvazhappilly

LinkedIn: linkedin.com/in/harrietjvazhappilly

Email: harrietjvazhappilly@example.com

---







