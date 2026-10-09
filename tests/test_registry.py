import importlib.util
import json
from pathlib import Path

from wormhole_lab.sweep import run_sweep

ROOT = Path(__file__).parent.parent
REGISTRY_PATH = ROOT / "reports" / "v0.1-wormhole-registry.json"

_spec = importlib.util.spec_from_file_location(
    "compare_registry", ROOT / "scripts" / "compare_registry.py"
)
_compare = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_compare)


def test_frozen_registry_matches_generator():
    with REGISTRY_PATH.open() as f:
        frozen = json.load(f)
    assert _compare.equal(frozen, json.loads(json.dumps(run_sweep())))


def test_compare_tolerates_last_digit_noise_but_not_real_changes():
    assert _compare.equal({"a": [1.0, 2e-12]}, {"a": [1.0 + 1e-12, 3e-12]})
    assert not _compare.equal({"a": [1.0]}, {"a": [1.001]})
    assert not _compare.equal({"a": True}, {"a": 1})
    assert not _compare.equal({"a": 1}, {"b": 1})
    assert not _compare.equal([1], [1, 2])
    assert _compare.equal("x", "x")
