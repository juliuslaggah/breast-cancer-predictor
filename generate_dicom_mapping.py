# generate_dicom_mapping.py

import json
import os
from pathlib import Path
import pandas as pd

# Load your true patient IDs from data.csv
df = pd.read_csv("data/data.csv")
true_ids = df["id"].astype(str).tolist()

mapping = {}

# Process dicom/train and dicom/test folders
for split in ("train", "test"):
    base = Path("dicom") / split
    if not base.exists():
        print(f"[ERROR] DICOM folder not found: {base}")
        continue

    for folder in os.listdir(base):
        folder_path = base / folder
        if not folder_path.is_dir():
            continue

        try:
            idx = int(folder)
        except ValueError:
            print(f"[WARN] Skipping non-numeric folder: {folder}")
            continue

        if idx < len(true_ids):
            patient_id = true_ids[idx]
            # Convert path to POSIX-style for cross-platform consistency
            mapping[patient_id] = f"{split}/{folder}"
        else:
            print(f"[WARN] No CSV ID for DICOM folder {split}/{folder} (index {idx})")

# Write the mapping
with open("dicom_mapping.json", "w") as f:
    json.dump(mapping, f, indent=2)

print(f"✅ Written new dicom_mapping.json with {len(mapping)} entries.")
