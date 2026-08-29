# Q11 × COSMOFLOW V1.4R4B — LOSSLESS CANONICAL BINARY PACKAGING

Status: PREREGISTERED — PROSPECTIVE INFRASTRUCTURE REPAIR
Date: 2026-08-23
Parent evidence: `Q11_COSMOFLOW_V1_4R4_PREREGISTRATION.md`

## Purpose

Replace the lossy/encoded durable-reference layer with the original V1.1R `raw_baseline.npz` bytes committed directly into repository history. The canonical binary is verified by SHA256 before decode and is the sole numerical reference for the permanent portable gate.

This stage is infrastructure only. It does not recompute Q11 scores, family ranks, RMSE competitions, p-values, or scientific classifications.

## Canonical source lock

The only permitted source is the original V1.1R GitHub Actions artifact:

- artifact ID: `9437578374`
- workflow run: `32456990085`
- head commit: `616f8b49e99cf19bca3bfd97f5ae506443246748`
- canonical file: `artifacts/v1.1/raw_baseline.npz`
- canonical SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`
- canonical byte size observed from the source artifact: `19506`

The packaging workflow MUST verify the source SHA256 before copying or committing the file. A regenerated baseline MUST NOT be substituted for the source artifact.

## Durable binary location

The exact source bytes will be committed unchanged at:

`q11_cosmoflow/canonical/v1.1r/raw_baseline.npz`

A provenance manifest will be committed at:

`q11_cosmoflow/canonical/v1.1r/CANONICAL_REFERENCE.md`

No JSON conversion, decimal rendering, float reserialization, base64 payload, split text payload, `np.savez`, or `np.savez_compressed` recreation is allowed in the canonical packaging path.

## Permanent R4B gate

Before `np.load` or any numerical comparison, the gate MUST verify that the repository-backed canonical binary SHA256 equals:

`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

After integrity verification, the gate inherits the V1.4R3 numerical acceptance criteria unchanged:

1. keys exactly `N`, `field_field`, `field_field_field`, `k`;
2. equal shapes;
3. all values finite;
4. `N` exact;
5. `k` exact;
6. `field_field`: element-wise rtol `1e-10`, atol `0`;
7. `field_field_field`: element-wise rtol `1e-5`, atol `0`;
8. no clipping, smoothing, epsilon substitution, feature substitution, or post-run threshold adjustment.

## Classification

- `PASS_LOSSLESS_CANONICAL_BINARY_GATE`
- `FAIL_CANONICAL_BINARY_INTEGRITY`
- `FAIL_STRUCTURE_OR_FINITE`
- `FAIL_PORTABLE_NUMERICAL_EQUIVALENCE`

## Historical firewall

V1.4R4B MUST NOT modify upstream CosmoFlow physics modules, `q11_cosmoflow/run_v1_1.py`, historical V1.2 expected hashes, historical preregistrations, or historical final-freeze records. Prior failed byte-level checks remain historical failures. An R4B PASS is prospective reproducibility infrastructure evidence only and does not alter scientific interpretation.

## Merge-gate integration rule

The permanent R4B workflow is intended to provide a fail-closed PR CI signal using the repository-backed canonical binary. Whether GitHub enforces that signal as a required status check depends on repository branch-protection/ruleset configuration and MUST NOT be claimed unless separately verified.