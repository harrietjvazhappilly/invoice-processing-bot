# Invoice Processing Bot

An invoice processing web app built with a **FastAPI backend** and a simple **HTML/CSS/JavaScript frontend**. The app accepts invoice uploads, extracts important invoice details, and generates CSV reports automatically.

## Features

- Upload invoice files from a browser UI
- Supports `.txt` invoice files
- Supports `.pdf` invoice files using OCR
- Saves uploaded files into `backend/uploads`
- Converts PDF invoices into text using `pdf2image` and `pytesseract`
- Extracts invoice details using regex:
  - Vendor
  - Date
  - Amount
  - Source file name
- Stores processed invoice records temporarily in memory
- Generates detailed invoice report:
  - `backend/reports/invoices.csv`
- Generates summary report:
  - `backend/reports/daily_report.csv`
- Provides FastAPI endpoints for processing invoices, viewing processed records, and checking report paths

## Tech Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn
- Pandas
- pdf2image
- pytesseract
- PyPDF2
- reportlab
- python-multipart

### OCR Requirements

PDF invoice processing requires:

- Tesseract OCR
- Poppler

Text invoice processing works without OCR system tools.

## Project Structure

```text
invoice-processing-bot/
|-- backend/
|   |-- main.py
|   |-- requirements.txt
|   |-- data/
|   |-- reports/
|   |   |-- invoices.csv
|   |   `-- daily_report.csv
|   |-- services/
|   |   |-- parse_invoices.py
|   |   |-- parse_ocr_invoices.py
|   |   |-- pdf_to_txt.py
|   |   `-- __init__.py
|   `-- uploads/
|-- frontend/
|   `-- index.html
`-- README.md
```

## Backend Functions

### `backend/main.py`

Creates the FastAPI application and exposes the API endpoints.

Available endpoints:

```text
GET /
```

Health check endpoint. Returns a message confirming the API is running.

```text
POST /process-invoice/
```

Accepts an uploaded `.txt` or `.pdf` invoice file.

Process:

1. Saves the uploaded file into `backend/uploads`
2. Converts PDF to text if the uploaded file is a PDF
3. Extracts invoice data
4. Adds the extracted record to temporary memory
5. Regenerates CSV reports
6. Returns the extracted invoice data and report paths

```text
GET /invoices/
```

Returns all invoice records processed during the current server session.

```text
GET /reports/
```

Returns the file paths for the generated reports.

### `backend/services/parse_invoices.py`

Contains invoice parsing and report generation logic.

Functions:

```python
parse_single_invoice(file_path: str)
```

Reads a text invoice and extracts:

- Vendor
- Date
- Amount
- Source

```python
generate_reports(records: list, reports_folder: str)
```

Creates two CSV reports:

- `invoices.csv`: detailed invoice records
- `daily_report.csv`: grouped report by vendor and date

### `backend/services/pdf_to_txt.py`

Contains PDF OCR conversion logic.

Function:

```python
convert_pdf_to_text(pdf_path: str)
```

Converts a PDF invoice into a `.txt` file using:

- `pdf2image`
- `pytesseract`

### `backend/services/parse_ocr_invoices.py`

Contains an additional invoice parsing function for OCR-generated text files.

Function:

```python
parse_invoices(file_path: str)
```

Extracts Vendor, Date, Amount, and Source from a text file.

## Frontend Function

### `frontend/index.html`

Provides the browser interface for users.

The UI allows users to:

- Choose a `.txt` or `.pdf` invoice file
- Upload it to the FastAPI backend
- View extracted invoice details in a table

The frontend sends requests to the backend using:

```javascript
fetch(`${apiBaseUrl}/process-invoice/`, {
  method: "POST",
  body: formData
});
```

Update this line if your backend port or live backend URL changes:

```javascript
const apiBaseUrl = "http://127.0.0.1:8001";
```

## Installation

Open a terminal in the project folder:

```powershell
cd "C:\Users\user\OneDrive\Desktop\invoice-processing-bot"
```

Install dependencies:

```powershell
pip install -r backend\requirements.txt
```

## Running The Project Locally

Start the backend server:

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

Open the backend health check:

```text
http://127.0.0.1:8001/
```

Expected response:

```json
{
  "status": "running",
  "message": "Invoice Processing API is ready"
}
```

Open the frontend UI:

```text
frontend/index.html
```

You can open it by double-clicking the file or running:

```powershell
start frontend\index.html
```

## How To Use

1. Start the FastAPI backend.
2. Open `frontend/index.html` in a browser.
3. Choose a `.txt` or `.pdf` invoice file.
4. Click **Process Invoice**.
5. View extracted invoice details in the table.
6. Check generated CSV reports in `backend/reports`.

## Generated Reports

### `backend/reports/invoices.csv`

Detailed invoice records.

Example:

```csv
Vendor,Date,Amount,Source
ABC Supplies,22/08/2025,245.6,invoice1.txt
XYZ Traders,23/08/2025,1120.0,invoice2.txt
```

### `backend/reports/daily_report.csv`

Summary grouped by vendor and date.

Example:

```csv
Vendor,Date,Total_Amount,Invoice_Count
ABC Supplies,22/08/2025,245.6,1
XYZ Traders,23/08/2025,1120.0,1
```

## Deployment Notes

Recommended deployment setup:

- Deploy frontend on Vercel
- Deploy backend on Render, Railway, or another Python backend hosting service

For backend deployment, use:

```text
Build Command:
pip install -r backend/requirements.txt

Start Command:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

After deploying the backend, update `apiBaseUrl` in `frontend/index.html`:

```javascript
const apiBaseUrl = "https://your-backend-url.com";
```

PDF OCR deployment may require extra server setup for Tesseract OCR and Poppler.

## Author

Harriet J. Vazhappilly

GitHub: https://github.com/harrietjvazhappilly

Email:

- harrietjvazhappilly@gmail.com
- 24ct245@mgits.ac.in
