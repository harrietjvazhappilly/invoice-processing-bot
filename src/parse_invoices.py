import re
import pandas as pd
from pathlib import Path

input_folder = Path("../data")      
output_file = Path("../reports/invoices.csv")
summary_file = Path("../reports/daily_report.csv")

vendor_pattern = re.compile(r"Vendor:\s*(.*)")
date_pattern = re.compile(r"(Invoice Date|Date):\s*([\d/-]+)")
amount_pattern = re.compile(r"(Total|Amount):\s*\$?([\d.]+)")
records = []

for file in input_folder.glob("*.txt"):  
    with open(file, "r") as f:
        text = f.read()
    
    vendor = vendor_pattern.search(text)
    date = date_pattern.search(text)
    amount = amount_pattern.search(text)

    records.append({
        "Vendor": vendor.group(1).strip() if vendor else None,
        "Date": date.group(2) if date else None,
        "Amount": float(amount.group(2)) if amount else None,
        "Source": file.name
    })

df = pd.DataFrame(records)
df.to_csv(output_file, index=False)

if not df.empty:
    summary = df.groupby(["Vendor","Date"]).agg(
        Total_Amount=("Amount", "sum"),
        Invoice_Count=("Amount", "count")
    ).reset_index()

    summary.to_csv(summary_file, index=False)
    print(f" Extracted {len(df)} invoices → {output_file}")
    print(f" Summary report created → {summary_file}")
else:
    print(" No invoices found in data/")