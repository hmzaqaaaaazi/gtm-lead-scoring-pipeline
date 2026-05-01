import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "output", "scored_companies.csv")
OUT_DIR    = os.path.join(BASE_DIR, "output")

df = pd.read_csv(INPUT_PATH, low_memory=False)

# ── Chart 1: Tier Distribution ────────────────────────────────────────────────
tier_order  = ["Tier 1", "Tier 2", "Tier 3", "Disqualified"]
tier_colors = ["green", "steelblue", "orange", "red"]
counts = [df[df["tier"] == t].shape[0] for t in tier_order]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(tier_order, counts, color=tier_colors, width=0.5, edgecolor="none")

for bar, count in zip(bars, counts):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 4,
        str(count),
        ha="center", va="bottom", fontsize=12, fontweight="bold"
    )

ax.set_title("ICP Tier Distribution — 994 B2B Companies", fontsize=14, fontweight="bold", pad=14)
ax.set_ylabel("Number of Companies", fontsize=11)
ax.set_ylim(0, max(counts) * 1.15)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.yaxis.set_visible(False)
ax.tick_params(axis="x", labelsize=12)
plt.tight_layout()
out1 = os.path.join(OUT_DIR, "tier_distribution.png")
fig.savefig(out1, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out1}")

# ── Chart 2: Score Distribution ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df["icp_score"], bins=20, color="steelblue", edgecolor="white", linewidth=0.5)
ax.axvline(x=80, color="red", linestyle="--", linewidth=1.5, label="Tier 1 threshold")
ax.text(81, ax.get_ylim()[1] * 0.95, "Tier 1 threshold", color="red", fontsize=9, va="top")
ax.set_title("ICP Score Distribution", fontsize=14, fontweight="bold", pad=14)
ax.set_xlabel("ICP Score", fontsize=11)
ax.set_ylabel("Number of Companies", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
out2 = os.path.join(OUT_DIR, "score_distribution.png")
fig.savefig(out2, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out2}")

# ── Chart 3: Top Industries in Tier 1 ────────────────────────────────────────
tier1 = df[df["tier"] == "Tier 1"].copy()
industry_counts = Counter()
for val in tier1["industries"].dropna():
    for tag in str(val).split(","):
        tag = tag.strip()
        if tag and tag.lower() not in ("nan", ""):
            industry_counts[tag] += 1

top10 = industry_counts.most_common(10)
labels = [t[0] for t in reversed(top10)]
values = [t[1] for t in reversed(top10)]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(labels, values, color="green", edgecolor="none")

for bar, val in zip(bars, values):
    ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va="center", ha="left", fontsize=10, fontweight="bold"
    )

ax.set_title("Top Industries in Tier 1 Accounts", fontsize=14, fontweight="bold", pad=14)
ax.set_xlabel("Count", fontsize=11)
ax.set_xlim(0, max(values) * 1.15)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
out3 = os.path.join(OUT_DIR, "top_industries_tier1.png")
fig.savefig(out3, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out3}")

print("\nAll 3 charts saved to output/")
