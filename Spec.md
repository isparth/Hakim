# Hakim — Product Spec

## Problem Statement

Developers using AI coding agents (Claude Code, Cursor, etc.) are getting code written for them but not learning from it. They accept whatever the agent produces, skip planning and review, and end up with codebases they can't reason about or maintain. The bottleneck has shifted from writing code to making good decisions — but nothing in their current toolset trains that judgment. Beginners in particular have no way to tell whether what the agent gave them is good or garbage.

---

## Goals

1. Users make better engineering decisions on their own projects after using Hakim — not just during a session.
2. Users internalize a structured development workflow (plan → test → implement → review) as a habit, not just as knowledge.
3. Hakim never re-teaches a concept the user has already encountered.
4. Users always make the final call — Hakim never decides for them.

---

## Non-Goals

- **Not a replacement for Claude Code / Cursor.** Hakim doesn't write code. It runs alongside the tools the user already has.
- **Not a course or curriculum.** There is no syllabus. Hakim teaches concepts just-in-time, triggered by the user's own project.
- **Not a passive chatbot.** Users can't ask "explain X" and receive a lecture — every lesson ends with the decision bounced back.
- **Not for experienced engineers.** Hakim is explicitly designed for people who are still learning judgment, not people who already have it.

---

## User Stories

**Decision Intercept**
- As a beginner developer building a side project, I want Hakim to catch the moments when a consequential decision is being made, so I'm forced to think about it instead of letting the agent decide for me.
- As a developer who doesn't know enough to make a call, I want a just-in-time lesson in the context of my actual project, so I can learn the concept and still make the decision myself.
- As a developer who just made a call, I want to know whether I was right and why, so I actually learn from the moment instead of just moving on.

**Two-Tier Decisions**
- As a beginner developer, I want to know both the right choice for my project *right now* and what a senior engineer would do in production, so I build real judgment without being overwhelmed or misled.

**Lesson Opportunities**
- As a developer working on auth (or any teachable concept), I want Hakim to offer — not interrupt — a chance to learn how it works, so I can go deep when I have the energy and skip when I don't.

**Memory & Spaced Repetition**
- As a developer who has used Hakim over multiple sessions, I want my knowledge base to grow so that Hakim quizzes me on what I already know instead of re-teaching it from scratch.

**Workflow Habits**
- As a developer who tends to vibe-code, I want Hakim to guide me through a structured workflow — planning, breaking down tasks, testing, reviewing — so that it becomes habit over time, not just a one-off.

---

## Requirements

### Must-Have (P0)

**Decision Intercept**
- Hakim observes the coding agent session passively — it has full context of what's happening in Claude Code, Cursor, or equivalent without the user needing to connect or configure anything per project.
- Hakim detects consequential decisions by reading the session context and matching it against a **decision taxonomy file** — a maintained list of decision types grouped by how consequential they are (e.g. choosing a database > choosing a naming convention). Decisions below the threshold are ignored.
- When a consequential decision appears in the user's project, Hakim intercepts and asks: *"What's your call, and why?"*
- The user either answers or chooses *"I don't know — teach me."*
  - If they answer: Hakim reveals whether they were right and explains the tradeoffs underneath.
  - If they choose "teach me": Hakim gives a mini-lesson grounded in their specific project, then bounces the decision back. The user must still choose — there is no offloading the judgment.
- After the decision is made, the user writes the takeaway in their own words. This is saved to their knowledge base.
- Work resumes after the intercept completes.

**Two-Tier Decision Explanation**
- Every decision is explained at two levels: the right call for this project right now, and what a more experienced engineer would do in a production context — with an honest explanation of why the latter would be overkill here.

**Lesson Opportunity**
- When Hakim detects a teachable concept in the user's work but there is no decision to intercept, it offers — it does not interrupt: *"I see you're working on X — want to learn how it works? Skip / Surface-level / Go deep."*
- The user's workflow continues regardless of what they choose.
- Hakim only offers if the concept is not already in the user's knowledge base (novelty gate).

**Knowledge Base**
- A persistent record of what the user has learned, written in their own words, with date and tag.
- Hakim checks the knowledge base before offering a lesson — if the concept is already there, it does not offer the lesson again.
- When a known concept resurfaces in the user's project, Hakim quizzes instead of teaches: *"You learned X a while back — quick gut check before we move on."*

---

### Nice-to-Have (P1)

- **Workflow nudges.** Hakim recognizes when the user is skipping important steps (jumping straight to implementation without a plan, not writing tests) and surfaces a prompt — not a blocker — to encourage the structured workflow.
- **Decision history.** The user can browse past decisions: what they chose, what the right answer was, what tradeoff they were taught.
- **Lesson depth control.** For Lesson Opportunities, "surface-level" and "go deep" produce meaningfully different outputs — not just more or less text, but different framing (overview vs. mechanics).

---

### Future (P2)

- **Proactive spaced repetition.** Hakim resurfaces past concepts on a schedule, not just when they happen to appear again in the project.
- **Progress view.** The user can see their knowledge base growing — concepts learned, decisions made, patterns in where they consistently get things wrong.
- **Multi-project memory.** The knowledge base carries across projects, not just within one.

---

## Open Questions

| Question | Who needs to answer |
|---|---|
| How opinionated is Hakim when it reveals "the right answer"? Some decisions have a clear better choice; others are genuinely contextual. Where's the line between confident guidance and false certainty? Needs a dedicated session to work through. | Product |
