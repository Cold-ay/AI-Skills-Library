"""Cross-check curated claims against preserved public API evidence."""
import json
import unittest
from pathlib import Path
import skills
import bundles

class ResearchRoundTests(unittest.TestCase):
    def test_observations_and_pins_match_preserved_evidence(self):
        snapshot=json.loads((skills.ROOT/'reports/2026-10-31-coding-context-mobile.json').read_text())
        entries={e['id']:e for e in skills.catalogue()}
        repos={r['repo']:r for r in snapshot['repositories']}
        self.assertEqual(snapshot['published_on'],'2026-10-31')
        for added in snapshot['added']:
            e=entries[added['id']];repo=repos[e['repo']]
            raw=json.loads((skills.ROOT/e['stars_evidence']).read_text())
            record=next(r for r in raw['response']['items'] if r['id']==repo['repository_id'])
            self.assertEqual(record['full_name'].lower(),e['repo'].lower())
            self.assertEqual(record['stargazers_count'],e['stars'])
            self.assertEqual(added['stars'],e['stars'])
            self.assertEqual(e['commit'],repo['commit'])
            self.assertIn('/'+e['commit']+'/',e['source'])
            self.assertEqual(raw['observed_at'],repo['observed_at'])
            self.assertFalse(e['codex']['runtime_tested']);self.assertFalse(e['claude']['runtime_tested'])
    def test_reference_only_context_and_plugin_dependencies_are_not_copy_installs(self):
        entries={e['id']:e for e in skills.catalogue()}
        for ident in ('self-managed-context','expo-overview','expo-design-system','expo-native-ui','test-driven-development'):
            self.assertFalse(entries[ident]['installable'])
        self.assertIn('runtime',entries['self-managed-context']['requirements'])
        snapshot=json.loads((skills.ROOT/'reports/2026-10-31-coding-context-mobile.json').read_text())
        reviewed=next(e for e in snapshot['revisited'] if e['id']=='filesystem-context')
        self.assertIn('already loaded tokens',reviewed['requirements'])
        self.assertEqual(entries['filesystem-context']['commit'],reviewed['preserved_catalogue_commit'])
        self.assertEqual(entries['react-native-skills']['codex']['status'],'unknown')
    def test_recipes_reference_available_skills_without_claiming_packages(self):
        recipes={b['id']:b for b in bundles.combinations()}
        for ident in ('evidence-led-coding','durable-context','expo-native-design'):
            self.assertFalse(recipes[ident]['downloadable'])
        self.assertTrue(any(e['category']=='mobile-app' for e in skills.catalogue()))
        html=(skills.ROOT/'site/dist/index.html').read_text()
        self.assertIn('2026-10-31-coding-context-mobile',html)

if __name__=='__main__':unittest.main()
