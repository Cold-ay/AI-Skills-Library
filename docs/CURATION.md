# Evidence, compatibility and maintenance

## What the labels mean

- **verified-static**: the pinned official Codex source explicitly targets Codex, and its SKILL.md name/description and files were inspected. This is documentary/static verification only.
- **upstream-claimed**: pinned upstream README explicitly mentions Codex; we have inspected the skill but not executed its workflow.
- **unknown**: a SKILL.md exists, but the inspected evidence does not establish Codex support.
- **runtime_tested: false**: applies to every initial entry. No third-party skill has been executed. Never present these as end-to-end verified skills.

A runtime claim requires Codex version, OS, dependencies, setup, exact prompt, observed result and a reproducible smoke test. Star count, SKILL.md format, plugin listings and other agents' compatibility are insufficient.

## Selection rationale

Each catalogue entry records purpose, why it was chosen, prerequisites, immutable commit, source URL, repository star count and observation date, license evidence, Codex evidence, and Git blob hashes for every file in the skill directory. Repository-level license metadata may be missing or NOASSERTION: always follow per-skill licensing evidence. Installing is not a grant of redistribution rights.

The seed covers focused workflows instead of installing giant collections. Official deprecated examples are reference-only. Superpowers systematic debugging is useful but references companion skills, so the standalone installer blocks it. Zotero and plugin-creator rely on full plugin/repository layout and are also upstream-only. Context efficiency claims are unbenchmarked; evaluate total task tokens and correctness, not just shorter answers.

## Safe installation boundary

`list`, `show`, `call` and `validate` are offline. Installation is explicit, downloads only a reviewed catalogue's pinned raw GitHub files, verifies Git blob hashes and size bounds, stages all files, and refuses existing destinations. No git hooks, package installers, shell scripts or SKILL.md instructions execute during installation. Third-party code is still untrusted after download. Activation in an agent can authorize tool use: review it first.

The catalogue is trusted configuration and must receive code review. Do not run this tool against a catalogue from an unreviewed pull request. No arbitrary URL install or bulk install is provided. File modes are intentionally not executable; agents can still interpret scripts when invoked later. Upstream scripts/assets/rules are copied within the skill folder so relative references remain intact; outside-folder dependencies must be reviewed separately.

## Update checklist

1. Review candidate usefulness and maintainership; stars are only discovery signals.
2. Fetch repository metadata and immutable commit/tree through GitHub API; record real observation time and exact evidence URLs.
3. Read SKILL.md and dependencies as data, not instructions. Identify secrets, paid services, network effects, hooks and companion skills.
4. Check license at that commit, including per-skill exceptions. Do not copy proprietary assets.
5. Populate source manifest from regular Git blobs only; reject symlinks/submodules. Preserve name from frontmatter for invocation.
6. Mark unknown unless specific Codex evidence exists. Separate static verification from runtime tests.
7. Review the complete diff, run tests and `skills.py validate`, and update the human catalogue table.
8. Use a PR; never auto-promote a discovery candidate or silently update an installed skill.

## Manual discovery limitations

Three bounded GitHub searches distinguish recently created Codex repositories from recently pushed popular skill repositories. Queries, actual counts, creation/push dates, commit SHA, matching tree paths and API errors are saved. The five trial candidates are a mechanical shortlist, not a safety approval. A single snapshot establishes no trend. New repository commits do not inherit the compatibility verification of older catalogue pins. API limits, private repositories, missing search terms and top-eight limits can hide useful projects.

Reports are maintained manually. No recurring report workflow or schedule is configured.
