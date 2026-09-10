# Changelog

All notable changes to this site are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed — Mini-Project 1 redesign (v2, 2026-09)
- New visual design for `css/style.css`: neutral light-grey paper (`#edeef0`),
  blue-black text, a single muted blue accent (`#2b5896`). System fonts only —
  a geometric-sans display/body stack plus a monospace stack for labels.
- Editorial layout: large tight headings, one narrow measure, more vertical air,
  hairline row rules instead of boxed tables, monospace breadcrumbs / table
  row-headers / footer, and bold text rendered in the accent colour.
- Call-to-action buttons (`.btn`) on the home hero and the assignments intro.
- Old WordPress "Twenty Nineteen" leftovers removed; every colour, size, and
  font is now a `:root` custom property.
- Tests added: palette-token presence, WCAG-AA contrast computed from the hex
  tokens, a no-web-fonts guarantee, and button-selector presence.

### Removed
- Netlify configuration (`netlify.toml`) and the GitHub Actions deploy workflow.
  The site is now standalone-local: serve it with `python3 -m http.server`.
- ~55% of `css/style.css` — dead rules (blog, featured-image, badge, WordPress
  block, and placeholder styles) inherited from the theme this layout came from.
- Verbatim content duplication: the course description / learning outcomes, the
  assignments-and-weights table, and the secrets-hygiene list each now live in
  one canonical place and are linked from elsewhere.

### Added
- Per-page `<meta name="description">`, a favicon, `<link rel="canonical">`,
  Open Graph / Twitter Card tags, `robots.txt`, and `sitemap.xml`.
- Accessibility: skip link, `aria-current` on the active nav item, named
  navigation landmarks, `<ol>` breadcrumbs, table `<caption>` and `scope`,
  an explicit `:focus-visible` style, and a print stylesheet.
- Real hyperlinks / `mailto:` for every external resource named in the copy.
- Expanded pytest suite: external links, week-title consistency, no duplicate
  content blocks, metadata, accessibility structure, HTML-lint checks, calendar
  consistency, and a CSS dead-code check. Pinned test dependencies.
- `CONTRIBUTING.md`, `CLAUDE.md`, and internal review docs under `docs/`.

### Changed
- Week 6, 10, 13, 14, 15 titles reconciled across schedule, `<title>`, `<h1>`,
  and breadcrumb.
- `index.html` hero heading is the course name instead of "Home".
- Muted text colour darkened for a safer AA contrast margin.
- Navigation markup normalized (shortest relative paths, consistent attributes).
- `.gitignore` trimmed from the full Python template to what this repo uses.
