import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import bundles
import report
import skills

class BundleTests(unittest.TestCase):
    def fixture(self):
        entry=copy.deepcopy(skills.catalogue()[0]);entry.update(id='demo',invocation='demo',installable=True,license={'spdx_id':'MIT'},files=[dict(path='SKILL.md',blob=skills.blob_hash(b'skill'))])
        pack=dict(id='demo-pack',title='Demo',summary='Demo workflow',skills=['demo'],stages=[dict(skill='demo',title='Review',task='Inspect provided files.')],requirements='None',conflicts='One owner',downloadable=True,licenses={'demo':dict(path='LICENSE',blob=skills.blob_hash(b'license'))})
        return entry,pack
    def test_review_and_recipe_gates(self):
        _,b=self.fixture()
        with self.assertRaises(ValueError):bundles.build_bundle(b,'/unused')
        b['downloadable']=False
        with self.assertRaises(ValueError):bundles.build_bundle(b,'/unused',True)
    def test_bad_hash_never_publishes(self):
        e,b=self.fixture()
        with tempfile.TemporaryDirectory() as d,patch('bundles.catalogue',return_value=[e]):
            p=Path(d)/'pack.zip'
            with self.assertRaises(ValueError):bundles.build_bundle(b,p,True,lambda _:b'wrong')
            self.assertFalse(p.exists())
    def test_license_hash_required(self):
        e,b=self.fixture()
        with tempfile.TemporaryDirectory() as d,patch('bundles.catalogue',return_value=[e]):
            with self.assertRaises(ValueError):bundles.build_bundle(b,Path(d)/'pack.zip',True,lambda u:b'skill' if u.endswith('SKILL.md') else b'wrong')
            self.assertEqual(list(Path(d).iterdir()),[])
    def test_reproducible_inert_archive_and_no_overwrite(self):
        e,b=self.fixture()
        def get(u):return b'skill' if u.endswith('SKILL.md') else b'license'
        with tempfile.TemporaryDirectory() as d,patch('bundles.catalogue',return_value=[e]):
            p=Path(d)/'one.zip';q=Path(d)/'two.zip'
            bundles.build_bundle(b,p,True,get);bundles.build_bundle(b,q,True,get)
            self.assertEqual(p.read_bytes(),q.read_bytes())
            with self.assertRaises(FileExistsError):bundles.build_bundle(b,p,True,get)
            with zipfile.ZipFile(p) as z:
                self.assertEqual(z.read('.agents/skills/demo/SKILL.md'),b'skill')
                self.assertIn('../demo/SKILL.md',z.read('.agents/skills/combination-demo-pack/SKILL.md').decode())
                self.assertTrue(all(not (i.external_attr>>16)&0o111 for i in z.infolist()))
    def test_claude_prompt_uses_file_adapter_not_codex_invocation(self):
        _,b=self.fixture()
        self.assertEqual(bundles.call_prompt(b),'$combination-demo-pack <your task>')
        text=bundles.call_prompt(b,'claude')
        self.assertIn('Read CLAUDE.md',text);self.assertIn('.agents/skills/combination-demo-pack/SKILL.md',text)
        self.assertNotIn('$combination',text)
    def test_claude_adapter_keeps_staged_loading_and_limits(self):
        _,b=self.fixture();text=bundles.claude_instructions(b)
        self.assertIn('.agents/skills/combination-demo-pack/SKILL.md',text)
        self.assertIn('When the user explicitly requests',text)
        self.assertIn('not a claim of upstream Claude support',text)
        self.assertNotIn('@.agents',text)
    def test_published_archives_match_catalogue_and_all_file_hashes(self):
        entries={e['id']:e for e in skills.catalogue()};packs={b['id']:b for b in bundles.combinations()}
        artifacts=json.loads((skills.ROOT/'site/dist/downloads/index.json').read_text())
        self.assertEqual({a['id'] for a in artifacts},{b['id'] for b in packs.values() if b['downloadable']})
        for a in artifacts:
            p=skills.ROOT/'site/dist/downloads'/a['file'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),a['sha256'])
            with zipfile.ZipFile(p) as z:
                m=json.loads(z.read('MANIFEST.json'));b=packs[a['id']];self.assertEqual(m['combination'],b)
                self.assertEqual(z.read('CLAUDE.md').decode(),bundles.claude_instructions(b))
                self.assertEqual(set(z.namelist()),set(m['sha256'])|{'MANIFEST.json'})
                for name,digest in m['sha256'].items():
                    skills.safe_path(name);self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),digest)
                for ident in b['skills']:
                    self.assertIn(entries[ident],m['skills'])
                    for f in entries[ident]['files']:self.assertEqual(skills.blob_hash(z.read('.agents/skills/'+ident+'/'+f['path'])),f['blob'])
                    self.assertEqual(skills.blob_hash(z.read('LICENSES/'+ident+'.txt')),b['licenses'][ident]['blob'])
    @patch('report.catalogue',return_value=[])
    def test_configurable_queries_and_limits(self,_):
        paths=[]
        def get(path):paths.append(path);return {'items':[]}
        s=report.collect(get,config={'window_days':30,'per_query':3,'queries':['browser stars:>=20 pushed:>={since}']})
        self.assertEqual(s['per_query'],3);self.assertIn('per_page=3',paths[0]);self.assertNotIn('{since}',paths[0])
        with self.assertRaises(ValueError):report.collect(get,config={'window_days':30,'per_query':999,'queries':['x']})

if __name__=='__main__':unittest.main()
