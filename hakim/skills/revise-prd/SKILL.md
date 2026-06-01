---
name: revise-prd
description: Use DURING the project (not for the initial PRD) whenever product scope shifts because of something you learned while building — a feature to add, drop, or reshape. Resolves the scope change and then syncs the PRD, tasks, and tech decisions so nothing drifts. Trigger whenever the user wants to change scope mid-build, or says "actually we also need…", "let's cut…", "this feature should really work like…", even if they never mention the PRD.
---

# revise-prd

This is the *mid-build* counterpart to `write-prd`. The initial PRD captured scope before any code
existed. This handles the scope changes you discover *while* building: a feature you didn't know you
needed, one that turns out pointless, one that should work differently. Changing scope as you learn
is healthy — letting the docs drift from what you're actually building is not.

So: **resolve the scope change**, then **sync everything**.

## 1. Resolve the change
Move the feature between Core / Additional / NOT-doing, or add / remove / reshape it. If the user is
genuinely unsure whether it belongs in scope *now* (vs later, vs never), that's a teachable call —
hand it to the teacher terminal with `request-decision`.

## 2. Sync — the whole point of this skill
Walk every artifact the change touches:

- **`prd.md`** — make the edit; note the date (living doc).
- **`tasks.md`** — a new feature usually means new tasks; a cut feature may orphan tasks to delete.
- **`technical_decisions.md`** — does the feature need a new data model, contract, or external API?
  If so, follow up with `revise-tech-decisions`.

End by stating what you synced, so nothing is left stale.

## When the ripple isn't clear
Run `grill-product` — get grilled until the scope change *and its consequences* are fully agreed
before you call it done.
