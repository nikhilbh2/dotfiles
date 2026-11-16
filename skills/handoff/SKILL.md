---
name: handoff
description: Write or refresh a portable project checkpoint before stopping, switching agents or environments, or starting a fresh session. Use when asked for a handoff, checkpoint, or context transfer; preserve decisions and verified state without copying a whole transcript.
---

# Handoff

Create a compact record that a fresh agent can use without this conversation.
Keep durable system documentation near code; store changing project state in the
user's chosen private context location. Do not treat this public skill repository
as the destination for project records.

## When to checkpoint

Checkpoint at meaningful milestones (decision made, branch/PR published, checks
changed), before switching tasks, agents or environments or ending a session, and
when a failure or blocker appears. Batch routine progress; do not commit a record
for every trivial tool result. A record is curated state, never a raw transcript or
a mirror of scratch files.

## Establish destination and scope

1. Find the existing project record from the user's request or repository context
   index. Reuse it rather than creating competing sources of truth.
2. If no destination is established, draft in the conversation or an authorized
   local workspace and ask where the durable record should live. Do not upload
   internal work to a personal/public repository. Never include credentials,
   authentication material, unrelated personal data, or raw transcripts.
3. Read the existing record and applicable repository instructions. Preserve
   still-relevant decisions and rationale; mark superseded decisions explicitly.
   Separate durable system behavior from this change's implementation details.

## Reconcile evidence

Inspect only authorized sources. Record the repository, branch, exact HEAD,
working-tree status (including untracked files), current PR/task links, tests and
CI at that HEAD, and any active worker. Never infer completion from a past agent's
claim or a green check on an earlier commit. Mark unavailable evidence unknown,
with its last observation time and a concrete verification step.

Use `references/checkpoint-template.md` for a project summary and
`references/run-record-template.md` for one worker's run; neither requires every
section. Capture: goal and scope; decisions with rationale; verified current state
(HEAD, checks) with observation times; blockers; one exact next action; source
links; active owner/writer; durable artifact pointers. Distinguish observed facts,
historical reports, plans, and recommendations. Record timestamps in UTC.

Keep the current state compact. Replace superseded state instead of appending
logs; link history (commits, PRs, older run records) rather than copying it. Keep
the rationale of decisions that still constrain the work, marking any reversal.
If a record grows beyond a quick read (roughly 150 lines), prune or split it.

## Preserve work, then hand off

- A transcript or summary does not preserve uncommitted changes or artifacts.
  Inventory them and identify their existing location and durability. If further
  backup is needed, propose it; do not automatically stash, reset, clean, commit,
  push, change branches, or copy sensitive files.
- Do not rely on `/tmp`, a single environment, or a session ID as the only copy of
  needed work. Preserve links to authorized durable artifacts where available.
- A run pointer may include environment link, worktree, branch/HEAD, agent/session
  ID, owner, observed status, last check, and next action. Treat IDs as metadata,
  not permission to access another system or interrupt a worker.
- Each concurrent worker writes only its own run record. The coordinator (or the
  single owner) merges results into the project summary.
- Fetch and read the record immediately before updating it. If it changed,
  reconcile rather than overwriting; never silently drop another writer's edit.
  Stage only the record files you changed; no mass `git add` or unrelated edits.
- On a rejected non-fast-forward push, fetch, rebase your record commit onto the
  remote branch, re-check the merged text, and retry. Stop after three attempts or
  any content conflict (abort the rebase) and report the conflict. Never force push.
- Before any push, verify the destination's visibility and ownership. Never put
  credentials, internal links or identifiers, customer data or project details in
  a public repository; generic procedures only.
- Writing a local handoff is not publishing it. Commit/push/upload only when the
  user has authorized that destination and action. Report separately whether the
  record is draft, saved locally, or verified on its authorized remote.
- Never stop or delete an environment as automatic cleanup. Only delete one when
  the user explicitly requests it.

## Finish

Return the record's location, what changed, the recommended next action, and any
missing evidence or unsaved work. Keep the handoff small enough to be read at the
start of the next session. Do not claim that a scheduler, monitor, or new agent is
running merely because the record describes one. This skill is a procedure, not
enforcement: say a checkpoint is automatic only if a hook or job is actually
configured and observed.

## Improve the workflow

When a handoff or resume hits repeated friction, propose a small, generic fix to
the skill with a test, and keep project-specific details in the private record.
