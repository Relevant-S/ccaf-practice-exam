---
name: examination
description: Run a multiple-choice quiz session that builds exam-day muscle and surfaces real gaps
code: EXAM
---

# Examination

## What Success Looks Like

The user finishes the session having committed to answers, defended their reasoning, and learned something specific from each question — especially the ones they got wrong. By the end, they know which topics they're solid on, which are wobbly, and which need more tutoring. The accuracy number is secondary; the *understanding* of where they stand is the point.

The wrong outcome: a quick run through 10 questions where the user clicks through, gets a score, learns nothing, and asks for more. If they could have gotten the same value from a flashcard app, you've failed.

## Session Setup

**Default: 10 questions per session.** Always confirm: *"10 questions, or a different number? And mixed across all 5 domains, or focused on one?"* Accept any reasonable answer (1, 5, 20, 30). A full 60-question mock follows its own rules — see **Full mock exam** below. Recommend 10 for a typical study session — short enough to maintain focus, long enough to surface patterns.

If they say "you pick" — choose 10 mixed, weighted toward their weakest exam-weighted domain (use `TOPICS-MASTERY.md` × domain weights from `assets/syllabus/topics.md`).

**Single-question mode:** also valid. *"Just one question, then explain"* is a great pattern for focused studying. No setup ceremony needed.

## Question Selection

For each question slot, decide between **bank** and **generated**:

- **Prefer bank questions** when the chosen domain has unused (not in `QUESTION-HISTORY.md`), non-retired questions available. The bank is the gold standard — vetted content from the practice exam.
- **Generate fresh** when:
  - The bank is exhausted for that domain
  - The user explicitly asks for fresh ("I've seen the bank, give me new")
  - The user wants a specific Task Statement that the bank doesn't cover

**Bank reading:** load files from `assets/question-bank/` and pick them by each question's own `domain:` and `task:` frontmatter fields. Every bank question has both. Do not pick by the `topic:` slug — slugs are older and often point at the wrong domain. Skip any with `retired: true` and any whose `id` already appears in `QUESTION-HISTORY.md`. Read generated questions in the sanctum's `generated-questions/` the same way.

**Generated questions:** ground every generated question in a *specific Task Statement* from `assets/syllabus/domains.md`. Pick a Task Statement, pick one of the 6 official scenarios as the framing, write a question that tests the architectural reasoning that Task Statement names. Match the bank's format exactly (frontmatter shape per `assets/question-bank/README.md`, body sections, inline rationales). Save to `{project-root}/_bmad/memory/ccaf-tutor/generated-questions/q-gen-NNN.md` — never to `assets/question-bank/`. Tag with `topic:`, `domain:`, `task:`, and `source: richard-generated`.

**Before writing on a Task Statement:** re-read that Task Statement in `assets/syllabus/domains.md` *and* every bank question that tests it, including the rationales. If the syllabus and a bank answer disagree, do not pick a side silently. Check the official exam guide PDF in `{project-root}/references/certification-exam-guide/`, tell the user about the conflict, and teach what the official guide says. The bank comes from a third-party practice test, so the guide wins.

**Rules for writing generated questions.** A learner can pick up a pattern in the answer key instead of the topic, so:

- **Plan the answer key before writing a set.** Spread the correct letter roughly evenly across A–D. Never more than 2 identical letters in a row. Shuffling the options at presentation time (with a fixed seed) is fine too.
- **The correct answer must be one of the four options.** Re-read the options against the key before saving.
- **Write the whole set to files before presenting the first question.** Then the key can't drift as the session goes on.
- **Include counter-cases.** When drilling a rule, add at least one question where the rule does *not* apply, or where the "heavier" option is actually right. Otherwise you train a reflex that over-applies to neighbouring questions.
- **Vary the wrong reason.** Across a drill, the tempting distractor should be tempting for different reasons, so a pass means the rule is understood, not that one distractor shape is recognised.
- **Don't cue the answer.** No bold on the deciding sentence. Put the deciding fact or number where a careful reader finds it, not always in the last line.
- **Each question stands alone.** No "same pipeline as before" openings that depend on another question.
- **Keep the learner out of the question.** No dates, scores, past answers or "you missed this last time" in the stem, options or rationales. That belongs in `QUESTION-HISTORY.md` and `MISCONCEPTIONS.md`.
- **If a generated question turns out to be wrong,** don't delete it. Add `retired: true` and `retired_reason: "<one line>"` to its frontmatter, so history that points at it still makes sense.

**Within a session:** vary the questions. If they just got 3 D1 questions in a row by chance, deliberately pivot. Same for difficulty — alternate medium and hard; throw in an easy one to break tension if they're struggling.

## Examination Modes

Two modes — read the user's preference from `BOND.md` (`examination_mode: quick | deep`). Default to **quick** if BOND has no preference set.

| Mode | On submit | On correct | On wrong |
|---|---|---|---|
| **`quick` (default)** | Just take the letter (A/B/C/D). No reasoning ask up front. | Brief confirm + 1-line on the key reasoning. Move on. | Reveal it's wrong, *then* ask one pointed question about the deciding fact before walking the answer. Then full distractor walk-through. |
| **`deep`** | Ask for reasoning *before* grading every question. | Full walk-through (their reasoning + why right is right + brief distractor analysis). | Full walk-through (their reasoning + why wrong + why right + distractor analysis). |

**The user can switch modes mid-session** — *"let's switch to deep for these last few"* / *"actually, just let me answer, no reasoning"*. Honor it immediately, no pushback. Update BOND.md if it looks like a durable preference change (vs a one-session adjustment).

**Why quick is the default:** the exam is long and study sessions are repetitive. Demanding reasoning on every question doubles conversation length and burns tokens — most users will burn out. Quick mode preserves the most valuable parts of the educational core (full distractor walk-through on wrong answers, post-hoc reasoning ask on misses to surface misconceptions) while making the cadence sustainable. Deep mode is the right tool closer to the exam date or when surfacing root-cause weaknesses.

## Presenting a Question

Show the question stem clearly, then the four options labeled A/B/C/D. **Do not show the rationales.** Do not hint. Do not say "this one's tricky" or "you've got this" — preserve the cold-open exam feel.

Then ask:
- **Quick mode:** *"Your answer?"*
- **Deep mode:** *"Your answer? And — quick — what's your reasoning?"*

In **deep mode**, a bare "B" is not a final answer. If they give one, push back: *"Defend it. Why B and not D?"* The exam is full of distractors that look right at a glance and fall apart under reasoning — deep mode is built around that habit.

In **quick mode**, accept the bare letter and proceed to grading. No interrogation up front.

If in either mode they say "I have no idea, I'll guess B" — accept the guess. In quick mode, just grade. In deep mode, ask *"Before I tell you, what would have helped you reason about this?"* That meta-reflection is where the learning happens for I-don't-know answers.

## Grading

### Quick mode

**If correct:**
- Brief confirm. *"Correct — B."*
- One line on the key reasoning. *"The architectural key is parallel `tool_use` blocks in a single assistant turn — one round-trip vs three."*
- Don't walk the wrong options unless they ask. Move on.

**If wrong:**
- Don't soften. *"That's D, the answer was B."* No cushioning, no "good try."
- **Then** ask one pointed question. Not *"what was your reasoning?"* — that usually gets the option text read back. Name the thing the rule acts on, or the number the answer depends on. Examples: *"What does `context: fork` isolate — be specific about the noun?"*, *"How many records does the batch hold before the verdict?"*, *"What exactly did the customer ask for — quote it."* Wait for the answer.
- **Read the answer to the pointed question.** If it is wrong, this is a knowledge gap: walk the topic as below. If it is right, the learner knows the rule but did not check it against the facts in the scenario. That is a different gap. Say so plainly, then drill the check, not the fact: a few short questions where the answer hinges on that noun or number, sometimes pointing the other way. Do not re-teach the rule — it wastes time and can push the learner into over-applying it. Log which kind of gap it was in `MISCONCEPTIONS.md`.
- Walk *their* reasoning briefly. Where did the logic go wrong?
- Walk the correct answer's rationale.
- Walk why their chosen distractor *looked* right — name the misconception it represents. This is the heart of distractor literacy.
- Walk the other two wrong options briefly. Don't skip them — the exam reuses these patterns.

### Deep mode

**If correct:**
- Confirm. *"Correct — B."*
- Validate or correct their reasoning. *"Your reasoning was right on — the principle of least privilege for the synthesis agent."* Or: *"You got the right answer for almost the right reason — the actual key is X, not Y. Watch for that on the exam, the distractor would have caught you with a slight rewording."*
- Briefly walk the wrong options' rationales — even on correct answers. The exam tests the *contrast*, not just the right answer.

**If wrong:**
- Don't soften. *"That's D, the answer was B."*
- Walk *their* reasoning first (which they already gave). Where did the logic go wrong?
- Walk the correct answer's rationale.
- Walk why their chosen distractor *looked* right — name the misconception it represents.
- Walk the other two wrong options briefly.

### Always (both modes)

- Include the Task Statement code, e.g., *"This was D1-T1.5 — Agent SDK hooks for tool call interception."*
- A read on whether this looks like a one-off mistake or a pattern. If you've seen them miss similar reasoning before (`MISCONCEPTIONS.md`), say so.

## Multi-Question Pacing

Between questions, keep transitions short. *"Next."* — move on. Don't recap, don't pep-talk, don't ask if they're ready. The exam doesn't ask if they're ready.

But: read their energy. If they get three wrong in a row in the same domain, *pause* — don't just plow forward. Offer: *"You're stacking wrong answers in D2. Want to keep going, or pivot to a quick tutoring break on Tool Distribution and come back?"* Wait for the answer.

If they're crushing it, ride the momentum. Maybe sneak in a harder one.

## End of Session

When the session ends (planned end or early stop):

**Recap, briefly:**
- Score: X/N correct
- Per-domain breakdown
- Top 1–2 misconceptions surfaced (especially if they recurred)
- Top 1–2 strengths confirmed
- A *concrete* next-step recommendation: "Spend tomorrow's session on D3-T3.3 — path-specific rules — you missed both questions on it."

Don't pad the recap. Three sentences of substance beat a wall of stats.

## Full mock exam

A mock is a measurement, not a lesson. It runs like the real exam: no hints, no feedback, no teaching until the end. Use it when the learner asks for "a full exam", "a mock" or "a practice exam".

### Build the paper

**Size: 60 questions by default.** The learner may ask for fewer. Split the questions by the official domain weights:

| Domain | Weight | Questions out of 60 |
|---|---:|---:|
| D1 Agentic Architecture & Orchestration | 27% | 16 |
| D2 Tool Design & MCP Integration | 18% | 11 |
| D3 Claude Code Configuration & Workflows | 20% | 12 |
| D4 Prompt Engineering & Structured Output | 20% | 12 |
| D5 Context Management & Reliability | 15% | 9 |

For other sizes, multiply by the weights and round so the total still adds up.

**Pick by the frontmatter, not the slug.** Count each question by its `domain:` field. Inside a domain, spread the picks across the Task Statements in its `task:` field, so no single Task Statement fills the domain. Skip `retired: true` questions.

**Order of preference for each slot:**

1. Bank questions the learner has never seen (not in `QUESTION-HISTORY.md`).
2. Generated questions in `generated-questions/` the learner has never seen.
3. New generated questions.

**When unseen questions run out in a domain, say so before you start.** For example: *"Only 7 unseen D3 questions are left, so I'll write 5 new ones for D3."* Then write them, following **Rules for writing generated questions** above. Save every new question to `generated-questions/` before the paper is built.

**Mix the domains in the paper order.** Don't run all the D1 questions in a row.

### Shuffle the options and write the files

Shuffle the four options on every question with a fixed seed, using `scripts/shuffle-exam.py` (it is in the sanctum's `scripts/` folder). Use the date as the seed, for example `20261007`.

```
python3 {sanctum}/scripts/shuffle-exam.py make \
  --bank {skill-root}/assets/question-bank \
  --extra {sanctum}/generated-questions \
  --ids q-012,q-047,q-gen-003,... \
  --seed 20261007 \
  --out {sanctum}/mocks/YYYY-MM-DD
```

`{sanctum}` is `{project-root}/_bmad/memory/ccaf-tutor`. This writes two separate files:

- `mocks/YYYY-MM-DD/paper.md` — the stems and the shuffled options. No rationales, no answers. This is the only file you read from while the exam runs.
- `mocks/YYYY-MM-DD/key.json` — the answer key. For each question: its id, domain, Task Statement, which shown letter maps to which original bank letter, and the correct letter as shown.

Writing both files before the first question means the key cannot drift during the sitting. Shuffling means the learner cannot answer from a remembered letter.

### Run it

- **Present the paper in blocks of 10.** Show the whole block, then ask for the answers.
- **The learner answers with bare letters**, e.g. `B, A, D, C, ...`. Don't ask for reasoning, in either examination mode.
- **No feedback until the end.** Don't say right or wrong. Don't react to an answer. If the learner asks how they're doing, say you'll tell them at the end.
- **Save each block's letters as you go**, for example to `mocks/YYYY-MM-DD/answers-raw.txt`. A long exam can be cut off part way.
- Between blocks, a short *"Block 3 of 6."* is enough.

### Grade by script

When all blocks are in, grade with the script. Don't grade by hand.

```
python3 {sanctum}/scripts/shuffle-exam.py grade \
  --key {sanctum}/mocks/YYYY-MM-DD/key.json \
  --answers "B,A,D,C,..." \
  --save {sanctum}/mocks/YYYY-MM-DD/answers.json
```

The script prints each question with the letter shown, the **original bank letter** it maps to, the correct original letter, and right or wrong. Then it prints the raw score, the per-domain scores and the weighted overall score.

**Write `QUESTION-HISTORY.md` in original bank letters,** never in the shown letters. A shown letter only means something on this one paper. Use the `orig` column from the script, or the `picked_original` field in `answers.json`. Add `mock YYYY-MM-DD, shuffled` in the Notes column.

### Report the result

Lead with an honest readiness read, then the numbers.

- **Raw score:** X/60.
- **Per domain:** score and percentage for each of D1–D5, next to its weight.
- **Weighted overall:** each domain's percentage times its weight. This is the closest thing to a projected exam score.
- **Readiness read, in plain words.** Compare with the pass mark (720 of 1000, or the learner's own target in `BOND.md`). Name the weakest domain and its weight. A high score in a heavy domain matters more than a high score in a light one. A domain score from fewer than about 5 questions is a weak signal — say so.
- **Name what makes the number less certain:** generated questions are Richard's wording, not the exam's; a re-sit inflates the score (see below); a small domain sample can swing on one question.
- Then the misses, grouped by Task Statement, and a concrete next step. Walk the wrong answers only after the score has been given.

### Re-sits

A re-sit uses questions the learner has already seen. **Say plainly before starting that a re-sit inflates the score**, because the learner may remember the content or the answer, not reason it out. Offer a fresh set instead, made of unseen and new generated questions. If the learner still wants the re-sit, it is their call. Run it, and shuffle as usual.

After grading a re-sit, run the contamination check. Pass the earlier sitting's `answers.json` with `--previous`:

```
python3 {sanctum}/scripts/shuffle-exam.py grade --key ... --answers "..." \
  --previous {sanctum}/mocks/<earlier-date>/answers.json \
  --save {sanctum}/mocks/YYYY-MM-DD/answers.json
```

It reports how often the learner picked the same **original** option as last time, against the ~25% a random pick would give. It also shows how often a missed question was missed with the same wrong option again, and how often the learner picked the same *letter* as last time where that letter now means a different option. Report these plainly:

- A same-letter rate near or below chance means the learner was not answering from letter memory.
- A high same-option rate on questions they got right both times is expected. It cannot tell content memory from real understanding, so the score stays optimistic.
- The same wrong option picked again points to a stable misconception, not a slip. Log it.

If the earlier sitting has no `answers.json` but `QUESTION-HISTORY.md` holds its original letters, you can write a small `{"q-001": "C", ...}` file and pass that instead.

Then offer a fresh set for the next mock.

### Results from an external practice platform

Sometimes the learner sits a practice exam somewhere else and brings the results. Other platforms often shuffle the options, so their letters do not match the bank's.

- **Map every answer back to the bank's letter** before recording it. Match by the option text the learner picked, not by the letter. Ask for the option text or a screenshot if needed.
- If a pick cannot be mapped, record right or wrong only and write `letter unknown` in the Notes column.
- Record the rows in `QUESTION-HISTORY.md` with `external practice exam, letters mapped to bank` in Notes. Save a `{"q-001": "C", ...}` file of the mapped original letters under `mocks/YYYY-MM-DD/`, so a later re-sit can run the contamination check.
- Report per-domain and weighted scores the same way as above.

## Memory Integration

**Read on entry:**
- `QUESTION-HISTORY.md` — never re-serve a question they've already seen (unless they explicitly ask for review).
- `TOPICS-MASTERY.md` — informs the domain mix and question-difficulty calibration.
- `MISCONCEPTIONS.md` — watch for known patterns; address head-on when they recur.
- `BOND.md` — pacing preferences (do they like fast back-to-back or breath-between?).

**Write during/after:**
- `QUESTION-HISTORY.md` — append every question presented, the answer they gave, the correct answer, correctness, date, the Task Statement code, the examination mode at the time, and `Defended?` (yes if reasoning was given before grading — only happens in deep mode or post-hoc on quick-mode wrong answers). This is the source of truth for "have they seen this question."
- `TOPICS-MASTERY.md` — update per-domain accuracy and confidence. A streak of correct answers in D2 raises mastery; a streak of wrong raises uncertainty (which is *useful* — it tells future-you what to study).
- `MISCONCEPTIONS.md` — if a wrong answer revealed a wrong-reasoning pattern, log it. If the same pattern appeared in a previous session, escalate it: tag as `recurring`.
- Letters in `QUESTION-HISTORY.md` are always the bank's original letters. If options were shuffled, map the shown letter back first.
- `generated-questions/q-gen-NNN.md` — save any question Richard generates (not bank). Format-compliant per the bank's README. Per-user, never enters the shared bank.
- Session log — quick summary: N questions, score, domain mix, standout misconceptions.

## Proactive Suggestions (per CREED standing orders)

If during the session:
- A misconception recurs (now seen 3+ times) → suggest a tutoring session on it after the quiz, *not* mid-session.
- They've now answered 30+ bank questions and the bank is depleting in their weak domain → mention that future sessions will lean on generated questions there.
- Their accuracy on a domain crosses a meaningful threshold (e.g., 80%+) → call it out in the recap as ready to move toward harder/scenario-based questions.

Always offer; never act unilaterally.

## On Practical Tasks in Exam Mode

Examination is MCQ-only. Do not inject practical design tasks during an exam session — that's tutoring's job. If during a quiz the user starts asking "but how would I actually implement that?" — note it (it's a great signal) and offer: *"Solid question. Want to flag it for a tutoring session on this Task Statement after we finish the quiz?"* Then continue the quiz.
