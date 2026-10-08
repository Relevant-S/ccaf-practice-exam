# CCAF Foundations Syllabus — Index

This folder is the **authoritative content map** for the *Claude Certified Architect – Foundations* exam. Richard reads it to:

- Decide what the user needs to know (domain weights → study priority)
- Map bank questions to official exam domains
- Detect coverage gaps (which official domains are under-represented in the question bank)
- Recommend external study material for areas the bank doesn't cover

**Source of truth:** Anthropic's *Claude Certified Architect – Foundations Certification Exam Guide*, **Version 1.0 (July 2026)**: `references/certification-exam-guide/CCA-Foundations-Exam-Guide-v1.0-July-2026.pdf`. The older Version 0.1 (Feb 10 2025) sits in the same folder, kept for history only. The tested content did not change between the two: the task statements, weights, scenarios and sample questions are word for word the same. What changed is the exam format: 60 items, 120 minutes, multiple-choice and multiple-response items, and a scaled score with a cut score of 720 (details in `domains.md`). The files in this folder are a structured restatement, not a replacement. When in doubt, check the v1.0 PDF.

## Files

| File | Contents |
|---|---|
| [`domains.md`](./domains.md) | The 5 exam domains, their weightings, all task statements with Knowledge + Skills bullets. Plus the 6 exam scenarios, exam format, in-scope and out-of-scope topics. The big knowledge map. |
| [`topics.md`](./topics.md) | Canonical topic-slug taxonomy. Maps the slugs used in the question bank to the 5 official domains. The lookup table Richard uses to roll up bank questions into domain coverage. |

## How Richard uses these files

- **At session start (any mode):** Richard does not load the entire syllabus eagerly. He loads `topics.md` (small) on first use to get the slug → domain mapping. He loads `domains.md` (larger) only when the user enters tutoring mode for a specific domain, or when generating a question.
- **In tutoring mode:** When the learner asks "teach me Domain 2", Richard pulls the relevant Task Statements from `domains.md` and uses the Knowledge/Skills bullets as the lesson outline. When generating practical tasks, he draws from the Skills bullets — those are the *applied* competencies the exam tests.
- **In examination mode:** When generating a new question (not from the bank), Richard grounds it in a specific Task Statement so the question is exam-relevant, not vibes-relevant.
- **In progress mode:** Richard rolls up bank-question results to the 5 domains via `topics.md`, then weights each domain's mastery against its exam weighting (e.g., D1 mastery counts for 27% of the projected exam score).

## What is NOT here

- The question bank itself — that's `assets/question-bank/`.
- The learner's personal study state — that's the per-user sanctum at `{project-root}/_bmad/memory/ccaf-tutor/`.
- External documentation — referenced from `domains.md` per domain, but not vendored here. Authoritative sources include:
  - Anthropic Claude API docs: https://docs.claude.com/
  - Claude Code docs: https://code.claude.com/docs/
  - Claude Agent SDK docs (linked from the above)
  - MCP specification: https://modelcontextprotocol.io/
