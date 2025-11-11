#!/usr/bin/env bash
set -euo pipefail

# Ensure a local bin on PATH
mkdir -p "$HOME/.local/bin"
case "$SHELL" in
  */zsh) grep -q 'export PATH=$HOME/.local/bin:$PATH' "$HOME/.zshrc" 2>/dev/null || \
         echo 'export PATH=$HOME/.local/bin:$PATH' >> "$HOME/.zshrc" ;;
  *)     grep -q 'export PATH=$HOME/.local/bin:$PATH' "$HOME/.bashrc" 2>/dev/null || \
         echo 'export PATH=$HOME/.local/bin:$PATH' >> "$HOME/.bashrc" ;;
esac

# Install ubi (tiny binary installer) and then git-spice
curl -fsSL https://raw.githubusercontent.com/houseabsolute/ubi/master/installer.sh | sh -s -- -b "$HOME/.local/bin"
"$HOME/.local/bin/ubi" --project abhinav/git-spice --exe gs -o "$HOME/.local/bin/gs"

# Optional: verify
"$HOME/.local/bin/gs" --version || true
