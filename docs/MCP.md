# Connect AI Skill Library through MCP

Use one connection to discover curated skills, inspect their provenance and load source instructions on demand. You do not need to copy every skill into your project. A full upstream plugin, runtime, service or package may still be required by an individual skill.

This release is a **local stdio MCP server**. The static website is the catalogue and setup guide; its URL is not a remote MCP endpoint. Clients that only accept HTTPS MCP servers cannot use this local transport. No public HTTP service or client account settings are created by the setup commands below.

## 1. Get the library

```sh
git clone https://github.com/Cold-ay/AI-Skills-Library.git
cd AI-Skills-Library
```

If you already have a checkout, review and pull its updates instead of creating another copy. The server uses the catalogue in that checkout; it does not silently update pins or change installed skills.

## 2. Prepare the optional MCP environment

Use Python 3.10 or newer. The original catalogue CLI remains usable without MCP dependencies.

macOS / Linux:

```sh
python3 -m venv .venv-mcp
.venv-mcp/bin/python -m pip install -r requirements-mcp.txt
.venv-mcp/bin/python scripts/smoke_mcp.py
```

Windows PowerShell:

```powershell
py -3 -m venv .venv-mcp
.\.venv-mcp\Scripts\python.exe -m pip install -r requirements-mcp.txt
.\.venv-mcp\Scripts\python.exe scripts\smoke_mcp.py
```

The environment pins the official MCP Python SDK to 2.3.0. Source reading needs outbound HTTPS to raw.githubusercontent.com; metadata search, combinations and reports work from the local checkout without that network request. The smoke check starts a real MCP client/server connection and makes no model API calls. Add `--fetch-source` to verify one public pinned instruction file; this still does not execute it.

## 3. Configure your client

Generate a configuration with the absolute paths for your own checkout. These commands print text only; they do not overwrite or register client settings. On Windows, use `.\.venv-mcp\Scripts\python.exe` in place of `.venv-mcp/bin/python` below.

For Codex:

```sh
.venv-mcp/bin/python mcp_server.py --config codex
```

Add the printed `[mcp_servers.ai_skill_library]` section to your client's MCP configuration, merging with existing settings. Codex's user configuration is `~/.codex/config.toml`. You can also register the same launch command with the Codex CLI:

```sh
codex mcp add ai_skill_library -- /absolute/path/AI-Skills-Library/.venv-mcp/bin/python /absolute/path/AI-Skills-Library/mcp_server.py
codex mcp list
```

Use the actual paths printed by the generator. Avoid registering the same server twice. See the [official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

For Claude Code or a client that accepts the `mcpServers` JSON format:

```sh
.venv-mcp/bin/python mcp_server.py --config claude
```

Merge the printed `ai_skill_library` entry into the client's existing MCP server configuration. For Claude Code you can instead use its CLI with your real paths:

```sh
claude mcp add --transport stdio ai_skill_library -- /absolute/path/AI-Skills-Library/.venv-mcp/bin/python /absolute/path/AI-Skills-Library/mcp_server.py
claude mcp list
```

Restart or reconnect the client as needed, approve its normal server trust prompt, and check that `search_skills` is visible. Host installation, tool policy, prompt menus and resource support vary; this library verifies the SDK protocol, not every desktop client's UI. See [Claude Code MCP setup](https://code.claude.com/docs/en/mcp).

## 4. Use it in a conversation

Example requests after connecting:

```text
Use the ai_skill_library MCP server to find skills for reviewing a SwiftUI app. Compare requirements and compatibility evidence before loading instructions.
```

```text
Use the ai_skill_library MCP server to get the react-motion combination. Load each stage's SKILL.md and its remaining pages only when needed, then help me build a reduced-motion-aware hero animation.
```

The website’s **MCP** section introduces the connection, offers task previews from current catalogue data, and provides a four-step setup wizard with client/OS choices and copyable commands. Previews and copy buttons do not run a local server. Skill cards offer **Copy MCP prompt**. Combination cards offer **MCP · Connected client** in the prompt selector. These buttons copy requests for the connected client; the website itself does not call your local server. Codex/Claude file-based invocation remains available as a separate option.

Clients exposing MCP prompts can request `use_skill` with `skill_id` and `task`, or `use_combination` with `combination_id` and `task`. These return task context, not a running agent. A skill source remains third-party reference data; host/user instructions and authorization still govern its use.

## Tools and progressive loading

| Tool | Purpose | Network |
|---|---|---|
| search_skills | Filter by task/category; sort by stars, name or research date | None |
| get_skill | Purpose, requirements, source pin and compatibility evidence | None |
| list_skill_files | Allowed source paths and expected Git blob hashes | None |
| read_skill_file | Hash-verify a single pinned UTF-8 source/reference file | Public GitHub raw |
| search_combinations | Find workflows by task and member category | None |
| get_combination | Ordered stages, member purposes, requirements and conflicts | None |
| list_reports | Dated report titles and slugs | None |
| read_report | Paginated text of a report in this checkout | None |

Searches return at most 30 results per page and provide `next_offset`. Source/report reads default to 120 lines, with a maximum of 400 lines and 64,000 characters per response. Follow `next_line` before treating a skill as fully read. Reading references does not automatically load sibling skills or install dependencies.

Resources: `skill-library://overview`, `skill-library://skills/{skill_id}`, and `skill-library://combinations/{combination_id}`. Resources return metadata and workflow structure; external source access is explicit through `read_skill_file` or the user-selected `use_skill` prompt.

## Boundaries and troubleshooting

The server exposes no install, shell execution, arbitrary URL fetching, project file editing or account-management tools. Remote reads are restricted to manifest-listed files at immutable catalogue commits, capped at 1 MB and checked against Git blob hashes. Redirects and binary source are rejected. Reports are restricted to known local Markdown slugs; path traversal and symlinks are rejected. Source text is not used as a tool description or permission grant.

Eight small source files can be cached in process memory. The server does not write a disk cache, contact telemetry endpoints or send your task text to a source repository. Its read-only annotation is backed by these API boundaries; the client may still have other powerful tools outside this server.

If source retrieval fails, check network access; do not substitute an unpinned main-branch file. A hash mismatch fails closed. If a skill needs a plugin/MCP tool that your client lacks, follow the pinned upstream setup after review. A catalogue support claim is not a runtime certification. MCP makes instructions easier to retrieve; it cannot create missing tool capabilities or guarantee token savings.

Run all protocol and library checks in the optional environment:

```sh
.venv-mcp/bin/python -m unittest discover -s tests -v
.venv-mcp/bin/python scripts/smoke_mcp.py --fetch-source
```

Maintainer reference: [official MCP Python SDK](https://py.sdk.modelcontextprotocol.io/get-started/). No third-party skill workflow is executed by these checks.
