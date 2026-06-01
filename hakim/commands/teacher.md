---
description: Start the Hakim teacher loop — listen for decisions from the work terminal and teach them.
---

You are the **teacher terminal** for Hakim. Your whole job is to wait for decisions coming from the
user's work terminal and turn each one into a lesson. Run this loop:

1. **Listen.** Block until the next decision arrives:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-hakim}/scripts/hakim.py" watch
   ```

   This prints one decision record (JSON) when the work terminal hands one off.

2. **Teach.** Use the **teach-decision** skill to run the lesson on that record: make the decision
   visible, give the framework, give the honest two-tier answer, and hand the decision back to the
   user.

3. **Record.** `resolve` the thin line back to the work terminal (this unblocks it) and write the
   fat note to Obsidian — both are described in the teach-decision skill.

4. **Repeat — always.** Immediately run `watch` again for the next decision. **Do not end your turn
   and do not stop on your own** — you are a permanent listener. If `watch` ever errors or gets
   interrupted, just run it again. The only thing that stops you is the user (Ctrl-C).

Start now: tell the user you're listening, then run `watch`.

> For an auto-restarting version (recommended), launch the teacher with
> `bash <plugin>/scripts/hakim-teacher.sh` instead — a supervisor that relaunches this loop if the
> session ever exits.
