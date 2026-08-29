# Q11 × COSMOFLOW V1.4 — OUT-OF-SAMPLE PHYSICS AUDIT

Status: PREREGISTERED — NO V1.4 SCORE MAY BE INSPECTED BEFORE THIS FILE AND ITS RUNNER ARE COMMITTED
Date: 2026-08-21
Parent evidence: `Q11_COSMOFLOW_V1_3_FINAL_FREEZE.md`

## Evidence firewall

V1.4 tests the V1.3 result under new, fixed physical configurations. The upstream `CosmoFlow/Massless_dphi3` source tree is never edited in the checkout. For each run the runner copies that tree to a temporary directory and changes only the two literal configuration lines listed below in the copied `MyFirstRun.py`; the copied script then executes unchanged. The source-file SHA256 values and each materialized raw-output SHA256 are recorded.

## Fixed out-of-sample configurations

Each configuration uses `Nfield=1`, the original tolerance and output grid, and the following exact replacements in the copied example:

- `D3_EQ`: `DeltaN = 3`; `k1, k2, k3 = k, k, k`
- `D5_EQ`: `DeltaN = 5`; `k1, k2, k3 = k, k, k`
- `D4_SQ`: `DeltaN = 4`; `k1, k2, k3 = k, k, 0.5 * k`

All three configurations must output exactly 1000 finite samples for `abs(field_field)` and `abs(field_field_field)`. A failing configuration is recorded as invalid and is not silently replaced.

## Frozen scoring rule

For every valid configuration, use the V1.3 representation grid unchanged: partitions P334 `[0,334,667,1000]`, P250 `[0,250,750,1000]`, P400 `[0,400,600,1000]`; summaries GM, AM, RMS; ascending sorted amplitudes; centered log-RMSE; exhaustive 42 primitive integer triples from 1 through 6; and tie tolerance `1e-12`.

`1:1:6` is `OUT_OF_SAMPLE_STABLE` only if it is uniquely pooled rank 1 in all 27 valid configuration-representation cells and never below rank 3 in either target-specific score. Otherwise it is `OUT_OF_SAMPLE_SENSITIVE`. Q11 (`1:2:3`) is descriptive only.
