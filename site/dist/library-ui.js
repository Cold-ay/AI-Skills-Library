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
 const api={sortLabels,normalizeSort,sortSkills,matchesPurpose};root.AI_SKILL_UI=api;
 if(typeof module==='object'&&module.exports)module.exports=api;
})(globalThis);
