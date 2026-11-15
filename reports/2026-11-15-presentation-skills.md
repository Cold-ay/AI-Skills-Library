# Presentation skills: HTML, editable PPTX and image decks — 2026-11-15

Six requested presentation skills reviewed and added under Presentations & PPT, with three workflow recipes. The library now has 62 entries, 26 combinations and five existing downloadable packs. All six new entries are reference-only: their pinned reading sets are not complete installations. This report does not introduce a recurring schedule.

## Choose by the artifact you need

- **Editable PowerPoint objects**: start with PPT Master. Its supported native conversion and existing-deck routes are the relevant distinction; verify the actual export in PowerPoint before relying on editability or fidelity.
- **A custom live browser presentation**: start with Frontend Slides. It offers visual style selection and HTML authoring without requiring a slide editor.
- **An editorial or Swiss-style talk**: choose Magazine Web PPT when its constrained visual system and presenter tools fit. Its current source license needs separate consideration before redistribution.
- **Repeatable template-based browser decks**: choose HTML PPT Studio, especially for technical talks and presenter notes.
- **Visual reading/sharing decks**: choose baoyu-slide-deck if you accept generated slide images and backend costs. Keep prompts so you can regenerate individual pages.
- **A reusable image-first style workflow**: visual-style-ppt is a conditional reference. Its model requirement and missing explicit license prevent an install/redistribution recommendation here.

A file ending in `.pptx` does not prove its text, chart or diagram is editable. HTML/CSS source editing, native PowerPoint object editing and replacing one full-slide image are different capabilities.

## Primary-source snapshot

| Requested name and pinned entry | Canonical repository | Repository stars | Main output route | Source license |
|---|---|---|---|---|
| [Frontend Slides](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/SKILL.md) | zarazhangrui/frontend-slides | 32,329 | html | MIT |
| [Magazine Web PPT](https://github.com/op7418/guizang-ppt-skill/blob/93d21bf4a73a851907a6eb00acbf30618236667a/SKILL.md) | op7418/guizang-ppt-skill | 29,800 | html | AGPL-3.0 |
| [HTML PPT Studio](https://github.com/lewislulu/html-ppt-skill/blob/fd1629067909ff55b36b905476de4e5f26062a1f/SKILL.md) | lewislulu/html-ppt-skill | 9,091 | html | MIT |
| [PPT Master](https://github.com/hugohe3/ppt-master/blob/b243a950e9f85998705551fb1b77c6459573ff39/skills/ppt-master/SKILL.md) | hugohe3/ppt-master | 76,891 | native-pptx | MIT |
| [baoyu-slide-deck](https://github.com/JimLiu/baoyu-skills/blob/ca703c2d7c2c4399a1dc0cf82224f8551e05a96d/skills/baoyu-slide-deck/SKILL.md) | JimLiu/baoyu-skills | 27,549 | image-pptx | MIT |
| [visual-style-ppt](https://github.com/irenerachel/visual-style-ppt-skill/blob/71224618a2049dc47c3f32b01e1fff119dc03f45/SKILL.md) | irenerachel/visual-style-ppt-skill | 398 | image-pptx | Not established |

Stars were collected from the GitHub API on this research run and describe whole repositories, not individual skills or quality. Exact timestamps, commits and complete trees are saved in `reports/evidence/2026-11-15-presentation-skills/`. No star-growth claim is made. Every new entry has explicit upstream Codex guidance or a claim, so all six are labeled **upstream-claimed**, with `runtime_tested: false`; none is labeled runtime verified. Claude support is also documentary only and remains unknown for visual-style-ppt.

## Identity and provenance

The supplied Zhihu links are entity-search links, not the original project sources. Their names seeded primary-source searches; their signed query tokens were not copied into this repository.

Frontend Slides resolves to Zara Zhang's `zarazhangrui/frontend-slides`. A separately maintained fork by wengzige appeared in search, but is not conflated with the original. Magazine Web PPT resolves to `op7418/guizang-ppt-skill`; its current invocation name is `guizang-ppt-skill`. HTML PPT Studio resolves to `lewislulu/html-ppt-skill`; its invocation is `html-ppt`.

“PPT Master” is ambiguous: search surfaced several unrelated or derivative repositories, including a Reveal.js workflow and portable forks. This review uses `hugohe3/ppt-master`, whose pinned skill metadata identifies that official repository. The names alone do not establish equivalence. No trust or compatibility claim is inherited from a directory listing or similarly named fork.

## What each skill adds and where it stops

### Frontend Slides

The core workflow shows multiple style previews, then builds a fixed 16:9 HTML deck. It also describes rebuilding content from an existing PPTX. This is a strong fit for talks, pitches and decks you want to customize in code; conversion is not a fidelity guarantee for every PowerPoint feature.

The “zero dependencies” description concerns core browser delivery, not every optional route: font links can still need network access, extraction uses `python-pptx`, and PDF/deployment helpers can download packages, browsers or publish files. The PDF helper captures slides as images, so the resulting PDF should not be described as native editable slide content. The complete support files are needed; the library's selected reading manifest is insufficient for installation.

### Magazine Web PPT

Its editorial and Swiss systems, speaker notes, audience synchronization and low-power path are distinctive for live talks. This is a design choice rather than a general-purpose PowerPoint generator. The source itself identifies HTML as its main deliverable.

The pinned license is AGPL-3.0, so it is not eligible for the library's MIT-only ZIP builder. Keep it as an upstream reference and review terms and bundled assets before redistribution. Optional image-model names are upstream terminology; this review did not establish access to those models. Runtime dependencies, offline fonts, fallback animation and presenter-window behavior need target-browser testing. Update checks described upstream must not silently replace a reviewed source pin.

### HTML PPT Studio

A modular static deck workflow separates theme, page layout and animation. Its presenter window and notes support technical sharing and repeatable reports. Compared with freeform Frontend Slides, it provides more explicit template scaffolding.

The whole assets/templates/runtime structure matters: moving just the HTML can break relative references. Remote font imports have fallbacks, so offline output can look different. The inspected PNG renderer assumes a macOS Chrome path; cross-platform use needs an explicit adaptation. Templates, theme counts and animations change over time; this report does not turn marketing counts into a permanent contract. It produces HTML and image captures, not native editable PowerPoint objects.

### PPT Master

This is the most relevant of the six for native PowerPoint delivery. The pinned router separates new generation, template creation and source-preserving editing of an existing deck. For supported SVG/native conversions, the intent is editable DrawingML objects rather than one screenshot per slide.

Use its complete official distribution: the current entry requires an attribution guard and supporting workflows/scripts; neither was executed here. Verify unsupported SVG/PowerPoint features, chart data, fonts and the chosen preservation route in a real export. Python and route-specific dependencies are required; optional source conversion/media dependencies have their own terms and service behavior. The root/package MIT label does not make every optional dependency MIT. Native editability and fidelity remain source-based claims, not measured results from this round.

### baoyu-slide-deck

This workflow saves an outline and a prompt per slide, supports style presets and selective regeneration, then merges generated raster images into PPTX/PDF. Its emphasis is reading and sharing rather than speaker-led delivery. The inspected PPTX merger uses image placement; prompts may be retained in speaker notes but are not native slide text.

The pinned skill describes native Codex image generation and alternative backends. A usable raster backend and Bun/npx plus merger packages must actually be available. Generation may involve billing and transmission of content; neither was configured here. Correcting rendered words generally means regenerating a page. Keep source prompts, citations, asset rights and approved images together rather than treating the PPTX alone as the editable source.

### visual-style-ppt

Its useful idea is a persistent Style Lock: a shared specification for typography, palette, layout, borders and text density across generated slide images. It includes outline/prompt approval, page-image review and an image-only PowerPoint delivery container.

The pinned source requires a model named “Image 2.5”, forbids an HTML fallback, and stops when that requirement is unavailable. This is an upstream requirement, not a verified statement about product availability or this environment. Defaults are Chinese-first; request English explicitly when needed. No license file was found in the complete pinned tree, so this entry is a conditional reference without a redistributed pack or install recommendation. Public availability is not treated as redistribution permission.

## Additional native-PPTX comparison

[Anthropic's pptx skill](https://github.com/anthropics/skills/tree/1780c5e5a552fd4d1c9d6a7b0cab26b0c2bef064/skills/pptx) was inspected as a comparison, not a seventh catalogue addition. Its per-skill `LICENSE.txt` is Apache-2.0 at the inspected pin; repository-level license metadata alone did not establish that. It describes PPTX creation/editing and package/rendering workflows. This review did not execute it or establish Codex runtime support. Prefer the specific workflow and actual editability you need over assuming every presentation skill outputs interchangeable files.

## Combinations: sequential roles, one authoring owner

- **Evidence to browser slides** (`research-to-html-slides`): Scientific Critical Thinking produces a claim ledger; Frontend Slides owns the deck; Web Design Guidelines reviews keyboard, contrast, motion and overflow. Handoff: claims → HTML deck → review findings.
- **Source to editable PowerPoint** (`source-to-editable-pptx`): Scientific Critical Thinking locks source claims; PPT Master selects and runs the appropriate native route; Verification Before Completion checks the actual export. Handoff: content contract → PPTX → evidence and limitations.
- **Outline to visual reading deck** (`visual-reading-deck`): baoyu-slide-deck owns prompts, approved images and packaging; Verification Before Completion checks image order, counts and readability. Handoff: prompts/images → image PPTX/PDF → measured checks.

These are recipes, not new ZIPs or proven integrations. Frontend Slides, Magazine Web PPT and HTML PPT Studio are alternative design owners; loading all three at once would create conflicting stage, layout and runtime rules. Likewise, baoyu-slide-deck and visual-style-ppt are alternative image-deck workflows. Adding a wrapper does not solve provider, license or dependency requirements.

Browse the [Presentations & PPT category](https://ai-skill-library.vercel.app/#library/presentations) and [Combinations](https://ai-skill-library.vercel.app/#combinations). The existing MCP connection can discover these catalogue entries and read the pinned files on demand; it does not run their scripts, install their assets or create a presentation merely by reading them.

## Discovery and invocation

```sh
python3 skills.py list --category presentations
python3 skills.py show ppt-master
python3 skills.py show html-ppt-studio
python3 bundles.py show source-to-editable-pptx
```

All six return an upstream-setup requirement if passed to the copy-only installer. The manifests intentionally contain selected reading files rather than a complete runnable distribution. Review the fixed upstream version and its documented setup separately before any installation; no global skill directory or client setting was changed.

With the library's MCP server already connected, a suitable research request is:

```text
Find presentation skills for editable PowerPoint, inspect ppt-master requirements,
and read its pinned entry instructions. Explain the required upstream setup;
do not execute its guard, installers or exporters during this review.
```

For Claude, use explicit file-based instructions or the appropriate upstream plugin/skill setup. The library's existing CLAUDE.md pack adapters do not automatically register these six upstream projects, and native command names should not be inferred from display names.

## Reusable research method

- **Resolve identities** with the exact requested names, then verify the original maintainer, canonical repository and actual SKILL.md path. Record ambiguous names and forks rather than merging them.
- **Capture primary evidence**: repository ID, stars and timestamp; full source commit; recursive tree; entry instructions; nearest license; output/export workflow and dependency files. GitHub descriptions and directory scores are leads, not proof.
- **Read instructions as data**. Inspect relevant scripts for package installation, external publication, file writes, image placement and host assumptions. This run verified 43 selected reading-file hashes against Git blobs; it did not audit all code or run those files.
- **Classify actual artifacts**: browser HTML, native object PPTX, image-only PPTX, PDF and image exports. Record notes, fonts, offline behavior, source-template preservation and the cost of later text corrections.
- **Separate claims from trials**: an explicit Codex mention supports an upstream-claimed label. A runtime claim would require a disposable sample, exact host/version, successful output and visual/editability checks.
- **Decide packaging last**. Missing licenses, differing terms, scripts, model requirements and incomplete asset trees prevent a generic copy-install or combined ZIP in this round. Keep a useful reference without implying a turnkey package.

Exact searches and decisions are in the adjacent JSON report; public API evidence and verified reading manifests are in the dated evidence directory. `research/queries-presentation-skills.json` is a configuration for future manual searches, not a claim those collector queries were executed in this run. Source snapshots remain dated; do not overwrite old observations to imply growth.

## Verification limits

Library tests validate catalogue structure, source pins, evidence, categories, reference-only gates, recipe membership and generated website content. They do not validate deck quality. No upstream installer, attribution guard, exporter, presentation runtime, model backend or image-generation call was executed; no native deck, PDF or slide image was produced. Cost, model access, PowerPoint fidelity, browser performance and accessibility remain unmeasured. No recurring task was created.
