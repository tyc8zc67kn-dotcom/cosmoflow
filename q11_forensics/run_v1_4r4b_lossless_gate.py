from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "q11_cosmoflow" / "canonical" / "v1.1r" / "raw_baseline.npz"
CURRENT = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1" / "raw_baseline.npz"
OUTDIR = ROOT / "q11_forensics" / "artifacts" / "v1.4r4b"
OUTDIR.mkdir(parents=True, exist_ok=True)

EXPECTED_REFERENCE_SHA256 = "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1"
EXPECTED_REFERENCE_SIZE = 19506
EXPECTED_KEYS = ["N", "field_field", "field_field_field", "k"]
RTOL = {"field_field": 1e-10, "field_field_field": 1e-5}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


# Fail closed before decoding the canonical reference.
if not REFERENCE.is_file():
    raise RuntimeError(f"FAIL_CANONICAL_BINARY_INTEGRITY missing={REFERENCE}")
reference_size = REFERENCE.stat().st_size
reference_sha = sha256(REFERENCE)
if reference_size != EXPECTED_REFERENCE_SIZE or reference_sha != EXPECTED_REFERENCE_SHA256:
    raise RuntimeError(
        "FAIL_CANONICAL_BINARY_INTEGRITY "
        f"expected_size={EXPECTED_REFERENCE_SIZE} observed_size={reference_size} "
        f"expected_sha256={EXPECTED_REFERENCE_SHA256} observed_sha256={reference_sha}"
    )

# Generate current baseline using the unchanged historical V1.1 runner.
subprocess.run(
    [sys.executable, str(ROOT / "q11_cosmoflow" / "run_v1_1.py")],
    cwd=ROOT,
    check=True,
)
current_sha = sha256(CURRENT)

with np.load(REFERENCE, allow_pickle=False) as ref_npz, np.load(CURRENT, allow_pickle=False) as cur_npz:
    ref_keys = sorted(ref_npz.files)
    cur_keys = sorted(cur_npz.files)
    expected_keys = sorted(EXPECTED_KEYS)
    structure_ok = ref_keys == expected_keys and cur_keys == expected_keys
    arrays = {}
    finite_ok = True
    shapes_ok = True

    if structure_ok:
        for key in EXPECTED_KEYS:
            ref = np.asarray(ref_npz[key])
            cur = np.asarray(cur_npz[key])
            same_shape = ref.shape == cur.shape
            finite = bool(np.isfinite(ref).all() and np.isfinite(cur).all())
            shapes_ok = shapes_ok and same_shape
            finite_ok = finite_ok and finite

            entry = {
                "shape_reference": list(ref.shape),
                "shape_current": list(cur.shape),
                "same_shape": same_shape,
                "finite": finite,
            }

            if same_shape and finite:
                delta = np.abs(cur - ref)
                denom = np.abs(ref)
                nonzero = denom > 0
                rel = np.zeros_like(delta, dtype=float)
                rel[nonzero] = delta[nonzero] / denom[nonzero]
                rel[~nonzero] = np.where(delta[~nonzero] == 0, 0.0, np.inf)
                entry.update(
                    {
                        "array_equal": bool(np.array_equal(cur, ref)),
                        "different_count": int(np.count_nonzero(cur != ref)),
                        "max_abs_diff": float(np.max(delta)) if delta.size else 0.0,
                        "max_rel_diff": float(np.max(rel)) if rel.size else 0.0,
                    }
                )
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
    else:
        for key in EXPECTED_KEYS:
            arrays[key] = {"gate_pass": False, "reason": "key_structure_mismatch"}

if not structure_ok or not shapes_ok or not finite_ok:
    classification = "FAIL_STRUCTURE_OR_FINITE"
elif all(arrays[k]["gate_pass"] for k in EXPECTED_KEYS):
    classification = "PASS_LOSSLESS_CANONICAL_BINARY_GATE"
else:
    classification = "FAIL_PORTABLE_NUMERICAL_EQUIVALENCE"

report = {
    "queue": "Q11 x COSMOFLOW V1.4R4B",
    "classification": classification,
    "q11_scoring_performed": False,
    "historical_runners_modified": False,
    "canonical_reference": {
        "path": str(REFERENCE.relative_to(ROOT)),
        "sha256": reference_sha,
        "expected_sha256": EXPECTED_REFERENCE_SHA256,
        "byte_size": reference_size,
        "expected_byte_size": EXPECTED_REFERENCE_SIZE,
        "integrity_verified_before_decode": True,
    },
    "current": {
        "path": str(CURRENT.relative_to(ROOT)),
        "sha256": current_sha,
        "byte_identical_to_reference": current_sha == reference_sha,
    },
    "environment": {
        "python": sys.version,
        "platform": platform.platform(),
        "cpu_model": cpu_model(),
        "numpy": np.__version__,
    },
    "gate": {
        "N": "EXACT",
        "k": "EXACT",
        "field_field_rtol": RTOL["field_field"],
        "field_field_field_rtol": RTOL["field_field_field"],
        "atol": 0.0,
    },
    "structure_ok": structure_ok,
    "shapes_ok": shapes_ok,
    "finite_ok": finite_ok,
    "arrays": arrays,
}

report_path = OUTDIR / "lossless_gate_report.json"
report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))

if classification != "PASS_LOSSLESS_CANONICAL_BINARY_GATE":
    raise SystemExit(2)
