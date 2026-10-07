# Topics Mastery

_Per-domain and per-Task-Statement read on what {user_name} knows. Updated after every tutoring or examination session that touches a topic._

_Mastery levels: **Solid** | **Good** | **Wobbly** | **Weak** | **Untested**. Use judgment, not just accuracy: factor in recency, depth of practical-task work, and whether reasoning was defended or just guessed correctly._

_Accuracy counts each question under its own `domain:` and `task:` fields, never its `topic:` slug. Keep every cell short: a Notes cell is a few words, not a sentence._

_Last-touched is the date of the most recent session that engaged this topic, in any mode (tutoring, examination, or progress check)._

---

## Domain Overview

| Domain | Weight | Mastery | Accuracy | Last touched |
|---|---:|---|---:|---|
| D1 Agentic Architecture & Orchestration | 27% | Untested | — | — |
| D2 Tool Design & MCP Integration | 18% | Untested | — | — |
| D3 Claude Code Configuration & Workflows | 20% | Untested | — | — |
| D4 Prompt Engineering & Structured Output | 20% | Untested | — | — |
| D5 Context Management & Reliability | 15% | Untested | — | — |

**Projected weighted exam score:** _Not yet — need first quiz_

---

## D1 — Agentic Architecture & Orchestration (27%)

| Task | Topic | Mastery | Notes |
|---|---|---|---|
| T1.1 | Agentic loops, `stop_reason` handling | Untested | |
| T1.2 | Coordinator-subagent orchestration | Untested | |
| T1.3 | Subagent invocation, context passing, `Task` tool | Untested | |
| T1.4 | Multi-step workflows, programmatic enforcement, handoff | Untested | |
| T1.5 | Agent SDK hooks (`PostToolUse`, interception) | Untested | |
| T1.6 | Task decomposition (chaining vs adaptive) | Untested | |
| T1.7 | Session state, resumption, `fork_session` | Untested | |

## D2 — Tool Design & MCP Integration (18%)

| Task | Topic | Mastery | Notes |
|---|---|---|---|
| T2.1 | Tool descriptions, disambiguation | Untested | |
| T2.2 | MCP `isError`, structured error responses | Untested | |
| T2.3 | Tool distribution, `tool_choice` | Untested | |
| T2.4 | MCP server config, `.mcp.json`, resources | Untested | |
| T2.5 | Built-in tools (Read/Write/Edit/Bash/Grep/Glob) | Untested | |

## D3 — Claude Code Configuration & Workflows (20%)

| Task | Topic | Mastery | Notes |
|---|---|---|---|
| T3.1 | CLAUDE.md hierarchy, `@import`, `.claude/rules/` | Untested | |
| T3.2 | Custom slash commands and skills, `context: fork` | Untested | |
| T3.3 | Path-specific rules with glob patterns | Untested | |
| T3.4 | Plan mode vs direct execution | Untested | |
| T3.5 | Iterative refinement (examples, TDD, interview pattern) | Untested | |
| T3.6 | Claude Code in CI/CD (`-p`, `--output-format json`) | Untested | |

> **D3 bank coverage:** 13 shipped questions for a 20%-weight domain (see `assets/syllabus/topics.md`). Generated questions fill the gap.

## D4 — Prompt Engineering & Structured Output (20%)

| Task | Topic | Mastery | Notes |
|---|---|---|---|
| T4.1 | Explicit criteria, false-positive reduction | Untested | |
| T4.2 | Few-shot prompting | Untested | |
| T4.3 | Structured output via `tool_use` + JSON schema | Untested | |
| T4.4 | Validation, retry, feedback loops | Untested | |
| T4.5 | Batch processing (Message Batches API) | Untested | |
| T4.6 | Multi-instance / multi-pass review | Untested | |

## D5 — Context Management & Reliability (15%)

| Task | Topic | Mastery | Notes |
|---|---|---|---|
| T5.1 | Conversation context, lost-in-the-middle | Untested | |
| T5.2 | Escalation, ambiguity resolution | Untested | |
| T5.3 | Error propagation across multi-agent systems | Untested | |
| T5.4 | Large codebase exploration, scratchpad files | Untested | |
| T5.5 | Human review workflows, confidence calibration | Untested | |
| T5.6 | Information provenance, conflict annotation | Untested | |
