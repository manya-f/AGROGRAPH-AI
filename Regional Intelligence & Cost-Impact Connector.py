
import pandas as pd

# ── Regional Intelligence Data Structure ──────────────────────────────────────
# 6 global agricultural regions, each with:
#   common_weeds      : list[str]  — top weed threats in that region
#   seasonal_risk     : dict       — season → risk level (low/medium/high/critical)
#   best_control_practices : list[str]
# ─────────────────────────────────────────────────────────────────────────────

REGIONAL_INTELLIGENCE = {

    "North America": {
        "common_weeds": [
            "Palmer amaranth (Amaranthus palmeri)",
            "Waterhemp (Amaranthus tuberculatus)",
            "Common ragweed (Ambrosia artemisiifolia)",
            "Giant foxtail (Setaria faberi)",
            "Common lambsquarters (Chenopodium album)",
            "Canada thistle (Cirsium arvense)",
            "Velvetleaf (Abutilon theophrasti)",
        ],
        "seasonal_risk": {
            "Spring":  "high",      # rapid warm-season weed emergence with row crops
            "Summer":  "critical",  # peak Palmer amaranth growth; heat accelerates spread
            "Autumn":  "medium",    # post-harvest weed seed bank replenishment
            "Winter":  "low",       # dormancy; opportunity for soil residual herbicide
        },
        "best_control_practices": [
            "Integrated weed management (IWM): rotate herbicide modes of action to combat glyphosate resistance",
            "Cover crops (cereal rye, crimson clover) to suppress early-season weed emergence",
            "Narrow row spacing in soybeans to achieve canopy closure faster",
            "Precision spot-spray technology (See & Spray, Carbon Robotics) for Palmer amaranth",
            "Scout weekly from V2 crop stage; economic threshold = 1 Palmer amaranth per 10 m row",
        ],
    },

    "South Asia": {
        "common_weeds": [
            "Parthenium weed (Parthenium hysterophorus)",
            "Barnyard grass (Echinochloa crus-galli)",
            "Wild oat (Avena fatua)",
            "Dodder (Cuscuta spp.)",
            "Spiny amaranth (Amaranthus spinosus)",
            "Goosegrass (Eleusine indica)",
            "Purple nutsedge (Cyperus rotundus)",
        ],
        "seasonal_risk": {
            "Kharif (Jun–Oct)":   "critical",  # monsoon drives explosive weed growth in rice/cotton
            "Rabi (Nov–Mar)":     "high",       # wheat-season weeds (Phalaris minor, wild oat)
            "Zaid (Apr–Jun)":     "medium",     # limited irrigation; moderate pressure
            "Pre-monsoon":        "high",       # Parthenium spreads rapidly before rains
        },
        "best_control_practices": [
            "Transplanted rice (vs. direct-seeded) to give crop head-start over barnyard grass",
            "Zero-tillage wheat planting using Happy Seeder to reduce Phalaris minor pressure",
            "Hand-weeding at 20–25 days after transplanting in rice (critical window)",
            "Pendimethalin 38.7 CS (pre-emergence) for Kharif broadleaf weeds",
            "Crop rotation: paddy → mustard → chickpea breaks weed cycles",
            "AI-powered drone scouting for large-scale Parthenium mapping in Punjab/Haryana",
        ],
    },

    "Sub-Saharan Africa": {
        "common_weeds": [
            "Striga (witchweed — Striga hermonthica)",
            "Speargrass (Imperata cylindrica)",
            "Goosegrass (Eleusine indica)",
            "Thorn apple (Datura stramonium)",
            "Mexican marigold (Tagetes minuta)",
            "Wild sorghum (Sorghum halepense)",
            "Black jack (Bidens pilosa)",
        ],
        "seasonal_risk": {
            "Long rains (Mar–Jun)":   "critical",  # Striga emergence coincides with maize/sorghum planting
            "Short rains (Oct–Dec)":  "high",       # second-season Striga cycle
            "Dry season (Jul–Sep)":   "low",        # seed dormancy; opportunity for soil management
            "Pre-planting (Feb)":     "high",       # volunteer Striga stimulation treatment window
        },
        "best_control_practices": [
            "Striga management: suicidal germination using ethylene gas or Striga-stimulating compounds before planting",
            "Push-pull intercropping: Desmodium (repels Striga) + Napier grass border (traps stemborers)",
            "Imazapyr-coated maize seed (IR-MAIZE) provides in-seed Striga control without spray",
            "Crop rotation with non-host legumes (cowpea, groundnut) — reduces Striga seed bank 50–90%",
            "Hand-pulling Striga before seed set (remove before purple flower opens)",
            "Community-level scouting networks for early Striga outbreak mapping",
        ],
    },

    "Europe": {
        "common_weeds": [
            "Black-grass (Alopecurus myosuroides)",
            "Volunteer oilseed rape (Brassica napus)",
            "Creeping thistle (Cirsium arvense)",
            "Cleavers / goosegrass (Galium aparine)",
            "Wild oat (Avena fatua)",
            "Poppies (Papaver rhoeas)",
            "Couch grass (Elymus repens)",
        ],
        "seasonal_risk": {
            "Autumn":  "critical",  # black-grass emergence coincides with winter wheat drilling
            "Winter":  "medium",    # slow growth but establishment under mild temps
            "Spring":  "high",      # rapid cleavers and brome growth; flag leaf protection period
            "Summer":  "low",       # crop canopy suppresses most weeds post-heading
        },
        "best_control_practices": [
            "Delayed drilling (after Oct 15) reduces black-grass autumn emergence by 50–80%",
            "Spring cropping in worst-affected fields breaks autumn-germinating weed cycles",
            "Herbicide resistance testing for black-grass populations before programme design",
            "GPS-guided variable-rate herbicide application (John Deere See & Spray, Trimble)",
            "Stale seedbed technique: cultivate and allow weed flush before drilling",
            "EU Green Deal compliance: target 50% pesticide reduction by 2030 — prioritise non-chemical methods",
        ],
    },

    "Southeast Asia": {
        "common_weeds": [
            "Barnyard grass (Echinochloa crus-galli)",
            "Purple nutsedge (Cyperus rotundus)",
            "Sprangletop (Leptochloa chinensis)",
            "Bur cucumber (Sicyos angulatus)",
            "Torpedo grass (Panicum repens)",
            "Water hyacinth (Eichhornia crassipes) — lowland rice",
            "Mimosa (Mimosa pudica)",
        ],
        "seasonal_risk": {
            "Wet season (May–Oct)":   "critical",  # flooded rice fields — barnyard grass explosion
            "Dry season (Nov–Apr)":   "high",       # irrigated rice and vegetables; nutsedge dominates
            "Land prep (Apr–May)":    "high",       # critical window before transplanting
            "Harvest period (Oct)":   "medium",     # volunteer rice and weed seed dispersal
        },
        "best_control_practices": [
            "Water management: maintain 5–10 cm flood depth in paddy fields to suppress barnyard grass",
            "Alternate wetting and drying (AWD) timing adjusted to minimise nutsedge establishment",
            "Bensulfuron-methyl + pretilachlor (Londax combo) for lowland paddy weeds",
            "System of Rice Intensification (SRI): wider spacing + mechanical weeding outcompetes weeds",
            "Drone-based herbicide application in terraced/flood-prone areas where tractor access is limited",
            "Integrated pest-weed management calendars aligned to IRRI protocols",
        ],
    },

    "Latin America": {
        "common_weeds": [
            "Palmer amaranth (Amaranthus palmeri)",
            "Hairy beggarticks (Bidens pilosa)",
            "Southern crabgrass (Digitaria ciliaris)",
            "Morningglory (Ipomoea spp.)",
            "Alexander grass (Brachiaria plantaginea)",
            "Common purslane (Portulaca oleracea)",
            "Tropical spiderwort (Commelina benghalensis)",
        ],
        "seasonal_risk": {
            "Summer (Nov–Feb, Southern Hemisphere)": "critical",   # soy/corn growing season — peak weed pressure
            "Autumn (Mar–Apr)":                      "high",       # second-crop (safrinha) establishment
            "Winter (May–Aug)":                      "low",        # pasture recovery; off-season management
            "Spring (Sep–Oct)":                      "high",       # pre-planting pressure in no-till systems
        },
        "best_control_practices": [
            "No-till with cover crops (brachiaria, crotalaria) to suppress broadleaf weeds in Cerrado",
            "INTEGRATED RESISTANCE MANAGEMENT: rotate glyphosate with PPO inhibitors + synthetic auxins",
            "Harvest weed seed control (chaff collection or narrow windrow burning) to cut weed seed bank",
            "Precision farming: variable-rate herbicide maps from satellite NDVI + NDWI indices",
            "Community resistance monitoring via HRAC Brazil network for early detection of resistant biotypes",
            "Biological control of tropical spiderwort with fungal pathogens (Bipolaris commelinae)",
        ],
    },
}

# ── Validation ────────────────────────────────────────────────────────────────
EXPECTED_REGIONS = {
    "North America", "South Asia", "Sub-Saharan Africa",
    "Europe", "Southeast Asia", "Latin America"
}
assert set(REGIONAL_INTELLIGENCE.keys()) == EXPECTED_REGIONS, (
    f"Missing/extra regions: {set(REGIONAL_INTELLIGENCE.keys()) ^ EXPECTED_REGIONS}"
)

for _region, _data in REGIONAL_INTELLIGENCE.items():
    assert _data.get("common_weeds"),          f"{_region}: common_weeds is empty"
    assert _data.get("seasonal_risk"),         f"{_region}: seasonal_risk is empty"
    assert _data.get("best_control_practices"), f"{_region}: best_control_practices is empty"

# ── Cost-Impact Connector Function ────────────────────────────────────────────
def cost_impact_connector(
    confidence: float,
    weed_severity: int,
    baseline_cost_usd_ha: float = 119.09,
    baseline_yield_loss_pct: float = 30.0,
) -> dict:
    """
    Compute the cost-impact of AI-assisted detection given prediction confidence
    and detected weed/disease severity.

    Parameters
    ----------
    confidence            : Model prediction confidence [0.0 – 1.0]
    weed_severity         : Severity score {0 = healthy, 1 = low, 2 = medium, 3 = high}
    baseline_cost_usd_ha  : Baseline pesticide cost (USD/ha); default = $119.09 (2022 global)
    baseline_yield_loss_pct: Baseline yield loss % without AI; default = 30%

    Returns
    -------
    dict with:
        pesticide_reduction_pct : % reduction in pesticide use enabled by AI
        cost_savings_usd_ha     : Pesticide cost saved per hectare (USD)
        yield_improvement_pct   : % improvement in yield retention
    """
    # ── Input validation ──────────────────────────────────────────────────────
    if not (0.0 <= confidence <= 1.0):
        raise ValueError(f"confidence must be in [0, 1]. Got: {confidence}")
    if weed_severity not in (0, 1, 2, 3):
        raise ValueError(f"weed_severity must be 0/1/2/3. Got: {weed_severity}")

    # ── Pesticide reduction logic ─────────────────────────────────────────────
    # Core idea: high confidence + high severity → large targeted reduction
    # (confident early detection means only the affected zone is treated,
    #  eliminating prophylactic broad-spectrum application).
    #
    # Severity 0 (healthy): no pesticide needed → 100% reduction vs. blanket spray
    # Severity 1 (low)    : precision spot-spray replaces 60–80% of area spray
    # Severity 2 (medium) : targeted application replaces 30–60% of area spray
    # Severity 3 (high)   : full-field treatment still needed but optimised timing

    # Severity baseline reduction ceilings (max achievable at 100% confidence)
    _MAX_REDUCTION = {0: 1.00, 1: 0.75, 2: 0.45, 3: 0.22}

    # Confidence-weighted reduction: scales linearly with confidence
    _max_red  = _MAX_REDUCTION[weed_severity]
    pesticide_reduction_pct = round(_max_red * confidence * 100, 2)

    # Cost savings per hectare
    cost_savings_usd_ha = round(baseline_cost_usd_ha * (_max_red * confidence), 2)

    # ── Yield improvement logic ───────────────────────────────────────────────
    # AI early detection enables earlier intervention → recovers yield loss.
    # Recovery fraction depends on severity (higher severity = higher potential gain)
    # modulated by confidence (low confidence → incomplete intervention).
    #
    # Recovery factor: fraction of baseline_yield_loss_pct recoverable
    _RECOVERY_FACTOR = {0: 0.0, 1: 0.35, 2: 0.55, 3: 0.70}

    _recoverable_loss = baseline_yield_loss_pct * _RECOVERY_FACTOR[weed_severity]
    yield_improvement_pct = round(_recoverable_loss * confidence, 2)

    return {
        "confidence":              round(confidence, 4),
        "weed_severity":           weed_severity,
        "pesticide_reduction_pct": pesticide_reduction_pct,
        "cost_savings_usd_ha":     cost_savings_usd_ha,
        "yield_improvement_pct":   yield_improvement_pct,
    }


# ── Validate cost_impact_connector returns valid numbers ─────────────────────
_test_inputs = [
    (0.95, 3),  # high confidence, high severity
    (0.75, 2),  # medium confidence, medium severity
    (0.50, 1),  # low confidence, low severity
    (0.99, 0),  # healthy — no treatment needed
    (0.30, 3),  # low confidence, high severity
]

connector_results = []
for _conf, _sev in _test_inputs:
    _res = cost_impact_connector(_conf, _sev)
    connector_results.append(_res)
    # Validate numeric returns
    assert isinstance(_res["pesticide_reduction_pct"], float), "pesticide_reduction_pct not float"
    assert isinstance(_res["cost_savings_usd_ha"],     float), "cost_savings_usd_ha not float"
    assert isinstance(_res["yield_improvement_pct"],   float), "yield_improvement_pct not float"
    assert 0 <= _res["pesticide_reduction_pct"] <= 100, "pesticide_reduction_pct out of range"
    assert _res["cost_savings_usd_ha"] >= 0,            "cost_savings_usd_ha negative"
    assert _res["yield_improvement_pct"] >= 0,          "yield_improvement_pct negative"

connector_results_df = pd.DataFrame(connector_results)

# ── Print Regional Intelligence Summary ──────────────────────────────────────
print("=" * 70)
print("  REGIONAL INTELLIGENCE — COVERAGE VALIDATION")
print("=" * 70)
for _region, _data in REGIONAL_INTELLIGENCE.items():
    _seasons = list(_data["seasonal_risk"].keys())
    _peak = [s for s, r in _data["seasonal_risk"].items() if r == "critical"]
    print(f"\n  {_region}")
    print(f"    Weeds tracked  : {len(_data['common_weeds'])}")
    print(f"    Seasons mapped : {len(_seasons)}")
    print(f"    Critical season: {_peak[0] if _peak else 'none'}")
    print(f"    Control methods: {len(_data['best_control_practices'])}")

print("\n" + "=" * 70)
print("  COST-IMPACT CONNECTOR — VALIDATION RESULTS")
print("=" * 70)
print(f"  {'Confidence':>12}  {'Severity':>9}  {'Pest. Reduction %':>18}  {'Cost Savings $/ha':>18}  {'Yield Impr. %':>14}")
print("  " + "─" * 80)
for _r in connector_results:
    print(
        f"  {_r['confidence']:>12.2f}  {_r['weed_severity']:>9}  "
        f"{_r['pesticide_reduction_pct']:>17.2f}%  "
        f"${_r['cost_savings_usd_ha']:>17.2f}  "
        f"{_r['yield_improvement_pct']:>13.2f}%"
    )

print("\n✅ Regional intelligence validated — 6 regions, all fields populated.")
print("✅ Cost-impact connector validated — returns valid numbers for all test cases.")
