"""The two standard geometric diagnostics of a wormhole's spatial slice.

Proper radial distance (Morris & Thorne 1988, eq. 3):

    l(r) = +/- integral_{r0}^{r} dr' / sqrt(1 - b(r')/r')

Embedding height, from embedding the equatorial slice as a surface of revolution
z = z(r) in flat 3-space (Morris & Thorne 1988, eq. 4a):

    dz/dr = +/- 1 / sqrt(r/b(r) - 1)

Both are computed here by numerical quadrature (`scipy.integrate.quad`), not a
memorized closed form, so they apply to any shape function in this package. For the
n=1 shape function (b = r0^2/r, the original Morris-Thorne worked example) both
integrals have known closed forms:

    l(r) = sqrt(r^2 - r0^2)
    z(r) = r0 * arccosh(r/r0)

`tests/test_embedding.py` checks the numerical quadrature against these closed forms.
"""

from __future__ import annotations

import math

from scipy.integrate import quad

from wormhole_lab.metrics import ShapeFunction


def proper_radial_distance(r: float, shape: ShapeFunction) -> float:
    if r < shape.r0:
        raise ValueError("r must be at or outside the throat (r >= r0)")
    if r == shape.r0:
        return 0.0

    def integrand(rp: float) -> float:
        return 1.0 / math.sqrt(1 - shape.b(rp) / rp)

    value, _ = quad(integrand, shape.r0, r, limit=200)
    return float(value)


def embedding_height(r: float, shape: ShapeFunction) -> float:
    if r < shape.r0:
        raise ValueError("r must be at or outside the throat (r >= r0)")
    if r == shape.r0:
        return 0.0

    def integrand(rp: float) -> float:
        return 1.0 / math.sqrt(rp / shape.b(rp) - 1)

    value, _ = quad(integrand, shape.r0, r, limit=200)
    return float(value)
