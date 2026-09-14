---
name: check-git-log-for-commits
description: The dev commits their own work between turns; check git log/status before asking or assuming commit state. Carried over from CaveDefender/SimpleFighter (same dev).
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:14.391Z
---

The dev commits changes themselves. Before asking "want me to commit?" or assuming something is uncommitted, check `git log --oneline` (and `git status`) — they often commit between turns without saying so.

**Why:** they've been mildly annoyed at being asked about a commit they'd already made; the git log is the source of truth for what's landed. (RhythmRage is now a git repo, remote `github.com/tsatria03/RhythmRage-NVGT`.)

**How to apply:** after an editing turn, run a quick `git log`/`git status` to see whether they've already committed before mentioning commits at all. Still never commit for them unless explicitly asked — and when you do commit, follow [[commit-authorship]] (no Claude author/co-author). Relates to [[list-modified-files]], [[dont-compile-yourself]].
