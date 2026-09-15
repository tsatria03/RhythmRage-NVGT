---
name: rhythmrage-bgt-to-nvgt-port
description: "Key facts about the BGT-to-NVGT port of Rhythm Rage — pack handling, loose-pack testing, folder layout"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T06:13:20.923Z
---

RhythmRage-NVGT is a port of Oriol Gomez's audio-only rhythm game from BGT (Blastbay Game Toolkit) to the new NVGT ([[nvgt-engine-location]]).

**Original BGT source (reference for the port):** `C:\Users\tonys\OneDrive\Desktop\rhythm-rage bgt-src` (path confirmed 2026-09-14; was previously `Rhythm_rage BGT_src`). Contains `game.bgt`, `classes.bgt`, `leveltool.bgt`, and the original `include/` files — use it to compare behavior when porting or diagnosing divergences from the original. NVGT differs substantially from BGT, so a divergence isn't automatically a port bug.

**Loose-pack testing behavior (important, non-obvious):**
- `main()` must call `generate_packs()` (the BGT-faithful single-folder builder), NOT `generate_all_packs()`. The port originally used `generate_all_packs()`, which compiled a loose folder to a `.pack` but did NOT load you into it and skipped rebuilds once the `.pack` existed. `generate_all_packs()` has been removed as dead code.
- A loose pack = a folder of raw `.ogg`/`.lvl` files dropped directly into `packs/`. On launch `generate_packs()` builds `packs/<name>.pack`, sets `pack` to it and `creatingpack=true`, then `main()` opens it and runs in creator/test mode: all levels unlocked, rebuilt every launch so edits show up. Only ONE loose folder allowed at a time (else "Multiple packs" alert).
- **Why testing doesn't corrupt your profile:** `ser()` (the only function that writes `save/rg.dat`) early-returns when `creatingpack` is true, so achievements, unlocks, and credits earned while testing a loose pack are never saved. This was true in BGT and is preserved here.
- The `mypacks/` folder is NOT read by the game (BGT or NVGT) — it's a holding area for editable source folders; you must copy a folder into `packs/` to build/test it in the game. The game allows only ONE loose folder in `packs/` at a time (generate_packs alerts "Multiple packs" otherwise). NOTE: the separate `lt.nvgt` authoring tool DOES scan `mypacks/` for its pack picker — you find timings there, then copy that one pack into `packs/` to test-run a level via the tool's `r` key.

**Layout (now a git repo, remote https://github.com/tsatria03/RhythmRage-NVGT.git):** local includes live in `includes/` (renamed from `include/`); `rg.nvgt`'s six `#include "includes/..."` lines match. `bgt_compat.nvgt` and `sound_pool.nvgt` stay bare (resolved from the engine include path). Changelog lives at `docks/changelog.txt` (terse one-liners under "New in 1.0.").

**Sound packs & save location (updated 2026-09-14 — the `data/` folder was removed entirely):** the built voice/UI sound packs `sounds1.pack`/`sounds2.pack` now live at the **repo root** (previously `data/assets/`). `set_sound_storage`/`package.create` use `path+"sounds"+lang+".pack"` (rg.nvgt `main()` + `generate_soundpack()`, and `nopack()` in `includes/utils.nvgt`). The save file `rg.dat` is now written to a **fixed app-data path regardless of the `installed` flag**: `DIRECTORY_APPDATA+"/Oriol Gomez/rg/saves/rg.dat"` (previously the relative `data/saves/rg.dat`), created via `directory_create(DIRECTORY_APPDATA+"/Oriol Gomez/rg/saves")` in `main()` (NVGT `directory_create` = Poco `createDirectories`, so it makes the whole chain). The raw `sounds/` source folder (packed by `generate_soundpack()` via `find_files("sounds/*")`) and `packs/` remain in the ROOT. `.gitignore` excludes all binary media (`*.pack`, `sounds/`, `mypacks/`, `packs/`) so a fresh clone is code-only; `generate_soundpack()` then finds an empty `sounds/` and returns without building. Note: `.gitignore` lists `lib/` and `release/` but the actual folders are `libs/` and `releases/` (mismatch, currently empty so harmless).
