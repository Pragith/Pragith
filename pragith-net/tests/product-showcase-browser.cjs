const { chromium } = require('/srv/docker/labs/agent-fleet/apps/golf/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const base = process.env.SITE_URL || 'http://127.0.0.1:4784';
const out = process.env.EVIDENCE_DIR || '/tmp/pragith-showcase-review';
(async () => {
  fs.mkdirSync(out, {recursive: true});
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const errors = [], checks = [];
  try {
    const page = await browser.newPage();
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    for (const width of [320, 390, 768, 1024, 1440]) {
      await page.setViewportSize({width, height: 936});
      for (const path of ['/', '/projects', '/teaching', '/about', '/projects/caffeinate-d']) {
        assert.equal((await page.goto(base + path, {waitUntil: 'networkidle'})).status(), 200);
        assert.equal(await page.locator('h1').count(), 1);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${width} ${path}`);
        await page.locator('img').evaluateAll(es => es.forEach(e => e.loading = 'eager'));
        await page.locator('img').evaluateAll(es => Promise.all(es.map(e => e.decode())));
        if (['/', '/projects', '/about'].includes(path)) {
          const intro = page.locator('main').getByRole('link', {name: 'Vriksh', exact: true});
          assert.equal(await intro.getAttribute('href'), 'https://vriksh.ca/');
          assert.ok((await page.locator('main').innerText()).includes('I founded and run Vriksh'));
        }
        if (['/', '/projects'].includes(path)) {
          const golf = page.getByTestId('project-golf-swing-analyzer');
          assert.equal(await golf.getByRole('link', {name: 'Open Golf Simulator', exact: false}).getAttribute('href'), 'https://sim.aperture.golf/');
          assert.ok((await golf.innerText()).includes('aim, choose a club and set shot power'));
        }
        if (path === '/') {
          const intro = await page.getByTestId('studio-intro').boundingBox();
          const hero = await page.locator('.home-hero').boundingBox();
          assert.ok(intro.y >= hero.y && intro.y + intro.height <= hero.y + hero.height);
          assert.deepEqual(await page.locator('[data-testid^="project-"] h3').allTextContents(), ['Quantum Lab', 'Aperture Golf', 'Jasoos']);
          assert.equal(await page.getByRole('link', {name: 'Start Quantum Lab', exact: false}).getAttribute('href'), 'https://learnquantum.science/');
          assert.equal(await page.getByRole('link', {name: 'Open swing analyzer', exact: false}).getAttribute('href'), 'https://analyze.aperture.golf/');
          await page.getByRole('link', {name: 'All products and experiments', exact: false}).click();
          assert.equal(new URL(page.url()).pathname, '/projects');
        }
        if (path === '/' || path === '/projects') {
          assert.equal(await page.locator('[data-testid^="project-"]').count(), 9);
          assert.equal(await page.locator('[data-testid="project-callrenard"] .project-visual').count(), 0);
          assert.equal(await page.locator('[data-testid="project-caffeinate-d"] .project-visual').count(), 0);
          assert.equal(await page.locator('[data-testid="project-callrenard"] a').getAttribute('href'), 'https://vriksh.ca/apps/callrenard');
          for (const slug of ['quantum-lab', 'golf-swing-analyzer', 'jasoos', 'velvet', 'rajadharma', 'barnone']) {
            const image = page.getByTestId('project-' + slug).locator('.project-visual > a');
            const href = await image.getAttribute('href');
            assert.equal((await page.request.get(base + href)).status(), 200);
          }
          await page.getByRole('link', {name: 'Source and build instructions', exact: false}).click();
          assert.equal(new URL(page.url()).pathname, '/projects/caffeinate-d');
          assert.ok(await page.getByRole('heading', {name: 'Build from source'}).isVisible());
        }
        await page.goto(base + path, {waitUntil: 'networkidle'});
        if (path === '/teaching') assert.equal(await page.getByRole('link', {name: 'Start Quantum Foundations', exact: false}).getAttribute('href'), 'https://learnquantum.science/');
        if (path === '/about') assert.ok((await page.locator('main').innerText()).includes('Website version 1.2.1'));
        await page.addScriptTag({path: '/srv/docker/family/pragith/superset/superset-frontend/node_modules/axe-core/axe.min.js'});
        const violations = await page.evaluate(async () => (await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}})).violations.map(v => ({id: v.id, targets: v.nodes.map(n => n.target)})));
        assert.deepEqual(violations, [], `${width} ${path}`);
        assert.equal(await page.locator('button, .btn, .lab-example').evaluateAll(es => es.every(e => getComputedStyle(e).borderTopLeftRadius === '0px')), true);
        if ([390, 1440].includes(width) && ['/', '/projects', '/teaching'].includes(path)) await page.screenshot({path: `${out}/${width}-${path.slice(1) || 'home'}.png`, fullPage: true});
        checks.push({width, path, accessibilityViolations: 0});
      }
    }
    await page.setViewportSize({width:390, height:936});
    await page.goto(base + '/');
    await page.getByRole('button', {name:'Menu', exact:true}).click();
    await page.getByRole('link', {name:'Teaching', exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/teaching');
    for (const path of ['/', '/projects', '/teaching']) {
      await page.goto(base + path);
      await page.addStyleTag({content:'html {font-size:200%!important;}'});
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, '200% ' + path);
    }
    assert.deepEqual(errors, []);
    fs.writeFileSync(`${out}/results.json`, JSON.stringify({base, checks, errors, flows:['home-to-projects', 'nine-grouped-projects', 'screenshot-links', 'tools-build-instructions', 'teaching-course-link', 'mobile-menu', '200%-text-reflow']}, null, 2));
    console.log(JSON.stringify({checks:checks.length, accessibilityViolations:0, errors}));
  } finally { await browser.close(); }
})().catch(e => {console.error(e); process.exitCode = 1;});
