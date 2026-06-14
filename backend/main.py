from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from pathlib import Path
import logging

# Import your services
from services.parse_invoices import extract_invoice_data
from services.pdf_to_txt import pdf_to_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Invoice Processing Bot")

# CORS - Allow Vercel frontend
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://invoice-bot-frontend-xyz.vercel.app"  # Update with YOUR Vercel URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = Path("uploads")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ============ ENDPOINTS ============

@app.get("/")
async def health_check():
    """Health check"""
    return {"status": "ok", "message": "Invoice Bot API is running"}

@app.post("/process-invoice/")
async def process_invoice(file: UploadFile = File(...)):
    """Process invoice (PDF or TXT)"""
    try:
        # Validate file
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(status_code=400, detail="Only PDF and TXT allowed")
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded: {file.filename}")
        
        # Process based on type
        text_content = ""
        if file.content_type == "application/pdf":
            try:
                text_content = pdf_to_text(str(file_path))
            except Exception as e:
                logger.error(f"PDF error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")
        else:
            with open(file_path, "r") as f:
                text_content = f.read()
        
        # Extract data
        invoice_data = extract_invoice_data(text_content)
        
        return {
            "status": "success",
            "filename": file.filename,
            "data": invoice_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/invoices/")
async def get_invoices():
    """Get processed invoices"""
    try:
        csv_path = REPORTS_DIR / "invoices.csv"
        if not csv_path.exists():
            return {"invoices": [], "message": "No invoices yet"}
        
        import pandas as pd
        df = pd.read_csv(csv_path)
        return {"status": "success", "invoices": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-report/{report_name}")
async def download_report(report_name: str):
    """Download CSV report"""
    try:
        report_path = REPORTS_DIR / report_name
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        return FileResponse(
            path=report_path,
            filename=report_name,
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)