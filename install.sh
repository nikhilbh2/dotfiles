#!/usr/bin/env bash
set -euo pipefail

# Resolve DOTFILES_DIR to this script's directory unless provided by the caller
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="${DOTFILES_DIR:-$SCRIPT_DIR}"

# Install Homebrew if missing
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "$HOME/.bashrc"
  eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
fi

# Install git-spice
brew install --cask abhinav/tap/git-spice

# --- Dotfiles you want in $HOME
ln -sf "$DOTFILES_DIR/.alias" "$HOME/.alias"

# Ensure the aliases file is sourced (bash & zsh)
grep -q 'source ~/.alias' "$HOME/.bashrc" 2>/dev/null || echo '[ -f ~/.alias ] && source ~/.alias' >> "$HOME/.bashrc"
grep -q 'source ~/.alias' "$HOME/.zshrc" 2>/dev/null || echo '[ -f ~/.alias ] && source ~/.alias' >> "$HOME/.zshrc"
