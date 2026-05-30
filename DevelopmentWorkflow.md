# Development Workflow (for working with an AI coding agent)

A step-by-step process for taking an idea from research through to a tested, implemented product — built specifically for a **human-in-the-loop** workflow with an AI coding agent.

> **Core principle:** The agent does the work; the human approves at every gate. The agent never advances to the next step on its own say-so. Nothing is "done" because the agent says so — it's done because a human verified it.

---

## Ground Rules (set up once, apply throughout)

These are always-on. They sit underneath every phase below.

- **Rules / conventions file.** Maintain a `CLAUDE.md` (or `.cursorrules` / equivalent) the agent reads every session: code style, naming, file structure, allowed libraries, lint/format commands, how to run tests, and hard "never do X" rules.
- **Independent strict review.** Code is reviewed by a **separate, strict review agent** — never the agent that wrote it. Self-review by the author agent doesn't count.
- **Git discipline.** Commit after every completed-and-verified task. Branch per milestone. This is your undo button when the agent makes a mess.
- **Logging & observability.** Heavy logging to the terminal throughout — print what happens at each step. This is what lets a human *see* that things actually work (e.g. confirm a row landed in the database), not just trust the agent.
- **Scope lock.** Each task means *"do exactly this task, nothing more."* No unrequested features, no drive-by refactors, no scope creep.
- **Pin dependencies & versions.** Lock versions in the tech-decisions doc. The agent must check the actual installed version before using an API — agents hallucinate APIs and assume versions that don't exist.
- **Security basics.** No hardcoded secrets, env vars for keys, never commit secrets.
- **Least privilege for the agent.** Give the agent the minimum access it needs — read-only or scoped where possible. It should **not** hold unsupervised production credentials or the ability to run irreversible actions (deploys, migrations, deletes) without a human pulling the trigger.
- **When stuck or uncertain → stop and ask.** The agent surfaces blockers and questions instead of guessing. Use a **grill-me session** for this back-and-forth — it's the mechanism for syncing human and agent until there are no open doubts.
- **Re-orient each session.** Start every session by pointing the agent at the PRD, tech decisions, `tasks.md`, and the current milestone. Agents lose all memory between sessions.
- **Keep the 3 docs in sync.** PRD, tech decisions, and tasks must reflect any change in plan. Make updating them an explicit step — don't let them go stale.

---

## Phase 1 — Planning

Every step here ends with a **human gate**: the human pulls the final trigger.

### 1. Research
Research what you want to make.
- **Goal:** Decide what to build.
- **Human gate:** The human decides what to build — by nature, this is a human decision.

### 2. Create a PRD
Break the product down into features.
- Separate **core (MVP) features** from **additional features**.
- **Human gate:** The human reads the PRD in full, runs a **grill-me session** to clear any doubts the agent has, and gives a final sign-off that the PRD is good.

### 3. Make your technical decisions
Select your tech stack and capture it in a `tech_stack.md` or `technical_decisions.md` file.
- **Goal:** Lock in the high-level technical decisions, such as:
  - What framework for the frontend
  - What language for the backend
  - What external APIs to use
  - How to handle auth
  - What databases to use
- **Human gate:** Back-and-forth between human and agent (use **grill-me**) until the decisions are finalized. Human and agent must be fully synced — no lingering doubts — before the human signs off.

### 4. Set up your codebase / environment
Get the necessary downloads and dependencies installed (e.g. set up Next.js).
- Keep it simple: a `localhost:3000` "hello world" with a simple backend too. **Simplicity is key here.**
- **Goal:** A working environment where you can code — **and observe**. Frontend, backend, and database are wired together so that later you can *see* data flowing end-to-end (this is what makes milestone verification possible).
- **Human gate (light):** Human just verifies the frontend is up on `localhost:3000` and the backend/database are connected.

### 5. Create a `tasks.md` file
Using the PRD and technical docs, build out your task list. **This is important.**

- Organize tasks into **milestones**. Each milestone should have its integration tests defined up front, before you start the milestone (write them as scenarios / acceptance criteria first, then implement them as the interfaces come into existence).
- Each task should be **well-scoped and testable**.
- **Highlight confusion and key decisions** that are blocking a task.
- **Structure tasks by dependency** — e.g. Task 1 → Task 2, where each task may depend on the one before it.
- **Highlight tasks that can be worked on in parallel.**
- **Label tasks by type** — some are frontend, some are API, some are about getting an external API to work, etc. Try to label them.
- **Human gate:** Back-and-forth until the human finalizes the task breakdown.

---

## Phase 2 — Implementation (TDD)

Now we start implementing, following **Test-Driven Development (TDD)**, milestone by milestone.

Start with the first milestone. **First, define the milestone's integration tests** — write out the end-to-end scenarios and acceptance criteria that mark the milestone as done. *(Human reviews these.)*

Then, for each task, run the **red → green → review** loop:

1. **Create the tests** for the task. *(Human reviews the tests before implementation.)*
2. **Confirm red.** Run the tests and confirm they **fail first** — proving they actually test something.
3. **Implement** the task. Scope-locked: this task only.
4. **Confirm green.** A human or a separate process runs the tests — **not the agent's word for it.**
5. **Independent review.** The strict review agent reviews the implementation for code quality.
6. **Finish the task.** Human confirms, then commit (git discipline).

Repeat for every task until you reach the end of the milestone. Then:

7. **Implement and run the integration tests** you defined at the start.
8. **Manual QA — human in the loop.** The agent provides the human a concrete manual checklist to exercise the feature for real (e.g. *"register via Google sign-in, then confirm the new user appears in the database"*). Backed by the logging/observability from setup, the human can *see* it work end-to-end. Tests passing ≠ product working.
9. **Fix bugs and integration issues.** Resolve anything QA or the integration tests surface.
10. **Human sign-off**, commit the milestone, then move on to the next.

---

## Phase 3 — Deployment

Deployment is the **highest-blast-radius** phase, so it's where the agent gets the **least** autonomy. The agent does the automatable prep and monitoring; the human owns every irreversible action (the production deploy, database migrations, secrets/infra changes, and rollback decisions). One human is **accountable** for each release.

### 1. Build the pipeline (CI/CD)
Set up a multi-stage pipeline: **build → test → staging → production**.
- Use **Infrastructure as Code (IaC)** so environments are repeatable, and keep **staging as close to production as possible** to avoid config drift.
- The pipeline runs **mandatory automated quality gates** — fast unit tests first, then integration/E2E — and only promotes code that passes.
- Fold in **security scanning** (dependency checks, secret scanning, container scanning) as a gate, not an afterthought.
- **AI does:** draft the pipeline config, IaC, and gate definitions.
- **Human gate:** review and approve the pipeline before it's trusted to promote anything.

### 2. Deploy to staging
Ship the validated build to a production-like staging environment.
- **Goal:** final verification in a real environment before live users are involved.
- **AI does:** run the deploy to staging, then draft a **smoke-test checklist** for the human.
- **Human gate:** run the smoke tests / manual QA against staging (this is the same human-in-the-loop verification as the milestone QA — actually exercise the feature end-to-end, backed by logs).

### 3. Go / no-go for production
The decision to release to live users is a **human call**.
- **Decouple deploy from release** with **feature flags** where possible — ship code dark, then turn it on deliberately.
- Use **progressive rollout** (canary / staged %) to limit blast radius rather than flipping everything to 100% at once.
- **Human gate:** explicit go/no-go. The agent never self-promotes to production.

### 4. Release to production
Execute the release.
- **AI does:** prepare the release (artifacts, flag config, canary steps) and stage everything.
- **Human gate:** a human triggers the actual production deploy and any **database migrations** — these are irreversible and stay manual.

### 5. Monitor & observe
A deploy isn't done at "shipped" — it extends into production.
- Watch logs, metrics, error rates, and alerts after release. Have alerting wired to where the team will actually see it (e.g. Slack).
- **AI does:** monitor, watch the observability signals, and **surface anomalies** to the human.
- **Human gate:** the human interprets the signals and decides whether the release is healthy.

### 6. Rollback plan
Define rollback triggers **before** you deploy, not during an incident.
- Know in advance what conditions cause a rollback and how to do it (and keep the previous good build/commit ready — this is where your git discipline pays off).
- **AI does:** prepare and document the rollback procedure ahead of time.
- **Human gate:** the human makes the rollback call and pulls the trigger.

---

- **Use grill-me / grill-me-with-docs throughout** — for back-and-forth, syncing, and any time the agent (or you) has a doubt. When stuck, ask; don't guess.
- **Keep the 3 docs in sync.** Any change in plan or decision must be reflected in the PRD, tech decisions, and tasks. Update them as an explicit step — don't let them go stale.
