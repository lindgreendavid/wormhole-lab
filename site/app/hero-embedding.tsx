"use client";

import { embeddingHeight, type ShapeParams } from "./physics";

const SHAPE: ShapeParams = { r0: 1, n: 1 };

function funnelPath(mirrored: boolean): string {
  const points: string[] = [];
  const steps = 40;
  for (let i = 0; i <= steps; i++) {
    const r = SHAPE.r0 * (1 + (9 * i) / steps);
    const z = embeddingHeight(SHAPE, r) * (mirrored ? -1 : 1);
    points.push(`${40 + z * 6},${100 - r * 9}`);
  }
  return `M ${points.join(" L ")}`;
}

/** A small, autoplaying, looping rotation of the real Morris-Thorne embedding diagram
 * (n=1 shape function) used as the hero's decorative visual. Purely CSS-driven rotation
 * (no canvas, no JS animation loop) so it respects `prefers-reduced-motion` for free via
 * the stylesheet rule below. */
export function HeroEmbedding() {
  return (
    <svg
      className="hero-embedding"
      viewBox="0 0 80 110"
      role="img"
      aria-label="Rotating embedding diagram of the Morris-Thorne wormhole throat"
    >
      <style>{`
        .hero-embedding-spin { transform-origin: 40px 55px; animation: hero-embedding-rotate 8s linear infinite; }
        @keyframes hero-embedding-rotate { from { transform: scaleX(1); } 50% { transform: scaleX(-1); } to { transform: scaleX(1); } }
        @media (prefers-reduced-motion: reduce) { .hero-embedding-spin { animation: none; } }
      `}</style>
      <g className="hero-embedding-spin">
        <path d={funnelPath(false)} fill="none" stroke="var(--acid)" strokeWidth="1.5" />
        <path d={funnelPath(true)} fill="none" stroke="var(--coral)" strokeWidth="1.5" />
        <circle cx="40" cy="91" r="2.5" fill="var(--white)" />
      </g>
    </svg>
  );
}
