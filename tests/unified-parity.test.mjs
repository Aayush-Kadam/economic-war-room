import test from "node:test";import assert from "node:assert/strict";import fs from "node:fs";import {deterministicUnified} from "../lib/unified-core.mjs";
const spec=JSON.parse(fs.readFileSync(new URL("../engine/unified_spec.json",import.meta.url),"utf8"));
const suite=JSON.parse(fs.readFileSync(new URL("./fixtures/unified_parity.json",import.meta.url),"utf8"));
const fields=["monthly_price_change","pce_yoy","output_gap","unemployment","financial_stress","policy_deviation_bp","policy_inflation_contribution","policy_output_contribution"];
for(const fixture of suite.fixtures)test(`Python/TypeScript parity ${fixture.name}`,()=>{const actual=deterministicUnified(spec,fixture.input,fixture.expected.length,fixture.shockSequence);let max=0;for(let i=0;i<actual.length;i++)for(const field of fields)max=Math.max(max,Math.abs(actual[i][field]-fixture.expected[i][field]));assert.ok(max<=suite.tolerance,`maximum difference ${max}`)});
