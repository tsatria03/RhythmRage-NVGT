---
name: no-crlf-normalization
description: Do NOT run post-edit CRLF-normalization passes; git handles line endings on commit. Carried over from CaveDefender/SimpleFighter (same dev).
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:50:23.132Z
---

Do not run a post-edit CRLF normalizer (e.g. a python `replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')` pass) after file edits. The dev's git setup (`.gitattributes` with `eol=crlf` + commit-time normalization) converts line endings automatically on commit.

**Why:** the normalization step adds noise to every turn and is redundant. Authoring new file CONTENT with CRLF still applies (don't deliberately write LF-only files), but no post-edit fixup pass is wanted. (The git "LF will be replaced by CRLF" warning on commit is expected and harmless.)

**How to apply:** after Edit/Write calls, just stop — no Bash normalization step. Related: [[list-modified-files]], [[angelscript-indentation]].
