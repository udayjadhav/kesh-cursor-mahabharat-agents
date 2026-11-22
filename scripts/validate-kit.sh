#!/usr/bin/env bash
# Kesh kit integrity validator — enforcement level D for kit structure (not agent runtime behavior).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAILS=0
WARNS=0

fail() { echo "FAIL: $*"; FAILS=$((FAILS + 1)); }
warn() { echo "WARN: $*"; WARNS=$((WARNS + 1)); }
ok() { echo "OK: $*"; }

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           KESH KIT VALIDATOR                                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "Root: $ROOT"
echo ""

# --- Python checker (portable JSON/YAML-ish frontmatter) ---
python3 - <<'PY' || exit 1
import re, sys
from pathlib import Path

root = Path(".")
fails = 0
warns = 0

def fail(msg):
    global fails
    print(f"FAIL: {msg}")
    fails += 1

def warn(msg):
    global warns
    print(f"WARN: {msg}")
    warns += 1

def ok(msg):
    print(f"OK: {msg}")

def parse_frontmatter(text, path):
    if not text.startswith("---"):
        fail(f"{path}: missing YAML frontmatter")
        return None
    end = text.find("\n---", 3)
    if end < 0:
        fail(f"{path}: unclosed frontmatter")
        return None
    block = text[3:end].strip()
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data

# Roster agents that require model pins
ROSTER = {
    "kesh", "vidura", "sanjaya", "vyasa", "vishwakarma", "sarthi",
    "krishna", "money-lens", "decision-engine", "kripacharya",
    "parth", "swachalit", "sutradhar", "niti",
    "bhishma", "lakshman", "draupadi",
    "api-architect", "ai-product-engineer",
}
SUPPORT = {"kesh-context", "kesh-flows", "kesh-output", "kesh-rules"}

agents_dir = root / "agents"
agent_files = sorted(agents_dir.glob("*.md"))
if not agent_files:
    fail("no agents/*.md found")

names = {}
for path in agent_files:
    text = path.read_text(encoding="utf-8")
    data = parse_frontmatter(text, path)
    if data is None:
        continue
    name = data.get("name")
    if not name:
        fail(f"{path}: frontmatter missing name")
        continue
    if name in names:
        fail(f"duplicate agent name '{name}': {names[name]} and {path}")
    names[name] = str(path)
    desc = data.get("description")
    if not desc:
        fail(f"{path}: frontmatter missing description")
    stem = path.stem
    if stem in ROSTER:
        model = data.get("model")
        if not model:
            fail(f"{path}: roster agent missing model")
        elif stem == "parth" and "bhishma" in names:
            pass  # checked after loop
    elif stem in SUPPORT:
        if data.get("model"):
            warn(f"{path}: support module has model (usually inherit parent)")
    else:
        warn(f"{path}: unknown agent stem '{stem}' (not in roster/support lists)")

# Model diversity invariant
parth = agents_dir / "parth.md"
bhishma = agents_dir / "bhishma.md"
if parth.exists() and bhishma.exists():
    pd = parse_frontmatter(parth.read_text(encoding="utf-8"), parth) or {}
    bd = parse_frontmatter(bhishma.read_text(encoding="utf-8"), bhishma) or {}
    if pd.get("model") and bd.get("model") and pd.get("model") == bd.get("model"):
        fail(f"Parth and Bhishma share model '{pd.get('model')}' — invariant violated")
    else:
        ok(f"Parth model={pd.get('model')} ≠ Bhishma model={bd.get('model')}")

missing_roster = ROSTER - set(names)
if missing_roster:
    fail(f"missing roster agents: {sorted(missing_roster)}")
else:
    ok(f"all {len(ROSTER)} roster agents present")

missing_support = SUPPORT - set(names)
if missing_support:
    fail(f"missing support modules: {sorted(missing_support)}")
else:
    ok(f"all {len(SUPPORT)} support modules present")

# Rules frontmatter
rules_root = root / "rules"
rule_files = list(rules_root.rglob("*.mdc"))
if not rule_files:
    fail("no rules/**/*.mdc found")

spec = rules_root / "kesh-agent-spec.mdc"
if not spec.exists():
    fail("rules/kesh-agent-spec.mdc missing")
else:
    sd = parse_frontmatter(spec.read_text(encoding="utf-8"), spec) or {}
    ver = sd.get("version", "")
    if not ver.startswith("2."):
        fail(f"kesh-agent-spec version is '{ver}' (expected 2.x)")
    else:
        ok(f"kesh-agent-spec version {ver}")

for path in sorted(rule_files):
    text = path.read_text(encoding="utf-8")
    data = parse_frontmatter(text, path)
    if data is None:
        continue
    if "description" not in data:
        fail(f"{path}: missing description in frontmatter")
    rel = path.relative_to(rules_root)
    if str(rel).startswith("standards/"):
        if path.name.startswith("_"):
            continue  # templates
        aa = data.get("alwaysApply", "")
        if aa.lower() == "true":
            fail(f"{path}: standards modules must not be alwaysApply: true")
        if "globs" not in data and path.name not in ("README.md",):
            warn(f"{path}: standards module missing globs")

# External voice must have frontmatter (regression)
ext = rules_root / "kesh-external-output-voice.mdc"
if ext.exists():
    if not ext.read_text(encoding="utf-8").startswith("---"):
        fail("kesh-external-output-voice.mdc missing YAML frontmatter")
    else:
        ok("kesh-external-output-voice.mdc has frontmatter")

# teams.mdc must not be always-on in rules/
if (rules_root / "teams.mdc").exists():
    warn("rules/teams.mdc present — prefer optional/teams.mdc for public kit")

# Spec references to agents — soft check for `@` or agents/<name>
spec_text = spec.read_text(encoding="utf-8") if spec.exists() else ""
for agent in ROSTER:
    # presence of agent name as word is enough soft check
    if agent.replace("-", " ") not in spec_text.lower() and agent not in spec_text.lower():
        # money-lens might appear as Money Lens
        if agent == "money-lens" and "money lens" in spec_text.lower():
            continue
        if agent == "decision-engine" and "decision engine" in spec_text.lower():
            continue
        warn(f"spec may not mention agent '{agent}'")

# Knowledge + standards presence
std = list((rules_root / "standards").rglob("*.mdc")) if (rules_root / "standards").exists() else []
if len(std) < 10:
    fail(f"expected substantial standards tree, found {len(std)} files")
else:
    ok(f"standards modules: {len(std)} files")

know = list((root / "knowledge").glob("*.md")) if (root / "knowledge").exists() else []
if len(know) < 5:
    fail(f"expected knowledge modules, found {len(know)}")
else:
    ok(f"knowledge modules: {len(know)} markdown files")

# Knowledge discovery capability
disc_rule = rules_root / "kesh-knowledge-discovery.mdc"
if not disc_rule.exists():
    fail("rules/kesh-knowledge-discovery.mdc missing")
else:
    ok("kesh-knowledge-discovery.mdc present")

hum = rules_root / "kesh-human-communication.mdc"
if not hum.exists():
    fail("rules/kesh-human-communication.mdc missing")
else:
    ok("kesh-human-communication.mdc present")

cq = rules_root / "kesh-code-quality.mdc"
if not cq.exists():
    fail("rules/kesh-code-quality.mdc missing")
else:
    ok("kesh-code-quality.mdc present")

niti_rule = rules_root / "kesh-niti.mdc"
if not niti_rule.exists():
    fail("rules/kesh-niti.mdc missing")
else:
    ok("kesh-niti.mdc present")

niti_scripts = root / "scripts" / "niti" / "lib.py"
if not niti_scripts.exists():
    fail("scripts/niti/lib.py missing")
else:
    ok("scripts/niti present")

niti_agent = agents_dir / "niti.md"
nm = parse_frontmatter(niti_agent.read_text(encoding="utf-8"), niti_agent) or {}
if nm.get("model") != "claude-4-6-sonnet":
    fail(f"NITI model should be claude-4-6-sonnet, got {nm.get('model')}")
else:
    ok("NITI model=claude-4-6-sonnet (Tier A evaluation)")

for rel in (
    "rules/kesh-execution-modes.mdc",
    "rules/kesh-context-packaging.mdc",
    "rules/kesh-quality-guardrails.mdc",
    "scripts/modes/select_mode.py",
    "scripts/standards/select_standards.py",
    "scripts/context/package.py",
    "scripts/cache/lib.py",
    "benchmarks/token-optimization/harness.py",
):
    if not (root / rel).exists():
        fail(f"token-opt missing: {rel}")
ok("token-optimization artifacts present")

for rel in (
    "agents/api-architect.md",
    "agents/ai-product-engineer.md",
    "skills/api-engineering/SKILL.md",
    "skills/data-engineering/SKILL.md",
    "skills/frontend-architecture/SKILL.md",
    "skills/workflow-architecture/SKILL.md",
    "skills/ai-engineering/SKILL.md",
    "skills/reliability-performance/SKILL.md",
    "skills/staff-engineering/SKILL.md",
    "scripts/skills/select_skills.py",
    "scripts/repo/profile.py",
    "scripts/adr/new.py",
    "scripts/quality/discover_tools.py",
    "optional/healthcare/README.md",
    "docs/kesh-2.0/STAFF-ENGINEER-EDITION.md",
):
    if not (root / rel).exists():
        fail(f"staff-edition missing: {rel}")
ok("staff-engineer-edition artifacts present")

# healthcare agent must NOT be in core agents/
if (agents_dir / "healthcare-domain.md").exists():
    fail("healthcare-domain.md must live under optional/healthcare/agents/, not agents/")
else:
    ok("healthcare-domain kept out of core agents/")

kd_skill = root / "skills" / "knowledge-discovery" / "SKILL.md"
if not kd_skill.exists():
    fail("skills/knowledge-discovery/SKILL.md missing")
else:
    ok("knowledge-discovery skill present")

tmpl = rules_root / "standards" / "_TEMPLATE.mdc"
if not tmpl.exists():
    fail("rules/standards/_TEMPLATE.mdc missing")
else:
    ok("standards template present")

manifest = root / "knowledge" / "manifest.json"
if not manifest.exists():
    fail("knowledge/manifest.json missing")
else:
    import json
    try:
        man = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(man.get("entries"), list) or len(man["entries"]) < 1:
            fail("manifest.json entries empty")
        else:
            ok(f"manifest.json entries: {len(man['entries'])}")
            for ent in man["entries"]:
                for mp in ent.get("mdc_paths", []):
                    if not (root / mp).exists():
                        fail(f"manifest mdc_path missing: {mp}")
    except Exception as e:
        fail(f"manifest.json invalid: {e}")

# install.sh exists and is executable-ish
inst = root / "install.sh"
if not inst.exists():
    fail("install.sh missing")
else:
    ok("install.sh present")

# Relative path references (mdc before md to avoid .md matching inside .mdc)
ref_re = re.compile(
    r"(?:(?:`|/)|(?<![A-Za-z0-9_./-]))"
    r"((?:agents|rules|docs|knowledge|hooks|scripts|optional|skills|tests)/"
    r"[A-Za-z0-9_./-]+\.(?:mdc|md|sh))"
)
skip_ref_files = {
    "docs/kesh-2.0/PHASE-1-BASELINE.md",
    "docs/kesh-2.0/PHASE-2-PLAN.md",
}
missing_refs = []
for path in list(root.rglob("*")):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix not in {".md", ".mdc", ".sh"}:
        continue
    rel = str(path.as_posix()).lstrip("./")
    if rel in skip_ref_files or rel == "scripts/validate-kit.sh":
        continue
    try:
        t = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for m in ref_re.finditer(t):
        target = m.group(1)
        # Skip URL path segments (e.g. https://cursor.com/docs/hooks.md)
        start = m.start(1)
        prefix = t[max(0, start - 12) : start]
        if "http://" in prefix or "https://" in prefix or "://" in prefix:
            continue
        if "my-repo" in target or "path/to" in target:
            continue
        # Install destination after INSTALL_TEAMS=1 — not shipped under rules/ in-repo
        if target == "rules/teams.mdc":
            continue
        if not (root / target).exists():
            missing_refs.append(f"{rel} -> {target}")
missing_refs = sorted(set(missing_refs))
if missing_refs:
    for item in missing_refs[:25]:
        fail(f"missing path ref: {item}")
    if len(missing_refs) > 25:
        fail(f"... and {len(missing_refs) - 25} more missing path refs")
else:
    ok("relative path references resolve")

# Forbidden company residue in public kit (soft)
# Skip this script and audit/plan docs that intentionally mention banned strings.
SKIP_RESIDUE = {
    "scripts/validate-kit.sh",
    "docs/kesh-2.0/PHASE-1-BASELINE.md",
    "docs/kesh-2.0/PHASE-2-PLAN.md",
}
NEEDLES = ("CertifyOS", "helpshift.com", "helpshift.atlassian")
residue = []
for path in list(root.rglob("*")):
    if not path.is_file():
        continue
    if ".git" in path.parts:
        continue
    # Optional org packs may contain employer names; keep them out of core scan
    if "optional" in path.parts and "healthcare" in path.parts:
        continue
    if path.suffix not in {".md", ".mdc", ".sh", ".json", ".yml", ".yaml"}:
        continue
    rel = str(path.as_posix()).lstrip("./")
    if rel in SKIP_RESIDUE or "PHASE-1-BASELINE" in path.name or "PHASE-2-PLAN" in path.name:
        continue
    try:
        t = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for needle in NEEDLES:
        if needle.lower() in t.lower():
            residue.append(f"{path}: contains '{needle}'")
if residue:
    for r in residue[:20]:
        fail(r)
else:
    ok("no CertifyOS/helpshift.com residue in scanned text files")

print("")
print(f"Summary: {fails} fail(s), {warns} warn(s)")
sys.exit(1 if fails else 0)
PY

EXIT=$?
if [[ $EXIT -eq 0 ]]; then
  echo ""
  echo "VALIDATOR PASSED"
else
  echo ""
  echo "VALIDATOR FAILED"
fi
exit "$EXIT"
