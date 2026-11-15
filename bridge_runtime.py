#!/usr/bin/env python3
"""Offline, copy-only installer shipped inside reviewed Skill Bridge packages."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

PLATFORMS = {'codex': '.agents/skills', 'claude': '.claude/skills', 'cursor': '.cursor/skills'}


def relative(value):
    p = PurePosixPath(value)
    if not value or str(p) != value or p.is_absolute() or '..' in p.parts or '\\' in value:
        raise ValueError('Unsafe package path')
    for part in p.parts:
        if (part in ('.', '..') or part.endswith((' ', '.')) or
                re.search(r'[\x00-\x1f<>:"|?*]', part) or
                part.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1, 10)), *('LPT'+str(i) for i in range(1, 10))}):
            raise ValueError('Unsupported package path')
    if not p.parts:
        raise ValueError('Empty package path')
    return p


def read_regular(root, path):
    relative(path)
    source = root
    for part in PurePosixPath(path).parts:
        source = source / part
        if source.is_symlink():
            raise ValueError('Package symlinks are not supported')
    if not source.is_file() or source.stat().st_size > 5_000_000:
        raise ValueError('Missing or oversized package file')
    return source.read_bytes()


def inspect_package(package):
    package = Path(package).resolve()
    manifest = json.loads(read_regular(package, 'PACKAGE.json'))
    if manifest.get('version') != 1:
        raise ValueError('Unsupported package version')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['invocation']):
        raise ValueError('Invalid invocation name')
    folders = manifest['folders']
    if not folders or len(folders) != len(set(f.casefold() for f in folders)):
        raise ValueError('Duplicate or missing skill folders')
    for folder in folders:
        relative(folder)
        if '/' in folder or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', folder):
            raise ValueError('Invalid skill folder')
    files = manifest['files']
    if not files or len(files) > 1000:
        raise ValueError('Invalid package inventory')
    payload = {}; total = 0; seen = set()
    for path, digest in files.items():
        p = relative(path)
        if len(p.parts) < 2 or p.parts[0] not in folders or path.casefold() in seen:
            raise ValueError('Invalid or duplicate payload destination')
        seen.add(path.casefold())
        if not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Invalid payload digest')
        content = read_regular(package, 'payload/' + path)
        total += len(content)
        if total > 25_000_000 or hashlib.sha256(content).hexdigest() != digest:
            raise ValueError('Payload integrity check failed')
        payload[path] = content
    for folder in folders:
        if folder + '/SKILL.md' not in payload:
            raise ValueError('Missing skill entry')
    # Prevent a file from also being used as a parent directory.
    keys = set(path.casefold() for path in payload)
    for path in payload:
        if any(str(p).casefold() in keys for p in PurePosixPath(path).parents if str(p) != '.'):
            raise ValueError('Conflicting payload paths')
    return manifest, payload


def install_package(package, platform, scope='project', project=None, reviewed=False, home=None):
    if platform not in PLATFORMS or scope not in ('project', 'user'):
        raise ValueError('Choose a supported platform and scope')
    if scope == 'project' and project is None:
        raise ValueError('Project scope requires --project /path/to/project')
    anchor = Path(home if home is not None else Path.home()) if scope == 'user' else Path(project)
    anchor = anchor.expanduser().resolve()
    if not anchor.is_dir():
        raise ValueError('The target home/project directory must already exist')
    manifest, payload = inspect_package(package)
    root = anchor
    for part in PLATFORMS[platform].split('/'):
        root = root / part
        if root.is_symlink() or (root.exists() and not root.is_dir()):
            raise ValueError('Target skills path must be a real directory')
    targets = [root / f for f in manifest['folders']]
    conflicts = [str(p) for p in targets if p.exists() or p.is_symlink()]
    if conflicts:
        raise ValueError('Nothing installed. Existing folders: ' + ', '.join(conflicts))
    result = {'installed': False, 'platform': platform, 'scope': scope,
              'destination': str(root), 'folders': manifest['folders'],
              'files': len(payload), 'invocation': manifest['invocation']}
    if not reviewed:
        return result
    root.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        with tempfile.TemporaryDirectory(prefix='.skill-bridge-', dir=root) as tmp:
            stage = Path(tmp)
            for path, content in payload.items():
                output = stage / path
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(content)
            # Reserve every final folder exclusively before copying any payload.
            for target in targets:
                target.mkdir()
                created.append(target)
            for target in targets:
                for child in (stage / target.name).iterdir():
                    shutil.move(str(child), target / child.name)
    except BaseException:
        for target in reversed(created):
            shutil.rmtree(target)
        raise
    result['installed'] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', choices=tuple(PLATFORMS), required=True)
    parser.add_argument('--scope', choices=('project', 'user'), default='project')
    parser.add_argument('--project')
    parser.add_argument('--reviewed', action='store_true', help='Copy files after source review; otherwise preview only')
    args = parser.parse_args()
    try:
        result = install_package(Path(__file__).resolve().parent, **vars(args))
        print(json.dumps(result, indent=2))
        prefix = '$' if args.platform == 'codex' else '/'
        print(('Installed. Open a new agent chat, confirm the skill appears, then paste: ' if result['installed'] else 'Preview only. Review files, then rerun with --reviewed. Chat prompt after installation: ') + prefix + result['invocation'] + ' <your task>')
        print('No upstream scripts or dependencies were executed. Local installation does not sync cloud accounts.')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, 'Error: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
