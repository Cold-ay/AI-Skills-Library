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
