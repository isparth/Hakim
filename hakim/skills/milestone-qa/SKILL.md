---
name: milestone-qa
description: Use at the end of a milestone to verify it actually works — run the integration tests defined up front, do human-in-the-loop manual QA, fix what surfaces, get an independent review, and sign off before moving on. Trigger whenever someone is wrapping up a milestone, doing QA, or about to call a chunk of work "done", even if they don't name it.
---

# milestone-qa

A milestone isn't done because the tasks are done — it's done when a human has *seen* it work. This
step closes that gap.

## 1. Integration tests
Implement and run the integration tests you defined at the start of the milestone (in `tasks.md`).
For UI / end-to-end scenarios, drive a real browser with the **Playwright** MCP; for non-UI paths,
run the test suite directly. Show the output either way.

## 2. Manual QA — human in the loop
Give the human a concrete checklist to exercise the feature *for real* — e.g. "register via Google
sign-in, then confirm the new user row appears in the database." Backed by the logging from setup,
the human can watch it work end-to-end. **Tests passing ≠ product working**; this catches what tests
miss.

## 3. Fix what surfaces
Resolve anything QA or the integration tests turn up. Each fix follows the same `tdd-task` discipline
(test → green → independent review) — don't hot-patch.

## 4. Independent review
Have the **`reviewer` subagent** review the milestone's changes (Task tool, `subagent_type:
reviewer`) — same rule as always: a different agent than the one who wrote it.

## 5. Sign off + commit
The human signs off, then commit the milestone (branch per milestone is the git-discipline default).
Then move to the next one.
