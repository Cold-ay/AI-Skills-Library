"""Read-only weekly discovery: data is never executed or auto-promoted to catalogue."""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from skills import ROOT, catalogue
API='https://api.github.com/'

def api(path):
    headers={'Accept':'application/vnd.github+json','User-Agent':'AI-Skills-Library'}
    if os.environ.get('GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
    for attempt in range(3):
        try:
            with urlopen(Request(API+path,headers=headers),timeout=30) as r:return json.load(r)
        except HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==2:raise
            time.sleep(2**attempt)

def collect(get=api, now=None):
    now=now or datetime.now(timezone(timedelta(hours=8)))
    since=(now-timedelta(days=90)).date().isoformat()
    queries=[f'"agent skills" stars:>=50 archived:false pushed:>={since}',f'"codex" "skills" stars:>=20 archived:false created:>={since}',f'"SKILL.md" stars:>=100 archived:false pushed:>={since}']
    result={'observed_at':now.isoformat(),'queries':queries,'errors':[],'repositories':[]}
    selected={e['repo']:{'curated'} for e in catalogue()}
    for query in queries:
        try:
            data=get('search/repositories?'+urlencode({'q':query,'sort':'stars','order':'desc','per_page':8}))
            if data.get('incomplete_results'):result['errors'].append('Incomplete search: '+query)
            for item in data['items']:selected.setdefault(item['full_name'],set()).add(query)
        except (HTTPError,URLError,TimeoutError,ValueError,KeyError) as exc:result['errors'].append('Search failed: '+query+' ('+type(exc).__name__+(' '+str(exc.code) if isinstance(exc, HTTPError) else '')+')')
    for repo,reasons in sorted(selected.items()):
        try:
            if not re.fullmatch(r'[\w.-]+/[\w.-]+',repo):raise ValueError('Bad repository')
            m=get('repos/'+repo);sha=get('repos/'+repo+'/commits/'+m['default_branch'])['sha']
            tree=get('repos/'+repo+'/git/trees/'+sha+'?recursive=1')
            paths=[f['path'] for f in tree['tree'] if f['type']=='blob' and f['path'].endswith('SKILL.md')]
            if tree.get('truncated'):result['errors'].append('Truncated tree: '+repo)
            result['repositories'].append(dict(repo=repo,stars=m['stargazers_count'],created_at=m['created_at'],pushed_at=m['pushed_at'],archived=m['archived'],license=(m.get('license') or {}).get('spdx_id','unknown'),commit=sha,skill_paths=paths[:20],skill_count=len(paths),reasons=sorted(reasons),codex='unknown',evidence=API+'repos/'+repo))
        except (HTTPError,URLError,TimeoutError,ValueError,KeyError) as exc:result['errors'].append('Repository failed: '+repo+' ('+type(exc).__name__+(' '+str(exc.code) if isinstance(exc, HTTPError) else '')+')')
    return result

def cell(s):return str(s).replace('|','\\|').replace('\n',' ').replace('<','&lt;').replace('>','&gt;')

def render(s,previous=None):
    old={r['repo']:r['stars'] for r in (previous or {}).get('repositories',[])}
    known={e['repo']:e for e in catalogue()}
    lines=['# Weekly AI Skills discovery','','Observed: '+s['observed_at'],'','Stars are repository popularity, not quality. Candidates remain unknown for Codex; SKILL.md presence is not a runtime test.','','| Repository | Stars | Change | Lane | Skill files | Codex | Evidence |','|---|---:|---:|---|---:|---|---|']
    for r in sorted(s['repositories'],key=lambda x:x['stars'],reverse=True):
        delta=f"{r['stars']-old[r['repo']]:+d}" if r['repo'] in old else 'baseline unavailable'
        lane='curated watchlist' if r['repo'] in known else 'review candidate' if r['skill_paths'] else 'reject: no skill files'
        compat=known[r['repo']]['codex']['status']+' (catalogue pin only)' if r['repo'] in known else 'unknown'
        lines.append(f"| [{r['repo']}](https://github.com/{r['repo']}) | {r['stars']} | {delta} | {lane} | {r['skill_count']} | {compat} | [API]({r['evidence']}) / [tree](https://github.com/{r['repo']}/tree/{r['commit']}) |")
    lines+=['','## Worth reviewing','','Mechanical shortlist: skill files present, non-archived, identified repository license. Not human endorsement; inspect per-skill licensing and instructions.']
    candidates=[r for r in s['repositories'] if r['repo'] not in known and r['skill_paths'] and not r['archived'] and r['license'] not in ('unknown','NOASSERTION')]
    for r in sorted(candidates,key=lambda x:x['stars'],reverse=True)[:5]:lines.append(f"- [{r['repo']}](https://github.com/{r['repo']}/tree/{r['commit']}): {r['stars']} stars; {r['skill_count']} skill files; {cell(r['license'])}; created {r['created_at']}. Codex unknown. Trial: inspect one skill and dependencies, then test in a disposable project.")
    if not candidates:lines.append('- No candidates met this limited screen.')
    lines+=['','## Review gate','','- Confirm usefulness, provenance, license and dependencies at the pinned commit.','- Inspect scripts, network calls, hooks, credentials and sibling references.','- Record Codex version, setup and a reproducible smoke test before claiming runtime verification.','- Update catalogue pins in a separate reviewed change; never execute a discovered installer.','','## Search coverage','']+['- `'+q+'` (top 8)' for q in s['queries']]
    lines+=['','Bounded search, not an exhaustive ranking. Star growth requires a prior dated snapshot.','','## Collection errors','']+(['- '+cell(e) for e in s['errors']] or ['None.'])
    return '\n'.join(lines)+'\n'

def main():
    s=collect();out=ROOT/'reports';out.mkdir(exist_ok=True);date=s['observed_at'][:10]
    older=sorted(p for p in out.glob('????-??-??.json') if p.stem<date)
    previous=json.loads(older[-1].read_text()) if older else None
    (out/(date+'.json')).write_text(json.dumps(s,indent=2)+'\n');(out/(date+'.md')).write_text(render(s,previous))
    print(f"Saved {date}: {len(s['repositories'])} repositories, {len(s['errors'])} errors")
    if s['errors']:raise SystemExit(1)
if __name__=='__main__':main()
