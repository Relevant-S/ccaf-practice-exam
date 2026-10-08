# CCAF Study Guide — Decision Rules and Concept Reference

> Exam answers follow the official exam guide. Where current Claude Code behaves differently, a "Product drift" note says so.

This guide is for you, the learner. It has three parts:

1. **Three decision rules** that sit under a large share of exam questions — and the cases where each rule flips.
2. **A concept reference**, one entry per task statement (T1.1 to T5.6), with ✅ right and ❌ wrong examples.
3. **A self-test** to check yourself before the exam.

The exam tests judgment in realistic production settings, not trivia. Most wrong options are not silly. They are reasonable moves made in the wrong situation.

For the matching list of distractor patterns, see `assets/common-traps.md`.

**The exam format (exam guide v1.0, July 2026).**

- 60 questions in 120 minutes — about 2 minutes each.
- Two item types: multiple choice and multiple response. Each item says how many answers to choose.
- You get 4 of the 6 scenarios, picked at random.
- Scaled score from 100 to 1,000. The pass mark is 720. A scaled score is not a percentage.
- The report shows pass or fail, plus your percentage correct in each domain.
- The guide does not say how blank answers are scored, so answer every question.

**Method for a choose-N item.** Judge each option true or false on its own against the scenario. Then check you picked exactly N.

---

## Part 1 — Three Decision Rules

### Rule 1 — Let the model judge at runtime, under explicit criteria

**The trap.** When a task means choosing between options or deciding how to recover, a wrong option often adds a layer that decides *for* the model: a classifier, a rules engine, a full upfront plan, or many subagents launched at once.

**Why it fails.**

- Classifiers and rules engines break on cases nobody planned for. New kinds of request do not fit old buckets.
- An upfront plan needs facts the agent does not have yet.
- Launching many investigations at once pays the full cost before you know where the answer is.

**The fix.** Give the model a goal and explicit criteria — a quality bar, what "resolved" means, when to escalate. Let it decide step by step.

**One-line test.** Does the design decide at *build time* (while you configure the agent, before any real request) or at *runtime* (while it handles one real request, with all the facts)? Prefer runtime.

**Example (T1.6, task decomposition).** A support agent gets tickets from "reset my password" to "I was double-charged, the app crashes, and I want to cancel one of two subscriptions."

- ❌ A classifier that sends each ticket to one of four fixed workflows.
- ❌ A complete plan for the whole ticket before acting.
- ❌ One subagent per category, all at once.
- ✅ The agent reads each ticket, splits it into sub-tasks as needed, and works each one under clear "resolved" and "escalate" criteria.

#### When structure wins

**1. A hard rule that must never fail → enforce it in code.** Use this when the rule is known in advance *and* one miss is unacceptable.

Example (T1.4 and T1.5, enforcement and hooks): no refund over $500 without human approval.

- ❌ A firm system-prompt instruction. A prompt is followed most of the time, not every time.
- ❌ Give the threshold as escalation criteria and let the model decide.
- ✅ A hook that intercepts the refund tool call *before* it runs, blocks it above $500, and sends the case to a human.

**2. Known, complete, independent work → fan out.** Example (T1.2 and T1.6): check all 200 signed contracts against the same 12-clause checklist.

- ✅ Fan out across parallel subagents, each taking a slice, then combine the results.

Fan-out is wrong when it is *premature*. It is right when there is nothing to discover about *what* to do — only volume.

**3. Known steps that depend on each other → a fixed pipeline.** Example (T1.6, prompt chaining): collect → analyze → report, where each step needs the last one's output. Known and dependent → chain. Known and independent → fan out. Unknown → adaptive.

#### Match the mechanism to the stakes

Do not over-correct. Not every guideline needs a hook. Style and judgment rules (naming, tone, a "back up first" habit in a repo where every change can be undone) can stay in the prompt. Two questions decide it:

1. Can plain code check or apply the rule, with no judgment?
2. Must it hold every single time, because one miss does real harm?

Two yeses → a hook or gate. Otherwise → prompt guidance, explicit criteria or few-shot examples. (T1.4 and T1.5: hooks give guaranteed compliance; prompts give probabilistic compliance.)

---

### Rule 2 — Keep the live state; add memory; compress only what is finished

**The trap.** When context gets full or noisy, a wrong option squashes or replaces the live state too early: summarize everything, start a fresh session, move the conversation into a vector database, or re-run every tool.

**The fix — try in this order:**

1. **Keep the active thread at full detail.** Whatever matters right now stays complete.
2. **Prune what is finished.** Replace a resolved sub-thread with a short summary. Drop tool output that newer output replaced. Trim verbose tool results to the fields you need.
3. **Keep hard facts out of any summary.** Put amounts, dates, order numbers, statuses and promises in a separate "case facts" block that is sent every turn.
4. **Use a heavier move only when a real trigger calls for it** (table below).

**Example (T5.1, conversation context).** A support agent is 45 minutes into a live conversation. Several issues came up. Context is filling. The customer is still working on the current issue.

- ❌ Put the whole conversation into a vector database.
- ❌ Start a fresh session and re-run every earlier tool call.
- ❌ Summarize everything into one paragraph, including the active issue.
- ✅ Keep the active issue in full. Summarize resolved sub-threads. Drop superseded tool output. Keep exact facts in a separate structured block.

#### When the heavier move is right

| Heavier move | Wrong when | Right when |
|---|---|---|
| External store (vector DB, knowledge base) | handling one live, bounded conversation | the knowledge is large, lasting and shared across sessions — "how were similar issues solved for thousands of other customers?" |
| Fresh session | it discards a live conversation and re-runs every tool | a customer returns later and old tool results are stale. Start fresh, inject a structured summary, make fresh tool calls. |
| Summarize or `/compact` | done early, on the active thread, or losing exact facts | done on resolved parts or verbose discovery output, with hard facts kept elsewhere |

**A common slip.** "Don't start fresh — the old results are stale." Re-running tools refreshes them, so staleness is not the flaw. The real flaws with "resume and re-call every tool" are the cost, and that the stale results stay in context and confuse the model.

---

### Rule 3 — Read the customer's signal before you act

The exam guide (T5.2, escalation) separates two cases. Decide which one you are in first.

| Situation | Right move |
|---|---|
| The customer **explicitly demands a human** | Escalate immediately. Do not investigate first. Pass the context you already have. |
| The customer is **frustrated but has not asked for a human**, and the fix is within the agent's power | Acknowledge the frustration. Offer to resolve it now. Escalate only if they repeat that they want a person. |
| The **policy is silent or unclear** about what they want | Escalate. Silence is not a "no". |
| **Several customer records match** | Ask for another identifier. Do not guess. |

**Always wrong:**

- interrogating the customer about what failed before
- quietly fixing things when they asked for a person
- escalating because of tone alone — sentiment does not measure how hard a case is
- using the model's self-reported confidence as the escalation trigger

**Example — explicit demand.** "I've explained this twice. I want to talk to a real person NOW." No tools called yet.

- ✅ Escalate now, passing the conversation history.
- ❌ Look up the account first, then escalate.
- ❌ Ask one more question before escalating.
- ❌ Offer to resolve it and escalate only if they ask again.

**Example — frustration, no demand.** "Third time this week the login fails. This is infuriating." The fix is a documented one-step token refresh the agent is allowed to do.

- ✅ Acknowledge, name the cause, say it can be fixed now, fix it — and offer a human if they prefer.
- ❌ Escalate because they are upset.

**Borderline wording.** "I just want to speak to someone who can actually help me", when the return is confirmed simple and one step away. The bank's answer: acknowledge, say it is resolvable now, and offer to complete it *or* escalate — their choice. Do not act without asking. Read the exact words: a clear demand for a human means escalate now.

---

## Part 2 — Concept Reference by Task Statement

Each entry: the idea, ✅/❌ examples, and the key facts. Task statement codes match the official exam guide.

---

### Domain 1 — Agentic Architecture & Orchestration (27%)

How agents are wired: the loop, coordinators and subagents, handoffs, sessions.

#### T1.1 — The agentic loop and `stop_reason`

The model asks for a tool → your code runs it → **the result is added to the conversation** → the model reads it and decides the next step. This repeats while `stop_reason` is `"tool_use"`. It ends when the model stops asking for tools (`stop_reason` is `"end_turn"`). The model drives the loop. It is not a script.

- ❌ A fixed sequence: run test → read file → fix → done.
- ❌ A decision tree that routes each step.
- ✅ Call a tool, see the result in the conversation, decide what to do next, repeat.

**Key fact.** If tool results are not appended to the conversation, the model cannot reason about them.

#### T1.2 — Coordinator–subagent orchestration

The coordinator is the hub. It decides per query which subagents to call, passes information between them, and combines their results. All communication goes through it, so it can see what ran, what failed and what came back.

- ❌ A trained classifier that maps each query to a fixed specialist.
- ❌ A fixed "fast path" router for simple-looking queries.
- ❌ Subagents that spawn their own subagents. The coordinator loses sight of the work.
- ✅ The coordinator reads each query, picks the subagents it needs, and merges the results.

**Do not over-spawn.** If the coordinator can answer a trivial follow-up itself, it should. Subagents are for scoped work that gains from isolation.

#### T1.3 — Subagent invocation and context passing

Subagents **do not inherit** the coordinator's context. Anything a subagent needs must go into its prompt.

- ❌ Assume the synthesis subagent can see what the research subagents found.
- ❌ Give the synthesis subagent tools to fetch other agents' histories.
- ❌ Run the agents one after another and assume the later one sees the earlier output. Running in sequence is not passing context.
- ✅ The coordinator puts the research findings into the synthesis subagent's prompt.

**Keep structure end to end.** Subagents should return structured content with source metadata (claim → source, dates). Do not return prose and rebuild the sources later.

**Context is degrading.** The agent has spent a long time in one area and now talks about "typical patterns" instead of the classes it found.

- ❌ Spawn a subagent for the next area, then merge its findings by hand in the tired main conversation.
- ✅ Summarize the key findings first, then spawn the subagent with that summary in its first prompt.

**Key fact (Agent SDK).** Subagents are spawned with the **Task** tool. A coordinator can only spawn them if `"Task"` is in its `allowedTools`. Listing subagent types in the prompt is not enough. To run subagents in parallel, the coordinator emits several Task calls in one response.

> **Product drift.** The exam guide calls this tool **Task**. In Claude Code 2.1.63 it was renamed **Agent**. `Task` still works as an alias. Answer "Task" on the exam.

#### T1.4 — Multi-step workflows, enforcement and handoff

Three ideas:

1. **Hard prerequisites go in code.** Example: block `process_refund` until `get_customer` has returned a verified customer ID. A prompt instruction has a non-zero failure rate.
2. **Fuzzy escalation decisions go in natural-language criteria** the model applies case by case.
3. **Human handoffs need a structured summary**, not raw material.

**Handoff example.** The agent escalates a billing dispute to a human who cannot see the transcript.

- ❌ Forward the original complaint plus raw tool output.
- ✅ A structured summary: customer ID, root cause, amount, recommended action, reason for escalation.

**Escalation criteria example.**

- ❌ A rules engine keyed on issue type × customer segment.
- ✅ "Escalate if the customer asks for a human, if the issue needs a policy exception, or if you cannot make progress."

**Graceful degradation.** A tool times out mid-process.

- ✅ Explain what you know, confirm what you verified, say what failed, and offer to retry or escalate.

**Multi-concern requests.** Split the request into separate items, investigate them in parallel with shared context, then give one combined answer.

#### T1.5 — Hooks for deterministic control

Hooks are code that runs at fixed points in the agent loop. They do not depend on what the model decides.

| Hook | When it runs | What it is for |
|---|---|---|
| **PreToolUse** | *before* a tool runs | Inspect the outgoing call. Can **block** it (a "deny" decision) and send the case elsewhere, such as human escalation. |
| **PostToolUse** | *after* the tool has run | Normalize or transform the result before the model sees it (for example, turn Unix timestamps, ISO 8601 dates and numeric status codes into one format). Can add feedback. **Cannot** prevent the call — it already happened. |

The exam guide calls the blocking kind "tool call interception hooks". It names PostToolUse for normalizing data.

- ❌ "NEVER issue refunds over $500 without approval" in the system prompt.
- ❌ A PostToolUse hook to stop large refunds — by then the refund has run.
- ✅ A hook that intercepts the refund call before it runs (PreToolUse), denies it above $500, and routes to a human.

**Mental model.** Prompt = persuasion (works most of the time). Hook = enforcement (works every time). Match the tool to how bad a miss would be.

**Pre or Post? One question.** Is the damage done the moment the tool runs (money moves, a file is deleted)? Then it must be PreToolUse. PostToolUse is too late to stop it. Use PostToolUse when you need what the tool produced — to clean it up or check it.

#### T1.6 — Task decomposition: fixed chain vs adaptive

When each step depends on what the last one found, decide the next step from the last result.

- ❌ "Write a full plan first, then execute it" for an unknown production error.
- ✅ Form a hypothesis, investigate, let each finding shape the next step, under a clear "diagnosed" bar.

**When fixed decomposition wins.** Known, independent steps — for example, the same review pass over each file, then a separate pass for cross-file issues. Also known steps that depend on each other, such as collect → analyze → report: a fixed pipeline, each output feeding the next. See Rule 1.

#### T1.7 — Sessions: resume, fork, and when to start fresh

- **Resume by name:** `claude --resume <name>` loads a specific earlier session.
- **Fork:** forking branches a resumed session into a new one, so you can try two approaches from the same starting point without changing the original. It is an option *on resume*:
  - Agent SDK: `resume` plus `fork_session` (Python) or `forkSession` (TypeScript).
  - CLI: `--resume` or `--continue` plus `--fork-session`.
- **Targeted delta on resume:** tell the agent exactly what changed (for example, which files were edited). Do not make it re-read everything.
- **Start fresh with a summary** when old tool results are stale (see Rule 2).
- **Polluted coding session** (several failed attempts, files changed by a teammate's push): start a fresh session, inject a summary of what you found *and what was tried and failed*, then re-read the current files. Not a re-read in the same session (stale results stay in context). Not a fork (it copies the clutter). Not a blank session (it loses the lessons).

- ❌ Run one refactoring approach, then start a fresh session for the other. You lose the shared starting point.
- ✅ Fork from the shared baseline, one approach per branch, then compare.

---

### Domain 2 — Tool Design & MCP Integration (18%)

#### T2.1 — Tool descriptions and splitting tools

The model chooses tools from their descriptions. First work out which problem you have.

| Symptom | Fix |
|---|---|
| The model picks the wrong one of several **clear** tools | Sharpen the descriptions: purpose, inputs, outputs, and how each differs from its neighbours. |
| **One tool does many jobs** through a free-text instruction, and outputs come back in the wrong shape | **Split** it into purpose-specific tools, each with its own contract. |

- ❌ Fix a vague `analyze_document(document, instruction)` tool by adding examples or an `analysis_type` enum.
- ✅ Split it into `extract_data_points`, `summarize_content`, `verify_claim_against_source`.
- ❌ Remove a competing tool, or add a routing classifier, when the real problem is unclear descriptions.

#### T2.2 — MCP tool errors

When a tool fails, **return the error as a tool result** so the model can reason about it. Do not throw an exception from the handler.

```json
{
  "content": [{ "type": "text", "text": "Payment service unavailable (timeout). Safe to retry." }],
  "isError": true
}
```

- `isError: true` marks a **tool execution error**. `content` is an **array** of content blocks.
- Problems with the protocol itself (unknown tool, malformed request) are **JSON-RPC errors**. That is a different layer.

**Exam-guide convention.** The guide also asks for structured metadata: `errorCategory` (transient / validation / permission, plus business errors such as policy violations), an `isRetryable` boolean, and a readable description. These are a *design convention from the exam guide*, not fields in the MCP spec. You put them in the content you return.

- ✅ Downstream outage → transient, retryable.
- ✅ Customer not eligible → business error, not retryable, with a customer-friendly explanation.
- ❌ A bare "Operation failed".

#### T2.3 — Tool distribution and `tool_choice`

Give each agent only the tools its role needs. Too many tools make selection worse.

`tool_choice` options in the exam guide:

| Value | Meaning |
|---|---|
| `"auto"` | The model may call a tool or answer in text. |
| `"any"` | The model must call *some* tool. |
| `{"type": "tool", "name": "..."}` | The model must call *this* tool. |
| `"none"` | The model may not call tools. |

**Force once, then free.** To make a step happen first, force that tool on the first call, then let the model choose in later turns.

- ❌ Force the same tool on every call. The model can never move on.
- ✅ Force it on the first call; use `auto` afterwards.

> **Product drift.** The newest models (Opus 5.5, Sonnet 5.5) reject `"any"` and forced `{"type": "tool"}`. The exam still tests them. Answer by the guide.

#### T2.4 — MCP server configuration

| Scope | File | Use for |
|---|---|---|
| Project | `.mcp.json` at the repo root, committed | shared team tooling |
| User | `~/.claude.json` | personal or experimental servers |

- **Secrets:** use environment-variable expansion, such as `${GITHUB_TOKEN}`, so no token is committed.
- **Discovery:** tools from every configured server are found when Claude connects and are all available at once.
- **Resources vs tools:** tools are actions. **Resources** expose content catalogs (issue summaries, doc trees, database schemas) so the agent can see what exists without exploratory calls.
- **Prefer existing community servers** for standard systems such as Jira. Build custom servers for team-specific workflows.
- If the agent keeps using Grep instead of a better MCP tool, **improve the MCP tool's description**.

- ✅ Shared Jira server in `.mcp.json` with `${JIRA_TOKEN}`; each developer sets their own token.
- ❌ A token pasted into `.mcp.json`.

#### T2.5 — Built-in tools

| Tool | Use for |
|---|---|
| Grep | searching file **contents** (callers of a function, an error message) |
| Glob | finding files by **name pattern** (`**/*.test.tsx`) |
| Read / Write | whole-file reads and writes |
| Edit | a targeted change, located by a unique `old_string` |
| Bash | running commands |

**When Edit's `old_string` is not unique:**

1. Use a longer `old_string` with enough surrounding lines to be unique.
2. Or use `replace_all` if every match should change.
3. Last resort: Read the file, change it, Write the whole file back.

The exam guide names Read + Write as the fallback. Pick it when that is the best option offered.

**Note.** Older models must Read a file before they can Edit it.

**Exploring code.** Start with Grep to find entry points, then Read to follow imports. Do not read every file up front. To trace a function used through wrappers, first find every exported name for it, then search for each name.

---

### Domain 3 — Claude Code Configuration & Workflows (20%)

#### T3.1 — CLAUDE.md hierarchy, `@import`, `.claude/rules/`

**How CLAUDE.md files load.** From broadest to most specific:

1. managed policy (organisation-wide)
2. user: `~/.claude/CLAUDE.md` — **only you**, not shared via version control
3. project: `./CLAUDE.md` or `./.claude/CLAUDE.md` — committed, shared with the team
4. local: `CLAUDE.local.md` — personal notes for this project

Subdirectory `CLAUDE.md` files load when Claude works with files in that directory.

**They are combined, not overridden.** All of them go into context together. If two contradict each other, Claude may pick either. So remove conflicts — do not rely on one "winning".

**Other facts:**

- The project `CLAUDE.md` loads automatically. It does **not** need an `@import`.
- `@path/to/file` imports another file into a CLAUDE.md, to keep it modular.
- `@import` organises; it does not save context. The imported file loads at launch, together with the CLAUDE.md that imports it. To load a rule only when it is needed, use a `.claude/rules/` file with `paths:`. *(From the Claude Code docs, not the exam guide.)*
- `CLAUDE.local.md` loading last does not make it win. The files are combined, so a conflict is still a conflict. *(From the Claude Code docs, not the exam guide.)*
- `.claude/rules/*.md` holds topic files. **With** a `paths:` glob in the frontmatter, a rule loads when Claude reads or edits a matching file. **Without** `paths:`, it loads at launch, like CLAUDE.md.
- `/memory` shows which memory files are loaded — use it to debug.

**Example.** A new teammate does not get the team's conventions.

- ❌ The conventions are in someone's `~/.claude/CLAUDE.md`. That is never shared.
- ✅ Move them to the project `CLAUDE.md` and commit it.

**Example — where should a convention live?** API conventions apply to every caller of the API, all over the repo.

- ❌ `.claude/rules/api.md` with `paths: ["src/api/**"]`. The glob misses callers outside `src/api/`.
- ✅ Project `CLAUDE.md`, or a glob that matches every file the convention governs.

**Test:** does the glob reach as far as the convention?

#### T3.2 — Custom commands, skills, and `context: fork`

| Location | Who gets it |
|---|---|
| `.claude/commands/`, `.claude/skills/` | the team, via version control |
| `~/.claude/commands/`, `~/.claude/skills/` | only you |

For a personal variant of a team skill, use a different name so you do not affect teammates.

**SKILL.md frontmatter fields the exam tests:**

- `context: fork` — runs the skill in a separate sub-agent context so its output does not pollute the main conversation. **Trigger: verbose output or exploratory context.** Not runtime. Not concurrency. Not sandboxing.
- `allowed-tools` — in the exam guide, **restricts** which tools the skill may use (for example, read-only).
- `argument-hint` — prompts for a required argument when the skill is called without one.

> **Product drift.** In current Claude Code, `allowed-tools` **pre-approves** the listed tools (no permission prompt). It does **not** stop the skill using other tools. Restricting tools is done with `disallowed-tools`. On the exam, use the guide's meaning: `allowed-tools` restricts.

| Wrong reason to fork | Why |
|---|---|
| "It runs for a long time" | A 25-minute skill that prints six lines costs the main context almost nothing. |
| "It runs in the background" | Fork decides *where output lands*, not *when work runs*. |
| "It sandboxes the skill" | That is a tool-access setting, not a fork. |

**Skill vs CLAUDE.md.** Skills are loaded on demand, for specific tasks. CLAUDE.md is always loaded, for universal standards. A twice-a-month release procedure belongs in a skill.

#### T3.3 — Path-specific rules

Put a rule file in `.claude/rules/` with a `paths:` glob. It loads only when Claude touches matching files, which saves context.

- ✅ `.claude/rules/testing.md` with `paths: ["**/*.test.ts"]` for test conventions spread over 30 directories.
- ✅ `paths: ["terraform/**/*"]` for Terraform conventions.
- ❌ A `CLAUDE.md` in each test directory. Directory-bound files cannot follow files spread across the repo.

#### T3.4 — Plan mode vs direct execution

**Plan mode** when the change is large or unclear: several valid approaches, design decisions to make, many files touched. Explore first, agree the approach, then build.

**Direct execution** when the change is small and clear: a one-file bug fix with an obvious cause.

- ❌ "Use plan mode because a mistake would be costly." Cost alone is not the trigger.
- ✅ Plan mode because there are three reasonable caching designs to choose between.
- ✅ Direct execution for adding one validation check and a test.

The **Explore** subagent can hold verbose discovery output away from the main context.

#### T3.5 — Iterative refinement

When output is off, it is usually a **communication** problem, not a capability problem.

- **Concrete input/output examples** beat prose descriptions. Include an edge case.
- **Test-driven iteration:** write the tests first, then iterate until they pass, sharing failures.
- **Interview pattern:** have Claude ask you questions to surface things you had not considered.
- **Interacting problems:** describe them together in one message. **Independent** problems: fix them one at a time.

- ❌ "Switch to a bigger model" because commit messages do not match team style.
- ✅ Give two or three examples of good messages and say why they are good.

#### T3.6 — Claude Code in CI/CD

CI runs with no human at a terminal and must produce machine-readable output.

- `-p` (`--print`) runs non-interactively.
- `--output-format json` plus `--json-schema` gives structured, parseable output.
- CLAUDE.md gives project context (test standards, review criteria) to CI runs too.

- ❌ `--resume` the session that wrote the code. It is biased toward its own work.
- ❌ Made-up flags or env vars (`--batch`, `CLAUDE_HEADLESS`).
- ✅ A fresh `claude -p` with `--output-format json` and `--json-schema`.

**Re-runs.** To avoid re-posting old findings, pass the previous findings in and ask only for new or unaddressed issues.

---

### Domain 4 — Prompt Engineering & Structured Output (20%)

#### T4.1 — Explicit criteria to cut false positives

Vague instructions ("be conservative", "only high-confidence findings") do not help much. Say exactly what to report and what to skip.

- ✅ "Flag a comment only when it contradicts the code's actual behaviour."
- ✅ "If the discount rate is not stated, return null." This stops the model inventing values.
- ❌ Add a second LLM to catch made-up values, or upgrade the model, before trying a clear instruction.

High false-positive rates in one category destroy trust in all categories. Consider switching that category off until it is fixed.

#### T4.2 — Few-shot prompting

The default fix for format and consistency problems. Show 2–4 examples of the exact input → output you want, including the awkward cases.

- ✅ Messy citations → examples showing each messy variant mapped to the normal form.
- ✅ Examples of documents with different layouts, so extraction works on all of them.

**Fix at the source.** When detailed instructions still give inconsistent output, add few-shot examples with reasoning. Do not reach first for a linter, rewriter or post-processing step. Exception: a rule plain code can apply with no judgment, that must hold every time (for example, run the formatter on every file written) → a hook. See Rule 1, "Match the mechanism to the stakes".

#### T4.3 — Structured output with tool use and JSON schemas

Use a tool with a JSON schema to get structured output. A schema removes **syntax** errors. It does not remove **meaning** errors (a total that does not add up, a value in the wrong field).

- `tool_choice: "auto"` — the model may answer in text instead.
- `"any"` — it must call one of the tools (useful when several extraction schemas exist).
- Forced tool — it must call that tool.
- (See the product-drift note in T2.3.)

**Handling messy data:**

| Situation | Do this |
|---|---|
| Inconsistent formats | strict schema + normalization rules in the prompt |
| Values that may be missing | make the field nullable; return null when absent |
| Unknown categories | `enum` + `"other"` + a free-text `detail` field |
| Data changes over time (amendments) | allow several values, each with source and effective date |
| Different content types in one report | render by type — tables for financials, prose for news |

- ❌ Map unknown categories to the closest enum. Lossy.
- ❌ One uniform intermediate format for all content types. It flattens the differences readers need.

#### T4.4 — Validation, retry and feedback loops

- **Cross-check.** Extract `calculated_total` and `stated_total`; flag mismatches.
- **Retry with the specific error** — the failed output plus what was wrong.
- **Know when retry cannot help.** If the needed data is *not in the input* (for example, "et al." with the full author list in another document), re-prompting cannot create it. If the data *is* in the input but formatted oddly, a retry with a format hint can work.
- **Track patterns.** Add a field that records which construct caused a finding, so you can see what is being dismissed.
- **Rules across several fields need code.** "End date after start date" or "line items add up to the total" compare fields. A JSON schema checks each field, not how fields relate. Check these in validation code (the exam guide names Pydantic) and send the specific error back on the retry.

#### T4.5 — Batch processing

**Message Batches API facts:**

- **50% cheaper** than standard calls.
- Most batches finish within **1 hour**. Requests not done within **24 hours** expire.
- **No latency guarantee.** Do not use it for blocking work like pre-merge checks.
- No multi-turn tool calling inside one request.
- Use `custom_id` to match each response to its request.

**Rules:**

- Batch the routine work; send urgent work to the real-time API.
- **SLA arithmetic with headroom:** `longest wait before sending + longest processing time ≤ SLA − cushion`. For a 30-hour SLA with a 24-hour worst case: every 4 hours → 28 hours (2-hour cushion) ✅. Every 6 hours → 30 hours, no margin ❌.
- **Failures:** resubmit only the failed requests (by `custom_id`), changed as needed — for example, chunk documents that were too long.
- **Refine the prompt on a sample** before sending a large batch.

#### T4.6 — Multi-instance and multi-pass review

A model reviewing its own work in the same session is biased toward it.

- ❌ Turn on extended thinking, make the review prompt harsher, or ask for a confidence score.
- ✅ An independent instance that sees only the diff and the review criteria.

**Multi-pass review of many files.** Do one pass per file for local issues, then a separate pass for cross-file issues. One huge pass spreads attention too thin.

---

### Domain 5 — Context Management & Reliability (15%)

#### T5.1 — Conversation context

**Risks:**

- **Progressive summarization** turns exact amounts, dates and promises into vague text.
- **Lost in the middle:** models handle the start and end of long inputs well, and may miss the middle.
- **Tool results pile up.** An order lookup may return 40 fields when 5 matter.
- **Stateless API:** if the agent "forgets" earlier turns, you are probably not sending the full history with each request.

**Fixes:**

- A **case-facts block** — amounts, dates, order numbers, statuses, promises — included in every prompt, outside the summarized history.
- For multi-issue sessions, **structured issue data** (order IDs, amounts, statuses) in a separate context layer.
- **Trim** tool output to the relevant fields before it accumulates.
- Put **key findings first** in long inputs, with clear section headers.

**Example.** Refund (turns 1–15), subscription (16–30), payment method (31–45). At turn 48: "What happened with my refund?" Context is nearly full.

- ❌ A sliding window of the last 30 turns. It drops the refund.
- ❌ Summarize earlier turns as narrative. The exact refund details blur.
- ✅ Extract structured issue data (order IDs, amounts, statuses) into a separate context layer.

#### T5.2 — Escalation and ambiguity resolution

See Rule 3 in Part 1 for the full table. In short:

- **Explicit demand for a human → escalate immediately, without investigating first.**
- **Frustration, fix within capability → acknowledge, offer to resolve, escalate if they repeat the request.**
- **Policy silent or unclear → escalate.**
- **Several matching records → ask for another identifier.**
- Sentiment and self-reported confidence are poor escalation triggers.
- Put explicit escalation criteria, with a few examples, in the system prompt.

#### T5.3 — Error propagation in multi-agent systems

A subagent's failure must reach the coordinator **as structured information**: failure type, what was tried, partial results, possible alternatives.

- **Access failure** (timeout) ≠ **valid empty result** (the search worked and found nothing). Report them differently.
- Subagents should retry transient failures locally and pass up only what they cannot fix.
- Mark coverage in the final output: which findings are well supported, and where sources were missing.

- ❌ Return empty results as if they were a success.
- ❌ Fail the whole workflow because one subagent failed.
- ❌ A generic "search unavailable".
- ✅ Five of seven queries worked → return those five plus structured context on the two that failed.

#### T5.4 — Exploring large codebases

**Context degradation:** in long sessions the model starts citing "typical patterns" instead of the specific classes it found.

**Patterns:**

- **Scratchpad file** — write key findings to a file and refer back to it.
- **Incremental trace** — Grep the entry points, follow imports, widen only as needed.
- **Subagents for named questions** — "find all test files for payments", "trace the refund flow". The main agent keeps the overview.
- **Summarize, then spawn** — inject the findings so far into the new subagent's first prompt.
- **Crash recovery** — each agent writes its state to a known location; on resume the coordinator loads it and injects it into prompts.
- **`/compact`** — reduces context when it fills with verbose discovery output.

| Blind fan-out ❌ | Scoped delegation ✅ |
|---|---|
| split by folder or file count | split by a named question |
| before you know where the answer is | once you know what you are looking for |
| main agent must read it all back | main agent keeps the overview |

- ❌ Spawn eight subagents to read eight folders, or read all 400 files first.
- ❌ Write a summary report, clear context, and continue from the report only.
- ✅ Grep the payment entry points, follow imports, note findings in a scratchpad.

#### T5.5 — Human review and confidence calibration

- **Route review effort** with field-level confidence scores, calibrated on a labelled validation set. Low confidence or contradictory sources → human.
- **Measure an automated stream** with stratified random sampling of high-confidence extractions. This also catches new error patterns.
- **Check accuracy by document type and field** before cutting human review. An overall 97% can hide one segment that fails badly.

- ❌ Send a random 20% of items to reviewers to decide what they check.
- ❌ "97% overall, so we can automate."

#### T5.6 — Provenance and conflicting sources

**Capture sources at ingestion, not afterwards.** As each source is read, tag every claim with its source and record conflicts in a structured index.

- ❌ Write the report, then guess which source each claim came from.
- ✅ Claim-to-source mappings from the start, which the synthesis step must preserve and merge.

**Other rules:**

- When sources conflict, show both values with their sources. Do not pick one quietly.
- Keep dates and collection periods in structured output, so a difference in time is not mistaken for a contradiction.
- Separate well-established findings from contested ones in the report.

---

## Part 3 — Self-Test

Cover the answer. Say which rule applies and why, then check.

### A. The three rules

**1.** The path through a task depends on what each step reveals. Fixed chain, full upfront plan, or adaptive?
> **Adaptive.** The facts needed to plan do not exist yet. (Rule 1; T1.6, decomposition)

**2.** A rule must never be broken, and its threshold ($10,000) is known today. Prompt instruction, escalation criteria, or a hook?
> **A hook that blocks the call before it runs.** Known rule plus unacceptable failure → enforce in code. (Rule 1 boundary; T1.5, hooks)

**3.** Should that hook be PreToolUse or PostToolUse?
> **PreToolUse** (a tool call interception hook). PostToolUse runs after the tool, so the refund would already be issued. (T1.5)

**4.** 500 known invoices, the same extraction on each, all independent. Sequential or fan-out?
> **Fan-out.** Known, complete, independent work. (Rule 1 boundary; T1.2)

**5.** A live 45-minute conversation is filling context; the current issue is active. Vector DB, fresh session, or keep-and-prune?
> **Keep the active thread, prune resolved parts, keep hard facts in a separate block.** (Rule 2; T5.1)

**6.** You need to recall how similar issues were solved for thousands of other customers. In context or external store?
> **External store.** Large, lasting, cross-session knowledge. (Rule 2 boundary)

**7.** A customer returns hours later; old tool results are stale. Re-call every tool, or new session + summary + fresh calls?
> **New session, structured summary, fresh calls.** (Rule 2 boundary; T5.1)

**8.** "I want to talk to a real person NOW." No tools called yet. What does the agent do?
> **Escalate immediately, passing the conversation history.** An explicit demand is honoured without investigating first. (Rule 3; T5.2)

**9.** "Third time this week this broke — infuriating." No request for a human. The fix is one documented step within the agent's authority.
> **Acknowledge, fix it, offer a human if they prefer.** Escalate only if they ask for a person. (Rule 3; T5.2)

**10.** The customer asks for a competitor price match. Policy only covers own-site price changes.
> **Escalate.** Policy is silent; do not treat silence as a "no". (T5.2)

### B. Orchestration and sessions (Domain 1)

**11.** A synthesis subagent's report is missing the research. Most likely cause?
> **The coordinator did not put the findings in its prompt.** Subagents do not inherit context. (T1.3)

**12.** A coordinator cannot spawn subagents at all. What do you check first?
> **Is `"Task"` in its `allowedTools`?** (T1.3; called Agent in current Claude Code)

**13.** Compare two refactoring strategies from the same starting point.
> **Resume the session with forking enabled** — one branch per strategy. (T1.7)

**14.** The coordinator gets a one-line follow-up it could answer itself.
> **Answer it directly.** Do not spawn a subagent for trivial work. (T1.2)

**15.** Escalating a billing dispute to a human who cannot see the transcript. What do you send?
> **A structured summary:** customer ID, root cause, amount, recommended action. (T1.4)

**16.** Eight files into a 45-file module, the agent is forgetting what it read.
> **Spawn subagents for specific, named questions** while the main agent coordinates. (T5.4)

### C. Tools and MCP (Domain 2)

**17.** The model keeps choosing the wrong one of several clear MCP tools. First lever?
> **Sharpen the tool descriptions.** (T2.1)

**18.** One generic tool with a free-text instruction keeps returning the wrong output shape.
> **Split it into purpose-specific tools with defined contracts.** (T2.1)

**19.** An MCP tool's downstream service is down. Throw, or return what?
> **Return a tool result with `isError: true` and a content array** describing the error. Add the exam guide's metadata (category: transient, retryable: true). (T2.2)

**20.** Force a context-fetch tool on the first call only.
> **Force that tool on the first call, then `auto`.** (T2.3)

**21.** A shared MCP server needs an API token.
> **`.mcp.json` with `${TOKEN}` env-var expansion.** Never commit the token. (T2.4)

**22.** Edit fails because the `old_string` appears five times.
> **Use a longer, unique `old_string`** (or `replace_all` if all should change). Read + Write is the fallback. (T2.5)

### D. Claude Code (Domain 3)

**23.** A teammate says the root `CLAUDE.md` only loads if you `@import` it.
> **False.** It loads automatically. (T3.1)

**24.** Your `~/.claude/CLAUDE.md` contradicts the project `CLAUDE.md`. Which wins?
> **Neither is guaranteed.** Files are combined, not overridden; Claude may follow either. Remove the conflict. (T3.1)

**25.** A `/scan` command dumps thousands of lines. Fork it? Why?
> **Yes — because of output volume.** (T3.2)

**26.** A skill runs for 25 minutes and prints six lines. "Fork it so it runs in the background."
> **No.** Fork controls where output lands, not when work runs. (T3.2)

**27.** API conventions apply to every caller, all over the repo. `paths: ["src/api/**"]`?
> **No — the glob is narrower than the convention.** Use the project CLAUDE.md or a glob that covers every caller. (T3.1, T3.3)

**28.** A skill must be read-only. Which frontmatter field, by the exam guide?
> **`allowed-tools`** with read-only tools. (In current Claude Code, use `disallowed-tools` to truly restrict.) (T3.2)

**29.** CI must review each PR and emit parseable findings.
> **Fresh `claude -p` + `--output-format json` + `--json-schema`.** Not `--resume`. (T3.6)

### E. Structured output and reliability (Domains 4 and 5)

**30.** Extractions invent values for fields not in the document.
> **Instruct: return null when the value is not stated** (and make the field nullable). (T4.1)

**31.** A category field keeps hitting values outside the enum.
> **`enum` + `"other"` + a `detail` field.** (T4.3)

**32.** SLA 30 hours at 99.9%; batches can take 24 hours. Every 6 hours or every 4?
> **Every 4 hours** — 28 hours, 2-hour cushion. (T4.5)

**33.** Should pre-merge checks use the Batch API to save 50%?
> **No.** No latency guarantee; blocking work needs the real-time API. (T4.5)

**34.** "97% overall accuracy." Cut human review?
> **First break accuracy down by document type and field.** (T5.5)

**35.** Scarce reviewers — how do you choose what they check?
> **Field-level confidence, calibrated on a labelled validation set.** (T5.5)

**36.** Thirty conflicting sources; stakeholders need to trace each claim. When do you capture provenance?
> **At ingestion** — tag claims with sources and log conflicts as you read. (T5.6)

**37.** 400-file repo: "Why does checkout double-charge?" First move?
> **Grep the payment entry points and follow imports.** (T5.4)

**38.** Two of seven subagent searches time out after a local retry.
> **Return the five results plus structured error context for the two failures.** (T5.3)
