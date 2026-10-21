# Ten web design skills: what is useful beyond the demo?

A source review of Debug Tuboshu's 67-second video, with a practical shortlist for this library and its report website.

## Source and method

Source: [10 Web Design Skills You Need](https://www.youtube.com/shorts/33cXtiB5v_I), by Debug Tuboshu. Reviewed on 2026-10-21. The YouTube page shows a publication date of 2026-08-10. The page has no description and offers no closed captions. I inspected the numbered cards and on-screen examples directly in the browser; this report is not a verbatim transcript or an audio transcription.

Timestamps below identify observed frames rather than exact segment boundaries. Repository mappings come from the project titles, matching READMEs and source contents. Current pinned sources can differ from the versions shown in the August video. No installer, launcher, hook or third-party skill script was executed during this review.

## The ten recommendations

| Video frame | Project | What it contributes | Library decision |
|---|---|---|---|
| 00:03 | Taste Skill | Art direction, composition and a visual review loop | Add taste-skill |
| 00:08 | UI/UX Pro Max | Searchable design-system and UX guidance | Add ui-ux-pro-max; upstream installation required |
| 00:15 | Impeccable | Design critique, quality checks and polish commands | Add impeccable; review launcher and hooks first |
| 00:22 | Frontend Design | Deliberate typography, colour and aesthetic direction | Already present as frontend-design |
| 00:27 | Hallmark | Layout structure and audits that resist repetitive templates | Add hallmark |
| 00:32 | GSAP Skills | Animation APIs, timelines and scroll behavior | Add the focused gsap-core skill |
| 00:38 | Stitch Skills | Design extraction and design-to-code workflows | Add stitch-design-md; Stitch MCP required |
| 00:43 | Web Interface Guidelines | Keyboard, focus, spacing, contrast and UI review | Already represented by web-design-guidelines |
| 00:51 | Nothing Design Skill | A monochrome industrial design system | Add nothing-design as a specialist option |
| 00:57 | Garden Skills | Article-to-web-video storytelling | Add web-video-presentation |

Garden is a collection rather than a single skill. Its beautiful-article companion is also added because an editorial workflow is directly relevant to publishing these reports. That companion was discovered in the repository; the video does not name it separately.

## The most useful combination

For a report blog, start with editorial structure: what should a reader learn, which sources support it, and what belongs in the article versus the catalogue. Taste Skill and Hallmark address different parts of this problem. Taste focuses on art direction and subject-specific composition; Hallmark pushes structural variety and offers audit-only behavior. One considered design direction is more useful than loading every aesthetic skill into the same session.

UI/UX Pro Max and Web Interface Guidelines are useful review lenses. Their value is in ordinary details: readable text, visible focus, labelled controls, responsive layout and predictable navigation. The existing Vercel entry already covers the latter, so a duplicate catalogue item would add little.

Impeccable is worth tracking for critique and refinement, but its current source has evolved beyond a passive Markdown guide. Its launcher may download an engine binary, and the upstream installer can add native hooks. This library records that dependency and directs users upstream instead of pretending that copying one folder provides the full integration.

GSAP is useful when a page needs coordinated animation. A reading-focused report site only needs restrained CSS transitions and reduced-motion support, so adding a runtime animation dependency would not improve this first version. The gsap-core entry is retained for future interactive explainers.

Stitch's design-md skill is useful once an existing Stitch project needs a reusable design language. Its documented MCP requirements make it a conditional tool. Nothing Design is similarly conditional: a distinctive industrial style can work for technical dashboards, but should be explicitly chosen rather than imposed on every report.

Garden's web-video-presentation provides a route from an article to a narrated, record-ready presentation. This is relevant to future report repurposing. The first site remains an article archive. Optional TTS, provider credentials and the upstream review/checkpoint workflow are documented rather than silently run.

## Evidence and actual Codex support

| Source | Repository stars observed | Codex evidence | Main integration limit |
|---|---:|---|---|
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | 99,768 | Upstream README documents a Codex plugin | Node 22+ and supported browser |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 137,926 | README documents uipro init --ai codex | Shared assets and platform layout |
| [Impeccable](https://github.com/pbakaus/impeccable) | 83,690 | README documents Codex provider and hooks | Binary launcher and native hooks |
| [Hallmark](https://github.com/Nutlope/hallmark) | 30,440 | README explicitly lists Codex | Review optional providers and script behavior |
| [GSAP Skills](https://github.com/greensock/gsap-skills) | 16,731 | README lists Codex in supported agents | Target application needs GSAP |
| [Stitch Skills](https://github.com/google-labs-code/stitch-skills) | 8,545 | README provides Codex marketplace instructions | Stitch MCP and plugin dependencies |
| [Nothing Design](https://github.com/dominikmartn/nothing-design-skill) | 2,833 | Inspected README does not establish Codex support | Claude-oriented tool metadata; unknown |
| [Garden Skills](https://github.com/ConardLi/garden-skills) | 13,036 | README explicitly includes Codex | Chinese instructions and workflow adaptation |

Counts are repository-level observations on 2026-10-21, not the values shown in the video or a measure of individual skill quality. Taste's count is from the preserved discovery snapshot; the remaining counts are from GitHub repository search API responses collected for this review. Fixed commits, per-skill manifests, license links and compatibility evidence are in catalog/skills.json; a compact review record is in the adjacent JSON file.

All newly claimed Codex support remains upstream-claimed. Nothing Design remains unknown. None has a recorded end-to-end Codex runtime test. MIT or Apache licensing of a skill repository also does not replace separate runtime, asset or service terms.

## What changed in the library and website

Nine entries were added: eight recommendations from the video plus Garden's beautiful-article companion. Frontend Design and Web Interface Guidelines were reused from the existing catalogue. Documentation is English, and reports are manually maintained. The original discovery snapshot and its collection failures remain available.

The Fieldnotes website uses a clear editorial hierarchy, a report archive, readable article pages, category navigation and a searchable skill catalogue. It includes a browser-local draft editor with Markdown export. Published reports remain repository files: export a draft, review it, add it to reports/, then rebuild and redeploy. No recurring reporting system is configured.
