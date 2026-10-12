# pragith.net

The personal professional website of Pragith Prakash, AI Forward Deployed Engineer, consultant and educator.

The site is a server-rendered FastAPI application with a Jinja2 frontend, the Fruit theme and a Docker deployment.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Jinja2
- **Frontend**: HTML5, a shared CSS stylesheet and theme tokens
- **Infrastructure**: Docker, Docker Compose
- **Package Management**: [uv](https://github.com/astral-sh/uv)
- **Security**: Uvicorn, security headers, rate limiting and Google reCAPTCHA v3

## Project Structure

```
pragith-net/
├── app/
│   ├── main.py            # Application entrypoint & routes
│   ├── config.py          # Environment configuration (Pydantic)
│   ├── services/          # Business logic
│   ├── templates/         # Jinja2 HTML templates
│   ├── static/            # Static assets
│   └── content/           # Flat-file content (Blog posts)
├── Dockerfile             # Multi-stage production build (uses uv)
├── docker-compose.yml     # Orchestration
├── pyproject.toml         # Python dependencies
└── tailwind.config.js     # CSS configuration
```

## Local Development (with uv)

We use `uv` for fast, reliable dependency management.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for full stack run)
- [uv](https://github.com/astral-sh/uv) (for local python dev)
- Node.js (optional, only if editing CSS locally)

### Option 1: Full Stack (Docker)

```bash
cp .env.example .env
docker-compose up --build
```
Access at `http://localhost:8000`.

### Option 2: Local Python Dev

To run the backend locally without Docker:

1.  **Sync Dependencies**:
    ```bash
    uv sync
    ```
    This creates a virtual environment in `.venv` and installs all dependencies.

2.  **Activate Environment**:
    ```bash
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Run Development Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

### CSS development and visual verification

The active frontend loads `app/static/site.css` for layout and components, then
`/theme.css` for the selected theme's tokens and font metadata. Edit those sources
directly; this frontend does not need a Tailwind build. Legacy Tailwind sources
remain for historical templates and are not loaded by the current portfolio.

Run `uv run pytest -q`, `ruff check app tests`, and start a preview with
`uv run uvicorn app.main:app --host 127.0.0.1 --port 4784`.

Run `node tests/visual-polish.cjs` for responsive checks, accessibility scans,
keyboard/form interactions, text enlargement and printable Resume verification.
The script uses the fleet host's Playwright and axe-core installations. Override
`SITE_URL` to verify the public deployment and `AUDIT_DIR` to choose the output
folder. Screenshots, a Resume PDF and results are saved outside the repository.
Inspect the screenshots as well as the automated results. The public test keeps
its console gate strict: Google's reCAPTCHA iframe currently emits storage-access
denial messages in Chromium, so the public run fails that gate even when all
layout, accessibility and interaction checks pass. See the 1.1.1 changelog for
the reproduced limitation; production contact delivery is not tested by this script.

Internal Python package metadata comes from `pyproject.toml`. Keep `VERSION`
and `uv.lock` synchronized when the package changes. Website copy releases use
dates and source commits; they do not introduce public website SemVer.
The website has no visible version label. Stylesheet URLs use a content-derived asset revision; internal package metadata stays separate from website releases.

### Copy checks

The fleet clone of `Pragith/linkedin-slop-detector` provides the unchanged 61-rule
matcher. The checker pins revision `ba39ed51c951d4e743c6b3318aae8c7ceb386c7f`.
It reports all raw matches, even below scoring thresholds, and fails on unresolved
matches. The one reviewed exception is the separator in the owner-supplied
“Claude Certified Architect – Foundations” credential. The raw match remains
in the report; no detector rule or threshold is changed.

```bash
node scripts/capture_copy.cjs /tmp/pragith-copy.json
node scripts/check_copy.cjs /tmp/pragith-copy.json /tmp/pragith-signals.json
node scripts/check_ste.cjs /tmp/pragith-copy.json /tmp/pragith-ste.json
```

Set `SITE_URL=https://pragith.net` for the public capture. The capture also renders
four source-only success/error templates without mail dispatch. These are labelled
as fixtures; they do not establish successful production contact delivery.
Set `DETECTOR_DIR` if the reference clone is elsewhere; its npm dependencies must
be installed. No detector rule or threshold is changed for this website.

The STE pass uses [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).
It combines manual editing with conservative sentence-length, paragraph-length,
contraction and selected-word checks. Instructions use separate steps. Product
names and technical terminology retain their meanings. This is a practical writing
pass, not certification of complete dictionary or part-of-speech conformity.

Before/after evidence and the full second review are stored in
`docs/copy-review-2026-10-12/final/`. The original 1.1.2 review remains unchanged.

## deployment

### Docker Build

```bash
docker build -t pragith-net:latest .
docker run -p 8000:8000 --env-file .env pragith-net:latest
```

## License

Proprietary. All rights reserved.

## Golf listing verification — 2026-09-22

`docker exec pragith-web uv run pytest -q`: 19 passed. The public homepage and Projects page passed browser checks at 390px and 1440px widths: Experimental status, live app links, successful app navigation and horizontal overflow. Zero console errors or page exceptions. Published through the existing bind mount and `docker restart pragith-web`.

Repeatable cross-site check: `node /srv/docker/labs/agent-fleet/scripts/verification/verify_golf_listings.cjs`.
