# Placement

Richard and the study map (`study-map/ccaf-study-map.html`) use the same placement. The map runs it in the browser. Richard runs it in First Breath when the learner has not done it in the map. **Keep the two in sync:** if you change a question or a rule here, change the `ROLES`, `EXP`, `PROBES` and `place()` code in the map too.

## Why role first

People can't rate what they don't know yet, so self-ratings ("solid / some / none") overstate readiness. The role tells us which basics are likely missing. A short knowledge check then confirms it.

## Step 1: Role

Ask: *"What do you do for a living?"*

| Code | Role |
|---|---|
| `dev` | Software developer or engineer |
| `qa` | QA or test engineer |
| `ops` | DevOps, IT or support engineer |
| `pm` | Product, project or business role |
| `design` | Designer |
| `other` | Something else, or a student |

## Step 2: What they have done themselves

Ask them to name which of these they have **actually done**, even once. Facts, not ratings.

| Code | Experience |
|---|---|
| `e_code` | Written code that other people use |
| `e_git` | Used git: commit, push, pull request |
| `e_term` | Run commands in a terminal |
| `e_json` | Read or edited JSON |
| `e_api` | Called an API (for example in Postman) |
| `e_ci` | Worked with CI pipelines (GitHub Actions, Jenkins…) |
| `e_chat` | Used ChatGPT or Claude in a browser |
| `e_cc` | Used Claude Code |
| `e_sdk` | Built something with the Claude API or Agent SDK |

## Step 3: Quick check, chosen by role

One question at a time. The learner answers with a letter **or "not sure"**. Say up front: *"Don't guess. 'Not sure' is the most useful answer when it's true: it shows me what to teach you."* Give no feedback until the end.

| Role | Questions |
|---|---|
| `dev` | p6, p7, c1, c2, c3, c4, plus p2 if no `e_git`, p3 if no `e_term`, p4 if no `e_json`, p8 if no `e_ci` |
| `ops` | p4, p5, p6, p7, c1, c2, plus p2 if no `e_git` |
| `qa` | p1–p8, plus c1 if `e_cc` |
| `pm`, `design`, `other` | p1–p8 |

The basics questions (p1–p8) each test one basics lesson (B1–B8). The concept questions (c1–c4) are light exam-style checks.

| Id | Tests | Question | Options | Answer |
|---|---|---|---|---|
| p1 | B1 Files & paths | Which file does the pattern `**/*.test.tsx` match? | A) src/login.tsx · B) src/auth/login.test.tsx · C) tests/notes.md · D) Only files in a folder named ** | B |
| p2 | B2 Git & PRs | You saved a file inside the project folder on your laptop. When does a teammate get it? | A) Immediately · B) After you commit and push it, and they pull · C) Only if it's in your home folder · D) Never | B |
| p3 | B3 Terminal & flags | In `claude -p "Summarise" --output-format json`, what is `--output-format`? | A) An option that sets the output format · B) A file name · C) An error message · D) A second program | A |
| p4 | B4 JSON | Which of these is valid JSON? | A) `{name: Anna}` · B) `{"name": "Anna", "age": 31}` · C) `<name>Anna</name>` · D) `name = "Anna"` | B |
| p5 | B5 APIs & errors | A request to another system fails. Which failure is worth retrying automatically? | A) The service timed out · B) You don't have permission · C) The order number doesn't exist · D) The input is in the wrong format | A |
| p6 | B6 LLMs & context | Claude gets a 300-page document plus a long chat history. What's the main risk? | A) It refuses to read it · B) Details get lost because everything competes for limited space · C) The document gets deleted · D) None: more text always helps | B |
| p7 | B7 Tools & agents | Claude needs today's order status from a shop's database. How does that usually work? | A) It already knows from training · B) It asks to use a tool; code fetches the data and returns it · C) It logs into the database itself · D) It can't be done | B |
| p8 | B8 CI/CD | Why can't a CI pipeline job stop and ask someone a question? | A) Nobody is watching while it runs · B) Pipelines forbid text · C) Questions cost extra · D) It can; it waits for the next push | A |
| c1 | D3 CLAUDE.md levels | A teammate doesn't get your Claude Code instructions. Your file is `~/.claude/CLAUDE.md`. Why? | A) It's in your home folder, which isn't shared · B) CLAUDE.md only works for one person · C) They need a newer Claude Code · D) The file is too long | A |
| c2 | D1 Hooks | A refund over $500 must never go through without a human. What's the strongest way to enforce that? | A) State it clearly in the prompt · B) A hook that blocks the call before it runs · C) Ask Claude to double-check · D) Use a bigger model | B |
| c3 | D5 Escalation | In a support chat, which is the clearest reason to hand over to a human right away? | A) The customer sounds annoyed · B) The customer explicitly asks for a human · C) Claude's confidence score is low · D) The chat is long | B |
| c4 | D4 Structured output | A program must read Claude's output, with the same fields every time. Best approach? | A) Ask nicely in the prompt · B) Structured output that follows a JSON schema · C) A longer prompt · D) Fix the output by hand | B |

## Step 4: Result

- **Gaps** = the basics whose question was answered wrong or "not sure". Basics that were not asked count as known.
- **Track C (Builder):** role `dev` or `ops`, has `e_cc` or `e_sdk`, at least 3 concept questions right, and at most 1 gap.
- **Otherwise Track B (Some background)** if there are 2 gaps or fewer.
- **Otherwise Track A (Newcomer).**

Then tell the learner their track and gaps in two or three plain sentences, and walk through every question they missed **briefly**: the right answer and one line on why. This is their first lesson.

## What each track changes

| | Track A: Newcomer | Track B: Some background | Track C: Builder |
|---|---|---|---|
| Start with | All basics lessons (B1–B8), then "Reading exam questions" (B9), then domains | The basics gaps, then B9, then domains | B9, then a 10-question diagnostic |
| Explanations | Plain words first, then the exam term. Define every technical word the first time. | Plain words for the gap areas; architect depth elsewhere | Architect depth |
| Examples | From the learner's job (see `BOND.md` role) | From the learner's job where it helps | Exam scenarios |
| First practice | Tutoring, not a quiz | Short quiz on a topic just studied | Diagnostic quiz |

The study map has the basics lessons (the **Basics** bubble). Point Track A and B learners there; it works in any browser.

## Recording it

Save to `BOND.md` under **Starting point**: role, experience codes, track, gaps, placement date, and whether it came from the map or from First Breath. A learner can redo placement any time ("redo my placement"); overwrite the section and note the date.
