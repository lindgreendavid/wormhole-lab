"""Command-line entry point: print a single computed cell for a chosen configuration."""

from __future__ import annotations

import argparse
import json

from wormhole_lab.sweep import compute_cell


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wormhole-lab",
        description="Compute Morris-Thorne wormhole quantities at one (r0, n, redshift, r) point.",
    )
    parser.add_argument("--r0", type=float, default=1.0, help="throat radius")
    parser.add_argument("--n", type=float, default=1.0, help="shape-function exponent")
    parser.add_argument(
        "--redshift", choices=["zero", "inverse"], default="zero", help="redshift-function preset"
    )
    parser.add_argument(
        "--radius-multiple", type=float, default=1.0, help="r expressed as a multiple of r0"
    )
    args = parser.parse_args()

    cell = compute_cell(args.r0, args.n, args.redshift, args.radius_multiple)
    print(json.dumps(cell, indent=2))


if __name__ == "__main__":
    main()
