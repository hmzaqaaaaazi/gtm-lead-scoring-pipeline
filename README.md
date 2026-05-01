# GTM Lead Scoring Pipeline

An automated ICP scoring system that processes B2B company data, scores each account against a weighted qualification rubric, and outputs a tiered prospect list ready for outreach.

## Overview

Processes 994 B2B companies, scores each across four dimensions, and classifies them into actionable tiers for sales and marketing teams.

## Scoring Methodology

| Variable | Max Points | Logic |
|---|---|---|
| Funding Stage | 25 | Series B = 25, Series A = 20, Series C = 10, Seed = 5 |
| Funding Recency | 25 | Last 3 months = 25, Last 6 months = 15, Last 12 months = 5 |
| Industry Fit | 30 | SaaS, AI, FinTech, Cybersecurity, Cloud = 30. Biotech, Hardware, Defense = 0 |
| Employee Range | 20 | 51-250 employees = 20, 251-500 = 15, 11-50 = 15, others = 5-10 |

## Tier Classification

| Tier | Score Range | Action | Count |
|---|---|---|---|
| Tier 1 | 80-100 | Immediate outreach | 308 |
| Tier 2 | 60-79 | Automated sequence | 458 |
| Tier 3 | 40-59 | Nurture | 205 |
| Disqualified | Below 40 | Do not contact | 23 |

## How to Run

Install dependencies:
```
pip install -r requirements.txt
```

Clean the data:
```
python src/clean_data.py
```

Run the scoring pipeline:
```
python src/score_leads.py
```

Generate visualizations:
```
python src/visualize.py
```

## Output Files

- `data/crunchbase_clean.csv` — cleaned and standardized company data
- `output/scored_companies.csv` — all 994 companies with ICP scores and tier assignments
- `output/top_tier1_companies.csv` — Tier 1 accounts sorted by score, includes contact email and founder name
- `output/tier_distribution.png` — bar chart of tier distribution
- `output/score_distribution.png` — histogram of ICP score distribution
- `output/top_industries_tier1.png` — top industries in Tier 1 accounts

## Data

Data sourced from Crunchbase. Dataset covers 994 real B2B companies funded between 2024 and 2026.

## Tech Stack

Python, pandas, matplotlib, python-dateutil
