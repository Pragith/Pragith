## 2026-10-12 — Portrait restoration 1.1.2

- [x] Restore the original effective portrait styling as explicitly requested.
- [x] Verify desktop/mobile rendering, 39 application tests and live version metadata; commit and push the restoration.
- [ ] Review every public page and its complete text for weak, generic or unsupported copy; report concrete revisions before changing copy.

## 2026-10-12 — Visual polish 1.1.1

- [x] Inspect the active source and live desktop/mobile rendering.
- [x] Consolidate styling, remove decorative treatment, and refine typography, spacing, square controls, navigation and forms.
- [x] Inspect generated screenshots, correct the theme font fallback and refine secondary actions.
- [x] Review and improve both pages of the printable Resume.
- [x] Pass 39 application tests, Ruff and 126 preview responsive checks with 18 clean accessibility scans.
- [x] Synchronize 1.1.1 product metadata and derive runtime versions from the manifest-generated package metadata.
- [x] Deploy through the existing bind mount and verify public rendering, asset version and installed package/API/UI metadata (1.1.1; application revision ce0299b).
- [x] Inspect live screenshots; pass 126 responsive checks, 18 accessibility scans and interaction flows. No horizontal overflow, page exceptions or accessibility violations.
- [ ] External console gate: Google reCAPTCHA's iframe logs storage-access denials in Chromium. The strict public browser test reports these and fails its console gate; retain anti-spam verification and track the external issue without suppressing it.
- [x] Commit the styling release (ce0299b) and publish the source and verification record to origin/pragith_2026.

## 2026-10-02 — Rajadharma support

- [x] Create the requested product page and canonical URL.
- [x] Add the native feedback proxy to the fixed game feedback service.
- [x] 38 application tests and Ruff pass; four public browser viewports pass with zero overflow/runtime errors. Public invalid feedback returns422 through the live backend without mail dispatch.
- [x] Publish website1.1.0; product page returns200 with stable canonical URL and SMTP feedback proxy reachable.
- [x] Commit and push verified source: 5b6068c.

- [x] Remove engineering-record sections from Home and Work, with redirects for the retired detail pages.
- [x] 1.0.1: Remove the generic sample exercise and its downloads; verify the public teaching page and enquiry path.

## 1.0.0 revision

- [x] Restore chronology, visible work, teaching programs and official event.
- [x] Reconcile CallRenard across both sites.
- [x] Validate form intent, keyboard navigation, print and responsive accessibility.
- [ ] Obtain issuer links and earned/expiry dates for five recorded credentials.
- [ ] Obtain an approved enterprise incident, design decision, tradeoff and operational outcome.

# Verification and publication follow-up

- [ ] `TODO_VERIFY`: Capture genuine screenshots from a macOS build of Caffeinate-d source version 0.2.0; keep its detail page noindexed until complete.
- [ ] `TODO_VERIFY`: Publish a matching signed Caffeinate-d release artifact before presenting a direct binary download.
- [ ] `TODO_VERIFY`: Approve specific public articles, recordings or podcast links before adding them to Writing.
- [ ] `TODO_VERIFY`: Approve any quantitative case-study outcomes beyond the multi-terabyte daily workload and hundreds-of-pipelines scale already supported by the current résumé.

## 2026-09-22 — Golf website listing

- [x] Add the experimental Fairway listing and live app link.
- [x] Verify and publish the updated pages: application tests passed; desktop/mobile public routes and live app links passed with zero browser errors.

## Main product order
- [x] Place Velvet first, Golf second and Renard third.
- [x] Implement compact product selectors across home and catalogue pages.
- [x] Verify and deploy product order, keyboard navigation and mobile layouts.
- [x] Inspect actual screenshots and improve density, typography and copy.
