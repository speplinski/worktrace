# Pilot — interim results

α = 0.1, δ = 0.05 (Bonferroni over classes). Calibration and held-out: units = (base episode, run), as registered; for configurations with several runs per episode these units are not independent, so the majority-vote line (one unit per base episode) and the common-core analysis are the statistically clean versions. ℓ_basis counts the five intervention arms only; null, placebo, sham and copy are controls (preregistration §2) and are reported as flip rates per arm (share of control arms whose action differs from the factual action). Units missing any arm are dropped and counted. Shifted: factual arm only.

## deficit:always_escalate

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 65.0% | 80.0% | 80.0% | 15.0% | 40.5% | – | 0.0% | 0.0% | 0.0% | 70.0% / 86.7% | 65.0% (60) |
| c5 | 60 | 100.0% | 100.0% | 100.0% | 0.0% | 11.9% | – | 0.0% | 0.0% | 0.0% | 100.0% / 100.0% | 100.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.898), track record ✗ (UB 0.777); c5: DSA ✗ (UB 1.000), track record ✗ (UB 1.000); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record ['c6'] → 0.0%; k=2: DSA ['c3', 'c6'] → 32.5%, track record ['c3', 'c6'] → 32.5%

## deficit:copies_count

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 10.0% | 25.0% | 25.0% | 15.0% | 94.5% | – | 0.0% | 0.0% | 0.0% | 13.3% / 26.7% | 25.0% (60) |
| c5 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.389), track record ✗ (UB 0.215); c5: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA [['c5'], ['c6']] (tie: expected) → 0.0%, track record [['c5'], ['c6']] (tie: expected) → 0.0%; k=2: DSA ['c5', 'c6'] → 0.0%, track record ['c5', 'c6'] → 0.0%

## deficit:memorised

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 0.0% | 80.0% | 80.0% | 80.0% | 64.2% | – | 0.0% | 0.0% | 0.0% | 60.0% / 100.0% | 56.7% (60) |
| c5 | 60 | 0.0% | 100.0% | 100.0% | 100.0% | 57.6% | – | 0.0% | 0.0% | 0.0% | 43.3% / 100.0% | 51.7% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.898), track record ✓ (UB 0.066); c5: DSA ✗ (UB 1.000), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record [['c3'], ['c5'], ['c6']] (tie: expected) → 36.1%; k=2: DSA ['c3', 'c6'] → 28.3%, track record [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 36.1%

## deficit:oracle

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c5 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c5: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA [['c3'], ['c5'], ['c6']] (tie: expected) → 0.0%, track record [['c3'], ['c5'], ['c6']] (tie: expected) → 0.0%; k=2: DSA [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 0.0%, track record [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 0.0%

## deficit:order_cue

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 45.0% | 78.3% | 78.3% | 33.3% | 46.4% | – | 27.5% | 4.3% | 0.0% | 36.7% / 70.0% | 31.7% (60) |
| c5 | 60 | 23.3% | 63.3% | 63.3% | 40.0% | 69.5% | – | 15.8% | 8.3% | 0.0% | 23.3% / 63.3% | 30.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.886), track record ✗ (UB 0.594); c5: DSA ✗ (UB 0.763), track record ✗ (UB 0.371); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record ['c6'] → 0.0%; k=2: DSA ['c5', 'c6'] → 15.0%, track record ['c5', 'c6'] → 15.0%

## H3 summary (interim)

- DSA vs track record: 10 (configuration, k) cells, rules differ in 2 (2 with a tie at the boundary, scored as expected error); DSA lower shifted error in 2, higher in 0, equal 0; one-sided sign test p = 0.25 (descriptive: k = 1 and k = 2 cells of one configuration are not independent).

(Interim; the pre-registered test runs on the full data.)


---

# Sensitivity analysis (post hoc): contested arms excluded (amendment A1)

## deficit:always_escalate

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 65.0% | 80.0% | 80.0% | 15.0% | 34.8% | – | 0.0% | 0.0% | 0.0% | 70.0% / 86.7% | 65.0% (60) |
| c5 | 60 | 100.0% | 100.0% | 100.0% | 0.0% | 13.8% | – | 0.0% | 0.0% | 0.0% | 100.0% / 100.0% | 100.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.898), track record ✗ (UB 0.777); c5: DSA ✗ (UB 1.000), track record ✗ (UB 1.000); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record ['c6'] → 0.0%; k=2: DSA ['c3', 'c6'] → 32.5%, track record ['c3', 'c6'] → 32.5%

## deficit:copies_count

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 10.0% | 25.0% | 25.0% | 15.0% | 94.0% | – | 0.0% | 0.0% | 0.0% | 13.3% / 26.7% | 25.0% (60) |
| c5 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.389), track record ✗ (UB 0.215); c5: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA [['c5'], ['c6']] (tie: expected) → 0.0%, track record [['c5'], ['c6']] (tie: expected) → 0.0%; k=2: DSA ['c5', 'c6'] → 0.0%, track record ['c5', 'c6'] → 0.0%

## deficit:memorised

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 0.0% | 73.3% | 73.3% | 73.3% | 70.4% | – | 0.0% | 0.0% | 0.0% | 60.0% / 100.0% | 56.7% (60) |
| c5 | 60 | 0.0% | 100.0% | 100.0% | 100.0% | 55.8% | – | 0.0% | 0.0% | 0.0% | 43.3% / 100.0% | 51.7% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.847), track record ✓ (UB 0.066); c5: DSA ✗ (UB 1.000), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record [['c3'], ['c5'], ['c6']] (tie: expected) → 36.1%; k=2: DSA ['c3', 'c6'] → 28.3%, track record [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 36.1%

## deficit:oracle

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c5 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c5: DSA ✓ (UB 0.066), track record ✓ (UB 0.066); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA [['c3'], ['c5'], ['c6']] (tie: expected) → 0.0%, track record [['c3'], ['c5'], ['c6']] (tie: expected) → 0.0%; k=2: DSA [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 0.0%, track record [['c3', 'c5'], ['c3', 'c6'], ['c5', 'c6']] (tie: expected) → 0.0%

## deficit:order_cue

| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c3 | 60 | 45.0% | 71.7% | 71.7% | 26.7% | 48.4% | – | 27.5% | 4.3% | 0.0% | 36.7% / 66.7% | 31.7% (60) |
| c5 | 60 | 23.3% | 58.3% | 58.3% | 35.0% | 74.6% | – | 15.8% | 8.3% | 0.0% | 23.3% / 60.0% | 30.0% (60) |
| c6 | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | – | 0.0% | – | 0.0% | 0.0% / 0.0% | 0.0% (60) |

Certified grants at α = 0.10: c3: DSA ✗ (UB 0.833), track record ✗ (UB 0.594); c5: DSA ✗ (UB 0.719), track record ✗ (UB 0.371); c6: DSA ✓ (UB 0.066), track record ✓ (UB 0.066)

H3 (matched coverage, k classes delegated; shifted outcome error): k=1: DSA ['c6'] → 0.0%, track record ['c6'] → 0.0%; k=2: DSA ['c5', 'c6'] → 15.0%, track record ['c5', 'c6'] → 15.0%

## H3 summary (interim)

- DSA vs track record: 10 (configuration, k) cells, rules differ in 2 (2 with a tie at the boundary, scored as expected error); DSA lower shifted error in 2, higher in 0, equal 0; one-sided sign test p = 0.25 (descriptive: k = 1 and k = 2 cells of one configuration are not independent).

(Interim; the pre-registered test runs on the full data.)

---

# Exploratory (A8, not registered): control arms with an action outside A* also count as basis failures

- deficit:always_escalate: DSA grants c6
- deficit:copies_count: DSA grants c5, c6
- deficit:memorised: DSA grants c6
- deficit:oracle: DSA grants c3, c5, c6
- deficit:order_cue: DSA grants c6

## H3 summary (interim)

- DSA vs track record: 10 (configuration, k) cells, rules differ in 2 (2 with a tie at the boundary, scored as expected error); DSA lower shifted error in 2, higher in 0, equal 0; one-sided sign test p = 0.25 (descriptive: k = 1 and k = 2 cells of one configuration are not independent).
