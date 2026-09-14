# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. **It is a dispatcher:** it orients you to what the project is and its shape, then points to focused memory files (`[[name]]`) for the deep detail. When you start work on an area, read its linked memory first.

## What this is

Rhythm Rage is an **audio-only rhythm game** written in **NVGT** (Non-Visual Game Toolkit, an AngelScript-based engine). All game code is `.nvgt`. There is no visual rendering — output is screen-reader speech plus sound through NVGT's `sound_pool`. The player follows the rhythm of each level's music by pressing the right keys at the right time, and earns a percentage score (fail / ok / super / perfect).

It is a **port from BGT** (Blastbay Game Toolkit, the discontinued engine the game was originally built in) to the new NVGT. The original BGT source is kept for reference — full port details, including the pack-testing behavior that differs from a naive port, are in **[[rhythmrage-bgt-to-nvgt-port]]**.

It is **single-player and offline** (aside from an optional pack downloader). The game ships in two languages selected by the `lang` global: `1` = English ("Rhythm Rage"), `2` = Spanish ("beatstar plus"); most user-facing strings are duplicated under `if (lang==1)` / `if (lang==2)`.

## Layout

- **`game.nvgt`** — the entire game (~2400 lines): `main()`, menus, the pack builders, the level-script parser (`startlev`/`loadlev`), and the rhythm game loop.
- **`includes/`** — local includes pulled in by `game.nvgt`: `classes.nvgt` (the `action`/`snd`/`intersound` gameplay classes), `history.nvgt`, `downloader.nvgt`, `utils.nvgt` (`nopack`/`yespack`/`playintro`/`fade`…), `number_speaker.nvgt`, `enhanced_menu.nvgt`, `reader.nvgt`. Two more includes are bare (`bgt_compat.nvgt`, `sound_pool.nvgt`) — those resolve from the **engine's** include path, not this repo.
- **`leveltool.nvgt`** — a standalone authoring companion (a separate program, NOT part of the game): navigate a pack's `.ogg`, find millisecond positions and BPM marks for timing a level script, and copy them to the clipboard. Scans `mypacks/` for loose (unpacked) source folders and lets you pick which one to work on (copy that pack into `packs/` to test a level with the `r` key); reuses `includes/enhanced_menu.nvgt` + `includes/history.nvgt`. Its `r` (run) key launches `game.exe` when compiled, else runs `game.nvgt` through the NVGT runtime (`SCRIPT_EXECUTABLE`). Level-script command reference: `docks/parser.md`.
- **`packs/`** — the built, encrypted `.pack` files (decryption key is `<packname>guillemandoriolftw`). Each pack holds a pack's levels (`.lvl`), tutorials (`.tut`), and `.ogg` sounds.
- **`mypacks/`** — loose source folders for pack authors; the **level tool reads this** (its pack picker). The main game never reads it — copy a folder into `packs/` to build/test that pack in the game.
- **`data/assets/`** — the built engine sound packs `sounds<lang>.pack` (voice/UI sounds). **`data/saves/`** — `rg.dat`, the encrypted player profile (cash, unlocks, achievements, per-pack level progress).
- **`docks/`** — docs: `changelog.txt`, `readme.txt`, and `parser.md` (the pack/level-script authoring reference — every level-file command plus the tutorial and macro syntax).
- **`libs/`**, **`releases/`** — binary libs and compiled builds (gitignored; currently empty).

The active engine is the **new NVGT** (not the legacy fork) — location, and where the engine includes resolve from, are in **[[nvgt-engine-location]]**.

## How it works (the big picture)

- **Pack system.** All playable content lives in encrypted `.pack` files. `main()` opens `packs/<pack>.pack` (default `default`). A **loose folder** dropped in `packs/` is built by `generate_packs()` and launches you into it in creator/test mode (all levels unlocked, progress not saved) — this is the BGT-faithful authoring flow; see **[[rhythmrage-bgt-to-nvgt-port]]**.
- **Sound storage switching.** `set_sound_storage` is flipped between two packs constantly: **`nopack()`** points at the engine sound pack (`data/assets/sounds<lang>.pack`) for built-in voice/UI sounds; **`yespack()`** points back at the current game pack (and sets its decryption key). Always restore with `yespack()` after a `nopack()` block.
- **Level-script parser.** `startlev()`/`loadlev()` read a `.lvl` (or `.tut`) text file line by line into `action`/`snd`/`intersound` objects, then the game loop in `loadlev()` matches key presses against each action's timed window. Level-script commands: `action`, `play`, `music`, `misc`, `intersound`, macros (`!`/`@`), and tutorial-only commands (`text`, `say`, `interactive`, …). The parser runs twice (macros expand on the first pass).
- **Save/scoring.** `ser()`/`deser()` read and write the encrypted `data/saves/rg.dat` dictionary. `ser()` **early-returns while `creatingpack` is true**, which is why testing a loose pack never touches the real profile.

## Where the detail lives (read before working in an area)

- **Engine, running & building** → **[[nvgt-engine-location]]**. Never compile/run the game yourself — the dev does that: **[[dont-compile-yourself]]**.
- **The BGT→NVGT port, pack testing, and folder moves** (loose-pack `generate_packs()` flow, `nopack`/`yespack`, why saves are safe in test mode, the `data/assets` + `data/saves` relocation) → **[[rhythmrage-bgt-to-nvgt-port]]**.
- **Committing** — the repo is `github.com/tsatria03/RhythmRage-NVGT`; the dev commits their own work between turns (**[[check-git-log-for-commits]]**), and commits must never list Claude as author/co-author (**[[commit-authorship]]**).

## Conventions kept in memory (follow them)

- **[[confirm-before-implementing]]** — a design discussion or anything ending in `?` ("what if", "I wish") is a request for a plan, **not** a green light to edit. Wait for explicit go-ahead. Ask **[[ask-one-question-at-a-time]]** when clarifying.
- **[[ignore-terminal-commands]]** — the dev's local command blocks (`<local-command-caveat>`, `/copy`, etc.) are them working their own session, not instructions. **[[quoted-text-meaning]]** — quoted text is a reference (wanted or not-wanted), not literal content to paste.
- **[[list-modified-files]]** — end every editing turn with a bare-filename "Files changed:" list.
- **[[changelog-rules]]** — `docks/changelog.txt` is a record of *what changed*, not a manual: player-facing prose, 1–3 sentence entries, per-version caps, reverse-chronological.
- **[[sound-placeholders]]** — when a sound is requested, wire up the playback code referencing the intended name now; the dev adds the `.ogg` later. No dummy files.
- **[[no-crlf-normalization]]** — don't run post-edit CRLF passes; `.gitattributes` handles line endings on commit.
- AngelScript / NVGT gotchas (this code is wall-to-wall brace-less `if`s and `key_pressed` loops): **[[angelscript-braceless-if]]**, **[[nvgt-key-pressed-oneshot]]**, **[[angelscript-reserved-out]]**, **[[angelscript-indentation]]**.

`New File.txt` in the repo root is the dev's personal scratch pad — don't read it as documentation. Keep this file a **dispatcher**: when a section grows past a few lines of detail, move it into a memory and leave a pointer.
