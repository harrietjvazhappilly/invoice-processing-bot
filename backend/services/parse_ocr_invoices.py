import re
import pandas as pd
from pathlib import Path

# Regex patterns
vendor_pattern = re.compile(r"Vendor:\s*(.*)")
date_pattern = re.compile(r"(Invoice Date|Date):\s*([\d/-]+)")
amount_pattern = re.compile(r"(Total|Amount):\s*\$?([\d.]+)")

def parse_invoices(file_path: str):

    txt_path = Path(file_path)

    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    vendor = vendor_pattern.search(text)
    date = date_pattern.search(text)
    amount = amount_pattern.search(text)

    record = {
        "Vendor": vendor.group(1).strip() if vendor else None,
        "Date": date.group(2) if date else None,
        "Amount": float(amount.group(2)) if amount else None,
        "Source": txt_path.name
    }

    return record
