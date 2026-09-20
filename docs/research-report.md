# Research report (v0.1)

This report records what the frozen registry (`reports/v0.1-wormhole-registry.json`, 192
cells: 2 throat radii × 4 shape-function exponents × 2 redshift presets × 12 radii) actually
shows, hypothesis by hypothesis, against the protocol committed in
[`docs/research-protocol.md`](research-protocol.md). All quoted numbers are in geometrized
units (G = c = 1) and can be reproduced exactly with `python scripts/generate_registry.py`.

## Hypothesis disposition

### H1 — flare-out forces NEC violation at the throat: **confirmed**

For every tested `n > 0` (12 of the 16 `(r0, n, redshift)` combinations with a genuine throat),
`rho + p_r < 0` exactly at `r = r0`. Representative values at `r0 = 1`:

| n | redshift | rho + p_r at throat |
| --- | --- | --- |
| 0.5 | zero | -0.059683 |
| 1.0 | zero | -0.079577 |
| 2.0 | zero | -0.119366 |
| 1.0 | inverse | -0.079577 |

This is not a coincidence of the specific presets tested: for the power-law shape family used
throughout, `rho + p_r = (b'r - b)/(8*pi*r^3) = -(n+1) r0^(n+1) / (8*pi*r^(n+3))`, which is
negative at every radius for every `n > -1` — the sign is fixed by the flare-out condition
itself, not by a choice of redshift function. The `n = 0` (constant, "thin-shell") case is the
boundary case: `b' = 0` identically, so `rho = 0` everywhere and the NEC violation comes
entirely from `p_r = -b/(8*pi*r^3) < 0`.

### H2 — the zero-tidal-force preset requires exotic matter everywhere: **confirmed**

For the `"zero"` redshift preset, `rho + p_r < 0` at all 12 tested radii, for every tested
shape exponent, all the way out to `r = 50 r0` (the farthest point sampled). This is a real,
verified property of the classic Morris & Thorne (1988) example — not merely a throat-local
effect — and is precisely why later wormhole literature considers "patching" `b(r)` to a vacuum
(Schwarzschild) exterior beyond some finite cutoff radius to localize the exotic-matter region.
This repository does not implement such a patched construction; see Limitations.

### H3 — a non-zero redshift function can localize the violation: **confirmed in aggregate, falsified for the steepest tested shape function**

For three of the four tested shape exponents under the `"inverse"` preset, there is a genuine,
finite band of radii where the *full* NEC (`rho+p_r >= 0` **and** `rho+p_t >= 0`) is satisfied
— not just one component:

| n | radii (× r0) where full NEC holds |
| --- | --- |
| 0.0 | 2.0 (boundary value; `nec_radial = 0.0` exactly) |
| 0.5 | 1.8, 1.9, 2.0 |
| 1.0 | 1.7, 1.8 |
| 2.0 | *(none tested)* |

For `n = 1` at `r0 = 1`, for example: `nec_radial` crosses from `-0.000304` at `r=1.6r0` to
`+0.001065` at `r=1.7r0`, while `nec_tangential` crosses from `+0.001575` to `+0.000621` to
`-0.000380` between `r=1.6r0` and `r=1.9r0` — the two components cross zero at *different*
radii, and the full NEC is satisfied only in the narrow window between those two crossings.
Outside that window — both near the throat and far away — the NEC is violated again, for
different reasons on each side (the radial component near the throat, the tangential component
far away).

For `n = 2` (the steepest shape function tested), no sampled radius satisfies the full NEC:
`nec_tangential` is already negative by `r = 1.5 r0` (`-0.000146`), before `nec_radial` turns
positive (`r = 1.5r0`: `+0.000873`), so the two crossings do not produce an overlapping window
at this grid resolution. **H3 as stated ("there exists at least one configuration...") is
literally confirmed by the `n in {0, 0.5, 1}` cases, but it does not hold for every tested shape
function — the steeper the throat, the harder it is (in this family) to localize the
violation**, which is reported here rather than reframing H3 after the fact.

### H4 — asymptotic flatness: **confirmed**

`|rho|`, `|p_r|`, `|p_t|` decrease monotonically toward the largest sampled radius (`r = 50 r0`)
for all 16 combinations, with no exception.

## What is proven vs. what is the real open problem

- **Proven, by this direct computation** (not merely asserted): if a static, spherically
  symmetric metric of the Morris-Thorne form has a throat satisfying the flare-out condition,
  the Einstein equations force `rho + p_r < 0` there. This is not a property of any specific
  matter model — it is a geometric consequence of the metric itself, and it is what the
  wormhole literature means by "the throat requires exotic matter."
- **The actual open problem, which this repository does not claim to solve**: no form of
  matter has ever been observed, or is predicted by the Standard Model, to violate the null
  energy condition in a sustained, macroscopic way. The only theoretically established
  NEC-violating effects are quantum (e.g. the Casimir vacuum between conducting plates), and
  the magnitude and duration of negative energy density achievable by such effects is
  extremely small and tightly bounded by quantum inequalities (Ford & Roman and related work
  through the 1990s–2000s constrains how much negative energy can be sustained over how long a
  region, for any known quantum field). Whether *any* physical mechanism could supply
  macroscopic, sustained NEC-violating stress-energy of the kind a human-traversable throat
  would require is the genuine unsolved question — this repository computes precisely how much
  and where such matter would need to exist, and stops there.

## Limitations (declared, not discovered by a critic)

- **Classical GR only.** No semiclassical backreaction, no quantum-gravity treatment, no
  attempt to evaluate whether Casimir-like or other quantum effects could actually supply the
  computed stress-energy profile at the required scale.
- **Static, spherically symmetric solutions only.** Rotating or dynamical wormhole geometries
  are out of scope.
- **No traveler-frame tidal-force analysis.** `src/wormhole_lab/tidal.py` computes only the
  proper acceleration a *static* observer needs to maintain position — not the tidal force felt
  by a traveler moving through the throat, which requires boosting the Riemann tensor into the
  traveler's rest frame (Morris & Thorne 1988, Sec. V). This is a materially harder calculation
  that v0.1 does not attempt; a reader should not infer anything about traversal comfort or
  survivability from this repository's proper-acceleration numbers alone.
- **A disclosed, finite grid**, not an exhaustive search over the infinite-dimensional space of
  valid `(b(r), Phi(r))` pairs. The reported H3 result (localization fails for `n=2`) is
  specific to the power-law family and radius grid tested here; it is not a general theorem
  that steep throats can never be localized under any redshift function.
- **No claim of existence.** Nothing in this repository asserts that traversable wormholes
  exist, have been observed, or are physically realizable — only what the equations require
  *if* one did.

## Exploratory thesis (not a finding)

This section is explicitly a proposal for further investigation, not a result of this study,
and is flagged as such throughout.

The H3 finding above — that a non-zero redshift function can shrink the exotic-matter region to
a finite shell, and that the shell's existence depends on how steep the throat is — suggests a
narrow, well-posed follow-up question: **for the power-law shape family used here, does there
exist a critical exponent `n*` above which no choice of finite, asymptotically-vanishing
redshift function can produce an overlapping NEC-satisfying window, and if so, can `n*` be
computed exactly (rather than bracketed by a grid search) from the crossing conditions on
`rho+p_r` and `rho+p_t`?** Answering this would not resolve the exotic-matter problem (a
satisfied NEC away from the throat says nothing about whether the *required* violation at the
throat itself can be physically sourced), but it would sharpen exactly which geometric throat
shapes are "worth" pairing with a more exotic redshift function search, and which are not. This
is offered as a concrete next step, not as evidence that it will succeed.
