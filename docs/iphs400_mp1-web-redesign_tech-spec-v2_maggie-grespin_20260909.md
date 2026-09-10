# MP1 Website Re-Design v2 — Tech Spec

**Author:** Maggie Grespin · IPHS 400 · 2026-09-09
**Branch:** `web-redesign-v2`
**Source inputs:**
- Instructor brief: `iphs400_mp1-web-redesign_instructor-brief_20260909.md`
- Visual reference: https://www.sunnypatel.net/ (one site, provided by me)
- Prior revision: `iphs400_mp1-web-redesign_tech-spec_maggie-grespin_20260903.md` (v1, already merged)

## Goal

Restyle the course site so it reads as deliberate and stylish, not like a default
academic template, while staying just as easy to scan for information. This is a
**visual redesign of `css/style.css`** plus small, mechanical HTML changes to the
shared skeleton. No course content changes.

## Non-negotiable constraints (unchanged from `CLAUDE.md`)

1. No build step, no JS, no web fonts, no CDN/analytics/third-party.
2. One stylesheet. Shared header / identical nav / footer across all 22 pages.
3. Course content is the instructor's. The **weights table** (syllabus) and the
   **Course Details table** (home) keep their exact content and the same
   information in the same cells. Format/borders/spacing may change; data may not.
4. Test suite stays green; add a test for every new rule.

## Direction

Borrow the *feel* of the reference — warm, calm, editorial, one accent, big
confident headings, lots of vertical air, hairline rules instead of boxes — on a
**warm cream (light) background**, not the reference's near-black and not the old
stark white.

### 1. Palette (token swap in `:root`)

| Token | Old | New | Role |
|---|---|---|---|
| `--bg` | `#fff` | `#f5efe2` | warm cream page background |
| `--surface` | (none) | `#faf6ec` | table/callout fill, a touch lighter than `--bg` |
| `--text` | `#111` | `#211d17` | warm near-black body text |
| `--text-lt` | `#6b6b6b` | `#6c6455` | warm grey — captions, eyebrows, muted |
| `--accent` | `#0073aa` | `#b24a2e` | burnt orange — links, current-nav, rules-of-emphasis |
| `--accent-dk` | `#005177` | `#8f3a22` | hover/active |
| `--border` | `#e0e0e0` | `#ddd2bd` | hairline rules |
| `--code-bg` | `#f5f5f5` | `#efe7d5` | inline code / `pre` |

Contrast (must pass WCAG AA, verified in a test):
- `--text` on `--bg`: ~13:1 ✅
- `--text-lt` on `--bg`: ~4.7:1 ✅ (AA for normal text)
- `--accent` on `--bg`: ~4.9:1 ✅ (AA for normal text and UI)

Final hexes may be nudged ±small during implementation to hit these ratios exactly;
the test is the source of truth.

### 2. Type — system fonts, editorial treatment

No font files. Three system stacks as tokens:

```css
--f-display: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--f-body:    ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--f-mono:    ui-monospace, "SF Mono", "Cascadia Code", "Roboto Mono", Menlo, Consolas, monospace;
```

- **Body:** `--f-body`, 19px / 1.65. (Down from the current 22px serif — the serif
  is the main "term-paper" tell. Sans at 19 reads clean and modern and still
  passes readability for long text.)
- **Display headings** (`h1`, hero): `--f-display`, weight 700, `line-height: 1.08`,
  `letter-spacing: -0.02em`. Hero `h1` large: `clamp(2.5rem, 6vw, 4rem)`.
- **Section headings** (`h2`): weight 700, ~1.6rem, `letter-spacing: -0.01em`.
- **Eyebrow labels:** new `.eyebrow` class — `--f-mono`, `text-transform: uppercase`,
  `font-size: 0.72rem`, `letter-spacing: 0.14em`, color `--text-lt`. This is the
  single biggest style win and it costs nothing. Applied to the little rule +
  label that already sits above each page `h1` and above `.section` blocks.
- **Tables:** numeric / percentage / date cells in `--f-mono` so the weights table
  and schedule read like a spec sheet.

### 3. Layout & "efficiency"

- Keep the single narrow measure. `--mw: 660px` for prose.
- More vertical rhythm between `.section` blocks: `margin-block: 4.5rem` (from the
  current tighter spacing).
- **Tables lose their box.** No outer border, no full grid. `border-bottom: 1px
  solid var(--border)` on each `<tr>` only; header row `border-bottom-width: 2px`;
  cell padding `0.7rem 1rem`; left-align, `--surface` fill optional. Same markup,
  same cells.
- **Nav gets the numbered treatment:** `01 Syllabus  02 Schedule  03 Assignments
  04 Policies  05 About` — the number rendered in `--f-mono` `--text-lt` via a
  `::before` on each `<li>` using `counter()`, so **the HTML link text does not
  change** (keeps the nav-consistency test and breadcrumb logic intact). Current
  page: accent color + thin accent underline instead of the current heavy
  underline.
- Hairline rule under the header instead of the current treatment.
- Footer: smaller, `--f-mono`, muted.

"Runs more efficiently" concretely:
- Delete dead rules left from the WordPress "Twenty Nineteen" origin (there are
  several unused `.site-*` and featured-image leftovers). Target: `style.css`
  under ~380 lines from 452.
- All color/spacing/font values become tokens — no hard-coded hexes in rules.
- No new HTTP requests, no JS, no layout-thrash patterns. Single stylesheet still.

### 4. Stretch (do only if base is green and time allows)

- `@media (prefers-color-scheme: dark)` block that remaps the 8 palette tokens to
  the reference's warm-dark values. Because everything is tokenized this is ~15
  lines and gives visitors who want dark the reference look for free.
- A restrained terminal motif for `pre`/`code` blocks on the week pages (corner
  dots + label), CSS-only.

## Files touched

- `css/style.css` — the redesign.
- All 22 `*.html` — only if the nav `counter()` approach needs a wrapper element,
  and the `.eyebrow` class added to the existing label span. Mechanical, identical
  edit per page, scripted.
- `tests/test_unit_css.py` — new assertions (see below).
- `README.md` / `CHANGELOG.md` — record what changed.
- `CLAUDE.md` — update the "Layout" / stylesheet description (currently says
  "serif reading text at 22px", "single accent blue").

## Tests to add (`test_unit_css.py`)

1. `test_palette_tokens_present` — `--bg`, `--surface`, `--text`, `--accent` etc.
   all defined in `:root`.
2. `test_no_legacy_blue` — the string `#0073aa` and `#005177` appear nowhere.
3. `test_contrast_text_on_bg` / `test_contrast_muted_on_bg` /
   `test_contrast_accent_on_bg` — parse the hex tokens, compute WCAG relative
   luminance, assert ratio ≥ 4.5 (text/muted) and ≥ 4.5 (accent).
4. `test_no_web_fonts` — no `@font-face`, no `fonts.googleapis`, no `.woff`.
5. `test_eyebrow_style_defined` — `.eyebrow` selector exists with
   `text-transform: uppercase` and a `letter-spacing`.
6. Keep: `test_has_print_stylesheet`, `test_no_dead_class_selectors`.

## Judgment calls (flag for review before implementing)

- **Sans body instead of serif.** Biggest single change to the reading
  experience. Alternative: keep a serif for `.page-content` prose only, sans for
  everything else. Default: go full sans (matches the reference, feels more
  current).
- **Numbered nav.** Stylistic, reversible, HTML-safe via `counter()`. Default: do it.
- **Cream is `#f5efe2`.** Warm but light. If it reads too yellow on a real screen,
  shift toward `#f3f0e8` (greyer cream). Decide from the preview screenshot.
- Dark-mode block and terminal motif are explicitly stretch, not core scope.

## Sequence

1. Build one static preview page (`/tmp` or a scratch file) with the new palette +
   type applied to the real home page. Screenshot desktop + mobile. Get sign-off
   on palette and type.
2. Write the new `style.css` against this spec.
3. Script the per-page HTML edits (`.eyebrow` class, nav wrapper if needed).
4. Add the tests; run the full suite; iterate to green.
5. Review every page rendered in the browser, desktop + mobile.
6. Update `CHANGELOG.md`, `README.md`, `CLAUDE.md`. Merge to `main`.
