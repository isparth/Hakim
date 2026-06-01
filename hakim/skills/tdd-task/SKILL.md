---
name: tdd-task
description: Use to implement a single task or feature using test-driven development — when the user wants to build a task from tasks.md, write tests first, do red-green-refactor, or implement something properly instead of one-shotting it. Trigger whenever someone is about to implement a scoped piece of work and you want tests-first discipline with an independent review gate.
---

# tdd-task

Implement **one** task, test-first, with the review done by a **different agent**. The loop is
red → green → independent review → human gate. Self-review doesn't count, and "the tests pass
because I say so" doesn't count.

## 0. Lock scope & align
Restate the one task in a sentence, then run `grill-task` — a quick alignment pass to confirm you
and the human mean the same thing by it, and to surface any doubts or assumptions *before* you write
a line. From here on, **only** this task — no extra features, no drive-by refactors. If you spot
other work, note it for later; don't do it now.

## 1. Red — tests first
Write the tests from the task's acceptance criteria, *before* any implementation. The human reviews
the tests — they're the spec made executable, so they're worth getting right. Then run them and
**confirm they fail**. Tests that pass before the code exists aren't testing anything.

If the user is still learning *how* to write good tests (what to assert, how to structure them),
that's a teachable moment — hand it to the teacher terminal with `request-decision` (frame it as in
step 4). The TDD habit is one of the highest-value things they'll learn; it's worth slowing down for
early on.

## 2. Green — make them pass (and instrument as you go)
Implement the smallest thing that passes the tests. Scope-locked. **Green isn't done until the code
is instrumented** — as you implement, add logging that prints the key inputs, the path taken,
outputs, external calls, and errors. Two reasons, both central to this workflow:
- The human can **see** it work (a row really landed, the API really returned 200) instead of
  trusting your word.
- When something breaks later, that runtime log **is** your debugging context. An agent that can
  read what actually happened will diagnose the bug; one guessing from the code alone often can't.
  Log richly now so future-you has something to read.

## 3. Confirm green — show it
Run the tests and **show the output in chat**. Don't *claim* they pass — demonstrate it. (Real
independent confirmation comes next, in review; this step is just you proving it with actual output
rather than your word.)

## 4. Independent review — a separate agent
Hand the change to the **`reviewer` subagent** via the Task tool:

```
Task(subagent_type: "reviewer", prompt: "<the task spec>\n\n<the diff>")
```

This is a hard rule: **the agent that wrote the code never reviews it** — authors are blind to their
own assumptions. Pass the reviewer only the **task spec + the diff** — not your reasoning, so it
judges the code as it stands. The reviewer re-runs the tests and linters itself; it doesn't take
"tests pass" on faith.

Surface its verdict to the human verbatim. On CHANGES NEEDED, address each point and re-review;
don't mark the task done until it's APPROVE.

**Teachable flags.** The reviewer also flags design-principle issues (SOLID, separation of concerns,
simplicity) and marks them **[teachable]** — but it doesn't teach them. A `[teachable]` flag is a
lesson, not a one-off bug, so hand it to the teacher terminal with `request-decision`. It isn't a
"which tool?" fork, so frame it as a refactor call:
- `decision`: "Refactor now or note for later? — <the principle the reviewer flagged>"
- `options`: `[{ "name": "refactor now" }, { "name": "note for later" }]`
- `leaning`: your honest call (a learning side-project doesn't owe every abstraction)
- `stakes`: usually **low** — log it and keep going, unless it's genuinely foundational

The teacher explains the principle and the user makes the two-tier call. The fix stays in the work
terminal; the teaching happens only in the teacher terminal.

## 5. Human gate + commit
Once review passes, the human confirms, then commit (commit after every completed-and-verified
task). One task, one commit.
