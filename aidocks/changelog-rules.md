---
name: changelog-rules
description: "Rules for writing changelog entries in rg/docks/english/changelog.txt — player-facing prose, sentence caps, per-version entry limits, reverse-chronological order. Adapted from CaveDefender/SimpleFighter (same dev)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-09-15T00:00:00.000Z
---

Rules for writing new entries in `rg/docks/english/changelog.txt`. The `docks/` folder is split by language into `english/` and `spanish/` subfolders; the English changelog is `english/changelog.txt` and its Spanish counterpart is `spanish/cambios.txt`. Existing style is terse one-liners under a `New in X.Y.` header.

- **A changelog is a RECORD OF WHAT CHANGED, not a manual.** The readme is the manual. The changelog just says, in a sentence or two, what's new or different. If an entry starts explaining *how to use* a feature (keys, sub-options, mechanics), it has drifted into readme territory — pull it back to the high-level "what changed."
- **A whole feature that lands in ONE version gets ONE concise "added X" entry**, not one entry per sub-feature/mechanic. Describe what it IS; let the readme carry every mechanic.
- **Player-facing prose only.** Describe what the player sees, hears, or can now do — never the code-side cause, internal field names, or refactors. If a change has no observable effect for the player, it does not belong in the changelog.
- **One entry = one line of 1–3 sentences. Default to 1.** Use 2 only for a meaningful caveat, a why, or a paired side-effect. Use 3 only when genuinely substantial. Don't pad to fill a sentence count.
- **No breathless run-ons — write each entry clean the FIRST time.** Each sentence carries ONE idea; never stack clauses or semicolon-joined piles into one sentence. The dev reads every entry by ear via screen reader, so a run-on is genuinely painful.
- **Skip changes too small to matter to the player.** Dev/code-only fixes are left out.
- **Per-version entry caps (independent per version):** a major `.0` release holds up to **20** entries; each minor (`.1`, `.2`, …) holds up to **10**. When the in-progress version is full, roll to the next minor rather than overflowing. **The `New in X.Y.` header line does NOT count as an entry** — count only the change lines beneath it (dev confirmed 2026-09-14).
- **Header format:** each version block starts `New in X.Y.` (trailing period), matching the existing file.
- **Reverse-chronological at both levels:** newest version block at the TOP of the file; within a block, newest entry at the top.
- The **game code** has no version constant to bump — the changelog header is the source of truth for the current version, so just keep its header/order consistent. (The build/release tooling does read `build/version.txt`, but that only drives the GitHub tag/title in `tools.py`; the game never reads it and it is not tied to changelog entries.)

**Why:** keeps the changelog readable and scoped; caps prevent bloat, the sentence limit prevents padding.

**How to apply:** follow exactly whenever a changelog entry is written or a new version block opened; the caps are hard limits. Related: [[confirm-before-implementing]], [[list-modified-files]].
