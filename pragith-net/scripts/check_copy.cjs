/* Use the detector's unmodified TypeScript core; no copied regex implementation. */
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { execFileSync } = require("node:child_process");
const detectorPath =
  process.env.DETECTOR_DIR ||
  "/srv/docker/labs/agent-fleet/apps/linkedin-slop-detector";
const esbuild = require(path.join(detectorPath, "node_modules/esbuild"));
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "pragith-detector-"));
const bundle = path.join(temporary, "core.cjs");
esbuild.buildSync({
  stdin: {
    contents: `export {DEFAULT_RULES} from './src/rules/defaultRules';
      export {executeRules, MAX_SCAN_LENGTH} from './src/core/matcher';
      export {SlopDetector} from './src/core/detector';
      export {DEFAULT_SETTINGS} from './src/storage/defaultSettings';`,
    resolveDir: detectorPath,
    loader: "ts",
  },
  outfile: bundle,
  platform: "node",
  bundle: true,
  format: "cjs",
});
const {
  DEFAULT_RULES,
  executeRules,
  MAX_SCAN_LENGTH,
  SlopDetector,
  DEFAULT_SETTINGS,
} = require(bundle);
const revision = execFileSync(
  "git",
  ["-C", detectorPath, "rev-parse", "HEAD"],
  { encoding: "utf8" },
).trim();
const expected = "ba39ed51c951d4e743c6b3318aae8c7ceb386c7f";
if (revision !== expected || DEFAULT_RULES.length !== 61)
  throw Error("Review the changed detector revision before using this gate.");
const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const pages = data.pages || data.snapshots;
const detector = new SlopDetector([...DEFAULT_RULES]);
const rows = [];
const structuredStrings = (value) => {
  if (typeof value === "string") return /^https?:/.test(value) ? [] : [value];
  if (Array.isArray(value)) return value.flatMap(structuredStrings);
  if (value && typeof value === "object")
    return Object.values(value).flatMap(structuredStrings);
  return [];
};
for (const page of pages) {
  const surfaces = [
    { name: "body", text: page.text },
    { name: "title", text: page.title },
    { name: "navigation", text: page.nav },
    { name: "footer", text: page.footer },
    ...page.metadata.map((item) => ({ name: item.name, text: item.content })),
    ...page.links.flatMap((item) => [
      { name: "link", text: item.text },
      { name: "accessible label", text: item.label || "" },
    ]),
    ...page.images.map((item) => ({ name: "image alt", text: item.alt })),
    ...(page.form
      ? Object.entries(page.form).map(([name, text]) => ({
          name: "form " + name,
          text,
        }))
      : []),
    ...structuredStrings(page.structuredData).map((text) => ({
      name: "structured data",
      text,
    })),
  ];
  for (const surface of surfaces) {
    if (surface.text.length > MAX_SCAN_LENGTH)
      throw Error(`Scan would truncate ${page.route} ${surface.name}`);
    const rawMatches = executeRules(surface.text, [...DEFAULT_RULES]);
    const result = detector.detect(surface.text, DEFAULT_SETTINGS);
    // Preserve the owner's exact credential name. Report its separator match,
    // without suppressing the raw matcher output or changing detector rules.
    const credential = "Claude Certified Architect – Foundations";
    const credentialOffset = surface.text.indexOf(credential);
    const reviewedMatches = rawMatches
      .filter(
        (match) =>
          page.route === "/resume" &&
          surface.name === "body" &&
          credentialOffset >= 0 &&
          match.ruleId === "structural-em-dash-spam" &&
          match.start === credentialOffset + credential.indexOf("–"),
      )
      .map((match) => ({
        ...match,
        disposition:
          "Owner-supplied proper-name separator; not rhetorical dash density.",
      }));
    rows.push({
      route: page.route,
      surface: surface.name,
      characters: surface.text.length,
      rawMatches,
      reviewedMatches,
      score: result.score,
      qualifiedMatches: result.matches,
    });
  }
}
// Browser-only error messages are not rendered until their error path runs.
for (const text of [
  "Verification is still loading. Please try again.",
  "Verification could not be completed. Please try again.",
  "Menu",
  "Close",
  "Skip to content",
]) {
  const rawMatches = executeRules(text, [...DEFAULT_RULES]);
  const result = detector.detect(text, DEFAULT_SETTINGS);
  rows.push({
    route: "source-state:shared-and-client-errors",
    surface: "message",
    characters: text.length,
    rawMatches,
    score: result.score,
    qualifiedMatches: result.matches,
  });
}
const report = {
  detectorRevision: revision,
  ruleCount: DEFAULT_RULES.length,
  rules: DEFAULT_RULES.map((rule) => ({
    id: rule.id,
    name: rule.name,
    category: rule.category,
    pattern: rule.pattern,
    flags: rule.flags,
    densityThreshold: rule.densityThreshold,
    rawMatches: rows.reduce(
      (total, row) =>
        total +
        row.rawMatches.filter((match) => match.ruleId === rule.id).length,
      0,
    ),
  })),
  pages: pages.length,
  surfaces: rows.length,
  rawMatches: rows.reduce((total, row) => total + row.rawMatches.length, 0),
  qualifiedMatches: rows.reduce(
    (total, row) => total + row.qualifiedMatches.length,
    0,
  ),
  reviewedProperNameMatches: rows.reduce(
    (total, row) => total + (row.reviewedMatches?.length || 0),
    0,
  ),
  unresolvedRawMatches: rows.reduce(
    (total, row) =>
      total + row.rawMatches.length - (row.reviewedMatches?.length || 0),
    0,
  ),
  rows,
};
fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 2) + "\n");
console.log(
  JSON.stringify({
    rules: report.ruleCount,
    pages: report.pages,
    surfaces: report.surfaces,
    rawMatches: report.rawMatches,
    qualifiedMatches: report.qualifiedMatches,
    reviewedProperNameMatches: report.reviewedProperNameMatches,
    unresolvedRawMatches: report.unresolvedRawMatches,
  }),
);
if (report.unresolvedRawMatches) {
  console.error(
    JSON.stringify(
      rows.filter((row) => row.rawMatches.length),
      null,
      2,
    ),
  );
  process.exitCode = 1;
}
