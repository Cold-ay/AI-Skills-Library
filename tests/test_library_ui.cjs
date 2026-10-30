'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {sortSkills,normalizeSort,matchesPurpose}=require('../site/dist/library-ui.js');
const rows=[
 {id:'zulu',stars:100,observed_at:'2026-10-21',category:'coding',codex:{status:'unknown'}},
 {id:'beta',stars:20,observed_at:'2026-10-31',category:'mobile-app',codex:{status:'verified-static'}},
 {id:'alpha',stars:100,observed_at:'2026-10-31',category:'token-context',codex:{status:'upstream-claimed'}}
];
const ids=items=>items.map(s=>s.id);
test('star sorts are numeric with deterministic alphabetical ties',()=>{
 assert.deepEqual(ids(sortSkills(rows,'stars-desc')),['alpha','zulu','beta']);
 assert.deepEqual(ids(sortSkills(rows,'stars-asc')),['beta','alpha','zulu']);
});
test('name, research date and documentary evidence sorts',()=>{
 assert.deepEqual(ids(sortSkills(rows,'name')),['alpha','beta','zulu']);
 assert.deepEqual(ids(sortSkills(rows,'recent')),['alpha','beta','zulu']);
 assert.deepEqual(ids(sortSkills(rows,'evidence')),['beta','alpha','zulu']);
});
test('sorting preserves source order and invalid URL modes use curated order',()=>{
 const before=JSON.stringify(rows);sortSkills(rows,'stars-desc');assert.equal(JSON.stringify(rows),before);
 assert.equal(normalizeSort('toString'),'curated');assert.equal(normalizeSort('bogus'),'curated');
 assert.deepEqual(ids(sortSkills(rows,'bogus')),ids(rows));assert.notEqual(sortSkills(rows,'curated'),rows);
});
test('purpose filtering includes workflows with matching members, preserves other stages',()=>{
 const workflow={skills:['zulu','beta']};
 assert.equal(matchesPurpose(workflow,rows,'coding'),true);
 assert.equal(matchesPurpose(workflow,rows,'mobile-app'),true);
 assert.equal(matchesPurpose(workflow,rows,'token-context'),false);
 assert.equal(matchesPurpose(workflow,rows,'all'),true);
 assert.deepEqual(workflow.skills,['zulu','beta']);
});
