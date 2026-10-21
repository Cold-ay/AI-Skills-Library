"""Generate the static AI Skill Library website from reviewed repository content."""
from html import escape
import json
from pathlib import Path
import re
import hashlib
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bundles import combinations
from urllib.parse import urlparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def inline(text):
    text=escape(text)
    def link(m):
        label,url=m.groups()
        if urlparse(url).scheme not in ('https','http'):return label
        return '<a href="'+url+'" target="_blank" rel="noopener noreferrer">'+label+'</a>'
    text=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)

def markdown(source):
    """Small escaped Markdown subset; raw HTML and unsafe URL schemes are never allowed."""
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if line.startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|\-]+$',lines[i+1]):
            headers=[inline(c.strip()) for c in line.strip('|').split('|')];i+=2;rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in lines[i].strip('|').split('|'))+'</tr>');i+=1
            out.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable comparison table"><table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>');continue
        if not line.strip():i+=1;continue
        match=re.match(r'^(#{1,6}) (.*)',line)
        if match:
            level=max(2,min(len(match[1]),6));out.append(f'<h{level}>'+inline(match[2])+f'</h{level}>');i+=1;continue
        if line.startswith('- '):
            items=[]
            while i<len(lines) and lines[i].startswith('- '):items.append('<li>'+inline(lines[i][2:])+'</li>');i+=1
            out.append('<ul>'+''.join(items)+'</ul>');continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- )',lines[i]):paragraph.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(out)

def build():
    dest=HERE/'dist';dest.mkdir(exist_ok=True)
    skills=json.loads((ROOT/'catalog/skills.json').read_text())
    posts=[]
    for file in sorted((ROOT/'reports').glob('*.md'),key=lambda p:(p.stem[:10], 'video-review' in p.stem, p.stem),reverse=True):
        source=file.read_text();title=source.splitlines()[0].lstrip('# ')
        video='video-review' in file.stem
        combo='combinations' in file.stem
        first_paragraph=next((line.strip() for line in source.splitlines()[1:] if line.strip() and not line.startswith(('#','|','-','```'))),'Read the findings, sources and limitations in this report.')
        posts.append(dict(slug=file.stem,title=title,date=file.stem[:10],category='Source review' if video else 'Discovery',readTime=max(1,len(source.split())//200),excerpt='Seven new skills, six workflow combinations and a reusable primary-source research method.' if combo else 'Ten recommendations, nine additions, and the evidence behind each decision.' if video else 'The preserved discovery snapshot: real repository stars, candidate projects and collection limits.' if file.stem=='2026-10-21' else first_paragraph[:240],html=markdown('\n'.join(source.splitlines()[1:])),source=f'https://github.com/Cold-ay/AI-Skills-Library/blob/main/reports/{file.name}',markdown=source))
    packs=combinations()
    artifacts=json.loads((dest/'downloads/index.json').read_text())
    for a in artifacts:
        path=dest/'downloads'/a['file']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('Bundle archive integrity mismatch')
    payload=json.dumps(dict(skills=skills,posts=posts,combinations=packs,downloads=artifacts),ensure_ascii=True)
    (dest/'data.js').write_text('window.AI_SKILL_LIBRARY = '+payload+';\n')
    print(f'Built {len(posts)} articles and {len(skills)} skill records in {dest}')
    return posts

if __name__=='__main__':build()
