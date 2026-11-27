// The World in One Day — 27 November 2026.
// Entry program for make.fun's "Sum up 27 November's world news in one
// image" bounty. The picture itself was drawn at build time by draw_day.py
// and ships in this repository as entry.png; this program's job is to hand
// that exact file to the grader, unchanged, in the output directory the
// grader names. It does no drawing, so both runs write identical bytes.
//
// Node 22, standard library only. Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ONE_MIB = 1024 * 1024;

const scriptDir = dirname(fileURLToPath(import.meta.url));
const picturePath = resolve(scriptDir, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

const picture = readFileSync(picturePath);
if (picture.length === 0) {
  throw new Error("entry.png is empty");
}
if (picture.length > ONE_MIB) {
  throw new Error(
    `entry.png is ${picture.length} bytes, over the 1 MiB limit`,
  );
}

mkdirSync(outDir, { recursive: true });
const target = resolve(outDir, "entry.png");
writeFileSync(target, picture);
console.log(`entry.png (${picture.length} bytes) -> ${target}`);
