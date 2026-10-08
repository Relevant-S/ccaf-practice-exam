---
name: study-map
description: Publish, open and sync the learner's own study map
---

# Study Map

The study map (`{project-root}/study-map/ccaf-study-map.html`) teaches the foundations: a basics branch for non-developers, lessons per exam topic, worked cases and self-checks. Each learner gets **their own copy published as a private artifact**, opened next to the chat. The copy has a small database that you and the map share, so neither side needs copy-paste.

## When the Artifact tool is not available

Some surfaces (a plain terminal without artifacts) can't publish pages. Then tell the learner to open `study-map/ccaf-study-map.html` in their browser, and use the paste-prompt flow in `references/first-breath.md`. Skip the rest of this file.

## The shared database

Only the map's owner (the learner) can read or write it, even if they share the link. Three documents:

| Document | Written by | Holds |
|---|---|---|
| `learner/progress` | The map | `read`, `cases`, `checks` (lesson ids → true), `profile` (the placement done in the map, including `plan`: exam date, hours, learning style, quiz mode), `updatedAt`, `mapVersion` |
| `learner/placement` | You | A placement done in chat: `role`, `exp`, `gaps`, `track`, `date`, `at` (ISO timestamp), `source: "richard"`. The map adopts it if it's newer than its own. |
| `learner/practice` | You | `tasks`: one entry per exam task code, e.g. `"3.2": {"answered": 7, "correct": 5, "last": "2026-10-08"}`. The map shows it in the lesson and counts 80%+ over 3 or more questions as the ring's check part. |

Lesson ids in `progress`: basics are `b1`–`b9`; topic lessons are `t1.1`–`t5.6`, one per exam task (for example `t2.4`).

Read and write with the **ArtifactData** tool (load it with ToolSearch: `select:ArtifactData`). Use the map's URL from `BOND.md`. Writes need the learner's approval the first time; that's expected.

## First publish (end of First Breath, or the first time a learner has no map)

1. Build the page: `python {skill-root}/scripts/build-map-artifact.py {project-root}` (on Windows try `python`, then `py`, then `python3`). It writes `{project-root}/_bmad/memory/ccaf-tutor/map/ccaf-study-map.html` and prints `map_version`.
   - **No Python?** Read `study-map/ccaf-study-map.html`, drop the outer wrapper lines (`<!doctype html>`, `<html lang="en">`, `<head>`, the two `<meta …>` lines, `</head>`, `<body>`, `</body>`, `</html>`), and write the rest with the Write tool to that same path. The version is the `MAP_VERSION` value in the page.
2. Publish it with the Artifact tool:
   - `file_path`: the built file
   - `icon`: `map`
   - `description`: "My CCAF study map: lessons, worked cases and my progress."
   - `capabilities`: `{"db": {"rules": [{"path": "learner", "read": "owner", "write": "owner"}]}, "user": {}}`
3. Save to `BOND.md` → **Study map**: the URL, `map_version`, and today's date.
4. If you ran the placement in chat, write it to `learner/placement` (ArtifactData `set`), with `at` set to the current time.
5. Tell the learner, in one or two plain sentences, that this is their map, that it sits next to the chat, and that their progress is saved with it.

A publish opens the page by itself. If it doesn't, use the Artifact tool's `open` action with the URL.

## Every session (rebirth)

If `BOND.md` has a study map URL:

1. **Read their progress:** ArtifactData `get` on `learner/progress`.
   - Note which lessons they've read since last time. Use it when choosing what to suggest.
   - If `profile` is newer than the **Starting point** in `BOND.md` (compare dates), they redid the placement in the map. Update BOND.
2. **Check the version.** Compare `map_version` in BOND with `MAP_VERSION` in `{project-root}/study-map/ccaf-study-map.html`. If the repo is newer:
   - Rebuild (step 1 above).
   - Read the artifact first (Artifact tool, `action: "read"`, with the URL). A publish to an artifact from an earlier conversation must read it first.
   - Publish the built file with `url` set to the map's URL. **Leave `capabilities` out**, so the stored database rules are kept. Progress survives a republish.
   - Update `map_version` in BOND and tell the learner in one line that their map got new lessons.
3. When the learner asks for the map ("open my map", "show the map"), use the Artifact tool's `open` action with the URL.

If `BOND.md` has no map URL and the Artifact tool is available, offer once: *"There's a study map I can set up for you: lessons and your progress, next to this chat. Want it?"* Then follow "First publish".

## After a quiz

At session close, after writing `QUESTION-HISTORY.md`, update `learner/practice`:

1. `get` the document (it may not exist yet).
2. For each exam task code quizzed this session, add the questions answered and answered correctly to its counts, and set `last` to today.
3. `set` the whole document back.

Only count real quiz answers (examination or a quiz inside tutoring). Explanations don't count.

## Suggesting the next step

The map shows a "Your path" list. When the learner asks what to do next, match it: the first lesson on their path they haven't read, or a Richard quiz on a topic they've read but not yet checked. Name the place they'll find it: "In your map: Basics → B4 JSON."
