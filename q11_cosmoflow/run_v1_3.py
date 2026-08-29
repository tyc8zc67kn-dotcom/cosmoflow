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
OUTDIR = ROOT / "q11_cosmoflow" / "artifacts" / "v1.3"
OUTDIR.mkdir(parents=True, exist_ok=True)
EXPECTED_RAW_SHA256 = "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1"
Q11, V12_WINNER, TIE_TOL = (1, 2, 3), (1, 1, 6), 1e-12
PARTITIONS = {"P334": (0, 334, 667, 1000), "P250": (0, 250, 750, 1000), "P400": (0, 400, 600, 1000)}
SUMMARIES = ("GM", "AM", "RMS")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def family_label(family: tuple[int, int, int]) -> str:
    return ":".join(map(str, family))


def rank_rows(rows: list[dict], score_key: str, rank_key: str) -> None:
    values = sorted({row[score_key] for row in rows})
    for row in rows:
        row[rank_key] = 1 + sum(value < row[score_key] - TIE_TOL for value in values)


def amplitudes(values: np.ndarray, bounds: tuple[int, int, int, int], summary: str) -> list[float]:
    if values.shape != (1000,) or not np.isfinite(values).all():
        raise ValueError("target must be finite with shape (1000,)")
    absolute = np.abs(values)
    result = []
    for start, end in zip(bounds[:-1], bounds[1:]):
        chunk = absolute[start:end]
        if chunk.size == 0 or np.any(chunk <= 0):
            raise ValueError("all bins must contain strictly positive absolute values")
        if summary == "GM":
            value = np.exp(np.mean(np.log(chunk)))
        elif summary == "AM":
            value = np.mean(chunk)
        else:
            value = np.sqrt(np.mean(chunk ** 2))
        result.append(float(value))
    return sorted(result)


def score(feature: list[float], family: tuple[int, int, int]) -> float:
    x = np.log(np.asarray(feature))
    y = np.log(np.asarray(family, dtype=float))
    return float(np.sqrt(np.mean(((x - x.mean()) - (y - y.mean())) ** 2)))


subprocess.run([sys.executable, str(ROOT / "q11_cosmoflow" / "run_v1_1.py")], cwd=ROOT, check=True)
source = V11_DIR / "raw_baseline.npz"
observed = sha256(source)
if observed != EXPECTED_RAW_SHA256:
    raise RuntimeError(f"REPRODUCIBILITY_GATE_FAILED expected={EXPECTED_RAW_SHA256} observed={observed}")
shutil.copy2(source, OUTDIR / "raw_baseline.npz")

with np.load(source, allow_pickle=False) as raw:
    targets = {"T01_field_field": np.asarray(raw["field_field"], dtype=float), "T02_field_field_field": np.asarray(raw["field_field_field"], dtype=float)}

families = [(a, b, c) for a in range(1, 7) for b in range(a, 7) for c in range(b, 7) if math.gcd(math.gcd(a, b), c) == 1]
assert len(families) == 42 and Q11 in families and V12_WINNER in families
features, rows, representation_summaries = {}, [], []

for partition_name, bounds in PARTITIONS.items():
    for summary in SUMMARIES:
        representation = f"{partition_name}_{summary}"
        vectors = {name: amplitudes(values, bounds, summary) for name, values in targets.items()}
        features[representation] = {"bounds": list(bounds), "summary": summary, "sorted_amplitudes": vectors}
        local = []
        for family in families:
            t01, t02 = score(vectors["T01_field_field"], family), score(vectors["T02_field_field_field"], family)
            local.append({"representation": representation, "family": family_label(family), "T01_RMSE": t01, "T02_RMSE": t02, "pooled_RMSE": (t01 + t02) / 2})
        for key, rank_key in (("T01_RMSE", "T01_rank"), ("T02_RMSE", "T02_rank"), ("pooled_RMSE", "pooled_rank")):
            rank_rows(local, key, rank_key)
        winner = next(row for row in local if row["family"] == family_label(V12_WINNER))
        q11 = next(row for row in local if row["family"] == family_label(Q11))
        representation_summaries.append({"representation": representation, "winner": family_label(V12_WINNER), "winner_pooled_rank": winner["pooled_rank"], "winner_T01_rank": winner["T01_rank"], "winner_T02_rank": winner["T02_rank"], "q11_pooled_rank": q11["pooled_rank"], "q11_tied_for_pooled_best": q11["pooled_rank"] == 1, "pooled_best_families": [row["family"] for row in local if row["pooled_rank"] == 1]})
        rows.extend(local)

robust_count = sum(item["winner_pooled_rank"] == 1 and len(item["pooled_best_families"]) == 1 for item in representation_summaries)
never_below_three = all(item["winner_T01_rank"] <= 3 and item["winner_T02_rank"] <= 3 for item in representation_summaries)
classification = "ROBUST_IN_THIS_AUDIT" if robust_count >= 8 and never_below_three else "REPRESENTATION_SENSITIVE"
summary = {"queue": "Q11 x COSMOFLOW V1.3", "reproducibility_gate": "PASS", "raw_sha256": observed, "family_count": 42, "representation_count": len(representation_summaries), "v12_winner": family_label(V12_WINNER), "v12_winner_unique_pooled_rank_1_count": robust_count, "v12_winner_never_below_rank_3_in_target_specific_analysis": never_below_three, "v12_winner_classification": classification, "q11": {"family": family_label(Q11), "pooled_rank_distribution": [item["q11_pooled_rank"] for item in representation_summaries], "tied_for_pooled_best_in_any_representation": any(item["q11_tied_for_pooled_best"] for item in representation_summaries)}, "representations": representation_summaries, "claim_scope": "Preregistered V1.3 representation grid and fixed 42-family registry only; non-causal."}

(OUTDIR / "representations.json").write_text(json.dumps(features, indent=2, sort_keys=True), encoding="utf-8")
with (OUTDIR / "scores.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["representation", "family", "T01_RMSE", "T01_rank", "T02_RMSE", "T02_rank", "pooled_RMSE", "pooled_rank"])
    writer.writeheader(); writer.writerows(rows)
(OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(summary, indent=2, sort_keys=True))
