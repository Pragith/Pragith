# Retirement — 2026-10-05

- Remove retired Agent Keyboard demo route, project listing and source symlink. Remove host deployment mount and verify home 200/demo 404.

# Changelog

## Copy review — 2026-10-12

- Review all 16 sitemap pages, six linked work summaries, the noindexed Caffeinate-d page, three additional contact intents and the 404 page: 27 live pages/states, 384 main text blocks and 3,717 captured main-text words including repeated sections.
- Review titles, search/social descriptions, link labels, image descriptions, form options/placeholders/prefills, shared navigation/footer and source-only success/failure/500 copy. Distinguish unused content fields and the 96 unrouted blog files from current published pages.
- Record 93 editorial findings with reasons, proposed wording, source references and page associations, including seven high-priority problems. Preserve verified career dates/titles, named teaching programs, meaningful technical terms, product limitations and artwork attribution; request evidence instead of inventing outcomes.
- Save the complete annotated capture and a searchable page-by-page HTML review under `docs/copy-review-2026-10-12/`. Validate all captured fragments have review decisions; check report filtering and rendering with zero browser exceptions. No public copy was rewritten or published as part of this audit.

## 1.1.2 — 2026-10-12

- Restore the portrait's original effective 20px rounded frame, soft shadow, subtle saturation/contrast treatment and 340px height limit at the owner's explicit request. This photograph is an intentional exception to square component styling.
- Keep the responsive browser checker from treating the portrait as a square control.
- Synchronize the manifest, lockfile, installed package and UI at 1.1.2. Published via the existing bind mount and container restart. `docker exec pragith-web uv run pytest -q`: 39 passed; Ruff and diff checks clean. Live browser checks at 390px and 1440px confirmed the original effective radius, shadow and filter; both screenshots were visually inspected.

## 1.1.1 — 2026-10-12

- Consolidate the inline component styles and revision overrides into one readable `site.css`; remove obsolete homepage, carousel and decorative rules from the active frontend.
- Replace the Fruit theme's unused palette, radius and display-size tokens with a compact semantic palette and a complete system-font stack. Remove the portrait shadow/filter and use square component frames while preserving product artwork.
- Establish consistent typography, reading widths, section spacing, responsive layouts, primary/secondary actions and 44px minimum button targets.
- Unify exact-page and parent-section navigation indicators; make the skip link focus the main content. Improve text enlargement and reduced-motion behavior.
- Give form fields consistent square borders, padding and keyboard focus. Keep social links secondary to the enquiry form, and retain message content when enquiry intent changes.
- Improve Resume print margins, heading spacing and section pagination so teaching entries stay together.
- Derive API/UI/asset versions from installed package metadata generated from `pyproject.toml`; synchronize manifest, lockfile and `VERSION` at 1.1.1.
- Correct stale tests that still expected the retired Agent Keyboard listing, and resolve two existing import lint errors.
- Preview validation: `uv run pytest -q` (39 passed), `ruff check app tests` (zero errors), `ruff format --check app/main.py tests/test_revision.py tests/test_site.py`, and `git diff --check` passed. `node tests/visual-polish.cjs` passed 126 route/viewport checks, 18 accessibility scans and keyboard, form, print, reduced-motion and 200% text flows; zero accessibility violations, horizontal overflow, console errors or page exceptions. Desktop/mobile screenshots and both Resume PDF pages were visually reviewed and refined.
- Published application revision `ce0299b` through the existing bind mount and `docker restart pragith-web`. The manifest, installed package, public OpenAPI metadata, footer and asset URLs agree on 1.1.1; the public stylesheet bytes match the source (SHA-256 b59c3874078b9bb8ce85a2824e29c0a4580a8df8340c9a8bb63969d8d6a0c72e); this deployment uses the source commit as its revision, with no separate build counter.
- Live verification: `docker exec pragith-web uv run pytest -q` passed 39 tests. `SITE_URL=https://pragith.net AUDIT_DIR=/tmp/pragith-polish-live node tests/visual-polish.cjs` completed 126 responsive checks, 18 accessibility scans and all interaction flows with no overflow, accessibility violations or page exceptions. Live desktop/mobile screenshots were inspected. Its strict console gate failed on ten Google reCAPTCHA iframe messages (`requestStorageAccess: Permission denied`); reproduction in both isolated and normal Chromium profiles confirmed the source is Google's `/recaptcha/api2/anchor`. This external console issue remains unresolved; it is not suppressed by the test, and contact delivery was not exercised against production SMTP.

## 1.1.0 — 2026-10-02

- Add the missing Rajadharma product page with developer credit, accurate game descriptions and feedback/privacy information. Keep the canonical URL stable when app visits carry UTM attribution.
- Add a bounded JSON-only public HTTPS feedback proxy for native Rajadharma clients; forward to the fixed internal feedback service, preserve meaningful failure statuses and withhold internal connection details.
- Include the product page in the sitemap and add route, forwarding, body-limit and failure-path regression coverage.

## 1.0.1 — 2026-09-22

- Validation: 28 application tests, Ruff, ten live responsive page checks, teaching enquiry, retired-route redirects and removed-download check passed; zero browser runtime errors.

- Remove the product engineering-record sections and their service-page references; redirect their URLs to Projects.
- Remove the generic CSV exercise, rubric and downloads from Teaching.
- Keep dated teaching appointments, named programs, the official event link and contextual inquiry actions.


## 1.0.0 — 2026-09-22

- Restore dated career history, promotion, assistant ownership and teaching programs from the supplied resume.
- Add visible project entries, genuine responsive media and two source-backed product engineering records.
- Synchronize CallRenard scope with Vriksh; retain professional work as bounded experience summaries.
- Simplify navigation and adapt teaching/speaking enquiries while preserving entered text and attribution.
- Preserve Google Analytics, Clarity, reCAPTCHA and delivery configuration.
- Add a real GDG event and illustrative teaching exercise; document credential and enterprise evidence gaps internally.
- Validate 29 application tests, 90 responsive checks and 18 accessibility scans.


## 2026-09-22 — Main product order

- Order the main portfolio as Velvet, Fairway Golf Swing Analyzer, then CallRenard.
- Promote Golf to the main product placement while retaining its Experimental status.
- Review rendered desktop/mobile pages, tighten spacing and hierarchy, and simplify product copy.
- Replace long product lists with accessible tab selectors: all names remain visible, one detail panel opens at a time, arrow/Home/End keys work, and JavaScript-free pages retain all details.


## 2026-09-22 — Golf Swing Analyzer listing

- Publish Fairway in the existing project sections with a direct link to the live application.
- Describe local 2D tracking, saved summaries and skeleton replay; label analysis Experimental and state its validation limits.

## Unreleased

- Repositioned pragith.net as the personal authority website of Pragith Prakash, using the canonical title “AI Forward Deployed Engineer.”
- Added Home, About, Experience, Case Studies, Services, Teaching, Projects / Labs, Writing, Contact and printable Resume experiences.
- Centralized verified experience, certifications, capabilities, case studies and project maturity in one public content source.
- Added six anonymized case studies and removed unsupported legacy delivery metrics.
- Replaced AI Fleet and dashboard-product positioning with controlled AI systems and vendor-neutral executive BI services.
- Corrected Agent Keyboard to Prototype and Caffeinate-d to Beta with its actual source/release state.
- Added canonical URLs, Open Graph metadata, Person and Vriksh structured data, robots rules and a sitemap containing only live canonical routes.
- Added route, redirect, SEO, content-policy, project-status, pronoun and contact-form acceptance tests.
- Reworked the presentation from a card-led commercial landing page into a personal editorial portfolio with narrative sections and portrait photography.
- Restored the Fruit visual system—SF typography, white canvas, graphite text, Apple blue, frost-gray surfaces and restrained product-style polish—without restoring the commercial landing-page structure.
- Added Velvet IPTV Player as a Production project linked to velvet.plus.
- Restored conditional Google Analytics and Microsoft Clarity instrumentation from environment configuration, with regression coverage.
- Added automatic GA4 attribution to internal Contact links using standard UTM parameters, a `contact_cta_click` event, and source/CTA context preserved through form submission.
- Expanded the analytics Content Security Policy to cover Google Analytics and Microsoft Clarity collection endpoints.
- Restored source-aware Contact form prefilling for speaking, teaching, AI, platform and analytics journeys while preserving URL tags through submission.
- Corrected the contact protection to use the configured reCAPTCHA v3 key and validate both score and action; reCAPTCHA is now loaded only on the Contact page.
- Removed Headmaster from the public project portfolio.
- Removed the repeated small-label heading pattern from every public page and deleted its shared styling.
- Rewrote public page copy to use specific technologies, responsibilities, operating constraints and first-person experience instead of slogans or feature-list cadence.
- Replaced stacked homepage case studies with an accessible carousel supporting buttons, arrow keys, touch gestures and a live position indicator.
- Reduced shared hero, section and entry spacing to improve desktop reading density while retaining the Fruit typography, palette and portrait-led presentation.
- Replaced the horizontally scrolling mobile navigation with a labelled Menu/Close control and a two-column navigation panel.
- Increased the Fruit link-blue contrast on frost-gray surfaces to meet WCAG AA contrast requirements.
