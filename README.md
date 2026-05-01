# GTM Lead Scoring Pipeline

An automated ICP scoring system that processes 994 real B2B companies sourced from Crunchbase, scores each against a weighted four-dimension qualification rubric, and outputs a ranked, tiered prospect list ready for outreach sequencing. Built as a GTM Engineer portfolio project to demonstrate signal-based lead qualification, ICP scoring logic, and pipeline automation across a real dataset of companies funded between 2024 and 2026.

## Why This Matters

Sales teams manually reviewing hundreds of leads waste hours on low-fit accounts. This system automatically scores every company across four business-relevant dimensions — funding stage, funding recency, industry fit, and employee range — and routes them into tiers so reps focus only on Tier 1 accounts and automation handles the rest. The result is a clean, prioritized prospect list that eliminates guesswork and puts outreach effort where it converts.

## Scoring Methodology

| Variable | Max Points | Business Justification |
|---|---|---|
| Funding Stage | 25 | Series A/B companies have confirmed PMF and active growth budgets |
| Funding Recency | 25 | Recently funded companies are actively spending on new infrastructure |
| Industry Fit | 30 | SaaS and AI companies have the highest propensity to buy GTM tooling |
| Employee Range | 20 | 50–250 employee companies are in active GTM scaling phase |

## Tier Classification

| Tier | Score Range | Recommended Action | Companies |
|---|---|---|---|
| Tier 1 | 80–100 | Immediate outreach | 308 |
| Tier 2 | 60–79 | Automated sequence | 458 |
| Tier 3 | 40–59 | Nurture | 205 |
| Disqualified | Below 40 | Do not contact | 23 |

## How to Run

Install dependencies:
```
pip install -r requirements.txt
```

Clean and standardize the raw data:
```
python src/clean_data.py
```

Score all companies and generate CSVs:
```
python src/score_leads.py
```

Generate charts and visualizations:
```
python src/visualize.py
```

## Output Files

| File | Description |
|---|---|
| `data/crunchbase_clean.csv` | Cleaned and standardized dataset with mapped columns and combined industries |
| `output/scored_companies.csv` | All 994 companies with ICP scores and tier assignments |
| `output/top_tier1_companies.csv` | Tier 1 accounts only, sorted by score descending, ready for outreach |
| `output/tier_distribution.png` | Bar chart showing count of companies per tier |
| `output/score_distribution.png` | Histogram of ICP scores across all companies with Tier 1 threshold line |
| `output/top_industries_tier1.png` | Top 10 industries appearing in Tier 1 accounts |

## Tech Stack

Python, pandas, matplotlib, python-dateutil

## Portfolio Note

This project is part of a GTM Engineer portfolio demonstrating hands-on skills in lead scoring, ICP qualification, data pipeline automation, and revenue operations analytics. Data sourced from Crunchbase Pro covering 994 real B2B companies funded between 2024 and 2026.
