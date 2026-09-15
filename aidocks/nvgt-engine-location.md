---
name: nvgt-engine-location
description: "Which NVGT engine RhythmRage-NVGT targets, and where the active vs legacy engines live"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a25e902-c2cb-46ca-8fe3-bc486457c6cb
  modified: 2026-07-21T04:28:48.832Z
---

RhythmRage-NVGT targets the **new NVGT** (NonVisual Game Toolkit by Sam Tupy), not the legacy engine.

- **Compiled runtime this project runs against:** `C:\nvgt2\nvgt2.exe` (windowless variant `nvgt2w.exe`) — the miniaudio build ([[nvgt-090-miniaudio-not-bass]]). The executable is named `nvgt2.exe`, NOT `nvgt.exe`. Its `C:\nvgt2\config.properties` sets `build.windows_bundle=1`/`build.mac_bundle=1` and does NOT set `no_auto_chdir`, so `auto_chdir` is active: running a script from source changes the working directory to the **script's own folder** (`g_scriptpath` = the script's parent dir); compiled, it changes to the executable's folder. (An older non-miniaudio NVGT lives at `C:\nvgt`; this project does not use it.)
- Active engine source (this game): `C:\Users\tonys\OneDrive\Desktop\nvgt-main`. Full engine C++ source (confirmed 2026-09-14) lives under the versioned subfolder `C:\Users\tonys\OneDrive\Desktop\nvgt-main\nvgt_0.90.0_dev` — `src/` (nvgt-specific registrations), `ASAddon/src/scriptstdstring.cpp` (the `string` type registration), and the script include folder `release/include/`.
- Legacy engine (reference only, NOT used): `C:\Users\tonys\OneDrive\Documents\github\tsatria03\misc\Legacy-NVGT`.

The two bare engine includes `rg.nvgt` relies on — `bgt_compat.nvgt` and `sound_pool.nvgt` — resolve from the new engine's include folder: `nvgt_0.90.0_dev\release\include\`. Run a script with `nvgt rg.nvgt`; debug with `nvgt -d rg.nvgt`. See [[rhythmrage-bgt-to-nvgt-port]].

**AngelScript string↔number gotcha (verified in engine source):** NVGT registers a value constructor `string(double)` (`ConstructStringDouble` → `AssignDoubleToString`, an `ostringstream` at `precision(15)`), which acts as an *implicit* conversion. So `double != string` compiles and silently becomes a **string** comparison of the stringified double, NOT a numeric one. At precision 15 a byte-count-sized double prints as plain integer digits (no scientific notation), so it often matches by luck — but any whitespace/formatting difference breaks it. There is NO string→double implicit conversion (no `opConv`/`opImplConv` to double on `string`). When comparing a numeric string to a number, always wrap with `string_to_number(...)`.
