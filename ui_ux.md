# UI/UX — Feature Requirements (v1)

Feature-level only. *What* the interface must do, not how it looks. Hakim is an Electron + React companion app running alongside Claude Code.

## Guiding constraints

- **Two interruption tiers, honored visually.** Blocking intercepts demand attention; lesson opportunities never steal it.
- **The user is looking at their terminal, not Hakim.** Hakim must pull them in when it matters and stay out of the way when it doesn't.
- **Hands the decision back, always.** No UI affordance ever lets the user offload the choice to Hakim.

---

## Features

### 1. Decision Intercept (blocking)
The core moment. Triggered when a high-consequence decision is detected.
- Surfaces the decision in plain language ("You're about to pick a database").
- Asks **"What's your call, and why?"** — user states their choice *and* reasoning in their own words.
- An explicit **"I don't know — teach me"** path (never the default, never pre-selected).
- Cannot be dismissed/ignored to bypass the decision — the agent is paused until resolved.
- Clear signal that the agent is **paused/waiting** because of this.

### 2. Reveal & feedback
After the user commits to a call.
- Shows whether they were right and the tradeoffs underneath.
- For the "teach me" path: mini-lesson → then **bounces the decision back** ("Now what would you choose?") → feedback. The user still has to choose.

### 3. Two-tier explanation
Used in every reveal/lesson.
- Presents **both tiers clearly distinguished**: the right call *for this project now*, and what you'd reach for *in production at scale* (and why that's overkill here).
- Must read as two honest, separate answers — not one hedged blob.

### 4. Takeaway capture
Closes every decision/lesson.
- A field for the user to **write the takeaway in their own words** (not pre-filled, not optional to engage with).
- Saved to the knowledge base; confirms it was saved.

### 5. Lesson Opportunity (non-blocking)
Triggered when a teachable concept is nearby but no decision is being forced.
- A **non-blocking offer**: "Working on auth — want to learn how it works?" with **Skip / Surface-level / Go deep**.
- Must not pause the agent or steal focus; easy to ignore.
- Only appears for concepts not already in the knowledge base.

### 6. Quiz / spaced repetition
When a *known* concept resurfaces.
- A quick **gut-check quiz** instead of a lesson ("You learned queues a while back — quick check").
- Lightweight; gives feedback on the answer.

### 7. Knowledge base browser
The user's growing record.
- Browse/search concepts they've learned, with date and tags.
- View each note (in the user's own words).
- Reachable any time, not only during intercepts.

### 8. Notifications & presence
How Hakim reaches a user who's focused on the terminal.
- **Menu-bar/system-tray presence** showing Hakim is running.
- **System notification** to pull the user into a blocking intercept.
- **Quieter notification** for non-blocking lesson offers.
- Clear **connection status**: is Hakim attached to an active Claude Code session.

### 9. Settings
- **Auth:** inherit the user's local Claude Code auth (default) or enter a BYOK API key.
- Knowledge base location.
- Notification preferences (e.g. mute lesson offers).

### 10. First-run / onboarding
- Explain what Hakim does and the two interruption tiers.
- Confirm it's connected to Claude Code and auth is working.
- Keep it short — get to a working state fast.

---

## Explicitly out of scope (v1)

- Visual design, branding, layout, theming — this file is feature-level only.
- A full progress/analytics dashboard (P2 in the spec).
- In-app editing of the decision taxonomy.
