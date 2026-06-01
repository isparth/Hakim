#!/usr/bin/env bash
# hakim-teacher — bulletproof teacher terminal.
#
# Starts a Hakim teacher session and KEEPS IT ALIVE. Two layers of safety:
#   1. The session itself runs a watch -> teach -> resolve loop and is told never
#      to stop on its own.
#   2. This supervisor restarts the session if it ever exits anyway (crash,
#      accidental quit, context reset).
#
# Run it FROM your project folder — the same folder the work terminal is in — so it
# shares that project's .hakim/ handoff file:
#
#     bash /path/to/hakim/scripts/hakim-teacher.sh
#
# Press Ctrl-C to stop the supervisor (otherwise it will keep relaunching).
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HAKIM_PY="$SCRIPT_DIR/hakim.py"

if ! command -v claude >/dev/null 2>&1; then
  echo "[hakim] Claude Code ('claude') is not on your PATH. Install it first." >&2
  exit 1
fi
if [ ! -f "$HAKIM_PY" ]; then
  echo "[hakim] cannot find hakim.py at: $HAKIM_PY" >&2
  exit 1
fi

# The absolute path is baked into the prompt so the teacher session doesn't depend
# on ${CLAUDE_PLUGIN_ROOT} being set in its shell — it just works.
PROMPT="You are the Hakim TEACHER terminal — a permanent listener that runs forever.

The Hakim CLI for this session is exactly:  python3 \"$HAKIM_PY\"
Use that for every hakim command (watch, resolve, note).

Loop, and never stop on your own:
1. Run:  python3 \"$HAKIM_PY\" watch
   It BLOCKS until the work terminal hands off a decision, then prints it as JSON.
2. Teach that decision with the teach-decision skill: the honest two-tier lesson, then
   hand the decision back to the user to decide.
3. Record it:  python3 \"$HAKIM_PY\" resolve <id> ...  and write the note with
   python3 \"$HAKIM_PY\" note ...  (payload shapes are in the teach-decision skill).
4. Go straight back to step 1. Never end your turn. If watch errors, just run it again.

Start now: tell the user you are listening, then run watch."

echo "[hakim] teacher supervisor started in: $(pwd)"
echo "[hakim] handoff file: $(pwd)/.hakim/decisions.jsonl"
echo "[hakim] Ctrl-C to stop."
while true; do
  claude "$PROMPT"
  echo "[hakim] teacher session ended — restarting in 2s (Ctrl-C now to stop)…"
  sleep 2
done
