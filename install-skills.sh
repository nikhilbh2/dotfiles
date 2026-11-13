#!/usr/bin/env bash
# Install only skill links. Never installs tools, signs in, or changes shell files.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$ROOT/skills"
SHARED="${XDG_DATA_HOME:-$HOME/.local/share}/skills"
DISCOVERY=("$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.codex/skills")
[[ -z "${CODEX_HOME:-}" ]] || DISCOVERY+=("$CODEX_HOME/skills")
DRY_RUN=false
case "${1:-}" in
  '') ;;
  --dry-run) DRY_RUN=true ;;
  -h|--help) printf 'Usage: bash install-skills.sh [--dry-run]\n'; exit 0 ;;
  *) printf 'Unknown argument: %s\n' "$1" >&2; exit 2 ;;
esac
[[ $# -le 1 ]] || { echo 'Too many arguments' >&2; exit 2; }

SOURCES=() DESTINATIONS=() ACTIONS=()
plan_link() {
  local source="$1" destination="$2" legacy="$3" target='' action='link' previous parent
  # Normalize lexical components and existing parent symlinks without requiring
  # the final link to exist. Python is already required by the bundled skills.
  destination="$(python3 -c 'import os,sys; print(os.path.join(os.path.realpath(os.path.dirname(sys.argv[1])),os.path.basename(sys.argv[1])))' "$destination")"
  source="$(python3 -c 'import os,sys; print(os.path.join(os.path.realpath(os.path.dirname(sys.argv[1])),os.path.basename(sys.argv[1])))' "$source")"
  [[ "$source" != "$destination" ]] || return 0
  parent="$(dirname "$destination")"
  while [[ ! -e "$parent" && ! -L "$parent" ]]; do parent="$(dirname "$parent")"; done
  if [[ ! -d "$parent" ]]; then
    printf 'Parent is not a directory: %s\n' "$parent" >&2; return 1
  fi
  for previous in "${DESTINATIONS[@]:-}"; do
    [[ "$previous" != "$destination" ]] || return 0
  done
  if [[ -L "$destination" ]]; then
    target="$(readlink "$destination")"
    if [[ "$target" == "$source" ]]; then
      action='keep'
    elif [[ "$target" == "$legacy" ]]; then
      action='migrate'
    else
      printf 'Refusing to replace existing symlink: %s -> %s\n' "$destination" "$target" >&2; return 1
    fi
  elif [[ -e "$destination" ]]; then
    printf 'Refusing to replace existing path: %s\n' "$destination" >&2; return 1
  fi
  SOURCES+=("$source"); DESTINATIONS+=("$destination"); ACTIONS+=("$action")
}

command -v python3 >/dev/null || { echo 'python3 is required' >&2; exit 1; }
# Preflight every destination before changing any of them.
for path in "$SOURCE"/*; do
  [[ -f "$path/SKILL.md" ]] || continue
  name="$(basename "$path")"
  legacy="$ROOT/skills/.local/share/skills/$name"
  shared="$SHARED/$name"
  plan_link "$path" "$shared" "$legacy"
  for directory in "${DISCOVERY[@]}"; do
    plan_link "$shared" "$directory/$name" "$legacy"
  done
done
for ((i=0; i<${#DESTINATIONS[@]}; i++)); do
  printf '%s: %s -> %s\n' "${ACTIONS[$i]}" "${DESTINATIONS[$i]}" "${SOURCES[$i]}"
  $DRY_RUN && continue
  [[ "${ACTIONS[$i]}" != keep ]] || continue
  mkdir -p -- "$(dirname -- "${DESTINATIONS[$i]}")"
  if [[ "${ACTIONS[$i]}" == migrate ]]; then
    # Recheck immediately before replacing only the managed legacy symlink.
    expected="$ROOT/skills/.local/share/skills/$(basename "${DESTINATIONS[$i]}")"
    [[ -L "${DESTINATIONS[$i]}" && "$(readlink "${DESTINATIONS[$i]}")" == "$expected" ]] || exit 1
    rm -- "${DESTINATIONS[$i]}"
  fi
  ln -s -- "${SOURCES[$i]}" "${DESTINATIONS[$i]}"
done
