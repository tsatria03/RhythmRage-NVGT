---
name: angelscript-reserved-out
description: "Never name a variable \"out\" (or other reserved words) in NVGT/AngelScript — compile error. Carried over from CaveDefender (same engine family)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:51:02.728Z
---

`out` is a reserved keyword in AngelScript (a parameter direction, like `in`/`inout`), so it cannot be used as a variable, parameter, or member name in any `.nvgt` code. Using it causes a compile error — which, since NVGT runs interpreted, stops the game from launching.

**Why:** the dev compiles the build themselves (see [[dont-compile-yourself]]), so a stray reserved-word name surfaces as a launch failure on their end, not a caught error on mine.

**How to apply:** pick a different name (e.g. `result`, `serialized`, `output`, `buf`) for any variable that would otherwise be `out`. Watch for other AngelScript reserved words too: `in`, `inout`, `shared`, `final`, `from`, `abstract`, `mixin`, etc.
