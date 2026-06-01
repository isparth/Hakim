# Hakim

A Claude Code plugin that teaches engineering **judgment while you build** — instead of lecturing
concepts in the abstract, it catches the real decisions in your own project and makes you reason
through them.

It runs as two terminals: a **work** terminal where you build, and a **teacher** terminal that runs
two-tier lessons (right-for-now vs the grown-up version) on the decisions the work terminal hands
over — sending back one clean line so the work context never bloats. On top of that sits a full
**dev-workflow** skill group (PRD → tech decisions → setup → tasks → TDD → QA) with an independent
reviewer agent.

## Start here

- **[SETUP.md](SETUP.md)** — install the plugin and run the two terminals.
- **[hakim/README.md](hakim/README.md)** — the plugin itself: skills, the handoff, MCP servers.
- **[ProductBrief.md](ProductBrief.md)** · **[DevelopmentWorkflow.md](DevelopmentWorkflow.md)** — the
  thinking and the workflow behind it.

The plugin lives in [`hakim/`](hakim/). Prove the handoff works with no Claude involved:

```
bash hakim/scripts/test_hakim.sh
```
