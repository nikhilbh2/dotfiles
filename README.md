# dotfiles

## AI skills

Canonical source: `skills/<name>/SKILL.md`. Keep reusable procedures and generic
examples here, not private project briefs, transcripts, credentials, or run data.

| Skill | Purpose |
| --- | --- |
| [thabto](skills/thabto/README.md) | Explicit read-only independent attempts, cross-review and synthesis |
| [handoff](skills/handoff/SKILL.md) | Write a verified, portable project checkpoint |
| [resume](skills/resume/SKILL.md) | Reconstruct context and verify state before the next authorized task |

Install only the bundled skills (requires Bash and Python 3):

```sh
bash ./install-skills.sh --dry-run
bash ./install-skills.sh
```

The installer links each skill into `~/.local/share/skills` (or
`$XDG_DATA_HOME/skills`), then exposes it through `~/.agents/skills`,
`~/.claude/skills`, and legacy `~/.codex/skills`. It also supports a custom
`CODEX_HOME`. It preflights all destinations before writing, keeps matching links,
and refuses unmanaged files or different symlinks. It migrates only exact legacy
links to this checkout's old `skills/.local/share/skills/<name>` path, including
links made dangling by the directory move. A link to a different checkout is a
conflict to review manually, not something the installer overwrites.

This is a link-based installation: keep the checkout available. Updating it updates
the linked source; rerun installation for added skills or after this migration.
Install on each computer/environment. Existing agent sessions may cache discovery;
verify in a fresh session using that provider's skill listing/invocation UI.
Link existence does not prove that an authenticated agent can use a skill.

`install-skills.sh` does not install provider CLIs, sign in, modify shell startup,
commit/push context, or schedule work. The broader `install.sh` does additional
machine setup; do not run it merely to refresh skills.

### Verification

```sh
python3 -m unittest discover -s tests -v
```

The offline suite tests fresh/repeated installation, legacy-link migration,
conflicts, dry-run, custom paths and bundled command help. It makes no model calls.
Use the [manual smoke test](tests/MANUAL.md) to verify discovery and a fresh-session
handoff with each authenticated provider. See [ROADMAP.md](ROADMAP.md) for follow-ons.

THABTO requires installed and authenticated provider CLIs. Its drivers and harness
remain unchanged from the [vendored version](skills/thabto/UPSTREAM.md). Run artifacts
remain outside the repo under `~/.local/state/thabto` (or `$XDG_STATE_HOME/thabto`).

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
