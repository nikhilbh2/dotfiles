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
