# CCAF study kit

This project helps people prepare for Anthropic's Claude Certified Architect – Foundations exam. Many people who open it are **not developers**. They may have just downloaded it and not know what to type.

## When someone seems new

If the first message is a greeting, "what now?", "how does this work?", or anything that isn't a clear task, welcome them in two or three plain sentences:

- This is a study kit for the CCAF exam, with a tutor called Richard and an interactive study map.
- To start, they just say **"Talk to Richard"**. He'll ask about their role, find their starting level and open their study map next to the chat.

Then stop and let them answer. Don't explain the repo's structure, BMad, or the files.

If they ask to see the map without Richard, open `study-map/ccaf-study-map.html` for them (in Claude Desktop, link the file so it opens in the preview pane; otherwise tell them to open it in a browser).

## Writing for learners

Use plain words. Explain any technical term the first time. Never assume they know git, the terminal or JSON.

## Working on the kit itself

Changes to Richard live in `.claude/skills/agent-ccaf-tutor/`. The study map and Richard's `assets/placement.md` share the placement questions; change both together. Learners' personal data lives in `_bmad/memory/` and is never committed.
