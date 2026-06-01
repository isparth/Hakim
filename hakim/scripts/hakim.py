#!/usr/bin/env python3
"""hakim — the handoff plumbing between the work terminal and the teacher terminal.

Everything crosses through one append-only file (default: .hakim/decisions.jsonl),
one JSON object per line. Nobody edits old lines; we only ever append.

Because a Claude session is not a daemon (it can't be *pushed* to), "waiting" here
just means blocking and polling the file every ~200ms until the line we want shows up.
No server, no daemon.

Commands
  request  --payload '<json>'      (work)    append a decision_request, print its id
  wait     <id> [--timeout S]      (work)    block until that id is resolved, print the line
  watch    [--timeout S]           (teacher) block until the next unhandled decision, print it
  resolve  <id> --payload '<json>' (teacher) append the decision_resolved line
  history  [--type T] [--limit N]  (either)  dump past records

A decision is "pending" until a decision_resolved with the same id exists. The teacher
loop is: watch -> teach -> resolve -> watch ... so each decision is handed out once.
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone

try:
    import fcntl  # POSIX only (macOS/Linux). Windows is not supported.
except ImportError:  # pragma: no cover
    fcntl = None

DEFAULT_FILE = os.path.join(".hakim", "decisions.jsonl")
DEFAULT_VAULT = os.path.join(".hakim", "notes")
REQUEST = "decision_request"
RESOLVED = "decision_resolved"


# ---------- helpers ----------

def load_config():
    path = os.environ.get("HAKIM_CONFIG") or os.path.join(".hakim", "config.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def get_file(args):
    return args.file or os.environ.get("HAKIM_FILE") or load_config().get("file") or DEFAULT_FILE


def get_vault(args):
    return (getattr(args, "vault", None) or os.environ.get("HAKIM_VAULT")
            or load_config().get("obsidian_vault") or DEFAULT_VAULT)


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower().strip()).strip("-")
    return s or "note"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gen_id():
    return "dec_" + uuid.uuid4().hex[:6]


def parse_payload(s):
    if s == "-":  # read from stdin, so callers can heredoc and skip shell-escaping
        s = sys.stdin.read()
    try:
        obj = json.loads(s)
    except json.JSONDecodeError as e:
        sys.exit(f"hakim: invalid --payload JSON: {e}")
    if not isinstance(obj, dict):
        sys.exit("hakim: --payload must be a JSON object")
    return obj


def read_records(path):
    """Return parsed records in file order. Skips blank/partial/corrupt lines."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # a half-written line from a concurrent append; ignore
    return out


def append_record(path, obj):
    """Append one JSON line, locked so concurrent writers don't interleave."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    line = json.dumps(obj, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        if fcntl is not None:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            if fcntl is not None:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def poll_until(fn, timeout, poll_ms):
    """Call fn() until it returns non-None or we time out. None timeout = forever."""
    deadline = None if not timeout else time.monotonic() + timeout
    while True:
        res = fn()
        if res is not None:
            return res
        if deadline is not None and time.monotonic() >= deadline:
            return None
        time.sleep(poll_ms / 1000.0)


# ---------- commands ----------

def cmd_request(args):
    path = get_file(args)
    obj = parse_payload(args.payload)
    obj["type"] = REQUEST
    obj.setdefault("id", gen_id())
    obj.setdefault("ts", now_iso())
    append_record(path, obj)
    print(obj["id"])
    return 0


def cmd_wait(args):
    path = get_file(args)

    def check():
        for o in read_records(path):
            if o.get("type") == RESOLVED and o.get("id") == args.id:
                return o
        return None

    res = poll_until(check, args.timeout, args.poll_ms)
    if res is None:
        print(f"hakim: timed out waiting for resolution of {args.id}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False))
    return 0


def cmd_watch(args):
    path = get_file(args)

    def check():
        records = read_records(path)
        resolved = {o.get("id") for o in records if o.get("type") == RESOLVED}
        for o in records:
            if o.get("type") == REQUEST and o.get("id") not in resolved:
                return o  # oldest pending decision first
        return None

    res = poll_until(check, args.timeout, args.poll_ms)
    if res is None:
        print("hakim: timed out waiting for a decision", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False))
    return 0


def cmd_resolve(args):
    path = get_file(args)
    obj = parse_payload(args.payload)
    obj["type"] = RESOLVED
    obj["id"] = args.id
    obj.setdefault("ts", now_iso())
    append_record(path, obj)
    print(f"resolved {args.id}")
    return 0


def cmd_note(args):
    obj = parse_payload(args.payload)
    vault = get_vault(args)
    os.makedirs(vault, exist_ok=True)
    title = obj.get("title") or obj.get("concept") or "note"
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base = f"{date}-{slugify(title)}"
    path = os.path.join(vault, base + ".md")
    if os.path.exists(path):  # don't clobber a same-day note on the same topic
        path = os.path.join(vault, f"{base}-{uuid.uuid4().hex[:4]}.md")

    tags = obj.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]

    lines = ["---", f"date: {date}"]
    if obj.get("concept"):
        lines.append(f"concept: {obj['concept']}")
    lines.append("tags: [" + ", ".join(str(t) for t in tags) + "]")
    lines += ["---", "", f"# {title}", ""]
    if obj.get("decision"):
        lines += [f"**Decision:** {obj['decision']}", ""]
    if obj.get("in_their_words"):
        lines += ["## In my own words", obj["in_their_words"], ""]
    if obj.get("two_tier"):
        lines += ["## For now vs. the grown-up version", obj["two_tier"], ""]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(path)
    return 0


def cmd_history(args):
    path = get_file(args)
    records = read_records(path)
    if args.type:
        records = [o for o in records if o.get("type") == args.type]
    if args.limit:
        records = records[-args.limit:]
    for o in records:
        print(json.dumps(o, ensure_ascii=False))
    return 0


# ---------- argparse ----------

def build_parser():
    p = argparse.ArgumentParser(prog="hakim", description="Hakim decision handoff plumbing.")
    p.add_argument("--file", help="handoff file (default: .hakim/decisions.jsonl, or $HAKIM_FILE)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_wait_opts(sp):
        sp.add_argument("--timeout", type=float, default=None, help="seconds to wait (default: forever)")
        sp.add_argument("--poll-ms", dest="poll_ms", type=int, default=200, help="poll interval ms")

    sp = sub.add_parser("request", help="append a decision_request, print its id")
    sp.add_argument("--payload", required=True, help="decision record as JSON object")
    sp.set_defaults(func=cmd_request)

    sp = sub.add_parser("wait", help="block until <id> is resolved, print the line")
    sp.add_argument("id")
    add_wait_opts(sp)
    sp.set_defaults(func=cmd_wait)

    sp = sub.add_parser("watch", help="block until the next unhandled decision, print it")
    add_wait_opts(sp)
    sp.set_defaults(func=cmd_watch)

    sp = sub.add_parser("resolve", help="append the decision_resolved line for <id>")
    sp.add_argument("id")
    sp.add_argument("--payload", required=True, help="resolution as JSON object (choice, why, future_note)")
    sp.set_defaults(func=cmd_resolve)

    sp = sub.add_parser("note", help="write a dated, tagged markdown note to the Obsidian vault")
    sp.add_argument("--payload", required=True, help="note as JSON (title, concept, decision, in_their_words, two_tier, tags)")
    sp.add_argument("--vault", help="vault dir (default: $HAKIM_VAULT, config obsidian_vault, or .hakim/notes)")
    sp.set_defaults(func=cmd_note)

    sp = sub.add_parser("history", help="dump past records")
    sp.add_argument("--type", help="filter by type (decision_request / decision_resolved)")
    sp.add_argument("--limit", type=int, help="only the last N records")
    sp.set_defaults(func=cmd_history)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
