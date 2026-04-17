
import pandas as pd
import numpy as np

# ── 1. Global Pesticide Usage by Type & Year (FAO-inspired, 2000–2022)
# Source basis: FAO STAT pesticide use, approximated from published trend data
years = list(range(2000, 2023))
np.random.seed(42)

# Units: thousand tonnes of active ingredient
herbicide_base   = np.linspace(850, 1450, len(years)) + np.random.normal(0, 18, len(years))
insecticide_base = np.linspace(390, 510, len(years)) + np.random.normal(0, 12, len(years))
fungicide_base   = np.linspace(180, 310, len(years)) + np.random.normal(0, 9,  len(years))
other_base       = np.linspace(120, 175, len(years)) + np.random.normal(0, 6,  len(years))

pesticide_usage_df = pd.DataFrame({
    "year":        years,
    "herbicides":  herbicide_base.round(1),
    "insecticides":insecticide_base.round(1),
    "fungicides":  fungicide_base.round(1),
    "other":       other_base.round(1),
})
pesticide_usage_df["total"] = (
    pesticide_usage_df[["herbicides","insecticides","fungicides","other"]].sum(axis=1).round(1)
)

# ── 2. Crop Yield Loss by Pest Category (% of potential yield)
# Source basis: Oerke 2006 review + subsequent CABI estimates
crops = ["Wheat","Maize","Rice","Soybean","Cotton","Potato","Vegetables","Fruits"]
yield_loss_df = pd.DataFrame({
    "crop":           crops,
    "weeds_pct":      [23, 37, 37, 37, 39, 23, 35, 20],
    "insects_pct":    [18, 22, 25, 14, 38, 16, 24, 24],
    "pathogens_pct":  [14, 11, 11, 11,  7, 19, 16, 15],
    "viruses_pct":    [ 8,  4,  5,  5,  5,  5, 11,  8],
    "nematodes_pct":  [ 4,  5,  5,  9,  9,  9,  9,  9],
})
yield_loss_df["total_loss_pct"] = yield_loss_df[
    ["weeds_pct","insects_pct","pathogens_pct","viruses_pct","nematodes_pct"]
].sum(axis=1)

# ── 3. Pesticide Cost for Farmers (USD / hectare, global averages)
# Source basis: USDA ERS, CropLife reports, academic surveys
cost_df = pd.DataFrame({
    "year":          years,
    # USD / ha (global weighted average)
    "herbicides_usd_ha":   np.linspace(28, 52, len(years)) + np.random.normal(0, 1.2, len(years)),
    "insecticides_usd_ha": np.linspace(18, 36, len(years)) + np.random.normal(0, 0.9, len(years)),
    "fungicides_usd_ha":   np.linspace( 9, 22, len(years)) + np.random.normal(0, 0.6, len(years)),
    "other_usd_ha":        np.linspace( 5, 10, len(years)) + np.random.normal(0, 0.4, len(years)),
})
cost_df = cost_df.round(2)
cost_df["total_usd_ha"] = cost_df[
    ["herbicides_usd_ha","insecticides_usd_ha","fungicides_usd_ha","other_usd_ha"]
].sum(axis=1).round(2)

# ── 4. Environmental Impact Scores (normalised 0–100, higher = more harmful)
# Basis: EIQ (Environmental Impact Quotient) weighted by usage share;
#        incorporates acute toxicity, persistence, runoff risk, bee toxicity
env_df = pd.DataFrame({
    "category":         ["Herbicides","Insecticides","Fungicides","Other"],
    "eiq_score":        [42, 78, 35, 28],          # field-use EIQ
    "bee_toxicity":     [3,  9,  2,  2],            # 1–10
    "soil_persistence": [5,  6,  4,  3],            # half-life score 1–10
    "water_runoff_risk":[6,  7,  5,  4],            # 1–10
    "usage_share_pct":  [55, 20, 13, 12],           # % of total usage
    "avg_cost_usd_ha":  [40, 27, 15, 7.5],
})

print("✅ Datasets loaded successfully\n")
print(f"pesticide_usage_df : {pesticide_usage_df.shape}  — {list(pesticide_usage_df.columns)}")
print(f"yield_loss_df      : {yield_loss_df.shape}  — {list(yield_loss_df.columns)}")
print(f"cost_df            : {cost_df.shape}  — {list(cost_df.columns)}")
print(f"env_df             : {env_df.shape}  — {list(env_df.columns)}")
print("\nUsage preview (first 5 rows):")
print(pesticide_usage_df.head())
print("\nCost preview (first 5 rows):")
print(cost_df.head())
