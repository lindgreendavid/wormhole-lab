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
