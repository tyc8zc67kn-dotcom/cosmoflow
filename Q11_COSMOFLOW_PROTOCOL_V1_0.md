# Q11 × CosmoFlow — Blind Interface Protocol V1.0

Status: BASELINE LOCKED / NUMERICAL Q11 SCORING NOT YET RUN

## Source freeze

- Repository: `tyc8zc67kn-dotcom/cosmoflow`
- Baseline branch: `main`
- Baseline commit observed before Q11 branch creation: `1e5585e534e6c34dad19181ff4bf5dd7ab252b95`
- Q11 branch: `q11-cosmoflow-v1`
- Core source files are not modified by this protocol.

## Evidence firewall

CosmoFlow remains the physics/numerical engine. Q11 is restricted to a downstream analysis layer.

Forbidden before the Q11 scoring rule is frozen:

1. Editing `Parameters.py`, `Theory.py`, or `Solver.py` to improve agreement with any Q11 family.
2. Selecting momentum configurations after inspecting which ones favor Q11.
3. Relabeling observables or changing normalization after seeing Q11 scores.
4. Reporting a pattern as causal evidence.
5. Inventing numerical outputs, hashes, ranks, p-values, RMSE values, or datasets.

## Canonical engine surface

The repository README defines the relevant architecture as:

- `Parameters.py`: time-dependent couplings and background variables.
- `Theory.py`: tensors defining the two- and three-point flow equations.
- `Solver.py`: initial conditions and numerical integration of the flow equations.

The `CosmoFlow/BlankTemplate` directory contains these three files and is the preferred neutral integration surface for the Q11 adapter.

## Admissible downstream observables

The first Q11 run may consume only deterministic numerical outputs produced by an unchanged CosmoFlow model run. Candidate observables must be frozen before numerical inspection and may include:

- selected two-point correlator values `Sigma` at pre-registered momentum/time locations;
- selected three-point correlator values `B` at pre-registered triangle configurations;
- dimensionless ratios derived from those pre-registered values;
- explicitly defined shape summaries whose formula is frozen before unblinding.

No candidate observable is considered empirical evidence until an actual reproducible run artifact exists.

## V1.0 completion state

Completed:

- repository identity verified;
- writable access verified;
- isolated Q11 branch created;
- baseline commit recorded;
- neutral `BlankTemplate` integration surface identified;
- evidence firewall written.

Not completed:

- executable environment reproduction;
- dependency/version lock beyond repository README prerequisites;
- deterministic baseline numerical run;
- output artifact hash freeze;
- Q11 family scoring;
- null-family competition;
- statistical significance or uniqueness analysis.

## Next queue

`Q11 × COSMOFLOW V1.1 — REPRODUCIBLE BASELINE RUN + ENVIRONMENT LOCK + RAW OUTPUT MATERIALIZATION`

Required before scoring:

1. reproduce one documented CosmoFlow example without Q11-specific edits;
2. freeze Python/package versions and model/configuration inputs;
3. save raw numerical outputs;
4. hash the run inputs and outputs;
5. define and freeze the Q11 feature extractor separately;
6. only then perform one-shot Q11 vs null-family scoring.
