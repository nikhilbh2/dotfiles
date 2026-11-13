# Fresh-session smoke test

Run after the offline tests in an isolated test checkout/home with authenticated
Claude Code or Codex. These steps are not performed by the installer.

1. Install skills with the narrow installer. Start a fresh provider session and
   confirm `handoff`, `resume`, and `thabto` are discovered. Record provider version,
   dotfiles revision and actual discovery paths. Do not run THABTO model calls
   merely to test discovery.
2. In a throwaway sample repository, ask the agent to implement a tiny greeting
   function with a test. Keep it local; do not publish anything.
3. Invoke `handoff` to write a checkpoint to an explicitly chosen local sample
   context directory. Ensure it accurately describes dirty/untracked files and
   labels the checkpoint local, not durably published.
4. End the session. Change one sample source file, without updating the checkpoint.
5. Start a fresh session with only `resume`, the checkpoint path and sample repo.
   Ask for orientation only. It should detect the changed worktree, describe goal
   and constraints, propose the next step, and not overwrite or launch work.
6. Repeat with the other provider. Test a missing artifact, unavailable CI, and an
   active worker. Expect unknown status and a coordination step, not fabricated
   success or a second writer.

Record actual outcomes, not just expected outcomes. Never use live work credentials,
private project data, paid calls, or public uploads as disposable test fixtures.
