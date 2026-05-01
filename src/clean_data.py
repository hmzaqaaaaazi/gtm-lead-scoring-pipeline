import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "crunchbase.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "crunchbase_clean.csv")

COLUMN_MAP = {
    "identifier-label": "company_name",
    "accent 7": "city",
    "accent 8": "state",
    "component--field-formatter 3": "funding_stage",
    "component--field-formatter 4": "last_funding_date",
    "component--field-formatter 9": "estimated_revenue",
    "component--field-formatter 12": "operating_status",
    "component--field-formatter 17": "website",
    "component--field-formatter 24": "full_description",
    "component--field-formatter 28": "employee_range",
    "ng-star-inserted 2": "contact_email",
    "accent 18": "founder_name",
}

INDUSTRY_COLS = [
    "accent 4", "accent 5", "accent 6",
    "accent 10", "accent 11", "accent 12", "accent 13", "accent 19",
]

df = pd.read_csv(INPUT_PATH, low_memory=False)
print(f"Rows before cleaning: {len(df)}")

def combine_industries(row):
    parts = []
    for col in INDUSTRY_COLS:
        val = str(row.get(col, "")).strip()
        if val and val not in ("nan", "—", "-", "–"):
            parts.append(val)
    seen = []
    for p in parts:
        if p not in seen:
            seen.append(p)
    return ", ".join(seen)

df["industries"] = df.apply(combine_industries, axis=1)

keep_cols = list(COLUMN_MAP.keys()) + ["industries"]
df = df[keep_cols].rename(columns=COLUMN_MAP)

def clean_str_col(series):
    return (
        series.astype(str)
        .str.strip()
        .replace(r"^\s*[—–-]\s*$", "", regex=True)
        .replace("nan", "")
    )

for col in df.columns:
    if col != "industries":
        df[col] = clean_str_col(df[col])

df = df[df["company_name"].str.strip().ne("")]
df = df.drop_duplicates(subset="company_name", keep="first")

df["funding_stage"] = df["funding_stage"].str.strip().str.title()
df["state"] = df["state"].str.strip().str.title()

print(f"Rows after cleaning:  {len(df)}")
print(f"\nShape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head().to_string())

df.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved to {OUTPUT_PATH}")
