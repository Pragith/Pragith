/* Run from pragith-net. Override SITE_URL and AUDIT_DIR for deployment checks. */
const { chromium } = require('/srv/docker/labs/agent-fleet/apps/golf/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const version = fs.readFileSync('VERSION', 'utf8').trim();
const site = process.env.SITE_URL || 'http://127.0.0.1:4784';
const output = process.env.AUDIT_DIR || '/tmp/pragith-polish-preview';
const axe = '/srv/docker/family/pragith/superset/superset-frontend/node_modules/axe-core/axe.min.js';
const routes = ['/', '/about', '/experience', '/teaching', '/contact', '/resume', '/projects', '/case-studies', '/case-studies/ai-mlops-automation', '/services', '/services/ai-systems', '/services/executive-bi', '/writing', '/business', '/privacy', '/legal', '/apps/rajadharma', '/projects/caffeinate-d'];
(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  const errors = [];
  const scans = [];
  const checks = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  for (const width of [360, 390, 690, 701, 900, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of routes) {
      const response = await page.goto(site + route, { waitUntil: 'domcontentloaded' });
      assert.equal(response.status(), 200, route);
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.locator('h1').count(), 1, route);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `overflow ${width} ${route}`);
      assert.equal(await page.locator('.release-version').innerText(), `v${version}`);
      assert.equal(await page.evaluate(() => [...document.querySelectorAll('body, .btn, input, select, textarea')].every(el => getComputedStyle(el).fontFamily.includes('system-ui'))), true, `font fallback ${route}`);
      assert.equal(await page.evaluate(() => [...document.querySelectorAll('.btn, .nav-toggle, .field input, .field select, .field textarea, .home-portrait, .project-visual img, .artifact')].every(el => getComputedStyle(el).borderRadius === '0px')), true, `square corners ${route}`);
      assert.equal(await page.evaluate(() => [...document.querySelectorAll('.btn')].every(el => el.getBoundingClientRect().height >= 44)), true, `button target ${route}`);
      if ([390, 1440].includes(width) && ['/', '/contact', '/projects', '/experience', '/teaching', '/case-studies'].includes(route)) {
        await page.screenshot({ path: path.join(output, `${width}-${route === '/' ? 'home' : route.slice(1)}.png`), fullPage: true });
      }
      if (width === 390) {
        await page.addScriptTag({ path: axe });
        const violations = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] } })).violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) })));
        scans.push({ route, violations });
      }
      checks.push({ width, route });
    }
  }
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto(site + '/');
  await page.keyboard.press('Tab');
  assert.equal(await page.locator('.skip-link').evaluate(el => el === document.activeElement), true);
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('main').evaluate(el => el === document.activeElement), true);
  await page.locator('.nav-toggle').click();
  assert.equal(await page.locator('.nav-links').isVisible(), true);
  await page.screenshot({ path: path.join(output, '390-menu.png') });
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('.nav-links').isVisible(), false);
  assert.equal(await page.locator('.nav-toggle').evaluate(el => el === document.activeElement), true);
  await page.goto(site + '/teaching');
  await page.getByRole('link', { name: 'Discuss a course or workshop', exact: true }).click();
  assert.equal(await page.locator('#engagement_type').inputValue(), 'Teaching / workshop');
  await page.locator('#message').fill('Please keep my workshop context.');
  await page.locator('#engagement_type').selectOption('Speaking engagement');
  assert.equal(await page.locator('h1').innerText(), 'Invite me to speak.');
  assert.equal(await page.locator('#message').inputValue(), 'Please keep my workshop context.');
  await page.getByRole('button', { name: 'Send enquiry' }).click();
  assert.equal(await page.locator('#name:invalid').count(), 1);
  await page.locator('#name').focus();
  assert.notEqual(await page.locator('#name').evaluate(el => getComputedStyle(el).outlineStyle), 'none');
  await page.goto(site + '/case-studies/ai-mlops-automation');
  assert.equal(await page.locator('.nav-link[data-section-current="true"]').innerText(), 'Work');
  await page.goto(site + '/resume');
  await page.emulateMedia({ media: 'print' });
  assert.equal(await page.locator('.global-nav').isVisible(), false);
  await page.pdf({ path: path.join(output, 'resume.pdf'), format: 'A4', printBackground: true });
  await page.emulateMedia({ media: 'screen', reducedMotion: 'reduce' });
  for (const width of [390, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of ['/', '/contact', '/projects', '/resume']) {
      await page.goto(site + route);
      await page.addStyleTag({ content: 'html { font-size: 200%; }' });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `text resize ${width} ${route}`);
      assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), 'auto');
    }
  }
  const result = { checks: checks.length, scans, errors, flows: ['menu open/escape', 'skip link', 'contextual contact', 'intent preserves message', 'required field validation', 'keyboard focus', 'section navigation', 'resume print', '200% text', 'reduced motion'] };
  fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(result, null, 2));
  await browser.close();
  console.log(JSON.stringify({ checks: result.checks, accessibilityScans: scans.length, violations: scans.filter(s => s.violations.length), errors }, null, 2));
  assert.equal(errors.length, 0, 'browser errors');
  assert.deepEqual(scans.filter(s => s.violations.length), [], 'accessibility violations');
})().catch(error => { console.error(error); process.exit(1); });
