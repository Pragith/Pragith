const {
  chromium,
} = require("/srv/docker/labs/agent-fleet/apps/golf/node_modules/playwright");
const fs = require("node:fs");
const { execFileSync } = require("node:child_process");
const site = process.env.SITE_URL || "http://127.0.0.1:4784";
const destination = process.argv[2] || "/tmp/pragith-copy-snapshot.json";
(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage();
  const response = await page.request.get(site + "/sitemap.xml");
  const paths = [
    ...new Set(
      [
        ...(await response.text()).matchAll(
          /<loc>https:\/\/pragith.net([^<]*)<\/loc>/g,
        ),
      ].map((m) => m[1]),
    ),
  ];
  await page.goto(site + "/case-studies");
  paths.push(
    ...(await page
      .locator('main a[href^="/case-studies/"]')
      .evaluateAll((els) => els.map((e) => e.getAttribute("href")))),
  );
  paths.push(
    "/projects/caffeinate-d",
    "/contact?engagement_type=Teaching%20%2F%20workshop",
    "/contact?engagement_type=Speaking%20engagement",
    "/contact?engagement_type=Hourly%20engineering",
    "/copy-audit-missing-page",
  );
  const snapshots = [];
  const fixtures = JSON.parse(
    execFileSync("uv", ["run", "python", "scripts/render_copy_states.py"], {
      encoding: "utf8",
      env: {
        ...process.env,
        GA_TAG: "",
        CLARITY_PROJECT_ID: "",
        RECAPTCHA_SITE_KEY: "",
      },
    }),
  );
  paths.push(...fixtures.map((f) => f.route));
  await page.route("**/__copy_fixture/**", async (route) => {
    const index = Number(
      new URL(route.request().url()).pathname.split("/").pop(),
    );
    await route.fulfill({
      status: 200,
      contentType: "text/html",
      body: fixtures[index].html,
    });
  });
  for (const route of paths) {
    const fixtureIndex = fixtures.findIndex((f) => f.route === route);
    const r = await page.goto(
      fixtureIndex >= 0
        ? site + "/__copy_fixture/" + fixtureIndex
        : site + route,
      { waitUntil: "domcontentloaded" },
    );
    snapshots.push({
      route,
      status: r.status(),
      sourceOnly: fixtureIndex >= 0,
      ...(await page.evaluate(() => ({
        title: document.title,
        structuredData: [
          ...document.querySelectorAll('script[type="application/ld+json"]'),
        ].map((e) => JSON.parse(e.textContent)),
        metadata: [
          ...document.querySelectorAll(
            'meta[name="description"],meta[property^="og:"],meta[name^="twitter:"]',
          ),
        ].map((e) => ({
          name: e.getAttribute("name") || e.getAttribute("property"),
          content: e.content,
        })),
        text: document.querySelector("main").innerText,
        units: [
          ...document.querySelectorAll(
            "main h1,main h2,main h3,main p,main li,main dt,main dd,main label,main option,main button,main pre,main .status,main .tag",
          ),
        ]
          .filter((e) => !e.closest(".honeypot"))
          .map((e) => ({
            tag: e.tagName,
            text: e.innerText.trim(),
            procedural: !!e.closest("ol"),
          }))
          .filter((e) => e.text),
        links: [...document.querySelectorAll("main a")].map((e) => ({
          text: e.textContent.trim(),
          href: e.getAttribute("href"),
          label: e.getAttribute("aria-label"),
        })),
        images: [...document.querySelectorAll("main img")].map((e) => ({
          src: e.getAttribute("src"),
          alt: e.alt,
        })),
        nav: document.querySelector("nav").innerText,
        footer: document.querySelector("footer").innerText,
        form: document.querySelector("#message")
          ? {
              placeholder: document.querySelector("#message").placeholder,
              value: document.querySelector("#message").value,
            }
          : null,
      }))),
    });
  }
  fs.writeFileSync(
    destination,
    JSON.stringify({ captured: new Date().toISOString(), snapshots }, null, 2),
  );
  console.log(
    JSON.stringify({
      pages: snapshots.length,
      units: snapshots.reduce((n, p) => n + p.units.length, 0),
      mainWords: snapshots.reduce((n, p) => n + p.text.split(/\s+/).length, 0),
    }),
  );
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
