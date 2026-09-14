---
name: confirm-before-implementing
description: Treat every design discussion as a question requiring explicit go-ahead — never a commission. Carried over from CaveDefender/SimpleFighter (same dev).
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:00.878Z
---

Treat every design discussion as a question requiring explicit go-ahead — never a commission. "I really wish X" / "what if we did Y" / "could we extend Z" / "I have an idea" are explorations, not instructions. Lay out the design, call out tradeoffs, ask for go-ahead. Stop and wait.

**Why:** The dev has repeatedly observed Claude over-implementing despite guardrails. There is no permission-layer backstop, so the rule rests entirely on instruction-following — vigilance matters more, not less.

**How to apply:**
- Default to asking "want me to proceed?" before any Edit/Write/destructive Bash, even when the change feels obvious or small.
- Never bundle implementation into the same turn as a proposal — split them so the dev can redirect.
- Never fan out into adjacent files unprompted (readme, changelog, memory) — each side-effect deserves its own go-ahead.
- **Hard rule: a message ending in `?` is a question, full stop.** Even when it reads like a polite imperative ("Could you fix X?"), respond with info or a plan and *wait* for "yes"/"go ahead"/"do it."
- **Treat information-seeking imperatives as questions too**, even without a `?`: "explain X", "tell me about X", "describe X", "walk me through X", "summarize X", "what does X do".
- **Exceptions** (proceed without re-asking): direct unambiguous commands ("rename X to Y", "go ahead", "do it", "yes please", "delete this"), follow-ups within an already-approved task, or bug fixes the dev explicitly asked for in the same message.

Related: [[list-modified-files]], [[ask-one-question-at-a-time]].
