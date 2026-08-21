# Q11 × COSMOFLOW V1.2 — FINAL BLIND COMPETITION FREEZE

Status: PASS
Date: 2026-08-21
Preregistration commit: `5501d0c0120db63e53bb07a695e3bea212d8123f`
Execution head commit: `93c410453f871dabd368c50dd09b73c9c021223c`
Workflow run: `32457300491`
Workflow conclusion: `success`

## Reproducibility gate
Frozen V1.1R raw SHA256 expected:
`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Regenerated V1.2 raw SHA256 observed:
`b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`

Gate result: PASS — exact byte-level match.

## Registered competition
- Targets: T01 field_field, T02 field_field_field
- Feature map: three fixed contiguous index bins, geometric mean absolute amplitude per bin, ascending ratio feature
- Null registry: all primitive nondecreasing integer triples 1<=a<=b<=c<=6, gcd=1
- Family count: 42
- Metric: centered log-ratio RMSE
- Aggregate: arithmetic mean across T01 and T02
- Tie tolerance: 1e-12

## Blind result
Best family: `1:1:6`
Best aggregate RMSE: `1.529946510163845`
Second-best distinct aggregate RMSE: `1.6158901216178547`

Q11 family: `1:2:3`
- T01 RMSE: `1.3544987517709224`
- T01 rank: `14`
- T02 RMSE: `2.72692140820515`
- T02 rank: `16`
- Aggregate RMSE: `2.0407100799880364`
- Aggregate rank: `16 / 42`
- Tied for best: `false`
- Absolute margin from best: `0.5107635698241915`
- Relative margin from best: `0.3338440699926776`

Pre-registered classification: `C — NOT_PREFERRED`

## Interpretation boundary
This result means only that, under the feature map and 42-family registry committed before score inspection, `1:2:3` was not the preferred integer-ratio family for this CosmoFlow baseline. The winner `1:1:6` is likewise only the best fit inside this registered comparison. This result does not establish a causal cosmological law or disprove Q11 outside this test definition.

## Artifact freeze
Artifact name: `q11-cosmoflow-v1-2-blind-competition`
Artifact ID: `9437680092`
Artifact size: `28153` bytes
Artifact ZIP digest: `sha256:767c246da8a7394976f00633525ca462b6dfa84245398351acfeae54b58c5edf`
Artifact expiry: `2026-11-19T07:08:03Z`

File SHA256:
- `raw_baseline.npz`: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`
- `features.json`: `32a7d938a6ab6e37df0f0486ce9cea6aab8d9aa9587e6914c5c2ea11f5f376e4`
- `family_registry.json`: `fbaf834ddb83f32e53ba5efe3c4d445f3189791317b248fc9912110e76950828`
- `scores.csv`: `ca90a0c0f7129144d931b3f656d60db75de3c17fa04039b37c9889aec5a1f9e4`
- `result.json`: `bc2b23e11bac23a4fd7147f3e5b906102cd76a5e89ff3fb57a46a0c2202e11d3`
- `run.log`: `097c9f89de8411e81b714e87cc296d6fae6ee8937fa770a7370baaca3dad651f`

## Queue result
V1.2 = PASS as an execution/audit stage.
Scientific comparison result = `C — NOT_PREFERRED` for Q11 1:2:3 under the registered V1.2 test.
