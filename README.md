# dotfiles

## AI skills

Install the bundled skills without running the rest of the environment setup:

```sh
bash ./install-skills.sh
```

The installer links each skill into `~/.local/share/skills` (or
`$XDG_DATA_HOME/skills`), then exposes it through `~/.agents/skills`,
`~/.claude/skills`, and `~/.codex/skills`. It also supports a custom `CODEX_HOME`.
Existing files and different symlinks are preserved; installation stops if a
destination conflicts. The main `install.sh` also installs these skills.

### THABTO

[THABTO](skills/.local/share/skills/thabto/README.md) runs independent model
attempts, mutual review, and revision for a read-only task. Invoke it by name,
for example: “Use THABTO to review this PR.” Claude Code and Codex must already
be installed and authenticated.

The skill is copied unchanged from
[`wihli/dotfiles`](https://github.com/wihli/dotfiles/tree/1eed389c3c99198e23edf12b600499ba6525bcd0/skills/.local/share/skills/thabto)
at commit `1eed389c3c99198e23edf12b600499ba6525bcd0`. This repository's
`skills/.local/share/skills/thabto` directory is the local source; make any
local changes there, then run the installer. Upstream documentation refers to
the original author's checkout as `wihli-dotfiles`.

Run artifacts stay under `~/.local/state/thabto` (or `$XDG_STATE_HOME/thabto`)
and are not part of this repository.

## Codex with the Vanta ChatGPT account

Ona agent shells can supply `CODEX_HOME` and `CODEX_API_KEY` for Ona's managed
provider. The `codex-vanta` launcher removes those overrides for its child
process, so Codex uses the user's normal `~/.codex` configuration and login.
It does not change the parent shell or install another Codex CLI.

Install the launcher on an existing box:

```sh
bash ./install-codex.sh
```

The main `install.sh` also installs it. Codex itself must be available on
`PATH`; see the [official CLI installation instructions](https://learn.chatgpt.com/docs/cli)
if a new box does not already provide it.

Run the following interactively on each new box, then open the printed link
in your browser and sign in with the Vanta ChatGPT account and workspace:

```sh
~/.local/bin/codex-vanta login --device-auth
~/.local/bin/codex-vanta login status
```

Device login must be enabled for the workspace. If it is unavailable, use the
[documented SSH callback forwarding flow](https://learn.chatgpt.com/docs/auth#fallback-forward-the-localhost-callback-over-ssh)
with `~/.local/bin/codex-vanta login` in the remote SSH session.

Login is intentionally separate from the non-interactive dotfiles installer.
It is cached per box. Keep credentials and `auth.json` outside this repository;
do not add an API key to dotfiles for this ChatGPT login workflow.

For THABTO, select this launcher using the driver's existing argument:

```sh
python3 ~/.local/share/skills/thabto/scripts/thabto.py \
  --task-file /path/to/task.md \
  --workspace /workspaces/obsidian \
  --claude-model claude-opus-5-5 \
  --codex-model gpt-6-sol \
  --codex-executable "$HOME/.local/bin/codex-vanta"
```

Configure Ona's dotfiles repository in Settings > Preferences as
`https://github.com/nikhilbh2/dotfiles`. Changes on a feature branch must reach
the branch Ona installs before new boxes receive them. Existing boxes need to
update their checkout and rerun the relevant installer scripts. See
[Ona's dotfiles documentation](https://ona.com/docs/ona/configuration/dotfiles/overview).
