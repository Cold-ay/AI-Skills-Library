import copy
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import skills
import report

class LibraryTests(unittest.TestCase):
    def entry(self):
        e=copy.deepcopy(skills.catalogue()[0]);e['files']=[{'path':'SKILL.md','blob':skills.blob_hash(b'example')}];return e
    def test_categories(self):self.assertEqual({e['category'] for e in skills.catalogue()},skills.CATEGORIES)
    def test_duplicate(self):
        e=self.entry()
        with self.assertRaises(ValueError):skills.validate([e,e])
    def test_mutable_ref(self):
        e=self.entry();e['commit']='main'
        with self.assertRaises(ValueError):skills.validate([e])
    def test_traversal(self):
        for p in ('../escape','/tmp/x','a/../../x','a\\b','a//b','./x'):
            with self.subTest(p=p),self.assertRaises(ValueError):skills.safe_path(p)
    def test_review_required(self):
        with self.assertRaises(ValueError):skills.install(self.entry(),'/unused')
    def test_reference_only(self):
        e=self.entry();e['installable']=False
        with self.assertRaises(ValueError):skills.install(e,'/unused',True)
    def test_hash_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):skills.install(self.entry(),d,True,lambda _:b'changed')
            self.assertEqual(list(Path(d).iterdir()),[])
    def test_install_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            target=skills.install(self.entry(),d,True,lambda _:b'example')
            self.assertEqual((target/'SKILL.md').read_bytes(),b'example')
            with self.assertRaises(ValueError):skills.install(self.entry(),d,True,lambda _:b'other')
    def test_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            e=self.entry();(Path(d)/e['id']).symlink_to(Path(d)/'missing')
            with self.assertRaises(ValueError):skills.install(e,d,True,lambda _:b'example')
    def test_offline_rollback(self):
        def fail(_):raise OSError('offline')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(OSError):skills.install(self.entry(),d,True,fail)
            self.assertEqual(list(Path(d).iterdir()),[])
class ReportTests(unittest.TestCase):
    def fake(self,p):
        if p.startswith('search/'):return {'items':[{'full_name':'demo/skills'}]}
        if '/commits/' in p:return {'sha':'a'*40}
        if '/git/trees/' in p:return {'tree':[{'type':'blob','path':'skills/demo/SKILL.md'}]}
        return dict(default_branch='main',stargazers_count=123,created_at='2026-10-01',pushed_at='2026-10-20',archived=False,license={'spdx_id':'MIT'})
    @patch('report.catalogue',return_value=[])
    def test_discovery(self,_):
        s=report.collect(self.fake,datetime(2026,10,21,tzinfo=timezone.utc))
        self.assertEqual(len(s['repositories']),1);self.assertEqual(s['repositories'][0]['codex'],'unknown')
        self.assertIn('baseline unavailable',report.render(s))
        self.assertIn('+23',report.render(s,{'repositories':[{'repo':'demo/skills','stars':100}]}))
    @patch('report.catalogue',return_value=[])
    def test_error(self,_):
        def fail(_):raise ValueError('broken')
        s=report.collect(fail);self.assertEqual(len(s['errors']),3);self.assertIn('Search failed',report.render(s))
    def test_markdown_escape(self):self.assertEqual(report.cell('<x>|\ny'),'&lt;x&gt;\\| y')
if __name__=='__main__':unittest.main()
