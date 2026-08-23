from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path(os.environ["Q11_REFERENCE_NPZ"])
CURRENT = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1" / "raw_baseline.npz"
OUTDIR = ROOT / "q11_forensics" / "artifacts" / "v1.4r3"
OUTDIR.mkdir(parents=True, exist_ok=True)

EXPECTED_REFERENCE_SHA256 = "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1"
RTOL = {"field_field": 1e-10, "field_field_field": 5e-6}
ATOL = 1e-12
EXPECTED_KEYS = ["N", "field_field", "field_field_field", "k"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(a: np.ndarray) -> str:
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(str(a.dtype).encode())
    h.update(json.dumps(list(a.shape)).encode())
    h.update(a.tobytes(order="C"))
    return h.hexdigest()


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


reference_sha = sha256(REFERENCE)
if reference_sha != EXPECTED_REFERENCE_SHA256:
    raise RuntimeError(f"FAIL_REFERENCE_INTEGRITY expected={EXPECTED_REFERENCE_SHA256} observed={reference_sha}")

subprocess.run([sys.executable, str(ROOT / "q11_cosmoflow" / "run_v1_1.py")], cwd=ROOT, check=True)
current_sha = sha256(CURRENT)

with np.load(REFERENCE, allow_pickle=False) as ref_npz, np.load(CURRENT, allow_pickle=False) as cur_npz:
    ref_keys = sorted(ref_npz.files)
    cur_keys = sorted(cur_npz.files)
    expected_keys = sorted(EXPECTED_KEYS)
    structure_ok = ref_keys == expected_keys and cur_keys == expected_keys
    arrays = {}
    finite_ok = True
    shapes_ok = True

    for key in EXPECTED_KEYS:
        if not structure_ok:
            arrays[key] = {"gate_pass": False, "reason": "key_structure_mismatch"}
            continue
        ref = np.asarray(ref_npz[key])
        cur = np.asarray(cur_npz[key])
        same_shape = ref.shape == cur.shape
        shapes_ok &= same_shape
        finite = bool(np.isfinite(ref).all() and np.isfinite(cur).all())
        finite_ok &= finite
        entry = {
            "shape_reference": list(ref.shape), "shape_current": list(cur.shape),
            "same_shape": same_shape, "finite": finite,
            "canonical_sha256": canonical_hash(cur),
            "reference_canonical_sha256": canonical_hash(ref),
        }
        if same_shape and finite:
            delta = np.abs(cur - ref)
            denom = np.abs(ref)
            rel = np.divide(delta, denom, out=np.zeros_like(delta, dtype=float), where=denom != 0)
            rel = np.where((denom == 0) & (delta != 0), np.inf, rel)
            entry.update({
                "array_equal": bool(np.array_equal(cur, ref)),
                "different_count": int(np.count_nonzero(cur != ref)),
                "max_abs_diff": float(np.max(delta)) if delta.size else 0.0,
                "max_rel_diff": float(np.max(rel)) if rel.size else 0.0,
            })
            if key in ("N", "k"):
                entry.update({"gate": "EXACT", "atol": 0.0, "rtol": 0.0,
                              "failing_elements": int(np.count_nonzero(cur != ref)),
                              "gate_pass": bool(np.array_equal(cur, ref))})
            else:
                limit = ATOL + RTOL[key] * denom
                fail = delta > limit
                entry.update({"gate": "ELEMENTWISE_ATOL_PLUS_RTOL", "atol": ATOL, "rtol": RTOL[key],
                              "failing_elements": int(np.count_nonzero(fail)),
                              "gate_pass": bool(np.all(~fail))})
        else:
            entry["gate_pass"] = False
        arrays[key] = entry

if not structure_ok or not shapes_ok or not finite_ok:
    classification = "FAIL_STRUCTURE_OR_FINITE"
elif all(arrays[k]["gate_pass"] for k in EXPECTED_KEYS):
    classification = "PASS_PORTABLE_NUMERICAL_EQUIVALENCE"
else:
    classification = "FAIL_PORTABLE_NUMERICAL_EQUIVALENCE"

report = {
    "queue": "Q11 x COSMOFLOW V1.4R3", "classification": classification,
    "q11_scoring_performed": False, "historical_runners_modified": False,
    "reference": {"path": str(REFERENCE), "sha256": reference_sha, "expected_sha256": EXPECTED_REFERENCE_SHA256},
    "current": {"path": str(CURRENT.relative_to(ROOT)), "sha256": current_sha,
                "byte_identical_to_reference": current_sha == reference_sha},
    "environment": {"python": sys.version, "platform": platform.platform(), "cpu_model": cpu_model(), "numpy": np.__version__},
    "gate": {"field_field_rtol": RTOL["field_field"], "field_field_field_rtol": RTOL["field_field_field"], "atol": ATOL},
    "structure_ok": structure_ok, "shapes_ok": shapes_ok, "finite_ok": finite_ok, "arrays": arrays,
}
report_path = OUTDIR / "portable_gate_report.json"
report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
if classification != "PASS_PORTABLE_NUMERICAL_EQUIVALENCE":
    raise SystemExit(2)
