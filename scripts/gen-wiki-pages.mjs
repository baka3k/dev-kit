#!/usr/bin/env node
/**
 * Generate compact wiki guides for skills that do not have one yet.
 *
 * Every page is derived from the skill's own SKILL.md: the description, the
 * argument-hint, the "do not use" boundaries, and the section outline. Nothing
 * is invented — the only authored data here is the one-line Vietnamese summary
 * and the related-skill list per page.
 *
 * Pages already present are left untouched, including hand-written deep dives:
 * only pages carrying the generator marker are rewritten. Use --adopt <skill> to
 * explicitly take over a hand-written page (it will be replaced by the template).
 *
 * Usage: node scripts/gen-wiki-pages.mjs [--adopt <skill> ...] [--check]
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CHECK = process.argv.includes("--check");
const ADOPT = (() => {
  const i = process.argv.indexOf("--adopt");
  return i === -1 ? new Set() : new Set(process.argv.slice(i + 1).filter((a) => !a.startsWith("--")));
})();

const SKIP = new Set(["dev-shared"]);

/** Vietnamese one-line summaries (English comes from the frontmatter description). */
const SUMMARY_VI = {
  "hi-api-contract-discovery":
    "Sinh draft hợp đồng API HTTP và bất đồng bộ (OpenAPI/AsyncAPI): endpoint, message, schema, auth, lỗi, consumer/provider — chỉ là draft có bằng chứng.",
  "hi-behavior-modeling":
    "Mô hình hoá hành vi kỹ thuật dưới dạng sequence, activity, state-machine và event-flow; cần anchor use-case hoặc entry-point.",
  "hi-brainstorm":
    "Hội đồng chuyên gia độc lập: sinh phương án cạnh tranh, phản biện, chấm điểm có trọng số trước khi triển khai.",
  "hi-chrome-devtools":
    "Tự động hoá trình duyệt bằng script Puppeteer CLI với phiên lưu bền: screenshot, network, performance, scraping, form, auth.",
  "hi-command-spec-discovery":
    "Sinh draft đặc tả lệnh/protocol wire-format: trường APDU/TLV, framing CLA/INS/P1/P2/Lc/Le, opcode, status word.",
  "hi-cortex":
    "Cài đặt và vận hành Cortex Harness: cấu hình, đồng bộ code/doc, hạ tầng database và vòng đời MCP cho graph/vector retrieval.",
  "hi-cross-artifact-validation":
    "Kiểm tra nhất quán chỉ-đọc giữa các output discovery: ID ổn định, actor/auth, state lifecycle, schema; không sửa artifact nguồn.",
  "hi-data-model-discovery":
    "Sinh draft mô hình dữ liệu logic và vật lý, ERD, từ điển dữ liệu, ownership, vòng đời, độ nhạy cảm và khoảng trống migration.",
  "hi-document-lifecycle":
    "Vòng đời tài liệu cho một domain: generate → clarify/refine → review/update, có pause/resume và chỉ một generator mỗi lượt.",
  "hi-document-refinement":
    "Tìm mơ hồ, thiếu thuật ngữ, thiếu ngữ nghĩa và Mermaid chưa đủ đặc tả; áp dụng câu trả lời đã xác thực vào bản candidate tách biệt.",
  "hi-document-review-resolution":
    "Gán đúng một disposition cho mỗi comment review và áp dụng thay đổi được chấp nhận một cách idempotent.",
  "hi-maintenance-docs":
    "Điều phối trọn bộ tài liệu bảo trì có bằng chứng qua 9 stage: recon/audit, module summary, use case, API/data/command, behavior, validation, refinement, review.",
  "hi-module-summary-report":
    "Tổng hợp artifact recon/audit sẵn có thành tóm tắt kiến trúc, phân tích theo module và đánh giá rủi ro.",
  "hi-repo-recon":
    "Lập bản đồ repository lạ: inventory module, entry-point map và catalog hàm chính; chỉ tạo bằng chứng cấu trúc.",
  "hi-repowiki":
    "Sinh hoặc cập nhật wiki repository ở /repowiki/: kiến trúc, cài đặt, cấu hình, CLI/build, API, test, deploy, module.",
  "hi-scout":
    "Thu thập bằng chứng có truy vết từ code, tài liệu dự án và nguồn ngoài (web docs, GitHub, ảnh/UI); có mode tuần tự và song song.",
  "hi-tech-build-audit":
    "Audit tech stack, build system, quản lý dependency, pipeline CI/CD, target deploy và giả định nền tảng.",
  "hi-usecase-discovery":
    "Sinh draft use case nghiệp vụ theo từng module: actor, quyền, rule, luồng, kết quả, ID, test và coverage.",
  "typesafe-ai":
    "Xây tính năng AI với TypeSafe System One (Jev): judgment có kiểu (choice/noul/score) như primitive lập trình.",
};

/** Related skills per page (kept in sync with devkit.md). */
const RELATIONS = {
  "hi-api-contract-discovery": ["hi-usecase-discovery", "hi-data-model-discovery", "hi-behavior-modeling", "hi-cross-artifact-validation", "hi-maintenance-docs", "hi-document-lifecycle", "hi-scout"],
  "hi-behavior-modeling": ["hi-usecase-discovery", "hi-cross-artifact-validation", "hi-maintenance-docs", "hi-document-lifecycle"],
  "hi-brainstorm": ["hi-plan", "hi-predict", "hi-sequential-thinking"],
  "hi-chrome-devtools": ["hi-scout"],
  "hi-command-spec-discovery": ["hi-usecase-discovery", "hi-behavior-modeling", "hi-cross-artifact-validation", "hi-maintenance-docs", "hi-document-lifecycle"],
  "hi-cortex": ["hi-scout", "hi-plan", "hi-craft", "hi-fix", "hi-debug", "hi-scenario", "hi-security"],
  "hi-cross-artifact-validation": ["hi-usecase-discovery", "hi-behavior-modeling", "hi-api-contract-discovery", "hi-data-model-discovery", "hi-command-spec-discovery", "hi-maintenance-docs"],
  "hi-data-model-discovery": ["hi-usecase-discovery", "hi-behavior-modeling", "hi-cross-artifact-validation", "hi-maintenance-docs", "hi-document-lifecycle"],
  "hi-document-lifecycle": ["hi-maintenance-docs", "hi-document-refinement", "hi-document-review-resolution", "hi-module-summary-report", "hi-usecase-discovery", "hi-behavior-modeling", "hi-api-contract-discovery", "hi-data-model-discovery", "hi-command-spec-discovery"],
  "hi-document-refinement": ["hi-document-lifecycle", "hi-maintenance-docs"],
  "hi-document-review-resolution": ["hi-document-lifecycle", "hi-maintenance-docs"],
  "hi-maintenance-docs": ["hi-repo-recon", "hi-tech-build-audit", "hi-module-summary-report", "hi-usecase-discovery", "hi-api-contract-discovery", "hi-data-model-discovery", "hi-command-spec-discovery", "hi-behavior-modeling", "hi-cross-artifact-validation", "hi-document-refinement", "hi-document-review-resolution"],
  "hi-module-summary-report": ["hi-repo-recon", "hi-tech-build-audit", "hi-maintenance-docs", "hi-repowiki"],
  "hi-repo-recon": ["hi-tech-build-audit", "hi-module-summary-report", "hi-usecase-discovery", "hi-maintenance-docs", "hi-repowiki"],
  "hi-repowiki": ["hi-repo-recon", "hi-tech-build-audit", "hi-module-summary-report"],
  "hi-scout": ["hi-plan", "hi-craft", "hi-fix", "hi-debug", "hi-cortex", "hi-docs-seeker"],
  "hi-tech-build-audit": ["hi-repo-recon", "hi-module-summary-report", "hi-repowiki"],
  "hi-usecase-discovery": ["hi-repo-recon", "hi-behavior-modeling", "hi-cross-artifact-validation", "hi-maintenance-docs", "hi-document-lifecycle"],
  "typesafe-ai": ["hi-plan", "hi-craft", "hi-security", "hi-scenario"],
};

const read = (p) => readFileSync(join(ROOT, p), "utf8");

const MARKER = "<!-- generated by scripts/gen-wiki-pages.mjs from SKILL.md; edit the skill, then re-run -->";

function frontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  return m ? m[1] : "";
}

function description(fm) {
  const block = fm.match(/^description:\s*(>[-+]?|\|[-+]?)?\s*\n?([\s\S]*?)(?=^[A-Za-z_][\w-]*:)/m);
  if (!block) return "";
  const folded = block[1] !== undefined;
  const body = block[2] ?? "";
  const text = folded
    ? body.split("\n").map((l) => l.trim()).filter(Boolean).join(" ")
    : body.trim();
  return text.replace(/^["']|["']$/g, "").trim();
}

function hint(fm) {
  return fm.match(/^argument-hint:\s*(.+)$/m)?.[1]?.trim().replace(/^"|"$/g, "") ?? "";
}

function boundaries(text, desc = "") {
  const found = [];
  const consider = (sentence) => {
    const s = sentence.trim();
    if (!s) return;
    if (/^(Do not|Do NOT|Never)\b/i.test(s) || /\b(never \w+|without modifying|do not\b)/i.test(s)) {
      found.push(s);
    }
  };

  desc.split(/(?<=\.)\s+/).forEach(consider);
  for (const line of text.split("\n")) {
    const clean = line
      .replace(/^[-*\s]+/, "")
      .replace(/^#{2,3}\s*/, "")
      .trim();
    if (!clean) continue;
    clean.split(/(?<=\.)\s+/).forEach(consider);
  }

  const seen = new Set();
  return found.filter((s) => {
    const key = s.slice(0, 60);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function outline(text) {
  return [...text.matchAll(/^## (.+)$/gm)]
    .map((m) => m[1].trim())
    .filter((h) => !/^(Source|References)/i.test(h));
}

/** Extracted text is copied verbatim from SKILL.md, so any relative link inside it
 *  would break once the sentence lands in wiki/<lang>/. Re-anchor such links to the
 *  skill directory. */
function reanchor(text, dir) {
  return text.replace(/\]\(([^)\s]+)\)/g, (whole, target) => {
    if (/^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith("#") || target.startsWith("../")) {
      return whole;
    }
    return `](../../${dir}/${target.replace(/^\.\//, "")})`;
  });
}

function page(dir, lang) {
  const text = read(join(dir, "SKILL.md"));
  const fm = frontmatter(text);
  const desc = reanchor(description(fm), dir);
  const argHint = hint(fm);
  const bounds = boundaries(text, desc).slice(0, 6).map((b) => reanchor(b, dir));
  const heads = outline(text);
  const relations = RELATIONS[dir] ?? [];
  const vi = SUMMARY_VI[dir];
  const skill = dir;

  if (lang === "vi") {
    return [
      `# ${skill}: hướng dẫn`,
      "",
      MARKER,
      "",
      `> ${vi ?? desc}`,
      "",
      `**Mô tả gốc (EN):** ${desc}`,
      "",
      "## Cách gọi",
      "",
      argHint ? "```text\n/" + skill + " " + argHint + "\n```" : `Gọi theo tên skill kèm mô tả task: \`/${skill} <task>\``,
      "",
      "## Ranh giới",
      "",
      ...(bounds.length ? bounds.map((b) => `- ${b}`) : ["- Không có câu ranh giới nào khớp extractor — kiểm tra clause loại trừ trong skill."]),
      "",
      "## Nội dung skill",
      "",
      ...heads.map((h) => `- ${h}`),
      "",
      "## Skill liên quan",
      "",
      ...(relations.length ? relations.map((r) => `- \`${r}\``) : ["- Không có quan hệ cross-skill được khai báo."]),
      "",
      `Nguồn: [${skill}/SKILL.md](../../${skill}/SKILL.md)`,
      "",
    ].join("\n");
  }

  return [
    `# ${skill}: guide`,
    "",
    MARKER,
    "",
    `> ${desc}`,
    "",
    "## Invocation",
    "",
    argHint ? "```text\n/" + skill + " " + argHint + "\n```" : `Called by name with a task description: \`/${skill} <task>\``,
    "",
    "## Boundaries",
    "",
    ...(bounds.length ? bounds.map((b) => `- ${b}`) : ["- No explicit \"do not use\" boundary declared in the skill."]),
    "",
    "## What the skill covers",
    "",
    ...heads.map((h) => `- ${h}`),
    "",
    "## Related skills",
    "",
    ...(relations.length ? relations.map((r) => `- \`${r}\``) : ["- No cross-skill relation declared."]),
    "",
    `Source: [${skill}/SKILL.md](../../${skill}/SKILL.md)`,
    "",
  ].join("\n");
}

const skills = readdirSync(ROOT, { withFileTypes: true })
  .filter((e) => e.isDirectory() && !e.name.startsWith(".") && !SKIP.has(e.name) && existsSync(join(ROOT, e.name, "SKILL.md")))
  .map((e) => e.name)
  .sort();

let written = 0;
let handWritten = 0;
const stale = [];
for (const dir of skills) {
  for (const lang of ["en", "vi"]) {
    const rel = join("wiki", lang, `${dir}-skill.md`);
    const next = page(dir, lang);
    const current = existsSync(join(ROOT, rel)) ? read(rel) : null;
    // Hand-written pages are only replaced on an explicit --adopt, never by --force.
    if (current !== null && !current.includes(MARKER) && !ADOPT.has(dir)) {
      handWritten += 1;
      continue;
    }
    if (current === next) continue;
    if (CHECK) {
      stale.push(rel);
      continue;
    }
    writeFileSync(join(ROOT, rel), next, "utf8");
    written += 1;
    console.log(`  written  ${rel}`);
  }
}

if (CHECK) {
  console.log(stale.length ? stale.map((s) => `  stale    ${s}`).join("\n") : "  wiki pages match the generator");
  process.exit(0);
}
console.log(`\n${written} page(s) written, ${handWritten} hand-written page(s) left untouched`);
