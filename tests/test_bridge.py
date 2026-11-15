import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import bridge
import bridge_runtime as runtime
import skills


class BridgeTests(unittest.TestCase):
    def fixture(self, root):
        package = root / 'package'; package.mkdir()
        data = {'demo/SKILL.md': b'---\nname: demo\ndescription: Example\n---\nInstructions',
                'demo/scripts/passive.py': b'raise RuntimeError("must never run")',
                'demo/LICENSES/upstream/LICENSE': b'copyright notice'}
        for name, content in data.items():
            p = package / 'payload' / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(content)
        manifest = dict(version=1, folders=['demo'], invocation='demo',
                        files={p: hashlib.sha256(b).hexdigest() for p, b in data.items()})
        (package / 'PACKAGE.json').write_text(json.dumps(manifest))
        return package

    def test_preview_has_no_side_effects_and_project_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root); project = root / 'project'; project.mkdir()
            result = runtime.install_package(package, 'codex', project=project)
            self.assertFalse(result['installed']); self.assertFalse((project / '.agents').exists())
            with self.assertRaises(ValueError): runtime.install_package(package, 'codex')
            with self.assertRaises(ValueError): runtime.install_package(package, 'unknown', project=project)

    def test_all_platforms_and_scopes_copy_only_with_notices(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root)
            for platform, location in runtime.PLATFORMS.items():
                for scope in ('project', 'user'):
                    target = root / (platform + '-' + scope); target.mkdir()
                    result = runtime.install_package(package, platform, scope, project=target, home=target, reviewed=True)
                    self.assertTrue(result['installed'])
                    self.assertEqual((target / location / 'demo/LICENSES/upstream/LICENSE').read_bytes(), b'copyright notice')
                    self.assertTrue((target / location / 'demo/scripts/passive.py').exists())

    def test_hash_failure_and_collision_install_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root); project = root / 'project'; project.mkdir()
            (package / 'payload/demo/SKILL.md').write_bytes(b'changed')
            with self.assertRaises(ValueError): runtime.install_package(package, 'codex', project=project, reviewed=True)
            self.assertFalse((project / '.agents').exists())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root); target = root / '.agents/skills/demo'; target.mkdir(parents=True)
            (target / 'keep.txt').write_text('keep')
            with self.assertRaises(ValueError): runtime.install_package(package, 'codex', project=root, reviewed=True)
            self.assertEqual([p.name for p in target.iterdir()], ['keep.txt'])

    def test_payload_and_target_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root); project = root / 'project'; project.mkdir()
            outside = root / 'outside'; outside.mkdir(); (project / '.agents').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError): runtime.install_package(package, 'codex', project=project, reviewed=True)
            self.assertEqual(list(outside.iterdir()), [])
            (project / '.agents').unlink()
            source = package / 'payload/demo/SKILL.md'; content = source.read_bytes(); source.unlink()
            (outside / 'text').write_bytes(content); source.symlink_to(outside / 'text')
            with self.assertRaises(ValueError): runtime.install_package(package, 'codex', project=project, reviewed=True)

    def test_unsafe_cross_platform_paths_rejected(self):
        for path in ('../x', '/x', 'a//b', 'a\\b', 'a/CON.txt', 'a/evil:stream', '.', 'a/trailing.', 'a/trailing '):
            with self.subTest(path=path), self.assertRaises(ValueError): runtime.relative(path)

    def test_failure_rolls_back_reserved_skill_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); package = self.fixture(root); project = root / 'project'; project.mkdir()
            with patch('bridge_runtime.shutil.move', side_effect=OSError('disk failure')):
                with self.assertRaises(OSError): runtime.install_package(package, 'codex', project=project, reviewed=True)
            self.assertEqual(list((project / '.agents/skills').iterdir()), [])

    def test_published_packages_retain_pinned_sources_and_current_installer(self):
        entries = {e['id']: e for e in skills.catalogue()}
        index = json.loads((bridge.DEST / 'index.json').read_text())
        self.assertEqual(len(index), 14)
        self.assertEqual(len([p for p in index if p['kind'] == 'skill']), 9)
        for record in index:
            path = bridge.DEST / record['file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record['sha256'])
            with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(path) as z:
                self.assertTrue(all(n.startswith(record['root'] + '/') for n in z.namelist()))
                self.assertTrue(all(not (f.external_attr >> 16) & 0o111 for f in z.infolist()))
                self.assertEqual(z.read(record['root'] + '/install.py'), (skills.ROOT / 'bridge_runtime.py').read_bytes())
                z.extractall(tmp); manifest, payload = runtime.inspect_package(Path(tmp) / record['root'])
                for entry in manifest['sources']:
                    self.assertEqual(entry, entries[entry['id']])
                    for f in entry['files']:
                        self.assertEqual(skills.blob_hash(payload[entry['id'] + '/' + f['path']]), f['blob'])
                    self.assertTrue(any(p.startswith(entry['id'] + '/LICENSES/upstream/') for p in payload))
                self.assertNotIn('frontend-slides', manifest['folders'])

    def test_self_contained_cli_works_outside_repository(self):
        path = bridge.DEST / 'combination-clear-website-interactions.zip'
        with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(path) as z:
            root = Path(tmp); z.extractall(root); package = root / 'ai-skill-library-combination-clear-website-interactions'
            project = root / 'my project'; project.mkdir()
            result = subprocess.run([sys.executable, str(package / 'install.py'), '--platform', 'claude', '--scope', 'project', '--project', str(project), '--reviewed'], cwd=root, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('/combination-clear-website-interactions', result.stdout)
            self.assertTrue((project / '.claude/skills/combination-clear-website-interactions/SKILL.md').exists())
            self.assertFalse((project / 'CLAUDE.md').exists())

    def test_bridge_build_is_reviewed_and_reproducible(self):
        with self.assertRaises(ValueError): bridge.build()
        with tempfile.TemporaryDirectory() as tmp:
            generated = bridge.build(Path(tmp), reviewed=True)
            current = json.loads((bridge.DEST / 'index.json').read_text())
            self.assertEqual(generated, current)


if __name__ == '__main__': unittest.main()
