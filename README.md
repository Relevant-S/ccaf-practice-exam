# CCAF Practice Exam — Richard the Tutor

A Claude Code skill that drills you for Anthropic's **Claude Certified Architect — Foundations** exam. Meet **Richard**: a patient-but-sharp tutor who teaches by topic, runs MCQ practice quizzes from a 60-question shared bank (and generates fresh ones grounded in the official Task Statements when the bank thins out), and tracks your mastery across the 5 official domains.

## Prerequisites

- **Claude Code** — install per [Anthropic's docs](https://docs.claude.com/claude-code).
- **Python 3.10+** — needed once on first run to scaffold your personal sanctum.
- **Git** — to clone the repo.

## Get Started

```bash
git clone https://github.com/Relevant-S/ccaf-practice-exam.git
cd ccaf-practice-exam
claude  # opens Claude Code in this directory
```

In the Claude Code session, just say:

> *"Talk to Richard"* — or — *"I want to study for the CCAF exam"*

On your **first run**, Richard runs **First Breath**: he scaffolds your personal sanctum (in `_bmad/memory/ccaf-tutor/` — gitignored, never leaves your machine) and asks a few quick calibration questions: your name, target exam date, weekly study budget, and starting confidence per technology. Takes 2–3 minutes.

From then on, every session resumes from your sanctum. Richard remembers what you've studied, what you got wrong, and what's next.

## What Richard Can Do

| Capability | When to use it |
|---|---|
| **Examination** | Run a 1–60 question quiz session. Defaults to 10, mixed across the 5 domains. Two modes: `quick` (just answer A/B/C/D) and `deep` (defend your reasoning before grading). |
| **Tutoring** | Teach a CCAF topic at architect depth, then verify with a graded practical task. |
| **Progress** | Honest read on where you stand: weighted domain mastery, recurring misconceptions, recommended focus for the time you have left. |
| **Reset** | Wipe progress and start fresh. Archives (doesn't delete) your existing sanctum. |

Just describe what you want — *"quiz me on D3"*, *"teach me about hooks"*, *"how am I doing?"* — Richard picks the right capability.

## What's in the Repo

```
.claude/skills/agent-ccaf-tutor/   The skill bundle (Richard's prompts, question bank, syllabus)
_bmad/                              BMad framework (config + supporting skills)
_bmad/memory/ccaf-tutor/            YOUR personal sanctum (gitignored)
docs/                               Project documentation
references/                         Source PDFs (e.g., the official exam guide)
```

The 60-question bank under `.claude/skills/agent-ccaf-tutor/assets/question-bank/` is shared by every install. Questions Richard generates for you are saved per-user under `_bmad/memory/ccaf-tutor/generated-questions/` and never shared.

## Privacy

Your sanctum is gitignored — your name, study cadence, mistakes, and progress all stay on your machine. Nothing personal is committed to the repo.

If you ever want to start over, just tell Richard *"reset my progress"* — he'll archive your current sanctum to a timestamped folder (recoverable) before scaffolding a fresh one.

## Contributing Questions

If you want to contribute to the shared question bank, the format is documented in `.claude/skills/agent-ccaf-tutor/assets/question-bank/README.md`. Add new questions in a PR — they'll then ship to every colleague's install.
