"""Standard-library dependency and evidence utility. Does not execute audited code."""
import argparse, hashlib, json, pathlib, subprocess, sys, os, stat
BASE = pathlib.Path(__file__).resolve().parents[1]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(p, *args):
    return subprocess.check_output(['git', '-C', str(p), *args], text=True, stderr=subprocess.DEVNULL, timeout=15).strip()

def snapshot(root):
    root = pathlib.Path(root).resolve()
    if not root.is_dir():
        raise ValueError('snapshot target must be an existing directory')
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            link = pathlib.Path(directory, name)
            if link.is_symlink():
                result[str(link.relative_to(root))] = 'symlink:' + os.readlink(link)
        dirs[:] = [d for d in dirs if d != '.git' and (not pathlib.Path(directory, d).is_symlink())]
        for name in files:
            p = pathlib.Path(directory, name)
            if p.is_symlink():
                result[str(p.relative_to(root))] = 'symlink:' + os.readlink(p)
            elif stat.S_ISREG(p.stat().st_mode):
                result[str(p.relative_to(root))] = digest(p)
            else:
                raise ValueError('snapshot refuses special files: ' + str(p.relative_to(root)))
    return result

def doctor(cache):
    result = {}
    for k, v in json.loads((BASE / 'dependencies.lock.json').read_text()).items():
        p = pathlib.Path(cache) / k
        try:
            ok = git(p, 'rev-parse', 'HEAD') == v['commit'] and (not git(p, 'status', '--porcelain')) and all(((p / f).is_file() and digest(p / f) == h for f, h in v['sha256'].items()))
            result[k] = {'available': bool(ok), 'runtime': 'not-probed', 'entry': str(p / v['entry']), 'reason': 'pinned content verified' if ok else 'commit/content/dirty mismatch'}
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            result[k] = {'available': False, 'reason': 'missing, unreadable or Git probe timed out'}
    return result

def require(condition):
    if not condition:
        raise ValueError('evidence or decision constraint failed')

def validate(r, root):
    root = pathlib.Path(root).resolve()
    require(r['version'] == 1)
    require(all((k in r for k in ['target', 'adapters', 'frontier', 'coverage', 'gaps', 'findings', 'decision'])))
    require(r['target']['scope'] and r['target']['commit'] == git(root, 'rev-parse', 'HEAD'))
    require(all((isinstance(r[k], list) for k in ['adapters', 'frontier', 'coverage', 'gaps', 'findings'])))
    contracts = {
        'adapters': ['name', 'mode', 'reason', 'loaded_paths', 'input_evidence_ids', 'output_artifact', 'limitations'],
        'frontier': ['trigger', 'question', 'action', 'observation', 'next'],
        'coverage': ['inspected', 'not_inspected'],
        'gaps': ['scope', 'missing_evidence', 'impact', 'owner', 'due', 'next_safe_verification']
    }
    for kind, fields in contracts.items():
        for record in r[kind]:
            require(isinstance(record, dict) and all(key in record for key in fields))
            if kind == 'adapters':
                require(record['mode'] in ['native', 'instruction-guided', 'fallback', 'missing', 'unused'])
                require(isinstance(record['loaded_paths'], list))
            elif kind == 'gaps':
                require(all(isinstance(record[k], str) and record[k].strip() for k in fields))
    require(r['frontier'] and r['coverage'])
    ids = set()
    for f in r['findings']:
        require(all((k in f for k in ['id', 'claim', 'status', 'severity', 'confidence', 'trigger', 'effect', 'evidence', 'counterevidence', 'boundary', 'remedy'])))
        require(f['id'] not in ids)
        ids.add(f['id'])
        require(f['status'] in ['source-observed', 'hypothesis', 'reproduced', 'refuted'])
        require(f['severity'] in ['critical', 'high', 'medium', 'low'] and f['confidence'] in ['high', 'medium', 'low'])
        require(f['boundary'] in ['source', 'component', 'integration', 'end-to-end', 'production'])
        require(f['evidence'] and isinstance(f['counterevidence'], list))
        for e in f['evidence']:
            rel = pathlib.Path(e['path'])
            p = root / rel
            require(not rel.is_absolute() and '..' not in rel.parts)
            require(p.resolve().is_relative_to(root) and (not any(((root / pathlib.Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)))))
            require(digest(p) == e['sha256'])
            require(type(e['line_start']) is int and type(e['line_end']) is int)
            require(1 <= e['line_start'] <= e['line_end'] <= len(p.read_text().splitlines()))
    d = r['decision']
    require(d['rationale'] and d['owner'])
    require(d['outcome'] in ['Go', 'No-go', 'Defer', 'Escalation', 'Exception', 'Insufficient-evidence'])
    if d['outcome'] == 'Go':
        require(d['owner'] not in ['unassigned', 'unknown'] and (not r['gaps']))
        require(r['coverage'] and r['adapters'])
        require(not any((f['status'] != 'refuted' and f['severity'] in ['high', 'critical'] for f in r['findings'])))
    if d['outcome'] == 'Exception':
        require(d.get('human_waiver') and d.get('expires') and d.get('authority'))
    return True

def main():
    a = argparse.ArgumentParser()
    a.add_argument('command', choices=['doctor', 'fetch', 'snapshot', 'validate'])
    a.add_argument('path')
    a.add_argument('target', nargs='?')
    ns = a.parse_args()
    if ns.command == 'validate' and not ns.target:
        a.error('validate requires REVIEW and TARGET')
    if ns.command == 'doctor':
        print(json.dumps(doctor(ns.path), indent=2))
    elif ns.command == 'snapshot':
        print(json.dumps(snapshot(ns.path), sort_keys=True, indent=2))
    elif ns.command == 'validate':
        validate(json.loads(pathlib.Path(ns.path).read_text()), ns.target)
        print('VALID')
    else:
        cache = pathlib.Path(ns.path).resolve()
        cache.mkdir(parents=True, exist_ok=True)
        for k, v in json.loads((BASE / 'dependencies.lock.json').read_text()).items():
            p = cache / k
            if p.exists():
                continue
            subprocess.run(['git', '-c', 'core.hooksPath=' + os.devnull, 'clone', '--no-checkout', v['url'], str(p)], check=True)
            subprocess.run(['git', '-C', str(p), '-c', 'core.hooksPath=' + os.devnull, 'checkout', '--detach', v['commit']], check=True)
        print(json.dumps(doctor(cache), indent=2))
if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError, TypeError, subprocess.CalledProcessError) as e:
        print('INVALID: ' + str(e), file=sys.stderr)
        sys.exit(1)
