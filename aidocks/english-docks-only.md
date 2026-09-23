---
name: english-docks-only
description: Only ever edit the English player docs (rg/docks/english/); never modify, sync, or offer to update the Spanish docs (rg/docks/spanish/).
metadata:
  node_type: memory
  type: feedback
---

When a change touches player-facing docs (changelog, readme, credits, todo list, parser reference), edit **only** `rg/docks/english/`. Never modify `rg/docks/spanish/` (`cambios.txt`, `leeme.txt`, `creador.md`/`creador.html`). Don't offer to sync the Spanish docs to match, and don't flag them as out of date after an English edit.

**Why:** the dev said so directly (2026-09-22), after an offer to bring `cambios.txt` in line with a changelog tightening. The Spanish docs are theirs to handle.

**How to apply:** this covers the doc files only. Spanish *in-game* strings (the `if (lang==2)` branches in `src/`) are still part of normal code edits. Related: [[changelog-rules]], [[list-modified-files]].
