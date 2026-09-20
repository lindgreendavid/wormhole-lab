"use client";

import { useId, useMemo, useState } from "react";
import {
  embeddingHeight,
  energyConditions,
  staticObserverAcceleration,
  stressEnergy,
  type RedshiftKind,
  type ShapeParams,
} from "./physics";

const SHAPE_EXPONENTS = [0, 0.5, 1, 2] as const;

function formatSci(value: number): string {
  if (Math.abs(value) < 1e-12) return "0";
  return value.toExponential(3);
}

function funnelPoints(shape: ShapeParams, maxMultiple: number, steps: number): [number, number][] {
  const pts: [number, number][] = [];
  for (let i = 0; i <= steps; i++) {
    const r = shape.r0 * (1 + ((maxMultiple - 1) * i) / steps);
    pts.push([r, embeddingHeight(shape, r)]);
  }
  return pts;
}

export function WormholeSimulator() {
  const r0SliderId = useId();
  const nSelectId = useId();
  const redshiftSelectId = useId();
  const radiusSliderId = useId();

  const [r0, setR0] = useState(1);
  const [n, setN] = useState<(typeof SHAPE_EXPONENTS)[number]>(1);
  const [redshift, setRedshift] = useState<RedshiftKind>("zero");
  const [radiusMultiple, setRadiusMultiple] = useState(1.7);

  const shape: ShapeParams = useMemo(() => ({ r0, n }), [r0, n]);
  const r = r0 * radiusMultiple;

  const se = useMemo(() => stressEnergy(shape, redshift, r), [shape, redshift, r]);
  const ec = useMemo(() => energyConditions(se), [se]);
  const accel = useMemo(
    () => staticObserverAcceleration(shape, redshift, r),
    [shape, redshift, r],
  );

  const maxMultiple = 3;
  const funnel = useMemo(() => funnelPoints(shape, maxMultiple, 60), [shape]);
  const zAtMax = funnel[funnel.length - 1][1] || 1;
  const scaleZ = 130 / zAtMax;
  const scaleR = 130 / (r0 * maxMultiple);

  const toSvg = ([rr, z]: [number, number]) => {
    const x = 150 + z * scaleZ;
    const y = 190 - rr * scaleR;
    return `${x},${y}`;
  };
  const pathTop = `M ${funnel.map(toSvg).join(" L ")}`;
  const pathBottom = `M ${funnel.map(([rr, z]) => toSvg([rr, -z])).join(" L ")}`;
  const markerY = 190 - r * scaleR;
  const markerXOffset = embeddingHeight(shape, r) * scaleZ;

  return (
    <div className="lab-grid">
      <div className="controls" aria-label="Wormhole simulator controls">
        <div className="control">
          <label htmlFor={r0SliderId}>
            Throat radius r0
            <output htmlFor={r0SliderId}>{r0.toFixed(1)}</output>
          </label>
          <input
            id={r0SliderId}
            type="range"
            min={0.5}
            max={5}
            step={0.5}
            value={r0}
            onChange={(event) => setR0(Number(event.target.value))}
          />
          <div className="range-labels">
            <span>0.5</span>
            <span>5.0</span>
          </div>
        </div>

        <div className="control">
          <label htmlFor={nSelectId}>Shape-function exponent n</label>
          <select
            id={nSelectId}
            value={n}
            onChange={(event) => setN(Number(event.target.value) as (typeof SHAPE_EXPONENTS)[number])}
          >
            {SHAPE_EXPONENTS.map((value) => (
              <option key={value} value={value}>
                n = {value} {value === 1 ? "(original Morris-Thorne example)" : ""}
                {value === 0 ? "(constant, thin-shell)" : ""}
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

        <div className="control">
          <label htmlFor={radiusSliderId}>
            Observe at r / r0
            <output htmlFor={radiusSliderId}>{radiusMultiple.toFixed(2)}</output>
          </label>
          <input
            id={radiusSliderId}
            type="range"
            min={1}
            max={maxMultiple}
            step={0.01}
            value={radiusMultiple}
            onChange={(event) => setRadiusMultiple(Number(event.target.value))}
          />
          <div className="range-labels">
            <span>throat</span>
            <span>{maxMultiple}r0</span>
          </div>
        </div>

        <div className="mechanism-note">
          <span>What you&apos;re seeing</span>
          <strong>
            The funnel is the real embedding diagram z(r) for this shape function, computed by
            numerical quadrature, not drawn by hand.
          </strong>
          <small>
            The marked point tracks where you are observing rho, p_r, and p_t. Drag &ldquo;Observe
            at r/r0&rdquo; toward the throat to watch the null-energy-condition readout flip.
          </small>
        </div>
      </div>

      <div className="simulator-panel">
        <div className="panel-title">
          <div>
            <span>Embedding diagram</span>
            <strong>Spatial slice through the throat</strong>
          </div>
        </div>
        <div className="diagram-wrap">
          <svg viewBox="0 0 300 380" role="img" aria-label="Embedding diagram of the wormhole throat with the current observation point marked">
            <path d={pathTop} fill="none" stroke="var(--acid)" strokeWidth="2" />
            <path d={pathBottom} fill="none" stroke="var(--acid)" strokeWidth="2" />
            <line x1="150" y1="10" x2="150" y2="370" stroke="#3a3450" strokeWidth="1" strokeDasharray="4 4" />
            <circle cx={150 + markerXOffset} cy={markerY} r="5" fill="var(--coral)" stroke="var(--white)" strokeWidth="1.5" />
            <circle cx={150 - markerXOffset} cy={markerY} r="5" fill="var(--coral)" stroke="var(--white)" strokeWidth="1.5" />
          </svg>
        </div>
        <p className="diagram-caption">
          Amber curve: z(r) = the real Morris-Thorne embedding height, integrated numerically from
          1/sqrt(r/b(r) - 1). Magenta markers: the radius currently selected by the slider.
        </p>

        <div className="readout-grid" role="status" aria-live="polite">
          <div>
            <span>rho (energy density)</span>
            <strong>{formatSci(se.rho)}</strong>
          </div>
          <div>
            <span>p_r (radial pressure)</span>
            <strong>{formatSci(se.pR)}</strong>
          </div>
          <div>
            <span>p_t (tangential pressure)</span>
            <strong>{formatSci(se.pT)}</strong>
          </div>
          <div>
            <span>Null energy condition</span>
            <strong className={ec.necSatisfied ? "is-satisfied" : "is-violated"}>
              {ec.necSatisfied ? "Satisfied" : "Violated (exotic matter required)"}
            </strong>
          </div>
          <div>
            <span>rho + p_r</span>
            <strong>{formatSci(ec.necRadial)}</strong>
          </div>
          <div>
            <span>Static-observer accel.</span>
            <strong>{formatSci(accel)}</strong>
          </div>
        </div>
      </div>
    </div>
  );
}
