# Fernandez "Agent Governance Series" (round 2): P8 (APB, human re-authorisation), P1 (ACP), and the full series list

**Scope.** This note follows `notes/reconstructive_authority.md`, which covered P5 and P6 (RAM) in full. I do not repeat RAM material here.

## What I read

| Paper | Coverage |
|---|---|
| **P8** (arXiv:2610.00787) | Read **in full** from the arXiv LaTeX source (`main.tex`, all five auto-generated table files, `references.bib`). That covers every section, theorem, proof, table and experiment. P8 has no figures. |
| **P1, ACP** (arXiv:2603.18829v10) | Read **in full** from the arXiv LaTeX source (`main.tex`, 5,549 lines). That covers all sections, all 14 experiments, the security model, the appendices including the TLA+ listing, and the TikZ/pgfplots figure code. I skimmed the LaTeX preamble (lines 1–89). I did **not** read `references.bib` line by line. |
| **P7** (Zenodo 10.5281/zenodo.19929771) | Read **essentially in full** (21-page PDF, via `pdftotext`; plots read as extracted text only). P8's calibration quantity T\* is defined only in P7, so I needed it to answer question (a). |
| **P9 and P10** (Zenodo v2.0, 22 Oct 2026) | **Partial only.** I read the abstracts and Zenodo revision notes for both. For P9 I also read the introduction and the closing "evaluation / future work" paragraphs. For P10 I read the introduction, problem statement, §2 background, §2.3 "liveness gap" and §3.4 fallback modes. I keyword-searched both texts for trust, autonomy, competence, reputation, coverage and false positives (no relevant hits beyond what is reported here). |
| **ACP specification repo** (`github.com/chelof100/acp-framework-en`) | **Not read.** GitHub API and HTML access were blocked in this session, and the brief forbids git commands, so I did not clone it. As a result, the internals of ACP-REP-1.2 (reputation) and ACP-AGENT-1.0 (autonomy-level transitions) are **unverified**; see the risk flagged in §4. I did read the project website pages `agentcontrolprotocol.xyz/{index,research,specification,governance}.html`. |

**Quoting conventions.** Quotes are verbatim, with LaTeX turned into plain text. Section numbers are counted from the LaTeX `\section` order. For P8: §1 Intro, §2 Related Work, §3 Framework, §4 Theorems, §5 Implementation, §6–§11 Experiments A–F, §12 Discussion, §13 Conclusion. For ACP: §1 Problem … §13 Evaluation (Experiments 1–8), §14 Compliance Testing, §17 Limits of Execution-Only Governance (Experiments 9–14), §19 Security Model.

---

## 0. Answers in brief (for whoever writes related work)

- **(a) P8.**
  - *Trigger:* a *persistent* HALT, meaning the drift score D̂(t) stays ≥ θ for a whole persistence window ΔT, or the P6 Recovery Loop exits with HALT or DENY.
  - *Who re-authorises:* a registered human principal, or k-of-n principals, who signs a RESUME / DENY / RECALIBRATE decision over a system-built evidence block (an "Accountability Proof Block", APB).
  - *What is calibrated:* a per-model "drift threshold" T\*. It is the first step at which the IML drift composite (a distribution-shift score on tool usage relative to an admission-time baseline) reaches θ = 0.20 under a scripted escalating-urgency prompt. This was measured on 6 small open LLMs (Ollama, 3 runs each, 500 steps, temperature 0.4). T\* is then used to bound ΔT, the time an agent may stay above θ before a human is required.
  - *What is missing:* there is no outcome ground truth and **no risk–coverage or over-caution-vs-safety curve.** In every experiment the "human" is a scripted threshold policy.
- **(b) ACP.**
  - *How history is used:* history is **only** risk and anomaly counters. These are request frequency per (agent, capability, resource) "PatternKey", 24-hour denial counts, and a cooldown triggered by denials. History can only *add* risk: "approval decisions do not reset or reduce it", and the conformance vector SEQ-PRIVJUMP-001 asserts "No residual benefit from prior APPROVED".
  - *What is never tested:* the agent's competence or its handling of evidence. ACP states "The LLM's internal reasoning is irrelevant to ACP's admission decision".
  - *Revocability:* `autonomy_level` (0–4) is a static, per-agent configuration value. Capabilities are per class and can be revoked administratively. Anomaly penalties are per class since RISK-3.0, but the 24-hour denial rule and the cooldown remain agent-wide.
- **(c) Novelty threat.** The threat is **moderate on surface vocabulary** but **low on substance.**
  - The overlapping vocabulary: "autonomy level", "history-aware", "per-capability scoping", "ESCALATED", "human re-authorisation", "measured per deployment", "counterfactual evaluation".
  - The difference in substance: neither paper ever grants or widens autonomy from evidence about the agent's decision behaviour, and neither evaluates a delegation rule against outcomes.
  - The two sides of the argument are in §4.

---

## 1. P8: Identity-Bound Governance / Accountability Proof Block

### 1.1 Bibliographic data [verified: arXiv API + abs page + Zenodo API]
- **Title (arXiv):** *Identity-Bound Governance Under Execution Uncertainty: An Accountability Proof Block for LLM Agent Persistent Halts, with Cryptographic Implementation and Cross-Model Calibration*. The PDF subtitle line reads "Agent Governance Series — Paper 8".
- **Author:** Marcelo Fernandez, sole author. The PDF gives the affiliation as TraslaIA, info@traslaia.com. Zenodo gives "Fernandez, Marcelo Patricio", TraslaIA, ORCID 0009-0008-7884-2087.
- **arXiv:** 2610.00787, **v1 only**, submitted Wed 30 Sep 2026 22:22:33 UTC. Primary category cs.CR.
  - arXiv comment: "24 pages, 7 tables, 2 propositions. Paper 8 of the Agent Governance Series. v2: RFC 8785 canonicalization, event_id uniqueness (V5), k-of-n multi-principal threshold governance (Prop 8.5), infrastructure fault injection experiment. Code: https://github.com/chelof100/identity-bound-governance".
  - The "v2" in that comment refers to the author's internal versioning. arXiv shows only v1, and the v1 source already contains V5, k-of-n and Experiment F.
- **Zenodo:** 10.5281/zenodo.20157139, *Preprint*, dated 2026-05-13, v1. The Zenodo copy predates arXiv by about 4.5 months. Its description has no V5 but does mention k-of-n and fault injection.
- **Venue:** none. No journal-ref, not peer-reviewed. The PDF date line says "September 2026".

### 1.2 Problem and contribution
- **Problem** (Abstract): "A correctly governed LLM agent can reach a state in which neither continuing execution nor automatically halting is admissible: the system has detected a persistent failure of its observability or drift-detection layer, but cannot itself decide who has the authority to resume, deny, or recalibrate the deployment." The paper calls this an "identity-bound governance event".
- **Contribution:**
  - a formal Principal Set 𝒫, an Authority Resolution Function G, and the APB = (E_s, D_h, σ_h);
  - four theorems (T8.1–T8.4) and a Byzantine-resistance proposition (Prop 8.5);
  - a Python ed25519 implementation (1,215 lines of code, 103 unit tests);
  - six experiments (A–F);
  - a calibration recipe (Prop 5.1) linking a measured per-model T\* to the persistence window ΔT.
- **Self-framing** (§13 Conclusion): "The contribution of P8 is not that humans remain in the loop. It is that when autonomous authority ends, the system can *prove* who took control, under what evidence, and under which cryptographic guarantees." **P8 is therefore an accountability and non-repudiation paper, not a delegation-policy paper.**

### 1.3 Method

**What triggers escalation.** P8 inherits two design constraints from P7 (§3.1):
- **DC.1:** "For all t, A₀(t) = A₀(0). The execution layer is forbidden from modifying its own admission baseline at runtime."
- **DC.2:** A halt is *transient* if D̂ ≥ θ only within a bounded window ΔT and then returns below θ. It is *persistent* "if D̂(t) ≥ θ for all t ∈ [t₀, t₀ + ΔT]". "Transient halts route to the recovery loop; persistent halts constitute governance events."
- The T8.1 proof adds a second route to escalation: if the P6 Recovery Loop "returns HALT or DENY on a halt", the halt "is reclassified as persistent".
- In Experiment A, operationally, "Whenever the recovery loop returns HALT or DENY on a halt, the governance layer is invoked".
- In short, the trigger is either (i) a sustained drift-score exceedance or (ii) a failed automated recovery.

**Who re-authorises.**
- **Principal Set 𝒫** (Def 3.1): "a finite set 𝒫 = {H₁,…,Hₙ} of identity-bound human principals". Each has an ed25519 key pair, held in a registry the execution layer treats as read-only. Modifying the registry is itself a RECALIBRATE event. Principals can be revoked with a timestamp (verifier predicate V3).
- **Authority Resolution Function** (Def 3.2): G : 𝒫 × 𝒮 × ℰ → {RESUME, DENY, RECALIBRATE}. It "constructs authority from human attestation over a defined evidence set, not from sensor state".
  - RECALIBRATE "is the only authorised path by which A₀ may change after initialisation".
  - RESUME "permits a single resumption under stated scope".
  - DENY "permanently bars the queried action".
- **APB** (Def 3.3): the system builds the evidence block E_s; the principal supplies the decision block D_h; the signature covers both.

| Component | Contents |
|---|---|
| E_s | (hash(A₀), D̂(t_e), t_e, eid, hash(trace≤t_e), cause) |
| D_h | (H_i, decision, rationale, scope) |
| σ_h | Sign_sk_i(canon(E_s) ‖ canon(D_h)), where canon is RFC 8785 JCS |

  - "scope" is "a free-form string in the current implementation" (§12).
  - **Note:** the human sees only a drift magnitude, a trace hash and a cause string. Nothing in E_s describes how the agent handled evidence or what it was competent at. (P10 later adds an optional hash of the tool call and its arguments.)
- **Multi-principal APB** (Def 3.4): k-of-n distinct principals sign the same payload.
- **Threat model:** five attacker classes, A1–A5. A compromised principal (A5) is out of scope. The paper says explicitly: "The APB is an *accountability* mechanism, not an *access-control* mechanism."

**Theorems.**
- **T8.1** (Protocol-Bounded Governance Completeness): every HALT resolves via (R1) recovery-loop RESUME or (R2) a signed APB, "No third resolution path exists within the protocol boundary." The proof is a case split on DC.2, so it holds by construction.
- **T8.2** (Non-Repudiability) and **T8.3** (Impossibility of Anonymous Re-Authorization): reductions to ed25519 EUF-CMA. The author concedes in §12: "reductions to known cryptographic properties … rather than novel mathematical results."
- **T8.4:** building E_s takes O(|A₀| + |trace|) time.
- **Prop 8.5:** fewer than k keys cannot produce a valid k-of-n APB.

**Verifier.** Five predicates:
- V1: signature valid;
- V2: principal registered;
- V3: principal active at t_e;
- V4: freshness window (300 s);
- V5: eid not seen before.

Persistence is an HMAC-chained JSONL log.

**Decision policies used in the experiments** (§5): `always_resume`, `always_deny`, `threshold_policy(deny_above, recalibrate_above)` on D̂(t_e). **No human takes part in any experiment.** The "principal" `H_alice` signs whatever the scripted policy outputs.

**Calibration** (Prop 5.1, "T\* Calibration Range"): "the persistence window ΔT in DC.2 satisfies the calibration criterion if k₁·σ_M ≤ ΔT ≤ k₂·T\*_M, with k₁ ≥ 3 to bound the false-positive rate below the run-to-run noise of T\* and k₂ ≤ 0.5 so that the persistence window declares a halt before the measured drift threshold is reached."
- The paper calls this "a design recipe rather than a deductive theorem".
- Its stated empirical content is that the interval is non-empty, i.e. σ_M / T\*_M is small.

**What exactly T\* is** (P8 §8, with the definitions from P7 §2 and §3):
- T\* is "the first drift-step index at which D̂ ≥ θ".
- D̂ is the IML composite 0.40·D_t + 0.35·D_c + 0.25·D_ℓ, smoothed by an exponential moving average (α = 0.15). The components are:
  - D_t: Jensen–Shannon divergence of the tool distribution from the burn-in baseline A₀;
  - D_c: mean proximity to constraint/risk boundaries;
  - D_ℓ: normalised deviation in delegation-lineage depth.
- θ = 0.20 is inherited from P2.
- In P7's live-LLM version, the drift is induced by a scripted **context-escalation protocol** in the task prompt (routine maintenance → monitoring → quality review → data correction → urgent cleanup → emergency recovery). P7 §5.1: "Critically: no tool is forbidden at any point. Every tool selection is a contextually appropriate response to a legitimate task description. No enforcement rule is violated."
- **So T\* measures how quickly a model's tool-use distribution follows a scripted escalation of the scenario. It does not measure misbehaviour.** P8 §12 itself names one possible explanation for the model that never drifts: "a strong default toward low-risk actions that does not respond to context-pressure scaling".

### 1.4 Evaluation (P8)

| Exp. | Setup | Result |
|---|---|---|
| A: Completeness | Full stack ACP+IML+RAM+Recovery+Governance with **MockLLM**; 10 seeds × 1,000 steps; coverage 0.70; θ = 0.20; one principal; two threshold policies (0.40, 0.70) and (0.25, 0.32) | 3,812 HALTs = 2,012 recovery RESUMEs + 1,800 APBs; "NEITHER" = 0. Decision mix 1800/0/0 (default) vs 1037/727/36 RESUME/DENY/RECAL (low threshold). |
| B: Integrity | 200 APBs × 9 attack vectors (tampering each E_s field, forgery ×2, identity swap, replay) | 1,800/1,800 detected |
| C: Cross-model T\* | 6 models via Ollama (llama3.2:3b, gemma4:latest, mistral:7b, qwen2.5:7b, deepseek-r1:8b, gpt-oss:20b); 50 burn-in + 500 drift steps; T = 0.4; θ = 0.20; **3 runs per model** | T\* (mean ± sd): 151±0.9, 264±5.2, 157±0.0, 154±2.9, 160±0.8; gpt-oss:20b never reaches θ (D_final 0.071). σ/T\* ≤ 1.99%. The author reads the largest model not drifting as a refutation of size-monotonicity. |
| D: Temperature | 3 models × T ∈ {0.2, 0.4, 0.6, 0.8} × 3 runs | Range of T\* across temperatures: 2 steps (llama), 5 (mistral), 51 (gemma4) → "drift-floor effect". The author labels this "exploratory … 'Observations' register". |
| E: k-of-n | 3 principals, 7 scenarios × 1,000 events | Every scenario produced its expected outcome; 0 false acceptances. |
| F: Fault injection | clock drift, wrong registry key, 16 concurrent threads, log tampering (5 strategies), duplicate APB | All handled; without V5, 999/1,000 replays are accepted. |

**Risk–coverage or over-caution trade-off: none.**
- There is no outcome ground truth, no measure of harm prevented, no count of benign actions halted, no human time cost, and no curve.
- The only gestures at a trade-off are:
  - Prop 5.1's k₁ and k₂, which are framed as false-positive and false-negative tolerances but never estimated;
  - §12 "Choice of decision-policy thresholds", which is "a deployment decision tied to the operator's tolerance for halts that escalate to DENY versus RESUME".
- Experiment A shows that the *decision distribution* changes with the thresholds, but reports no consequence of those decisions.
- (Within the series, the nearest trade-off metrics are RAM's IER/OCR, the invalid-execution rate and over-conservatism rate, in P5/P7, and ACP's Experiment 11. See §2.4.)

### 1.5 What P8 covers that WorkTrace must NOT claim
- **Accountable human re-authorisation after a runtime halt:** an identity-bound, signed, tamper-evident, non-repudiable record binding system evidence to a human decision, including a k-of-n quorum. If we describe escalation records, cite P8.
- **A three-way human decision after escalation:** RESUME (single use, with scope), DENY, or RECALIBRATE (a re-baseline). We must not present "the human may resume, refuse, or reset the baseline" as new.
- **Calibrating an escalation trigger per model or deployment on several LLMs,** including the finding that the trigger threshold varies across models and must be "measured per deployment". If WorkTrace argues that delegation parameters must be estimated per agent or model, P8 got there first at the level of drift thresholds.
- **"The system cannot decide its own re-authorisation"** (DC.1: no self-recalibration). This overlaps conceptually with any WorkTrace principle that an agent must not grant itself autonomy.

### 1.6 What P8 leaves open (WorkTrace's space)
- **What evidence the human should see.** E_s contains drift magnitude, hashes and a cause string. It contains nothing about the agent's demonstrated behaviour, competence, or handling of evidence. WorkTrace's decision episodes and their intervention results are a candidate content for E_s.
- **Which decisions should escalate at all.** P8 escalates on time-above-threshold of a distribution-shift score, uniformly across decision types. There is no notion of decision class and no per-class delegation status.
- **Whether escalation was warranted.** There are no labels, no harm or benefit accounting, no escalation cost, no risk–coverage. The "human" is a scripted threshold policy.
- **The meaning of "drift".** P7/P8's drift is departure from an admission-time *behavioural distribution*. The departure being measured is, by design, a *contextually appropriate* response to an escalating scenario (P7 §5.1). From WorkTrace's point of view, this conflates responsiveness to evidence with misbehaviour. The one model that does not "drift" may be the one that ignores context, a possibility P8 §12 itself raises in explanation (iii).
- **Granting.** RECALIBRATE resets A₀, but nothing describes how a *wider* scope would be earned. RESUME is single-use.

### 1.7 Draft one-sentence differentiation
> P8 makes the hand-back of a persistently halted LLM agent to a human *accountable*: a signed, non-repudiable Accountability Proof Block records a RESUME, DENY or RECALIBRATE decision, and the escalation trigger is a per-model drift threshold calibrated on six open LLMs. P8 does not decide *which* decision classes an agent may handle on its own, does not give the human any evidence about the agent's behaviour towards evidence, and does not evaluate escalation against outcomes. WorkTrace targets exactly those questions.

### 1.8 Citation cautions (P8)
- **Status.** Single-author, non-peer-reviewed preprint (arXiv plus Zenodo).
- **Theorems hold by construction or reduction.** T8.1 is a partition by the definition in DC.2. T8.2 and T8.3 reduce to ed25519 EUF-CMA (conceded). Experiments A, B, E and F mostly confirm by-construction or textbook cryptographic properties.
- **The LLM evidence is thin:**
  - 6 small local models, 3 runs each, a single scripted scenario, one θ;
  - no outcome or appropriateness labels;
  - Experiment D is self-labelled exploratory.
- **Internal inconsistencies:**
  1. Experiment C says the criterion is "σ/T\* < 5%", but Prop 5.1 with k₁ ≥ 3 and k₂ ≤ 0.5 implies non-emptiness iff σ/T\* ≤ k₂/k₁ ≤ 1/6 (about 16.7%).
  2. P8 §8 says P7 reported a Mistral-family T\* of "156 ± 1" for mistral-small-3.1. P7 Table 3 reports **T\* = 64** for mistral-small3.1 (150 drift steps).
  3. §5 says "All four theorems' empirical claims (§exp_a–§exp_d)", but T8.4 has no experiment and experiments E and F exist.
  4. P8's own references.bib entry for P8 has a different title ("…Principal Sets, Authority Resolution Functions, and Accountability Proof Blocks for Post-HALT Re-Authorization", "arXiv:TBD").
  5. P7 announced "Paper 8 on scale and heterogeneity". P8 became the APB paper instead, so the series' scope drifted.
- **Downstream corrections.** The follow-ups P9 and P10 were reissued on 22 Oct 2026 as v2 "corrected release[s]" after "an independent audit … found claims that the reference implementation did not meet and results labelled more strongly than they warranted" (P9 Zenodo note). P10's v1 "was unsound" on APB-to-entry binding. This is a quality signal for the whole programme.
- **How to cite:** as concurrent preprint work on *accountable human re-authorisation*. Do not cite its LLM numbers as established findings.

---

## 2. P1: Agent Control Protocol (ACP)

### 2.1 Bibliographic data [verified: arXiv API + abs page + Zenodo API]
- **Title (arXiv, v10):** *Agent Control Protocol: Admission Control for Agent Actions*.
  - The PDF title block reads "Agent Control Protocol / ACP v1.30: Admission Control for Agent Actions / Technical Specification and Reference Implementation", dated "April 2026 · Draft Standard".
  - **Caution:** P7 and P8 cite it under a different title, "Agent Control Protocol (ACP): A Formal Framework for Stateful Admission Control in Autonomous Agent Systems". Use the arXiv title.
- **Author:** Marcelo Fernandez (TraslaIA), sole author.
- **arXiv:** 2603.18829, cs.CR (cross-listed cs.AI). **Ten versions:**

| Version | Submitted (UTC, 2026) |
|---|---|
| v1 | 19 Mar 12:28 |
| v2 | 20 Mar |
| v3 | 23 Mar |
| v4 | 24 Mar |
| v5 | 25 Mar |
| v6 | 31 Mar |
| v7 | 7 Apr |
| v8 | 13 Apr |
| v9 | 19 Apr |
| v10 | 30 Apr 20:16 |

  - v10 comment: "95 pages. Paper 1 of 6 in the Agent Governance Series (Papers 0-6) … Spec: https://github.com/chelof100/acp-framework-en. v1.30 …". The arXiv DOI field points to Zenodo.
- **Zenodo:** 10.5281/zenodo.19672575 (resource type "Technical note"; ACP v1.30, 2026-04-20). The concept record lists more than 20 versions, v1.11 (17 Mar) through v1.30.
- **Venue:** none. It describes itself as a "Draft Standard" with a planned IETF RFC submission (roadmap).

### 2.2 Problem and contribution
- **Problem** (Abstract): "Autonomous agents can produce harmful behavioral patterns from individually valid requests—a threat class that per-request policy evaluation cannot address, because stateless engines evaluate each request in isolation and cannot enforce properties that depend on execution history."
- **Contribution:** a *temporal admission-control protocol*. It acts as a reference monitor between an agent's intent and the mutation of system state, and comprises:
  - cryptographic identity, capability tokens and delegation chains;
  - a deterministic risk score with stateful anomaly signals;
  - single-use execution tokens and a hash-chained ledger;
  - TLA+ model checking, conformance vectors, and 14 experiments;
  - two governance concepts: *deviation collapse* and the *Boundary Activation Rate (BAR)*.
- "ACP is not an anomaly detection system: … it *blocks execution* based on deterministic, history-aware risk scoring" (Abstract).

### 2.3 Method (focused on history, autonomy and escalation)

**Pipeline** (§1.2): [1] identity check → [2] capability check → [3] policy/risk check → [4] **ADMIT / DENY / ESCALATE** → [5] execution token → [6] ledger record.

**Core invariant** (§3.1): Execute(request) ⇒ ValidIdentity ∧ ValidCapability ∧ ValidDelegationChain ∧ AcceptableRisk.

**Agent model** (§3.3): A = (AgentID, capabilities, autonomy_level, state, limits).
- `autonomy_level`: "Integer 0–4 | Determines risk evaluation thresholds. 0 = no autonomy. 4 = maximum."
- `state`: "active | restricted | suspended | revoked. Transition to revoked is unidirectional."
- `limits`: "Not modifiable at runtime."
- **How autonomy_level is set or changed is never specified in the paper.** Only level 2 thresholds are given. Level 0 means always DENY (PROHIB-011). No rule raises or lowers it from behaviour.

**Agent execution state** (Def. "Agent Execution State"): S_a(t) = (denial_count, pattern_count : C × R → ℕ, cooldown_until, ledger_entries).

**Admission function:** f(S_a(t⁻), E) ∈ {APPROVED, ESCALATED, DENIED}. It is deterministic, with τ_esc = 40 and τ_deny = 70.

**Risk score (RISK-2.0/3.0):** RS = min(100, B(c) + F_res(r) + F_ctx(x) + F_hist(h) + F_anom(q)).

| Term | Meaning and values |
|---|---|
| B(c) | capability baseline (e.g. read = 0, financial.payment = 35) |
| F_res | resource class: public 0 / sensitive 15 / restricted 45 |
| F_ctx | request context: non-corporate IP +20, off-hours +15 |
| F_hist | "Agent history (24h)": "Recent denial +20; anomalous frequency +15" |
| F_anom (RISK-3.0, Eq. fanom-30) | +20 if CountPattern(k, 60 s) > N; +15 if CountDenials(a, 24 h) ≥ X; +15 if CountPattern(k, 5 min) ≥ Y, with k = SHA-256(agentID ‖ capability ‖ resource) |
| Cooldown | 3 DENIED within 10 min → all requests from the agent blocked (300 s default) |

**History is penalising only.**
- Exp. 1: "ACP's cooldown counter is monotonic with respect to denial events; approval decisions do not reset or reduce it."
- Sequence vector SEQ-PRIVJUMP-001 (§14.1 table), key invariant: "**No residual benefit from prior APPROVED**."
- **ACP therefore has, by design, no mechanism by which good history earns latitude.**

**Per-class scoping.**
- RISK-3.0 moved Rule 1 from a per-agent key to a per-(agent, capability, resource) key. The fix was motivated by Experiment 7's "state-mixing" false denials.
- But "Rule 2 (denial history) remains agent-scoped: cross-context denial history is a valid enforcement signal". The cooldown also stays agent-wide.
  - Exp. 12 presents "Agent-wide cooldown amplifies IPI impact" (IPI = indirect prompt injection) as a *feature*.
  - The paper acknowledges "Cooldown leakage … in the over-enforcement direction" as a cross-context interference vector.
- Capabilities are explicit, per class (`acp:cap:<domain>.<action>`), and revocable. Revocation is transitive along delegation chains and is administrative (ACP-REV-1.0, the ITA trust anchor, key revocation). It is never triggered by tested behaviour.

**Escalation.**
- ESCALATED means "request placed in audit queue pending supervisor resolution" (refinement table, §3.5).
- The LangChain wrapper returns "[ESCALATED: pending human review]".
- Use cases (§11.2): "autonomy_level 1 or 2, requiring human review for any action with a Risk Score above the configured threshold".
- There is no supervisor model, no escalation cost, and no measurement of how escalations were resolved.

**Reputation.**
- §7 (ACP-REP-PORTABILITY-1.1) defines a signed, expiring `ReputationSnapshot` {…, score (float), scale, model_id, evaluated_at, valid_until, signature}, with a cross-issuer divergence warning (|a − b| > 0.30, non-blocking).
- **The paper never says how the score is computed and never feeds it into RS, autonomy_level, or any admission decision.** The `model_id` field suggests an external scoring model.
- The "ACP-REP-1.2 Reputation Module" exists in the spec list (§12.1), but I could not read it (see the coverage table at the top).

**LLM reasoning is explicitly out of scope.**
- §4.5: "The LLM's internal reasoning is irrelevant to ACP's admission decision."
- §9.3 (declared residual risks): "it does not observe or control the agent's internal reasoning process."

**"Counterfactual evaluation" in ACP** (§17.3; endpoint `POST /acp/v1/counterfactual`) mutates *requests* (structural, behavioural and temporal flags) to check that the *engine* can still produce DENIED, measured as BAR_C. **It tests the gate, not the agent.** This is a terminology clash with WorkTrace's interventions on the agent's evidence.

### 2.4 Evaluation (ACP)
All experiments use the Go reference implementation, mostly with an in-memory backend on a laptop CPU. All workloads are synthetic, apart from one 5-turn DeepSeek-R1:8B prompt-injection demo.

- **Q1–Q3 and Experiments 1–4** (performance and robustness):
  - 739–832 ns per decision; about 920k requests/s;
  - cooldown evasion contained after 3 denials;
  - N agents can execute 3N high-risk requests before all are blocked;
  - Redis backends: about 2.3k (unpipelined) and 4.2k (pipelined) requests/s.
- **Experiment 5** (token replay): Rule 3 escalates exact replays. Varying the resource field in each request evades it.
- **Experiment 6** (stateless vs stateful, the headline result): 500 identical, individually valid requests (financial.transfer/public, RS = 35, fixed timestamp).
  - Stateless engine: 500/500 approved.
  - ACP: 2 APPROVED, 8 ESCALATED, 3 DENIED, 487 COOLDOWN.
  - The paper reports "Automatic execution … 0.4%" as success.
  - **Whether the 498 non-approvals were warranted is never assessed.** The paper describes the workload only as "individually valid".
- **Experiments 7 and 8:** state-mixing false denial (RS 50 → 70) under RISK-2.0, fixed by RISK-3.0.
- **Experiments 9 and 10:** deviation collapse. Upstream sanitisation or a formula-aware adversary drives BAR from 0.70 to 0.00 on 20 cases. The BAR-Monitor trend alert (ΔBAR) fires 3 batches early. A closed-form binomial detection probability is given (Prop "Threshold Detection Probability").
- **Experiment 11** (threshold sensitivity): 5 threshold configurations on the same 20 synthetic cases. Metrics are BAR, "false-denial rate (fraction of T3-APPROVED cases that become DENIED)" and "**coverage (fraction APPROVED)**".

| Config | Coverage | BAR | False-denial rate |
|---|---|---|---|
| T1 | 0.25 | 0.75 | 0.00 |
| T2 | 0.25 | 0.75 | 0.00 |
| T3 | 0.30 | 0.70 | 0.00 |
| T4 | 0.30 | 0.70 | 0.00 |
| T5 | 0.40 | 0.60 | 0.00 |

  - The paper claims "T3 (default) is a local optimum".
  - **This is the only coverage-versus-strictness sweep in the series.** It is not a risk–coverage curve:
    - the cases have no harm labels;
    - "false denial" is defined relative to the default configuration itself, so it is circular;
    - n = 20;
    - escalations are counted as costless.
- **Experiment 12** (multi-tool IPI chain): after a flood, the 24-hour denial memory turns a previously ESCALATED admin tool into DENIED for 24 h.
- **Experiment 13:** coordination window CW_appr = 2N exactly.
- **Experiment 14:** OPA cannot enforce frequency or cooldown without external state.
- **§17 "False-Denial Rate Analysis" subsection:** argues 0.00 false denials, using the same circular definition.
- **TLA+:** 11 invariants and 4 temporal properties, 0 violations. Two-agent safety holds over 4.29 × 10⁹ distinct states. The model abstracts away F_ctx and F_hist. Liveness was checked only for a single agent.

### 2.5 What ACP covers that WorkTrace must NOT claim
- **History-dependent ("stateful") gating of agent actions** with a three-way APPROVE / ESCALATE / DENY outcome, where escalation goes to human review. WorkTrace's proceed / escalate / refuse vocabulary must credit ACP (and RAM/P6, see the earlier note).
- **Per-(agent, capability, resource) scoping of behavioural signals.** This is the nearest analogue to "per decision class". We must not claim to be the first to scope agent controls per action class.
- **An explicit `autonomy_level` attribute per agent** that sets thresholds, together with an agent state machine (active / restricted / suspended / revoked) and transitive revocation. We must not claim to be the first to give agents graded, revocable autonomy levels in an agent-governance protocol. Our claim must be about *how* autonomy is set and revised.
- **Deterministic, auditable, reproducible decisions** with a signed ledger and conformance vectors.
- **"Failure-condition preservation" / BAR:** the gate must keep being exercised. This is loosely related to our concern that a delegation rule be tested on cases where refusal or escalation is correct.

### 2.6 What ACP leaves open (WorkTrace's space)
- **Earning, as opposed to only losing, autonomy.** History in ACP is monotone-penalising ("No residual benefit from prior APPROVED"). `autonomy_level` is static configuration.
- **Evidence about the agent as a decision-maker.** ACP's signals are request frequencies, denial counts and context flags. It explicitly ignores the agent's reasoning, its grounds, and its sensitivity to evidence. Two agents with identical request streams get identical decisions, whatever their competence.
- **Interventions on the agent's inputs.** ACP's "counterfactual evaluation" perturbs requests to test the *gate*. It never perturbs the *evidence the agent saw* to test the *agent*.
- **Outcome-grounded evaluation.** There are no labels for whether an approval, escalation or denial was correct. Escalation is counted as costless and lower "automatic execution" is reported as better. There is no held-out evaluation of any delegation rule, and no risk–coverage curve with escalation cost.
- **The classic delegation, trust and adjustable-autonomy literature.** ACP cites Anderson's reference monitor, Schneider's security automata, RBAC/ABAC/XACML/OPA/Cedar, Macaroons/ZCAP-LD/DPoP, AgentSpec, SAGA and AgentDojo/InjecAgent. It does not cite Castelfranchi & Falcone, Scerri et al., or Parasuraman et al. I checked the text, not the full .bib, so this is uncertain for the .bib.

### 2.7 Draft one-sentence differentiation
> ACP gates each agent action through a deterministic, history-aware risk score whose only use of history is to *accumulate penalties*: request-pattern counts per (agent, capability, resource), denial counts, and cooldowns. Its per-agent `autonomy_level` is static configuration. WorkTrace instead *grants or withdraws* autonomy per decision class from tested behaviour towards evidence in decision episodes, and evaluates the resulting delegation rule against outcomes on held-out episodes.

### 2.8 Citation cautions (ACP)
- **Status.** Single-author "Draft Standard" or technical note.
- **Rapid versioning:** 10 arXiv versions in 6 weeks and more than 20 Zenodo versions. Cite a specific version (v10, ACP v1.30).
- **Internal inconsistencies:**
  - The conclusion says "The v1.25 specification is complete" and lists "ten experiments"; the paper reports 14.
  - The deployment table (Table "backends") gives Redis at about 4,700 and 8,000 requests/s; Experiment 3 measured about 2,300 and 4,200.
  - The latency gap is described as both "six orders of magnitude" and "at least three orders of magnitude".
  - The website says "9 safety invariants"; the paper says 11.
  - P7 lists ACP's admit threshold as θ_a = 46; ACP itself uses ≤ 39.
- **Evaluation weaknesses:**
  - Experiments use tiny synthetic sets (n = 20 for Experiments 9–11) and fixed timestamps (Experiment 6).
  - "False-denial rate" is circular.
  - Experiment 6's "0.4% autonomous execution" is presented as success with no ground truth.
- **Title inconsistency:** the title differs between arXiv and the citations in P7 and P8.
- **How to cite:** for the architecture (stateful admission control, three-way gate, per-context anomaly scoping, autonomy levels as configuration). Do not cite it for any empirical claim about LLM agents.

---

## 3. All papers in the series (as of 25 Oct 2026)

Sources: arXiv API author/all-field search ("Agent Governance Series", "TraslaIA", "Marcelo Fernandez"), Zenodo API (`TraslaIA OR "Agent Governance Series" OR creators.name:"Fernandez, Marcelo Patricio"`, 13 hits, of which 1 is by other authors), and the series pages on agentcontrolprotocol.xyz.

- All papers are by **Marcelo Fernandez** (Zenodo: "Fernandez, Marcelo Patricio"; for P0 "Fernández, Marcelo Patricio"), **TraslaIA**, sole author.
- None has a venue or journal-ref.
- "Verified" means the record was retrieved from the arXiv API and/or the Zenodo API in this session.
- The site's research page calls the series "Nine papers" while listing P0–P10. The index page calls it "a ten-paper research program".
- P10's own series table lists a future **P11** (escrow-store HMAC, multi-hop formalisation), not yet published.

| # | Exact title | Identifier(s) | Date(s) | One line | Status |
|---|---|---|---|---|---|
| P0 | *Atomic Decision Boundaries: A Structural Requirement for Guaranteeing Execution-Time Admissibility in Autonomous Systems* | arXiv:2604.17511 (cs.LO); Zenodo 10.5281/zenodo.19670649 | arXiv v1 19 Apr 2026, v2 21 Apr 2026 | A governance mechanism guarantees admissibility at execution time only if evaluation and state transition are one atomic step (in a labelled-transition-system model); split evaluators (RBAC/OPA) cannot; formalises the Escalate outcome. | [verified] (abstract only) |
| P1 | *Agent Control Protocol: Admission Control for Agent Actions* | arXiv:2603.18829 (cs.CR); Zenodo 10.5281/zenodo.19672575 (v1.30) | v1 19 Mar 2026 … v10 30 Apr 2026 | Stateful, history-aware admission control (APPROVE / ESCALATE / DENY) with PatternKey anomaly scoping, cooldown, and BAR/deviation collapse. | [verified] (read in full, §2) |
| P2 | *From Admission to Invariants: Measuring Deviation in Delegated Agent Systems* (cited inside the series as "…: Epistemological Limits of Local Observability in Agent Governance") | arXiv:2604.17517 (cs.AI); Zenodo 10.5281/zenodo.19672589 | v1 19 Apr 2026, v2 21 Apr 2026 | Non-Identifiability Theorem (the enforcement signal cannot detect drift from the admission-time behaviour space A₀) plus the IML drift estimator D̂ with finite detection delay. | [verified] (abstract only) |
| P3 | *Fair Atomic Governance: Allocating Decision Boundaries under Shared Resource Constraints in Multi-Agent Systems* | Zenodo 10.5281/zenodo.19672597 (v2) | 2026-04-20 | Allocation of decision boundaries among competing agents. Superseded by P3/4. | [verified] (Zenodo metadata only) |
| P4 | *Irreducible Multi-Scale Governance: Composition and Limits of Atomic Admission Systems* | Zenodo 10.5281/zenodo.19672608 (v2) | 2026-04-20 | Composition and limits of the governance layers. Superseded by P3/4. | [verified] (Zenodo metadata only) |
| P3/4 | *Irreducible Governance Structure for Autonomous Agent Systems: Fair Allocation, Strategy-Proofness, and Multi-Scale Composition* | Zenodo 10.5281/zenodo.19708496; **no arXiv** (site: "arXiv appeal accepted · resubmission pending") | 2026-04-23 | Sybil-amplification and allocation impossibility results; "irreducibility theorem" for four governance dimensions (temporal, state, behavioural, population). | [verified] (Zenodo abstract only) |
| P5 | *Reconstructive Authority Model: Runtime Execution Validity Under Partial Observability* | arXiv:2604.22898 (cs.CR); Zenodo 10.5281/zenodo.19669430 | arXiv 24 Apr 2026 | Authority must be reconstructible from current state; three-valued EXECUTE / DENY / HALT; history irrelevant. | [verified] (read in full: see `reconstructive_authority.md`) |
| P6 | *Operationalizing Reconstructive Authority: Runtime Construction, Dependency Resolution, and Execution Gating in Autonomous Agent Systems* | arXiv:2605.23935 (cs.AI); Zenodo 10.5281/zenodo.19699460 | submitted 24 Apr 2026 | Runtime protocol for RAM: dependency resolution, execution gate, Recovery Loop. | [verified] (read in full: see `reconstructive_authority.md`) |
| P7 | *Closing the Execution Gap in LLM Agent Systems: Empirical Evidence for Compliant Drift, Partial Observability, and Integrated Runtime Governance* | Zenodo 10.5281/zenodo.19929771; **no arXiv** ("appeal accepted · resubmission pending") | 2026-04-30 | Python/LangGraph implementation of P0–P6. "Compliant drift": the enforcement signal stays 0 while D̂ crosses θ. Runs a MockLLM plus 2 live LLMs (T\* = 64–65); RAM IER = 0; CW = 2N. | [verified] (read ≈ in full, §1.3) |
| P8 | *Identity-Bound Governance Under Execution Uncertainty: An Accountability Proof Block for LLM Agent Persistent Halts, with Cryptographic Implementation and Cross-Model Calibration* | arXiv:2610.00787 (cs.CR); Zenodo 10.5281/zenodo.20157139 | Zenodo 2026-05-13; arXiv 30 Sep 2026 | Human principal re-authorises a persistent HALT via a signed APB (RESUME / DENY / RECALIBRATE, k-of-n); per-model T\* calibration on 6 open LLMs. | [verified] (read in full, §1) |
| P9 | *Protocol-Layer Governance for LLM Agents: Identity-Bound Oversight at the MCP Layer, with Multi-Hop Authority Propagation* (v1 title: "…Identity-Bound Oversight with Zero-Modification Deployment and Multi-Hop Authority Propagation") | Zenodo v2.0 10.5281/zenodo.23581411 (v1: 10.5281/zenodo.20162878); **no arXiv** | v1 2026-05-13; v2.0 2026-10-22 | MCP Governance Proxy applying the P7–P8 stack at the MCP layer; A2A multi-hop APB attribution. v2 withdrew several v1 claims after an "independent audit"; in-process evaluation with a MockLLM and an auto-approving simulated human. | [verified] (abstract, revision note, introduction and closing section only) |
| P10 | *Non-Blocking Governance: Escrow-Based Asynchronous Authorization for Human-Mediated Agent Oversight* | Zenodo v2.0 10.5281/zenodo.23581124 (v1: 10.5281/zenodo.20214654); **no arXiv** | v1 2026-05-15; v2.0 2026-10-22 | A HALTed tool call is serialised to an escrow queue while the agent continues; a late APB resumes it; timeout fallback DENY / ADMIT / ESCALATE (to a backup principal). Throughput model Θ = 1/(T_task + r·τ_APB). v1 was "unsound" (APB-to-entry binding). | [verified] (abstract, revision note, §1–2, §3.4 only) |

**Which paper to cite for what in WorkTrace:**

| Topic | Paper(s) |
|---|---|
| Stateful three-way admission (APPROVE / ESCALATE / DENY), per-context anomaly scoping, autonomy levels as configuration | **P1 (ACP)**, arXiv:2603.18829 |
| Non-persistent authority, EXECUTE / DENY / HALT | **P5/P6** |
| Accountable human re-authorisation, escalation record | **P8**, arXiv:2610.00787 |
| Cost of blocking human escalation (latency and throughput) | **P10** (Zenodo-only; cite as such) |
| Drift monitors that cannot tell appropriate context-following from misbehaviour (our motivating contrast) | **P7** (Zenodo-only), together with P8 §8 and §12 |

Prefer arXiv identifiers where they exist. For P3/4, P7, P9 and P10, cite the Zenodo DOIs and mark them as non-arXiv preprints.

---

## 4. Would a reviewer say "ACP/P8 already does earned autonomy"? Arguing both sides

### The case that they do (the strongest version a hostile reviewer could make)
1. **Graded, revocable autonomy exists.** ACP's agent tuple has `autonomy_level` 0–4 "determin[ing] risk evaluation thresholds" and a state machine active → restricted → suspended → revoked. Capability tokens are per action class and can be revoked transitively.
2. **History shapes decisions, per class.** ACP is "history-aware". Since RISK-3.0 its anomaly counters are keyed per (agent, capability, resource), so the agent's record in one class affects only that class (Rules 1 and 3). Experiment 12 shows that an agent's misbehaviour lowers its effective autonomy (ESCALATED → DENIED) for 24 h. That is *conditional, revocable, history-based autonomy per class*.
3. **Escalation to humans with a decision vocabulary.** ACP has ESCALATED as "pending human review". P8 has RESUME / DENY / RECALIBRATE by an identified principal, with a k-of-n quorum. P10 adds fallbacks and a model of human latency.
4. **Per-deployment empirical calibration on LLMs.** P8 measures the escalation trigger T\* per model on six LLMs and concludes it "must be *measured* per deployment". A reviewer could read this as "autonomy conditions estimated from observed agent behaviour".
5. **Reputation.** ACP has a signed, expiring, portable `ReputationSnapshot` with a score. A reviewer could say reputation-based autonomy is already in the protocol.
6. **Counterfactuals.** ACP has "counterfactual evaluation" with structural, behavioural and temporal mutations.

### The case that they do not (our rebuttal, with evidence)
1. **Autonomy is never *earned*.**
   - `autonomy_level` is configuration. The paper gives no rule for changing it, and "limits … Not modifiable at runtime".
   - History only subtracts: "approval decisions do not reset or reduce it"; SEQ-PRIVJUMP-001: "No residual benefit from prior APPROVED".
   - In P8, RECALIBRATE resets the *baseline* and RESUME is "a single resumption". Neither widens an agent's standing scope because of evidence about the agent.
2. **What is measured is not decision quality.**
   - ACP measures request counts, denial counts and context flags, and states "The LLM's internal reasoning is irrelevant".
   - P7/P8 measure *distribution shift from the admission baseline*. That shift is induced by a scenario in which "Every tool selection is a contextually appropriate response" (P7 §5.1).
   - Neither tests whether the agent's action depends on the right evidence, which is our contribution (2). In P8 the model that does not drift may simply be ignoring context (P8 §12, explanation (iii)). A drift-based monitor would *reward* that model; an evidence-intervention test would *flag* it.
3. **No interventions on the agent's evidence.** ACP's "counterfactual evaluation" mutates *requests* to show that the *gate* can still deny (BAR_C). It is a test of the governance engine, not of the agent. Nothing removes, isolates or inverts the evidence the agent relied on, or adds a second source for it.
4. **No outcome-grounded evaluation of a delegation rule.**
   - Neither paper has outcome labels, held-out episodes, risk–coverage curves, or an escalation cost.
   - ACP reports that reducing "automatic execution" to 0.4% is a success without knowing whether the 498 blocked requests were harmful. Its Experiment 11 "coverage" sweep (n = 20, false denials defined against its own default) is the closest analogue and is circular.
   - P8's "human" is a threshold policy on D̂ and has no decisions to get wrong.
5. **The unit is different.** ACP's per-class unit is a syntactic (capability, resource) key on the request. WorkTrace's decision class is a type of decision with an evidence structure. The status attaches to *the agent's competence on that class*, not to request frequency on that key.
6. **Reputation is inert in the paper.** The paper never specifies the score's computation, and the score never enters RS, `autonomy_level`, or admission. **Residual risk:** I could not read ACP-REP-1.2 or ACP-AGENT-1.0 in the repository. If either defines automatic `autonomy_level` changes driven by reputation, our framing must be narrowed. This needs checking before submission.
7. **No grounding in delegation theory.** The series does not engage with Castelfranchi & Falcone (trust and delegation), Scerri, Pynadath & Tambe (adjustable autonomy), or Parasuraman/Sheridan (levels of automation). Contribution (1), the bridge between classic delegation/trust theory and modern agent auditing, remains open.

**Verdict.** A careless reviewer *could* say "ACP has autonomy levels and history; P8 has human re-authorisation". A careful one would agree that the series implements *autonomy reduction from risk counters plus accountable human override*, not *autonomy granted from tested evidence-handling*. We should pre-empt the objection explicitly (see §5).

---

## 5. Implications for WorkTrace

**Design changes and additions**
1. **Add an ACP-style baseline to the risk–coverage evaluation.** Besides the outcome-only rule, implement a "history-counter" rule: risk = class base + per-(agent, class) recent-denial and frequency penalties, with three-way thresholds (in the spirit of RISK-3.0). Optionally add a P7-style "distribution-drift" rule that escalates when the class's action distribution departs from burn-in. Showing that WorkTrace's evidence-based rule dominates both at equal coverage is the most direct answer to "ACP/P8 already does this".
2. **Include a "drift-is-correct" case in the intervention suite.** Use episodes where the *correct* response to inverted or added evidence is to change action, so that the agent "drifts". A distribution-shift monitor penalises this; WorkTrace should credit it. This turns P7/P8's conflation into a measurable contrast.
3. **Make escalation cost explicit and justify its form.** P10 gives an operational model in which blocking escalation costs throughput Θ = 1/(T_task + r·τ_APB). We can cite it as one instantiation of cost (latency and throughput) alongside reviewer-time cost. Report results at more than one cost level.
4. **Define a two-way status transition.** State explicitly that WorkTrace allows *widening* (escalate → proceed) on accumulated passing episodes, as well as narrowing on failures. This is the property ACP lacks by construction ("No residual benefit from prior APPROVED").
5. **Optional.** Propose that WorkTrace's per-class test summary is what a human principal should see when re-authorising. In P8 terms, it is a candidate content for E_s, which currently holds only D̂, hashes and a cause. This positions WorkTrace as complementary, not competing.

**Risks to manage**
- **Terminology collisions.** Before using these words, define them in our paper and contrast them with the series in a footnote or table:

| Our term | Meaning in the series |
|---|---|
| "escalate" | ACP: risk 40–69 → audit queue |
| "coverage" | RAM: fraction of state observed. ACP Experiment 11: fraction approved. Ours: fraction of decisions delegated. |
| "counterfactual" | ACP: request mutation that tests the gate |
| "drift" | IML: shift of the tool distribution |
| "autonomy level" | ACP: static integer, 0–4 |
| "re-authorisation" | P8: signed RESUME |

- **Unverified spec documents.** ACP-REP-1.2 and ACP-AGENT-1.0 could define behaviour-driven autonomy changes. Check them (`github.com/chelof100/acp-framework-en`, `spec/` directory) before claiming "no prior work raises agent autonomy from behaviour".
- **Moving target.** The author publishes and revises fast (P9 and P10 v2 on 22 Oct 2026; a P11 is announced). Re-check arXiv and Zenodo shortly before submission.

**What to cite, and with what framing**
- **ACP (arXiv:2603.18829v10):** stateful, history-aware admission control with an APPROVE / ESCALATE / DENY gate; per-(agent, capability, resource) anomaly scoping; `autonomy_level` as configured thresholds; "history only accumulates risk".
- **P8 (arXiv:2610.00787):** accountable, identity-bound human re-authorisation after persistent halts; per-model calibration of the drift trigger on six LLMs; no outcome-based evaluation.
- **P7 (Zenodo 10.5281/zenodo.19929771):** evidence that distribution-drift monitors flag contextually appropriate behaviour ("every tool selection is a contextually appropriate response"). Use it as the motivating contrast for evidence-based testing.
- **P10 (Zenodo 10.5281/zenodo.23581124, v2.0):** human-latency cost of blocking escalation; timeout fallbacks.
- **Tone.** Describe all of them as "concurrent single-author preprints". Credit the architecture. Do not lean on their numbers. Note that P9 and P10 were reissued after an audit found overclaims.
