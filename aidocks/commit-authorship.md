---
name: commit-authorship
description: "User's rule for git commits in this project — never add Claude as author or co-author"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:43:42.705Z
---

Never add Claude/Anthropic as the author or co-author of git commits in this project. Do NOT include the `Co-Authored-By: Claude ...` trailer or any "Generated with Claude Code" line in commit messages.

**Why:** The user wants commits to appear authored solely by them.

**How to apply:** Write plain commit messages with no attribution trailers. Let git use the user's own configured author identity — do not pass `--author` or add co-author trailers.
