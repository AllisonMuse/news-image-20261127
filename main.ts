// The World in One Day - Friday 27 November 2026, third edition.
// Node 22, standard library only. The picture itself is entry.png beside
// this file, drawn by draw_v3.py; this program checks it and hands it to
// the grader's output directory.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const BYTE_CAP = 1024 * 1024;
const SIDE_CAP = 1024;

async function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const png = await readFile(join(here, "entry.png"));

  const signature = [...png.subarray(0, 8)];
  if (signature.join(",") !== PNG_SIGNATURE.join(",")) {
    throw new Error("entry.png does not start with the PNG signature");
  }
  if (png.length > BYTE_CAP) {
    throw new Error(`entry.png is ${png.length} bytes, over the 1 MiB cap`);
  }
  if (png.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk where one belongs");
  }
  const width = png.readUInt32BE(16);
  const height = png.readUInt32BE(20);
  if (width > SIDE_CAP || height > SIDE_CAP) {
    throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
  }

  // The entry is a pre-rendered picture: the bytes copied here are the
  // bytes draw_v3.py wrote, so two runs of this program always agree.
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  await mkdir(outDir, { recursive: true });
  const target = join(outDir, "entry.png");
  await writeFile(target, png);

  const back = await readFile(target);
  if (!back.equals(png)) {
    throw new Error("the copied entry.png differs from the source");
  }
  console.log(JSON.stringify({
    ok: true,
    file: "entry.png",
    width,
    height,
    bytes: png.length,
    sha256: createHash("sha256").update(png).digest("hex"),
  }));
}

await main();
