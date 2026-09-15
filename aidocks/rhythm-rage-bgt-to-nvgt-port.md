---
name: rhythm-rage-bgt-to-nvgt-port
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

**Layout (git repo, remote https://github.com/tsatria03/RhythmRage-NVGT.git; reorganized 2026-09-14):** source lives in **`src/`** (`rg.nvgt`, `lt.nvgt`, `lt.properties`, `includes/`), game data/run files in **`rg/`** (`packs/`, `mypacks/`, `sounds/`, `sounds1.pack`, `sounds2.pack`, `docks/`, `parser.md`, launchers). `rg.nvgt`'s `#include "includes/..."` lines resolve because they're relative to the script (src/). `bgt_compat.nvgt`/`sound_pool.nvgt` stay bare (engine include path). Changelog: `docks/changelog.txt`. Full run/build details → [[rhythm-rage-run-and-build]].

**Sound packs & save location (data/ folder removed):** the built voice/UI sound packs `sounds1.pack`/`sounds2.pack` live in **`rg/`** (were `data/assets/`, briefly repo root). `set_sound_storage`/`package.create`/`generate_soundpack()` use `path+"sounds"+lang+".pack"`, and `generate_soundpack()` scans `path+"sounds/*"` (the raw source in `rg/sounds/`) — see `nopack()` in `includes/utils.nvgt`. The save file `rg.dat` is written to a **fixed app-data path regardless of `installed`**: `DIRECTORY_APPDATA+"/Oriol Gomez/rg/saves/rg.dat"` (was the relative `data/saves/rg.dat`), created via `directory_create(DIRECTORY_APPDATA+"/Oriol Gomez/rg/saves")` in `main()`. `.gitignore` excludes binary media (`*.pack`, `rg/sounds/`, `rg/mypacks/`, `rg/packs/`), `releases/`, and the intermediate build bundles (`src/rg/`, `src/rg.app/`).
