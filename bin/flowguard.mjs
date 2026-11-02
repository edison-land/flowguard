#!/usr/bin/env node
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
const marker = '.flowguard-install.json';
const payload = ['SKILL.md', 'LICENSE', 'DEPENDENCIES.md', 'dependencies.lock.json',
  'agents', 'references', 'scripts/flowguard.py'];

function exists(p) {
  try { fs.lstatSync(p); return true; }
  catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}

// Refuse symlink traversal, including links in existing destination ancestors.
export function assertNoLinks(p) {
  let current = path.resolve(p);
  for (;;) {
    if (exists(current) && fs.lstatSync(current).isSymbolicLink()) {
      throw new Error(`Refusing symbolic link: ${current}`);
    }
    const parent = path.dirname(current);
    if (parent === current) return;
    current = parent;
  }
}

function fileMap(base, entries) {
  const result = {};
  function walk(rel) {
    const absolute = path.join(base, rel);
    const stat = fs.lstatSync(absolute);
    if (stat.isSymbolicLink()) throw new Error(`Refusing symbolic link: ${absolute}`);
    if (stat.isDirectory()) {
      for (const name of fs.readdirSync(absolute).sort()) walk(path.join(rel, name));
    } else if (stat.isFile()) {
      result[rel] = createHash('sha256').update(fs.readFileSync(absolute)).digest('hex');
    } else throw new Error(`Refusing special file: ${absolute}`);
  }
  for (const entry of entries) walk(entry);
  return result;
}

export function destinations({ agent = 'both', project, home = os.homedir() } = {}) {
  if (!['codex', 'claude', 'both'].includes(agent)) throw new Error('Use --agent codex, claude, or both.');
  const base = path.resolve(project || home);
  if (project && (!fs.existsSync(base) || !fs.statSync(base).isDirectory())) {
    throw new Error('--project must be an existing directory.');
  }
  const selected = agent === 'both' ? ['codex', 'claude'] : [agent];
  return selected.map(name => ({
    agent: name,
    path: path.join(base, name === 'codex' ? '.agents' : '.claude', 'skills', 'flowguard'),
  }));
}

export function install(options = {}) {
  const wanted = fileMap(root, payload);
  const targets = destinations(options);
  // Preflight every target before writing to any of them.
  const plan = targets.map(target => {
    assertNoLinks(target.path);
    if (!exists(target.path)) return { ...target, action: 'install' };
    const recordPath = path.join(target.path, marker);
    if (!fs.lstatSync(target.path).isDirectory() || !exists(recordPath)) {
      throw new Error(`Existing unmanaged destination; nothing overwritten: ${target.path}`);
    }
    const actual = fileMap(target.path, fs.readdirSync(target.path).filter(n => n !== marker));
    assertNoLinks(recordPath);
    const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
    if (record.package !== pkg.name || record.version !== pkg.version ||
        JSON.stringify(Object.entries(actual).sort()) !== JSON.stringify(Object.entries(wanted).sort())) {
      throw new Error(`Existing or changed installation; back it up separately before installing: ${target.path}`);
    }
    return { ...target, action: 'unchanged' };
  });
  if (!options.dryRun) {
    for (const target of plan) {
      if (target.action === 'unchanged') continue;
      // Claim the leaf exclusively; never merge into a directory another process created.
      fs.mkdirSync(path.dirname(target.path), { recursive: true });
      assertNoLinks(path.dirname(target.path));
      fs.mkdirSync(target.path);
      for (const rel of Object.keys(wanted)) {
        const output = path.join(target.path, rel);
        fs.mkdirSync(path.dirname(output), { recursive: true });
        fs.copyFileSync(path.join(root, rel), output, fs.constants.COPYFILE_EXCL);
      }
      fs.writeFileSync(path.join(target.path, marker), JSON.stringify({
        package: pkg.name, version: pkg.version, files: wanted,
      }, null, 2) + '\n', { flag: 'wx' });
    }
  }
  return { version: pkg.version, dryRun: Boolean(options.dryRun), destinations: plan };
}

export function main(args) {
  const command = args.shift();
  if (!command || ['help', '--help', '-h'].includes(command)) {
    console.log(`FlowGuard ${pkg.version}
  flowguard install [--agent codex|claude|both] [--project DIR] [--dry-run]
  flowguard doctor CACHE
  flowguard fetch CACHE                 Explicit network download of optional sources
  flowguard snapshot TARGET
  flowguard validate REVIEW TARGET

install defaults to user skills for both agents. --project writes only under DIR.
Existing installations are never overwritten. No install hooks, telemetry, or API keys.
The review itself is performed by your coding agent, not this CLI.
Python helpers require Python 3.9+ and Git; FLOWGUARD_PYTHON overrides python3.`);
    return 0;
  }
  if (command === '--version') { console.log(pkg.version); return 0; }
  if (command === 'install') {
    const options = {};
    while (args.length) {
      const option = args.shift();
      if (option === '--dry-run') options.dryRun = true;
      else if (['--agent', '--project'].includes(option)) {
        const value = args.shift();
        if (!value || value.startsWith('--')) throw new Error(`Missing value for ${option}`);
        options[option.slice(2)] = value;
      } else throw new Error(`Unknown option: ${option}`);
    }
    console.log(JSON.stringify(install(options), null, 2));
    return 0;
  }
  if (['doctor', 'fetch', 'snapshot', 'validate'].includes(command)) {
    const result = spawnSync(process.env.FLOWGUARD_PYTHON || 'python3',
      [path.join(root, 'scripts', 'flowguard.py'), command, ...args], { stdio: 'inherit', shell: false });
    if (result.error) throw new Error(`Cannot start Python: ${result.error.message}`);
    return result.status ?? 1;
  }
  throw new Error(`Unknown command: ${command}. Run flowguard --help.`);
}

if (process.argv[1] && fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { process.exitCode = main(process.argv.slice(2)); }
  catch (error) { console.error(`FlowGuard: ${error.message}`); process.exitCode = 1; }
}
