# Install directly with Codex

AI Skill Library publishes ordinary GitHub skill directories under `installables/codex/skills/`. Eligible skill and combination cards have an **Install with Codex** button. It copies a request for Codex's built-in `$skill-installer`; paste it into Codex to review and install. Clicking the website button does not open Codex, copy files or submit a chat message.

The initial native distribution includes the same nine standalone skills and five combination wrappers as Skill Bridge. It preserves pinned original skill files and their license notices. Reference-only entries and recipes requiring upstream setup are excluded. ZIP installers remain available for other hosts and offline installation.

## Use it

- On a skill or combination card, click **Install with Codex**, then paste into Codex. This direct card action uses the built-in installer's personal destination.
- For project scope, open [Skill Bridge](https://ai-skill-library.vercel.app/#install), choose Codex and **One project**, then copy the native installer request. It asks Codex to substitute the actual absolute current-project path and use `--dest <project>/.agents/skills`.
- Codex reviews the pinned source and license notices, checks all destination folders, and calls its bundled `install-skill-from-github.py` helper.
- After Codex confirms the installed folders, use the requested `$skill-name` or `$combination-name` on your next turn. If your client has not discovered it, start a new session and check the skill picker. This distribution does not validate upstream task behavior merely by copying files.

The bundled installer checked for this implementation defaults to `$CODEX_HOME/skills`, normally `~/.codex/skills`. This is distinct from Skill Bridge's explicit personal `.agents/skills` destination. Respect the installed helper's current defaults and configured CODEX_HOME. Project installation uses the documented `.agents/skills` location. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills) and the bundled `$skill-installer` instructions in your Codex installation.

## Combination example

The generated request for Clear Website Interactions passes all three paths in one helper invocation:

```text
--repo Cold-ay/AI-Skills-Library
--ref d396aceec262c23b199f953852046bc2ebf19649
--path installables/codex/skills/design-everyday-things installables/codex/skills/microinteractions installables/codex/skills/combination-clear-website-interactions
```

These are helper arguments, not a standalone shell command. `$skill-installer` locates its own bundled helper. Project-scope requests add a properly quoted, real `--dest` path. Members and wrapper must share the same destination skills root so `../<member>/SKILL.md` handoffs work. Dependencies are listed explicitly; the built-in installer does not discover them from the wrapper.

After installation:

```text
$combination-clear-website-interactions Review the skill discovery and onboarding journey.
```

A standalone Microinteractions installation lists only `installables/codex/skills/microinteractions`, and is invoked as `$microinteractions <your task>`.

## Conflicts and limits

The real bundled installer copies multiple folders sequentially. It refuses an existing destination as it reaches it; it does **not** promise whole-request rollback. The copied request therefore asks Codex to check **all** destinations before invoking it and stop on any existing skill. A filesystem error can still leave a partial installation; Codex must report the exact outcome rather than claim automatic rollback.

Installation copies source files and license notices. It does not run upstream scripts or install runtime dependencies. Do not replace existing skills, alter client settings or infer support for reference-only projects. If the built-in installer is unavailable, the request asks Codex to explain that requirement rather than download and execute a substitute installer. Local skills do not automatically sync to a cloud account or remote worker.

## Maintainer publication

```sh
python3 codex_export.py --reviewed
# Review and commit codex_export.py and installables/codex/ before pinning the release.
python3 codex_export.py --publish-ref <full-commit-containing-the-export>
python3 site/build.py
```

Commit the exported tree first. Then pin that commit in the website registry and commit the website changes. This avoids a self-referential commit hash. Push the resulting history so the pinned export commit is reachable on GitHub before users invoke the request.

- `installables/codex/index.json` records every exported path/hash, source pin and workflow definition.
- `site/dist/codex-installer.json` records the immutable repository commit, per-choice paths and export-index SHA-256.
- `--publish-ref` inspects `git archive` for the chosen commit and rejects a committed inventory or local-tree mismatch. Mutable branch names are rejected.
- The website build rejects a stale registry or source hash drift. It reads local checked-in metadata without needing remote access or older Git objects in a shallow CI checkout.
- Rebuilds preserve edited/unmanaged files by stopping instead of overwriting them. Unchanged reviewed upstream bytes are shared across combinations; no duplicate member installation is required within one request.

## Validation scope

Tests compare every generated source/license byte with the reviewed archive payloads, verify explicit combination membership and sibling references, check immutable request generation and both scopes, and exercise the installed Codex helper's real path validation/copying into a temporary directory with the checkout source supplied locally. This is installer compatibility testing, not an agent skill execution test.

All five generated combination wrappers pass the bundled skill frontmatter validator. That validator flags extra upstream `version` metadata in Nothing Design and `compatibility` metadata in Scientific Critical Thinking; those pinned originals are preserved rather than silently rewritten. A validator warning about metadata is not evidence that a task workflow has been run successfully or failed inside Codex. Native skill-session behavior remains untested.

The published network smoke check also passed using the actual bundled installer with an immutable GitHub commit and temporary destinations: one standalone skill and its three-folder combination, with all 29 copied files matching the source. See [the result](evidence/codex-native-installer-smoke.json). This proves the tested download/install path, not runtime quality of the installed skills.
