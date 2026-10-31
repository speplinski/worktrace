# Measures registered in §5.4 that §6 does not report

**Table 5.** Calibration and held-out losses, control-arm flips, non-reaction and escalation calibration per configuration and class (common core, registered key; `paper/pilot/appendix_measures.md`, generated from `results_core.md`). Flip rates (null; placebo and sham) are the share of control arms on which the action changed; non-reaction (non-react.) is the share of interventions that made the factual action inadmissible on which the agent kept it; over-escalation (over-esc.) is the share of arms with an admissible non-escalation answer on which the agent escalated, under-escalation (under-esc.) the share of arms whose only admissible answer was escalation on which it did not. "–" marks an arm or measure that does not exist for the configuration or class.

| configuration | class | cal. ℓ_out | cal. ℓ_WT | held-out ℓ_out / ℓ_WT | shifted ℓ_out | null flip | placebo, sham flip | non-react. | over-esc. | under-esc. |
|---|---|---|---|---|---|---|---|---|---|---|
| Basal 2.0-max | discrepancy | 40.0% | 85.0% | 46.7% / 96.7% | 26.7% | – | 5.0% | 81.5% | 0.5% | 14.3% |
| Basal 2.0-max | freshness | 55.0% | 98.3% | 43.3% / 96.7% | 48.3% | – | 13.3% | 45.0% | 0.0% | – |
| Basal 2.0-max | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | – | 0.0% | – | – | 0.0% |
| Claude Haiku 5.5 | discrepancy | 0.0% | 8.3% | 0.0% / 13.3% | 0.0% | 0.0% | 0.8% | 1.0% | 0.0% | 0.0% |
| Claude Haiku 5.5 | freshness | 10.0% | 55.0% | 10.0% / 46.7% | 25.0% | 13.3% | 20.0% | 1.2% | 4.5% | – |
| Claude Haiku 5.5 | onboarding | 3.3% | 8.3% | 6.7% / 10.0% | 0.0% | 13.3% | 10.8% | – | – | 4.3% |
| Claude Opus 5.5 | discrepancy | 0.0% | 10.0% | 0.0% / 10.0% | 0.0% | 0.0% | 0.0% | 4.1% | 0.0% | 0.0% |
| Claude Opus 5.5 | freshness | 20.0% | 41.7% | 13.3% / 43.3% | 16.7% | 3.3% | 5.0% | 0.0% | 0.0% | – |
| Claude Opus 5.5 | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | 0.0% | 0.0% | – | – | 0.0% |
| Claude Sonnet 5.5 | discrepancy | 0.0% | 16.7% | 0.0% / 20.0% | 1.7% | 0.0% | 0.8% | 4.1% | 0.0% | 0.0% |
| Claude Sonnet 5.5 | freshness | 3.3% | 45.0% | 6.7% / 30.0% | 6.7% | 1.7% | 3.3% | 5.7% | 0.0% | – |
| Claude Sonnet 5.5 | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | 0.0% | 0.0% | – | – | 0.0% |
| Bielik 11B v3 (one-pass) | discrepancy | 51.7% | 95.0% | 30.0% / 93.3% | 43.3% | – | 7.5% | 62.0% | 5.4% | 71.4% |
| Bielik 11B v3 (one-pass) | freshness | 50.0% | 98.3% | 50.0% / 100.0% | 70.0% | – | 25.8% | 51.0% | 0.0% | – |
| Bielik 11B v3 (one-pass) | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | – | 0.0% | – | – | 0.0% |
| Gemma 4 26B | discrepancy | 5.0% | 31.7% | 0.0% / 23.3% | 1.7% | – | 8.3% | 8.6% | 0.0% | 0.0% |
| Gemma 4 26B | freshness | 6.7% | 48.3% | 0.0% / 33.3% | 23.3% | – | 7.5% | 2.4% | 2.9% | – |
| Gemma 4 26B | onboarding | 1.7% | 10.0% | 3.3% / 6.7% | 0.0% | – | 5.0% | – | – | 4.3% |
| gpt-oss 120B | discrepancy | 20.0% | 61.7% | 26.7% / 70.0% | 23.3% | – | 30.8% | 10.6% | 0.0% | 51.0% |
| gpt-oss 120B | freshness | 48.3% | 98.3% | 36.7% / 100.0% | 48.3% | – | 38.3% | 17.9% | 37.1% | – |
| gpt-oss 120B | onboarding | 6.7% | 31.7% | 13.3% / 33.3% | 1.7% | – | 29.2% | – | – | 15.2% |
| Mistral Small 3.2 | discrepancy | 20.0% | 75.0% | 26.7% / 80.0% | 20.0% | – | 35.0% | 50.7% | 1.0% | 2.0% |
| Mistral Small 3.2 | freshness | 55.0% | 95.0% | 46.7% / 100.0% | 50.0% | – | 26.7% | 45.2% | 0.0% | – |
| Mistral Small 3.2 | onboarding | 6.7% | 11.7% | 0.0% / 10.0% | 1.7% | – | 18.3% | – | – | 5.8% |
| Qwen 3.8 27B | discrepancy | 10.0% | 35.0% | 13.3% / 43.3% | 16.7% | – | 9.2% | 11.5% | 0.0% | 0.0% |
| Qwen 3.8 27B | freshness | 0.0% | 40.0% | 0.0% / 36.7% | 26.7% | – | 0.0% | 3.4% | 0.0% | – |
| Qwen 3.8 27B | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | – | 0.0% | – | – | 0.0% |
| GPT-6 Luna (Decisions API) | discrepancy | 26.7% | 70.0% | 20.0% / 80.0% | 10.0% | 0.0% | 14.2% | 42.6% | 0.0% | 12.2% |
| GPT-6 Luna (Decisions API) | freshness | 50.0% | 91.7% | 43.3% / 96.7% | 51.7% | 0.0% | 7.5% | 63.3% | 0.8% | – |
| GPT-6 Luna (Decisions API) | onboarding | 25.0% | 35.0% | 23.3% / 26.7% | 1.7% | 0.0% | 28.3% | – | – | 19.6% |
| GPT-6 Luna | discrepancy | 8.3% | 33.3% | 10.0% / 30.0% | 10.0% | 10.0% | 10.0% | 6.8% | 0.0% | 0.0% |
| GPT-6 Luna | freshness | 0.0% | 33.3% | 0.0% / 26.7% | 21.7% | 1.7% | 0.8% | 0.0% | 0.0% | – |
| GPT-6 Luna | onboarding | 26.7% | 41.7% | 13.3% / 33.3% | 3.3% | 25.0% | 27.5% | – | – | 24.6% |
| GPT-6.1 Sol | discrepancy | 0.0% | 8.3% | 0.0% / 10.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.5% | 0.0% |
| GPT-6.1 Sol | freshness | 0.0% | 33.3% | 0.0% / 30.0% | 25.0% | 0.0% | 0.0% | 0.0% | 0.0% | – |
| GPT-6.1 Sol | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | 0.0% | 0.0% | – | – | 0.0% |
| GPT-6.1 Terra | discrepancy | 8.3% | 30.0% | 13.3% / 30.0% | 3.3% | 6.7% | 15.0% | 3.4% | 5.0% | 0.0% |
| GPT-6.1 Terra | freshness | 0.0% | 33.3% | 0.0% / 30.0% | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | – |
| GPT-6.1 Terra | onboarding | 46.7% | 68.3% | 60.0% / 66.7% | 16.7% | 25.0% | 28.3% | – | – | 51.4% |
| Liquid AI d1-3B | discrepancy | 65.0% | 100.0% | 53.3% / 100.0% | 51.7% | – | 0.0% | 100.0% | 0.0% | 100.0% |
| Liquid AI d1-3B | freshness | 63.3% | 100.0% | 70.0% / 100.0% | 73.3% | – | 6.7% | 87.5% | 0.0% | – |
| Liquid AI d1-3B | onboarding | 0.0% | 0.0% | 0.0% / 0.0% | 0.0% | – | 0.0% | – | – | 0.0% |

Table 5 collects these measures. Out-of-permission actions were attempted by no configuration in any class. Protocol incidents (all splits): Gemma 4 26B, 13 reseeded retries after rejected tool calls and one run that hit the turn limit; gpt-oss 120B, one reseeded retry, three decisions recovered from text and one run without a decision; Mistral Small 3.2, six server timeouts and two runs without a decision; none elsewhere. Excluding the three gpt-oss units with text-recovered decisions, the robustness check of §5.7, changes no grant, because the configuration certifies nothing in any class under any rule. Majority voting over the three runs of Claude Haiku 5.5 (all data) certifies the discrepancy class for the DSA rule (upper bound 0.059 against 0.116 with runs as units), leaves the other grants unchanged and leaves the delegation-test selections unchanged (both rules delegate the discrepancy class at $k = 1$ and the discrepancy and onboarding classes at $k = 2$). Escalation calibration varies widely: GPT-6.1 Terra under-escalated 51% of the onboarding-class arms whose only admissible answer was escalation, and gpt-oss 120B over-escalated 37% of the freshness-class arms with an admissible non-escalation answer.
