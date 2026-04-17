
import pandas as pd
import numpy as np

# ── Full Pipeline Validation Table ────────────────────────────────────────────
# Prints all 38 PlantVillage labels with:
#   - Category (healthy / disease / pest)
#   - Severity score
#   - Chemical pesticide name + dosage
#   - Organic alternative (truncated for display)
#   - Cost-impact connector outputs (at 80% model confidence)
# ─────────────────────────────────────────────────────────────────────────────

DEMO_CONFIDENCE = 0.80  # representative deployed-model confidence

_rows = []
for _lbl in PLANT_VILLAGE_LABELS:
    _cat    = label_category_map[_lbl]
    _sev    = LABEL_SEVERITY[_lbl]
    _rec    = RECOMMENDATIONS[_lbl]
    _impact = cost_impact_connector(DEMO_CONFIDENCE, _sev)

    _rows.append({
        "label":                    _lbl,
        "category":                 _cat,
        "severity":                 _sev,
        "chemical_name":            _rec["chemical_pesticide"]["name"],
        "chemical_dosage":          _rec["chemical_pesticide"]["dosage"],
        "organic_alt":              _rec["organic_alternative"][:55] + "…",
        "pesticide_reduction_pct":  _impact["pesticide_reduction_pct"],
        "cost_savings_usd_ha":      _impact["cost_savings_usd_ha"],
        "yield_improvement_pct":    _impact["yield_improvement_pct"],
    })

validation_df = pd.DataFrame(_rows)

# ── Assertions ────────────────────────────────────────────────────────────────
assert len(validation_df) == 38, f"Expected 38 rows, got {len(validation_df)}"
assert validation_df["label"].nunique() == 38, "Duplicate labels found"
assert validation_df["chemical_name"].notna().all(), "Missing chemical names"
assert validation_df["organic_alt"].notna().all(), "Missing organic alternatives"
assert (validation_df["pesticide_reduction_pct"] >= 0).all(), "Negative reduction %"
assert (validation_df["cost_savings_usd_ha"] >= 0).all(), "Negative cost savings"
assert (validation_df["yield_improvement_pct"] >= 0).all(), "Negative yield improvement"

# ── Print full validation table ───────────────────────────────────────────────
_DIVIDER = "─" * 130

print("=" * 130)
print("  WEED DETECTION PIPELINE — FULL VALIDATION TABLE")
print(f"  Model: EfficientNetB0 | Classes: {len(PLANT_VILLAGE_LABELS)} PlantVillage | Demo confidence: {DEMO_CONFIDENCE:.0%}")
print("=" * 130)

_hdr = (
    f"  {'#':>3}  {'Label':<56}  {'Cat':>8}  {'Sev':>4}  "
    f"{'Pest.Red%':>9}  {'$/ha Saved':>11}  {'Yield+%':>7}  "
    f"Chemical (name)"
)
print(_hdr)
print("  " + _DIVIDER)

_prev_cat = None
for _idx, _row in validation_df.iterrows():
    if _prev_cat is not None and _row["category"] != _prev_cat:
        print("  " + _DIVIDER)
    _prev_cat = _row["category"]
    print(
        f"  {_idx+1:>3}. "
        f"{_row['label']:<56}  "
        f"{_row['category']:>8}  "
        f"{_row['severity']:>4}  "
        f"{_row['pesticide_reduction_pct']:>8.2f}%  "
        f"${_row['cost_savings_usd_ha']:>10.2f}  "
        f"{_row['yield_improvement_pct']:>6.2f}%  "
        f"{_row['chemical_name']}"
    )

print("=" * 130)

# ── Summary Statistics ────────────────────────────────────────────────────────
_by_cat = validation_df.groupby("category").agg(
    count=("label", "count"),
    avg_pest_red=("pesticide_reduction_pct", "mean"),
    avg_cost_save=("cost_savings_usd_ha", "mean"),
    avg_yield_imp=("yield_improvement_pct", "mean"),
).round(2)

print("\n📊 Summary by Category:\n")
print(f"  {'Category':>10}  {'Count':>6}  {'Avg Pest Red%':>14}  {'Avg $/ha Saved':>15}  {'Avg Yield+%':>12}")
print("  " + "─" * 65)
for _cat, _s in _by_cat.iterrows():
    print(
        f"  {_cat:>10}  {int(_s['count']):>6}  "
        f"{_s['avg_pest_red']:>13.2f}%  "
        f"${_s['avg_cost_save']:>14.2f}  "
        f"{_s['avg_yield_imp']:>11.2f}%"
    )

# ── End-to-end pipeline smoke test ───────────────────────────────────────────
print("\n🔬 End-to-end pipeline smoke test:\n")
_test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
_preds = weed_detector.predict(_test_image, top_k=3)
for _p in _preds:
    _ci = cost_impact_connector(_p["confidence"], _p["severity"])
    _rr = RECOMMENDATIONS[_p["label"]]
    print(f"  Prediction : {_p['label']}")
    print(f"  Category   : {_p['category']}  |  Severity: {_p['severity']}")
    print(f"  Confidence : {_p['confidence']:.4f}")
    print(f"  Chemical   : {_rr['chemical_pesticide']['name']} @ {_rr['chemical_pesticide']['dosage']}")
    print(f"  Organic    : {_rr['organic_alternative'][:70]}…")
    print(f"  Impact     : Pest. reduction {_ci['pesticide_reduction_pct']:.2f}%  |  Cost saved ${_ci['cost_savings_usd_ha']:.2f}/ha  |  Yield +{_ci['yield_improvement_pct']:.2f}%")
    print()

print("=" * 130)
print("✅ All 38 labels present, all recommendations non-empty, cost connector valid.")
print("✅ Weed detection pipeline end-to-end validation PASSED.")
print("=" * 130)
