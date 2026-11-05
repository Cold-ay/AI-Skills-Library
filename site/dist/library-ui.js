/* Pure catalogue operations shared by the browser UI and regression tests. */
(function(root){
 'use strict';
 const sortLabels={curated:'Curated order','stars-desc':'GitHub stars: high to low','stars-asc':'GitHub stars: low to high',name:'Name: A–Z',recent:'Research date: newest first',evidence:'Codex evidence level'};
 const evidenceRank={'verified-static':0,'upstream-claimed':1,unknown:2};
 function normalizeSort(value){return Object.hasOwn(sortLabels,value)?value:'curated';}
 function sortSkills(entries,mode){
  const result=entries.slice();mode=normalizeSort(mode);
  const name=(a,b)=>a.id.localeCompare(b.id,'en');
  const compare={
   'stars-desc':(a,b)=>b.stars-a.stars||name(a,b),
   'stars-asc':(a,b)=>a.stars-b.stars||name(a,b),
   name,
   recent:(a,b)=>b.observed_at.localeCompare(a.observed_at)||name(a,b),
   evidence:(a,b)=>(evidenceRank[a.codex.status]??3)-(evidenceRank[b.codex.status]??3)||name(a,b)
  }[mode];
  return compare?result.sort(compare):result;
 }
 function matchesPurpose(combination,entries,category){
  return category==='all'||combination.skills.some(id=>entries.some(s=>s.id===id&&s.category===category));
 }
 function mcpSetupPlan(client='codex',platform='posix'){
  client=client==='claude'?'claude':'codex';platform=platform==='windows'?'windows':'posix';
  const python=platform==='windows'?'.\\.venv-mcp\\Scripts\\python.exe':'.venv-mcp/bin/python';
  return [
   {title:'Get the library',description:'Open a terminal and clone the repository. Already have it? Use your existing checkout and review its updates.',command:'git clone https://github.com/Cold-ay/AI-Skills-Library.git\ncd AI-Skills-Library'},
   {title:'Prepare the server',description:'Use Python 3.10 or newer. This creates an isolated environment and installs the official MCP SDK.',command:(platform==='windows'?'py -3':'python3')+' -m venv .venv-mcp\n'+python+' -m pip install -r requirements-mcp.txt'},
   {title:'Connect '+(client==='claude'?'Claude Code':'Codex'),description:'Run this to print configuration with your actual checkout paths. Merge the output into your client’s MCP settings, then reconnect. This command only prints settings.',command:python+' mcp_server.py --config '+client},
   {title:'Check the connection',description:'Run the protocol check below. In your reconnected client, confirm search_skills is available, then paste the example request.',command:python+' scripts/smoke_mcp.py'}
  ];
 }
 const api={sortLabels,normalizeSort,sortSkills,matchesPurpose,mcpSetupPlan};root.AI_SKILL_UI=api;
 if(typeof module==='object'&&module.exports)module.exports=api;
})(globalThis);
