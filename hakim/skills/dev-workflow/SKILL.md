---
name: dev-workflow
description: Use at the very start of building any software project, or whenever the user asks "what's next", "how should I build this", "where do I start", or seems about to jump straight into coding without a plan. Orients them in the plan → tech-decisions → setup → tasks → TDD → QA workflow, sets up the ground rules and living docs, and points to the right step skill. Trigger this whenever someone is starting to build something real and hasn't set up the workflow yet, even if they never say the word "workflow".
---

# dev-workflow (the spine)

This is a **human-in-the-loop** workflow for building real software with an AI agent. The point is
to stop the user from vibe-coding (one-shotting the agent and accepting whatever comes back) and
instead walk them through plan → decide → build → verify, repeatedly, until it's habit. That habit
*is* the highest-leverage lesson.

**Two principles run underneath everything:**
1. **The agent does the work; the human approves at every gate.** Nothing is "done" because the
   agent says so — it's done because a human verified it.
2. **Learn at decisions.** When a real decision shows up, don't just pick it — hand it to the teacher
   terminal with the `request-decision` skill, so the user understands *why* and gets sharper for
   next time.

## The map

| # | Step | Skill | Output (a *living* doc) |
|---|---|---|---|
| 1 | Decide what to build | (human) | — |
| 2 | Features / scope (initial) | `write-prd` | `prd.md` |
| 3 | Tech stack + core models/contracts (initial) | `tech-decisions` | `technical_decisions.md` |
| 4 | Get a hello-world running + observable | `setup-environment` | working localhost |
| 5 | Break into milestones + tasks | `plan-tasks` | `tasks.md` |
| 6 | Implement each task, test-first | `tdd-task` | code + tests |
| 7 | Verify the milestone for real | `milestone-qa` | signed-off milestone |

Each step ends at a **human gate** — the human pulls the trigger, then you move on. Don't advance
on your own say-so.

## Tools you use throughout (not numbered steps)

These aren't steps — reach for them whenever the moment calls, all through the project:

- **`revise-prd`** — product scope changes mid-build (add / cut / reshape a feature), then syncs the docs.
- **`revise-tech-decisions`** — a technical decision surfaces or changes mid-build, then syncs the docs.
- **`grill-product` / `grill-tech`** — get grilled to clear any doubt before locking a product or
  technical decision. Use them liberally; alignment beats guessing.

The initial `write-prd` / `tech-decisions` set the baseline; the `revise-*` skills evolve it.
Separating creation from evolution is deliberate — deciding something mid-build is a different moment,
with a different risk (stale docs), than planning it up front. The `revise-*` skills exist to keep
everything **synced** when reality moves.

## First time in a project — one-time setup

1. If there's no `CLAUDE.md`, create one and write in the ground rules from
   [references/ground-rules.md](references/ground-rules.md). These are always-on conventions the
   agent should read every session (review discipline, scope lock, git, version pinning, etc.).
2. Create a `docs/` folder to hold `prd.md`, `technical_decisions.md`, and `tasks.md` as they come.

## Every session after — re-orient

Agents lose memory between sessions. Start by pointing yourself at `prd.md`,
`technical_decisions.md`, `tasks.md`, and the current milestone. Then figure out where the user is
in the map above and continue from there.

## Keep the docs in sync

The three docs (PRD, tech decisions, tasks) drift if you let them. Whenever a plan or decision
changes, updating them is an explicit step — not an afterthought.

## What to do now

Work out which step the user is on from the map and **invoke that step's skill**. If they're just
starting, that's usually `write-prd`. Tell them plainly where they are and what's next — don't make
them guess.
