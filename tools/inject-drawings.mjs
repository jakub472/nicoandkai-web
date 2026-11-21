// Generates the isometric "stepped massing" line drawings and injects them into index.html
// between <!--drawing:NAME--> ... <!--/drawing:NAME--> markers. Idempotent: run it after tweaking.
//
//   node tools/inject-drawings.mjs
//
// The drawing is an abstract concept sketch (terraced volumes stepping down a slope, a nod to
// the name "Ke Schodům"). It is NOT the architectural design of the building.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

// ---------- isometric projection ----------
const U = 54;                       // px per model unit
const C = Math.cos(Math.PI / 6);
const S = 0.5;
const P = (x, y, z) => [(x - y) * C * U, (x + y) * S * U - z * U];
const fmt = (n) => (Math.round(n * 10) / 10).toString();
const pts = (arr) => arr.map(([x, y, z]) => P(x, y, z)).map(([a, b]) => `${fmt(a)} ${fmt(b)}`);
const poly = (arr) => 'M' + pts(arr).join('L') + 'Z';
const line = (a, b) => `M${pts([a, b]).join('L')}`;

// ---------- model ----------
const STEP_W = 1.15, DEPTH = 3.6, FLOOR = 0.92;
const heights = [5.5, 4.6, 3.7, 2.8, 1.9];   // descending toward the viewer = terraces on a slope
const main = heights.map((h, i) => ({
  x0: i * STEP_W, x1: (i + 1) * STEP_W, y0: 0, y1: DEPTH, z0: 0, z1: h, ctx: false,
}));

// neighbouring massing (flat boxes): [cx, cy, w, d, h]
const neighbours = [
  [-3.1, 0.2, 2.2, 2.6, 1.5], [-3.0, 4.6, 2.0, 2.4, 1.2], [1.0, 6.9, 2.6, 2.0, 1.4],
  [4.4, 6.6, 2.0, 2.2, 1.0], [8.2, 5.0, 2.4, 2.4, 1.6], [8.6, 0.8, 2.2, 2.6, 1.3],
  [-3.4, -3.6, 2.6, 2.2, 1.1], [1.6, -3.4, 2.4, 2.0, 1.6], [6.2, -3.2, 2.2, 2.2, 1.0],
  [10.6, -2.2, 2.0, 2.4, 1.4],
].map(([cx, cy, w, d, h]) => ({
  x0: cx - w / 2, x1: cx + w / 2, y0: cy - d / 2, y1: cy + d / 2, z0: 0, z1: h, ctx: true,
}));

const faces = ({ x0, x1, y0, y1, z0, z1 }) => ({
  top: [[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]],
  left: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],    // plane y = y1
  right: [[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]],   // plane x = x1
});

function build({ id, label }) {
  const bounds = { x0: 1e9, y0: 1e9, x1: -1e9, y1: -1e9 };
  const track = (arr) => arr.forEach(([x, y, z]) => {
    const [a, b] = P(x, y, z);
    bounds.x0 = Math.min(bounds.x0, a); bounds.x1 = Math.max(bounds.x1, a);
    bounds.y0 = Math.min(bounds.y0, b); bounds.y1 = Math.max(bounds.y1, b);
  });

  // ground: site outline, two street lines, plot boundary
  const g = [[-6, -6, 0], [13, -6, 0], [13, 10, 0], [-6, 10, 0]];
  track(g);
  const plot = [[-0.6, -0.6, 0], [STEP_W * 5 + 0.6, -0.6, 0], [STEP_W * 5 + 0.6, DEPTH + 0.6, 0], [-0.6, DEPTH + 0.6, 0]];
  const ground =
    `<path class="d-ground" d="${poly(g)}"/>` +
    `<path class="d-ground d-dash" d="${line([-6, 8.6, 0], [13, 8.6, 0])}${line([-6, 4.9, 0], [13, 4.9, 0])}"/>` +
    `<path class="d-plot d-dash" d="${poly(plot)}"/>`;

  // painter's algorithm: far -> near, white fill hides what is behind
  const items = [...main, ...neighbours]
    .sort((a, b) => (a.x0 + a.x1 + a.y0 + a.y1) - (b.x0 + b.x1 + b.y0 + b.y1));

  let n = 0, body = '';
  for (const b of items) {
    const f = faces(b);
    track(f.top); track(f.left); track(f.right);
    const { x0, x1, y0, y1, z1 } = b;
    const st = () => (b.ctx ? '' : ` style="--i:${n++}"`);
    let s = `<g class="${b.ctx ? 'd-ctx' : 'd-main'}">`;
    s += `<path class="d-face" pathLength="1"${st()} d="${poly(f.left)}"/>`;
    s += `<path class="d-face" pathLength="1"${st()} d="${poly(f.right)}"/>`;
    s += `<path class="d-face" pathLength="1"${st()} d="${poly(f.top)}"/>`;

    if (b.ctx) {
      const m = 0.1;
      s += `<path class="d-detail" d="${poly([[x0 + m, y0 + m, z1], [x1 - m, y0 + m, z1], [x1 - m, y1 - m, z1], [x0 + m, y1 - m, z1]])}"/>`;
    } else {
      const m = 0.14;
      let d = poly([[x0 + m, y0 + m, z1], [x1 - m, y0 + m, z1], [x1 - m, y1 - m, z1], [x0 + m, y1 - m, z1]]);
      for (let k = 1; k * FLOOR < z1 - 0.2; k++) {
        const zf = k * FLOOR;
        d += line([x0, y1, zf], [x1, y1, zf]) + line([x1, y0, zf], [x1, y1, zf]);
      }
      let win = '';
      for (let k = 0; (k + 1) * FLOOR <= z1 + 0.01; k++) {
        const za = k * FLOOR + 0.3, zb = k * FLOOR + 0.72;
        win += poly([[x0 + 0.16, y1, za], [x1 - 0.16, y1, za], [x1 - 0.16, y1, zb], [x0 + 0.16, y1, zb]]);
        win += line([(x0 + x1) / 2, y1, za], [(x0 + x1) / 2, y1, zb]);
        win += poly([[x1, y0 + 0.35, za], [x1, y0 + 1.5, za], [x1, y0 + 1.5, zb], [x1, y0 + 0.35, zb]]);
        win += poly([[x1, y0 + 2.1, za], [x1, y1 - 0.35, za], [x1, y1 - 0.35, zb], [x1, y0 + 2.1, zb]]);
      }
      s += `<path class="d-detail" d="${d}"/><path class="d-window" d="${win}"/>`;
    }
    body += s + '</g>';
  }

  const pad = 26;
  const vb = [bounds.x0 - pad, bounds.y0 - pad, bounds.x1 - bounds.x0 + pad * 2, bounds.y1 - bounds.y0 + pad * 2]
    .map(fmt).join(' ');
  return `<svg class="drawing" id="${id}" viewBox="${vb}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">` +
    `<g class="d-ground-g">${ground}</g>${body}</svg>`;
}

const LABEL = 'Ilustrační axonometrické schéma terasovitě klesajících objemů';
const variants = {
  hero: build({ id: 'drawing-hero', label: LABEL }),
  project: build({ id: 'drawing-project', label: LABEL }),
};

const pages = ['index.html', 'ke-schodum/index.html'];
for (const rel of pages) {
  const file = join(root, rel);
  let html = readFileSync(file, 'utf8');
  const done = [];
  for (const [name, svg] of Object.entries(variants)) {
    const re = new RegExp(`(<!--drawing:${name}-->)[\\s\\S]*?(<!--/drawing:${name}-->)`);
    if (!re.test(html)) continue;
    html = html.replace(re, () => `<!--drawing:${name}-->\n${svg}\n<!--/drawing:${name}-->`);
    done.push(name);
  }
  writeFileSync(file, html);
  console.log(rel, '->', done.join(', ') || '(žádné značky)');
}
