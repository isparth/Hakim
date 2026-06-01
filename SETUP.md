# Hakim — Setup Guide

Hakim runs as **two terminals on the same project folder**:

- **Work terminal** — where you build. When you hit a real decision, it pauses and hands it off.
- **Teacher terminal** — where the lesson happens. It teaches, you decide, and the work terminal
  resumes with one clean line.

This guide gets both running.

---

## Prerequisites

- **Claude Code** installed and logged in.
- **Python 3** — for the handoff plumbing. Check: `python3 --version` (macOS already has it).
- **Node.js / npx** — for the MCP servers (Context7, Playwright, GitHub). Check: `npx --version`.
- *Optional:* a **GitHub personal access token** (only if you want tasks as GitHub issues), and an
  **Obsidian vault** (to keep the lesson notes there).

---

## 1. Get the plugin

You can install straight from GitHub, or from a local copy if you're still working on it.

### Option A — from GitHub (once you've pushed this repo)

In Claude Code, run:

```
/plugin marketplace add <your-github-username>/Hakim
/plugin install hakim@hakim-marketplace
```

Claude Code downloads the repo and installs the plugin for you. Replace
`<your-github-username>` with wherever you pushed it (e.g. `parthpoudel/Hakim`).

### Option B — from a local copy (development)

Clone or open the repo, then point Claude Code at the folder:

```
/plugin marketplace add /absolute/path/to/Hakim
/plugin install hakim@hakim-marketplace
```

(`hakim-marketplace` is the marketplace name defined in `.claude-plugin/marketplace.json`; the plugin
inside it is `hakim`.)

### Verify

Run `/plugin` — you should see **hakim** listed and enabled. Its skills (`write-prd`,
`tech-decisions`, `tdd-task`, …) and the `/teacher` command are now available, and the three MCP
servers are registered.

---

## 2. Configure (optional)

Hakim keeps its state in a `.hakim/` folder in your project. A config file controls where things go:

`.hakim/config.json`
```json
{
  "file": ".hakim/decisions.jsonl",
  "obsidian_vault": ".hakim/notes",
  "stakes_default": "high"
}
```

- **`obsidian_vault`** — point this at your real Obsidian vault to keep lesson notes there.
- **GitHub token** (only if you want GitHub issues): `export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx`
  in the shell you launch Claude Code from. Don't want GitHub at all? Delete the `github` block from
  `hakim/.claude-plugin/plugin.json`.

The `.hakim/decisions.jsonl` and `.hakim/notes/` are runtime data (gitignored); `config.json` is
yours to keep.

---

## 3. Run it — the two terminals

Open the **same project folder** in two terminals.

**Terminal 1 — Work.** Launch Claude Code and just start building. The `dev-workflow` skill orients
you, and `request-decision` steps in on its own when you hit a consequential fork.

**Terminal 2 — Teacher.** You want this one to keep listening no matter what, so start it with the
**supervisor launcher**, run **from the same project folder**:

```
bash /path/to/hakim/scripts/hakim-teacher.sh
```

During local development that's `bash hakim/scripts/hakim-teacher.sh` from the repo; once installed,
the script lives under the plugin's folder (symlink it somewhere handy if you like). It keeps a
teacher session alive and **restarts it if it ever drops**, while the session itself loops
watch → teach → resolve and is told never to stop. Press **Ctrl-C** to stop it (otherwise it keeps
relaunching).

*Simpler alternative:* just launch Claude Code and run `/teacher` (or `/hakim:teacher`) — same loop,
without the auto-restart safety net. Fine for a quick session.

Both terminals talk through `.hakim/decisions.jsonl` — that's the whole handoff.

---

## 4. A first run

In the **Work** terminal, try:

> "I want to build a recipe-sharing web app — help me start the right way."

What happens:
1. `dev-workflow` orients you → `write-prd` (features) → `tech-decisions` (the stack).
2. At the database choice, the work terminal pauses: *"head to your teacher terminal."*
3. The **Teacher** terminal lights up, runs the two-tier lesson (right-for-now vs the grown-up
   version), and you decide.
4. The work terminal resumes with one line (`Using Postgres — relational links`) and keeps going. A
   dated note lands in your Obsidian vault.

From there the workflow continues: `setup-environment` → `plan-tasks` → `tdd-task` (red → green →
independent review) → `milestone-qa`.

---

## 5. Verify the plumbing (no Claude needed)

You can prove the handoff works with plain shell, before involving any agent:

```
bash hakim/scripts/test_hakim.sh
```

16 checks should pass — two shell processes round-tripping a decision through the file.

---

## MCP servers

- **Context7** (docs) and **Playwright** (browser tests) auto-install via `npx` the first time
  they're used — no token, no manual install.
- **GitHub** (optional) needs the token above and is only used in the task-planning step *if* you
  choose issues over `tasks.md`. It uses `@modelcontextprotocol/server-github`; swap it for the
  official GitHub MCP server in `hakim/.claude-plugin/plugin.json` if you prefer.

---

## Updating / removing

- **Update:** `/plugin marketplace update hakim-marketplace`, then reinstall if needed.
- **Enable/disable/remove:** open the `/plugin` menu and manage `hakim` there.

---

## Troubleshooting

- **Skills not showing up** — run `/plugin`, confirm `hakim` is enabled; restart Claude Code if you
  just installed it.
- **Teacher never catches a decision** — make sure both terminals are launched from the *same* folder
  (so they share the same `.hakim/decisions.jsonl`).
- **MCP server errors** — confirm `npx` works; the GitHub server needs `GITHUB_PERSONAL_ACCESS_TOKEN`.
- **Want fewer interruptions** — set `stakes_default` lower, or tell the work agent to only hand off
  genuinely foundational decisions.
