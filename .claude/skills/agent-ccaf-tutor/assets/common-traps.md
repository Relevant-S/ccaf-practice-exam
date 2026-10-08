# Common Traps — Distractor Patterns on the CCAF Exam

A library of the wrong moves that catch most CCAF learners. Each one looks reasonable. Each one fails for a reason you can name.

**How the tutor uses this file:**

- **When explaining a wrong answer.** Find the trap the learner fell into. Name it. Show the right move. Then show the boundary case, so the learner does not over-correct.
- **When writing a question.** Each trap is a family of distractors. Build one wrong option from the trap. Now and then, write a question where the boundary case applies and the "trap" move is the right answer. That checks the learner reads the scenario and does not just flip a reflex.

**How each trap is laid out:**

| Field | What it holds |
|---|---|
| Tempting wrong move | What the distractor offers |
| Why it tempts | Why a smart person picks it |
| Right move | What the exam rewards instead |
| When the "wrong" move is right | The boundary case. Teach this too, or the learner over-corrects. |
| Task statements | Where it shows up in the exam guide |
| Bank examples | Questions in `assets/question-bank/` that test it |

Exam answers follow the official exam guide. Where current Claude products behave differently, the study guide (`references/study-guide.md`) has a "Product drift" note.

---

## Trap 1 — Structure over judgment

**Tempting wrong move.** Add a layer that decides *for* the model. Examples:

- a classifier that sorts each request into a fixed bucket
- a rules engine keyed on issue type and customer segment
- a fixed "fast path" router for simple-looking queries
- a full plan written before the agent has looked at anything
- many subagents launched at once, before anyone knows where the answer is ("premature fan-out")

**Why it tempts.** Structure feels safe, testable and in control. It looks like good engineering.

**Right move.** Give the model a goal and explicit criteria. Criteria means things like a quality bar, what counts as "resolved", and when to escalate. Then let it decide at runtime, one step at a time.

The reason is simple. The facts needed to decide well only exist once the real request arrives. A classifier or upfront plan decides before those facts exist. It breaks on cases nobody planned for.

**One-line test.** Does this design make the decision at build time (before the facts exist) or at runtime (when they exist)? Prefer runtime.

**When the "wrong" move is right.**

- **A hard rule that must never fail → put it in code (a hook or gate).** Use this when the rule is known in advance *and* one miss is unacceptable. Example: "no refund over $500 without human approval". A prompt, however firm, is followed most of the time, not every time. See bank q-017 (refund gate via a hook).
- **Known, complete, independent work → fan out.** Example: the same 12-field extraction over 340 known contracts. There is nothing to discover about *what* to do, only volume. See bank q-067 (fixed fan-out wins) and q-033 (coordinator spawns parallel subagents for precedents).
- **Known steps that depend on each other → a fixed pipeline (prompt chaining).** Example: collect → analyze → report, where each step needs the last one's output. The steps are known, so nothing needs deciding at runtime. Quick sort: known and independent → fan out; known and dependent → chain; unknown → adaptive. (T1.6, task decomposition.)

**Do not over-correct the other way: match the mechanism to the stakes.** Not every guideline needs a hook. A style or judgment rule (naming, tone, "back up before a risky overwrite" in a repo where every change can be undone) can stay in the prompt, even if it is followed only most of the time. Two-question test for a hook:

1. Can plain code check or apply it, with no judgment?
2. Must it hold every single time, because one miss does real harm?

Two yeses → a hook or gate. Otherwise → prompt guidance, explicit criteria or few-shot examples. (T1.4 and T1.5: hooks for guaranteed compliance, prompts for probabilistic compliance.)

**Task statements.** T1.2 (coordinator–subagent orchestration), T1.4 (multi-step workflows and escalation criteria), T1.5 (hooks), T1.6 (task decomposition), T5.4 (large codebase exploration).

**Bank examples.** q-010 (adaptive investigation of an unknown error), q-026 (natural-language escalation criteria, not a rules engine), q-037 (give the subagent goals and quality criteria, not steps), q-039 (coordinator picks subagents per query, not a fixed router), q-007 (Grep the entry points and follow imports, not parallel subagents), q-085 (three files already found — just read them).

---

## Trap 2 — Compress or replace, instead of preserve and add

**Tempting wrong move.** When context gets full or noisy, throw the live state away or squash it. Examples:

- summarize the whole conversation into one paragraph, including the issue still being worked on
- start a fresh session and rebuild everything
- move a live, bounded conversation into a vector database
- re-run every earlier tool call "to be safe"
- write a summary report, clear the context, and work only from the report

**Why it tempts.** Each option clearly "saves space" or "refreshes data". It sounds tidy.

**Right move.** Keep the active thread at full detail. Prune what is finished: replace a resolved sub-thread with a short summary, and drop tool output that newer output has replaced. Trim verbose tool results to the fields you need. Pull hard facts (amounts, dates, order numbers, statuses, promises) into a separate block that is never summarized. Compress only what is already resolved, never the active thread.

**When the "wrong" move is right.**

| Heavier move | Wrong when | Right when |
|---|---|---|
| External store (vector DB, knowledge base) | managing one live, bounded conversation | the knowledge is large, lasting and shared across sessions — for example "how were similar issues solved for thousands of other customers?" |
| Fresh session | it throws away a live conversation and re-runs every tool | the customer comes back later and old tool results are stale. Start fresh, inject a short structured summary, then re-fetch only what this request needs. See bank q-021 (returning customer with stale results). |
| Summarize / `/compact` | done early, on the active thread, or in a way that loses exact facts | done on resolved or verbose discovery output, with the hard facts kept elsewhere |

**The developer version of the fresh-session case.** A coding session is polluted: three fix attempts failed, and a teammate's push made earlier file reads out of date. Right: a fresh session, plus an injected summary of what was found *and what was tried and failed*, then re-read the current files. Wrong: re-read the files in the same session (the stale results stay in context). Wrong: fork the session (the fork copies the clutter). Wrong: a blank session with no summary (it loses the lessons). The exam guide (T1.7) says to start fresh with injected summaries when earlier tool results are stale.

A common slip: rejecting a fresh session "because the old results are stale". Re-running tools would refresh them, so staleness is not the problem. The problem with "resume and re-call everything" is cost, and that the old results still sit in context and confuse the model.

**Task statements.** T1.7 (session resumption and forking), T5.1 (conversation context), T5.4 (codebase exploration and scratchpads), T5.6 (provenance).

**Bank examples.** q-001 (scratchpad file, not pre-summarizing), q-003 (spawn subagents for named questions, not summary-then-clear), q-021 (new session + summary + fresh calls), q-025 (trim order data to relevant fields, not a vector DB), q-068 (case-facts block outside the summarized history).

---

## Trap 3 — Mishandling the customer's signal

**Tempting wrong move.** One of these:

- investigate first (look up the account, call tools) when the customer has demanded a human
- interrogate the customer about what went wrong in earlier attempts
- quietly fix the problem yourself when the customer clearly asked for a person
- escalate because the customer sounds upset, when they did not ask for a human
- refuse, or stretch a policy by analogy, when the policy says nothing about the request

**Why it tempts.** Investigating feels thorough. Fixing feels helpful. Escalating on anger feels kind. Each sounds like good service.

**Right move.** First decide which case you are in. The exam guide (T5.2) separates them on purpose.

| What the customer did | Right move |
|---|---|
| **Explicitly demanded a human** ("I want to talk to a real person NOW") | Escalate now. Do not investigate first. Pass the context you have (the conversation history) to the human. See bank q-019. |
| **Frustrated, no demand for a human**, and the fix is within the agent's power | Acknowledge the frustration. Say it can be fixed now. Offer to fix it. Escalate if they repeat that they want a person. See bank q-081 (fix the token refresh, offer a human). |
| **Asks for "someone who can help"** while the fix is confirmed, simple and one step away | The bank answer is: acknowledge, say it is resolvable now, offer to complete it *or* escalate — their choice. Do not act without asking. See bank q-028. |
| **Policy is silent or unclear** on what they ask | Escalate. Do not treat silence as a "no", and do not invent a rule by analogy. See bank q-082 (competitor price match). |
| **Several customer records match** | Ask for another identifier. Do not guess. |

**Two rules that hold in every row:**

- Do not interrogate the customer about past attempts.
- Do not silently resolve over an explicit request for a person.

**When the "wrong" move is right.** Escalating on sentiment alone is wrong. Sentiment does not tell you how hard the case is. But if a frustrated customer *repeats* their wish for a person after you offered to help, that repeat is the trigger. Escalate then.

**Tutor note.** Phrasing decides which row applies. A clear demand ("connect me to a person", "I want a human NOW") is row one. Read the exact words before choosing. If a question's wording is truly between rows, say so when explaining it.

**Task statements.** T5.2 (escalation and ambiguity resolution), T1.4 (handoff patterns).

**Bank examples.** q-019, q-026, q-028, q-065 (when to ask a clarifying question), q-081, q-082.

---

## Trap 4 — Forking context for the wrong reason

**Tempting wrong move.** Add `context: fork` to a skill because:

- it takes a long time to run
- forking will let it "run in the background" while you keep working
- forking will sandbox it or make it read-only

**Why it tempts.** The word "fork" sounds like process forking, so people think of time, concurrency and isolation of *execution*.

**Right move.** `context: fork` runs the skill in a separate sub-agent context. Its job is to keep the skill's output out of the main conversation. The trigger is **verbose output** (thousands of lines of analysis) or **exploratory context** (brainstorming alternatives) that would pollute the main session. Only the result comes back.

| Wrong reason | Why it is wrong |
|---|---|
| "It runs for a long time" | Runtime does not matter. A 25-minute skill that prints six lines does not need a fork. |
| "It lets it run in the background" | Fork decides *where output lands*, not *when work runs*. |
| "It sandboxes it" | Limiting tools is a different frontmatter field (`allowed-tools` in the exam guide's terms). |

**One-line test.** How much output would land in the main conversation? A lot → fork. Very little → do not fork.

**When the "wrong" move is right.** There is no case where duration alone justifies a fork. But a long-running skill that *also* streams a flood of output should be forked — because of the output.

**Task statements.** T3.2 (custom slash commands and skills).

**Bank examples.** q-073 (fork the 3,000-line audit, not the slow 4-line one), q-079 (reject a fork for a six-line skill), q-084 (fork the skill that emits 9,000 lines before a short verdict), q-080 (`allowed-tools` for a read-only guarantee).

---

## Trap 5 — A path rule narrower than the convention, and choosing the wrong home

**Tempting wrong move.** Put a team convention in `.claude/rules/` with a `paths:` glob that covers only part of the code the convention governs. Example: API-calling conventions with `paths: ["src/api/**"]`, when callers of the API live all over the repo.

**Why it tempts.** Path rules feel precise and modern. They save context. People pick the most finely scoped tool without checking its reach.

**Right move.** Compare two things: where the glob matches, and where the convention applies. If the glob is narrower, the convention silently disappears outside it.

| Where the convention applies | Home |
|---|---|
| Everywhere in the project, all the time | Project `CLAUDE.md` (committed) |
| A real file pattern, even if spread across many folders (`**/*.test.ts`, `terraform/**/*`) | `.claude/rules/*.md` with a `paths:` glob that matches every such file |
| A task done now and then (a release procedure, a migration) | An on-demand skill in `.claude/skills/` |
| Just you, not the team | User-level `~/.claude/CLAUDE.md` — it is not shared through version control |

**When the "wrong" move is right.** A `paths:` rule is the best choice when a real file pattern exists and matches the convention's whole reach. It beats a subdirectory `CLAUDE.md` when the files are spread across many directories.

**Task statements.** T3.1 (CLAUDE.md hierarchy and scoping), T3.2 (skills vs CLAUDE.md), T3.3 (path-specific rules).

**Bank examples.** q-070 (test conventions → rules file with a glob), q-072 (conventions not reaching teammates → committed root CLAUDE.md), q-077 (release procedure → a skill with `argument-hint`).

---

## Trap 6 — Splitting state ownership

**Tempting wrong move.**

- In multi-agent systems: give each agent its own state file and let each reload it on its own after a crash.
- In long conversations: keep only a loose narrative summary, so exact facts blur. Or the reverse: keep only a facts table and drop the conversation the customer expects you to remember.

**Why it tempts.** Separate state per agent feels modular. A summary feels efficient.

**Right move.**

- **Multi-agent crash recovery:** each agent writes a structured report to a known place. On resume, the coordinator loads the reports and injects the relevant state into each agent's prompt. The coordinator stays in charge. See bank q-045.
- **Long multi-issue conversations:** keep exact facts (order IDs, amounts, statuses, dates) in a separate structured layer that is sent every turn. Keep it *alongside* the conversation, not instead of it. See bank q-030 (structured issue data in a separate context layer) and q-068 (case-facts block).

**When the "wrong" move is right.** Separate per-agent output is fine — as long as the coordinator is the one that reads it and decides what each agent sees.

**Task statements.** T1.2 (coordinator orchestration), T1.3 (context passing), T5.1 (conversation context), T5.4 (crash recovery with manifests).

**Bank examples.** q-030, q-045, q-068.

---

## Trap 7 — SLA arithmetic with no headroom

**Tempting wrong move.** Pick the option whose worst case lands exactly on the deadline. Example: a 30-hour SLA, batches every 6 hours, up to 24 hours to process → 30 hours worst case.

**Why it tempts.** The numbers add up. It also maximizes batch size and savings.

**Right move.** Use this formula:

`longest wait before a batch is sent + longest processing time ≤ SLA − a safety cushion`

Batches every 4 hours give 4 + 24 = 28 hours, which leaves a 2-hour cushion. A target like 99.9% needs margin, not a tie.

**When the "wrong" move is right.** Never at a high reliability target. If the scenario says the deadline is soft, a tighter fit may be fine — but the exam rarely says that.

**Related.** The Batch API has no latency guarantee. Do not use it for blocking work like pre-merge checks. Batch the routine work; send urgent work to the real-time API.

**Task statements.** T4.5 (batch processing).

**Bank examples.** q-046 (every 4 hours, not every 6), q-054 (resubmit only the failed documents, chunked), q-055 (batch the routine, real-time the urgent).

---

## Trap 8 — Smaller recurring traps

Short entries. Same layout, compressed.

### 8a. Raw artifacts in a human handoff

- **Wrong:** forward the original complaint plus raw tool output to the human agent.
- **Why it tempts:** nothing is lost.
- **Right:** a structured summary — customer ID, root cause, amount, action taken or recommended, reason for escalation. The human often cannot see the transcript and should not redo the agent's work.
- **Boundary:** passing the conversation history along *with* an immediate escalation is fine (bank q-019). The trap is raw dumps *instead of* synthesis.
- **Task statement:** T1.4 (handoff patterns). **Bank:** q-027 (billing-dispute handoff), q-018 (structured handoff before `escalate_to_human`).

### 8b. A richer description for a vague, multi-purpose tool

- **Wrong:** fix a generic `analyze_document(document, instruction)` tool by adding examples to its description, or an `analysis_type` enum.
- **Why it tempts:** better descriptions *do* fix wrong tool choice.
- **Right:** split it into purpose-specific tools, each with its own input and output contract.
- **Boundary:** when the model picks the wrong one of several *clear* tools, sharpen the descriptions. That is the right fix there. See bank q-004 and q-008.
- **Task statement:** T2.1 (tool interfaces and descriptions). **Bank:** q-035.

### 8c. Forcing `tool_choice` on every call

- **Wrong:** set `tool_choice` to a specific tool on every turn.
- **Why it tempts:** it guarantees the tool runs.
- **Right:** force it on the first call only, then let the model choose in later turns.
- **Boundary:** forcing a specific tool once is exactly right when one step must come first (for example, metadata extraction before enrichment).
- **Task statement:** T2.3 (tool distribution and `tool_choice`), T4.3 (structured output). **Bank:** q-050.

### 8d. One uniform representation for every content type

- **Wrong:** push all content (financial data, news, research) through one shared intermediate format before rendering.
- **Why it tempts:** it looks clean and consistent.
- **Right:** render by type — tables for financial data, prose for news.
- **Task statement:** T4.3 (structured output). **Bank:** q-040.

### 8e. Mapping unknown values to the closest enum

- **Wrong:** when a category is not in the enum, pick the nearest one.
- **Why it tempts:** the schema stays strict.
- **Right:** add an `other` value plus a free-text `detail` field. Nothing is lost, and new categories become visible.
- **Task statement:** T4.3. **Bank:** q-057.

### 8f. Random sampling to decide what reviewers check

- **Wrong:** send a random share of extractions to human reviewers to "allocate" scarce review time.
- **Why it tempts:** random sampling is a sound statistical tool.
- **Right:** have the model output field-level confidence. Calibrate the review threshold on a labelled validation set. Route low-confidence fields to humans.
- **Boundary:** stratified random sampling *is* right for **measuring** the error rate of extractions that are already auto-approved, and for catching new error patterns. Measuring a stream is a different job from choosing which items a reviewer sees. See bank q-083.
- **Task statement:** T5.5 (human review and confidence calibration). **Bank:** q-047.

### 8g. Trusting an aggregate accuracy number

- **Wrong:** "97% overall accuracy, so we can cut human review."
- **Why it tempts:** it is a big, real number.
- **Right:** break accuracy down by document type and by field first. The total can hide one segment that fails badly.
- **Task statement:** T5.5. **Bank:** q-051.

### 8h. "The synthesis agent needs tools"

- **Wrong:** the synthesis subagent is missing earlier results, so give it tools to fetch other agents' histories.
- **Why it tempts:** it sounds like adding capability.
- **Right:** subagents do not inherit the coordinator's context. The coordinator must put earlier outputs into the synthesis agent's prompt.
- **Also wrong:** run the agents one after another and assume the later one sees the earlier output. Running in sequence is not passing context. The data still has to be in the prompt.
- **Task statement:** T1.3 (subagent invocation and context passing). **Bank:** q-034, q-043.

### 8i. Letting a subagent spawn its own children

- **Wrong:** speed up work by letting a subagent spawn more subagents, or build a recursive hierarchy, or use an external queue.
- **Why it tempts:** it looks like more parallelism.
- **Right:** the coordinator spawns the parallel subagents itself and aggregates the results. That keeps one hub that can see what ran, what failed and what came back.
- **Task statement:** T1.2 (coordinator–subagent orchestration). **Bank:** q-033.

### 8j. Spawning a subagent for trivial work

- **Wrong:** send a one-line follow-up to a new subagent.
- **Right:** the coordinator answers it directly. Save subagents for scoped work that gains from isolation.
- **Task statement:** T1.2. **Bank:** q-042.

### 8k. Cleaning up afterwards instead of fixing at the source

- **Wrong:** detailed instructions still give inconsistent output (assertion styles, finding format, how skills are split), so add a linter, a rewriter or a post-processing step to tidy it afterwards.
- **Why it tempts:** code feels reliable, and the tidy-up step does make the output look consistent.
- **Right:** fix it at the source. Add 2–4 few-shot examples of the output you want, with the reason for each, covering the varied cases. The exam guide calls few-shot examples the most effective technique when detailed instructions alone give inconsistent results.
- **Boundary:** use the two-question test from Trap 1. If plain code can do it with no judgment *and* it must hold every time (for example, run the formatter on every file Claude writes), a hook is right — here a PostToolUse hook.
- **Task statement:** T4.2 (few-shot prompting), T1.5 (hooks). **Bank:** q-056 (few-shot examples, not post-extraction normalization), q-048.

### 8l. Trusting the JSON schema with rules across several fields

- **Wrong:** count on the strict JSON schema to make sure "end date is after start date" or "line items add up to the total".
- **Why it tempts:** tool use with a schema already guarantees the output's shape.
- **Right:** a schema checks each field's shape and type. It cannot express rules that compare fields. Check those in validation code (the exam guide names Pydantic), and send the specific error back on the retry. Or extract both values (`calculated_total` and `stated_total`) and flag a mismatch.
- **Boundary:** for syntax and shape errors, the schema via tool use is enough. No extra code is needed for those.
- **Task statement:** T4.3 (schemas remove syntax errors, not meaning errors), T4.4 (validation and retry). **Bank:** q-060 (cross-check the totals).

---

## Trap 9 — Reading the options before the scenario

This is a reading habit, not a knowledge gap. It causes misses even when the learner knows the rule.

**Tempting wrong move.** Read the options, then pick the one that echoes the scenario's last or loudest number or phrase.

**Why it tempts.** Scenarios often end with a vivid detail. Options are written to quote it.

**Right move — the four-step reading protocol:**

1. **Name the rule** the question is testing (for example, "the fork trigger").
2. **Name the quantity the rule needs** (for the fork trigger: total output that would land in the main conversation — not runtime, not summary length).
3. **Find that quantity in the text**, wherever it sits. It may be early, in the middle, or buried in a sentence.
4. **Only then read the options.**

**Choose-N items.** Exam guide v1.0 has two item types: multiple choice and multiple response. Each item says how many answers to choose. For a choose-N item, judge each option true or false on its own against the scenario. Then check you picked exactly N. The guide does not say how blank answers or multiple-response items are scored, so answer every question.

**Tutor note.** When writing questions, sometimes place the deciding figure early and end the scenario with a decoy figure. If a learner misses one, ask them to run the four steps aloud.

**Task statements.** All of them.
