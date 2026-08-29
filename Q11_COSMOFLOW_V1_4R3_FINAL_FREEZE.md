# Q11 × COSMOFLOW V1.4R3 — PORTABLE REPRODUCIBILITY GATE FINAL FREEZE

Status: PASS (prospective portable numerical-equivalence gate)
Date: 2026-08-23
Preregistration: `Q11_COSMOFLOW_V1_4R3_PREREGISTRATION.md`
Implementation head: `64959e7126542fd28319ac352322da0056e828a1`
Validation-matrix head: `62050f5fc9743fe6d31d59da7cff9086cb74035c`

## Purpose

V1.4R3 replaces byte-identical NPZ matching as the proposed prospective portability criterion with decoded numerical-content checks. Historical V1.2 records and their failed byte-hash gates are not rewritten or reclassified.

## Frozen gate

Canonical V1.1R reference:

- artifact ID: `9437578374`
- workflow run: `32456990085`
- `raw_baseline.npz` SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Acceptance rules frozen before V1.4R3 execution:

- exact key set and shapes;
- all values finite;
- `N`: exact equality;
- `k`: exact equality;
- `field_field`: element-wise relative tolerance `1e-10`, absolute tolerance `0`;
- `field_field_field`: element-wise relative tolerance `1e-5`, absolute tolerance `0`;
- no clipping, smoothing, epsilon replacement, or post-run threshold adjustment.

These tolerances are infrastructure portability criteria informed by the already-frozen V1.4R2 CPU-variance audit. They are not statistical uncertainty estimates and are not scientific significance thresholds.

## Primary V1.4R3 CI result

Workflow run: `32611314290`
Conclusion: `success`
Runner CPU: `AMD EPYC 7763 64-Core Processor`
Classification: `PASS_PORTABLE_NUMERICAL_EQUIVALENCE`

The generated current baseline was byte-identical to the V1.1R reference on this runner:

`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

All four arrays passed their registered gates. No Q11 scoring was performed.

Primary artifact:

- artifact ID: `9485603772`
- name: `q11-cosmoflow-v1-4r3-portable-gate`
- ZIP digest: `sha256:c579daa02c1a44876c2391fd3a92dc01d337851123054fb15997767cbe6724e6`
- `portable_gate_report.json`: `eebca46f2ac068a43c6136c7ba5fb2bc0b967610066065b07067200131f77fce`
- environment freeze: `698c945c5a78bcba7c61d2c080b9c4e8eeef45f0a1d08b5ee73ed1e0cdd6178d`
- gate log: `44ded7536f6195236c5ca6ee3a0a11afbd6591d43970d6c4f830c0aef01d4de6`

## Four-worker validation matrix

Workflow run: `32611355956`
Conclusion: all 4 jobs `success`

Artifacts:

- replicate 1: artifact `9485616510`, ZIP digest `sha256:1476aaafc4d3ac0071b741c692e5e6846a9abfdd6c282ab52cd552faabfaa36f`
- replicate 2: artifact `9485615195`, ZIP digest `sha256:8a56fb0aa224c615c6d86fe7c57f68ccbf69b047eaaf9a4fd996c8b900d493d0`
- replicate 3: artifact `9485614718`, ZIP digest `sha256:9b7627013a6f339fa690ad22f292e06274613a8d70e4322546a5166552b4cba4`
- replicate 4: artifact `9485615178`, ZIP digest `sha256:a65859ecbae4f7b800ff84e4bb2b52a9398785cef799ed28735938de083307e7`

All four matrix workers happened to run on `AMD EPYC 7763 64-Core Processor`, and all four produced the original V1.1R byte hash with zero decoded-array differences. Therefore this matrix confirms repeatability but does not by itself constitute a fresh Intel CI validation.

## Cross-architecture validation against frozen V1.4R2 evidence

V1.4R2 had already frozen Intel Xeon outputs before the V1.4R3 thresholds were executed. Applying the V1.4R3 rules to those preserved Intel arrays gives:

- `field_field` maximum relative difference: `3.020716468182771e-11`, below the frozen `1e-10` limit;
- `field_field_field` maximum relative difference: `2.6815178008940224e-06`, below the frozen `1e-5` limit;
- `N` and `k`: bit-identical.

Thus the frozen V1.4R3 criterion accepts both the observed AMD/V1.1R output family and the previously frozen Intel output family without altering thresholds after V1.4R3 execution.

This is an infrastructure portability conclusion only. It does not alter any Q11 family score, ranking, RMSE, or scientific interpretation.

## Evidence firewall

- `q11_cosmoflow/run_v1_1.py`: unchanged by V1.4R3.
- `q11_cosmoflow/run_v1_2.py`: unchanged by V1.4R3.
- upstream CosmoFlow physics modules: unchanged by V1.4R3.
- historical expected hashes and final-freeze records: unchanged.
- Q11 scoring performed in V1.4R3: FALSE.

A V1.4R3 PASS does not retroactively label the failed V1.2 PR-triggered byte-hash runs as PASS. It establishes a prospective CPU-portable numerical-equivalence gate for later integration.

## Operational limitation

The current workflow fetches canonical reference artifact `9437578374`, whose GitHub Actions retention is finite. Before V1.4R3 becomes the long-term merge gate, the canonical V1.1R reference must be persisted in a non-expiring repository/release-backed form or the workflow will eventually lose access to its reference. This is an operational durability blocker, not a numerical reproducibility failure.

## Queue result

V1.4R3 = `PASS_PORTABLE_NUMERICAL_EQUIVALENCE` for the observed AMD output family and the previously frozen Intel output family under the registered tolerances.

Long-term integration status: `PASS_WITH_REFERENCE_RETENTION_BLOCKER`.
