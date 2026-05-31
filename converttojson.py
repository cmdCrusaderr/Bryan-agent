import pandas as pd
import os
import glob

# Find all CSVs in the data folder
csv_files = glob.glob("data/*.csv")

for file in csv_files:
    # Read the CSV
    df = pd.read_csv(file)
    # Convert and save as JSONL
    new_filename = file.replace('.csv', '.jsonl')
    df.to_json(new_filename, orient='records', lines=True)
    print(f"Converted {file} -> {new_filename}")

print("\n✅ All data optimized to enterprise JSONL format!")