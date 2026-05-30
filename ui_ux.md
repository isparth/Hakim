# UI/UX — Look & Feel (v1)

How the interface should look and feel. Not a pixel spec — a description of the intended visual language and interaction feel. Hakim is an Electron + React companion to Claude Code.

## Overall feel

- **A calm dev-tool companion, not an app that shouts.** It should feel native beside a code editor and a terminal: quiet, focused, confident. The opposite of a gamified, badge-pushing study app and the opposite of a nagging paperclip.
- **Dark-mode first.** Editor-adjacent palette — deep neutral background, one restrained accent color, high-contrast text. Light mode is a secondary theme.
- **Mentor tone, visually.** Spacious, unhurried, lots of breathing room. Prose in a clean sans; anything code-ish (file names, commands, the decision itself) in monospace so it reads as "from your project."
- **Motion is subtle.** Gentle fades and slides, never bouncy or attention-grabbing for its own sake. Movement is reserved to signal the one thing that matters: the agent just paused.

## Form factor

Two surfaces:
1. **A menu-bar/tray presence** — a small icon always there. Calm when idle; a subtle accent dot when an intercept is waiting. Click for a compact dropdown: connection status, "open Hakim," quick mute.
2. **The main window** — a focused single-column app for intercepts and lessons, with the knowledge base living in a wider two-pane layout.

---

## The surfaces

### Decision Intercept (blocking) — center stage
The most important screen. When a high-consequence decision is caught, a **focused card window comes to the front** over a dimmed backdrop, so it's unmistakable the work has stopped.
- **Top:** a small, calm "⏸ Agent paused" marker in the accent color — present but not alarming.
- **Middle:** the decision stated in plain language, with the concrete project detail in monospace ("about to add **Supabase** as your database").
- **The prompt — "What's your call, and why?"** — a roomy text input that invites real sentences, not a one-word answer. Any preset choices sit as understated chips above it.
- **Bottom, deliberately quiet:** a plain-text **"I don't know — teach me"** link — visible, never a big button, never pre-selected. The visual weight pushes the user toward attempting their own call first.

### Reveal & feedback — same card, calm transition
After they commit, the card **transitions in place** (no new window) to the verdict.
- A clear but understated right/not-quite signal — a check or a gentle correction, never a red buzzer or a celebration.
- Below it, the tradeoffs, in readable prose.

### Two-tier explanation — visibly two answers
Whenever Hakim explains, the two tiers are **laid out as two distinct, side-by-side (or stacked) blocks**, clearly labeled — e.g. **"For this project, now"** (visually primary, full-strength) and **"At production scale"** (secondary, slightly muted, marked as the senior/future view). The split must be obvious at a glance so they never blur into one hedged paragraph.

### Takeaway capture — looks like a note
Closing every decision: a **lined, note-like text area** that visually echoes the knowledge base, signalling "this becomes your note." Empty by default — it should feel like *their* page, not a form. A small "saved to your knowledge base" confirmation after.

### Lesson Opportunity (non-blocking) — a quiet corner toast
The deliberate opposite of the intercept. A **small, low-contrast toast slides into a bottom corner**, never covering anything, never taking focus. One line ("Working on auth — want to learn how it works?") and three soft buttons: **Skip · Surface · Go deep**. Ignored cleanly if untouched; the terminal keeps running behind it.

### Quiz / spaced repetition — a light card
For a concept they already know: a **compact single-question card**, friendlier and lighter than an intercept. Quick to answer, with brief feedback. Reads as a check-in, not a test.

### Knowledge base — an Obsidian-like reading space
The wider, two-pane view:
- **Left:** a searchable list of concepts, each showing its tag(s) and date, newest or most-relevant first.
- **Right:** the selected note, rendered as clean readable Markdown — *their* words, lightly styled.
- The overall feel is a personal notebook that's visibly **growing**, not a database admin screen.

### Settings & onboarding — minimal and plain
- **Settings:** a short, plain list — auth (inherit Claude Code, or paste a key), knowledge-base location, notification/mute toggles. No sprawling preference panels.
- **First run:** a few calm steps that explain the two interruption styles, confirm the Claude Code connection is live, then get out of the way fast.

---

## Visual hierarchy principle

The whole look hangs off **one contrast**: the **blocking intercept owns the screen** (front-and-center card, dimmed world behind, the accent reserved for "paused"), while the **lesson offer is the smallest, quietest thing on screen** (corner, low-contrast, dismissible). A user should be able to tell which kind of moment it is from across the room, before reading a word.
