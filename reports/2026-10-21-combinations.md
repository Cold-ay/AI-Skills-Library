# Beyond individual skills: workflows you can reuse

Seven additions, six proposed combinations, four downloadable packs, and a repeatable research method. Observed 2026-10-21. This is a targeted expansion, not an exhaustive ranking. The original discovery snapshot and video review remain unchanged.

## New skills and their purpose

| Skill | Useful for | Repository stars | Codex evidence | Packaging decision |
|---|---|---:|---|---|
| agent-browser | Browser automation and exploratory testing | 44,368 | Upstream claim | Reference only: CLI-served instructions and Chromium required |
| composition-patterns | Composable React APIs and component boundaries | 32,753 | Unknown in inspected README | Standalone skill; combination recipe only |
| research-lookup | Gather a scholarly evidence packet | 53,459 | Upstream claim | Upstream setup: Parallel CLI/authentication and network |
| literature-review | Search protocol, screening and citation checks | 53,459 | Upstream claim | Upstream setup: Python, network and optional publishing services |
| scientific-critical-thinking | Evaluate bias, methods and claim strength | 53,459 | Upstream claim | Core text appraisal copy; optional figure generation excluded |
| gsap-react | React-scoped animation and cleanup | 16,731 | Upstream claim | Standalone instructions; runtime packages installed separately |
| gsap-timeline | Labels, sequence timing and motion composition | 16,731 | Upstream claim | Standalone instructions; requires GSAP runtime |

Stars describe whole repositories, not individual skills. GSAP counts reuse the video review's same-day snapshot. The three scientific skills share one repository count. Raw API metadata, exact queries and pinned source URLs are preserved in the companion JSON and evidence directory. No third-party scripts, service calls or Codex workflows were executed in this review.

## Proposed combinations

| Workflow | Stages | Deliverable | Availability |
|---|---|---|---|
| React motion studio | GSAP core → timeline → React lifecycle | Scoped React animations with cleanup | ZIP |
| Industrial interface + motion | Nothing design → GSAP core | A deliberate monochrome interface with restrained motion | ZIP; Nothing's Codex compatibility unknown |
| Article to presentation | Beautiful Article → Web Video Presentation | Editorial article and a separate scene-based presentation | ZIP; frontend dependencies and Chinese source instructions |
| Evidence to editorial report | Scientific Critical Thinking → Beautiful Article | Evidence appraisal table, then a traceable web article | ZIP; provided sources, no retrieval service |
| React architecture review | Composition Patterns → React Best Practices | Component API plan followed by a performance review | Recipe; incomplete redistribution license evidence |
| Scholarly research pipeline | Literature Review → Research Lookup → Critical Thinking | Search protocol, bounded packet and critique | Recipe; service authentication and sibling dependencies |

“Together” means a staged workflow with a defined owner and handoff. It does not mean loading every instruction at once. For example, the evidence reviewer owns claim strength, while the article designer owns presentation; the designer must preserve uncertainty. All combinations are static proposals, not tested end-to-end Codex integrations.

## What is in a download?

Each ZIP contains unchanged pinned skill files, supporting assets, upstream MIT license texts, a full manifest with source commits and file hashes, and a library-authored `combination-*` orchestration skill. Archive SHA-256 checksums are displayed in the website and saved in the download index. No installer or dependency manager runs during packaging or extraction.

Review a ZIP in a clean staging directory, then copy its `.agents/skills` folders to the project without overwriting an existing installation. In a new Codex session, explicitly invoke the combination, for example `$combination-react-motion Build a reduced-motion-aware hero animation`. Runtime packages and optional services are not included. Scripts inside upstream folders remain inert files until someone chooses to execute them.

## How this research was performed

- Start with missing task coverage: browser QA, research evidence quality and React motion lifecycle.
- Search primary GitHub sources using `site:github.com skills browser agent-browser vercel-labs` and `site:github.com skills research scientific K-Dense`.
- Verify original repositories through exact `repo:OWNER/REPO` GitHub API searches. Preserve responses rather than copying stars from promotional lists.
- Read fixed Git checkouts: README, chosen SKILL.md, linked assets, dependency instructions and license. Add complementary GSAP skills from the earlier pinned original source.
- Separate text-only/core use from external runtimes, paid APIs, hooks and sibling-skill dependencies. Keep agent-browser, Research Lookup and Literature Review out of standalone downloads.
- Record include/defer decisions and build only the packs with complete standalone file and license evidence. Never execute a candidate's installer to decide whether it is trustworthy.

For reuse, the [research playbook](https://github.com/Cold-ay/AI-Skills-Library/blob/main/docs/RESEARCH.md) includes search lanes, screening gates, limitations, manual collector commands and a review template. The collector's configurable queries are in `research/queries.json`. Searches do not auto-promote candidates or schedule future runs.

## Evidence and limitations

[Agent Browser source](https://github.com/vercel-labs/agent-browser), [Vercel Agent Skills source](https://github.com/vercel-labs/agent-skills), [Scientific Agent Skills source](https://github.com/K-Dense-AI/scientific-agent-skills), and [GSAP source](https://github.com/greensock/gsap-skills) are the original upstream repositories. The companion JSON records exact immutable links for each addition.

Upstream support claims are documentary evidence only. `hidden` metadata and Claude-style tool names in some sources may behave differently in Codex. Critical Thinking's optional schematic workflow refers to a sibling skill that is excluded; the included workflow explicitly limits use to core appraisal. A retrieval count is not proof of bibliographic identity or claim support. English queries and bounded result sets have coverage bias, and star growth cannot be inferred from one snapshot.
