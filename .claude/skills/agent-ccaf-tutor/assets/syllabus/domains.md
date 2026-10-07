# CCAF Foundations — Domains, Task Statements, and Exam Scenarios

Faithful structured restatement of Anthropic's *Claude Certified Architect – Foundations Certification Exam Guide* (Version 0.1, Feb 10 2025). Source PDF: `references/certification-exam-guide/Claude+Certified+Architect+–+Foundations+Certification+Exam+Guide.pdf`.

---

## Exam Format

- **Question type:** Multiple choice, single correct answer. 4 options. Distractors are designed to look plausible to a candidate with incomplete knowledge.
- **Scoring:** Scaled 100–1,000. **Pass mark: 720.** Pass/fail designation. No penalty for guessing — unanswered questions count as incorrect.
- **Scenario structure:** The exam draws **4 scenarios at random from the 6 scenarios** below. Each scenario frames a set of questions in a realistic production context.
- **Target candidate:** Solution architect with 6+ months of hands-on experience building with Claude APIs, Agent SDK, Claude Code, and MCP.

## The 6 Exam Scenarios

Each scenario is a recurring backdrop that Richard should use when generating new questions, so they feel exam-realistic.

| # | Scenario | Primary domains |
|---|---|---|
| 1 | **Customer Support Resolution Agent** — Agent SDK; MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`; target 80%+ first-contact resolution | D1, D2, D5 |
| 2 | **Code Generation with Claude Code** — Custom slash commands, CLAUDE.md, plan mode vs direct execution | D3, D5 |
| 3 | **Multi-Agent Research System** — Coordinator + specialized subagents (web search, document analysis, synthesis, report generation) | D1, D2, D5 |
| 4 | **Developer Productivity with Claude** — Claude Agent SDK + built-in tools (Read, Write, Bash, Grep, Glob) + MCP servers for codebase exploration | D2, D3, D1 |
| 5 | **Claude Code for CI/CD** — Automated code review, test generation, PR feedback; minimize false positives | D3, D4 |
| 6 | **Structured Data Extraction** — JSON schema validation, edge cases, downstream system integration | D4, D5 |

## Domain Weightings

| # | Domain | Weight |
|---|---|---:|
| D1 | Agentic Architecture & Orchestration | **27%** |
| D2 | Tool Design & MCP Integration | **18%** |
| D3 | Claude Code Configuration & Workflows | **20%** |
| D4 | Prompt Engineering & Structured Output | **20%** |
| D5 | Context Management & Reliability | **15%** |

---

## Domain 1 — Agentic Architecture & Orchestration (27%)

### T1.1 Design and implement agentic loops for autonomous task execution

**Knowledge of:**
- The agentic loop lifecycle: send request to Claude, inspect `stop_reason` (`"tool_use"` vs `"end_turn"`), execute requested tools, return results for the next iteration.
- How tool results are appended to conversation history so the model can reason about the next action.
- The distinction between **model-driven decision-making** (Claude chooses tools based on context) and **pre-configured decision trees** or fixed tool sequences.

**Skills in:**
- Implementing loop control flow that continues when `stop_reason == "tool_use"` and terminates when `stop_reason == "end_turn"`.
- Adding tool results to conversation context between iterations.
- **Avoiding anti-patterns:** parsing natural language to determine loop termination, using arbitrary iteration caps as the *primary* stopping mechanism, checking assistant text content as a completion indicator.

### T1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

**Knowledge of:**
- **Hub-and-spoke architecture** — coordinator manages all inter-subagent communication, error handling, routing.
- Subagents have **isolated context** — they do not inherit the coordinator's conversation history automatically.
- The coordinator's role: task decomposition, delegation, result aggregation, deciding which subagents to invoke based on query complexity.
- Risk: **overly narrow task decomposition** by the coordinator → incomplete coverage of broad topics.

**Skills in:**
- Coordinator agents that **dynamically select** which subagents to invoke based on query requirements (vs always routing through the full pipeline).
- Partitioning research scope across subagents to minimize duplication.
- **Iterative refinement loops** — coordinator evaluates synthesis output for gaps, re-delegates with targeted queries, re-invokes synthesis until coverage is sufficient.
- Routing all subagent communication through the coordinator for observability and consistent error handling.

### T1.3 Configure subagent invocation, context passing, and spawning

**Knowledge of:**
- The `Task` tool spawns subagents — `allowedTools` must include `"Task"` for a coordinator to invoke subagents.
- Subagent context must be **explicitly provided in the prompt** — no automatic inheritance, no shared memory between invocations.
- `AgentDefinition` configuration: descriptions, system prompts, tool restrictions per subagent type.
- **Fork-based session management** for exploring divergent approaches from a shared analysis baseline.

**Skills in:**
- Including complete prior-agent findings directly in the subagent's prompt (e.g., passing search results to the synthesis subagent).
- Using **structured data formats** to separate content from metadata (URLs, document names, page numbers) when passing context between agents.
- **Spawning parallel subagents** by emitting multiple `Task` tool calls in a single coordinator response (not across separate turns).
- Coordinator prompts that specify research goals and quality criteria — not step-by-step procedures — so subagents can adapt.

### T1.4 Implement multi-step workflows with enforcement and handoff patterns

**Knowledge of:**
- The difference between **programmatic enforcement** (hooks, prerequisite gates) and **prompt-based guidance** for workflow ordering.
- When **deterministic compliance** is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate.
- **Structured handoff protocols** for mid-process escalation: customer details, root cause, recommended actions.

**Skills in:**
- Programmatic prerequisites that block downstream tools until prerequisites complete (e.g., block `process_refund` until `get_customer` returns a verified ID).
- Decomposing multi-concern requests into distinct items, investigating each in parallel using shared context, then synthesizing a unified resolution.
- Compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to humans who lack the conversation transcript.

### T1.5 Apply Agent SDK hooks for tool call interception and data normalization

**Knowledge of:**
- `PostToolUse` hooks intercept tool results for **transformation** before the model processes them.
- Hooks that intercept **outgoing** tool calls to enforce compliance (e.g., block refunds above a threshold).
- Hooks for **deterministic guarantees** vs prompt instructions for **probabilistic compliance**.

**Skills in:**
- `PostToolUse` hooks that normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools.
- Tool-call interception hooks that block policy-violating actions (e.g., refunds > $500) and redirect to alternative workflows (human escalation).
- Choosing hooks over prompt-based enforcement when business rules require **guaranteed** compliance.

### T1.6 Design task decomposition strategies for complex workflows

**Knowledge of:**
- **Fixed sequential pipelines** (prompt chaining) vs **dynamic adaptive decomposition** based on intermediate findings.
- Prompt chaining patterns: e.g., analyze each file individually, then run a cross-file integration pass.
- Adaptive investigation plans: generate subtasks based on what is discovered at each step.

**Skills in:**
- Choosing the right pattern: **prompt chaining** for predictable multi-aspect reviews; **dynamic decomposition** for open-ended investigations.
- Splitting large code reviews into per-file local-analysis passes + a separate cross-file integration pass to avoid attention dilution.
- Decomposing open-ended tasks ("add comprehensive tests to a legacy codebase") by mapping structure first, identifying high-impact areas, then planning adaptively.

### T1.7 Manage session state, resumption, and forking

**Knowledge of:**
- Named session resumption with `--resume <session-name>`.
- `fork_session` for independent branches from a shared analysis baseline.
- Importance of informing the agent about file changes when resuming sessions after code modifications.
- Why starting fresh with a structured summary is sometimes more reliable than resuming with stale tool results.

**Skills in:**
- `--resume` for continuing named investigation sessions across work sessions.
- `fork_session` to compare two approaches (e.g., two refactoring strategies) from a shared codebase analysis.
- Choosing **resumption** (prior context still valid) vs **fresh-start with injected summary** (prior tool results stale).
- Informing a resumed session about specific file changes for targeted re-analysis.

---

## Domain 2 — Tool Design & MCP Integration (18%)

### T2.1 Design effective tool interfaces with clear descriptions and boundaries

**Knowledge of:**
- **Tool descriptions are the primary tool-selection mechanism** — minimal descriptions cause unreliable selection among similar tools.
- Effective descriptions include: input formats, example queries, edge cases, boundary explanations.
- Ambiguous/overlapping descriptions cause misrouting (e.g., `analyze_content` vs `analyze_document` with near-identical descriptions).
- System prompt wording can override tool descriptions: keyword-sensitive instructions create unintended tool associations.

**Skills in:**
- Writing tool descriptions that differentiate purpose, inputs, outputs, and *when to use this tool vs alternatives*.
- Renaming tools to eliminate functional overlap (e.g., `analyze_content` → `extract_web_results` with web-specific description).
- Splitting generic tools into purpose-specific tools (e.g., `analyze_document` → `extract_data_points` + `summarize_content` + `verify_claim_against_source`).
- Reviewing system prompts for keyword-sensitive instructions that override well-written tool descriptions.

### T2.2 Implement structured error responses for MCP tools

**Knowledge of:**
- The MCP `isError` flag for communicating tool failures.
- Error categories: **transient** (timeouts, service unavailability), **validation** (invalid input), **business** (policy violations), **permission**.
- Why uniform errors ("Operation failed") prevent the agent from making appropriate recovery decisions.
- Difference between **retryable** and **non-retryable** errors; structured metadata prevents wasted retries.

**Skills in:**
- Returning structured error metadata: `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable description.
- `retriable: false` flags + customer-friendly explanations for business-rule violations.
- Local error recovery within subagents for transient failures; propagating to coordinator only what cannot be resolved locally, with partial results and what was attempted.
- Distinguishing **access failures** (need retry decision) from **valid empty results** (successful query, no matches).

### T2.3 Distribute tools appropriately across agents and configure tool choice

**Knowledge of:**
- Too many tools (e.g., 18 instead of 4–5) **degrades selection reliability** by increasing decision complexity.
- Agents with tools outside their specialization tend to misuse them (e.g., a synthesis agent attempting web searches).
- **Scoped tool access:** give agents only the tools needed for their role; limited cross-role tools for high-frequency needs.
- `tool_choice` options: `"auto"`, `"any"`, forced selection (`{"type": "tool", "name": "..."}`).

**Skills in:**
- Restricting each subagent's tool set to those relevant to its role.
- Replacing generic tools with constrained alternatives (e.g., `fetch_url` → `load_document` that validates document URLs).
- Scoped cross-role tools for high-frequency needs (e.g., `verify_fact` for the synthesis agent) while routing complex cases through the coordinator.
- `tool_choice` forced selection to ensure a specific tool runs first (e.g., force `extract_metadata` before enrichment), then process subsequent steps in follow-up turns.
- `tool_choice: "any"` to guarantee the model calls a tool rather than returning conversational text.

### T2.4 Integrate MCP servers into Claude Code and agent workflows

**Knowledge of:**
- MCP server scoping: **project-level** (`.mcp.json`, shared via VCS) vs **user-level** (`~/.claude.json`, personal/experimental).
- Environment variable expansion in `.mcp.json` (e.g., `${GITHUB_TOKEN}`) for credentials without committing secrets.
- All configured MCP servers' tools are discovered at connection time and available simultaneously.
- **MCP resources** for exposing content catalogs (issue summaries, doc hierarchies, DB schemas) to reduce exploratory tool calls.

**Skills in:**
- Configuring shared MCP servers in project-scoped `.mcp.json` with env var expansion.
- Configuring personal/experimental MCP servers in `~/.claude.json`.
- Enhancing MCP tool descriptions to prevent the agent from preferring built-in tools (Grep) over more capable MCP tools.
- Choosing community MCP servers over custom implementations for standard integrations (e.g., Jira); reserve custom for team-specific workflows.
- Exposing content catalogs as MCP resources to give agents visibility into available data.

### T2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob)

**Knowledge of:**
- **Grep** for content search (function names, error messages, import statements).
- **Glob** for file path patterns (extension/name matching).
- **Read/Write** for full-file ops; **Edit** for targeted modifications via unique text matching.
- When Edit fails (non-unique text), fall back to Read + Write.

**Skills in:**
- Selecting Grep for code-content search across a codebase.
- Selecting Glob for filename patterns (e.g., `**/*.test.tsx`).
- Read + Write fallback when Edit cannot find unique anchor text.
- **Building codebase understanding incrementally** — start with Grep to find entry points, then use Read to follow imports, rather than reading all files upfront.
- Tracing function usage across wrapper modules: identify all exported names first, then search for each across the codebase.

---

## Domain 3 — Claude Code Configuration & Workflows (20%)

> **Note:** the question bank is currently light on Domain 3 (only ~5 questions vs the 20% exam weight). Richard should generate supplemental Claude-Code questions and direct the learner to the official Claude Code docs at https://code.claude.com/docs/ for hands-on grounding.

### T3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, modular organization

**Knowledge of:**
- CLAUDE.md hierarchy: **user-level** (`~/.claude/CLAUDE.md`), **project-level** (`.claude/CLAUDE.md` or root `CLAUDE.md`), **directory-level** (subdirectory `CLAUDE.md` files).
- User-level settings apply only to that user — `~/.claude/CLAUDE.md` is **not** shared with teammates via VCS.
- `@import` syntax for referencing external files (modular CLAUDE.md).
- `.claude/rules/` directory for topic-specific rule files as an alternative to a monolithic CLAUDE.md.

**Skills in:**
- Diagnosing config-hierarchy issues (e.g., teammate not getting instructions because they live in user-level instead of project-level).
- `@import` to selectively include relevant standards in each package's CLAUDE.md.
- Splitting large CLAUDE.md into focused topic files in `.claude/rules/` (`testing.md`, `api-conventions.md`, `deployment.md`).
- Using `/memory` to verify which memory files are loaded.

### T3.2 Create and configure custom slash commands and skills

**Knowledge of:**
- Project-scoped commands in `.claude/commands/` (shared via VCS) vs user-scoped in `~/.claude/commands/`.
- Skills in `.claude/skills/` with `SKILL.md` frontmatter: **`context: fork`**, **`allowed-tools`**, **`argument-hint`**.
- `context: fork` runs the skill in an isolated subagent context, preventing skill outputs from polluting the main conversation.
- Personal skill customization: variants in `~/.claude/skills/` with different names so teammates aren't affected.

**Skills in:**
- Project-scoped slash commands in `.claude/commands/` for team-wide availability.
- `context: fork` for skills that produce verbose output (codebase analysis) or exploratory context (brainstorming).
- `allowed-tools` to restrict tool access during skill execution (e.g., limit to file writes to prevent destructive actions).
- `argument-hint` to prompt for required parameters when invoked without args.
- Choosing between **skills** (on-demand, task-specific) and **CLAUDE.md** (always-loaded, universal standards).

### T3.3 Apply path-specific rules for conditional convention loading

**Knowledge of:**
- `.claude/rules/` files with YAML frontmatter `paths` field containing glob patterns.
- Path-scoped rules load **only** when editing matching files — reduces irrelevant context and tokens.
- Glob-pattern rules beat directory-level CLAUDE.md when conventions span multiple directories (e.g., test files spread throughout a codebase).

**Skills in:**
- Creating `.claude/rules/` files with YAML path scoping (e.g., `paths: ["terraform/**/*"]`).
- Glob patterns to apply conventions by file type regardless of directory (e.g., `**/*.test.tsx` for all test files).
- Choosing path-specific rules over subdirectory CLAUDE.md when conventions span the codebase.

### T3.4 Determine when to use plan mode vs direct execution

**Knowledge of:**
- **Plan mode** for: large-scale changes, multiple valid approaches, architectural decisions, multi-file modifications.
- **Direct execution** for: simple, well-scoped changes (e.g., adding a single validation check).
- Plan mode enables safe exploration and design before committing to changes.
- The **Explore subagent** isolates verbose discovery output and returns summaries to preserve main-conversation context.

**Skills in:**
- Plan mode for tasks with architectural implications: microservice restructuring, library migrations affecting 45+ files, choosing between integration approaches.
- Direct execution for well-understood changes with clear scope: single-file bug fix, adding a date validation conditional.
- Explore subagent for verbose discovery phases.
- Combining plan mode (investigation) with direct execution (implementation).

### T3.5 Apply iterative refinement techniques for progressive improvement

**Knowledge of:**
- **Concrete input/output examples** beat prose descriptions when the latter are interpreted inconsistently.
- **Test-driven iteration:** write tests first, share failures to guide improvement.
- **Interview pattern:** have Claude ask questions to surface considerations the developer hadn't anticipated.
- **All-issues-at-once** for interacting problems vs **sequential** for independent problems.

**Skills in:**
- 2–3 concrete input/output examples to clarify transformation requirements.
- Test suites covering expected behavior, edge cases, performance — then iterating by sharing test failures.
- Interview pattern for unfamiliar domains (cache invalidation strategies, failure modes).
- Specific test cases with example input + expected output to fix edge case handling.
- Multiple interacting issues in a single detailed message vs sequential iteration for independents.

### T3.6 Integrate Claude Code into CI/CD pipelines

**Knowledge of:**
- `-p` (or `--print`) flag for non-interactive mode in pipelines.
- `--output-format json` and `--json-schema` CLI flags for structured CI output.
- CLAUDE.md as the mechanism for providing project context (testing standards, fixtures, review criteria) to CI-invoked Claude Code.
- **Session context isolation:** the same Claude session that generated code is less effective at reviewing it than an independent review instance.

**Skills in:**
- `-p` to prevent interactive input hangs.
- `--output-format json` + `--json-schema` for machine-parseable structured findings (auto-post as inline PR comments).
- Including prior review findings on re-runs after new commits — instruct Claude to report only new or unaddressed issues.
- Providing existing test files in context so test generation doesn't duplicate.
- CLAUDE.md documenting testing standards, valuable test criteria, fixtures.

---

## Domain 4 — Prompt Engineering & Structured Output (20%)

### T4.1 Design prompts with explicit criteria to improve precision and reduce false positives

**Knowledge of:**
- **Explicit criteria** beat vague instructions ("flag comments only when claimed behavior contradicts actual code behavior" vs "check that comments are accurate").
- General instructions like "be conservative" or "only report high-confidence findings" do **not** improve precision.
- High false-positive rates undermine developer trust — bad categories poison good ones.

**Skills in:**
- Writing specific review criteria defining which issues to report (bugs, security) vs skip (minor style, local patterns) instead of confidence-based filtering.
- Temporarily disabling high false-positive categories to restore trust while improving prompts.
- Defining explicit severity criteria with concrete code examples per severity level.

### T4.2 Apply few-shot prompting to improve output consistency and quality

**Knowledge of:**
- Few-shot examples are the **most effective** technique for consistently formatted, actionable output when instructions alone fail.
- Few-shot demonstrates **ambiguous-case handling** (tool selection for ambiguous requests, branch-level coverage gaps).
- Few-shot enables **generalization** to novel patterns rather than only matching pre-specified cases.
- Few-shot reduces hallucination in extraction tasks (informal measurements, varied document structures).

**Skills in:**
- 2–4 targeted few-shot examples for ambiguous scenarios — show **reasoning** for why one action was chosen over plausible alternatives.
- Few-shot examples that demonstrate the desired output format (location, issue, severity, suggested fix).
- Few-shot distinguishing acceptable patterns from genuine issues to reduce false positives while enabling generalization.
- Few-shot for varied document structures (inline citations vs bibliographies, methodology sections vs embedded details).
- Few-shot from documents with varied formats to address empty/null extraction of required fields.

### T4.3 Enforce structured output using tool use and JSON schemas

**Knowledge of:**
- **`tool_use` with JSON schemas** is the most reliable approach for guaranteed schema-compliant output — eliminates JSON syntax errors.
- `tool_choice`: **`"auto"`** (model may return text), **`"any"`** (must call a tool, can choose which), **forced** (must call a specific tool).
- Strict JSON schemas eliminate **syntax errors** but not **semantic errors** (line items not summing, values in wrong fields).
- Schema design: required vs optional fields, enum + `"other"` + detail string for extensible categories.

**Skills in:**
- Defining extraction tools with JSON schemas as input parameters; extract from `tool_use` response.
- `tool_choice: "any"` to guarantee structured output when multiple extraction schemas exist and document type is unknown.
- Forced tool selection (`{"type": "tool", "name": "extract_metadata"}`) to ensure a specific extraction runs first.
- **Optional/nullable fields** when source documents may not contain the info — prevents fabrication.
- Enums with `"unclear"` for ambiguous and `"other"` + detail for extensible categorization.
- Format normalization rules in prompts alongside strict schemas.

### T4.4 Implement validation, retry, and feedback loops for extraction quality

**Knowledge of:**
- **Retry with error feedback:** append specific validation errors to the prompt on retry.
- **Limits of retry:** retries are ineffective when info is simply absent from source (vs format/structural errors).
- **Feedback loop design:** track which code constructs trigger findings (`detected_pattern`) for systematic dismissal-pattern analysis.
- **Semantic validation errors** (values don't sum, wrong field) vs **schema syntax errors** (eliminated by tool use).

**Skills in:**
- Follow-up requests including original document + failed extraction + specific validation errors.
- Identifying when retries will be ineffective vs when they will succeed.
- Adding `detected_pattern` to enable false-positive analysis.
- Self-correction validation flows: extract `calculated_total` + `stated_total` to flag discrepancies; `conflict_detected` boolean for inconsistent source data.

### T4.5 Design efficient batch processing strategies

**Knowledge of:**
- **Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed latency SLA.**
- Batch is appropriate for: non-blocking, latency-tolerant workloads (overnight reports, weekly audits, nightly test generation).
- Batch is **not** appropriate for: blocking workflows (pre-merge checks).
- Batch API does **not** support multi-turn tool calling within a single request.
- `custom_id` fields correlate batch request/response pairs.

**Skills in:**
- Matching API to latency requirements: synchronous for blocking pre-merge; batch for overnight/weekly.
- Calculating batch submission frequency for SLAs (e.g., 4-hour windows to guarantee 30-hour SLA with 24-hour batch processing).
- Handling batch failures: resubmit only failed `custom_id`s with appropriate modifications (e.g., chunk oversized docs).
- Prompt refinement on a sample set before batch-processing large volumes.

### T4.6 Design multi-instance and multi-pass review architectures

**Knowledge of:**
- **Self-review limitations:** a model retains reasoning context from generation, making it less likely to question its own decisions in the same session.
- **Independent review instances** (without prior reasoning context) are more effective than self-review or extended thinking.
- **Multi-pass review:** per-file local analysis + cross-file integration to avoid attention dilution and contradictory findings.

**Skills in:**
- Second independent Claude instance for code review.
- Per-file local passes + separate integration pass for cross-file data flow.
- Verification passes where the model self-reports confidence alongside findings.

---

## Domain 5 — Context Management & Reliability (15%)

### T5.1 Manage conversation context to preserve critical information across long interactions

**Knowledge of:**
- **Progressive summarization risks:** condensing numbers, percentages, dates, customer-stated expectations into vague summaries.
- **"Lost in the middle":** models reliably process the beginning and end of long inputs but may omit the middle.
- Tool results accumulate disproportionately to relevance (e.g., 40+ fields per order lookup when only 5 are relevant).
- Importance of passing **complete conversation history** in subsequent API requests.

**Skills in:**
- Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent **"case facts" block** included in each prompt, outside summarized history.
- Persisting structured issue data into a separate context layer for multi-issue sessions.
- Trimming verbose tool outputs to relevant fields **before** they accumulate.
- Placing key findings at the **beginning** of aggregated inputs; explicit section headers to mitigate position effects.
- Subagents include metadata (dates, source locations, methodological context) in structured outputs.
- Upstream agents return structured data (key facts, citations, relevance scores) instead of verbose content when downstream agents have limited context budgets.

### T5.2 Design effective escalation and ambiguity resolution patterns

**Knowledge of:**
- Escalation triggers: customer requests for human, **policy exceptions/gaps** (not just complex cases), inability to make meaningful progress.
- Distinction: escalate immediately on explicit customer demand vs offer to resolve when straightforward.
- **Sentiment-based escalation and self-reported confidence are unreliable** proxies for case complexity.
- Multiple customer matches require **clarification** (request additional identifiers) — not heuristic selection.

**Skills in:**
- Explicit escalation criteria with few-shot examples in the system prompt.
- Honoring explicit human requests immediately, without first attempting investigation.
- Acknowledging frustration while offering resolution when within capability; escalate only if customer reiterates preference.

> **These two bullets cover different cases, not a conflict.** If the customer **explicitly asks for a human**, escalate immediately, without investigating first (bank q-019). If the customer is **frustrated but has not clearly asked for a human**, acknowledge it, say what you can do now, and let them choose; escalate if they ask again (bank q-028). The exam guide's Knowledge bullet states the same split: "escalating immediately when a customer explicitly demands it versus offering to resolve when the issue is straightforward."
- Escalating when policy is ambiguous/silent on the request (e.g., competitor price matching when policy only addresses own-site).
- Asking for additional identifiers on multi-match results, not selecting heuristically.

### T5.3 Implement error propagation strategies across multi-agent systems

**Knowledge of:**
- **Structured error context** (failure type, attempted query, partial results, alternatives) enables intelligent coordinator recovery.
- **Access failures** (timeouts, retry decisions) vs **valid empty results** (successful query, no matches).
- Generic error statuses ("search unavailable") hide valuable context.
- **Anti-patterns:** silently suppressing errors (returning empty as success) **and** terminating entire workflows on single failures.

**Skills in:**
- Returning structured error context: failure type, what was attempted, partial results, potential alternatives.
- Distinguishing access failures from valid empty results.
- Subagents do local recovery for transient failures; propagate only what they can't resolve, with what was attempted and partial results.
- Synthesis output with **coverage annotations** indicating which findings are well-supported vs which topic areas have gaps due to unavailable sources.

### T5.4 Manage context effectively in large codebase exploration

**Knowledge of:**
- **Context degradation in extended sessions** — models start giving inconsistent answers, referencing "typical patterns" rather than specific classes discovered earlier.
- **Scratchpad files** persist key findings across context boundaries.
- **Subagent delegation** isolates verbose exploration output while the main agent coordinates.
- **Structured state persistence** for crash recovery: each agent exports state to a known location; coordinator loads a manifest on resume.

**Skills in:**
- Spawning subagents for specific questions ("find all test files," "trace refund flow dependencies") while main agent preserves coordination.
- Scratchpad files recording key findings, referenced for subsequent questions.
- Summarizing key findings from one phase before spawning subagents for the next.
- Crash recovery via structured agent state exports (manifests).
- `/compact` to reduce context usage during extended exploration when context fills with verbose discovery.

### T5.5 Design human review workflows and confidence calibration

**Knowledge of:**
- **Aggregate accuracy metrics** (e.g., 97% overall) may **mask** poor performance on specific document types or fields.
- **Stratified random sampling** for measuring error rates in high-confidence extractions and detecting novel patterns.
- **Field-level confidence scores** calibrated using labeled validation sets, for routing review attention.
- Validate accuracy by document type and field segment **before** automating high-confidence extractions.

**Skills in:**
- Stratified random sampling of high-confidence extractions for ongoing error rate measurement.
- Analyzing accuracy by document type and field to verify consistent performance.
- Field-level confidence scores; calibrating review thresholds with labeled validation sets.
- Routing low-confidence or ambiguous/contradictory source extractions to human review.

### T5.6 Preserve information provenance and handle uncertainty in multi-source synthesis

**Knowledge of:**
- Source attribution lost during summarization when findings are compressed without preserving claim-source mappings.
- Structured **claim-source mappings** that synthesis must preserve and merge.
- Conflicting statistics from credible sources: **annotate conflicts with source attribution** rather than arbitrarily picking one.
- **Temporal data:** require publication/collection dates in structured outputs to prevent temporal differences from being misinterpreted as contradictions.

**Skills in:**
- Structured claim-source mappings (URLs, document names, relevant excerpts) preserved through synthesis.
- Reports with explicit sections distinguishing **well-established** from **contested** findings; preserve original source characterizations and methodology.
- Document analysis includes conflicting values, explicitly annotated; coordinator decides reconciliation.
- Publication/collection dates in structured outputs.
- Rendering content types appropriately: financial as tables, news as prose, technical as structured lists (not all uniform).

---

## In-Scope Topics (explicitly tested)

- Agentic loop implementation: control flow on `stop_reason`, tool result handling, loop termination
- Multi-agent orchestration: coordinator-subagent, task decomposition, parallel subagents, iterative refinement
- Subagent context management: explicit passing, structured state persistence, crash-recovery manifests
- Tool interface design: descriptions, splitting vs consolidating, naming for disambiguation
- MCP tool and resource design: resources for catalogs, tools for actions, description quality
- MCP server configuration: project vs user scope, env var expansion, multi-server simultaneous access
- Error handling and propagation: structured responses, transient/business/permission, local recovery
- Escalation decision-making: explicit criteria, honoring customer preferences, policy gap identification
- CLAUDE.md configuration: hierarchy, `@import` patterns, `.claude/rules/` with glob patterns
- Custom commands and skills: project vs user scope, `context: fork`, `allowed-tools`, `argument-hint`
- Plan mode vs direct execution: complexity assessment, architectural decisions, single-file changes
- Iterative refinement: I/O examples, test-driven, interview pattern, sequential vs parallel issue resolution
- Structured output via `tool_use`: schema design, `tool_choice`, nullable fields to prevent hallucination
- Few-shot prompting: ambiguous targeting, format consistency, false-positive reduction
- Batch processing: Message Batches API appropriateness, latency assessment, failure handling by `custom_id`
- Context window optimization: trimming tool outputs, structured fact extraction, position-aware ordering
- Human review workflows: confidence calibration, stratified sampling, accuracy segmentation
- Information provenance: claim-source mappings, temporal data, conflict annotation, coverage gap reporting

## Out-of-Scope Topics (NOT tested)

- Fine-tuning or training custom models
- Claude API authentication, billing, account management
- Detailed implementation of specific languages/frameworks (beyond what tool/schema config requires)
- Deploying or hosting MCP servers (infra, networking, container orchestration)
- Claude's internal architecture, training process, model weights
- Constitutional AI, RLHF, safety training methodologies
- Embedding models or vector DB implementation details
- Computer use (browser automation, desktop interaction)
- Vision/image analysis capabilities
- Streaming API implementation or server-sent events
- Rate limiting, quotas, API pricing calculations
- OAuth, API key rotation, authentication protocols
- Specific cloud provider configurations (AWS, GCP, Azure)
- Performance benchmarking, model comparison metrics
- Prompt caching implementation details (beyond knowing it exists)
- Token counting algorithms, tokenization specifics

> **Implication for Richard:** if the learner asks a question that's clearly out-of-scope, gently redirect to in-scope material. The exam doesn't test these.

---

## Authoritative External References

- Anthropic Claude API docs: https://docs.claude.com/
- Claude Code docs: https://code.claude.com/docs/en/overview (use this when teaching Domain 3)
- Claude Agent SDK docs: linked from the above
- Model Context Protocol spec: https://modelcontextprotocol.io/

---

## Preparation Exercises (from the official guide)

The guide ships four hands-on exercises. Richard can use these as the *spine* for tutoring-mode practical tasks, adapting them to the learner's pace.

| # | Title | Domains reinforced |
|---|---|---|
| 1 | Build a Multi-Tool Agent with Escalation Logic | D1, D2, D5 |
| 2 | Configure Claude Code for a Team Development Workflow | D3, D2 |
| 3 | Build a Structured Data Extraction Pipeline | D4, D5 |
| 4 | Design and Debug a Multi-Agent Research Pipeline | D1, D2, D5 |

Full exercise specs are in the source PDF (Preparation Exercises section).
