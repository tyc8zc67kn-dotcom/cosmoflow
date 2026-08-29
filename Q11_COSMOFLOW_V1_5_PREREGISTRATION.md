# Q11 × COSMOFLOW V1.5 — D3 T02 SENSITIVITY LOCALIZATION

Status: PREREGISTERED — NO V1.5 RANK MAY BE READ BEFORE THIS COMMIT.

V1.4 found `1:1:6` sensitive in target T02 at DeltaN=3 under P334_GM and P400_GM. V1.5 localizes that observation without changing the family registry. The source is copied to a temporary directory for each execution and is not edited in the checkout.

Run fixed equilateral DeltaN values 2, 3, 4, 5, and 6. For T02 only, score the frozen 42-family registry in P334_GM, P400_GM, and control P334_AM, with sorted bin amplitudes, centered log-RMSE, and tie tolerance 1e-12. Output only the winning family and ranks/scores of `1:1:6` and `1:2:3`; this is descriptive and non-causal.
