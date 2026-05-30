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

### 7. Language / stack — **TypeScript + Node end-to-end** *(confirmed)*
One language across the hook scripts, the local service, and the companion app. Avoids a Python/JS split and keeps the whole thing approachable.

### 8. Auth & accounts — **none in v1**
Single user, single machine, local files. No login, no server.
> *Two-tier honesty:* Right call for v1. The moment you want the knowledge base to sync across devices or back up to the cloud, you'd add accounts and a sync layer — but that's a later problem.

### 9. Companion app framework — **Electron + Node/Express**
The companion app is built with **Electron**, with a **Node + Express** server inside the main process. Express is the **front door the Claude Code hooks knock on**: hook scripts `POST` their event JSON to a localhost endpoint. Backend ↔ UI uses **Electron IPC** (`ipcMain`/`ipcRenderer`), not HTTP. Frontend is **React** (in TypeScript).

**Why Electron over the alternatives:**

| | Electron *(chosen)* | Tauri | Swift / SwiftUI |
|---|---|---|---|
| UI written in | Web | Web | Native (SwiftUI) |
| Backend language | **Node — matches our stack** | Rust (language split) | Swift (language split) |
| Platforms | Mac/Win/Linux | Mac/Win/Linux | Mac only |
| Feel | Web-in-a-window | Web-in-a-window | Truly native, lightest |

Electron wins for v1 because it keeps **everything in one language** (decision #7): the hooks, the Express service, and the app are all Node/TS, and the app can share code with the service. Its only real downside — bundle size / RAM — **doesn't matter for a local dev tool**.

**The migration escape hatch (decided deliberately):**
- **→ Tauri is cheap** if we ever need a leaner footprint: both use a web frontend, so the entire UI carries over and we'd only swap the Node backend for Rust. But per **YAGNI we don't pre-plan this** — Electron is production-grade (VS Code, Slack) and may well be the permanent answer. Move only if a real constraint appears.
- **→ Swift is NOT a migration, it's a rewrite** — native UI means none of the web frontend transfers. So Electron is *not* a stepping stone to Swift. If a **native menu-bar companion** ever becomes core to the product, that's a from-scratch decision to make on its own merits, not something we drift into.

> *Two-tier honesty:* For v1, run the Express server **inside Electron's main process** — one thing to launch. The grown-up version splits the Hakim service into a **separate daemon** so hooks can reach it even when the UI window is closed. Overkill now; the seam is there for later.

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
| **How to detect a "decision" from hook events** — the hardest technical risk. | A consequential choice (which database) may surface as a plan, a prompt, or a file write. Which hook(s) to watch, and how to reliably catch the decision *before* it's locked in, needs dedicated research/prototyping. |

---

## Explicitly NOT deciding yet

- Multi-tool support (Cursor, etc.) — Claude Code only for v1.
- Cloud sync / accounts / multi-device — local-only for v1.
- Spaced-repetition scheduling internals — the KB stores enough to enable it later (P2 in the spec).
