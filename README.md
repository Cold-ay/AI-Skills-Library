# AI Skills Library

An evidence-based catalogue of useful AI skills, with a small discovery/install CLI and an editorial report website. Covers website/UI, video, coding, token/context efficiency, research/automation and skill engineering.

**28 curated entries · 6 combinations · 4 downloadable packs · English documentation · Manual reports · No scheduled updates**

## Discover a skill

Python 3.9+; standard library only. No paid API is needed to browse the library.

```sh
git clone https://github.com/Cold-ay/AI-Skills-Library.git
cd AI-Skills-Library
python3 skills.py list
python3 skills.py list --category website-ui
python3 skills.py list --query animation
python3 skills.py show taste-skill
```

[Browse the catalogue](docs/CATALOG.md) · [Read the video analysis](reports/2026-10-21-video-review.md) · [Current discovery snapshot](reports/2026-10-21.md) · [Evidence standards](docs/CURATION.md)

## Install and call

Read the complete pinned skill folder, dependencies, compatibility evidence and license before installing. Then copy the reviewed files into your project:

```sh
python3 skills.py install taste-skill --dest /path/to/project/.agents/skills --reviewed
python3 skills.py call taste-skill 'Review the visual direction of this website'
```

`call` prints `$design-taste-frontend Review the visual direction of this website`. Paste it into a new Codex session after confirming the skill is loaded. The invocation uses the skill's frontmatter name, which can differ from its catalogue ID.

Use `--dest ~/.agents/skills` explicitly for a personal destination. Existing skills are never overwritten. Entries needing a full plugin, shared dependencies, binary launchers or hooks point to upstream installation instead of using standalone copying.

Installation only downloads pinned files and verifies Git blob hashes. It does not execute third-party scripts, hooks or skill instructions. Later use inside an agent can invoke tools, so review the source first.

## Where to start

| Task | Suggested entry | Main requirement |
|---|---|---|
| Distinctive website art direction | taste-skill | Node 22+ and a supported browser for its scripts |
| Product UI and design-system choices | ui-ux-pro-max | Upstream Codex installation and Python data search |
| Design critique and polish | impeccable | Review upstream binary launcher and native hooks |
| Layout variety and design audit | hallmark | Review optional service integrations |
| React performance | react-best-practices | Match rules to your framework version |
| Accessibility and interface review | web-design-guidelines | Reads external guidelines at use time |
| Web animation | gsap-core | GSAP in your target project |
| Record-ready article presentations | web-video-presentation | Vite, React and TypeScript; optional TTS |
| Programmatic video | remotion-best-practices | Node.js and Remotion |
| Long-session handoff | context-compression | Measure quality as well as token use |
| Research citations | zotero | Zotero Desktop and its complete plugin |
| Plugin engineering | plugin-creator | Upstream repository workflow |

Codex labels distinguish static official evidence, upstream support claims and unknown compatibility. **None of the third-party workflows has been runtime-tested in Codex.** Three deprecated `openai/skills` entries remain migration references; current official examples are in [openai/plugins](https://github.com/openai/plugins).

## Reports and website

The redesigned AI Skill Library uses static HTML, CSS and JavaScript. See [Vercel setup](docs/VERCEL.md) for its hosting configuration.

Reports are added manually under `reports/`. The existing 2026-10-21 snapshot is preserved, including its collection errors. The video review adds a separate dated article and evidence file. No weekly schedule, report automation or scheduling template is included.

The `site/` directory contains the AI Skill Library website: report articles, a searchable skill catalogue, topic filters, and a browser-local Markdown draft editor with export. Published pages are generated from repository reports and catalogue data.

```sh
python3 site/build.py
python3 -m http.server 8765 --directory site/dist
```

Open `http://localhost:8765`. See [website publishing and authoring](docs/WEBSITE.md). Browser drafts stay on that browser until exported; publishing a report requires adding its Markdown to this repository and rebuilding/redeploying the site.

The optional `python3 report.py` collector is **manual only**. It reads public GitHub metadata and writes a dated snapshot; it never modifies the curated catalogue. API failures are recorded and return a failing exit status. The script is not used by the website build.

## Validate

```sh
python3 -m unittest discover -s tests -v
python3 skills.py validate
python3 site/build.py
```

Tests cover catalogue invariants, safe installation, integrity failure rollback, report evidence and safe website generation. See [validation notes](docs/VALIDATION.md).

Official reference: [Build skills](https://learn.chatgpt.com/docs/build-skills). Third-party projects retain their own licenses. This library stores original curation notes, source links and file manifests and reviewed downloadable packs with unchanged third-party files and their licenses.

## Combinations and downloads

Browse [workflow combinations](https://ai-skill-library.vercel.app/#combinations): four downloadable packs and two dependency-aware recipes. Each explains its stages, handoff artifacts, prerequisites, conflicts and evidence limits. Packs include pinned original skill files, MIT license texts, provenance manifests and a `combination-*` orchestration skill. They are static integration proposals; no end-to-end Codex runtime test is claimed.

```sh
python3 bundles.py list
python3 bundles.py show react-motion
python3 bundles.py call react-motion
# After source/license review, build a fresh archive (never runs upstream code):
python3 bundles.py build react-motion --out /tmp/react-motion-new.zip --reviewed
```

Review and extract downloaded ZIPs in a staging directory. Copy `.agents/skills` into a project after checking existing folders; install runtime dependencies separately. Start a new Codex session and invoke `$combination-react-motion <your task>`. Check archive checksums in `site/dist/downloads/index.json`.

For your own discovery, use the [research playbook](docs/RESEARCH.md), [editable search configuration](research/queries.json), and [review template](research/review-template.md). The [expansion report](reports/2026-10-21-combinations.md) records seven additional skills, decisions and source limitations. Collection remains manual.

### Claude Code support

Packs include `CLAUDE.md` alongside the shared `.agents/skills` source files. Merge the adapter into your project's existing CLAUDE.md, keep the skill folders, then choose **Claude Code · CLAUDE.md** on the website or run:

```sh
python3 bundles.py call react-motion --agent claude
```

Paste the resulting file-based request into Claude Code. This does not install native slash commands, execute code or establish runtime compatibility. See [host setup](docs/WEBSITE.md#claude-code--claudemd).
