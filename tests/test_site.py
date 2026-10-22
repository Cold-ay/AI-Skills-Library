import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('site_builder',Path(__file__).resolve().parents[1]/'site/build.py')
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)

class SiteTests(unittest.TestCase):
    def test_raw_html_and_javascript_are_escaped(self):
        text=site.markdown('<script>alert(1)</script>\n\n[click](javascript:evil)')
        self.assertNotIn('<script>',text);self.assertNotIn('href="javascript:',text)
        self.assertIn('&lt;script&gt;',text)
    def test_links_and_tables(self):
        text=site.markdown('| Source | Status |\n|---|---|\n| [GitHub](https://github.com) | unknown |')
        self.assertIn('<table>',text);self.assertIn('rel="noopener noreferrer"',text)
        self.assertIn('<th scope="col">Source</th>',text)
    def test_code_is_not_interpreted(self):
        text=site.markdown('```html\n<img src=x onerror=alert(1)>\n```')
        self.assertIn('&lt;img',text);self.assertNotIn('<img',text)
    def test_reports_and_skills_are_built_from_repository(self):
        posts=site.build()
        self.assertEqual(len(posts),len(list((site.ROOT/'reports').glob('*.md'))))
        self.assertTrue(any(p['slug']=='2026-10-21-video-review' for p in posts))
        by={p['slug']:p for p in posts}
        self.assertEqual(by['2026-10-21']['category'],'Discovery')
        self.assertIn('preserved discovery snapshot',by['2026-10-21']['excerpt'])
        self.assertEqual(by['2026-10-21-weekly']['category'],'Discovery')
        self.assertIn('humanizer',by['2026-10-21-weekly']['excerpt'])
        self.assertNotEqual(by['2026-10-21']['excerpt'],by['2026-10-21-weekly']['excerpt'])
        self.assertTrue((site.HERE/'dist/data.js').read_text().startswith('window.AI_SKILL_LIBRARY = '))
    def test_no_recurring_report_workflow(self):
        self.assertFalse((site.ROOT/'docs/workflows/weekly.yml').exists())
        for path in (site.ROOT/'.github/workflows').glob('*.yml'):
            self.assertNotIn('schedule:',path.read_text())

if __name__=='__main__':unittest.main()
