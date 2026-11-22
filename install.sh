#!/usr/bin/env bash
# Kesh Cursor Kit 2.6 — installs agents, rules (incl. standards/), skills,
# core docs, and optionally knowledge modules / safety hooks into ~/.cursor
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURSOR_DIR="${CURSOR_DIR:-$HOME/.cursor}"
DRY_RUN="${DRY_RUN:-0}"
INSTALL_KNOWLEDGE="${INSTALL_KNOWLEDGE:-0}"
INSTALL_HOOKS="${INSTALL_HOOKS:-0}"
INSTALL_NITI="${INSTALL_NITI:-0}"
INSTALL_HEALTHCARE="${INSTALL_HEALTHCARE:-0}"
SKIP_CLOJURE="${SKIP_CLOJURE:-0}"
INSTALL_TEAMS="${INSTALL_TEAMS:-0}"
# Archive employer-only alwaysApply leftovers that are NOT part of this kit
# (they otherwise keep forcing old / company-specific behavior in every tab).
ARCHIVE_LOCAL_ONLY="${ARCHIVE_LOCAL_ONLY:-1}"

usage() {
  cat <<'EOF'
Kesh Cursor Kit installer (2.6)

Usage:
  ./install.sh                         Install agents, rules, skills, core docs
  CURSOR_DIR=/path ./install.sh        Custom Cursor config root
  DRY_RUN=1 ./install.sh               Show actions without copying
  INSTALL_KNOWLEDGE=1 ./install.sh     Also install knowledge/ → ~/.cursor/knowledge/kesh/
  INSTALL_HOOKS=1 ./install.sh         Also copy optional safety hooks (opt-in)
  INSTALL_NITI=1 ./install.sh          NITI scripts + telemetry hooks + ~/.cursor/niti layout
  INSTALL_HEALTHCARE=1 ./install.sh     Optional healthcare domain pack (not in public core)
  SKIP_CLOJURE=1 ./install.sh          Omit Clojure standards after copy
  INSTALL_TEAMS=1 ./install.sh         Copy optional/teams.mdc into rules/
  ARCHIVE_LOCAL_ONLY=0 ./install.sh    Keep employer-only rules already in ~/.cursor/rules

What gets installed by default:
  agents/*.md              →  $CURSOR_DIR/agents/
  rules/** (nested OK)     →  $CURSOR_DIR/rules/
  skills/*/SKILL.md        →  $CURSOR_DIR/skills/<name>/
  docs/*.md (core)         →  $CURSOR_DIR/knowledge/kesh/docs/
  scripts/{modes,standards,context,cache,skills,repo,adr,quality}

Existing destination dirs are backed up with a timestamp suffix before overwrite.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

count_files() {
  local dir="$1"
  local pattern="$2"
  if [[ ! -d "$dir" ]]; then
    echo 0
    return
  fi
  find "$dir" -type f -name "$pattern" 2>/dev/null | wc -l | tr -d ' '
}

AGENT_N="$(count_files "$SCRIPT_DIR/agents" '*.md')"
RULE_N="$(count_files "$SCRIPT_DIR/rules" '*.mdc')"
STD_N="$(count_files "$SCRIPT_DIR/rules/standards" '*.mdc')"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           KESH CURSOR KIT 2.6 — INSTALLER                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Target:             $CURSOR_DIR"
echo "Dry run:            $DRY_RUN"
echo "Install knowledge:  $INSTALL_KNOWLEDGE"
echo "Install hooks:      $INSTALL_HOOKS"
echo "Install NITI:       $INSTALL_NITI"
echo "Install healthcare pack: $INSTALL_HEALTHCARE"
echo "Skip Clojure:       $SKIP_CLOJURE"
echo "Install teams:      $INSTALL_TEAMS"
echo "Archive local-only: $ARCHIVE_LOCAL_ONLY"
echo "Agents:             $AGENT_N  |  Rules: $RULE_N (standards: $STD_N)"
echo ""

install_dir() {
  local src="$1"
  local dest="$2"
  local label="$3"

  if [[ ! -d "$src" ]]; then
    echo "  skip $label (missing: $src)"
    return
  fi

  mkdir -p "$dest"

  if [[ -n "$(ls -A "$dest" 2>/dev/null || true)" ]]; then
    local backup="${dest}-backup-$(date +%Y%m%d-%H%M%S)"
    echo "  backup $label → $backup"
    if [[ "$DRY_RUN" != "1" ]]; then
      cp -a "$dest" "$backup"
    fi
  fi

  echo "  install $label"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "    (dry-run) cp -a $src/. $dest/"
  else
    cp -a "$src/." "$dest/"
  fi
}

copy_file() {
  local src="$1"
  local dest="$2"
  local label="$3"
  if [[ ! -f "$src" ]]; then
    echo "  skip $label (missing: $src)"
    return
  fi
  echo "  install $label"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "    (dry-run) cp $src $dest"
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
  fi
}

if [[ "$DRY_RUN" != "1" ]]; then
  mkdir -p "$CURSOR_DIR"/{agents,rules,skills,scripts}
fi

install_dir "$SCRIPT_DIR/agents"       "$CURSOR_DIR/agents"       "agents ($AGENT_N files)"
install_dir "$SCRIPT_DIR/rules"        "$CURSOR_DIR/rules"        "rules ($RULE_N files, incl. standards/)"

# Install every skills/<name>/ directory that contains SKILL.md
if [[ -d "$SCRIPT_DIR/skills" ]]; then
  for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_name="$(basename "$skill_dir")"
    if [[ -f "$skill_dir/SKILL.md" ]]; then
      install_dir "$skill_dir" "$CURSOR_DIR/skills/$skill_name" "skills/$skill_name"
    fi
  done
fi

# Staff-edition helper scripts (modes/standards/context/cache already via NITI or separate)
for helper in skills repo adr quality modes standards context cache; do
  if [[ -d "$SCRIPT_DIR/scripts/$helper" ]]; then
    install_dir "$SCRIPT_DIR/scripts/$helper" "$CURSOR_DIR/scripts/$helper" "scripts/$helper"
  fi
done

if [[ "$INSTALL_KNOWLEDGE" == "1" ]]; then
  install_dir "$SCRIPT_DIR/knowledge" "$CURSOR_DIR/knowledge/kesh" "knowledge → knowledge/kesh"
  if [[ -d "$SCRIPT_DIR/optional/knowledge-cache" ]]; then
    install_dir "$SCRIPT_DIR/optional/knowledge-cache" "$CURSOR_DIR/knowledge/cache" "knowledge-cache schema notes"
  fi
fi

# Always publish human-readable kit docs AFTER knowledge so they are not clobbered.
publish_kit_docs() {
  if [[ ! -d "$SCRIPT_DIR/docs" ]]; then
    return
  fi
  if [[ "$DRY_RUN" != "1" ]]; then
    mkdir -p "$CURSOR_DIR/knowledge/kesh/docs"
  fi
  for doc in WORKFLOW.md ARCHITECTURE.md AGENTS.md SKILLS.md STANDARDS.md RULES.md INSTALL.md \
             KNOWLEDGE.md KNOWLEDGE-DISCOVERY.md; do
    if [[ -f "$SCRIPT_DIR/docs/$doc" ]]; then
      copy_file "$SCRIPT_DIR/docs/$doc" "$CURSOR_DIR/knowledge/kesh/docs/$doc" "docs/$doc"
    fi
  done
  if [[ -d "$SCRIPT_DIR/docs/kesh-2.0" ]]; then
    install_dir "$SCRIPT_DIR/docs/kesh-2.0" "$CURSOR_DIR/knowledge/kesh/docs/kesh-2.0" "docs/kesh-2.0"
  fi
  copy_file "$SCRIPT_DIR/README.md" "$CURSOR_DIR/knowledge/kesh/README.md" "kit README.md"
  copy_file "$SCRIPT_DIR/CHANGELOG.md" "$CURSOR_DIR/knowledge/kesh/CHANGELOG.md" "kit CHANGELOG.md"
}
publish_kit_docs

# Employer / legacy files that live in ~/.cursor/rules but are NOT shipped by this kit
# keep forcing old alwaysApply behavior across every tab. Move them aside (recoverable).
if [[ "$ARCHIVE_LOCAL_ONLY" == "1" ]]; then
  archive_dir="$CURSOR_DIR/rules-archived-local-only-$(date +%Y%m%d-%H%M%S)"
  archived=0
  for leftover in \
      helpshift-architecture-knowledge.mdc \
      helpshift-simple-language.mdc \
      teams.mdc \
      clojure-daily-tips.mdc \
      clojure-review.mdc; do
    src="$CURSOR_DIR/rules/$leftover"
    # Keep teams.mdc if user explicitly asked to install it this run
    if [[ "$leftover" == "teams.mdc" && "$INSTALL_TEAMS" == "1" ]]; then
      continue
    fi
    # Top-level clojure duplicates standards/ — archive only if standards copy exists
    if [[ "$leftover" == "clojure-daily-tips.mdc" || "$leftover" == "clojure-review.mdc" ]]; then
      if [[ ! -f "$CURSOR_DIR/rules/standards/$leftover" && ! -f "$SCRIPT_DIR/rules/standards/$leftover" ]]; then
        continue
      fi
    fi
    if [[ -f "$src" ]]; then
      if [[ "$archived" -eq 0 ]]; then
        echo "  archive local-only rules → $archive_dir"
        if [[ "$DRY_RUN" != "1" ]]; then
          mkdir -p "$archive_dir"
        fi
        archived=1
      fi
      echo "    move $leftover"
      if [[ "$DRY_RUN" != "1" ]]; then
        mv "$src" "$archive_dir/"
      fi
    fi
  done
fi

if [[ "$INSTALL_HOOKS" == "1" || "$INSTALL_NITI" == "1" ]]; then
  if [[ "$DRY_RUN" != "1" ]]; then
    mkdir -p "$CURSOR_DIR/hooks"
  fi
  copy_file "$SCRIPT_DIR/hooks/deny-destructive-shell.sh" \
    "$CURSOR_DIR/hooks/deny-destructive-shell.sh" "hooks/deny-destructive-shell.sh"
  copy_file "$SCRIPT_DIR/hooks/hooks.json.example" \
    "$CURSOR_DIR/hooks/hooks.json.example" "hooks/hooks.json.example"
  copy_file "$SCRIPT_DIR/hooks/README.md" \
    "$CURSOR_DIR/hooks/README.md" "hooks/README.md"
  if [[ "$DRY_RUN" != "1" ]]; then
    chmod +x "$CURSOR_DIR/hooks/deny-destructive-shell.sh" 2>/dev/null || true
  fi
  echo "  note: enable hooks by creating $CURSOR_DIR/hooks.json (see hooks/README.md)"
  echo "        project-level hooks: copy into <repo>/.cursor/ instead"
fi

if [[ "$INSTALL_NITI" == "1" ]]; then
  install_dir "$SCRIPT_DIR/scripts/niti" "$CURSOR_DIR/scripts/niti" "scripts/niti"
  install_dir "$SCRIPT_DIR/niti" "$CURSOR_DIR/niti-kit" "niti schemas/templates (kit copy)"
  copy_file "$SCRIPT_DIR/hooks/niti-telemetry.sh" \
    "$CURSOR_DIR/hooks/niti-telemetry.sh" "hooks/niti-telemetry.sh"
  copy_file "$SCRIPT_DIR/hooks/niti-stop-trigger.sh" \
    "$CURSOR_DIR/hooks/niti-stop-trigger.sh" "hooks/niti-stop-trigger.sh"
  copy_file "$SCRIPT_DIR/hooks/hooks.json.niti.example" \
    "$CURSOR_DIR/hooks/hooks.json.niti.example" "hooks/hooks.json.niti.example"
  if [[ "$DRY_RUN" != "1" ]]; then
    chmod +x "$CURSOR_DIR/hooks/niti-telemetry.sh" \
             "$CURSOR_DIR/hooks/niti-stop-trigger.sh" 2>/dev/null || true
    mkdir -p "$CURSOR_DIR/niti/logs" "$CURSOR_DIR/niti/reports"
    if [[ ! -f "$CURSOR_DIR/niti/state.json" ]]; then
      cp "$SCRIPT_DIR/niti/templates/state.json" "$CURSOR_DIR/niti/state.json"
    fi
    touch "$CURSOR_DIR/niti/logs/events.jsonl" \
          "$CURSOR_DIR/niti/logs/executions.jsonl" \
          "$CURSOR_DIR/niti/recommendations.jsonl"
  fi
  echo "  note: merge hooks.json.niti.example into $CURSOR_DIR/hooks.json to enable telemetry"
  echo "        runtime logs: $CURSOR_DIR/niti/  (override with KESH_NITI_HOME)"
fi

if [[ "$INSTALL_TEAMS" == "1" ]]; then
  copy_file "$SCRIPT_DIR/optional/teams.mdc" "$CURSOR_DIR/rules/teams.mdc" "optional/teams.mdc"
fi

if [[ "$INSTALL_HEALTHCARE" == "1" ]]; then
  if [[ -d "$SCRIPT_DIR/optional/healthcare/agents" ]]; then
    # Merge optional agents into agents dir (explicit opt-in)
    for f in "$SCRIPT_DIR/optional/healthcare/agents"/*.md; do
      [[ -f "$f" ]] || continue
      copy_file "$f" "$CURSOR_DIR/agents/$(basename "$f")" "healthcare agent $(basename "$f")"
    done
  fi
  if [[ -d "$SCRIPT_DIR/optional/healthcare/skills" ]]; then
    for skill_dir in "$SCRIPT_DIR/optional/healthcare/skills"/*/; do
      [[ -d "$skill_dir" ]] || continue
      skill_name="$(basename "$skill_dir")"
      install_dir "$skill_dir" "$CURSOR_DIR/skills/$skill_name" "healthcare skills/$skill_name"
    done
  fi
  echo "  note: optional healthcare pack installed — keep PHI out of prompts/logs"
fi

if [[ "$SKIP_CLOJURE" == "1" ]]; then
  echo "  remove Clojure standards (SKIP_CLOJURE=1)"
  if [[ "$DRY_RUN" != "1" ]]; then
    rm -f "$CURSOR_DIR/rules/standards/clojure-review.mdc" \
          "$CURSOR_DIR/rules/standards/clojure-daily-tips.mdc"
  else
    echo "    (dry-run) rm standards/clojure-*.mdc"
  fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    INSTALLATION COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Reload Cursor window (Cmd+Shift+P → Developer: Reload Window)"
echo "  2. In chat: @kesh <your task>"
echo "  3. Adaptive lifecycle: $CURSOR_DIR/knowledge/kesh/docs/WORKFLOW.md"
echo "  4. Optional: ./scripts/validate-kit.sh  (from this repo)"
echo ""
echo "Upgrade: re-run ./install.sh — backups are created automatically."
echo "Breaking change: Agent Maximization replaced by adaptive task classes;"
echo "Money Lens no longer hard-stops mandatory bug/security/incident work."
echo "Local-only employer rules (if any) archived under $CURSOR_DIR/rules-archived-local-only-*."
echo ""
