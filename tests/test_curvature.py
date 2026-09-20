"""Correctness of the Einstein-tensor-derived stress-energy, checked two independent ways.

1. Against the Phi=0 ("zero-tidal-force") closed forms, which follow trivially from the
   general formula by setting Phi'=Phi''=0 -- a simpler sub-case that is unambiguous and
   widely reproduced in the literature.
2. Against the conservation identity that any (rho, p_r, p_t, Phi) sourced by a static,
   spherically symmetric metric via the Einstein equations MUST satisfy, as a consequence
   of the Bianchi identity (independent of the specific matter model):

       dp_r/dr = -(rho + p_r) Phi'(r) + (2/r) (p_t - p_r)

   If the implemented formulas contained an algebra error, this identity would fail.
"""

import math

import pytest

from wormhole_lab.curvature import stress_energy
from wormhole_lab.metrics import RedshiftFunction, ShapeFunction

PI = math.pi


@pytest.mark.parametrize("n", [0.0, 0.5, 1.0, 2.0])
@pytest.mark.parametrize("r0", [1.0, 3.0])
def test_zero_tidal_force_closed_forms(r0, n):
    shape = ShapeFunction(r0=r0, n=n)
    redshift = RedshiftFunction(kind="zero", r0=r0)
    for multiple in (1.2, 2.0, 5.0):
        r = r0 * multiple
        se = stress_energy(r, shape, redshift)
        b = shape.b(r)
        bp = shape.b_prime(r)

        expected_rho = bp / (8 * PI * r**2)
        expected_p_r = -b / (8 * PI * r**3)
        expected_p_t = (b - bp * r) / (16 * PI * r**3)

        assert se.rho == pytest.approx(expected_rho, rel=1e-10)
        assert se.p_r == pytest.approx(expected_p_r, rel=1e-10)
        assert se.p_t == pytest.approx(expected_p_t, rel=1e-8)


@pytest.mark.parametrize("redshift_kind", ["zero", "inverse"])
@pytest.mark.parametrize("n", [0.5, 1.0, 2.0])
def test_flare_out_implies_nec_violation_at_throat(redshift_kind, n):
    """The one qualitative claim this whole repo rests on: flare-out (b'(r0) < 1) forces
    rho + p_r < 0 at the throat, for *any* finite Phi (the Phi-dependent term in p_r is
    multiplied by (1 - b/r), which is exactly zero at the throat)."""
    r0 = 2.0
    shape = ShapeFunction(r0=r0, n=n)
    redshift = RedshiftFunction(kind=redshift_kind, r0=r0)
    se = stress_energy(r0, shape, redshift)
    assert se.rho + se.p_r < 0


@pytest.mark.parametrize("redshift_kind", ["zero", "inverse"])
@pytest.mark.parametrize("n", [0.5, 1.0, 2.0])
@pytest.mark.parametrize("r0", [1.0, 4.0])
def test_conservation_identity_holds(redshift_kind, n, r0):
    shape = ShapeFunction(r0=r0, n=n)
    redshift = RedshiftFunction(kind=redshift_kind, r0=r0)
    r = r0 * 3.0
    h = r0 * 1e-5

    se = stress_energy(r, shape, redshift)
    se_plus = stress_energy(r + h, shape, redshift)
    se_minus = stress_energy(r - h, shape, redshift)
    dpr_dr_numeric = (se_plus.p_r - se_minus.p_r) / (2 * h)

    phi_p = redshift.phi_prime(r)
    rhs = -(se.rho + se.p_r) * phi_p + (2 / r) * (se.p_t - se.p_r)

    assert dpr_dr_numeric == pytest.approx(rhs, abs=1e-8, rel=1e-6)


def test_stress_energy_rejects_r_inside_throat():
    shape = ShapeFunction(r0=2.0, n=1.0)
    redshift = RedshiftFunction(kind="zero", r0=2.0)
    with pytest.raises(ValueError):
        stress_energy(1.0, shape, redshift)
