# Q11 × COSMOFLOW V1.4R4B — FINAL FREEZE

Status: PASS — LOSSLESS CANONICAL BINARY GATE
Date: 2026-08-23

## Scope

Infrastructure-only closure of the durable-reference problem. No Q11 scoring, family ranking, RMSE competition, p-value calculation, or scientific reclassification was performed.

## Canonical binary provenance

The original V1.1R Actions artifact was packaged byte-for-byte into repository history by GitHub Actions.

Source:

- artifact ID: `9437578374`
- workflow run: `32456990085`
- source head commit: `616f8b49e99cf19bca3bfd97f5ae506443246748`
- source path: `artifacts/v1.1/raw_baseline.npz`
- byte size: `19506`
- SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Repository freeze:

- packaging commit: `d93180725dc92b51bc2802e40caba59188840d98`
- repository path: `q11_cosmoflow/canonical/v1.1r/raw_baseline.npz`
- provenance manifest: `q11_cosmoflow/canonical/v1.1r/CANONICAL_REFERENCE.md`

The packaging workflow verified SHA256 and byte size before committing. The canonical path does not pass through JSON, decimal rendering, base64 payload, split text payload, or a regenerated NPZ serialization.

## Permanent gate

Workflow: `Q11 CosmoFlow V1.4R4B Lossless Canonical Binary Gate`

PR-triggered run:

- run ID: `32612124189`
- tested head: `f256ab331b7dbd101756edd58a8acb8601f0eaf0`
- result: 4/4 matrix jobs succeeded

Evidence artifacts:

- replicate 1: artifact `9485825688`, digest `sha256:112601f8203e6ea00ff8a92034d3592fc69ef973c4ad5873af467d189afa05f0`
- replicate 2: artifact `9485829721`, digest `sha256:8b2460fbffebb011b6b6f878e8fda5c89440ebd078bb1045b01ea811f11e9c0a`
- replicate 3: artifact `9485831653`, digest `sha256:4366474e816a7b903ff351c29111d7f2d102c611f4acdb461848e79aaee900f4`
- replicate 4: artifact `9485821965`, digest `sha256:1382496a4f0f01a3eb46ec813c6d16e72a29019ef654e9b658ea95e07215b99f`

Every matrix job passed the pre-decode canonical integrity step and the numerical-equivalence gate.

## Observed cross-CPU evidence in this run

At least one successful R4B job ran on `INTEL(R) XEON(R) PLATINUM 8573C`. For that job:

- canonical SHA256 verified before decode: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`
- generated baseline SHA256: `55a666e07da2c1b1774743734b55298bf9349140bec997d3953d7fa7a12ed440`
- `N`: exact
- `k`: exact
- `field_field`: max relative difference `5.3689117386999085e-11`, below frozen rtol `1e-10`
- `field_field_field`: max relative difference `1.698803925899337e-06`, below frozen rtol `1e-5`
- classification: `PASS_LOSSLESS_CANONICAL_BINARY_GATE`

This is reproducibility-infrastructure evidence, not a scientific effect.

## Interpretation firewall

- Historical V1.2 byte-hash failures remain historical failures.
- V1.4R4B does not modify the historical V1.1 runner or upstream CosmoFlow physics modules.
- A workflow PASS is not scientific support for Q11.
- The canonical repository binary fixes reference durability and serialization fidelity; it does not change any scientific conclusion from V1.2–V1.4.

## Merge-gate enforcement status

The R4B workflow is fail-closed CI by behavior, but repository branch protection is currently disabled on `main`. Therefore this record does **not** claim that GitHub enforces R4B as a required status check. Required-check enforcement is a separate repository-settings action.