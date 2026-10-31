# R3: The "earned autonomy" family: Trust Before Autonomy, Earned Authority, Sovereign-OS, Digital Apprentice

Round 3 note, 25 Oct 2026. Written after reading `positioning.md` v2 and the round-2 notes on these works (`r2_learned_permissions.md` §5, `r2_novelty_sweep.md` §3, `r2_mas_delegation_theory.md` §2.19). This note replaces their partial readings.

## 0. What was read

| Work | Read | Source |
|---|---|---|
| Trust Before Autonomy (2610.18789v1) | **Full text**: §§1–6, Tables 1–2, Figs 1–2, appendix A–D (meta-analysis protocol, transcriptions, insights I1–I10, limitations). | arXiv PDF + HTML (tables cross-checked in HTML) |
| Earned Authority (2607.23586v1) | **Full text**: §§I–IX and the whole appendix, including Defs 1–13, Props 1–7, Thms 1–3, Remarks 1–11 and the proof of Thm 3. | arXiv PDF |
| Sovereign-OS (2603.14011v1) | **Full text** (4 pp. + appendices A–C). Also read the **public code**: `sovereign_os/agents/auth.py`, plus the permission, audit and overrun paths in `governance/engine.py` and `auditor/review_engine.py`. Source: github.com/Justin0504/Sovereign-OS, HEAD b9c9e5e, committed 2026-10-25. It was shallow-cloned into the scratchpad only to read the code; no git command touched the paper repository. | arXiv PDF; GitHub |
| Digital Apprentice (2606.04321v1) | **Full text** (5 pp.), with Table 1 and Eqs 1–5 cross-checked in HTML. | arXiv PDF + HTML |

## 1. Answers to the key questions (summary)

**(a) Trust Before Autonomy (TBA).**
- **Evidence validity is not interventional.** TBA defines it as "the share of claims whose cited evidence, when re-executed, reproduces the claim within the service's tolerance" (§3, P3). The cited pipeline is re-run deterministically, without the agent. This checks that the claim is reproducible from what the agent cites. It does not check whether the agent's decision depends on that evidence. Nothing perturbs the evidence. In DSA terms this is the *provenance* component, not the *grounding* component.
- **Unanswerable variants are a special case of "remove X", not its equivalent.** They are built from physical causes that make the data unable to answer: cloud or smoke cover, no post-event acquisition, resolution too coarse, a sensor that cannot observe the quantity, stale data, an ill-defined class (§3 P2, §5). Three things are fixed:
  - the correct response is always *abstain*;
  - the unit is the task variant;
  - the score is abstention F1 and selective risk–coverage.

  TBA has no pairing with the agent's declared grounds, no "only X", "invert X" or "second source" condition, no redundancy control, and no case where the correct response to a removal is a *different action* or the *same action* (because a redundant source exists). TBA also proposes these variants without building any.
- **Unit.** The unit is a rung per task type (example tasks: scene search, draft flood mask, checkpointed workflow, release-ready map, cloud screening; Fig. 2). It is not a decision class inside an episode.
- **Certification and experiment.** There is no formal certification: "Thresholds are set by the operational user; the protocol fixes the structure, not the numbers" (Tab. 2 caption). The only estimator given is pass^k = C(c,k)/C(n,k). There is no experiment of its own; the evidence is a re-analysis of 12 published benchmarks' tables.
- **Named constructs.** TBA names three "trust properties": P1 Reliability, P2 Epistemic honesty, P3 Verifiability. P2 and P3 overlap two or three of DSA's seven components (uncertainty/contradiction boundaries, escalation, provenance). They are presented as properties to measure, not as a capability construct with a validity claim. No construct named "decision-structured agency", "decision quality" or "grounded agency" appears.

**(b) Earned Authority (EA).**
- **Argument.** A grant fixes an immutable effect ceiling B. Below B, authority may contract freely and expand only under an evidence relation ⊢. No runtime evidence can raise B.
- **Formal results.**
  - Corollary 1 / Prop. 6: the effect bound is Scope(L_max) for *any* ⊢, including a compromised one.
  - Prop. 4: if the agent can itself produce the qualifying evidence, the evidence gate gives no security bound below the ceiling.
  - Prop. 5: a gate tightens the bound only through a premise "outside the agent's causal reach" ("an external attestation, a human countersignature, … or an evaluation the agent cannot run on itself", Remark 2).
- **What this means for WorkTrace.** Widening autonomy (escalate → proceed for a class) *is* EA's "gated ascent beneath the ceiling", which EA explicitly allows. So there is no contradiction, as long as WorkTrace:
  - fixes the ceiling to the human-issued permissions in the episode;
  - frames the DSA rule as a **reliability allocation, not a security bound**;
  - binds certificates to the agent configuration (EA's transition envelope);
  - adds decay (EA Remark 5).

  See §7.

**(c) Baseline definitions.**
- Sovereign-OS is a scalar additive score: +5 per audit pass, −15 per fail, −10 per overrun; start 50, clamp [0,100]; capability thresholds 10/40/50/60/80. The audit is an LLM judge, pass if score ≥ 0.50.
- Digital Apprentice uses non-overlapping windows of N outputs per skill. Promotion requires ρ(W_t) < ρ(W_{t−3}), ρ ≤ τ_corr, an optional scorer gate, and human authorisation. Demotion is automatic when ρ > ρ_demote or OOD uncertainty > u_max. N, τ_corr, τ, p, ρ_demote and u_max are **not given numerically**.
- Implementable specifications are in §6.

**(d) Differentiation sentences.** In §§2–5 and collected in §8.

**Novelty threat level.** Low for W2. Low to moderate for W3 and DSA: TBA prescribes a gated, revocable, per-task autonomy ladder with abstention tests and risk–coverage, and names "epistemic honesty" and "verifiability". These must be cited as conceptual precedents. None of the four papers runs an interventional evidence test or evaluates a promotion rule against alternatives.

---

## 2. Trust Before Autonomy

**Bibliographic data.** Georgios Angelidis, Aggelos Psiris, Spyridon Evangelatos, Thomas Lagkas, Panagiotis Sarigiannidis, Iraklis Varlamis, Georgios Th. Papadopoulos.
- Title: *Trust Before Autonomy: Rethinking Agentic Remote Sensing for Crisis Response*. arXiv:2610.18789v1 [cs.CV], 13 Oct 2026. **[verified]** (arXiv API).
- Affiliations: Harokopio University of Athens; Netcompany-Intrasoft; Democritus University of Thrace; University of Western Macedonia.
- Venue: none stated. The format is a 5-page CVF-style position paper plus appendix. Only v1 exists.

**Problem & contribution.** EO agent benchmarks measure capability; crisis response needs to know "when can its answer be relied on, and how much of the decision may it take alone?" (§1). Position: "autonomy should be earned, not assumed … granted autonomy in proportion to demonstrated reliability, epistemic honesty and verifiability" (Abstract). Contributions:
1. A meta-analysis of 12 agentic RS/EO/GIS benchmarks (trust-coverage audit plus re-analysis of their tables).
2. Three trust properties with measurable definitions.
3. An autonomy ladder L1–L5, adapted from the user roles of Feng et al. 2025.
4. A staged readiness protocol R1–R5.

Conclusion: "current evidence justifies assistive roles only" (L1–L2).

**Method.**
- **Trust properties (§3).**
  - P1 Reliability: pass^k over repeated runs plus accuracy on held-out *events* rather than images.
  - P2 Epistemic honesty: "The agent abstains when the data cannot answer and reports uncertainty that survives the tool chain". It is scored with selective risk–coverage and abstention F1 on unanswerable variants, with conformal segmentation propagated through the chain and calibration error.
  - P3 Verifiability: every claim carries its evidence (scene IDs, dates, bands, tools, parameters, intermediate masks). Evidence validity = share of claims reproduced on re-execution of the cited evidence.
- **Ladder (§4, Fig. 2).**
  - L1 Operator: look-ups; "must declare when no suitable scene exists".
  - L2 Collaborator: drafts with an uncertainty map.
  - L3 Consultant: checkpointed workflow; needs pass^k on replayed events and useful abstention.
  - L4 Approver: release-ready product for human approval; needs shadow-mode agreement and high evidence validity.
  - L5 Observer: acts without approval; only low-consequence sub-tasks such as cloud screening.
- **Readiness protocol (§5, Tab. 2).** Each gate lists its setting, what is measured, and the condition to pass.

  | Gate | Setting | Measured | Pass condition |
  |---|---|---|---|
  | R1 Benchmark | Curated tasks with unanswerable variants, k = 5 repeats | Accuracy, pass^k, abstention F1, risk–coverage, calibration error, $ per correct answer | "Stable pass^k and abstention above user threshold" |
  | R2 Replay | Archived emergency activations | Agreement with reference, evidence validity, time to product | "Within the service's QC tolerance" |
  | R3 Shadow | Live events, nothing released | Agreement with analysts, useful-abstention rate, analyst time saved | "Sustained across event types" |
  | R4 Supervised | Outputs enter QC | Rejection rate at QC, correction effort | "Low rejection over a set period" |
  | R5 Conditional | Low-consequence sub-tasks only | Continuous monitoring, drift | "Revoked on any drift" |

  "an agent is promoted one rung … only after passing the corresponding gate … and demoted on failure" (§5).

**Evaluation.** There is no experiment of its own. The meta-analysis re-reads published tables; only within-paper contrasts are used, and Spearman ρ over 8–13 models is descriptive. Numbers useful to WorkTrace:
- **F2.** Task "success" exceeds tool-call correctness by 8.5–54.3 pp on identical queries (Geo-OLM). ThinkGeo GPT-4o tool accuracy is 67.7% against 9.8% answer accuracy.
- **F3.** "Grounding, not planning, is the bottleneck". Gold tool order gives +25.6–28.9 pp exact match but only +1.1–4.4 pp final accuracy (DORA). Spatial-Agent traces 79.4% of failures to faulty API data or mismatched search results. Fetching context through map APIs costs all 11 MapEval agents accuracy (mean −16.5 pp).
- **F5.** Capability does not predict abstention: ρ = −0.25, 0.33, 0.50, all n.s. (GeoBenchX, GeoNatureAgent, MapEval-API). Reflexion raises coverage but not precision (0.72→0.71).
- **F1.** 1/12 benchmarks repeat runs, 3/12 have unanswerable tasks, 0/12 measure calibration.

**What it covers that WorkTrace must NOT claim.**
- "Autonomy is earned / granted by rung, not by leaderboard".
- A per-task, gated, demotable and revocable autonomy ladder with explicit evidence per rung.
- Using **abstention on unanswerable variants** and **selective risk–coverage** as a gate for autonomy.
- Re-executing cited evidence as a deterministic verifiability check.
- Replay of archived real cases before live use, then shadow mode.
- The empirical point that completion is not correctness and that capability does not predict abstention.

**What it leaves open that WorkTrace addresses.**
1. Any **interventional** test of whether a decision depends on the right external evidence. Evidence validity re-runs the cited pipeline *without the agent*. Unanswerable variants test only the abstention response.
2. Redundancy: a correct "same action after removal" when a second source exists; the independent-second-source condition; joint reading against declared grounds.
3. A unit finer than the task, namely decision classes within multi-step episodes.
4. Any numbers: certification, finite-sample control, matched-coverage comparison of gating rules. TBA leaves thresholds to the user.
5. Any execution. "No agent has formally passed even gate R1" because no benchmark reports both pass^k and abstention (§4).

**Draft differentiation sentence.** "Angelidis et al. (2026) argue that crisis-EO agents should climb an autonomy ladder only through gates on repeated-run reliability, abstention on unanswerable task variants, risk–coverage and the reproducibility of cited evidence, but they leave thresholds to operators and run none of these gates; WorkTrace instead intervenes on the external evidence behind individual decisions (remove, only, invert, independent second source), with the correct response known by construction and read jointly against the agent's declared grounds, and it evaluates the resulting per-decision-class rule on held-out episodes against outcome-, approval-, counter- and confidence-based rules."

Short form for "unanswerable variants": "TBA's unanswerable variants are the special case of our *remove X* in which X is the only decisive evidence and the correct response is to abstain; WorkTrace's generator also produces removals whose correct response is a different action or the same action via an independent source."

**Citation cautions.**
- An arXiv preprint (v1, 13 days old) with no stated venue.
- A position paper in a different domain (EO/crisis); all quantitative statements are re-analyses of others' tables with small n.
- The authors disclose that Claude was used to extract values and compute statistics.
- Cite it as a *concurrent position*, not as evidence. Do not quote its correlations as significant: only F2/F3-type contrasts are robust.
- It uses Feng et al.'s levels: K. J. Kevin Feng, David W. McDonald, Amy X. Zhang, *Levels of Autonomy for AI Agents*, arXiv:2506.12469, 2025 **[verified]**.
- Its abstention scoring cites Wen et al., *Know Your Limits: A Survey of Abstention in Large Language Models*, TACL 13:529–556, 2025, doi:10.1162/tacl_a_00754 **[verified]**.

---

## 3. Earned Authority under a Fixed Ceiling

**Bibliographic data.** Zhaoxi Zhang (University of Technology Sydney), Xiaomei Zhang (Griffith University). *Are You Still the Agent I Authorized? Earned Authority under a Fixed Ceiling for Evolving Agents*. arXiv:2607.23586v1 [cs.AI], 26 Jul 2026. **[verified]** (arXiv API). No venue or comment.

**Problem & contribution.** Self-evolving agents change memory, skills, tools, workflow, delegation and task phase while a grant is live. The paper asks three questions (§I):
1. "Did the agent or task change in a way relevant to this grant?" (continuity)
2. "If the grant remains valid, what authority should be active now?" (allocation)
3. "What authority can no runtime evidence ever exceed?" (security boundary)

Contributions:
- authorization continuity as a grant-relative transition-validity guard;
- "conditional authority beneath an immutable ceiling: descent is free, ascent is evidence-gated, and no runtime evidence can move the user-issued boundary";
- a non-amplification theorem;
- six mutation classes (control state, capability, delegation, task/phase, trust context, enforcement; Table I).

Central normative claim (§I): "A system may condition authority on demonstrated performance only if it also fixes a bound that no performance can move."

**Method (formal model).**
- **Grant and lease.** A grant fixes a ceiling B (= Scope(L_max)), an initial active authority P₀ ⊆ B, and a transition envelope M of admissible mutation labels (§V-A; Defs 1, 5). A lease is L = ⟨C_G; goal g, phase p, resources R, effect types E, budget τ⟩, with a componentwise authority order ⪯ forming a meet-semilattice (Def. 2, Prop. 1).
- **Clamp.** P_t = P_t^prop ∩ B (Eq. 2; structured form L_t = L_t^prop ⊓ L_max, Eq. 11). Descent (a proposal ⪯ L_{t−1}) is admitted unconditionally. Every other proposal, including an incomparable one, needs Evid(t) ⊢ L_t^prop (Def. 5). "Only a new user grant can replace B."
- **Envelope.** If any mutation label since the grant lies outside M, the grant is *suspended* before the next protected action, even if effects stay below B (Fig. 2: admit / clamp / suspend). Envelope and ceiling are independent guards (Remark 8). The envelope must be grant-fixed and not float (Remark 7).
- **Authority need** = the family of effect sets under which some completing plan exists (Def. 4). Prop. 3: need can rise, fall or become incomparable under mutation, and can change on a **phase change alone** with a bit-identical manifest.
- **Escalation closure and gate-dependent bound** (Defs 6–7, Thm 2). Reach(L_max, L₀, ⊢) is the union of scopes in the least downward-closed set closed under realizable evidence. Two results:
  - Prop. 4: if ⊢ is "unconditionally realizable", then Reach = Scope(L_max).
  - Remark 1: this is "plausible for gates based only on evidence that the session can itself realize, such as some task outcomes, test records, declared effect manifests, or execution history".
- **Prop. 5 / Remark 2 (design rule).** "A gate can support a security bound below the ceiling only through premises that the session cannot itself realize." Examples: "an external attestation, a human countersignature, a wall-clock or calendar condition, or an evaluation the agent cannot run on itself".
- **Remark 4.** Gating still "can reduce expected exposure and non-adversarial blast radius, lower prompt cost, and provide an auditable authority trajectory. Ceiling occupancy is consequently a utility measure."
- **§B4.** The evidence rule "need not be adversarially robust": a fully compromised evidence channel only raises L_t to L_max. Hence it "may use signals that would be unacceptable as security boundaries, including test pass rates or historical error rates". The two questions are separated: "will this agent mishandle the authority is answered by evidence, and what is the most this agent could do if that evidence is wrong is answered by the ceiling."
- **Def. 8 / Prop. 6 (separation obligation).** Every grant fixes L_max such that no input to ⊢ can raise it. A ladder that lets evidence advance the bound L(1) ⪯ … ⪯ L(K) has guaranteed bound Scope(L(K)), "not the stage the agent currently occupies but the highest stage its own conduct can reach".
- **Remark 5.** Without decay, "L_t drifts upward to L_max and stays there". A practical instantiation "needs an explicit decay rule, for example dropping any component of L_t not exercised within k steps or since the last phase boundary".
- **Non-amplification.** Thm 1 (compact form) and Thm 3 (structured form, proved by induction under A1 complete mediation, A2 closure-sound monitor view, A3 sound admission, A4 attenuating delegation, A5 monitor integrity, and single-lease attribution). Prop. 7 shows A2 cannot be dropped. Theorems bound atomic effects, not information flow (Remark 11). Goal and phase validity relies on a sound semantic oracle Ω (Assumption 1), which EA says empirical tests should avoid by fixing goals and phases in advance.
- **§VII-a, the critique of "earned autonomy".** "Our objection is not to gradual allocation beneath a limit. It is to allowing performance evidence to raise the limit itself. … a security claim below B additionally needs an external premise such as an independent audit, authorized countersignature, or evaluation the agent cannot run on itself. The ladder must also terminate beneath a boundary that no rung can move." Table II lists "Earned-autonomy ladder: performance evidence may raise the terminal boundary → no fixed ceiling remains unless the ladder terminates below one."

**Evaluation.** None. §VIII proposes metrics for a future study: grant persistence rate, post-mutation unauthorized-effect rate, false invalidation rate, interaction cost.

**What it covers that WorkTrace must NOT claim.**
- The fixed-ceiling / free-descent / gated-ascent structure.
- Separating reliability allocation from the security bound.
- The result that self-realizable evidence (outcomes, tests, histories) cannot tighten the adversarial bound.
- Invalidating grants on agent or context mutation.
- Phase-dependent authority.

WorkTrace must not present "the ceiling" or "revocation on drift" as its own ideas.

**What it leaves open that WorkTrace addresses.**
- EA explicitly defers *which signals* should drive ⊢: "That question requires future measurement of which signals predict safe handling at which scope and with what decay" (Appendix, open problems b).
- That is exactly H3. WorkTrace supplies a concrete ⊢: a per-decision-class DSA certificate from evaluator-run interventions on held-out generated episodes. It also gives an empirical comparison of candidate ⊢ relations (outcome, approval, counter, confidence, DSA) by their effect on outcome errors at matched coverage.
- EA has no empirical component.

**Draft differentiation sentence.** "Zhang and Zhang (2026) show that evidence about an agent may allocate authority only beneath a ceiling that no runtime evidence can move, and leave open which signals should drive that allocation; WorkTrace adopts the ceiling (the human-issued permissions of each episode), treats its delegation rule as a reliability allocation beneath it, and supplies and tests one such signal: an evaluator-run, interventional test of the agent's behaviour towards external evidence, certified per decision class."

**Citation cautions.**
- An arXiv preprint, v1, unreviewed, by a doctoral student and a co-author.
- The formal results are elementary set-inclusion arguments; they are sound as stated but do not need heavy weight.
- Its "earned autonomy" targets are practitioner blogs: AWS, KnowBe4, CSA ×2 (refs [31]–[34]), not Digital Apprentice or TBA.
- Cite it for the separation obligation (Def. 8 / Prop. 6) and for the design rule on non-self-realizable premises (Remark 2).

---

## 4. Sovereign-OS

**Bibliographic data.** Aojie Yuan, Haiyue Zhang, Ziyi Wang, Yue Zhao (University of Southern California; University of Maryland). *Sovereign-OS: A Charter-Governed Operating System for Autonomous AI Agents with Verifiable Fiscal Discipline*. arXiv:2603.14011v1 [cs.CR], 14 Mar 2026. Comment: "4 pages, 2 figures, 2 tables, demo paper". **[verified]** (arXiv API). Venue not stated. Code (MIT): github.com/Justin0504/Sovereign-OS.

**Problem & contribution.** Agent frameworks orchestrate but do not govern: no fiscal constraints, no earned permissions, no tamper-evident audit. Four contributions:
1. A YAML Charter: mission, competencies, fiscal boundaries, KPIs with verification prompts.
2. A CFO/Treasury: balance reserve, daily burn cap, margin floor 0.35, plus an auction.
3. "**Earned-autonomy permissions.** We implement a TrustScore model (SovereignAuth) with asymmetric updates (+5 success, −15 failure) and tiered capability thresholds" (§1).
4. SHA-256 proof hashes on audit reports and an append-only ledger.

**Method (permission rule, paper version).**
- **TrustScore (§3.1).** s ∈ [0,100] per agent, base 50.
- **Thresholds (Table 1).** A capability is granted iff s ≥ θ.

  | Capability | θ |
  |---|---|
  | READ_FILES | 10 |
  | WRITE_FILES | 40 |
  | CALL_EXTERNAL_API | 50 |
  | EXECUTE_SHELL | 60 |
  | SPEND_USD | 80 |

- **Updates (§3.2).** +5 per audit success (cap 100), −15 per failure (floor 0), −10 per budget overrun. "an agent starting at score 50 … requires 2 consecutive audit successes to unlock shell access (50→55→60) and 6 to unlock spending (50→80). A single audit failure from score 50 drops the agent to 35, revoking write-file access."
- **Audit (§2.5).** A judge LLM (default GPT-4o) scores each output 0–1 against the KPI verification prompt; a score ≥ 0.50 passes.
- **Enforcement.** Permission is checked before the task runs. On denial it raises `PermissionDeniedError` and the task fails; there is no escalation path.
- **Auction utility.** U = (confidence/cost) × P × TrustScore/100, with P = 1.5 for high-priority tasks and 1.0 otherwise. This is inferred from the worked example U = 0.7/4 × 1.0 × 0.55 = 0.096; the printed formula is garbled in the PDF.
- **No window, no class.** The rule has no windowing, no statistics, and no per-class structure in the paper: one scalar per agent gates all capabilities.

**Code at HEAD (2026-10-25) differs from the paper.** Use this only as a variant.
- Quality-scaled deltas: a pass gives round(5·score); a fail gives round(−15·(1−score)).
- **Per-(agent, category) trust**, seeded from global trust.
- A graduated autonomous spend ceiling, linear from $1 at s = 80 to $50 at s = 100.
- Just-in-time task-scoped capability leases.
- Overrun = actual cost > 1.25 × estimate.
- A value-aware minimum audit score.
- Optional self-repair retries before the audit result is recorded.

**Evaluation.**
- 30 synthetic fiscal scenarios: 100% blocked.
- 200 "trust-escalation missions" over agents with "consistently successful, mixed, and frequently failing" profiles: "94% correct permission gating". Errors are said to occur at threshold boundaries where the pending audit was not yet recorded.
- 1,200+ audit reports: zero hash mismatches.

There are no baselines, no ground truth independent of the judge, and no measure of whether granted autonomy reduced errors.

**What it covers that WorkTrace must NOT claim.** The term "earned-autonomy permissions". A dynamic, revocable, threshold-tiered permission system driven by audited outcomes. Tamper-evident audit records.

**What it leaves open.**
- The signal is LLM-judged *output quality*; nothing about the basis of decisions.
- There is no per-decision-class unit (paper version), no statistical guarantee, no evaluation of the rule's effect on errors, and no ceiling separate from the score: SPEND_USD is reachable by score alone, which is exactly EA's Table II "earned-autonomy ladder".

**Draft differentiation sentence.** "Sovereign-OS unlocks capability tiers from a single TrustScore updated by +5/−15 after each LLM-judged audit of task output, which in steady state grants a tier whenever the audit pass rate stays above roughly 75–80%, whatever evidence the outputs rested on; WorkTrace implements it as an outcome-based baseline and replaces its signal with interventional tests of evidence handling per decision class."

**Citation cautions.**
- A 4-page demo paper, not peer-reviewed as far as is known.
- "94% correct permission gating" is measured against the system's own rule, not against any notion of a correct grant.
- Internal inconsistency: Fig. 8's caption says the "TrustScore drops from 55 to 35", which does not match a single −15 (55 → 40).
- The code has evolved far beyond the paper. Cite the paper's rule (v1) for the baseline and state which version is implemented.

---

## 5. The Digital Apprentice

**Bibliographic data.** Travis Weber, Rohit Taneja (Pheo Inc). *The Digital Apprentice: A Framework for Human-Directed Agentic AI Development* (in-paper subtitle "Earned Autonomy Through Observational Learning and Inference-Time Decision Memory"). arXiv:2606.04321v1 [cs.AI], 3 Jun 2026. Comment: "Submitted to ACM AI Leadership Summit 2026, Visionary Papers Track. 5 pages, 2 figures". **[verified]** (arXiv API). Industry authors; not peer-reviewed as far as is known.

**Problem & contribution.** "autonomy is earned, not assumed" (Abstract). Taxonomies describe levels; "our contribution is the machinery for moving between levels: what evidence justifies an increase in autonomy, who must authorize it, and how the system detects when autonomy should be withdrawn" (§1). The system pairs the framework with ADAPT, an inference-time control plane covering multi-policy inference, a six-dimension quality rubric, preference emission from corrections, and drift-triggered policy switching.

**Method (graduation rule, §2).**
- **Tiers.** Per-skill finite-state machine (Table 1):

  | Tier | What the agent may do | Human role / effects |
  |---|---|---|
  | Pre-L0 | Observe-only | — |
  | L0 Sandbox | Isolated drafts | Supervisor reviews 100% of outputs; "no execution" |
  | L1 Draft | Candidate outputs routed toward execution | Endorser approves before external effects |
  | L2 Autonomous | Executes independently under continuous monitoring | Delegator intervenes on exceptions |

  "The agent cannot promote itself."
- **Entry.** Pre-L0 → L0 requires only human authorisation after an observation period of N sessions.
- **Windows.** W_t = the t-th window of N consecutive outputs for one skill. Promotion uses non-overlapping windows; rolling windows may be used for monitoring.
- **Correction rate.** c(x) = 1 if output x needed a human correction; ρ(W) = mean c (Eq. 1).
- **Scorer gate Q1** (if a validated scorer Q exists): (1/|W|) Σ 1[Q(x) ≥ τ] ≥ p (Eq. 2).
- **Promotion** (Eq. 3): Graduate(L_i → L_{i+1}) ⇔ (C1 ∧ C2) ∧ (¬SCORER ∨ Q1) ∧ (H_auth = 1), where:
  - C1 is ρ(W_t) < ρ(W_{t−k}) with k = 3;
  - C2 is ρ(W_t) ≤ τ_corr;
  - H_auth is a recorded human authorisation.
- **Demotion.** Automatic "when ρ(W) > ρ_demote or out-of-distribution uncertainty exceeds u_max", rate-based to avoid oscillation. "Re-escalation requires satisfying Eq. 3 again with new H_auth."
- **Complacency.** Explicitly named: "a low correction rate can indicate either genuine competence or a reviewer who has stopped checking carefully". Reviewer engagement is "a monitored quantity"; §6 recommends "periodic seeded checks".

**Evaluation.**
- A proof-of-concept on one open corpus: 40–60 prompts per arm, a Qwen generator, and a Gemma LLM judge on the six-dimension rubric.
- Triage-stage means: 0.717 (corpus RAG) → 0.957 (after onboarding); under drift 0.930 → 0.957 after switching policy.
- No CIs, no inter-rater agreement, no significance tests.
- **The graduation rule is never run or evaluated.**

**What it covers that WorkTrace must NOT claim.**
- Per-skill (≈ per-class) autonomy tiers.
- Explicit evidence-gated promotion with human authorisation and automatic asymmetric demotion.
- The "agent cannot promote itself" principle.
- Naming automation complacency as a threat to correction-based gates.

Its rubric has a "Grounding" dimension ("Uses approved source concepts without fabrication"), scored by an LLM judge on outputs, so WorkTrace should not claim to be the first to rate "grounding" in the context of earned autonomy. The claim is the *interventional* test.

**What it leaves open.**
- The signal is human correction rate plus judge quality (outcome and approval).
- The thresholds have no numerical values.
- C1 has a corner case (below).
- At L2 the correction rate is censored, because humans see only exceptions.
- There is no evaluation of the rule and no held-out or shifted test.

**Draft differentiation sentence.** "The Digital Apprentice promotes a skill one autonomy tier when its human-correction rate over non-overlapping windows has fallen below a threshold and below its value three windows earlier, optionally with a judge-quality gate, and a human signs off; WorkTrace replaces that correction signal, which the authors themselves note is confounded by reviewer complacency, with evaluator-run interventions on external evidence, and evaluates both rules on the same held-out, evidence-shifted episodes."

**Citation cautions.**
- A 5-page visionary-track submission from a company that sells the control plane.
- The pilot measures generation quality, not autonomy decisions.
- Cite it for the rule's *shape* only.
- It cites Parasuraman & Manzey, *Complacency and Bias in Human Use of Automation: An Attentional Integration*, Human Factors 52(3):381–410, 2010, doi:10.1177/0018720810376055 **[verified]**, which is worth citing directly for the complacency argument against approval-based rules.

---

## 6. Baselines: implementable specifications

General mapping to WorkTrace's three decisions:
- "capability or tier granted" ⇒ **proceed** autonomously in decision class c;
- "not granted" ⇒ **escalate**;
- legally reserved classes are always escalate, outside the ceiling.

The baseline should be as strong as possible, not a straw man. So, by default, **every episode in c updates the baseline's state from the agent's proposed action**, including escalated ones: a shadow audit, with the outcome label taken from the generator's oracle. In both papers an escalated or denied task produces no audit. That variant is weaker; report it as a sensitivity arm.

### B-SOS: Sovereign-OS TrustScore (paper v1, per class)

```
state: s[c] = 50 for every decision class c (paper: one score per agent; variant B-SOS-global shares s across classes)
after episode e in class c:
    pass  = outcome_correct(e)                 # paper: LLM-judge score >= 0.50 vs KPI; here: oracle, judge as a variant
    s[c]  = min(100, s[c] + 5) if pass else max(0, s[c] - 15)
    if cost_overrun(e): s[c] = max(0, s[c] - 10) # code: actual > 1.25 x estimate; usually N/A in WorkTrace
decide(c) = PROCEED if s[c] >= theta[c] else ESCALATE
theta: paper tiers 10/40/50/60/80 by effect class (read / write / external call / execute / spend); for matched coverage sweep theta in {0,5,...,100}
```

Properties worth reporting:
- Reachable states are multiples of 5.
- **Steady state.** The score drifts upward iff 5p − 15(1−p) > 0, i.e. **pass rate p > 0.75**. Stationary probability of s ≥ 60 (computed for this note):

  | p | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 |
  |---|---|---|---|---|---|
  | P(s ≥ 60) | 0.16 | 0.45 | 0.78 | 0.95 | 0.99 |

  P(s ≥ 80) is 0.07, 0.26, 0.58, 0.82 and 0.94 at the same p. So B-SOS is in effect a "recent pass rate ≳ 0.8" rule with a memory of roughly a few dozen episodes.
- **Revocation is immediate.** One failure removes any tier within 15 points.
- **Code variant B-SOS-q:** delta = round(5·q) on pass, round(−15·(1−q)) on fail, with q = judge score; per-category trust seeded from global.

### B-DA: Digital Apprentice correction-rate graduation (per class)

```
state: tier[c] in {L0, L1, L2}; start L0 (Pre-L0 observation assumed done)
windows: non-overlapping blocks of N consecutive episodes of class c; rho_t = mean correction indicator in W_t
correction indicator: corr(e) = 1 if the (simulated) reviewer would correct the agent's proposal
                      = oracle_wrong(e) AND NOT reviewer_miss(e);   reviewer_miss ~ Bernoulli(m)   # m = complacency, default 0
at end of each W_t (t >= 4):
    C1 = rho_t < rho_{t-3}            # paper, k = 3; see ambiguity below
    C2 = rho_t <= tau_corr
    Q1 = (no scorer) or mean[Q(e) >= tau] >= p
    if C1 and C2 and Q1 and H_auth: tier[c] += 1   (max L2)       # H_auth simulated = 1, counted as one review event
monitoring (rolling window of last N in c, evaluated after each episode):
    if rho_roll > rho_demote (or OOD score > u_max): tier[c] -= 1  # demotion depth not specified; we assume one tier
decide(c) = PROCEED if tier[c] == L2 else ESCALATE   # L0, L1 both require human review or approval before effect
```

Parameters the paper leaves open, with proposed defaults:
- **N:** 25 (sensitivity 10/50).
- **τ_corr:** swept for matched coverage.
- **ρ_demote:** 2·τ_corr.
- **Scorer:** off in the main arm.
- **OOD trigger:** off, or fed with the same evidence-shift detector given to all rules.

Ambiguities to state in the paper:
1. **C1 is unsatisfiable for a perfect agent.** If ρ_t = ρ_{t−3} = 0, C1 is false, because the inequality is strict. Use the favourable reading "ρ_t < ρ_{t−3} or ρ_t = 0".
2. **Earliest promotion.** Promotion to L2 needs at least 4N episodes for the first step, then more windows; with N = 25 that is ≥ 100 episodes per class. Comparable to WorkTrace's ~100 per class, but promotions happen sequentially, two steps.
3. **Censoring at L2.** Corrections are seen only on exceptions. In the main arm assume full outcome observation, which favours the baseline. Add a seeded-check-rate arm.

### Optional B-TBA: abstention-aware gate (Trust Before Autonomy R1)

This is recommended because it is the strongest "evidence-aware" competitor.

```
proceed in class c iff pass^k_hat(c) >= a  AND  abstentionF1(c on unanswerable variants) >= b
pass^k_hat = mean over tasks of C(c_i,k)/C(n_i,k), k = 5
unanswerable variants = WorkTrace "remove X" episodes where X is the sole decisive source and the oracle's correct response is escalate/refuse
```

If WorkTrace beats B-SOS and B-DA but not B-TBA, the contribution narrows to the remove-with-redundancy, only, invert and second-source conditions and to the joint reading. That is worth knowing before writing.

---

## 7. Adopting Earned Authority's ceiling without contradicting widening

1. **Ceiling.** For each deployment the human principal fixes B as the set of decision classes, with their permitted effects, in which the agent may *ever* proceed. This is the `permissions` field of the decision episode. Legally reserved classes (AMLR art. 76(5)(b)) are outside B by construction. The DSA rule never adds a class to B; only a new human grant does (EA Def. 5, Def. 8).
2. **Widening = gated ascent beneath B.** Moving class c from escalate to proceed is EA's "ascent", gated by ⊢ = "a valid DSA certificate for c". This is explicitly allowed (EA §VII-a: "Our objection is not to gradual allocation beneath a limit"). Narrowing (proceed → escalate or refuse) is "descent" and needs no evidence. Refuse and escalate are always admissible.
3. **Escalate = per-action confirmation.** In EA's Table II, escalate is a fresh user decision per protected action. So the WorkTrace rule chooses, per class, between active authority and per-action confirmation. The escalation cost is EA's "interaction cost".
4. **Independent evaluator** (EA Prop. 5 / Remark 2). The evidence must rest on premises the agent cannot realise: held-out episodes and seeds the agent never sees, interventions applied by the evaluator to external evidence, ground truth from the generator, a second oracle in code separate from the evaluator, and certificates signed by the evaluator. Add a human countersignature for the highest-impact classes.
5. **But claim reliability, not security.** The agent's *behaviour* on test episodes is agent-produced. An agent that can tell test from live episodes (evaluation awareness), or an injected agent that behaves well under test, can manufacture qualifying evidence. Then Prop. 4 applies and the adversarial bound is B.
   - Paper wording: "The DSA rule allocates autonomy beneath a fixed ceiling to reduce expected outcome errors; the security bound is the ceiling."
   - Add an indistinguishability requirement: interventional episodes are interleaved with and formatted like live ones. Report a test-awareness check, e.g. a canary or a probe asking the agent whether it is being tested.
6. **Transition envelope.** Bind each certificate to the measured agent configuration: model ID, system prompt, tool set, memory or skill state, scaffold, and decision-class definitions. Any change outside a pre-declared envelope *suspends* all proceed grants until re-certification (EA §V-A, Table I). Report a "false invalidation" count, as in EA §VIII.
7. **Decay** (EA Remark 5). Certificates expire after T episodes or days, or when a class is not exercised within k episodes. This is separate from the e-process revocation, which reacts to observed failures.
8. **Phase.** EA Prop. 3 shows authority need can change with task phase alone. Decision classes should be defined to include phase, e.g. "draft verdict" vs "release verdict", so that a certificate for one phase does not carry to the next.

## 8. Differentiation sentences (collected)

- **TBA:** "Angelidis et al. (2026) argue that crisis-EO agents should climb an autonomy ladder only through gates on repeated-run reliability, abstention on unanswerable task variants, risk–coverage and the reproducibility of cited evidence, but they leave thresholds to operators and run none of these gates; WorkTrace instead intervenes on the external evidence behind individual decisions, with the correct response known by construction, and evaluates the resulting per-decision-class rule on held-out episodes against outcome-, approval-, counter- and confidence-based rules."
- **TBA, unanswerable variants:** "Unanswerable variants are the special case of our *remove X* in which X is the only decisive evidence and the correct response is to abstain."
- **TBA, evidence validity:** "Their evidence validity re-executes the cited pipeline without the agent and so checks the reproducibility of claims, not whether the agent's decision depends on that evidence."
- **EA:** "Zhang and Zhang (2026) show that evidence about an agent may allocate authority only beneath a ceiling that no runtime evidence can move, and leave open which signals should drive that allocation; WorkTrace adopts the ceiling, treats its delegation rule as a reliability allocation beneath it, and supplies and tests one such signal."
- **Sovereign-OS:** "Sovereign-OS unlocks capability tiers from a TrustScore updated +5/−15 after LLM-judged audits of task output, in effect a rule that grants a tier while the recent pass rate stays above roughly 0.75–0.8, whatever evidence the outputs rested on."
- **Digital Apprentice:** "The Digital Apprentice promotes a skill when its windowed human-correction rate falls and a human signs off, a signal the authors themselves note is confounded by reviewer complacency; WorkTrace replaces it with evaluator-run interventions on external evidence and compares both rules on the same held-out, evidence-shifted episodes."

## 9. Implications for WorkTrace

**Threats to novelty (in order).**
1. **TBA pre-empts the shape of W3 as a prescription.** A per-task, gated, demotable, revocable autonomy ladder with risk–coverage and abstention tests and held-out-event evaluation. It also names P2 "epistemic honesty" and P3 "verifiability", which overlap the DSA components "uncertainty/contradiction boundaries", "escalating correctly" and "preserving provenance".
   - Mitigation: cite TBA as a concurrent position. Say DSA *includes* TBA's epistemic honesty and verifiability as components and adds intervention-tested grounding, decision-point recognition, authority scope and revision after correction. DSA's distinctive claim is predictive validity of the intervention-tested profile (H3), which TBA does not test.
   - TBA's F5 (capability does not predict abstention) is supporting evidence for DSA's *discriminant* validity against accuracy. Cite it as descriptive (n = 8–11, n.s.).
2. **"Remove X" overlaps unanswerable and abstention tasks** (TBA; GeoBenchX, MapEval and others via TBA; the Wen et al. 2025 survey). W2 must say explicitly that remove X with a sole decisive source and abstention as the correct response is the known special case. The new elements are the redundancy-robust set (remove with a second source present, only X, invert X, add an independent second source), joint reading against declared grounds, and correct responses other than abstain.
3. **Mechanism novelty is nil.** Per-class tiers, gated promotion, auto-demotion, "agent cannot promote itself", the ceiling, and suspension on mutation are all published (DA, Sovereign-OS, TBA, EA). This is consistent with positioning v2: the contribution is the signal plus the comparison.

**Design changes.**
- Implement **B-SOS** and **B-DA** exactly as in §6, with stated ambiguity resolutions and a shadow-audit default that favours the baselines. Add **B-TBA** (pass^5 plus abstention F1 on sole-source removals) as the strongest evidence-aware baseline.
- Add a **reviewer-complacency arm** (miss rate m > 0 at higher tiers) for approval and correction rules. DA itself names this weakness, and Parasuraman & Manzey 2010 supports it. It is a principled advantage of evaluator-run tests.
- Adopt EA's structure explicitly: ceiling = episode permissions; ascent by certificate; free descent; certificates bound to agent configuration with a transition envelope; decay; per-phase classes. Wording: "reliability allocation beneath a fixed ceiling"; never "security guarantee".
- Add an **evaluation-awareness / indistinguishability** check for intervention episodes. Without it, EA's Prop. 4 argument says the evidence is agent-realizable.
- Report EA-style secondary metrics: false revocations/invalidations, escalation (interaction) cost, ceiling occupancy.

**Naming.** Avoid "earned autonomy" and "earning autonomy" (Sovereign-OS, DA, TBA, EA). "Graduated autonomy" and "readiness gates" are also taken. "Evidence-contingent delegation" and "decision-structured agency" did not appear in any of the four papers.

**Things to cite.**
- TBA (concurrent position; F2, F3, F5 as motivation).
- EA (Def. 8 separation obligation; Prop. 5 / Remark 2; Remark 5 decay).
- Sovereign-OS and DA as baseline templates.
- Feng et al. 2025, arXiv:2506.12469 [verified].
- Wen et al. 2025, TACL, doi:10.1162/tacl_a_00754 [verified].
- Parasuraman & Manzey 2010, doi:10.1177/0018720810376055 [verified].
- Progent (Shi, He, Wang, Li, Wu, Guo, Song), arXiv:2504.11703 [verified]: automatic narrowing, approval-gated expansion.
- Optionally the capability-binding work EA builds on: Z. Zhou, *Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use*, arXiv:2603.14332 [verified].

**Re-check before submission.** TBA v2 or venue; whether EA gains an empirical section (it announces a mutation-replay study); later Sovereign-OS versions (the code already has per-category trust).
