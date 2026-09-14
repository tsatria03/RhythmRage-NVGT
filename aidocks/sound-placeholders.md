---
name: sound-placeholders
description: "When the dev requests a sound, wire up the playback CODE referencing the intended filename now; the dev adds the actual .ogg later. No dummy files. Carried over from CaveDefender/SimpleFighter (same dev)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:36.791Z
---

When the dev asks for a feature to play a sound, **add the sound-playing code immediately, referencing the intended sound name**, even though the audio does not exist yet. The dev adds the real sound later ("when I find the perfect sound"). The code reference *is* the placeholder.

- **Do NOT** create a dummy/empty/copied `.ogg` file. A "placeholder" here means the code, not a stand-in asset.
- **Do NOT** withhold or comment out the playback code waiting for the file — wire it up as if the sound exists.
- After wiring it, **remind the dev which sound to add and where** (it stays silent until then).

How sounds are played in this codebase (match these patterns):
- **From the active pack:** most game audio loads by bare name from the currently open `pack_file` (`music.load("newlevel")`, `levjing.load(perfectjng)`) after `yespack()` sets storage/decryption. Pack sounds are referenced WITHOUT the `.ogg` extension and WITHOUT a path — the pack build strips both.
- **UI/one-shot sounds:** `pool.play_stationary("<name>", false)` via the global `sound_pool pool`.
- **Engine sound pack (voice/UI):** `nopack()` switches storage to `data/assets/sounds<lang>.pack` before loading built-in speaker/UI sounds; call `yespack()` again afterward. See [[rhythmrage-bgt-to-nvgt-port]] for the nopack/yespack storage-switching model.

**Why:** the dev designs features first and sources the "perfect" sound later; blocking on the asset (or faking one) just slows iteration.

**How to apply:** any "it should play <name>" request → add the load/play call with that exact name, then note the sound to add. Pair with [[list-modified-files]] when reporting.
