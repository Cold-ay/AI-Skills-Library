"""Exercise the real stdio protocol without an LLM or third-party skill execution."""
import argparse
import json
from pathlib import Path
import sys
import anyio
from mcp import Client, StdioServerParameters

ROOT=Path(__file__).resolve().parents[1]

async def check(fetch_source):
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'mcp_server.py')])
    with anyio.fail_after(45):
        async with Client(params) as client:
            tools=(await client.list_tools()).tools
            assert all(tool.annotations.read_only_hint for tool in tools)
            query=await client.call_tool('search_skills',{'category':'mobile-app','limit':3})
            assert not query.is_error and query.structured_content['items']
            combo=await client.call_tool('get_combination',{'combination_id':'react-motion'})
            assert not combo.is_error and len(combo.structured_content['stages'])==3
            overview=await client.read_resource('skill-library://overview')
            prompts=(await client.list_prompts()).prompts
            report={'transport':'stdio','tools':[t.name for t in tools],
                    'prompts':[p.name for p in prompts], 'overview':json.loads(overview.contents[0].text),
                    'source_fetch':'not requested','third_party_execution':False}
            if fetch_source:
                result=await client.call_tool('read_skill_file',{'skill_id':'gsap-core','max_lines':20})
                assert not result.is_error, result.content
                data=result.structured_content
                assert data['verified'] and data['text']
                report['source_fetch']={k:data[k] for k in ('skill_id','source','commit','blob','verified','next_line')}
            print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch-source',action='store_true',help='Read one pinned public GitHub text file and verify its hash; never execute it')
    anyio.run(check,p.parse_args().fetch_source)
