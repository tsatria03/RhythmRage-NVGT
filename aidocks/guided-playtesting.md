---
name: guided-playtesting
description: When the dev playtests a change, walk them through it one step per message (which pack, which level by its spoken title, what to do, what to report), and track the checklist and results here.
metadata:
  node_type: memory
  type: feedback
---

When a change needs playtesting, guide the dev **one step per message**: name the pack, the level by the **title the game speaks** (the first line of the `.lvl`, e.g. 01 = "rhythm test", not just the file number), what to do, and what to report back. Wait for their result before giving the next step. Explain how a level is played if it's unfamiliar; read its `.tut`/`.lvl` to do that.

**Why:** the dev asked for "one step at a time" (2026-10-24) after a multi-item test list, didn't know which level "01" meant, and needed the pipes mechanics spelled out. They asked for this walkthrough to be kept in aidocks.

**How to apply:** record each step's result below as it comes in, so a later session can resume mid-checklist. Pick test levels by measuring the pack sources in `rg/mypacks/` (same-key gaps, key count) rather than guessing. Prefer the slowest level that still exercises the change: the dev found hardcore "remix 1" too fast (2026-10-24). For "should play the same as before" checks, use a level the dev has already played and has a score for. A level they've never played gives no baseline. Related: [[ask-one-question-at-a-time]], [[known-bugs-2026-09-evaluation]].

## Current checklist: refactor item 1, one key-name lookup (no player-visible change), started 2026-10-24

1. Default "rhythm test" (01): enter notes still register. Result: PASSED (2026-10-24), perfect.
2. Retro world "rhythm & spell" (05): letter keys still register. Result: PASSED (2026-10-24). All keys worked. Score 55% (was 79% before the wrong-key fix), from misspellings: a wrong letter that isn't corrected now costs two misses (wrongkey + the note's fail). This was raised with the dev, who put the score down to their own unfamiliarity with the level and kept the current behavior. Don't raise it again unless they ask.
3. Extension1 "ghost buster" (01): the interactive tutorial part, which uses intersound key_ names, still responds to its keys. Result: PASSED (2026-10-24).
4. Optional, only if the dev wants it: a throwaway mypacks copy with key=banana, run via test a pack, should show the new "key not recognized ... You can use enter, space, the arrow keys..." alert. Ask before creating any folder in mypacks. The dev said yes. Created `rg/mypacks/keytest/` (2026-10-24): default 01 + its sounds + the pack-wide sounds, with the first action's key=banana. Result: PASSED (2026-10-24). The alert read exactly as intended, and the folder was deleted afterwards.

**Checklist result: refactor item 1 PASSED all four steps (2026-10-24).**

## Earlier checklist: wrong key counts as a miss (option 1), started 2026-10-24

Default "rhythm test" (01) uses only enter, with notes about 2s apart, so it can test both halves cleanly.
1. Several times, press space in the middle of a gap, about a second away from any beat. Expect a miss sound each time, but the score is still perfect. Result: PASSED (2026-10-24).
2. On one beat, press space instead of enter right on the beat, then quickly press enter. Expect a miss sound, then a hit. The score drops below perfect (one miss in 13 judged). Result: PASSED (2026-10-24), 92% ("pretty good"). The first try scored 85% because space was still held when enter was pressed. A press only counts while it's the only key down (older rule), so the enter was ignored and the note failed. Tell the dev to fully let go of the wrong key first.

**Checklist result: wrong-key fix PASSED both steps (2026-10-24).**

## Earlier checklist: timing proposal C (nearest-note judging, 150ms late band), started 2026-10-24

1. Hardcore pack, "remix 1" (hardcore/10.lvl): the dev found it too fast to play. Swapped for the default pack's "Jago's memory" (default/05.lvl), a memory game where two space presses about 0.4s apart repeat throughout. Press the first space of a pair a bit late on purpose. Expect a single late sound, with the second space still hittable. This level has no early/late sounds of its own (all fall back to fail_generic), so judge by whether the second space still punches. Result: PASSED (2026-10-24). A slightly late first space no longer took the second one with it.
2. Retro world pack, "rhythm & spell" (retro_world/05.lvl; 16 keys, no close same-key repeats): should play exactly as before. Result: INCONCLUSIVE (2026-10-24). The dev scored 68% ("terrible", default thresholds, no misc settings), but had never played it before, so there was no baseline. The letter-hunting is just hard. A second try scored 79% ("ok", a pass), so the dev was improving and nothing looked broken. Replaced with default "rhythm test" (01), which scored perfect before the change. Result: PASSED (2026-10-24), perfect again.
3. Default pack, "pipes" (default/12.lvl): arrow holds still work, including escape (pause) mid-hold and resume. Result: scored 79% (78% before the change), so holds are working. Pause mid-hold and resume: the following pipes played properly. PASSED (2026-10-24).
4. A perfect run on any level still auto-plays every note correctly. Result: PASSED (2026-10-24). A perfect run of default "cruel kings and dying men" (02a) missed nothing. Note: the menu's "soundtrack" option strips all notes, so it can't test auto-play. Perfect run needs a super on the level plus 500 creds.

**Checklist result: timing proposal C PASSED all four steps (2026-10-24).**

## Past checklists

- Timing A + B (keyboard delay shift, calibration), 2026-10-24: calibration gave 15ms. "rhythm test" was perfect. "pipes" scored 78% on a first try, with the misses on unfamiliar holds, not the delay. Passed.
