#!/usr/bin/env bash
# Runs kit validator + hook smoke checks. Exit non-zero on failure.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PASS=0
FAIL=0

assert_eq() {
  local name="$1" got="$2" want="$3"
  if [[ "$got" == "$want" ]]; then
    echo "PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $name (got='$got' want='$want')"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Kit validator ==="
chmod +x scripts/validate-kit.sh hooks/deny-destructive-shell.sh
if ./scripts/validate-kit.sh; then
  echo "PASS: validate-kit.sh"
  PASS=$((PASS + 1))
else
  echo "FAIL: validate-kit.sh"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Staff edition tests ==="
if python3 -m unittest discover -s tests/staff -p 'test_*.py' -v; then
  echo "PASS: staff edition unittest"
  PASS=$((PASS + 1))
else
  echo "FAIL: staff edition unittest"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Token optimization tests ==="
if python3 -m unittest discover -s tests/token -p 'test_*.py' -v; then
  echo "PASS: token optimization unittest"
  PASS=$((PASS + 1))
else
  echo "FAIL: token optimization unittest"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== NITI telemetry tests ==="
chmod +x hooks/niti-telemetry.sh hooks/niti-stop-trigger.sh 2>/dev/null || true
if python3 -m unittest discover -s tests/niti -p 'test_*.py' -v; then
  echo "PASS: niti telemetry unittest"
  PASS=$((PASS + 1))
else
  echo "FAIL: niti telemetry unittest"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Hook smoke tests ==="
HOOK=hooks/deny-destructive-shell.sh
chmod +x hooks/niti-telemetry.sh hooks/niti-stop-trigger.sh 2>/dev/null || true

perm_allow=$(echo '{"command":"ls -la"}' | KESH_HOOK_MODE=ask "$HOOK" | python3 -c 'import json,sys; print(json.load(sys.stdin)["permission"])')
assert_eq "allow innocent command" "$perm_allow" "allow"

perm_ask=$(echo '{"command":"git push --force origin main"}' | KESH_HOOK_MODE=ask "$HOOK" | python3 -c 'import json,sys; print(json.load(sys.stdin)["permission"])')
assert_eq "ask on force-push" "$perm_ask" "ask"

perm_deny=$(echo '{"command":"DROP TABLE users;"}' | KESH_HOOK_MODE=deny "$HOOK" | python3 -c 'import json,sys; print(json.load(sys.stdin)["permission"])')
assert_eq "deny on DROP TABLE when mode=deny" "$perm_deny" "deny"

perm_off=$(echo '{"command":"rm -rf /"}' | KESH_HOOK_MODE=off "$HOOK" | python3 -c 'import json,sys; print(json.load(sys.stdin)["permission"])')
assert_eq "off mode allows destructive" "$perm_off" "allow"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[[ "$FAIL" -eq 0 ]]
