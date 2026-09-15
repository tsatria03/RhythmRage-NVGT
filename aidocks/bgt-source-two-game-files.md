---
name: bgt-source-two-game-files
description: "The BGT source folder has TWO game scripts — game.bgt (2023, canonical, port basis) and z.bgt (2016 backup) — with different store designs; don't confuse them"
metadata:
  node_type: memory
  type: reference
---

The original BGT source ([[rhythm-rage-bgt-to-nvgt-port]], at `C:\Users\tonys\OneDrive\Desktop\rhythm-rage bgt-src`) contains **two nearly-identical game scripts**. They look almost the same but are different versions of the game's life — don't mix them up when diffing the port:

- **`game.bgt`** — 2023-12-05, ~2370 lines. The **newer, canonical** version; the NVGT port was made from this (correctly). **Free store**: `store()`/`packloop()` have no credit gate, no price, no `lesscash` on buy — buying a pack just adds it to `unlocks` and switches to it. On no packs left it goes to `getpacks()` (the port later changed this to return to the menu at the dev's request).
- **`z.bgt`** — 2016-07-25, ~1799 lines. An **older snapshot/backup** ("z" prefix matches `z.iss`, the installer marker). **Paid store** (a legacy design later removed): `store()` gates on `if (cash<2500)` (bounce to menu with a "not enough credits" message), forces `if (!SCRIPT_COMPILED) cash=50000` for dev testing, deducts `lesscash(7)` on buy, and plays a `nomore` sound (then returns to menu) when all packs are owned.

**Key takeaway:** the paid store is *legacy*, removed between 2016 and 2023. The port's free store is faithful to the latest source (`game.bgt`). A compiled BGT build showing a "need N credits" store gate (the dev saw "need at least 1000") is an OLD pre-2023 binary from the paid-store lineage — its threshold matches neither source file exactly, so it's a further revision in that older line, not the current design. When comparing the port against "the BGT game," compare against **`game.bgt`**, not `z.bgt`, unless specifically investigating the old paid store.
