# Contributing

Wormhole Lab welcomes small, evidence-backed changes.

1. Open an issue for new research scope or a change to what a computed quantity represents.
2. Create a focused branch.
3. Add or update tests and documentation with the implementation.
4. Run `pytest`, `ruff check .`, `ruff format --check .`, `mypy src`, `python -m build`, the
   registry generator with a byte comparison against the committed registry, and the complete
   web lint/build/test suite in `site/`.
5. Use English Conventional Commits and submit a draft pull request.

Never commit personal data, secrets, transient generated reports, or claims unsupported by the
implemented mathematics. The frozen release registry (`reports/v0.1-wormhole-registry.json`) is
a reviewed exception and may change only alongside its versioned protocol, generator, tests, and
report. Any new physics claim must state the exact equation implemented, its literature source,
and an independent correctness check (a closed-form special case or a conservation identity) —
see `docs/research-protocol.md` for the standard this project holds itself to. This repository
has no empirical dataset to fit against; do not imply a numeric fit or measurement where none
exists, and label any author's own proposed resolution to the open problem as an explicitly
flagged "Exploratory thesis," never as a finding.
