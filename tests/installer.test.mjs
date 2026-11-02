import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { destinations, install } from '../bin/flowguard.mjs';

const cli = fileURLToPath(new URL('../bin/flowguard.mjs', import.meta.url));
function fixture(t) {
  const dir = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'flowguard-test-')));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

test('user locations match each host', () => {
  const found = destinations({ home: '/example/home' });
  assert.equal(found[0].path, path.resolve('/example/home/.agents/skills/flowguard'));
  assert.equal(found[1].path, path.resolve('/example/home/.claude/skills/flowguard'));
});
test('dry-run does not create destination directories', t => {
  const project = fixture(t);
  assert.equal(install({ project, dryRun: true }).destinations.length, 2);
  assert.deepEqual(fs.readdirSync(project), []);
});
test('installs complete skill payload for both hosts and repeats without changes', t => {
  const project = fixture(t);
  const result = install({ project });
  for (const target of result.destinations) {
    assert.match(fs.readFileSync(path.join(target.path, 'SKILL.md'), 'utf8'), /name: flowguard/);
    for (const rel of ['scripts/flowguard.py', 'references/evidence.md', 'dependencies.lock.json', 'agents/openai.yaml']) {
      assert.ok(fs.statSync(path.join(target.path, rel)).isFile());
    }
  }
  assert.ok(install({ project }).destinations.every(d => d.action === 'unchanged'));
});
test('preflight refuses existing content without partially installing the other host', t => {
  const project = fixture(t);
  const dest = destinations({ project })[1].path;
  fs.mkdirSync(dest, { recursive: true });
  fs.writeFileSync(path.join(dest, 'mine'), 'keep');
  assert.throws(() => install({ project }), /unmanaged/);
  assert.equal(fs.existsSync(path.join(project, '.agents')), false);
  assert.equal(fs.readFileSync(path.join(dest, 'mine'), 'utf8'), 'keep');
});
test('refuses modified installations and extra user files', t => {
  const project = fixture(t);
  const dest = install({ project, agent: 'codex' }).destinations[0].path;
  fs.writeFileSync(path.join(dest, 'user-notes.md'), 'mine');
  assert.throws(() => install({ project, agent: 'codex' }), /changed installation/);
  assert.equal(fs.readFileSync(path.join(dest, 'user-notes.md'), 'utf8'), 'mine');
});
test('refuses symlink destination ancestors', t => {
  const project = fixture(t);
  const elsewhere = fixture(t);
  fs.symlinkSync(elsewhere, path.join(project, '.agents'), 'dir');
  assert.throws(() => install({ project, agent: 'codex' }), /symbolic link/);
  assert.deepEqual(fs.readdirSync(elsewhere), []);
});
test('CLI runs through npm-style bin symlink', t => {
  const project = fixture(t);
  const linked = path.join(project, 'flowguard');
  fs.symlinkSync(cli, linked);
  const result = spawnSync(process.execPath, [linked, '--version'], { encoding: 'utf8' });
  assert.equal(result.status, 0);
  assert.equal(result.stdout.trim(), '0.1.0');
});
test('CLI rejects invalid options without creating output', t => {
  const project = fixture(t);
  const result = spawnSync(process.execPath, [cli, 'install', '--project', project, '--agent', 'unknown'], { encoding: 'utf8' });
  assert.equal(result.status, 1);
  assert.deepEqual(fs.readdirSync(project), []);
});
