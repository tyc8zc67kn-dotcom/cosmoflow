from __future__ import annotations

import hashlib
import json
import os
import platform
import runpy
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "CosmoFlow" / "Massless_dphi3" / "MyFirstRun.py"
EXAMPLE_DIR = EXAMPLE.parent
OUTDIR = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Preserve upstream example semantics. We only intercept plt.show via Agg and
# collect globals after execution. No Q11 scoring or feature selection occurs here.
os.chdir(EXAMPLE_DIR)
sys.path.insert(0, str(EXAMPLE_DIR))
ns = runpy.run_path(str(EXAMPLE), run_name="__main__")

N = np.asarray(ns["N"])
f = ns["f"]
field_field = np.asarray(np.abs(f[0][0, 0]))
field_field_field = np.asarray(np.abs(f[6][0, 0, 0]))
k = float(ns["k"])

raw_path = OUTDIR / "raw_baseline.npz"
np.savez_compressed(
    raw_path,
    N=N,
    field_field=field_field,
    field_field_field=field_field_field,
    k=np.asarray([k], dtype=float),
)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

manifest = {
    "queue": "Q11 x COSMOFLOW V1.1",
    "stage": "REPRODUCIBLE BASELINE RUN + ENVIRONMENT LOCK + RAW OUTPUT MATERIALIZATION",
    "q11_scoring_performed": False,
    "source_example": "CosmoFlow/Massless_dphi3/MyFirstRun.py",
    "source_blob_shas": {
        "MyFirstRun.py": "79cba7fa3ef6381307ff4ba3801f20ba4628bd31",
        "Parameters.py": "91e75f63c7e0f2e10582a1f9a99a92bcb92819d5",
        "Theory.py": "b8fdeb6760c3d49b1e1eab95f721e549e5b54c47",
        "Solver.py": "8401cf3c512a3da87c8c32b50c291cb2af65b03f",
    },
    "environment": {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
    },
    "configuration": {
        "DeltaN": float(ns["DeltaN"]),
        "Nfield": int(ns["Nfield"]),
        "Rtol": float(ns["Rtol"]),
        "Atol": float(ns["Atol"]),
        "N_exit": float(ns["N_exit"]),
        "Ni": float(ns["Ni"]),
        "Nf": float(ns["Nf"]),
        "N_output_points": int(N.size),
        "kinematics": "equilateral",
        "k1": float(ns["k1"]),
        "k2": float(ns["k2"]),
        "k3": float(ns["k3"]),
    },
    "raw_output": {
        "path": str(raw_path.relative_to(ROOT)),
        "sha256": sha256(raw_path),
        "field_field_shape": list(field_field.shape),
        "field_field_field_shape": list(field_field_field.shape),
        "finite_field_field": bool(np.isfinite(field_field).all()),
        "finite_field_field_field": bool(np.isfinite(field_field_field).all()),
    },
}
manifest_path = OUTDIR / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
manifest["manifest_sha256"] = sha256(manifest_path)
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

print(json.dumps(manifest, indent=2, sort_keys=True))
