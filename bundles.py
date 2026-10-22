"""Build deterministic, inert skill ZIPs from reviewed pins; never execute source code."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
from skills import ROOT, catalogue, safe_path, blob_hash, fetch, raw_file_url


def combinations():
    data=json.loads((ROOT/'catalog/combinations.json').read_text())
    entries={e['id']:e for e in catalogue()};seen=set()
    for b in data:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',b['id']) or b['id'] in seen:
            raise ValueError('Invalid combination id')
        seen.add(b['id'])
        if len(b['skills'])<2 or len(set(b['skills']))!=len(b['skills']):raise ValueError('Duplicate or missing members')
        for ident in b['skills']:
            if ident not in entries:raise ValueError('Unknown member')
            if b['downloadable'] and (not entries[ident]['installable'] or (entries[ident].get('license') or {}).get('spdx_id')!='MIT'):
                raise ValueError('Bundle requires reviewed standalone MIT members')
        if not b['stages'] or not b['requirements'] or not b['conflicts']:raise ValueError('Missing workflow boundaries')
        if any(stage['skill'] not in b['skills'] for stage in b['stages']):raise ValueError('Unknown stage member')
        if b['downloadable']:
            for ident in b['skills']:
                license=b['licenses'][ident];safe_path(license['path'])
                if not re.fullmatch(r'[0-9a-f]{40}',license['blob']):raise ValueError('Unpinned license')
    return data


def workflow(b,entries):
    lines=['---','name: combination-'+b['id'],'description: '+b['summary'],'---','','# '+b['title'],'',b['summary'],'','Use only when this combination is explicitly requested. Follow the stages in order; do not load all skills at once. Host and user instructions take precedence. Never install dependencies, send data or run bundled scripts without reviewing them for the current task.','','## Stages','']
    for i,stage in enumerate(b['stages'],1):
        e=entries[stage['skill']]
        lines+=['### '+str(i)+'. '+stage['title'],'',f"Read ../{e['id']}/SKILL.md for ${e['invocation']}. {stage['task']}",'']
    lines+=['## Dependencies','',b['requirements'],'','## Conflicts and limits','',b['conflicts'],'','Compatibility is proposed from static source review, not an end-to-end Codex runtime test. Stop and report missing dependencies rather than silently substituting tools.']
    return '\n'.join(lines)+'\n'



def claude_instructions(b):
    path='.agents/skills/combination-'+b['id']+'/SKILL.md'
    return ('# '+b['title']+' — Claude Code workflow\n\n'
        'When the user explicitly requests the '+b['id']+' workflow, read `'+path+'`, then read each stage skill from its sibling folder as needed. Paths in this file are relative to the project root. Paths inside a SKILL.md are relative to that skill directory.\n\n'
        'The .agents directory is shared source storage here; this adapter does not claim that Claude Code automatically discovers it as native slash-command skills. Use an explicit request to read the workflow. Do not use Codex dollar-prefixed invocations as Claude slash commands.\n\n'
        'Follow the stages in order and preserve the handoff artifacts. Load only the stage needed. Follow existing project conventions and user/host instructions. Never run bundled scripts, install dependencies, contact services or launch subagents merely because this file was loaded; review their need within the current authorized task. Report missing host tools or dependencies.\n\n'
        '## Requirements\n\n'+b['requirements']+'\n\n## Conflicts and limits\n\n'+b['conflicts']+'\n\n'
        'This is a library-authored CLAUDE.md adapter, not a claim of upstream Claude support or a successful end-to-end runtime test. No dependencies are bundled.\n')


def call_prompt(b,agent='codex'):
    if not b['downloadable']:return 'Recipe only: follow stages in show; no integration skill installed.'
    if agent=='claude':return 'Read CLAUDE.md and follow .agents/skills/combination-'+b['id']+'/SKILL.md for this task: <your task>'
    return '$combination-'+b['id']+' <your task>'


def build_bundle(b,destination,reviewed=False,downloader=fetch):
    if not reviewed:raise ValueError('Review pins and licenses first; pass --reviewed')
    if not b['downloadable']:raise ValueError('Recipe only; upstream setup required')
    entries={e['id']:e for e in catalogue()};payload={};total=0
    def add(name,data):
        nonlocal total
        safe_path(name)
        total+=len(data)
        if total>25_000_000:raise ValueError('Bundle exceeds 25 MB')
        payload[name]=data
    for ident in b['skills']:
        e=entries[ident]
        if not e['installable'] or (e.get('license') or {}).get('spdx_id')!='MIT':raise ValueError('Unreviewed member')
        for f in e['files']:
            safe_path(f['path'])
            data=downloader(raw_file_url(e['repo'], e['commit'], e['path'], f['path']))
            if len(data)>5_000_000 or blob_hash(data)!=f['blob']:raise ValueError('Skill integrity mismatch')
            add('.agents/skills/'+ident+'/'+f['path'],data)
        license=b['licenses'][ident];safe_path(license['path'])
        data=downloader(f"https://raw.githubusercontent.com/{e['repo']}/{e['commit']}/{license['path']}")
        if blob_hash(data)!=license['blob']:raise ValueError('License integrity mismatch')
        add('LICENSES/'+ident+'.txt',data)
    add('.agents/skills/combination-'+b['id']+'/SKILL.md',workflow(b,entries).encode())
    add('CLAUDE.md',claude_instructions(b).encode())
    add('README.md',('# '+b['title']+'\n\n'+b['summary']+'\n\nReview all files before use. Extract into a clean staging directory, then copy .agents/skills into your project after checking for collisions. No packages or dependencies are installed by extraction. Start a new Codex session and explicitly invoke `$combination-'+b['id']+' <your task>`. For Claude Code, copy or merge the included CLAUDE.md into the project root without replacing existing instructions, keep .agents/skills alongside it, and explicitly ask Claude to read the combination SKILL.md. This adapter uses file references, not native slash-command discovery. The workflow sequences skills; simultaneous execution and runtime compatibility in either host are untested.\n\n'+b['requirements']+'\n\n'+b['conflicts']+'\n\nOriginal upstream files remain unmodified and retain their licenses. The orchestration text is library-authored. ZIPs contain instruction text and may contain passive scripts; nothing was executed to build them.\n').encode())
    manifest={'combination':b,'skills':[entries[i] for i in b['skills']],'sha256':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(payload.items())}}
    add('MANIFEST.json',(json.dumps(manifest,indent=2)+'\n').encode())
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive creation preserves previous artifacts and prevents partial published files.
    with destination.open('xb') as stream:
        with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
            for name,data in sorted(payload.items()):
                info=zipfile.ZipInfo(name,(2026,10,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,data)
    return {'file':destination.name,'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'bytes':destination.stat().st_size,'files':len(payload)}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('list')
    for cmd in ('show','call','build'):
        parser=sub.add_parser(cmd);parser.add_argument('id')
        if cmd=='call':parser.add_argument('--agent',choices=('codex','claude'),default='codex')
        if cmd=='build':parser.add_argument('--out',required=True);parser.add_argument('--reviewed',action='store_true')
    args=p.parse_args()
    try:
        data=combinations()
        if args.command=='list':
            for b in data:print(b['id']+' — '+b['title']+' ['+('ZIP' if b['downloadable'] else 'recipe only')+']')
            return
        b=next((b for b in data if b['id']==args.id),None)
        if b is None:raise ValueError('Unknown combination')
        if args.command=='show':print(json.dumps(b,indent=2))
        elif args.command=='call':print(call_prompt(b,args.agent))
        else:print(json.dumps(build_bundle(b,args.out,args.reviewed),indent=2))
    except (ValueError,OSError,KeyError) as e:p.exit(1,'Error: '+str(e)+'\n')
if __name__=='__main__':main()
