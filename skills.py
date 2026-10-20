#!/usr/bin/env python3
"""Auditable skill discovery and opt-in file installation. Python 3.9+, stdlib only."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
CATEGORIES = {'website-ui', 'video', 'coding', 'token-context', 'research-automation', 'skill-engineering'}
STATUSES = {'verified-static', 'upstream-claimed', 'unknown'}

def safe_path(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or '\\' in value or str(p) != value:
        raise ValueError('Unsafe relative path: ' + value)
    return p

def validate(entries):
    ids = set()
    for e in entries:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', e['id']) or e['id'] in ids:
            raise ValueError('Invalid or duplicate id')
        ids.add(e['id'])
        if e['category'] not in CATEGORIES or e['codex']['status'] not in STATUSES:
            raise ValueError('Invalid category or compatibility status')
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', e['repo']) or not re.fullmatch(r'[0-9a-f]{40}', e['commit']):
            raise ValueError('Invalid source or unpinned commit')
        safe_path(e['path'])
        if type(e['stars']) is not int or e['stars'] < 0 or not e['observed_at']:
            raise ValueError('Missing star evidence')
        if not e['codex']['evidence'] or e['codex']['runtime_tested'] is not False:
            raise ValueError('Unsupported runtime claim')
        if not e['reason'] or not e['requirements'] or not e['license_evidence']:
            raise ValueError('Missing curation evidence')
        names = set()
        for f in e['files']:
            safe_path(f['path'])
            if f['path'] in names or not re.fullmatch(r'[0-9a-f]{40}', f['blob']):
                raise ValueError('Invalid file manifest')
            names.add(f['path'])
        if 'SKILL.md' not in names:
            raise ValueError('Missing SKILL.md')
    return entries

def catalogue():
    return validate(json.loads((ROOT / 'catalog/skills.json').read_text()))

def fetch(url):
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError('Only pinned GitHub raw sources allowed')
    with urllib.request.urlopen(url, timeout=30) as r:
        data = r.read(5_000_001)
    if len(data) > 5_000_000:
        raise ValueError('File exceeds 5 MB limit')
    return data

def blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def install(e, destination, reviewed=False, downloader=fetch):
    if not reviewed:
        raise ValueError('Review source and requirements first; explicitly pass --reviewed')
    if not e['installable']:
        raise ValueError('This entry requires the upstream plugin/dependency installation; see show')
    destination = Path(destination).expanduser().resolve()
    target = destination / e['id']
    if target.exists() or target.is_symlink():
        raise ValueError('Refusing to overwrite existing skill')
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.skill-stage-', dir=destination) as tmp:
        staging = Path(tmp) / e['id']
        staging.mkdir()
        total = 0
        for f in e['files']:
            safe_path(f['path'])
            data = downloader(f"https://raw.githubusercontent.com/{e['repo']}/{e['commit']}/{e['path']}/{f['path']}")
            total += len(data)
            if total > 25_000_000 or blob_hash(data) != f['blob']:
                raise ValueError('Size limit or integrity mismatch; nothing installed')
            out = staging / f['path']
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        # mkdir is exclusive: concurrent installs cannot overwrite an existing directory.
        target.mkdir()
        try:
            for child in staging.iterdir():
                shutil.move(str(child), target / child.name)
        except BaseException:
            shutil.rmtree(target)
            raise
    return target

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    ls = sub.add_parser('list'); ls.add_argument('--category', choices=sorted(CATEGORIES)); ls.add_argument('--query', default='')
    sub.add_parser('validate')
    for command in ('show', 'call', 'install'):
        s = sub.add_parser(command); s.add_argument('id')
        if command == 'call': s.add_argument('task', nargs='?', default='Help me with this task.')
        if command == 'install':
            s.add_argument('--dest', default='.agents/skills'); s.add_argument('--reviewed', action='store_true')
    args = p.parse_args()
    try:
        entries = catalogue()
        if args.command == 'validate':
            print(f'Validated {len(entries)} curated skills'); return
        if args.command == 'list':
            for e in entries:
                if (not args.category or e['category'] == args.category) and args.query.lower() in json.dumps(e, ensure_ascii=False).lower():
                    print(f"{e['id']:28} {e['category']:20} {e['codex']['status']:18} ★{e['stars']}  {e['summary']}")
            return
        e = next((e for e in entries if e['id'] == args.id), None)
        if e is None: raise ValueError('Unknown skill id; use list')
        if args.command == 'show': print(json.dumps(e, indent=2, ensure_ascii=False))
        elif args.command == 'call':
            print(f"${e['invocation']} {args.task}")
            print('Paste into Codex after installation and a new session. This command does not run the agent.', file=sys.stderr)
        else: print('Installed files (no scripts executed):', install(e, args.dest, args.reviewed))
    except (ValueError, KeyError, OSError) as exc:
        p.exit(1, f'Error: {exc}\n')

if __name__ == '__main__': main()
