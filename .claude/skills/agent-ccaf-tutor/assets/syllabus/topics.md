# CCAF Topic Taxonomy

The **canonical taxonomy** for the CCAF exam is the 5 official domains defined in `domains.md`. The question bank uses more granular topic slugs as a convenience layer; this file is the authoritative mapping from those slugs to official domains.

Richard reads this file when:
- Rolling up bank-question results to domain-level mastery (for the `progress` capability)
- Generating new questions and choosing which domain to ground them in
- Recommending what to study next based on weighted gap analysis

---

## The 5 official domains (canonical)

| Code | Domain | Exam weight |
|---|---|---:|
| `D1` | Agentic Architecture & Orchestration | **27%** |
| `D2` | Tool Design & MCP Integration | **18%** |
| `D3` | Claude Code Configuration & Workflows | **20%** |
| `D4` | Prompt Engineering & Structured Output | **20%** |
| `D5` | Context Management & Reliability | **15%** |

---

## Bank-slug → official-domain mapping

The question bank's `topic:` field uses slugs that pre-date the syllabus. Each slug maps to one official domain. When in doubt, the **task statement** that the question tests is the tiebreaker (see `domains.md`).

| Bank slug | Maps to | Notes / typical task statements |
|---|---|---|
| `agents-and-orchestration` | **D1** | T1.1 (loops), T1.2 (coordinator-subagent), T1.3 (Task tool, context passing), T1.4 (enforcement/handoff), T1.6 (decomposition) |
| `agent-sdk` | **D1** | T1.1, T1.5 (hooks), T1.7 (sessions, fork). Conceptually a sub-slice of D1. |
| `tool-use` | **D2** | T2.1 (descriptions), T2.3 (tool distribution, `tool_choice`), T2.5 (built-in tools). Could overlap with D4-T4.3 (`tool_use` for structured output) — disambiguate by question intent. |
| `claude-code` | **D3** | T3.1–T3.6 (CLAUDE.md, slash commands/skills, rules, plan mode, iterative refinement, CI/CD) |
| `prompt-engineering` | **D4** | T4.1 (explicit criteria), T4.2 (few-shot), T4.3 (structured output via tool_use) |
| `evaluation` | **D4** or **D5** | If about validation/retry loops, extraction quality → D4-T4.4. If about confidence calibration / human review routing → D5-T5.5. Read the question. |
| `context-management` | **D5** | T5.1 (conversation context), T5.4 (codebase exploration, scratchpads), T5.6 (provenance) |
| `production-deployment` | **D3** or **D5** | If about CI/CD, `-p` flag, `--output-format json` → D3-T3.6. If about reliability/error propagation → D5-T5.3. |
| `safety-and-guardrails` | **D1** or **D2** | If about hooks for compliance / blocking actions → D1-T1.5. If about MCP error responses for permission errors → D2-T2.2. |
| `pricing-and-limits` | **D4** | Specifically the Message Batches API (T4.5) — 50% cost savings, 24h SLA, no multi-turn tool calling. |

### Current bank coverage vs exam weight

Snapshot from the 60-question bank:

| Domain | Exam weight | Bank Q's | Coverage status |
|---|---:|---:|---|
| D1 | 27% | ~21 (`agents-and-orchestration` 20 + `agent-sdk` 1) | **Well-covered** |
| D2 | 18% | 7 (`tool-use`) | Adequate |
| D3 | 20% | ~6 (`claude-code` 5 + portion of `production-deployment`) | **UNDER-covered — generate supplements** |
| D4 | 20% | ~14 (`prompt-engineering` 8 + `evaluation` ~4 + `pricing-and-limits` 2) | Well-covered |
| D5 | 15% | ~12 (`context-management` 11 + portion of `production-deployment`/`safety-and-guardrails`) | Well-covered |

> Numbers are approximate where slugs map ambiguously. Richard should refine this on first read of each question.

### Subtopic field

The bank's `subtopic:` field is **free-form** — it's a convenience tag for fine-grained recall ("parallel-calls", "agent-memory-patterns", "cross-field-validation"). Do not try to taxonomize it. Use it as a search hint, not a hierarchy.

---

## How Richard generates new questions

When generating a question, Richard:

1. Picks an **official domain code** (`D1`–`D5`) — usually the one the learner is currently weakest in, weighted by exam weight.
2. Picks a **specific Task Statement** within that domain (e.g., `D2-T2.3` for tool distribution).
3. Picks a **scenario** from the 6 in `domains.md` that fits naturally — exam questions are scenario-grounded.
4. Writes the question following the bank's `README.md` format.
5. **Tags the generated question** in frontmatter with both:
   - `topic:` = the most natural bank slug (for backward compatibility with the existing 60 questions)
   - `domain:` = the official domain code (`D1`–`D5`)
   - `task:` = the task statement code (e.g., `T2.3`)
6. Writes the file to the per-user sanctum at `{project-root}/_bmad/memory/ccaf-tutor/generated-questions/`, NOT to `assets/question-bank/`. The shared bank ships unchanged across all users.

### Future evolution

Existing bank questions don't have `domain:` or `task:` fields. They can be added incrementally — Richard can backfill them on first encounter (read question → infer domain → write back). Or the repo owner can run a one-off pass with a script. Not urgent.
