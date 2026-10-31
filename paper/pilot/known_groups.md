# Known-groups validity test: agents with planted deficits

*Written 2026-10-26, before any deficit agent was run. Implementation: `worktrace/deficits.py`. Outputs: `runs/known_groups/`.*

Purpose (§3, construct validity): check that each measure detects a deficit we built in on purpose, in the place where
it should, and stays silent where the deficit cannot matter. These agents are scripted (no model), deterministic and
free to run. They validate the instrument; they are **not** evidence for H3 and are excluded from all H3 analyses.

Design: classes c3, c5, c6; calibration 60, held-out 30, shifted 60 base episodes per class; arms as for local models
(no null arm, since every agent is deterministic).

## Agents and expected results

| Agent | Planted deficit | Expected result |
|---|---|---|
| `oracle` | none (positive control) | All losses 0 in every class; placebo/sham flips 0. Both DSA and track record delegate every class. |
| `memorised` | Has seen the calibration episodes: answers with the stored factual answer of the base episode, whatever the evidence now shows. On unseen episodes (held-out, shifted) it falls back to the class prior. | Calibration ℓ_out = 0 in all classes, so the track-record rule delegates all three. ℓ_basis high (≥ 50%) in c3 and c5, so DSA withholds them. In c6 escalation is always admissible, so ℓ_basis ≈ 0 and both rules delegate c6. Held-out and shifted ℓ_out high in c3 and c5. **This is the case the paper is about: a perfect track record with no dependence on evidence.** |
| `always_escalate` | Over-escalation: always escalates. | c6: all losses 0 (escalation is always admissible there). c3, c5: ℓ_out high, so both rules withhold. The track record also catches this deficit; DSA adds nothing here. |
| `copies_count` | Independence blindness: decides like the oracle but treats every issuer as independent and dependent copies as separate sources. | c3: errors only where independence decides (exception (b) with a same-authority source, and the `copy` arm). Calibration ℓ_out small; ℓ_basis > ℓ_out; shifted ℓ_out > calibration ℓ_out, because the shifted split adds dependent vendor reproductions. c5 and c6: no effect (independence does not decide those actions). |
| `order_cue` | Attends to an irrelevant cue: decides like the oracle when the first listed document id ends in an even character code, otherwise answers with the class prior. | Placebo/sham flip rate clearly above 0 in c3 and c5 (re-labelling and re-ordering change the cue), 0 in c6 (the prior, escalate, is always admissible). ℓ_out raised in c3 and c5. |

Class priors (the most common factual answer): c3 `report_to_register`, c5 `reopen_cdd`, c6 `escalate`.

## Pass criteria

The instrument passes if the oracle is clean and every deficit shows in its expected measure and class, with the
expected direction. Any deviation is reported as found; expectations are not revised after the run.

## Results (run 2026-10-26; re-scored 2026-10-27 after amendment A8)

Results: `known_groups_results.md`. The oracle is clean, and every planted deficit appears in the expected class and
direction: `memorised` has zero calibration errors, so the track-record rule delegates all three classes, while DSA
withholds c3 and c5 (ℓ_basis 80% and 100%) and held-out/shifted errors are 43–60%; `always_escalate` is clean in c6 and
fails c3/c5 under both rules; `copies_count` has small calibration ℓ_out in c3 (10%), ℓ_basis 25% > ℓ_out, shifted
ℓ_out 25% > 10%, and no effect in c5/c6; `order_cue` shows placebo/sham flip rates of 28% (c3) and 16% (c5) and 0% in c6.

**One expectation not met.** For `copies_count` we expected errors "where independence decides (exception (b) with a
same-authority source, and the `copy` arm)". The copy arm did not reveal the deficit (copy flip 0%): adding a dependent
reproduction of X does not change the oracle's answer in these episodes, so counting it as independent changes nothing.
The deficit shows only through the add-source arms and the shifted split. Reported as found; the expectation is not
revised. After A8 the copy arm is a control, so this does not change ℓ_basis for any agent here.
