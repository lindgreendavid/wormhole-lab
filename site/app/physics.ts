/**
 * Client-side port of the Morris-Thorne formulas in `src/wormhole_lab` (Python), plus a
 * null-geodesic tracer used only by the light-bending view. Every closed-form quantity here
 * mirrors the equations documented in `docs/research-protocol.md`; the geodesic tracer is
 * new (not present in the Python package) and is documented at its own definition below.
 *
 * This file intentionally duplicates the Python formulas rather than depending on a shared
 * package, so it is validated independently in `tests/rendered-html.test.mjs` against the
 * same closed forms the Python `tests/test_curvature.py` checks.
 */

export type RedshiftKind = "zero" | "inverse";

export interface ShapeParams {
  r0: number;
  n: number;
}

export function shapeB({ r0, n }: ShapeParams, r: number): number {
  return r0 ** (n + 1) / r ** n;
}

export function shapeBPrime({ r0, n }: ShapeParams, r: number): number {
  return (-n * r0 ** (n + 1)) / r ** (n + 1);
}

export function flareOutValue({ n }: ShapeParams): number {
  return -n;
}

export function phi(kind: RedshiftKind, r0: number, r: number): number {
  return kind === "zero" ? 0 : -r0 / r;
}

export function phiPrime(kind: RedshiftKind, r0: number, r: number): number {
  return kind === "zero" ? 0 : r0 / r ** 2;
}

export function phiDoublePrime(kind: RedshiftKind, r0: number, r: number): number {
  return kind === "zero" ? 0 : (-2 * r0) / r ** 3;
}

export interface StressEnergy {
  rho: number;
  pR: number;
  pT: number;
}

const PI = Math.PI;

function lambdaPrime(shape: ShapeParams, r: number): number {
  const b = shapeB(shape, r);
  const bp = shapeBPrime(shape, r);
  return (bp * r - b) / (2 * r ** 2 * (1 - b / r));
}

export function stressEnergy(shape: ShapeParams, redshift: RedshiftKind, r: number): StressEnergy {
  const b = shapeB(shape, r);
  const bp = shapeBPrime(shape, r);
  const rho = bp / (8 * PI * r ** 2);

  if (Math.abs(r - shape.r0) < 1e-12) {
    return { rho, pR: -b / (8 * PI * r ** 3), pT: 0 };
  }

  const oneMinusBOverR = 1 - b / r;
  const phiP = phiPrime(redshift, shape.r0, r);
  const phiPP = phiDoublePrime(redshift, shape.r0, r);
  const lamP = lambdaPrime(shape, r);

  const pR = (-b / r ** 3 + (2 * oneMinusBOverR * phiP) / r) / (8 * PI);
  const pT =
    (oneMinusBOverR * (phiPP + phiP ** 2 - lamP * phiP + (phiP - lamP) / r)) / (8 * PI);
  return { rho, pR, pT };
}

export interface EnergyConditions {
  necRadial: number;
  necTangential: number;
  necSatisfied: boolean;
}

export function energyConditions(se: StressEnergy): EnergyConditions {
  const necRadial = se.rho + se.pR;
  const necTangential = se.rho + se.pT;
  return { necRadial, necTangential, necSatisfied: necRadial >= 0 && necTangential >= 0 };
}

/** Composite (Simpson's rule) numerical integration on [a, b] with `steps` intervals (even). */
function integrate(f: (x: number) => number, a: number, b: number, steps = 400): number {
  const n = steps % 2 === 0 ? steps : steps + 1;
  const h = (b - a) / n;
  let sum = f(a) + f(b);
  for (let i = 1; i < n; i++) {
    const x = a + i * h;
    sum += (i % 2 === 0 ? 2 : 4) * f(x);
  }
  return (sum * h) / 3;
}

export function properRadialDistance(shape: ShapeParams, r: number): number {
  if (r <= shape.r0) return 0;
  return integrate((rp) => 1 / Math.sqrt(1 - shapeB(shape, rp) / rp), shape.r0 + 1e-9, r);
}

export function embeddingHeight(shape: ShapeParams, r: number): number {
  if (r <= shape.r0) return 0;
  return integrate((rp) => 1 / Math.sqrt(rp / shapeB(shape, rp) - 1), shape.r0 + 1e-9, r);
}

export function staticObserverAcceleration(
  shape: ShapeParams,
  redshift: RedshiftKind,
  r: number,
): number {
  return phiPrime(redshift, shape.r0, r) * Math.sqrt(1 - shapeB(shape, r) / r);
}

/**
 * Null-geodesic bending, computed from first principles for this metric.
 *
 * For an equatorial null geodesic with conserved impact parameter `bImp = L/E`, the radial
 * equation reduces (after the energy E cancels) to:
 *
 *   (dphi/dr)^2 = (bImp / r^2)^2 / [ (1 - b(r)/r) * (e^{-2 Phi(r)} - bImp^2 / r^2) ]
 *
 * derived directly from the null condition -e^{2Phi} dt^2 + dr^2/(1-b/r) + r^2 dphi^2 = 0
 * together with the two conserved quantities E = e^{2Phi} dt/dlambda, L = r^2 dphi/dlambda.
 * This is not present in the Python package; it is implemented here solely to drive the
 * light-bending visualization, and is checked in `tests/rendered-html.test.mjs` against the
 * flat-space limit (b, Phi -> 0), where a straight line r*sin(phi - phi0) = bImp is recovered.
 */
export interface GeodesicResult {
  points: { r: number; phi: number }[];
  /** true if the ray reached the throat without a turning point (passes through). */
  throughThroat: boolean;
}

function radicand(shape: ShapeParams, redshift: RedshiftKind, bImp: number, r: number): number {
  return Math.exp(-2 * phi(redshift, shape.r0, r)) - bImp ** 2 / r ** 2;
}

function dPhiDr(shape: ShapeParams, redshift: RedshiftKind, bImp: number, r: number): number {
  const oneMinusBOverR = 1 - shapeB(shape, r) / r;
  const rad = radicand(shape, redshift, bImp, r);
  if (oneMinusBOverR <= 0 || rad <= 0) return NaN;
  return bImp / r ** 2 / Math.sqrt(oneMinusBOverR * rad);
}

/**
 * Trace an equatorial null geodesic inbound from `rStart` toward the throat.
 *
 * Two outcomes: either the radicand stays positive all the way to r0 (the ray passes
 * through the throat, `throughThroat: true`), or it hits a genuine turning point at some
 * r_turn > r0 (the ray is deflected back out). In the second case the outgoing branch is
 * obtained by reflecting the incoming one about phi(r_turn) -- valid because |dphi/dr|
 * depends only on r, not on the direction of travel, so the trajectory is exactly
 * symmetric about the point of closest approach.
 */
export function traceNullGeodesic(
  shape: ShapeParams,
  redshift: RedshiftKind,
  bImp: number,
  rStart: number,
  steps = 600,
): GeodesicResult {
  const incoming: { r: number; phi: number }[] = [{ r: rStart, phi: 0 }];
  const dr = (shape.r0 - rStart) / steps;
  let phiVal = 0;
  let r = rStart;
  let throughThroat = true;

  for (let i = 1; i <= steps; i++) {
    const rNext = rStart + dr * i;
    const slope = dPhiDr(shape, redshift, bImp, rNext);
    if (Number.isNaN(slope)) {
      throughThroat = false;
      break;
    }
    phiVal += slope * dr;
    r = rNext;
    incoming.push({ r, phi: phiVal });
  }

  if (throughThroat) {
    return { points: incoming, throughThroat };
  }

  const phiTurn = incoming[incoming.length - 1].phi;
  const outgoing = incoming
    .slice(0, -1)
    .reverse()
    .map((p) => ({ r: p.r, phi: 2 * phiTurn - p.phi }));
  return { points: [...incoming, ...outgoing], throughThroat };
}
