---
name: setup-environment
description: Use after tech decisions are locked, to scaffold the project and get a minimal working app running — a hello-world on localhost with frontend, backend, and database wired together, plus logging so you can see data flow. Trigger whenever someone is setting up a new codebase, installing the stack, or getting their first end-to-end "it runs" moment, even if they don't name it.
---

# setup-environment

Goal: a **working, observable** skeleton you can build on — and, crucially, *see* working. Not the
app yet, just everything wired together.

Keep it dead simple. The target:
- A hello-world frontend up on `localhost` (e.g. `:3000`).
- A backend running and reachable.
- The database connected — prove it with one trivial round-trip (write a row, read it back).
- **Heavy logging** at each hop, so a human can watch data actually flow end-to-end.

That observability is the whole point: later, milestone verification depends on a human being able
to *see* it work (a row really landed in the DB), not trust the agent. Wire it in from the start.

Use the stack and versions from `technical_decisions.md` — and check the *actually installed*
versions as you go (agents hallucinate versions). If something can't be what the doc said, that's a
real change: update `technical_decisions.md` (keep the docs in sync).

## Human gate (light)
The human just confirms the frontend loads and the backend/database are connected. This step is
plumbing, so the gate is light.
