from wormhole_lab.sweep import (
    RADIUS_MULTIPLES,
    REDSHIFT_PRESETS,
    SHAPE_EXPONENTS,
    THROAT_RADII,
    compute_cell,
    run_sweep,
)


def test_compute_cell_has_expected_keys():
    cell = compute_cell(r0=1.0, n=1.0, redshift_kind="zero", radius_multiple=2.0)
    expected_keys = {
        "r0",
        "n",
        "redshift",
        "radius_multiple",
        "r",
        "flare_out_value",
        "rho",
        "p_r",
        "p_t",
        "nec_radial",
        "nec_tangential",
        "sec_trace",
        "nec_satisfied",
        "wec_satisfied",
        "sec_satisfied",
        "proper_radial_distance",
        "embedding_height",
        "static_observer_proper_acceleration",
    }
    assert set(cell.keys()) == expected_keys
    assert cell["r"] == 2.0


def test_run_sweep_covers_full_grid():
    registry = run_sweep()
    expected_cells = (
        len(THROAT_RADII) * len(SHAPE_EXPONENTS) * len(REDSHIFT_PRESETS) * len(RADIUS_MULTIPLES)
    )
    assert len(registry["cells"]) == expected_cells
    assert registry["grid"]["throat_radii"] == list(THROAT_RADII)


def test_run_sweep_is_deterministic():
    a = run_sweep()
    b = run_sweep()
    assert a == b


def test_throat_cells_always_violate_nec():
    registry = run_sweep()
    throat_cells = [c for c in registry["cells"] if c["radius_multiple"] == 1.0 and c["n"] > 0]
    assert throat_cells
    for cell in throat_cells:
        assert cell["nec_radial"] < 0
        assert cell["nec_satisfied"] is False
