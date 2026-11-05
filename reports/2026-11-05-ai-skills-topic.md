# Website skills from the GitHub ai-skills topic — 2026-11-05

Three new website skills, one downloadable design workflow and one testing recipe. The library now contains 56 skills and 23 combinations. This is a manual research report; no recurring schedule is configured.

## Where to start

For AI Skill Library itself, start with clearer action labels and feedback: users need to distinguish viewing instructions, copying a command, installing a skill and connecting an MCP client. The design pair below can review that journey without adding an animation framework. The testing skill can help maintain browser regression tests later; discovering it does not mean those tests have already run.

## Selected skills

| Skill and pinned instructions | Purpose | Repository stars | Codex evidence |
|---|---|---|---|
| [design-everyday-things](https://github.com/wondelai/skills/blob/d8d5d75f83da9f16d8aad5bab5f5b341a4770a30/design-everyday-things/SKILL.md) | Make website controls understandable | 2,590 | upstream-claimed |
| [microinteractions](https://github.com/wondelai/skills/blob/d8d5d75f83da9f16d8aad5bab5f5b341a4770a30/microinteractions/SKILL.md) | Design button feedback and interaction states | 2,590 | upstream-claimed |
| [playwright-best-practices](https://github.com/currents-dev/playwright-best-practices-skill/blob/283d5cbc5d11aac1abda058b16ad22c317d54dc0/playwright-best-practices/SKILL.md) | Write resilient website tests | 419 | unknown |

Stars are exact repository observations recorded on 2026-11-05, not skill-specific scores. The two Wondel entries share one repository count; do not add them together. All selected files are Markdown. Their regular Git blob hashes were verified before packaging; none of their instructions or scripts was executed.

### Design of Everyday Things: make the next action understandable

Use this to inspect navigation labels, control placement, constraints, visible outcomes and error recovery. For this site, ask whether a new visitor understands the difference between “Review the skill”, “Copy command” and “Set up your connection”. Its output should be a short control map: action, expected outcome, failure path and proposed label.

This is Wondel.ai's third-party interpretation of Don Norman's framework, not an official skill from Norman or the book publisher. Its scoring rubrics, timing rules and study percentages are design heuristics, not a usability test or guarantee. Optional sibling skills named in the instructions are not installed by this library.

### Microinteractions: make state changes visible and honest

Use this for copy feedback, filtering, retry behavior and step-by-step onboarding. Define idle, focus, pending, success and failure states, including repeated clicks and interruptions. For the MCP page, copying a setup command should confirm only the copy operation; it must never imply that installation or connection succeeded.

This is Wondel.ai's third-party interpretation of Dan Saffer's framework. It needs no animation package. Project accessibility requirements and reduced-motion behavior take precedence over decorative effects. Treat the skill's numeric self-scores as prompts for review, not measured user outcomes.

### Playwright Best Practices: turn behavior into regression checks

Currents.dev's activity index routes a testing task to focused references rather than loading the whole collection. Useful starting points are semantic locators, retrying assertions, keyboard/accessibility checks, responsive behavior and test isolation. The pinned folder contains 59 Markdown files, including the index; do not rely on the README's reference count as an inventory contract.

Requirements for executing generated tests include Node.js, TypeScript, Playwright Test and browser binaries; accessibility tooling is optional. Currents' hosted service is not required for the core guidance. No explicit Codex support was established in the pinned README or skill, so compatibility remains **unknown**. Claude runtime compatibility was not established either.

There are examples that need correction before reuse: the soft-assertion reference uses `expect.soft.hasFailures()`, while the official documentation demonstrates checking `test.info().errors`. The locator reference includes `internal:shadow`; use documented public locators and their default shadow-DOM handling. This is a useful reference collection with caveats, not a blanket endorsement of every snippet. Check the installed version and compile/run generated tests in the target project. See [official assertions](https://playwright.dev/docs/test-assertions#soft-assertions) and [official locators](https://playwright.dev/docs/locators#locate-in-shadow-dom).

## Combinations and download

- **Clear website interactions**: Design of Everyday Things owns the control map; Microinteractions owns feedback within that map. The downloadable `clear-website-interactions` pack includes fixed upstream files, both MIT license texts, provenance, a staged workflow and a CLAUDE.md adapter. These are sequential responsibilities, not simultaneous independent design directors.
- **Website interaction QA**: Microinteractions supplies a state contract; Playwright Best Practices translates it into tests; Verification Before Completion reports actual results. This is a recipe requiring project/browser setup, with no ZIP or runtime compatibility claim.

Find both by title on the website's Combinations page. The download is inert instruction text; it does not install dependencies or register a client. Review files in a staging folder and merge CLAUDE.md with existing instructions.

## Candidates held back

| Candidate | Decision and reason |
|---|---|
| UI UX Pro Max | Already in the library. The topic search found 145,419 repository stars in this snapshot; preserve its existing catalogue pin and dated observation rather than silently updating unrelated evidence. |
| Wondel high-perf-browser | Defer pending a correction/adapter. Useful transport and loading guidance, but its suggested Lighthouse CI INP assertion is not a substitute for field INP. Check [Web Vitals measurement guidance](https://web.dev/articles/vitals) and [lab versus field data](https://web.dev/articles/lab-and-field-data-differences). No performance improvement was measured here. |
| Wondel refactoring-ui | Defer: overlaps current design owners and its large-text contrast example oversimplifies the size requirement. Existing frontend-design, Impeccable and Web Design Guidelines remain available. |
| Wondel create-website | Defer: journey orchestrator referencing sibling skills; copying one folder is incomplete. Existing combinations already define website handoffs. |
| Agentic SEO Skill | Defer: root instructions and README reviewed. Installer, script dependencies, SEO claims and specialist files need a deeper scoped audit before inclusion. No installer was run. |
| TestDino Playwright Skill | Alternative watchlist candidate. Root README/index reviewed; individual sub-skills were not deeply reviewed. Avoid adding two overlapping testing suites in this round. |
| docmd | Website/documentation compiler rather than a skill; no SKILL.md in the fixed repository tree. Keep as tooling research, not a skill card. |
| Agent harnesses, registries and unrelated domains | Excluded by website-development scope, regardless of stars. A topic tag alone does not establish task fit. |

## Reproduce this research

1. Start at [GitHub's ai-skills topic](https://github.com/topics/ai-skills), sorted by stars. Capture a timestamp because rankings change.
2. Query GitHub repository search with `topic:ai-skills archived:false`, sorting by stars descending and limiting to 50. This API query excludes archived projects and may differ from the topic page. This run returned 2228 matches; only the first 50 were triaged from metadata.
3. Compare candidate repositories and skill paths against `catalog/skills.json`. Separate actual skills from frameworks, registries and general tools.
4. Deepen into five relevant repositories: Wondel, Currents, TestDino, Agentic SEO and docmd. Resolve default-branch HEAD to a full commit, read the README/license and inspect the recursive tree. Read chosen SKILL.md files and selected linked references as data. Do not run install commands, hooks or scripts.
5. For accepted folders, reject non-regular blobs and verify every file's Git blob hash. Preserve root license hashes. Record Codex claims separately from evidence of runtime behavior.
6. Record include/defer reasons and actual uncertainties. Add entries only after review; regenerate the website and validate hashes/tests.

The exact search response, repository metadata, commit trees and selected-file verification inventories are preserved under `reports/evidence/2026-11-05-ai-skills-topic/`. The adjacent JSON report is the machine-readable decision log. Full selected instruction bytes remain at their immutable upstream links and in the reviewed design pack; the evidence folder does not claim every reference example was individually validated.

For future manual collection, `research/queries-website-topic.json` provides topic and task refinements. Only the top-50 broad topic query was executed for this report; the refinements are future searches, not claimed results:

```sh
python3 report.py --config research/queries-website-topic.json --output reports/YYYY-MM-DD-website-topic
python3 skills.py list --category website-ui
python3 skills.py show microinteractions
python3 bundles.py show clear-website-interactions
```

After reviewing sources, installation can use the library's copy-only installer:

```sh
python3 skills.py install microinteractions --dest .agents/skills --reviewed
python3 skills.py call microinteractions "Review copy feedback and failure states"
```

The installer also copies the new entries' pinned root license into `LICENSES/upstream/` inside each installed skill. Installation copies files; it does not run them. The call command prints a prompt. Start a new Codex session after installation; upstream-claimed support still needs your own runtime verification. For Claude, use the pack's CLAUDE.md file-based adapter rather than assuming native slash-command discovery.

## Limits

This is a bounded, star-ranked sample of public, topic-tagged repositories, not an exhaustive survey. Smaller projects, repositories outside this topic and non-English results may be missed. Install counts were not independently captured for these entries; the skills.sh leaderboard was consulted only for discovery context. Popularity does not prove safety, quality or compatibility. No upstream skill execution, website performance benchmark, full accessibility audit or end-to-end Codex/Claude skill trial was performed.
