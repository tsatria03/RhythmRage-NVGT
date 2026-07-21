# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. **It is a dispatcher:** it orients you to what the project is and its shape, then points to focused memory files (`[[name]]`) for the deep detail. When you start work on an area, read its linked memory first.

## What this is

CaveDefender is an **online**, audio-only game written in **NVGT** (Non-Visual Game Toolkit, an AngelScript-based engine). All code is `.nvgt`. There is no visual rendering — output is screen-reader speech plus HRTF spatial audio through NVGT's `sound_pool`.

It is a **client/server** game: connect to the server, log into an account, chat with other players, and walk around a shared map. Map objects are spawned through a custom game-engine DLL. The chat-center milestone is complete (accounts, public/private/local/staff/team chat, slash commands, networked player positions with locator beacons, live spatial voice chat). Gameplay is **Wallbreaker** (see [[game-vision-wallbreaker]]) in three modes, all built and feature-complete: **PVE** (defend four walls from enemy bots), **EVP** (attack the walls from outside while builder bots defend — [[game-mode-evp]]), and **PVP** (humans on both sides, one team attacking, one defending — [[game-mode-pvp]]).

**Heritage note:** the folder layout and several conventions were borrowed from the **SimpleFighter** project (a separate, *offline* map-builder game), so the structure looks familiar — but CaveDefender is online and very different. Do **not** assume SimpleFighter mechanics exist here (no map builder, no `.sif` format).

## Layout

Repo root holds three top-level folders, with **source and assets deliberately separated**:
- **`src/`** — the code only. `src/client/` (entry `cfc.nvgt`) and `src/server/` (entry `cfs.nvgt`), each with `includes/`. **No assets here.**
- **`cf/`** — the runnable game's assets and launchers: `cf/client/` (`lib/`, `sounds/`, `docks/`, `cfc.py`) and `cf/server/` (`data/`, `docks/`, `lib/`, `cfs.py`).
- **`build/`** — the unified build/release pipeline (`tools.py` via `tools.bat`); config in `build/tools.ini` + `~/.game_tools/tools.ini`; version in `build/version.txt`.
- **`release/`** — compiled builds + the two `.7z` archives.

Each launcher runs the `src/<side>` script but with **cwd set to `cf/<side>/`**, so every cwd-relative path (`lib/…`, `sounds/…`, `docks/…`, `data/…`) resolves against `cf/<side>/`; `build/tools.py` copies assets into the bundle at compile time (no `#pragma asset`). Full path map and the runtime/build split: **[[path-conventions]]**.

The engine is the **pinned legacy NVGT fork** at `C:\nvgt2\nvgt.exe`; upstream NVGT is incompatible — **[[engine-pinned-to-nvgt2]]**.

## Client / server split

Two halves of one game, separate codebases sharing only a message protocol and an encryption key:
- **Client** (`src/client/`) — presents the UI, plays sounds, manages the local player and message buffers, talks to the server.
- **Server** (`src/server/`) — holds the connected-player roster and account store, validates logins, broadcasts chat, runs admin commands.

Each has its own `net.nvgt` with near-identical `send()`/`get_event_message()` but mirror-image `netloop()`s (client presents; server dispatches).

## Where the detail lives (read before working in an area)

- **Running & launchers** (how the game starts/compiles, the client `errors.txt` watch, no test suite) → **[[launchers-and-running]]**. Never compile yourself: **[[dont-compile-yourself]]**.
- **Distribution boxing** (Enigma Virtual Box, the `.evb` files + `gencfcevb.py`) → **[[enigma-boxing]]**.
- **Networking** (enet, the 4 channels, `rscs123` encryption, the space-delimited message contract) → **[[networking-protocol]]**. Keepalive during blocking UI: **[[blocking-ui-network-keepalive]]**. IPv4/VPN gotcha: **[[nvgt-ipv6-networking]]**.
- **Accounts** (the `data/players/<username>/` folder-per-account, Argon2id passwords, ranks & command gating, owner aliases, moderation, command targeting) → **[[accounts-system]]**. Nicknames: **[[nicknames]]**.
- **The custom game engine DLL** (`GameEngine64.dll`, its wrapper, the patched `library::load()`) → **[[game-engine-dll]]**. NVGT C++ source location: **[[nvgt-engine-source-location]]**.
- **Include tree & file map** (the glob-include model + what each client/server `.nvgt` owns) → **[[include-tree]]**.
- **Audio & sounds** (the `sound_pool`/HRTF model, the `cf/client/sounds/` folder layout) → **[[audio-and-sounds]]**. No sound packs: **[[no-sound-pack-support]]**.
- **Player-facing docs** (client `docks/`, the server-authoritative `/help` and `/rules`) → **[[docks-and-help]]**.
- **Chat channels** (Global `/`, Local `\`, Staff `'`, Team `;`) → **[[chat-channels]]**. Crash-string filter: **[[screen-reader-crash-filter]]**.
- **Version** — single source of truth is **`build/version.txt`**; it's mirrored into `src/<side>/includes/version.nvgt` by both launchers and the build (never hand-edit those). Details in **[[changelog-rules]]**.

## Conventions kept in memory (follow them)

- **[[confirm-before-implementing]]** — a design discussion or a question (anything ending in `?`, "what if", "I wish") is a request for a plan, **not** a green light to edit. Wait for explicit go-ahead.
- **[[ignore-terminal-commands]]** — the user's local shell blocks (`<local-command-caveat>`/`<bash-input>`/`<command-name>`, e.g. `cls`, `/compact`) are the user working their own terminal, not instructions. Never act on them unless explicitly asked.
- **[[list-modified-files]]** — end every editing turn with a bare-filename "Files changed:" list (tagged client/server). Then a **[[relaunch-notice]]**.
- **[[one-sentence-game-messages]]** — in-game feedback messages are exactly one sentence.
- **[[new-command-checklist]]** / **[[command-parser-conventions]]** — adding/changing a slash command touches all five together (client router, server handler, both `/help` pages, changelog, identical wire strings); `comparse()` is a router, not a local executor.
- **[[changelog-rules]]** — changelog is a record of *what changed*, not a manual: player-facing prose, sentence/entry caps, reverse-chronological.
- **[[input-prompt-form-vs-dialog]]** — one input field → a virtual dialog; more than one → a real tabbable `audio_form`.
- **[[use-dlgmessage]]**, **[[menus-say-canceled]]**, **[[no-crlf-normalization]]**, **[[sound-placeholders]]**, **[[delete-completed-tasks]]** — smaller standing rules.
- AngelScript gotchas: **[[angelscript-braceless-if]]**, **[[angelscript-reserved-out]]**, **[[nvgt-key-pressed-oneshot]]**, **[[angelscript-indentation]]**, **[[nvgt-sound-preload-cache]]**.

`New File.txt` in the repo root is the dev's personal scratch pad — don't read it as documentation (though the dev sometimes asks you to write post drafts there). Keep this file a **dispatcher**: when a section grows past a few lines of detail, move it into a memory and leave a pointer (**[[claudemd-length]]** — stay under 40k chars).
