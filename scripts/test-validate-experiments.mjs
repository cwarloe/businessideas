import test from 'node:test';
import assert from 'node:assert/strict';
import { validateExperiment, experimentResult, summarize } from './validate-experiments.mjs';

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
