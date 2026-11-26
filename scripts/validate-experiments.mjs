#!/usr/bin/env node
/**
 * Checks evidence-bearing experiment travelers without claiming any field work.
 * The public repository only accepts anonymized/safe evidence references.
 */
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const recordsDirectory = resolve(root, 'experiments');
const idPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function text(value) { return typeof value === 'string' && value.trim().length > 0; }
function date(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}
function nonnegative(value) { return typeof value === 'number' && Number.isFinite(value) && value >= 0; }
function nullableNumber(value) { return value === null || nonnegative(value); }
function own(value, key) { return Object.prototype.hasOwnProperty.call(value ?? {}, key); }

function evidenceReference(ref, repoRoot) {
  if (typeof ref !== 'string' || !ref.trim()) return false;
  if (/^https:\/\/[^\s]+$/.test(ref)) return true;
  if (isAbsolute(ref) || ref.includes('\\') || ref.includes('#') || ref.includes('?')) return false;
  const full = resolve(repoRoot, ref);
  const rel = relative(repoRoot, full);
  return rel !== '' && rel !== '..' && !rel.startsWith(`..${sep}`) && existsSync(full);
}

export function validateExperiment(record, history, repoRoot = root) {
  const errors = [];
  const alerts = [];
  const add = message => errors.push(message);
  if (!record || typeof record !== 'object' || Array.isArray(record)) return { errors: ['record must be an object'], alerts };
  if (record.schema_version !== 1) add('schema_version must be 1');
  if (!text(record.id) || !idPattern.test(record.id)) add('id must be a lowercase hyphenated slug');
  const ideas = new Set((history?.ideas ?? []).map(item => item.id));
  if (!ideas.has(record.idea)) add('idea must reference a known decision-history idea');
  const event = (history?.events ?? []).find(item => item.id === record.history_event_id);
  if (!event || event.idea !== record.idea || !['hypothesis', 'experiment'].includes(event.kind)) {
    add('history_event_id must reference a hypothesis or experiment event for this idea');
  }
  const states = new Set(['PLANNED', 'RUNNING', 'COMPLETED', 'CANCELLED']);
  if (!states.has(record.state)) add('state must be PLANNED, RUNNING, COMPLETED or CANCELLED');

  const p = record.plan ?? {};
  for (const field of ['hypothesis', 'customer_segment', 'method', 'success_definition']) {
    if (!text(p[field])) add(`plan.${field} must contain text`);
  }
  if (!date(p.registered_on)) add('plan.registered_on must be a valid date');
  if (!Number.isInteger(p.minimum_sample) || p.minimum_sample <= 0) add('plan.minimum_sample must be a positive integer');
  if (!nonnegative(p.target_success_rate) || p.target_success_rate > 1) add('plan.target_success_rate must be 0–1');
  for (const field of ['budget_cap_usd', 'owner_hours_cap']) {
    if (!own(p, field) || !nullableNumber(p[field])) add(`plan.${field} must be a nonnegative number or explicit null (unknown)`);
  }

  const a = record.authorization ?? {};
  if (!['NOT_APPROVED', 'APPROVED'].includes(a.status)) add('authorization.status must be NOT_APPROVED or APPROVED');
  if (a.status === 'APPROVED' && (!text(a.approved_by) || !date(a.approved_on))) {
    add('approved experiments require approver and approval date');
  }
  if (a.status === 'NOT_APPROVED' && (a.approved_by !== null || a.approved_on !== null)) {
    add('unapproved experiments cannot carry approval details');
  }

  const o = record.observation ?? {};
  for (const field of ['sample', 'successes']) {
    if (o[field] !== null && (!Number.isInteger(o[field]) || o[field] < 0)) add(`observation.${field} must be a nonnegative integer or null`);
  }
  if (o.sample !== null && o.successes !== null && o.successes > o.sample) add('successes cannot exceed sample');
  for (const field of ['spent_usd', 'owner_hours']) {
    if (!own(o, field) || !nullableNumber(o[field])) add(`observation.${field} must be a nonnegative number or explicit null (unknown)`);
  }
  if (!Array.isArray(o.evidence)) add('observation.evidence must be an array');
  else for (const [i, ref] of o.evidence.entries()) {
    if (!evidenceReference(ref, repoRoot)) add(`observation.evidence[${i}] must be an existing repository path or HTTPS source`);
  }
  if (record.state === 'PLANNED') {
    if (o.started_on !== null || o.finished_on !== null || o.sample !== null || o.successes !== null || o.spent_usd !== null || o.owner_hours !== null || o.evidence?.length) {
      add('PLANNED must not imply any recorded execution or observations');
    }
  } else if (record.state === 'RUNNING' || record.state === 'COMPLETED') {
    if (a.status !== 'APPROVED') add('RUNNING and COMPLETED require explicit owner authorization');
    if (!date(o.started_on)) add('RUNNING and COMPLETED require observation.started_on');
    if (date(o.started_on) && date(p.registered_on) && p.registered_on > o.started_on) add('plan must be registered before the observed start date');
    if (date(o.started_on) && date(a.approved_on) && a.approved_on > o.started_on) add('approval date cannot follow the observed start date');
    if (record.state === 'RUNNING' && o.finished_on !== null) add('RUNNING cannot have a finished_on date');
  }
  if (record.state === 'COMPLETED') {
    if (!date(o.finished_on) || (date(o.started_on) && o.finished_on < o.started_on)) add('COMPLETED requires finished_on not before started_on');
    if (!Number.isInteger(o.sample) || o.sample < 0 || !Number.isInteger(o.successes) || o.successes < 0) add('COMPLETED requires measured sample and successes');
    if (!Array.isArray(o.evidence) || o.evidence.length === 0) add('COMPLETED requires at least one evidence reference');
  }
  if (record.state === 'CANCELLED' && (!date(o.finished_on) || !text(record.cancellation_reason))) {
    add('CANCELLED requires a date and explicit reason');
  }

  const d = record.owner_decision ?? {};
  if (!['PENDING', 'CONTINUE', 'CHANGE', 'STOP'].includes(d.status)) add('owner_decision.status is invalid');
  if (d.status !== 'PENDING') {
    if (!['COMPLETED', 'CANCELLED'].includes(record.state)) add('owner decision cannot precede completion or cancellation');
    if (!text(d.decided_by) || !date(d.decided_on) || !text(d.why)) add('owner decision requires who, date and rationale');
    if (date(d.decided_on) && date(o.finished_on) && d.decided_on < o.finished_on) add('owner decision cannot predate the experiment finish');
  } else if (d.decided_by !== null || d.decided_on !== null || d.why !== null) {
    add('PENDING cannot be represented as an implicit owner decision');
  }

  if (nonnegative(p.budget_cap_usd) && nonnegative(o.spent_usd) && o.spent_usd > p.budget_cap_usd) {
    alerts.push('BUDGET_OVERRUN: do not conceal this truthful observation; escalate for review');
  }
  if (nonnegative(p.owner_hours_cap) && nonnegative(o.owner_hours) && o.owner_hours > p.owner_hours_cap) {
    alerts.push('OWNER_TIME_OVERRUN: escalate for review');
  }
  return { errors, alerts };
}

export function experimentResult(record) {
  if (record.state !== 'COMPLETED') return 'NOT_MEASURED';
  const p = record.plan, o = record.observation;
  if (!Number.isInteger(o.sample) || o.sample < p.minimum_sample || o.sample === 0) return 'INCONCLUSIVE';
  return o.successes / o.sample >= p.target_success_rate ? 'MET_PREDECLARED_THRESHOLD' : 'MISSED_PREDECLARED_THRESHOLD';
}

export function summarize(records) {
  const completed = records.filter(x => x.state === 'COMPLETED');
  const measured = completed.filter(x => experimentResult(x) !== 'INCONCLUSIVE');
  const allKnown = completed.every(x => nonnegative(x.observation.spent_usd) && nonnegative(x.observation.owner_hours));
  return {
    records: records.length,
    planned: records.filter(x => x.state === 'PLANNED').length,
    running: records.filter(x => x.state === 'RUNNING').length,
    completed: completed.length,
    evaluable: measured.length,
    passed_threshold: measured.filter(x => experimentResult(x) === 'MET_PREDECLARED_THRESHOLD').length,
    threshold_attainment_rate: measured.length ? measured.filter(x => experimentResult(x) === 'MET_PREDECLARED_THRESHOLD').length / measured.length : null,
    total_spent_usd: completed.length && allKnown ? completed.reduce((sum, x) => sum + x.observation.spent_usd, 0) : null,
    total_owner_hours: completed.length && allKnown ? completed.reduce((sum, x) => sum + x.observation.owner_hours, 0) : null,
    note: 'Threshold attainment measures only evaluated experiments meeting their own predefined threshold; it is not first-pass yield, business success or owner approval. Null means unmeasured, not zero.'
  };
}

function run() {
  const errors = [];
  const alerts = [];
  let history;
  try { history = JSON.parse(readFileSync(resolve(root, 'docs/data/decision-history.json'), 'utf8')); }
  catch (error) { console.error(`Cannot load decision history: ${error.message}`); process.exitCode = 2; return; }
  const files = readdirSync(recordsDirectory).filter(file => file.endsWith('.json') && !file.startsWith('_')).sort();
  const seen = new Set();
  const records = [];
  for (const file of files) {
    let record;
    try { record = JSON.parse(readFileSync(resolve(recordsDirectory, file), 'utf8')); }
    catch (error) { errors.push(`${file}: invalid JSON (${error.message})`); continue; }
    const check = validateExperiment(record, history, root);
    if (seen.has(record?.id)) errors.push(`${file}: duplicate experiment id ${record.id}`);
    seen.add(record?.id);
    if (`${record?.id}.json` !== file) errors.push(`${file}: filename must match experiment id`);
    errors.push(...check.errors.map(e => `${file}: ${e}`));
    alerts.push(...check.alerts.map(a => `${file}: ${a}`));
    records.push(record);
  }
  for (const e of errors) console.error(`ERROR: ${e}`);
  for (const a of alerts) console.error(`ALERT: ${a}`);
  if (errors.length) {
    console.log(JSON.stringify({ validation: 'INVALID', records_seen: records.length, metrics: null }, null, 2));
    process.exitCode = 1;
    return;
  }
  console.log(JSON.stringify({ validation: 'VALID', ...summarize(records) }, null, 2));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) run();
