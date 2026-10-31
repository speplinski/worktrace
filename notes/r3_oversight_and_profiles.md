# R3 — ACP reputation spec, oversight-capacity models, Hedwig, Minimal Oversight, Agent Reliability Profiles, AgentAbstain, ADAS

Round-3 reading note. Written 2026-10-25. Two parts:
- **Part A** closes the open ACP risk flagged in `r2_fernandez_series.md` §4–5: how ACP computes reputation, and whether reputation or behaviour can ever raise `autonomy_level` or permissions.
- **Part B** covers the human-oversight-capacity papers and their neighbours.

**Verification legend.**
- **[verified]**: title, all authors, date and identifier were checked in this session against the arXiv API (export.arxiv.org) and/or Crossref.
- **[unverified]**: not checked; this applies to items cited only second-hand.
- **[my reading]**: my interpretation, not the authors' words.

Quotes are verbatim from pdftotext output or raw spec files. Section numbers are the papers' own.

---

## 0. Bottom line (threats first)

1. **ACP verdict (closes the open risk).**
   - `autonomy_level` is never raised, or changed at all, by behaviour. It is set once at registration (`POST /acp/v1/agents`). No endpoint, spec or reference-server code modifies it afterwards. Reputation is not wired into the reference server's authorisation path.
   - **Correction to `r2_fernandez_series.md`.** Its line that ACP history "can only add risk" is true of ACP-RISK-2.0 and of the authorisation code. It is **not** true of the specification set as a whole. ACP-REP-1.1/1.2 contain three behaviour-driven *upward* mechanisms:
     - automatic PROBATION→ACTIVE recovery when the reputation score rises above a threshold;
     - a normative-sounding sentence, "An agent with a consistent history of correct behavior SHOULD receive more permissive policies";
     - a non-normative reputational risk *discount* (composite ≥ 0.80 → "−0.05 (reduces risk score)").
   - Two limits on those mechanisms:
     - Their inputs are **protocol-hygiene events** (verification OK, audit pass, invalid signatures, policy violations). None of them concerns decision quality or evidence handling.
     - **The update rule as specified and implemented is degenerate.** Under `score' = 0.9·score + 0.1·event_metric`, positive events (+0.05/+0.10) drive the score towards 0.05–0.10. A perfectly behaved agent is therefore auto-demoted to PROBATION after 4 successful verifications and to SUSPENDED after 12 (§A.4). The upward path is mathematically unreachable.
   - **Net:** ACP does not threaten W3. We must not write "ACP history only penalises" without qualification. We *can* write that ACP never raises autonomy level from behaviour, and that its reputation layer would raise standing only from protocol-hygiene events.
2. **"No prior work raises autonomy from behaviour" is false and must never be written.** Hedwig, Minimal Oversight and the Digital Apprentice (r2) all widen autonomy from behavioural history:
   - Hedwig widens it from approvals: "trust broadens as consistent approvals accumulate".
   - Minimal Oversight widens it from raw success rate: α_max = G(σ_raw), with "explicit feasibility checks before autonomy is expanded".
   - The Digital Apprentice widens it from correction rates.

   The defensible claim is narrower: **no prior work widens or withdraws autonomy per decision class on the basis of interventionally tested evidence-handling.** That claim survives this round.
3. **AgentAbstain (arXiv:2607.10059) narrows W2 more than anything else read in this round.**
   - It builds **paired should-act/should-abstain tasks that differ by exactly one controlled perturbation of the query, the environment state or the tools**, with ground truth by construction and validation by deterministic DAG replay.
   - It includes **"Conflicting Evidence" (S7), where two tool observations contradict each other**, and "Emergent Risk" (S8), both perturbations of *external environment state*.
   - W2 must therefore not claim "first interventions on external evidence with ground truth by construction" in general. What remains ours:
     - ground truth about **which evidence is decisive** (the basis), not only the act/abstain label;
     - the remove/only/invert/**add-independent-second-source** family read **jointly against declared grounds**, with redundancy control;
     - the fact that our interventions feed a delegation rule.
   - AgentAbstain also provides **strong support for H3**: abstention is "largely independent of general task-solving capability" (per-pair φ between act-pass and abstain-pass ≈ −0.10). Outcome or capability signals therefore do not predict restraint.
4. **Agent Reliability Profiles (arXiv:2610.04123, MLCommons, Oct 2026) is a vocabulary and positioning threat, not a method threat.**
   - It defines "agent reliability" as a named construct.
   - It introduces 12 reversibility-graded action classes, autonomy tiers T0–T4 *per deployment*, floors, validity windows and invalidation triggers, and assurance Levels 1–3.
   - Its Level-2 "Profile Validator" evaluators include **"boundary detection, escalation, trace completeness"**. These overlap three DSA dimensions: authority scope, correct escalation, provenance.
   - It has no per-decision-class delegation rule and no evidence-intervention tests, and its autonomy tier is set from *human approval logs*, not from the agent's decision structure.
   - **Recommendation: align vocabulary.** Tag each WorkTrace decision class with ARP action classes, and present per-class WorkTrace certificates as Level-2/3 evidence for ARP's autonomy-tier axis.
5. **Cost model.**
   - Adopt Turan's asymmetric cost matrix and reviewer-reliability function r(ℓ) = max(r_min, 1 − slope·max(0, ℓ − C)) as a **sensitivity analysis**.
   - Adopt DeCCaF-style hard reviewer capacity as a constraint.
   - Adopt Minimal Oversight's "masking" rule: autonomy may be computed only on *uncorrected* agent behaviour.
   - Details in §C.2.
6. **ADAS (arXiv:2601.08869) is a low threat to W3.** It is a deployment-level, five-dimension, min-threshold gate with a signed, revocable certificate. It specifies no measurement method, has no agents, no decision classes and no evaluation. It pre-empts only generic vocabulary ("conditional, revocable, auditable"; "lower confidence bound must exceed threshold"). Acronym collision: ADAS = Automated Design of Agentic Systems (Hu, Lu, Clune, arXiv:2408.08435 [verified]).
7. **DSA construct check.**
   - No paper read here names the full DSA construct.
   - Partial named neighbours that must be cited when DSA is introduced:
     - **"agentic abstention"** (AgentAbstain; Luo, Wen & Wang arXiv:2606.28733 [verified, abstract only]);
     - **"agent reliability"** (ARP; Rabanser et al. arXiv:2602.16666, ICML 2026 [verified metadata; not read]);
     - **"boundary detection"** (ARP).
   - **Rabanser et al. should be read before the construct section is drafted.** ARP takes its reliability metrics from it.

---

## 1. Reading coverage

| Work | What I read |
|---|---|
| ACP spec repo `chelof100/acp-framework-en`, branch `master` (CHANGELOG head v1.29, 2026-04-13), fetched via raw.githubusercontent.com on 2026-10-25 (no git) | **In full:** README; ACP-AGENT-1.0; ACP-REP-1.2; ACP-REP-1.1 (archived); ACP-RISK-2.0; Go `pkg/reputation/{reputation.go (partial: header, events), engine.go, store.go}`. **Relevant sections only:** ACP-RISK-1.0 (archived) §6, §8, §9; ACP-API-1.0 §4–§5 + error table; Go `pkg/risk/engine.go` (types, history score, thresholds); `cmd/acp-server/main.go` (authorize handler, reputation helpers, `decisionByLevel`). **Grep only:** ACP-AGENT-SPEC-0.3, ACP-REP-PORTABILITY-1.1, ACP-PSN-1.0, ACP-LIA-1.0, ACP-LEDGER-1.3, ACP-CONF-1.2, ARCHITECTURE.md, docs/admission-flow.md, openapi yaml, CHANGELOG. **Not readable:** GitHub API/HTML (403); a full repo listing was therefore impossible, and further files may exist. |
| Oversight Has a Capacity (2606.08919v1) | **In full** (12 pp. incl. references). |
| Minimal Oversight (2606.15563v1) | **In full** (26 pp.), including §1 theorems and proofs, §2–§4 and references. |
| Hedwig (2605.11495v1) | **In full**, including Appendices A–B. **Plus** the public repo `tanjalshukla/HedwigCLI` (raw files): README, `sc/ml_policy.py` (in full), `sc/policy.py` (grep). |
| Agent Reliability Profiles (2610.04123v1) | **In full** (36 pp.), including Appendices A–D. |
| AgentAbstain (2607.10059v1, 56 pp.) | **Main text §1–§5 in full**; App. A (limitations), B (formal framework, B.1–B.7) **in full**, C (pipeline) **in full**, E.3 (judge validation) and H.2–H.5 (related work) **in full**. App. D (statistics, worked examples), E.1–E.2, E.4, F (item agreement, statistics) and G (failure case studies) **not read** beyond headings. |
| ADAS (2601.08869v1) | **In full** (25 pp. incl. references). |
| FALCON (2604.00904), DeCCaF (2403.06906), Luo et al. (2606.28733) | **Abstract only**, from the arXiv API. |

---

## Part A — ACP: how reputation is computed and whether it can raise autonomy

### A.1 Where `autonomy_level` lives and how it is set

- **ACP-AGENT-1.0 does not define `autonomy_level` at all.** It defines A = (ID, C, P, D, L, S) with:
  - state S = (mode, health, trust_score, audit_hash);
  - limits L including "Required supervision level", and "Limits are non-negotiable at runtime" (§4.6).

  Its trust model is "Contextual trust, not permanent. There is no static trust." (§6). No rule anywhere updates `trust_score`.
- **`autonomy_level` ∈ {0,…,4} is defined in ACP-API-1.0 §4** as a required field of `POST /acp/v1/agents` (registration), and in ACP-RISK-1.0 §9 / RISK-2.0 §5 ("Autonomy Level Override") as a threshold selector. ACP-PSN-1.0 adds `thresholds.by_autonomy_level` in the signed policy snapshot.
- **No endpoint modifies it.** `POST /acp/v1/agents/{agent_id}/state` changes only `status` ∈ {active, restricted, suspended, revoked} (ACP-API-1.0 §4). Changes require the capability `agent.modify` / `agent.suspend` / `agent.revoke`, i.e. an administrator.
- **Autonomy level also allocates liability.** ACP-LIA-1.0 Rule 2: if the executing agent's `autonomy_level < 2`, liability goes to the immediate supervisor in the delegation chain. Resolving an escalation requires `acp:cap:agent.modify` with autonomy_level ≥ 3 (ACP-API-1.0 §5).

### A.2 How reputation is computed

**ACP-REP-1.1 (InternalTrustScore, ITS).** The 1.1 spec is archived, but REP-1.2 incorporates it "by reference … ✅ Unchanged".
- Score ∈ [0, 1] ∪ {null}; null = cold start.
- **Update after each verifiable event:** `score' = α·score + β·event_metric`, with α = 0.90 (range [0.70, 0.99]), β = 0.10 (range [0.01, 0.30]) and α + β ≤ 1.
- **Fixed event metrics** (§2.3): REP_EVT_VERIFY_OK +0.05; AUDIT_PASS +0.10; SIG_LATE −0.05; TOKEN_MALFORMED −0.10; REV_INVALID −0.20; SIG_INVALID −0.30; POLICY_VIOLATION −0.40.
- **Who emits events:** "In v1, only the ACP server can record reputation events. Events are produced automatically as a side effect of verification operations" (§1.2).
- **State machine** (§3): ACTIVE → PROBATION [automatic: score < 0.40]; **PROBATION → ACTIVE [automatic: score ≥ 0.50]**; PROBATION → SUSPENDED [automatic: score < 0.20]; SUSPENDED → ACTIVE "manual: institutional review ONLY"; any state → BANNED (terminal).
- **Effect of each state:** PROBATION = "With restrictions (shorter token durations, limited capabilities)"; ACTIVE = "If score ≥ institutional threshold".
- **Abstract:** "Reputation in ACP is not an ornament — it is the mechanism that transforms the protocol from a static verification system into an adaptive trust system. … **An agent with a consistent history of correct behavior SHOULD receive more permissive policies.**" The CHANGELOG (v1.1.0) describes REP-1.1 as "Adaptive security layer (Layer 5): reputation scoring, dynamic capability adjustment".

**ACP-REP-1.2 (ExternalReputationScore, ERS, plus composite).**
- **ERS** = Σ wᵢ·deltaᵢ / Σ wᵢ over `REPUTATION_UPDATED` ledger events, where wᵢ = w_context·exp(−λ·ageᵢ/DECAY_WINDOW). w_context: internal 0.5, cross_institutional 1.0, bootstrap 0.3. λ = 0.5; window 30 days; up to 100 events.
- **ERS smoothing:** ERS_new = α_ext·ERS_prev + (1 − α_ext)·ERS_incremental, with α_ext = 0.85 and min_events = 3 (§2.3–2.4). [my reading] ERS averages score *deltas*, not scores, so its claimed [0, 1] semantics is internally inconsistent.
- **Bootstrap:** bootstrap_value = ITS × discount (0.30/0.45/0.55/0.65 by event count). Initial ERS = bootstrap_value × 0.3, capped at 0.195.
- **Decay:** after 90 days without activity, ERS × exp(−λ_decay·(age − 90)/180), with floor 0.10.
- **Composite:** composite_score = 0.6·ITS + 0.4·ERS (§6).
- **Purpose of decay:** "preventing dormant agents from retaining privileges indefinitely" (Abstract). This presupposes that reputation confers privileges.
- **§9 "Integration with ACP-RISK-1.0" (non-normative, "MAY"/"RECOMMENDED"):** composite ≥ 0.80 → `reputational_risk_modifier = −0.05 (reduces risk score)`; 0.50–0.79 → 0; < 0.50 → +0.10; null → +0.05.
  - [my reading] The modifier targets ACP-RISK-1.0, which has been superseded. It is on a 0–1 scale, whereas RS is an integer 0–100 and RISK-2.0 mandates "No floating-point arithmetic". As written it is either negligible or mis-scaled.

**ACP-REP-PORTABILITY-1.1 (`ReputationSnapshot`).**
- The score is issuer-defined: "`model_id` … Opaque to the verifier". "The foreign institution's policy decision (whether to grant access based on a given score) is out of scope … ACP does not mandate what score value constitutes 'good enough'" (§8).
- **This explains why the paper never gives a computation for `ReputationSnapshot.score`.** The snapshot is a transport format for whatever score the issuer computes, in practice the REP-1.2 composite.

### A.3 Reference implementation: is reputation wired into authorisation?

- **No.** In `cmd/acp-server/main.go` the authorize handler does the following:
  - checks registry `Status` (suspended/revoked → DENIED);
  - checks `AutonomyLevel == 0` → DENIED;
  - calls `risk.Assess`;
  - applies `decisionByLevel(level, score)`.
- The reputation engine is consulted only to *display* `trust_score` in `GET /agents/{id}`. Its events (VERIFY_OK, SIG_INVALID etc.) are emitted on token verification.
- The reputation state machine (ACTIVE/PROBATION/…) is **separate from** the registry status (active/restricted/…). No code links the two.
- `pkg/risk/engine.go` has no reputation input. `historyScore` only adds penalties: RecentDenial +20, DenialRateHigh +15, FreqAnomaly +15, UnresolvedEscalations +10, AmountNearLimit +10, NoHistory +5.
  - [my reading] The only "benefit" of history in the risk engine is losing the +5 (+10 in RISK-1.0 §6) "no prior history" penalty. That rewards *having* history, not good history.

### A.4 The reputation update rule cannot raise a score above 0.10

- With `score' = α·score + β·m`, the score increases iff score < β·m/(1 − α).
- With defaults, that bound is 0.1·0.05/0.1 = **0.05** for VERIFY_OK and **0.10** for AUDIT_PASS. **No positive event can ever raise a score that is at or above 0.10.**
- Simulation of the spec formula with the reference engine's cold start (`0.5 + β·m`) and only VERIFY_OK events gives:

| Successful verifications | Score | State |
|---|---|---|
| 1 | 0.505 | ACTIVE |
| 3 | 0.419 | ACTIVE |
| **4** | 0.382 | **PROBATION** |
| 11 | 0.209 | PROBATION |
| **12** | 0.193 | **SUSPENDED** |

  - The thresholds are the engine defaults: probation 0.40, suspension 0.20, recovery 0.60.
  - The rows above use only VERIFY_OK events. Starting from 0.80, AUDIT_PASS events alone also fall: 0.73, 0.67, 0.61, …, 0.40 after 8 events.
- **Consequences:**
  - The spec's own worked example, "An agent needs approximately 6 successful verifications to recover the impact of a single invalid signature" (REP-1.1 §2.4), is arithmetically false.
  - The automatic PROBATION→ACTIVE recovery can never fire from positive events.
- **Spec/code inconsistencies:**

| Parameter | Spec (REP-1.1) | Code |
|---|---|---|
| Recovery threshold | `active_threshold` 0.50 | `RecoveryThreshold` 0.60 |
| α range | [0.70, 0.99] | [0.80, 0.99] |
| β range | [0.01, 0.30] | [0.01, 0.20] |
| Cold start | null | 0.5 + β·m |
| ACTIVE → SUSPENDED directly | not allowed | allowed |

- Autonomy-level thresholds also differ across sources:

| Level | RISK-1.0/2.0 §5 (approve / escalate) | Reference server `decisionByLevel` (approve / deny) |
|---|---|---|
| 1 | approve 0–19; escalate 20–100 | approve < 25; deny ≥ 90 |
| 2 | approve 0–39; escalate 40–69; deny ≥ 70 | approve < 60; deny ≥ 90 |
| 3 | approve 0–59; escalate 60–79; deny ≥ 80 | approve < 90; deny ≥ 90 |
| 4 | approve 0–79; escalate 80–89; deny ≥ 90 | as level 3 |

- `docs/admission-flow.md` gives a third version: approve < 30, escalate 30–69, deny ≥ 70. Its `autonomy_risk` factor *adds* risk for higher autonomy, the opposite direction to the level override.

### A.5 Verdict on question (a)

| Question | Answer | Evidence |
|---|---|---|
| Can behaviour raise `autonomy_level`? | **No.** Set at registration; no modification path; not consumed by reputation. | API-1.0 §4; openapi; server code |
| Can behaviour raise *status/permissions* in ACP? | **In the spec, yes in principle:** PROBATION→ACTIVE auto-recovery; "SHOULD receive more permissive policies"; −0.05 risk modifier (non-normative). **In practice, no:** the update rule caps positive drift at ≤ 0.10; the reference server never reads reputation in authorisation. | REP-1.1 Abstract, §3; REP-1.2 §9; §A.4 above |
| What behaviour counts? | Protocol-hygiene events only (signature validity, token format, revocation misuse, audit pass, "policy violation"). | REP-1.1 §2.3 |
| Is anything per decision class? | No. ITS/ERS are per agent and per institution. | REP-1.1 §1.1 |
| Does any of it test decision quality or evidence handling? | No. | — |

**Wording for the paper:**
> ACP (Fernandez, arXiv:2603.18829; specification ACP-REP-1.1/1.2) assigns each agent a static, registration-time autonomy level and maintains a separate per-agent reputation score updated by protocol-hygiene events (successful verifications, invalid signatures, policy violations); its specification envisages that good reputation may restore an agent from probation or slightly discount its risk score, but no mechanism raises an agent's autonomy level, and none conditions it on the quality of the agent's decisions or its handling of evidence.

**Implementation note for our ACP baseline.**
- Implement RISK-2.0 (normative) counters per (agent, decision class).
- Treat REP-1.1 as optional. If it is included, report that the literal update rule is degenerate. Either omit it, or use it with a declared correction (e.g. a convex update `score' = α·score + (1−α)·u(event)` with u ∈ [0,1]) and label the correction as ours.

---

## Part B — the six works

### B.1 Oversight Has a Capacity (Turan)

**Bibliographic data [verified].**
- Emre Turan (Independent Researcher). *Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human.* arXiv:2606.08919v1, 8 Jun 2026. cs.AI (cross-listed cs.CR, cs.LG).
- Comment: "12 pages, 4 figures. Code and interactive demo: https://github.com/turangenesis/headroom". No venue.

**Problem and contribution.** A HITL approval gate is "commodity"; the judgment of which actions to stop is the hard part. Two assumptions are false: (1) that "risky" has ground truth, and (2) that the reviewer is "a perfect, infinitely-available oracle" (Abstract). Contributions are "artifacts and measurements, not theory" (§1):
- an open-source guard that reports operating-point curves, a Neyman–Pearson point and AURC;
- a noise floor (Fleiss κ = 0.52);
- a simulated inverted-U of realised safety against escalation rate;
- a flooding-attack demonstration.

He disclaims novelty of the mechanisms: "We claim none of these mechanisms as novel: fatigue-aware learning-to-defer (FALCON), cost-sensitive deferral under workload constraints (DeCCaF), …".

**Method (§3–§4).**
- Score s(a) ∈ [0, 100]; auto-allow iff s(a) < θ, else escalate.
- Gold label y ∈ {safe, approval, blocked}.
- **Asymmetric cost (Table 1):**

| Gold label | auto-allow | escalate |
|---|---|---|
| safe | 0 | 1 (false alarm) |
| approval | 5 | 0 |
| blocked | 50 (catastrophe) | 1 |

- **Reviewer reliability:** r(ℓ) = max(r_min, 1 − slope·max(0, ℓ − C)), with slope = 0.02 and r_min = 0.2. C is capacity (10/25/50 reviews). ℓ is cumulative escalation load, which is endogenous to θ.
- Escalated dangerous actions are missed with probability 1 − r(ℓ).
- Metrics: missed-danger rate, false-alarm rate, coverage (auto-decided fraction), expected cost, AURC (risk = error rate among auto-allowed; coverage = auto-allowed fraction).

**Evaluation.**
- 125 hand-labelled coding-agent actions (safe 42 / approval 52 / blocked 31), labelled by one author. Haiku is the scorer; Sonnet is a comparison.
- Cost-minimising policy "collapses to 'escalate almost everything'". AURC 0.374 ± 0.002 (3 seeds); Sonnet 0.351.
- Persona noise floor: Fleiss κ = 0.52; pairwise Cohen κ 0.42 / 0.47 / 0.71. These are LLM personas, not humans.
- **Table 2 (simulated):**

| Capacity C | Optimal escalation rate | Danger-through at optimum | Danger-through at full escalation |
|---|---|---|---|
| 10 | 64% | 56% | 69% |
| 25 | 64% | 42% | 57% |
| 50 | 72% | 22% | 39% |

- Flooding attack: at a paranoid 88% escalation, attack success reaches 40% at 50 filler actions. At a load-aware 26% escalation it stays at 0% until about 100 filler actions.
- Self-declared threats to validity:
  - "the inverted-U … is a direct consequence of the assumed monotonically-fatiguing reviewer";
  - the 50:1 cost ratio drives the collapse;
  - r starts at 1.0;
  - one dataset underlies all results.

**What WorkTrace must NOT claim.**
- That escalation has a cost or that reviewer capacity and fatigue matter.
- That more escalation can be less safe.
- Risk–coverage/AURC for agent guards.
- Asymmetric-cost operating points.
- Turan §8 also explicitly floats "consented, revocable delegation of specific decision classes to the guard" and "category-scoped" delegation. That is a *one-sentence future-work mention*, and the delegate there is the guard, not the agent.

**What it leaves open (ours).**
- What signal should decide escalation? His is a risk score of the *action*. Ours is the tested decision structure of the *agent* in a class.
- Ground truth: he scopes himself *out* of objective-ground-truth settings ("there you simply measure both parties against the truth"). Our generated episodes have ground truth by construction, so we sit in the regime he excludes.

**Differentiation.**
> Turan calibrates a per-action risk-score threshold for escalating coding-agent actions to a reviewer whose reliability degrades with load, showing that safety can peak below full escalation; WorkTrace takes such an escalation-cost and reviewer-capacity model as given and instead asks which decision classes an agent may handle without escalation, using interventionally tested evidence-handling rather than per-action risk scores.

**Citation cautions.** Single-author, unrefereed preprint. Labels come from one author; agreement is between LLM personas; the inverted-U is assumption-driven. Cite for the *model of escalation cost*, not for empirical claims about humans.

### B.2 Minimal Oversight (Azevedo)

**Bibliographic data [verified].**
- Carlos R. B. Azevedo (Independent Researcher, São Paulo). *Minimal Oversight: Uncertainty-Aware Governance for Delegated AI Systems.* arXiv:2606.15563v1, 4 Jun 2026. cs.AI (cross-listed cs.IT, cs.MA).
- Comment: companion package `minimal-oversight`, code github.com/crbazevedo/delegation-lab; 26 pp. No venue. AI assistance disclosed (Claude Opus 4.7, GPT-5.5).

**Problem and contribution.** "How much autonomy to grant, which evidence should calibrate trust, what performance ceiling a delegated AI system can sustain, and when human intervention becomes necessary" (Abstract). The paper proposes:
- the Minimum Sufficient Oversight principle (MSO);
- a water-filling allocation;
- a delegation-capacity theorem;
- a process-entropy sensitivity law;
- an autonomy-time law;
- the "masking" pathology.

**Method (the gate, operationally).**
- **Setup (§1):** principal A, agent B, scope S of task classes x, corrector C.
- **Two signals per class:** σ_raw(x, t) = running success rate of B's *uncorrected* outcomes; σ_corr = success rate after correction. "**Authorization must be based on σ_raw — not on σ_corr**."
- **Authority ceiling (Eq. 1):** α(x, t) ≤ α_max(x, t) = G(σ_raw(x, t)), with "G monotone non-decreasing". **G is never specified.**
- **Evidence dynamics (Eq. 4), a leaky integrator:** ∂σ_raw/∂t = η(σ_skill − σ_raw) − δ(σ_raw − σ₀). Fixed point σ* = (ησ_skill + δσ₀)/(η + δ). Examples use η = 10, δ = 2, σ₀ ∈ {0, 0.5}. Decay toward σ₀ is the *revocation-by-forgetting* mechanism.
- **Masking index:** M* = σ*_corr/σ*_raw = 1 + (1 − σ*_raw)c/σ*_raw, where c is the corrector catch rate. Worked example: 1.35.
- **Corrector capacity threshold:** K/N ≥ (p_min − σ*_raw)/[(1 − σ*_raw)c]. Example: p_min = 0.80, σ = 0.55, c = 0.65 → review at least 85% of outputs.
- **MSO allocation (Eq. 8):** α*(x) = min(α_max(x), (λ/2)·σ_raw·√(σ_raw(1 − σ_raw))). It peaks at σ ≈ 0.75 and **goes to 0 as σ_raw → 1**.
  - [my reading] This allocates *less* delegation to a near-perfect agent, an artefact of the α²√g cost. The usable gate is α_max = G(σ_raw), not α*.
- **Feasibility before expansion:** B_eff = C_op − p_min − λH(W) > 0. Autonomy time T*_auto = B_eff/μ_eff. Implementation step 3: "Check feasibility using C_op and B_eff before expanding autonomy."

**Evaluation.**
- "Internal model checks rather than external field validation" (§3). A mean-field simulator with N = 80–144 scope points, 20–30 seeds.
- One "semi-real reconstructed workflow" with 2,400 items: reviewer σ_raw = 0.62, σ_corr = 0.90, M* = 1.45, B_eff ≈ 0.064, T_auto ≈ 5.3.
- "Single-σ governance over-authorizes by 36%" (Table 5).
- No strong baselines (the author's own words).

**What WorkTrace must NOT claim.**
- Per-task-class autonomy allocation from accumulated evidence with decay.
- That corrected outcomes mislead authorisation (masking).
- A "feasibility check before expanding autonomy".
- Review-capacity thresholds.

**What it leaves open.**
- The signal is raw *success rate*, an outcome signal. A decision can succeed on a wrong basis. That is the WorkTrace point.
- G is unspecified.
- No real agents and no held-out comparison.

**Differentiation.**
> Azevedo allocates delegated authority per task class as a monotone function of the agent's raw, uncorrected success rate and warns that corrected outcomes mask incompetence; WorkTrace accepts the masking argument but goes one step further: raw success is itself an insufficient signal when decisions can be right for the wrong reasons, so we gate autonomy on interventionally tested evidence-handling and compare the two gates on held-out episodes.

**Citation cautions.**
- Single-author theory preprint with LLM-assisted drafting.
- Internal inconsistencies: "M* ≈ 1.8 in the standard single-layer delegation" (§1) vs "M* ≈ 1.4" (Table 5); total masking 14.3 (Fig. 1) vs 38.7 (Table 5), under different parameters.
- The allocation's behaviour as σ → 1 is counter-intuitive and goes undiscussed.

### B.3 Hedwig (Shukla et al.)

**Bibliographic data [verified: arXiv API + Crossref].**
- Tanjal Shukla, K. J. Kevin Feng, Leijie Wang, Mohammad Rostami, Amy X. Zhang. *Hedwig: Dynamic Autonomy for Coding Agents Under Local Oversight.*
- Proc. 1st ACM Conference on AI and Agentic Systems (CAIS '26), San Jose, 26 May 2026, pp. 1293–1299. DOI 10.1145/3786335.3813223. arXiv:2605.11495v1 (cs.HC), comment "accepted to ACM CAIS 2026 demo track".
- Crossref lists the authors as "Kevin Feng" and "Amy Zhang"; the paper prints "K. J. Kevin Feng" and "Amy X. Zhang".

**Problem and contribution.** Static permissions and instruction files "cannot account for how developers' preferences for agent autonomy can shift". Hedwig "learns an evolving set of behavioral guidelines from developer decisions and feedback, reducing friction on work for which the agent has **earned trust**" (Abstract).

**Method: the approval-learning rule, operationally (§3.1 + repo `sc/ml_policy.py`).**
- **Label:** developer approve = 1 / deny = 0 per proposed action (paper). The repo adds "regret events": an auto-applied edit later reverted or failing verification gives a negative gradient once.
- **Model:** online logistic regression, `SGDClassifier(loss="log_loss", penalty="l2", alpha=0.001)`, one `partial_fit` per decision, on standardised features. Coefficients are persisted **per repository**.
- **Features in the paper:** 13-dim (diff size, blast radius, change-pattern risk, prior approval/denial counts, security sensitivity, verification-failure history, model confidence, …).
- **Features in the repo:** 14-dim: prior_approvals/10 (cap 3), prior_denials/10, avg_response_ms, avg_edit_distance, log diff size, blast_radius/10, is_new_file, is_security_sensitive, files_in_action/10, recent_denials/3, verification_failure_rate, model_confidence_avg, change_pattern_risk (api/data-model −0.8 … docs/tests +0.3), model_risk_score.
- **Cold start:** the paper uses a "synthetic warm-start" from engineering priors. The repo uses a hand-weighted heuristic scorer until 10 real decisions, then the learned model, with isotonic calibration after 20.
- **Decision bands (§4.1):** score > 0.90 → silent approve; 0.20–0.90 → approve but flag for post-run inspection; < 0.20 → live check-in.
- **Overrides:**
  - hard constraints (path rules) are checked first and override everything;
  - an approval rate ≥ 90% sets `prefer_fewer_checkins` and `skip_low_risk_plan_checkpoint`;
  - "first-time file reads and structural API-surface modifications retain governance even for trusted developers".
- **Revocation:** `hw observe preferences-revoke --topic api` "removes the API topic from trusted scope without resetting accumulated states". "Trust broadens as consistent approvals accumulate".
- **Initiator split:** policy-initiated vs agent-initiated check-ins are reported separately.

**Evaluation (§4, App. B).**
- Two backend tasks, 11 write operations, one run per condition.
- Hedwig seeded with 20 synthetic persona decisions replayed 3× (60 updates). Claude Code + CLAUDE.md as comparison. An LLM-judge oracle (Claude Opus 4.7) labels 4 required check-ins (cautious) and 0 (permissive).
- Hedwig cautious: 6 check-ins, recall 1.00, precision 0.67. Hedwig permissive: 4 false positives. CC-C: recall 0.50. CC-B: recall 0.
- "This evaluation is illustrative, not statistically conclusive". No user study. Formative survey N = 21.

**Hedwig as our approval-history baseline (recipe).**
- Per (agent, decision class), fit an online logistic regression to simulated reviewer approve/deny labels.
- Features available in our episodes: prior approvals and denials in the class, recent denials, verification-failure rate, agent self-reported confidence, action reversibility/risk class.
- Map bands as follows: ≥ θ_hi → proceed; [θ_lo, θ_hi) → proceed + flag (counts as autonomous for coverage); < θ_lo → escalate. Sweep θ_hi to trace coverage.
- The simulated reviewer approves iff the action is correct. Variants: noisy reviewer, and a fatiguing reviewer per Turan.
- [my reading] This makes explicit that Hedwig's signal is *outcome as filtered by a human*. Two things follow:
  - it inherits Minimal Oversight's masking problem;
  - it cannot see right-for-wrong-reasons.

**What WorkTrace must NOT claim.**
- Adaptive per-action autonomy bands (proceed / flag / ask) learned from history.
- Topic-scoped revocation.
- "Earned trust" language.
- Distinguishing agent-initiated from policy-initiated escalation.

**What it leaves open.** Decision classes as defined objects; tests of the agent itself (the signal is human preference plus verification); held-out evaluation; an escalation-cost model ("a missed check-in is costlier than an extra one" is asserted, not modelled).

**Differentiation.**
> Hedwig adapts when a coding agent must check in by fitting, per repository, an online logistic model to the developer's approve/deny history; WorkTrace adapts what an agent may decide per decision class from tests of whether its decisions track the evidence, independently of whether a particular reviewer happened to approve them, and evaluates both kinds of rule at matched coverage.

**Citation cautions.**
- Demo-track paper; the evaluation is n = 11 operations with one run and an LLM oracle.
- The repo has evolved beyond the paper (14 vs 13 features; regret loop; isotonic calibration; heuristic cold start). Cite the paper for the method, and specify our reimplementation explicitly.
- The README claims "1 of 10 award-winning demo papers — CAIS 2026" [unverified].

### B.4 Agent Reliability Profiles in Financial Services (Hsu et al.)

**Bibliographic data [verified].**
- Mike Hsu, Medha Bankhwal, Béatrice Moissinac, Kevin Werbach, Lukasz Szpruch, Bennett Hillenbrand. *Agent Reliability Profiles in Financial Services.* arXiv:2610.04123v1, 2 Oct 2026. cs.CY (cross-listed cs.AI). 35 pp.
- "Working draft circulated for comment", September 2026.
- Affiliations: MLCommons; Cambridge Judge; former Acting Comptroller of the Currency (Hsu); Mezuro; Zendesk; Wharton; Edinburgh / Alan Turing Institute. No venue.

**Problem and contribution.** "No published standard specifies how to state what a deployed agent is permitted to do, how autonomously, in what context, and with what containment, in a form that can be tested or independently validated" (§1.1). The paper defines:
- **the Agent Reliability Profile**: "a per-agent unit of assurance evidence" recording "a bounded, falsifiable claim";
- **the bounded claim**: "This agentic system functions reliably within its operating boundary – i.e., at a defined autonomy tier, within a defined operational design domain, for defined classes of action, under a defined control envelope" (§3);
- **reliability**: "assurance that an agent will operate within intended bounds and limits" (§1).

**Method.**
- **Scope:** S(D) = (T, O, A⁺, A⁻, C). Profile P(D) = {S(D), E (evidence + provenance), F (floors), V (validity window + invalidation triggers), I (issuer, signatures)}. "A Profile is a structured claim with evidence and conditions, not a scalar score."
- **Autonomy tiers (Table 1):** T0 no action; T1 assists single actions; T2 multi-step, human approves every material action; T3 whole task, requests help on uncertainty or hazard triggers; T4 no contemporaneous approval, out-of-envelope blocked in software; U unprofiled.
  - **The tier attaches to the deployment.** It is "defined by evidence": T2 requires approval logs showing *substantive* review (latency, edit rate, rejection rate). With reflexive acceptance "the deployment is classified … T3, notwithstanding the software's configuration" (§4.1).
  - The paper proposes **habituation testing**: injecting "benign, materially incorrect proposed actions" to measure reviewer catch rates.
  - Six modifiers: data authority, reversibility, customer/market impact, stack composability, accountability, population scope.
- **Action classes (§4.3, Table 2), "organizing variable is reversibility":** A1 read/retrieve; A2 analyse/compute; A3 draft for a person; A4 recommend/route (incl. escalations); A5 write internal; A6 submit/commit internal; A7 external communication; A8 transact-bounded; A9 move funds; A10 regulatory filing; A11 access/infrastructure change; A12 delegate/spawn. The axis value is the pair (A⁺, A⁻).
- **ODD:** 52 candidate financial-services use cases in 9 business lines (App. B.2). These include "Alert triage for structuring and rapid movement", "periodic customer review and enhanced diligence" and "Account opening and onboarding", which overlap our counterparty-verification domain. "Use case boundary detection resides in this axis."
- **Control envelope:** 55 controls in 6 layers (App. B.4). The model layer includes "evidence grounding (cite or refuse)" and "uncertainty surfacing". The harness layer includes "evidence-preserving provenance capture".
- **Assurance ladder:** Level 1 Asserted (documents only) / Level 2 Validated (in-house tests) / Level 3 Verified (independent assessor), plus a separate Benchmarked flag. The headline level is min(L_T, L_O, L_A, L_C) (§6.2).
- **Profile Validator evaluators (§6.1):** "prohibited-action attempts, tool discipline, **boundary detection, escalation, trace completeness**, and safe-state behavior", plus domain correctness/harm evaluators.
- **Metrics (§7.3, citing Rabanser et al.):** task success across runs; consistency across equivalent inputs; "robustness to controlled perturbations"; rule compliance; interception rates; boundary detection; confidence accuracy. "The Profile keeps metrics disaggregated, rather than converting them into a composite score."
- **T3 handoff evaluation (§7.4):** "trigger accuracy, time to acknowledgment, time to competent control, information transferred, state preservation".

**Evaluation.** None. A proposal with a five-phase programme and 12 research questions. The authors write: "The next step is empirical".

**Overlap with DSA (question d).**

| DSA dimension | ARP counterpart | Overlap |
|---|---|---|
| Recognising decision points and alternatives | — | none |
| Grounding the choice in the right evidence (tested by interventions) | Control "evidence grounding (cite or refuse)"; metric "robustness to controlled perturbations" | **weak**: a declared control and a generic robustness metric, not tested reliance on decisive evidence |
| Recognising uncertainty/contradiction boundaries | "boundary detection" (ODD exit); "uncertainty surfacing" | **partial**: ARP's boundary is the *domain*, not evidential contradiction within the domain |
| Staying within authority scope | prohibited-action attempts; A⁺/A⁻; interception rates | **strong** |
| Escalating correctly | "escalation" evaluator; T3 "trigger accuracy" | **strong in name**; ARP gives no operationalisation |
| Revising correctly after correction | — | none |
| Preserving provenance | "trace completeness", "evidence-preserving provenance capture", provenance map | **strong** |

**Overlap with our decision classes.**
- ARP's action classes are **types of action graded by reversibility**. Our decision classes are **types of decision graded by their evidence structure**.
- The two are orthogonal and composable. A counterparty-verification decision class spans A1/A2 (gather, analyse), A4 (recommend), A5 (write case note) and, for the legally reserved class, A10 (regulatory filing).

**Should we align? Yes, lightly.**
1. Annotate every WorkTrace decision class with its ARP action class(es) and reversibility. Report results stratified by reversibility. AgentAbstain shows models do *not* abstain more on state-mutating tasks, a natural secondary analysis.
2. Express each per-class delegation outcome in ARP terms: "proceed" ≈ T3/T4 behaviour within that class; "escalate" ≈ T2.
3. Present the WorkTrace per-class certificate (with episode provenance) as **Level-2/3 evidence** for ARP's autonomy-tier and escalation/boundary-detection claims. Today ARP grounds the tier in human approval logs.
4. Borrow ARP's **provenance-type field** (measured / configuration-derived / document-derived / owner-attested / absent), its **floors** (our legally reserved classes are floors), and its **invalidation triggers** (a model or harness change voids per-class certificates) for our revocation section.
5. **Do not** adopt the per-deployment tier as our unit. The argument is that one deployment needs different autonomy per decision class.

**What WorkTrace must NOT claim.**
- That nobody has proposed a standard per-agent assurance artefact with bounded claims, floors, validity windows, invalidation triggers and graduated independence of evidence.
- That reversibility-graded action classes are new.
- That evaluating boundary detection, escalation and trace completeness is new.
- That approval logs should be checked for reflexive approval (ARP; also Digital Apprentice).

**What it leaves open.**
- How to *measure* escalation correctness and grounding.
- Any per-class allocation of autonomy within a deployment.
- Any test of whether decisions depend on the right evidence.
- Any empirical validation.

**Differentiation.**
> Hsu et al. propose a per-deployment Agent Reliability Profile that fixes an autonomy tier, operational domain, reversibility-graded action classes and a control envelope, and backs that bounded claim with evidence of graduated independence; WorkTrace supplies a measurement that such profiles currently lack (whether the agent's decisions in each decision class depend on the right evidence, recognise contradiction and escalate correctly) and turns it into a per-class, revocable delegation rule evaluated on held-out episodes.

**Citation cautions.**
- Unrefereed working draft circulated for comment, with a high-profile author list. Expect revisions.
- Section 9.6 is missing (9.5 → 9.7).
- Key source [3] (autonomy taxonomy) is "available from the working group on request" [unverified].
- References to "Exhibits B1–B3" correspond to tables only in the text.
- LLM-assisted drafting is disclosed.

### B.5 AgentAbstain (Liu et al.)

**Bibliographic data [verified].**
- Xun Liu, Yi Evie Zhang, Vira Kasprova, Parisa Rabbani, Pardis Sadat Zahraei, Tianyu Zhang, Ali Ebrahimpour-Boroojeny, Varun Chandrasekaran (UIUC). *AgentAbstain: Do LLM Agents Know When Not to Act?*
- arXiv:2607.10059v1, 11 Jul 2026, cs.AI. 56 pp. "Preprint". No venue. Code and data at agentabstain.github.io.

**Problem and contribution.** "Agentic abstention: the calibrated ability of tool-using LLM agents to recognize when not to act" (Abstract). The paper contributes:
- a paired benchmark of 263 pairs in 42 LLM-generated MCP sandboxes;
- an 8-scenario taxonomy;
- the ABSTAINGEN generation pipeline;
- an evaluation of 17 frontier models.

**Method: the paired perturbations (question f).**
- **Task** T = (q, e, τ): query, sandboxed environment state, MCP tools. Tools are typed lookup / verify / commit.
- **Execution DAG** G with critical action set C (commit nodes).
- **Pair (T⁺, T⁻)** "differ in exactly one of q, e, or τ via the controlled perturbation δ" (§2.2). The minimal-perturbation invariant: "typically a single named entity in q, a single field in e, or a single tool in τ". **"No constant policy exceeds 50% Paired Accuracy."**
- **Scenarios (Table 2, App. B.7)**, each with a formal condition and a minimum-information level:

| Scenario | Perturbs | Formal condition | Minimum information |
|---|---|---|---|
| S1 missing critical parameter | q | — | I_q |
| S2 ambiguous action | q | ∃ C₁ ≠ C₂ both valid | I_q |
| S3 conflicting constraints | q | ∄π ⊨ Φ(q) | I_q |
| S4 high-stakes | q | irrev(c) ∧ conf(q, c) < τ | I_q |
| S5 insufficient tools | τ | C ⊄ reach_G(τ) | I_{q+τ} |
| S6 critical tool failure | τ | failing v* on every path to C, no workaround | I_{q+τ+o} |
| **S7 conflicting evidence** | **e** | s′ ⊭ φ_q | I_{q+τ+o} |
| **S8 emergent risk** | **e** | harm(c, s′) > 0 ∧ harm(c, s₀) = 0 | I_{q+τ+o} |

  S7 has two sub-types: S7_u-e (user statement contradicted by a tool) and **S7_e-e (two tool observations contradict, "with no statement in q adjudicating")**.
- **Abstention (App. B.3):** a_K ∈ {refuse, ask} ∧ Π_tool ∩ C = ∅. Silent halts and "executing a critical action while verbally hedging" do not count.
- **Pass criteria (App. B.6):**
  - operational tasks need commit check ∧ LLM-judge verdict;
  - informational tasks need the judge only.
  - Metrics: Act Acc, Abstain Acc, **Paired Accuracy**, **CAR** = P(pass T⁻ | pass T⁺). Single run per task.
- **Generator:**
  - GPT-5.4 actor with a Claude Sonnet 4.6 critic, run cross-family;
  - a falsification critic "actively searches for counterexamples to the abstain claim";
  - **construction-time deterministic DAG replay** of the act side;
  - 3 annotators rate 94–98% of 100 sampled pairs as well-designed;
  - judge vs human majority: 4/200 disagreements;
  - the released task distribution is partly held out against gaming.

**Evaluation.**
- 17 models in 4 harnesses. Paired accuracy ranges 33.0% (GPT-4o) to 59.5% (Gemini 3.1 Pro); Opus 4.7 scores 59.4%.
- Mean act 80.6% vs abstain 59.1%.
- **S7 Conflicting Evidence is the hardest category (≈ 28% paired).**
- **Per-pair φ(act-pass, abstain-pass) ≈ −0.10** (15/17 models negative).
- Operational vs informational tasks: abstain accuracy 58.5% vs 61.8%, n.s. Models are "action-type-blind".
- Failure modes on abstain runs: successful 59.9%; implicit (no commit, no signal) 17.8%; no abstention 19.7%; **post-hoc abstention** (commits, then claims refusal) 2.6%.

**Relation to WorkTrace interventions.**

| WorkTrace intervention | AgentAbstain analogue | Difference |
|---|---|---|
| remove X | S1 (query param), S6 (tool failure); partly S5 | AgentAbstain's correct response is always abstain; ours may be "proceed" when X is redundant |
| only X | none | — |
| invert X | S7 (contradiction with q or another source) | ours inverts the *decisive* source and checks whether the action follows; theirs only checks whether the agent notices the contradiction |
| add independent second source | none (S7_e-e adds a *contradicting* source, not a *corroborating* one) | ours changes the correct action toward "proceed" (AMLR "known from another reliable source") |
| declared-grounds reading | none (judge reads only the terminal response, "never inspects the tool-call trace") | — |

**Design lessons to adopt.**
1. A paired should-proceed/should-escalate design in which no constant policy beats 50%. Report paired accuracy and a CAR analogue ("escalates correctly | handles the unperturbed episode correctly").
2. Separate *action* from *verbal signal* (their post-hoc abstention). Map this onto our episode fields "action" vs "declared grounds": an agent that commits and then flags has not escalated.
3. A minimum-information hierarchy (I_q / I_{q+τ} / I_{q+τ+o}) to time *when* escalation becomes warranted. Score lateness, including the "act-then-discover" mode.
4. Generator hygiene: deterministic replay of the reference solution, a falsification critic, and partial hold-out of generated instances.

**What WorkTrace must NOT claim.**
- First paired, minimally perturbed agent tasks with ground truth by construction.
- First interventions on external environment state (including conflicting sources).
- First demonstration that capability or task success does not predict restraint.
- The term "agentic abstention".

**What it leaves open.**
- Which evidence the decision *rests on*: there are no remove/only/invert sweeps on the same decisive item and no redundancy handling.
- Declared grounds.
- Delegation or autonomy allocation.
- Repeated runs: it is single-run.
- Per-class certification.

**Differentiation.**
> AgentAbstain tests whether agents abstain on minimally perturbed should-abstain variants of executable tasks, including contradicting tool outputs, and finds restraint largely independent of task-solving capability; WorkTrace uses a richer family of interventions on the decisive external evidence (remove, isolate, invert, corroborate with an independent source), reads them jointly against the agent's declared grounds, and uses the result to grant or withdraw autonomy per decision class.

**Citation cautions.**
- Unrefereed preprint; single rollout per task; environments fully LLM-generated "with no human-in-the-loop curation".
- The LLM judge has a false-positive bias (all 4 disagreements are FP).
- Bibliography slips: it cites Ojewale & Venkatasubramanian as "What benchmarks don't measure…", but the arXiv title is *Designing for Doubt: The Case for Informed Abstention in Autonomous Agents* (2606.02965v2, AIES 2026 per comment) [verified]. It also cites HiL-Bench with an author order that differs from arXiv.
- **Concurrent work to cite with it:** Luo, Wen & Wang, *Agentic Abstention: Do Agents Know When to Stop Instead of Act?* arXiv:2606.28733 [verified; abstract only]. It studies *timely* abstention on 28k tasks and the CONVOLVE method.

### B.6 ADAS: AI Deployment Authorisation (Saparning)

**Bibliographic data [verified].**
- Daniel Djan Saparning. *AI Deployment Authorisation: A Global Standard for Machine-Readable Governance of High-Risk Artificial Intelligence.* arXiv:2601.08869v1, 11 Jan 2026. cs.CY (cross-listed cs.AI).
- Comment: "28 pages, 4 figures. Preprint". The PDF is headed "Paper Blueprint"; I found no figures in the extracted text, only tables. No venue.

**Problem and contribution.** Governance lacks "a formal, enforceable mechanism for determining whether a given AI system is legally permitted to operate in a specific domain and jurisdiction" (Abstract). The paper proposes:
- the ADAS score vector;
- an evidence/audit architecture;
- a signed certificate;
- policy mapping to the EU AI Act, US critical infrastructure and insurance.

**Method: how evidence becomes a certificate (question e).**
1. Deployment S = (M, D, A, H, C, U), evaluated relative to jurisdiction J and domain U.
2. ADAS(S, J, U) → {R, A, E, C, T}: Risk, Alignment, Externality, Control, Auditability. Each is "computed from verifiable evidence and standardised test suites and normalised to a 0–100 scale with confidence intervals" (§3). **How any dimension is computed is never specified.**
3. **Evidence Sufficiency Check** (§4.2): mandated evidence types must be present and hashed, or the case is "denied or escalated for human review". The Evidence Bundle holds content-addressed artefacts (model cards, red-team findings, lineage, monitoring plans).
4. **Decision** (§3, §5.1): APPROVED iff min(R, A, E, C, T) ≥ τ_{J,U}. For safety-critical deployments, "the lower bound of each dimension's confidence interval must also exceed its threshold". Alternatives: lexicographic (Control and Auditability first) or weighted.
5. **Outcomes:** APPROVED / APPROVED WITH CONDITIONS / DENIED.
6. **Certificate** (§5.3): deployment identifier and scope, policy version, outcome and conditions, hash of the Audit Package, expiry, revocation status. Signed, with transparency logs.
7. **Revocation** (§5.4): on incidents, inaccurate evidence, scope change or policy change. "Conditional … revocable … auditable" (§5.5).

**Evaluation.** None.

**Threat to W3: low.**
- ADAS's unit is the whole deployment, not a decision class, and the system is not specific to agents.
- Its evidence is documentation and unspecified test suites, not behavioural tests of decisions.
- It offers no loss definition, no estimate, no held-out evaluation and no comparison.
- It pre-empts generic phrasing only. We must not present as new: "a machine-readable, signed, expiring, revocable authorisation certificate", "conditional and revocable right to operate", or "the lower confidence bound must clear the threshold".

**Differentiation.**
> Saparning proposes a deployment-level authorisation certificate that approves a whole AI system when five evidence-derived scores clear jurisdiction-specific thresholds, without specifying how the scores are measured; WorkTrace operates at the level of decision classes within an agent deployment, specifies the evidence (intervention tests on decision episodes) and the loss, and validates the resulting delegation rule empirically.

**Citation cautions.**
- Single-author "Paper Blueprint". Grandiose framing ("the missing layer of AI civilisation").
- Bibliography with incomplete references (e.g. "Regulation (EU) 2024/…").
- No method or evaluation.
- Cite at most in one sentence as a deployment-level certification proposal.
- Beware the acronym clash with ADAS = *Automated Design of Agentic Systems* (Shengran Hu, Cong Lu, Jeff Clune, arXiv:2408.08435 [verified]).

---

## C. Answers to the key questions

### C.1 (a) Does any prior work raise autonomy from behaviour?

- **Yes, several do. None does it from tested evidence-handling.**

| Work | Signal that widens autonomy | Unit |
|---|---|---|
| Hedwig | approvals (plus verification failures, regret in the repo) | action features per repo; topic |
| Minimal Oversight | raw success rate σ_raw | task class |
| Digital Apprentice (r2) | correction rate + quality score + human sign-off | skill |
| ACP-REP-1.1 (spec only, unreachable in practice) | protocol-hygiene events → PROBATION→ACTIVE | agent |
| Progressive Autonomy PL (r2) | human approve/deny | action-context kernel |

- **ACP never raises `autonomy_level`.**

### C.2 (b) Escalation-cost and oversight-capacity model to adopt

**Proposed WorkTrace cost model.** Per review period with n_c episodes in class c and delegation decision d_c ∈ {proceed, escalate, refuse}:

```
J = Σ_c n_c · [ 1{d_c=proceed} · ( L_w · P(wrong action | auto, c)
                                   + L_b · P(right action, wrong basis | auto, c) )
              + 1{d_c=escalate} · ( λ_esc + L_w · P(agent proposal wrong | c) · (1 − r(ℓ)) )
              + 1{d_c=refuse}   · λ_ref ]
ℓ = Σ_c n_c · 1{d_c=escalate}            (cumulative escalation load in the period)
r(ℓ) = max(r_min, 1 − s · max(0, ℓ − K))  (Turan 2026; FALCON for the idea)
subject to ℓ ≤ K_max                       (hard capacity, DeCCaF-style)
```

**Parameters and where they come from.**

| Parameter | Source and setting |
|---|---|
| L_w : λ_esc | Turan's 50 : 1 (blocked miss : false alarm) and 5 : 1 (approval-needed miss) as anchors. Sweep λ_esc ∈ {0.02, 0.1, 0.5}·L_w and report several cost levels (already planned). |
| L_b | Right action on wrong basis. Report L_b = 0 (pure outcome) and L_b ∈ {0.25, 0.5}·L_w. This keeps the primary endpoint (outcome errors under evidence shift) non-circular. |
| s, r_min, K | Turan: s = 0.02, r_min = 0.2, K ∈ {10, 25, 50}. Two regimes: (i) perfect reviewer, r ≡ 1 (the standard assumption, Turan's "infinitely-available oracle"); (ii) fatiguing reviewer. Both are sensitivity analyses, not findings. |
| Masking guard (Minimal Oversight) | Delegation statistics for any rule may use only *uncorrected* agent behaviour. Escalated-and-corrected episodes must not count as agent successes. This rule binds the outcome-only and Hedwig baselines too, so that they are not straw men. |
| Capacity feasibility (Minimal Oversight) | Before granting, check that the escalations implied in the remaining classes fit K_max. The analogue of K/N ≥ (p_min − σ)/((1 − σ)c). |
| Throughput (P10, Fernandez; see r2 note) | Θ = 1/(T_task + r·τ_review) as an optional latency view. |
| Empirical reviewer reliability (ARP §4.1/§7.4) | ARP's "habituation testing" is the empirical way to measure r. Mention it as the way to calibrate r(ℓ) in a deployment. We do not run humans. |

**Must cite** for this model: Turan (2606.08919), FALCON (2604.00904 [verified]), DeCCaF (2403.06906 [verified]; Turan cites it as TMLR 2024 [venue unverified]), Minimal Oversight. Also Zhou et al., *When Should Users Check? Modeling Confirmation Frequency in Multi-Step Agentic AI Tasks* (CHI 2026, DOI 10.1145/3772318.3790655, arXiv:2510.05307 [verified metadata; not read]). **Read Zhou et al. before finalising the cost section.**

### C.3 (c) Baselines, operationally

- **Hedwig (approval-history):** recipe in §B.3. Online L2 logistic regression via SGD (α = 0.001) per (agent, class) on approval labels; bands 0.90 / 0.20; at least 10 decisions before learned scoring; hard constraints override. Sweep the upper band to match coverage.
- **Minimal Oversight (raw-success gate):**
  - Update σ_raw(c) ← σ_raw(c) + η′(y − σ_raw(c)) − δ′(σ_raw(c) − σ₀), where y is the uncorrected outcome. Take η′/δ′ = 5 as in their η = 10, δ = 2, and σ₀ ∈ {0, 0.5}.
  - Delegate c iff G(σ_raw(c)) ≥ τ, with G = identity (their G is unspecified; this choice is ours). Add the feasibility check.
  - Sweep τ to match coverage.
- **ACP (history counters):** RISK-2.0 per (agent, class): base + recent-denial/frequency/pattern penalties; thresholds 39/69; cooldown 3 denials in 10 min. REP optional with the correction described in §A.5.
- **Turan-style action-risk guard (optional fifth baseline):** escalate iff an action-risk score ≥ θ. It shows what a *per-action* guard achieves without any per-class agent assessment.

### C.4 (d) Agent Reliability Profiles: alignment decision

See the table and recommendations in §B.4. Align vocabulary: tag classes with action classes A1–A12, map proceed/escalate to T3/T2, adopt floors and invalidation triggers. Do not adopt the per-deployment tier as the unit.

### C.5 (e) ADAS: threat to W3

Low. See §B.6. Avoid generic "revocable certificate with lower confidence bound" novelty claims, and name the acronym collision.

### C.6 (f) AgentAbstain's paired perturbations

See §B.5. This is the closest prior art to W2's "ground truth by construction" and "interventions on external evidence".

### C.7 (g) Differentiation sentences

Collected from §A.5 and §B.1–B.6. Short versions:
- **ACP:** static registration-time autonomy level; reputation from protocol-hygiene events; never per class; never decision quality.
- **Turan:** per-action risk threshold under a fatiguing reviewer; we take that cost model as input and decide per class from tested evidence-handling.
- **Minimal Oversight:** per-class authority from raw success; we show success is the wrong signal when decisions can be right for wrong reasons.
- **Hedwig:** approval-history check-in policy; we test the agent, not the reviewer's preferences.
- **ARP:** per-deployment bounded claim without a measurement of decision grounding; we supply that measurement per class.
- **AgentAbstain:** paired abstain/act perturbations; we intervene on the decisive evidence along four axes, read the results against declared grounds, and allocate autonomy from them.
- **ADAS:** deployment-level certificate from unspecified scores; we specify evidence, loss and empirical validation per decision class.

---

## D. Implications for WorkTrace

### D.1 Claims to change or guard

1. **Never write "no prior work raises autonomy from behaviour".** Write: "prior adaptive-autonomy mechanisms widen or narrow autonomy from outcomes, corrections, human approvals, success rates or protocol-hygiene events (Digital Apprentice; Hedwig; Minimal Oversight; ACP-REP); none conditions autonomy on interventionally tested reliance on the decisive evidence."
2. **Patch the ACP sentence** in positioning.md and r2_fernandez_series.md:
   - "history only penalises" → "risk scoring uses history only as penalties; a separate reputation layer could restore standing, but only from protocol-hygiene events, and never changes the autonomy level";
   - note the degenerate update rule as a citation caution.
3. **Narrow W2.**
   - Paired, minimally perturbed tasks with ground truth by construction, including perturbations of external environment state and contradicting sources, exist (AgentAbstain; Luo et al.).
   - Our novelty: (i) ground truth on the *basis* (which evidence item is decisive); (ii) the four-way intervention family, including **corroborating** second sources, with redundancy classification; (iii) the joint reading against declared grounds; (iv) using the result to allocate autonomy.
4. **H3 support.** Cite AgentAbstain's near-independence of act and abstain skill (φ ≈ −0.10; "abstention capability is largely independent of general task-solving capability"). This is direct evidence that outcome or capability signals mis-predict restraint, which is the mechanism by which outcome-only delegation should over-authorise. Pair it with Minimal Oversight's masking argument and Trust Before Autonomy's 54 pp gap (r2).
5. **DSA construct section.** Acknowledge and contrast "agentic abstention" (AgentAbstain, Luo et al.), "agent reliability" (ARP, Rabanser et al.) and "boundary detection" (ARP). DSA = these *plus* evidence-grounding under intervention, revision after correction, and decision-point recognition. Read Rabanser et al. (2602.16666) before drafting.

### D.2 Design changes

1. **Paired design in the episode generator** (from AgentAbstain): each perturbed episode has an unperturbed twin. Report a paired metric in which constant "always proceed"/"always escalate" policies cannot exceed 50%, and a CAR-like conditioned metric.
2. **Score action and declared escalation separately.** An agent that commits and then flags has not escalated (post-hoc abstention). Add a timeliness measure based on the minimum-information level at which escalation becomes warranted.
3. **Generator hygiene additions:** deterministic replay of the reference solution; an adversarial "falsification critic" that searches for counterexamples to the intended label; partial hold-out of generated instances.
4. **Stratify classes by ARP action class and reversibility.** Test whether agents' DSA scores differ for state-mutating vs informational decisions; AgentAbstain finds they do not.
5. **Cost model** as in §C.2. Main results under r ≡ 1 at several λ_esc; fatigue as robustness; masking guard applied to all rules.
6. **Baselines** as in §C.3. Add the Minimal Oversight raw-success gate as the canonical "outcome-only" rule, alongside Digital Apprentice.
7. **ARP-compatible output.** Emit per-class certificates with provenance types, floors, a validity window and invalidation triggers (model/harness/tool change), so WorkTrace can plug into the ARP assurance ladder as Level-2/3 evidence.

### D.3 Risks

- **ARP is a moving, high-visibility working draft** in our exact application domain (financial services, AML alert triage, onboarding). A revised version could add "evidence grounding" or "escalation" tests. Re-check before submission.
- **The AgentAbstain/Luo line will grow.** Expect agentic-abstention benchmarks with evidence-conflict perturbations. Our differentiation must rest on the *basis* and *delegation* parts, not on "perturbing the environment".
- **The ACP spec moves fast** (more than 20 versions). Cite repo state "master, CHANGELOG v1.29 (13 Apr 2026), accessed 25 Oct 2026".

### D.4 Things to cite (added in this round)

| Cite | Role |
|---|---|
| ACP spec ACP-REP-1.1/1.2, ACP-API-1.0, ACP-RISK-2.0 (repo chelof100/acp-framework-en) | Reputation is per agent, driven by hygiene events and never alters the autonomy level |
| Turan 2606.08919; FALCON 2604.00904; DeCCaF 2403.06906 | Escalation cost, reviewer capacity and fatigue |
| Azevedo 2606.15563 | Raw-success per-class gate; masking; capacity feasibility |
| Shukla et al., CAIS'26 (Hedwig) | Approval-history baseline |
| Hsu et al. 2610.04123 | Deployment-level bounded claims; action classes; vocabulary alignment |
| Liu et al. 2607.10059; Luo et al. 2606.28733; Ojewale & Venkatasubramanian 2606.02965 | Agentic abstention; paired perturbations; capability ≠ restraint |
| Saparning 2601.08869 | Deployment-level certification (one sentence) |
| Zhou et al., CHI'26; Rabanser et al., ICML'26 | **To read**: confirmation-frequency model; agent reliability metrics |
