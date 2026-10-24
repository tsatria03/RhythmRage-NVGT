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

## Current checklist: timing proposal C (nearest-note judging, 150ms late band), started 2026-10-24

1. Hardcore pack, "remix 1" (hardcore/10.lvl): the dev found it too fast to play. Swapped for the default pack's "Jago's memory" (default/05.lvl), a memory game where two space presses about 0.4s apart repeat throughout. Press the first space of a pair a bit late on purpose. Expect a single late sound, with the second space still hittable. This level has no early/late sounds of its own (all fall back to fail_generic), so judge by whether the second space still punches. Result: PASSED (2026-10-24). A slightly late first space no longer took the second one with it.
2. Retro world pack, "rhythm & spell" (retro_world/05.lvl; 16 keys, no close same-key repeats): should play exactly as before. Result: INCONCLUSIVE (2026-10-24). The dev scored 68% ("terrible", default thresholds, no misc settings), but had never played it before, so there was no baseline. The letter-hunting is just hard. A second try scored 79% ("ok", a pass), so the dev was improving and nothing looked broken. Replaced with default "rhythm test" (01), which scored perfect before the change. Result: PASSED (2026-10-24), perfect again.
3. Default pack, "pipes" (default/12.lvl): arrow holds still work, including escape (pause) mid-hold and resume. Result: scored 79% (78% before the change), so holds are working. Pause mid-hold and resume: the following pipes played properly. PASSED (2026-10-24).
4. A perfect run on any level still auto-plays every note correctly. Result: PASSED (2026-10-24). A perfect run of default "cruel kings and dying men" (02a) missed nothing. Note: the menu's "soundtrack" option strips all notes, so it can't test auto-play. Perfect run needs a super on the level plus 500 creds.

**Checklist result: timing proposal C PASSED all four steps (2026-10-24).**

## Past checklists

- Timing A + B (keyboard delay shift, calibration), 2026-10-24: calibration gave 15ms. "rhythm test" was perfect. "pipes" scored 78% on a first try, with the misses on unfamiliar holds, not the delay. Passed.
