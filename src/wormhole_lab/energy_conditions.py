"""Classical pointwise energy conditions, evaluated from the computed stress-energy.

Definitions (standard, e.g. Visser, *Lorentzian Wormholes*, Ch. 12):
  - Null energy condition   (NEC): rho + p_r >= 0  and  rho + p_t >= 0
  - Weak energy condition   (WEC): rho >= 0  and NEC
  - Strong energy condition (SEC): rho + p_r + 2 p_t >= 0  and NEC
"""

from __future__ import annotations

from dataclasses import dataclass

from wormhole_lab.curvature import StressEnergy


@dataclass(frozen=True)
class EnergyConditionReport:
    nec_radial: float  # rho + p_r
    nec_tangential: float  # rho + p_t
    sec_trace: float  # rho + p_r + 2 p_t
    nec_satisfied: bool
    wec_satisfied: bool
    sec_satisfied: bool


def evaluate(se: StressEnergy) -> EnergyConditionReport:
    nec_radial = se.rho + se.p_r
    nec_tangential = se.rho + se.p_t
    sec_trace = se.rho + se.p_r + 2 * se.p_t
    nec_ok = nec_radial >= 0 and nec_tangential >= 0
    wec_ok = nec_ok and se.rho >= 0
    sec_ok = nec_ok and sec_trace >= 0
    return EnergyConditionReport(
        nec_radial=nec_radial,
        nec_tangential=nec_tangential,
        sec_trace=sec_trace,
        nec_satisfied=nec_ok,
        wec_satisfied=wec_ok,
        sec_satisfied=sec_ok,
    )
