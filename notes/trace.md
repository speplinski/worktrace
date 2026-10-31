# TRACE (Chang & Chang, arXiv:2607.12480) — reading note for WorkTrace

**Coverage of this reading.** I read the full arXiv HTML (v1, the only version) end to end: Abstract, §1–§8, Appendices A–H, and the reference list. Figures were seen only as their extracted text labels and captions; the photorealistic Fig. 3 is an AI-generated illustration. Math was read from the HTML text rendering. Nothing was skipped. The PDF was not separately consulted, since the HTML is the same v1.

Section numbers below (§x) refer to TRACE's own sections.

---

## 1. Bibliographic data

- **Title:** *TRACE: An Operational Reasoning Schema for Auditable Agentic Commitments*
- **Authors:**
  - Edward Y. Chang, Stanford University (echang@cs.stanford.edu)
  - Emily J. Chang, Quadrivium AI
- **arXiv:** 2607.12480, **v1**, submitted 14 Jul 2026. This is the only version as of 2026-10-25.
- **Subject and classes:** cs.AI. ACM classes H.2.4, I.2.7, C.2.4.
- **Length:** 46 pages, 18 tables, 4 figures (from the arXiv comments field).
- **Venue:** none stated. It is a preprint.
  - It repeatedly refers to a "companion volume" and "companion implementation" that is meant to implement the system and run the experiments.
  - My guess is that this is Chang's ACM Books series, *The Path to AGI* (vol. I = Chang 2025; vol. II = Chang 2026b, *System-2 Reasoning*). **Uncertain:** the paper never names which volume.
- **Acronym:** the paper expands the acronym two ways.
  - Main text: "Typed Reasoning And Commitment Evidence".
  - App. B: the executable writer is "TRACE: Typed Reasoning Argument Critique and Evaluation".
- **Research programme:** the paper belongs to one author's programme and builds on: CRIT, SocraSynth, EVINCE, RCA, ERM, RLER, Trivium, Mnemosyne, MACI, SagaLLM, ALAS (ALAS is named in §7 but has no reference entry), and DIKE/ERIS.

## 2. Problem & motivation

- **§2 is a three-layer argument that "reasoning is not in the language model":**
  1. **Mechanism.** Autoregressive maximum-likelihood training computes *association*. Causal vocabulary is "high-probability tokens, not inference steps". The paper names a "maximum-likelihood trap" / **"modal basin"**: unconditioned sampling, and self-consistency over closely related conditionals, reproduce the familiar answer. Role-conditioned adversarial debate (SocraSynth/EVINCE) is presented as the way out.
  2. **Patches.** Chain-of-thought (CoT) is often post hoc (Turpin 2023; Lanham 2023; Chen et al. 2025c). Outcome-reward RL rewards *what* answer was accepted, not *why*. The reward is "one scalar per episode, blind to the user, the stakes, the claim type, and the evidence standard". RLVR mostly re-weights paths the base model already had (Yue 2025) and can lead to sycophancy.
  3. **Formal absence.** Table 1 lists the formal constructs of reasoning: elenchus, Toulmin roles, Walton schemes and critical questions, Dung attack graphs, burden/standards, DAGs, do(x), identification, partial-identification bounds, counterfactual machinery. None exists "as machinery" in an LLM. A social argument follows (Mercier & Sperber): "a solitary model … contains no second side."
- **Gap stated in §2.3:** "What the field lacks is a shared, typed, versioned schema for recording what was claimed, what kind of reasoning the claim required, what evidence and warrants were offered, what was tested and how, what failed, what is missing, and what verdict followed." Reasoning traces such as CoT, debate transcripts and rewards do not survive the episode as data.
- **Agentic motivation:** durable side effects of agentic systems (memory writes, plan commitments, obligations) should be attributable, contestable and improvable. The analogies are the write-ahead log and the flight recorder.

## 3. Core contribution(s), in their words

- **Abstract:** "a typed, versioned schema for recording reasoning traces, one reference procedure for writing records against that schema, and one operating discipline, no durable state change without a record."
- **Design claim (§1, boxed):** "The unit of contribution is the record, not any stage algorithm. Reasoning evaluation should be decomposed into typed, auditable responsibilities that read and write one versioned TRACE record; a claim must be typed before it is tested, and tested at the standard its type demands; and the record is judged not by a quality scalar but by what its consumers, admission control, plan gating, and temporal learning, can do with it."
- **Five stated contributions (§1):**
  1. The schema: TraceRecord plus its specialization TraceCausalRecord. It is "versioned like an interface, carrying evaluation state, including rung, identification status, bounds, missing evidence, and regret, rather than argument structure alone".
  2. A type system: four layers of typed evaluation, with "an explicit subsumption rule".
  3. A reference writer (Algorithms 1–2), "presented for auditability and cost discipline rather than claimed as optimal".
  4. Two worked illustrations: the music-lessons sentence and the flood search-and-rescue vignette.
  5. TRACE-Bench: a benchmark and ablation *plan*. Its null hypothesis is a single-pass writer.
- **Three goals (§1):**
  - **Record:** one schema.
  - **Protocol:** "no service passes reasoning state to another in any other form". The schema is "simultaneously a log format and an exchange protocol".
  - **Improvement through the callers:** CRIT, SocraSynth, EVINCE, RCA, ERM, RLER, Trivium, Mnemosyne, MACI.
- **Three non-goals (§1):**
  - TRACE "does not itself optimize or improve reasoning".
  - The writer is not optimal.
  - TRACE is "not a universal reasoning-quality metric". Its "scores measure compliance with the declared, versioned TRACE policy".
- **Positioning against AIF (§4.2):** "AIF records an argument's structure, while TRACE additionally records its adjudication … AIF is an interchange format for arguments; TRACE is an interchange format for evaluated arguments and the commitments they license."

## 4. Schema

### 4.1 Full type listing (App. A, verbatim field names)

```
TraceRecord = {
  schema_version, writer_id, policy_version, claim_id,
  claim_text, claim_type, reasoning_family, argument_scheme,
  premises, warrants, role_states, evidence,
  source_credibility, counter_reasons, defeaters,
  context_frame, value_frame, embedded_subclaims,
  routing_decisions, criticisms, stage_results, attack_graph,
  audit_result, score_vector, failed_gates, missing, repair,
  cost, provenance, regret_score, revision_history,
  consumer_actions, final_status
}

TraceCausalRecord = TraceRecord + {
  causal_rung, variables, graph_fragment, assumptions,
  missing_evidence, alternative_explanations, intervention,
  counterfactual_query, identifiability_status, bounds
}
```

The listing gives **field names only**. No JSON types, cardinalities or value domains are published, even though the paper calls it a "versioned JSON type definition".

Value domains that appear elsewhere in the text:
- `role_states` ∈ {stated, elicited, reconstructed, absent, contradicted}.
  - The states apply to roles R1 claim, R2 grounds, R3 warrant, R4 backing, R5 qualifier and R6 rebuttal.
  - They also apply to the extensions R7 counter-considerations, R8 undercutters and R9 presumption/burden.
- Verdict / `final_status` ∈ {Accept, Qualify, Revise, Defer, Reject}, plus "No Argument" at detection (Alg. 2; T6 in Table 16).
- Plug-in output ∈ {pass, fail, bound, defer}.
- `causal_rung` ∈ {1 association, 2 intervention, 3 counterfactual}.
- `identifiability_status` ∈ {identified, partially identifiable / bounded, underidentified}. These are stated in prose and in Table 11 ("identified; bounded; underidentified; defer").

### 4.2 Field groups as presented in §3.2

| Group | Fields | Purpose |
|---|---|---|
| Typing | `claim_text`, `claim_type`, `reasoning_family`, `argument_scheme` | Fix the standard the claim is tested against |
| Anatomy | `premises`, `warrants`, `role_states`, `defeaters` | Includes reconstructed enthymemes and their "charity delta" |
| Evidence and settlement | `evidence`, `source_credibility`, `criticisms`, `attack_graph` | Audited support and the accounting of objections |
| Causal | `causal_rung`, `graph_fragment`, `identifiability_status`, `bounds`, `missing_evidence` | Causal claims (TraceCausalRecord only) |
| Outcome | `final_status`, `score_vector`, `failed_gates`, `missing`, `repair`, `cost` | The verdict and what follows from it |
| Infrastructure | `schema_version`, `writer_id`, `policy_version`, `provenance`, `revision_history`, `regret_score`, `consumer_actions` | Versioning, attribution, history, downstream use |

**Minor inconsistency.** §D.3 says the record "generalizes accordingly, with four added fields: the scheme, the scheme's critical questions with their answers, the warrants, and the embedded subclaims with their routing". App. A has no explicit critical-questions field; they presumably sit in `criticisms` or `stage_results`.

### 4.3 Reasoning types (four layers, §4.2)

1. **Claim types:** factual, definitional, causal, counterfactual, predictive, diagnostic, normative, legal, policy, preference, explanatory.
2. **Reasoning types:** deductive, inductive, abductive, analogical, causal, probabilistic, defeasible, practical, deontic, dialectical, narrative, contextual.
   - Table 6 operationalizes **ten families**: deductive; inductive/statistical; abductive; analogical/case-based; causal; probabilistic; defeasible; practical; deontic/legal/normative; dialectical/contextual.
   - Each family comes with a surface signature, a standard and a typical failure.
3. **Argument schemes (Walton):** expert opinion, witness testimony, sign, cause–effect, correlation–cause, analogy, precedent, rule, consequences, practical reasoning, values, ignorance, popular opinion, slippery slope, threat, commitment.
4. **Context and value evaluation:** audience, stakes, vulnerability, culture, role, institutional norm, fairness, harm, autonomy, reversibility, proportionality. This layer is DIKE–ERIS.

Further structure:
- **Subsumption rule:** "schemes screen, families adjudicate". If a critical question has a formal counterpart, the plug-in decides it and the defect is charged once (§4.3.1, §6).
- **Pearl's ladder** is "the type system for causal claims inside the roof", not the roof itself.
- **Proposition 1 (rung-boundedness of debate):** with only rung-1 evidence, "no debate protocol … can warrant a verdict tighter than the partial-identification bounds"; "The optimal reachable verdict is the bound, or defer."

### 4.4 Versioning (§3.2 rule 2, §4.3.1)

- "Fields are added by version and deprecated by version, never silently mutated; every consumer declares the schema versions it can read; freezing version 1.0 is the first phase of the implementation plan."
- Two versioned objects: `schema_version` and a separate `policy_version`. The policy is "the declared, versioned gates, weights, and thresholds under which a record's score vector and verdict are computed".
- The role vocabulary, scheme registry, family taxonomy and gate metrics are all versioned: "adding a role … is a version bump, not a refutation".
- Score weights α, β are "governance decisions: versioned, audited, and owned by the governance layer (DIKE and ERIS)".
- Writes are atomic and append-only: "a record is never mutated in place, and corrections enter through revision_history" (§3.3).

### 4.5 The operating rule ("TRACE discipline")

- "no durable state change without a TRACE record."
- "A memory is not committed, a plan is not cleared, and an obligation is not updated unless a TRACE record has been written against the schema and carries a verdict." (§1)

### 4.6 Writer API (§3.3)

- Signature: `write(record: TraceRecord) -> WriteResult{record_id, schema_version, policy_version, validation: pass|fail(violations), stored}`.
- Validation is *schema* validation.
- "Who constructs the record is deliberately outside the API." Any process that emits a valid record conforms. That includes "a single structured model call".

### 4.7 The record–consumer contract (§3.4)

**The record guarantees four properties to any conforming consumer:**
- **Immutability:** corrections arrive as new revisions through `revision_history`.
- **Version legibility:** the consumer can refuse versions it does not understand.
- **Self-containment:** "verdict, failed gates, missing items, and repair live inside the record".
- **Provenance:** "every field is attributable to the stage and inputs that produced it".

**The consumer accepts four obligations in return:**
- **Version pinning.**
- **Fail closed:** "an incomplete, invalid, or unreadable record, or one whose decisive evidence is unavailable, must never be treated as acceptance; the safe default is to withhold the durable action".
- **Authority separation:** "the record's verdict is advisory about warrant, not a grant of authority; the consumer owns the mapping from verdict to durable action under its own declared, versioned policy, and a consumer may hold a technically acceptable claim when its own stakes demand more, or escalate to a human".
- **Action write-back:** to `consumer_actions`, "so the record accumulates its own downstream consequences".

**Two corollaries:**
- "a TRACE verdict and a consumer decision are different objects: defer is a property of the record, while Hold is a plan-gate action the consumer writes back".
- "the same record may license different actions for different consumers … without any change to the record."

### 4.8 Reference writer (§5, App. B)

The writer runs a formulation gate (stage 0) and then seven stages:
1. CRIT intake and Toulmin anatomy
2. Family typing and routing
3. Walton scheme and critical questions
4. Family tests, including Pearl typing and identification
5. Gated debate
6. Attack graph and acceptability under grounded semantics
7. Verdict, score and repair

Further details:
- **Debate is optional.** It runs only "if a hard flag is raised and declared stakes and remaining budget warrant escalation" (Alg. 2, line 5).
- **Debate-ness conditions D1–D4:**
  - D1 role separation
  - D2 objective opposition
  - D3 epistemic diversity
  - D4 external adjudication
- **Stopping rule (Prop. 2).** The stop is framed as an SPRT whose thresholds come from ERM regret asymmetries. Outcomes:
  - qualified proposal
  - rejected
  - defer
  - diminishing returns
- **Cost model:** E[cost] ≈ c0 + p_a(c_intake + c_tests) + p_a·p_e·c_debate.

## 5. What is model-declared vs independently verified? Who checks truthfulness?

**What is model- or human-mediated.**
- The writer is unconstrained: "a single structured model call can emit one whole" record.
- The reference writer's intake, typing, warrant reconstruction, source credibility, practical/value fit, alternatives and debate are model-, retrieval- or human-mediated (App. B, cost anatomy).
- §3.3 meets the circularity objection ("the associative generator audits itself") as follows: "The schema converts an unreliable generator into a checkable proposer: every model-mediated emission lands in a typed field that validation, gates, perturbations, and the human-agreement boundary can check."

**What is "largely model-independent once the representation is declared" (§7).**
- Identification against a declared graph (do-calculus).
- Deductive validity (proof or entailment check).
- Acceptability (deterministic semantics over a declared attack graph).
- But: "The representation boundary, the graph, subclaims, warrants, and attack edges themselves, remains model- or human-mediated and is therefore measured separately by typing, extraction, and human-audit agreement."

**Explicit admission (§7.2, limit 7):** "Gates verify field consistency, not field truth. A deterministic gate reads what the record says; a writer that fabricates evidence entries or misstates support can populate fields that pass every gate." The countermeasures they name:
- provenance and source-credibility fields
- "the perturbation suite, which tests that verdicts track decisive evidence"
- they concede "record faithfulness is not world truth".

**Who checks.**
- The schema validator checks conformance only.
- Gates check internal consistency.
- Plug-ins/adjudicator check the support relation *as declared*.
- Sampled human audit covers reconstructed warrants.
- A "cold judge" re-derives the verdict from the ledger (M6, external-judge gap).
- The *consumer* owns acceptance.

**What is missing.** No component checks the record against the acting agent's actual behaviour or against hidden world state. In the vignette they deliberately keep hidden simulation truth out of the writer's premises: "Hidden simulation state is not a premise available to the writer."

**Important for us.** The record documents the reasoning about a *claim*. It does not test whether the declared grounds were what *caused an agent's action*. The perturbation tests (§7 below) target the *adjudicator's verdict*, not the agent's decision.

## 6. Evaluation

**No empirical evaluation.** Nothing is implemented or measured in this paper. Their own statements:
- Abstract: "The vignette is illustrative, not an empirical result; a closed-loop evaluation is specified but left to future work, so the paper's contribution is the schema and its consumer contract, not a performance claim."
- §7.1: the flood numbers "are deterministic fixtures chosen to expose the record logic; they are not experimental measurements" (success 0.92, support 0.28, OOD 0.82).

**What is specified but not run:**
- **TRACE-Bench (App. E).**
  - Items are 1–5 sentence passages with context and an optional evidence ledger.
  - Gold records are annotated by ≥2 independent annotators with adjudication.
  - Three data tiers: synthetic/templated; adapted argument-mining and causal datasets; expert-written mixed arguments.
  - Tasks T0–T7: detection, anatomy, typing/routing, scheme questions, family plug-ins, defeaters, verdict/repair, cost/learning.
  - 17 metrics (Table 15). The hard-gated ones are UnsupportedRate, OverclaimRate, RungCollapseRate and BoundViolationRate.
  - Headline metrics: **WrongAcceptRate** ("fraction of unsupported, overclaiming, or formally invalid arguments that receive Accept or Qualify") and **DeferQuality** (does a defer name evidence that actually flips or tightens the claim when supplied).
  - RecordUtility is a weighted scalar used for reporting only. The rule is "gate, then optimize", lexicographic.
- **Baselines:** direct answer, CoT only, self-consistency, LLM-as-judge, single-pass record emission (the null hypothesis), debate without typed routing (the programme's own earlier method), CRIT without plug-ins, plug-ins without critical questions.
- **Ablations (Table 17):** no detector, no anatomy, no routing, no schemes, no causal plug-in, no ledger, no attack graph, scalar-only, no cost.
- **Planned closed-loop experiment (§7):** "two identical agents on a multi-week task stream, one writing memory through the gate and one writing freely". It "is the headline test of the schema's consumer value".
- **Flood study pre-registered outcomes (§7.1):** unsupported-commitment rate, false-hold rate, decision latency, record reconstructability, repair success, localization of invalidated plan branches.
- **Plan-gating measures (App. H):** "prevented-error rate on plans that pass structural validation yet fail justification, false-hold rate, added latency, repair success, and branch-localization accuracy".
- **Memory-admission measures (App. G):** admission precision/recall against experts, stale-memory correction rate, defer quality.
- **Five pre-registered falsification criteria (§7):**
  1. A single-pass writer matches the staged writer.
  2. The no-gates ablation shows no WrongAcceptRate separation.
  3. The perturbation metrics fail to separate systems.
  4. Human agreement at the typing boundary falls below threshold.
  5. The record-gated agent does not beat its ungated twin on downstream task error and error recurrence.

## 7. Intervention / perturbation / counterfactual testing of evidence

Yes, but **specified only, on the adjudication/debate verdict, and without redundancy handling.**

- **M3, evidence-counterfactual sensitivity (App. F.1):** "Ablate ledger items and re-adjudicate: the verdict should move when decisive evidence is removed and stay fixed when rhetoric-only turns are removed or paraphrased. This is the debate analogue of chain-of-thought faithfulness tests by corruption and truncation (Lanham et al. 2023). A verdict insensitive to its own evidence is fluent consensus, now detectable."
- **M1, procedural invariance:** re-run under role reassignment, speaking order, persona relabelling and seed. The score is CR = 1 − Pr[V_π ≠ V]. "A consensus that flips with seating order is rhetorical, not epistemic."
- **M2, warranted convergence ratio:** the share of belief movement that co-occurs with newly admitted evidence. 1 − WCR is a "sycophancy index".
- **M6, external-judge gap:** "Give the ledger, and only the ledger, to an adjudicator that did not participate … A real convergence survives being re-derived from its own evidence by a stranger."
- **"Faithful" consumer sense (§7):** "the verdict is reconstructable from the record alone by a cold judge, and it moves under evidence ablation, so the stated reasons are decisive rather than decorative."
- **"Actionable" sense:** "repairs, when applied, flip verdicts at a measurable rate, and defers name evidence that resolves them when supplied". This is an *add-evidence* intervention, tested through DeferQuality.
- **Epistemic tier two (§7.1):** "checkable without any ground truth … whether a verdict survives role, order, and seed permutation and whether it moves when decisive evidence is ablated and stays when only rhetoric is paraphrased". It is "the contamination-resistant core of TRACE-Bench, resistant by test design rather than by secrecy". "The paper's warrant lives in tiers one and two."
- **Worked example:** the music trace reports that "procedural-invariance reruns with permuted roles reproduce the verdict, and the ledger alone … suffices for a cold judge to re-derive it". This is narrative, not measured.
- **Counterfactuals elsewhere** appear as a *claim type* (rung 3) and as CRIT's "counterfactual questioning" of context shift. They are not used as an intervention protocol on agent inputs.
- **No intervention-family design beyond these.** There is no "only X", no "invert X" (flip the evidence's sign/content), and no "add second independent source". "Decisive evidence" is never defined operationally, so it is unclear how decisiveness would be established independently of the ablation itself.

## 8. Authority, permissions, delegation, gating of actions

**How a record gates action.** The verdict lives in the record. A consumer reads `final_status` and `failed_gates` and maps them under *its own* policy to an action, then writes that action back to `consumer_actions`.

- **Memory (Mnemosyne, App. G):** "The gate is one function, admit(record), mapping the record's final_status and failed_gates to one of four outcomes: commit, commit with qualifier, quarantine, or reject."
  - Quarantined records stay retrievable but marked.
  - A Defer is "prospective memory": the named missing evidence is "registered as a trigger", and when matching evidence arrives the record is re-adjudicated.
  - "Reconsolidation is re-audit": a defeated premise propagates through `revision_history`, and dependants are queued for re-audit.
- **Plans (MACI, App. H, §7).**
  - Structural admission (well-formedness, acyclicity, resource and temporal constraints) "belongs to the plan validator". "TRACE gates the justificatory residue … TRACE audits the plan's warrants, not its wiring."
  - Consumer actions are **Hold** and **Clear**. Example: "MACI writes Hold to consumer_actions, cites RN(1), and leaves the alternative branches available." Later it writes "Clear for the southern dispatch with the exact authorizing record version".
- **Proceed / escalate / refuse analogue.**
  - Record verdicts: Accept / Qualify / Revise / Defer / Reject.
  - Consumer actions: commit / qualify / quarantine / reject, or Hold / Clear.
  - Escalation appears only as a consumer option: "a consumer may hold a technically acceptable claim when its own stakes demand more, or escalate to a human".
  - In the vignette, a human Incident Commander "approves high-stakes actions". RS(1) clears only with "external Incident Commander approval where required".
  - The record row RV(1) lists "any authority requirement" among its decisive fields, and its consumer consequence is "Clear only the bounded verification action; do not treat it as indirect clearance of the boat dispatch". This is the closest thing to **scope-bounded** clearance: a cleared, reversible information-gathering step does not transfer authority to the irreversible step.
- **Authority is explicitly not granted by records:**
  - "the record's verdict is advisory about warrant, not a grant of authority" (§3.4)
  - "technical TRACE clearance does not manufacture emergency-command authority" (§7.2)
  - "A fluent consensus … is not truth and it is not authority" (§8)
  - Table 10 caption: "without treating prediction as permission"
  - §5.3: "The pipeline improves proposals; it does not make them self-authorizing."
- **Stakes-sensitivity** exists in two places:
  - The writer's debate escalation is gated by "flags, stakes, and budget", a cost device.
  - "in high-stakes settings, when type confidence falls below a declared threshold the correct action is to defer or route to an external adjudicator" (§6).
  - Context layer 4 includes stakes and reversibility.
- **What is absent:**
  - **No permissions model.** There is no permissions/scope field in the schema, and no notion of what the agent was *allowed* to do. The only mention is "any authority requirement" in one vignette row.
  - **No delegation in the MAS sense.** No delegator, delegatee or scope.
  - **No notion that autonomy is earned or revoked based on an agent's tested track record** across episodes or decision classes.
  - **Gating is per claim, per record, every time.** It is not a standing, conditional grant per decision class.
  - The consumer policy that maps verdict to action is declared to exist ("its own declared, versioned policy") but is **not specified or evaluated**.
  - There is no risk–coverage analysis, no escalation-cost model, and no comparison against an outcome-only rule for gating decisions. The closest are the planned "false-hold rate" and "added latency".
  - "Delegation", "adjustable autonomy" and "trust" never occur in the text.

## 9. Redundancy / overdetermination handling

**Not addressed for evidence.**
- M3 is a single-item "remove decisive evidence" ablation. With two redundant decisive items, removing one would leave the verdict fixed and could misread a well-grounded verdict as evidence-insensitive. The paper does not discuss this.
- "Overdetermination" does not appear in the text. "Redundancy" appears only in unrelated senses:
  - double-counting of defects across critical questions and family tests ("defects are counted once")
  - "redundant debate" (cost)
  - "Annotation should be redundant"

**Adjacent idea: source correlation, not overdetermination.**
- §5.3 and App. F say that correlated generators make agreement cheap.
- Prop. 4 / M5 define an effective panel size n_eff = n/(1+(n−1)ρ̄).
- "consensus is weak evidence under correlated generators".
- This concerns redundancy among *agents/judges*, not among evidence items supporting one decision. It bears on our "add second source" intervention: they would predict that a correlated second source adds little. That is a useful citation for motivating *independence* of the added source.

## 10. Limitations

**Acknowledged (§7 non-claims, §7.2):**
- The staging is not optimal.
- The family taxonomy is not complete.
- Weights are not universal.
- "The model-mediated stages are not claimed to execute reliably; their reliability is measured, not assumed".
- Convergence metrics are not claimed to track truth.
- The benchmark is not representative.
- Hidden confounders; absent or corrupted evidence; underidentification; unknowable counterfactuals; shared priors mean shared errors.
- "Correct causal reasoning does not by itself determine wise action".
- "Gates verify field consistency, not field truth".
- Simulation truth is not an input.
- Clearance does not create command authority.
- No empirical results; the closed loop is future work.

**Limitations I see:**
1. **Zero empirical evidence.** Every metric, benchmark and consumer claim is a plan. Even the schema has only field *names*, with no types or semantics per field.
2. **Unit of analysis.** The unit is the *claim/argument* (text in, verdict out), not the *agent's decision* (situation, permissions, action, consequence). The record says whether a claim is warranted, not whether the agent's behaviour depended on the grounds it declared.
3. **Writer–actor collapse.** The writer may be the same model whose reasoning is recorded ("a single structured model call can emit one whole"). Fabricated but consistent records pass the gates; they admit this. The perturbation suite tests the adjudicator's sensitivity to ledger items, not the actor's.
4. **No redundancy-robust interventions.** Single-item ablation, with "decisive evidence" undefined (see §9 above).
5. **Consumer policy is a black box.** Authority separation pushes the verdict→action mapping onto consumers, but that mapping, the place where autonomy is actually decided, is unspecified and unevaluated.
6. **No cross-episode trust state.**
   - Trivium (temporal regret) and RLER learn policies from records, so there is learning over time.
   - But there is no per-agent or per-decision-class authorization that widens or narrows.
   - Every commitment is gated afresh.
7. **Self-referential programme.** Heavy reliance on the author's own unpublished or under-submission components: Mnemosyne is "under submission", ALAS is uncited, and the "companion volume" is unspecified.
8. **"Faithful" means re-derivable and ablation-sensitive *verdicts*.** It does not mean faithfulness of the stated reasons to the model's internal computation. Calling it "faithful" risks conflation with the CoT-faithfulness literature they cite.
9. **Debate-centric.** Much machinery (SPRT stopping, D1–D4, M1–M6) concerns multi-LLM debate convergence, which is orthogonal to delegation.
10. **Naming inconsistency** of the acronym between main text and App. B.

## 11. Related work they cite that matters to us

**CoT faithfulness / unfaithful reasoning**
- Turpin, M., Michael, J., Perez, E., Bowman, S. R. (2023). Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting. NeurIPS.
- Lanham, T., Chen, A., Radhakrishnan, A., et al. (2023). Measuring faithfulness in chain-of-thought reasoning. (arXiv; no venue given in their list.)
- Chen, Y., Benton, J., Radhakrishnan, A., et al. (2025c). Reasoning models don't always say what they think. arXiv:2505.05410.
- Huang, J., Chen, X., Mishra, S., et al. (2024). Large language models cannot self-correct reasoning yet. ICLR.
- Perez, E., Ringer, S., Lukošiūtė, K., et al. (2023). Discovering language model behaviors with model-written evaluations. Findings of ACL.
- Sharma, M., Tong, M., Korbak, T., et al. (2024). Towards understanding sycophancy in language models. ICLR.
- Mirzadeh, I., et al. (2025). GSM-Symbolic. ICLR.
- Wu, Z., et al. (2024). Reasoning or reciting? … counterfactual tasks. NAACL.

**Argumentation (schemas, interchange, acceptability, burden)**
- Toulmin, S. E. (1958). *The Uses of Argument*. CUP.
- Walton, D., Reed, C., Macagno, F. (2008). *Argumentation Schemes*. CUP. Walton (2006) *Fundamentals of Critical Argumentation*; Walton (2013) *Methods of Argumentation*, CUP.
- Dung, P. M. (1995). On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games. *Artificial Intelligence* 77(2):321–357.
- Prakken, H. (2010). An abstract framework for argumentation with structured arguments. *Argument & Computation* 1(2):93–124.
- Modgil, S., Prakken, H. (2014). The ASPIC+ framework for structured argumentation: a tutorial. *Argument & Computation* 5(1):31–62.
- Toni, F. (2014). A tutorial on assumption-based argumentation. *Argument & Computation* 5(1):89–117.
- Baroni, P., Caminada, M., Giacomin, M. (2011). An introduction to argumentation semantics. *KER* 26(4):365–410.
- Bench-Capon, T., Dunne, P. E. (2007). Argumentation in artificial intelligence. *AIJ* 171:619–641.
- Prakken, H., Vreeswijk, G. (2002). Logics for defeasible argumentation. *Handbook of Philosophical Logic* vol. 4, 219–318.
- Gordon, T. F., Prakken, H., Walton, D. (2007). The Carneades model of argument and burden of proof. *AIJ* 171:875–896.
- Bench-Capon, T. (2003). Persuasion in practical argument using value-based argumentation frameworks. *J. Logic & Computation* 13(3):429–448.
- Atkinson, K., Bench-Capon, T. (2007). Practical reasoning as presumptive argumentation using action based alternating transition systems. *AIJ* 171:855–874.
- Chesñevar, C., McGinnis, J., Modgil, S., Rahwan, I., Reed, C., Simari, G., South, M., Vreeswijk, G., Willmott, S. (2006). Towards an argument interchange format. *KER* 21(4):293–316. **This is the closest-in-kind prior schema they compare against.**
- Lawrence, J., Bex, F., Reed, C., Snaith, M. (2012). AIFdb: infrastructure for the argument web. COMMA, 515–516.
- Pollock, J. L. (1987). Defeasible reasoning. *Cognitive Science* 11(4):481–518.
- van Eemeren, F. H., Grootendorst, R. (2004). *A Systematic Theory of Argumentation: The Pragma-Dialectical Approach*. CUP.
- Lippi & Torroni (2016), Argumentation mining. *ACM TOIT* 16(2).
- Lawrence & Reed (2019), Argument mining: a survey. *Computational Linguistics* 45(4).
- Wachsmuth et al. (2017) EACL; Wachsmuth et al. (2024) LREC-COLING.
- AI & law: Ashley (1990); Prakken & Sartor (1996) *AI & Law* 4; Bench-Capon & Sartor (2003) *AIJ* 150.

**Belief revision / truth maintenance (relevant to revocation and append-only revision)**
- Alchourrón, Gärdenfors, Makinson (1985). *J. Symbolic Logic* 50(2):510–530.
- Doyle, J. (1979). A truth maintenance system. *AIJ*.
- de Kleer, J. (1986). An assumption-based TMS. *AIJ*.
- Reiter (1980) *AIJ* 13; McCarthy (1980) *AIJ* 13.

**Decision theory / sequential testing (relevant to escalation cost)**
- Savage (1954); Raiffa & Schlaifer (1961).
- Howard, R. A. (1966). Information value theory. *IEEE TSSC* 2(1):22–26.
- Wald (1945) *Ann. Math. Stat.* 16(2); Wald & Wolfowitz (1948) *Ann. Math. Stat.* 19(3).

**Causal inference**
- Pearl, J. (2009). *Causality*, 2nd ed., CUP. Pearl & Mackenzie (2018). *The Book of Why*.
- Manski, C. F. (1990). Nonparametric bounds on treatment effects. *AER* 80(2):319–323.
- Balke, A., Pearl, J. (1997). Bounds on treatment effects from studies with imperfect compliance. *JASA* 92(439):1171–1176.
- Shpitser, I., Pearl, J. (2006). Identification of joint interventional distributions in recursive semi-Markovian causal models. AAAI.
- Imbens & Rubin (2015), CUP; Peters, Janzing, Schölkopf (2017), MIT Press; Guo et al. (2020) *ACM CSUR* 53(4); Feder et al. (2022) *TACL* 10.
- Kıcıman, Ness, Sharma, Tan (2024). Causal reasoning and LLMs. *TMLR*. Zečević et al. (2023). Causal parrots. *TMLR*.
- Jin et al. (2023) CLadder, NeurIPS; Jin et al. (2024) Corr2Cause, ICLR; Geng et al. (2026) CausalT5k.

**Debate / correlated judges (relevant to "second source" independence)**
- Aumann (1976) *Ann. Stat.* 4(6); Geanakoplos & Polemarchakis (1982) *JET* 28(1); DeGroot (1974) *JASA* 69.
- Ladha, K. K. (1992). The Condorcet jury theorem, free speech, and correlated votes. *AJPS* 36(3):617–634.
- Irving, Christiano, Amodei (2018), AI safety via debate. Brown-Cohen, Irving, Piliouras (2024, ICML; 2025, arXiv:2506.13609).
- Du et al. (2024b) ICML; Liang et al. (2024) EMNLP; Wynn, Satija, Hadfield (2025); Yao et al. (2025); Choi, Zhu, Li (2025) NeurIPS; Zhang et al. (2025).

**Author's own agent-systems line (cite for gating and admission)**
- Chang & Geng (2025). SagaLLM: context management, validation, and transaction guarantees for multi-agent LLM planning. *PVLDB* 18(12):4874–4886.
- Chang, Geng, Chang (2027). Mnemosyne: agentic transaction processing for validating and repairing AI-generated workflows. Under submission, PVLDB.
- Chang & Geng (2026). Epistemic regret minimization: label-free causal critique beyond outcome reward. arXiv:2602.11675.
- Chang (2026c). Trivium: temporal regret as a first-class objective for causal-memory controllers. arXiv:2606.04421.
- Chang (2026a). Diagnosing and mitigating sycophancy and skepticism in LLM causal judgment. ACL 2026.
- Chang (2023a). Prompting LLMs with the Socratic method (CRIT). IEEE CCWC, arXiv:2303.08769.
- Chang (2023b). SocraSynth. CSCI; arXiv:2402.06634.
- Chang (2024). EVINCE. arXiv:2408.14575.
- Chang (2025). *Multi-LLM Agent Collaborative Intelligence*, vol. I, ACM Books (source of MACI).
- Chang (2026b). *System-2 Reasoning …*, vol. II, ACM Books.

**Not cited at all — the gap our contribution (1) fills:**
- MAS delegation and trust theory: Castelfranchi & Falcone; Jennings; Wooldridge; social commitments (Singh); norms.
- Adjustable / sliding autonomy: Scerri, Pynadath, Tambe; Bradshaw; Dorais; Sheridan & Verplank levels of automation.
- Provenance standards: W3C PROV and data-provenance literature. "Provenance" is only a field.
- Selective prediction / abstention / risk–coverage: Geifman & El-Yaniv; Chow; conformal.
- Modern agent-auditing and agent-logging work. They do not cite contemporary LLM-agent audit, oversight or permissioning papers.

## 12. Verbatim quotes useful for our related work

1. §1 (operating rule): "no durable state change without a TRACE record. A memory is not committed, a plan is not cleared, and an obligation is not updated unless a TRACE record has been written against the schema and carries a verdict."
2. §3.4 (authority separation): "the record's verdict is advisory about warrant, not a grant of authority; the consumer owns the mapping from verdict to durable action under its own declared, versioned policy, and a consumer may hold a technically acceptable claim when its own stakes demand more, or escalate to a human."
3. §7.2 (limit 7): "Gates verify field consistency, not field truth. A deterministic gate reads what the record says; a writer that fabricates evidence entries or misstates support can populate fields that pass every gate."
4. App. F.1, M3: "Ablate ledger items and re-adjudicate: the verdict should move when decisive evidence is removed and stay fixed when rhetoric-only turns are removed or paraphrased."
5. §7 (consumer claims): "Faithful: the verdict is reconstructable from the record alone by a cold judge, and it moves under evidence ablation, so the stated reasons are decisive rather than decorative."
6. §8: "What the record buys is not correctness but attributability: when the system is wrong, the record says where."

Extras:
- §7: "TRACE audits the plan's warrants, not its wiring."
- §2.2, against outcome reward: "Outcome reward addresses what answer was accepted while leaving unclear why the answer was correct, why another answer was wrong, or which hidden assumption failed".

## 13. Positioning for WorkTrace

### 13.1 What TRACE already covers (we must NOT claim as new)

- **A typed, versioned, append-only record schema** for an agent's reasoning, with:
  - verdict, failed gates, missing items and repair *inside* the record
  - provenance per field
  - revision history
  - write-back of downstream actions (`consumer_actions` ≈ our "observed consequences" slot, at least as declared actions)
- **The principle that a record must exist before a durable action** (memory commit, plan clearance), with fail-closed consumers. We cannot claim "gate actions on a structured evidence record" as novel.
- **Separation of the record's verdict from authority to act**, with consumer-side escalation to a human and stake-dependent strictness. We cannot claim "the auditor's verdict is not authority" or "the same evidence may license different actions at different stakes" as novel.
- **An outcome vocabulary of accept/qualify/defer/reject plus hold/clear/quarantine**, where "defer" names missing evidence and a bounded repair (an information-gathering action). Our proceed/escalate/refuse needs to be related to this, not presented as the first such triad. Their "defer + repair" is close to an *evidence-seeking* option we may lack.
- **The critique of outcome-only signals.** They argue that records beat scalar outcomes for learning (§2.2; the "Consequential" claim in §7). We cannot claim to be first to argue "judge by reasoning record, not task success". We *can* claim to be first to *test* it for delegation.
- **Ablation-based sensitivity of a verdict to its stated evidence (M3), as a faithfulness criterion**, plus "cold-judge" reconstructability and procedural invariance. They explicitly link this to Lanham-style CoT corruption tests. Our "remove X" intervention is *not* novel in isolation.
- **Contamination resistance "by test design rather than by secrecy"** through perturbation suites. Our Goodhart story must cite this.
- **A typed graph of grounds:** Toulmin roles, warrants, attack graph, causal `graph_fragment`. A "graph of declared grounds" per se is not new. AIF is also prior art; they cite it.

### 13.2 What TRACE leaves open (our space)

1. **Decision episode vs claim record.** TRACE's unit is a *claim* adjudicated from text. Ours is an *agent's decision episode* that carries **information available** and **permissions**, which TRACE lacks: no permissions/scope field, and the only "authority" mention is in prose. Our episode also binds declared grounds to the *action taken* and the *observed consequences*.
2. **Behavioural verification of declared grounds.**
   - TRACE ablates evidence and re-runs the *adjudicator*. It concedes that gates check consistency, not truth, and that the writer can be the same model.
   - We intervene on the *agent's inputs* and observe whether its *action* changes as its declared grounds predict. That tests the actor, not the judge.
3. **Redundancy-robust intervention family.** TRACE has single-item "remove decisive evidence" only. It has no "only X", no "invert X", and no "add independent second source", and no treatment of overdetermination, where single ablation produces false "insensitive" readings. Their correlated-generator / n_eff argument supports our insistence on *independent* second sources and is citable.
4. **Earned, conditional, revocable autonomy per decision class.**
   - TRACE gates every commitment afresh, per record.
   - The consumer's verdict→action policy is "declared" but unspecified.
   - There is no standing authorization that widens or narrows with an agent's tested track record, no decision-class scoping, and no revocation trigger.
   - This is exactly our delegation rule.
5. **Empirical test.** TRACE has no data and no results.
   - We provide held-out generated episodes.
   - We provide a risk–coverage comparison against an outcome-only rule.
   - We price escalation cost explicitly. TRACE only plans "false-hold rate" and "added latency".
6. **MAS bridge.** TRACE cites no delegation, trust or adjustable-autonomy literature. Our contribution (1) is uncontested by it.

### 13.3 How close is TRACE's gating to our delegation rule?

- **Close in architecture.** A record is a precondition of action. A consumer maps record status plus its own stakes to proceed (Clear/commit), hold or refuse (Hold/quarantine/reject), or escalate to a human. Scope is bounded in the narrow sense that clearing a reversible verification step does not clear the irreversible dispatch (RV(1)).
- **Far in substance.**
  1. TRACE's gate is evaluated **per claim, per instance**, on the *warrant of a claim*. Ours is a standing rule **per decision class**, conditioned on the agent's *tested behaviour towards evidence* across episodes.
  2. TRACE's gate inputs are writer-produced verdicts, consistency checks only. Ours are intervention-test outcomes on the actor.
  3. TRACE does not specify or evaluate the verdict→action policy. We do, against an outcome-only baseline, with escalation cost.
- **Framing for us:** TRACE's "consumer policy" is precisely the unspecified slot our delegation rule fills.

### 13.4 How close are `missing` / `failed_gates` / "what was tested and failed" to our verifiability tests?

- **Close in vocabulary, different in object.**
  - `missing` and `failed_gates` record which *evidential or formal conditions on the claim* are unmet (unsupported premise, rung collapse, bound violation, OOD support gate) and what evidence would resolve them.
  - They are produced by the writer/adjudicator and describe the *argument's* status.
  - Our verifiability tests ask whether the *agent's decision actually depends on its declared grounds* under remove / only / invert / add-source interventions. They describe the *agent's* evidence-responsiveness.
- **Closest TRACE analogues** are M3 and DeferQuality ("defers name evidence that resolves them when supplied", i.e., add-evidence → verdict flip). Both are specified-but-unrun tests on the *verdict*, not on the actor's action. Neither handles redundancy.

### 13.5 One-sentence differentiation (draft for related work)

> TRACE (Chang & Chang, 2026) specifies a typed, versioned record that must exist before an agent's durable state changes and leaves the verdict-to-action mapping to each consumer's own policy. WorkTrace supplies what that slot lacks: a decision-class-level delegation rule that grants, conditions and revokes autonomy based on intervention tests (redundancy-robust remove/only/invert/add-source tests on the agent's own decisions, not on an adjudicator's verdict) that check whether the agent's actions actually track its declared grounds. We evaluate that rule empirically, on held-out episodes, against an outcome-only rule with escalation cost; TRACE specifies its evaluation but runs none.

A shorter variant:
> Where TRACE records and adjudicates the warrant for each commitment, WorkTrace tests whether an agent's decisions respond to their declared grounds and uses that tested behaviour to decide which classes of decisions the agent may take without escalation.
