# Agent workflow roadmap

## This foundation
- [x] One canonical `skills/<name>` source with safe, narrow installation.
- [x] Keep THABTO as a peer skill, with provenance and offline smoke checks.
- [x] Add provider-neutral `handoff` and `resume` with templates.

## Next, in small slices
- [ ] Choose an approved private work-context repository; keep work data out of
      public dotfiles. Establish an index, owner and save/publish policy.
- [ ] Exercise a harmless sample handoff in fresh Claude and Codex sessions.
      Verify actual discovery, not just symlink existence. Then pilot one project.
- [ ] Add `project-brief` if the handoff brief section proves insufficient.
- [ ] Add a small validated per-run registry and `project-status` reconciliation:
      environment/session, branch/HEAD, owner, observed state, next action, timestamp.
- [ ] Add a setup diagnostic that reports CLI versions, skill discovery and private
      context access without exposing credentials.
- [ ] Add authorized environment adapters and explicit-only deletion safeguards.
- [ ] Add scheduler/coordinator integration: selected project, check interval or
      event, permission limits, notification threshold and stopping condition.
      A registry is not a scheduler, and a skill is not a process supervisor.
- [ ] Add `review-pr` / `investigate-alert` only after the lifecycle is tested.

Keep task/PR/CI systems authoritative; checkpoints link and reconcile them, not
silently replace them. Session handles and local caches are conveniences, not the
only durable project record. This roadmap authorizes no external actions.
