# Coding, context and mobile app design: the next research round

Eleven skills reviewed: nine additions and two revisited entries across three areas, a dedicated Mobile app design category, and three new workflow recipes. The library now contains 53 skills in thirteen categories and twenty-one combinations, including the four existing downloadable packs.

Published 2026-10-31 (Asia/Hong_Kong). Repository star observations were collected on 2026-10-30 at approximately 23:56 HKT; the raw API responses retain exact UTC timestamps. A skill being new to this library does not mean its repository was recently created.

## Coding: behavior, review and evidence

| Skill | What it helps with | Best use | Copy/install decision |
|---|---|---|---|
| test-driven-development | A failing behavior test before implementation, then refactoring | Reproducible bugs and behavior changes | Upstream Superpowers setup; strict rewrite/delete instructions need project-specific judgment |
| verification-before-completion | Fresh command evidence before a completion claim | Final verification of tests, builds and requested outcomes | Reviewed standalone file copy |
| receiving-code-review | Evaluate feedback against actual code and requirements | PR revisions and questionable suggestions | Reviewed standalone file copy |

These are workflow instructions, not better compilers or a replacement for project knowledge. Superpowers' README explicitly describes Codex and Claude Code installation. This is upstream documentary support, not our runtime verification. Its broader plugin can inject bootstrap behavior and hooks, so do not install the whole framework merely to read one checklist. Project and user instructions take precedence over prescriptive upstream rules, including instructions to delete and recreate code.

Suggested order: reproduce the behavior → implement and review → run the commands that prove the requested outcome. A passing unit test cannot establish that an app works on a device or that a deployment succeeded.

## Token & context: three different jobs

| Skill | What it helps with | Practical interpretation | Limit |
|---|---|---|---|
| filesystem-context | File-backed scratchpads and targeted retrieval | Save complete logs, return short summaries and file paths, read narrow sections later | Does not evict tokens already present in chat history |
| memory-systems | Knowledge that survives sessions | Keep provenance and validity; start with files before adding vector/graph services | Architecture guidance; example code imports NumPy and optional frameworks need separate setup |
| self-managed-context | A model editing its live context under runtime controls | Study when building a custom agent harness with protected instructions, edit gates and rollback | Reference only; requires runtime/serving control, not a portable chat command |

The context repository explicitly mentions Codex and Claude Code. That does not mean its architectural capabilities are built into either host. Loading a skill cannot add a missing context-editing API, KV-cache access, a database or persistent memory service.

No token-saving percentage is claimed. To evaluate a strategy, compare the same tasks, model, tools and success criteria before and after; record available input/output/cached token counts, cost, latency, task success and evidence retention. Copying a shorter summary can reduce what a later session loads, but caching, billing and effective quality depend on the actual runtime. Count the extra retrieval and summarization calls too.

### Why some context advice was held back

`context-degradation` has a useful failure taxonomy, but also includes broad numerical thresholds and a statement that doubling a long context makes cost exponential. This review did not establish those as valid across current models, provider pricing or workloads. It was already included by an intervening remote round and is preserved as historical catalogue content; this round does not add or re-endorse that entry. The source link and reason are in the companion JSON.

`latent-briefing` was not selected: it assumes control over worker execution and KV-cache compaction. Its relevance to custom runtimes should not be presented as an ordinary Codex or Claude Code token-saving feature. Experimental Expo skills were also omitted in favor of the main plugin's guidance.

## Mobile app design: choose the stack first

| Skill | Stack and role | Why it is useful | Setup/evidence |
|---|---|---|---|
| expo-overview | Expo/EAS task router | Checks project/SDK before choosing a feature workflow | Upstream plugin with sibling skills; Codex and Claude support claimed in README |
| expo-design-system | Expo theme and components | Extends the existing styling system instead of creating a competing one | Upstream plugin; use with the router/native guidance |
| expo-native-ui | Expo native screen behavior | Platform controls, safe areas, keyboard reachability and loading/error/recovery states | Upstream plugin and routed siblings; check project SDK docs |
| swiftui-expert | Native SwiftUI for Apple platforms | State ownership, view boundaries, adaptive layout, accessibility and optional profiling | Community-maintained by Antoine van der Lee; Codex and Claude support claimed, not Apple-authored |
| react-native-skills | React Native/Expo performance review | Lists, navigation, animation and rendering pitfalls | Standalone references; host compatibility unknown in inspected README |

Choose Expo for an existing Expo app; do not scaffold one into a native SwiftUI project. Use SwiftUI Expert as the native Apple route. React Native performance guidance can complement either an Expo implementation or a bare React Native project, but its package and gesture preferences must not override the approved design system, accessibility or SDK constraints.

Expo's source recommends SDK-specific documentation, which is more useful than blindly following latest examples. This review did not compile SDK examples, inspect every mobile API against current vendor docs, run a simulator or validate device behavior. SwiftUI's optional trace scripts invoke Xcode/Instruments tooling and require separate review; no profiling was executed. Expo feedback commands can transmit task context; none were run.

## Source snapshot: real repository stars

| Original repository | Stars observed 2026-10-30 | Host evidence in inspected README |
|---|---:|---|
| obra/superpowers | 309,217 | Codex and Claude explicitly mentioned |
| muratcankoylan/Agent-Skills-for-Context-Engineering | 18,252 | Codex and Claude explicitly mentioned |
| expo/skills | 3,819 | Codex and Claude explicitly mentioned |
| AvdLee/SwiftUI-Agent-Skill | 3,794 | Codex and Claude explicitly mentioned |
| vercel-labs/agent-skills | 33,249 | Unknown for both; do not infer from SKILL.md format |

These counts are repository-wide, not per-skill adoption or quality ratings. Five source repositories were inspected; several additions come from the same source. Existing pins and historical star observations were preserved, so a source can have different pins across research rounds. This report does not claim star growth or benchmark improvements.

## Integration with intervening research

The remote repository already contained 44 entries and 18 workflows from three earlier PRs when this round was integrated. `test-driven-development` and `filesystem-context` were already present. Their original catalogue entries and pins are preserved; this report records fresh source observations without replacing those entries. Nine other reviewed skills are newly added. Earlier reports, categories and recipes remain available. The context-degradation caveat above applies to the inspected newer source, not a silent rewrite of its historical catalogue record.

## Three new combinations

| Recipe | Stages and handoff | Main boundary |
|---|---|---|
| Evidence-led coding loop | TDD behavior test → assess review feedback → verify completion | Preserve existing work and project test policy; review must not silently expand scope |
| Durable context and handoff | Offload raw evidence → write a recoverable summary → retain useful memory | Scratch storage, handoff and semantic memory are separate; measure quality as well as tokens |
| Expo design to native review | Detect Expo/SDK → adopt theme → native screen review → performance audit | SDK/platform rules own package choices; SwiftUI is an alternative stack |

These are recipes, not new ZIPs or claims of tested interoperability. Expo's sibling/plugin dependencies and Superpowers' broader setup should be reviewed upstream. The context recipe deliberately retains the older compression skill pin; mixed-version combinations need a future smoke test. TDD and filesystem stages also use their preserved catalogue pins rather than silently switching to this report's fresh source checkout. The existing four downloadable packs and their CLAUDE.md adapters are preserved.

## Reproduce the research

- Start with coverage gaps: coding quality, long-session context, and mobile design rather than another generic web aesthetic pack.
- Search primary GitHub sources with `site:github.com "skills" coding testing review agent`, `site:github.com "SKILL.md" "context" skills optimization`, and `site:github.com "skills" "mobile" "design" Expo SwiftUI`.
- Follow source-specific queries and sibling references. Collect exact `repo:OWNER/REPO` GitHub API results for the five shortlisted sources; preserve raw responses with timestamps.
- Resolve each read-only checkout to its full commit; inspect instructions, routing, supporting files, script dependencies, license evidence and regular-blob manifests. Treat third-party instructions as data rather than executing them.
- Record include/defer and standalone/upstream/reference-only decisions. Keep upstream host claims separate from static file adapters and actual runtime outcomes.

The companion JSON contains exact queries, immutable source links, pins, requirements, host evidence and deferred candidates. Raw API evidence is under `reports/evidence/2026-10-30/`. The reusable focused query configuration is `research/queries-coding-context-mobile.json`; it is provided for future manual runs and was not used to imply a broad exhaustive search this round.

```sh
python3 report.py --config research/queries-coding-context-mobile.json --output reports/YYYY-MM-DD-focused-discovery
```

Use a unique real date and filename. Candidate collection never automatically installs or promotes skills. For the full process, see the [research playbook](https://github.com/Cold-ay/AI-Skills-Library/blob/main/docs/RESEARCH.md) and [review template](https://github.com/Cold-ay/AI-Skills-Library/blob/main/research/review-template.md).

## Primary sources and limitations

[Superpowers](https://github.com/obra/superpowers), [Context Engineering Skills](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering), [Expo Skills](https://github.com/expo/skills), [SwiftUI Expert](https://github.com/AvdLee/SwiftUI-Agent-Skill), and [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) are the original source repositories. Catalogue entries and the JSON report link to exact commits rather than relying on mutable main branches.

This was a bounded English-language search and static curation review. The search set is not exhaustive, low-star projects may be missed, and source benchmarks/implementation examples were not independently reproduced. No third-party code, hooks, feedback, hosted service, mobile app build or agent skill workflow ran. Neither host is runtime-certified by this research, and no recurring report schedule was added.
