---
name: known-bugs-2026-09-evaluation
description: Open bug list from the full code evaluation on 2026-09-22 — save prefix-match mixup, tutorial busy-wait, preload early return, parser crash-on-typo paths, plus gameplay/structure risks. Check here before fixing or re-reporting a bug.
metadata:
  node_type: memory
  type: project
---

Bugs found in a full read of `src/` on **2026-09-22** (nothing fixed yet at time of writing). Line numbers are from that date and will drift — find by the function/snippet named. When one gets fixed, mark it **FIXED (date)** here rather than deleting it, and check `git log` first ([[check-git-log-for-commits]]).

## Bugs (most important first)

1. **FIXED (2026-09-22)**: all three lookups now go through `find_level_entry()`, which compares the name field exactly. Saves that were already corrupted aren't repaired. Logged in the 1.4 changelog. Original report: **Save records mix up levels whose names share a prefix — hits shipped packs.** `set_level` / `get_level` / `get_percent` (`includes/game.nvgt` ~1976, ~2002, ~2020) match an entry with `string_left(lvl[i],level.length())==level`, a *prefix* test. Packs have `01`/`01a`, `10`/`10a`, `05`/`05a`/`05b`/`05c` (retro_world, hardcore, default). Scenario: pass `01`, pass `01a`, then improve `01` — `set_level` removes the old `01` entry and appends the new one at the END, so `get_level("01")` now finds `01a===…` first and shows 01a's rating; the next improvement to `01` deletes 01a's record. Fix: compare the part before the first `===` exactly.
2. **FIXED (2026-09-22)**: `wait(3)` added before `i--; continue;`. Logged in 1.4. Original report: **Tutorial timed `play` busy-waits with no `wait()`.** In `startlev()`, `play <sound> <time>` while `tutem.position` hasn't reached the time does `i--; continue;` (~1015-1021) with no yield — q/escape are dead during the wait and a CPU core is pinned. Same trap as [[nvgt-busy-loop-needs-wait]].
3. **Tutorial start sound likely replays at tutorial end.** The parser's two-pass loop (`for (uint i=1;i<3;i++)`, ~963): on pass 2 `tutorial` is still true, so `tutes.play_wait()` (~966) runs again before the empty-string `break`, then `loadlev` plays `tut_end`. Possibly BGT-faithful — confirm with the dev before "fixing".
4. **`preload_add` only preloads the first of a comma list.** `includes/classes.nvgt` ~30: `return true;` sits inside the per-file loop, so `name=a,b` never preloads `b` (loaded on first play → possible mid-level hitch). The duplicate-check `return false` also aborts the rest of the list.
5. **Level-script typos crash (index out of range) instead of showing the friendly alert** — author-facing only:
   - `action`/`play` time-error alerts print `lines[curline]` (~1371, ~1630): that's the NEXT line, and out of range on the last line.
   - Macro branch reads `words[1]`/`words[2]` (~1760-1761) before the `words.length()` checks.
   - Tutorial `seek` (~1593) tests `string_to_number(words[2])` when `words.length()==2` → always crashes. Undocumented and unused by any pack (latent).
   - `words[0]=="!" or words[0]=="@" && !tutorial` (~1759): `&&` binds tighter, so `!` macros are processed inside tutorials too.

6. **FIXED (2026-09-22)**: `wait(3)` at the loop top, escape cancels (stops music, no mark saved), both removals use index 0, and the average is `sum/length`. Logged in 1.4. Original report: **Level tool tap tempo busy-loops with no `wait()` and likely hangs.** `lt.nvgt` ~306-340 (b → "tap tempo"): the `while(true)` loop only ends after 10 **h** taps, but never yields. Per [[nvgt-busy-loop-needs-wait]], `key_pressed(KEY_H)` then never fires, so the music loops forever at 100% CPU and the tool must be force-closed. It also has no escape check. Same loop, math slips: `remove_at(0); remove_at(1);` drops taps 1 and 3 (the list shifts), and `round(avg/taps.length()-1,0)` subtracts 1ms instead of dividing by `length()-1`.

**Busy-loop audit (2026-09-22):** every `while`/`continue`-driven loop in `src/` (game, shared includes, `lt.nvgt`) was checked. Only #2 and #6 lack a yield. The enhanced_menu `continue`s are one-shot per key press and reach `wait(5)` next pass, so they're fine.

## Gameplay / robustness risks (design calls — ask the dev before changing)

- **"late" almost never fires.** With `timewindow=150`: early is d∈[-374,-85], hit (-85,75), late only [75,85), then timeout-fail at +85. Late presses read as fails.
- **Keyboard delay widens instead of shifting.** `timewindow=150+keycal` (~859) widens both sides; a latency offset should shift the target time. `calibrate_keyboard()` also only records presses *after* the beep (`press.elapsed<200`), so the average is biased late.
- **Wrong-key presses are free** — `action.badkey()` plays the miss sound but never increments `bad`. May be intended leniency.
- **Non-atomic save.** `ser()` writes `rg.dat` in place (and is called on every page up/down repeat in menus, `rg.nvgt` ~113); a corrupt file makes `deser()` silently start a fresh profile. Safer: write temp + rename.
- **Screens navigate by recursion, never returning** (`start`→`startgame`→`startlev`→`loadlev`→`startgame`…). NVGT's default `max_stack_size` is 0 (unlimited), so it's slow growth, not a crash. Fragile spot: the pause-menu `quit` branches in `loadlev` call `startgame(1)` with no `return` (~574, ~601), unlike `restart` — safe only because every path ends in `exit()`.

## Maintainability notes (not bugs)

144 paired `if (lang==1)`/`if (lang==2)` blocks (a string table would help; player-facing typos "Pitty", "sintax"); the ~40-line key-name→`KEY_*` chain is duplicated (~1192 and ~1402); the arrow/first-letter pack browser is copy-pasted ~5×; `startlev()` is ~1,070 lines.

Doc drift: CLAUDE.md says packs live in `rg/data/packs/`, but the code uses `packdir` = `%APPDATA%/Oriol Gomez/RhythmRage/packs/` (`rg.nvgt` ~262), and `generate_packs()` scans there. Related: [[rhythm-rage-bgt-to-nvgt-port]], [[angelscript-braceless-if]].
