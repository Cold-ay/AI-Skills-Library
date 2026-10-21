# AI Skill Library: review template

## Applied repository skills

- **Frontend Design** from anthropics/skills: intentional visual direction, product-specific content, restrained motion and clear typography. Source pinned in catalog/skills.json as frontend-design.
- **Web Design Guidelines** from vercel-labs/agent-skills: semantic controls, visible focus, labels, meaningful navigation, empty states, reduced motion, source evidence and draft-loss feedback. Current upstream guideline text was read during this review.

The skills were used as design and review instructions. No third-party installer, launcher or bundled script was executed. Hallmark and the other catalogue projects remain useful references; this revision does not claim that their full workflows ran.

## Direction

A useful software library rather than a magazine masthead. The home page starts with a real task selector, category browsing and a focused selection of skills. Reports have their own archive and reading view. All website branding uses the singular name **AI Skill Library**.

- Canvas: white, with cool surfaces (#f5f7fc) and subtle dividers (#e3e8f0).
- Type: system sans-serif with a strong hierarchy; monospace only for executable invocation text.
- Accent: cobalt (#2854dc); ink (#18243b); muted text (#627086).
- Layout: workflow-led discovery, seven categories, selected skill records, report feature and source standard.
- Motion: short user-triggered feedback; no autoplay animation; reduced-motion preference respected.
- Content: the existing 21 skill records and two reports. No invented adoption metrics or runtime-verification claims.

## Template views

- `#home`: project-type selector, seven categories, curated starting points and report feature.
- `#library`: skill search, category/evidence filters, source details and invocation copy.
- `#reports`: searchable, filtered report archive.
- `#article/<slug>`: full article and Markdown download.
- `#draft`: browser draft, explicit save and export.
- `#about`: source and compatibility standards.

The preview was reviewed before deployment was authorized. Vercel serves the generated static files without a framework build.
