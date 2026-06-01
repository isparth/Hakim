---
name: request-decision
description: Use the moment you are about to make a consequential, hard-to-reverse engineering decision while building — choosing a database, backend/frontend language, framework, architecture pattern, auth approach, or hosting/deploy target. Instead of silently picking one, hand the decision to the teacher terminal so the user learns and decides. Trigger on any "which X should we use?" fork that the rest of the project gets built on top of.
---

# request-decision (work terminal)

You are the **work** agent. When you reach a real decision, you do **not** pick it yourself and
move on. You hand it off, the user learns and decides in their teacher terminal, and you continue
with the one-line conclusion. This keeps your context clean — the messy debate never lands here.

The helper script is invoked as (works installed-as-plugin or from the repo root):

```
python3 "${CLAUDE_PLUGIN_ROOT:-hakim}/scripts/hakim.py" <command> ...
```

## Step 1 — Rate the stakes

Ask two questions:
- **How hard is this to undo later?**
- **How much of the project gets built on top of it?**

- **HIGH** — hard to undo *and* foundational (database, language, framework, architecture, auth,
  hosting). → you will **wait**.
- **LOW** — easy to swap later or localized to one feature (a helper library, a file layout, a
  name). → you will **not wait**; log it and keep going.

If genuinely unsure, treat it as HIGH. Better to pause once too often than build on an
unexamined foundation.

## Step 2 — Write the decision record

Build a JSON object with these fields (keep `project` to one line — don't dump history):

```json
{
  "project": "one-line: what's being built + that the owner is learning",
  "decision": "the actual question, e.g. 'Which database for users + recipes?'",
  "options": [
    { "name": "Postgres", "note": "short, honest one-liner" },
    { "name": "MongoDB",  "note": "short, honest one-liner" }
  ],
  "leaning": { "choice": "your honest tentative pick", "why": "one line" },
  "stakes": "high",
  "trigger": "what you were about to do, e.g. 'about to write db/schema.sql'"
}
```

`leaning` matters most — it's what lets the teacher give the user the two-tier answer
("right for now, here's the grown-up version"). Be honest, not diplomatic.

## Step 3 — Send it

Pipe the record via stdin (heredoc) so apostrophes and quotes are safe:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-hakim}/scripts/hakim.py" request --payload - <<'JSON'
{ ...the decision record... }
JSON
```

This prints a decision id like `dec_a1b2`. Keep it.

## Step 4 — Wait or keep going (the one knob)

**HIGH stakes → wait.** First tell the user in chat, plainly:

> I've hit a real decision here — *which database to use*. I've sent it to your **teacher
> terminal**. Head over there to think it through and decide; I'll pick up the moment you do.

Then block on it. Run this with the Bash tool's **timeout set to its max (`600000` ms ≈ 10 min)** so
the wait window isn't cut short:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-hakim}/scripts/hakim.py" wait dec_a1b2 --timeout 570
```

One of two things comes back:

- **The choice** — a JSON line, e.g.
  `{"choice":"Postgres","why":"data has clear links","future_note":"replicas later — overkill now"}`
  → go to Step 5.
- **`hakim: timed out waiting for resolution of dec_a1b2`** (exit code 2) → the user simply hasn't
  decided yet. Tell them plainly you're still holding for the teacher terminal, then **run the exact
  same `wait` command again.** Repeat for as long as it takes.

**Never stop waiting on your own.** The bounded `--timeout` is *only* there so a single Bash call
stays under Claude Code's ~10-minute cap — without it, a longer lesson gets killed mid-wait and
surfaces as an error. So if you ever see a raw error instead of the clean timeout message, treat it
the same way: just run the `wait` again. Only the user resolving the decision (or ending the
session) ends the wait.

**LOW stakes → don't wait.** You've already logged it with `request`. Proceed with your
`leaning`. The teacher may turn it into a relaxed lesson later; you don't block.

## Step 5 — Take the conclusion and move on

When the line comes back, state the choice in **one sentence** and continue building:

> Using **Postgres** — the data has clear links between users, recipes, and ingredients.

Then keep going. **Do not** re-open the debate, re-list the options, or re-justify at length.
The decision is settled. Re-deriving it is exactly the context bloat this system exists to prevent.

## Notes
- One decision at a time. Don't batch several `request`s and wait on all of them.
- If `wait` returns a timeout message instead of a choice, the user hasn't decided yet — tell
  them you're still waiting on the teacher terminal, then wait again.
