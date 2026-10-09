# Security policy

## Supported version

Security fixes are applied to the latest Wormhole Lab release. The project is research and
educational software; it performs deterministic closed-form general-relativity calculations
only, accepts no untrusted file uploads, and must not be treated as engineering guidance for
any real physical system.

## Reporting a vulnerability

Please use GitHub's private vulnerability-reporting flow for this repository. Do not include
secrets, personal data, or exploit payloads in a public issue.

## Dependency boundary

CI rejects known high-severity vulnerabilities in production web dependencies
(`pnpm audit --prod --audit-level high`). The interactive site accepts no user file uploads,
no authentication, and no server-side persistence of visitor input — every simulator control is
computed client-side from typed, bounded numeric inputs (throat radius and shape-function
preset selection only).

The `braces` package (GHSA-vfj7-8cjw-p6xm, stack exhaustion on deeply nested glob patterns) is a
transitive build-time dependency of the toolchain, absent from the deployed worker bundle. The advisory's
fixed version (3.0.4) was not yet published when this was recorded (latest 3.0.3), so it is tracked in
`site/pnpm-workspace.yaml` and `site/scripts/security-audit.mjs` until a fix ships. The site never evaluates
user-supplied glob patterns. The `sharp` and `source-map-js` advisories are fixed by `pnpm` overrides to
patched versions.
