
import pandas as pd
import numpy as np

# ── Simulation: AI-Assisted Early Detection Impact ─────────────────────────
# Models two farming paradigms across three AI improvement levels:
#   • Traditional Farming  — baseline (no AI assistance)
#   • AI-Assisted Farming  — early detection efficiency gains of 20 / 30 / 40 %
#
# Three core metrics computed per scenario:
#   1. Reduced pesticide usage (kt active ingredient)
#   2. Cost savings per hectare (USD / ha)
#   3. Improved yield retention per crop (% points recovered)
# ──────────────────────────────────────────────────────────────────────────

# Baseline values: latest year (2022) from upstream data
_latest_usage = pesticide_usage_df[pesticide_usage_df["year"] == pesticide_usage_df["year"].max()].iloc[0]
_latest_cost  = cost_df[cost_df["year"] == cost_df["year"].max()].iloc[0]

BASELINE_TOTAL_USAGE_KT = float(_latest_usage["total"])          # kt active ingredient
BASELINE_TOTAL_COST_HA  = float(_latest_cost["total_usd_ha"])    # USD / ha

# Pesticide category breakdown (kt) — baseline
_usage_cats = {
    "herbicides":   float(_latest_usage["herbicides"]),
    "insecticides": float(_latest_usage["insecticides"]),
    "fungicides":   float(_latest_usage["fungicides"]),
    "other":        float(_latest_usage["other"]),
}

# Cost category breakdown (USD / ha) — baseline
_cost_cats = {
    "herbicides":   float(_latest_cost["herbicides_usd_ha"]),
    "insecticides": float(_latest_cost["insecticides_usd_ha"]),
    "fungicides":   float(_latest_cost["fungicides_usd_ha"]),
    "other":        float(_latest_cost["other_usd_ha"]),
}

# AI detection efficiency assumptions:
#   AI primarily reduces insecticide & fungicide applications most
#   (targeted early detection catches outbreaks before broad-spectrum spraying).
#   Herbicides benefit less (weed management is pre-emptive / agronomic).
#   Reduction factors per detection improvement level:
#                         20 %   30 %   40 %
_detection_improvements = [0.20,  0.30,  0.40]

# Category-specific multipliers: fraction of each category's usage that AI can reduce
_ai_reduction_multiplier = {
    "herbicides":   0.50,   # 50 % of gain applies to herbicides (spatial targeting)
    "insecticides": 1.00,   # 100 % of gain — real-time scout & spray
    "fungicides":   0.85,   # 85 % — early pathogen detection, fewer prophylactic sprays
    "other":        0.60,   # misc (nematicides etc.)
}

# Yield loss addressable by AI: fraction of each pest category's loss recoverable
# via timely intervention (before economic threshold is crossed)
_yield_recovery_factor = {
    "weeds_pct":      0.40,   # earlier detection → targeted herbicide / mechanical removal
    "insects_pct":    0.70,   # highest benefit — AI scouts spot infestations early
    "pathogens_pct":  0.65,   # disease forecasting models cut fungicide lag
    "viruses_pct":    0.30,   # limited — viruses spread fast; AI helps early removal
    "nematodes_pct":  0.20,   # difficult to address in-season
}

# ── 1. Pesticide Usage Simulation DataFrame ─────────────────────────────────
_usage_records = []

# Traditional baseline
_usage_records.append({
    "scenario":       "Traditional",
    "detection_gain": 0.0,
    **{k: round(v, 2) for k, v in _usage_cats.items()},
    "total_usage_kt": round(BASELINE_TOTAL_USAGE_KT, 2),
})

# AI scenarios
for _gain in _detection_improvements:
    _row = {"scenario": f"AI-Assisted ({int(_gain*100)}%)", "detection_gain": _gain}
    _total = 0.0
    for _cat, _base_kt in _usage_cats.items():
        _reduced_kt = _base_kt * (1 - _gain * _ai_reduction_multiplier[_cat])
        _row[_cat] = round(_reduced_kt, 2)
        _total += _reduced_kt
    _row["total_usage_kt"] = round(_total, 2)
    _usage_records.append(_row)

sim_usage_df = pd.DataFrame(_usage_records)

# Savings vs. baseline
sim_usage_df["usage_saved_kt"]  = round(BASELINE_TOTAL_USAGE_KT - sim_usage_df["total_usage_kt"], 2)
sim_usage_df["usage_saved_pct"] = round(sim_usage_df["usage_saved_kt"] / BASELINE_TOTAL_USAGE_KT * 100, 2)

# ── 2. Cost Savings Simulation DataFrame ────────────────────────────────────
_cost_records = []

# Traditional baseline
_cost_records.append({
    "scenario":        "Traditional",
    "detection_gain":  0.0,
    **{f"{k}_usd_ha": round(v, 2) for k, v in _cost_cats.items()},
    "total_cost_usd_ha": round(BASELINE_TOTAL_COST_HA, 2),
})

for _gain in _detection_improvements:
    _row = {"scenario": f"AI-Assisted ({int(_gain*100)}%)", "detection_gain": _gain}
    _total_cost = 0.0
    for _cat, _base_cost in _cost_cats.items():
        _reduced_cost = _base_cost * (1 - _gain * _ai_reduction_multiplier[_cat])
        _row[f"{_cat}_usd_ha"] = round(_reduced_cost, 2)
        _total_cost += _reduced_cost
    _row["total_cost_usd_ha"] = round(_total_cost, 2)
    _cost_records.append(_row)

sim_cost_df = pd.DataFrame(_cost_records)

sim_cost_df["cost_saved_usd_ha"]  = round(BASELINE_TOTAL_COST_HA - sim_cost_df["total_cost_usd_ha"], 2)
sim_cost_df["cost_saved_pct"]     = round(sim_cost_df["cost_saved_usd_ha"] / BASELINE_TOTAL_COST_HA * 100, 2)

# ── 3. Yield Retention Simulation DataFrame ─────────────────────────────────
_yield_records = []
_loss_pest_cols = ["weeds_pct", "insects_pct", "pathogens_pct", "viruses_pct", "nematodes_pct"]

for _, _crop_row in yield_loss_df.iterrows():
    _crop_name = _crop_row["crop"]
    _baseline_loss = float(_crop_row["total_loss_pct"])
    _potential_yield_pct = 100.0  # normalise potential to 100%

    # Traditional: yield retention = 100 - total_loss_pct  (approx; no AI)
    _trad_retention = _potential_yield_pct - _baseline_loss

    _rec = {
        "crop":                     _crop_name,
        "baseline_total_loss_pct":  _baseline_loss,
        "Traditional_retention_pct": round(_trad_retention, 2),
    }

    for _gain in _detection_improvements:
        _recovered_loss = 0.0
        for _pcol in _loss_pest_cols:
            _recovered_loss += float(_crop_row[_pcol]) * _yield_recovery_factor[_pcol] * _gain
        _ai_retention = _trad_retention + _recovered_loss
        _scen_key = f"AI_{int(_gain*100)}_retention_pct"
        _rec[_scen_key]                     = round(min(_ai_retention, 100.0), 2)
        _rec[f"AI_{int(_gain*100)}_gain_pp"] = round(_recovered_loss, 2)

    _yield_records.append(_rec)

sim_yield_df = pd.DataFrame(_yield_records)

# ── 4. Master Scenario Summary DataFrame ────────────────────────────────────
_scenarios  = ["Traditional", "AI-Assisted (20%)", "AI-Assisted (30%)", "AI-Assisted (40%)"]
_gains      = [0.0, 0.20, 0.30, 0.40]

sim_scenarios_df = pd.DataFrame({
    "scenario":             _scenarios,
    "detection_efficiency": [f"{int(g*100)}%" for g in _gains],
    "total_usage_kt":       sim_usage_df["total_usage_kt"].values,
    "usage_saved_kt":       sim_usage_df["usage_saved_kt"].values,
    "usage_saved_pct":      sim_usage_df["usage_saved_pct"].values,
    "total_cost_usd_ha":    sim_cost_df["total_cost_usd_ha"].values,
    "cost_saved_usd_ha":    sim_cost_df["cost_saved_usd_ha"].values,
    "cost_saved_pct":       sim_cost_df["cost_saved_pct"].values,
    # Average yield retention across all 8 crops per scenario
    "avg_yield_retention_pct": [
        round(sim_yield_df["Traditional_retention_pct"].mean(), 2),
        round(sim_yield_df["AI_20_retention_pct"].mean(), 2),
        round(sim_yield_df["AI_30_retention_pct"].mean(), 2),
        round(sim_yield_df["AI_40_retention_pct"].mean(), 2),
    ],
})
sim_scenarios_df["avg_yield_gain_pp"] = round(
    sim_scenarios_df["avg_yield_retention_pct"] - sim_scenarios_df["avg_yield_retention_pct"].iloc[0], 2
)

# ── Print Summary ─────────────────────────────────────────────────────────
print("=" * 62)
print("  AI-ASSISTED EARLY DETECTION SIMULATION  —  RESULTS SUMMARY")
print("=" * 62)

print("\n📦 Pesticide Usage (kt active ingredient):")
print(sim_usage_df[["scenario", "total_usage_kt", "usage_saved_kt", "usage_saved_pct"]].to_string(index=False))

print("\n💰 Cost per Hectare (USD / ha):")
print(sim_cost_df[["scenario", "total_cost_usd_ha", "cost_saved_usd_ha", "cost_saved_pct"]].to_string(index=False))

print("\n🌾 Avg Yield Retention across 8 Crops (%):")
print(sim_scenarios_df[["scenario", "avg_yield_retention_pct", "avg_yield_gain_pp"]].to_string(index=False))

print("\n🗂️  DataFrames available for downstream visualisations:")
print(f"  sim_usage_df     : {sim_usage_df.shape}   — usage by category & scenario")
print(f"  sim_cost_df      : {sim_cost_df.shape}   — costs by category & scenario")
print(f"  sim_yield_df     : {sim_yield_df.shape}    — yield retention per crop & scenario")
print(f"  sim_scenarios_df : {sim_scenarios_df.shape}    — master summary across all scenarios")
print("\n✅ Simulation complete")
