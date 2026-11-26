import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { evidenceReference, validHttpsSource, validLocalEvidenceFile } from './source-reference.mjs';

test('valid local sources are existing files, never directories or escaping paths', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-source-'));
  try {
    writeFileSync(join(sandbox, 'evidence.md'), '# synthetic fixture\n');
    symlinkSync(process.execPath, join(sandbox, 'external'));
    assert.equal(validLocalEvidenceFile('evidence.md', sandbox), true);
    for (const bad of ['.', '../README.md', 'external', 'https://example.com/source', 'evidence.md#anchor', 'evidence.md?secret=1']) {
      assert.equal(validLocalEvidenceFile(bad, sandbox), false, bad);
    }
  } finally {
    rmSync(sandbox, { recursive: true, force: true });
  }
});

test('malformed URLs or URL userinfo cannot satisfy source validation', () => {
  for (const bad of ['https://', 'https:///example.com/source', 'https://user:password@example.com/source', 'https://example.com\\evil.com/source', 'https://example .com/source', 'http://example.com/source']) {
    assert.equal(validHttpsSource(bad), false, bad);
  }
  assert.equal(validHttpsSource('https://example.com/reference#figure-2'), true);
});

test('generic experiment references obey the same rules used by decision history', () => {
  const sandbox = mkdtempSync(join(tmpdir(), 'businessideas-combined-'));
  try {
    writeFileSync(join(sandbox, 'evidence.txt'), 'synthetic aggregate');
    assert.equal(evidenceReference('evidence.txt', sandbox), true);
    assert.equal(evidenceReference('https://example.com/study', sandbox), true);
    assert.equal(evidenceReference('.', sandbox), false);
    assert.equal(evidenceReference('https:///example.com/study', sandbox), false);
  } finally {
    rmSync(sandbox, { recursive: true, force: true });
  }
});
