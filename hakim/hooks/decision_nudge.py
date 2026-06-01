#!/usr/bin/env python3
"""Safety-net nudge: a PreToolUse hook that reminds the work agent to hand off a
foundational decision *before* it lays down the file that bakes it in.

Fires only when *creating* (not editing) a file that usually encodes a tech decision —
dependency manifests, schemas, infra. Non-blocking: it only injects a reminder. The agent
is still the real detector (see the request-decision skill); this just catches misses.
"""

import json
import os
import re
import sys

SIGNAL = re.compile(
    r"(^|/)("
    r"package\.json|requirements\.txt|pyproject\.toml|go\.mod|Cargo\.toml|Gemfile|"
    r"composer\.json|Dockerfile|docker-compose\.ya?ml|next\.config\.[jt]s|"
    r"vite\.config\.[jt]s|prisma/schema\.prisma|schema\.sql|.*\.tf"
    r")$"
)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path") or ""
    if not path or not SIGNAL.search(path):
        return 0
    if os.path.exists(path):
        return 0  # editing an existing foundational file — likely settled; stay quiet

    msg = (
        f"Hakim: you're about to create `{os.path.basename(path)}`, which usually bakes in a "
        "foundational tech decision (stack, dependencies, database, infra). If there's a real "
        "'which X should we use?' fork here, use the request-decision skill to hand it to the "
        "teacher terminal before committing to it. If it's already settled, ignore this."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": msg,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
