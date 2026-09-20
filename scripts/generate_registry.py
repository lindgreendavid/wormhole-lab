#!/usr/bin/env python3
"""Regenerate the frozen wormhole registry. Deterministic: no seeds, no randomness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wormhole_lab.sweep import run_sweep


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "reports" / "v0.1-wormhole-registry.json",
    )
    args = parser.parse_args()

    registry = run_sweep()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        json.dump(registry, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
