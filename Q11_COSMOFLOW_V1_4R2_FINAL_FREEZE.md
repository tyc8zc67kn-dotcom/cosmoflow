# Q11 × COSMOFLOW V1.4R2 — CROSS-RUNNER REPRODUCIBILITY FINAL FREEZE

Status: PASS (forensic execution); `CROSS_RUNNER_NUMERICAL_VARIANCE`
Date: 2026-08-23
Workflow run: `32610869046`
Head commit: `55ddaf82348faf67e9325b93c227f63e8eac4075`

## Result

Four independent GitHub-hosted `ubuntu-22.04` workers executed the unchanged V1.1 runner twice each under Python 3.8.18 and the locked package set.

### Replicates 1–2 — AMD

CPU: `AMD EPYC 7763 64-Core Processor`

Both replicates classified `BYTE_IDENTICAL`.

For run A and run B in both AMD replicates:

- `raw_baseline.npz` SHA256: `b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1`
- all decoded canonical array hashes match frozen V1.1R;
- all uncompressed `.npy` member hashes match frozen V1.1R;
- both repeated executions on each worker are byte-identical.

### Replicates 3–4 — Intel

CPU: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`

Both replicates classified `NUMERICAL_CONTENT_MISMATCH` relative to frozen V1.1R, while remaining internally deterministic within each Intel worker.

For run A and run B in both Intel replicates:

- `raw_baseline.npz` SHA256: `f06ddb99d7f6c251ee763e727bcbc33cddf95552d04f16e18876566ccbae74fc`
- `N` canonical SHA256 remains `d7875947f671da06a7b2337cf74d20d25361d2a949d4b38d2f7634aa60368c97`;
- `k` canonical SHA256 remains `8dc7dd6e9f001c5f4dd575bf2754e7c9717af0823c8e522cf2e0abeb290b3157`;
- `field_field` canonical SHA256 changes from the frozen AMD/V1.1R reference `1b499519284fec668425fc62c34adb7dc58f5b90aa7e9b6b826da3cff7744560` to `fa35b580c565b060cf299e887a17f9602b1976af36e8c6549eb07f1873980c20`;
- `field_field_field` canonical SHA256 changes from `8a2da84f5473a2b07afde360ce9291c07bf4000077b367717f4be24163991aaa` to `43aba9d29bc56a4d109496c74a82ac36f011276f20d2455aebee747378537e05`.

The Intel run A and run B hashes are identical to each other, and replicates 3 and 4 reproduce the same Intel-specific hashes.

## Numerical-difference magnitude audit

Direct comparison of the archived frozen V1.1R artifact against the downloaded Intel replicate-3 run-A artifact gives:

- `N`: 0 changed elements; exact equality.
- `k`: 0 changed elements; exact equality.
- `field_field`: 999 / 1000 elements differ at the bit level; maximum absolute difference `4.287358024157584e-09`; maximum relative difference `3.020716468182771e-11`.
- `field_field_field`: 999 / 1000 elements differ at the bit level; maximum absolute difference `1.0357332939747721e-05`; maximum relative difference `2.6815178008940224e-06`.

These values characterize numerical reproducibility only. They are not Q11 scores and carry no physical interpretation by themselves.

## Classification

`CROSS_RUNNER_NUMERICAL_VARIANCE`

The evidence rejects the hypothesis that the observed reproducibility problem can be explained solely by `np.savez_compressed` ZIP metadata or serialization timestamps. The decoded numerical correlator arrays themselves can differ across GitHub-hosted CPU implementations while remaining deterministic within the tested CPU groups.

## Relation to the `2c810b...` V1.2 incident

The current V1.2 workflow has repeatedly reported:

`2c810b1801e55e783c839003e34179809071c0861392a6ea0b5b973e7951cf33`

at its frozen byte gate.

That failed workflow does not upload the rejected `raw_baseline.npz`, so V1.4R2 cannot decode that specific file and must not claim that `2c810b...` is identical to the Intel `f06ddb...` pattern. The supported conclusion is narrower: cross-runner numerical variance is independently demonstrated and is sufficient to show that a single whole-NPZ byte hash is not portable across the tested GitHub-hosted CPU environments.

## Artifacts

Workflow: `Q11 CosmoFlow V1.4R2 Cross-Runner Reproducibility Audit`
Run: `32610869046`

- replicate 1 artifact ID `9485481267`, ZIP digest `sha256:953d0e2c14b917bc4d853d4d3268a4ecb6f4f495f293e8703d0854d87a37e34f`
- replicate 2 artifact ID `9485481544`, ZIP digest `sha256:ba7858e890a511fe1154ad9ab3cd3552e1f52ebcd174c8bb21c07ed4c3cc021e`
- replicate 3 artifact ID `9485480897`, ZIP digest `sha256:6042bff79ad5239ff11c9377f9d8b1639b2515badbbf96d4e9771db10179c492`
- replicate 4 artifact ID `9485480588`, ZIP digest `sha256:aeaa24c3bb9f29ce3da9f201c9040de76c02175e309f09e11214e208b366cb1d`

## Evidence firewall

- Q11 scoring performed: FALSE.
- Prior V1.2/V1.3/V1.4 scientific results are not changed by this audit.
- No expected hash has been rewritten.
- No prior preregistration has been retroactively changed.
- No upstream physics module or existing V1.1/V1.2 runner was modified in V1.4R/V1.4R2.

## Merge gate

PR #1 remains Draft.

The next admissible engineering stage is a separately preregistered reproducibility-gate repair that distinguishes a portable numerical-content/tolerance criterion from a platform-specific byte-container identity check, or pins the execution architecture explicitly. That repair must be prospective and must not reinterpret or erase the failed byte-gate records.
