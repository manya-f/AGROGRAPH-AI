
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG     = "#1D1D20"
TEXT   = "#fbfbff"
SEC    = "#909094"
COLORS = ["#A1C9F4", "#FFB482", "#8DE5A1", "#D0BBFF", "#ffd400"]
COST_CATS   = ["herbicides_usd_ha","insecticides_usd_ha","fungicides_usd_ha","other_usd_ha","total_usd_ha"]
COST_LABELS = ["Herbicides","Insecticides","Fungicides","Other","Total"]

_yrs = cost_df["year"].values

cost_trend_fig, ax = plt.subplots(figsize=(11, 5.5))
cost_trend_fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

for cat, label, color in zip(COST_CATS, COST_LABELS, COLORS):
    _lw = 2.5 if cat == "total_usd_ha" else 1.8
    _ls = "--" if cat == "total_usd_ha" else "-"
    ax.plot(_yrs, cost_df[cat].values, color=color, linewidth=_lw,
            linestyle=_ls, label=label, marker="o", markersize=3.5, alpha=0.9)

# Annotate 2022 total
_tot_2022 = cost_df.loc[cost_df["year"]==2022, "total_usd_ha"].values[0]
ax.annotate(f"${_tot_2022:.0f}/ha",
            xy=(2022, _tot_2022), xytext=(2018, _tot_2022 + 7),
            arrowprops=dict(arrowstyle="->", color=TEXT, lw=1.0),
            color=TEXT, fontsize=9)

_yticks = [0, 20, 40, 60, 80, 100, 120]
ax.set_yticks(_yticks)
ax.set_yticklabels([f"${v}" for v in _yticks], color=TEXT, fontsize=9)
ax.set_xticks(_yrs[::2])
ax.set_xticklabels([str(y) for y in _yrs[::2]], color=TEXT, fontsize=9, rotation=30)

ax.set_title("Pesticide Cost per Hectare by Category (2000–2022)",
             color=TEXT, fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year", color=SEC, fontsize=10)
ax.set_ylabel("Cost (USD / hectare)", color=SEC, fontsize=10)
ax.tick_params(colors=TEXT)
for spine in ax.spines.values():
    spine.set_edgecolor("#444")
ax.grid(axis="y", color="#333", linewidth=0.5, alpha=0.5)
ax.legend(loc="upper left", framealpha=0.25, facecolor=BG, labelcolor=TEXT, fontsize=9)

cost_trend_fig.tight_layout()
print("✅ Cost trend chart created")
