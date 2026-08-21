# Q11 × COSMOFLOW V1.3 — FEATURE-ROBUSTNESS + BINNING ADVERSARIAL AUDIT + LEAVE-ONE-TARGET-OUT + NULL STABILITY

Status: PREREGISTERED — NO V1.3 WINNER OR Q11 SCORE MAY BE INSPECTED BEFORE THE COMMIT CONTAINING THIS FILE
Date: 2026-08-21
Parent evidence record: `Q11_COSMOFLOW_V1_2_FINAL_FREEZE.md`
Frozen raw baseline SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

## 1. Purpose and evidence firewall

V1.3 audits whether V1.2's winning family `1:1:6` is stable under fixed, deliberately varied representations. It is not an attempt to improve the standing of Q11 (`1:2:3`). The upstream CosmoFlow physics modules may not be altered. Every feature rule, boundary, family registry, metric, and interpretation threshold below is frozen before any V1.3 score is read.

The V1.1 baseline must be regenerated first and must have the frozen SHA256 above. A mismatch aborts all V1.3 scoring.

## 2. Targets and ratio families

The only targets are V1.2's two finite, 1000-sample arrays: T01 `abs(field_field)` and T02 `abs(field_field_field)`. The family universe is exactly the 42 primitive, nondecreasing triples `(a,b,c)` with `1 <= a <= b <= c <= 6` and `gcd(a,b,c)=1`, in lexicographic order. The centered log-RMSE metric and `1e-12` tie rule are identical to V1.2.

## 3. Fixed representation grid

For every target, score every one of these nine representations (three partitions × three summaries):

- Partitions by fixed zero-based half-open indices: `P334 = [0,334,667,1000]`; `P250 = [0,250,750,1000]`; `P400 = [0,400,600,1000]`.
- Per-bin summaries of the strictly positive absolute samples: geometric mean (`GM`), arithmetic mean (`AM`), and root-mean-square (`RMS`).
- The three resulting bin amplitudes are sorted ascending before scoring, as in V1.2. There is no fitting, clipping, epsilon, peak selection, or data-dependent binning.

This grid is intentionally adversarial to V1.2's 334/333/333 geometric-mean representation: it changes both bin boundaries and amplitude functional while keeping the target, dimensionality, scale invariance, and null universe fixed.

## 4. Scores and leave-one-target-out

For each representation and family, calculate T01 and T02 centered log-RMSEs. Report separate ranks for each target (the two leave-one-target-out analyses) and their arithmetic mean (the pooled analysis). No target-specific winner may be selected for a pooled claim.

## 5. Null stability and classification

For each representation, retain the full 42-family ranking. Let `W` be V1.2's winner `1:1:6` and `Q` be Q11 `1:2:3`.

- `W` is **ROBUST_IN_THIS_AUDIT** only if it is uniquely rank 1 in at least 8 of the 9 pooled representations and is never below rank 3 in either target-specific analysis.
- `W` is **REPRESENTATION_SENSITIVE** otherwise.
- Q11 is reported descriptively: its pooled-rank distribution and whether it is tied for rank 1 in any representation. No new “preferred” claim for Q11 is permitted from a subset of this grid.

These classifications concern this preregistered robustness grid only; they establish neither a physical law nor a causal ratio.

## 6. Required outputs

The run must write and hash `raw_baseline.npz`, `representations.json`, `scores.csv`, `summary.json`, `run.log`, `SHA256SUMS.txt`, and an environment freeze. The final report must state the V1.1 reproducibility-gate outcome and may be frozen only after a successful CI artifact exists.
