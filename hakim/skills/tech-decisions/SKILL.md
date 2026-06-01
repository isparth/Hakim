---
name: tech-decisions
description: Use right after the PRD is finalised, when choosing the INITIAL tech stack — database, backend and frontend language/framework, external APIs, auth, hosting — and capturing the few core data models and core API contracts. Trigger whenever someone is deciding what technologies to build with, starting a technical_decisions or tech_stack doc, or about to scaffold a project's foundations, even if they never name it. For tech changes once you're already building, use revise-tech-decisions instead, not this skill.
---

# tech-decisions

Goal: choose the **stack**, plus the **few core data models** and **few core API contracts**, into
`technical_decisions.md`. This is the foundation the project gets built on — which is exactly why
each choice is worth deciding deliberately, and worth *learning*.

## Hold this framing the whole time

You're at step 2–3. **Nothing is built yet.** That has two big implications, and the doc should
reflect both:

- **Minimal.** Decide only what you need to start: the stack, and only the *central* entities and
  endpoints. Modeling everything now is impossible (you don't know enough) and wasteful (most of it
  will change).
- **Extensible and expected to change.** Data models *will* evolve all through implementation. The
  doc is a living starting point, not a contract. Write it so that's obvious — minimal fields,
  marked as "will change." When they *do* change mid-build, that's `revise-tech-decisions` (which
  also syncs everything) — this skill is only the initial pass.


## The decision loop — this is the heart of it

The stack choices (database, backend language/framework, frontend, external APIs, auth, hosting) are
**consequential, hard-to-reverse decisions**. Don't just pick them and write them down. For each one:

1. **Hand it to the teacher terminal** with the `request-decision` skill — so the user learns *why*,
   gets the honest two-tier answer (right-for-now vs the grown-up version), and decides themselves.
2. **Record the resolved choice** in the doc — the one-line conclusion that comes back, plus the
   pinned version.

That loop — *decide by learning* — is the whole reason this product exists. The tech-decisions step
is where it pays off most, because these are the choices the user will most benefit from understanding.

**Rate each pick's stakes exactly as `request-decision` describes:** hard-to-undo *and* foundational
(database, language, framework, auth) → HIGH → hand off and wait for the teacher. Trivial or easily
swapped (a date-formatting library, a local file layout) → LOW → just pick it, record it, and keep
moving. Don't block on the trivial ones, and don't silently pick the foundational ones.

## Pin versions (and don't trust your memory)

Before writing a version into the doc, check the *actually installed* version (e.g. run the tool's
`--version`, read the lockfile). Agents hallucinate versions and APIs that don't exist; the doc must
reflect reality.

## Ground the choices in real docs (Context7)

When weighing options or pinning a version, pull the *current* documentation with the **Context7**
MCP instead of relying on memory — compare how two libraries actually work, confirm a feature
exists, get accurate version/API details. This is the antidote to hallucinated APIs, and it keeps
the two-tier teaching honest because it's grounded in what the tool really does today.

Division of labor: **Context7** is for deciding and confirming *before* you install (what's current,
what the API looks like); the **`--version`/lockfile check** above is for recording what *actually
landed* afterward. Use both — they answer different questions.

## The doc shape

```markdown
# Technical decisions — <project>

> Living document, created <date>. Minimal by design; data models especially WILL change during
> implementation. Last updated: <date>.

## Stack
| Area | Choice | Version | Why (one line) |
|---|---|---|---|
| Database | Postgres | 16.x | relational; data has clear links |
| Backend | <lang/framework> | | |
| Frontend | <lang/framework> | | |
| Auth | | | |
| External APIs | | | |
| Hosting | | | |

## Core data models (only the central few — will change)
**<Entity>** — <one line on what it is>
- field: type  // only the fields you're sure of now

## Core API contracts (only the central few)
`<METHOD> /path` — <purpose>
- in: { ... minimal ... }
- out: { ... minimal ... }
```

## Save it

Save the doc to `docs/technical_decisions.md` (create `docs/` if it doesn't exist) so the later
skills can find it. Order matters: draft → save the file → human reads it → sign-off. Don't leave it
sitting in chat.

## The human gate

The human reads the doc in full and signs off — these choices are theirs to own, and they're
load-bearing for everything built on top. Human and agent must be fully synced — no lingering doubts
— before sign-off. Use `grill-tech` for the back-and-forth; it's worth the time here.
