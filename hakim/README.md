# Hakim

Teaches engineering judgment **while you build**. Instead of lecturing concepts in the abstract,
it catches the real decisions in your own project and makes you reason through them.

It runs as **two terminals**:

- **Work terminal** — you build here with Claude Code.
- **Teacher terminal** — lessons happen here.

When the work agent hits a consequential decision, it stops and hands it off. You learn and decide
in the teacher terminal. The teacher sends back **one clean line**, and the work agent keeps
building — so the work terminal's context never fills up with the messy debate.

```
work terminal                         teacher terminal
─────────────                         ────────────────
hits a real decision
  └─ writes a decision record ──►  watch picks it up
        (then waits)                  └─ runs the two-tier lesson with you
                                      └─ you decide
  resumes with one line  ◄──────────  resolve sends back {choice, why, future_note}
                                      └─ writes a fat note to Obsidian
```

## How it works

Everything crosses through one append-only file, `.hakim/decisions.jsonl` (which doubles as your
decision history). The plumbing is a tiny zero-dependency Python script, `scripts/hakim.py`:

| Command | Who | Does |
|---|---|---|
| `request` | work | append a decision, print its id |
| `wait <id>` | work | block until that decision is resolved |
| `watch` | teacher | block until the next unhandled decision |
| `resolve <id>` | teacher | send back the one-line conclusion |
| `note` | teacher | write a dated, tagged note to your Obsidian vault |
| `history` | either | dump past decisions |

"Waiting" is just blocking and polling the file — no daemon, no server.

## Setup

1. **Config** — `.hakim/config.json` (created for you):
   ```json
   { "file": ".hakim/decisions.jsonl", "obsidian_vault": ".hakim/notes", "stakes_default": "high" }
   ```
   Point `obsidian_vault` at your real Obsidian vault to keep the learning notes there.

2. **Two terminals, same project folder:**
   - **Teacher:** start the listener with the supervisor launcher (recommended) —
     `bash scripts/hakim-teacher.sh` from your project folder, which auto-restarts if it ever drops —
     or just run the `/teacher` command for a quick, no-safety-net session.
   - **Work:** just build. The **request-decision** skill fires on its own when you hit a real
     fork (database, language, framework, auth, hosting…).

## The one knob — stakes

- **High** → the work agent waits for you (the *Decision Intercept*).
- **Low** → it logs the decision and keeps going (a relaxed *Lesson Opportunity* later).

Same machinery either way.

## The dev-workflow skills

Hakim also ships a group of lightweight skills that walk the user through a structured build — so
they follow a real workflow instead of vibe-coding, and hit teachable decisions along the way. Each
is a thin facilitator that produces a *living* doc and hands the real decisions to the teacher
terminal.

| Skill | Step | Output |
|---|---|---|
| `dev-workflow` | the spine / map | sets up ground rules + docs, says what's next |
| `write-prd` | features & scope (initial) | `prd.md` (Core / Additional / NOT-doing) |
| `tech-decisions` | stack + core models/contracts (initial) | `technical_decisions.md` (each choice taught) |
| `setup-environment` | hello-world + observability | a running, observable skeleton |
| `plan-tasks` | milestones + tasks | `tasks.md` (tests-first, scoped, ordered) |
| `tdd-task` | implement one task | code + tests, red → green → review |
| `milestone-qa` | verify the milestone | manual QA + sign-off |
| `revise-prd` | scope change mid-build | edits `prd.md` **and syncs** tasks/tech |
| `revise-tech-decisions` | tech decision mid-build | edits `technical_decisions.md` **and syncs** tasks/code |
| `grill-product` / `grill-tech` | clear doubts (used throughout) | alignment before locking a decision |

Review is enforced by a separate **`reviewer` agent** — code is never reviewed by the agent that
wrote it. `tdd-task` and `milestone-qa` delegate to it. The reviewer also *flags* design-principle issues
(SOLID, separation of concerns, simplicity) and marks them teachable — but it doesn't teach them; the
lesson is delivered in the teacher terminal. Only the teacher teaches.

## MCP servers it uses

The plugin wires in three MCP servers for the steps that need them:

- **Context7** — current, real documentation for the stack. Used in `tech-decisions` /
  `revise-tech-decisions` so choices and version pins are grounded in what tools actually do today,
  not hallucinated. No token needed.
- **Playwright** — drives a real browser for end-to-end integration tests in `milestone-qa`.
- **GitHub** *(optional)* — create one issue per task instead of `tasks.md`, if you prefer issue
  tracking. Needs a `GITHUB_PERSONAL_ACCESS_TOKEN`; remove it from `plugin.json` if you'd rather
  keep tasks in the file. (Uses `@modelcontextprotocol/server-github` via npx — swap for the
  official server if you prefer.)

## Observability is first-class

The workflow leans hard on logging. The implementation agent instruments code with runtime logging —
inputs, actions, outputs, errors — so a human can *see* it work, and so that when something breaks,
the logs are the agent's debugging context rather than guesswork. It's an always-on ground rule and
baked into `setup-environment` and `tdd-task`.

## Test it (no Claude needed)

```bash
bash scripts/test_hakim.sh
```

Two shell processes round-trip a decision through the file — proving the handoff before any agent
is wired in.
