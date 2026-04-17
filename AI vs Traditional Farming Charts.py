
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# ── Design System ─────────────────────────────────────────────────────────
BG    = "#1D1D20"
TEXT  = "#fbfbff"
SEC   = "#909094"
GOLD  = "#ffd400"
GREEN = "#17b26a"
WARN  = "#f04438"

AI_COLORS = {
    "Traditional":       "#909094",
    "AI-Assisted (20%)": "#A1C9F4",
    "AI-Assisted (30%)": "#FFB482",
    "AI-Assisted (40%)": "#8DE5A1",
}
CAT_COLORS = {
    "herbicides":   "#A1C9F4",
    "insecticides": "#FF9F9B",
    "fungicides":   "#D0BBFF",
    "other":        "#FFB482",
}

SCENARIOS     = ["Traditional", "AI-Assisted (20%)", "AI-Assisted (30%)", "AI-Assisted (40%)"]
SCEN_LABELS   = ["Traditional", "AI 20%", "AI 30%", "AI 40%"]
PEST_CATS     = ["herbicides", "insecticides", "fungicides", "other"]
PEST_LABELS   = ["Herbicides", "Insecticides", "Fungicides", "Other"]

def _style(fig, axes):
    """Apply Zerve dark theme to a figure and all its axes."""
    fig.patch.set_facecolor(BG)
    for _ax in (axes if hasattr(axes, "__iter__") else [axes]):
        _ax.set_facecolor(BG)
        _ax.tick_params(colors=SEC, labelsize=10)
        _ax.xaxis.label.set_color(SEC)
        _ax.yaxis.label.set_color(SEC)
        _ax.title.set_color(TEXT)
        for _sp in _ax.spines.values():
            _sp.set_edgecolor("#333338")

# ─────────────────────────────────────────────────────────────────────────
# CHART 1 — Grouped Bar: Pesticide Usage Reduction by Category & Scenario
# ─────────────────────────────────────────────────────────────────────────
grouped_bar_fig, gb_ax = plt.subplots(figsize=(13, 7))
_style(grouped_bar_fig, gb_ax)

_x      = np.arange(len(PEST_CATS))
_n_scen = len(SCENARIOS)
_width  = 0.18
_offsets = np.linspace(-(_n_scen - 1) / 2, (_n_scen - 1) / 2, _n_scen) * _width

for _si, (_scen, _off) in enumerate(zip(SCENARIOS, _offsets)):
    _row   = sim_usage_df[sim_usage_df["scenario"] == _scen].iloc[0]
    _vals  = [_row[_c] for _c in PEST_CATS]
    _bars  = gb_ax.bar(
        _x + _off, _vals, _width,
        color=list(AI_COLORS.values())[_si],
        label=SCEN_LABELS[_si],
        alpha=0.92,
        zorder=3,
    )
    # Annotate top of each bar with value
    for _b in _bars:
        _h = _b.get_height()
        gb_ax.text(
            _b.get_x() + _b.get_width() / 2, _h + 8,
            f"{_h:.0f}", ha="center", va="bottom",
            fontsize=7.5, color=SEC
        )

gb_ax.set_xticks(_x)
gb_ax.set_xticklabels(PEST_LABELS, fontsize=12, color=TEXT)
gb_ax.set_ylabel("Usage (kt active ingredient)", fontsize=11, color=SEC)
gb_ax.set_title(
    "Pesticide Usage by Category — Traditional vs AI-Assisted Scenarios",
    fontsize=14, color=TEXT, fontweight="bold", pad=16
)
gb_ax.legend(
    frameon=False, fontsize=10,
    labelcolor=TEXT, loc="upper right"
)
gb_ax.grid(axis="y", color="#333338", linewidth=0.6, zorder=0)
gb_ax.set_ylim(0, max(sim_usage_df["herbicides"]) * 1.22)
grouped_bar_fig.tight_layout()
print("✅ Chart 1 — Grouped bar complete")

# ─────────────────────────────────────────────────────────────────────────
# CHART 2 — Stacked Cost Savings: Absolute cost/ha saved per category & scenario
# ─────────────────────────────────────────────────────────────────────────
cost_savings_fig, cs_ax = plt.subplots(figsize=(11, 7))
_style(cost_savings_fig, cs_ax)

# Build savings vs baseline per category
_baseline_costs = sim_cost_df[sim_cost_df["scenario"] == "Traditional"].iloc[0]
_ai_scenarios   = sim_cost_df[sim_cost_df["scenario"] != "Traditional"].reset_index(drop=True)
_ai_labels      = ["AI 20%", "AI 30%", "AI 40%"]
_bottoms        = np.zeros(3)
_handles        = []

for _pi, (_pcat, _plabel) in enumerate(zip(PEST_CATS, PEST_LABELS)):
    _col_name = f"{_pcat}_usd_ha"
    _savings   = _baseline_costs[_col_name] - _ai_scenarios[_col_name].values
    _bars = cs_ax.bar(
        _ai_labels, _savings,
        bottom=_bottoms,
        color=list(CAT_COLORS.values())[_pi],
        alpha=0.92,
        zorder=3,
        label=_plabel,
    )
    # Value labels inside stacked bars
    for _b, _sv in zip(_bars, _savings):
        _mid_y = _b.get_y() + _b.get_height() / 2
        if _b.get_height() > 0.8:
            cs_ax.text(
                _b.get_x() + _b.get_width() / 2, _mid_y,
                f"${_sv:.2f}", ha="center", va="center",
                fontsize=8.5, color=BG, fontweight="bold"
            )
    _bottoms += _savings
    _handles.append(mpatches.Patch(color=list(CAT_COLORS.values())[_pi], label=_plabel))

# Total label on top of each stack
for _bi, (_lab, _tot) in enumerate(zip(_ai_labels, _bottoms)):
    cs_ax.text(
        _bi, _tot + 0.4,
        f"${_tot:.2f}/ha", ha="center", va="bottom",
        fontsize=11, color=GOLD, fontweight="bold"
    )

cs_ax.set_ylabel("Cost Saved (USD / ha)", fontsize=11, color=SEC)
cs_ax.set_title(
    "Cost Savings per Hectare by Pesticide Category — AI vs Traditional",
    fontsize=14, color=TEXT, fontweight="bold", pad=16
)
cs_ax.legend(
    handles=_handles, frameon=False, fontsize=10,
    labelcolor=TEXT, loc="upper left"
)
cs_ax.grid(axis="y", color="#333338", linewidth=0.6, zorder=0)
cs_ax.set_ylim(0, _bottoms.max() * 1.22)
cost_savings_fig.tight_layout()
print("✅ Chart 2 — Stacked cost savings complete")

# ─────────────────────────────────────────────────────────────────────────
# CHART 3 — Horizontal Bars: Yield retention % gain per crop under AI
# ─────────────────────────────────────────────────────────────────────────
yield_fig, yd_ax = plt.subplots(figsize=(12, 7))
_style(yield_fig, yd_ax)

_crop_names   = sim_yield_df["crop"].tolist()
_n_crops      = len(_crop_names)
_gain_cols    = ["AI_20_gain_pp", "AI_30_gain_pp", "AI_40_gain_pp"]
_gain_labels  = ["AI 20%", "AI 30%", "AI 40%"]
_gain_colors  = [AI_COLORS["AI-Assisted (20%)"],
                 AI_COLORS["AI-Assisted (30%)"],
                 AI_COLORS["AI-Assisted (40%)"]]

_y      = np.arange(_n_crops)
_h      = 0.22
_g_offs = np.array([-1, 0, 1]) * _h

for _gi, (_gcol, _glab, _gcol_color) in enumerate(zip(_gain_cols, _gain_labels, _gain_colors)):
    _gains = sim_yield_df[_gcol].values
    _hbars = yd_ax.barh(
        _y + _g_offs[_gi], _gains, _h * 0.9,
        color=_gcol_color, alpha=0.92, zorder=3, label=_glab
    )
    # Value labels at end of bars
    for _b, _gv in zip(_hbars, _gains):
        yd_ax.text(
            _gv + 0.15, _b.get_y() + _b.get_height() / 2,
            f"+{_gv:.1f} pp", va="center", ha="left",
            fontsize=8, color=SEC
        )

yd_ax.set_yticks(_y)
yd_ax.set_yticklabels(_crop_names, fontsize=12, color=TEXT)
yd_ax.set_xlabel("Yield Retention Gain (percentage points)", fontsize=11, color=SEC)
yd_ax.set_title(
    "Yield Retention Gain per Crop — AI-Assisted vs Traditional Farming",
    fontsize=14, color=TEXT, fontweight="bold", pad=16
)
yd_ax.legend(
    frameon=False, fontsize=10, labelcolor=TEXT, loc="lower right"
)
yd_ax.grid(axis="x", color="#333338", linewidth=0.6, zorder=0)
yd_ax.set_xlim(0, sim_yield_df[_gain_cols].values.max() * 1.35)
yield_fig.tight_layout()
print("✅ Chart 3 — Yield retention horizontal bars complete")

# ─────────────────────────────────────────────────────────────────────────
# CHART 4 — Scenario Summary Table (printed DataFrame)
# ─────────────────────────────────────────────────────────────────────────
_display_df = sim_scenarios_df[[
    "scenario", "detection_efficiency",
    "total_usage_kt", "usage_saved_kt", "usage_saved_pct",
    "total_cost_usd_ha", "cost_saved_usd_ha", "cost_saved_pct",
    "avg_yield_retention_pct", "avg_yield_gain_pp"
]].copy()

_display_df.columns = [
    "Scenario", "Detection Eff.",
    "Total Usage (kt)", "Usage Saved (kt)", "Usage Saved (%)",
    "Total Cost ($/ha)", "Cost Saved ($/ha)", "Cost Saved (%)",
    "Avg Yield Retention (%)", "Yield Gain (pp)"
]

print("\n" + "=" * 100)
print("  SCENARIO COMPARISON — Traditional Farming vs AI-Assisted Early Detection")
print("=" * 100)
print(_display_df.to_string(index=False))
print("=" * 100)
print("\nKey takeaways:")
for _, _r in sim_scenarios_df.iterrows():
    if _r["scenario"] == "Traditional":
        continue
    print(
        f"  • {_r['scenario']:20s} — saves {_r['usage_saved_pct']:.1f}% pesticide | "
        f"${_r['cost_saved_usd_ha']:.2f}/ha cost saving | "
        f"+{_r['avg_yield_gain_pp']:.1f} pp yield retention"
    )
print()
print("✅ Chart 4 — Scenario summary table printed")
