# 🌿 Pesticide Savings Calculator API
### Developer Reference · v1.0.0

> **Quick Start** — You can be up and running in under 2 minutes. Jump to [§ Quick Start](#quick-start) if you're in a hurry.

---

## Endpoint Reference

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `GET` | `/health` | Service health check — returns status and version | None |
| `POST` | `/calculate` | Calculate pesticide reduction & cost savings for a farm | None |

**Base URL:** `https://<your-deployment-host>`  
**Protocol:** HTTPS · **Format:** JSON · **API Version:** `1.0.0`

---

## Schemas

### `POST /calculate` — Request Body · `CalculateRequest`

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `farm_size_acres` | `float` | ✅ | `> 0` | Total farm area in acres |
| `pesticide_usage_kg_per_acre` | `float` | ✅ | `> 0` | Current pesticide application rate (kg / acre) |
| `ai_efficiency_percent` | `float` | ✅ | `20.0 – 40.0` | AI detection efficiency improvement (%). Linear interpolation is applied for non-integer values |
| `crop_type` | `string` | ❌ | — | Optional crop name for context (e.g. `"wheat"`, `"corn"`, `"soybeans"`). Does **not** affect the calculation |

```json
// CalculateRequest — full example
{
  "farm_size_acres": 500.0,
  "pesticide_usage_kg_per_acre": 2.0,
  "ai_efficiency_percent": 30.0,
  "crop_type": "corn"
}
```

---

### `POST /calculate` — Response Body · `CalculateResponse`

| Field | Type | Description |
|-------|------|-------------|
| `farm_size_acres` | `float` | Farm area in acres (echoed from request) |
| `farm_size_ha` | `float` | Farm area converted to hectares (1 acre = 0.404686 ha) |
| `crop_type` | `string \| null` | Crop type provided by caller (informational) |
| `ai_efficiency_percent` | `float` | AI efficiency % used for this calculation |
| `traditional_usage_kg` | `float` | Total pesticide under traditional methods (kg) |
| `ai_usage_kg` | `float` | Total pesticide with AI-assisted detection (kg) |
| `pesticide_reduction_kg` | `float` | Pesticide eliminated by AI (kg) |
| `efficiency_improvement_pct` | `float` | % of pesticide use eliminated |
| `traditional_cost_usd` | `float` | Baseline pesticide cost, USD (from $119.09/ha benchmark) |
| `ai_cost_usd` | `float` | Pesticide cost with AI, USD |
| `cost_savings_usd` | `float` | Total cost saved by adopting AI, USD |
| `summary` | `string` | Plain-language narrative summary of savings |

```json
// CalculateResponse — full example
{
  "farm_size_acres": 500.0,
  "farm_size_ha": 202.343,
  "crop_type": "corn",
  "ai_efficiency_percent": 30.0,
  "traditional_usage_kg": 1000.0,
  "ai_usage_kg": 803.6,
  "pesticide_reduction_kg": 196.4,
  "efficiency_improvement_pct": 19.64,
  "traditional_cost_usd": 24106.97,
  "ai_cost_usd": 18891.17,
  "cost_savings_usd": 5215.8,
  "summary": "On a 500.0-acre farm for corn, AI-assisted pest detection at 30% efficiency is projected to reduce pesticide use by 196.4 kg (19.6%), saving approximately $5,215.80 in pesticide costs (from $24,106.97 down to $18,891.17)."
}
```

---

### `GET /health` — Response Body · `HealthResponse`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | `"ok"` when the service is healthy |
| `version` | `string` | API version string (e.g. `"1.0.0"`) |

```json
{ "status": "ok", "version": "1.0.0" }
```

---

### Error Response (HTTP 422 — Validation Error)

Returned by FastAPI / Pydantic when required fields are missing or constraints are violated.

| Field | Type | Description |
|-------|------|-------------|
| `detail` | `array` | List of validation error objects |
| `detail[].loc` | `array` | Location of the offending field (e.g. `["body", "ai_efficiency_percent"]`) |
| `detail[].msg` | `string` | Human-readable error message |
| `detail[].type` | `string` | Pydantic error type identifier |

```json
// 422 example — ai_efficiency_percent out of range
{
  "detail": [
    {
      "loc": ["body", "ai_efficiency_percent"],
      "msg": "Value error, ai_efficiency_percent must be between 20 and 40 (inclusive). Received: 75.",
      "type": "value_error"
    }
  ]
}
```

---

## AI Efficiency Benchmarks

Efficiency fractions are linearly interpolated between the three calibrated anchor points derived from the canvas simulation:

| AI Efficiency | Pesticide Reduction | Cost Reduction | $/ha Saved |
|:-------------:|:-------------------:|:--------------:|:----------:|
| 20% | 13.09% | 14.43% | $17.18 |
| 30% | 19.64% | 21.64% | $25.77 |
| 40% | 26.19% | 28.86% | $34.37 |

**Baseline cost:** `$119.09 / ha` · **Conversion:** `1 acre = 0.404686 ha`

---

## cURL Examples

### 1️⃣ Small Farm — 50 acres, moderate usage, AI 20%

```bash
curl -X POST "https://<your-deployment-host>/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "farm_size_acres": 50.0,
    "pesticide_usage_kg_per_acre": 1.5,
    "ai_efficiency_percent": 20.0,
    "crop_type": "wheat"
  }'
```

### 2️⃣ Large Farm — 2,000 acres, heavy usage, AI 30%

```bash
curl -X POST "https://<your-deployment-host>/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "farm_size_acres": 2000.0,
    "pesticide_usage_kg_per_acre": 3.5,
    "ai_efficiency_percent": 30.0,
    "crop_type": "corn"
  }'
```

### 3️⃣ Invalid Input — `ai_efficiency_percent` out of range (error handling demo)

```bash
curl -X POST "https://<your-deployment-host>/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "farm_size_acres": 200.0,
    "pesticide_usage_kg_per_acre": 2.0,
    "ai_efficiency_percent": 75.0
  }'
```

**Expected HTTP 422 response:**
```json
{
  "detail": [
    {
      "loc": ["body", "ai_efficiency_percent"],
      "msg": "Value error, ai_efficiency_percent must be between 20 and 40 (inclusive). Received: 75.0.",
      "type": "value_error"
    }
  ]
}
```

### Health Check

```bash
curl "https://<your-deployment-host>/health"
# → {"status":"ok","version":"1.0.0"}
```

---

## Python `requests` Examples

```python
import requests

BASE_URL = "https://<your-deployment-host>"

# ── Example 1: Small Farm (50 acres) ──────────────────────────────────────────
response = requests.post(
    f"{BASE_URL}/calculate",
    json={
        "farm_size_acres": 50.0,
        "pesticide_usage_kg_per_acre": 1.5,
        "ai_efficiency_percent": 20.0,
        "crop_type": "wheat",
    },
)
response.raise_for_status()
result = response.json()
print(f"Cost savings: ${result['cost_savings_usd']:,.2f}")
print(f"Pesticide reduction: {result['pesticide_reduction_kg']:.1f} kg ({result['efficiency_improvement_pct']:.1f}%)")
print(result["summary"])

# ── Example 2: Large Farm (2,000 acres) ───────────────────────────────────────
response = requests.post(
    f"{BASE_URL}/calculate",
    json={
        "farm_size_acres": 2000.0,
        "pesticide_usage_kg_per_acre": 3.5,
        "ai_efficiency_percent": 30.0,
        "crop_type": "corn",
    },
)
result = response.json()
print(f"Cost savings: ${result['cost_savings_usd']:,.2f}")

# ── Example 3: Error Handling ─────────────────────────────────────────────────
response = requests.post(
    f"{BASE_URL}/calculate",
    json={
        "farm_size_acres": 200.0,
        "pesticide_usage_kg_per_acre": 2.0,
        "ai_efficiency_percent": 75.0,  # invalid — must be 20–40
    },
)
if response.status_code == 422:
    errors = response.json()["detail"]
    for err in errors:
        print(f"Validation error on '{err['loc'][-1]}': {err['msg']}")
```

---

## Expected Outputs for the Three Example Inputs

| Scenario | Farm Size | Usage Rate | AI Efficiency | Farm (ha) | Trad. Usage (kg) | Reduction (kg) | Reduction % | Trad. Cost ($) | AI Cost ($) | **Savings ($)** |
|----------|-----------|-----------|:-------------:|:---------:|:-----------------:|:--------------:|:-----------:|:--------------:|:-----------:|:---------------:|
| Small Farm | 50 acres | 1.5 kg/acre | 20% | 20.23 ha | 75.0 kg | 9.8 kg | 13.09% | $2,410.70 | $2,063.22 | **$347.47** |
| Large Farm | 2,000 acres | 3.5 kg/acre | 30% | 809.37 ha | 7,000.0 kg | 1,374.8 kg | 19.64% | $96,427.49 | $75,579.32 | **$20,848.17** |
| Invalid Input | 200 acres | 2.0 kg/acre | 75% | — | — | — | — | — | — | **HTTP 422 ❌** |

> **Note on rounding:** Response values are rounded to 2 decimal places. The `summary` field provides a narrative description suitable for reports.

---

## Quick Start

Get results in 4 steps:

**1. Check the service is up**
```bash
curl https://<your-deployment-host>/health
```

**2. Send your first calculation**
```bash
curl -X POST "https://<your-deployment-host>/calculate" \
  -H "Content-Type: application/json" \
  -d '{"farm_size_acres": 500, "pesticide_usage_kg_per_acre": 2.0, "ai_efficiency_percent": 30}'
```

**3. Parse the response** — grab `cost_savings_usd`, `pesticide_reduction_kg`, and `summary` for your report or dashboard.

**4. Explore the interactive docs** — visit `https://<your-deployment-host>/docs` for the auto-generated Swagger UI where you can try every endpoint in-browser.

---

### Key Constraints to Remember

| Rule | Detail |
|------|--------|
| `ai_efficiency_percent` range | Must be **20 – 40** (inclusive). Values outside this range return HTTP 422 |
| `farm_size_acres` | Must be **> 0** |
| `pesticide_usage_kg_per_acre` | Must be **> 0** |
| `crop_type` | Optional. Included in response & summary but does not affect numbers |
| Interpolation | Values between 20–40 are **linearly interpolated** from the three benchmark anchor points |

---

*Benchmarks derived from a multi-scenario global pesticide simulation (canvas analysis, 2022 dataset). Baseline: $119.09/ha · 1 acre = 0.404686 ha.*
