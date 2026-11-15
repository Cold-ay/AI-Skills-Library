"""Build portable Skill Bridge installers from the already-reviewed, inert ZIPs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

import bundles
from skills import ROOT, blob_hash, catalogue, safe_path

DEST = ROOT / 'site/dist/bridge'


def reviewed_payloads():
    entries = {e['id']: e for e in catalogue()}
    combos = {b['id']: b for b in bundles.combinations()}
    singles = {}; groups = {}
    artifacts = json.loads((ROOT / 'site/dist/downloads/index.json').read_text())
    for artifact in artifacts:
        path = ROOT / 'site/dist/downloads' / artifact['file']
        if hashlib.sha256(path.read_bytes()).hexdigest() != artifact['sha256']:
            raise ValueError('Original archive integrity mismatch')
        combo = combos[artifact['id']]
        with zipfile.ZipFile(path) as z:
            manifest = json.loads(z.read('MANIFEST.json'))
            if manifest['combination'] != combo:
                raise ValueError('Archive workflow differs from catalogue')
            for name, digest in manifest['sha256'].items():
                safe_path(name)
                if hashlib.sha256(z.read(name)).hexdigest() != digest:
                    raise ValueError('Original archive member integrity mismatch')
            group = {}
            for ident in combo['skills']:
                entry = entries[ident]
                if entry not in manifest['skills'] or not entry['installable'] or (entry.get('license') or {}).get('spdx_id') != 'MIT':
                    raise ValueError('Unreviewed bridge member')
                single = {}
                for f in entry['files']:
                    content = z.read('.agents/skills/' + ident + '/' + f['path'])
                    if blob_hash(content) != f['blob']:
                        raise ValueError('Pinned source integrity mismatch')
                    single[ident + '/' + f['path']] = content
                license = combo['licenses'][ident]
                content = z.read('LICENSES/' + ident + '.txt')
                if blob_hash(content) != license['blob']:
                    raise ValueError('Pinned license integrity mismatch')
                single[ident + '/LICENSES/upstream/' + license['path']] = content
                if ident in singles and singles[ident] != single:
                    raise ValueError('Conflicting single-skill source packages')
                singles[ident] = single
                group.update(single)
            wrapper = bundles.workflow(combo, entries)
            # This is library-authored orchestration; keep it neutral across hosts.
            wrapper = re.sub(r' for \$[a-z0-9-]+\.', '.', wrapper)
            group['combination-' + combo['id'] + '/SKILL.md'] = wrapper.encode()
            groups[combo['id']] = group
    return entries, combos, singles, groups


def package(kind, record, payload, destination):
    ident = record['id']; root = 'ai-skill-library-' + kind + '-' + ident
    invocation = record['invocation'] if kind == 'skill' else 'combination-' + ident
    folders = sorted({path.split('/')[0] for path in payload})
    sources = [record] if kind == 'skill' else [e for e in catalogue() if e['id'] in record['skills']]
    manifest = dict(version=1, kind=kind, id=ident, invocation=invocation, folders=folders,
                    requirements=record['requirements'], sources=sources,
                    files={path: hashlib.sha256(content).hexdigest() for path, content in sorted(payload.items())})
    runtime = (ROOT / 'bridge_runtime.py').read_bytes()
    readme = ('# Skill Bridge: ' + (record.get('title') or ident) + '\n\n'
              '1. Review install.py, PACKAGE.json and every payload file. Compare the ZIP SHA-256 with the website. Hashes check integrity, not publisher authenticity.\n'
              '2. Extract this entire folder. In a terminal, change to this folder. Python 3.9+ is required; no pip installation or network is needed.\n'
              '3. Preview: python3 install.py --platform codex --scope project --project "/absolute/path/to/project"\n'
              '4. After reviewing: repeat that command with --reviewed. Choose claude or cursor for those local clients; --scope user installs to the current user instead. On Windows use py -3 instead of python3.\n'
              '5. Open a new chat in the target project, confirm the skill is available, and use $' + invocation + ' <your task> in Codex, or /' + invocation + ' <your task> in Claude Code / Cursor. If native discovery is unavailable, explicitly ask the agent to read the installed SKILL.md.\n\n'
              'Destinations: Codex .agents/skills; Claude Code .claude/skills; Cursor .cursor/skills. Project scope uses the selected project; user scope uses the home directory. Cloud accounts and remote workers are not synced.\n\n'
              'Existing folders are never replaced or merged. If there is a collision, use the existing installation or review a separate project. No settings, CLAUDE.md, AGENTS.md, hooks, scripts or dependencies are executed/modified by the installer. Upstream instructions are unmodified; the combination wrapper is library-authored and staged. Installing instruction files does not establish runtime compatibility.\n\n'
              '## Requirements\n\n' + record['requirements'] + '\n').encode()
    members = {root + '/install.py': runtime,
               root + '/PACKAGE.json': (json.dumps(manifest, indent=2) + '\n').encode(),
               root + '/README.md': readme}
    for path, content in payload.items():
        safe_path(path)
        members[root + '/payload/' + path] = content
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / (kind + '-' + ident + '.zip')
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, content in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content)
    return dict(kind=kind, id=ident, title=record.get('title') or ident,
                file=output.name, root=root, invocation=invocation,
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                bytes=output.stat().st_size, files=len(payload), folders=folders)


def build(destination=DEST, reviewed=False):
    if not reviewed:
        raise ValueError('Review source packages and installer, then pass --reviewed')
    entries, combos, singles, groups = reviewed_payloads()
    results = []
    for kind, records, payloads in [('skill', entries, singles), ('combination', combos, groups)]:
        for ident, payload in sorted(payloads.items()):
            results.append(package(kind, records[ident], payload, Path(destination)))
    (Path(destination) / 'index.json').write_text(json.dumps(results, indent=2) + '\n')
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed', action='store_true')
    args = parser.parse_args()
    try:
        print('Built', len(build(reviewed=args.reviewed)), 'offline bridge packages')
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, 'Error: ' + str(exc) + '\n')
