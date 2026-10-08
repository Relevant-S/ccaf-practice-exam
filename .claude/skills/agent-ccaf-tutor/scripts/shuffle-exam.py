#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Shuffle a mock exam paper and grade it — for Richard (agent-ccaf-tutor).

Standard library only. Two subcommands:

  make   Build a paper and a separate answer key.
         python3 shuffle-exam.py make --bank DIR [--extra DIR ...] \
             --ids q-001,q-002,... --seed N --out DIR

         Writes DIR/paper.md  (stems and shuffled options; no rationales, no key)
         and    DIR/key.json  (per question: id, domain, task, the
                               shown->original letter map, the correct letter
                               as shown, and the correct original letter).

  grade  Grade the learner's letters against the key.
         python3 shuffle-exam.py grade --key DIR/key.json --answers "B,A,C,..." \
             [--previous OLD_answers.json] [--save DIR/answers.json]
         For a multiple-response ("choose N") item, give its letters together,
         e.g. "B,AD,C". Order inside an item does not matter.

         Prints one line per question (letter shown, the ORIGINAL bank letter it
         maps to, the correct original letter, right or wrong), then the raw
         score, per-domain scores and the weighted overall score.
         --save writes the picks (in original letters) for QUESTION-HISTORY.md
         and for a later --previous check.
         --previous compares with an earlier sitting: how often the learner
         picked the same ORIGINAL option as last time, against chance.

The bank format is: YAML-ish frontmatter, a "## Question" section, and a
"## Options" section with lines like "- **A)** text", each followed by an
indented "  - **Rationale:** ..." line. Rationales are never copied to the paper.

Two question types:
  mcq-single  options A-D, frontmatter "correct: B" (one letter).
  mcq-multi   options A-D up to A-F, frontmatter "select: 2" and
              "correct: [B, D]" (a list). Graded right only if the picked set
              equals the key exactly (our convention; the exam guide does not
              say whether partial credit exists).
In key.json and answers.json a multi item's letters are a sorted string, e.g. "BD".
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from datetime import date
from pathlib import Path

LETTERS = ["A", "B", "C", "D"]            # options on a single-answer item
ALL_LETTERS = ["A", "B", "C", "D", "E", "F"]  # a multi item may use 4 to 6

# Official exam domain weights.
DOMAIN_WEIGHTS = {"D1": 0.27, "D2": 0.18, "D3": 0.20, "D4": 0.20, "D5": 0.15}

OPTION_RE = re.compile(r"^- \*\*([A-Z])\)\*\*\s?(.*)$")
RATIONALE_RE = re.compile(r"^\s+- \*\*Rationale:\*\*")


# ---------- parsing ----------

def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Return (frontmatter dict, index of the first body line)."""
    meta: dict = {}
    if not lines or lines[0].strip() != "---":
        return meta, 0
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return meta, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            meta[m.group(1)] = value
    raise ValueError("frontmatter is not closed with '---'")


def parse_question(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, start = parse_frontmatter(lines)

    section = None
    stem: list[str] = []
    options: dict[str, list[str]] = {}
    current: str | None = None
    in_rationale = False

    for line in lines[start:]:
        if line.startswith("## "):
            name = line[3:].strip().lower()
            section = name if name in ("question", "options") else "other"
            current = None
            in_rationale = False
            continue
        if section == "question":
            stem.append(line)
        elif section == "options":
            m = OPTION_RE.match(line)
            if m:
                current = m.group(1)
                options[current] = [m.group(2)]
                in_rationale = False
            elif RATIONALE_RE.match(line):
                in_rationale = True
            elif current and not in_rationale and line.startswith("  "):
                # Continuation of a multi-line option (e.g. a code block).
                options[current].append(line[2:])
            # Anything else (blank lines, rationale continuation) is dropped.

    qid = meta.get("id") or path.stem
    raw_correct = meta.get("correct", "").strip().upper()
    multi = meta.get("question_type", "").strip() == "mcq-multi" or raw_correct.startswith("[")
    found = sorted(options)

    if not multi:
        if found != LETTERS:
            raise ValueError(f"{qid}: expected options A-D, found {found}")
        correct = raw_correct
        if correct not in LETTERS:
            raise ValueError(f"{qid}: frontmatter 'correct' is missing or invalid")
        select = 1
    else:
        if not (4 <= len(found) <= 6) or found != ALL_LETTERS[:len(found)]:
            raise ValueError(f"{qid}: a multiple-response item needs 4-6 options A-D..A-F with no gaps, found {found}")
        letters = [x.strip() for x in raw_correct.strip("[]").split(",") if x.strip()]
        if len(letters) < 2 or len(set(letters)) != len(letters) or any(x not in found for x in letters):
            raise ValueError(f"{qid}: 'correct' must be a list of 2+ distinct option letters, e.g. [B, D]")
        correct = "".join(sorted(letters))
        try:
            select = int(meta.get("select", len(letters)))
        except ValueError:
            raise ValueError(f"{qid}: 'select' must be a number") from None
        if select != len(letters):
            raise ValueError(f"{qid}: 'select: {select}' does not match {len(letters)} letters in 'correct'")

    def tidy(block: list[str]) -> str:
        return "\n".join(block).strip("\n").rstrip()

    return {
        "id": qid,
        "domain": meta.get("domain") or None,
        "task": meta.get("task") or None,
        "type": "mcq-multi" if multi else "mcq-single",
        "select": select,
        "correct": correct,
        "stem": tidy(stem),
        "options": {k: tidy(v) for k, v in options.items()},
    }


def map_letters(mapping: dict[str, str], picked: str) -> str | None:
    """Map shown letter(s) to original letter(s); a sorted string, or None if any is invalid."""
    if not picked:
        return None
    out = [mapping.get(ch) for ch in picked]
    if any(o is None for o in out):
        return None
    return "".join(sorted(out))


def find_question(qid: str, dirs: list[Path]) -> Path:
    for d in dirs:
        p = d / f"{qid}.md"
        if p.is_file():
            return p
    # Fall back to matching the frontmatter id.
    for d in dirs:
        for p in sorted(d.glob("*.md")):
            try:
                head = p.read_text(encoding="utf-8").split("\n", 20)[:20]
            except OSError:
                continue
            if any(re.match(rf"^id:\s*['\"]?{re.escape(qid)}['\"]?\s*$", h.strip()) for h in head):
                return p
    raise FileNotFoundError(f"question {qid} not found in: {', '.join(str(d) for d in dirs)}")


# ---------- make ----------

def cmd_make(args: argparse.Namespace) -> int:
    dirs = [Path(args.bank)] + [Path(e) for e in (args.extra or [])]
    for d in dirs:
        if not d.is_dir():
            print(f"error: not a directory: {d}", file=sys.stderr)
            return 2

    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    if not ids:
        print("error: --ids is empty", file=sys.stderr)
        return 2
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        print(f"error: duplicate ids: {', '.join(dupes)}", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    block = args.block
    paper: list[str] = [f"# Mock exam — {len(ids)} questions", ""]
    paper.append("Answer each question with one letter, or with N letters where it says \"Choose N\" "
                 "(e.g. B, AD, C). No feedback until the end.")
    paper.append("")
    key_items = []

    for n, qid in enumerate(ids, start=1):
        q = parse_question(find_question(qid, dirs))
        multi = q["type"] == "mcq-multi"
        shown = ALL_LETTERS[:len(q["options"])]
        order = shown[:]  # order[i] = original letter shown at position i
        rng.shuffle(order)
        shown_to_orig = {shown[i]: order[i] for i in range(len(shown))}
        orig_to_shown = {o: s for s, o in shown_to_orig.items()}
        correct_shown = "".join(sorted(orig_to_shown[c] for c in q["correct"]))

        if (n - 1) % block == 0:
            last = min(n + block - 1, len(ids))
            paper += [f"## Block {(n - 1) // block + 1} — questions {n}–{last}", ""]
        paper += [f"### Q{n}", "", q["stem"], ""]
        if multi and not re.search(rf"choose\s+{q['select']}\b", q["stem"], re.IGNORECASE):
            paper += [f"**Choose {q['select']}.**", ""]
        for s in shown:
            text = q["options"][shown_to_orig[s]]
            first, *rest = text.split("\n")
            paper.append(f"- **{s})** {first}")
            paper += [f"  {r}" if r else "" for r in rest]
        paper.append("")

        item = {
            "n": n,
            "id": q["id"],
            "domain": q["domain"],
            "task": q["task"],
            "map": shown_to_orig,
            "correct": correct_shown,
            "correct_original": q["correct"],
        }
        if multi:
            item["type"] = "mcq-multi"
            item["select"] = q["select"]
        key_items.append(item)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "paper.md").write_text("\n".join(paper).rstrip() + "\n", encoding="utf-8")
    key = {"seed": args.seed, "created": date.today().isoformat(), "questions": key_items}
    (out / "key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")

    moved = sum(1 for k in key_items if k["correct"] != k["correct_original"])
    singles = [k for k in key_items if k.get("type") != "mcq-multi"]
    spread = {s: sum(1 for k in singles if k["correct"] == s) for s in LETTERS}
    n_multi = len(key_items) - len(singles)
    print(f"Wrote {out / 'paper.md'} and {out / 'key.json'} ({len(key_items)} questions, seed {args.seed}).")
    print(f"Correct letter moved by the shuffle on {moved}/{len(key_items)} questions.")
    print("Correct-letter spread on single-answer items: " + ", ".join(f"{s}={c}" for s, c in spread.items()))
    if n_multi:
        print(f"Multiple-response (choose N) items: {n_multi}")
    return 0


# ---------- grade ----------

def parse_answers(raw: str, has_multi: bool = False) -> list[str]:
    raw = raw.strip().upper()
    if "," in raw or " " in raw:
        parts = [p.strip() for p in re.split(r"[,\s]+", raw) if p.strip()]
    elif has_multi:
        raise ValueError('this paper has "choose N" items: separate the answers with commas, e.g. "B,AD,C"')
    else:
        parts = list(raw)
    return parts


def load_previous(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "answers" in data:
        data = data["answers"]
    prev: dict[str, dict] = {}
    for qid, v in data.items():
        if isinstance(v, str):
            prev[qid] = {"picked_original": v.upper()}
        elif isinstance(v, dict):
            prev[qid] = v
    return prev


def cmd_grade(args: argparse.Namespace) -> int:
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))
    items = key["questions"]
    answers = parse_answers(args.answers, any(i.get("type") == "mcq-multi" for i in items))
    if len(answers) != len(items):
        print(f"error: {len(answers)} answers for {len(items)} questions", file=sys.stderr)
        return 2

    results = []
    print(f"{'#':>3}  {'id':<10} {'dom':<4} {'task':<6} shown  orig  correct(orig)  result")
    for item, ans in zip(items, answers):
        if item.get("type") == "mcq-multi":
            # A set of letters: order does not matter, and it must match the key exactly.
            ans = "".join(sorted(set(ans))) if ans != "-" else ans
            picked_orig = map_letters(item["map"], ans)
        else:
            picked_orig = item["map"].get(ans)  # None for a blank or invalid answer
        ok = ans == item["correct"]
        results.append({**item, "picked": ans, "picked_original": picked_orig, "ok": ok})
        print(f"{item['n']:>3}  {item['id']:<10} {str(item['domain'] or '?'):<4} "
              f"{str(item['task'] or '?'):<6} {ans:^5}  {str(picked_orig or '-'):^4}  "
              f"{item['correct_original']:^13}  {'RIGHT' if ok else 'wrong'}")

    total = len(results)
    right = sum(r["ok"] for r in results)
    print()
    print(f"Raw score: {right}/{total} ({100 * right / total:.1f}%)")

    by_dom: dict[str, list[int]] = {}
    for r in results:
        d = r["domain"] or "?"
        by_dom.setdefault(d, [0, 0])
        by_dom[d][0] += r["ok"]
        by_dom[d][1] += 1
    print("Per domain:")
    for d in sorted(by_dom):
        ok_n, n = by_dom[d]
        w = DOMAIN_WEIGHTS.get(d)
        wtxt = f"weight {int(w * 100)}%" if w else "no weight (domain tag missing)"
        print(f"  {d}: {ok_n}/{n} ({100 * ok_n / n:.1f}%)  {wtxt}")
    weighted_doms = [d for d in by_dom if d in DOMAIN_WEIGHTS]
    if weighted_doms:
        wsum = sum(DOMAIN_WEIGHTS[d] for d in weighted_doms)
        wscore = sum(DOMAIN_WEIGHTS[d] * by_dom[d][0] / by_dom[d][1] for d in weighted_doms) / wsum
        note = "" if len(weighted_doms) == 5 else f" (only {len(weighted_doms)} of 5 domains present; weights re-normalised)"
        print(f"Weighted overall: {100 * wscore:.1f}%{note}")
    missing = [d for d in DOMAIN_WEIGHTS if d not in by_dom]
    if missing:
        print(f"Domains with no questions on this paper: {', '.join(missing)}")

    if args.previous:
        prev = load_previous(Path(args.previous))
        same = moved_n = shown_same = shown_den = 0
        same_prev_wrong = prev_wrong = 0
        for r in results:
            p = prev.get(r["id"])
            if not p or not p.get("picked_original") or not r["picked_original"]:
                continue
            moved_n += 1
            is_same = r["picked_original"] == p["picked_original"]
            same += is_same
            if p["picked_original"] != r["correct_original"]:
                prev_wrong += 1
                same_prev_wrong += is_same
            # Letter memory: did they pick the LETTER they picked last time,
            # where that letter now points at a different option?
            old_shown = p.get("picked_shown")
            if old_shown and map_letters(r["map"], old_shown) != p["picked_original"]:
                shown_den += 1
                shown_same += r["picked"] == old_shown
        print()
        print(f"Re-sit check against {args.previous}:")
        if moved_n == 0:
            print("  No overlapping questions with usable previous answers.")
        else:
            print(f"  Same ORIGINAL option as last time: {same}/{moved_n} ({100 * same / moved_n:.0f}%); "
                  f"a random pick would match ~25%.")
            if prev_wrong:
                print(f"  Of the {prev_wrong} questions missed last time, the same wrong option again: "
                      f"{same_prev_wrong}/{prev_wrong} ({100 * same_prev_wrong / prev_wrong:.0f}%).")
            if shown_den:
                print(f"  Same LETTER as last time where that letter now means a different option: "
                      f"{shown_same}/{shown_den} ({100 * shown_same / shown_den:.0f}%); chance ~25%.")
            print("  A high same-option rate on questions answered right both times is expected.")
            print("  It cannot tell recall of content from real understanding, so treat the score as optimistic.")

    if args.save:
        out = {
            "date": date.today().isoformat(),
            "key": str(args.key),
            "answers": {
                r["id"]: {
                    "picked_shown": r["picked"],
                    "picked_original": r["picked_original"],
                    "correct_original": r["correct_original"],
                    "ok": r["ok"],
                    "domain": r["domain"],
                    "task": r["task"],
                }
                for r in results
            },
        }
        Path(args.save).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"\nSaved picks (original letters) to {args.save}")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(description="Shuffle and grade a CCAF mock exam.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    mk = sub.add_parser("make", help="build paper.md and key.json")
    mk.add_argument("--bank", required=True, help="question bank directory")
    mk.add_argument("--extra", action="append", help="extra question directory (repeatable)")
    mk.add_argument("--ids", required=True, help="comma-separated question ids, in paper order")
    mk.add_argument("--seed", type=int, required=True, help="fixed shuffle seed")
    mk.add_argument("--out", required=True, help="output directory")
    mk.add_argument("--block", type=int, default=10, help="questions per block (default 10)")

    gr = sub.add_parser("grade", help="grade answers against key.json")
    gr.add_argument("--key", required=True, help="key.json from 'make'")
    gr.add_argument("--answers", required=True,
                    help='letters as shown, e.g. "B,A,C" or "BAC"; a choose-N item as "B,AD,C"; use - for blank')
    gr.add_argument("--previous", help="answers.json from an earlier sitting (or {id: original_letter})")
    gr.add_argument("--save", help="write this sitting's picks to a JSON file")

    args = ap.parse_args()
    try:
        return cmd_make(args) if args.cmd == "make" else cmd_grade(args)
    except (ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
