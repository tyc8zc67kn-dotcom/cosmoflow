# Q11 × COSMOFLOW V1.4R — REPRODUCIBILITY GATE FORENSIC AUDIT

Status: PREREGISTERED FORENSIC AUDIT — NO RUNNER FIX / NO EXPECTED-HASH CHANGE
Date: 2026-08-23
Parent evidence: `Q11_COSMOFLOW_V1_4_FINAL_FREEZE.md`
Incident under audit: current PR-triggered V1.2 regeneration reported `raw_baseline.npz` SHA256 `2c810b1801e55e783c839003e34179809071c0861392a6ea0b5b973e7951cf33` while the frozen V1.1R byte hash is `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`.

## 1. Evidence firewall

This audit is diagnostic only.

Forbidden during V1.4R:

1. changing `q11_cosmoflow/run_v1_1.py`;
2. changing `q11_cosmoflow/run_v1_2.py` or its expected frozen raw hash;
3. editing upstream CosmoFlow physics modules;
4. changing feature extraction, family registry, scores, rankings, or prior classifications;
5. treating a container-byte mismatch as a numerical mismatch without comparing decoded array contents;
6. treating matching numerical arrays as proof of a physical claim.

V1.4R performs no Q11 scoring.

## 2. Frozen V1.1R reference

Archived successful V1.1R artifact ID: `9437578374`.
Frozen container SHA256:

`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Canonical decoded-array reference hashes are computed from the archived V1.1R `raw_baseline.npz` using:

`SHA256(str(dtype) || NUL || compact_JSON(shape) || NUL || contiguous_C_order_bytes)`

Reference hashes:

- `N`: `d7875947f671da06a7b2337cf74d20d25361d2a949d4b38d2f7634aa60368c97`
- `field_field`: `1b499519284fec668425fc62c34adb7dc58f5b90aa7e9b6b826da3cff7744560`
- `field_field_field`: `8a2da84f5473a2b07afde360ce9291c07bf4000077b367717f4be24163991aaa`
- `k`: `8dc7dd6e9f001c5f4dd575bf2754e7c9717af0823c8e522cf2e0abeb290b3157`

Uncompressed ZIP-member (`*.npy`) SHA256 references from that same archived artifact:

- `N.npy`: `d8ab82d5456d7146bfd4e9a42a23b1cffc0b6d7cc77a3fa04c427d070db56582`
- `field_field.npy`: `1d3b6d6759d7a2d620800e87affe1d8520c888caf870c007321942293ceeba23`
- `field_field_field.npy`: `76c38bd5f4c76072adca003d2a5bb0174e22ada825251557b25bb7c1900f28b5`
- `k.npy`: `23dd9625d24644656662ca7303243396e67b51e057569add945ffb4505059573`

These references are evidence fingerprints only. They are not Q11 scores.

## 3. Forensic procedure

In one locked CI environment:

1. execute the existing V1.1 runner without modification;
2. copy its `raw_baseline.npz` into the forensic output directory as run A;
3. execute the same existing V1.1 runner a second time;
4. copy the second output as run B;
5. for A and B record:
   - whole-file SHA256;
   - file size;
   - ZIP member names, timestamps, CRC, compressed/uncompressed sizes and uncompressed member SHA256;
   - decoded array dtype, shape, canonical content SHA256 and raw C-order byte SHA256;
6. compare both runs against each other and against the frozen V1.1R canonical decoded-array hashes.

No score-producing V1.2/V1.3/V1.4 runner is called by this audit.

## 4. Frozen classification

The audit classification is determined mechanically:

- `BYTE_IDENTICAL`: both forensic NPZ file hashes equal the frozen V1.1R container hash and all canonical array hashes match.
- `SERIALIZATION_ONLY`: one or both NPZ file hashes differ from the frozen container hash, but all decoded canonical array hashes for both runs match the frozen V1.1R references exactly.
- `NUMERICAL_CONTENT_MISMATCH`: any decoded canonical array hash differs from the frozen V1.1R reference.
- `INTERNAL_NONDETERMINISM`: run A and run B decoded canonical array hashes differ from each other.
- `FORENSIC_ERROR`: required arrays/members are missing or the procedure cannot complete.

`INTERNAL_NONDETERMINISM` takes precedence over `NUMERICAL_CONTENT_MISMATCH`; `NUMERICAL_CONTENT_MISMATCH` takes precedence over `SERIALIZATION_ONLY`.

## 5. Required artifacts

The workflow must preserve and hash at least:

- `run_a/raw_baseline.npz`
- `run_b/raw_baseline.npz`
- `forensic_report.json`
- `SHA256SUMS.txt`
- `environment-freeze-v1.4r.txt`

A later fix, if any, requires a separate superseding record after this diagnostic result exists. V1.4R itself must not modify the runner or relax the existing reproducibility gate.
