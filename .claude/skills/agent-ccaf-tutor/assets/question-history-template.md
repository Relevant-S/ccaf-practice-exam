# Question History

_Append-only log of every question presented to {user_name}. The `examination` capability uses this to skip already-seen questions, and the `progress` capability uses it for accuracy and recency stats._

_Keep entries terse — one row per question. The full content lives in `assets/question-bank/q-NNN.md` (bank) or `generated-questions/q-gen-NNN.md` (Richard-generated). Don't quote question text or rationales here — that's wasted tokens on every load._

_Format:_

```
| Date | Question ID | Domain | Task | Mode | User answer | Correct | Result | Defended? | Notes |
|------|-------------|--------|------|------|-------------|---------|--------|-----------|-------|
```

- **Mode** — `quick` or `deep`, the examination mode at the time of this question.
- **Defended?** — `yes` if {user_name} gave reasoning *before* grading (always in deep mode; never in quick mode pre-grading). `post-hoc` if reasoning was given after a wrong-answer reveal in quick mode (this still feeds `MISCONCEPTIONS.md`). `no` if no reasoning was given. A guess that happened to be correct is *not* the same as a defended correct answer.
- **Notes** — optional, very brief. Use for things like "recurring misconception" or "second-guess from D" — anything future-you would want to know without re-reading the question.

---

## Sessions

| Date | Question ID | Domain | Task | Mode | User answer | Correct | Result | Defended? | Notes |
|------|-------------|--------|------|------|-------------|---------|--------|-----------|-------|
