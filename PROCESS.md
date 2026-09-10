# MP1 Redesign — Process & Decisions

This document details the design decisions and methodology behind the MP1 website redesign. For the summary report, see `iphs400_mp1-web-redesign_report_maggie-grespin_20260910.md`.

## Foundational Decisions

### Reusing the in-class critique

I was the project lead for my group, so I reused the critique we generated during class on 09/01 instead of regenerating it. This gave me a clear foundation to build from. I then stripped the Netlify/CI config first so the tech-spec wouldn't carry findings about a deploy pipeline we'd intentionally removed.

### Reviewing and approving the tech-spec

I reviewed everything before Claude implemented any changes, including five key judgment calls:

1. **Leaving a build step / templating system out of scope** — It contradicts the site's no-build-step design philosophy. I approved keeping this constraint.
2. **Assuming theailab.net as the canonical URL** — Clear decision about the deployment target.
3. **Direction of each de-duplication** — How to consolidate duplicated content across pages.
4. **Using longer week-title wording for more context** — Readability over brevity.
5. **Never rewriting any policy text** — Respect for the instructor's official content. I approved all of these.

### Test-first implementation

For the first three implementation tasks, I had Claude work test-first:
- Write a test that defines what "done" means
- Watch it fail
- Make the change
- Watch the whole suite pass
- Then, finally, commit

I verified every commit was scoped to one task and only one test was run for that task, so nothing was quietly weakened or over-edited.

The three tasks I checked this closely were:
- The list of external URLs it linked
- Which page each duplicated block moved to
- The week-title wording

## Content & Information Architecture Decisions

### Reorganizing the weights table

I chose to group the weights table into three sections: **Ongoing**, **Mini-Projects**, and **Final Project** rather than force one strict date-ordered list. This made sense because the two assignment tracks (ongoing + mini-projects vs. final project) run in parallel.

It bothered me that the Nov. 13 dates showed up *after* the Mini-Project 4 Nov. 20 due date in a purely chronological ordering. My grouping makes it clear what belongs to which track.

### The "Mini-Project 1" confusion

The assignment email calls this exercise "Mini-Project 1," but the site itself says "Mini-Project 1" is "Development Environment Configuration." I left the site as-is rather than rewrite the assignment based on one ambiguous sentence. I logged this confusion in `docs/iphs400_mp1-web-redesign_open-questions_maggie-grespin_20260903.md` for clarity.

I was too unsure to take out the original description entirely, so I kept it documented as an open question instead.

### Minor Home page changes

I added an **Office Hours row** to the Course Details table (value taken from the syllabus). I originally wanted to add an email row but chose not to — this website is public and I didn't want to put Professor Chun's personal contact info on a repo I control.

## Aesthetic & Interaction Decisions

### Palette iteration

I iterated the color palette live with Claude via screenshots. My direction was:
- "Go lighter, maybe cream"
- "Try a blue parallel to the yellow, not too in your face"
- "More blue"
- "I don't love the cream"
- Asked which background is easiest on the eyes for long reading
- Landed on `#edeef0` (cool neutral, not pure white, not dark)

### Font and decoration choices

I chose to follow the reference site's aesthetic (Geist, Hanken Grotesk) but implement it with a system font stack instead because the site bans web fonts. I matched the *look* rather than the exact fonts.

I also deliberately rejected the custom JavaScript cursor from the reference — our site is no-JS on principle. It loads instantly, works everywhere, and is one less thing to break.

### Navigation and discovery

I added:
- **Call-to-action buttons** (filled + outline with arrow) to highlight information students seek
- **"On this page" section jump list** fixed in the top-right corner on wide screens, inline above content on narrow ones
- **Hyperlinks throughout** so major topics referenced on one page link to their full sections
- **Adjacent week navigation** in the schedule so you can move from Week 4 to Week 3 or Week 5

## Final Review

I reviewed the rendered site page by page in Chrome before finalizing:
- Checked table text size
- Removed the header underline
- Shortened TOC labels
- Fixed boldness inconsistencies
- Tightened spacing

Then merged to main and pushed to my fork.

## What I Didn't Do (and Why)

- **Dark mode** — Left as a future feature; would only need ~15 lines of CSS
- **Search functionality** — Decided the hyperlinks were enough for navigation
- **Active section highlighting in "On this page"** — Would need JavaScript, which I deliberately didn't add to keep the site simple
- **Terminal motif for code blocks** — Sketched it in the spec but cut it for scope
