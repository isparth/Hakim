#!/usr/bin/env bash
# Round-trips the handoff with no Claude involved: two shell processes, one file.
# Run: bash hakim/scripts/test_hakim.sh
set -u

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="python3 $DIR/hakim.py"
TMP="$(mktemp -d)"
export HAKIM_FILE="$TMP/decisions.jsonl"
trap 'rm -rf "$TMP"' EXIT

PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); echo "  ok   - $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL - $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }

echo "1) request prints an id and lands in history"
id="$($PY request --payload '{"decision":"db?","stakes":"high"}')"
check "id has dec_ prefix"            "[[ '$id' == dec_* ]]"
check "request is in history"          "$PY history --type decision_request | grep -q 'db?'"

echo "2) wait blocks, then unblocks when resolve lands (the handoff)"
( $PY wait "$id" --timeout 5 > "$TMP/wait.out"; echo $? > "$TMP/wait.rc" ) &
wpid=$!
sleep 0.3
$PY resolve "$id" --payload '{"choice":"Postgres","why":"links","future_note":"replicas later"}' >/dev/null
wait $wpid
check "wait exited 0"                  "[[ \"\$(cat "$TMP/wait.rc")\" == 0 ]]"
check "wait returned the choice"        "grep -q Postgres '$TMP/wait.out'"
check "wait returned future_note"       "grep -q 'replicas later' '$TMP/wait.out'"

echo "3) watch returns the next unhandled decision (skips the resolved one)"
( $PY watch --timeout 5 > "$TMP/watch.out"; echo $? > "$TMP/watch.rc" ) &
sleep 0.3
id2="$($PY request --payload '{"decision":"which auth?","stakes":"low"}')"
wait
check "watch exited 0"                  "[[ \"\$(cat "$TMP/watch.rc")\" == 0 ]]"
check "watch returned the new decision" "grep -q 'which auth?' '$TMP/watch.out'"
check "watch skipped the resolved one"  "! grep -q 'db?' '$TMP/watch.out'"

echo "4) wait times out (exit 2) when nothing resolves"
$PY wait dec_nope --timeout 1 2>/dev/null; rc=$?
check "wait timed out with code 2"      "[[ $rc == 2 ]]"

echo "5) concurrent appends from 10 processes all land, no corruption"
for i in $(seq 1 10); do $PY request --payload "{\"decision\":\"d$i\"}" >/dev/null & done
wait
n="$($PY history --type decision_request | wc -l | tr -d ' ')"
# 1 (db?) + 1 (auth?) + 10 = 12
check "all 12 requests present"         "[[ $n == 12 ]]"

echo "6) --payload - reads stdin (heredoc), survives apostrophes"
id3="$($PY request --payload - <<'JSON'
{"decision":"queue or cron?","why":"you'll need retries","stakes":"high"}
JSON
)"
check "stdin request landed"            "$PY history | grep -q \"you'll need retries\""
check "stdin request got an id"         "[[ '$id3' == dec_* ]]"

echo "7) note writes a dated, tagged markdown file to the vault"
notepath="$($PY note --vault "$TMP/vault" --payload - <<'JSON'
{"title":"Databases: relational vs document","concept":"database","decision":"Chose Postgres","in_their_words":"my data has clear links","two_tier":"for-now Postgres; grown-up read replicas","tags":["database","decision"]}
JSON
)"
check "note file was created"           "[[ -f '$notepath' ]]"
check "note filename is dated"          "[[ \"\$(basename '$notepath')\" == 20*-databases-relational-vs-document.md ]]"
check "note has the user's words"       "grep -q 'clear links' '$notepath'"
check "note has tags frontmatter"       "grep -q 'tags: \[database, decision\]' '$notepath'"

echo
echo "PASS=$PASS FAIL=$FAIL"
[[ $FAIL == 0 ]]
