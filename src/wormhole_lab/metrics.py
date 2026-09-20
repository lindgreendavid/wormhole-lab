"""The Morris-Thorne metric's two free functions: shape b(r) and redshift Phi(r).

Metric (Morris & Thorne 1988, eq. 1), geometrized units, signature -+++:

    ds^2 = -e^{2 Phi(r)} dt^2 + dr^2 / (1 - b(r)/r) + r^2 (dtheta^2 + sin^2(theta) dphi^2)

A wormhole solution requires, at the throat r = r0:
  - b(r0) = r0
  - the "flare-out" condition b'(r0) < 1 (the embedded surface must flare outward)
  - Phi(r) finite everywhere (no event horizon; this is what makes it traversable)

This module implements one disclosed one-parameter family of shape functions and two
disclosed redshift-function presets. Every function returns exact analytic derivatives —
no finite-difference approximation is used anywhere in this package.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShapeFunction:
    """b(r) = r0^(n+1) / r^n, the power-law family used throughout this study.

    n = 1 reproduces the original Morris & Thorne (1988) worked example, b(r) = r0^2 / r.
    n = 0 is the constant "thin-shell" case, b(r) = r0 for all r.
    Flare-out at the throat requires b'(r0) < 1; for this family b'(r0) = -n, so every
    n > -1 (in particular every n >= 0 tested here) satisfies flare-out.
    """

    r0: float
    n: float

    def __post_init__(self) -> None:
        if self.r0 <= 0:
            raise ValueError("r0 must be positive")
        if self.n <= -1:
            raise ValueError("n must be > -1 for the flare-out condition to hold")

    def b(self, r: float) -> float:
        return float(self.r0 ** (self.n + 1) / r**self.n)

    def b_prime(self, r: float) -> float:
        return float(-self.n * self.r0 ** (self.n + 1) / r ** (self.n + 1))

    def flare_out_value(self) -> float:
        """b'(r0); flare-out requires this to be < 1."""
        return self.b_prime(self.r0)


@dataclass(frozen=True)
class RedshiftFunction:
    """Phi(r) and its first two derivatives, for a named, disclosed preset.

    "zero": Phi(r) = 0 everywhere -- the "zero-tidal-force" wormhole (Morris & Thorne 1988,
        Section III). No proper acceleration is needed to remain static anywhere.
    "inverse": Phi(r) = -r0 / r -- finite everywhere (no horizon), -> 0 at infinity, a
        standard illustrative non-zero-redshift example from the wormhole literature.
    """

    kind: str
    r0: float

    def __post_init__(self) -> None:
        if self.kind not in ("zero", "inverse"):
            raise ValueError(f"unknown redshift preset: {self.kind!r}")

    def phi(self, r: float) -> float:
        if self.kind == "zero":
            return 0.0
        return -self.r0 / r

    def phi_prime(self, r: float) -> float:
        if self.kind == "zero":
            return 0.0
        return self.r0 / r**2

    def phi_double_prime(self, r: float) -> float:
        if self.kind == "zero":
            return 0.0
        return -2.0 * self.r0 / r**3
