import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import bridge
import codex_export as exporter


def installer_script():
    return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills/.system/skill-installer/scripts/install-skill-from-github.py'


class CodexExportTests(unittest.TestCase):
    def test_native_tree_matches_reviewed_bridge_payloads(self):
        index = json.loads((exporter.EXPORT / 'index.json').read_text())
        entries, combos, singles, groups = bridge.reviewed_payloads()
        self.assertEqual(len(index['entries']), 14)
        for record in index['entries']:
            payload = singles[record['id']] if record['kind'] == 'skill' else groups[record['id']]
            for path, content in payload.items():
                self.assertEqual((exporter.EXPORT / 'skills' / path).read_bytes(), content)
            for path in record['paths']:
                self.assertTrue((exporter.ROOT / path / 'SKILL.md').is_file())
            self.assertEqual([Path(p).name for p in record['paths']], record['folders'])
        for path, digest in index['files'].items():
            self.assertEqual(hashlib.sha256((exporter.EXPORT / path).read_bytes()).hexdigest(), digest)

    def test_combinations_list_every_member_and_wrapper_last(self):
        index = json.loads((exporter.EXPORT / 'index.json').read_text())
        combos = {b['id']: b for b in bridge.bundles.combinations()}
        for record in index['entries']:
            if record['kind'] != 'combination': continue
            self.assertEqual(record['folders'], combos[record['id']]['skills'] + ['combination-' + record['id']])
            wrapper = (exporter.ROOT / record['paths'][-1] / 'SKILL.md').read_text()
            for member in combos[record['id']]['skills']:
                self.assertIn('../' + member + '/SKILL.md', wrapper)

    def test_rebuild_is_deterministic_and_preserves_edited_files(self):
        with self.assertRaises(ValueError): exporter.export()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'export'
            index = exporter.export(True, target)
            self.assertEqual(exporter.export(True, target), index)
            source = target / 'skills/gsap-core/SKILL.md'; source.write_text('local edit')
            with self.assertRaises(ValueError): exporter.export(True, target)
            self.assertEqual(source.read_text(), 'local edit')

    def test_branch_refs_cannot_be_published(self):
        for ref in ('main', 'HEAD', 'a' * 7, '../x'):
            with self.assertRaises(ValueError): exporter.committed_export(ref)

    @unittest.skipUnless(installer_script().is_file(), 'Bundled Codex installer not installed in this environment')
    def test_real_codex_installer_copies_all_published_folders(self):
        # Exercise the real bundled installer validation/copy path, with only its
        # network checkout replaced by the local repository. No upstream execution.
        script = installer_script(); sys.path.insert(0, str(script.parent))
        try:
            spec = importlib.util.spec_from_file_location('codex_installer_under_test', script)
            installer = importlib.util.module_from_spec(spec); sys.modules[spec.name] = installer; spec.loader.exec_module(installer)
            index = json.loads((exporter.EXPORT / 'index.json').read_text())
            paths = sorted({p for e in index['entries'] for p in e['paths']})
            with tempfile.TemporaryDirectory() as tmp, patch.object(installer, '_prepare_repo', return_value=str(exporter.ROOT)):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = installer.main(['--repo', exporter.REPO, '--path', *paths, '--dest', tmp])
                self.assertEqual(result, 0)
                self.assertEqual(len(list(Path(tmp).iterdir())), 14)
                for path in paths:
                    source = exporter.ROOT / path; installed = Path(tmp) / source.name
                    for file in source.rglob('*'):
                        if file.is_file(): self.assertEqual((installed / file.relative_to(source)).read_bytes(), file.read_bytes())
        finally:
            sys.path.remove(str(script.parent))

    def test_published_registry_matches_source_index(self):
        if not exporter.REGISTRY.exists(): self.skipTest('Export must be committed before publishing its registry')
        registry = exporter.validate_registry()
        self.assertEqual(len(registry['entries']), 14)
        self.assertRegex(registry['ref'], r'^[0-9a-f]{40}$')


if __name__ == '__main__': unittest.main()
