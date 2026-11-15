"""Presentation identity, evidence, output distinctions and setup boundaries."""
import json
import unittest

import bundles
import skills


class PresentationResearchTests(unittest.TestCase):
    def setUp(self):
        self.entries = {e['id']: e for e in skills.catalogue()}
        self.root = skills.ROOT / 'reports/evidence/2026-11-15-presentation-skills'
        self.review = json.loads((skills.ROOT / 'reports/2026-11-15-presentation-skills.json').read_text())

    def test_pins_stars_and_reading_manifests_match_primary_evidence(self):
        verified = json.loads((self.root / 'verified-reading-files.json').read_text())
        self.assertEqual(len(self.review['added']), 6)
        for addition in self.review['added']:
            entry = self.entries[addition['id']]
            evidence = json.loads((skills.ROOT / entry['stars_evidence']).read_text())
            tree = {f['path']: f for f in evidence['tree']['tree']}
            self.assertFalse(evidence['tree']['truncated'])
            self.assertEqual(entry['commit'], evidence['commit'])
            self.assertEqual(entry['stars'], evidence['metadata']['stargazers_count'])
            self.assertEqual(entry['repo'], evidence['metadata']['full_name'])
            for f in entry['files']:
                path = f['path'] if entry['path'] == '.' else entry['path'] + '/' + f['path']
                self.assertIn(tree[path]['mode'], ('100644', '100755'))
                self.assertEqual(f['blob'], tree[path]['sha'])
                self.assertTrue(any(v['repo'] == entry['repo'] and v['path'] == path and v['blob'] == f['blob'] for v in verified))

    def test_formats_and_aliases_do_not_imply_editable_pptx(self):
        formats = {e['id']: e['presentation']['format'] for e in self.entries.values() if e['category'] == 'presentations'}
        self.assertEqual({k for k, v in formats.items() if v == 'html'}, {'frontend-slides', 'magazine-web-ppt', 'html-ppt-studio'})
        self.assertEqual({k for k, v in formats.items() if v == 'native-pptx'}, {'ppt-master'})
        self.assertEqual({k for k, v in formats.items() if v == 'image-pptx'}, {'baoyu-slide-deck', 'visual-style-ppt'})
        self.assertEqual(self.entries['magazine-web-ppt']['invocation'], 'guizang-ppt-skill')
        self.assertEqual(self.entries['html-ppt-studio']['invocation'], 'html-ppt')
        self.assertEqual(self.entries['ppt-master']['repo'], 'hugohe3/ppt-master')

    def test_reference_only_license_and_runtime_boundaries(self):
        for addition in self.review['added']:
            entry = self.entries[addition['id']]
            self.assertFalse(entry['installable'])
            self.assertTrue(entry['presentation']['reading_set_only'])
            self.assertEqual(entry['codex']['status'], 'upstream-claimed')
            self.assertFalse(entry['codex']['runtime_tested'])
            with self.assertRaises(ValueError):
                skills.install(entry, '/unused', reviewed=True)
        self.assertEqual(self.entries['magazine-web-ppt']['license']['spdx_id'], 'AGPL-3.0')
        self.assertIsNone(self.entries['visual-style-ppt']['license'])
        self.assertIn('Image 2.5', self.entries['visual-style-ppt']['requirements'])
        self.assertEqual(self.entries['visual-style-ppt']['claude']['status'], 'unknown')

    def test_recipes_keep_one_deck_author_and_remain_unbundled(self):
        packs = {b['id']: b for b in bundles.combinations()}
        author_ids = {a['id'] for a in self.review['added']}
        for ident in self.review['combinations']:
            pack = packs[ident]
            self.assertFalse(pack['downloadable'])
            self.assertEqual(len(author_ids.intersection(pack['skills'])), 1)
        for pack in packs.values():
            if pack['downloadable']:
                self.assertFalse(author_ids.intersection(pack['skills']))
        payload = (skills.ROOT / 'site/dist/data.js').read_text()
        self.assertIn('2026-11-15-presentation-skills', payload)
        self.assertIn("'presentations':'Presentations & PPT'", (skills.ROOT / 'site/dist/app.js').read_text())


if __name__ == '__main__':
    unittest.main()
