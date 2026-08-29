# Q11 × COSMOFLOW V1.4R4 — DURABLE CANONICAL REFERENCE PACKAGING + MERGE-GATE INTEGRATION

Status: PREREGISTERED — PROSPECTIVE INFRASTRUCTURE REPAIR
Date: 2026-08-23
Parent evidence: `Q11_COSMOFLOW_V1_4R3_FINAL_FREEZE.md`

## Purpose

Remove the finite-retention dependency from the V1.4R3 portable gate by packaging the canonical V1.1R decoded arrays inside repository history and using that repository-backed reference for a PR-triggered merge gate.

This stage does not recompute Q11 scores, family ranks, RMSE competitions, V1.2–V1.4 scientific classifications, or historical expected byte hashes.

## Durable canonical reference

Repository path:

`q11_forensics/reference/v1.1r_canonical_arrays.json`

The file is restored from the exact Git blob previously materialized from the original V1.1R artifact, rather than regenerated from a new baseline execution.

Required embedded provenance:

- original artifact ID: `9437578374`
- original workflow run: `32456990085`
- original head commit: `616f8b49e99cf19bca3bfd97f5ae506443246748`
- original raw baseline SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

The gate MUST abort if these provenance fields do not match exactly.

## Numerical acceptance rule

The V1.4R4 merge gate inherits the frozen V1.4R3 criteria without modification:

1. keys exactly `N`, `field_field`, `field_field_field`, `k`;
2. shapes equal to the durable reference;
3. all values finite;
4. `N` bit-identical;
5. `k` bit-identical;
6. `field_field`: element-wise relative tolerance `1e-10`, absolute tolerance `0`;
7. `field_field_field`: element-wise relative tolerance `1e-5`, absolute tolerance `0`;
8. no clipping, smoothing, epsilon substitution, feature-based substitution, or post-run threshold adjustment.

## Merge-gate rule

A PR-triggered V1.4R4 workflow is a blocking CI signal by behavior: a non-PASS numerical classification exits non-zero. Repository branch-protection configuration is outside this repository-file stage and is not claimed unless separately verified.

Classification:

- `PASS_DURABLE_PORTABLE_GATE`
- `FAIL_DURABLE_REFERENCE_PROVENANCE`
- `FAIL_STRUCTURE_OR_FINITE`
- `FAIL_PORTABLE_NUMERICAL_EQUIVALENCE`

## Firewall

V1.4R4 MUST NOT modify upstream CosmoFlow physics modules, `q11_cosmoflow/run_v1_1.py`, historical V1.2 expected hashes, historical preregistrations, or final-freeze records. A V1.4R4 PASS is prospective infrastructure evidence only and does not relabel historical failed CI runs as PASS.
