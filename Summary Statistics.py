
import pandas as pd
import numpy as np

# ── 1. Usage growth 2000 → 2022 ───────────────────────────────────────────
start = pesticide_usage_df[pesticide_usage_df["year"] == 2000].iloc[0]
end   = pesticide_usage_df[pesticide_usage_df["year"] == 2022].iloc[0]

print("═══ PESTICIDE USAGE GROWTH (2000 → 2022) ═══")
for col in ["herbicides","insecticides","fungicides","other","total"]:
    pct = (end[col] - start[col]) / start[col] * 100
    print(f"  {col:<15}: {start[col]:>7.1f} → {end[col]:>7.1f} kt  ({pct:+.1f}%)")

# Decade-over-decade CAGR
_n_years = 22
_cagr = (end["total"] / start["total"]) ** (1 / _n_years) - 1
print(f"\n  CAGR (total usage, 22 yr): {_cagr*100:.2f}%/yr")

# ── 2. Usage share (latest year) ─────────────────────────────────────────
print("\n═══ USAGE SHARE (2022) ═══")
_row = end
_tot = _row["total"]
for col in ["herbicides","insecticides","fungicides","other"]:
    print(f"  {col:<15}: {_row[col]/_tot*100:.1f}%")

# ── 3. Cost summary ───────────────────────────────────────────────────────
print("\n═══ PESTICIDE COST / HECTARE ═══")
c_start = cost_df[cost_df["year"] == 2000].iloc[0]
c_end   = cost_df[cost_df["year"] == 2022].iloc[0]
for col in ["herbicides_usd_ha","insecticides_usd_ha","fungicides_usd_ha","other_usd_ha","total_usd_ha"]:
    pct = (c_end[col] - c_start[col]) / c_start[col] * 100
    print(f"  {col:<25}: ${c_start[col]:>6.2f} → ${c_end[col]:>6.2f}  ({pct:+.1f}%)")

_cost_cagr = (c_end["total_usd_ha"] / c_start["total_usd_ha"]) ** (1 / _n_years) - 1
print(f"\n  Cost CAGR (22 yr): {_cost_cagr*100:.2f}%/yr")

# ── 4. Yield-loss ranking ─────────────────────────────────────────────────
print("\n═══ YIELD LOSS BY CROP (sorted, %) ═══")
_ranked = yield_loss_df.sort_values("total_loss_pct", ascending=False)
print(_ranked[["crop","weeds_pct","insects_pct","pathogens_pct","total_loss_pct"]].to_string(index=False))

print(f"\n  Average yield loss across crops: {yield_loss_df['total_loss_pct'].mean():.1f}%")
print(f"  Dominant threat (avg):  weeds {yield_loss_df['weeds_pct'].mean():.1f}%  |  "
      f"insects {yield_loss_df['insects_pct'].mean():.1f}%  |  "
      f"pathogens {yield_loss_df['pathogens_pct'].mean():.1f}%")

# ── 5. Environmental impact summary ──────────────────────────────────────
print("\n═══ ENVIRONMENTAL IMPACT SCORES ═══")
print(env_df[["category","eiq_score","bee_toxicity","soil_persistence",
              "water_runoff_risk","usage_share_pct"]].to_string(index=False))

_weighted_eiq = (env_df["eiq_score"] * env_df["usage_share_pct"]).sum() / env_df["usage_share_pct"].sum()
print(f"\n  Weighted avg EIQ (by usage share): {_weighted_eiq:.1f}")

# ── 6. Headline KPIs ─────────────────────────────────────────────────────
print("\n═══ HEADLINE KPIs ═══")
print(f"  Total pesticide use 2022     : {end['total']:.0f} kt active ingredient")
print(f"  Total farmer cost 2022 (avg) : ${c_end['total_usd_ha']:.2f} / ha")
print(f"  Costliest category           : Herbicides (${c_end['herbicides_usd_ha']:.2f}/ha)")
print(f"  Most environmentally harmful : Insecticides (EIQ 78, bee toxicity 9/10)")
print(f"  Highest-risk crop (yield loss): {_ranked.iloc[0]['crop']} "
      f"({_ranked.iloc[0]['total_loss_pct']}% loss)")
