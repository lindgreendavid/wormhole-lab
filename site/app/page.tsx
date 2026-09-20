"use client";

import { useState } from "react";
import { HeroEmbedding } from "./hero-embedding";
import { WormholeSimulator } from "./wormhole-simulator";
import { LightBending } from "./light-bending";

const VIEWS = [
  {
    id: "simulator",
    label: "Embedding + stress-energy",
    blurb: "Adjust the throat and watch the real computed rho, p_r, p_t and NEC status change.",
  },
  {
    id: "geodesics",
    label: "Light-bending",
    blurb: "Real null geodesics, traced from the exact metric, passing or deflecting.",
  },
] as const;

export default function Home() {
  const [view, setView] = useState<(typeof VIEWS)[number]["id"]>("simulator");

  return (
    <>
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <nav className="nav">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">
            WH
          </span>
          <span>Wormhole Lab</span>
        </div>
        <div className="nav__links">
          <a href="#lab">Laboratory</a>
          <a href="#report">Report</a>
          <a href="#exploratory">Exploratory thesis</a>
          <a href="#sources">Sources</a>
        </div>
      </nav>

      <main id="main">
        <section className="hero">
          <div className="eyebrow">
            <span>General relativity</span>
            <span>Question → established theory → open problem → boundary</span>
          </div>
          <h1>
            The wormhole&apos;s throat requires <em>exotic matter</em>. Computed, not asserted.
          </h1>
          <p className="hero__lead">
            If a static, spherically symmetric, horizon-free wormhole exists, Einstein&apos;s
            equations force a specific, computable property on the matter at its throat. This
            laboratory implements the real Morris-Thorne (1988) field equations, checks the
            implementation two independent ways, and lets you see exactly what those equations
            require.
          </p>
          <div className="hero__demo">
            <HeroEmbedding />
            <p className="hero__demo-caption">
              The real embedding diagram, rotating — not a decorative illustration.
            </p>
          </div>
          <div className="hero__actions">
            <a className="button button--primary" href="#lab">
              Open the laboratory
            </a>
            <a
              className="button button--ghost"
              href="https://github.com/lindgreendavid/wormhole-lab"
            >
              View the repository
            </a>
          </div>
          <div className="hero__principles">
            <span>No claimed data fit</span>
            <span>Two independent correctness checks</span>
            <span>Falsified sub-case reported</span>
            <span>Open problem stated, not solved</span>
          </div>
        </section>

        <section className="lab" id="lab">
          <div className="section-heading">
            <div>
              <span className="section-index">01</span>
              <p>Laboratory</p>
            </div>
            <h2>See what the equations require</h2>
          </div>

          <div className="limitations-first">
            <h3>Before you explore: what this is and isn&apos;t</h3>
            <ul>
              <li>
                Every number below is an exact evaluation of the closed-form Morris-Thorne
                equations — there is no dataset being fit, and no claim that these wormholes
                exist.
              </li>
              <li>
                The light-bending view shows only one side of the throat; it does not attempt to
                render a second &ldquo;universe&rdquo; on the far side.
              </li>
              <li>
                Only a static observer&apos;s proper acceleration is computed — not a moving
                traveler&apos;s tidal forces, which need a harder calculation this repository
                does not attempt.
              </li>
            </ul>
          </div>

          <div className="view-tabs" role="tablist" aria-label="Laboratory view">
            {VIEWS.map((v) => (
              <button
                key={v.id}
                type="button"
                role="tab"
                aria-selected={view === v.id}
                className={view === v.id ? "is-active" : ""}
                onClick={() => setView(v.id)}
              >
                <span>{v.label}</span>
                <small>{v.blurb}</small>
              </button>
            ))}
          </div>

          {view === "simulator" ? <WormholeSimulator /> : <LightBending />}
        </section>

        <section className="decision">
          <div className="section-heading">
            <div>
              <span className="section-index">02</span>
              <p>Reading the result</p>
            </div>
            <h2>Three ways to read this</h2>
          </div>
          <div className="decision-reading">
            <article>
              <span>Proven</span>
              <h3>Flare-out forces NEC violation at the throat</h3>
              <p>
                Not a property of any specific matter model — a geometric consequence of the
                metric itself, confirmed by direct computation for every tested configuration.
              </p>
            </article>
            <article>
              <span>Open problem</span>
              <h3>No known matter violates the NEC macroscopically</h3>
              <p>
                The only established NEC-violating effects are quantum (e.g. the Casimir
                vacuum), and quantum inequalities tightly bound how much negative energy can be
                sustained, for how long. This repository computes the requirement; it does not
                supply the matter.
              </p>
            </article>
            <article>
              <span>Nuance</span>
              <h3>Localizing the violation depends on throat steepness</h3>
              <p>
                A non-zero redshift function can shrink the exotic-matter region to a finite
                shell for gentler throats — but this fails for the steepest shape function
                tested, reported here rather than smoothed over.
              </p>
            </article>
          </div>
        </section>

        <section className="report" id="report">
          <div className="section-heading section-heading--light">
            <div>
              <span className="section-index">03</span>
              <p>Research report</p>
            </div>
            <h2>Hypothesis disposition</h2>
          </div>

          <div className="equation-card">
            <div>
              <span>The metric under study</span>
              <code>ds² = -e^(2Φ(r)) dt² + dr²/(1-b(r)/r) + r² dΩ²</code>
              <code>Throat: b(r0) = r0, flare-out: b&apos;(r0) &lt; 1</code>
            </div>
            <p>
              Morris &amp; Thorne, <em>American Journal of Physics</em> 56, 395 (1988). Every
              quantity in this laboratory is derived from this metric&apos;s orthonormal-frame
              Einstein tensor — the standard result for a static, spherically symmetric
              spacetime.
            </p>
          </div>

          <table className="hypothesis-table">
            <caption className="sr-only">Preregistered hypotheses and their disposition</caption>
            <thead>
              <tr>
                <th scope="col">Hypothesis</th>
                <th scope="col">Disposition</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>H1 — flare-out forces NEC violation at the throat</td>
                <td>
                  <span className="disposition disposition--confirmed">Confirmed</span>
                </td>
              </tr>
              <tr>
                <td>H2 — zero-tidal-force preset requires exotic matter everywhere</td>
                <td>
                  <span className="disposition disposition--confirmed">Confirmed</span>
                </td>
              </tr>
              <tr>
                <td>H3 — a non-zero redshift function can localize the violation</td>
                <td>
                  <span className="disposition disposition--mixed">
                    Confirmed in aggregate; falsified for the steepest tested shape function
                  </span>
                </td>
              </tr>
              <tr>
                <td>H4 — asymptotic flatness</td>
                <td>
                  <span className="disposition disposition--confirmed">Confirmed</span>
                </td>
              </tr>
            </tbody>
          </table>
          <p>
            Full reasoning, exact registry values, and every disclosed limitation:{" "}
            <a href="https://github.com/lindgreendavid/wormhole-lab/blob/main/docs/research-report.md">
              docs/research-report.md
            </a>
            .
          </p>
        </section>

        <section className="exploratory" id="exploratory">
          <div className="section-heading">
            <div>
              <span className="section-index">04</span>
              <p>Not a finding</p>
            </div>
            <h2>Exploratory thesis</h2>
          </div>
          <div className="exploratory-note">
            <h3>A proposed follow-up question, explicitly flagged as speculative</h3>
            <p>
              The H3 result — that a non-zero redshift function can shrink the exotic-matter
              region to a finite shell, and that this depends on how steep the throat is —
              suggests a narrow, well-posed follow-up: for this power-law shape family, does a
              critical exponent exist above which no finite, asymptotically-vanishing redshift
              function can produce an overlapping NEC-satisfying window, and can it be derived
              exactly from the crossing conditions rather than bracketed by a grid search?
            </p>
            <p>
              This would not resolve the exotic-matter problem — a satisfied NEC away from the
              throat says nothing about whether the required violation at the throat itself can
              be physically sourced. It is offered as a concrete next step, not as evidence that
              it will succeed.
            </p>
          </div>
        </section>

        <section id="sources">
          <div className="section-heading">
            <div>
              <span className="section-index">05</span>
              <p>Research trail</p>
            </div>
            <h2>Sources</h2>
          </div>
          <div className="source-list">
            <a href="https://github.com/lindgreendavid/wormhole-lab">
              <span>Repository</span>
              <strong>wormhole-lab</strong>
              <p>The full implementation, tests, protocol, and frozen registry.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/wormhole-lab/blob/main/docs/research-protocol.md">
              <span>Protocol</span>
              <strong>docs/research-protocol.md</strong>
              <p>Preregistered before any registry existed.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/wormhole-lab/blob/main/docs/research-report.md">
              <span>Report</span>
              <strong>docs/research-report.md</strong>
              <p>Every hypothesis&apos;s disposition, limitations, and the exploratory thesis.</p>
              <b aria-hidden="true">→</b>
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div>
          <span className="brand__mark" aria-hidden="true">
            WH
          </span>
          <p>Part of the Lab Notes research portfolio.</p>
        </div>
        <a href="https://github.com/lindgreendavid/wormhole-lab/blob/main/ACCESSIBILITY.md">
          Accessibility statement
        </a>
      </footer>
    </>
  );
}
