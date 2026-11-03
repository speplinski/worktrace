# 1 Introduction

*Draft v1, 25 Oct 2026. Every fact is taken from the reading notes in `notes/`; the note is given in an HTML comment after each paragraph.*

## 1.1 The delegation question

Organisations that deploy AI agents must decide which decisions an agent may take without human review. Supervisors now ask them to make this decision explicitly and to revisit it. The Financial Stability Board's 2026 sound practices suggest that firms "may also progressively increase an agent's ability to interact with the external environment as they gain confidence it can do so safely", with "triggers for transitioning between different forms of human oversight based on performance metrics or user requests" (FSB, 2026). The UK Financial Conduct Authority (FCA) calls for "continuous, conditional assurance" and for frameworks covering "delegated authority" (Rusu, 2026). Neither says what evidence should ground the confidence on which autonomy is extended.

<!-- r2_governance_context.md: S11, S12, §A -->

## 1.2 Why track records are not enough

The default answer is a track record: success rates, human approvals, correction rates, model confidence, or a judge's reading of the agent's trace. A track record answers whether the agent's actions turned out correct. A delegator also needs to know whether they were correct *for the right reasons and within scope*, because only then can past success be expected to transfer to the next case. This is the premise of the paper. The pilot tested one consequence of it, that a rule built on evidence tests, that is, on interventions on the evidence the agent consults, delegates more safely than a track record, and §6.1 reports that it could not confirm this. Outcome success masks the basis of a decision, much as human correction masks an agent's raw competence (Azevedo, 2026).

The gap is not hypothetical. In CXBench, 80.1% of runs that passed the outcome check failed process checks in regulated customer-experience workflows (Yu et al., 2026). Procedure-aware evaluation finds that between 27% and 78% of reported τ-bench successes, depending on model and domain, are "corrupt successes" (Cao et al., 2026). In paired tasks, an agent's skill at acting correctly and its skill at correctly abstaining are nearly independent (phi coefficient φ ≈ −0.10; Liu et al., 2026). Self-reports do not close the gap: verbalised confidence barely separates correct from incorrect answers (area under the ROC curve, AUROC, 0.47–0.66; Shen, 2026), and stated reasoning can be unfaithful to what drives a model's answer (Turpin et al., 2023).

There is also a formal reason. Relational properties of an agent's behaviour, such as what its action depends on, are 2-safety hyperproperties that no monitor of a single trace can decide; deciding them requires comparing executions (Pandey et al., 2026b). Calibrating on final outcomes cannot control the share of correct outcomes reached on an unsupported basis (Opoku & Banahene, 2026). The philosophy of meaningful human control reached the same conclusion from another direction: a system must "demonstrably and verifiably be responsive to the human moral reasons relevant in the circumstances", and this holds "no matter how efficient [it] may be in performing specific tasks" (Santoni de Sio & van den Hoven, 2018).

<!-- r4_minimal_oversight.md; r2_agent_evaluation.md; r3_outcome_process_gap.md; r3_oversight_and_profiles.md; r3_certification_stats.md; r2_faithfulness_interventions.md; r4_pandey_certifier.md §3; r4_care_drive.md §2.2 -->

## 1.3 A motivating example

In the pilot of §5, Claude Sonnet 5.5 reads a customer file in which the central beneficial-ownership register names one owner while a business-register excerpt and a notarial deed record a transfer of all shares to another. It asks the customer to correct the register entry, the action the policy admits here: the deed is a source independent of the register's controlling authority, so the exception to the reporting duty applies. Its explanation is accurate, names the deed as decisive, and an LLM judge reading the explanation finds the grounds sound. Remove the deed and run the same case again (episode c3-100005, run 0, in `runs/pilot/sonnet55_calibration.jsonl`): the agent gives the same action, now resting on the business-register excerpt, and writes that nothing in the file shows the two registers to be independent, "that is an assumption". Under the policy the only admissible answer is now to report the discrepancy: its rule R2(b) requires, beyond the legal text it paraphrases, that the other source be independent of the register's controlling authority (§8). Without that condition the second decision would also be admissible, and §8 reports the results under that reading as well. The first decision was correct, and its record read well; what the record could not show is that the decision did not turn on the document it named. That is the gap this paper is about, and §6.2 counts how often the judge passes such decisions.



## 1.4 Question, finding and contributions

We ask which evidence should decide that an agent may take a class of decisions without review: its track record, an LLM judge's reading of its trace, or its reaction to changes in the evidence. For the last we define *decision-structured agency* (DSA): the extent to which an agent configuration, within a class of decisions, regularly recognises and reacts to the evidence that ought to settle those decisions. It also covers escalating when that evidence is missing or contradictory or when an action would exceed the agent's authority. The notion descends from reasons-responsiveness (Fischer & Ravizza, 1998) and from the tracking condition of meaningful human control (Santoni de Sio & van den Hoven, 2018).

Our prospectively specified pilot does not show that delegating on DSA beats a track record. The registered test favoured DSA, but the advantage rested on cases where our own policy admits more than one reading, and it disappeared when those cases were excluded or the answer key was reviewed. Under every answer key, an LLM judge passed most of the decisions that failed an evidence test. The main lesson concerns method: in an evaluation of this kind the answer key is part of the instrument. It feeds both the test and the criterion against which the test is judged, and two separately written oracles (programs that compute the correct action from the generator's hidden facts) that agree with each other can still share the same contestable reading. Cao (2026) shows that policy ambiguity can masquerade as agent error in benchmark scores; we show that it can also decide which delegation rule appears to work.

We make three contributions.

**C1. A construct and its measurement.** We define DSA per pair (agent configuration, decision class) and measure it by composed interventions on the external evidence the agent consults, with control arms, scoring responses against the agent-declared grounds (§3). Which response each intervention requires is fixed by oracles that encode one reading of the policy; the pilot shows how much rests on that reading.

**C2. A delegation rule.** We give a rule that grants, narrows and revokes autonomy per decision class beneath a fixed, human-set ceiling, with certificates bound to the agent's configuration (§4). The statistical machinery is standard; the novelty is the loss it controls. The pilot exercises only the granting step; narrowing, revocation and transfer between classes are specified but not yet tested.

**C3. A prospectively specified pilot with a full audit trail.** On a synthetic counterparty-verification workflow with 14 model configurations, we compare delegation on DSA with delegation on a track record, the registered primary comparison, and with rules built on an LLM judge, at matched autonomy and under evidence shift (§5, §6). We publish the registration, every amendment, the log of policy ambiguities, the author's review of the oracles' answers and the code, so that each step from data to conclusion can be checked.

## 1.5 Scope

We study ordinary, non-adversarial shifts in evidence. When sources can be corrupted adversarially, no procedure that sees the same evidence can avoid handing off ambiguous cases to a human (Pandey et al., 2026a); for that setting we propose combining our rule with a source-quorum gate. Our guarantees hold for generated episodes and relative to a family of interventions fixed in advance. What the rule provides is reliability allocation beneath a fixed ceiling, not a security guarantee. The case study encodes publicly available anti-money-laundering rules in a fully synthetic environment. It uses no real entities and no institutional data, and makes no claim of regulatory compliance.

<!-- r4_pandey_certifier.md §2; r3_earned_autonomy_family.md (Earned Authority); r2_governance_context.md §C -->

---

---

## References

All entries are in `paper/references.bib` (verified 2026-10-26; see its `x-verified` fields). Keys cited in this section: `azevedo2026minimal`, `cao2026loopholes`, `cao2026pae`, `fischer1998responsibility`, `fsb2026sound`, `liu2026agentabstain`, `opoku2026toolchain`, `pandey2026certified`, `pandey2026local`, `rusu2026fca`, `santonidesio2018mhc`, `turpin2023unfaithful`, `yu2026cxbench`.
