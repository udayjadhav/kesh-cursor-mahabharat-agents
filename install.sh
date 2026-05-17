#!/usr/bin/env bash
# Kesh Cursor Kit — installs agents, rules, and skills into ~/.cursor
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURSOR_DIR="${CURSOR_DIR:-$HOME/.cursor}"
DRY_RUN="${DRY_RUN:-0}"

usage() {
  cat <<'EOF'
Kesh Cursor Kit installer

Usage:
  ./install.sh              Install to ~/.cursor (default)
  CURSOR_DIR=/path ./install.sh   Custom Cursor config root
  DRY_RUN=1 ./install.sh    Show actions without copying

What gets installed:
  agents/*.md   →  $CURSOR_DIR/agents/
  rules/*.mdc   →  $CURSOR_DIR/rules/
  skills/xray/* →  $CURSOR_DIR/skills/xray/

Existing files are backed up with a timestamp suffix before overwrite.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           KESH CURSOR KIT — INSTALLER                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Target: $CURSOR_DIR"
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
    echo "    (dry-run) cp -a $src/* $dest/"
  else
    cp -a "$src/." "$dest/"
  fi
}

if [[ "$DRY_RUN" != "1" ]]; then
  mkdir -p "$CURSOR_DIR"/{agents,rules,skills/xray}
fi

install_dir "$SCRIPT_DIR/agents"       "$CURSOR_DIR/agents"       "agents (21 files)"
install_dir "$SCRIPT_DIR/rules"        "$CURSOR_DIR/rules"        "rules (12 files)"
install_dir "$SCRIPT_DIR/skills/xray"  "$CURSOR_DIR/skills/xray"  "skills/xray"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    INSTALLATION COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Restart Cursor (or reload window)"
echo "  2. In chat, invoke: @kesh <your task>"
echo "  3. Read docs/WORKFLOW.md for the full 15-step flow"
echo ""
echo "Optional: customize rules/teams.mdc for your org (see optional/)"
echo ""
