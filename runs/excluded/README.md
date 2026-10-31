# Excluded runs

`gptoss20b_*.jsonl` — gpt-oss 20B was dropped from the pilot by amendment A9 (2026-10-27) before any of its pilot
runs existed. The author's local queue had been started from the earlier version of `scripts/pilot_local.sh`, so the
runs were produced anyway (calibration complete, held-out partial) and pushed on 2026-10-28. As A9 decided, they are
not analysed; they are kept here for transparency and are not read by `worktrace.analysis` (it reads `runs/pilot/`).
