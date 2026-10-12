/* Conservative STE-derived structural checks, not full dictionary certification. */
const fs = require("node:fs");
const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const pages = data.pages || data.snapshots;
const contractions =
  /\b(?:I|you|we|they|he|she|it)['’](?:m|re|ve|ll|d|s)\b|\b\w+n['’]t\b/gi;
const reviewedVerbs =
  /\b(?:investigat(?:e|es|ed|ing)|implement(?:s|ed|ing)?|troubleshoot(?:s|ed|ing)?|leverag(?:e|es|ed|ing)|utiliz(?:e|es|ed|ing))\b/gi;
const issues = [];
const sentences = [];
for (const page of pages) {
  for (const unit of page.units) {
    if (!["P", "LI", "DD"].includes(unit.tag)) continue;
    const parts = unit.text.split(/(?<=[.!?])\s+/).filter(Boolean);
    if (unit.tag === "P" && parts.length > 6)
      issues.push({ route: page.route, rule: "6.6", text: unit.text });
    for (const text of parts) {
      const procedural =
        unit.procedural ||
        /^(?:Open|Clone|Build|Run|Use|Tell|Describe|Include|Send|Try|Start|Choose|Design|Evaluate|Document|Report|Select|Enter|Make)\b/.test(
          text,
        );
      const limit = procedural ? 20 : 25;
      const words = text.trim().split(/\s+/).length;
      sentences.push({
        route: page.route,
        type: procedural ? "instruction" : "description",
        words,
        limit,
        text,
      });
      if (words > limit)
        issues.push({
          route: page.route,
          rule: procedural ? "5.1" : "6.3",
          words,
          limit,
          text,
        });
      for (const match of text.matchAll(contractions))
        issues.push({ route: page.route, rule: "4.2", match: match[0], text });
      for (const match of text.matchAll(reviewedVerbs))
        issues.push({
          route: page.route,
          rule: "1.1 dictionary follow-up",
          match: match[0],
          text,
        });
    }
  }
  for (const text of [
    page.title,
    ...page.metadata
      .filter((item) =>
        ["description", "og:description", "twitter:description"].includes(
          item.name,
        ),
      )
      .map((item) => item.content),
    ...page.links.map((item) => item.text),
    ...page.images.map((item) => item.alt),
    ...Object.values(page.form || {}),
  ]) {
    for (const match of text.matchAll(contractions))
      issues.push({ route: page.route, rule: "4.2", match: match[0], text });
  }
}
const report = {
  standard: "ASD-STE100 Issue 9 (2025-01-15)",
  source: "https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf",
  scope:
    "STE-derived structural and selected-word checks; whitespace counts conservatively include all names. Manual editing handles voice, meaning, steps and terminology. This is not complete dictionary/part-of-speech conformity certification.",
  pages: pages.length,
  sentences: sentences.length,
  longestInstruction: Math.max(
    ...sentences
      .filter((item) => item.type === "instruction")
      .map((item) => item.words),
  ),
  longestDescription: Math.max(
    ...sentences
      .filter((item) => item.type === "description")
      .map((item) => item.words),
  ),
  issues,
  sentenceChecks: sentences,
};
fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 2) + "\n");
console.log(
  JSON.stringify({
    pages: report.pages,
    sentences: report.sentences,
    issues: report.issues.length,
    longestInstruction: report.longestInstruction,
    longestDescription: report.longestDescription,
  }),
);
if (issues.length) {
  console.error(JSON.stringify(issues, null, 2));
  process.exitCode = 1;
}
