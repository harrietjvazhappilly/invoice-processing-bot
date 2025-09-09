import re
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "data"        
output_file = base_dir / "reports/invoices.csv"
summary_file = base_dir / "reports/daily_report.csv"

vendor_pattern = re.compile(r"Vendor:\s*(.*)")
date_pattern = re.compile(r"(Invoice Date|Date):\s*([\d/-]+)")
amount_pattern = re.compile(r"(Total|Amount):\s*\$?([\d.]+)")

records = []

txt_files = list(data_dir.glob("*.txt"))
if not txt_files:
    raise FileNotFoundError("No OCR .txt files found in 'data/' folder.")

for txt_path in txt_files:
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    vendor = vendor_pattern.search(text)
    date = date_pattern.search(text)
    amount = amount_pattern.search(text)

    records.append({
        "Vendor": vendor.group(1).strip() if vendor else None,
        "Date": date.group(2) if date else None,
        "Amount": float(amount.group(2)) if amount else None,
        "Source": txt_path.name
    })

df = pd.DataFrame(records)

df.to_csv(output_file, index=False)
print(f"Extracted {len(df)} invoices → {output_file.name}")

if not df.empty:
    summary = df.groupby("Vendor").agg(
        Total_Amount=("Amount", "sum"),
        Invoice_Count=("Amount", "count")
    ).reset_index()

    summary.to_csv(summary_file, index=False)
    print(f"Summary report created → {summary_file.name}")
else:
    print("No invoices found.")
