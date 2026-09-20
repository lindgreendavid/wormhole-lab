#!/usr/bin/env python3
"""Byte-exact (post-JSON-parse) comparison of two registry files. Exits non-zero on mismatch."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()

    with args.expected.open() as f:
        expected = json.load(f)
    with args.actual.open() as f:
        actual = json.load(f)

    if expected != actual:
        print("MISMATCH: registry does not match committed reports file", file=sys.stderr)
        return 1

    print("OK: registry matches committed reports file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
