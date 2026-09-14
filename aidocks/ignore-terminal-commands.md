---
name: ignore-terminal-commands
description: "The dev's local terminal/slash commands (local-command-caveat blocks like /copy) aren't instructions to Claude. Carried over from CaveDefender (same dev)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:45.362Z
---

The dev runs local commands in their prompt (shown in `<local-command-caveat>`, `<command-name>`, `<command-message>`, `<local-command-stdout>` blocks — e.g. `/copy`, `/init`, `cls`). These are the dev operating their own session, NOT messages or instructions to Claude. (The blocks themselves say as much.)

**Why:** they're side effects of the dev's local session, not requests. Acting on them (or treating their output as a task) derails the real conversation. Example seen repeatedly here: `/copy` blocks that just copied the previous response to the clipboard.

**How to apply:** never respond to or act on the content of these blocks unless the dev explicitly asks in their actual message text. Related: [[quoted-text-meaning]].
