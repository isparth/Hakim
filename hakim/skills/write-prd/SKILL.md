---
name: write-prd
description: Use when starting a new project and working out the INITIAL set of features / scope / PRD — the first cut before any code exists. Trigger whenever someone is first figuring out what to build, even if they never say "PRD". For changing the PRD mid-build (adding, dropping, or reshaping features once you're already building), use revise-prd instead, not this skill.
---

# write-prd

A PRD here is simple: the agreed list of features, split into **Core (MVP)** and **Additional
(later)**. That's it. Its job is to get the human and agent pointed at the same thing before any
code exists.

Two consequences:
- **Don't over-specify.** No implementation detail, no edge-case fishing. Keep it feature/product level.
- **Expect it to move.** You'll add, drop, and reshape features as you build — that's expected, not
  a failure of planning.

If the user is vague about the product they want to build, use the `grill-product` skill to sharpen
it before drafting.

## Drafting it

Draft using this shape:

```markdown
# PRD — <project>

## What this is
<few sentences: what is the product and what problem is it solving>

## Core (MVP)
- [ ] <feature as an outcome>
- [ ] <feature as an outcome>

## Additional (later)
Nice-to-haves that aren't the focus for the MVP.
- <feature>
- <feature>

## Explicitly NOT doing (for now)
- <thing you're consciously skipping, so it doesn't creep in>

> Living document — created <date>. Features will change as we learn. Last updated: <date>.
```

Save the draft to `docs/prd.md` (create `docs/` if it doesn't exist) so the later skills can find
it. Order matters: draft → save the file → human reads it → sign-off. Don't treat it as done while
it only exists in the chat.

## Changing it later is a different skill

This skill is the *initial* PRD only. Once you're building and scope shifts — a feature to add, cut,
or reshape — use `revise-prd`, which makes the change *and* syncs the other docs. Keeping creation
and evolution separate is deliberate: they're different moments with different risks (the mid-build
risk is stale docs).

## The human gate

The human reads the PRD in full and signs off — this is *their* product. If anything's fuzzy or you
have doubts, run a `grill-product` session to clear them before sign-off rather than guessing.
</content>
