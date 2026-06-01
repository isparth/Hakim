---
name: grill-task
description: Use right before implementing a single task (e.g. at the scope-lock step of tdd-task) to get the human and agent aligned on exactly what the task is and what "done" means. Lighter than grill-product / grill-tech — the goal is shared understanding of THIS one task, and a chance for the agent to surface any doubts, assumptions, or ambiguities before writing code. Trigger whenever you're about to build a scoped task and want to confirm you're building the right thing.
---

# grill-task

A quick alignment pass on **one task**, just before you implement it. Unlike `grill-product` and
`grill-tech`, this is **not** a relentless interrogation — the goal is simply that you and the human
mean the same thing by this task before any code exists. Light touch: align, then build.

The real value here is the agent **surfacing its own doubts**. Misalignment hides in the gap between
what the task says and what the agent silently assumes — so say the quiet part out loud rather than
guessing and building the wrong thing.

**If there are no real doubts, don't manufacture any.** Sometimes the task is genuinely clear — the
acceptance criteria are unambiguous and you know exactly what to build. In that case say so in one
line and go straight to building. Don't invent questions just to run the ritual.

## First, look — don't ask what you can read
Read the task and its acceptance criteria in `tasks.md`, plus anything relevant in `prd.md` /
`technical_decisions.md`. Resolve what you can yourself. Only raise what's *genuinely* unclear.

## Then surface your doubts — one at a time
For each thing you're unsure about, state it plainly **with a proposed default**, so the human can
just confirm or correct rather than answer from scratch:
- Assumptions you're making (that would otherwise get baked into the code silently).
- Ambiguities in the acceptance criteria — what does "done" actually include?
- Edge cases or inputs the task doesn't mention.
- Anything underspecified you'd otherwise have to guess at.

Take a position; don't just dump a list of open questions on the human.

## Stay scoped to this task
Only **this** task. If a doubt is really about product scope, that's `grill-product` / `revise-prd`;
if it's about architecture or a tech choice, that's `grill-tech` / `revise-tech-decisions`; if it's
a genuine, consequential decision worth learning, hand it to the teacher with `request-decision`.
Don't let alignment quietly grow the task.

## When to stop
Stop as soon as you both agree what this task is and what "done" looks like — that's alignment, and
it's enough. If you had no doubts to begin with, you're already there — just proceed. Don't
over-grill; this is a confirmation, not a gauntlet. If the back-and-forth
sharpened the acceptance criteria, update `tasks.md` so the spec matches what you agreed. Then go
write the tests.
