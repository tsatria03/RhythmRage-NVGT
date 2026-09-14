---
name: list-modified-files
description: "End every turn that edited files with an explicit \"Files changed:\" list, bare filenames only. Carried over from CaveDefender/SimpleFighter (same dev)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:06.387Z
---

After any turn that modifies files, explicitly tell the dev WHICH files were touched, using bare filenames only, so they can review the changes themselves.

**Why:** The dev is a screen reader user and reviews changes by opening the files; a summary that describes edits without naming every touched file makes them hard to find. They know the repo layout, so directory paths are noise — bare filenames read more cleanly.

**How to apply:** End each response that performed edits with a short "Files changed:" list covering every file written, edited, or deleted that turn — including doc and config files, not just code. One line per file, bare filenames only (e.g. `game.nvgt`, `utils.nvgt`, `changelog.txt`) — no directory paths. RhythmRage is a single game (no client/server split), so no side tags are needed; if two touched files share a name across folders, add just enough to disambiguate. Related: [[confirm-before-implementing]], [[no-crlf-normalization]].
