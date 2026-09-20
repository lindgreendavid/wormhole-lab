"""Stress-energy implied by the metric, via the orthonormal-frame Einstein tensor.

For the general static, spherically symmetric metric

    ds^2 = -e^{2 Phi(r)} dt^2 + e^{2 Lambda(r)} dr^2 + r^2 dOmega^2,   e^{-2 Lambda} = 1 - b(r)/r

the Einstein equations G_(mu)(nu) = 8 pi T_(mu)(nu) give, in the orthonormal frame
(this is the standard result for this metric ansatz, e.g. Misner, Thorne & Wheeler
*Gravitation* Sec. 23.5; specialized to wormholes in Morris & Thorne 1988, eqs. 10-12):

    8 pi rho(r)  = b'(r) / r^2
    8 pi p_r(r)  = -b(r)/r^3 + 2 (1 - b(r)/r) Phi'(r) / r
    8 pi p_t(r)  = (1 - b(r)/r) [ Phi''(r) + Phi'(r)^2 - Lambda'(r) Phi'(r)
                                   + (Phi'(r) - Lambda'(r)) / r ]

with Lambda'(r) = (b'(r) r - b(r)) / (2 r^2 (1 - b(r)/r)).

Identifying T_that_that = rho, T_rhat_rhat = p_r, T_thetahat_thetahat = p_t (a static,
locally anisotropic perfect-fluid-like source, per Morris & Thorne).

This module does not trust the algebra above in isolation: ``tests/test_curvature.py``
checks it two independent ways -- (1) against the Phi=0 closed forms that follow directly
from setting Phi'=Phi''=0 above, and (2) against the general-relativistic conservation
identity dp_r/dr = -(rho + p_r) Phi' + (2/r)(p_t - p_r), which every physically consistent
(rho, p_r, p_t, Phi) derived from a metric via the Bianchi identity must satisfy exactly,
independent of any specific matter model.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from wormhole_lab.metrics import RedshiftFunction, ShapeFunction

PI = math.pi


@dataclass(frozen=True)
class StressEnergy:
    rho: float
    p_r: float
    p_t: float


def lambda_prime(r: float, shape: ShapeFunction) -> float:
    b = shape.b(r)
    bp = shape.b_prime(r)
    return (bp * r - b) / (2 * r**2 * (1 - b / r))


def stress_energy(r: float, shape: ShapeFunction, redshift: RedshiftFunction) -> StressEnergy:
    if r < shape.r0:
        raise ValueError("r must be at or outside the throat (r >= r0)")
    b = shape.b(r)
    bp = shape.b_prime(r)
    one_minus_b_over_r = 1 - b / r

    rho = bp / (8 * PI * r**2)

    if r == shape.r0:
        # 1 - b/r -> 0 exactly at the throat; the Phi'-dependent term vanishes there
        # (it is multiplied by (1 - b/r)), so both p_r and p_t reduce to their
        # Phi-independent throat values.
        p_r = -b / (8 * PI * r**3)
        p_t = 0.0
        return StressEnergy(rho=rho, p_r=p_r, p_t=p_t)

    phi_p = redshift.phi_prime(r)
    phi_pp = redshift.phi_double_prime(r)
    lam_p = lambda_prime(r, shape)

    p_r = (-b / r**3 + 2 * one_minus_b_over_r * phi_p / r) / (8 * PI)
    p_t = one_minus_b_over_r * (phi_pp + phi_p**2 - lam_p * phi_p + (phi_p - lam_p) / r) / (8 * PI)
    return StressEnergy(rho=rho, p_r=p_r, p_t=p_t)
