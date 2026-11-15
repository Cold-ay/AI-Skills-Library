# Validation record — 2026-10-21

- Initial remote clone was empty; no existing tracked files were replaced.
- Python unittest: 13 tests passed. Offline tests cover installation integrity/failure paths and report behavior.
- Catalogue validation: 12 entries, all six requested categories.
- CLI smoke: list, show, call and validate. `call react-best-practices` produces `$vercel-react-best-practices`, using the upstream frontmatter name rather than assuming the folder name.
- Live installer smoke: downloaded pinned `anthropics/skills` frontend-design files into a disposable workspace destination; all Git blob hashes matched. No skill instructions or scripts were executed, and the skill was not activated.
- Live report collection: 11 repositories collected, 18 repository HTTP errors. The initial dated report is explicitly incomplete; collector exited 1. This demonstrates failure visibility, not a successful scheduled run.
- Live source review: GitHub metadata, commit/tree manifests, selected SKILL.md files and READMEs inspected for seven sources. Deprecated openai/skills entries were retained only as migration references.
- No end-to-end Codex execution of third-party skills, paid API calls, or live GitHub Actions run is claimed. No report schedule is configured.

## Current revision

Documentation is now English. The weekly report workflow template and report PR template have been removed at the user’s request. Existing snapshot data remains preserved. Nine video-related entries have been added, bringing the catalogue to 21. No downloaded skill scripts, launchers, hooks or instructions have been executed.

## Website checks

- 18 unit tests passed, including raw HTML/script escaping, unsafe link rejection, Markdown code/tables, repository-driven article generation and absence of a scheduled report workflow.
- JavaScript syntax check passed. Site build generated 2 reports and 21 skill records.
- Local browser checks passed: video review navigation, video category filter, keyword search, empty results, evidence disclosure, invocation copy, draft save, draft restoration after reload and Markdown export.
- Layout was visually inspected in the local browser. Responsive styles and reduced-motion handling are included; no physical mobile-device test is claimed.
- Website drafts use browser storage, not a server database. Publishing a new report requires adding its Markdown to the repository and rebuilding/redeploying.

## Deployment

Sites private deployment succeeded on 2026-10-21. Deployed source commit: 061aa1bb430b95b47a282f800026921f49f38a5f (the separate Sites source repository). URL: https://ai-skills-fieldnotes.spicy-dog-4235.chatgpt.site

## AI Skill Library redesign template

The current redesign is local-only and not deployed. It applies the repository’s Frontend Design skill and current Vercel Web Design Guidelines. Existing 18 tests and JavaScript syntax validation pass. Browser checks cover task switching, category navigation, shareable search state and reload persistence. Current branding is AI Skill Library. Vercel static configuration is prepared for later user deployment; no Vercel linking, deployment or Git push was performed for this revision.

## Combinations and research expansion

- Current catalogue: 28 skills, six combinations, four downloadable ZIPs and three articles.
- 24 unit tests passed. New tests verify bundle member/catalogue agreement, every upstream Git blob hash, license hashes, SHA-256 manifests, non-executable file modes, deterministic ZIP bytes, corrupt-download rollback and overwrite rejection. Configurable discovery limits and query substitution are covered.
- Browser preview verified workflow search, requirements expansion, a real React motion ZIP download and navigation to the linked individual skill.
- Research used public primary-source searches, preserved GitHub API metadata and fixed Git checkouts. No newly discovered scripts or skill workflows ran. Package validation does not establish end-to-end Codex compatibility.
- The earlier Vercel preparation note above is historical. The production site is now Git-linked at `https://ai-skill-library.vercel.app`; pushes to main trigger its existing deployment integration.

## CLAUDE.md adapter

- All four ZIPs now include a library-authored root CLAUDE.md adapter; original upstream skill bytes and licenses are preserved.
- 26 unit tests passed, including adapter content, explicit Claude file-path prompts and archive manifest/checksum coverage. CLI `bundles.py call react-motion --agent claude` was verified.
- Browser preview verified host selection switches the displayed prompt and setup instructions to Claude Code. Compatibility badges remain explicitly Codex evidence. Claude Code itself was not executed; this is file-based integration support, not a runtime certification.

## Research round published 2026-10-31

- Reviewed 11 skills from five original repositories; added nine and preserved two already catalogued entries, preserving all earlier catalogue records and reports. Raw star observations retain 2026-10-30 UTC timestamps.
- Added Mobile app design as the thirteenth category, and three recipe-only combinations. Four existing downloadable archives and their hashes remain unchanged.
- 32 unit tests passed after integrating the remote research updates. New checks compare every added star count and repository identity with preserved API responses, verify source pins and host evidence boundaries, and keep plugin/custom-runtime entries out of standalone copying.
- Browser preview verified Mobile app design filtering, SwiftUI search within that category, and the dated article with comparison tables. CLI category filtering and combination listing passed.
- Static inspection only: no third-party code, source feedback commands, mobile builds/simulators, benchmark reproduction or end-to-end agent workflow execution. No token savings or runtime certification claimed.

## Sorting and skill-purpose UI

- 33 Python tests and four Node tests passed. Sorting checks cover numeric star ordering, deterministic ties, alphabetical/date/evidence ordering, invalid modes and source-array preservation. Purpose filtering tests retain every stage of a matched workflow.
- Browser preview verified descending/ascending star order within a category, URL restoration after reload, category-based combination filtering, and separate purpose/workflow-role fields.
- Added content hashes to asset URLs after observing a stale stylesheet during visual verification; the build/test checks these against actual asset bytes.

## MCP connection — 2026-11-05

- Added a local stdio server using the official MCP Python SDK 2.3.0 in an optional isolated environment. Eight read-only tools, three resource routes and two task prompts expose catalogue metadata, ordered combinations, bounded report/source reads and provenance.
- 46 Python tests passed with the MCP environment, including an actual stdio subprocess launched from another working directory. The original Python 3.9 environment passes 44 tests with two SDK protocol tests skipped when the optional dependency is absent. Four JavaScript tests passed.
- Live SDK client/server smoke test discovered all tools/prompts, read the overview, retrieved React motion stages and fetched GSAP core at its catalogue commit. Its Git blob hash matched. No third-party scripts, installers, hooks or agent workflows ran.
- Tests exercise unknown IDs, manifest restrictions, traversal, report symlinks, binary/oversized content, hash mismatch, page bounds, metadata-only search and absolute-path configuration generation.
- Client configuration is generated but host/account settings are not edited. The static Vercel website is not a remote MCP endpoint. No specific Codex/Claude desktop UI connection or full skill runtime certification is claimed.

## MCP introduction and setup wizard — 2026-11-05

- Added an MCP main-navigation section and home-page callout, preserving the old connection route. Visual explanation and interactive task examples are based on current catalogue data; they do not simulate a successful live connection.
- Browser preview verified task switching, Claude/Windows setup selection, step navigation, command copy feedback and the final request step. Five JavaScript tests cover sorting/filtering and platform/client-specific setup commands; 46 Python tests continue to pass.
- Windows commands use an explicit PowerShell relative executable path. Full technical setup and the local-stdio limitation remain available. No client settings or server capabilities were changed by this UI update.

## Website topic research — 2026-11-05

- Preserved all 53 prior skill entries and 21 prior combinations unchanged; added three reviewed website skills, a licensed design pack and a QA recipe. Current totals: 56 skills, 23 combinations, five downloadable packs and eight reports.
- New entries have pinned root license manifests; the copy-only installer verifies and preserves their notices. Offline tests cover copied notices, rollback on hash mismatch and unsafe/colliding paths. Existing entries without that optional manifest retain their prior behavior.
- 51 Python tests and five JavaScript tests passed, including evidence/pin cross-checks and archive integrity checks. Website build and git whitespace checks passed. Packaging verification does not establish upstream runtime skill quality.
- The public topic API search is bounded to 50 star-ranked results. Selected instructions were read, references sampled and 77 selected Markdown blobs hash-verified; no upstream installer, script or skill workflow was executed.

## Presentation research — 2026-11-15

- Added six reference-only presentation entries and three recipes; preserved all 56 previous entries and 23 previous combinations unchanged. Current totals: 62 skills, 26 combinations, five existing ZIP packs and nine reports.
- Verified 43 selected reading-file hashes against pinned Git trees. Source modes include ordinary files and executable script blobs inspected as text; none was executed. Reading manifests are incomplete upstream installations.
- 55 Python tests and five JavaScript tests passed. New checks cover original-source identity, aliases, exact stars/commits, reading manifests, output distinctions, installer refusal, missing/AGPL license boundaries and one authoring owner per recipe. Website build, JavaScript syntax and whitespace checks passed.
- No deck was generated, no image backend configured and no exporter or attribution guard run. Test results establish library integrity, not upstream presentation quality or host runtime compatibility.
