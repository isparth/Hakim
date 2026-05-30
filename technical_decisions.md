# Technical Decisions — v1

Everything runs locally. No cloud, no server, no accounts.

## Decisions

1. **Integration:** Claude Code only, via its hooks system (`PreToolUse`, `UserPromptSubmit`, etc., configured in `settings.json`).

2. **Intercept model:** Hybrid, driven by the taxonomy's severity grouping.
   - High-consequence decisions → hook **blocks** the agent until the user answers.
   - Lower-consequence → **non-blocking notification**; agent keeps going.

3. **Interaction surface:** A local companion app (not the terminal).

4. **App framework:** Electron. Frontend in **React**. Node + Express server in the main process — the Express endpoint is where the Claude Code hooks POST their events. Backend ↔ UI over Electron IPC.

5. **Language/stack:** TypeScript + Node end-to-end (hooks, service, app).

6. **The brain:** Claude. Cheap model (Haiku) for decision detection/classification; stronger model (Sonnet/Opus) for lessons and feedback. Prompt caching on the system prompt + taxonomy.

7. **Brain auth / who pays:** *(confirmed allowed — see rules below)* Hakim runs locally and **inherits the user's existing Claude Code auth** via the **Claude Agent SDK**. Calls draw from the user's own monthly **Agent SDK credit** (Pro $20 / Max 5x $100 / Max 20x $200, starting June 15 2026; separate from chat limits, per-user, no rollover). **Fallback:** BYOK (user's own Anthropic API key). Cost always sits with the user, never with us.
   - **Hard rule:** never build "Login with Claude" into Hakim, and never route requests through a hosted service on the user's behalf — Anthropic prohibits both. We only ever inherit auth the user set up themselves, locally.
   - **Must be token-frugal:** the subscription credit is capped and stops when exhausted. Haiku for the high-volume detection pass + prompt caching, so we don't burn the user's monthly credit.

8. **Storage:** Local only. We store **knowledge context** — what the user has already learned — as Markdown files (Obsidian-compatible), one note per concept with date + tags. No other database.

9. **Decision taxonomy:** A versioned config file (YAML or Markdown) listing what counts as a consequential decision, grouped by severity.

## The intercept flow

1. Claude Code is about to do something consequential.
2. A `PreToolUse` hook fires and POSTs to the local Express endpoint.
3. The service classifies it against the taxonomy. High-consequence → hold the hook, push a prompt to the app.
4. User answers in the app, writes their takeaway → saved to the knowledge context.
5. The service releases the hook → agent resumes.

Low-consequence items skip the hold — notify and allow immediately.

## Open

- **Decision detection from hook events** — which hook(s) to watch and how to catch a decision before it's locked in. Needs prototyping against real session data.
