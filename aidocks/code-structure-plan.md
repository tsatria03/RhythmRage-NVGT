---
name: code-structure-plan
description: The agreed code-structure refactor plan (2026-09-23), five ranked refactors with a concrete recommended implementation, risks, and test plan for each, plus per-item status. Read before restructuring any of startlev/loadlev, the list browsers, the bilingual strings, or screen navigation.
metadata:
  node_type: memory
  type: project
---

Structure review from 2026-09-23. **Nothing implemented yet.** The dev asked for the plan to be recorded, and each item needs an explicit go-ahead first ([[confirm-before-implementing]]). Update the **Status** line of an item as it lands.

**Ground rules for every item**
- These are refactors: **no player-visible change**, so **no changelog entry** ([[changelog-rules]]).
- **One item per commit**, so each gets its own test pass. The dev compiles and tests ([[dont-compile-yourself]]).
- Keep the code's style: brace-less `if`s ([[angelscript-braceless-if]]), one `key_pressed` read per key per frame ([[nvgt-key-pressed-oneshot]]), a `wait()` at the top of any new input loop ([[nvgt-busy-loop-needs-wait]]).
- Line numbers below are from 2026-09-23 and will drift. Find code by function name.

## Measurements (2026-09-23)

`startlev()` ~1,090 lines · `loadlev()` ~370 (level loop plus score screen) · `start()` ~170 · 111 globals in `rg.nvgt` · 51 calls among `start`/`startgame`/`startlev`/`loadlev`, none of which return · 6 hand-written list browsers · 144 `lang==1`/`lang==2` pairs.

## Order (by risk against benefit)

1 → 2 → 3 → 4 → 5. Items 1 and 2 only move code around (test: "every pack still loads and plays the same"). Items 4 and 5 change code players interact with directly and need a careful playthrough.

---

## 1. One key-name lookup: `key_from_name()`
**Status:** not started. **Risk:** very low. **Benefit:** removes ~80 duplicated lines. The allowed-keys error message becomes accurate.

**Problem.** The ~40-line `if/else` chain mapping a key name to a `KEY_*` code appears twice in `startlev()`: for `action … key=<name>` and for `intersound … key_<name>`. Both error messages still say "You can use space, enter, right, left, up or down, for now", which is years out of date.

**Recommended fix.**
- In `rg.nvgt`, add `string[] akeynames={"enter","space","up","down","right","left","1",…,"0","a",…,"z"};` in **exactly the same order** as the existing `int[] akeys` (which is `KEY_RETURN,KEY_SPACE,KEY_UP,KEY_DOWN,KEY_RIGHT,KEY_LEFT,KEY_1…KEY_9,KEY_0,KEY_A…KEY_Z`). That keeps one list of allowed keys.
- `int key_from_name(string name)` returns `akeys[i]` where `akeynames[i]==name`, else `0`.
- Both callers become `key=key_from_name(what[1]); if (key==0) { alert(…); exit(); }`. The alert should list the real set: "enter, space, the arrow keys, a to z, or 0 to 9".
- Keep `iskey()` as it is (it already uses `akeys`).

**Test.** Every pack loads. A level using letter and number keys plays. `key=banana` shows the new alert. The extension1 interactive tutorial (`key_enter`) still works.

## 2. Split `startlev()` into per-command handlers, and `loadlev()` into loop plus result
**Status:** not started. **Risk:** medium (large move, but no logic change). **Benefit:** biggest. Almost every bug found on 2026-09-22 was in `startlev()`.

**How `startlev()` is shaped today (must be preserved exactly).**
- Setup: resets, the play/tutorial/perfect-run/soundtrack choice menu, `replaying` handling, loading the file.
- `for (uint i=1;i<3;i++)`: **two parser runs**. The second run processes only `macrostuff` (expanded macros). On the second run, the `if (tutorial)` block replays `tutes` before the empty-string `break`. **That's intentional** (Oriol Gomez's design, see [[known-bugs-2026-09-evaluation]] #3). Don't "fix" it.
- Inside, **two separate else-if chains** per line:
  - chain A: `play` (tutorial), `stopsounds`, `wait`, `interactive`, `intersound`, `playwait`
  - chain B (starts `if (words[0]=="text"…)`): `text`, `misc`, `action`, `seek`, `debug`, `play` (level), `music` (tutorial), `say`, `fade`, `exit`, `stop`, `music` (level), `!`/`@` macros
  - Commands are split by `words[0]` plus the `tutorial` flag, and no command runs in both chains.
- Per-line setup before the chains: the tutorial q/escape checks (which can call `skip_tutorial()`/`quit_tutorial()` and `return` out of `startlev`), splitting `words`, `curline=i+1`, and pulling `ach` out of the rest of the line.
- Control-flow quirks the handlers must keep:
  - tutorial timed `play` **re-runs the same line** (`wait(3); i--; continue;`)
  - `interactive` setup and `intersound` end in `continue`
  - the interactive run loop can **return out of `startlev()`** on skip/quit
  - `music name=` **changes `ln`**, the name passed to `loadlev()`
  - `music` sets `lev_vol`
  - macros add to `macrostuff`

**Recommended fix.**
- Add a small `class parse_state { string[] lines; string ln; int lev_vol; string macrostuff; string ach; }`, created once per `startlev()` call, instead of adding more globals.
- Each command gets `int parse_<cmd>(string[]@ words, parse_state@ ps)` returning a code: `PARSE_NEXT` (0, go on), `PARSE_RERUN` (1, the caller does `i--`), or `PARSE_ABORT` (2, the caller `return`s because a skip or quit already left for another screen).
- The loop body becomes: per-line setup, then a lookup on `words[0]` and `tutorial` that calls the handler, then act on the code. **Keep chain A before chain B**, and keep the `continue` behavior.
- Suggested handlers: `parse_action`, `parse_play_level`, `parse_play_tutorial`, `parse_misc`, `parse_debug`, `parse_music_level`, `parse_music_tutorial`, `parse_macro`, `parse_interactive`, `parse_intersound`, and one `parse_tutorial_simple` for `text`/`say`/`wait`/`playwait`/`stopsounds`/`fade`/`exit`/`stop`/`seek`.
- `check_value()`/`check_parts()` (added 2026-09-22) move with their commands unchanged.
- **`loadlev()`:**
  - Move the score screen (everything after `//calculate here`: the calc ticks and `skippable_wait`, the `well`/`val` tier, the jingle loop, `set_level`, `win_pack`) into `void show_result()`.
  - Merge the **two near-identical escape branches** (listen-only modes versus a real playthrough) into one `handle_level_pause()` that calls `pause_menu(perfectrun or musiconly)`. It returns resume, quit or restart, and the loop acts on the result. This also adds the `return` that's missing after the quit→`startgame(1)` call.

**Test.** Every level and tutorial in every pack plays identically:
- hit, early, late and fail sounds; the score; the jingle
- macros, `@` references, `debug mode`/`seek` in creator mode
- the extension1 interactive tutorial, including skip and quit from its pause menu
- perfect run and soundtrack pause
- restart from the pause menu

Also test a deliberately broken script for each of the new error alerts.

## 3. One helper for bilingual messages
**Status:** not started. **Risk:** low per edit, but ~144 edits. **Benefit:** a language can't be forgotten, and the code gets shorter.

**Problem.** Every message is written twice, as `if (lang==1) X("en"); if (lang==2) X("es");`.

**Recommended fix.** Add to `utils.nvgt`:
- `void say2(string en,string es)` → `rd.say(lang==2?es:en);`
- `void add2(string en,string es)` → `rd.add(lang==2?es:en,false,true);` (the common flags; keep the full form wherever the flags differ, e.g. `achprizes` uses `true,true`)
- `void alert2(string title,string en,string es)`
- `string tr(string en,string es)` → returns the right one, for string building (`inst`, `lock`, the result `message`, `stre`)

Convert **mechanically, one file per commit**, starting with `menu.nvgt` then `game.nvgt`.

**Watch for:**
- **The two-line style** (`if (lang==1)` alone, the message on the next line; see `ser()` in `game.nvgt` and `lt.nvgt` ~159-170). It converts the same way, but check the pairing by eye.
- **Unequal pairs.** Only convert pairs where both lines call the same function with the same extra arguments. Leave anything else, like a pair where only one side exists or the arguments differ, and note it.
- **Brace-less guards.** A scan on 2026-09-23 found **no** brace-less `if` directly above a language pair. Re-check before converting, because merging two guarded lines into one would change what the guard covers.
- `lt.nvgt` doesn't include `utils.nvgt` (it uses its own targeted includes), so give it its own copy of the helpers or leave it alone.
- A full translation table (`tr("key")` plus per-language files) is only worth it if a **third language** is ever added. Don't build it now.

**Test.** Browse every menu in English and in Spanish. Every message must still be spoken in the right language.

## 4. One shared list browser
**Status:** not started. **Risk:** medium, because small differences in what gets spoken and when are noticeable by ear. **Benefit:** replaces ~6×60 lines of copies.

**The six browsers and how they differ (all must be kept):**

| Browser | Focus behavior | Enter | After enter | Extra keys |
|---|---|---|---|---|
| `store`/`packloop` | speaks the name **and previews the pack's `name` sound** (storage switch, see `preview_pack`) | buy (−1000) | leaves to `start()` | tab = credits; escape also destroys pool + music |
| `packchange`/`packloop2` | speaks + previews | switch pack | leaves to `start()` | |
| `getpacks` | speaks | download (beep progress; escape aborts the download) | **stays**, the list shrinks, "no more" ends it | |
| `compilepacks` | speaks | compile (beep progress) | stays, list shrinks | |
| `decompilepacks` | speaks | decompile | stays, list shrinks | |
| `testpacks` | speaks | build the temp test pack | leaves to `startgame(1)` | |

Common to all: the starting position is `-1` (nothing focused until the first arrow press, and up from `-1` goes to the last item); down/right and up/left both navigate with `key_repeating` and wrap; first letter jumps via `next_first_letter()`; `get_characters()` clears typed input when the browser opens; `wait(5)` each time around.

**Recommended fix.** A `class list_browser` in a new `includes/browser.nvgt`:
- `string[] items; int pos=-1; bool preview_packs=false;`
- `int run()` returns the index chosen with enter (or −1 for escape) and does the navigation, speaking, first-letter jumping and optional preview.
- The caller's own loop does the work on enter and decides whether to go again (shrinking list) or leave. So `getpacks`/`compile`/`decompile` loop around `run()`, while `store`/`packchange`/`testpacks` call it once.
- Store's tab-for-credits goes in an optional `funcdef void browser_key(int key)` hook, like `enhanced_menu`'s callback.

**Considered but not recommended:** using `enhanced_menu` for these. It would change the menu sounds, the opening announcement and the starting position (it opens focused on an item, not at −1), all of which players would hear.

**Test.** Each of the six browsers, by ear, against the old build: the first arrow press, wrap-around in both directions, first letter, the pack-name preview (store and change pack), tab for credits, escape, the list shrinking (download, compile, decompile), empty-list messages.

## 5. Screens return instead of calling each other
**Status:** not started. **Risk:** highest. **Benefit:** stops the call stack growing and removes a class of missing-`return` bugs. **Recommendation: do last, or skip.** NVGT's `max_stack_size` defaults to 0 (unlimited), so the current setup works in practice.

**Problem.** `start` → `startgame` → `startlev` → `loadlev` → `startgame` → … never return, so each level played leaves several unfinished calls on the stack. Code after one of these calls only runs if something returns. The 2026-09-22 review found the pause-menu quit branches in `loadlev()` calling `startgame(1)` with no `return`.

**Recommended fix (incremental; each step can ship on its own):**
1. `main()`: replace the final `start();` with `while (true) start();`. This does nothing yet, because `start()` never returns.
2. Sub-screens reached from the main menu (`store`, `packchange`, `getpacks`, `compilepacks`, `decompilepacks`, `testpacks`, `achprizes`, `achclear`, `calibrate_keyboard`, `change_language`) change their final `start(); return;` to just `return;`. `start()`'s `if (o==…)` branches already fall through to its end, so it returns to the loop, which calls `start()` again. Do one sub-screen per step.
3. Level flow: add a global `string next_screen` (`"menu"`, `"select"`, `"level"`) and make `startgame`/`startlev`/`loadlev` set it and return, with the `main()` loop choosing what to run. The state flags must keep their meaning across the handoff: `replaying`, `restarted`, `testing`, `pretestpack`, `levpos`, `skipleveljingle`, `mp`, `question_state`, `perfectrun`, `musiconly`, `last`, `okval`. The test-pack teardown at the top of `start()` must still run whenever the menu is reached.
4. `com!=""` (a level run from the command line or the level tool) must still `exit()` where it does today.

**Test.** Every route between screens: menu → each sub-screen → back; level select → level → result → select; pause-menu quit, restart and resume; tutorial skip and quit; perfect run; soundtrack; ending a test pack (with the confirmation); a level launched from the level tool's `r`; language change; restart.

## Not planned

- **111 globals:** too spread out to fix directly. Items 2 and 4 move some of them into `parse_state` and `list_browser` as a side effect. Don't do a separate globals pass.
- **Timing item C** (judge each press against the nearest note) is gameplay, not structure. It's tracked in [[known-bugs-2026-09-evaluation]].
