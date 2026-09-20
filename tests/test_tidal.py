import math

import pytest

from wormhole_lab.metrics import RedshiftFunction, ShapeFunction
from wormhole_lab.tidal import static_observer_proper_acceleration


def test_zero_tidal_force_preset_needs_no_acceleration_anywhere():
    shape = ShapeFunction(r0=1.5, n=1.0)
    redshift = RedshiftFunction(kind="zero", r0=1.5)
    for multiple in (1.0, 1.5, 5.0, 100.0):
        r = 1.5 * multiple
        assert static_observer_proper_acceleration(r, shape, redshift) == 0.0


def test_inverse_preset_acceleration_vanishes_at_throat():
    """1 - b/r = 0 exactly at the throat, so the proper acceleration is zero there
    regardless of Phi'."""
    shape = ShapeFunction(r0=2.0, n=1.0)
    redshift = RedshiftFunction(kind="inverse", r0=2.0)
    assert static_observer_proper_acceleration(2.0, shape, redshift) == pytest.approx(0.0)


def test_inverse_preset_acceleration_matches_formula():
    r0 = 2.0
    shape = ShapeFunction(r0=r0, n=1.0)
    redshift = RedshiftFunction(kind="inverse", r0=r0)
    r = 6.0
    expected = (r0 / r**2) * math.sqrt(1 - (r0**2 / r) / r)
    assert static_observer_proper_acceleration(r, shape, redshift) == pytest.approx(expected)


def test_rejects_r_inside_throat():
    shape = ShapeFunction(r0=2.0, n=1.0)
    redshift = RedshiftFunction(kind="zero", r0=2.0)
    with pytest.raises(ValueError):
        static_observer_proper_acceleration(1.0, shape, redshift)
