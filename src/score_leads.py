import pandas as pd
import os
from dateutil import parser as dateparser
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH  = os.path.join(BASE_DIR, "data",   "crunchbase_clean.csv")
OUT_ALL     = os.path.join(BASE_DIR, "output", "scored_companies.csv")
OUT_TIER1   = os.path.join(BASE_DIR, "output", "top_tier1_companies.csv")

TODAY = date(2026, 4, 30)

# ── Funding stage (25 pts) ────────────────────────────────────────────────────
STAGE_SCORES = {
    "Series B": 25,
    "Series A": 20,
    "Series C": 10,
    "Seed":      5,
}

def score_funding_stage(val):
    return STAGE_SCORES.get(str(val).strip(), 0)

# ── Funding recency (25 pts) ──────────────────────────────────────────────────
def score_funding_recency(val):
    try:
        funded = dateparser.parse(str(val), dayfirst=False).date()
        days = (TODAY - funded).days
        if days < 0:
            days = 0
        if days <= 90:
            return 25
        if days <= 180:
            return 15
        if days <= 365:
            return 5
        return 0
    except Exception:
        return 0

# ── Industry fit (30 pts) ─────────────────────────────────────────────────────
HIGH_FIT = {
    "saas", "software", "ai", "artificial intelligence", "fintech",
    "cybersecurity", "developer", "data analytics", "cloud",
    "generative ai", "sales automation", "nlp", "machine learning",
}
ZERO_FIT = {
    "biotech", "hardware", "defense", "manufacturing",
    "aerospace", "gambling", "sports", "real estate",
}

def score_industry(val):
    text = str(val).lower()
    for kw in HIGH_FIT:
        if kw in text:
            return 30
    for kw in ZERO_FIT:
        if kw in text:
            return 0
    return 15

# ── Employee range (20 pts) ───────────────────────────────────────────────────
EMPLOYEE_SCORES = {
    "1-10":     5,
    "11-50":   15,
    "51-100":  20,
    "101-250": 20,
    "251-500": 15,
    "501-1000": 5,
    "1001+":    0,
}

def score_employees(val):
    v = str(val).strip()
    for key, pts in EMPLOYEE_SCORES.items():
        if key.lower() in v.lower():
            return pts
    return 10  # unknown / empty

# ── Tier classification ───────────────────────────────────────────────────────
def assign_tier(score):
    if score >= 80:
        return "Tier 1"
    if score >= 60:
        return "Tier 2"
    if score >= 40:
        return "Tier 3"
    return "Disqualified"

# ── Main ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_PATH, low_memory=False)

df["score_stage"]    = df["funding_stage"].apply(score_funding_stage)
df["score_recency"]  = df["last_funding_date"].apply(score_funding_recency)
df["score_industry"] = df["industries"].apply(score_industry)
df["score_employee"] = df["employee_range"].apply(score_employees)

df["icp_score"] = (
    df["score_stage"] + df["score_recency"] +
    df["score_industry"] + df["score_employee"]
)
df["tier"] = df["icp_score"].apply(assign_tier)

# Drop intermediate score columns before saving
df_out = df.drop(columns=["score_stage", "score_recency", "score_industry", "score_employee"])
df_out.to_csv(OUT_ALL, index=False)

# Tier 1 export
TIER1_COLS = [
    "company_name", "icp_score", "industries", "city", "state",
    "funding_stage", "last_funding_date", "employee_range",
    "estimated_revenue", "website", "contact_email", "founder_name",
]
tier1 = df_out[df_out["tier"] == "Tier 1"].sort_values("icp_score", ascending=False)
tier1[TIER1_COLS].to_csv(OUT_TIER1, index=False)

# ── Terminal summary ──────────────────────────────────────────────────────────
print("=" * 60)
print(f"  GTM LEAD SCORING PIPELINE — RESULTS")
print("=" * 60)
print(f"\nTotal companies scored: {len(df_out)}\n")

tier_order = ["Tier 1", "Tier 2", "Tier 3", "Disqualified"]
print(f"{'Tier':<15} {'Count':>6} {'Pct':>7} {'Avg Score':>10}")
print("-" * 42)
for tier_name in tier_order:
    group = df_out[df_out["tier"] == tier_name]
    count = len(group)
    pct   = count / len(df_out) * 100
    avg   = group["icp_score"].mean() if count else 0
    print(f"{tier_name:<15} {count:>6} {pct:>6.1f}% {avg:>10.1f}")

print("\n── Top 10 Tier 1 Companies ─────────────────────────────")
top10 = tier1.head(10)[["company_name", "icp_score"]]
for i, row in enumerate(top10.itertuples(), 1):
    print(f"  {i:>2}. {row.company_name:<35} {row.icp_score} pts")

email_count = tier1["contact_email"].apply(
    lambda x: bool(str(x).strip()) and str(x).strip() not in ("", "nan")
).sum()
print(f"\nTier 1 companies with contact email: {email_count} / {len(tier1)}")
print("=" * 60)
print(f"\nOutputs saved:")
print(f"  {OUT_ALL}")
print(f"  {OUT_TIER1}")
