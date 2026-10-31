# 2 Background and related work

*Draft v1, 25 Oct 2026. Facts taken only from `notes/`; the source note is given in an HTML comment after each paragraph. Each paragraph ends with one differentiation sentence.*

**2.1 Delegation and trust in multi-agent systems.** Castelfranchi and Falcone (1998) define delegation as one agent relying on another for a task, and grade it from weak to strict and from open to closed. Their socio-cognitive account makes trust a decision to delegate, indexed by trustor, trustee, context, task and goal, and grounded in beliefs about competence, willingness and opportunity (Castelfranchi & Falcone, 2000). Scerri et al. (2002) cast adjustable autonomy as a cost-sensitive transfer of control between agent and human, but their model *assumes* a given quality of agent decisions. Lee and See (2004) ask for reliance calibrated to the system's real capability. Work on trust across tasks shows that trust can be transferred by matching task requirements to agent features (Falcone & Castelfranchi, 2008; Venanzi et al., 2011), that category priors should give way to direct evidence (Burnett et al., 2010), and that transfer follows task similarity, from harder tasks to easier ones (Soh et al., 2020). Tomašev et al. (2026) bring this tradition to LLM agents. They propose authority graduated by trust, with "algorithmic circuit breakers" for revocation and behavioural metrics as trust signals, and they note that current systems "lack robust mechanisms for the dynamic assessment of competence". Their framework is conceptual, without a measurement procedure or evaluation. *We give an operational instance, tested in a pre-registered pilot: competence is estimated per decision class from intervention tests rather than assumed (Scerri) or read from reputation.*

<!-- r2_mas_delegation_theory.md; r3_trust_transfer_classes.md; r3_intelligent_delegation.md -->

**2.2 Reasons-responsiveness and meaningful human control.** Fischer and Ravizza (1998) ground responsibility in a decision mechanism that is moderately reasons-responsive: it recognises reasons and reacts to them across a range of circumstances. Santoni de Sio and van den Hoven (2018) recast this as the *tracking* condition of meaningful human control. A system must "demonstrably and verifiably" respond to the relevant human reasons, and good results can come from "tracking the wrong property". Mecacci and Santoni de Sio (2020) operationalise tracking for dual-mode vehicles, and Veluwenkamp (2022) argues that the reasons tracked must be normative. CARE-Drive (Suryana et al., 2026) is the first behavioural test of tracking for a foundation model. It varies decision facts and prompt-supplied reasons for a single-step driving model and estimates the sensitivity of its decisions. It has no per-case ground truth for which fact should decide, no escalation option, and no link to delegation, and it does not separate recognising a reason from acting on it. *DSA carries the tracking test to multi-step agents and to external evidence whose decisive role and redundancy are set by construction, relative to one reading of the policy. It scores receptivity and reactivity separately and uses the resulting profile to allocate autonomy.*

<!-- r4_care_drive.md §1, §2, §5.1 -->

**2.3 Traces, provenance and auditability.** Structured provenance has a long history (W3C, 2013). For LLM agents, LEDGER builds layered claim-to-evidence graphs over observed sessions and states the problem crisply: "Visibility, however, is not the same as auditability" (Kim et al., 2026). TRACE specifies a typed record that must exist before any durable state change, and leaves to each consumer the policy that maps a verdict to an action (Chang & Chang, 2026). DNative-Twin takes the committed decision as its unit of replay and comparison, and treats authority as "granted in advance" (Pang et al., 2026). DEMM grades whether a decision's evidence suffices for an external audit and warns against the "container fallacy" (Solozobov, 2026). Graph of Trace records the agent's own declared dependencies as justification edges (Gao et al., 2026a). A recent survey organises the field around six trust functions: verification, attribution, debugging, safety enforcement, audit and recovery. It lists an authorization relation as open (Wang et al., 2026a). *These systems make decisions inspectable. None tests whether the recorded grounds are what the decision depends on, and none decides what an agent may do next.*

<!-- ledger.md; trace.md; dnative_twin.md; r2_reconstructability.md; r2_tracing_systems.md; survey_traces_to_trust.md -->

**2.4 Faithfulness and evidence interventions.** Stated reasons can be unfaithful (Turpin et al., 2023; Lanham et al., 2023), and interventions are the standard test. Atanasova et al. (2023) insert inputs and reconstruct inputs from explanations. Matton et al. (2025) compare the causal effect of input concepts with how often explanations cite them. Pawar et al. (2026) test necessity and sufficiency of the factors a model cites. Khanzadeh (2026) edits the agent's own reasoning steps. Closer to agents, AgentAbstain pairs should-act and should-abstain tasks that differ by one perturbation (Liu et al., 2026). Liao (2026) changes the source authority of evidence in next-action tasks. "Copies or Sources?" (Gao et al., 2026b) and GraphEcho (Wang et al., 2026b) contrast copied with independent sources, and Nautil removes an investigator's cited grounds against a matched control (Bi et al., 2026). AUDITA formalises overdetermination with actual causation and shows that single-cause deletion fails under redundancy (Du & Chen, 2026). The design itself, an input change with an expected response, has a longer lineage: metamorphic testing in software engineering (Segura et al., 2016), behavioural test suites such as CheckList (Ribeiro et al., 2020), contrast sets (Gardner et al., 2020) and counterfactually augmented data (Kaushik et al., 2020), and the diagnosis of models that are right for the wrong reasons through heuristics (McCoy et al., 2019) or shortcuts (Geirhos et al., 2020). *The operators exist. We compose them, adding an independent source and then removing the original, to separate redundancy from non-use for one decision. We read the result against the agent-declared grounds and use it prospectively to allocate autonomy, not retrospectively to attribute blame.*

<!-- r2_faithfulness_interventions.md; ariadne.md; r3_evidence_interventions.md; r3_oversight_and_profiles.md (AgentAbstain); r2_causal_attribution.md -->

**2.5 The outcome–process gap.** Several 2026 benchmarks show that outcome checks pass agents whose process is defective: CXBench in regulated customer-experience workflows (Yu et al., 2026), procedure-aware evaluation of τ-bench (Cao et al., 2026), deterministic evidence-path checks in GroundEval (Flynt, 2026), and "lucky passes" in software-engineering agents (Sahoo et al., 2026). ToolChain-CRC (conformal risk control) proves that calibration on final answers cannot control unsupported intermediate steps (Opoku & Banahene, 2026). Cao (2026) adds a caution that applies to any benchmark of this kind, ours included: when a natural-language policy is silent, ambiguous or contradictory, a single gold answer scores policy ambiguity as agent error. *These audits check procedure or evidence paths. We check whether the action depends on the evidence that should warrant it, which a procedurally compliant trace can hide, and we show that the same kind of ambiguity can decide which delegation rule appears to work (§6.1).*

<!-- r2_agent_evaluation.md; r3_outcome_process_gap.md; r3_certification_stats.md -->

**2.6 Graduated autonomy and certified deployment.** Several systems already widen or narrow agent autonomy from experience. The Digital Apprentice promotes per-skill tiers when correction rates fall (Weber & Taneja, 2026). Hedwig learns check-in behaviour from a developer's approvals (Shukla et al., 2026). Sovereign-OS moves permissions with audited outcomes (Yuan et al., 2026). Minimal Oversight caps authority by a raw success rate, after correcting for masking (Azevedo, 2026). Trust Before Autonomy prescribes a gated, revocable ladder (Angelidis et al., 2026). Earned Authority shows that self-produced evidence must not raise a fixed ceiling (Zhang & Zhang, 2026). The Agent Control Protocol accumulates only penalties from history (Fernandez, 2026). Agent Reliability Profiles define action classes and autonomy tiers for financial services (Hsu et al., 2026). On the statistical side, READY qualifies confidence-threshold escalation policies on held-out cases, with explicit review cost and an LLM-judged process defect (Chatrath et al., 2026). Shen (2026) certifies per model–task pair; Role-Stratified CRC certifies per stratum (Rahman et al., 2026); Conformal Selective Acting certifies anytime (Khosravi & Huo, 2026). Pandey et al. (2026a) gate actions on agreement among sources from separate control domains. *Each delegates on outcomes, corrections, approvals, confidence, judged traces or source counts. We delegate on interventionally measured DSA, and we compare against these rules run through one certification engine.*

<!-- r2_learned_permissions.md; r3_earned_autonomy_family.md; r4_minimal_oversight.md; r2_fernandez_series.md; r3_oversight_and_profiles.md; r3_ready.md; r3_certification_stats.md; r4_pandey_certifier.md -->

**2.7 Answer keys as part of the instrument.** Every test of this kind needs an oracle that says what the correct response is, and the oracle problem is a central difficulty of software testing (Barr et al., 2015). Knight and Leveson (1986) showed that independently written versions of a program fail on the same inputs far more often than independence would predict, because their authors find the same cases hard; the lesson carries to two oracles written from one specification. In machine learning, label errors in test sets change the ranking of models (Northcutt et al., 2021), and disagreement among human annotators is a property of the task rather than noise to be averaged away (Plank, 2022). Jacobs and Wallach (2021) read such problems through measurement theory: a score is valid only if the construct it operationalises and the procedure that produces its labels are both examined. Multiverse analysis reports a result under every defensible analytic choice instead of one (Steegen et al., 2016), and formalising law as code shows that statute text leaves choices the formaliser must make explicit (Merigoux et al., 2021). *We apply these lessons to the normative map of an agent evaluation: we log the readings of the policy that the oracles encode, report the primary result under every logged combination, and show that the choice of reading decided which delegation rule appeared to work (§6.1, §8).*

<!-- verified 2026-10-29 via the arXiv and Crossref APIs; see references.bib x-verified fields -->

---

## Table 1 — Comparison with the closest work (✓ present; (✓) partial, see the notes; – absent)

Legend: ✓ = present; ◐ = partial (see footnote); – = absent. Columns:
- **(a) Decision unit:** a single decision is the unit of analysis.
- **(b) External-evidence interventions:** the agent's external evidence is changed and the agent is re-run.
- **(c) Redundancy:** redundant or overdetermined evidence is handled.
- **(d) Declared grounds:** the agent's own stated grounds are scored.
- **(e) Per-class autonomy:** autonomy is allocated per class of decisions or tasks.
- **(f) Revocation:** autonomy is withdrawn.
- **(g) Held-out:** evaluation on held-out cases.
- **(h) Shift:** evaluation under distribution shift.
- **(i) Empirical:** empirical study with LLM agents.

| Work | (a) decision unit | (b) evidence interventions | (c) redundancy | (d) declared grounds | (e) per-class autonomy | (f) revocation | (g) held-out | (h) shift | (i) empirical |
|---|---|---|---|---|---|---|---|---|---|
| LEDGER (Kim et al., 2026) | – | – | – | – | – | – | – | – | ◐¹ |
| TRACE (Chang & Chang, 2026) | ◐² | – | ◐³ | ✓ | – | – | – | – | – |
| DNative-Twin (Pang et al., 2026) | ✓ | ◐⁴ | – | – | – | – | – | – | – |
| DEMM (Solozobov, 2026) | ✓ | – | – | – | – | – | – | – | – |
| Project Ariadne (Khanzadeh, 2026) | – | – | – | ◐⁵ | – | – | – | – | ◐⁶ |
| Pawar et al. (2026) | ◐⁷ | ◐⁸ | – | ✓ | – | – | – | – | ✓ |
| AgentAbstain (Liu et al., 2026) | ◐⁷ | ✓ | – | – | – | – | – | – | ✓ |
| AUDITA (Du & Chen, 2026) | – | – | ✓ | – | – | – | – | – | ◐⁹ |
| CARE-Drive (Suryana et al., 2026) | ✓ | ◐¹⁰ | – | – | – | – | – | – | ✓ |
| CXBench (Yu et al., 2026) | – | – | – | – | – | – | – | – | ✓ |
| Pandey et al. (2026a) | ✓ | ◐¹¹ | ✓ | – | – | – | – | – | ✓ |
| Intelligent AI Delegation (Tomašev et al., 2026) | – | – | – | – | ◐¹² | ◐¹² | – | – | – |
| Trust Before Autonomy (Angelidis et al., 2026) | – | ◐¹³ | – | – | ◐¹² | ◐¹² | – | – | – |
| Digital Apprentice (Weber & Taneja, 2026) | – | – | – | – | ✓ | ✓ | – | – | – |
| Hedwig (Shukla et al., 2026) | – | – | – | – | ✓ | ✓ | – | – | ◐¹⁴ |
| Minimal Oversight (Azevedo, 2026) | – | – | – | – | ✓ | ◐¹⁵ | – | – | – |
| READY (Chatrath et al., 2026) | – | – | – | – | ◐¹⁶ | ◐¹⁷ | ✓ | – | ✓ |
| Certified deferral (Shen, 2026) | ◐¹⁸ | – | – | – | ◐¹⁹ | – | ✓ | ◐²⁰ | ◐²¹ |
| Role-Stratified CRC (Rahman et al., 2026) | ◐²² | ◐²³ | – | – | ◐²⁴ | – | ✓ | ✓ | ✓ |
| Conformal Selective Acting (Khosravi & Huo, 2026) | ◐²⁵ | – | – | – | – | ◐²⁶ | ◐²⁷ | ✓ | ◐²⁸ |
| **WorkTrace / DSA (this paper)** | ✓ | ✓ | ✓ | ✓ | ✓ | ◐²⁹ | ✓ | ✓ | ✓ |

Footnotes:
1. LEDGER: two qualitative case studies, no metrics.
2. TRACE: one record per claim or commitment.
3. TRACE: argues that correlated sources add little (effective panel size); no tests.
4. DNative-Twin: replay under declared changes to recorded state; no LLM agent is re-run.
5. Ariadne: intervenes on the agent's generated reasoning steps, not on stated grounds about evidence.
6. Ariadne: single-model QA without tools; numbers internally inconsistent.
7. Pawar, AgentAbstain: single decision or task pair, not multi-step episodes.
8. Pawar: changes input factors of tool-free decisions.
9. AUDITA: live LLM pipelines, but evidence partly simulated.
10. CARE-Drive: varies facts written into a single prompt.
11. Pandey et al.: corrupted sources in synthetic payment episodes.
12. Prescribed, not implemented or evaluated.
13. Trust Before Autonomy: "unanswerable variants" correspond to removing the sole decisive source.
14. Hedwig: evaluated on 11 operations with an LLM judge.
15. Minimal Oversight: implicit, through a decaying success-rate estimate; simulation only.
16. READY: one global threshold per agent and workflow, with per-case accept or escalate.
17. READY: re-qualification on version changes, no statistical monitoring.
18. Shen: single multiple-choice answers, not agent decisions.
19. Shen: one certified confidence threshold per model–task pair.
20. Shen: threshold transfer between two tasks only; the certificate assumes no shift.
21. Shen: eleven small LLMs on multiple-choice QA, without tools.
22. Role-Stratified CRC: individual argument fields of tool calls.
23. Role-Stratified CRC: prompt injections in tool outputs, contrasted with clean runs on recorded traces; agents are not re-run.
24. Role-Stratified CRC: thresholds per argument role, gating field values at run time, not autonomy; recalibration, no revocation.
25. Conformal Selective Acting: act or abstain on single outputs in one stream.
26. Conformal Selective Acting: all certifications reset at fixed epoch boundaries; no data-driven revocation.
27. Conformal Selective Acting: risk is controlled online on the same stream; a held-out split only calibrates the score.
28. Conformal Selective Acting: RLVR-trained LLMs on benchmark streams, including live online fine-tuning, not agents with tools.
29. This paper: revocation is specified (§4.6) but not exercised in the pilot.


---

---

## References

All entries are in `paper/references.bib` (verified 2026-10-26; see its `x-verified` fields). Keys cited in this section: `angelidis2026tba`, `atanasova2023faithfulness`, `azevedo2026minimal`, `bi2026nautil`, `burnett2010bootstrapping`, `cao2026loopholes`, `cao2026pae`, `castelfranchi1998delegation`, `castelfranchi2000trust`, `chang2026trace`, `chatrath2026ready`, `du2026audita`, `falcone2008generalizing`, `fernandez2026acp`, `fischer1998responsibility`, `flynt2026groundeval`, `gao2026copies`, `hsu2026arp`, `khanzadeh2026ariadne`, `khosravi2026csa`, `kim2026ledger`, `lanham2023measuring`, `lee2004trust`, `liao2026provenance`, `liu2026agentabstain`, `matton2025walk`, `mecacci2020mhc`, `opoku2026toolchain`, `pang2026dnative`, `rahman2026rolestratified`, `sahoo2026agentlens`, `santonidesio2018mhc`, `scerri2002adjustable`, `shen2026provable`, `shukla2026hedwig`, `soh2020multitask`, `solozobov2026demm`, `suryana2026caredrive`, `tomasev2026delegation`, `turpin2023unfaithful`, `veluwenkamp2022reasons`, `venanzi2011facing`, `wang2026graphecho`, `weber2026apprentice`, `yu2026cxbench`, `yuan2026sovereign`, `zhang2026earned`; added 2026-10-29: `barr2015oracle`, `gardner2020contrast`, `geirhos2020shortcut`, `jacobs2021measurement`, `kaushik2020cad`, `knight1986independence`, `mccoy2019right`, `merigoux2021catala`, `northcutt2021label`, `plank2022variation`, `ribeiro2020checklist`, `segura2016metamorphic`, `steegen2016multiverse`.
