
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG     = "#1D1D20"
TEXT   = "#fbfbff"
SEC    = "#909094"
COLORS = ["#A1C9F4", "#FFB482", "#8DE5A1", "#D0BBFF"]

env_impact_fig, ax = plt.subplots(figsize=(9, 6))
env_impact_fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

for i, row in env_df.iterrows():
    _size = row["usage_share_pct"] * 28      # scale bubble
    ax.scatter(row["avg_cost_usd_ha"], row["eiq_score"],
               s=_size, color=COLORS[i], alpha=0.85, zorder=3,
               edgecolors="white", linewidths=0.6)
    _offset_x = 1.5
    _offset_y = 1.5 if i % 2 == 0 else -4
    ax.annotate(
        f"{row['category']}\n(EIQ {row['eiq_score']}, ${row['avg_cost_usd_ha']}/ha)",
        xy=(row["avg_cost_usd_ha"], row["eiq_score"]),
        xytext=(row["avg_cost_usd_ha"] + _offset_x, row["eiq_score"] + _offset_y),
        color=TEXT, fontsize=9, ha="left",
        arrowprops=dict(arrowstyle="-", color=SEC, lw=0.8)
    )

# Quadrant shading
ax.axvline(30, color="#444", linewidth=0.7, linestyle=":")
ax.axhline(50, color="#444", linewidth=0.7, linestyle=":")
ax.text(5,  85, "High harm\nLow cost",  color="#f04438", fontsize=8, alpha=0.7)
ax.text(38, 85, "High harm\nHigh cost", color="#ffd400", fontsize=8, alpha=0.7)
ax.text(5,  15, "Low harm\nLow cost",   color="#17b26a", fontsize=8, alpha=0.7)
ax.text(38, 15, "Low harm\nHigh cost",  color=SEC,       fontsize=8, alpha=0.7)

_xticks = [0, 10, 20, 30, 40, 50, 60]
ax.set_xticks(_xticks)
ax.set_xticklabels([f"${v}" for v in _xticks], color=TEXT, fontsize=9)
_yticks = [0, 20, 40, 60, 80, 100]
ax.set_yticks(_yticks)
ax.set_yticklabels([str(v) for v in _yticks], color=TEXT, fontsize=9)

ax.set_xlim(0, 65)
ax.set_ylim(0, 100)
ax.set_title("Environmental Impact vs. Cost by Pesticide Category\n(Bubble size = % of total usage)",
             color=TEXT, fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("Average Cost (USD / hectare)", color=SEC, fontsize=10)
ax.set_ylabel("Environmental Impact Quotient (EIQ, 0–100)", color=SEC, fontsize=10)
ax.tick_params(colors=TEXT)
for spine in ax.spines.values():
    spine.set_edgecolor("#444")
ax.grid(color="#333", linewidth=0.4, alpha=0.4)

env_impact_fig.tight_layout()
print("✅ Environmental impact bubble chart created")
