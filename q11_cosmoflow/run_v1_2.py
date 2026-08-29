from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V11_DIR = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1"
OUTDIR = ROOT / "q11_cosmoflow" / "artifacts" / "v1.2"
OUTDIR.mkdir(parents=True, exist_ok=True)

PREREG_COMMIT = "5501d0c0120db63e53bb07a695e3bea212d8123f"
EXPECTED_RAW_SHA256 = "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1"
Q11 = (1, 2, 3)
TIE_TOL = 1e-12


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


# Reproduce the frozen V1.1 baseline first. Scoring is forbidden if the bytes differ.
subprocess.run([sys.executable, str(ROOT / "q11_cosmoflow" / "run_v1_1.py")], cwd=ROOT, check=True)
source_raw = V11_DIR / "raw_baseline.npz"
observed_raw_sha = sha256(source_raw)
if observed_raw_sha != EXPECTED_RAW_SHA256:
    raise RuntimeError(
        f"REPRODUCIBILITY_GATE_FAILED expected={EXPECTED_RAW_SHA256} observed={observed_raw_sha}"
    )

raw_copy = OUTDIR / "raw_baseline.npz"
shutil.copy2(source_raw, raw_copy)
assert sha256(raw_copy) == EXPECTED_RAW_SHA256

with np.load(raw_copy, allow_pickle=False) as data:
    N = np.asarray(data["N"], dtype=float)
    targets = {
        "T01_field_field": np.asarray(data["field_field"], dtype=float),
        "T02_field_field_field": np.asarray(data["field_field_field"], dtype=float),
    }


def extract_feature(values: np.ndarray) -> dict:
    if values.shape != (1000,):
        return {"valid": False, "reason": f"shape={values.shape}"}
    if not np.isfinite(values).all():
        return {"valid": False, "reason": "nonfinite"}
    abs_values = np.abs(values)
    bins = np.array_split(abs_values, 3)
    if [len(b) for b in bins] != [334, 333, 333]:
        return {"valid": False, "reason": "unexpected_bin_sizes"}
    if any(np.any(b <= 0) for b in bins):
        return {"valid": False, "reason": "exact_zero_or_nonpositive_after_abs"}
    amplitudes = np.array([np.exp(np.mean(np.log(b))) for b in bins], dtype=float)
    sorted_values = np.sort(amplitudes)
    gm = float(np.exp(np.mean(np.log(sorted_values))))
    normalized = sorted_values / gm
    orientation = [int(i) for i in np.argsort(amplitudes)]
    return {
        "valid": True,
        "bin_sizes": [334, 333, 333],
        "bin_geometric_means": [float(x) for x in amplitudes],
        "sorted_feature": [float(x) for x in sorted_values],
        "normalized_sorted_feature": [float(x) for x in normalized],
        "orientation_argsort_zero_based": orientation,
    }


features = {name: extract_feature(values) for name, values in targets.items()}
features_record = {
    "queue": "Q11 x COSMOFLOW V1.2",
    "preregistration_commit": PREREG_COMMIT,
    "raw_sha256_verified": observed_raw_sha,
    "N_shape": list(N.shape),
    "N_min": float(np.min(N)),
    "N_max": float(np.max(N)),
    "targets": features,
}
(OUTDIR / "features.json").write_text(
    json.dumps(features_record, indent=2, sort_keys=True), encoding="utf-8"
)

families = []
for a in range(1, 7):
    for b in range(a, 7):
        for c in range(b, 7):
            if math.gcd(math.gcd(a, b), c) == 1:
                families.append((a, b, c))
assert len(families) == 42
assert Q11 in families

registry = {
    "rule": "1<=a<=b<=c<=6 and gcd(a,b,c)=1; lexicographic order",
    "count": len(families),
    "q11_family": list(Q11),
    "families": [list(f) for f in families],
}
(OUTDIR / "family_registry.json").write_text(
    json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8"
)

valid = all(item.get("valid") is True for item in features.values())
rows = []
result = {
    "queue": "Q11 x COSMOFLOW V1.2",
    "preregistration_commit": PREREG_COMMIT,
    "reproducibility_gate": "PASS",
    "raw_sha256": observed_raw_sha,
    "family_count": 42,
    "q11_family": "1:2:3",
}

if not valid:
    result["classification"] = "D — INCONCLUSIVE_FEATURE_INVALID"
    result["aggregate_competition_performed"] = False
else:
    feature_vectors = {
        name: np.asarray(record["sorted_feature"], dtype=float)
        for name, record in features.items()
    }

    def score(feature: np.ndarray, family: tuple[int, int, int]) -> float:
        x = np.log(feature)
        x = x - np.mean(x)
        y = np.log(np.asarray(family, dtype=float))
        y = y - np.mean(y)
        return float(np.sqrt(np.mean((x - y) ** 2)))

    for family in families:
        target_scores = {name: score(vec, family) for name, vec in feature_vectors.items()}
        aggregate = float(np.mean(list(target_scores.values())))
        rows.append({
            "family": f"{family[0]}:{family[1]}:{family[2]}",
            "a": family[0], "b": family[1], "c": family[2],
            "T01_RMSE": target_scores["T01_field_field"],
            "T02_RMSE": target_scores["T02_field_field_field"],
            "aggregate_RMSE": aggregate,
        })

    rows.sort(key=lambda r: r["aggregate_RMSE"])

    distinct_scores = []
    for r in rows:
        s = r["aggregate_RMSE"]
        if not distinct_scores or abs(s - distinct_scores[-1]) > TIE_TOL:
            distinct_scores.append(s)

    for r in rows:
        r["aggregate_rank"] = 1 + sum(ds < r["aggregate_RMSE"] - TIE_TOL for ds in distinct_scores)

    for target_key in ("T01_RMSE", "T02_RMSE"):
        values = sorted({r[target_key] for r in rows})
        for r in rows:
            r[target_key.replace("RMSE", "rank")] = 1 + sum(v < r[target_key] - TIE_TOL for v in values)

    q11 = next(r for r in rows if r["family"] == "1:2:3")
    best_score = rows[0]["aggregate_RMSE"]
    best = [r for r in rows if abs(r["aggregate_RMSE"] - best_score) <= TIE_TOL]
    second_best_distinct = next((s for s in distinct_scores if s > best_score + TIE_TOL), None)
    q11_tied_best = q11["aggregate_rank"] == 1 and len(best) > 1

    if q11["aggregate_rank"] == 1 and not q11_tied_best:
        classification = "A — PREFERRED_IN_THIS_REGISTERED_COMPETITION"
    elif q11_tied_best:
        classification = "B — NON_UNIQUE"
    else:
        classification = "C — NOT_PREFERRED"

    abs_margin = float(q11["aggregate_RMSE"] - best_score)
    rel_margin = None if best_score == 0 else float(abs_margin / best_score)

    result.update({
        "aggregate_competition_performed": True,
        "classification": classification,
        "best_families": [r["family"] for r in best],
        "best_aggregate_RMSE": float(best_score),
        "second_best_distinct_aggregate_RMSE": None if second_best_distinct is None else float(second_best_distinct),
        "q11": {
            "T01_RMSE": float(q11["T01_RMSE"]),
            "T01_rank": int(q11["T01_rank"]),
            "T02_RMSE": float(q11["T02_RMSE"]),
            "T02_rank": int(q11["T02_rank"]),
            "aggregate_RMSE": float(q11["aggregate_RMSE"]),
            "aggregate_rank": int(q11["aggregate_rank"]),
            "tied_for_best": bool(q11_tied_best),
            "absolute_margin_from_best": abs_margin,
            "relative_margin_from_best": rel_margin,
        },
        "claim_scope": "Fixed V1.2 feature map and fixed exhaustive 42-family integer-ratio registry only; non-causal.",
    })

with (OUTDIR / "scores.csv").open("w", newline="", encoding="utf-8") as fh:
    fields = ["family", "a", "b", "c", "T01_RMSE", "T01_rank", "T02_RMSE", "T02_rank", "aggregate_RMSE", "aggregate_rank"]
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row[k] for k in fields})

(OUTDIR / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
