# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. **It is a dispatcher:** it orients you to what the project is and its shape, then points to focused memory files (`[[name]]`) for the deep detail. When you start work on an area, read its linked memory first.

## What this is

Rhythm Rage is an **audio-only rhythm game** written in **NVGT** (Non-Visual Game Toolkit, an AngelScript-based engine). All game code is `.nvgt`. There is no visual rendering — output is screen-reader speech plus sound through NVGT's `sound_pool`. The player follows the rhythm of each level's music by pressing the right keys at the right time, and earns a percentage score (fail / ok / super / perfect).

It is a **port from BGT** (Blastbay Game Toolkit, the discontinued engine the game was originally built in) to the new NVGT. The original BGT source is kept for reference — full port details, including the pack-testing behavior that differs from a naive port, are in **[[rhythm-rage-bgt-to-nvgt-port]]**.

It is **single-player and offline** (aside from an optional pack downloader). The game ships in two languages selected by the `lang` global: `1` = English ("Rhythm Rage"), `2` = Spanish ("beatstar plus"); most user-facing strings are duplicated under `if (lang==1)` / `if (lang==2)`.

## Layout

The repo splits **source** from the **game data / run folder** (post-reorg):

- **`src/`** — all `.nvgt` source. **`rg.nvgt`** (formerly `game.nvgt`; → `rg.exe`) is now just the **entry point**: globals, `main()`, and the menu callbacks (`checkmenu`/`menu2`); it pulls in every local include via the wildcard `#include"includes/*.nvgt"` (plus the two bare engine includes `bgt_compat.nvgt` and `sound_pool.nvgt`, which resolve from the **engine's** include path). **`lt.nvgt`** + `lt.properties` is the standalone level tool (formerly `leveltool.nvgt`; → `lt.exe`) — it uses *targeted* includes (`enhanced_menu`, `history`), NOT the wildcard, so it stays independent of the game globals.
  **`includes/`** now holds the split-out game code plus the shared libs:
  - `game.nvgt` — the bulk of gameplay: the `startlev`/`loadlev` level-script parser, the rhythm game loop, the store/change-pack/downloader browsers (`store`/`packloop`/`packloop2`/`getpacks`), and the first-letter nav helpers (`next_first_letter`/`preview_pack`).
  - `menu.nvgt` — the main menu + level select (`start()`/`startgame()`).
  - `packgen.nvgt` — pack + sound-pack building (`generate_packs()`/`generate_soundpack()`).
  - `classes.nvgt` (the `action`/`snd`/`intersound` classes), `enhanced_menu.nvgt` (menu class — arrow + first-letter nav), `history.nvgt`, `reader.nvgt`, `number_speaker.nvgt`, `downloader.nvgt`, `utils.nvgt` (`nopack`/`yespack`/`playintro`/`fade`…).
  NVGT's builder de-dupes includes by absolute path, so files pulled both by the wildcard and by an explicit `#include` compile only once.
- **`rg/`** — the game's data/run folder (ships alongside the compiled exe). All runtime data lives under **`data/`**: `data/packs/` (built encrypted `.pack` content — levels `.lvl`, tutorials `.tut`, `.ogg`; decryption key `<packname>guillemandoriolftw`), `data/assets/` (`sounds1.pack`/`sounds2.pack`, the built voice/UI sound packs, one per language), `data/saves/` (`rg.dat`, the portable profile). Also `mypacks/` (loose author sources — the **level tool** reads these, the game never does), `sounds/` (raw source for building the sound packs into `data/assets/`), `docks/` (player-facing docs, split into `english/` and `spanish/` subfolders — includes the level-script authoring reference `docks/english/parser.md`), and the Python launchers `rg.py`/`lt.py`. No `lib/` — the compiler supplies the platform libraries (**[[nvgt-090-miniaudio-not-bass]]**).
- **`build/`** — `tools.py`/`tools.bat`/`tools.ini`: a menu with git helpers plus **Compile** and **Package** for Windows + Mac.
- **`releases/`** — gitignored build output: `windows/RhythmRage_windows/rg/` (game + `lt.exe` + empty `mypacks/`), `mac/RhythmRage_mac/rg.app`, and `archives/*.zip`.
- **`aidocks/`** (repo root) — these memory files. Player-facing docs live under **`rg/docks/`**, split by language: `english/` (`changelog.txt`, `readme.txt`, `credits.txt`, `todo list.txt`, `parser.md`/`parser.html`) and `spanish/` (`cambios.txt`, `leeme.txt`, `creador.md`/`creador.html`). The level-script reference is `rg/docks/english/parser.md`.

The level tool (`lt.nvgt`) is a **separate authoring program, NOT part of the game**: it plays a pack's `.ogg` and finds millisecond/BPM marks for timing a level script, scanning `mypacks/` for source folders; its `r` key launches the game. It ships **Windows-only**.

Running from source, the compiled layout, and the compile/package pipeline → **[[rhythm-rage-run-and-build]]**. The save file is the portable `path+"data/saves/rg.dat"` (`rg/data/saves/rg.dat` from source; next to the exe when portable; under `%APPDATA%\Oriol Gomez\rg\` when installed). Active engine + runtime → **[[nvgt-engine-location]]** (the new NVGT, not the legacy fork).

## How it works (the big picture)

- **Pack system.** All playable content lives in encrypted `.pack` files under `rg/data/packs/` (paths built from the `path` prefix — `path+"data/packs/…"`). `main()` opens the current `.pack` (default `default`). A **loose folder** dropped in `data/packs/` is built by `generate_packs()` and launches you into it in creator/test mode (all levels unlocked, progress not saved) — this is the BGT-faithful authoring flow; see **[[rhythm-rage-bgt-to-nvgt-port]]**.
- **Sound storage switching.** `set_sound_storage` is flipped between two packs constantly: **`nopack()`** points at the built-in voice/UI sound pack (`path+"data/assets/sounds<lang>.pack"`, i.e. `rg/data/assets/sounds<lang>.pack`); **`yespack()`** points back at the current game pack (and sets its decryption key). Always restore with `yespack()` after a `nopack()` block.
- **Level-script parser.** `startlev()`/`loadlev()` read a `.lvl` (or `.tut`) text file line by line into `action`/`snd`/`intersound` objects, then the game loop in `loadlev()` matches key presses against each action's timed window. Level-script commands: `action`, `play`, `music`, `misc`, `intersound`, macros (`!`/`@`), and tutorial-only commands (`text`, `say`, `interactive`, …). The parser runs twice (macros expand on the first pass).
- **Save/scoring.** `ser()`/`deser()` read and write the encrypted player profile at `path+"data/saves/rg.dat"` — a **portable** path relative to `path`, so the save travels with the game folder (from source: `rg/data/saves/rg.dat`; portable: next to the exe; installed: under `%APPDATA%\Oriol Gomez\rg\`). `ser()` **early-returns while `creatingpack` is true**, which is why testing a loose pack never touches the real profile.

## Where the detail lives (read before working in an area)

- **Engine & runtime location** → **[[nvgt-engine-location]]** (the miniaudio NVGT at `C:\nvgt2\nvgt2.exe`). **Running from source & the build/package pipeline** → **[[rhythm-rage-run-and-build]]**. Never compile/run the game yourself — the dev does that: **[[dont-compile-yourself]]**.
- **The BGT→NVGT port & pack testing** (loose-pack `generate_packs()` flow, `nopack`/`yespack`, why saves are safe in test mode, sound-pack + save relocation) → **[[rhythm-rage-bgt-to-nvgt-port]]**. Compiled libs / miniaudio → **[[nvgt-090-miniaudio-not-bass]]**.
- **Known open bugs** (from the 2026-09-22 full code evaluation, with status) → **[[known-bugs-2026-09-evaluation]]**. Check it before fixing or re-reporting a bug.
- **Where memories go** → all project memories live in **`aidocks/`**, indexed by `aidocks/MEMORY.md`: **[[memory-lives-in-aidocks]]**.
- **Committing** — the repo is `github.com/tsatria03/RhythmRage-NVGT`; the dev commits their own work between turns (**[[check-git-log-for-commits]]**), and commits must never list Claude as author/co-author (**[[commit-authorship]]**).

## Conventions kept in memory (follow them)

- **[[confirm-before-implementing]]** — a design discussion or anything ending in `?` ("what if", "I wish") is a request for a plan, **not** a green light to edit. Wait for explicit go-ahead. Ask **[[ask-one-question-at-a-time]]** when clarifying.
- **[[ignore-terminal-commands]]** — the dev's local command blocks (`<local-command-caveat>`, `/copy`, etc.) are them working their own session, not instructions. **[[quoted-text-meaning]]** — quoted text is a reference (wanted or not-wanted), not literal content to paste.
- **[[list-modified-files]]** — end every editing turn with a bare-filename "Files changed:" list.
- **[[english-docks-only]]** — edit only `rg/docks/english/`; never touch or offer to sync `rg/docks/spanish/`.
- **[[changelog-rules]]** — `docks/english/changelog.txt` is a record of *what changed*, not a manual: player-facing prose, 1–3 sentence entries, per-version caps, reverse-chronological.
- **[[sound-placeholders]]** — when a sound is requested, wire up the playback code referencing the intended name now; the dev adds the `.ogg` later. No dummy files.
- **[[no-crlf-normalization]]** — don't run post-edit CRLF passes; `.gitattributes` handles line endings on commit.
- AngelScript / NVGT gotchas (this code is wall-to-wall brace-less `if`s and `key_pressed` loops): **[[angelscript-braceless-if]]**, **[[nvgt-key-pressed-oneshot]]**, **[[angelscript-reserved-out]]**, **[[angelscript-indentation]]**.

`New File.txt` in the repo root is the dev's personal scratch pad — don't read it as documentation. Keep this file a **dispatcher**: when a section grows past a few lines of detail, move it into a memory and leave a pointer.
