---
name: dont-compile-yourself
description: "Don't run the NVGT compiler/runner — the dev compiles and verifies builds themselves. Carried over from CaveDefender/SimpleFighter (same dev)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:18.899Z
---

Do NOT compile or run the game yourself — don't invoke `nvgt rg.nvgt`, `nvgt -c`, or otherwise launch the NVGT compiler/runtime to build or test. Make the code edits and stop; the dev compiles, runs, and verifies on their own machine.

**Why:** the dev prefers to control the build/verify step themselves.

**How to apply:** after editing `.nvgt` files, just report the change and the [[list-modified-files]] list. It's fine to read code, reason about correctness, and note "this should compile," but never actually run a compile/launch to check. (Read-only diagnostics like grep and git status are still fine.) The active engine is the new NVGT — see [[nvgt-engine-location]].
