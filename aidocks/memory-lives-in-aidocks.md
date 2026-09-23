---
name: memory-lives-in-aidocks
description: This project's memories live in the repo's aidocks/ folder (indexed by aidocks/MEMORY.md), not the default ~/.claude memory dir; CLAUDE.md is the dispatcher to read first.
metadata:
  node_type: memory
  type: feedback
---

Save every new memory for RhythmRage as a file in `aidocks/` at the repo root and add its one-line pointer to `aidocks/MEMORY.md`. Don't write project memories to the default `~/.claude/projects/.../memory/` folder. Before working in an area, read `CLAUDE.md` (the dispatcher) and the aidocks memory it links to.

**Why:** the dev asked for this directly (2026-09-22). aidocks is checked into the repo, so the notes travel with the project, and CLAUDE.md points into it.

**How to apply:** follow the frontmatter format of the existing aidocks files (`name`, `description`, `metadata.node_type: memory`, `metadata.type`). Update an existing file rather than duplicating it, and link related notes with `[[name]]`. Example: [[known-bugs-2026-09-evaluation]].
