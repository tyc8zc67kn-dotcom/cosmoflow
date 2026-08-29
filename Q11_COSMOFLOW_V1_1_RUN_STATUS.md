# Q11 × COSMOFLOW V1.1 — RUN STATUS

Status: **BLOCKED_AT_EXECUTION_GATE**

This record distinguishes materialized infrastructure from an actually completed numerical baseline run.

## Scope

Queue: `Q11 × COSMOFLOW V1.1 — REPRODUCIBLE BASELINE RUN + ENVIRONMENT LOCK + RAW OUTPUT MATERIALIZATION`

Baseline example: `CosmoFlow/Massless_dphi3/MyFirstRun.py`

Upstream source blobs frozen for this run:

- `MyFirstRun.py` — `79cba7fa3ef6381307ff4ba3801f20ba4628bd31`
- `Parameters.py` — `91e75f63c7e0f2e10582a1f9a99a92bcb92819d5`
- `Theory.py` — `b8fdeb6760c3d49b1e1eab95f721e549e5b54c47`
- `Solver.py` — `8401cf3c512a3da87c8c32b50c291cb2af65b03f`

## Materialized

- `q11_cosmoflow/requirements-v1.1.txt`
- `q11_cosmoflow/run_v1_1.py`
- `.github/workflows/q11-cosmoflow-v1-1.yml`
- Draft PR #1: Q11 × CosmoFlow V1.1 reproducible baseline

Environment specification:

- Python `3.8.18`
- numpy `1.24.4`
- scipy `1.10.1`
- matplotlib `3.7.5`
- tqdm `4.66.5`

## Execution evidence

At the time of this record, GitHub returned no workflow runs for head commit `2b179b746c6d503d0734ca451ded2f68653bf733`, and the combined commit status contained no status checks.

The local execution environment available to the agent is Python 3.13 with SciPy 1.17, where the upstream `Theory.py` dependency `scipy.misc.derivative` is unavailable. Direct repository cloning is also unavailable in that runtime because outbound DNS/network access to GitHub is blocked.

Therefore no numerical baseline output has been claimed.

## Evidence firewall

The following remain **NOT MATERIALIZED** and must not be invented:

- `raw_baseline.npz`
- numerical correlator values from a new V1.1 run
- V1.1 raw-output SHA256
- V1.1 manifest SHA256
- PASS/FAIL classification of numerical reproducibility
- any Q11 score, rank, RMSE, p-value, family preference, or 1:2:3 comparison

Q11 scoring remains sealed.

## Gate

V1.1 may advance from `BLOCKED_AT_EXECUTION_GATE` only after a compatible runner actually executes the frozen upstream example and produces inspectable raw artifacts plus hashes.
