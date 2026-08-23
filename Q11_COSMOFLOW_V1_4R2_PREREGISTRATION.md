# Q11 × COSMOFLOW V1.4R2 — CROSS-RUNNER REPRODUCIBILITY AUDIT

Status: PREREGISTERED — DIAGNOSTIC ONLY / NO RUNNER FIX / NO HASH RELAXATION
Date: 2026-08-23
Parent: `Q11_COSMOFLOW_V1_4R_PREREGISTRATION.md`

## Trigger for this superseding diagnostic

V1.4R single-worker forensic execution produced two byte-identical regenerations matching the frozen V1.1R container and decoded-array fingerprints. During the same PR state, the independent V1.2 workflow again regenerated `raw_baseline.npz` as `2c810b1801e55e783c839003e34179809071c0861392a6ea0b5b973e7951cf33` and correctly stopped at its frozen byte gate.

Therefore a single-worker test cannot distinguish a worker-dependent numerical difference from other cross-runner effects.

## Evidence firewall

V1.4R2:

- does not modify `run_v1_1.py`;
- does not modify `run_v1_2.py`;
- does not change any expected hash;
- does not call any Q11 scoring stage;
- does not change prior results or classifications;
- treats each CI worker as an independent reproducibility replicate.

## Procedure

Run the existing V1.4R forensic script independently on four GitHub-hosted `ubuntu-22.04` matrix workers using the same Python 3.8.18 and locked package set. Each worker executes the existing V1.1 runner twice and records whole-container hashes, uncompressed `.npy` member hashes, decoded canonical array hashes, and environment details.

## Classification

Cross-runner interpretation is mechanical:

- `CROSS_RUNNER_BYTE_STABLE`: all workers report `BYTE_IDENTICAL`.
- `CROSS_RUNNER_SERIALIZATION_VARIANCE`: at least one worker reports `SERIALIZATION_ONLY`, none reports decoded numerical mismatch.
- `CROSS_RUNNER_NUMERICAL_VARIANCE`: at least one worker reports `NUMERICAL_CONTENT_MISMATCH` or `INTERNAL_NONDETERMINISM`.
- `CROSS_RUNNER_INCONCLUSIVE`: one or more workers fail to produce a valid report.

No physical or Q11 claim follows from any of these labels.
