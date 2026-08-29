# Q11 × COSMOFLOW V1.2 — PRE-REGISTERED FEATURE EXTRACTION + BLIND NULL-FAMILY COMPETITION

Status: PREREGISTERED — NO V1.2 SCORE MAY BE READ BEFORE THIS COMMIT
Date: 2026-08-21
Parent evidence record: `Q11_COSMOFLOW_V1_1R_FINAL_FREEZE.md`
Frozen raw baseline SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

## 1. Evidence firewall
This stage may read numerical values only after this preregistration is committed. No feature formula, bin boundary, family-generation rule, score, ranking rule, or classification rule may be changed after numerical scoring is observed. Any later change requires a superseding version and a fresh run clearly labelled post-hoc.

No upstream CosmoFlow physics module may be modified for V1.2.

## 2. Admissible raw targets
Exactly two raw time-series targets are admissible from the frozen V1.1R baseline:

- T01 = `abs(field_field)`
- T02 = `abs(field_field_field)`

The frozen output grid contains 1000 samples over N ∈ [-4, 10]. No other target may be introduced in V1.2 after scoring begins.

## 3. Pre-registered feature extraction
For each target T independently:

1. Verify shape is exactly `(1000,)` and all values are finite.
2. Partition the 1000 samples by index into three contiguous bins using `numpy.array_split`, yielding sizes 334, 333, 333. This is an index partition fixed before reading scores and does not depend on extrema, crossings, peaks, or fitted parameters.
3. In each bin j, require every absolute value to be strictly greater than zero. If any exact zero occurs, that target is `FEATURE_INVALID` and receives no ratio score. No epsilon, imputation, clipping, smoothing, peak-picking, or replacement is allowed.
4. Define the bin amplitude by the geometric mean:

   `A_j = exp(mean(log(abs(T_j))))`

5. Form the primary ratio feature as the ascending sorted vector:

   `F = sort([A_1, A_2, A_3])`

   Sorting makes the primary competition a magnitude-ratio test and intentionally removes temporal orientation.
6. Normalize only for reporting by `F / geometric_mean(F)`. The score formula below is already scale invariant and does not require a fitted physical amplitude.
7. Record the original unsorted order permutation as an orientation audit field. Orientation is descriptive only and MUST NOT affect the primary family rank in V1.2.

## 4. Null-family registry
The V1.2 family universe is generated exhaustively, not manually selected:

`S = {(a,b,c): 1 <= a <= b <= c <= 6 and gcd(a,b,c) = 1}`

where `gcd(a,b,c) = gcd(gcd(a,b),c)`.

This rule yields exactly 42 primitive nondecreasing integer-ratio families. The registry is sorted lexicographically. `1:2:3` is included because it satisfies the same rule; it receives no special inclusion or weighting.

The code MUST assert `len(S) == 42` and MUST assert `(1,2,3) in S` before scoring.

## 5. Scale-invariant family score
For target feature vector `F=(f1,f2,f3)` and candidate family `R=(r1,r2,r3)`, define centered log vectors:

`x = log(F) - mean(log(F))`

`y = log(R) - mean(log(R))`

Then define target score:

`RMSE_log(F,R) = sqrt(mean((x-y)^2))`

Lower is better. This metric is invariant to a common multiplicative scale on F or R.

## 6. Aggregate competition
If both T01 and T02 are valid, the aggregate score for each family is the arithmetic mean of the two target RMSE values:

`aggregate(R) = mean([RMSE_T01(R), RMSE_T02(R)])`

If either target is invalid, V1.2 aggregate competition is `INCONCLUSIVE_FEATURE_INVALID` and no aggregate rank may be claimed.

Families are ranked by ascending aggregate score. Numerical ties are defined as absolute aggregate-score difference <= `1e-12`; tied families share the same rank. No secondary tie-breaker may improve Q11's position.

## 7. Pre-registered Q11 report fields
For family `1:2:3`, report only after the blind run:

- T01 RMSE and target rank
- T02 RMSE and target rank
- aggregate RMSE
- aggregate rank among 42 families
- best family/families and score
- second-best distinct score when defined
- absolute and relative margin between 1:2:3 and the best family
- whether 1:2:3 is tied for best under the 1e-12 rule

## 8. Classification rule
V1.2 classification is intentionally narrow and non-causal:

- `A — PREFERRED_IN_THIS_REGISTERED_COMPETITION`: 1:2:3 has aggregate rank 1 and is not tied.
- `B — NON_UNIQUE`: 1:2:3 is tied for aggregate rank 1.
- `C — NOT_PREFERRED`: 1:2:3 aggregate rank is greater than 1.
- `D — INCONCLUSIVE_FEATURE_INVALID`: one or both targets fail the pre-registered validity rules.

Even classification A is only a statement about this fixed feature map and this fixed 42-family registry. It is not evidence of causality, a fundamental cosmological law, or a proof of Q11.

## 9. Reproducibility gate
The V1.2 workflow must first regenerate the V1.1 baseline with the same locked environment and configuration, compute SHA256 of `raw_baseline.npz`, and require exact equality with:

`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

If the hash differs, scoring MUST abort before feature extraction and classification.

## 10. Required artifacts
A successful V1.2 run must materialize and hash at least:

- regenerated `raw_baseline.npz`
- `features.json`
- `family_registry.json`
- `scores.csv`
- `result.json`
- `run.log`
- `SHA256SUMS.txt`
- environment freeze

Q11 scores remain sealed until the preregistration commit containing this document exists in repository history.