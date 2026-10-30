# AI Skill Library website

AI Skill Library is a static, English-language journal generated from the reviewed repository reports and skill catalogue. Its source is in site/; its deployable files are in site/dist/.

## Read and explore

- Journal: featured video review, searchable report archive and topic filters.
- Articles: full reports, readable comparison tables, original Markdown links and downloads.
- Skill library: keyword search, twelve discipline filters, compatibility filters, evidence details and copyable invocation prompts.
- New note: a browser-local Markdown draft editor with explicit save and export.
- Curation: evidence labels and the manual editorial standard.

No external fonts, analytics, runtime packages, API credentials or network data fetching are required by the static site. Opening repository/source links leaves the site.

## Write a report

1. Open New note. Enter an English title and Markdown body.
2. Save browser draft to keep it on that browser, or export a Markdown copy. Browser storage can be cleared or unavailable; export important work.
3. Add the exported file to reports/ with a dated filename, for example 2026-10-22-design-review.md. You can use the GitHub link in the editor.
4. Review the report sources and compatibility claims. A saved browser draft is not a published report.
5. Run python3 site/build.py. It regenerates site/dist/data.js from reports/*.md and catalog/skills.json.
6. Commit the source and generated data, then redeploy the site.

The renderer supports headings, paragraphs, bullet lists, fenced code, tables, inline code, bold text and HTTPS/HTTP links. Raw HTML is escaped. Keep documents within this subset for predictable output. Repository links remain the source of truth.

## Preview and test

```sh
python3 site/build.py
python3 -m http.server 8765 --directory site/dist
python3 -m unittest discover -s tests -v
```

Open http://localhost:8765. Article and library filters use hash routes and work on static hosts without rewrite rules. Browser testing should cover article navigation, back behavior, search, category/evidence filters, empty states, copy buttons, browser draft save/restore, Markdown export, mobile layout and horizontal table scrolling.

## Hosting and preview status

The current design is named AI Skill Library. Existing historical Sites identity remains in site/.openai/hosting.json, but it is not used by the Vercel setup or the exported static template.

For later Vercel deployment, use the committed generated files under site/dist/ and the root vercel.json configuration. See [Vercel setup](VERCEL.md). The website has no runtime API, backend or environment-variable requirement. Rebuild after changing repository reports or the catalogue, then include the generated data.js in your eventual commit.

## Combination packs

`catalog/combinations.json` defines stage owners, handoff tasks, requirements, conflict handling and exact license blobs. `bundles.py` produces inert, deterministic ZIPs from pinned GitHub files after explicit source review. The website serves checked-in archives from `site/dist/downloads/`; `index.json` records their sizes and SHA-256 checksums. Update an archive and its index together after reviewing any pin changes. `site/build.py` rejects checksum drift. Unit tests also compare archive members, provenance and license hashes with the current catalogue.

The Combinations page provides workflow search, individual skill links, setup details and downloads. Recipe-only workflows intentionally have no ZIP or synthetic callable integration skill. The research playbook, configuration and review template live in `docs/RESEARCH.md` and `research/`. New manual collector runs use unique filenames to preserve previous snapshots.

### Claude Code / CLAUDE.md

Each downloadable pack also contains a root `CLAUDE.md` adapter. Keep the shared `.agents/skills` directory in the project and merge the adapter into an existing project CLAUDE.md rather than replacing that file. The adapter loads the chosen workflow explicitly by file path; it does not register native Claude slash commands or assume `.agents/skills` is automatically discovered by Claude Code.

Choose **Claude Code · CLAUDE.md** in the combination page to copy an explicit file-based prompt. CLI equivalent: `python3 bundles.py call react-motion --agent claude`. The default Codex prompt remains available. The adapter does not change upstream instructions, grant tool permissions or install dependencies. Neither host has an end-to-end runtime verification claim.

Reference: [Claude Code project memory](https://code.claude.com/docs/en/memory). CLAUDE.md supplies project instructions; a copied prompt requests a specific workflow.

## Skill sorting and member purposes

The Skills page supports curated order, GitHub stars (descending/ascending), alphabetical name, newest research observation, and documentary Codex evidence level. Sorting applies after category, evidence and text filters, preserves the source catalogue order, and uses names to break ties. The URL's `sort` parameter restores the selection on reload; unknown values fall back to curated order. Research date means `observed_at`, not upstream update time. Repository stars come from different dated snapshots and are not quality scores.

Combination members display their catalogue category, general purpose and task-specific workflow role as separate fields. **Contains skills for** selects workflows containing at least one skill in that category; all stages remain visible and in their original order. It intersects with the existing workflow search and works with either host prompt option.

Pure sorting and purpose-filter logic lives in `site/dist/library-ui.js`. Run `node --test tests/test_library_ui.cjs` (Node 18+) for its regression checks. `site/build.py` versions stylesheet and script URLs with content hashes so UI changes are not hidden by cached assets.
