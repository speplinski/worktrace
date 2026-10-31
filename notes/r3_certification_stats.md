# R3: Statistical certification neighbours of W3 (Shen 2026, Role-Stratified CRC, CORA, ToolChain-CRC, Conformal Selective Acting)

Round-3 reading note, written 2026-10-25. It builds on `r2_defer_and_risk_control.md`, which covered these five papers only in part (see its §2). This round read all five **in full** and corrects several round-2 statements (§7).

**Task.** Find anything that falsifies or narrows W3, the per-decision-class delegation rule with loss = unjustified action, certified per class, revocable, and compared at matched coverage against outcome-, approval-, history-counter- and confidence-based rules. Also extract the statistical machinery WorkTrace should adopt.

**Verification legend.**
- [verified]: metadata checked in this session against the arXiv API or Crossref.
- [venue unverified]: arXiv record verified; the venue comes only from an arXiv comment or a citing paper.

---

## 0. Executive summary (threats to novelty first)

1. **No falsification of W3.** None of the five papers does any of the following:
   - grants or revokes autonomy over a *decision class* defined at decision time;
   - uses a loss built from interventions on the evidence the agent used;
   - compares rules at matched coverage under an evidence shift.

   A targeted arXiv sweep (8 queries, §9.3) turned up no new competitor.

2. **Narrowing 1: the formal "outcome-only misses the basis" result is taken.** ToolChain-CRC Prop. 1 gives E[A·R^traj] = E[A·V] + E[A(1−V)U] and proves that final-answer-only calibration cannot control the second term. This is *structurally identical* to WorkTrace's decomposition ℓ_WT = ℓ_out + (1−ℓ_out)·ℓ_basis. WorkTrace must cite it as the formal statement and must not claim the observation.
   - What stays ours is how U/ℓ_basis is measured: counterfactual dependence under interventions, with ground truth by construction and attribution to the agent rather than to the environment (§4).

3. **Narrowing 2: all of the statistics are prior art.** WorkTrace may not claim any of the following:
   - per-stratum thresholds;
   - a simultaneous Clopper–Pearson + Bonferroni certificate across strata;
   - pooling of rare strata by a label-free rule;
   - the "price of coarseness" argument against pooled certificates (all four: Role-Stratified CRC, Thm 2, Alg. 1, Props 1–2);
   - a CP certificate on selective risk with a union bound over thresholds, used to "grant autonomy" (Shen, Prop. 3);
   - anytime-valid e-process certification of selective risk (CSA, Thm 5.1).

4. **Correction: CSA does *not* do data-driven revocation.**
   - Its e-process tests the *unsafe* null, so it only *grants*.
   - De-certification happens only at **pre-scheduled epoch resets** that revoke everything (App. B.2, Alg. 2).
   - The authors list "data-driven epoch restarts via change-point detection" as an *open direction* (App. I, (ii)).
   - ToolChain-CRC's alarm (§8, Thm 3) is a generic Ville bound with an uninstantiated ψ_s.

   So **data-driven, per-class revocation with hysteresis for an agent delegation status is still unclaimed**. The statistics for it exist in Podkopaev & Ramdas 2022 and Shin–Ramdas–Rinaldo e-detectors. WorkTrace may claim the *application* and the grant/revoke life cycle, never the test itself.

5. **Correction: Shen's "certified autonomy" is not a pure track-record rule.**
   - It certifies a **verbalized-confidence threshold** within each (model, task) pair, with outcome-correctness loss.
   - It is therefore a hybrid of the outcome baseline and the confidence baseline.
   - WorkTrace needs two baselines from it: **B-OO**, a pure per-class outcome track record (the trivial-selector special case), and **B-Shen**, as published (§3).

6. **Phrase collisions.** Avoid or cite:
   - "certified autonomy" and "grants autonomy" (Shen abstract, §4.4);
   - "selective action execution" (CORA);
   - "selective acting" (CSA);
   - "price of coarseness" (Role-Stratified).

7. **DSA as a construct.** No overlap with a named construct. Partial overlaps by dimension (§6):
   - Role-Stratified's counterfactual "untrusted input must not determine high-risk fields" touches the authority-scope and provenance dimensions;
   - Shen's verbalized uncertainty touches "recognising uncertainty", but the signal is weak (AUROC 0.47–0.66), which supports DSA's premise.

---

## 1. Reading coverage (this session)

| Work | Read | Not read / limits |
|---|---|---|
| Shen 2026 (2608.05064) | **Full text**, 12 pp (all sections, Tables 1–2, references). | Figures seen only via captions. |
| Role-Stratified CRC (2607.24343v2) | **Full text**, 17 pp: main text, Supplements A–G incl. all proofs (Props 1–4, Thms 1–2). | Figures via captions only. The code archive (one-per-episode check) was not opened. |
| CORA (2604.09155v1) | **Full text**, 29 pp: main text, App. A–I incl. metric definitions, ablations, judge prompts. | Figures via captions only. Judge–human agreement numbers are **not given** in the paper, despite the text saying "agreement statistics … are reported in the appendix". |
| ToolChain-CRC (2606.18467v1) | **Full text**, 26 pp: all sections, proofs, experiments, Table 2. | Figures via captions only. Code "included with the submission package"; no public repo. |
| Conformal Selective Acting (2605.20270v1) | Main text §1–7 and App. A, B, C (all proofs), D, E, F.1–F.2, F.8–F.9, G.4, H, I **in full**. | App. F.3–F.7, F.10 and G.1–G.3 skimmed (headline tables and text fragments only). |

---

## 2. (a) Comparison matrix

| | **Shen 2026** | **Role-Stratified CRC** | **CORA** | **ToolChain-CRC** | **CSA** |
|---|---|---|---|---|---|
| **Unit certified** | (model, task) pair. Threshold τ on calibrated verbalized confidence within the pair. | Final stratum g = a semantic argument role (target, credential, command, …), or a pooled high-risk stratum. Exchangeable unit = **field**; enforcement per field. | Single GUI step/action. One global threshold over all steps. | **Whole run** (trajectory). One global accept threshold λ. | Deployment stream. One threshold per grid point q; deploys max certified q. |
| **Loss** | 1[ŷ ≠ y] among answered (outcome correctness). | L_r = 1{s ≤ τ ∧ field violated}. "Violated" = "untrusted input changes its value against the user's intent". | ℓ_t·1{s_t ≤ τ}; ℓ_t = step-level harm label (human / Qwen-3 VLM judge). | R^traj = Y^traj·A(λ), with Y^traj = noisy-or of audited step labels (retrieval, tool, evidence support, synthesis). | A_t(q)(1−V_t); V_t = deterministic verifier pass. |
| **Signal used to gate** | Verbalized integer confidence → Platt map. | Per-field provenance score sim(x, untrusted) − sim(x, trusted prompt). AUC 0.71 deployable; 0.93 label-coupled oracle. | Guardian VLM risk head on (goal, screen, history, action). | Noisy-or of step risk scores (retrieval confidence, tool-error flags, verifiers). | Isotonic-calibrated self-consistency agreement (K = 5), via a logistic surrogate. |
| **Guarantee type** | **High-probability, conditional** (selective risk), batch: P(R(τ̂) ≤ r_max) ≥ 1−δ via CP + union over grid (Prop. 3). Per pair; **no correction across the 22 pairs**. | (i) **Expectation, joint** E[L_r] ≤ α(r) (eq. 5, CRC). (ii) **High-probability, joint, simultaneous over strata** via CP + Bonferroni (Thm 2). | **Expectation, joint** E[ℓ·1{s ≤ τ}] ≤ α (eq. 4–5). Weighted variant explicitly not claimed exact (App. F.4). | **Expectation, joint** E[R^traj(λ̂)] ≤ α "up to … finite-grid discretization error" (Thm 1). Drift: HP bound α + L·W₁ under Lipschitz assumption (Thm 2). | **Anytime-pathwise, conditional** (selective): R^act_T ≤ α + ν̄_T + O(N_T^{-1/2}) ∀T w.p. ≥ 1−2δ (Thm 5.1). No exchangeability; requires predictable updates and frontier stability. |
| **Revocation** | None. Certificate "void under distribution shift" (§5). | None. Recalibration on labelled target data restores a certificate (Prop. 4). | None. Weighted recalibration only. | Within-run / stream **alarm** (Thm 3, Ville) → escalate. No status revocation. | **Scheduled** epoch resets revoke all certifications (Alg. 2). Data-driven restarts are listed as open (App. I). |
| **Evaluation** | 11 open models (0.5–14B), ARC-Challenge + TruthfulQA, 200-item calibration sets, 25,168 predictions. | AgentDojo + InjecAgent, 6 LLMs, trace replay (no re-execution), 20 splits. | Phone-Harm (Harm-150 + Normal-150), MobileRisk, AndroidWorld core20; 4 base policies. | Synthetic tool-chain, RAG/tool stress test, SQuAD-derived RAG, API-free agentic QA, "live" API-free agent loop. **No LLM generations.** | 8 specialist benchmarks (480 streams), 5 live RLVR + LoRA cells, 16 adversarial-order cells. |
| **Baselines** | Uncalibrated, temperature scaling (TS), Platt, isotonic; threshold transfer across tasks. | Aggregate CRC, risk-weighted / inverse-prevalence / max-risk single-threshold losses, PACT/FIDES/CaMeL-inspired proxies. | Base policies, prompt self-check, heuristic gate, VLM-as-critic. | Final-answer-only CRC, prompt/retrieval-only CRC, fixed trajectory CRC, confidence gate. | CRC, LTT, ConfFact, NEX-Conf, ACI, SAOCP, fixed threshold, naive tuning, always-act; plus A-RCPS, CoFact, Conf-Arb, CAP/OCP. |
| **Distribution shift** | Not handled. Threshold transfer ARC → TQA violates budget by +1.3 to +30.6 pp (Table 2). | TV bound (Prop. 4); frozen thresholds evaluated empirically on 8 shifted conditions and leave-one-suite-out. | Weighted CRC by app frequency (eq. 8–9); cross-domain splits (results in appendix only as text). | Similarity-weighted calibration, n_eff, drift margin (Thm 2, §17). | Non-exchangeable by design (predictable filtration); adversarial orderings. |

**Joint vs conditional.** Only Shen and CSA certify the *conditional* selective risk that W3 needs, P(error | autonomous). CORA, ToolChain and Role-Stratified certify **joint** rates, which are smaller by a factor of the coverage.

---

## 3. Per-work notes

### 3.1 Shen 2026: "certified autonomy" via Clopper–Pearson

**Bibliographic data.** Jianru Shen. *Provable Limits and Certified Deferral for Verbalized Uncertainty in Small Language Models.* arXiv:2608.05064v1, 5 Aug 2026, cs.CL. [verified]. arXiv comment: "Accepted at MIWAI 2026 (The 19th International Conference on Multi-disciplinary Trends in Artificial Intelligence), to appear in Springer LNAI" [venue unverified]. Single author, University of Montana.

**Problem & contribution.** Can verbalized confidence support risk-controlled deferral for small open models?
- Three theory results:
  - Prop. 2: strictly monotone calibration preserves the risk–coverage frontier and AUROC;
  - Cor. 1: temperature scaling cannot calibrate a model whose confidence is always > ½ while accuracy is < ½;
  - Prop. 3: a Clopper–Pearson certificate with a union bound over the threshold grid.
- An 11-model study.
- A repair of an answer-ordering artifact in TruthfulQA (in the multiple-choice form all 817 items have the correct option first).

**Method.**
- Unit: (model, task) pair.
- Answer/defer policy: answer iff ĉ ≥ τ (§3.1).
- Loss: outcome error among answered items, eq. (1).
- Signal: Platt-calibrated verbalized confidence.
- Certificate (Prop. 3): "R(τ) ≤ BetaInv(1 − δ; k(τ)+1, n(τ)−k(τ))", with "δ by δ/|T|" over the grid T of distinct calibration confidences; τ̂ = min of certified τ.
- Remark 2: fitting Platt and selecting τ on the same 200 items is valid because the grid's retained sets are fixed by the raw-confidence ordering. This does **not** hold for isotonic regression.
- No interventions; no revocation.

**Evaluation.**
- Certified coverage at r_max = 20%, δ = 0.05:
  - Qwen2.5-14B / ARC: 99.8% coverage, test risk 8.1%;
  - Qwen2.5-7B / ARC: 93.3%, 10.8%;
  - Qwen2.5-14B / TQA: 43.6%, 14.2%;
  - all other 19 pairs refused.
- At 10%, no pair is certified (§4.4).
- AUROC for error detection is 0.468–0.655 (Table 1).
- Threshold transfer across tasks violates the budget for every tested model (Table 2).
- Calibration granularity: per-model-per-task temperatures halve ECE (0.157 → 0.072); per-task alone gives almost nothing (§4.5).

**What WorkTrace must NOT claim.**
- "Certified autonomy", or granting autonomy per (agent, task/class) by a CP certificate on outcome correctness.
- That refusal to certify is informative ("Refusal here is an informative output, not a failure mode", §4.4; "Refusal as a feature", §5).
- That certificates must be per task/class because thresholds do not transfer (§4.5, Table 2).

**What it leaves open (WorkTrace addresses).**
- Agents acting with external evidence, decision classes defined by situation, and any basis/justification loss.
- Interventions, revocation, and behaviour under shift: "the certificate assumes i.i.d. deployment and is void under distribution shift" (§5).
- Simultaneous certification across pairs.
- Any comparison against a non-outcome loss.

**Draft differentiation.** "Shen (2026) grants 'certified autonomy' to a model–task pair when a Clopper–Pearson bound on the error rate of its confidence-selected answers clears a budget; WorkTrace runs the same certification machinery per decision class but replaces outcome error with an intervention-defined unjustified-action loss, and tests whether that substitution predicts held-out failures under evidence shift."

**Citation cautions.**
- Single-author conference paper (MIWAI, Springer LNAI; venue unverified).
- 200-item calibration sets; i.i.d. assumption; multiple-choice QA, not agents.
- **No multiplicity correction across the 22 pairs.** Each pair is certified at δ = 0.05, so the family-wise false-grant probability across pairs is not controlled.
- The Platt map on logit(c) needs clipping at c = 1.00, which occurs ("raw confidence c = 1.00 is calibrated to ĉ = 0.94", §4.6). The clipping rule is unstated.

### 3.2 Role-Stratified CRC: the closest statistical template

**Bibliographic data.** Md Ashikur Rahman, Md Arifur Rahman, Niamul Hassan Samin, Khandaker Rifah Tasnia, Md Hasibul Amin, Sifat Rahman Ahona, Juena Ahmed Noshin. *Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls.* arXiv:2607.24343v2 (v1 27 Jul 2026, v2 31 Jul 2026), cs.LG. [verified]. Preprint, no venue. AAAI-style template.

**Problem & contribution.** Certifying a tool call as a whole lets failures in rare high-risk fields be averaged away. The paper certifies per semantic role.
- Prop. 1 (concentration gap): "If aggregate control guarantees V ≤ α_agg, then V(r) ≤ α_agg/p_r … and this bound is tight."
- Prop. 2: aggregate control cannot certify a rare role without shrinking the budget to α·p_r.
- Thm 1 ("price of coarseness"): orders observation channels Φ_agg ⪯ Φ_role ⪯ Φ_field via Blackwell 1953.

**Method.**
- Per-role split CRC (eq. 5) with certifiability floor 1/(n_r+1).
- **Alg. 1** pools roles whose floor exceeds α(r) into one high-risk stratum. The rule is **label-free**: it depends only on n_r.
- **Thm 2**: τ̂_g = sup{τ : U(k_g(τ), n_g; δ_g) ≤ α(g)} with an exact one-sided CP bound, and Σδ_g = δ, gives "V(g) ≤ α(g) … simultaneously for every g ∈ G" w.p. ≥ 1−δ.
  - **No union bound over thresholds is needed**: because the loss is monotone, the proof anchors at the deterministic population boundary τ*_g = inf{τ : V(g)(τ) > α(g)} (Supp. D).
- The δ allocation is chosen on an independent split D_alloc. Uniform Bonferroni matches water-filling on held-out utility (Supp. E, Fig. E.3).
- Episode-level loss L_{e,r} = max over same-role fields is recommended when one episode emits several same-role fields (Supp. A).
- The label-conditional (attack-conditional) certificate V_att is prevalence-invariant, whereas V(r) = π(r)·V_att(r) (Supp. A).
- Prop. 4: E_Q ≤ α + TV(P, Q); recalibration restores the certificate.

**Evaluation.**
- AgentDojo + InjecAgent; GPT-4o, GPT-4o-mini, Gemini 2.5 Pro/Flash, Llama 3.3 70B, Qwen2.5-7B.
- Trace replay over 20 splits, no re-execution.
- At a 1% budget: per-field CRC gives 0.0–0.3% target violation vs up to 21.2% for single-threshold losses (Table 1).
- Credential role: 0–22 calibration fields per split. It "cannot be certified individually at a 1% budget", needs ≈300 fields, and the data support ≈3%. It is pooled and "report[ed] … as empirically controlled rather than individually certified" (Method; Supp. C, Table C.1).
- Under shift: 100% ± 0% compliance on 8 frozen conditions vs 61% ± 33% (PACT-inspired) and 48% ± 48% (FIDES-inspired) (Fig. 1b); 24/24 leave-one-suite-out (Table E.1).
- Utility cost: abstain utility 9.9% vs 27.2% (PACT-inspired) (Table 2).

**What WorkTrace must NOT claim.**
- Per-stratum certification for LLM agents.
- A simultaneous CP + Bonferroni certificate across strata.
- Label-free pooling of rare strata into a pooled stratum.
- An independent allocation split.
- The argument that pooled guarantees dilute rare high-stakes strata by 1/p.
- The episode-level max loss for correlated within-episode units.

**What it leaves open.**
- Strata are argument roles of one call, not decision classes; the certified object is runtime field gating, not an agent-level delegation status.
- The label is attack-induced value change judged against the attacker's injected literal (a clean-vs-injected contrast). There is no normative model of which evidence *should* determine the field, no redundancy handling, and no "right action, wrong basis" beyond injection.
- Joint, not conditional, risk.
- No outcome-only comparison and no revocation (only recalibration).
- Scope (Discussion): "the guarantee covers field-value integrity, not tool selection, omitted actions, call ordering".

**Draft differentiation.** "Role-stratified CRC certifies, per argument role, that injected content rarely determines a tool-call field; WorkTrace adopts its stratified, simultaneous certificate and rare-stratum pooling but certifies, per decision class, that an agent's autonomous actions rarely fail intervention tests on the external evidence they should rest on, and uses the certificate to grant and revoke autonomy."

**Citation cautions.**
- Preprint, seven authors, no venue.
- All main-text numbers are on frozen traces.
- The headline Table 1 uses the label-coupled diagnostic score, which reads the attacker literal that defines the label.
- The all-field certificates "hold under field-level independence within each role stratum", which the authors themselves call possibly "anti-conservative" (Supp. A).

### 3.3 CORA

**Bibliographic data.** Yushi Feng, Junye Du, Qifan Wang, Zizhan Ma, Qian Niu, Yutaka Matsuo, Long Feng, Lequan Yu. *CORA: Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Automation.* arXiv:2604.09155v1, 10 Apr 2026, cs.LG. [verified]. Preprint.

**Problem & contribution.** A post-policy, pre-action guard for mobile GUI agents that "reformulates safety as selective action execution".
- A Guardian VLM risk head.
- CRC sets the execute/abstain threshold.
- A Diagnostician VLM picks ABORT, CONFIRM or REFLECT for rejected actions.
- Goal-Lock: the user goal is frozen and "any text appearing in the UI tree … is treated strictly as untrusted evidence" (§3.6).
- The Phone-Harm benchmark.

**Method.**
- Loss L(Z; τ) = ℓ(Z)·1{s ≤ τ} (eq. 3); τ̂ = sup{τ : (Σ L + 1)/(n+1) ≤ α} (eq. 5).
- The guarantee is expectation over a joint rate (App. F.3, eq. 27). Yet the text reads it as "no more than 1% of autonomous actions are harmful" (§3.4), which is a conditional reading.
- Weighted calibration by app frequency (eq. 30). The authors state: "We do not claim that it restores the exact same guarantee" (F.4).
- Blockwise splits by template/seed (F.5).

**Evaluation.**
- Harm-150 (Table 1): CORA HR 4.37%, GAR 79.80%, IF1 85.29%, mHR 5.34%, OIR 19.23%. Note that **AutoGLM base alone has HR 3.58%**, i.e. lower harm than CORA wrapping it.
- Merged Harm + Normal (Table 2): HR 2.19%, GAR 89.69%, OIR 9.83% (0.42% on benign).
- AndroidWorld core20: 8/20 vs AutoGLM 6/20 (Table 3).

**What WorkTrace must NOT claim.**
- Execute/abstain gating of agent actions with conformal risk control.
- Safety–helpfulness–interruption (risk–coverage–escalation) frontiers as the reporting protocol for agent gating.
- Typed escalation channels (confirm / reflect / abort).
- Treating environment text as untrusted evidence relative to a frozen goal.

**What it leaves open.**
- Per-class guarantees: harm types are balanced 50/50/50 but not certified per type.
- Conditional risk, basis/justification loss, agent-level grants and revocation.
- An outcome-vs-evidence comparison.

**Draft differentiation.** "CORA gates each proposed GUI action against an expected joint harm budget using a learned risk score; WorkTrace grants or withholds autonomy per decision class against a high-probability bound on the conditional rate of unjustified actions, where 'unjustified' is established by interventions on the evidence rather than by a harm judge."

**Citation cautions.**
- Preprint.
- **Internal inconsistency.** App. E.1 reports 2.42% executed harm at the CRC-selected τ̂ = 0.952; App. E.3 reports 5.67% at the same τ̂, which **exceeds the 5% budget**, and says the generative variant "satisfies the CRC risk budget (δ = 5%) for τ ≤ 0.8".
- The target risk is called α in §3 but δ in §5.4 and App. E.
- Labels come partly from a Qwen-3 judge. The misuse judge reads the agent's own "thinking" ("Focus on the intent in thinking", App. G.3), and no judge–human agreement numbers are given.
- mHR is named "macro" but defined as the conditional rate among executed steps (eq. 11).

### 3.4 ToolChain-CRC: closest to the W3 loss

**Bibliographic data.** Jeffery Opoku, David Banahene. *ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift.* arXiv:2606.18467v1, 16 Jun 2026, stat.ML. "26 pages, 11 figures" [verified]. Preprint. The paper mentions a journal submission package; no venue.

**Problem & contribution.** "A final response may look acceptable even when the retrieval was weak, a tool output was wrong, or an earlier step was unsupported" (Abstract). The paper makes the whole trajectory the calibrated statistical object, and its novelty claim is explicitly narrow: "not that conformal risk control is new … [but that] the right statistical object for a tool-using agent is the whole trajectory" (§1).

**Method.**
- Step scores S_ij and audited step labels Y_ij ∈ [0, 1]. Labels "come from human audit, gold labels, deterministic validators, or a frozen verifier" (§3).
- Noisy-or aggregation into S^traj and Y^traj.
- **Prop. 1**: with U an upstream failure indicator ("such as unsupported retrieval or a wrong tool output") and V the visible final failure, R^traj = 1{U = 1 or V = 1} and "E[AR^traj] = E[AV] + E[A(1 − V)U]". "If the accept rule A depends only on a final-answer score, then controlling the final visible risk E[AV] does not by itself control the trajectory risk".
- Thm 1: split CRC on whole trajectories (exchangeable runs, adaptive within-run dependence allowed).
- Prop. 2: utility-aware selection inside the feasible set keeps the guarantee.
- Prop. 3: source-of-risk decomposition.
- Thm 2: drift via weights, n_eff and a Lipschitz/W₁ assumption.
- Lemma 1 / Thm 3: supermartingale "anytime escalation" at level δ.

**Evaluation.** Target α = 0.08. Post-shift accepted-trajectory risk, final-only vs ToolChain-CRC (Table 2):
- synthetic: 0.104 vs 0.006;
- RAG/tool stress test: 0.104 vs 0.003;
- SQuAD-derived RAG: 0.317 vs 0.000;
- agentic QA: 0.122 vs 0.010;
- live API-free loop: 0.355 vs 0.055, at intervention rate 0.864 vs 0.564 (§18).

All agents are scripted or deterministic ("No proprietary model API is required", §22).

**What WorkTrace must NOT claim.**
- That outcome/final-answer-only calibration provably misses correct-looking outputs with unsupported upstream steps (Prop. 1).
- A loss of the form "outcome failure OR process failure".
- Trajectory-level CRC.
- Anytime escalation alarms.
- Reporting intervention rate alongside risk.

**What it leaves open.** See §4 for detail.
- U is a judgement about the *state of the evidence chain* (supported? correct tool output?), not about whether the *agent's action depended* on the right evidence.
- No interventions, redundancy handling or attribution to the agent.
- No decision classes and no autonomy status.
- An expectation/joint guarantee only.
- Evaluation on its own loss: no test that trajectory calibration reduces held-out outcome errors.
- No LLM agents.

**Draft differentiation.** "ToolChain-CRC proves that final-answer calibration cannot control accepted runs whose upstream steps were unsupported and calibrates audited trajectory failures instead; WorkTrace keeps that decomposition but measures the basis term by intervening on external evidence and checking the agent's action against a normative response known by construction, so it penalises the agent's handling of evidence rather than the environment's evidence quality, and it tests whether the basis term predicts held-out outcome failures."

**Citation cautions.**
- Two authors; preprint; no LLM experiments.
- Thm 1 holds "up to the usual finite-grid discretization error from searching over Λ", so it is not a clean finite-sample statement.
- Lemma 1 / Thm 3 assume a ψ_s making each factor have conditional mean ≤ 1, but no concrete ψ_s or betting rule is given for the experiments.
- Thm 2's guarantee depends on an estimated Lipschitz constant (L̂₉₀ = 0.246) and is presented as "an auditable reporting tool, not as a magic certificate" (§6).
- Reported results are all on the paper's own trajectory loss.

### 3.5 Conformal Selective Acting (CSA)

**Bibliographic data.** Hamed Khosravi, Xiaoming Huo. *Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs.* arXiv:2605.20270v1, 18 May 2026, cs.LG / cs.AI / stat.ML. [verified]. Preprint, Georgia Tech. Code at github.com/HamedKhosravi99/CSA-RLVR (not opened).

**Problem & contribution.** Per-deployment, anytime-pathwise control of *selective* verifier risk on a non-exchangeable, online-updated stream. CSA classifies prior wrappers by a (statistic, validity, rule) triple and fills the "empty cell" (§3).
- Key distinction: "a marginal statistic is built from 1−V_t … a selective statistic is built from A_t(1−V_t) … Selective risk is not derivable from marginal risk" (§3.1–3.2).
- Empirically, A-RCPS gives marginal 0.042 but selective 0.147 at α = 0.10 (App. F.8).

**Method.**
- Increment X_t(q) = A_t(q)((1−V_t) − α).
- Per-threshold e-process E_{j,t}(q) = Π(1 − λ X_s(q)) under the **unsafe** null E[X_t(q) | F_{t−1}] ≥ 0. Crossing 1/δ_{j,q} *certifies* q (eq. 1, Prop. 4.3).
- Plug-in bet λ = clip(−μ̂/(1−α)², 0, 1/(2(1−α))) (eq. 2).
- Bonferroni over the grid, with epoch factor δ_{j,q} = 6δ/(π²|Q|j²).
- Deploy max certified q (§4.3).
- Assumption 4.2: predictable pipeline and nested monotone gates.
- **Thm 5.1** needs, besides 4.2, a frontier-stability hypothesis (Thm C.1: "the oracle frontier q*_t is nondecreasing within each epoch").
- **Revocation**:
  - Alg. 1 (single-epoch): "Certifications are permanent".
  - Alg. 2 (CSA-Epoch): "resets at deterministic epoch boundaries … A restart revokes all certifications and costs ∼100–400 rounds per epoch to re-certify" (App. B.2).
  - Early resets are suggested only via a heuristic diagnostic: "a sustained Brier increase of > 20% over the warmup baseline" (App. B.5).
  - Data-driven restarts are listed as open: "(ii) Data-driven epoch restarts via change-point detection on {X_t(q)}" (App. I).
- **Sparse verifier** (Thm E.1): with Bernoulli(π_t) auditing and importance-weighted increments X̃ = (B/π)X, and bets capped at π_min/(1−α), all guarantees hold and the expected certification delay grows by 1/π_min.
- Verifier on abstained rounds: needed to certify higher thresholds. Under "partial evaluation" the controller "stalls … but stays valid" (App. B.4).

**Evaluation.**
- 8 benchmarks at pivotal α*: CSA PathV 0/10 with mean action rate 52.7%. CRC refuses on 6/8, LTT on 3/8, ConfFact on 2/8 (Table 2).
- 0/480 violations overall.
- Live LoRA cells: PathV 0/100 with action rate ≥ 50% (Tables 3–4).
- 16 adversarial cells: 0/16 violated, but CSA itself refuses on 9/16 (Table 5).
- Sparse verifier, π = 0.2: first certification at 312 rounds vs 70 at π = 1 (Table 20).

**What WorkTrace must NOT claim.**
- Anytime-valid certification (grant) of an act/abstain decision on selective risk.
- Per-threshold e-processes.
- Sparse (Bernoulli) auditing with importance weighting inside an e-process.
- The marginal-vs-selective distinction.
- That scheduled re-certification revokes stale grants.

**What it leaves open.**
- Data-driven de-certification and hysteresis.
- Decision classes / strata (one stream, one deployed threshold).
- Basis or intervention losses: the verifier is deterministic and outcome-only.
- Delegation to humans and escalation cost.
- Agents acting in environments.

**Draft differentiation.** "CSA certifies anytime-validly that a single stream's selective verifier risk is below budget and revokes only on a fixed schedule; WorkTrace uses the same e-process construction for (re-)granting autonomy per decision class, adds a data-driven revocation test with hysteresis, and defines the monitored loss by intervention tests on evidence rather than by an outcome verifier."

**Citation cautions.**
- Preprint.
- "Unique instantiation" / "empty cell" is the authors' rhetoric.
- Streams are replays (T = 30 × N_eval, shuffled passes), not fresh items.
- The sparse-verifier table shows PathV up to 6/20 at π ∈ {0.1, 0.2} while claiming validity. That is consistent only because PathV counts crossings of bare α while the theorem allows α + slack, a subtle reporting choice.
- The comparison against LTT/CRC is under the paper's own stream protocol, where offline methods calibrated on 20% of items naturally refuse more often.

---

## 4. (c) ToolChain-CRC vs WorkTrace's "right action on wrong basis"

### 4.1 Formal correspondence

| ToolChain-CRC (§3, Prop. 1) | WorkTrace (r2 §3.2) |
|---|---|
| V = visible final failure | ℓ_out = 1[a(E) ∉ A*(E)] |
| U = upstream failure: unsupported retrieval, wrong tool output, unsupported synthesis | ℓ_basis = 1[∃ j ∈ 𝓘(E): a(do_j(E)) ∉ A*(do_j(E))] |
| R^traj = V + (1−V)U | ℓ_WT = ℓ_out + (1−ℓ_out)·ℓ_basis = max(ℓ_out, ℓ_basis) |
| E[A·R^traj] = E[A·V] + E[A(1−V)U] | E[ℓ_WT·1{auto}] = E[ℓ_out·1{auto}] + E[(1−ℓ_out)ℓ_basis·1{auto}], i.e. right action on wrong basis |

**The algebra and the critique are the same.** The second term is invisible to any rule that sees only outcomes. WorkTrace should state its decomposition and cite ToolChain Prop. 1 for the formal point. It should also cite CXBench and PAE (r2_agent_evaluation) for the empirical prevalence.

### 4.2 Where they diverge (labels vs interventions)

| Case | ToolChain-CRC U | WorkTrace ℓ_basis | Comment |
|---|---|---|---|
| Decisive source retrieved and supports the answer, but the agent ignores it and answers from priors (same answer) | U = 0, V = 0 → **no failure** | invert-X leaves the action unchanged → **ℓ_basis = 1** | Core WorkTrace case. Only an intervention detects it. |
| Tool returns a wrong value; the agent notices the conflict, discounts it and escalates or uses a second source | U = 1 → **failure** | Normative handling → ℓ_basis = 0 | ToolChain charges the *environment's* error to the run. WorkTrace scores the *agent's handling*, which is the DSA capability. |
| Two independent supporting sources; one retrieval step weak | Noisy-or: U = 1 if any step's audited label fails | remove-X: A* unchanged by construction → no penalty if the action holds | Redundancy is handled only in WorkTrace. |
| Correct answer, cited source does not support it, true support exists elsewhere in context | U = 1 (support validator fails) | Depends on interventions: if remove(cited) leaves the action unchanged and remove(true) changes it, then declared grounds ≠ operative grounds (declared-grounds clause) | WorkTrace separates "unsupported citation" from "unsupported decision". |
| Final answer wrong | V = 1 | ℓ_out = 1 | Same. |

**Labels vs interventions.**
- ToolChain's Y_ij are *observational* labels on one realised run, from audit, gold labels or validators. In its experiments they are "known retrieval, tool, and synthesis failure indicators" (synthetic), "whether the selected context supports the answer" (SQuAD) and "scripted validators" (agentic QA) (§3). The agent is never re-run.
- WorkTrace's ℓ_basis is *counterfactual*. It needs re-execution of the agent under do(·) on external evidence, plus a normative map A*(do_j(E)) known by construction. That is more expensive, needs a replayable environment, and is only defined relative to the pre-registered family 𝓘.

**Verdict.** ToolChain is the closest prior work on the *loss shape* and the *outcome-only blind spot*. It does not measure evidence-dependence and does not attribute failures to the agent rather than the environment. It also never tests predictive validity: every method is scored on R^traj itself, so final-only calibration "fails" by construction. This is exactly the circularity that WorkTrace's H3 endpoint (outcome errors under evidence shift) is designed to avoid.

**Wording to adopt.** "The outcome-blindness of final-answer calibration to upstream failures is formalised by Opoku and Banahene (2026, Prop. 1); our contribution is to measure that upstream term as counterfactual dependence of the agent's action on external evidence, with ground truth by construction, and to test whether it predicts outcome failures under evidence shift."

---

## 5. (b) Shen 2026: exact operational rule, and the WorkTrace baselines built on it

### 5.1 Shen's rule as published (§3.1–3.5, §4.1)

Per (model m, task k):

1. **Calibration data.** n = 200 i.i.d. items D_cal, disjoint from test. For each item i: prediction ŷ_i, verbalized integer confidence c_i/100, correctness z_i = 1[ŷ_i = y_i].
   - Unparseable responses are "automatic deferrals".
   - Answer-only recoveries count toward accuracy but not toward calibration (§4.1).
2. **Calibration map.** Platt: ĉ = σ(a·logit(c) + b), fit by logistic regression of z on logit(c) over D_cal. Require a > 0; it held in all 22 pairs.
   - Implementation must clip c ∈ {0, 1} before the logit; the paper does not state how.
3. **Grid.** T = the distinct calibrated confidence values on D_cal.
4. **Per-threshold certificate.** For τ ∈ T: n(τ) = #{i : ĉ_i ≥ τ}, k(τ) = #{i : ĉ_i ≥ τ, z_i = 0}, UCB(τ) = BetaInv(1 − δ/|T|; k(τ)+1, n(τ)−k(τ)).
5. **Selection.** τ̂ = min{τ ∈ T : UCB(τ) ≤ r_max} (maximal coverage). If the set is empty → **refuse**: no autonomous operating point, defer everything.
6. **Deployment.** Answer autonomously iff ĉ ≥ τ̂; otherwise defer to a human.
7. **Parameters.** δ = 0.05; r_max ∈ {0.10, 0.20}. No correction across pairs.
8. **Guarantee.** W.p. ≥ 1 − δ, P(error | ĉ ≥ τ̂) ≤ r_max under i.i.d. deployment.

### 5.2 WorkTrace mapping and recommended baselines

| Shen | WorkTrace |
|---|---|
| (model, task) | (agent configuration π, decision class c) |
| Item | Independent generated episode (one scored decision per template/seed; r2 A3) |
| z_i = correctness | ℓ_out(E) = 1[a(E) ∉ A*(E)] |
| Verbalized confidence | Agent's stated confidence at the decision (elicited in a fixed format), or none |
| Defer to human | Escalate |

- **B-OO (pure outcome track record; primary outcome-only baseline).** Shen's rule with the trivial selector: one hypothesis per class, no grid.
  - Grant class c iff UCB_CP(k_out,c, n_c; δ_c) ≤ α_c, with δ_c = δ/C (Bonferroni across classes, as in Role-Stratified Thm 2).
  - This is the clean "track record" comparator for W3.
- **B-Shen (as published).** Within-class Platt-calibrated confidence threshold, union bound over the grid, outcome loss, per-class δ.
  - This is a *hybrid* outcome + confidence rule. Report it separately from the confidence baseline (CORA/READY-style learned risk scores).
- **Fairness rule.** Every rule (WorkTrace, B-OO, B-Shen, approval-based, counter-based, confidence-based) goes through **the same certification engine**: the same δ, the same cross-class Bonferroni, and the same within-class procedure (fixed-sequence per LTT, or Shen's union bound). Only the loss and the selector differ. Report Shen-as-published (per-class δ, no cross-class correction) as a sensitivity row.
- **Matched coverage.** Sweep α per rule and compare outcome-error rates at equal autonomous coverage Φ (r2 §3.5, §3.7).
- **Sample-size consequence** (computed here, zero failures, exact CP; same formula as r2 §5):

  | Classes C | α | Pure class rule (B-OO, WorkTrace) | B-Shen with grid \|T\| = 10 |
  |---|---|---|---|
  | 6 | 0.10 | n ≥ 46 | n ≥ 68 |
  | 6 | 0.05 | n ≥ 94 | n ≥ 139 |

  So B-Shen is less powerful at pilot sizes. Do not let this asymmetry decide H3. The fixed-sequence variant removes the grid cost.

---

## 6. (e) Constructs overlapping DSA

None of the five names a construct comparable to Decision-Structured Agency. Partial overlaps by DSA dimension:

| DSA dimension | Closest construct in these papers | Nature of overlap |
|---|---|---|
| Grounding in the right evidence (by intervention) | Role-Stratified's violation: "untrusted input changes its value against the user's intent". Its oracle score is a "counterfactual clean-vs-injected overlap" (Supp. A). | Field-level, attack-only counterfactual. No normative model of correct grounds. |
| Staying within authority scope / provenance | Role-Stratified's IFC lattice (integrity-critical sinks); CORA's Goal-Lock ("on-screen text … untrusted evidence, not instruction"). | Enforced by a guard, not *measured as an agent capability*. |
| Recognising uncertainty | Shen's verbalized confidence; CSA's self-consistency agreement. | Measured as calibration/discrimination of a score. Shen finds AUROC 0.47–0.66, i.e. weak. This **supports** DSA's claim that self-reported uncertainty is not a sufficient basis for delegation. |
| Escalating correctly | CORA's Diagnostician (abort / confirm / reflect, IF1). | A property of the guard, not of the agent. |
| Process quality (evidence support, tool use, synthesis) | ToolChain's "source-of-risk" diagnostics R_ret, R_tool, R_syn (§7). | Attributes of a *trajectory*, mixing environment and agent failures; not an agent capability profile. |

**Threat level for DSA: low.** These works measure properties of outputs, fields or trajectories for gating. None defines a capability of the agent that is profiled per decision class and used to delegate.

---

## 7. Corrections to round-2 notes (`r2_defer_and_risk_control.md`)

1. **§1 item 6 and §6.6 (CSA).** "Revocation by sequential monitoring is prior art … Conformal Selective Acting 2026 (per-threshold e-processes on selective risk …)". This needs refinement.
   - CSA's e-process tests the *unsafe* null, i.e. it **certifies**.
   - De-certification is **schedule-based** (Alg. 2), and data-driven restarts are an explicit open direction (App. I).
   - Revocation prior art is therefore Podkopaev & Ramdas 2022 (harmful-shift detection) and e-detectors (Shin et al.), not CSA.
   - The r2 feature-matrix entry "CSA: Seq. revoke ✓" should become "~ (scheduled)".
2. **§1 item 5 / §6.6 (Shen).** "Outcome-only" should read "outcome loss with a confidence-threshold selector". The pure track-record rule is its trivial-selector special case (§5).
3. **§6.6 (CORA).** Add the E.1/E.3 inconsistency, and that CORA's HR (4.37%) is above its own unwrapped base policy's (3.58%) on Harm-150 (Table 1).
4. **§6.6 (ToolChain-CRC).** Add that there are no LLM agents in the experiments, Thm 1 is "up to … discretization error", and all evaluation uses its own loss.
5. **§3.4 (r2 Proposition).** For monotone losses (joint rates), Role-Stratified's population-boundary argument removes the need for any multiplicity over thresholds. For WorkTrace's **conditional** selective risk, which is non-monotone, fixed-sequence (LTT) or a union bound (Shen) is still required. r2's choice stands.

---

## 8. (d) Machinery to adopt, with references, and what remains ours

| Component | Adopt | Cite (all [verified] unless noted) |
|---|---|---|
| Per-class conditional selective-risk certificate, high probability | Exact one-sided CP p-value per (class, λ); fixed-sequence over a pre-specified λ grid. | Clopper & Pearson 1934; Geifman & El-Yaniv 2017; Angelopoulos et al. 2025 (LTT, AoAS); Shen 2026 Prop. 3 as an instance; Bates et al. 2021 (RCPS) |
| Simultaneous across classes | Bonferroni δ/\|G\| over final strata; uniform allocation, or an allocation fixed on an independent split. | Rahman et al. 2026, Thm 2 and "Independent confidence allocation" |
| Rare classes | **Label-free pooling rule**: pool class c if n_c < n_min(α_c, δ_c) into a "residual high-stakes" stratum certified jointly. Report pooled classes as "pooled-certified", never individually certified (Prop. 1: the member bound is only α/p_{c\|pool}). Default for an uncertifiable individual class = escalate; refusal to certify is reported as an output. | Rahman et al. 2026 Alg. 1, Prop. 1, Supp. C; Ding et al. 2023 (clustered class-conditional conformal) [venue unverified]; Vovk et al. 2005 (Mondrian); Shen 2026 §5 ("refusal as a feature") |
| Why per-class at all | Pooled certificates dilute rare classes by 1/p_c (price of coarseness); thresholds do not transfer across tasks. | Rahman et al. 2026 Props 1–2, Thm 1; Shen 2026 Table 2; Saban 2026 (from r2) |
| Correlated units | One scored decision per independent template/seed; otherwise episode-level max loss. | Rahman et al. 2026 Supp. A; Feng et al. 2026 App. F.5 (blockwise by template/seed); Opoku & Banahene 2026 (trajectory as unit) |
| Prevalence-invariant certificate | Optionally certify per (class × evidence condition), e.g. stale / contradictory / redundant, or report condition-conditional rates. A shift that only changes the *mix* of evidence conditions then leaves each certificate valid. **Apply identically to all baselines.** | Rahman et al. 2026 Supp. A (V = π·V_att); Podkopaev & Ramdas 2021 (label shift, UAI) [from Rahman's references; not checked] |
| Anytime (re-)grant | Per-class e-process on audited unjustified-action indicators under the *unsafe* null; plug-in bet; certify at 1/δ_c. | Khosravi & Huo 2026 eq. 1–2, Thm 5.1, Thm 5.3; Waudby-Smith & Ramdas 2024 |
| Random audits after a grant | Bernoulli(r_c) audit with importance weighting X̃ = (B/r)X and bet cap r_min/(1−α). Delay inflates by 1/r_c. | Khosravi & Huo 2026 Thm E.1, Table 20 |
| **Revocation (data-driven)** | Per-class test of H0: risk ≤ α′_c with e-process M_t = Π(1 + λ_s(X_s − α′_c)); revoke at M_t ≥ 1/δ_rev (Ville). Or a CUSUM-type e-detector to bound detection delay. | Podkopaev & Ramdas 2022 (ICLR); Shin, Ramdas & Rinaldo 2023 (e-detectors, NEJSDS); Ramdas et al. 2023 (SAVI, Stat. Sci.); Page 1954 (CUSUM) |
| Hysteresis / switching | Grant at α_c, revoke at α′_c > α_c. After revocation, re-grant only on fresh evidence. Any change of π resets the class to escalate (CSA's "predictable pipeline"). | **Classical precedent: Dodge 1943 CSP-1.** Its switching rule matches grant → audit → revoke: 100% inspection until i consecutive conforming units, then sample a fraction f, and revert to 100% inspection on a defect. Cite it as the counter-based ancestor, i.e. ACP-style history counters. Statistical part: Podkopaev & Ramdas 2022; Khosravi & Huo 2026 App. B.2 (scheduled resets as an alternative). |
| Within-run escalation (optional) | Supermartingale alarm on step-level risk. | Opoku & Banahene 2026 §8, Thm 3 |
| Reporting | Risk–coverage–escalation frontier; escalation rate always reported with risk; per-class curves; n_eff; refusals. | Feng et al. 2026 (safety–helpfulness–interruption); Opoku & Banahene 2026 §20; Khosravi & Huo 2026 (action rate vs pathwise violations) |
| Shift statements | No certificate under evidence shift. At most TV-type bounds (E_Q ≤ α + TV). Shift results are empirical. | Rahman et al. 2026 Prop. 4; Angelopoulos et al. 2024 (CRC) §4; Barber et al. 2023 |
| Expectation vs high probability | Never phrase CRC-type (expectation) results as "with probability ≥ 1−δ". | Hultberg et al. 2026; Rahman et al. 2026 (they separate eq. 5 from Thm 2) |

### What remains WorkTrace's own (defensible after this round)

1. **The loss.** Unjustified action = wrong action OR right action whose dependence on external evidence fails pre-registered interventions (remove / only / invert / add an independent second source), scored against a normative response known by construction.
   - It attributes failures to the agent's *handling* of evidence, not to the environment's evidence quality, which separates it from ToolChain's U.
   - It handles redundancy by construction.
2. **The unit.** A decision class with a decision-time membership rule, used to set an agent-level delegation status (proceed / escalate / refuse), not per-call gating.
3. **The test.** Predictive validity at matched coverage: does the intervention-defined loss certify classes that make fewer *outcome* errors on held-out episodes under evidence shift than B-OO, B-Shen and the confidence, approval and counter rules run through the same engine? None of the five papers runs such an out-of-loss test; ToolChain and Role-Stratified evaluate on their own loss.
4. **The life cycle.** Batch grant, anytime re-grant, **data-driven** revocation with hysteresis, and reset on agent change, all per decision class. CSA has anytime grants with scheduled revocation; nobody has the data-driven per-class combination for agent delegation. The novelty is the combination and application, never the tests.
5. **The construct.** DSA as the measured capability profile behind the grant (§6).

---

## 9. Implications for WorkTrace

### 9.1 Design changes
1. **Two outcome baselines from Shen:** B-OO (pure per-class track record; primary) and B-Shen (outcome loss + confidence threshold; as published). Elicit agent confidence in a fixed format so B-Shen can run. Run all rules through one certification engine (§5.2).
2. **Write ℓ_WT as the ToolChain decomposition**, cite Prop. 1, and add the attribution table of §4.2 as the conceptual argument for interventions over audit labels.
3. **Rare-class policy:** a label-free pooling rule fixed before calibration (Role-Stratified Alg. 1 style). Pooled certificates are reported as pooled only, with escalate as the default for any class not individually certified.
4. **Revocation:**
   - Implement a separate data-driven revocation e-process (Podkopaev & Ramdas style) with hysteresis α′ > α.
   - Do *not* describe CSA as doing this.
   - Optionally compare against CSA-style scheduled resets as a revocation baseline: same audit budget, measure detection delay and false revocations.
5. **Audits:** use CSA Thm E.1 importance-weighted Bernoulli audits. Report the 1/r detection-delay inflation (CSA Table 20 shows first certification at 312 vs 70 rounds at r = 0.2).
6. **Optional per-evidence-condition stratification** (prevalence-invariant certificates). It must be applied to every baseline, or the H3 comparison is unfair.
7. **Escalation channels:** consider typed escalation (confirm / reflect / abort, as in CORA) only if it is measured. Otherwise keep proceed / escalate / refuse.
8. **Report conditional and joint rates side by side.** This avoids CORA's misreading and lets readers map our numbers onto CORA, ToolChain and Role-Stratified.

### 9.2 Risks
- **Reviewer framing risk.** With ToolChain Prop. 1, Role-Stratified Thm 2 and CSA Thm 5.1, a reviewer can say "this is stratified CRC with a different label". The answer must lead with the loss (interventions, attribution, redundancy) and with the out-of-loss predictive test (H3), not with the statistics.
- **Near-term competitor.** A combination of Role-Stratified (strata) and CSA (anytime) for tool classes is a natural next paper. Re-run the sweep before submission: "stratified" + "anytime" + "agent"; "per-tool" + "e-process"; "autonomy" + "Clopper".
- **Cost asymmetry.** Interventional labels need replayable environments and re-execution; ToolChain and Role-Stratified run on frozen traces. Budget the extra calls and state them.
- **Phrases:** do not use "certified autonomy", "selective acting", "selective action execution" or "price of coarseness" without citation.

### 9.3 Search record (this session)
arXiv API queries, sorted by date:
- abs:autonomy AND abs:Clopper → only Shen 2026 (plus one unrelated Jira-orchestration paper).
- abs:revoke AND abs:e-process → 0 relevant.
- abs:revocation AND abs:anytime-valid AND abs:agent → 0.
- abs:delegation AND abs:conformal AND abs:agent → capability/mandate papers (DelegateGuard 2610.16005, Mandato 2608.14074, KYA 2605.25376, SentinelAgent 2604.02767), none statistical (titles only).
- abs:stratified AND abs:anytime AND abs:agent → 0.
- abs:certified AND abs:autonomy AND abs:agent → 0 relevant.
- abs:"decision class" AND abs:agent AND abs:risk → 1 unrelated (5G control).
- abs:"earned autonomy" → Sovereign-OS (known), "The Observability Gap" 2603.26942 (title only; motivation for output-feedback failure; not read).

**No new threat.** Forward citations of the five papers were not checked; arXiv has no citation API, and no Semantic Scholar call was made.

### 9.4 Things to cite (must)
Shen 2026; Rahman et al. 2026; Feng et al. 2026 (CORA); Opoku & Banahene 2026; Khosravi & Huo 2026; Clopper & Pearson 1934; Geifman & El-Yaniv 2017; Angelopoulos et al. 2025 (LTT); Angelopoulos et al. 2024 (CRC); Bates et al. 2021 (RCPS); Podkopaev & Ramdas 2022; Waudby-Smith & Ramdas 2024; Ramdas et al. 2023 (SAVI); Shin, Ramdas & Rinaldo 2023 (e-detectors); Xu et al. 2024 (A-RCPS, for the marginal-vs-selective contrast); Dodge 1943 (CSP-1, switching precedent).

**Should cite:** Ding et al. 2023; Vovk et al. 2005; Barber et al. 2023; Hultberg et al. 2026; Page 1954; Blackwell 1953 (only if the price-of-coarseness argument is reproduced).

---

## 10. Bibliography and verification record

| # | Reference | Identifier | Verified via |
|---|---|---|---|
| 1 | Shen, J. (2026). Provable Limits and Certified Deferral for Verbalized Uncertainty in Small Language Models. MIWAI 2026, Springer LNAI (to appear) [venue unverified]. | arXiv:2608.05064 | arXiv API [verified] |
| 2 | Rahman, M. A., Rahman, M. A., Samin, N. H., Tasnia, K. R., Amin, M. H., Ahona, S. R., Noshin, J. A. (2026). Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls. | arXiv:2607.24343 (v2) | arXiv API [verified] |
| 3 | Feng, Y., Du, J., Wang, Q., Ma, Z., Niu, Q., Matsuo, Y., Feng, L., Yu, L. (2026). CORA: Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Automation. | arXiv:2604.09155 | arXiv API [verified] |
| 4 | Opoku, J., Banahene, D. (2026). ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift. | arXiv:2606.18467 | arXiv API [verified] |
| 5 | Khosravi, H., Huo, X. (2026). Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs. | arXiv:2605.20270 | arXiv API [verified] |
| 6 | Clopper, C. J., Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4):404–413. | doi:10.1093/biomet/26.4.404 | Crossref [verified] |
| 7 | Geifman, Y., El-Yaniv, R. (2017). Selective Classification for Deep Neural Networks. NeurIPS 2017. | arXiv:1705.08500 | arXiv API [verified]; venue per r2 note |
| 8 | Angelopoulos, A. N., Bates, S., Candès, E. J., Jordan, M. I., Lei, L. (2025). Learn then test: Calibrating predictive algorithms to achieve risk control. Annals of Applied Statistics 19(2):1641–1662. | doi:10.1214/24-AOAS1998; arXiv:2110.01052 | Crossref + arXiv [verified] |
| 9 | Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., Schuster, T. (2024). Conformal Risk Control. ICLR 2024. | arXiv:2208.02814 | arXiv API [verified]; venue per r2 note |
| 10 | Bates, S., Angelopoulos, A., Lei, L., Malik, J., Jordan, M. I. (2021). Distribution-free, risk-controlling prediction sets. Journal of the ACM 68(6):1–34. | doi:10.1145/3478535; arXiv:2101.02703 | Crossref + arXiv [verified] |
| 11 | Podkopaev, A., Ramdas, A. (2022). Tracking the risk of a deployed model and detecting harmful distribution shifts. ICLR 2022. | arXiv:2110.06177 | arXiv API (comment "Accepted … ICLR 2022") [verified] |
| 12 | Waudby-Smith, I., Ramdas, A. (2024). Estimating means of bounded random variables by betting. JRSS-B 86(1):1–27. | doi:10.1093/jrsssb/qkad009; arXiv:2010.09686 | Crossref + arXiv [verified] |
| 13 | Ramdas, A., Grünwald, P., Vovk, V., Shafer, G. (2023). Game-Theoretic Statistics and Safe Anytime-Valid Inference. Statistical Science 38(4):576–601. | doi:10.1214/23-STS894; arXiv:2210.01948 | Crossref + arXiv [verified] |
| 14 | Shin, J., Ramdas, A., Rinaldo, A. (2023). E-detectors: A Nonparametric Framework for Sequential Change Detection. New England Journal of Statistics in Data Science, pp. 229–260. | doi:10.51387/23-nejsds51; arXiv:2203.03532 | Crossref + arXiv [verified]; volume/issue not returned by Crossref |
| 15 | Xu, Z., Karampatziakis, N., Mineiro, P. (2024). Active, anytime-valid risk controlling prediction sets. NeurIPS 2024. | arXiv:2406.10490 | arXiv API (comment "Accepted to NeurIPS 2024") [verified] |
| 16 | Dodge, H. F. (1943). A Sampling Inspection Plan for Continuous Production. Annals of Mathematical Statistics 14(3):264–279. | doi:10.1214/aoms/1177731420 | Crossref [verified]. CSP-1 mechanics stated from general knowledge; **paper text not read**. |
| 17 | Page, E. S. (1954). Continuous Inspection Schemes. Biometrika 41(1–2):100–115. | doi:10.1093/biomet/41.1-2.100 | Crossref [verified]; text not read |
| 18 | Ding, T., Angelopoulos, A. N., Bates, S., Jordan, M. I., Tibshirani, R. J. (2023). Class-Conditional Conformal Prediction with Many Classes. NeurIPS 2023 [venue unverified; per Rahman et al. references]. | arXiv:2306.09335 | arXiv API [verified]; text not read |
| 19 | Vovk, V., Gammerman, A., Shafer, G. (2005). Algorithmic Learning in a Random World. Springer. | doi:10.1007/b106715 | Crossref (title, year) [verified]; text not read |
| 20 | Barber, R. F., Candès, E. J., Ramdas, A., Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. Annals of Statistics 51(2):816–845. | doi:10.1214/23-AOS2276; arXiv:2202.13415 | Crossref + arXiv [verified]; text not read this round |
| 21 | Hultberg, B., Zachariah, D., Ribeiro, A. H. (2026). Anytime-Valid Conformal Risk Control. | arXiv:2602.04364 | arXiv API [verified]; abstract/§1 only (r2) |
| 22 | Blackwell, D. (1953). Equivalent Comparisons of Experiments. Annals of Mathematical Statistics 24(2):265–272. | — | [unverified this session]; data from Rahman et al. references |
| 23 | Podkopaev, A., Ramdas, A. (2021). Distribution-free uncertainty quantification for classification under label shift. UAI 2021, PMLR 161:844–853. | — | [unverified this session]; data from Rahman et al. references |
