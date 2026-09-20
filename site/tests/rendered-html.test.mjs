import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the finished laboratory", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>Wormhole Lab/);
  assert.match(html, /exotic matter/i);
  assert.match(html, /Morris-Thorne/);
  assert.match(html, /Embedding \+ stress-energy/);
  assert.match(html, /Light-bending/);
  assert.match(html, /Hypothesis disposition/);
  assert.match(html, /Confirmed in aggregate; falsified for the steepest tested shape function/);
  assert.match(html, /Exploratory thesis/);
  assert.match(html, /Skip to main content/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Starter Project/);
});

test("ships accessible controls and research boundaries", async () => {
  const [page, simulator, lightBending, layout, styles, packageJson] = await Promise.all([
    readFile(new URL("app/page.tsx", root), "utf8"),
    readFile(new URL("app/wormhole-simulator.tsx", root), "utf8"),
    readFile(new URL("app/light-bending.tsx", root), "utf8"),
    readFile(new URL("app/layout.tsx", root), "utf8"),
    readFile(new URL("app/globals.css", root), "utf8"),
    readFile(new URL("package.json", root), "utf8"),
  ]);
  assert.match(simulator, /aria-label="Wormhole simulator controls"/);
  assert.match(simulator, /htmlFor=\{r0SliderId\}/);
  assert.match(simulator, /role="status" aria-live="polite"/);
  assert.match(lightBending, /aria-label="Light-bending controls"/);
  assert.match(page, /className="skip-link"/);
  assert.match(page, /role="tablist"/);
  assert.match(styles, /prefers-contrast: more/);
  assert.match(styles, /forced-colors: active/);
  assert.match(styles, /prefers-reduced-motion: reduce/);
  assert.match(layout, /Wormhole Lab/);
  assert.doesNotMatch(packageJson, /react-loading-skeleton|drizzle/);
});

test("ships the complete frozen wormhole registry into the interactive release", async () => {
  const registry = JSON.parse(
    await readFile(new URL("../reports/v0.1-wormhole-registry.json", root), "utf8"),
  );
  assert.equal(registry.schema_version, "0.1");
  assert.ok(registry.cells.length > 0);
  assert.ok(
    registry.cells.every((cell) => typeof cell.nec_satisfied === "boolean"),
    "every cell must report an NEC satisfaction boolean",
  );
});
