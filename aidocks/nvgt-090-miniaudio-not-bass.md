---
name: nvgt-090-miniaudio-not-bass
description: "NVGT 0.90.0 uses miniaudio (compiled into the exe), not BASS — bass*.dll are obsolete; what RhythmRage's compiled bundle actually needs in lib/"
metadata:
  node_type: memory
  type: reference
---

NVGT 0.90.0 ([[nvgt-engine-location]]) has completed the BASS→**miniaudio** audio switch that NVGT's own distribution doc still only describes as a future plan. The whole sound system (`sound` object, `tts_voice`, mixing, reverb, pitch/tempo) is miniaudio, **statically compiled into the exe** — evidence: `dep/miniaudio_*.c` files, `sound.cpp` built on miniaudio, and no BASS anywhere in the engine. So **`bass.dll`, `bassmix.dll`, `bass_fx.dll` are obsolete** and are NOT bundled/needed. NVGT's "Libraries needed for distribution" doc is OUT OF DATE on this — don't tell the dev bass is required.

**What RhythmRage's compiled bundle actually ships in `game/lib/` (verified 2026-09-14 from the bundler output):** `phonon.dll` (Steam Audio HRTF/geometric reverb, still a separate native lib via `miniaudio_phonon.c`), plus the three screen-reader clients `nvdaControllerClient64.dll` (NVDA), `SAAPI64.dll` (System Access), `zdsrapi.dll` (ZDSR). That 4-DLL set is complete and correct — the game runs with exactly those.

**Not needed / correctly excluded:** `nvgt_curl.dll` (no `#pragma plugin` in the project; built-in HTTP replaced the curl plugin), `nvgt_sqlite.dll`, `git2*.dll`, `GPUUtilities.dll`, `TrueAudioNext.dll`, `systemd_notify.dll`. The project's hand-made source `lib/` folder still had stale `bass*.dll` + `nvgt_curl.dll` that do nothing.

**Distribution note:** NVGT's one-click compile/bundle copies the correct libs automatically (excluding optional plugin libs via `build.shared_library_excludes`); the compiler output is ground truth, not the doc. Consider shipping `3rd_party_code_attributions.html` (from NVGT's lib folder) for open-source attribution compliance.
