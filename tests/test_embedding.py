"""Numerical quadrature checked against the n=1 shape function's known closed forms.

For b(r) = r0^2 / r:
    l(r) = sqrt(r^2 - r0^2)            (proper radial distance)
    z(r) = r0 * arccosh(r / r0)        (embedding height)
"""

import math

import pytest

from wormhole_lab.embedding import embedding_height, proper_radial_distance
from wormhole_lab.metrics import ShapeFunction


@pytest.mark.parametrize("r0", [1.0, 2.5])
@pytest.mark.parametrize("multiple", [1.001, 1.1, 2.0, 10.0])
def test_proper_radial_distance_closed_form(r0, multiple):
    shape = ShapeFunction(r0=r0, n=1.0)
    r = r0 * multiple
    expected = math.sqrt(r**2 - r0**2)
    assert proper_radial_distance(r, shape) == pytest.approx(expected, rel=1e-5, abs=1e-6)


@pytest.mark.parametrize("r0", [1.0, 2.5])
@pytest.mark.parametrize("multiple", [1.001, 1.1, 2.0, 10.0])
def test_embedding_height_closed_form(r0, multiple):
    shape = ShapeFunction(r0=r0, n=1.0)
    r = r0 * multiple
    expected = r0 * math.acosh(r / r0)
    assert embedding_height(r, shape) == pytest.approx(expected, rel=1e-5, abs=1e-6)


def test_at_throat_both_are_zero():
    shape = ShapeFunction(r0=3.0, n=1.0)
    assert proper_radial_distance(3.0, shape) == 0.0
    assert embedding_height(3.0, shape) == 0.0


def test_monotonically_increasing_with_radius():
    shape = ShapeFunction(r0=1.0, n=1.0)
    radii = [1.01, 1.5, 2.0, 5.0, 20.0]
    ells = [proper_radial_distance(r, shape) for r in radii]
    zs = [embedding_height(r, shape) for r in radii]
    assert ells == sorted(ells)
    assert zs == sorted(zs)


def test_rejects_r_inside_throat():
    shape = ShapeFunction(r0=2.0, n=1.0)
    with pytest.raises(ValueError):
        proper_radial_distance(1.0, shape)
    with pytest.raises(ValueError):
        embedding_height(1.0, shape)
