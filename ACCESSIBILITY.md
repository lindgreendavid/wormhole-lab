# Accessibility statement

Wormhole Lab is designed toward WCAG 2.2 Level AA, matching this maintainer's other
laboratories. This statement covers the public interactive site built from `site/`.

## What is supported

- Semantic landmarks, ordered headings, a skip link, descriptive page title, and visible
  keyboard focus.
- Full keyboard operation for every simulator control (throat radius, shape exponent, redshift
  preset, observation radius); no drag-only custom interaction — every control is a native
  `<input type="range">` or `<select>`.
- Live readouts use `role="status" aria-live="polite"` so a change in the null-energy-condition
  verdict is announced without requiring the visual embedding diagram to be perceived.
- Text labels, not color alone: the NEC verdict is always shown as a text string
  ("Satisfied" / "Violated (exotic matter required)"), and the light-bending outcome table
  states "Passes through the throat" / "Deflected back outward" as text, with color as a
  secondary cue only.
- A full accessible data table always accompanies the light-bending diagram, not hidden behind
  a script-only chart with no fallback.
- The "before you explore" limitations panel is shown **before** any simulator control, mirroring
  the reading-order discipline used across this maintainer's other research laboratories.
- High-contrast and forced-color mode support; reduced-motion support (the hero's embedding
  animation and smooth scrolling both respect `prefers-reduced-motion: reduce`).
- Reflow down to a 320 CSS-pixel viewport and support for 200% text zoom without hiding
  navigation destinations.
- No autoplay of audio/video, no flashing content, no time limits, no authentication walls.

## Verification

Every change passes semantic HTML assertions and `eslint-plugin-jsx-a11y`. The release
checklist also covers keyboard order, focus visibility, non-text alternatives, labels, zoom/
reflow, reduced motion, target size, and color-independent meaning. Automated checks cannot
prove accessibility or compatibility with every assistive-technology combination.

## Known limitations

- The embedding diagram and light-bending SVGs are inherently visual; the numeric readout grid
  and the light-bending outcome table are the non-visual equivalents, but they are a summary,
  not a point-by-point equivalent of the diagram.
- Mathematical notation is expressed as Unicode and plain text rather than MathML.
- The interface and documentation are currently in English.

## Feedback

Open an accessibility issue at
https://github.com/lindgreendavid/wormhole-lab/issues/new and include the page section,
browser, assistive technology, and expected behavior when possible. Security-sensitive reports
should use the private process in [`SECURITY.md`](SECURITY.md).

## Standard

The target is the W3C Web Content Accessibility Guidelines 2.2 Level AA:
https://www.w3.org/TR/WCAG22/. Conformance language is intentionally bounded: this is an
engineering statement and testing record, not a third-party accessibility certification.
