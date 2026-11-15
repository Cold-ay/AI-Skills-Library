'use strict';
const {skills,posts,combinations,downloads,mcpGuide,bridgePackages=[],codexInstaller}=window.AI_SKILL_LIBRARY;
const names={'presentations':'Presentations & PPT','website-ui':'Website & UI','mobile-app':'Mobile app design','video':'Video & storytelling','coding':'Coding','token-context':'Token & context','research-automation':'Research & automation','skill-engineering':'Skill engineering','writing-editing':'Writing & editing','product-management':'Product management','electronics-eda':'Electronics & EDA','mobile-release':'Mobile release','game-development':'Game development','writing-communication':'Writing & communication'};
const {sortLabels,normalizeSort,sortSkills,matchesPurpose,mcpSetupPlan,bridgePlan,codexInstallPlan}=window.AI_SKILL_UI;
const statuses={'verified-static':'Official static evidence','upstream-claimed':'Upstream claims support','unknown':'Unknown compatibility'};
const $=s=>document.querySelector(s);
if($('#mcp-guide'))$('#mcp-guide').innerHTML=mcpGuide||'';
function mcpSkillPrompt(id){return 'Use the ai_skill_library MCP server to inspect get_skill for '+id+', then read_skill_file for its SKILL.md and remaining pages. Review requirements and use the skill for: <your task>. Do not assume reading source installs its dependencies.';}
function el(tag,cls,text){const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node;}
function link(href,text,cls){const node=el('a',cls,text);node.href=href;if(href.startsWith('https:')){node.target='_blank';node.rel='noopener noreferrer';}return node;}
function toast(text){$('#toast').textContent=text;$('#toast').classList.add('visible');clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').classList.remove('visible'),3500);}
function download(name,text){const url=URL.createObjectURL(new Blob([text],{type:'text/markdown;charset=utf-8'}));const a=link(url,'');a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function copy(text,button){const label=button.dataset.copyLabel||button.textContent;button.dataset.copyLabel=label;try{await navigator.clipboard.writeText(text);clearTimeout(button.copyTimer);button.textContent='Copied ✓';button.copyTimer=setTimeout(()=>button.textContent=label,1800);}catch{toast('Clipboard unavailable. Select the visible command or open the full setup reference to copy it.');}}
$('#nav-count').textContent=skills.length;$('#skill-count').textContent=skills.length;$('#post-count').textContent=String(posts.length).padStart(2,'0');
function categoryIcon(category){const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');const paths={'presentations':'M3 4h18v13H3z M12 17v5 M8 22h8 M7 8h10 M7 12h6','mobile-app':'M7 2h10v20H7z M10 5h4 M11 19h2','website-ui':'M3 5h18v14H3z M3 9h18 M7 7h.01 M10 7h.01','video':'M4 5h16v14H4z M10 9l5 3-5 3z','coding':'M8 6l-6 6 6 6 M16 6l6 6-6 6 M14 3l-4 18','token-context':'M4 6h16 M4 12h16 M4 18h16 M8 3v6 M16 9v6 M9 15v6','research-automation':'M15 15l6 6 M17 10a7 7 0 1 0-14 0 7 7 0 0 0 14 0','skill-engineering':'M5 3v18 M19 3v18 M2 8h6 M16 16h6 M8 8h8v8H8z','writing-editing':'M4 20h4l10.5-10.5-4-4L4 16z M13.2 6.8l4 4','product-management':'M7 3h10v4H7z M6 7h12v14H6z M9 12h6 M9 16h4','electronics-eda':'M8 8h8v8H8z M4 10h4 M4 14h4 M16 10h4 M16 14h4 M10 4v4 M14 4v4 M10 16v4 M14 16v4','mobile-release':'M8 2h8a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z M11 19h2','game-development':'M6 9h12a4 4 0 0 1 4 4v2a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4v-2a4 4 0 0 1 4-4z M8 13h4 M10 11v4 M16 13h.01 M18 15h.01','writing-communication':'M4 5h16v10H8l-4 4z M8 9h8 M8 12h5'};const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d',paths[category]||'M6 3h9l3 3v15H6z M9 12h6 M9 16h4');svg.append(path);return svg;}
const shortNames={'presentations':'Presentations & PPT','website-ui':'Website & UI','mobile-app':'Mobile app design','video':'Video','coding':'Coding','token-context':'Token & context','research-automation':'Research','skill-engineering':'Skill engineering','writing-editing':'Writing & editing','product-management':'Product','electronics-eda':'Electronics','mobile-release':'Mobile release','game-development':'Games','writing-communication':'Communication'};
const categories=[...Object.keys(names).filter(category=>skills.some(s=>s.category===category)),...new Set(skills.map(s=>s.category).filter(category=>!(category in names)))];
if($('#category-count'))$('#category-count').textContent=String(categories.length);
for(const category of categories){const name=names[category]||category,short=shortNames[category]||name;const count=skills.filter(s=>s.category===category).length;const a=link('#library/'+category,name);a.append(el('span','',String(count).padStart(2,'0')));$('#topic-links').append(a);const tile=link('#library/'+category,'','category-tile');tile.dataset.category=category;const symbol=el('span','category-icon');symbol.setAttribute('aria-hidden','true');symbol.append(categoryIcon(category));tile.append(symbol,el('h3','',short),el('span','',count+(count===1?' skill':' skills')));$('#category-grid').append(tile);const o=el('option','',name);o.value=category;$('#category-select').append(o);}
let postFilter='All';
function renderPosts(){const query=$('#report-search').value.trim().toLowerCase();const found=posts.filter(p=>(postFilter==='All'||p.category===postFilter)&&JSON.stringify([p.title,p.excerpt,p.markdown]).toLowerCase().includes(query));$('#posts').replaceChildren();$('#report-empty').hidden=!!found.length;for(const p of found){const row=link('#article/'+p.slug,'','post-row');const icon=el('div','post-icon'+(p.category==='Discovery'?' discovery':''),p.category==='Discovery'?'↗':'10');icon.setAttribute('aria-hidden','true');icon.append(el('small','',p.category==='Discovery'?'Discovery':'Design review'));const info=el('div','post-info');const meta=el('div','meta');meta.append(el('span','tag',p.category),el('span','',p.date+' / '+p.readTime+' min read'));info.append(meta,el('h3','post-title',p.title),el('p','',p.excerpt));row.append(icon,info,el('span','post-arrow','↗'));$('#posts').append(row);}}
$('#report-search').addEventListener('input',renderPosts);$('#post-filters').addEventListener('click',e=>{const button=e.target.closest('[data-post-filter]');if(!button)return;postFilter=button.dataset.postFilter;for(const b of $('#post-filters').querySelectorAll('button')){b.classList.toggle('selected',b===button);b.setAttribute('aria-pressed',b===button?'true':'false');}renderPosts();});
function codexInstallButton(kind,id){const plan=codexInstallPlan(codexInstaller,kind,id,'user');if(!plan)return null;const button=el('button','button small codex-install-action','Install with Codex');button.type='button';button.title='Copy a pinned request to paste into Codex; clicking does not install.';button.setAttribute('aria-label','Copy Codex installer request for '+id);button.addEventListener('click',()=>copy(plan.request,button));return button;}
function skillCard(s,heading='h2'){const card=el('article','skill-card');const top=el('div','card-top');top.append(el('span','tag',names[s.category]||s.category),el('span','','☆ '+s.stars.toLocaleString('en-US')));card.append(top,el(heading,'',s.id),el('p','',s.summary),el('span','badge '+s.codex.status,statuses[s.codex.status]));const details=el('details');details.append(el('summary','','Evidence & installation'));details.append(el('p','',s.reason),el('p','',s.requirements),el('p','','Source: '+s.repo+' · Commit '+s.commit.slice(0,12)),el('p','','Stars observed '+s.observed_at+'. No Codex runtime test recorded.'));const cmd=s.installable?'python3 skills.py install '+s.id+' --dest /path/to/project/.agents/skills --reviewed':'Upstream installation required; inspect the pinned README and dependencies.';details.append(el('code','',cmd),el('code','','$'+s.invocation+' <your task>'));details.append(link('https://github.com/'+s.repo+'/blob/'+s.commit+'/README.md','Pinned setup instructions ↗'));const actions=el('div','card-actions');actions.append(link(s.source,'Read source ↗'));const button=el('button','','Copy invocation');button.type='button';button.setAttribute('aria-label','Copy '+s.id+' invocation');button.addEventListener('click',()=>copy('$'+s.invocation+' <your task>',button));const mcpButton=el('button','','Copy MCP prompt');mcpButton.type='button';mcpButton.setAttribute('aria-label','Copy '+s.id+' MCP prompt');mcpButton.addEventListener('click',()=>copy(mcpSkillPrompt(s.id),mcpButton));actions.append(button,mcpButton);const nativeButton=codexInstallButton('skill',s.id);if(nativeButton)actions.append(nativeButton);actions.append(link('#install/skill/'+s.id,bridgePackages.some(p=>p.kind==='skill'&&p.id===s.id)?'Install in your agent ↗':'Setup options ↗','quiet-link bridge-launch'));card.append(details,actions);return card;}
function renderSkills(){const query=$('#skill-search').value.trim().toLowerCase(),category=$('#category-select').value,compat=$('#compat-select').value;const found=skills.filter(s=>(category==='all'||s.category===category)&&(compat==='all'||s.codex.status===compat)&&JSON.stringify([s.id,s.invocation,s.summary,s.reason,s.requirements,s.repo]).toLowerCase().includes(query));const mode=normalizeSort($('#skill-sort')?.value);$('#skills').replaceChildren(...sortSkills(found,mode).map(s=>skillCard(s)));$('#library-results').textContent=found.length+' of '+skills.length+' skills · '+sortLabels[mode];$('#skill-empty').hidden=!!found.length;}

for(const id of ['skill-search','category-select','compat-select','skill-sort'])$('#'+id).addEventListener(id==='skill-search'?'input':'change',()=>{renderSkills();const category=$('#category-select').value;const params=new URLSearchParams();if($('#skill-search').value)params.set('q',$('#skill-search').value);if($('#compat-select').value!=='all')params.set('evidence',$('#compat-select').value);if($('#skill-sort')?.value!=='curated')params.set('sort',normalizeSort($('#skill-sort')?.value));history.replaceState(null,'','#library'+(category==='all'?'':'/'+category)+(params.size?'?'+params:''));});
function article(slug){const p=posts.find(p=>p.slug===slug);const container=$('#article');container.replaceChildren();if(!p){container.append(el('h1','','Report not found'),el('p','','Return to the reports to choose an available report.'));return;}
const head=el('header','article-header');head.append(el('span','tag',p.category),el('h1','',p.title));const meta=el('div','meta');meta.append(el('span','',p.date),el('span','',p.readTime+' minute read'),el('span','','AI Skill Library'));head.append(meta);const actions=el('div','article-actions');actions.append(link(p.source,'View Markdown source ↗'));const exportButton=el('button','','Download report ↓');exportButton.type='button';exportButton.addEventListener('click',()=>download(p.slug+'.md',p.markdown));actions.append(exportButton);head.append(actions);const body=el('article','prose');body.innerHTML=p.html;container.append(head,body);document.title=p.title+' — AI Skill Library';}
function route(){const value=location.hash.slice(1)||'home';const [path,query='']=value.split('?');const params=new URLSearchParams(query);const [page,key,itemId]=path.split('/');const known=['home','reports','library','article','draft','about','combinations','connect','install'];const target=page==='mcp'?'connect':known.includes(page)?page:'home';for(const view of document.querySelectorAll('.view'))view.hidden=view.id!==target+'-view';for(const a of document.querySelectorAll('[data-nav]')){const active=a.dataset.nav===(target==='article'?'reports':target);a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}document.title=target==='connect'?'MCP — AI Skill Library':'AI Skill Library';if(target==='install')renderBridge(key,itemId);if(target==='article')article(key);if(target==='library'){$('#category-select').value=[...$('#category-select').options].some(o=>o.value===key)?key:'all';$('#skill-search').value=params.get('q')||'';$('#compat-select').value=statuses[params.get('evidence')]?params.get('evidence'):'all';if($('#skill-sort'))$('#skill-sort').value=normalizeSort(params.get('sort'));renderSkills();}window.scrollTo(0,0);}
try{const stored=JSON.parse(localStorage.getItem('ai-skill-library-draft') || localStorage.getItem('fieldnotes-draft')||'null');if(stored){$('#draft-title').value=String(stored.title||'');$('#draft-body').value=String(stored.body||'');$('#draft-status').textContent='Your previous browser draft has been restored.';}}catch{$('#draft-status').textContent='Browser storage unavailable. Export your draft to keep it.';}
$('#draft-form').addEventListener('submit',e=>{e.preventDefault();try{localStorage.setItem('ai-skill-library-draft',JSON.stringify({title:$('#draft-title').value,body:$('#draft-body').value}));$('#draft-status').textContent='Saved in this browser. Export Markdown to add it to the repository.';}catch{$('#draft-status').textContent='Could not save to browser storage. Use Export .md to keep your work.';}});
$('#export-draft').addEventListener('click',()=>{if(!$('#draft-form').reportValidity())return;const title=$('#draft-title').value.trim(),body=$('#draft-body').value;const date=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Hong_Kong',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());const slug=title.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,70)||'report';download(date+'-'+slug+'.md','# '+title+'\n\n'+body+'\n');$('#draft-status').textContent='Markdown exported. Add it to reports/ and rebuild to publish.';});
// Skill Bridge prepares local installation; browsing/copying never installs a package.
function renderBridge(kind,ident){
 kind=kind==='combination'?'combination':'skill';$('#bridge-kind').value=kind;
 const records=kind==='skill'?skills:combinations;
 $('#bridge-item').replaceChildren(...records.map(record=>{const option=el('option','',(record.title||record.id)+(bridgePackages.some(p=>p.kind===kind&&p.id===record.id)?'':' · upstream setup'));option.value=record.id;return option;}));
 const record=records.find(r=>r.id===ident)||records.find(r=>bridgePackages.some(p=>p.kind===kind&&p.id===r.id))||records[0];
 $('#bridge-item').value=record.id;
 const pkg=bridgePackages.find(p=>p.kind===kind&&p.id===record.id);
 $('#bridge-title').textContent=record.title||record.id;$('#bridge-summary').textContent=record.summary;
 $('#bridge-requirements').textContent=record.requirements;
 $('#bridge-source').href=kind==='skill'?record.source:'https://github.com/Cold-ay/AI-Skills-Library/blob/main/catalog/combinations.json';
 $('#bridge-evidence').textContent=kind==='skill'?'Codex evidence: '+statuses[record.codex.status]+'. A portable package does not establish upstream support in another host.':record.compatibility;
 $('#bridge-availability').textContent=pkg?'Portable installer available':'Upstream setup needed';
 $('#bridge-ready').hidden=!pkg;$('#bridge-upstream').hidden=!!pkg;
 const native=$('#bridge-platform').value==='codex'?codexInstallPlan(codexInstaller,kind,record.id,$('#bridge-scope').value):null;
 $('#codex-native').hidden=!native;
 if(native){$('#codex-native-destination').textContent=native.destination;$('#codex-native-paths').replaceChildren(...native.paths.map(path=>el('li','',path)));$('#codex-native-ref').textContent=native.ref;$('#codex-native-source').href=native.source;$('#codex-native-request').textContent=native.request;$('#codex-native-chat').textContent=native.chat;$('#codex-native-copy').onclick=()=>copy(native.request,$('#codex-native-copy'));}

 if(pkg){
  const plan=bridgePlan(pkg,$('#bridge-platform').value,$('#bridge-scope').value,$('#bridge-computer').value);
  $('#bridge-download').href='bridge/'+pkg.file;$('#bridge-download').download=pkg.file;
  $('#bridge-download').textContent='Download for '+({codex:'Codex',claude:'Claude Code',cursor:'Cursor'}[$('#bridge-platform').value])+' ↓';
  $('#bridge-package-info').textContent=Math.ceil(pkg.bytes/1024)+' KB · '+pkg.folders.length+' skill folders · Extracted folder: '+pkg.root;
  $('#bridge-checksum').textContent=pkg.sha256;$('#bridge-preview').textContent=plan.preview;$('#bridge-install').textContent=plan.install;$('#bridge-chat').textContent=plan.chat;$('#bridge-destination').textContent=plan.directory;$('#bridge-setup-copy').onclick=()=>copy(plan.setup,$('#bridge-setup-copy'));
 }else{
  $('#bridge-download').removeAttribute('href');
  $('#bridge-blocked-reason').textContent=!record.installable&&kind==='skill'?record.requirements:'This source has not been published as a complete licensed portable package. Existing CLI/source setup may be available; review its requirements first.';
 }
 const mcp=kind==='skill'?mcpSkillPrompt(record.id):'Use the ai_skill_library MCP server to get_combination for '+record.id+'. Review requirements and load stage instructions with read_skill_file only as needed. Help me with: <your task>.';
 $('#bridge-mcp-copy').onclick=()=>copy(mcp,$('#bridge-mcp-copy'));
 document.title='Skill Bridge — '+(record.title||record.id)+' — AI Skill Library';
}
$('#bridge-kind').addEventListener('change',()=>{location.hash='#install/'+$('#bridge-kind').value;});
$('#bridge-item').addEventListener('change',()=>{location.hash='#install/'+$('#bridge-kind').value+'/'+$('#bridge-item').value;});
for(const id of ['bridge-platform','bridge-scope','bridge-computer'])$('#'+id).addEventListener('change',()=>renderBridge($('#bridge-kind').value,$('#bridge-item').value));
for(const name of ['preview','install','chat'])$('#bridge-'+name+'-copy').addEventListener('click',()=>copy($('#bridge-'+name).textContent,$('#bridge-'+name+'-copy')));

window.addEventListener('hashchange',route);renderPosts();renderSkills();route();

$('.skip').addEventListener('click',event=>{event.preventDefault();$('#content').focus();});

const featuredIds=['taste-skill','react-best-practices','gsap-core','context-compression','remotion-best-practices','plugin-creator'];
for(const id of featuredIds){const s=skills.find(s=>s.id===id);if(s)$('#featured-skills').append(skillCard(s,'h3'));}
const starterIds={website:'taste-skill',coding:'systematic-debugging',video:'remotion-best-practices'};
let starterSkill;
function setStarter(task){starterSkill=skills.find(s=>s.id===starterIds[task]);$('#starter-category').textContent=names[starterSkill.category];$('#starter-name').textContent=starterSkill.id;$('#starter-description').textContent=starterSkill.summary;$('#starter-status').textContent=statuses[starterSkill.codex.status];$('#starter-status').className='badge '+starterSkill.codex.status;$('#starter-code').textContent='$'+starterSkill.invocation;$('#starter-detail').href='#library/'+starterSkill.category;for(const button of document.querySelectorAll('[data-task]')){const active=button.dataset.task===task;button.classList.toggle('selected',active);button.setAttribute('aria-pressed',String(active));}}
for(const button of document.querySelectorAll('[data-task]'))button.addEventListener('click',()=>setStarter(button.dataset.task));
$('#starter-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText('$'+starterSkill.invocation+' <your task>');toast('Invocation copied. Paste into Codex after installing the skill.');}catch{toast('Select the invocation text to copy it.');}});
setStarter('website');

let draftDirty=false;
for(const field of ['draft-title','draft-body'])$('#'+field).addEventListener('input',()=>{draftDirty=true;});
$('#draft-form').addEventListener('submit',()=>{if($('#draft-status').textContent.startsWith('Saved in this browser'))draftDirty=false;});
window.addEventListener('beforeunload',event=>{if(draftDirty){event.preventDefault();event.returnValue='';}});

for(const category of categories){
 if(combinations.some(b=>matchesPurpose(b,skills,category))){const option=el('option','',names[category]||category);option.value=category;$('#bundle-purpose')?.append(option);}
}
function renderCombinations(){
 const selectedHost=$('#bundle-agent')?.value;
 const claude=selectedHost==='claude',mcp=selectedHost==='mcp';
 const host=mcp?'your connected MCP client':claude?'Claude Code':'Codex';
 const query=$('#bundle-search').value.trim().toLowerCase();
 const purpose=$('#bundle-purpose')?.value||'all';
 const found=combinations.filter(b=>matchesPurpose(b,skills,purpose)&&JSON.stringify(b).toLowerCase().includes(query));
 $('#bundle-results').textContent=found.length+(found.length===1?' workflow · ':' workflows · ')+found.filter(b=>b.downloadable).length+' downloadable '+(found.filter(b=>b.downloadable).length===1?'pack':'packs');
 $('#combinations').replaceChildren();
 if(!found.length)$('#combinations').append(el('p','empty','No workflows match. Try a task such as React, article or research.'));
 for(const b of found){
  const card=el('article','skill-card combination-card');
  card.append(el('span','tag',b.downloadable?'Downloadable workflow':'Recipe · upstream setup'),el('h2','',b.title),el('p','',b.summary));
  const list=el('ol','combination-stages');
  for(const stage of b.stages){
   const li=el('li');const skill=skills.find(s=>s.id===stage.skill);
   const purpose=el('dl','member-purpose');purpose.append(el('dt','','Purpose'),el('dd','',skill.summary),el('dt','','Workflow role'),el('dd','',stage.title+'. '+stage.task));
   li.append(link('#library/'+skill.category,names[skill.category]||skill.category,'tag member-category'),link('#library?q='+encodeURIComponent(skill.id),skill.id+' ↗','member-name'),purpose,el('span','badge '+skill.codex.status,'Codex: '+statuses[skill.codex.status]));list.append(li);
  }
  card.append(list,link('#install/combination/'+b.id,bridgePackages.some(p=>p.kind==='combination'&&p.id===b.id)?'Install in your agent ↗':'Setup options ↗','quiet-link bridge-launch'));
  const details=el('details');details.append(el('summary','','Requirements & conflict handling'),el('p','',b.requirements),el('p','',b.conflicts),el('p','',b.compatibility));card.append(details);
  const nativeButton=codexInstallButton('combination',b.id);if(nativeButton)card.append(nativeButton);
  const artifact=downloads.find(d=>d.id===b.id);
  if(b.downloadable&&artifact){const a=link('downloads/'+artifact.file,'Download ZIP ↓','button primary');a.download=artifact.file;const prompt=mcp?'Use the ai_skill_library MCP server to get_combination for '+b.id+'. Read each stage skill with read_skill_file, including remaining pages, only as needed. Review requirements and help me with: <your task>.':claude?'Read CLAUDE.md and follow .agents/skills/combination-'+b.id+'/SKILL.md for this task: <your task>':'$combination-'+b.id+' <your task>';
   const promptBox=el('div','workflow-prompt');
   const promptHeader=el('div','workflow-prompt-header');
   const button=el('button','workflow-copy');button.type='button';button.setAttribute('aria-label','Copy '+b.title+' prompt');
   const icon=document.createElementNS('http://www.w3.org/2000/svg','svg');icon.setAttribute('viewBox','0 0 24 24');icon.setAttribute('aria-hidden','true');
   const iconPath=document.createElementNS('http://www.w3.org/2000/svg','path');const copyPath='M9 9h11v11H9z M15 9V4H4v11h5';iconPath.setAttribute('d',copyPath);icon.append(iconPath);
   const label=el('span','','Copy prompt');button.append(icon,label);
   const command=el('code','workflow-command',prompt);command.tabIndex=0;
   button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(prompt);clearTimeout(button.copyTimer);label.textContent='Copied';iconPath.setAttribute('d','M5 12l4 4L19 6');button.classList.add('is-copied');toast('Prompt copied. Paste into '+host+' after setting up this pack.');button.copyTimer=setTimeout(()=>{label.textContent='Copy prompt';iconPath.setAttribute('d',copyPath);button.classList.remove('is-copied');},2000);}catch{command.focus();toast('Clipboard unavailable. Select and copy the prompt shown here.');}});
   promptHeader.append(el('span','workflow-prompt-label','Use in '+host),button);
   promptBox.append(promptHeader,command,el('p','workflow-prompt-help',mcp?'Connect ai_skill_library first, then paste into your client and replace <your task>. MCP retrieves instructions; upstream dependencies still need setup.':claude?'Keep .agents/skills in your project and merge the included CLAUDE.md with existing instructions. Paste into Claude Code and replace <your task>. Copying does not install or run anything.':'After installing this pack, paste into a new Codex chat and replace <your task>. Copying does not install or run the workflow.'));
   card.append(a,promptBox,el('small','bundle-integrity',Math.ceil(artifact.bytes/1024)+' KB · '+artifact.files+' files · SHA-256 '+artifact.sha256));card.append(el('p','',mcp?'MCP retrieves pinned source directly; no ZIP extraction is needed to read instructions. External tool and runtime dependencies still require separate setup.':'Review the ZIP, stage extraction, then copy .agents/skills into your project without overwriting existing folders. Dependencies are installed separately.'));}
  else {card.append(el('code','','python3 bundles.py show '+b.id));const button=el('button','button small','Copy MCP workflow prompt');button.type='button';button.addEventListener('click',()=>copy('Use the ai_skill_library MCP server to get_combination for '+b.id+'. Review stage requirements, load instructions with read_skill_file as needed, and help me with: <your task>.',button));card.append(button,link('#connect','MCP setup ↗','quiet-link'));}
  $('#combinations').append(card);
 }
}
$('#bundle-purpose')?.addEventListener('change',renderCombinations);$('#bundle-search').addEventListener('input',renderCombinations);$('#bundle-agent')?.addEventListener('change',renderCombinations);renderCombinations();

// MCP onboarding is an interactive guide; commands run only when the user pastes them locally.
let mcpStep=0;
const mcpStepNames=['Get the library','Prepare the server','Connect your client','Try your first request'];
function renderMcpSetup(){
 const plan=mcpSetupPlan($('#mcp-client').value,$('#mcp-platform').value);const step=plan[mcpStep];
 $('#mcp-step-count').textContent='Step '+(mcpStep+1)+' of 4';$('#mcp-step-title').textContent=step.title;$('#mcp-step-description').textContent=step.description;$('#mcp-step-command').textContent=step.command;
 $('#mcp-first-request').hidden=mcpStep!==3;$('#mcp-previous').disabled=mcpStep===0;$('#mcp-next').hidden=mcpStep===3;
 for(const [index,button] of Array.from($('#mcp-steps').children).entries()){button.classList.toggle('selected',index===mcpStep);button.setAttribute('aria-pressed',String(index===mcpStep));}
}
for(const [index,name] of mcpStepNames.entries()){const button=el('button');button.type='button';button.append(el('span','',String(index+1).padStart(2,'0')),el('span','',name));button.addEventListener('click',()=>{mcpStep=index;renderMcpSetup();});$('#mcp-steps').append(button);}
for(const id of ['mcp-client','mcp-platform'])$('#'+id).addEventListener('change',renderMcpSetup);
$('#mcp-previous').addEventListener('click',()=>{mcpStep=Math.max(0,mcpStep-1);renderMcpSetup();});$('#mcp-next').addEventListener('click',()=>{mcpStep=Math.min(3,mcpStep+1);renderMcpSetup();});
$('#mcp-command-copy').addEventListener('click',()=>copy($('#mcp-step-command').textContent,$('#mcp-command-copy')));$('#mcp-request-copy').addEventListener('click',()=>copy($('#mcp-request-text').textContent,$('#mcp-request-copy')));
$('#mcp-start').addEventListener('click',()=>{$('#mcp-setup').scrollIntoView({block:'start'});$('#mcp-client').focus({preventScroll:true});});
$('#mcp-skill-count').textContent=skills.length;$('#mcp-workflow-count').textContent=combinations.length;
const mcpDemos={mobile:{question:'Help me choose skills for a mobile app.',category:'mobile-app',ids:['expo-design-system','swiftui-expert']},coding:{question:'Help me review code and verify the result.',category:'coding',ids:['receiving-code-review','verification-before-completion']},context:{question:'Help me keep a long session focused.',category:'token-context',ids:['filesystem-context','context-compression']}};
function renderMcpDemo(key){const demo=mcpDemos[key];$('#mcp-demo-question').textContent=demo.question;$('#mcp-demo-tool').textContent='search_skills({ category: "'+demo.category+'" })';$('#mcp-demo-results').replaceChildren();for(const id of demo.ids){const skill=skills.find(s=>s.id===id);if(!skill)continue;const card=link('#library?q='+encodeURIComponent(id),'','mcp-demo-result');card.append(el('span','tag',names[skill.category]||skill.category),el('h3','',skill.id),el('p','',skill.summary),el('span','mcp-demo-link','Review the skill ↗'));$('#mcp-demo-results').append(card);}for(const button of document.querySelectorAll('[data-mcp-demo]')){const selected=button.dataset.mcpDemo===key;button.classList.toggle('selected',selected);button.setAttribute('aria-pressed',String(selected));}}
for(const button of document.querySelectorAll('[data-mcp-demo]'))button.addEventListener('click',()=>renderMcpDemo(button.dataset.mcpDemo));
renderMcpSetup();renderMcpDemo('mobile');
