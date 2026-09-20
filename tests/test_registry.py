import json
from pathlib import Path

from wormhole_lab.sweep import run_sweep

REGISTRY_PATH = Path(__file__).parent.parent / "reports" / "v0.1-wormhole-registry.json"


def test_frozen_registry_matches_generator():
    with REGISTRY_PATH.open() as f:
        frozen = json.load(f)
    assert frozen == run_sweep()
