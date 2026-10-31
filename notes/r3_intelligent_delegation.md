# R3: Tomašev, Franklin & Osindero, "Intelligent AI Delegation" (Google DeepMind, arXiv:2602.11865): full reading

Round-3 reading note, 2026-10-25. Builds on `positioning.md` v2 and on `r2_mas_delegation_theory.md` §2.18, which this note supersedes for this paper. Purpose: find out whether this paper falsifies or narrows W1/W2/W3 or the DSA construct, and extract design lessons.

---

## 0. Read first: verdict for WorkTrace's claims

- **No threat to W2 or W3.** The paper (§§1–7, 42 pp. PDF) contains **no** counterfactual, intervention or evidence-sensitivity test.
  - "counterfactual": 0 occurrences in the body.
  - "evidence": 1 occurrence, about verification artefacts ("the evidence standard required for the task to be considered valid", §6.1).
  - It never speaks of the *basis* of an agent's decision, of declared grounds, of redundancy, or of decision classes.
  - It has no evaluation, no data and no metrics. It is a framework and position paper with protocol sketches.
- **W1 stays as narrowed in v2: "first *operational, tested*"; this paper is the conceptual predecessor.** It already links classic delegation and MAS trust theory to LLM agents. It already proposes trust-scoped "graduated authority", process-based "behavioral metrics", and permissions revoked automatically by "algorithmic circuit breakers". WorkTrace must not claim any of these as concepts.
- **Context-specific trust is already there.** The paper has trust as a "context-dependent threshold", reputation as a "portfolio of signed, context-specific credentials", and "safety floors … for specific classes of tasks".
  - So per-*class* or per-*context* trust is not new, even inside the LLM-agent literature.
  - Our per-*decision*-class unit is finer: decisions inside a task, not task or skill domains. The difference is real but must be argued, not assumed.
- **DSA as a construct: moderate overlap at the level of *desiderata*, none at the level of *measurement*.** The paper lists, as normative requirements for agents, almost every DSA component except evidence grounding:
  - recognising ambiguity and stepping outside the "zone of indifference" ("dynamic cognitive friction");
  - challenging errors yet accepting valid overrides;
  - seeking clarification;
  - staying within attenuated scope;
  - immutable provenance.

  It names no capability construct that bundles them and proposes no way to measure them. DSA is new as a *measured profile*, not as a list of virtues. Write it that way.
- **Most useful lesson: a new baseline H3 must include.** The paper's own proposal for process-based trust is a "transparency score … informed on the clarity and soundness of reasoning and explanations provided" plus a "safety score" for protocol compliance (§4.6, Table 3). Our current baseline list (outcome, approval, history counter, confidence) **lacks a reasoning-trace-quality rule**.
  - A reviewer will ask: "why not just score the reasoning, as DeepMind proposes?"
  - Add a "trace-judged behavioural-metric" baseline: an LLM judge rates the clarity and soundness of declared grounds and protocol compliance. It is the strongest non-interventional process baseline, and beating it is the cleanest empirical answer to this paper.
- **Small corrections to the round-2 note** (§1.3 below):
  - They do **not** cite Lee & See 2004. Their trust-calibration definition is their own wording.
  - They do not cite Scerri et al. 2002 or Parasuraman–Sheridan–Wickens 2000.
  - Their citation of Falcone & Castelfranchi's SMC-A paper as 2002 is wrong (Crossref: 2001), as round 2 already noted.

---

## 1. Bibliographic data and reading status

- **Tomašev, Nenad; Franklin, Matija; Osindero, Simon** (all Google DeepMind). *Intelligent AI Delegation.* arXiv:2602.11865v1 [cs.AI], submitted 12 Feb 2026. License CC BY 4.0. **[verified: arXiv API]**. Only v1 exists as of 25 Oct 2026. No venue: a preprint, not peer-reviewed.
- **What I read:** the **full text**: arXiv HTML (all sections §1–§7, footnotes 1–4, Tables 1–3, the JSON protocol sketches in §6.1), cross-checked against the PDF (42 pp.).
  - The two figures were read as images: Fig. 1 "A flowchart of Task Decomposition and Task Assignment"; Fig. 2 "The adaptive coordination cycle".
  - The reference list (~248 entries) was extracted in full and searched for the classic MAS, trust and automation works; not every entry was checked.
- **Structure:**
  - §1 Introduction
  - §2 Foundations (2.1 Definition, 2.2 Aspects, 2.3 Human organisations)
  - §3 Previous work
  - §4 Framework (4.1 Decomposition, 4.2 Assignment, 4.3 Multi-objective optimisation, 4.4 Adaptive coordination, 4.5 Monitoring, 4.6 Trust & reputation, 4.7 Permission handling, 4.8 Verifiable task completion, 4.9 Security)
  - §5 Ethical delegation (5.1 Meaningful human control, 5.2 Accountability in long chains, 5.3 Reliability & efficiency, 5.4 Social intelligence, 5.5 User training, 5.6 De-skilling)
  - §6 Protocols (MCP, A2A, AP2, UCP; 6.1 delegation-centred extensions)
  - §7 Conclusion
- **There is no "open problems" or "limitations" section.** The open problems in §3 of this note are gaps the authors *state* in passing ("Current delegation systems lack…", "remains non-trivial", "is difficult"), quoted verbatim.

---

## 2. Framework map (with key quotes)

### 2.1 Definition of delegation (§2.1)

> "We define intelligent delegation as a sequence of decisions involving task allocation, that also incorporates transfer of authority, responsibility, accountability, clear specifications regarding roles and boundaries, clarity of intent, and mechanisms for establishing trust between the two (or more) parties. Complex tasks may also involve steps pertaining to task decomposition, as well as careful capability lookup and matching to inform allocation decisions." (§2.1)

> "Delegation (Castelfranchi and Falcone, 1998) is more than just task decomposition … delegation necessitates the assignment of responsibility and authority … and thus implicates accountability for outcomes. Delegation thus involves risk assessment, which can be moderated by trust (Griffiths, 2005)." (§1)

**Aspects (§2.2).**
- Delegator (human/AI) and delegatee (human/AI).
- Task characteristics:
  - complexity, criticality, uncertainty, duration, cost, resource requirements, constraints;
  - **verifiability**: "Tasks with high verifiability … allow for 'trustless' delegation or automated checking. Conversely, tasks with low verifiability (e.g., open-ended research) require high-trust delegatees or expensive, labor-intensive oversight";
  - **reversibility**: "Irreversible tasks … require stricter liability firebreaks and steeper authority gradients";
  - contextuality, subjectivity.
- Granularity, autonomy, monitoring (continuous / periodic / event-triggered), reciprocity.
- Three delegator→delegatee configurations: human→AI, AI→AI, AI→human. Hierarchical vs non-hierarchical.

**Organisational concepts (§2.3).**
- Principal–agent problem.
- Span of control: "how many AI agents a human expert can reliably oversee without excessive fatigue, and with an acceptably low error rate".
- Authority gradient (sycophancy of delegatees).
- Zone of indifference.
- Trust calibration.
- Transaction-cost economics.
- Contingency theory.

Two quotes that matter for DSA:

> "Intelligent delegation therefore requires the engineering of dynamic cognitive friction: agents must be capable of recognizing when a request, while technically 'safe,' is contextually ambiguous enough to warrant stepping outside their zone of indifference to challenge the delegator or request human verification." (§2.3, Zone of Indifference)

> "Trust Calibration. … trust calibration, where the level of trust placed in a delegatee is aligned with their true underlying capabilities. … Explainability plays an important role in establishing trust in AI capability …, yet this method may not be sufficiently reliable or sufficiently scalable. … Calibrating trust in autonomous systems is difficult, as current AI models are prone to overconfidence even when factually incorrect." (§2.3)

### 2.2 Framework pillars (Table 1, §4 preamble)

| Pillar | Core requirement | Technical implementation |
|---|---|---|
| Dynamic Assessment | Granular inference of agent state | Task Decomposition (§4.1), Task Assignment (§4.2) |
| Adaptive Execution | Handling context shifts | Adaptive Coordination (§4.4) |
| Structural Transparency | Auditability of process and outcome | Monitoring (§4.5), Verifiable Completion (§4.8) |
| Scalable Market | Efficient, trusted coordination | Trust & Reputation (§4.6), Multi-objective Optimisation (§4.3) |
| Systemic Resilience | Preventing systemic failures | Security (§4.9), Permission Handling (§4.7) |

> "Dynamic Assessment. Current delegation systems lack robust mechanisms for the dynamic assessment of competence, reliability, and intent within large-scale uncertain environments. Moving beyond reputation scores, a delegator must infer details of a delegatee's current state relative to task execution." (§4)

Note: the "current state" they then list is operational, not epistemic: "real-time resource availability … computational throughput, budgetary constraints, and context window saturation – alongside current load, projected task duration, and the specific sub-delegation chains in operation".

### 2.3 The delegation lifecycle (implicit; reconstructed from §4 and Figs. 1–2)

The paper uses "delegation lifecycle" (§4.6, §4.8: "The delegation lifecycle culminates in verifiable task completion") but never defines it as a list. Reconstructed:

1. **Decomposition (§4.1, Fig. 1).**
   - Analyse criticality, complexity and resources; decide parallel vs sequential.
   - Decision node **"Is Outcome Verifiable?"**: if not, recursively decompose further ("contract-first decomposition").
   - Choose human vs AI by speed and cost; generate proposals; estimate success, cost and duration; keep alternatives; write the final specification ("roles, resource boundaries, progress reporting frequency, and the specific certifications required to prove the delegatee's capability").
2. **Assignment (§4.2).**
   - Centralised registry or decentralised market (bids).
   - Skill and reputation check; negotiation; smart contract fixing monitoring, privacy, **autonomy** and verification terms.
   - "the exact level of autonomy granted … atomic execution … and open-ended delegation … This level of autonomy should not be static; it may be constrained implicitly by market costs or explicitly by the delegator's trust model." Recursive delegation means "delegating the act of delegation itself".
3. **Multi-objective optimisation (§4.3).**
   - Continuous: the delegator seeks Pareto optimality on a "trust-efficiency frontier".
   - It updates beliefs "about each agent's likelihood of success, expected task duration, and cost".
   - A "complexity floor" lets trivial tasks bypass the protocol.
4. **Adaptive coordination (§4.4, Fig. 2).**
   - External triggers: spec change or cancel, resource change, priority change, security alert.
   - Internal triggers: performance degradation, budget overrun, verification failure, unresponsive agent.
   - Then the cycle: monitoring → issue detection → diagnose root cause → evaluate response.
   - Response evaluation (Fig. 2): check reversibility → urgency → scope → "Need Escalation?".
   - Irreversible high-criticality failures go to "Immediate Termination or Human Escalation".
   - Stability measures: "cooldown periods for re-bidding, damping factors in reputation updates, or increasing fees on frequent re-delegation".
5. **Monitoring (§4.5, Table 2).** Five axes:
   - target: outcome-level vs process-level;
   - observability: indirect vs direct;
   - transparency: black-box vs white-box;
   - privacy: full transparency vs cryptographic;
   - topology: direct vs transitive.
6. **Trust & reputation (§4.6).** See §2.4.
7. **Permission handling (§4.7).** See §2.5.
8. **Verifiable completion (§4.8).**
   - Four verification families: direct inspection, trusted third party, cryptographic proofs (zk-SNARKs), game-theoretic consensus.
   - On success, a signed verifiable credential is issued ("Agent A certifies that Agent B successfully completed Task T on Date D to Specification S") and enters B's reputation log.
   - Disputes use escrow, an optimistic model and a challenge bond; post-hoc error discovery "triggers a retroactive update to the delegatee's reputation score".
9. **Security (§4.9).** Threat taxonomy:
   - malicious delegatee: exfiltration, poisoning, verification subversion, resource exhaustion, unauthorised access, backdoors;
   - malicious delegator: harmful tasks, probing, prompt injection, model extraction, reputation sabotage;
   - ecosystem: Sybil attacks, collusion, agent traps, agentic viruses, protocol exploitation, cognitive monoculture.

   Defence in depth: TEEs, least privilege, input sanitisation, DIDs, mTLS.

### 2.4 Trust and reputation (§4.6, Table 3)

> "We define trust as the delegator's degree of belief in a delegatee's capability to execute a task in alignment with explicit constraints and implicit intent. This belief is dynamically formed and updated based on verifiable data streams collected via the monitoring protocols described previously (see Section 4.5)."

> "Reputation serves as a predictive signal, derived from an aggregated and verifiable history of past actions, which act as a proxy for an agent's latent reliability and alignment. We distinguish reputation as the public, verifiable history of an agent's reliability, and trust as the private, context-dependent threshold set by a delegator. An agent may have high overall reputation, yet fail to meet the specific, contextual trust threshold required for certain high-stakes task. … Higher trust enables the delegator to incur a lower monitoring and verification cost."

Three reputation models (Table 3):

| Model | Mechanism (verbatim) | Utility (verbatim) |
|---|---|---|
| Immutable Ledger | "Encodes task outcomes, resource consumption, and constraint adherence as verifiable transactions on a tamper-proof blockchain." | "… though it requires safeguards against 'gaming' via low-risk task selection." |
| Web of Trust | "Utilizes Decentralized Identifiers to issue signed, context-specific Verifiable Credentials attesting to specific capabilities." | "Moves beyond generic scores to a portfolio model, enabling precise delegation based on domain-specific expertise …" |
| **Behavioral Metrics** | "Derives transparency and safety scores by analyzing the execution process, specifically the clarity of reasoning traces and protocol compliance." | "Evaluates how a task is performed rather than just the result, ensuring high-stakes tasks align with safety standards." |

Prose elaboration of behavioural metrics:

> "A final approach would be to focus more on behavioral and explainability metrics, where reputation depends on how an agent performs its task, not just the final outcome. It would be possible to include a transparency score … informed on the clarity and soundness of reasoning and explanations provided, as well as a safety score derived from compliance to predefined safety protocols."

Ledger contents:

> "task completion success or failure, total resource consumption (compute, time), adherence to deadlines, adherence to constraints, and the quality of the final output as judged by the delegator."

Gaming:

> "an agent can inflate its reputation by only accepting simple, low-risk tasks."

**Graduated authority** (the key sentence):

> "Furthermore, trust informs the dynamic scoping of authority and autonomy. This mechanism of graduated authority results in low-trust agents facing strict constraints, such as transaction value caps and mandatory oversight, while high-reputation agents operate with minimal intervention. This dynamic calibration leverages computable trust to optimize the trade-off between operational efficiency and safety."

Attribution under malicious instructions:

> "A critical challenge arises when a trustworthy agent strictly executes malicious human instructions, potentially incurring unfair reputational damage. To mitigate this, agents must rigorously evaluate incoming requests, soliciting clarification or additional context when necessary, or rejecting the requests where appropriate. Furthermore, market audits must distinguish between agent execution failure and malicious directives …"

### 2.5 Permission handling and automatic revocation (§4.7)

- **Low stakes:** "For routine low-stakes tasks, characterized by low criticality and high reversibility …, agents can be granted default standing permissions derived from verifiable attributes – such as organisational membership, active safety certifications, or a reputation score exceeding a trusted threshold."
- **High stakes:** "permissions must be risk-adaptive … granted on a just-in-time basis, strictly scoped to the immediate task's duration, and, where appropriate, gated by mandatory human-in-the-loop approval or third-party authorisation". Motivation: the confused deputy (Hardy 1988).
- **Privilege attenuation in chains:** "When an agent sub-delegates a task, it cannot transmit its full set of authorities; instead, it must issue a permission that restricts access to the strict subset of resources required for that specific sub-task."
  - Semantic constraints (operation-level).
  - "Meta-permissions … govern which permissions a particular delegator in the chain is allowed to grant".
  - An external verifier may be consulted before a permission transfer.
- **Automatic revocation:**

> "Finally, the lifecycle of permissions must be governed by continuous validation and automated revocation. Access rights are not static endowments but dynamic states that persist only as long as the agent maintains the requisite trust metrics. The framework should implement algorithmic circuit breakers: if an agent's reputation score drops suddenly (see Section 4.6) or an anomaly detection system flags suspicious behavior, active tokens should be immediately invalidated across the delegation chain. To manage this complexity at scale, permissioning rules should be defined via policy-as-code …"

- **Protocol sketch (§6.1):** Delegation Capability Tokens (Macaroons/Biscuits) carrying cryptographic caveats, invalidated if the delegatee exceeds scope, with "restriction chaining" along the chain.

### 2.6 Verification (§4.1, §4.8, §6.1)

- "contract-first decomposition as a binding constraint, wherein task delegation is contingent upon the outcome having precise verification. If a sub-task's output is too subjective, costly, or complex to verify …, the system should recursively decompose it further … until the resulting units of work match the specific verification capabilities, such as formal proofs or automated unit tests, of the available delegatees." (§4.1)
- "effective verification is not an afterthought but a constraint on design; … ensuring that every delegated objective is inherently verifiable." (§4.8)
- Fallibility: "verification processes are not infallible. Subjective tasks … can lead to disagreements even when precise rubrics are used, and errors may only be discovered long after a task is marked complete." (§4.8)
- The §6.1 `verification_policy` JSON (A2A Task extension) requires artefacts such as a `unit_test_log` with a validator and a `zk_snark_trace`. "This forces the delegatee to simulate the verification step before accepting the task."

All verification here is **of outcomes or of computation integrity** ("a specific program was executed correctly on a given input"). It is never verification of *why* the delegatee chose what it chose.

### 2.7 Accountability (§4.8, §5.1–5.2)

- Recursive verification in A→B→C: A verifies B's work and "that B has correctly verified the work of its own sub-delegatee C". "Responsibility in delegation chains is transitive and follows the individual branches. Agents are accountable for the totality of the tasks they have been granted and cannot absolve themselves of accountability by blaming subcontractors. Liability is derived from the chain of contracts." (§4.8)
- **Liability firebreaks** (§5.2): "pre-defined contractual stop-gaps where an agent must either: 1. Assume full, non-transitive liability for all downstream actions … 2. Halt execution and request an updated transfer of authority from the human principal." Plus "the system must maintain immutable provenance, ensuring that even if an outcome is unintended, the chain of custody regarding who delegated what to whom remains auditorially transparent."
- Meaningful human control (§5.1):
  - Moral crumple zone (Elish).
  - Cognitive friction vs **alarm fatigue**: "If verification requests for delegation sub-steps are sent to human overseers too frequently, overseers may eventually default to heuristic approval". "friction must be context-aware: … seamless execution for tasks with low criticality or low uncertainty, but dynamically increase cognitive load … when the system encounters higher uncertainty or is faced with unanticipated scenarios."
- Safety floors (§5.3): "mandatory verification steps for specific classes of tasks (e.g., financial transactions or health data handling) that cannot be bypassed for the sake of efficiency."

### 2.8 Multi-agent delegation chains

Chains (A→B→C, X→A→…→Y) recur throughout the paper:
- the zone of indifference propagates intent mismatches ("each agent acting as an unthinking router rather than a responsible actor", §2.3);
- transitive monitoring via signed attestations ("Agent A does not monitor C directly, but instead monitors B's ability to monitor C", §4.5);
- privilege attenuation and meta-permissions (§4.7);
- recursive verification and liability (§4.8);
- liability firebreaks (§5.2);
- revocation "across the delegation chain" (§4.7);
- restriction chaining of DCTs (§6.1).

### 2.9 Monitoring and the faithfulness caveat (§4.5)

> "process-level monitoring … is essential for tasks that are long-running, critical, or where the how is as important as the what."

> "Robust black-box monitoring protocols need to also take into account the fact that the generated model's thoughts in natural language do not always faithfully match the model's true internal state (Turpin et al., 2023)."

The §6.1 monitoring stream levels are `L0_IS_OPERATIONAL, L1_HIGH_LEVEL_PLAN_UPDATES, L2_COT_TRACE, L3_FULL_STATE`.

**Internal tension worth citing.** The paper warns that reasoning traces are unfaithful (§4.5), yet its process-based reputation scores "the clarity and soundness of reasoning and explanations provided" (§4.6). WorkTrace resolves this tension: declared grounds are treated as claims and tested by intervening on the external evidence, not by judging the prose.

### 2.10 Evaluation

**None.** There are no experiments, data, metrics, baselines or formal model. The protocol extensions are illustrative: "neither comprehensive, nor meant as a definitive proposal" (§6.1).

---

## 3. Key questions

### (a) How close is "graduated authority from trust / behavioural metrics" to WorkTrace's per-class revocable autonomy from interventional evidence tests?

**Close in the shape of the mechanism; different in the input, the unit and the validation.**

| Dimension | Tomašev et al. | WorkTrace |
|---|---|---|
| Mechanism | Trust → "dynamic scoping of authority and autonomy"; low trust → "transaction value caps and mandatory oversight"; high reputation → "minimal intervention" (§4.6) | Per class c: proceed / escalate / refuse |
| Revocation | "algorithmic circuit breakers": reputation drops suddenly, or an anomaly detector flags → tokens invalidated (§4.7); damping and cooldowns against oscillation (§4.4) | e-process with hysteresis on the unjustified-action rate |
| **Input (basis of trust)** | Outcome ledger (success, resources, deadlines, constraint adherence, delegator-judged quality); credentials; "behavioral metrics" = clarity and soundness of reasoning + protocol compliance | Interventions on external decision-time evidence (remove / only / invert / add independent second source) against declared grounds, with ground truth by construction |
| Unit | Agent (reputation), qualified by a task-level "context-dependent threshold", "context-specific" credentials ("domain-specific expertise"), and task attributes (criticality, reversibility) | Decision class (decisions within a task) |
| Validation | None | Held-out episodes under evidence shift; matched-coverage comparison with outcome / approval / counter / confidence (and, recommended, trace-judged) rules |
| Escalation cost | Qualitative (alarm fatigue, span of control, "reliability premium") | Explicit c_esc in the risk–coverage evaluation |

Specific checks:
- **Testing the basis of decisions:** **no.** The closest is "how a task is performed rather than just the result" (Table 3). It is operationalised as reasoning clarity and soundness and protocol compliance, i.e. inspection of the trace, not a test of what the action depends on.
- **Counterfactuals:** **no** (0 occurrences). The only "counterfactual" in the reference list is Foerster et al. 2018 (COMA, MARL credit assignment), cited for MARL coordination.
- **Evidence sensitivity:** **no.** "Sensitiv*" occurs only for data sensitivity (privacy) and task criticality.
- **Decision classes / task types:**
  - **Partly.** Task *characteristics* (§2.2) define how strict delegation should be (verifiability, reversibility, criticality).
  - Trust is "context-dependent"; credentials are "context-specific" (portfolio, domain-specific); safety floors apply to "specific classes of tasks" (§5.3).
  - Classes are given by domain or risk, not estimated as competence per class. There is no notion of a *decision* inside a task as the unit.
  - WorkTrace must therefore present per-class granularity as an *inherited* idea (Falcone & Castelfranchi 1999; Lee & See functional specificity; Tomašev et al. context-specific trust). The new part is that class-level competence is **estimated by test**.

Distance in one line: **same governance loop (trust → scoped authority → automatic revocation), with the trust signal left open: outcomes plus reasoning-trace quality. WorkTrace supplies a tested signal for the competence term and validates the loop.**

### (b) Which of their stated gaps does WorkTrace operationalise? (verbatim)

The paper has no list of open problems; these are the gaps it states.

1. **Competence assessment.** "Current delegation systems lack robust mechanisms for the dynamic assessment of competence, reliability, and intent within large-scale uncertain environments." (§4, Dynamic Assessment)
   - WorkTrace operationalises *competence* (evidence handling per class).
   - Not *intent*; we say so (willingness is unmeasured; see the r2 MAS note).
2. **Trust calibration via explanations is unreliable.** "Explainability plays an important role in establishing trust in AI capability …, yet this method may not be sufficiently reliable or sufficiently scalable." and "Calibrating trust in autonomous systems is difficult" (§2.3)
   - WorkTrace: calibration is checked against held-out episodes; trust comes from tests, not explanations.
3. **Unfaithful traces.** "the generated model's thoughts in natural language do not always faithfully match the model's true internal state (Turpin et al., 2023)." (§4.5)
   - WorkTrace: declared grounds are tested by intervention, not read.
4. **Reputation gaming by task selection.** "an agent can inflate its reputation by only accepting simple, low-risk tasks." (§4.6; Table 3)
   - WorkTrace: certification per decision class on *generated* episodes whose class mix the evaluator controls. The agent cannot choose which episodes it is tested on.
5. **Incompetence vs malice; failure vs bad directive.** "This opacity obscures the distinction between incompetence and malice" (§4) and "market audits must distinguish between agent execution failure and malicious directives" (§4.6)
   - WorkTrace operationalises a *related* separation: internal vs external attribution. The generator controls evidence quality, so evidence-caused failures are not charged to the agent.
   - It does **not** address malice. Do not over-claim.
6. **Low-verifiability tasks.** "Conversely, tasks with low verifiability (e.g., open-ended research) require high-trust delegatees or expensive, labor-intensive oversight." (§2.2) and "errors may only be discovered long after a task is marked complete" (§4.8)
   - WorkTrace gives a way to *earn* high trust where outcome verification is unavailable or delayed: verify the **basis** of the decision instead of its outcome.
   - **This is the best framing hook** (§4 below).
7. **The cost of human checking.** "the effective implementation of such human-in-the-loop approaches remains non-trivial. Human expertise can create a scalability bottleneck, as the cognitive load of verifying long reasoning traces …" (§3) and "If verification requests … are sent to human overseers too frequently, overseers may eventually default to heuristic approval" (§5.1)
   - WorkTrace: explicit escalation cost and risk–coverage trade-off; escalate only where class-level tests fail.
8. **Graduated authority and circuit breakers are proposed without a defined trust metric or a validation** (§4.6–4.7).
   - WorkTrace: the defined metric (unjustified-action rate per class), the certificate, the revocation rule, and the held-out test.

Items WorkTrace does **not** address: market and bidding, smart contracts and escrow, cryptographic verification, transitive monitoring, Sybil and collusion, de-skilling, social intelligence, protocols.

### (c) How to phrase W1 to credit them fairly while remaining a contribution

**Do not say:**
- "first to connect MAS delegation theory to LLM agents";
- "we introduce graduated / revocable / trust-scoped autonomy";
- "we introduce process-based trust";
- "first to use verifiability / reversibility as delegation criteria";
- "first per-context trust for agents".

**Draft W1 (contribution list):**

> *W1. An operational and empirically tested instantiation of trust-based delegation theory for LLM agents.* Tomašev et al. (2026) recently carried the socio-cognitive theory of delegation (Castelfranchi & Falcone 1998) and computational trust (Ramchurn et al. 2004) over to AI agents, proposing that trust should scope agents' authority ("graduated authority"), be informed by how a task is performed and not only its result ("behavioral metrics"), and be revoked automatically when trust metrics fall. They leave the trust signal to outcome ledgers, credentials and the clarity of reasoning traces, and do not evaluate the loop. We supply (i) a tested competence signal, the per-decision-class rate of unjustified actions, estimated by interventions on decision-time evidence rather than by reading the agent's reasoning, and (ii) a grant-and-revoke rule built on it, whose predictive validity we measure on held-out episodes against outcome-, approval-, history-, confidence- and trace-judged rules.

**Related-work sentence (short):**

> "Closest in spirit is Tomašev et al.'s (2026) framework for intelligent AI delegation, which grounds LLM-agent delegation in Castelfranchi and Falcone's theory and proposes trust-scoped 'graduated authority' with automatic revocation, informed by process-level 'behavioral metrics'; it does not specify how those metrics are measured beyond reasoning-trace clarity and protocol compliance, and it reports no evaluation. WorkTrace defines one such metric by intervention and tests the resulting delegation rule."

**Introduction framing (one sentence, early):**

> "Recent proposals already argue that AI agents should earn graduated, revocable authority from trust (Tomašev et al., 2026); what is missing is a basis for that trust that does not reduce to track records or to the agent's own account of its reasoning."

This ties directly to the working title "Beyond Track Records".

**Tone.** Credit them in the introduction, not only in related work, as round 2 already recommended. Use their vocabulary where it fits: "graduated authority", "circuit breaker", "contract-first", "liability firebreak". This signals continuity and makes the gap (an unspecified trust signal, no validation) evident without polemic.

### (d) Do they name a capability construct overlapping DSA?

**No named, measured construct.** They do state, as desiderata scattered across the paper, most DSA components:

| DSA component | Tomašev et al. passage (verbatim) | Status there |
|---|---|---|
| Recognising decision points and alternatives | Delegator side only: "iteratively generate several proposals …; Alternative proposals should be kept in-context" (§4.1) | About decomposition proposals, not the agent's own decision points |
| **Grounding the choice in the right evidence (tested)** | none | **Absent.** The only process proxy is "clarity and soundness of reasoning" (§4.6) |
| Recognising uncertainty / contradiction boundaries | "dynamic cognitive friction: agents must be capable of recognizing when a request, while technically 'safe,' is contextually ambiguous enough to warrant stepping outside their zone of indifference" (§2.3); "Calibration of trust also involves a self-awareness of one's own capabilities" (§2.3) | Desideratum |
| Staying within authority scope | privilege attenuation, semantic constraints, DCT caveats; "if a delegatee attempts to go beyond the requested scope" the token is invalidated (§4.7, §6.1) | Enforced by infrastructure, not measured as a capability |
| Escalating correctly | "challenge the delegator or request human verification" (§2.3); "soliciting clarification or additional context when necessary, or rejecting the requests where appropriate" (§4.6); "knowing when to interrupt for feedback and when to remain silent" (§5.4) | Desideratum |
| Revising correctly after correction | "assertive enough to challenge a recognized human error (overcoming sycophancy) while remaining open to accepting valid overrides" (§5.4) | Desideratum (social intelligence) |
| Preserving provenance | "the system must maintain immutable provenance … who delegated what to whom" (§5.2) | System-level property, not an agent capability |

Constructs they *do* name, none of which is measured:
- "dynamic cognitive friction" (§2.3);
- "zone of indifference" (§2.3);
- "trust calibration" (§2.3);
- "social intelligence" and "bi-directional clarity" (§5.4);
- "behavioral metrics" / "transparency score" / "safety score" (§4.6);
- "certifiable agentic capabilities" (§1).

**Implications for DSA.**
1. DSA is not pre-empted as a construct, but its *components* are not new as desiderata. Present DSA as **a measured, decision-level profile that operationalises capabilities that delegation frameworks already require** (cite Tomašev et al. for zone of indifference / cognitive friction, override acceptance, scope adherence, provenance).
2. Their "behavioral metrics" (transparency + safety score) is the **nearest named competitor to DSA as a basis for delegation**. Explicitly contrast:
   - their scores are judged from traces and compliance logs;
   - DSA's grounding component is established by intervention, and the other components by scripted probes (contradiction, correction, scope).
3. "certifiable agentic capabilities" (§1) is a phrase, not a construct; it nonetheless supports our "certified per class" framing.
4. A related DeepMind work they cite tests "doing the right thing for the right reasons" behaviourally, by varying a cost: **Mao et al. 2023, arXiv:2305.18269** [verified: arXiv API]. It is a *behavioural, intervention-style test of the basis of an action*, in deep RL agents, for moral motivation.
   - **Abstract only read.** Abstract: "Morally-motivated behavior should persist despite mounting cost; by measuring an agent's sensitivity to this cost, we gain deeper insight into underlying motivations."
   - Relevance: precedent for "test the basis by perturbing an input and measuring sensitivity". It also **collides with title candidate 2** ("Right for the Right Reasons…"; that phrase is also the title of Ross et al. 2017, arXiv:1703.03717 [verified]).
   - Cite it in W2's related work as a sensitivity-based test of motivation (not of evidence use, not for delegation).

### (e) Their classic MAS, trust and automation citations: list, verification, gaps

All entries below are as given in their reference list. Verification status is from my own lookups (Crossref API unless noted).

**Classic MAS delegation, trust and coordination**

| Their citation (as given) | Verified bibliographic data | Status | In WorkTrace notes? |
|---|---|---|---|
| Castelfranchi & Falcone (1998), "Towards a theory of delegation for agent-based systems", RAS 24(3–4):141–157 | doi:10.1016/S0921-8890(98)00028-1 | [verified, r2] | yes (read in full, r2) |
| Falcone & Castelfranchi (**2002** in their list), "The human in the loop of a delegated agent: the theory of adjustable social autonomy", IEEE SMC-A 31(5):406–418 | Crossref: **2001**, 31(5):406–418, doi:10.1109/3468.952715 | [verified]. **Their year is wrong** | yes (abstract only) |
| **Griffiths, N. (2005)**, "Task delegation using experience-based multi-dimensional trust", Proc. 4th AAMAS, pp. 489–496 | Nathan Griffiths, 2005, AAMAS '05, pp. 489–496, doi:10.1145/1082473.1082548 | [verified] | **NO, add.** Abstract read (Semantic Scholar): "a mechanism, called multi-dimensional trust, which allows agents to model the trustworthiness of others according to various criteria … combined with other factors to enable the selection of cooperative partners … experimental validation". **Precedent for multi-dimensional, experience-based trust driving delegation, with an experimental evaluation.** The dimensions are outcome-type (the abstract mentions delay, reduced quality, failure). Cite in W1/W3 as the classic *experience-based, multi-dimensional* basis that we contrast with test-based evidence handling |
| Ramchurn, Huynh & Jennings (2004), "Trust in multi-agent systems", KER 19(1):1–25 | doi:10.1017/S0269888904000116 | [verified, r2] | yes |
| Pinyol & Sabater-Mir (2013), "Computational trust and reputation models for open multi-agent systems: a review", AIR 40(1):1–25 | doi:10.1007/s10462-011-9277-z (Crossref issued 2011 online; vol. 40, 2013) | [verified] | yes (not read) |
| **Yu, H., Shen, Z., Leung, C., Miao, C., Lesser, V. R. (2013)**, "A Survey of Multi-Agent Trust Management Systems", IEEE Access 1:35–50 | doi:10.1109/ACCESS.2013.2259892 | [verified] | **NO, optional add** as a further MAS trust survey (not read) |
| **Cheng, M., Yin, C., Zhang, J., Nazarian, S., Deshmukh, J., Bogdan, P. (2021)**, "A General Trust Framework for Multi-Agent Systems", AAMAS 2021, pp. 332–340 | Crossref returns this record with DOI 10.65109/prjw5260 (an unusual prefix; probably the new IFAAMAS DOI scheme; check before citing) | [verified title/authors/pages; DOI to double-check] | **NO, optional** (not read) |
| **Smith, R. G. (1980)**, "The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver", IEEE Trans. Computers C-29(12):1104–1113 | doi:10.1109/TC.1980.1675516 | [verified] | Mentioned only in r2_learned_permissions. **Add** if we discuss task allocation / bidding (one line) |
| Sandholm (1993) CNP marginal cost, AAAI; Xu & Weigand (2001); Vokřínek et al. (2007) | not checked | [unverified] | No; not needed |
| **Shehory, O. M., Sycara, K., Jha, S.**, "Multi-agent coordination through coalition formation" (their year 1997; ATAL'97) | Crossref: LNCS (Intelligent Agents IV), **1998**, pp. 143–154, doi:10.1007/BFb0026756 | [verified]; year differs (workshop 1997, proceedings 1998) | No; not needed |
| Lau & Zhang (2003); Aknine et al. (2004), coalition formation | not checked | [unverified] | No; not needed |

**Human factors, trust in automation, human–AI delegation**

| Their citation | Verified data | Status | In our notes? |
|---|---|---|---|
| **Lubars, B., Tan, C. (2019)**, "Ask Not What AI Can Do, But What AI Should Do: Towards a Framework of Task Delegability", NeurIPS 32 | arXiv:1902.03245 (NeurIPS venue as given by them; arXiv API journal_ref empty) | [verified: arXiv; venue per their list] | **NO, add.** A per-*task* delegability framework (from the title; content not read). Relevant precedent for class-level delegability attributes |
| Guggenberger, T., Lämmermann, L., Urbach, N., Walter, A. M., Hofmann, P. (2023), "Task delegation from AI to humans: a principal-agent perspective", ICIS 2023 | not found in Crossref; AIS eLibrary/DBLP not reachable (bot wall) | **[unverified]** | No; optional |
| Fuchs, A., Passarella, A., Conti, M. (2024), "Optimizing Delegation in Collaborative Human-AI Hybrid Teams", ACM TAAS 19(4):1–33 | doi:10.1145/3687130 | [verified] | **No, consider.** Learned delegation between human and AI |
| Fuchs, Passarella, Conti, "Optimizing Delegation Between Human and AI Collaborative Agents" (their: ECML-PKDD 2023, pp. 245–260) | Crossref: CCIS (Springer), issued **2025**, pp. 245–260, doi:10.1007/978-3-031-74627-7_18 (workshop proceedings of ECML PKDD 2023) | [verified]; year/venue nuance | No |
| **Lee, M. H., Tok, M. Z. Y. (2025)**, "Towards Uncertainty Aware Task Delegation and Human-AI Collaborative Decision-Making", FAccT '25, pp. 2274–2289 | doi:10.1145/3715275.3732155 | [verified] | **NO, add** to the confidence-based-delegation baselines family (not read) |
| Fügener, A., Grahl, J., Gupta, A., Ketter, W. (2022), "Cognitive Challenges in Human–AI Collaboration: Investigating the Path Toward Productive Delegation", ISR 33(2):678–696 | doi:10.1287/isre.2021.1079 | [verified] | No; optional (AI delegating to humans) |
| Hemmer, P. et al. (2023), "Human-AI Collaboration: The Effect of AI Delegation on Human Task Performance and Task Satisfaction", IUI '23, pp. 453–463 | doi:10.1145/3581641.3584052 | [verified] | No; optional |
| Ma, S. et al. (2023), "Who Should I Trust: AI or Myself? …", CHI '23 | doi:10.1145/3544548.3581058 | [verified] | No; optional (appropriate trust) |
| Kohn, S. C., de Visser, E. J., Wiese, E., Lee, Y.-C., Shaw, T. H. (2021), "Measurement of Trust in Automation: A Narrative Review and Reference Guide", Front. Psychol. 12:604977 | doi:10.3389/fpsyg.2021.604977 | [verified] | No; optional |
| Wischnewski, M., Krämer, N., Müller, E. (2023), "Measuring and Understanding Trust Calibrations for Automated Systems …", CHI '23 | doi:10.1145/3544548.3581197 | [verified] | No; **useful** if we claim "calibration" for the rule |
| Dzindolet, M. T. et al. (2003), "The role of trust in automation reliance", IJHCS 58(6):697–718 | doi:10.1016/S1071-5819(03)00038-7 | [verified] | No; optional |
| Parasuraman, R., Molloy, R., Singh, I. L. (1993), "Performance Consequences of Automation-Induced 'Complacency'", IJAP 3(1):1–23 | doi:10.1207/s15327108ijap0301_1 | [verified] | No; optional (rubber-stamping risk in escalation) |
| Bainbridge, L. (1983), "Ironies of automation", Automatica 19(6):775–779 | doi:10.1016/0005-1098(83)90046-8 | [verified] | No; optional (de-skilling of escalation targets) |

**Responsibility and security**

| Their citation | Verified data | Status |
|---|---|---|
| Dastani, M., Yazdanpanah, V., "Responsibility of AI Systems", AI & Society 38(2):843–852 | doi:10.1007/s00146-022-01481-4 (Crossref issued 2022 online; vol. 38, 2023) | [verified] |
| Santoni de Sio, F., Mecacci, G. (2021), "Four Responsibility Gaps with Artificial Intelligence …", Phil. & Tech. 34(4):1057–1084 | doi:10.1007/s13347-021-00450-x | [verified] |
| Slota, S. C. et al., "Many hands make many fingers to point …", AI & Society 38(4):1287–1299 | doi:10.1007/s00146-021-01302-0 (online 2021) | [verified] |
| Elish, M. C., "Moral Crumple Zones …" | Crossref: SSRN pre-print 2016, doi:10.2139/ssrn.2757236. They cite the 2019 *Engaging Science, Technology, and Society* version | [verified as SSRN 2016; journal version not checked] |
| Franklin, M., Ashton, H., Awad, E., Lagnado, D. (2022), "Causal framework of artificial autonomous agent responsibility", AIES '22, pp. 276–284 | Crossref, OpenAlex and S2 were all rate-limited | **[unverified]** |
| Hardy, N. (1988), "The Confused Deputy", ACM SIGOPS OSR 22(4):36–38 | doi:10.1145/54289.871709 | [verified] |
| Birgisson, A. et al. (2014), "Macaroons …", NDSS 2014 | doi:10.14722/ndss.2014.23212 | [verified] |
| Mao, Y., Reinecke, M. G., Kunesch, M., Duéñez-Guzmán, E. A., Comanescu, R., Haas, J., Leibo, J. Z. (2023), "Doing the right thing for the right reason: Evaluating artificial moral cognition by probing cost insensitivity", arXiv:2305.18269 | arXiv API | [verified]; abstract only |

**What they do NOT cite** (we do; this is a differentiation point for W1):
- Lee & See 2004 (correction to r2: they never cite it);
- Scerri, Pynadath & Tambe 2002 (adjustable autonomy / transfer of control);
- Parasuraman, Sheridan & Wickens 2000 (levels of automation);
- Sabater & Sierra 2005;
- Feng et al. 2025 (levels of autonomy);
- Castelfranchi & Falcone 2000 (degree of trust) and the 2010 book.

Their bridge uses C&F 1998 and SMC-A for *definitions* (delegation; degrees of autonomy) and MAS trust surveys for *trust mechanisms*. It does **not** use C&F's degree-of-trust decomposition (competence × willingness × opportunity) or Scerri's decision-quality vs escalation-cost model.
- **WorkTrace's theory bridge is therefore deeper on two specific points:** (i) which component of trust is estimated (ability, separated from generator-controlled opportunity), and (ii) the Scerri cost model of escalation.
- State this neutrally; it is a legitimate part of W1.

**Must-add from their list:** Griffiths 2005 (AAMAS), Lubars & Tan 2019 (NeurIPS), Lee & Tok 2025 (FAccT), Mao et al. 2023 (arXiv).
**Useful:** Wischnewski et al. 2023 (trust-calibration measurement), Smith 1980 (contract net, one line), Fuchs et al. 2024 (TAAS).
**Before citing:** read Griffiths 2005 in full (a green OA copy is listed by Semantic Scholar via doi:10.82444/warw.33642529; not accessed) and at least the abstract of Lubars & Tan.

### (f) Design implications (delegation chains, task verifiability, contracts)

1. **Verifiability is the key positioning axis, and we should adopt it explicitly.**
   - Their "contract-first decomposition" makes delegation "contingent upon the outcome having precise verification", decomposing until outputs are checkable.
   - WorkTrace targets the **residual decisions whose outcome is not verifiable at decision time** (e.g. counterparty risk calls, whose consequences arrive late or never).
   - Actions:
     - (i) Tag each decision class with their attributes: **verifiability, reversibility, criticality**.
     - (ii) Report H3 results stratified by outcome verifiability. The prediction: the outcome-only rule is competitive where outcomes are verifiable and fails where they are delayed or noisy.
     - (iii) Phrase the contribution as "verifying the basis of a decision when its outcome cannot be verified in time".
   - This turns their framework into our motivation rather than our competitor.
2. **Add a "behavioral-metrics" baseline (trace-judged process trust) to H3.** An LLM judge scores the clarity and soundness of the declared grounds G and protocol compliance per episode; grant per class when the mean score exceeds a threshold at matched coverage.
   - This is their proposal made concrete, and the main non-interventional process baseline.
   - Also report the *disagreement* between trace-judged scores and interventional verdicts (complements H2).
3. **Revocation design: cite them and borrow their stability lesson.**
   - Their circuit breaker (sudden reputation drop or anomaly flag → immediate invalidation) is the concept. Our e-process with hysteresis is a statistically grounded version.
   - They explicitly call for "cooldown periods … damping factors in reputation updates" against oscillation (§4.4). Cite this for our hysteresis.
   - Evaluate the false-revocation rate and the revocation delay after an injected shift.
4. **Represent the grant as policy-as-code / a capability token.** Express a WorkTrace grant as a machine-readable object (class, verdict, α_c, certificate evidence, validity, revocation trigger, rule version), analogous to their `verification_policy` and DCT caveats.
   - Link P (the episode's permissions) to attenuated tokens.
   - This connects the episode schema to their protocol layer, and to PROV (r2 note) for the executed record.
   - Do not claim protocol contributions.
5. **Delegation chains: scope out, but make the episode chain-ready.**
   - Add optional fields to E: `delegated_by`, `on_behalf_of` (PROV `actedOnBehalfOf`), `permission_token_id` / attenuation, `sub_delegations[]`.
   - Note that "whether and to whom to sub-delegate" is itself a decision class ("delegating the act of delegation", §4.2) that WorkTrace could certify.
   - Their transitive monitoring ("A … monitors B's ability to monitor C") suggests a future extension: certifying an agent's *verification* decisions as a decision class.
   - State as future work. In the paper, the principal→agent link is single.
6. **Gaming and evaluation awareness: threats to validity.**
   - Their footnote 1 (models "detect when they are being evaluated"; van der Weij, Greenblatt, Needham, Hubinger) applies to our testing as much as to their reputation.
   - Their low-risk task-selection gaming argument supports our design choice that the *evaluator*, not the agent, chooses the episode mix per class.
   - Cite both.
7. **Escalation cost has a human-factors side we should cite.**
   - Alarm fatigue and default heuristic approval (§5.1, Michels et al. 2025; Parasuraman et al. 1993 complacency) mean that escalation is not only costly but may degrade human accuracy as volume grows.
   - Our sensitivity analysis over c_esc and e_H should include a scenario where e_H rises with escalation volume. A one-parameter extension.
8. **Black-box compatibility is an advantage worth stating.**
   - Their monitoring taxonomy distinguishes black-box from white-box, with privacy constraints.
   - WorkTrace's interventions act on *external* evidence and observe actions. They need no access to internal state or chain-of-thought, only a controllable replay sandbox.
   - So they fit their black-box / privacy-constrained setting, where trace-based behavioural metrics do not.
9. **Their escalation logic is reversibility-driven; ours is competence-driven plus a reversibility hard floor.**
   - Fig. 2 routes irreversible failures to "Immediate Termination or Human Escalation".
   - Keep our hard "always escalate" classes (legal restrictions, irreversible high-criticality), cite their "safety floors … for specific classes of tasks" (§5.3), and let tests decide only within the remaining classes.

---

## 4. Standard per-work fields (preamble format)

**Bibliographic data.** Tomašev, N., Franklin, M., Osindero, S. (2026). *Intelligent AI Delegation.* arXiv:2602.11865v1 [cs.AI], 12 Feb 2026. Google DeepMind. Preprint, not peer-reviewed. [verified: arXiv API]. Read: **full text** (HTML + PDF, figures as images).

**Problem & contribution.** Existing decomposition and delegation in agentic systems "rely on simple heuristics, and are not able to dynamically adapt to environmental changes and robustly handle unexpected failures" (Abstract). They propose a framework (five pillars, nine components), grounded in organisational theory and classic MAS delegation and trust. Its elements:
- trust and reputation that scope authority;
- automatic revocation;
- contract-first verifiable decomposition;
- transitive accountability;
- ethical considerations;
- extensions to MCP, A2A, AP2 and UCP.

**Method.** Conceptual. The mechanisms are listed in §2: graduated authority, behavioural metrics, circuit breakers, liability firebreaks, privilege attenuation, verification credentials, and the protocol sketches (`verification_policy`, monitoring levels L0–L3, RFQ/`bid_object`, Delegation Capability Tokens, `state_snapshot`). There are no formal definitions beyond the prose definitions of delegation and trust.

**Evaluation.** None.

**What it covers that WorkTrace must NOT claim.**
- Connecting C&F delegation theory and MAS trust/reputation to LLM agents.
- Graduated / trust-scoped / revocable autonomy for agents, including automatic revocation on trust-metric drops.
- Process-based ("how, not only what") trust as a concept.
- Context-specific trust thresholds and domain-specific credentials.
- Task verifiability, reversibility and criticality as delegation criteria.
- Escalation governed by reversibility.
- Agents "stepping outside the zone of indifference" to challenge or escalate as a desideratum.
- Accepting valid overrides vs resisting sycophancy.
- Privilege attenuation in chains.
- Immutable provenance of who delegated what to whom.
- Cooldowns and damping against re-allocation oscillation.

**What it leaves open that WorkTrace addresses.**
- What "behavioral metrics" measure and whether they are valid. Their proposal, reasoning-trace clarity, conflicts with their own faithfulness caveat (§4.5).
- How to obtain trust for low-verifiability decisions without labour-intensive oversight.
- Robustness of reputation to task-selection gaming.
- A defined trust metric, threshold and revocation rule with statistical guarantees.
- Any empirical test that process-based trust predicts better than outcome-based reputation.
- Per-*decision*-class competence (vs per-domain credentials).
- An explicit escalation cost in the delegation decision.
- Separation of agent-caused from evidence-caused failure.

**Draft one-sentence differentiation.**
> "Tomašev et al. (2026) propose that AI agents receive graduated, automatically revocable authority on the basis of trust informed by process-level 'behavioral metrics', but leave those metrics to reasoning-trace clarity and protocol compliance and report no evaluation; WorkTrace replaces trace inspection with interventions on decision-time evidence, estimates the resulting unjustified-action rate per decision class, and tests whether a grant-and-revoke rule built on it outperforms outcome-, approval-, history-, confidence- and trace-judged rules on held-out episodes."

**Citation cautions.**
- arXiv preprint, v1 only, not peer-reviewed. Three DeepMind authors; a position/framework paper. Do not present it as an established standard.
- Reference error: Falcone & Castelfranchi SMC-A is 2001, not 2002.
- Minor: they cite Shehory et al. as 1997; the LNCS volume is 1998.
- They do **not** cite Lee & See; do not write "as Tomašev et al., following Lee & See…".
- Quote "graduated authority" and "behavioral metrics" (US spelling) exactly as they appear in §4.6 / Table 3.
- Fig. 2 (adaptive coordination) is the only place where an explicit "Need Escalation?" node appears; cite it as a figure, not a formal rule.

---

## 5. Implications for WorkTrace

**Novelty status after this full reading.**
- W1 (operational, tested bridge): **holds as narrowed.** The paper is conceptual, has no measurement, and does not use C&F's degree-of-trust decomposition or Scerri's cost model.
- W2 (evidence-basis interventions): **untouched.** The only nearby item they cite is Mao et al. 2023: cost-sensitivity probing of RL agents' moral motivation. It is a sensitivity test of the basis of an action, but not of evidence use and not for delegation; add it to W2's related work.
- W3 (per-class delegation rule): **holds.** The mechanism (graduated, revocable) is theirs as a concept. The basis, unit, statistics and validation are ours.
- DSA: **holds as a measured construct**, but its components are listed by them as desiderata. Cite them as the source of the requirements and position DSA as their measurement.

**Design changes (prioritised).**
1. **Add the trace-judged "behavioral metrics" baseline to H3** (LLM judge of the clarity and soundness of declared grounds, plus protocol compliance). High priority: it is the direct empirical answer to this paper.
2. **Tag decision classes with verifiability / reversibility / criticality** and stratify H3 by outcome verifiability. Frame WorkTrace as "verifying the basis when the outcome cannot be verified in time".
3. **Revocation:** cite their circuit breakers and their damping/cooldown recommendation for our hysteresis; report false-revocation rate and detection delay.
4. **Episode schema:** add optional chain fields (`delegated_by`, `on_behalf_of`, `permission_token`, `sub_delegations`). Note sub-delegation and verification as certifiable decision classes (future work).
5. **Grant object as policy-as-code** (versioned, auditable), mirroring their `verification_policy` / DCT idea. No protocol claims.
6. **Escalation cost model:** add an alarm-fatigue scenario (human error rate rising with escalation volume) to the c_esc/e_H sensitivity analysis.
7. **Threats to validity:** evaluation awareness (their footnote 1 sources); internal vs external attribution, not malice detection.

**Wording.**
- Use "graduated authority" and "circuit breaker" with attribution.
- Avoid "certified autonomy" (Shen) and "earned autonomy" (Sovereign-OS), as before.
- Title candidate 2 ("Right for the Right Reasons…") collides with Mao et al. 2023 ("Doing the right thing for the right reason") and with Ross, Hughes & Doshi-Velez, "Right for the Right Reasons: Training Differentiable Models by Constraining their Explanations", arXiv:1703.03717 (IJCAI 2017) [title and authors verified via arXiv API; venue from memory, unverified]. **Prefer "Beyond Track Records"**, which also maps cleanly onto their reputation-as-history definition: "reputation as the public, verifiable history of an agent's reliability".

**Things to cite (new from this note).**
- Tomašev et al. 2026, prominently: introduction + related work + revocation design.
- Griffiths 2005 (AAMAS): experience-based multi-dimensional trust for delegation. **Read it before citing.**
- Lubars & Tan 2019 (NeurIPS): task delegability.
- Lee & Tok 2025 (FAccT): uncertainty-aware delegation, in the confidence-baseline family.
- Mao et al. 2023 (arXiv): sensitivity-based test of an action's basis.
- Wischnewski et al. 2023 (CHI): measuring trust calibration.
- Optional: Smith 1980 (contract net), Fuchs et al. 2024 (TAAS), Yu et al. 2013 (IEEE Access), Parasuraman et al. 1993 (complacency).

**Risks.**
- *Medium.* A reviewer from the DeepMind / agentic-web community may see WorkTrace as "an instance of Tomašev et al.'s behavioural metrics". Mitigation: concede it explicitly (it *is* a concrete behavioural metric) and win on (i) why intervention rather than trace-judging, shown empirically by the new baseline, and (ii) held-out validation.
- *Low–medium.* Follow-up works citing 2602.11865 may operationalise graduated authority.
  - An arXiv abstract search for "intelligent delegation" (25 Oct 2026) found only two other hits: 2604.07813 (a learning theory) and 2603.09619 (context engineering). From titles neither is relevant, but they were not read.
  - **Forward-citation search done** (Semantic Scholar graph API, 25 Oct 2026): **17 citing papers.**
  - Abstracts read (arXiv API) for the six whose titles looked relevant. **None operationalises graduated authority from tested behaviour, and none uses evidence interventions.** Relevant ones:
    - **Hu, Rong & Van Kleek, "Dissociative Identity: Language Model Agents Lack Grounding for Reputation Mechanisms", arXiv:2605.30169** [verified: arXiv API; abstract only].
      - Argues reputation is "structurally inapplicable" to LLM agents. Agents are "an assemblage of mutable modules—foundation models, system prompts, tool-access policies, external memory", so identity-based, ex post, sanction-based governance collapses.
      - Proposes "a shift to observability-based, ex ante, constitutive, protocol-based behavioral harnesses".
      - **Supports WorkTrace's "beyond track records" thesis** (ex ante tests instead of reputation).
      - **Design implication:** bind each grant to a *configuration fingerprint* (model, prompt, tools, memory policy) and require re-certification when any module changes.
      - Cite in W1/W3.
    - **Azevedo, "Minimal Oversight: Uncertainty-Aware Governance for Delegated AI Systems", arXiv:2606.15563** (already on the round-3 supplementary list) [verified: arXiv API; abstract only].
      - The abstract asks "which evidence should calibrate trust", names "masking" ("corrected performance can hide the competence signal needed to calibrate trust"), and recommends "sensitivity-based intervention" and "explicit feasibility checks before autonomy is expanded".
      - It is a variational/information-theoretic framework with synthetic simulations.
      - **Raise its reading priority.** "Sensitivity-based intervention" must be checked: from the abstract it appears to mean *where to intervene as overseer*, not perturbing evidence, but this is unconfirmed.
      - "Masking" is also a good argument for us: when humans correct the agent's outputs, the outcome record hides the agent's own competence, which is one more reason outcome-based rules mis-estimate competence.
    - Chen et al., "Comparing Human Oversight Strategies for Computer-Use Agents", arXiv:2604.04918 [verified: arXiv API; abstract only]. Finding: "users judged whether the agent acted correctly, not whether the action was safe". Relevant to the quality of escalation (e_H) and to H1′-style arguments about what human review catches.
    - Huang, Xiao & Vishnoi, "Delegation and Verification Under AI", arXiv:2603.02961 [abstract only]: a rational-worker model of delegation plus verification effort, with phase transitions. Tangential.
    - Mitra et al., arXiv:2610.07657 (DEFER, MAS security) and Benjamin, Jain & Nandakumar, arXiv:2608.04292 (BIND, biometric delegation tokens) [abstracts only]: not about earned autonomy.
  - The other 11 citing papers were judged irrelevant **by title only**: MarketBench, AIP identity protocol, AESP, Headless Firm, Post-AGI economies, AI-literacy meta-analysis, DARKSIDE, model routing, user simulators, multi-agent exploration, "Autonomous AI Scientist 2030".
  - Semantic Scholar coverage of late-2026 arXiv may be incomplete. Re-run before submission.
- *Low.* Their per-context trust and "classes of tasks" safety floors weaken any claim that per-class delegation is new for LLM agents. We do not make that claim; keep it that way.

**Additional design change, from the forward-citation search.**
8. **Configuration-bound grants:** a certificate applies to a fingerprinted agent configuration (model, system prompt, tool policy, memory policy). Any change triggers re-testing. This follows Hu et al., arXiv:2605.30169: LLM agents are "mutable modules", which undermines reputation.

**Open TODOs from this note.**
- Re-run the forward-citation search for 2602.11865 before submission (done once on 25 Oct 2026: 17 citing papers, none threatening).
- Read Azevedo, arXiv:2606.15563 ("Minimal Oversight") in full, in particular what "sensitivity-based intervention" means.
- Read Griffiths 2005 in full.
- Read the abstract and framework of Lubars & Tan 2019.
- Verify Franklin et al. 2022 (AIES) and Guggenberger et al. 2023 (ICIS) if they are cited.
- Double-check the DOI of Cheng et al. 2021.
