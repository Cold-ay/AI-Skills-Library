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
const {mcpSetupPlan}=require('../site/dist/library-ui.js');
test('MCP setup uses the selected client and platform without assuming an installed server',()=>{
 const windows=mcpSetupPlan('claude','windows');assert.equal(windows.length,4);assert.ok(windows[2].command.startsWith('.\\.venv-mcp'));
 assert.ok(windows[1].command.startsWith('py -3 -m venv'));
 assert.ok(windows[2].command.includes('.venv-mcp\\Scripts\\python.exe mcp_server.py --config claude'));
 assert.ok(windows[3].command.endsWith('scripts/smoke_mcp.py'));
 const posix=mcpSetupPlan('codex','posix');assert.ok(posix[2].command.endsWith('--config codex'));
 assert.ok(posix[2].description.includes('only prints settings'));
 assert.ok(!posix.some(step=>step.command.includes('codex mcp add')));
});

test('Skill Bridge generates native local paths, preview and explicit installation commands',()=>{
 const {bridgePlan}=require('../site/dist/library-ui.js');
 const pkg={invocation:'combination-react-motion',root:'ai-skill-library-combination-react-motion'};
 const codex=bridgePlan(pkg,'codex','project','posix');
 assert.equal(codex.directory,'<project>/.agents/skills');
 assert.equal(codex.chat,'$combination-react-motion <your task>');
 assert.ok(codex.preview.includes('--project "/path/to/project"'));
 assert.ok(!codex.preview.includes('--reviewed'));
 assert.equal(codex.install,codex.preview+' --reviewed');
 const claude=bridgePlan(pkg,'claude','user','windows');
 assert.equal(claude.directory,'~/.claude/skills');
 assert.equal(claude.chat,'/combination-react-motion <your task>');
 assert.ok(claude.install.startsWith('py -3 install.py'));
 assert.ok(!claude.install.includes('--project'));
 const cursor=bridgePlan(pkg,'cursor','project','windows');
 assert.equal(cursor.directory,'<project>/.cursor/skills');
 assert.ok(cursor.install.includes('C:\\path\\to\\project'));
 assert.equal(bridgePlan(null),null);
 assert.equal(bridgePlan(pkg,'cloud'),null);
});


test('chat setup request pins a package, reviews before installation, and respects the selected scope',()=>{
 const {bridgePlan}=require('../site/dist/library-ui.js');
 const pkg={invocation:'microinteractions',root:'ai-skill-library-skill-microinteractions',file:'skill-microinteractions.zip',sha256:'a'.repeat(64)};
 const project=bridgePlan(pkg,'cursor','project');
 assert.ok(project.setup.includes('https://ai-skill-library.vercel.app/bridge/skill-microinteractions.zip'));
 assert.ok(project.setup.includes('a'.repeat(64)));
 assert.ok(project.setup.includes('Review README.md, install.py, PACKAGE.json'));
 assert.ok(project.setup.includes('--platform cursor --scope project --project <absolute current-project path>'));
 assert.ok(project.setup.includes('If files conflict'));
 assert.ok(project.setup.includes('Do not run any upstream script'));
 const personal=bridgePlan(pkg,'claude','user');
 assert.ok(personal.setup.includes('--platform claude --scope user'));
 assert.ok(!personal.setup.includes('--project'));
});
