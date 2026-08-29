from __future__ import annotations

import base64
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REFDIR = ROOT / "q11_forensics" / "reference"
PARTS = [REFDIR / f"v1.1r_payload.part{i}" for i in range(1, 5)]
CURRENT = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1" / "raw_baseline.npz"
OUTDIR = ROOT / "q11_forensics" / "artifacts" / "v1.4r4"
OUTDIR.mkdir(parents=True, exist_ok=True)

EXPECTED_PAYLOAD_SHA256 = "ed99f52be4f3fd0d8ea6f47b1c131c6aa5deb6193d39b661f3541abf5144e7b2"
EXPECTED_PROVENANCE = {
    "artifact_id": 9437578374,
    "workflow_run": 32456990085,
    "head_commit": "616f8b49e99cf19bca3bfd97f5ae506443246748",
    "raw_baseline_sha256": "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1",
}
RTOL = {"field_field": 1e-10, "field_field_field": 1e-5}
EXPECTED_KEYS = ["N", "field_field", "field_field_field", "k"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def raw_float64_bytes(arr: np.ndarray) -> bytes:
    return np.asarray(arr, dtype="<f8", order="C").tobytes(order="C")


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


payload_bytes = b"".join(path.read_bytes() for path in PARTS)
payload_sha = sha256_bytes(payload_bytes)
if payload_sha != EXPECTED_PAYLOAD_SHA256:
    raise RuntimeError(
        f"FAIL_DURABLE_REFERENCE_PROVENANCE payload_sha expected={EXPECTED_PAYLOAD_SHA256} observed={payload_sha}"
    )
payload = json.loads(payload_bytes.decode("utf-8"))

source = payload.get("source", {})
for key, expected in EXPECTED_PROVENANCE.items():
    if source.get(key) != expected:
        raise RuntimeError(
            f"FAIL_DURABLE_REFERENCE_PROVENANCE key={key} expected={expected!r} observed={source.get(key)!r}"
        )
if payload.get("encoding") != "float64_c_order_raw_bytes_base64":
    raise RuntimeError("FAIL_DURABLE_REFERENCE_PROVENANCE encoding mismatch")

field_specs = payload.get("arrays", {})
exact_hashes = payload.get("exact_hashes", {})
if sorted(field_specs.keys()) != ["field_field", "field_field_field"]:
    raise RuntimeError("FAIL_DURABLE_REFERENCE_PROVENANCE field key structure mismatch")
if sorted(exact_hashes.keys()) != ["N", "k"]:
    raise RuntimeError("FAIL_DURABLE_REFERENCE_PROVENANCE exact hash key structure mismatch")

reference_fields = {}
for key in ("field_field", "field_field_field"):
    spec = field_specs[key]
    if spec.get("dtype") != "<f8" or spec.get("shape") != [1000]:
        raise RuntimeError(f"FAIL_DURABLE_REFERENCE_PROVENANCE {key} metadata mismatch")
    raw = base64.b64decode(spec["data_b64"], validate=True)
    expected_nbytes = 1000 * np.dtype("<f8").itemsize
    if len(raw) != expected_nbytes:
        raise RuntimeError(f"FAIL_DURABLE_REFERENCE_PROVENANCE {key} byte length mismatch")
    reference_fields[key] = np.frombuffer(raw, dtype="<f8").copy()

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

    if not structure_ok:
        for key in EXPECTED_KEYS:
            arrays[key] = {"gate_pass": False, "reason": "key_structure_mismatch"}
    else:
        for key in ("N", "k"):
            cur = np.asarray(cur_npz[key], dtype="<f8")
            expected_shape = exact_hashes[key]["shape"]
            expected_hash = exact_hashes[key]["sha256_raw"]
            same_shape = list(cur.shape) == expected_shape
            finite = bool(np.isfinite(cur).all())
            observed_hash = sha256_bytes(raw_float64_bytes(cur)) if same_shape else None
            gate_pass = same_shape and finite and observed_hash == expected_hash
            shapes_ok = shapes_ok and same_shape
            finite_ok = finite_ok and finite
            arrays[key] = {
                "gate": "EXACT_RAW_FLOAT64_SHA256",
                "gate_pass": gate_pass,
                "same_shape": same_shape,
                "shape_reference": expected_shape,
                "shape_current": list(cur.shape),
                "finite": finite,
                "expected_raw_sha256": expected_hash,
                "observed_raw_sha256": observed_hash,
            }

        for key in ("field_field", "field_field_field"):
            ref = reference_fields[key]
            cur = np.asarray(cur_npz[key], dtype="<f8")
            same_shape = ref.shape == cur.shape
            finite = bool(np.isfinite(ref).all() and np.isfinite(cur).all())
            shapes_ok = shapes_ok and same_shape
            finite_ok = finite_ok and finite
            entry = {
                "same_shape": same_shape,
                "shape_reference": list(ref.shape),
                "shape_current": list(cur.shape),
                "finite": finite,
                "gate": f"RTOL_{RTOL[key]:.0e}_ATOL_0",
            }
            if same_shape and finite:
                delta = np.abs(cur - ref)
                denom = np.abs(ref)
                nonzero = denom > 0
                rel = np.zeros_like(delta, dtype=float)
                rel[nonzero] = delta[nonzero] / denom[nonzero]
                rel[~nonzero] = np.where(delta[~nonzero] == 0, 0.0, np.inf)
                limit = RTOL[key] * denom
                entry.update({
                    "array_equal": bool(np.array_equal(cur, ref)),
                    "different_count": int(np.count_nonzero(cur != ref)),
                    "max_abs_diff": float(np.max(delta)) if delta.size else 0.0,
                    "max_rel_diff": float(np.max(rel)) if rel.size else 0.0,
                    "gate_pass": bool(np.all(delta <= limit)),
                })
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
        "parts": [str(p.relative_to(ROOT)) for p in PARTS],
        "joined_payload_sha256": payload_sha,
        "expected_joined_payload_sha256": EXPECTED_PAYLOAD_SHA256,
        "encoding": payload["encoding"],
        "source": source,
    },
    "environment": {
        "python": sys.version,
        "platform": platform.platform(),
        "cpu_model": cpu_model(),
        "numpy": np.__version__,
    },
    "gate": {
        "N": "EXACT_RAW_FLOAT64_SHA256",
        "k": "EXACT_RAW_FLOAT64_SHA256",
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
