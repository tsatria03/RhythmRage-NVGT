---
name: angelscript-indentation
description: "AngelScript/NVGT ignores indentation entirely; don't flag uneven whitespace after edits. Carried over from CaveDefender (same engine family)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:51:06.393Z
---

AngelScript (the `.nvgt` language) is brace-delimited, so indentation is purely cosmetic and never affects compilation — unlike Python. RhythmRage's source is almost entirely unindented (flush-left statements), which is fine and normal for this codebase.

**Why:** flagging or apologizing for "uneven indentation" after edits is noise — it has zero effect on the code.

**How to apply:** after an edit leaves whitespace slightly off, don't call it out or spend tool calls fixing it for compilation's sake. Only adjust indentation if the dev explicitly asks for tidy formatting. Grouping is by braces, not indentation — see [[angelscript-braceless-if]]. Related: [[no-crlf-normalization]].
