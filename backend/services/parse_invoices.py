import re
import pandas as pd
from pathlib import Path

# Regex patterns
vendor_pattern = re.compile(r"Vendor:\s*(.*)")
date_pattern = re.compile(r"(Invoice Date|Date):\s*([\d/-]+)")
amount_pattern = re.compile(r"(Total|Amount):\s*\$?([\d.]+)")


def extract_invoice_data(file_path: str):
    file = Path(file_path)

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    vendor = vendor_pattern.search(text)
    date = date_pattern.search(text)
    amount = amount_pattern.search(text)

    return {
        "Vendor": vendor.group(1).strip() if vendor else None,
        "Date": date.group(2) if date else None,
        "Amount": float(amount.group(2)) if amount else None,
        "Source": file.name
    }


def generate_reports(records: list, reports_folder: str):

    reports_path = Path(reports_folder)
    reports_path.mkdir(exist_ok=True)

    output_file = reports_path / "invoices.csv"
    summary_file = reports_path / "daily_report.csv"

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)

    if not df.empty:
        summary = df.groupby(["Vendor", "Date"]).agg(
            Total_Amount=("Amount", "sum"),
            Invoice_Count=("Amount", "count")
        ).reset_index()

        summary.to_csv(summary_file, index=False)
    else:
        pd.DataFrame(columns=["Vendor", "Date", "Total_Amount", "Invoice_Count"]).to_csv(
            summary_file, index=False
        )

    return {
        "detailed_report": str(output_file),
        "summary_report": str(summary_file)
    }
