"""Topic curation provenance, license preservation and published workflow checks."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import skills
import bundles


class WebsiteTopicTests(unittest.TestCase):
    def test_selected_sources_match_preserved_evidence(self):
        root = skills.ROOT / 'reports/evidence/2026-11-05-ai-skills-topic'
        snapshot = json.loads((skills.ROOT / 'reports/2026-11-05-ai-skills-topic.json').read_text())
        entries = {e['id']: e for e in skills.catalogue()}
        topic = json.loads((root / 'topic-stars.json').read_text())
        self.assertEqual(len(topic['response']['items']), 50)
        for record in snapshot['added']:
            entry = entries[record['id']]
            evidence = json.loads((skills.ROOT / entry['stars_evidence']).read_text())
            tree = {f['path']: f for f in evidence['tree']['tree']}
            self.assertEqual(evidence['commit'], entry['commit'])
            self.assertEqual(evidence['metadata']['stargazers_count'], entry['stars'])
            self.assertEqual(evidence['observed_at'][:10], entry['observed_at'])
            self.assertFalse(evidence['tree']['truncated'])
            self.assertFalse(entry['codex']['runtime_tested'])
            self.assertEqual(record['codex'], entry['codex']['status'])
            for f in entry['files']:
                upstream = tree[entry['path'] + '/' + f['path']]
                self.assertEqual(upstream['mode'], '100644')
                self.assertEqual(upstream['sha'], f['blob'])
                self.assertTrue(f['path'].endswith('.md'))
            for f in entry['license_files']:
                self.assertEqual(tree[f['path']]['sha'], f['blob'])
        self.assertEqual(entries['playwright-best-practices']['codex']['status'], 'unknown')

    def fixture(self):
        entry = copy.deepcopy(skills.catalogue()[0])
        entry['files'] = [{'path': 'SKILL.md', 'blob': skills.blob_hash(b'instructions')}]
        entry['license_files'] = [{'path': 'LICENSE.md', 'blob': skills.blob_hash(b'notice')}]
        return entry

    def test_install_preserves_pinned_root_notice(self):
        entry = self.fixture()
        urls = []
        def download(url):
            urls.append(url)
            return b'notice' if url.endswith('/LICENSE.md') else b'instructions'
        with tempfile.TemporaryDirectory() as dest:
            target = skills.install(entry, dest, True, download)
            self.assertEqual((target / 'LICENSES/upstream/LICENSE.md').read_bytes(), b'notice')
        self.assertEqual(urls[-1], skills.raw_file_url(entry['repo'], entry['commit'], '.', 'LICENSE.md'))

    def test_bad_notice_hash_rolls_back_install(self):
        with tempfile.TemporaryDirectory() as dest:
            with self.assertRaises(ValueError):
                skills.install(self.fixture(), dest, True, lambda url: b'changed' if url.endswith('/LICENSE.md') else b'instructions')
            self.assertEqual(list(Path(dest).iterdir()), [])

    def test_license_manifest_rejects_unsafe_and_colliding_paths(self):
        for path in ('../LICENSE', '/LICENSE', 'a\\LICENSE'):
            entry = self.fixture()
            entry['license_files'][0]['path'] = path
            with self.assertRaises(ValueError):
                skills.validate([entry])
        entry = self.fixture()
        entry['files'].append({'path': 'LICENSES/upstream/LICENSE.md', 'blob': 'a' * 40})
        with self.assertRaises(ValueError):
            skills.validate([entry])

    def test_workflow_roles_and_publishing(self):
        packs = {b['id']: b for b in bundles.combinations()}
        self.assertEqual(packs['clear-website-interactions']['skills'], ['design-everyday-things', 'microinteractions'])
        self.assertTrue(packs['clear-website-interactions']['downloadable'])
        self.assertFalse(packs['website-interaction-qa']['downloadable'])
        payload = (skills.ROOT / 'site/dist/data.js').read_text()
        self.assertIn('2026-11-05-ai-skills-topic', payload)
        self.assertIn('clear-website-interactions.zip', payload)


if __name__ == '__main__':
    unittest.main()
