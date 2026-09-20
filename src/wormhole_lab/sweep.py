"""The deterministic parameter sweep that produces the frozen registry.

Unlike this maintainer's empirical studies (e.g. three-body-lab), there is no data to fit
and therefore no random seeding anywhere in this module: every entry is an exact,
deterministic evaluation of the closed-form expressions in `curvature`, `embedding`, and
`tidal` at disclosed (r0, n, redshift preset, r/r0) grid points. Re-running
`scripts/generate_registry.py` must always reproduce the committed registry byte-for-byte.
"""

from __future__ import annotations

from typing import Any

from wormhole_lab.curvature import stress_energy
from wormhole_lab.embedding import embedding_height, proper_radial_distance
from wormhole_lab.energy_conditions import evaluate
from wormhole_lab.metrics import RedshiftFunction, ShapeFunction
from wormhole_lab.tidal import static_observer_proper_acceleration

# Disclosed grid, fixed before interpretation (docs/research-protocol.md).
THROAT_RADII: tuple[float, ...] = (1.0, 5.0)
SHAPE_EXPONENTS: tuple[float, ...] = (0.0, 0.5, 1.0, 2.0)
REDSHIFT_PRESETS: tuple[str, ...] = ("zero", "inverse")
RADIUS_MULTIPLES: tuple[float, ...] = (
    1.0,
    1.01,
    1.1,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
    5.0,
    10.0,
    50.0,
)


def _round(value: float, digits: int = 12) -> float:
    """Round to a fixed precision so the registry is stable across platforms/library
    versions (quad's last-bit behavior can otherwise vary)."""
    return round(value, digits)


def compute_cell(r0: float, n: float, redshift_kind: str, radius_multiple: float) -> dict[str, Any]:
    shape = ShapeFunction(r0=r0, n=n)
    redshift = RedshiftFunction(kind=redshift_kind, r0=r0)
    r = r0 * radius_multiple

    se = stress_energy(r, shape, redshift)
    ec = evaluate(se)
    ell = proper_radial_distance(r, shape)
    z = embedding_height(r, shape)
    a_static = static_observer_proper_acceleration(r, shape, redshift)

    return {
        "r0": r0,
        "n": n,
        "redshift": redshift_kind,
        "radius_multiple": radius_multiple,
        "r": _round(r),
        "flare_out_value": _round(shape.flare_out_value()),
        "rho": _round(se.rho),
        "p_r": _round(se.p_r),
        "p_t": _round(se.p_t),
        "nec_radial": _round(ec.nec_radial),
        "nec_tangential": _round(ec.nec_tangential),
        "sec_trace": _round(ec.sec_trace),
        "nec_satisfied": ec.nec_satisfied,
        "wec_satisfied": ec.wec_satisfied,
        "sec_satisfied": ec.sec_satisfied,
        "proper_radial_distance": _round(ell),
        "embedding_height": _round(z),
        "static_observer_proper_acceleration": _round(a_static),
    }


def run_sweep() -> dict[str, Any]:
    cells: list[dict[str, Any]] = []
    for r0 in THROAT_RADII:
        for n in SHAPE_EXPONENTS:
            for redshift_kind in REDSHIFT_PRESETS:
                for radius_multiple in RADIUS_MULTIPLES:
                    cells.append(compute_cell(r0, n, redshift_kind, radius_multiple))

    return {
        "schema_version": "0.1",
        "grid": {
            "throat_radii": list(THROAT_RADII),
            "shape_exponents": list(SHAPE_EXPONENTS),
            "redshift_presets": list(REDSHIFT_PRESETS),
            "radius_multiples": list(RADIUS_MULTIPLES),
        },
        "cells": cells,
    }
