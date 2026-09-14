---
name: nvgt-busy-loop-needs-wait
description: "NVGT input loops must call wait() each iteration to pump window/input events — a busy loop with no yield never sees key presses (BGT tolerated it, NVGT does not)"
metadata:
  node_type: memory
  type: reference
---

In NVGT, any `while` loop that reads input (`key_pressed`/`key_released`/`key_down`) **must call `wait()` every iteration**. NVGT is SDL-based: without a yield the loop never pumps the window/input event queue, so all key functions return false forever — the loop looks frozen and registers no input (and pins a CPU core). BGT's runtime polled input without needing a yield, so BGT busy loops "worked" and ported code can silently break.

**This bit RhythmRage twice** (both carried over from BGT busy loops):
- `calibrate_keyboard()` — fixed with `wait(1)` (see its inline comment).
- The **interactive-tutorial** loop in `startlev()`/`loadlev()` (the no-args `interactive` branch that runs `intersound` cues) — had NO wait, so interactive tutorials in every pack failed to register any key press (Enter always "missed", Escape dead). Fixed 2026-09-14 by adding `wait(5)` at the **top** of the `while(true)` loop, so the yield also runs after each `continue`. Interactive tutorials live only in the `extension1` pack ([[bgt-source-two-game-files]] context).

**How to apply:** when porting or writing any NVGT input loop, put a `wait(3..5)` inside it (top of the loop is safest so `continue` paths still yield). Related: [[nvgt-key-pressed-oneshot]] (edge-triggered reads), [[rhythmrage-bgt-to-nvgt-port]].
