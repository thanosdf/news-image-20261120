// The World in One Day, 20 November 2026.
//
// This program is the whole entry: the finished front page already sits
// beside this file as entry.png, drawn by draw.py, and all this program
// does is hand that finished image to the grader untouched.
//
// It runs on Node 22 with the standard library only, makes no network
// calls and reads no clock, so both runs write the same bytes.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
