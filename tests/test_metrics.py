import pytest

from wormhole_lab.metrics import RedshiftFunction, ShapeFunction


def test_shape_function_throat_condition():
    shape = ShapeFunction(r0=2.0, n=1.0)
    assert shape.b(2.0) == pytest.approx(2.0)


def test_shape_function_flare_out_matches_minus_n():
    for n in (0.0, 0.5, 1.0, 2.0):
        shape = ShapeFunction(r0=3.0, n=n)
        assert shape.flare_out_value() == pytest.approx(-n)
        assert shape.flare_out_value() < 1.0


def test_shape_function_b_prime_is_analytic_derivative():
    shape = ShapeFunction(r0=1.5, n=1.3)
    r = 4.0
    h = 1e-6
    numeric = (shape.b(r + h) - shape.b(r - h)) / (2 * h)
    assert shape.b_prime(r) == pytest.approx(numeric, rel=1e-6)


def test_shape_function_rejects_invalid_params():
    with pytest.raises(ValueError):
        ShapeFunction(r0=-1.0, n=1.0)
    with pytest.raises(ValueError):
        ShapeFunction(r0=1.0, n=-1.0)


def test_redshift_zero_preset_is_identically_zero():
    redshift = RedshiftFunction(kind="zero", r0=1.0)
    for r in (1.0, 2.0, 100.0):
        assert redshift.phi(r) == 0.0
        assert redshift.phi_prime(r) == 0.0
        assert redshift.phi_double_prime(r) == 0.0


def test_redshift_inverse_preset_derivatives_are_analytic():
    redshift = RedshiftFunction(kind="inverse", r0=2.0)
    r = 5.0
    h = 1e-6
    numeric_first = (redshift.phi(r + h) - redshift.phi(r - h)) / (2 * h)
    assert redshift.phi_prime(r) == pytest.approx(numeric_first, rel=1e-5)

    numeric_second = (redshift.phi_prime(r + h) - redshift.phi_prime(r - h)) / (2 * h)
    assert redshift.phi_double_prime(r) == pytest.approx(numeric_second, rel=1e-4)


def test_redshift_inverse_preset_finite_everywhere_and_decays():
    redshift = RedshiftFunction(kind="inverse", r0=1.0)
    assert abs(redshift.phi(1.0)) < 2.0
    assert abs(redshift.phi(1000.0)) < 1e-2


def test_redshift_rejects_unknown_preset():
    with pytest.raises(ValueError):
        RedshiftFunction(kind="bogus", r0=1.0)
