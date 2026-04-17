
import pandas as pd

# ── Helper: quick profile ──────────────────────────────────────────────────
def profile(name, df):
    print(f"\n{'═'*55}")
    print(f"  {name}  ({df.shape[0]} rows × {df.shape[1]} cols)")
    print(f"{'═'*55}")
    null_counts = df.isnull().sum()
    print(f"Null counts:\n{null_counts.to_string()}")
    print(f"\nDtypes:\n{df.dtypes.to_string()}")
    print(f"\nDescriptive stats:")
    print(df.describe(include="all").to_string())

profile("pesticide_usage_df", pesticide_usage_df)
profile("cost_df",            cost_df)
profile("yield_loss_df",      yield_loss_df)
profile("env_df",             env_df)

# ── Validation checks ──────────────────────────────────────────────────────
print("\n\n── Validation ──────────────────────────────────────────────────────")

# 1. No nulls expected
for _name, _df in [("usage", pesticide_usage_df), ("cost", cost_df),
                    ("yield_loss", yield_loss_df), ("env", env_df)]:
    _n_null = _df.isnull().sum().sum()
    print(f"  {_name}: {_n_null} nulls {'✅' if _n_null == 0 else '⚠️'}")

# 2. Usage values positive
assert (pesticide_usage_df[["herbicides","insecticides","fungicides","other"]] > 0).all().all()
print("  Usage values all positive ✅")

# 3. Yield-loss percentages in [0, 100]
loss_cols = ["weeds_pct","insects_pct","pathogens_pct","viruses_pct","nematodes_pct","total_loss_pct"]
for _col in loss_cols:
    assert yield_loss_df[_col].between(0, 100).all(), f"{_col} out of range"
print("  Yield-loss % all in [0,100] ✅")

# 4. Cost values positive
assert (cost_df.drop(columns="year") > 0).all().all()
print("  Cost values all positive ✅")

# 5. EIQ scores in [0, 100]
assert env_df["eiq_score"].between(0, 100).all()
print("  EIQ scores all in [0,100] ✅")

# ── Quick summary ──────────────────────────────────────────────────────────
print("\n\n── Key ranges ───────────────────────────────────────────────────────")
print(f"  Usage total  : {pesticide_usage_df['total'].min():.0f} – "
      f"{pesticide_usage_df['total'].max():.0f} kt active ingredient")
print(f"  Cost / ha    : ${cost_df['total_usd_ha'].min():.2f} – "
      f"${cost_df['total_usd_ha'].max():.2f}")
print(f"  Max yield loss (single crop): "
      f"{yield_loss_df['total_loss_pct'].max()}% "
      f"({yield_loss_df.loc[yield_loss_df['total_loss_pct'].idxmax(),'crop']})")
print(f"  Highest EIQ  : {env_df.loc[env_df['eiq_score'].idxmax(),'category']} "
      f"({env_df['eiq_score'].max()})")
