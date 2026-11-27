// Second edition of the 27 November 2026 world-news image (Node 22,
// standard library only). The picture itself is entry.png beside this
// file, drawn by draw_day.py; this program validates it and copies it to
// the output directory the grader provides.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const MAX_BYTES = 1024 * 1024; // the gate takes at most 1 MiB
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(
    `entry.png is ${bytes.length} bytes, over the ${MAX_BYTES} byte cap`,
  );
}
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
const { width, height } = readPngSize(bytes);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const copied = readFileSync(target);
if (!copied.equals(bytes)) {
  throw new Error("copied entry.png does not match the source");
}
console.log(
  `entry.png: ${width}x${height}, ${bytes.length} bytes, ` +
    `sha256 ${createHash("sha256").update(bytes).digest("hex").slice(0, 16)}…`,
);

// Minimal PNG header parse: width and height live at bytes 16..24.
function readPngSize(buf) {
  if (buf.length < 24 || buf.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk");
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}
