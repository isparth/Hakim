# Product Brief — Working Draft

## One-liner
A companion that teaches beginner-to-intermediate developers how to make good engineering decisions while they build something — by catching the real decisions in their own project and making them reason through them, instead of lecturing concepts in the abstract.

## The core thesis
In the AI era, the bottleneck has moved from writing syntax to making good decisions: knowing what to ask the agent for, decomposing a vague task into pieces it can nail, and being able to tell whether what came back is good or garbage. Syntax (how to write a for-loop in Go) no longer matters much. Judgment matters. This product trains judgment.

The deeper principle: concepts are the precondition for judgment, not a substitute for it. You can't choose between a message queue and a cron job if you've never heard of either — awareness lets you see that a decision exists. But knowing the definition isn't the same as reaching for the right tool at the right moment. So we teach concepts as ammunition for decisions, just-in-time, never as a syllabus to march through.

## The deeper goal: instilling a professional workflow
Beyond individual decisions and concepts, the product's real ambition is to change how the developer works — not just what they know. Most beginners (and many intermediates) vibe-code: one-shot the agent, accept whatever comes back, skip planning and tests and review. The result is a mess they can't maintain or reason about.

This product walks the developer through a structured development workflow — plan, break down tasks, implement with tests, review — and makes them do it, repeatedly, until it becomes habit. The workflow itself is the highest-leverage lesson: a developer who has internalised planned, tested, reviewed loops has already closed most of the gap to a competent engineer. Everything else — the concepts, the decisions, the tradeoffs — hangs off that spine.

The goal is not just a developer who knows more. It's a developer who works differently.

## Who it's for
People who want to learn — explicitly not people who already know. Beginners through junior/intermediate developers. They are happy to go slower in exchange for getting good. The canonical user: a smart non-engineer (e.g. a consultant) who wants to learn engineering by building something real on the side, who has correctly decided syntax memorization is pointless.

## What it is NOT
- Not the opportunistic 30-second "fill the idle time while the agent runs" companion. (You don't learn anything in 30 seconds.)
- Not a passive explainer / lecture machine. ("Just ask Claude to explain" already exists and is free.)
- Not a tool that makes decisions for you. It always hands the decision back.

## The two core teaching moments

### 1. The Decision Intercept (mandatory — a choice is being made)
When the agent is about to make a consequential decision (tech stack, database, architecture), the workflow pauses and runs this loop:

```
Decision appears
   → "What's your call, and why?"  (in your own words)
       → User chooses
           → Reveal: were they right? + the tradeoffs underneath
       → OR user hits "I don't know — teach me"
           → Mini-lesson (concrete, in the context of THEIR project)
           → Bounce the decision back: "Now what would you choose?"
           → Feedback
   → Capture: user writes the takeaway in their own words → saved to knowledge base
   → Resume building
```

The "I don't know" escape hatch never lets the user offload the judgment — the worst case is "learn the thing, then you still have to choose."

### 2. The Lesson Opportunity (invitational — no fork, just a teachable concept nearby)
When the agent is touching a teachable concept (e.g. auth) but there's no decision to resolve, the workflow offers — it doesn't interrupt:

> "I see you're working on auth — want to learn how it works? Skip / Surface-level / Go deep"

The work continues regardless; the lesson is opt-in, and the user picks the depth in the moment.

The bar for offering a lesson (so it doesn't become a nagging paperclip): the primary gate is novelty against the knowledge base — only offer if we haven't already taught it. (Cheapest, most powerful filter, and it reuses the memory system. Importance and project-centrality can layer on later.)

## The signature feature: two-tier decisions
Every decision is taught in two tiers, honest in both directions:

> "For this side project, Supabase is genuinely the right call — fast, handles the hard parts for you. But if you were building this in production at scale, you'd reach for X instead, and here's why — that'd be overkill here and slow you down."

Why this is the heart of the product: real engineering advice sounds insane for a weekend project (no one needs read replicas for their todo app). Telling a beginner the "grown-up" version without the "for now" version makes them quit. Doing both respects where they are and installs the senior mental model. Possible tagline: **learn the shortcut and the real thing, every time.**

## The memory layer (the defensibility)
Knowledge-base integration (Obsidian or similar) gives the product memory the raw agent structurally cannot have. This is the moat — "just ask Claude" can't do it:

- Never re-teach the same concept twice.
- Notes are written in the user's own words, dated, tagged.
- When a known concept resurfaces, quiz instead of teach (spaced repetition): "You learned queues a while back — quick gut check before we move on."
