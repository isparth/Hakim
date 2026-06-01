---
name: plan-tasks
description: Use after the PRD and tech decisions, to break the work into milestones and tasks — when the user wants a tasks.md, a task breakdown, a build order, or to plan what to implement first. Trigger whenever someone is turning a plan into an ordered, scoped list of work, even if they don't say "tasks".
---

# plan-tasks

Turn the PRD + tech decisions into `tasks.md`: the ordered, scoped build plan. This is where vague
intent becomes work an agent can actually nail one piece at a time.

## Organize by milestone
Group tasks into **milestones** (a milestone = a coherent, verifiable slice of the product). For
each milestone, **define its integration tests up front** — write them as end-to-end scenarios /
acceptance criteria *before* the tasks, so "done" is defined before you start building. (UI / end-to-end
scenarios get exercised with the Playwright MCP at QA time — phrase them as concrete browser steps
where that applies.)

## Size tasks at the feature level — not tiny
This is the thing people get wrong, so get it right: **make tasks big — feature-sized — not small.**
Today's coding agents handle substantial, hard work in one pass. Chopping a feature into a dozen
micro-steps ("create the model", "add the endpoint", "wire the form") just adds ceremony and buries
the real feature under bookkeeping, for no benefit.

A good task is a **coherent slice of user-facing capability** you could describe in one sentence and
prove with an acceptance test — e.g. *"a user can register and log in with email + password"* — not
five separate tasks for the model, the endpoint, the hashing, the form, and the session. Big, but
not huge: one feature, not the whole backend.

Judge a task by **scope and testability, not size**:
- **Well-scoped** — one coherent capability with clear boundaries; you can say where it starts and ends.
- **Testable** — you can write an acceptance scenario that proves it works end to end.
- **Independently verifiable** — it lands as a real, demoable piece of the product.

Default to *bigger*. Only split when a piece genuinely can't be tested as part of the whole, or when
two parts are truly independent and could run in parallel.

Each task also carries:
- **Dependencies** — Task 1 → Task 2 where one needs the other.
- **A parallel flag** — for genuinely independent tasks that can run at the same time.
- **A type label where it fits** — `[frontend]` / `[api]` / `[db]` / `[external]`; a vertical feature
  slice may span several, which is fine — label the dominant one or skip it.
- **Decision flags** — any open decision blocking the task (a handoff candidate for the teacher terminal).

## Shape

```markdown
# Tasks — <project>

## Milestone 1: <name>
**Integration tests (define first):**
- Scenario: <end-to-end behavior that proves the milestone works>

**Tasks (feature-sized):**
- [ ] 1. User can register + log in with email/password — *acceptance: sign up, log out, log back in*
- [ ] 2. User can create and view a recipe  (depends on 1)
- [ ] 3. User can search recipes by ingredient  (parallel with 2)
```

## Where the tasks live — `tasks.md` or GitHub issues
Default to `tasks.md` (a local file the agent re-reads each session). Some people prefer issue
tracking — if the user does, use the **GitHub** MCP to create one issue per task instead, with the
same structure (scoped, labeled, dependencies noted). **Ask which they want; don't assume** — plenty
of people prefer the single file.

## Human gate
Back-and-forth until the human finalizes the breakdown. Use `grill-tech` if the scoping or ordering
is fuzzy.
