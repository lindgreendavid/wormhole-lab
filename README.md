# Wormhole Lab

<p><a href="https://github.com/lindgreendavid/lindgreendavid/tree/main/brand"><img src="https://raw.githubusercontent.com/lindgreendavid/lindgreendavid/main/brand/lab-notes-mark.svg" width="52" align="right" alt="Lab Notes research-cycle mark"></a></p>

**Part of the [Lab Notes Research Portfolio](https://blog-interactive.lindgreendavid.workers.dev/)** · General relativity · Question → established theory → open problem → boundary

A rigorous computed exploration of the Morris-Thorne traversable wormhole: the real
general-relativistic metric, the stress-energy it forces via the Einstein equations, and the
actual open problem that stress-energy implies.

**[Open the live interactive laboratory](https://wormhole-lab-interactive.lindgreendavid.workers.dev)**
· plain-language write-up on the `blog` hub: not yet published (see [`CHANGELOG.md`](CHANGELOG.md)).

**Research question:** does a spherically symmetric, static, horizon-free ("traversable")
wormhole exist as a valid solution of General Relativity — and if so, what does Einstein's
equations force the matter threading its throat to be?

This is **not** a claim that traversable wormholes exist in nature, and never implies otherwise.
It is a bounded, checkable exercise in classical General Relativity: implement the real
Morris & Thorne (1988) field equations exactly, verify the implementation two independent ways,
and report precisely what those equations do and do not require.

**Headline finding (v0.1.0):** every tested shape function satisfying the flare-out condition
(the geometric requirement for a wormhole "throat" to open outward rather than pinch shut)
forces a null-energy-condition violation at the throat, for every redshift-function preset
tested — confirming, by direct computation rather than by assertion, the textbook claim that
traversable wormholes require "exotic matter." That is a rigorously derived property of the
metric, not itself in question. The real open problem — which this repository does **not**
claim to solve — is that no matter is known to exist in the quantity and configuration such a
throat would require. Full reasoning and the disclosed limitations: see
[`docs/research-report.md`](docs/research-report.md).

## What this contributes

- An independently checkable implementation of the Morris-Thorne field equations: every
  formula is validated against (1) its Phi=0 "zero-tidal-force" closed form and (2) the
  general-relativistic energy-momentum conservation identity that must hold for *any* valid
  (rho, p_r, p_t, Phi) sourced from this metric — not against another simulation or a fitted
  dataset, since none exists for this problem.
- A frozen, deterministic registry of computed stress-energy, energy-condition, and geometric
  (embedding/proper-distance) quantities across a disclosed grid of throat radii, shape-function
  exponents, and redshift-function presets — reproducible byte-for-byte, same discipline as
  this maintainer's empirical laboratories.
- An honest statement of what is proven (NEC violation at the throat, forced by flare-out) vs.
  what remains a genuinely open problem (no known matter violates the NEC macroscopically) vs.
  what is explicitly this author's own exploratory framing, never presented as a result — see
  [`docs/research-report.md`](docs/research-report.md#exploratory-thesis-not-a-finding).
- An interactive way to *see* the embedding geometry and the exotic-matter requirement respond
  to the throat radius and shape function, rather than only being told the throat requires
  exotic matter.
- What it does **not** contribute: a claim that traversable wormholes exist or can be built, a
  full traveler tidal-force analysis (that requires the boosted Riemann tensor; out of scope
  for v0.1 — see [`docs/research-report.md`](docs/research-report.md#limitations)), or any
  quantum-gravitational treatment of the exotic-matter requirement.

## What's here

| Path | What it is |
| --- | --- |
| [`docs/research-protocol.md`](docs/research-protocol.md) | The preregistered hypotheses, the exact equations to be implemented, their literature source, and the independent checks that must pass — written before any registry existed. |
| [`docs/research-report.md`](docs/research-report.md) | What the frozen registry actually shows, hypothesis by hypothesis, the literature-grounded statement of the real open problem, disclosed limitations, and a clearly flagged exploratory-thesis section. |
| [`src/wormhole_lab/`](src/wormhole_lab/) | The Python package: shape/redshift function presets, the Einstein-tensor-derived stress-energy, energy-condition evaluation, embedding/proper-distance quadrature, and the static-observer proper-acceleration calculation. |
| [`tests/`](tests/) | Closed-form and conservation-identity regression tests, plus a byte-comparison test against the frozen registry. |
| [`reports/v0.1-wormhole-registry.json`](reports/v0.1-wormhole-registry.json) | The frozen, deterministic sweep output. |
| [`site/`](site/) | An interactive Next.js (vinext) laboratory: a live embedding-diagram/simulator with throat-radius and shape-function controls, and a light-bending geodesic view, built for Cloudflare Workers. |

## Run the calculator locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

# Print every computed quantity at one (r0, n, redshift, r) point:
wormhole-lab --r0 1.0 --n 1.0 --redshift zero --radius-multiple 1.0
```

## Reproduce the registry

```bash
source .venv/bin/activate
python scripts/generate_registry.py --output /tmp/v0.1-wormhole-registry.json
cmp reports/v0.1-wormhole-registry.json /tmp/v0.1-wormhole-registry.json  # should be silent
```

This is fully deterministic — every entry is an exact closed-form evaluation, with no fitting
and no random seeding anywhere in this package. CI runs the same comparison on every push.

## Run the interactive site locally

```bash
cd site
pnpm install
pnpm run dev      # local development server
pnpm run build    # production build (Cloudflare Workers target)
pnpm run test     # build + node --test
pnpm run lint     # eslint
```

`site/wrangler.jsonc` is configured for deployment to Cloudflare Workers as
`wormhole-lab-interactive`. This repository does not run `wrangler deploy` — that is a manual
step the maintainer runs after reviewing a build.

## Quality gates

```bash
ruff check .
ruff format --check .
mypy src
pytest                      # includes a 95% coverage gate
python -m build

cd site && pnpm run lint && pnpm run build && pnpm run test
```

## Scope and limitations (short version — full version in the report)

Classical General Relativity only (no quantum-gravitational treatment of the exotic-matter
requirement), static and spherically symmetric solutions only, no traveler-frame tidal-force
analysis (static-observer proper acceleration only), and a disclosed, arbitrary parameter grid
rather than an exhaustive search over shape/redshift functions. See
[`docs/research-protocol.md`](docs/research-protocol.md#scope-boundaries-declared-before-results)
and [`docs/research-report.md`](docs/research-report.md#limitations) for the complete,
disclosed list.

## License

MIT. See [`LICENSE`](LICENSE).

## Citation

See [`CITATION.cff`](CITATION.cff).
