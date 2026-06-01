---
name: grill-tech
description: Use to stress-test the TECHNICAL side of a plan — stack, architecture, data models, API contracts, tradeoffs — by interviewing the user relentlessly until you both reach shared understanding. Use during tech-decisions, tech changes mid-build, or any time a technical approach is fuzzy and needs aligning before moving on. Trigger when the user says "grill me on the tech", "stress-test this design", "poke holes in this architecture", or whenever technical doubts need clearing.
---

# grill-tech

Interview the user relentlessly about every aspect of the **technical** plan until you reach genuine
shared understanding. Walk down each branch of the design tree, resolving dependencies between
decisions one by one.

- Ask the questions **one at a time**.
- For each question, **provide your recommended answer** — take a position, don't just interrogate.
- If a question can be answered by reading the code or `technical_decisions.md`, **go look instead of
  asking**.

Focus on the technical design:
- Why this stack? What's the honest tradeoff against the alternative?
- Where does the data live, and how is it shaped? What changes as the product grows?
- How do the pieces talk to each other (the contracts)?
- What's the blast radius of each choice — what breaks if it's wrong, and how hard is it to undo?
- What could go wrong: failure modes, edge cases, scale, security?

Keep going until the doubts are gone and you and the user are aligned. This is the mechanism for
clearing confusion before a technical decision is locked — reach for it throughout the project, not
just at the start.
