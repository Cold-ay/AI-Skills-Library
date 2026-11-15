# Skill Bridge: download, install, use in chat

Skill Bridge is the local installation bridge between AI Skill Library and Codex, Claude Code or Cursor. Open [Use in your agent](https://ai-skill-library.vercel.app/#install), choose a skill or combination, choose your local agent and scope, download the ZIP, review/extract it, and follow the terminal and chatbox steps.

The website cannot write into an agent's local skill folders. A download or copied prompt does not install a skill or send a chat message. The ZIP includes a standalone Python installer; it runs only when you run it locally. No account, API key, local web server, global npm package or repository clone is required. Python 3.9+ is required.

## Codex built-in installer option

When Codex is selected, eligible entries also offer **Install with Codex**. This copies a pinned GitHub-folder request for the built-in `$skill-installer`; the native method does not use the portable ZIP installer. Combinations list every member and wrapper explicitly. Project scope adds `--dest <project>/.agents/skills`; personal scope uses the built-in helper’s default, normally `$CODEX_HOME/skills` or `~/.codex/skills`, rather than the portable installer’s explicit `.agents` path. The built-in multi-path installer is sequential and is not transactional: check all destinations before it runs, and report any partial failure. See [the native installer guide](CODEX-INSTALLER.md).

## Supported local platforms

| Platform | Project skills | Personal skills | Native chat invocation |
|---|---|---|---|
| Codex | `<project>/.agents/skills/` | `~/.agents/skills/` | `$skill-name <your task>` |
| Claude Code | `<project>/.claude/skills/` | `~/.claude/skills/` | `/skill-name <your task>` |
| Cursor | `<project>/.cursor/skills/` | `~/.cursor/skills/` | `/skill-name <your task>` |

These directory and invocation conventions are documented in [official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills) and [Cursor skills](https://prod.cursor.com/help/customization/skills), checked on 2026-11-15. Package structure follows those conventions; upstream runtime behavior in each host is not thereby verified.

Local installation does not sync a cloud account, upload a skill, register an MCP server or configure a remote worker. Install in the environment where the agent actually runs. Platform policies or agent versions may restrict discovery. Start a new chat in the selected project and confirm the skill appears; if native discovery is unavailable, explicitly ask the agent to read the installed SKILL.md. This bridge does not use undocumented deep links to open or submit chat messages.

## Example: one skill

Download `skill-microinteractions.zip`, extract the entire archive, and open a terminal inside `ai-skill-library-skill-microinteractions/`.

Preview the destination and verify the payload without making changes:

```sh
python3 install.py --platform codex --scope project --project "/absolute/path/to/your/project"
```

Review README.md, install.py, PACKAGE.json and the payload. Compare the archive SHA-256 against the website. After review, copy files into the selected project:

```sh
python3 install.py --platform codex --scope project --project "/absolute/path/to/your/project" --reviewed
```

For all local projects, choose personal scope explicitly:

```sh
python3 install.py --platform codex --scope user --reviewed
```

On Windows use `py -3` in place of `python3`, and provide the real Windows project path. The website generates the matching command. For Claude Code or Cursor change `--platform` to `claude` or `cursor`. Do not paste a placeholder project path unchanged.

After installation, open a new Codex chat in that project and use:

```text
$microinteractions Review this form's success, failure and repeated-click feedback.
```

The equivalent native request in Claude Code or Cursor begins `/microinteractions`. A file-based fallback is an explicit request to read the installed SKILL.md; an account's web chat does not automatically see local files.

## Install from the agent chatbox

The website also offers **Copy setup request**. Paste it into a local Codex, Claude Code or Cursor agent with network, filesystem and terminal tools. The request pins the archive URL and SHA-256, asks for archive-path inspection and source review, runs the destination preview, and installs only after those checks pass. Project scope means that agent’s current project; confirm the current project in your session before pasting. User scope means that agent environment’s current user. The agent stops on conflicts, missing permissions or unsuitable code. The website does not send the request, execute it, or claim installation succeeded. Afterward, confirm installed paths and open a new chat to invoke the skill.

## Example: a combination

Download `combination-clear-website-interactions.zip`. Run its installer for the chosen platform and scope. It copies the two original skills and a library-authored `combination-clear-website-interactions` wrapper into the same native skills root. Sibling file references remain valid.

```text
$combination-clear-website-interactions Review the skill download and onboarding flow.
```

Claude Code / Cursor use `/combination-clear-website-interactions`. Unlike the older shared `.agents` ZIP adapters, bridge packages install natively into the chosen host's directory. They do not require editing or replacing a project CLAUDE.md or AGENTS.md. Existing downloads and their CLAUDE.md adapters are preserved unchanged.

## What is available

The initial bridge publishes nine standalone skills and five combinations, derived entirely from the five already-reviewed MIT download packs. The included skills are GSAP Core, GSAP Timeline, GSAP React, Nothing Design, Beautiful Article, Web Video Presentation, Scientific Critical Thinking, Design of Everyday Things and Microinteractions. All five current downloadable combinations are available.

Other catalogue entries remain selectable with clear upstream-setup messaging and an MCP/source route. `installable` in the legacy copy-only CLI is not sufficient proof of a complete licensed portable package. The bridge does not infer missing root licenses, silently drop support files or package reference-only presentation skills. More sources can be added after full dependency, license and packaging review.

## Installer behavior

- Validates the package inventory and SHA-256 of every payload file before changing destination folders. Hashes detect content drift, not publisher authenticity; keep the downloaded installer itself within your source review.
- Preserves original upstream skill bytes and copies pinned license notices inside each skill's `LICENSES/upstream/` folder. The library-authored workflow wrapper removes Codex-specific invocation wording while retaining stage file references.
- Copies passive files only. No payload module is imported and no upstream script, hook, installer, service, dependency or agent is executed. Once you ask an agent to use a skill, normal host/user instructions and permissions still apply.
- Stops if any target skill folder already exists, including symlinks. It does not merge, overwrite or remove existing skills. A combination whose members are already present will also stop: use that existing setup, a separate project, or the MCP workflow after reviewing requirements.
- Rejects path traversal, unsupported Windows names, symlink sources/targets, conflicting paths and size violations. Reserves new target folders exclusively and rolls back those new folders on a copy failure. Empty parent directories may remain.
- Does not modify credentials, client settings, project instruction files or the existing MCP read-only service. Upstream runtime dependencies are separate from the installer.

## Maintainer build and validation

```sh
python3 bridge.py --reviewed
python3 site/build.py
python3 -m unittest discover -s tests -q
node --test tests/test_library_ui.cjs
```

`bridge.py` reads the existing verified archives and source catalogue offline. It verifies original file/license hashes, builds deterministic self-contained ZIPs under `site/dist/bridge/` and writes their index. `site/build.py` verifies each published bridge ZIP checksum before including its metadata. Rebuild bridge archives whenever the installer, source pins, source packages or workflow definitions change. Do not hand-edit the generated archives or index.

Validation covers all three local directory layouts, project/personal scope, dry-run behavior, conflict and hash failures, symlink rejection, rollback, original file/license preservation, deterministic builds and running a standalone packaged installer outside this repository. It does not claim a successful native skill session inside Codex, Claude Code or Cursor.
