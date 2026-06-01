# Ground rules (always-on)

These sit underneath every step. Write them into the project's `CLAUDE.md` so the agent reads them
every session. They exist because they're the difference between a maintainable project and a mess
the user can't reason about.

- **Conventions live in `CLAUDE.md`.** Code style, naming, structure, allowed libraries, how to run
  tests/lint/format, and hard "never do X" rules. The agent reads this every session.
- **Independent review.** Code is reviewed by a *different* agent than the one that wrote it.
  Self-review by the author doesn't count — authors are blind to their own assumptions.
- **Git discipline.** Commit after every completed-and-verified task; branch per milestone. This is
  the undo button when the agent makes a mess.
- **Logging & observability.** Print what happens at each step — key inputs, actions, outputs, and
  errors — so a human can *see* it work (e.g. a row actually landed in the DB), not just trust the
  agent. This runtime log is also the agent's richest **debugging** context when something breaks:
  read it first, don't guess from the code alone.
- **Scope lock.** Each task means *exactly this task, nothing more.* No drive-by refactors, no
  unrequested features.
- **Pin versions.** Lock versions in the tech-decisions doc, and check the *actually installed*
  version before using an API — agents hallucinate APIs and assume versions that don't exist.
- **Security basics.** No hardcoded secrets; keys in env vars; never commit secrets.
- **Least privilege.** The agent gets the minimum access it needs. No unsupervised production
  credentials or irreversible actions (deploys, migrations, deletes) without a human pulling the trigger.
- **Stuck or uncertain → stop and ask.** Surface the blocker instead of guessing. A
  `grill-product` / `grill-tech` session is the mechanism for syncing until there are no open doubts.
- **Re-orient each session.** Start by pointing the agent at the PRD, tech decisions, tasks, and the
  current milestone. Agents lose all memory between sessions.
- **Keep the docs in sync.** Any change in plan updates the PRD, tech decisions, and tasks — as an
  explicit step, so they don't go stale.
