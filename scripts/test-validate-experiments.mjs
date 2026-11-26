import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { validateExperiment, experimentResult, scanExperimentArtifacts, summarize } from './validate-experiments.mjs';

const history = {
  ideas: [{ id: 'milk-bar' }],
  events: [{ id: 'milk-bar-demo-1', idea: 'milk-bar', kind: 'experiment' }]
};

function planned() {
  return {
    schema_version: 1,
    id: 'milk-bar-demo-1',
    idea: 'milk-bar',
    history_event_id: 'milk-bar-demo-1',
    state: 'PLANNED',
    plan: { registered_on: '2026-11-26', hypothesis: 'A buys B', customer_segment: 'defined buyers', method: 'anonymous test', success_definition: 'unique paid orders', minimum_sample: 5, target_success_rate: 0.4, budget_cap_usd: 10, owner_hours_cap: 2 },
    authorization: { status: 'NOT_APPROVED', approved_by: null, approved_on: null },
    observation: { started_on: null, finished_on: null, sample: null, successes: null, spent_usd: null, owner_hours: null, evidence: [] },
    owner_decision: { status: 'PENDING', decided_by: null, decided_on: null, why: null },
    cancellation_reason: null
  };
}

function completed() {
  const r = planned();
  r.state = 'COMPLETED';
  r.authorization = { status: 'APPROVED', approved_by: 'Charles', approved_on: '2026-11-26' };
  r.observation = { started_on: '2026-11-26', finished_on: '2026-11-27', sample: 10, successes: 5, spent_usd: 9, owner_hours: 1.5, evidence: ['playbook/new-idea-template.md'] };
  return r;
}

test('planned travel has no invented outcomes and no measured yield', () => {
  const r = planned();
  assert.deepEqual(validateExperiment(r, history).errors, []);
  assert.equal(experimentResult(r), 'NOT_MEASURED');
  assert.equal(summarize([r]).threshold_attainment_rate, null);
  assert.equal(summarize([r]).total_spent_usd, null);
});

test('completed sourced results are evaluable but never auto-approved', () => {
  const r = completed();
  assert.deepEqual(validateExperiment(r, history).errors, []);
  assert.equal(experimentResult(r), 'MET_PREDECLARED_THRESHOLD');
  assert.equal(r.owner_decision.status, 'PENDING');
  assert.equal(summarize([r]).threshold_attainment_rate, 1);
});

test('undersized sample is inconclusive, not a success', () => {
  const r = completed();
  r.observation.sample = 3; r.observation.successes = 3;
  assert.equal(experimentResult(r), 'INCONCLUSIVE');
  assert.equal(summarize([r]).threshold_attainment_rate, null);
});

test('unapproved execution cannot be recorded as completed', () => {
  const r = completed();
  r.authorization = planned().authorization;
  assert.match(validateExperiment(r, history).errors.join('; '), /authorization/);
});

test('postdated plans, approvals and decisions are rejected', () => {
  const r = completed();
  r.plan.registered_on = '2026-11-28';
  r.authorization.approved_on = '2026-11-27';
  r.owner_decision = { status: 'CONTINUE', decided_by: 'Charles', decided_on: '2026-11-26', why: 'Hypothetical example' };
  const errors = validateExperiment(r, history).errors.join('; ');
  for (const part of ['registered', 'approval date', 'owner decision cannot predate']) assert.match(errors, new RegExp(part));
});

test('planned cannot contain fabricated field evidence', () => {
  const r = planned();
  r.observation.sample = 5;
  assert.match(validateExperiment(r, history).errors.join('; '), /PLANNED/);
});

test('unknown source, impossible counts and dates fail closed', () => {
  const r = completed();
  r.history_event_id = 'made-up';
  r.observation.successes = 99;
  r.observation.finished_on = '2026-02-30';
  r.observation.evidence = ['../../secret.csv'];
  const errors = validateExperiment(r, history).errors.join('; ');
  for (const part of ['history_event_id', 'successes', 'finished_on', 'evidence']) assert.match(errors, new RegExp(part));
});

test('completed evidence must link to a file, not an existing directory', () => {
  const r = completed();
  r.observation.evidence = ['playbook'];
  assert.match(validateExperiment(r, history).errors.join('; '), /observation\.evidence/);
});

test('completed evidence rejects malformed or credential-bearing HTTPS references', () => {
  const r = completed();
  for (const badRef of ['https://', 'https:///example.com/evidence', 'https://user:token@example.com/source', 'https://example .com/source', 'https://example.com\\evil.com/file']) {
    r.observation.evidence = [badRef];
    assert.match(validateExperiment(r, history).errors.join('; '), /observation\.evidence/, badRef);
  }
  r.observation.evidence = ['https://example.com/aggregate-research'];
  assert.deepEqual(validateExperiment(r, history).errors, []);
});

test('local evidence cannot escape checkout by following a symlink', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-evidence-'));
  try {
    symlinkSync(process.execPath, join(sandbox, 'outside'));
    const r = completed();
    r.observation.evidence = ['outside'];
    assert.match(validateExperiment(r, history, sandbox).errors.join('; '), /observation\.evidence/);
  } finally {
    rmSync(sandbox, { recursive: true, force: true });
  }
});

test('actual budget/time overruns are alerted but factual records remain valid', () => {
  const r = completed();
  r.observation.spent_usd = 11;
  r.observation.owner_hours = 2.5;
  const check = validateExperiment(r, history);
  assert.deepEqual(check.errors, []);
  assert.equal(check.alerts.length, 2);
});

test('missing dollars are unknown, not fabricated zero', () => {
  const r = completed();
  r.observation.spent_usd = null;
  assert.deepEqual(validateExperiment(r, history).errors, []);
  assert.equal(summarize([r]).total_spent_usd, null);
  assert.equal(summarize([r]).total_owner_hours, 1.5);
  assert.equal(summarize([r]).known_owner_hours, 1.5);
  assert.equal(summarize([r]).unknown_spend_records, 1);
});

test('unknown owner hours do not suppress measured dollar totals', () => {
  const r = completed();
  r.observation.owner_hours = null;
  const s = summarize([r]);
  assert.equal(s.total_spent_usd, 9);
  assert.equal(s.known_spent_usd, 9);
  assert.equal(s.total_owner_hours, null);
  assert.equal(s.unknown_owner_hours_records, 1);
});

test('running and completed and cancelled expenditure is counted', () => {
  const done = completed();
  const running = completed();
  running.id = 'milk-bar-demo-2';
  running.state = 'RUNNING';
  running.observation.finished_on = null;
  running.observation.spent_usd = 4;
  running.observation.owner_hours = 1;
  const cancelled = completed();
  cancelled.id = 'milk-bar-demo-3';
  cancelled.state = 'CANCELLED';
  cancelled.cancellation_reason = 'Not a viable sample';
  cancelled.observation.spent_usd = 20;
  cancelled.observation.owner_hours = 3;
  assert.deepEqual(validateExperiment(cancelled, history).errors, []);
  const s = summarize([done, running, cancelled]);
  assert.equal(s.executed_records, 3);
  assert.equal(s.total_spent_usd, 33);
  assert.equal(s.total_owner_hours, 5.5);
  assert.equal(s.evaluable, 1);
});

test('cancelled work that started cannot evade authorization or chronology', () => {
  const r = completed();
  r.state = 'CANCELLED';
  r.cancellation_reason = 'Unexpected problem';
  r.authorization = planned().authorization;
  r.observation.finished_on = '2026-11-25';
  const errors = validateExperiment(r, history).errors.join('; ');
  assert.match(errors, /authorization/);
  assert.match(errors, /finish date/);
});

test('an unstarted planned experiment may be cancelled without approval or spend', () => {
  const r = planned();
  r.state = 'CANCELLED';
  r.cancellation_reason = 'Found cheaper alternative before launch';
  r.observation.finished_on = '2026-11-26';
  assert.deepEqual(validateExperiment(r, history).errors, []);
  r.observation.spent_usd = 5;
  assert.match(validateExperiment(r, history).errors.join('; '), /CANCELLED without an observed start/);
});

test('partial unknown running and cancelled costs do not vanish from known sums', () => {
  const r = completed();
  r.state = 'RUNNING';
  r.observation.finished_on = null;
  r.observation.owner_hours = null;
  const c = completed();
  c.state = 'CANCELLED';
  c.cancellation_reason = 'Stopped after a day';
  c.observation.spent_usd = null;
  c.observation.owner_hours = 2;
  const s = summarize([r, c]);
  assert.equal(s.known_spent_usd, 9);
  assert.equal(s.unknown_spend_records, 1);
  assert.equal(s.total_spent_usd, null);
  assert.equal(s.known_owner_hours, 2);
  assert.equal(s.unknown_owner_hours_records, 1);
  assert.equal(s.total_owner_hours, null);
});

test('unearned owner decisions and cancellations are rejected', () => {
  const r = planned();
  r.owner_decision.status = 'CONTINUE';
  assert.match(validateExperiment(r, history).errors.join('; '), /owner decision/);
  r.owner_decision = planned().owner_decision;
  r.state = 'CANCELLED';
  assert.match(validateExperiment(r, history).errors.join('; '), /CANCELLED/);
});

test('no records preserves unknown threshold attainment and cost', () => {
  const s = summarize([]);
  assert.equal(s.records, 0);
  assert.equal(s.threshold_attainment_rate, null);
  assert.equal(s.total_spent_usd, null);
});

test('experiment scanner accepts only named top-level JSON travelers and harmless stock files', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-artifacts-'));
  try {
    for (const name of ['README.md', '_template.json', '.DS_Store', '.gitkeep', 'milk-bar-demo-1.json']) {
      writeFileSync(join(sandbox, name), '{}');
    }
    assert.deepEqual(scanExperimentArtifacts(sandbox), { files: ['milk-bar-demo-1.json'], errors: [] });
  } finally { rmSync(sandbox, { recursive: true, force: true }); }
});

test('experiment scanner fails closed on unvalidated nested, uppercase and export files', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-artifacts-'));
  try {
    writeFileSync(join(sandbox, 'milk-bar.JSON'), '{}');
    writeFileSync(join(sandbox, 'buyer-export.csv'), 'synthetic,not-real');
    mkdirSync(join(sandbox, 'nested'));
    writeFileSync(join(sandbox, 'nested', 'milk-bar.json'), '{}');
    const scan = scanExperimentArtifacts(sandbox);
    assert.deepEqual(scan.files, []);
    for (const name of ['milk-bar.JSON', 'buyer-export.csv', 'nested']) {
      assert.ok(scan.errors.some(error => error.includes(name)), name);
    }
  } finally { rmSync(sandbox, { recursive: true, force: true }); }
});

test('experiment scanner rejects symlinked traveler without reading its target', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-artifacts-'));
  try {
    symlinkSync(process.execPath, join(sandbox, 'fake-traveler.json'));
    const scan = scanExperimentArtifacts(sandbox);
    assert.deepEqual(scan.files, []);
    assert.ok(scan.errors.some(error => error.includes('fake-traveler.json')));
  } finally { rmSync(sandbox, { recursive: true, force: true }); }
});
