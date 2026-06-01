---
name: revise-tech-decisions
description: Use DURING implementation (not at the start) whenever a technical decision comes up that the initial tech-decisions pass didn't settle — a task is blocked on a choice, a data model needs to change, an API contract needs adjusting, or a stack choice turns out wrong or unnecessary. Resolves the decision and then syncs every affected doc and the code so nothing drifts. Trigger whenever a tech decision surfaces mid-build, even if the user just says "I think we need to change X" or "this is blocked on deciding Y".
---

# revise-tech-decisions

This is the *mid-build* counterpart to `tech-decisions`. The initial pass set the broad stack before
any code existed. This one handles the decisions reality forces on you *while* you implement: a task
blocks on a choice, a data model needs a new field, a contract was wrong, a decision turns out
unnecessary. Those are normal and constant — data models especially change all through
implementation. The danger isn't making these decisions; it's letting the docs rot while the code
moves on.

So this skill is two jobs: **resolve the decision**, then **sync everything**.

## 1. Resolve the decision
If it's consequential (changes a data model lots of things depend on, swaps a library, changes a
contract), treat it as a real decision: hand it to the teacher terminal with `request-decision` so
the user learns *why* and decides. Trivial, local choices you can just make and record.

When the change involves a new library or API, pull current docs with the **Context7** MCP and
verify it really works the way you expect *before* committing — don't pin from memory.

## 2. Sync — the whole point of this skill
Once decided, walk every artifact the decision touches and update it in the same breath. Do not stop
at the one file in front of you:

- **`technical_decisions.md`** — update the stack row / data model / API contract. Note *what changed
  and why*, with the date (living doc).
- **`tasks.md`** — does this add, change, or orphan tasks? A new field may need a migration task; a
  dropped approach may delete tasks.
- **`prd.md`** — only if the change actually shifts product scope (it usually doesn't; if it does,
  that's a `revise-prd` follow-up).
- **The code** — if a data model or contract changed, the migrations and usages must follow — as
  scoped tasks through `tdd-task`, not a hot-patch.

End by stating plainly what you synced, so the user can see nothing was left stale.

## When the blast radius is unclear
If you're not sure where a change ripples, that's a `grill-tech` moment — get grilled until you and
the user agree on the full reach of the change before you call it synced. Guessing here is how docs
and code silently diverge.
