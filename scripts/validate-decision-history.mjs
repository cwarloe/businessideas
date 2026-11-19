#!/usr/bin/env node
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dataFile = resolve(repositoryRoot, 'docs/data/decision-history.json');
const errors = [];

function report(message) { errors.push(message); }
function isText(value) { return typeof value === 'string' && value.trim().length > 0; }
function validDate(value) {
  return typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)
    && !Number.isNaN(Date.parse(`${value}T00:00:00Z`))
    && new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) === value;
}

let data;
try { data = JSON.parse(readFileSync(dataFile, 'utf8')); }
catch (error) { console.error(`Unable to read decision history: ${error.message}`); process.exit(1); }

if (data.version !== 1) report('version must be 1');
if (!Array.isArray(data.ideas) || !data.ideas.length) report('ideas must be a nonempty array');
if (!Array.isArray(data.events)) report('events must be an array');

const ideas = new Set();
for (const [index, idea] of (Array.isArray(data.ideas) ? data.ideas : []).entries()) {
  if (!isText(idea?.id) || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(idea.id)) report(`ideas[${index}]: invalid id`);
  if (!isText(idea?.label)) report(`ideas[${index}]: missing label`);
  if (ideas.has(idea?.id)) report(`ideas[${index}]: duplicate id ${idea.id}`);
  ideas.add(idea?.id);
}

const kinds = new Set(['decision', 'hypothesis', 'experiment', 'finding', 'lesson']);
const statuses = new Set(['adopted', 'preferred', 'provisional', 'proposed', 'deferred', 'rejected', 'open', 'untested', 'planned', 'completed', 'unverified', 'researched', 'documented']);
const records = new Map();

for (const [index, event] of (Array.isArray(data.events) ? data.events : []).entries()) {
  const key = `events[${index}]`;
  if (!event || typeof event !== 'object' || Array.isArray(event)) { report(`${key}: must be an object`); continue; }
  if (!isText(event.id) || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(event.id)) report(`${key}: invalid id`);
  if (records.has(event.id)) report(`${key}: duplicate id ${event.id}`);
  records.set(event.id, event);
  if (!validDate(event.date)) report(`${key}: invalid date ${event.date}`);
  if (!ideas.has(event.idea)) report(`${key}: unknown idea ${event.idea}`);
  if (!kinds.has(event.kind)) report(`${key}: unsupported kind ${event.kind}`);
  if (!statuses.has(event.status)) report(`${key}: unsupported status ${event.status}`);
  for (const field of ['title', 'summary', 'why']) if (!isText(event[field])) report(`${key}: ${field} must contain text`);
  if (event.revisitWhen !== null && event.revisitWhen !== undefined && !isText(event.revisitWhen)) report(`${key}: revisitWhen must contain text or null`);
  if (!Array.isArray(event.sources) || event.sources.length === 0) {
    report(`${key}: at least one source is required`);
  } else {
    for (const [sourceIndex, source] of event.sources.entries()) {
      const location = `${key}.sources[${sourceIndex}]`;
      if (!isText(source?.label)) report(`${location}: missing label`);
      if (Boolean(source?.path) === Boolean(source?.url)) { report(`${location}: specify exactly one path or url`); continue; }
      if (source.path) {
        if (typeof source.path !== 'string' || isAbsolute(source.path) || source.path.includes('\\')) { report(`${location}: invalid local path`); continue; }
        const full = resolve(repositoryRoot, source.path);
        if (relative(repositoryRoot, full).startsWith('..') || !existsSync(full)) report(`${location}: missing or outside-repository file ${source.path}`);
      } else if (!/^https:\/\/[^\s]+$/.test(source.url)) {
        report(`${location}: external source must be an HTTPS URL`);
      }
    }
  }
}

for (const event of records.values()) {
  if (event.supersedes !== undefined) {
    if (!records.has(event.supersedes) || event.supersedes === event.id) report(`${event.id}: supersedes must name a different existing event`);
    else if (event.date < records.get(event.supersedes).date) report(`${event.id}: cannot supersede a later event`);
  }
}

if (errors.length) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  console.error(`History validation failed with ${errors.length} issue(s).`);
  process.exit(1);
}

console.log(`Validated ${records.size} history entries across ${ideas.size} ideas; all local sources exist.`);
