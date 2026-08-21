# Q11 × COSMOFLOW V1.1R — GITHUB ACTIONS EXECUTION RECOVERY + FIRST SUCCESSFUL RAW ARTIFACT FREEZE

Status: PASS
Date: 2026-08-21
Branch: q11-cosmoflow-v1
Head commit: 616f8b49e99cf19bca3bfd97f5ae506443246748
Workflow run: 32456990085
Workflow run number: 6
Workflow conclusion: success

## Recovery finding
The prior failure was caused by `tee` attempting to write `q11_cosmoflow/artifacts/v1.1/run.log` before the artifact directory existed. The numerical CosmoFlow baseline itself completed and produced raw output. V1.1R fixed only workflow plumbing by creating the directory before execution and enabling `pipefail`. No upstream physics modules were modified.

## Locked execution environment
- Runner: ubuntu-22.04
- Python: 3.8.18
- NumPy: 1.24.4
- SciPy: 1.10.1
- Matplotlib: 3.7.5

## Baseline configuration
- Source example: `CosmoFlow/Massless_dphi3/MyFirstRun.py`
- Nfield: 1
- DeltaN: 4
- N_exit: 0
- Ni: -4
- Nf: 10
- N output points: 1000
- Rtol: 1e-4
- Atol: 1e-180
- k1 = k2 = k3 = 1.0
- Kinematics: equilateral

## Source blob freeze
- MyFirstRun.py: `79cba7fa3ef6381307ff4ba3801f20ba4628bd31`
- Parameters.py: `91e75f63c7e0f2e10582a1f9a99a92bcb92819d5`
- Solver.py: `8401cf3c512a3da87c8c32b50c291cb2af65b03f`
- Theory.py: `b8fdeb6760c3d49b1e1eab95f721e549e5b54c47`

## Raw output materialization
- `field_field` shape: 1000
- `field_field_field` shape: 1000
- all field-field values finite: true
- all field-field-field values finite: true

## SHA256 freeze
- `raw_baseline.npz`: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`
- `manifest.json`: `5e53f9ffcf19ecf1c181c6b65695c9ca2d691579b80d96b033890cfd0152c915`
- `run.log`: `40d517d2bb46deb8d5786837eede4a0839843d6b5c5f3092dc320e4653835501`

Manifest internal SHA256 reported by runner: `86aef845bde9ab08e883f4de7360543aaf2f43808264b0639557d91c715be159`

## Uploaded GitHub Actions artifact
- Artifact ID: 9437578374
- Name: `q11-cosmoflow-v1-1-baseline`
- Size: 22039 bytes
- Artifact ZIP digest: `sha256:b6b8dd7c7b762f95d4ef01efe3f3a2c6361fde35d8f632c44fbe2e724ea28a3b`
- Expiry: 2026-11-19T07:03:49Z

## Evidence firewall
Q11 scoring performed: FALSE
No 1:2:3 score, RMSE, rank, p-value, family selection, or post-hoc feature selection was performed in V1.1R.

## Queue result
V1.1R = PASS.
First successful raw artifact freeze completed.

Next admissible stage: Q11 × COSMOFLOW V1.2 — PRE-REGISTERED FEATURE EXTRACTION + BLIND NULL-FAMILY COMPETITION, only after feature definitions and comparison rules are frozen before reading Q11 scores.
