from wormhole_lab.curvature import stress_energy
from wormhole_lab.energy_conditions import evaluate
from wormhole_lab.metrics import RedshiftFunction, ShapeFunction


def test_nec_violated_at_throat_for_zero_tidal_force():
    shape = ShapeFunction(r0=1.0, n=1.0)
    redshift = RedshiftFunction(kind="zero", r0=1.0)
    se = stress_energy(1.0, shape, redshift)
    report = evaluate(se)
    assert report.nec_radial < 0
    assert not report.nec_satisfied
    assert not report.wec_satisfied
    assert not report.sec_satisfied


def test_zero_tidal_force_violates_nec_at_every_radius():
    """For the zero-tidal-force preset (Phi=0), rho + p_r = (b'r - b)/(8 pi r^3); for this
    package's whole power-law shape-function family b'r - b = -(n+1) r0^(n+1)/r^n < 0 for
    every n > -1, at every r -- not merely near the throat. This is a real, verified
    property of the classic Morris & Thorne (1988) worked example, and is why later
    wormhole constructions "patch" b(r) to vacuum beyond a finite radius to localize the
    exotic-matter region (out of scope for this repository; see the research report)."""
    shape = ShapeFunction(r0=1.0, n=1.0)
    redshift = RedshiftFunction(kind="zero", r0=1.0)
    for multiple in (1.001, 2.0, 1000.0, 1.0e6):
        se = stress_energy(multiple, shape, redshift)
        report = evaluate(se)
        assert report.nec_radial < 0
        assert not report.nec_satisfied


def test_inverse_redshift_has_a_finite_nec_satisfying_shell():
    """For the 'inverse' redshift preset, rho + p_r and rho + p_t each change sign once
    (verified numerically while developing this test), but at different radii: rho + p_r
    is negative near the throat and positive beyond r ~ 1.6 r0; rho + p_t is positive near
    the throat and negative beyond r ~ 1.8 r0. Between those two crossings there is a
    genuine finite shell where *both* are non-negative and the full NEC is satisfied --
    unlike the zero-tidal-force preset, which violates the NEC at every radius
    (see test_zero_tidal_force_violates_nec_at_every_radius). Outside that shell -- both
    near the throat and far away -- the NEC is violated again, for different reasons on
    each side."""
    shape = ShapeFunction(r0=1.0, n=1.0)
    redshift = RedshiftFunction(kind="inverse", r0=1.0)

    near = evaluate(stress_energy(1.1, shape, redshift))
    assert near.nec_radial < 0
    assert not near.nec_satisfied

    inside_shell = evaluate(stress_energy(1.7, shape, redshift))
    assert inside_shell.nec_radial > 0
    assert inside_shell.nec_tangential > 0
    assert inside_shell.nec_satisfied

    far = evaluate(stress_energy(1000.0, shape, redshift))
    assert far.nec_tangential < 0
    assert not far.nec_satisfied


def test_report_fields_are_internally_consistent():
    shape = ShapeFunction(r0=2.0, n=0.5)
    redshift = RedshiftFunction(kind="inverse", r0=2.0)
    se = stress_energy(3.0, shape, redshift)
    report = evaluate(se)
    assert report.nec_radial == se.rho + se.p_r
    assert report.nec_tangential == se.rho + se.p_t
    assert report.sec_trace == se.rho + se.p_r + 2 * se.p_t
    assert report.wec_satisfied == (report.nec_satisfied and se.rho >= 0)
    assert report.sec_satisfied == (report.nec_satisfied and report.sec_trace >= 0)
