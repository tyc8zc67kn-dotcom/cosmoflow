from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_JSON = ROOT / "q11_forensics" / "reference" / "v1.1r_canonical_arrays.json"
CURRENT = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1" / "raw_baseline.npz"
OUTDIR = ROOT / "q11_forensics" / "artifacts" / "v1.4r4"
OUTDIR.mkdir(parents=True, exist_ok=True)

EXPECTED_PROVENANCE = {
    "artifact_id": 9437578374,
    "workflow_run": 32456990085,
    "head_commit": "616f8b49e99cf19bca3bfd97f5ae506443246748",
    "raw_baseline_sha256": "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1",
}
RTOL = {"field_field": 1e-10, "field_field_field": 1e-5}
EXPECTED_KEYS = ["N", "field_field", "field_field_field", "k"]


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


payload = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
source = payload.get("source", {})
for key, expected in EXPECTED_PROVENANCE.items():
    if source.get(key) != expected:
        raise RuntimeError(
            f"FAIL_DURABLE_REFERENCE_PROVENANCE key={key} expected={expected!r} observed={source.get(key)!r}"
        )

reference_arrays = payload.get("arrays", {})
if sorted(reference_arrays.keys()) != sorted(EXPECTED_KEYS):
    raise RuntimeError("FAIL_DURABLE_REFERENCE_PROVENANCE reference key structure mismatch")

subprocess.run(
    [sys.executable, str(ROOT / "q11_cosmoflow" / "run_v1_1.py")],
    cwd=ROOT,
    check=True,
)

with np.load(CURRENT, allow_pickle=False) as cur_npz:
    cur_keys = sorted(cur_npz.files)
    structure_ok = cur_keys == sorted(EXPECTED_KEYS)
    arrays = {}
    finite_ok = True
    shapes_ok = True

    for key in EXPECTED_KEYS:
        if not structure_ok:
            arrays[key] = {"gate_pass": False, "reason": "key_structure_mismatch"}
            continue

        ref = np.asarray(reference_arrays[key], dtype=float)
        cur = np.asarray(cur_npz[key], dtype=float)
        same_shape = ref.shape == cur.shape
        finite = bool(np.isfinite(ref).all() and np.isfinite(cur).all())
        shapes_ok = shapes_ok and same_shape
        finite_ok = finite_ok and finite

        entry = {
            "same_shape": same_shape,
            "shape_reference": list(ref.shape),
            "shape_current": list(cur.shape),
            "finite": finite,
        }

        if same_shape and finite:
            delta = np.abs(cur - ref)
            denom = np.abs(ref)
            nonzero = denom > 0
            rel = np.zeros_like(delta, dtype=float)
            rel[nonzero] = delta[nonzero] / denom[nonzero]
            rel[~nonzero] = np.where(delta[~nonzero] == 0, 0.0, np.inf)
            entry.update({
                "array_equal": bool(np.array_equal(cur, ref)),
                "different_count": int(np.count_nonzero(cur != ref)),
                "max_abs_diff": float(np.max(delta)) if delta.size else 0.0,
                "max_rel_diff": float(np.max(rel)) if rel.size else 0.0,
            })
            if key in ("N", "k"):
                entry["gate"] = "EXACT"
                entry["gate_pass"] = bool(np.array_equal(cur, ref))
            else:
                limit = RTOL[key] * denom
                entry["gate"] = f"RTOL_{RTOL[key]:.0e}_ATOL_0"
                entry["gate_pass"] = bool(np.all(delta <= limit))
        else:
            entry["gate_pass"] = False

        arrays[key] = entry

if not structure_ok or not shapes_ok or not finite_ok:
    classification = "FAIL_STRUCTURE_OR_FINITE"
elif all(arrays[k]["gate_pass"] for k in EXPECTED_KEYS):
    classification = "PASS_DURABLE_PORTABLE_GATE"
else:
    classification = "FAIL_PORTABLE_NUMERICAL_EQUIVALENCE"

report = {
    "queue": "Q11 x COSMOFLOW V1.4R4",
    "classification": classification,
    "q11_scoring_performed": False,
    "historical_runners_modified": False,
    "durable_reference": {
        "path": str(REFERENCE_JSON.relative_to(ROOT)),
        "source": source,
    },
    "environment": {
        "python": sys.version,
        "platform": platform.platform(),
        "cpu_model": cpu_model(),
        "numpy": np.__version__,
    },
    "gate": {
        "field_field_rtol": RTOL["field_field"],
        "field_field_field_rtol": RTOL["field_field_field"],
        "atol": 0.0,
    },
    "structure_ok": structure_ok,
    "shapes_ok": shapes_ok,
    "finite_ok": finite_ok,
    "arrays": arrays,
}

report_path = OUTDIR / "durable_gate_report.json"
report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))

if classification != "PASS_DURABLE_PORTABLE_GATE":
    raise SystemExit(2)
