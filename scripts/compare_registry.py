#!/usr/bin/env python3
"""Compare two registries: exact for structure/ints/bools/strings, a narrow tolerance for floats.

`scipy.integrate.quad` and BLAS can differ in the last bits across platforms, which flips the 12th
decimal after rounding; a relative 1e-9 / absolute 1e-10 tolerance is far below any scientifically
relevant difference while still catching a wrong formula.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def equal(a: Any, b: Any) -> bool:
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b, strict=True))
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, float) or isinstance(b, float):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-10)
    return a == b


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()

    expected = json.loads(args.expected.read_text())
    actual = json.loads(args.actual.read_text())

    if not equal(expected, actual):
        print("MISMATCH: registry does not match committed reports file", file=sys.stderr)
        return 1

    print("OK: registry matches committed reports file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
