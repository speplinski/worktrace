# Reconstructive Authority (RAM, P5) and its operationalisation (P6): reading note

**Coverage.** I read both papers in full from their arXiv LaTeX sources (`main.tex` and `references.bib`, downloaded via `arxiv.org/e-print/`). That covers every section, appendix, table, theorem, listing and figure caption. I did **not** look at the five PNG plots in P5 (`Figures/*.png`). Their numbers are restated in the text and captions, and those are what I used. For the companion papers in the same series (P0, P1/ACP, P2/IML, P8), I read **only the arXiv abstracts** (marked "abstract only" below).

Quotes below are verbatim from the LaTeX sources, with LaTeX markup turned into plain text (e.g. `$A(t)=\bot$` is written A(t) = ⊥, `\textsc{halt}` is written HALT).

---

## 1. Bibliographic data

### P5: the predecessor that defines RAM
- **Title:** *Reconstructive Authority Model: Runtime Execution Validity Under Partial Observability.* The PDF title block adds the subtitle line "Agent Governance Series — Paper 5".
- **Author:** Marcelo Fernandez, sole author. The PDF title block gives the affiliation as "*Independent Research*". The arXiv author field reads "Marcelo Fernandez - TraslaIA". Zenodo gives "Fernandez, Marcelo Patricio", affiliation TraslaIA.
- **arXiv:** 2604.22898, **v1 only**, submitted Fri 24 Apr 2026 13:19:27 UTC. arXiv comment: "Agent Governance Series, Paper P5. Standalone resubmission following consolidation of P3+P4 into a single paper (P3/4, submit/7510907). Prior submission: submit/7501806. …". No journal-ref.
- **Zenodo DOI:** 10.5281/zenodo.19669430. Zenodo lists it as a *Preprint* with publication date 2026-04-20, version 1. The PDF's date line says "April 2026".
- **Venue:** none. It is a preprint and has not been peer-reviewed.
- **Length:** 15 sections, Appendix A (the full proof of Theorem 1), 5 figures, and synthetic experiments.

### P6: the paper we were asked to read
- **Title:** *Operationalizing Reconstructive Authority: Runtime Construction, Dependency Resolution, and Execution Gating in Autonomous Agent Systems.*
- **Author:** Marcelo Fernandez, sole author. The PDF title block says "TraslaIA, agentcontrolprotocol.xyz". The arXiv author field reads "Marcelo Fernandez - TraslaIA".
- **arXiv:** 2605.23935, **v1 only**. The abs page lists the submission as "[v1] Fri, 24 Apr 2026 13:32:09 UTC (21 KB)", 13 minutes after P5.
  - *Uncertainty:* a 2605.* identifier normally means May 2026. The source tarball is stamped 26 May 2026, so the paper was probably announced late, possibly after being put on hold. Cite it as arXiv:2605.23935 (2026).
  - arXiv comment: "Agent Governance Series, Paper P6. Companion papers on arXiv: P0 (2604.17511), P1 (2603.18829), P2 (2604.17517). P3/4 and P5 submitted concurrently (pending arXiv IDs). Zenodo: 10.5281/zenodo.19699460". No journal-ref.
- **Zenodo DOI:** 10.5281/zenodo.19699460. Zenodo lists it as a *Preprint* with publication date 2026-04-22, version 1.1.
- **Venue:** none. It is a preprint and has not been peer-reviewed.
- **Length:** 13 sections and 6 TikZ figures. It is short: 70 KB of LaTeX, much of which is figure code.

### Series context (from the papers' series tables and arXiv metadata)
"Agent Governance Series", all papers by M. Fernandez:
- **P0** *Atomic Decision Boundaries*, arXiv:2604.17511.
- **P1** *Agent Control Protocol (ACP)*, arXiv:2603.18829 (v10, 95 pp.).
- **P2** *From Admission to Invariants* (IML), arXiv:2604.17517. The arXiv title is "…: Measuring Deviation in Delegated Agent Systems", but P5 and P6 cite it as "…: Epistemological Limits of Local Observability in Agent Governance".
- **P3/4** *Irreducible Governance Structure*, Zenodo 19708496 only.
- **P5** RAM.
- **P6** Operationalizing RAM.
- **Later:** **P8** *Identity-Bound Governance Under Execution Uncertainty: An Accountability Proof Block for LLM Agent Persistent Halts…*, arXiv:2610.00787 (30 Sep 2026). See §6.

All of these are single-author preprints. Nine numbered papers appeared between March and September 2026, and none has a journal-ref.

---

## 2. Problem and motivation

**P5.** Governance by attestation (TEEs, oracle-signed state proofs, "justification-based control") guarantees *integrity* but not *coverage*. The provable state S_p is always a strict subset of the real execution-relevant state S_r. Whatever lies in the gap δ = S_r \ S_p can make an action invalid even though every attestation check passes. P5 states the core claim as: "*an authenticated projection of state is necessary, never sufficient*." It reframes the governance question from "Is execution still consistent with what was approved?" to "Can authority still be constructed from what is true now?" (§1).

**P6.** "Autonomous agent systems fail not only due to incorrect decisions, but due to executing decisions whose authority no longer holds at runtime" (Abstract). Its running example is a financial transfer authorised at t₀ whose recipient is flagged by t₁, which it calls "execution under stale authority". P6 states that RAM defines the validity condition but not how to enforce it, and says plainly: "This paper does not extend the theoretical definition of Reconstructive Authority. Instead, it addresses a distinct problem: how to enforce authority reconstruction as a runtime execution protocol." (§1)

Both papers frame the failure as **"not a failure of decision quality, but of execution validity"** (P6 §1). That framing sets aside how well the agent decides, which is exactly the thing WorkTrace studies.

---

## 3. Definition of Reconstructive Authority

### P5 (the theory)
**Core principle** (§4.1): "Execution authority is not a persistent property granted at admission, but a derivable property that must be continuously reconstructible from the current state." "Execution is valid at time t if and only if authority can be constructed from S_r(t). This removes dependency on historical decisions, stored justifications, and previously attested envelopes."

**Definition: Coverage Envelope** (§4.3). E(t) = (S_p(t), H(t), δ(t)), where:
- S_p(t) ⊆ S_r(t) is the proven state, meaning the components that are observable and cryptographically attestable;
- H(t) is the *declared assumptions*: "explicit propositions about unobserved state that the system accepts as operationally necessary for authority construction";
- δ(t) = S_r(t) \ S_p(t) is the "acknowledged unobservable residual". Its permanent existence is attributed to P2 (IML).

Coverage for an action class α is:
- *adequate* if F can derive A(t) = true from E(t) under α's requirements;
- *partial* if it suffices only for some α′ ⊊ α;
- *insufficient* if no α′ ⊆ α can be authorised.

**Definition: Reconstructive Authority** (§4.4). F : 𝓔 × 𝓐 → 𝓐 ∪ {false, ⊥}, and A(t) = F(E(t), α) for the requested action class α. The outcomes are:
- F = α: execute at full scope;
- F = α′ ⊊ α: execute with narrowed privileges;
- F ∈ {false, ⊥}: halt or defer.

⊥ means "*insufficient information* to determine authority for any sub-class". false means "a definitive refusal".

**Other formal pieces in P5:**
- *Proposition (Non-persistence):* A(t₀) = true does not imply A(t₁) = true for t₁ > t₀, "even when no explicit policy violation is detected".
- *Invariants as constructive conditions:* "F(S_r(t)) is defined only if invariants hold over S_r(t). If invariants fail, F becomes undefined (⊥)."
- *Partial observability:* F(S_r(t)) = ⊥ if required components of S_r(t) are unknown. "The default behavior is halt or defer."
- *Drift redefined:* "Drift at t ≡ F(S_r(t)) ∈ {false, ⊥}". The paper says this "eliminates the need to define, detect, or classify drift explicitly".
- *Execution loop:* observe Ŝ_r(t) ⊆ S_r(t), compute A(t) = F(Ŝ_r(t)), proceed iff true, otherwise halt or re-resolve. "Historical authority grants are not consulted."

**Theorems (P5 §5 and App. A):**
- **Theorem 1 (Attestation insufficiency):** "No attestation-based governance system can guarantee execution validity with respect to the real execution state S_r unless execution authority is reconstructible from S_r(t) at runtime." The proof is a constructive counterexample: pick a component s* ∈ δ with G(S_p) = true and F(S_r) = false.
- **Corollaries:** Enforcement limitation; Oracle limitation (S_p^oracle = S_p ∪ S_p^ext ⊊ S_r); Justification limitation.
- **Theorem 2 (Necessity of RAM):** "Execution validity can only be guaranteed if execution authority is defined as a function over S_r(t): A(t) = F(S_r(t)) and execution is permitted if and only if F(S_r(t)) = true." Only a proof sketch is given.

**Positioning claims in P5 §4.2.** RAM is said to differ from "conservative halt policies", which need "a probability measure over states and a tunable threshold", and from POMDP abstention. In P5's words, F is "a deterministic constructor that returns ⊥ when required state components are missing—not when uncertainty is high."

### P6 (the operational redefinition)
**System model** (§2):
- S_r(t) is the real state and O(t) ⊆ S_r(t) the observable state.
- A(t) = F(S_r(t)).
- U : V → [0, 1] is an uncertainty map over state variables, with threshold θ_auth.

**Definition 1 (Authority Constructibility).** D(a) is the set of variables needed to evaluate authority for action a.
- Constructible(a, O(t)) ≜ Observable(D(a), O(t)) ∧ Closed(D(a)) ∧ Consistent(D(a)).
- *Observability:* U(d) ≤ θ_auth for every d ∈ D(a).
- *Closure:* the dependency graph has no unresolved upstream dependencies.
- *Consistency:* no invariant violations are detected over the evaluated dependencies.

"If this condition holds, authority can be evaluated as either valid or invalid. Otherwise, authority is non-evaluable."

**Definition 2 (Undefined Authority):** ¬Constructible ⇒ A(t) = ⊥, "and execution must not proceed."

**Runtime protocol inputs** (§4.1): O(t), action class C, "Policy prior P₀(C) (candidate generator only)", F, and U.

**Proposition (Prior Non-Authority):** "No execution decision can be derived from P₀(C) alone. Authority requires runtime construction over O(t)." The prior "can only propose initial candidate variables". Runtime may *promote* variables outside the prior, and "Demotion of required variables is not permitted within the same decision cycle under uncertainty."

**Dependency resolution:** D(t) = Resolve(O(t)). "Dependencies are not statically defined. They emerge from the current observable state at runtime." The seven steps are: initialise candidates from P₀; evaluate F on O(t); derive the required set R(t); promote into the authority-defining set A_d(t); check observability and uncertainty for each variable; if any is unresolved, A = ⊥ (halt); if all pass, A = True.

**Non-persistence:** "A(t) ≠ A(t+Δ) unless explicitly recomputed from fresh state." The authors say this is not an engineering limitation but a logical consequence of the model.

### Note: P5 and P6 do not fully agree (worth knowing before citing either)
- **Codomain of F.** In P5, F returns action classes (α, α′ ⊊ α) or {false, ⊥}, and *both* false and ⊥ lead to halt. In P6, F is ternary (True / False / ⊥): False leads to **deny** and ⊥ leads to **halt**. Privilege narrowing survives in P6 only as a decision code.
- **Thresholds.** P5 §4.2 says RAM needs neither a probability measure nor a tunable threshold. P6 builds observability on U(v) ≤ θ_auth, a tunable threshold on an uncertainty score. P6 §10.2 still says RAM rejects risk thresholds: "partial observability that affects authority-defining variables produces A(t) = ⊥ regardless of the magnitude of uncertainty."

---

## 4. Execution gating (P6), IML, ACP, Recovery Loop, safety and liveness

**Definition 3 (Execution State)** (P6 §2):
- EXECUTE if Constructible ∧ A(t) = True;
- DENY if Constructible ∧ A(t) = False;
- HALT if ¬Constructible.

The gate's output is gate(t) ∈ {EXECUTE, DENY, HALT}. The abstract calls the first outcome "admit". The decision table calls it `ADMIT_AUTHORITY_CONSTRUCTIBLE`.

**Deny versus halt** (the paper calls this "the central innovation of this paper"):
- DENY is "falsified authority": A is constructible and evaluates to False.
- HALT is "non-evaluable authority" (A = ⊥).
- "Halt occurs when authority cannot be evaluated due to incomplete dependency resolution, not when it is invalid. Systems that collapse this distinction treat epistemic incompleteness as a denial decision, which is incorrect…"

**Architecture** (§3). There are four components: State Acquisition Layer, Authority Construction Engine, Execution Gate, and Audit Layer. The Audit Layer records O(t), D(t), the decision and failure conditions "without influencing the execution decision".

**Decision codes** (§6, Table 1, seven codes):

| Code | Meaning |
|---|---|
| `ADMIT_AUTHORITY_CONSTRUCTIBLE` | execute |
| `HALT_AUTHORITY_UNDEFINED_REQUIRED_DEPENDENCY` | a required dependency is not observable |
| `HALT_AUTHORITY_UNDEFINED_UNCERTAINTY` | U(v) > θ_auth |
| `HALT_MISSING_REQUIRED_SIGNAL` | "request signal acquisition" |
| `HALT_REATTESTATION_REQUIRED` | "Authority previously valid; state change mandates reconstruction" |
| `CONTINUE_BOUNDED_NON_AUTHORITY_DRIFT` | drift only in variables that do not define authority: "Execute; log drift event" |
| `NARROW_PRIVILEGE_REEVALUATE` | "Authority partially constructible": "Reduce action scope; re-evaluate" |

The table caption says "Every execution attempt resolves to exactly one code". Oddly, the table has no `DENY` code, even though the worked example (§4.6) emits one.

**Proposition (Execution Safety Invariant):** "If A(t) ≠ True, no action in execution class C proceeds. This is enforced structurally by the execution gate, not by policy configuration."

**Roles of the three layers.**
- **RAM** "defines authority and dependency resolution".
- **IML** (P2) "detects drift and invariant violations". IML signals trigger RAM recomputation, which is "mandatory before every state-mutating action". It is event-driven, with no polling.
- **ACP** (P1) "enforces execution gating and transitions". RAM is "the authorization criterion at the execution gate (stage 3 of the 6-stage ACP flow)" and "replaces the admission-time authorization criterion at stage 3 with a runtime constructibility check."

In one sentence: "RAM defines what must be true; IML checks whether it remains true; ACP decides whether execution proceeds."

**Runtime enforcement loop** (§4.7, pseudocode):
1. Observe.
2. Resolve D.
3. If not observable, closed or consistent, set HALT, call `wait_for_update()`, and loop.
4. If `is_valid`, set EXECUTE; otherwise DENY.
5. On DENY, reject and return.
6. On EXECUTE, revalidate before execution with IML (drift or invariant violation leads to HALT and a new loop iteration).
7. Execute, then monitor after execution and call `trigger_recovery` if drift is detected.

**Recovery Loop** (§9):
- *HALT semantics:* A(t) = F(S_r(t)) = ⊥, caused by missing signals, uncertainty above the bound, or drift. "HALT is not a terminal failure, but a controlled suspension of execution."
- *Stages:*
  1. Signal Extraction: the minimal unresolved set U(t).
  2. IML Trigger.
  3. State Augmentation: S_r(t′) = S_r(t) ∪ ΔO, "or reduce action scope". If that fails, "revert to the last atomically consistent state" per P0.
  4. Reconstruction Attempt: A(t′) = F(S_r(t′)).
  5. Resolution: if A(t′) ≠ ⊥, resume; "If A(t′) = ⊥ ⇒ remain in HALT or escalate".

**Theorems in P6, stated exactly:**
- **Theorem 1 (Stale Authority Under Drift):** "Any system that does not recompute authority at execution time will eventually execute under invalid authority when S_r(t) changes continuously." The proof *assumes* that the variables D(t₀) become invalid at some t₁.
- **Theorem 2 (Conditional Liveness under Recoverable Observability):** "If all authority-defining variables required by F are eventually observable or resolvable, then a system implementing the Recovery Loop will eventually exit HALT and resume execution."
  - *Assumptions:* (1) Eventual Observability, (2) Finite Resolution, (3) Stable Evaluation Window.
  - *Formally:* "if ∃ t′ > t such that Constructible(a, O(t′)) holds, then ∃ t″ ≥ t′ such that ExecState(a, O(t″)) ∈ {EXECUTE, DENY}."
- **Theorem 3 (Authority Validity):** "Any system that permits execution under incomplete authority-defining state cannot guarantee that no action proceeds without constructible authority."
- **Theorem 4 (Execution Safety under Constructible Authority):** ∀ a, O(t): Execute(a, O(t)) ⇒ (Constructible(a, O(t)) ∧ A(t) = True). Only a proof sketch is given, by enumerating the paths through the loop.

**Assessment of the proofs (mine).** All the results are short arguments by construction or definition. There is no mechanised proof, no model checking in P5 or P6, and no complexity analysis.
- The safety theorem is true by definition of the gate.
- The informal statement of liveness ("resume execution") is stronger than its formal statement (EXECUTE *or* DENY). The proof then asserts F(S_r(t″)) = True, which does not follow from the assumptions.
- The formal liveness statement is close to trivial given Definition 3, apart from the stable-window assumption.
- In Figure 6 (the state machine), the DENY node is labelled "A(t) = ⊥", which contradicts the text. The same figure sends "Invariant Violation" from EXECUTE to DENY, whereas Definition 1 makes an invariant violation a constructibility failure, which should lead to HALT.

---

## 5. Where does authority come from: tested behaviour or policies and current state? (critical for us)

**Unambiguous answer: from the current (observable) state of the world, evaluated by a designer-specified construction function F with designer-specified dependencies and invariants. It is never derived from the agent's past behaviour, track record, tested competence or reasoning quality.** History is explicitly excluded. The evidence:

- P5 §4.1: "This removes dependency on historical decisions, stored justifications, and previously attested envelopes."
- P5 §4.9: "No execution step occurs without a fresh authority computation. Historical authority grants are not consulted."
- P5 §6 Table 1 ("RAM vs Attestation-Based Models"), row "Role of history": **"None (history irrelevant)"**.
- P5 §10 (design implication 1): "Authority must be stateless at runtime. Systems must not depend on prior decisions, sealed contexts, or persistent authority tokens."
- P6 §4.2: the policy prior P₀(C) "cannot authorize execution independently … can only propose initial candidate variables for F".
- In both papers, the variables F checks describe **the world or the transaction**: account status, transaction limit, risk indicator (P6 §4.6); identity consistency, behaviour stability, regulatory compliance, context integrity (P5 §9.5).
  - "behavior_stability" refers to the *user's/transaction's* behavioural pattern ("anomalous behavior is detected in a parallel session"), not the agent's.
- P6 §11.6: "It does not guarantee correctness of the authority model itself, completeness of dependency specification, or optimality of decisions." P6 §11.4 adds that F, D(a) and the invariants are a specification burden placed on designers.

**What "authority" means here.** It is closest to *runtime authorisation / precondition validity* (attribute-based access control made non-persistent and three-valued), not to *delegated autonomy* in the Castelfranchi & Falcone or Scerri et al. sense. There is no principal (a party who delegates), no model of the delegate's trustworthiness, and no learning from outcomes.

**One link to our "behaviour towards evidence".** P5 §3.2 ("The Self-Justification Boundary") names the problem of an agent that writes its own justifications: "Execution authority depends on the system's ability to correctly describe the conditions under which it is allowed to act." It calls this a failure "of *epistemic completeness*". P5's remedy is to take the agent's justification out of the authority decision and rely on external state. The agent's handling of evidence is **never tested**. WorkTrace takes the opposite route: it tests that handling directly through evidence interventions.

**Nuance at the level of the series (outside the assigned papers; abstracts only).** ACP (P1, arXiv:2603.18829) is described as "deterministic, history-aware risk scoring" with "anomaly accumulation, cooldown", and it is "escalating after 3 actions and denying after 11" in a 500-request test. That history is a count of *risk and anomaly signals* per (agent, capability, resource), not evidence of competence. Even so, a reviewer could point to it. We should say that the series' history-awareness is risk accumulation over request traces, not testing of decision behaviour. I have not verified ACP's internals.

---

## 6. Escalation to humans, delegation by humans, scope of autonomy, revocation

**Humans.** Neither P5 nor P6 contains a human principal, operator, overseer, or human-in-the-loop. A full-text search for "human", "operator", "delegat*", "trust" (apart from TEE "trusted"), "competence" and "reputation" finds nothing relevant.

**Escalation.** The word appears exactly once in P6, in Recovery Loop step 5: "If A(t′) = ⊥ ⇒ remain in HALT or escalate". The target, protocol and cost of escalation are not specified.

P5 rules out overriding a halt: "The correct response is to improve observability or relax authority requirements, not to override the halt. Overriding the halt restores the attestation failure mode." (P5 §11.2). In the same place it frames a persistent halt as "a feature, not a bug: it surfaces *observability debt* explicitly." P5 §9.8 adds: "A persistently high OCR is a signal to invest in observability engineering, not to override the halt."

**Elsewhere in the series (abstracts only).**
- **P0** (arXiv:2604.17511) "formalize[s] the Escalate outcome … proving that it transfers rather than eliminates the atomicity requirement".
- **P8** (arXiv:2610.00787, Sep 2026) covers *human* re-authorisation after persistent halts. It introduces the "Accountability Proof Block (APB): a system-constructed evidence block, a human-supplied decision block, and an ed25519 signature binding both to a registered principal", plus a "k-of-n multi-principal" variant. It also calibrates a drift threshold T* across six open LLMs and finds it "stable within model … but varying across models … T* must therefore be measured per deployment". This is the series' closest point to "escalation to humans", and P8 has empirical work on LLMs.
- **Recommendation:** if our related work mentions the series' escalation story, read P8 in full first.

**Delegation by humans.** None in P5 or P6. "Delegated" appears only in the arXiv title of P2 ("Measuring Deviation in Delegated Agent Systems"), and P2 defines an admissible behaviour space A₀ "established at admission time" (abstract).

**Scope of autonomy.** This is handled through **action classes**:
- P5: α ∈ 𝓐, with "Dynamic narrowing (α → α′)", where "Coverage is partial for α if it suffices for a strict subset α′ ⊊ α".
- P6: action class C is an input; the code `NARROW_PRIVILEGE_REEVALUATE` means "Reduce action scope; re-evaluate".
- P6 §8.4 (P3/4 allocation): "allocation controls who arrives at the gate; RAM controls what executes once they arrive."
- Narrowing is computed **per execution instance from the current coverage**. It is not a standing status of the class.

**Revocation.** There is no explicit revocation operation. Revocation is *implicit and continuous*: authority is non-persistent and recomputed at every action ("authority expires with the state that produced it", P6 §13). Nothing is ever *granted* to the agent that could later be revoked.

---

## 7. Evaluation

**P6: none.** P6 is purely a specification with formal arguments. It contains one hand-worked example (three scenarios over variables x₁–x₃ with θ_auth = 0.2), pseudocode, and diagrams. It has no implementation, no data, no metrics and no experiments. The conclusion lists "empirical evaluation in real-world deployments" as future work.

**P5: a synthetic simulation only** (§9).
- *State model:* the "real state" is S_r = {I, B, R, C, E} (identity, behaviour, regulatory, context, emergent).
- *Drift injection:* observable 30%, delayed 25%, hidden 25%, ambiguous 20%.
- *Baselines:* Attestation (S_p ⊊ S_r) and Oracle-extended attestation.
- *Seed and sample size:* seed 42. §9.2 says N = 10,000 steps per model, but §9.6 says N = 100,000 per coverage level; the two are inconsistent.
- *Data and code:* no external data. No code link in P5 (later series papers do link GitHub).
- *Metrics:*
  - IER = |exec with A_r = false| / |executions| (invalid execution rate);
  - SHR = |halts with A_r = false| / |A_r = false| (safe-halt rate);
  - OCR = |halts with A_r = true| / |A_r = true| (over-conservatism rate).
- *Results at coverage 0.1:* Attestation IER 0.423 / SHR 0.145 / OCR 0.053; Oracle 0.393 / 0.293 / 0.111; **RAM 0.000 / 1.000 / 0.000**.
- *At full coverage:* Attestation and Oracle both have IER = 0.233 (attributed to "undefined state … treated as benign"). RAM has IER = 0 "at every coverage level".

**Assessment of the P5 evaluation (mine).** RAM's perfect scores hold by construction. The simulated ground truth A_r is computed by the same function that RAM uses as F. The authors concede the OCR part: "OCR = 0.000 because the authority function F is precisely scoped to the components that determine real authority."

The abstract and conclusion claim that attestation IER is "proportional to (1 − |S_p|/|S_r|)", but their own numbers do not show proportionality: IER is 0.233 at full coverage, where the claim would predict zero. At best the relation is affine plus an ε_semantic term, which they then add.

There are no LLM agents, no real workloads, no variance or confidence intervals, and no **risk–coverage curve**. An "OCR–IER Pareto frontier" is listed only as future work (P5 §11.3(ii)). P5 §11.2 concedes: "Empirical validation on production agent workloads remains an open task."

---

## 8. Connection to LLM-agent reasoning faithfulness, evidence, and provenance graphs

**No real connection in either paper.**
- **LLMs.** Mentioned only once, in P5's future work: "evaluation on real agent workloads including … LLM agent tool execution logs". There is no treatment of chain-of-thought faithfulness, sycophancy, or how an agent uses evidence.
- **"Evidence."** The word does not occur in P5 or P6. The closest notion is "observability" of state variables. In P8 (abstract only), "evidence block" means a system-generated record attached to a halt event.
- **Provenance.** Only an "audit artifact" or "audit layer". P6 §7 records the prior candidates, the required set R(t) "with discovery path", promotions into A_d(t) "with reason", U(v) for each variable, and the final code. P6 requires that sampled logs be "sufficient to reconstruct the authority lineage for any queried point in time". The audit layer has "no causal role in authority decision" (P5 Fig. 1 caption; also P6 §3.4).
  - This is a lineage of *decision inputs*, not a provenance graph of the agent's reasoning. It is never used to judge the agent.
- **Dependency graph.** P6's "dependency graph induced by D(a)" (the Closure condition) is a graph of state variables needed to evaluate authority. It is not an evidence or provenance graph of a decision episode, and it is never formalised beyond the word "closed".
- **Only conceptual bridge:** P5's "Self-Justification Boundary" (§3.2), discussed in §5 above.

---

## 9. Limitations

### Acknowledged by the authors
**P6 §11:**
1. Dependency on observability: the system may "remain in the HALT state indefinitely", and liveness "does not hold if dependencies are permanently unresolvable".
2. Latency overhead.
3. Recovery complexity.
4. Specification burden: "Incomplete or incorrect specifications will produce incorrect constructibility evaluations".
5. Non-deterministic environments: oscillation between HALT and EXECUTE; the Stable Evaluation Window "may not hold in adversarial settings".
6. Scope of guarantees: there is no guarantee of "correctness of the authority model itself, completeness of dependency specification, or optimality of decisions".

**P6 §12 costs:** halts more often than threshold-based systems, higher latency, liveness conditional on observability. The paper calls this "choosing correctness over availability", with the claim that "halting is always preferable to acting without constructible authority."

**P5 §11.2:** computational overhead; persistent halting (framed as surfacing "observability debt"); multi-agent scalability ("RAM does not solve distributed state aggregation"); a synthetic experimental basis.

**P5 future work:** RAM + ACP integration, an OCR–IER Pareto frontier, empirical validation, adversarial state injection, learned state inference, and multi-agent RAM.

### Limitations I see
1. **The paradigm is "authority = correct, complete specification of F".** All of the epistemic difficulty moves into F, D(a), the invariants and θ_auth, and these are assumed to be given. Nothing tells us how to obtain or validate F for open-ended LLM decisions, where "authority-defining variables" are not enumerable state fields.
2. **No notion of the agent as a decision-maker.** The paper says outright that failure is "not a failure of decision quality". RAM therefore cannot tell a competent agent from an incompetent one if both face the same observable state.
3. **Guarantees are definitional.** Safety follows from the gate's definition. Liveness is conditional on eventual observability and, as stated formally, is nearly vacuous. Some proofs assume their conclusions (Stale Authority) or contain non-sequiturs (the liveness proof asserts F = True).
4. **Internal inconsistencies:**
   - P5 versus P6 on thresholds and on false-leads-to-halt versus false-leads-to-deny;
   - Figure 6 labels;
   - the decision-code table lacks a DENY code;
   - N = 10k versus 100k;
   - the "proportional" claim;
   - P2's title cited differently from its arXiv title.
5. **Citation accuracy problems:**
   - CertiKOS (Gu et al., OSDI 2016, a certified OS kernel) is cited as an example of "justification-based control" with TEEs;
   - "ATLAS~\cite{zhang2020deco}" cites the DECO paper for a system called ATLAS;
   - the author list in the Astraea bib entry (Adler et al. 2018) looks wrong to me. My recollection is that it includes N. Veira and A. Kastania, not "Neil Brown, Andreas Worley". *Unverified; check before citing.*
6. **Little engagement with the literature.** There is no engagement with delegation, adjustable autonomy, trust, selective prediction or abstention (beyond one POMDP citation), or LLM-agent safety beyond AI Control (Greenblatt et al.) and AI Safety Gridworlds (Leike et al.).
7. **Evaluation is circular:** the oracle is F itself (§7 above).
8. **Escalation is unspecified:** there is no model of a human and no escalation cost. Halting has no cost in their objective except "OCR", which in their simulation is zero by construction.
9. **Publication pattern:** single-author self-citation network, and rapid preprint output (many papers in about six months). P5 and P6 were submitted 13 minutes apart.

---

## 10. Related work they cite

Only references actually cited in the text are listed below. Both `.bib` files contain additional *uncited* entries (e.g. Abadi, Burrows, Lampson & Plotkin 1993, "A Calculus for Access Control in Distributed Systems"; Goguen & Meseguer 1982; Wooldridge 2009; Hadfield-Menell et al. 2016; LangGraph). These do not appear in the compiled reference lists, so **they must not be described as cited.**

### Delegation, adjustable autonomy, trust (the classic MAS literature)
**None cited in either paper.** There is no Castelfranchi & Falcone, no Scerri, Pynadath & Tambe, no Jennings or Wooldridge (the Wooldridge entry is in the .bib but uncited), no Parasuraman/Sheridan levels of automation, and no trust or reputation models. **This gap is the space our contribution (1) occupies.**

### Authority and access control (P6 §10.4 only)
- OASIS (2013). *eXtensible Access Control Markup Language (XACML) Version 3.0.* OASIS Standard. https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html
- Open Policy Agent Project (2016). *Open Policy Agent (OPA).* https://www.openpolicyagent.org (CNCF Graduated Project).
- Mentioned without citation: "Policy-as-Code frameworks (Rego, Sentinel, Kyverno)". P0's abstract (not read in full) classifies RBAC, ABAC, OPA, Cedar and AWS IAM as "split systems".

### Attestation, trusted execution, oracles
- Costan, V., & Devadas, S. (2016). *Intel SGX Explained.* IACR Cryptology ePrint Archive 2016/086. [P5, P6]
- Sabt, M., Achemlal, M., & Bouabdallah, A. (2015). *Trusted Execution Environment: What It Is, and What It Is Not.* IEEE Trustcom/BigDataSE/ISPA, 57–64. [P6]
- Gu, R., Shao, Z., Chen, H., Wu, X., Kim, J., Sjöberg, V., & Costanzo, D. (2016). *CertiKOS: An Extensible Architecture for Building Certified Concurrent OS Kernels.* OSDI, 653–669. [P5; cited for "justification-based control", which looks like a mis-citation]
- Zhang, F., Maram, S. K. D., Malvai, H., Goldfeder, S., & Juels, A. (2020). *DECO: Liberating Web Data Using Decentralized Oracles for TLS.* ACM CCS, 1919–1938. [P5; cited as "ATLAS"]
- Adler, J., et al. (2018). *Astraea: A Decentralized Blockchain Oracle.* IEEE iThings/Blockchain 2018. [P5; the bib author list may be wrong]

### Runtime verification (P5 §2.1)
- Leucker, M., & Schallhart, C. (2009). *A Brief Account of Runtime Verification.* J. Logic and Algebraic Programming 78(5), 293–303.
- Falcone, Y., Mounier, L., Fernandez, J.-C., & Richier, J.-L. (2012). *Runtime Verification of Component-Based Systems.* Proc. 4th Int. Symp. on Leveraging Applications (as given in the bib; not verified).
- Havelund, K., & Roşu, G. (2002). *Synthesizing Monitors for Safety Properties.* TACAS, 342–356.

### Partial observability (P5)
- Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). *Planning and Acting in Partially Observable Stochastic Domains.* Artificial Intelligence 101(1–2), 99–134.

### Distributed systems (P6)
- Lamport, L. (1978). *Time, Clocks, and the Ordering of Events in a Distributed System.* CACM 21(7), 558–565.

### AI safety (P6 §10.2 and §10.5)
- Greenblatt, R., et al. (2024). *AI Control: Improving Safety Despite Intentional Subversion.* arXiv:2312.06942. This is the only modern LLM-safety work cited; P6 casts RAM as "complementary and orthogonal" to it.
- Leike, J., Martic, M., Krakovna, V., Ortega, P. A., Everitt, T., Lefrancq, A., Orseau, L., & Legg, S. (2017/2018). *AI Safety Gridworlds.* arXiv:1711.09883. P6 lumps it with "risk-threshold systems" (a questionable characterisation).

### Self-citations (series)
P0 *Atomic Decision Boundaries* (arXiv:2604.17511); P1 *ACP* (arXiv:2603.18829); P2 *IML* (arXiv:2604.17517); P3/4 *Irreducible Governance Structure* (Zenodo 19708496); P5 RAM (arXiv:2604.22898); P6 (arXiv:2605.23935).

---

## 11. Verbatim quotes for our related work

1. P6, Abstract: "Prior work defined Reconstructive Authority (RAM) as a condition for valid execution: actions are permitted only if authority can be constructed from current state."
2. P6, §1 Introduction: "This is not a failure of decision quality, but of execution validity."
3. P6, §2 System Model: "HALT corresponds to *non-evaluable authority*: authority cannot be determined because one or more constructibility conditions fail (A(t) = ⊥)."
4. P5, §4.1 Core Principle: "Execution authority is not a persistent property granted at admission, but a derivable property that must be continuously reconstructible from the current state."
5. P5, §6 Table 1 ("RAM vs Attestation-Based Models"), row *Role of history*: "None (history irrelevant)". The companion line in P5 §4.9 reads: "Historical authority grants are not consulted."
6. P5, §3.2 The Self-Justification Boundary: "Execution authority depends on the system's ability to correctly describe the conditions under which it is allowed to act."

A possible extra quote: P6 §11.6, "It does not guarantee correctness of the authority model itself, completeness of dependency specification, or optimality of decisions."

---

## 12. Positioning for WorkTrace

### What they cover (we must not claim novelty for)
- **Non-persistent, per-action authority computed at runtime from current observable state**, so that authority granted at admission goes stale.
- **A three-valued execution gate**: EXECUTE / DENY / HALT, with HALT meaning "non-evaluable" as distinct from "denied". We must not present "proceed / escalate / refuse" as the first three-way gate for agent actions without crediting this.
  - Note, though, that their HALT means *suspend and gather state*, not *hand over to a human*, and their DENY means *the preconditions are false*, not *this class is not delegated to the agent*.
- **Privilege narrowing per action class** (α → α′ ⊊ α).
- **Fail-closed treatment of missing or uncertain information**, plus a recovery loop that acquires missing signals.
- **Safety-versus-availability metrics**: IER, SHR and OCR, which play the role of risk and over-conservatism. They explicitly propose an "OCR–IER Pareto frontier" as future work. We should cite this as the nearest analogue of our risk–coverage framing.
- **Structured audit artifacts** recording why each variable defined authority.

### What they leave open (our space)
- **Authority from the agent's tested behaviour.** They exclude history by design ("Role of history: None"). Earning autonomy from tested decision episodes is the opposite stance and is not addressed anywhere.
- **Decision quality and behaviour towards evidence.** They set aside "decision quality" and solve self-justification by removing the agent's account from the loop. They never test whether the agent's decisions respond correctly to evidence, which our evidence interventions do.
- **A delegation relationship.** There is no principal, no delegation theory (no Castelfranchi & Falcone, no Scerri et al.), no adjustable autonomy, no human escalation target, and no escalation cost. "Escalate" appears once, unspecified.
- **Class-level, standing (but revocable) status** learned or estimated from episodes and then **evaluated on held-out episodes**. Their status is recomputed for each instance from a hand-specified F, and their "evaluation" is tautological.
- **LLM agents.** None: no reasoning traces, no evidence or provenance graphs, no faithfulness.
- **An empirical risk–coverage curve with escalation cost** against an outcome-only baseline. Absent; the closest they offer is the future-work Pareto frontier.

### Complementarity (useful framing for the paper)
RAM and WorkTrace answer different questions and compose:
- WorkTrace asks: *may this agent decide class C on its own at all?*
- RAM asks: *are the preconditions of this specific action constructible from the current state?*

A WorkTrace "proceed" status could sit upstream of a RAM-style gate, close to their own "allocation controls who arrives at the gate" layer.

### One-sentence differentiation
> Reconstructive Authority makes each *action's* authority a non-persistent function of the *current world state* under a designer-specified constructor, explicitly ignoring history. WorkTrace instead makes an *agent's* autonomy over a *decision class* a conditional, revocable status *earned from tested behaviour towards evidence* in decision episodes, and evaluates that status on held-out episodes by risk–coverage with escalation cost.

### How much weight to give it
P5, P6 and the rest of the series are **single-author, non-peer-reviewed preprints** (arXiv plus Zenodo, no journal-ref or venue), produced at a high rate. The guarantees are definitional and the only evaluation (P5) is synthetic and circular. My recommendation:
- Cite them as **concurrent preprint work** on runtime authorisation for agents.
- Credit the ternary gate and the non-persistence idea.
- Do not treat their theorems or numbers as established results.
- If we discuss human escalation, read P8 (arXiv:2610.00787, human-signed Accountability Proof Block after persistent halts, with LLM drift-threshold calibration) in full, since it is the series' nearest point to our escalation story.
