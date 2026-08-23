# Q11 × COSMOFLOW V1.4R3 — PORTABLE REPRODUCIBILITY GATE REPAIR

Status: PREREGISTERED — PROSPECTIVE INFRASTRUCTURE REPAIR
Date: 2026-08-23
Parent evidence: `Q11_COSMOFLOW_V1_4R2_FINAL_FREEZE.md`

## Purpose

V1.4R3 repairs the portability failure identified by V1.4R/V1.4R2 without rewriting V1.1R, V1.2, V1.3, or V1.4 evidence. The prior byte-level gate remains historical evidence and is not edited. No Q11 score, family rank, RMSE competition, or scientific classification is recomputed in this stage.

## Forensic basis

V1.4R2 established that the unchanged CosmoFlow baseline is deterministic within observed CPU families but can differ numerically across CPU architectures. AMD replicates reproduced the frozen V1.1R `raw_baseline.npz` byte-for-byte, while Intel replicates produced different decoded `field_field` and `field_field_field` values. `N` and `k` remained bit-identical.

The largest observed relative differences against the frozen V1.1R reference were approximately:

- `field_field`: `3.020716468182771e-11`
- `field_field_field`: `2.6815178008940224e-06`

These observations are infrastructure evidence, not a scientific effect.

## Canonical reference

The sole numerical reference is the original V1.1R GitHub Actions artifact:

- artifact ID: `9437578374`
- artifact name: `q11-cosmoflow-v1-1-baseline`
- workflow run: `32456990085`
- head commit: `616f8b49e99cf19bca3bfd97f5ae506443246748`
- frozen `raw_baseline.npz` SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

The workflow must verify this SHA256 before using the reference. A mismatch aborts the audit.

## Portable gate

A newly generated baseline passes only if all of the following hold:

1. keys are exactly `N`, `field_field`, `field_field_field`, `k`;
2. all arrays have the same shapes as the V1.1R reference;
3. all values are finite;
4. `N` is bit-identical to the reference;
5. `k` is bit-identical to the reference;
6. `field_field` satisfies element-wise `abs(current-reference) <= 1e-10 * abs(reference)`;
7. `field_field_field` satisfies element-wise `abs(current-reference) <= 1e-5 * abs(reference)`;
8. no additive absolute tolerance, clipping, smoothing, epsilon replacement, or post-run threshold adjustment is allowed.

The two relative tolerances are intentionally frozen above the observed V1.4R2 cross-CPU envelope before any V1.4R3 execution. They are a portability criterion, not an uncertainty estimate and not a statistical significance threshold.

## Classification

- `PASS_PORTABLE_NUMERICAL_EQUIVALENCE`: every rule above passes.
- `FAIL_REFERENCE_INTEGRITY`: canonical reference SHA256 is wrong.
- `FAIL_STRUCTURE_OR_FINITE`: key, shape, or finiteness rule fails.
- `FAIL_PORTABLE_NUMERICAL_EQUIVALENCE`: `N`/`k` differ or either numerical target exceeds its frozen tolerance.

Whole-file NPZ byte equality is recorded descriptively but is no longer the portable acceptance criterion.

## Firewall

V1.4R3 MUST NOT modify `q11_cosmoflow/run_v1_1.py`, `q11_cosmoflow/run_v1_2.py`, upstream CosmoFlow physics modules, historical expected hashes, preregistrations, or final-freeze records. A V1.4R3 PASS does not retroactively convert a failed V1.2 CI run into a historical PASS. It only defines a prospective CPU-portable reproducibility gate for later integration.
