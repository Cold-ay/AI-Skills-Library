# Fieldnotes website

Fieldnotes is a static, English-language journal generated from the reviewed repository reports and skill catalogue. Its source is in site/; its deployable files are in site/dist/.

## Read and explore

- Journal: featured video review, searchable report archive and topic filters.
- Articles: full reports, readable comparison tables, original Markdown links and downloads.
- Skill library: keyword search, six discipline filters, compatibility filters, evidence details and copyable invocation prompts.
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

## Hosting

The site is published privately using Sites: [Open Fieldnotes](https://ai-skills-fieldnotes.spicy-dog-4235.chatgpt.site). Its identity and static directory are recorded in site/.openai/hosting.json. Keep that identity for future redeploys. The site contains the current reviewed reports at deployment time; it does not pull live data from GitHub or update on a schedule. Source changes in GitHub require an explicit rebuild and redeploy.

A separate deployment checkout is used for the Sites source helper so its managed source repository does not replace this GitHub repository's remote. Only generated website assets and its hosting manifest are copied into that checkout. No credentials are stored in repository files.
