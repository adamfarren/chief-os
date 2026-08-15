#!/bin/bash
#
# Chief OS — Install / Sync Script
#
# Creates symlinks from ~/.claude/skills/ → this repo for all public skills.
# Skips skills that have local overrides (Canvas-specific modifications).
# Never touches private/proprietary skills that live only locally.
#
# Usage:
#   ./install.sh          — install/update symlinks
#   ./install.sh --status — show what's linked, overridden, and private
#

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
BACKUP_DIR="$SKILLS_DIR/.backups/$(date +%Y%m%d-%H%M%S)"

# Public skills that get symlinked to the repo.
# A name listed in OVERRIDE_SKILLS below is skipped here, so a skill may safely
# appear in both lists: the override always wins.
PUBLIC_SKILLS=(
  1-1
  chief-1-1
  chief-board
  chief-initiative
  chief-competitive
  chief-deal
  chief-digest
  chief-escalation
  chief-event
  chief-fundraise
  chief-investor
  chief-linkedin
  chief-memo
  chief-partnerships
  chief-performance
  chief-pipeline
  chief-roadmap
  chief-workload
  claude-usage
  funnel
  customer-360
  unslop
  whiteboard
)

# Skills with local overrides — exist in repo but are NOT symlinked
# because the local version contains proprietary modifications.
# This list takes precedence over PUBLIC_SKILLS whenever a local version exists:
# a real directory here is never replaced and never backed up. If no local version
# exists (a fresh clone), the repo copy is linked so the skill still works.
OVERRIDE_SKILLS=(
  chief           # Router table references company-specific skills
  chief-style     # Contains a company-specific Figma file key
  chief-context   # Contains real company data (strategy, org, voice)
  chief-org       # Contains real company roster and org chart data
  company-update  # Local version has operational UUIDs (Notion DB, channel IDs, workspace slug)
  customer-360    # Local version names company-specific tools + real customer slugs; repo is generic
  chief-roadmap   # Local version references a company-specific roadmap + employees by name
  funnel          # Local version references company-specific HubSpot config + lead-source values
  1-1             # Local version references a company handbook page + employee first names in examples
)

# OVERRIDE_SKILLS takes precedence over PUBLIC_SKILLS. Returns 0 when the skill
# is overridden locally and must not be touched.
is_override() {
  local needle="$1" s
  for s in "${OVERRIDE_SKILLS[@]}"; do
    [[ "$needle" == "$s" ]] && return 0
  done
  return 1
}

status_mode=false
if [[ "${1:-}" == "--status" ]]; then
  status_mode=true
fi

if $status_mode; then
  echo "Chief OS — Skill Status"
  echo "======================="
  echo ""
  echo "Symlinked (public → repo):"
  for skill in "${PUBLIC_SKILLS[@]}"; do
    is_override "$skill" && continue
    target="$SKILLS_DIR/$skill"
    if [[ -L "$target" ]]; then
      echo "  ✓ $skill → $(readlink "$target")"
    elif [[ -d "$target" ]]; then
      echo "  ✗ $skill (real directory — run install.sh to link)"
    else
      echo "  - $skill (not installed)"
    fi
  done
  echo ""
  echo "Local overrides (in repo, but local version used):"
  for skill in "${OVERRIDE_SKILLS[@]}"; do
    target="$SKILLS_DIR/$skill"
    if [[ -d "$target" && ! -L "$target" ]]; then
      echo "  ✓ $skill (local override active)"
    elif [[ -L "$target" ]]; then
      echo "  ! $skill (symlinked — should be a local override)"
      echo "      your local version was displaced by an earlier install; restore it from $SKILLS_DIR/.backups/"
    else
      echo "  - $skill (not installed)"
    fi
  done
  echo ""
  echo "Private skills (local only, not in repo):"
  for dir in "$SKILLS_DIR"/*/; do
    skill="$(basename "$dir")"
    # Skip if it's in public or override lists
    skip=false
    for s in "${PUBLIC_SKILLS[@]}" "${OVERRIDE_SKILLS[@]}"; do
      [[ "$skill" == "$s" ]] && skip=true && break
    done
    # Skip hidden dirs
    [[ "$skill" == .* ]] && continue
    if ! $skip; then
      echo "  • $skill"
    fi
  done
  exit 0
fi

echo "Chief OS — Installing skill symlinks"
echo "Repo:   $REPO_DIR"
echo "Target: $SKILLS_DIR"
echo ""

mkdir -p "$SKILLS_DIR"

linked=0
skipped=0
backed_up=0
overridden=0
displaced=0

for skill in "${PUBLIC_SKILLS[@]}"; do
  source="$REPO_DIR/skills/$skill"
  target="$SKILLS_DIR/$skill"

  if [[ ! -d "$source" ]]; then
    echo "  WARN: $skill not found in repo, skipping"
    continue
  fi

  # Never displace a locally overridden skill, even if it is also in PUBLIC_SKILLS.
  # An override only applies when a local version actually exists, so a fresh clone
  # still gets the repo copy rather than an empty slot.
  if is_override "$skill"; then
    if [[ -L "$target" ]]; then
      echo "  WARN: $skill is a local override but is currently a symlink."
      echo "        An earlier install displaced your local version. Restore it with:"
      echo "          rm $target && mv $SKILLS_DIR/.backups/<timestamp>/$skill $target"
      ((displaced++))
      continue
    fi
    if [[ -d "$target" ]]; then
      ((overridden++))
      continue
    fi
    ln -s "$source" "$target"
    echo "  Linked $skill (repo version — replace it with a real directory to override locally)"
    ((linked++))
    continue
  fi

  # Already correctly linked
  if [[ -L "$target" ]] && [[ "$(readlink "$target")" == "$source" ]]; then
    ((skipped++))
    continue
  fi

  # Remove existing symlink pointing elsewhere
  if [[ -L "$target" ]]; then
    rm "$target"
  fi

  # Back up existing real directory
  if [[ -d "$target" ]]; then
    mkdir -p "$BACKUP_DIR"
    mv "$target" "$BACKUP_DIR/$skill"
    echo "  Backed up $skill → .backups/"
    ((backed_up++))
  fi

  ln -s "$source" "$target"
  echo "  Linked $skill"
  ((linked++))
done

# Seed chief-context with example data if it doesn't exist
if [[ ! -d "$SKILLS_DIR/chief-context" ]]; then
  cp -r "$REPO_DIR/skills/chief-context" "$SKILLS_DIR/chief-context"
  echo "  Seeded chief-context with example data (edit with /chief-context)"
fi

# Install the MCP health check hook
HOOKS_DIR="$HOME/.claude/hooks"
HOOK_SRC="$REPO_DIR/hooks/mcp-check.py"
HOOK_DST="$HOOKS_DIR/mcp-check.py"
if [[ -f "$HOOK_SRC" ]]; then
  mkdir -p "$HOOKS_DIR"
  if [[ ! -f "$HOOK_DST" ]]; then
    cp "$HOOK_SRC" "$HOOK_DST"
    chmod +x "$HOOK_DST"
    echo "  Installed hooks/mcp-check.py → ~/.claude/hooks/"
    echo "  NOTE: Register it in ~/.claude/settings.json under hooks.UserPromptSubmit"
    echo "        (see hooks/mcp-check.py header for the JSON snippet)"
  else
    echo "  Hook already present: ~/.claude/hooks/mcp-check.py (not overwritten)"
  fi
fi

echo ""
echo "Done: $linked linked, $skipped already current, $backed_up backed up, $overridden left as local overrides"
if [[ $displaced -gt 0 ]]; then
  echo "WARNING: $displaced override skill(s) are symlinked and need restoring from backups (see above)"
fi
if [[ $backed_up -gt 0 ]]; then
  echo "Backups: $BACKUP_DIR"
fi
echo ""
echo "Override skills (local, not linked):"
for skill in "${OVERRIDE_SKILLS[@]}"; do
  if [[ -d "$SKILLS_DIR/$skill" ]]; then
    echo "  • $skill"
  fi
done
