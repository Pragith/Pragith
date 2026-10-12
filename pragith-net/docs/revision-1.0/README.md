# pragith.net 1.0.0 review

22 September 2026. Baseline 3f81018. Review: http://127.0.0.1:4784. Target: https://pragith.net.

## Claim reconciliation

| Claim | Source | Decision |
|---|---|---|
| Employers, roles, promotion, eighteen-month assistant ownership | Owner-supplied resume | Restore chronology; preserve confidential client boundaries |
| Multi-terabyte datasets and hundreds of pipelines | Supplied resume | Estate context, separate from personal outcome |
| Fairway one-frame pipeline | apps/golf/src/vision/pipeline.ts | Concrete decision, source excerpt and timing tradeoff; no phone performance claim |
| CallRenard call states | renard/backend/app/services/call_flow.py, call_state_machine.py, agent_scripts.py at 1220a14 | Shared development/demo facts; sample formatter output, no verified live-call claim |
| Teaching appointments and programs | Supplied resume | Named dates; new exercise explicitly illustrative |
| GDG Edmonton session | Official event JSON-LD retained in gdg-event.json | Speaker and 1 October 2022 date |
| Certification status | Issuer/date records unavailable | Omit status claims; names and missing fields retained in claim-register.json |
| Enterprise outcomes | Summary-level source only | Keep six concise professional summaries; do not invent incidents |

CallRenard JSON matches /srv/docker/vriksh/ca/app/product-facts.json. Check with scripts/sync_product_facts.py TARGET --check. Reachability does not establish telephone workflow execution.

## Route and copy changes

Existing URLs remain. Main navigation is Work (/case-studies), Experience, Teaching, About, Contact; Resume is a utility. Projects, Services and Writing remain linked from the footer and relevant sections. Two new routes: /case-studies/fairway-frame-pipeline and /case-studies/callrenard-call-states. Agent Keyboard retains its path and adds a return link.

Professional experience follows the homepage introduction. All five projects are visible, Fairway first. Generic cases now show bounded responsibilities rather than repetitive results/lessons. Teaching/speaking forms adapt headings, labels and helpers without overwriting entered messages. Caffeinate-d editorial readiness prose is removed. Writing contains a dated official event.

## Assets and screenshots

Fairway: saved skeleton replay from a test clip, timing disabled. Velvet: genuine film-selection screen with attributed Big Buck Bunny demonstration content. Agent Keyboard: actual browser prototype. Caffeinate-d: source/build artifact pending macOS capture. No invented professional artifacts.

Before: before-1440.png and before-390.png. After: 1440/390-0.png (home), -5.png (projects), -7.png (Fairway), -15.png (teaching contact). resume.pdf: two-page A4 print output.

## Verification

- pytest -q -p no:cacheprovider in pragith-site-review: 29 passed.
- ruff check changed Python modules/tests/scripts: passed; git diff --check passed.
- node tests/revision-browser.cjs: 90 page checks at 360/390/768/1024/1440 pixels, 18 axe scans, zero violations and page exceptions.
- Flows: teaching inquiry, speaking selection preserving message, required-field validation, menu Escape/focus, prototype return, resume print, 200% text and reduced motion.
- Form success/failure use safe test mocks. Production inquiries were never submitted. SMTP delivery remains untested.
- Linux server, headless Chromium 145 desktop emulation. Physical devices and field performance were not measured.

## Remaining source questions

An enterprise case needs publishable source/destination types, a concrete failure, the chosen design and tradeoff, and observed operational behavior. Credentials need issuer URLs/IDs and earned/expiry dates. Caffeinate-d needs a genuine macOS capture and signed binary release before advertising downloads. These gaps are kept out of public review commentary.

## Production verification

Deployed application revision d45ab49, release 1.0.0, at https://pragith.net on 22 September 2026. Sixteen public route/viewport checks at 390 and 1440 passed with zero page exceptions. Google Analytics is present on every checked route; reCAPTCHA is present on the checked contact contexts. Source candidates, intrinsic image sizes and results are retained in production-results.json. live-390.png and live-1440.png show the served homepage. Production environment and mailer configuration were unchanged.
