# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-09-20

### Added

- A preregistered research protocol (`docs/research-protocol.md`) fixing the research
  question, the exact Morris-Thorne field equations to be implemented (with literature
  source), the disclosed shape/redshift function presets and radius grid, four falsifiable
  hypotheses, and two independent correctness checks (a closed-form reduction and a
  general-relativistic conservation identity) — committed before any registry existed.
- A validated Python implementation (`wormhole_lab`) of the Morris-Thorne metric's
  orthonormal-frame Einstein tensor, energy-condition evaluation, embedding-geometry
  quadrature, and static-observer proper acceleration; 100% branch-covered, regression-tested
  against both the zero-tidal-force closed forms and the conservation identity.
- A frozen, deterministic, byte-checked registry (`reports/v0.1-wormhole-registry.json`)
  covering a 2-throat-radius x 4-shape-exponent x 2-redshift-preset x 12-radius grid (192
  cells), with no randomness anywhere in the generator.
- A research report (`docs/research-report.md`) recording every hypothesis's disposition,
  including a hypothesis (H3) reported as confirmed only in aggregate and falsified for the
  steepest tested shape function, rather than reframed after the fact; a literature-grounded
  statement of the real open problem (the exotic-matter requirement); explicit limitations;
  and an "Exploratory thesis" section clearly flagged as a proposal, not a finding.
- Repository hygiene: `pyproject.toml` (ruff, mypy strict, pytest with a 95% coverage gate),
  CI (Python quality, registry byte-comparison, site lint/build/test), CodeQL, and the standard
  set of community/governance docs.
