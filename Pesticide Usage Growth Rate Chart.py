
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG     = "#1D1D20"
TEXT   = "#fbfbff"
SEC    = "#909094"
COLORS = ["#A1C9F4", "#FFB482", "#8DE5A1", "#D0BBFF"]
CATS   = ["herbicides", "insecticides", "fungicides", "other"]
LABELS = ["Herbicides", "Insecticides", "Fungicides", "Other"]

_yrs = pesticide_usage_df["year"].values[1:]  # drop first (no prior year)

usage_growth_fig, ax = plt.subplots(figsize=(11, 5))
usage_growth_fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

for cat, label, color in zip(CATS, LABELS, COLORS):
    _vals = pesticide_usage_df[cat].values
    _yoy  = np.diff(_vals) / _vals[:-1] * 100
    ax.plot(_yrs, _yoy, color=color, linewidth=2, label=label, marker="o",
            markersize=3, alpha=0.9)

# Zero line
ax.axhline(0, color=SEC, linewidth=0.8, linestyle="--", alpha=0.6)

ax.set_xlim(_yrs[0], _yrs[-1])
_ylim = max(abs(ax.get_ylim()[0]), abs(ax.get_ylim()[1]))
_yticks_vals = [-8, -4, 0, 4, 8, 12]
ax.set_yticks(_yticks_vals)
ax.set_yticklabels([f"{v:+.0f}%" for v in _yticks_vals], color=TEXT, fontsize=9)
ax.set_xticks(_yrs[::2])
ax.set_xticklabels([str(y) for y in _yrs[::2]], color=TEXT, fontsize=9, rotation=30)

ax.set_title("Year-over-Year Pesticide Usage Growth Rate by Category",
             color=TEXT, fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year", color=SEC, fontsize=10)
ax.set_ylabel("YoY Growth (%)", color=SEC, fontsize=10)
ax.tick_params(colors=TEXT)
for spine in ax.spines.values():
    spine.set_edgecolor("#444")

ax.legend(loc="upper right", framealpha=0.25, facecolor=BG,
          labelcolor=TEXT, fontsize=9)
ax.grid(axis="y", color="#333", linewidth=0.5, alpha=0.5)

usage_growth_fig.tight_layout()
print("✅ Growth-rate chart created")
