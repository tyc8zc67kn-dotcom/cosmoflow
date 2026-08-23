# Q11 × COSMOFLOW V1.4R3 — PORTABLE REPRODUCIBILITY GATE REPAIR

Status: PREREGISTERED — PROSPECTIVE INFRASTRUCTURE REPAIR
Date: 2026-08-23
Parent evidence: `Q11_COSMOFLOW_V1_4R2_FINAL_FREEZE.md`

## Purpose

V1.4R3 repairs the portability failure identified by V1.4R/V1.4R2 without rewriting V1.1R, V1.2, V1.3, or V1.4 evidence. The prior byte-level gate remains historical evidence and is not edited. No Q11 score, family rank, RMSE competition, or scientific classification is recomputed in this stage.

## Forensic basis

V1.4R2 established that the unchanged CosmoFlow baseline is deterministic within observed CPU families but can differ numerically across CPU architectures. AMD replicates reproduced the frozen V1.1R `raw_baseline.npz` byte-for-byte, while Intel replicates produced different decoded `field_field` and `field_field_field` values. `N` and `k` remained bit-identical.

Largest observed relative differences against V1.1R:

- `field_field`: `3.020716468182771e-11`
- `field_field_field`: `2.6815178008940224e-06`

These observations are infrastructure evidence only.

## Canonical reference

The sole numerical reference is the original V1.1R GitHub Actions artifact:

- artifact ID: `9437578374`
- workflow run: `32456990085`
- head commit: `616f8b49e99cf19bca3bfd97f5ae506443246748`
- `raw_baseline.npz` SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Canonical decoded-array SHA256 references:

- `N`: `d7875947f671da06a7b2337cf74d20d25361d2a949d4b38d2f7634aa60368c97`
- `k`: `8dc7dd6e9f001c5f4dd575bf2754e7c9717af0823c8e522cf2e0abeb290b3157`
- `field_field`: `1b499519284fec668425fc62c34adb7dc58f5b90aa7e9b6b826da3cff7744560`
- `field_field_field`: `8a2da84f5473a2b07afde360ce9291c07bf4000077b367717f4be24163991aaa`

The validation must verify the reference artifact hash before comparison. A mismatch aborts the audit.

## Portable gate

A regenerated baseline passes only if all rules below hold:

1. keys are exactly `N`, `field_field`, `field_field_field`, `k`;
2. shapes match the frozen reference;
3. all values are finite;
4. `N` is bit-identical to reference;
5. `k` is bit-identical to reference;
6. `field_field` satisfies element-wise `abs(x-r) <= 1e-12 + 1e-10 * abs(r)`;
7. `field_field_field` satisfies element-wise `abs(x-r) <= 1e-12 + 5e-6 * abs(r)`;
8. every element must pass; no percentile, aggregate, majority, clipping, smoothing, imputation, or post-run tolerance adjustment is allowed.

The tolerances are frozen before V1.4R3 validation and sit above the maximum cross-CPU relative differences measured in V1.4R2. They are engineering portability criteria, not uncertainty estimates or statistical significance thresholds.

Whole-file NPZ SHA256 and canonical decoded-array hashes remain recorded as provenance, but whole-container byte equality is descriptive and is not required for portable acceptance.

## Validation design

Execute the unchanged V1.1 numerical procedure on four independent GitHub-hosted `ubuntu-22.04` workers with Python 3.8.18 and the locked V1.1 package set.

Each worker must record CPU model, regenerate the baseline, apply the frozen portable gate, and report whole NPZ SHA256, canonical array hashes, maximum absolute and relative differences, and failing-element counts.

No failed or invalid worker may be silently replaced.

Aggregate classification:

- `PASS_PORTABLE_NUMERICAL_EQUIVALENCE`: all four workers satisfy every frozen rule.
- `FAIL_REFERENCE_INTEGRITY`: reference verification fails.
- `FAIL_STRUCTURE_OR_FINITE`: structure/finiteness fails on any worker.
- `FAIL_PORTABLE_NUMERICAL_EQUIVALENCE`: any worker exceeds a numerical criterion.
- `INCONCLUSIVE`: a required worker or reference artifact cannot be evaluated.

## Relationship to V1.2

V1.4R3 MUST NOT modify `q11_cosmoflow/run_v1_1.py`, `q11_cosmoflow/run_v1_2.py`, upstream physics modules, historical expected hashes, preregistrations, or final-freeze records.

A V1.4R3 PASS does not retroactively convert any failed V1.2 CI run into PASS. It establishes only a prospective portable gate. Integration into future blind/scoring workflows requires a later separately versioned stage.

## Evidence firewall

Q11 scoring performed: FALSE.

No scientific result from V1.2/V1.3/V1.4 is altered by this engineering repair.

## Merge gate

PR #1 remains Draft during V1.4R3. A portable PASS is necessary but not sufficient for merge; current CI and evidence-chain consistency must be audited afterward.
