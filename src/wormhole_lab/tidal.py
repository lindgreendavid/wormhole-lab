"""What a *static* observer at radius r must do to stay put.

Scope note (see docs/research-report.md "Limitations"): this module deliberately stops
short of a full traveler tidal-force analysis. The tidal force felt by a moving traveler
requires the Riemann tensor boosted into the traveler's rest frame (Morris & Thorne 1988,
Section V) -- a substantially more involved calculation this v0.1 does not attempt. What
is implemented instead is the simpler, unambiguous proper acceleration a static observer
(one who is not falling, and not moving radially) must maintain against gravity:

    a_rhat(r) = Phi'(r) * sqrt(1 - b(r)/r)

This is the standard orthonormal-frame radial proper-acceleration result for any static
observer in a metric of the form ds^2 = -e^{2 Phi} dt^2 + dr^2/(1-b/r) + ...; it is the same
formula that reduces to the familiar Schwarzschild "hovering" acceleration
a = M / (r^2 sqrt(1 - 2M/r)) when Phi(r) = (1/2) ln(1 - 2M/r). For the zero-tidal-force
preset (Phi = 0) this is identically zero everywhere: a static observer anywhere in that
spacetime is already in free fall and needs no thrust to stay at fixed r, which is the
literal meaning of "zero-tidal-force" wormhole in Morris & Thorne's terminology.
"""

from __future__ import annotations

import math

from wormhole_lab.metrics import RedshiftFunction, ShapeFunction


def static_observer_proper_acceleration(
    r: float, shape: ShapeFunction, redshift: RedshiftFunction
) -> float:
    if r < shape.r0:
        raise ValueError("r must be at or outside the throat (r >= r0)")
    return redshift.phi_prime(r) * math.sqrt(1 - shape.b(r) / r)
