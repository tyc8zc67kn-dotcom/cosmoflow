# Q11 × COSMOFLOW V1.4 — FINAL OUT-OF-SAMPLE AUDIT FREEZE

Status: PASS (execution); `OUT_OF_SAMPLE_SENSITIVE` (registered robustness classification)
Date: 2026-08-21
Preregistration / execution commit: `ce71c61c3377499cbdaa45efd826e4acbeedb280`
Workflow run: `32458576226` (`success`)

## Result

All three preregistered out-of-sample configurations completed with finite 1000-sample outputs:

- `D3_EQ` (DeltaN 3, equilateral): `2e83fa267486995693054d4299ded04b618a7b9068972b6fb690d3c103ecb79a`
- `D5_EQ` (DeltaN 5, equilateral): `5977d4399c623e1a5b3dff198944a233e3f59b2d9b9d392f421dc26c4d3676ce`
- `D4_SQ` (DeltaN 4, squeezed): `baa9495bbb3ba75ea8e504bf54021fe2ba3bd5f9140d6e46a170a1ec0840fe2b`

V1.2 winner `1:1:6` was uniquely pooled rank 1 in **26 / 27** preregistered configuration-representation cells. However, the target-specific D3_EQ checks ranked it 5th for T02 at P334_GM and 15th for T02 at P400_GM. It therefore fails the preregistered rule requiring it never to fall below rank 3 in either leave-one-target-out analysis.

Classification: `OUT_OF_SAMPLE_SENSITIVE`.

Q11 (`1:2:3`) never led: its best pooled rank was 13 / 42, with ranks spanning 13–19 across the 27 cells.

## Interpretation boundary

The V1.3 result was robust to its representation grid on the original baseline, but it is not uniformly robust once this fixed three-configuration physics audit is introduced. The correct conclusion is narrower than either a universal `1:1:6` claim or a Q11 validation: this is a representation-and-regime-sensitive numerical pattern within the registered tests.

## Artifact freeze

Artifact: `q11-cosmoflow-v1-4-out-of-sample-audit` (ID `9438112807`)

- ZIP digest: `sha256:fdb7ab2c9b28c81826c9ed7957e45a2dab9565da41164a609542d57e930b95b6`
- Expiry: `2026-11-19T07:25:39Z`
- `scores.csv`: `e9e2ad4179f2e0ad6215076f7440b4aa82ddc6c386c26d95b3b1d04aeb250f4e`
- `summary.json`: `2b8e9a9b1a4ca3e642c34b515e81021dc46e2fbbe0a2921a100671499f5a8e65`
- `run.log`: `20d09bbd38de7dad6445610ef7add8ed00762e5738734d34c45f970674d601f4`
