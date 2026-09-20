import test from "node:test";import assert from "node:assert/strict";import fs from "node:fs";
const page=fs.readFileSync(new URL("../app/page.tsx",import.meta.url),"utf8");
test("counterfactual disclaimer is visible",()=>assert.match(page,/model-generated counterfactuals/i));
test("interface exposes seven historical decisions",()=>assert.equal((page.match(/date:"2022-/g)||[]).length,7));
test("seeded simulation uses 1000 paths",()=>assert.match(page,/paths=1000/));
