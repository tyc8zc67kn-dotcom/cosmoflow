from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "q11_forensics" / "artifacts" / "v1.4r"
OUT.mkdir(parents=True, exist_ok=True)
V11 = ROOT / "q11_cosmoflow" / "artifacts" / "v1.1" / "raw_baseline.npz"
RUNNER = ROOT / "q11_cosmoflow" / "run_v1_1.py"

FROZEN_CONTAINER_SHA = "b3247d19e54dda0652b77649e2c5826ed44b5c633ad8a6d15b0e96319eec84e1"
REF_ARRAY = {
    "N": "d7875947f671da06a7b2337cf74d20d25361d2a949d4b38d2f7634aa60368c97",
    "field_field": "1b499519284fec668425fc62c34adb7dc58f5b90aa7e9b6b826da3cff7744560",
    "field_field_field": "8a2da84f5473a2b07afde360ce9291c07bf4000077b367717f4be24163991aaa",
    "k": "8dc7dd6e9f001c5f4dd575bf2754e7c9717af0823c8e522cf2e0abeb290b3157",
}
REF_MEMBER = {
    "N.npy": "d8ab82d5456d7146bfd4e9a42a23b1cffc0b6d7cc77a3fa04c427d070db56582",
    "field_field.npy": "1d3b6d6759d7a2d620800e87affe1d8520c888caf870c007321942293ceeba23",
    "field_field_field.npy": "76c38bd5f4c76072adca003d2a5bb0174e22ada825251557b25bb7c1900f28b5",
    "k.npy": "23dd9625d24644656662ca7303243396e67b51e057569add945ffb4505059573",
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_array_sha(arr: np.ndarray) -> str:
    a = np.ascontiguousarray(arr)
    h = hashlib.sha256()
    h.update(str(a.dtype).encode("utf-8"))
    h.update(b"\0")
    h.update(json.dumps(list(a.shape), separators=(",", ":")).encode("utf-8"))
    h.update(b"\0")
    h.update(a.tobytes(order="C"))
    return h.hexdigest()


def inspect_npz(path: Path) -> dict:
    record = {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": sha256_file(path),
        "file_size": path.stat().st_size,
        "zip_members": {},
        "arrays": {},
    }
    with zipfile.ZipFile(path, "r") as zf:
        for zi in zf.infolist():
            payload = zf.read(zi.filename)
            record["zip_members"][zi.filename] = {
                "date_time": list(zi.date_time),
                "crc": zi.CRC,
                "compress_size": zi.compress_size,
                "file_size": zi.file_size,
                "compress_type": zi.compress_type,
                "member_sha256": sha256_bytes(payload),
                "reference_member_sha256": REF_MEMBER.get(zi.filename),
                "matches_reference_member": (
                    zi.filename in REF_MEMBER and sha256_bytes(payload) == REF_MEMBER[zi.filename]
                ),
            }
    with np.load(path, allow_pickle=False) as data:
        if set(data.files) != set(REF_ARRAY):
            raise RuntimeError(f"unexpected arrays: {data.files}")
        for name in sorted(data.files):
            a = np.asarray(data[name])
            csha = canonical_array_sha(a)
            record["arrays"][name] = {
                "dtype": str(a.dtype),
                "shape": list(a.shape),
                "canonical_sha256": csha,
                "raw_c_order_sha256": sha256_bytes(np.ascontiguousarray(a).tobytes(order="C")),
                "reference_canonical_sha256": REF_ARRAY[name],
                "matches_reference": csha == REF_ARRAY[name],
            }
    record["all_arrays_match_reference"] = all(v["matches_reference"] for v in record["arrays"].values())
    record["all_members_match_reference"] = all(
        name in record["zip_members"] and record["zip_members"][name]["matches_reference_member"]
        for name in REF_MEMBER
    )
    return record


def run_once(label: str) -> dict:
    subprocess.run([sys.executable, str(RUNNER)], cwd=ROOT, check=True)
    target_dir = OUT / label
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = target_dir / "raw_baseline.npz"
    shutil.copy2(V11, copied)
    return inspect_npz(copied)


def main() -> None:
    report = {
        "queue": "Q11 x COSMOFLOW V1.4R",
        "purpose": "REPRODUCIBILITY GATE FORENSIC AUDIT",
        "q11_scoring_performed": False,
        "runner_modified": False,
        "expected_hash_modified": False,
        "frozen_container_sha256": FROZEN_CONTAINER_SHA,
        "reference_arrays": REF_ARRAY,
        "reference_members": REF_MEMBER,
    }
    try:
        a = run_once("run_a")
        b = run_once("run_b")
        report["run_a"] = a
        report["run_b"] = b

        same_decoded_between_runs = all(
            a["arrays"][name]["canonical_sha256"] == b["arrays"][name]["canonical_sha256"]
            for name in REF_ARRAY
        )
        all_ref_a = a["all_arrays_match_reference"]
        all_ref_b = b["all_arrays_match_reference"]
        byte_a = a["file_sha256"] == FROZEN_CONTAINER_SHA
        byte_b = b["file_sha256"] == FROZEN_CONTAINER_SHA

        report["comparison"] = {
            "decoded_arrays_identical_between_runs": same_decoded_between_runs,
            "run_a_matches_frozen_container": byte_a,
            "run_b_matches_frozen_container": byte_b,
            "run_a_all_arrays_match_reference": all_ref_a,
            "run_b_all_arrays_match_reference": all_ref_b,
            "run_a_all_members_match_reference": a["all_members_match_reference"],
            "run_b_all_members_match_reference": b["all_members_match_reference"],
        }

        if not same_decoded_between_runs:
            classification = "INTERNAL_NONDETERMINISM"
        elif not (all_ref_a and all_ref_b):
            classification = "NUMERICAL_CONTENT_MISMATCH"
        elif byte_a and byte_b:
            classification = "BYTE_IDENTICAL"
        else:
            classification = "SERIALIZATION_ONLY"
        report["classification"] = classification
    except Exception as exc:
        report["classification"] = "FORENSIC_ERROR"
        report["error"] = repr(exc)
        (OUT / "forensic_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        raise

    report_path = OUT / "forensic_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
