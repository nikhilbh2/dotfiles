#!/usr/bin/env bash
set -euo pipefail

CODEX_DOTFILES_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CODEX_LAUNCHER_SOURCE="$CODEX_DOTFILES_DIR/bin/codex-vanta"
CODEX_LAUNCHER_TARGET="$HOME/.local/bin/codex-vanta"

if [[ -L "$CODEX_LAUNCHER_TARGET" && "$(readlink -- "$CODEX_LAUNCHER_TARGET")" == "$CODEX_LAUNCHER_SOURCE" ]]; then
  printf 'Codex launcher is already installed.\n'
elif [[ -e "$CODEX_LAUNCHER_TARGET" || -L "$CODEX_LAUNCHER_TARGET" ]]; then
  printf 'Refusing to replace existing path: %s\n' "$CODEX_LAUNCHER_TARGET" >&2
  exit 1
else
  mkdir -p -- "$HOME/.local/bin"
  ln -s -- "$CODEX_LAUNCHER_SOURCE" "$CODEX_LAUNCHER_TARGET"
  printf 'Installed Codex launcher: %s\n' "$CODEX_LAUNCHER_TARGET"
fi
