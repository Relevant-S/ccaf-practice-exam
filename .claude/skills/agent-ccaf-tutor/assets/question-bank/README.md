# CCAF Question Bank — Format Specification

This folder is the **shared question bank** that ships with the `agent-ccaf-tutor` skill (Richard). Every person who installs the agent gets the same questions in the same shape. Per-user state (which questions you've seen, your answers, mastery) lives in the per-user sanctum at `{project-root}/_bmad/memory/ccaf-tutor/`, never here.

**Audience for this spec:** humans converting source material (screenshots, PDFs, videos) into questions, and any LLM helping with that conversion.

---

## File layout

```
assets/question-bank/
├── README.md              # this file
├── _images/               # all referenced images live here
│   ├── q-007-diagram.png
│   └── q-022-code.png
├── q-001.md
├── q-002.md
└── ...
```

**One question per file.** Filename: `q-NNN.md` where `NNN` is a zero-padded sequential ID (`q-001.md`, `q-042.md`, `q-100.md`). The ID is permanent — never renumber. If a question is retired, leave a tombstone (see "Retiring questions" below) rather than reusing the slot.

Images go in `_images/` and are referenced from the question with relative paths (`![](_images/q-007-diagram.png)`). Naming convention: `q-NNN-{short-slug}.png`.

---

## Question file format

Each `q-NNN.md` file has YAML frontmatter + a structured Markdown body. **All fields are required unless marked optional.**

### Frontmatter

```yaml
---
id: q-001
topic: tool-use            # canonical topic slug — see "Topics" below
subtopic: parallel-calls   # optional, free-form
source: practice-test-A    # where this question came from
source_ref: "Q14"          # optional — original numbering in the source
difficulty: medium         # easy | medium | hard
question_type: mcq-single  # mcq-single (only type for now)
has_image: false           # true if the body references an image
has_code: true             # true if the body contains a code block
correct: B                 # A | B | C | D
tags: [api, streaming]     # optional — free-form additional tags
---
```

### Body structure

The body uses **fixed section headings** so Richard can parse it deterministically:

```markdown
## Question

{The question stem. Can be multiple paragraphs. May contain code blocks,
inline code, or image references.}

## Options

- **A)** {option A text — may span multiple lines, may contain code}
  - **Rationale:** {one paragraph. For the correct option, starts with
    "Correct." and explains the architectural reasoning. For wrong options,
    explains the misconception or failure mode that makes it wrong.}
- **B)** {option B text}
  - **Rationale:** {…}
- **C)** {option C text}
  - **Rationale:** {…}
- **D)** {option D text}
  - **Rationale:** {…}

## References

- {Optional: link to Anthropic docs, blog post, or reference material}
- {Optional: cross-reference to related questions, e.g. "see also q-042"}
```

**Why every option carries a rationale:** Richard's job is understanding, not memorization. Telling the user why the right answer is right is half the job — explaining what makes the *plausible-looking wrong answers* wrong is where the real learning happens. Co-locating the rationale with each option keeps the right-vs-wrong reasoning side-by-side instead of scattered across two sections.

---

## Worked example

`q-001.md`:

```markdown
---
id: q-001
topic: tool-use
subtopic: parallel-calls
source: practice-test-A
source_ref: "Q14"
difficulty: medium
question_type: mcq-single
has_image: false
has_code: true
correct: B
tags: [api, streaming]
---

## Question

You are designing a Claude-powered agent that needs to fetch weather data
for three cities to answer a single user query. The model has access to a
`get_weather(city)` tool. Which approach minimizes end-to-end latency?

## Options

- **A)** Make three sequential tool calls in three separate model turns,
  one city per turn.
  - **Rationale:** Three sequential turns means three full model
    round-trips — roughly 3× the latency of the parallel approach for
    independent calls.
- **B)** Allow Claude to issue all three `get_weather` tool calls in
  parallel within a single assistant turn, then return all three results
  in a single user turn.
  - **Rationale:** Correct. Claude supports issuing multiple `tool_use`
    blocks in a single assistant turn. Returning all corresponding
    `tool_result` blocks in a single user turn lets the model continue
    with full context after one round-trip, rather than three. This is
    the canonical "parallel tool use" pattern and is the latency-optimal
    architecture when the tool calls are independent.
- **C)** Combine the three cities into one prompt and ask the model to
  hallucinate the weather without using the tool.
  - **Rationale:** Hallucinated tool results are not real data; this
    defeats the purpose of giving the model a tool and produces
    unreliable answers.
- **D)** Use streaming with `stop_sequences` set to "weather" so the
  model pauses between each city.
  - **Rationale:** `stop_sequences` is a generation-control mechanism,
    not a tool orchestration primitive. It would not make tool calls
    parallel and would likely break the response format.

## References

- https://docs.claude.com/en/docs/build-with-claude/tool-use/overview
- See also q-008 (sequential vs. parallel decision criteria)
```

---

## Edge cases

### Questions with images

Set `has_image: true`. Reference the image inline in the `## Question`
section:

```markdown
## Question

Examine the agent architecture diagram below. Which component is
responsible for tool result aggregation?

![Agent architecture diagram](_images/q-007-architecture.png)
```

If the image itself is the entire question (e.g. "what's wrong with this
code?"), the text in `## Question` should still describe what to look at
so a screen-reader-only or text-only consumer (including some LLM
processing modes) can still parse the intent.

### Questions with code

Use fenced code blocks with a language tag:

````markdown
## Question

Review the following Claude API call. What's the issue?

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    tools=[weather_tool],
    tool_choice={"type": "any"},
    stream=True,
)
```
````

Set `has_code: true` in frontmatter. Code can also appear inside option
text — wrap inline with backticks or a fenced block as needed.

### Long / case-study questions

Some exam questions present a multi-paragraph scenario before asking the
actual question. Put the full scenario inside `## Question` — don't split
it. If the scenario is reused across multiple questions in the source,
duplicate it into each question file (questions are self-contained).

### Questions with multi-line options

Options can span multiple lines or contain code. Keep the `- **A)**`
prefix on the first line:

```markdown
- **A)** Use a single system prompt that contains all the tool
  definitions, then call the model in a loop, parsing tool calls
  out of the assistant's text response.
- **B)** ...
```

---

## Topics

The canonical topic slugs are defined by the CCAF syllabus (which lives
at `assets/syllabus/`). Until the syllabus is loaded, use working slugs
and refactor later. **Slugs are kebab-case, lowercase, stable.** A few
likely candidates based on Anthropic's public material:

- `prompt-engineering`
- `tool-use`
- `agents-and-orchestration`
- `context-management`
- `claude-code`
- `agent-sdk`
- `evaluation`
- `safety-and-guardrails`
- `production-deployment`
- `model-selection`
- `multimodal`
- `pricing-and-limits`

**The authoritative list lives in `assets/syllabus/topics.md`** once that
file exists. If you add a topic that isn't in the syllabus yet, also add
it there with a one-line definition.

---

## Source attribution

The `source` field identifies where a question came from:

- `practice-test-A`, `practice-test-B`, ... — replace with real source
  names once known (e.g. `whizlabs-2026-q1`).
- `anthropic-docs-example` — questions derived from official documentation.
- `richard-generated` — **never used in this folder.** Generated
  questions live in the per-user sanctum, not here.

Use `source_ref` to preserve the original numbering ("Q14", "Section
3.2") so we can trace back to the source if a question is disputed.

---

## What does NOT go in this folder

- **Per-user state** (your answers, your accuracy, what you've seen) —
  lives in the sanctum, never here.
- **Richard-generated questions** — also sanctum, under
  `{project-root}/_bmad/memory/ccaf-tutor/generated-questions/`. Generated questions
  may be promoted into this shared bank later by an explicit human step,
  but never automatically.
- **Personal study notes** — sanctum.
- **The CCAF syllabus** — sibling folder `assets/syllabus/`.

---

## Retiring questions

If a question is found to be wrong, ambiguous, or out of scope:

1. Set `retired: true` in the frontmatter.
2. Add a `retired_reason: "..."` field explaining why.
3. Leave the file in place — do **not** delete or renumber.

Retired questions are skipped by Richard during examination and tutoring,
but the IDs remain stable so historical references in user sanctums
(e.g. "you got q-042 wrong twice") don't break.

---

## Validation checklist (before committing a question)

- [ ] Frontmatter has all required fields, valid values
- [ ] `correct` is one of A, B, C, D
- [ ] Exactly four options, each with a `- **X)**` prefix
- [ ] Each option has a `**Rationale:**` sub-bullet
- [ ] The rationale on the `correct` option starts with `Correct.` and explains the reasoning
- [ ] The rationales on the three wrong options each name the specific misconception or failure mode
- [ ] If `has_image: true`, the image file exists in `_images/`
- [ ] If `has_code: true`, code blocks have a language tag
- [ ] Topic slug matches one in `assets/syllabus/topics.md` (or is added there)
- [ ] Filename matches `id` field
