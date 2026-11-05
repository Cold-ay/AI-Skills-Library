import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock
import library_mcp as api
import skills
from mcp_server import create_server, client_config


class McpLibraryTests(unittest.TestCase):
    def fixture(self, text=b'one\ntwo\nthree'):
        e=copy.deepcopy(skills.catalogue()[0]);e.update(id='demo',files=[dict(path='SKILL.md',blob=skills.blob_hash(text))])
        downloader=Mock(return_value=text)
        return api.Library(entries=[e],recipes=[],downloader=downloader),downloader

    def test_metadata_and_search_do_not_fetch_source(self):
        lib,get=self.fixture();self.assertEqual(lib.search_skills(query='demo')['total'],1)
        self.assertEqual(lib.get_skill('demo')['file_count'],1);get.assert_not_called()
        self.assertNotIn('files',lib.get_skill('demo'))

    def test_verified_source_pagination(self):
        lib,get=self.fixture();first=lib.read_skill_file('demo',max_lines=2)
        self.assertEqual(first['text'],'one\ntwo');self.assertEqual(first['next_line'],3);self.assertTrue(first['verified'])
        self.assertEqual(lib.read_skill_file('demo',start_line=3)['text'],'three')
        self.assertIn('/'+lib.skill('demo')['commit']+'/',get.call_args.args[0])

    def test_manifest_rejects_paths_before_any_fetch(self):
        lib,get=self.fixture()
        for path in ('../README.md','/etc/passwd','a\\b','.env','README.md'):
            with self.subTest(path=path),self.assertRaises(ValueError):lib.read_skill_file('demo',path)
        get.assert_not_called()

    def test_mismatched_source_never_returned(self):
        lib,get=self.fixture();get.return_value=b'changed'
        with self.assertRaisesRegex(ValueError,'integrity'):lib.read_skill_file('demo')

    def test_binary_and_excessive_source_rejected(self):
        for raw in (b'\x00text',b'\xff',b'a'*(api.SOURCE_LIMIT+1)):
            lib,_=self.fixture(raw)
            with self.assertRaises(ValueError):lib.read_skill_file('demo')

    def test_invalid_bounds_and_unknown_ids(self):
        lib,get=self.fixture()
        for args in ({'max_lines':401},{'start_line':0}):
            with self.assertRaises(ValueError):lib.read_skill_file('demo',**args)
        get.assert_not_called()
        with self.assertRaises(ValueError):lib.get_skill('missing')
        with self.assertRaises(ValueError):lib.search_skills(limit=31)
        with self.assertRaises(ValueError):lib.search_skills(category='missing')
        with self.assertRaises(ValueError):lib.search_skills(sort='missing')

    def test_search_sort_and_page_are_nonmutating(self):
        lib,_=self.fixture();a=copy.deepcopy(lib.entries[0]);a.update(id='second',stars=0,observed_at='2099-01-01');lib.entries.append(a)
        original=copy.deepcopy(lib.entries)
        self.assertEqual(lib.search_skills(sort='recent')['items'][0]['id'],'second')
        self.assertEqual(lib.search_skills(limit=1)['next_offset'],1)
        self.assertEqual(lib.search_skills(offset=1)['items'][0]['id'],'second')
        self.assertEqual(lib.entries,original)

    def test_report_read_is_confined_to_slugs_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'2026-11-05.md').write_text('# Title\n\nReport')
            (root/'alias.md').symlink_to(root/'2026-11-05.md')
            lib=api.Library(entries=[],recipes=[],reports=root)
            self.assertEqual(len(lib.list_reports()),1)
            self.assertIn('Report',lib.read_report('2026-11-05')['text'])
            for slug in ('../README','/etc/passwd','alias'):
                with self.assertRaises(ValueError):lib.read_report(slug)

    def test_combination_returns_member_purpose_and_stage_order(self):
        lib=api.Library();combo=lib.get_combination('react-motion')
        self.assertEqual([s['skill'] for s in combo['stages']],['gsap-core','gsap-timeline','gsap-react'])
        self.assertTrue(all(s['member']['summary'] for s in combo['stages']))
        self.assertIn('read_skill_file',combo['next_step'])
        self.assertGreater(lib.search_combinations(category='mobile-app')['total'],0)

    def test_source_fetch_rejects_redirects_and_unapproved_hosts(self):
        with self.assertRaises(ValueError):api.download_source('https://example.com/a')
        with self.assertRaises(ValueError):api.NoRedirect().redirect_request(None,None,None,None,None,None)

    def test_configs_are_absolute_and_do_not_modify_clients(self):
        data=json.loads(client_config('claude'))['mcpServers']['ai_skill_library']
        self.assertTrue(Path(data['command']).is_absolute());self.assertTrue(Path(data['args'][0]).is_absolute())
        self.assertIn('[mcp_servers.ai_skill_library]',client_config('codex'))


@unittest.skipUnless(importlib.util.find_spec('mcp'),'Install requirements-mcp.txt for MCP protocol tests')
class McpProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_in_memory_protocol_tools_resources_prompts_and_error(self):
        from mcp import Client
        lib,_=McpLibraryTests().fixture()
        async with Client(create_server(lib)) as client:
            tools=(await client.list_tools()).tools
            self.assertEqual(len(tools),8)
            self.assertTrue(all(t.annotations.read_only_hint for t in tools))
            self.assertFalse(any('install' in t.name or 'execute' in t.name for t in tools))
            result=await client.call_tool('read_skill_file',{'skill_id':'demo','max_lines':2})
            self.assertEqual(result.structured_content['text'],'one\ntwo')
            failure=await client.call_tool('read_skill_file',{'skill_id':'demo','path':'../secret'})
            self.assertTrue(failure.is_error)
            overview=await client.read_resource('skill-library://overview')
            self.assertEqual(json.loads(overview.contents[0].text)['skill_count'],1)
            prompt=await client.get_prompt('use_skill',{'skill_id':'demo','task':'Review this example.'})
            self.assertIn('Review this example.',prompt.messages[0].content.text)

    async def test_stdio_process_from_another_working_directory(self):
        from mcp import Client,StdioServerParameters
        with tempfile.TemporaryDirectory() as d:
            params=StdioServerParameters(command=sys.executable,args=[str(skills.ROOT/'mcp_server.py')],cwd=d)
            async with Client(params) as client:
                r=await client.call_tool('search_skills',{'query':'SwiftUI'})
                self.assertFalse(r.is_error);self.assertGreater(r.structured_content['total'],0)
                prompts=(await client.list_prompts()).prompts
                self.assertEqual({p.name for p in prompts},{'use_skill','use_combination'})
                skill=await client.read_resource('skill-library://skills/swiftui-expert')
                self.assertEqual(json.loads(skill.contents[0].text)['id'],'swiftui-expert')

if __name__=='__main__':unittest.main()
