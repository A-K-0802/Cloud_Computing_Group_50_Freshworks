"""
analyze.py  –  Group 50 | Theme 4: Serverless Cold Start Analysis
Person B deliverable.

Reads results/latency.csv and produces:
  - results/summary.csv
  - results/latency_graph.png   (the main deliverable graph)
  - results/latency_analysis.xlsx  (with Raw data + Summary sheets)

Usage:
    python benchmark/analyze.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Load data ──────────────────────────────────────────────────────────
csv_path = "results/latency.csv"
if not os.path.exists(csv_path):
    print("ERROR: results/latency.csv not found.")
    print("       Run benchmark/benchmark.py first.")
    raise SystemExit(1)

df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from {csv_path}\n")

# ── Identify cold vs warm ──────────────────────────────────────────────
# cold_start column from API response (True on request 1 of each round)
# Fallback: treat request_no == 1 as cold if column missing
if "cold_start" in df.columns and df["cold_start"].notna().any():
    cold     = df[df["cold_start"] == True]
    warm_all = df[df["cold_start"] == False]
else:
    print("NOTE: cold_start column not available; using request_no==1 as cold.")
    cold     = df[df["request_no"] == 1]
    warm_all = df[df["request_no"] > 1]

warm100 = df[df["request_no"] == 100] if 100 in df["request_no"].values else warm_all.tail(ROUNDS := df["round"].max())

# ── Summary stats ──────────────────────────────────────────────────────
summary = pd.DataFrame({
    "metric": [
        "Cold (1st req) avg ms",
        "Warm (last req) avg ms",
        "Warm (all warm) avg ms",
        "Warm (all warm) p95 ms",
        "Cold-to-Warm ratio",
    ],
    "value": [
        round(cold["latency_ms"].mean(), 2),
        round(warm100["latency_ms"].mean(), 2),
        round(warm_all["latency_ms"].mean(), 2),
        round(warm_all["latency_ms"].quantile(0.95), 2),
        round(cold["latency_ms"].mean() / warm_all["latency_ms"].mean(), 2),
    ],
})
summary.to_csv("results/summary.csv", index=False)
print("-- Summary ------------------------------------------")
print(summary.to_string(index=False))
print()

# ── Figure: 2 panels ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Group 50 | Serverless Cold Start Benchmark", fontsize=14, fontweight="bold")

# Panel 1 – Line chart: latency across all requests in Round 1
r1 = df[df["round"] == 1].copy()
colors_line = ["#d9534f" if c else "#5cb85c"
               for c in r1.get("cold_start", r1["request_no"] == 1)]
axes[0].scatter(r1["request_no"], r1["latency_ms"], c=colors_line, s=20, zorder=3)
axes[0].plot(r1["request_no"], r1["latency_ms"], color="#aaa", linewidth=0.8, zorder=2)
axes[0].set_title("Latency per Request (Round 1)")
axes[0].set_xlabel("Request Number")
axes[0].set_ylabel("Latency (ms)")
axes[0].grid(True, linestyle="--", alpha=0.5)
cold_patch = mpatches.Patch(color="#d9534f", label="Cold start")
warm_patch = mpatches.Patch(color="#5cb85c", label="Warm")
axes[0].legend(handles=[cold_patch, warm_patch])

# Panel 2 – Bar chart: Cold avg vs Warm avg (across all rounds)
categories = ["Cold\n(1st req avg)", "Warm\n(last req avg)", "Warm\n(all reqs avg)"]
values     = [cold["latency_ms"].mean(),
              warm100["latency_ms"].mean(),
              warm_all["latency_ms"].mean()]
bar_colors = ["#d9534f", "#5cb85c", "#5bc0de"]
bars = axes[1].bar(categories, values, color=bar_colors, width=0.5, edgecolor="white")
axes[1].set_title("Cold vs Warm – Average Latency (all rounds)")
axes[1].set_ylabel("Latency (ms)")
axes[1].grid(True, axis="y", linestyle="--", alpha=0.5)
for bar, val in zip(bars, values):
    axes[1].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1,
                 f"{val:.1f} ms",
                 ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("results/latency_graph.png", dpi=150, bbox_inches="tight")
print("SAVED: results/latency_graph.png")

# ── Excel workbook ─────────────────────────────────────────────────────
with pd.ExcelWriter("results/latency_analysis.xlsx", engine="openpyxl") as xw:
    df.to_excel(xw, sheet_name="Raw data", index=False)
    summary.to_excel(xw, sheet_name="Summary", index=False)

print("SAVED: results/latency_analysis.xlsx")
print("\nAll done! Open results/latency_graph.png to see your graph.")
print("Add a column chart in Excel: Summary sheet -> Insert -> Column Chart.")
