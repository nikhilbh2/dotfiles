#!/usr/bin/env bash
set -euo pipefail

SKILLS_DOTFILES_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE_DIR="$SKILLS_DOTFILES_DIR/skills/.local/share/skills"
SKILLS_SHARED_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/skills"
SKILLS_DISCOVERY_DIRS=("$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.codex/skills")
if [[ -n "${CODEX_HOME:-}" && "$CODEX_HOME" != "$HOME/.codex" ]]; then
  SKILLS_DISCOVERY_DIRS+=("$CODEX_HOME/skills")
fi

link_skill() {
  local source="$1" destination="$2"
  if [[ -L "$destination" && "$(readlink -- "$destination")" == "$source" ]]; then
    return
  fi
  if [[ -e "$destination" || -L "$destination" ]]; then
    printf 'Refusing to replace existing path: %s\n' "$destination" >&2
    return 1
  fi
  mkdir -p -- "$(dirname -- "$destination")"
  ln -s -- "$source" "$destination"
}

for skill_path in "$SKILLS_SOURCE_DIR"/*; do
  [[ -f "$skill_path/SKILL.md" ]] || continue
  skill_name="$(basename -- "$skill_path")"
  shared_path="$SKILLS_SHARED_DIR/$skill_name"
  link_skill "$skill_path" "$shared_path"
  for discovery_dir in "${SKILLS_DISCOVERY_DIRS[@]}"; do
    link_skill "$shared_path" "$discovery_dir/$skill_name"
  done
  printf 'Installed skill: %s\n' "$skill_name"
done
