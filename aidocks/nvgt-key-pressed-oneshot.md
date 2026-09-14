---
name: nvgt-key-pressed-oneshot
description: NVGT key_pressed() is edge-triggered and consumed on first read each frame — never read the same key twice in one loop iteration. Carried over from CaveDefender (same engine family).
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:57.859Z
---

`key_pressed(KEY_X)` in NVGT is **consumed on the first read** each frame (it reports the press once, then reads false). Reading the SAME key in two separate `if` checks within one loop iteration means the second check always sees false. (`keys_pressed()`, which RhythmRage's `loadlev()` game loop uses to grab the frame's presses as a list, is the list-form of the same edge-triggered model.)

**Why:** if one physical key needs to drive multiple behaviors (a modifier combo, or two different mode branches), two sibling `if (key_pressed(KEY_X))` checks will have the first one eat the press so the second never fires.

**How to apply:** when one key drives multiple behaviors, read it **once** into an `if` and branch inside — `if (key_pressed(KEY_X)) { if (modifier) ...; else ...; }` — not two sibling `if`s that each call `key_pressed(KEY_X)`. Different keys per check are fine. See [[angelscript-reserved-out]] for another engine gotcha.
