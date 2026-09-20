"use client";

import { useId, useMemo, useState } from "react";
import { traceNullGeodesic, type RedshiftKind, type ShapeParams } from "./physics";

const N_OPTIONS = [0, 0.5, 1, 2] as const;

/**
 * Renders a set of real null-geodesic light rays (see `physics.ts::traceNullGeodesic`) around
 * a wormhole throat, in the (r, phi) plane of a single coordinate patch (r >= r0). Rays with a
 * small enough impact parameter reach the throat with the radicand still positive and are
 * drawn continuing through it (labeled, not visually extended into a second "universe" copy,
 * which this repository does not attempt to render). Rays with a larger impact parameter are
 * deflected at a genuine computed turning point and drawn bending back outward.
 */
export function LightBending() {
  const r0SliderId = useId();
  const nSelectId = useId();
  const redshiftSelectId = useId();

  const [r0, setR0] = useState(1);
  const [n, setN] = useState<(typeof N_OPTIONS)[number]>(1);
  const [redshift, setRedshift] = useState<RedshiftKind>("zero");

  const shape: ShapeParams = useMemo(() => ({ r0, n }), [r0, n]);
  const rStart = r0 * 8;
  const impactParameters = useMemo(() => [1.05, 1.4, 1.8, 2.4, 3.2].map((m) => m * r0), [r0]);

  const traces = useMemo(
    () =>
      impactParameters.map((bImp) => ({
        bImp,
        result: traceNullGeodesic(shape, redshift, bImp, rStart),
      })),
    [shape, redshift, rStart, impactParameters],
  );

  const scale = 140 / rStart;
  const center = { x: 150, y: 190 };

  function toXY(r: number, phi: number): string {
    const x = center.x + r * scale * Math.sin(phi);
    const y = center.y - r * scale * Math.cos(phi);
    return `${x},${y}`;
  }

  return (
    <div className="lab-grid">
      <div className="controls" aria-label="Light-bending controls">
        <div className="control">
          <label htmlFor={r0SliderId}>
            Throat radius r0
            <output htmlFor={r0SliderId}>{r0.toFixed(1)}</output>
          </label>
          <input
            id={r0SliderId}
            type="range"
            min={0.5}
            max={3}
            step={0.5}
            value={r0}
            onChange={(event) => setR0(Number(event.target.value))}
          />
        </div>
        <div className="control">
          <label htmlFor={nSelectId}>Shape-function exponent n</label>
          <select
            id={nSelectId}
            value={n}
            onChange={(event) => setN(Number(event.target.value) as (typeof N_OPTIONS)[number])}
          >
            {N_OPTIONS.map((value) => (
              <option key={value} value={value}>
                n = {value}
              </option>
            ))}
          </select>
        </div>
        <div className="control">
          <label htmlFor={redshiftSelectId}>Redshift function</label>
          <select
            id={redshiftSelectId}
            value={redshift}
            onChange={(event) => setRedshift(event.target.value as RedshiftKind)}
          >
            <option value="zero">Zero-tidal-force (Phi = 0)</option>
            <option value="inverse">Inverse (Phi = -r0/r)</option>
          </select>
        </div>
        <div className="mechanism-note">
          <span>What you&apos;re seeing</span>
          <strong>
            Five real null geodesics, each with a different impact parameter, integrated from
            dphi/dr = (b/r^2) / sqrt((1 - b(r)/r)(e^-2Phi - b^2/r^2)).
          </strong>
          <small>
            Rays that reach the throat without a turning point are drawn continuing into it
            (this view does not attempt to render a second universe on the far side). Rays with
            a larger impact parameter reach a genuine computed turning point and bend back out.
          </small>
        </div>
      </div>

      <div className="simulator-panel">
        <div className="panel-title">
          <div>
            <span>Light-bending view</span>
            <strong>Null geodesics near the throat</strong>
          </div>
        </div>
        <div className="diagram-wrap">
          <svg viewBox="0 0 300 380" role="img" aria-label="Light rays bending or passing through the wormhole throat">
            <circle cx={center.x} cy={center.y} r={r0 * scale} fill="none" stroke="var(--coral)" strokeWidth="2" />
            {traces.map(({ bImp, result }) => {
              const d = `M ${result.points.map((p) => toXY(p.r, p.phi)).join(" L ")}`;
              return (
                <path
                  key={bImp}
                  d={d}
                  fill="none"
                  stroke={result.throughThroat ? "var(--blue)" : "var(--acid)"}
                  strokeWidth="1.5"
                />
              );
            })}
          </svg>
        </div>
        <p className="diagram-caption">
          Magenta circle: the throat at r = r0. Blue rays: pass through the throat. Amber rays:
          deflected at a computed turning point outside the throat.
        </p>
        <table>
          <caption className="sr-only">Which rays pass through vs. deflect, by impact parameter</caption>
          <thead>
            <tr>
              <th scope="col">Impact parameter (× r0)</th>
              <th scope="col">Outcome</th>
            </tr>
          </thead>
          <tbody>
            {traces.map(({ bImp, result }) => (
              <tr key={bImp}>
                <td>{(bImp / r0).toFixed(2)}</td>
                <td>{result.throughThroat ? "Passes through the throat" : "Deflected back outward"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
