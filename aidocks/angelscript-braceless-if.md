---
name: angelscript-braceless-if
description: A brace-less if/else in AngelScript governs only ONE statement; adding a 2nd into a branch orphans the else and breaks compile. Carried over from CaveDefender (same engine family).
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:51.850Z
---

A brace-less `if` / `else if` / `else` in AngelScript (the `.nvgt` language) governs only the **single next statement**. RhythmRage's `game.nvgt` is written almost entirely brace-less (huge `if (lang==1) ...; if (lang==2) ...;` and `else if` chains), so dropping a SECOND statement into a branch makes that statement unconditional — it sits between the `if` body and any following `else`, orphaning the `else` ("else with no matching if"). That's a **compile error**, and since NVGT runs the script interpreted, a compile failure means the game **won't launch at all**.

**How to apply:** to add any extra statement inside a brace-less `if`/`else` chain, either brace the branch — `if (cond) { a(); b(); }` — or restructure so each branch still governs one statement. Don't trust indentation to group statements — NVGT ignores whitespace entirely (see [[angelscript-indentation]]); only braces group. Watch this especially when editing the language/`lang` conditionals and the menu/level-parser dispatch chains.
