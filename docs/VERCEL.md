# Vercel setup for AI Skill Library

AI Skill Library is configured as a static Vercel project. The generated website is checked in under site/dist/.

## Deploy the repository when ready

1. Review the template and make any desired design changes.
2. Run `python3 site/build.py` to regenerate the static data from reports/ and catalog/skills.json.
3. Run `python3 -m unittest discover -s tests -v`.
4. Commit and push the reviewed changes when you are ready for Git-based deployment.
5. Import the repository into Vercel, with Framework Preset **Other** and Root Directory at the repository root (`.`).
6. The root `vercel.json` sets Output Directory to `site/dist`, with empty build and installation commands. Generated assets are already included, so the Vercel build does not require Python, Node packages or credentials.
7. Review the intended account and project, then deploy.

The empty build step is intentional: this version serves checked-in static output. If reports or catalogue data changes, run the local generator and include its data.js output in your commit. No scheduled reports, automatic source fetching or server-side storage are configured.

## Standalone template archive

The exported template archive contains index.html, CSS, JavaScript, generated report/catalogue data, an SVG icon and its own vercel.json. For that archive, Output Directory is `.` because its files are already at the root. It is a snapshot; the repository remains the source for future report updates.

## Behavior after deployment

- Hash routes work without server rewrites.
- All reports and skills are included at build time.
- Drafts are stored in the visitor's browser and can be exported to Markdown.
- Saving a draft does not publish a report or write to GitHub.
- Clipboard copy requires the normal secure browser context, which Vercel provides over HTTPS.
- The template does not add a login gate. Choose access settings separately when you deploy.

The setup needs no runtime secrets. Deployment status is recorded separately after the platform confirms a successful build.
