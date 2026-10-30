# Reusable AI skills research playbook

Goal: find workflows that solve a stated task, record why they are useful, and preserve enough evidence for another person to repeat the review. Popularity orders the inspection queue; it does not prove quality, safety, compatibility or star growth.

## 1. Define the question

Write the task, inputs, expected output, host (such as Codex), allowed services, budget and a concrete success check. Example: “Build a React animation that cleans up on unmount and respects reduced motion.” Choose one of website/UI, mobile app design, video, coding, context efficiency, research/automation or skill engineering. List existing skills so duplicates are not mistaken for new findings.

## 2. Search through complementary lanes

- Popular maintained collections: `"agent skills" stars:>=50 archived:false pushed:>=YYYY-MM-DD`.
- Emerging projects: `"codex" "skills" stars:>=20 archived:false created:>=YYYY-MM-DD`.
- Skill-format discovery: `"SKILL.md" stars:>=100 archived:false pushed:>=YYYY-MM-DD`.
- Task-specific search: `site:github.com skills browser agent-browser vercel-labs` or `site:github.com skills research scientific K-Dense`.
- Provenance check: `repo:OWNER/REPO` through GitHub repository search, then the upstream README, SKILL.md, file tree, license and commit.
- Follow references and sibling skills from credible originals. Record this as a different discovery route from a broad search.

GitHub repository search searches repository metadata/README according to GitHub's search semantics; a query containing SKILL.md does not establish that such a file exists. Inspect the pinned tree. Search is bounded, ranking changes, and these English queries miss other languages and smaller projects. Add low-star and language-specific searches for your domain rather than declaring the results exhaustive.

## 3. Collect a manual snapshot

```sh
python3 report.py --config research/queries.json --output reports/2026-10-22-my-research
```

Change the date/name for each run. Configuration sets the time window, query strings and maximum results per query; `{since}` expands to the window start. The collector adds the existing catalogue watchlist, deduplicates repositories, and records stars, dates, source commit, skill paths, errors and unknown compatibility. It never installs candidates or edits the catalogue. Optional `GH_TOKEN` can raise API limits; keep it in the environment, never reports. A nonzero exit with reports means collection was partial: inspect errors before interpreting the results. Existing snapshots are not overwritten.

The 2026-10-21 expansion used targeted web searches, three exact-repository API searches and read-only Git checkouts rather than running the full collector again. Raw API results are in `reports/evidence/2026-10-21-combinations/`; the dated JSON records queries, additions and deferrals. GSAP stars reuse the earlier same-day snapshot, not a fresh observation. No growth claim is made.

## 4. Review a fixed version

Inspect sources as data. Resolve HEAD to a full commit and keep regular-blob file manifests. Read the complete chosen SKILL.md, linked references, scripts, sibling references, hooks and license text. Do not run cloned installers, hooks or scripts during discovery. Root licenses and notices can live outside the skill folder. Record any per-skill exceptions.

Apply these gates in order:

| Gate | Pass evidence | Otherwise |
|---|---|---|
| Task fit | Specific inputs, outputs, useful steps | Reject duplicate or vague prompts |
| Provenance | Original maintainer, fixed source and file hashes | Hold for source verification |
| License | Explicit redistribution terms, notices and exceptions | Link/reference only; no ZIP |
| Dependencies | Host tools, versions, sibling skills, credentials, data destinations | Upstream setup or recipe only |
| Codex support | Pinned official evidence or explicit upstream claim | Unknown; do not infer from format |
| Runtime quality | Disposable-project test, host/version, input/output and failures | Static review only |
| Combination fit | Separate responsibilities, input/output handoffs, conflict owner | Keep separate or make sequential |

Existing status vocabulary is `verified-static` (official documentary evidence), `upstream-claimed`, and `unknown`. None means runtime tested. A true runtime result needs a separately recorded reproducible trial; current schema deliberately disallows claiming that result without changing the evidence model.

## 5. Make a decision, with reasons

Copy `research/review-template.md`. Record include/defer/reject, the reason, exact evidence and uncertainty. Avoid a single invented quality score. Compare new observations with earlier snapshots for star growth only when both timestamps and repository identity match. Add selected entries to `catalog/skills.json`; others stay in the report. Preserve earlier reports even when a conclusion changes.

For combinations, define task, stage order, skill owner, handoff artifact, prerequisites and conflicts. A design director and a second design director often compete; a designer followed by an animation specialist has clearer boundaries. Downloadable packs require standalone members, verified license files and all pinned assets. Service-based skills remain recipes until their setup has been reviewed. Optional services must not become hidden mandatory dependencies.

## 6. Validate and publish deliberately

```sh
python3 skills.py validate
python3 bundles.py list
python3 -m unittest discover -s tests -v
python3 site/build.py
```

Review the diff and generated articles. Test the site's search, workflow links, ZIP contents and invocation text. Building an archive tests packaging, not the behavior of the upstream skills. Add a dated report describing findings, omissions and collection failures. No recurring schedule is configured.

## Focused round: published 2026-10-31

The coding/context/mobile round uses `research/queries-coding-context-mobile.json` for future collection. Its actual method was targeted primary-source web search, exact repository API lookups and pinned Git review; see `reports/2026-10-31-coding-context-mobile.json` for the complete query and decision log. Observations occurred at 23:56 HKT on 2026-10-30; the publication date is 2026-10-31. Preserve this distinction when comparing snapshots.

For context skills, distinguish file offloading, session compaction, persistent memory and live runtime context editing. Never turn benchmark-specific thresholds or architecture proposals into universal savings claims. For mobile design, detect Expo/React Native versus native SwiftUI, check the project SDK/OS target and note device/simulator checks not performed. Claude and Codex support claims must be attributed separately; unknown evidence stays unknown.
