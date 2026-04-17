
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG     = "#1D1D20"
TEXT   = "#fbfbff"
SEC    = "#909094"
LOSS_COLORS = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF"]
LOSS_LABELS = ["Weeds", "Insects", "Pathogens", "Viruses", "Nematodes"]
LOSS_COLS   = ["weeds_pct","insects_pct","pathogens_pct","viruses_pct","nematodes_pct"]

# Sort by total loss descending
_df = yield_loss_df.sort_values("total_loss_pct", ascending=True)

crop_yield_fig, ax = plt.subplots(figsize=(10, 6))
crop_yield_fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

_crops = _df["crop"].values
_y = np.arange(len(_crops))

_left = np.zeros(len(_crops))
for col, label, color in zip(LOSS_COLS, LOSS_LABELS, LOSS_COLORS):
    _vals = _df[col].values
    bars = ax.barh(_y, _vals, left=_left, color=color, label=label,
                   edgecolor=BG, linewidth=0.5, height=0.65, alpha=0.9)
    # Label segments > 8%
    for j, (v, l) in enumerate(zip(_vals, _left)):
        if v >= 8:
            ax.text(l + v/2, j, f"{v}%", ha="center", va="center",
                    color=BG, fontsize=8, fontweight="bold")
    _left += _vals

# Total labels at end of bars
for j, (crop, total) in enumerate(zip(_crops, _df["total_loss_pct"].values)):
    ax.text(total + 0.5, j, f"{total}%", va="center", color=TEXT, fontsize=9)

ax.set_yticks(_y)
ax.set_yticklabels(_crops, color=TEXT, fontsize=10)
_xticks = [0, 20, 40, 60, 80, 100]
ax.set_xticks(_xticks)
ax.set_xticklabels([f"{v}%" for v in _xticks], color=TEXT, fontsize=9)

ax.set_xlim(0, 115)
ax.set_title("Estimated Crop Yield Loss by Pest Category (%)",
             color=TEXT, fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Potential Yield Lost (%)", color=SEC, fontsize=10)
ax.tick_params(colors=TEXT)
for spine in ax.spines.values():
    spine.set_edgecolor("#444")
ax.grid(axis="x", color="#333", linewidth=0.4, alpha=0.4)

ax.legend(loc="lower right", framealpha=0.25, facecolor=BG,
          labelcolor=TEXT, fontsize=9)

crop_yield_fig.tight_layout()
print("✅ Crop yield loss chart created")
