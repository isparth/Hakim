# Technical Decisions — Working Draft

> **Status:** v1 scope. Draft for back-and-forth — not yet signed off. Push back on anything; per our workflow these aren't final until human and agent are fully synced.
> **Scope:** High-level decisions only — the stack and the architecture. Not folder structure, libraries, or implementation detail.

---

## Architecture at a glance

Hakim is a **local-first companion** that watches a Claude Code session, intercepts consequential decisions, and teaches through a separate app. Nothing runs in the cloud in v1.

```
   ┌──────────────┐   hook fires    ┌──────────────────┐   prompt    ┌─────────────────┐
   │  Claude Code │ ──────────────▶ │   Hakim service  │ ──────────▶ │  Companion app  │
   │   (+ hooks)  │ ◀────────────── │   (local daemon) │ ◀────────── │  (user answers) │
   └──────────────┘  release/allow  └──────────────────┘   answer    └─────────────────┘
                                       │          │
                          Anthropic API│          │ local files
                                       ▼          ▼
                               (the "brain")   Markdown KB + taxonomy
```

The agent does the coding. The hook is the tripwire. The service is the brain-and-traffic-cop. The app is where the human thinks. Everything lives on the user's machine.

---

## Decisions

### 1. Integration mechanism — **Claude Code hooks**
v1 targets **Claude Code only**. We use its hooks system (`PreToolUse`, `UserPromptSubmit`, etc., configured in `settings.json`) as the tripwire. This is the only chosen tool that lets us genuinely intercept *before* the agent acts — which the core feature requires.
> *Two-tier honesty:* For v1 this is exactly right — one tool, a real interception point, fast to build. At scale you'd abstract the integration so Cursor and others plug in behind the same interface; that's overkill now and would slow us down before we've proven the loop works.

### 2. Intercept model — **hybrid (block big, advise small)**
The taxonomy's severity grouping drives behavior:
- **High-consequence** decisions → the hook **blocks** the agent (returns a blocking decision / non-zero exit) and waits until the user answers in the app.
- **Lower-consequence** items → **non-blocking notification**; the agent keeps going, Hakim pings the app.

### 3. Interaction surface — **companion app, local-first**
The user sees and answers prompts in a dedicated app, not the terminal. Richer room for lessons, quizzes, and browsing the knowledge base. Because it must read local files (the KB, Claude Code's session transcripts) and talk to the local hook process, **it has to be local-first** — not a cloud web app.

### 4. The brain — **Anthropic Claude API**
Hakim needs an LLM to detect decisions, generate the two-tier lessons, and grade the user's answers. We use the Anthropic API with a **tiered model approach**: a cheap, fast model (e.g. Haiku) for the high-volume detection/classification pass, a stronger model (Sonnet/Opus) for lessons and feedback. Use **prompt caching** for the system prompt + taxonomy to keep cost down.

### 5. Knowledge base — **Markdown files (Obsidian-compatible)**
The moat is "notes in the user's own words." Plain Markdown keeps them user-readable, portable, diff-able, and gives Obsidian integration for free. One note per concept, with date + tags in frontmatter.

### 6. Decision taxonomy — **a versioned config file**
The list of what counts as a consequential decision, grouped by severity, lives in a checked-in config file (YAML or Markdown). Authored and maintained by us; versioned so we can improve it over time. This is a core product artifact, not just config.

### 7. Language / stack — **TypeScript + Node end-to-end** *(recommended, open)*
One language across the hook scripts, the local service, and the companion app. Avoids a Python/JS split and keeps the whole thing approachable. *(See open sub-decisions.)*

### 8. Auth & accounts — **none in v1**
Single user, single machine, local files. No login, no server.
> *Two-tier honesty:* Right call for v1. The moment you want the knowledge base to sync across devices or back up to the cloud, you'd add accounts and a sync layer — but that's a later problem.

---

## How the block actually works (the load-bearing flow)

This is the crux, so spelling it out:

1. Claude Code is about to do something consequential (e.g. write a file that introduces a database dependency).
2. A `PreToolUse` hook fires and calls the local Hakim service.
3. The service classifies the action against the **taxonomy**. High-consequence → it tells the hook to **hold**, and pushes a prompt to the companion app.
4. The agent is paused. The user answers in the app ("What's your call, and why?" → choose, or "teach me").
5. The user writes their takeaway → saved to the Markdown KB.
6. The service releases the hook → **the agent resumes**.

For low-consequence items, step 3 sends a notification instead and immediately allows the tool call — the agent never waits.

---

## Open sub-decisions (to resolve next)

| Question | Notes |
|---|---|
| **Desktop vs. local web app** for the companion. | Both can be local-first. Desktop (Tauri/Electron) feels native and gets filesystem access cleanly; a local web app (localhost) is lighter to build but needs a local server. Tauri leans light, Electron leans familiar. |
| **Confirm TypeScript/Node** as the single stack. | Alternative: Python for the service (stronger LLM-orchestration ecosystem) + JS only for the app. Trades the single-language simplicity for a more natural LLM backend. |
| **How to detect a "decision" from hook events** — the hardest technical risk. | A consequential choice (which database) may surface as a plan, a prompt, or a file write. Which hook(s) to watch, and how to reliably catch the decision *before* it's locked in, needs dedicated research/prototyping. |

---

## Explicitly NOT deciding yet

- Multi-tool support (Cursor, etc.) — Claude Code only for v1.
- Cloud sync / accounts / multi-device — local-only for v1.
- Spaced-repetition scheduling internals — the KB stores enough to enable it later (P2 in the spec).
