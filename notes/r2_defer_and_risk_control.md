# R2 — Learning to defer, selective prediction and risk control: the statistical basis for WorkTrace's delegation rule (contribution 3)

Round-2 reading note. Written 2026-10-25. Scope: when a system should act autonomously, escalate or refuse, and what guarantees it can give. Covers selective classification and the reject option, learning to defer (L2D), conformal prediction and risk control (CRC, LTT), anytime-valid sequential monitoring, abstention and escalation for LLMs, and a 2024–2026 sweep for LLM-agent work that already does what contribution 3 proposes.

**Verification legend.** [verified] means the bibliographic data was checked in this session against the arXiv API, Crossref, an OpenReview API record, or the official proceedings page (named per item in §9). [venue unverified] means the arXiv record is verified but the venue comes only from the arXiv comment or from citing papers. [not read] means the metadata is verified but the text was not opened. Every item lists the sections actually read.

**Search method.** arXiv API keyword queries (about 40), web search (6 queries), and forward links from the references of the papers read. DBLP blocked automated access, so venues were checked on Crossref, OpenReview and the proceedings pages instead. Full texts came from arXiv PDFs (pdftotext) and the JMLR PDF.

---

## 1. Executive summary (novelty threats first)

1. **The statistical machinery of contribution 3 is not new, and none of it may be claimed.** All of the following already exist: per-group thresholds with exact binomial (Clopper–Pearson) certificates, a Bonferroni split across groups, fixed-sequence testing over thresholds, guarantees on the selective risk P(error | act), and anytime-valid e-processes for later monitoring. Sources: Geifman & El-Yaniv 2017; LTT (Angelopoulos et al. 2021/2025); Trust or Escalate (ICLR 2025); Conformal Selective Acting 2026.
2. **Closest technical threat: Role-Stratified CRC for LLM tool calls (arXiv:2607.24343, Jul 2026).** It calibrates conformal risk control separately for each stratum (the semantic role of a tool-call argument). It gives a simultaneous Clopper–Pearson + Bonferroni certificate across strata and pools rare strata. It proves a "price of coarseness" result: a pooled guarantee lets a rare stratum's violation rate reach α/p_r. Its violation label is evidence-based: untrusted input changed a field. It does **not** grant or revoke autonomy over a *decision class*. It does not test whether the agent's behaviour depends on the declared grounds, and it has no outcome-only comparison and no revocation.
3. **Execute/abstain with CRC for agents: CORA (arXiv:2604.09155, Apr 2026).** It calibrates a per-action execute/abstain threshold for GUI agents with CRC on a *harm* label and reports safety–helpfulness–interruption frontiers. The guarantee is in expectation, on the joint rate P(harm ∧ execute), and pooled over all actions. There are no per-class grants and no basis/justification label.
4. **"Right answer on the wrong basis" as a loss already appears in ToolChain-CRC (arXiv:2606.18467, Jun 2026).** It controls a trajectory loss that counts upstream unsupported retrieval or tool failure even when the final answer looks fine, and proves that final-answer-only calibration misses this. Its labels come from audits and validators, not from interventions on the agent's evidence. Its unit is a single run, not a decision class.
5. **"Certified autonomy" is already used as a phrase.** Shen 2026 (arXiv:2608.05064) "grants autonomy" per model–task pair via union-corrected Clopper–Pearson on *answer correctness*. That is exactly WorkTrace's **outcome-only baseline**, which helps the framing but means WorkTrace must not claim "certified autonomy" as a new idea.
6. **Revocation by sequential monitoring is prior art.** Sources: Podkopaev & Ramdas 2022 (sequential tests for harmful risk increase); Conformal Selective Acting 2026 (per-threshold e-processes on selective risk for a deployment stream); ToolChain-CRC (anytime escalation alarm within a run).
7. **What remains open (after this sweep).** No paper found does all four of the following:
   - (i) grants autonomy **per decision class** as a revocable, agent-level status;
   - (ii) uses a loss defined by **interventions on external evidence** (wrong action OR right action on a wrong basis, with redundancy handled);
   - (iii) compares this against an **outcome-only rule on the same machinery** at matched coverage on held-out episodes;
   - (iv) closes the loop with **anytime-valid revocation and re-grant**.

   The novelty must sit in the loss, the unit and the empirical comparison, not in the statistics.
8. **Main honesty risk.** Every guarantee here is a statement about the *generator* distribution. Moving from generated to real episodes breaks exchangeability. WorkTrace must state "certified on the generator, validated on N real episodes" and never claim a real-world certificate it does not have (§4).

---

## 2. Reading coverage

| Work | What was read in this session |
|---|---|
| Chow 1970 | **Not read** (IEEE paywall). Metadata verified. Known only through the summaries in El-Yaniv & Wiener §1 and Madras et al. §4. |
| El-Yaniv & Wiener 2010 | Abstract, §1, §2 (definitions), start of §3. |
| Geifman & El-Yaniv 2017 | Full text up to §5.2 (problem, SGR algorithm, Lemma 3.1, Thm 3.2, CIFAR tables). |
| Hendrickx et al. survey | **Not read**. Metadata verified. |
| Madras, Pitassi & Zemel 2018 | Abstract, §1, §2.2–2.4 (loss definitions, equivalence proof), §3 fragments. |
| Mozannar & Sontag 2020 | Abstract, §1, §3 (problem formulation), §4 statement of L_CE and Thm 1, §5.1. |
| Angelopoulos & Bates (Gentle Intro) | ToC, §4.1 (group-balanced), §4.6 (drift), §5.5 (selective classification). |
| Conformal Risk Control | §1–2.4, §4.1–4.2 (shift, TV bound, quantile risk). |
| Learn then Test | §1–2.2, §2.3 (FWER definitions, fixed-sequence statement), §3.2 (selective classification). |
| Podkopaev & Ramdas 2022 | Abstract, §2 (Alg. 1, Prop. 1, Remarks 1–3). |
| Hultberg et al. 2026 (anytime CRC) | Abstract, §1. |
| Waudby-Smith & Ramdas; Howard et al.; Ramdas et al. SAVI; Vovk & Wang; Shafer 2021; Grünwald et al. | **Not read**. Metadata verified. Cited only as the standard references named by the papers that were read. |
| Xu et al. 2024 (A-RCPS) | **Not read**. Characterised only through Conformal Selective Acting §3. |
| KnowNo (Ren et al. 2023) | §3.2–3.3 (Props 1–2). |
| Introspective Planning (Liang et al.) | **Not read**. Metadata verified. |
| Conformal abstention (Yadkori et al.) | Abstract, §2 statement of the guarantee (E[R] ≤ α), Prop. 3.1 statement. |
| Conformal Alignment (Gui et al.) | Abstract. |
| Trust or Escalate (Jung et al.) | §2–2.1, Thm 1, App. A.1 start. |
| Role-Stratified CRC (2607.24343) | Abstract, intro, related work, problem setup, aggregate-budget failure (Props 1–2, Thm 1), method incl. Alg. 1 and Thm 2. Experiments only via Table 1 and the text around it. |
| CORA (2604.09155) | Abstract, §1–5.2, Tables 1–3, App. F.5 fragment. |
| ToolChain-CRC (2606.18467) | Abstract, §1–5 (Prop 1, Thm 1, Props 2–3). **Not** the anytime-alarm proof or the experiments. |
| Conformal Selective Acting (2605.20270) | Abstract, §1–5.2 (framework table, e-process, Thm 5.1, Thm 5.3). Not the experiments. |
| Shen 2026 (2608.05064) | Abstract, Prop. 3, §4.4. |
| Strategic Decision Support (2606.12587) | Abstract, §1–4 opening (SDS-Opt, Thm 3.1, online protocol). |
| Think Short, Defer Smart (2607.26865) | Abstract, §1 opening, Prop. 1 statement (via search). |
| SafeCommit (2608.04289) | Abstract, §1–2.4, §3.1 opening. |
| Calibration Is Not Control (2606.21399) | Abstract, §1–2.2. |
| Oversight Has a Capacity (2606.08919) | Abstract, §1–3, references. |
| Calibrating Conservatism / CCO (2605.28807) | Abstract, §1. |
| ReDAct (2604.07036) | Abstract, §4.2 (threshold selection, via search). |
| Bayesian Self-Escalation (2608.24087); To Ask or Not to Ask (2510.08314); G-CARB (2610.05563); LLMCert-T (2510.03992); ABC II (2608.12895); E-valuator (2512.03109); PACE (2606.08106); Ramaswamy 2026; Right-for-Wrong-Reasons (2601.00513); PPRM (2602.02229); Fernandez P8 (2610.00787); Domain-Conditioned Safety (2606.05233); Calibration & Risk-Budgeted Decisions (2610.19811); CCPO (2511.11828); Anytime Contracts (2610.22781) | Abstract / first page only. |

---

## 3. (a) Formalisation proposal for WorkTrace's delegation rule

The notation is meant to drop straight into the paper. Every design choice names the work that licenses it.

### 3.1 Objects

- **Agent configuration** π, including model version, prompt and tools. Every guarantee is indexed by π. Any change to π voids the certificate. This mirrors Conformal Selective Acting §2: a test calibrated on an earlier score map "targets a probability measure distinct from the one governing subsequent rounds".
- **Decision classes** 𝒞 = {1,…,C}: a fixed partition of decision situations. Each class has an operational membership rule κ(E) ∈ 𝒞 that is computable **at decision time** from (context, permissions, available information) alone, never from the outcome. Statistically the classes are the *groups* or *strata* of Mondrian / group-balanced conformal prediction (Gentle Intro §4.1; Vovk et al. 2005). The classes must be fixed **before** any calibration label is seen (see §4, A6).
- **Episode** E = (C, I, P, G, A, O) as in the paper. A = a(E) is the agent's action, chosen from the set {domain actions} ∪ {escalate, refuse}.
- **Normative action map** A*(E) ⊆ 𝒜: the set of correct actions. In generated episodes it is known by construction. It may contain *escalate*, for example when the decisive evidence is missing.
- **Intervention family** 𝓘(E) = {do_j}: operators on *external* evidence (remove X, only X, invert X, add an independent second source). Each operator yields a variant episode do_j(E). The generator also knows A*(do_j(E)), so the normative response to every intervention is known by construction. This is what makes the loss below computable without an LLM judge, and it handles redundancy: if a redundant source remains after "remove X", A* does not change, so an agent that keeps its answer is not penalised.

### 3.2 Losses

Two losses are defined on the same episodes. Using two losses on identical statistical machinery is the clean way to set up H3.

- **Outcome loss:** ℓ_out(E) = 1[a(E) ∉ A*(E)].
- **Basis (justification) loss:** ℓ_basis(E) = 1[∃ j ∈ 𝓘(E): a(do_j(E)) ∉ A*(do_j(E))]. The action fails to track the evidence the way the normative model requires: it ignores an inversion, survives the removal of the only support, or changes when an irrelevant or redundant item is perturbed. Optionally, add a declared-grounds clause: the items in G are not among the items whose intervention changes A*.
- **WorkTrace loss ("unjustified action"):** ℓ_WT(E) = max(ℓ_out, ℓ_basis), so ℓ_WT ≥ ℓ_out pointwise.
  - This is a *counterfactual-correctness* loss over a pre-registered intervention family. It is the evidence-side analogue of ToolChain-CRC's trajectory loss R^traj = 1{U or V} (its Prop. 1), but measured by intervention rather than by audited step labels.
  - **What the guarantee is about.** It always holds *relative to 𝓘*. Unjustified behaviour on features no intervention probes is invisible to it.

The loss counts only actions the agent takes autonomously. Escalate and refuse do not count as "unjustified actions"; they are charged through cost (§3.6).

### 3.3 The certified quantity: class-conditional selective risk

For class c and an optional within-class readiness threshold λ (selection g_λ(E) = 1[s(E) ≥ λ], where s is any score, e.g. agent confidence or the stability of its answer across interventions):

  R_c(λ) := P( ℓ_WT(E) = 1 | g_λ(E) = 1, κ(E) = c ),   φ_c(λ) := P( g_λ(E) = 1 | κ(E) = c ).

The pure per-class rule (the whole class is either autonomous or not) is the special case λ = −∞, φ_c = 1.

- **Conditional, not joint.** R_c is the *selective* risk P(unjustified | autonomous, class c), the El-Yaniv & Wiener §2 definition R(f,g) = E[ℓ·g]/Φ.
  - CORA and Role-Stratified CRC instead certify the *joint* rate P(harm ∧ execute), which is smaller by a factor of the coverage.
  - The two are not interchangeable: "Selective risk is not derivable from marginal risk; a different statistic is required" (Conformal Selective Acting §3.1). The brief's target "P(unjustified action | autonomous, class c)" is the conditional quantity, so the paper must use that.
- **High probability, not expectation.** Conformal risk control gives E[L_{n+1}(λ̂)] ≤ α, averaged over calibration draws. Hultberg et al. 2026 §1 note that for n = 500 "there is a 48% chance of drawing D_n such that the rate exceeds the specified α".
  - A certification claim that issues a grant therefore needs the (α, δ) form of LTT Def. 1: "P(R(T_λ̂) ≤ α) ≥ 1 − δ".
  - Selective risk is also non-monotone in λ, so plain CRC does not apply. See CRC §2.4 ("if the risk is non-monotone, then this algorithm does not control the risk") and Gentle Intro §5.5 ("not guaranteed that model accuracy is monotone in the cutoff λ"). LTT and SGR handle it.

### 3.4 Certification (grant) procedure

**Inputs.** For each class c: calibration episodes D_c (one per independent generator template/seed; see §4, A3), the loss ℓ_WT, a pre-specified finite grid Λ_c = {λ_1 > λ_2 > … > λ_m} running from most to least conservative, targets α_c, and an overall error δ.

For each (c, λ):
- n_c(λ) = number of episodes in D_c with g_λ = 1;
- k_c(λ) = number of those with ℓ_WT = 1;
- **p-value** p_{c,λ} = P( Bin(n_c(λ), α_c) ≤ k_c(λ) ).

This is the exact binomial (Clopper–Pearson) p-value for H_{c,λ}: R_c(λ) > α_c. It is valid conditional on n_c(λ), by the conditioning argument in the proof of Geifman & El-Yaniv's Thm 3.2. LTT §3.2 and Trust or Escalate §2.1 use the same construction.

**Multiplicity.**
- *Within a class:* fixed-sequence testing along Λ_c (LTT §2.3.1; Trust or Escalate §2.1). Test λ_1, λ_2, … at level δ_c and stop at the first non-rejection. There is no multiplicity cost along the sequence.
- *Across classes:* Bonferroni δ_c = δ/C, or an allocation chosen on an independent split (Role-Stratified CRC, "Independent confidence allocation").
- **Output:** the grant set Ĝ = {c : at least λ_1 rejected}, and for c ∈ Ĝ the threshold λ̂_c = the last rejected λ in the sequence.

**Proposition (per-class delegation guarantee).** Assume:
- the episodes in D_c are i.i.d. draws from the class-c episode distribution P_c of the generator, and future class-c episodes are drawn from the same P_c;
- κ is fixed in advance, Λ_c is fixed in advance or depends only on unlabelled scores (Shen 2026, Remark 2), and π is fixed.

Then

  P( ∃ c ∈ Ĝ : R_c(λ̂_c) > α_c ) ≤ δ.

Equivalently, with probability ≥ 1 − δ over the calibration data, *every* class in which the agent is granted autonomy has P(unjustified | autonomous, class c) ≤ α_c simultaneously.

*Proof sketch.* Each p_{c,λ} is super-uniform under H_{c,λ}, conditional on n_c(λ) (Geifman & El-Yaniv, proof of Thm 3.2). Fixed-sequence testing controls the FWER within c at level δ_c (LTT Prop. 3). A union bound across classes gives δ (LTT Thm 1 with Bonferroni; same structure as Role-Stratified CRC Thm 2). ∎

This is a direct instance of LTT and SGR. **The paper must present it as an application, not a contribution.**

**Three-way rule.** Two one-sided tests per class give a principled proceed / escalate / refuse mapping:
- **proceed**: c ∈ Ĝ (upper bound ≤ α_c);
- **refuse**: the lower Clopper–Pearson bound on R_c exceeds a higher level β_c. The agent is certified *bad* in class c, so it should not even draft or propose there (the class is removed from its permissions). The p-value is P(Bin(n, β_c) ≥ k), and the second family needs its own δ budget.
- **escalate**: otherwise (insufficient evidence either way).

Alternatively, if "refuse" in WorkTrace means the *agent* refusing an out-of-permission action, then refuse is part of A* and is certified like any other action. **Decision needed: pick one meaning and state it.**

**Outcome-only baseline.** The identical procedure with ℓ_out in place of ℓ_WT. This is exactly what Shen 2026 calls granting "certified autonomy". Because ℓ_WT ≥ ℓ_out, the WorkTrace grant set is (at matched α) a subset of the outcome-only grant set. The empirical question is whether the extra classes the outcome-only rule admits are the ones that fail on held-out or shifted episodes (§3.7).

### 3.5 Coverage and risk–coverage curves

- **System-level autonomous coverage** under a deployment class mix w_c: Φ = Σ_c w_c · 1[c ∈ Ĝ] · φ_c(λ̂_c).
- **Realised held-out unjustified rate among autonomous actions:** R̄ = Σ_c w_c 1[c∈Ĝ] φ_c R_c / Φ.
- **Curve:** sweep α (and/or the within-class λ) and plot (Φ, R̄) on held-out episodes for the WorkTrace rule and the outcome-only rule. This is the risk–coverage curve of El-Yaniv & Wiener §2 and Geifman & El-Yaniv §4, lifted to a delegation policy.
- **Reporting.** Report per-class curves as well as the pooled one. Role-Stratified CRC (Prop. 1) shows why: a pooled guarantee α implies only R_c ≤ α / w_c for a class of prevalence w_c, so rare high-stakes classes can be badly violated under a pooled certificate. This is a good argument for per-class certification; cite it.

### 3.6 Escalation cost

The delegation decision has a cost side that the risk constraint does not capture. Learning-to-defer supplies the vocabulary:
- the system loss mixes the machine's loss on non-deferred cases with the *expert's* loss on deferred ones (Mozannar & Sontag eq. 1–3);
- a constant deferral cost recovers rejection learning (Madras et al. §2.3–2.4: "rejection learning is exactly a special case of learning to defer: a DM with constant loss α on each example").

Proposed expected cost per episode:

  J = Σ_c w_c [ 1[c∈Ĝ] ( φ_c L_c R_c + (1−φ_c)(κ_c + h_c L_c) ) + 1[c∉Ĝ] ( κ_c + h_c L_c ) ],

where:
- L_c = harm of one unjustified action in class c;
- κ_c = escalation cost (reviewer time, latency);
- h_c = reviewer error rate on escalated class-c cases. It is not zero: KnowNo's guarantee holds only "under the assumption of accurate human help" (§3.2).

Optional extensions:
- **Capacity:** Σ_c w_c (1 − 1[c∈Ĝ] φ_c) ≤ B (workload-constrained L2D; Alves et al., cited, not read).
- **Fatigue:** h_c increasing in escalation load (FALCON; Turan 2026 reports that "more human oversight can make a system less safe", from a model, not a human study).

**Decision rule.** Risk is the hard constraint, cost is the objective among certified options. LTT §2.1 explicitly allows choosing "any λ ∈ Λ̂ … (even in a data-driven way)". ToolChain-CRC Prop. 2 shows that utility-aware selection inside the feasible set preserves the guarantee.

**Reporting.**
- Cost-adjusted curves for a few ratios κ/L (e.g. 0.01, 0.1, 1).
- The escalation count at matched coverage.
- *Value of the escalation channel*: Calibration Is Not Control (NeurIPS 2026) shows that states with equal failure risk differ in whether intervention helps. A cost model that charges escalation uniformly may misstate the value of the WorkTrace rule, so note it as a limitation.

### 3.7 Held-out evaluation and the H3 test (avoiding circularity)

**Circularity risk.** If the WorkTrace rule is calibrated on ℓ_WT and then *evaluated* on ℓ_WT, it wins by construction: the outcome-only rule was never asked to control ℓ_basis. A fair H3 needs an evaluation target that neither rule was calibrated on.

**Recommended primary endpoint: outcome errors under evidence shift.** Use held-out episodes from the same classes in which shortcut cues are broken (decoy evidence, redundancy removed, decisive item inverted), generated with fresh hidden seeds. Measure ℓ_out there.

**H3 (predictive form).** At matched autonomous coverage Φ, the WorkTrace rule yields a lower held-out outcome-error rate under evidence shift than the outcome-only rule. The secondary endpoint is ℓ_WT on held-out data with no shift.

**H3 fails if** the two rules give statistically indistinguishable held-out outcome-error rates at matched Φ. Use a pre-registered paired test across classes and configurations.

### 3.8 Revocation and re-grant (sequential monitoring)

After a grant, class c runs autonomously and a **random audit** is drawn: each autonomous episode is audited independently with probability r_c, decided before seeing anything about the episode. Audited episodes get X_t = ℓ_WT, via replay with interventions where the environment allows it; otherwise X_t = ℓ_out and the certificate is downgraded accordingly. Random selection is what keeps the audited stream unbiased. The same principle drives the randomised exploration in Strategic Decision Support §4 and the labelled/unlabelled split in PPRM.

**Revocation test.** H0^rev_c: E[X_t | F_{t−1}] ≤ α'_c for all t (still safe). Use the betting e-process

  M_t = ∏_{s≤t} (1 + λ_s (X_s − α'_c)),  λ_s ∈ [0, 1/α'_c), λ_s predictable.

Under H0 this is a nonnegative supermartingale. **Revoke** at the first t with M_t ≥ 1/δ_rev. By Ville's inequality, P_{H0}(ever revoke) ≤ δ_rev under continuous monitoring. This is the "probability of ever raising a false alarm" property of Podkopaev & Ramdas (Remark 3) and the e-process construction quoted in Conformal Selective Acting §4.2 (attributed there to Waudby-Smith & Ramdas). Podkopaev & Ramdas give a version relative to the calibration bound, H0: R_T ≤ R_S + ε_tol (their eq. 1, Alg. 1). It fits "revoke when deployment risk exceeds the certified level by more than a tolerance".

**Within-class selection.** If a within-class threshold λ is used, monitor the *gated* increment A_t(X_t − α'), not the raw one (Conformal Selective Acting §3.1, §4.2).

**Hysteresis.** Grant at α_c and revoke at α'_c > α_c (e.g. 0.05 / 0.10). Otherwise a class whose true rate sits at α flaps between states.

**Re-grant.** After a revocation the class returns to *escalate*. Re-grant needs fresh evidence. Use either a new batch certificate (§3.4) or the anytime-valid grant test from Conformal Selective Acting: for H0^unsafe: E[X] ≥ α, the process K_t = ∏(1 + λ_s(α − X_s)), λ_s ∈ [0, 1/(1−α)], certifies once K_t ≥ 1/δ.
- With a clean run and maximal bet, K_t ≥ 1/δ exactly when (1−α)^{−t} ≥ 1/δ. That is the same n as the zero-failure Clopper–Pearson bound (59 at α = δ = 0.05), so anytime validity costs nothing in the clean case.
- The maximal bet is destroyed by a single failure, though, so use a plug-in bet (Conformal Selective Acting eq. 2).

**Agent updates.** Any change to π resets the class to *escalate*. A changed π is a different agent; Conformal Selective Acting's "predictable pipeline" assumption formalises why.

**Simulation in this session** (§5.4). With a Kelly bet tuned to 2α′:
- the false-revocation rate at the boundary p = α′ was ≤ δ, as theory requires (0.037 and 0.028 at δ = 0.05);
- when the true rate doubles, the median detection delay is about 113 audited episodes at α′ = 0.05 and about 57 at α′ = 0.10.

At a 10% audit rate that is about 1,100 and 570 autonomous episodes respectively. **Revocation is slow unless audits are frequent or failures are frequent.** This is an honest limitation and an argument for higher audit rates in high-stakes classes.

---

## 4. (b) Assumptions that break the guarantees, and how to state them

| # | Assumption | What breaks | Mitigation / honest statement |
|---|---|---|---|
| A1 | **Exchangeability (i.i.d.) between calibration and future episodes within a class** | All of §3.4. Every reviewed method needs it (CRC Thm 1; LTT §1.1 "i.i.d."; Role-Stratified "Under exchangeability between calibration and test fields"; CORA §3.4). | Generate calibration and held-out episodes with independent hidden seeds from the same generator. State: *"guarantees hold for episodes drawn from generator G with seeds independent of calibration."* |
| A2 | **Generated vs real episodes (the sim-to-real gap)** | The certificate is about P_gen,c, not P_real,c. For a [0,1] loss, \|E_real ℓ − E_gen ℓ\| ≤ TV(P_gen,c, P_real,c) (cf. CRC Prop. 3: E L ≤ α + B Σ TV). The TV distance is unknown and can be close to 1. **Selective (conditional) risk is more fragile still**, because the selected subset can shift too. Weighted / covariate-shift CRC (CRC §4.1; Tibshirani et al. 2019) needs P_real ≪ P_gen, a known or estimable likelihood ratio, *and an unchanged conditional law of the label given the covariates*. The last is implausible here, because the label is the agent's own behaviour on different evidence. | Do **not** claim a real-world certificate. Report: (i) the generator certificate; (ii) a *separate* small real-episode validation with its own Clopper–Pearson interval, typically wide (see §5); (iii) the sequential audit monitor (§3.8), which is the only mechanism that tracks real deployment risk. PPI (Angelopoulos et al. 2023) does **not** fix this: it needs the large unlabelled set to come from the *target* distribution, not the generator. Suggested wording: *"Our guarantees are distribution-free relative to the episode generator; they transfer to deployment only insofar as deployment episodes of class c are exchangeable with generated ones, which we cannot verify and partially probe with N real episodes."* |
| A3 | **Independence of calibration units** | Several episodes from one template/seed, or several decisions within one trajectory, are correlated. n then overstates the effective sample size and Clopper–Pearson is anti-conservative. Role-Stratified CRC warns that "n_r can overstate the effective sample size" and offers a one-per-episode variant. CORA uses blockwise / episode-level splits. | Make the template/seed the unit: one scored decision per independent template per class, or cluster-level aggregation. Report the effective n. |
| A4 | **Validity of the loss (interventions)** | ℓ_WT is relative to the intervention family 𝓘. Untested dependencies are invisible. In generated episodes A* is exact; in real episodes intervention replay may be impossible (no counterfactual environment), so ℓ_basis is unobserved. If the measured label detects an unjustified action with sensitivity s < 1, then the observed rate q ≈ s·p and certifying q ≤ α does not certify p ≤ α. | Pre-register 𝓘 per class. State the guarantee as "unjustified **with respect to 𝓘**". Estimate s on generated episodes where ground truth is known, and certify q ≤ s_min·α. Example: s = 0.8, α = 0.05 means certifying q ≤ 0.04, which needs n ≥ 74 clean episodes instead of 59 (α = δ = 0.05). |
| A5 | **Goodhart / adaptivity** | If the agent or its developers tune against the generator or the calibration episodes, future episodes stop being exchangeable with calibration ones. | Hidden seeds, held-out templates, a frozen π, re-certification after any change (Conformal Selective Acting's "predictable pipeline"). |
| A6 | **Class definition fixed in advance and computable at decision time** | Data-dependent class merging or splitting after seeing labels invalidates the error accounting. Misrouting (κ wrong at decision time) mixes classes, so P(unjustified \| assigned c) ≠ R_c. | Freeze κ before calibration. If rare classes must be pooled, decide on an independent allocation split (as Role-Stratified CRC does). Report the misrouting rate. |
| A7 | **Multiplicity** | Per-class claims at level δ do not give a simultaneous claim across classes, configurations or α levels. | Bonferroni δ/C for "all granted classes" (Prop. §3.4). Pre-specify α. If several α values are reported, treat them as a curve, not as separate certificates. |
| A8 | **Rare classes** | The smallest certifiable α is about 1/(n_c+1) for CRC, and from Clopper–Pearson it follows from §5. Rare classes cannot be certified at strict α. | Pool into a "high-risk residual" class (pooled certificate only). Otherwise default to escalate; refusal to certify is an informative output (Shen §4.4). |
| A9 | **Non-stationarity after the grant** | The batch certificate says nothing about drift. Ville-based monitoring controls false revocation under H0 but has a detection delay (§3.8). If p_t drifts, "risk" means running risk (Podkopaev & Ramdas eq. 2, independence only). | Revocation e-process + hysteresis + audit rate set per class stake. State the expected detection delay. |
| A10 | **Expectation vs high probability** | CRC-type statements are in expectation over calibration sets, not per realised calibration (Hultberg et al.). | Use the (α, δ) form for grants. Never phrase a CRC result as "with probability ≥ 1−δ". |
| A11 | **Joint vs conditional risk** | CORA's "no more than 1% of autonomous actions are harmful" (§3.4) is a joint-rate guarantee E[ℓ·1{execute}] ≤ α, not a rate among executed actions. Misreading it overstates safety by a factor 1/coverage. | WorkTrace certifies the conditional rate (§3.3) and says so explicitly. |
| A12 | **Human oracle** | L2D and KnowNo-style guarantees assume a fixed or accurate expert. Reviewers disagree (Fleiss κ = 0.52 on agent-action risk; Turan 2026) and fatigue. | Charge h_c > 0 in the cost model. Do not claim system-level guarantees for escalated cases. |

**Limitation paragraph template.** *"All certificates are statements about episodes drawn from our generator, conditional on a fixed agent configuration, a pre-registered intervention family, and a decision-class map fixed before calibration. They do not transfer to real deployments without an exchangeability assumption we cannot test. The real-episode validation (N = …) is descriptive, and the sequential monitor is the only mechanism that tracks deployment risk, with detection delays reported in §… ."*

---

## 5. (c) Minimal sample sizes

All numbers were computed in this session with exact binomial tails (pure Python; scripts in the scratchpad, `bin/samples.py`, `bin/power6.py`, `bin/eproc.py`). n counts **autonomously handled, independent** calibration episodes in the class (the denominator of the selective risk). If only a fraction φ of the class is autonomous, the class needs n/φ episodes.

### 5.1 Smallest n such that the one-sided (1−δ) Clopper–Pearson upper bound is ≤ α, given k observed unjustified actions

| α | δ | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 |
|---|---|---|---|---|---|---|---|
| 0.05 | 0.10 | 45 | 77 | 105 | 132 | 158 | 184 |
| 0.05 | 0.05 | **59** | 93 | 124 | 153 | 181 | 208 |
| 0.05 | 0.01 | 90 | 130 | 165 | 198 | 229 | 259 |
| 0.10 | 0.10 | 22 | 38 | 52 | 65 | 78 | 91 |
| 0.10 | 0.05 | **29** | 46 | 61 | 76 | 89 | 103 |
| 0.10 | 0.01 | 44 | 64 | 81 | 97 | 113 | 127 |

For k = 0 the closed form is n ≥ ln δ / ln(1−α), roughly the "rule of three" n ≈ 3/α at δ = 0.05.

### 5.2 With multiplicity (Bonferroni δ/C, C = 6 classes; and additionally δ/(6·10) for a 10-point threshold grid tested with Bonferroni instead of fixed-sequence)

| α | δ | correction | k=0 | k=1 | k=2 | k=5 |
|---|---|---|---|---|---|---|
| 0.05 | 0.10 | C=6 | 80 | 119 | 153 | 243 |
| 0.05 | 0.05 | C=6 | **94** | 135 | 170 | 264 |
| 0.05 | 0.05 | C=6 × grid 10 | 139 | 185 | 225 | 329 |
| 0.10 | 0.10 | C=6 | 39 | 58 | 75 | 120 |
| 0.10 | 0.05 | C=6 | **46** | 66 | 83 | 130 |
| 0.10 | 0.05 | C=6 × grid 10 | 68 | 91 | 110 | 162 |

Fixed-sequence testing over the grid avoids the grid factor (LTT §2.3.1), so the "C=6" rows apply.

### 5.3 What n buys: upper bound after n clean episodes (k = 0, δ = 0.05)

| n | 10 | 20 | 30 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|---|---|
| 95% upper bound | 0.259 | 0.139 | 0.095 | 0.058 | 0.030 | 0.015 | 0.006 |

### 5.4 Power: n needed so that P(certify) ≥ 0.8 when the true unjustified rate is p (δ = 0.05)

| α | correction | p = 0 | p = 0.01 | p = 0.02 | p = 0.03 | p = 0.05 |
|---|---|---|---|---|---|---|
| 0.05 | single class | 59 | 124 | 234 | 601 | — |
| 0.05 | C = 6 | 94 | 203 | 405 | 1030 | — |
| 0.10 | single class | 29 | — | 61 | — | 179 |
| 0.10 | C = 6 | 46 | — | 100 | — | 304 |

Coverage scaling: for α = δ = 0.05, k = 0, the class needs 59 / 74 / 118 / 197 episodes at φ = 1 / 0.8 / 0.5 / 0.3.

**Revocation (simulation, 1,000 streams, horizon 3,000 audited episodes, δ = 0.05, Kelly bet tuned to 2α′).**

| α′ | true p | P(revoke) | median delay | 90th pct |
|---|---|---|---|---|
| 0.05 | 0.025 | 0.000 | — | — |
| 0.05 | 0.05 (boundary) | 0.037 | — | — |
| 0.05 | 0.10 | 1.0 | 113 | 302 |
| 0.05 | 0.15 | 1.0 | 48 | 96 |
| 0.10 | 0.05 | 0.000 | — | — |
| 0.10 | 0.10 (boundary) | 0.028 | — | — |
| 0.10 | 0.20 | 1.0 | 57 | 158 |
| 0.10 | 0.30 | 1.0 | 25 | 47 |

A predictable plug-in bet gave similar validity and somewhat slower detection at 2α (median 221 / 85).

### 5.5 Implications for the pilot (≈6 classes × 2–3 agent configurations)

- **α = 0.10, δ = 0.05, simultaneous over 6 classes** is the realistic headline. The floor is 46 clean autonomous episodes per class. For 80% power at a true rate of 2% it is about 100. With ~100 calibration + ~100 held-out per class per configuration, that is about 1,200 base episodes per configuration. Multiplied by |𝓘| ≈ 4–5 intervention variants, it is about 5–6k agent runs per configuration.
- **α = 0.05** is feasible only for classes where the agent is near-perfect (true p ≲ 1%; ~200 per class with C = 6). Present it as a stretch result.
- **Real-episode validation** at these sizes is descriptive only. For example, 30 clean real episodes give an upper bound of 0.095. State this.

---

## 6. Notes on individual works

### 6.1 Foundations: selective classification and the reject option

#### Chow (1970)
- **Bibliographic data:** C. K. Chow. "On optimum recognition error and reject tradeoff." *IEEE Transactions on Information Theory* 16(1):41–46, 1970. doi:10.1109/TIT.1970.1054406. [verified, Crossref] **[not read]**.
- **Problem & contribution:** per El-Yaniv & Wiener §1 and Madras et al. §4, the Bayes-optimal reject rule when the distributions are known, and the error–reject tradeoff.
- **Method / Evaluation:** not read.
- **WorkTrace must NOT claim:** the reject option or the error–reject tradeoff.
- **Leaves open:** finite-sample guarantees, groups, and agents.
- **Differentiation:** "Classic reject-option theory (Chow, 1970) optimises when to abstain given known class posteriors; WorkTrace asks when an agent may act unsupervised in a decision class, given finite tested evidence of how it handles evidence."
- **Cautions:** cite only for the concept.

#### El-Yaniv & Wiener (2010)
- **Bibliographic data:** Ran El-Yaniv, Yair Wiener. "On the Foundations of Noise-free Selective Classification." *JMLR* 11(53):1605–1641, 2010. [verified, jmlr.org page + PDF].
- **Problem & contribution:** characterises the risk–coverage (RC) trade-off; theory for the realizable (noise-free) case, including "perfect learning".
- **Method:** a selective classifier (f, g) with coverage Φ = E[g(X)] and risk R = E[ℓ·g]/Φ (§2, Defs 1–2). Positive results take the form Pr{R ≤ B_R ∧ Φ ≥ B_Φ} ≥ 1−δ.
- **Evaluation:** theory.
- **WorkTrace must NOT claim:** the coverage / selective-risk definitions or the RC curve.
- **Leaves open:** agnostic and noisy settings (later work), groups, sequential settings.
- **Differentiation:** use as the definitional citation for R_c and φ_c.
- **Cautions:** the realizable-case results do not apply to WorkTrace. Cite it for the definitions only.

#### Geifman & El-Yaniv (2017), SGR
- **Bibliographic data:** Yonatan Geifman, Ran El-Yaniv. "Selective Classification for Deep Neural Networks." *NeurIPS 30 (NIPS 2017)*. arXiv:1705.08500. [verified, arXiv API + papers.nips.cc page].
- **Problem & contribution:** given a trained classifier and a confidence function κ, learn a threshold so that the selective risk is ≤ r* with probability ≥ 1−δ, maximising coverage.
- **Method:** SGR (Alg. 1): binary search over thresholds, each with the exact binomial bound B* (Lemma 3.1, "the tightest possible numerical generalization bound"), union bound over ⌈log₂ m⌉ steps (Thm 3.2). The proof conditions on the number of accepted points, which is the argument that makes per-class conditional certificates valid.
- **Evaluation:** CIFAR-10/100, ImageNet. For example, CIFAR-10 at δ = 0.001: desired risk 0.01 gives test risk 0.0092 at coverage 0.786 (Table 1). They report that "an unprecedented 2% error in top-5 ImageNet classification can be guaranteed with probability 99.9%, and almost 60% test coverage" (abstract).
- **WorkTrace must NOT claim:** high-probability selective-risk control by threshold calibration with binomial bounds.
- **Leaves open:** groups/classes, non-classification actions, the basis of the decision, sequential settings.
- **Differentiation:** "WorkTrace applies SGR/LTT-style selective-risk certification per decision class, with the loss redefined from prediction error to interventionally measured unjustified action."
- **Cautions:** the footnote in §5.2 says no Bonferroni correction was applied across the reported table rows. Use a cleaner procedure (fixed sequence).

#### Hendrickx, Perini, Van der Plas, Meert & Davis (2024): survey
- **Bibliographic data:** "Machine learning with a reject option: a survey." *Machine Learning* (2024). doi:10.1007/s10994-024-06534-x. arXiv:2107.11277. [verified, Crossref + arXiv] **[not read]**.
- Cite as the survey entry point for the reject option. All other fields: not read.

### 6.2 Learning to defer

#### Madras, Pitassi & Zemel (2018)
- **Bibliographic data:** David Madras, Toniann Pitassi, Richard Zemel. "Predict Responsibly: Improving Fairness and Accuracy by Learning to Defer." *NeurIPS 31 (2018)*. arXiv:1711.06664. [verified, arXiv API + proceedings.neurips.cc page].
- **Problem & contribution:** a model can say "pass" to an external decision-maker (DM). The decision to pass should depend on the DM's accuracy and biases ("adaptive rejection learning").
- **Method:** L_defer = −Σ[(1−s)ℓ(Y, Ŷ_M) + s ℓ(Y, Ŷ_D) + s γ_defer] (eq. 7); rejection learning uses a constant γ_reject (eq. 4–6). §2.4: "rejection learning is exactly a special case of learning to defer: a DM with constant loss α on each example."
- **Evaluation:** fairness datasets with simulated DMs (high-accuracy, biased, inconsistent). Numbers not extracted.
- **WorkTrace must NOT claim:** that deferral should depend on the downstream human's competence, or a joint system loss.
- **Leaves open:** finite-sample guarantees, classes of decisions, autonomy of agents, evidence-handling.
- **Differentiation:** "Learning to defer optimises per-instance pass decisions against a downstream decision-maker's loss; WorkTrace decides per decision class whether an agent's tested evidence-handling licenses it to act without a human, and certifies that decision."
- **Cautions:** none of note.

#### Mozannar & Sontag (2020)
- **Bibliographic data:** Hussein Mozannar, David Sontag. "Consistent Estimators for Learning to Defer to an Expert." *ICML 2020*, PMLR 119. arXiv:2006.01862. [verified, arXiv API + proceedings.mlr.press/v119 page].
- **Problem & contribution:** learn a classifier h and a rejector r that defers to an expert M, given samples of the expert's decisions. Gives the first consistent convex surrogate for multiclass deferral.
- **Method:**
  - System loss L(h,r) = E[ℓ(x,y,h(x)) 1{r=0} + ℓ_exp(x,y,m) 1{r=1}] (eq. 2). The 0–1 version (eq. 3) adds the expert's misclassification. "setting l_exp(x,y,m) = c for a constant c > 0" recovers rejection learning. Instance-dependent expert costs: ℓ_exp = 1{m≠y} + c(x).
  - Reduction to cost-sensitive learning with surrogate L_CE (Thm 1: convex, upper-bounds L_{0−1}, consistent).
  - Bayes rule (§5.1): defer iff max_y η_y(x) ≤ P(Y = M | X = x).
- **Evaluation:** synthetic, CIFAR-10 with simulated experts, CIFAR-10H, hate speech. Numbers not extracted.
- **WorkTrace must NOT claim:** the system-loss formulation with expert cost, or the Bayes deferral rule.
- **Leaves open:** distribution-free guarantees on the autonomous region, group/class-level autonomy, sequential revocation.
- **Differentiation:** WorkTrace's cost J (§3.6) is the class-level, certification-constrained analogue of the Mozannar–Sontag system loss.
- **Cautions:** consistency is asymptotic. It gives no finite-sample risk bound.

#### Related L2D items (cited for completeness)
All [verified, arXiv API] **[not read]** unless stated.
- Verma & Nalisnick. "Calibrated Learning to Defer with One-vs-All Classifiers." ICML 2022 [venue per arXiv comment]. arXiv:2202.03673.
- Mozannar, Lang, Wei, Sattigeri, Das, Sontag. "Who Should Predict? Exact Algorithms For Learning to Defer to Humans." AISTATS 2023 [venue per arXiv comment]. arXiv:2301.06197.
- Okati, De, Gomez-Rodriguez. "Differentiable Learning Under Triage." arXiv:2103.08902 [venue unverified].
- Leitão, Saleiro, Figueiredo, Bizarro. "Human-AI Collaboration in Decision-Making: Beyond Learning to Defer." ICML 2022 Workshop [venue per arXiv comment]. arXiv:2206.13202. The closest thing to a survey: it critiques L2D's assumptions (an expert prediction on every instance, no capacity limits, static environments).
- Alves et al. "Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints." arXiv:2403.06906 (TMLR 2024 per citing paper; [venue unverified]).
- Zhang, Nguyen, Rosewarne, Wells, Carneiro. "Fatigue-Aware Learning to Defer via Constrained Optimisation." arXiv:2604.00904.
- Lykouris & Weng. "Learning to Defer in Congested Systems: The AI-Human Interplay." arXiv:2402.12237.
- Bary, Macq, Petit. "No Need for Learning to Defer? A Training Free Deferral Framework to Multiple Experts through Conformal Prediction." arXiv:2509.12573.
- Pugnana, De Toni, Barbera, Pellungrini, Lepri, Passerini. "To Ask or Not to Ask: Learning to Require Human Feedback." arXiv:2510.08314 (abstract read). It generalises L2D so that expert feedback enriches the model rather than replacing it.
- Bansal et al. "Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance." CHI 2021 [venue per arXiv comment]. arXiv:2006.14779. The complementarity reference.

**Survey status.** No dedicated 2024–2026 survey of learning to defer was found on arXiv (API title and abstract queries) or on the web. For abstention in LLMs, Wen et al., "Know Your Limits: A Survey of Abstention in Large Language Models" (TACL 2024 per arXiv comment; arXiv:2407.18418) [verified arXiv] **[not read]**.

### 6.3 Conformal prediction and risk control

#### Angelopoulos & Bates: Gentle Introduction
- **Bibliographic data:** Anastasios N. Angelopoulos, Stephen Bates.
  - arXiv: "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification." arXiv:2107.07511.
  - Journal: "Conformal Prediction: A Gentle Introduction." *Foundations and Trends in Machine Learning* 16(4):494–591, 2023. doi:10.1561/2200000101.
  - [verified, arXiv API + Crossref]. Note the two different titles.
- **Problem & contribution:** a tutorial.
- **Method (sections read):**
  - §4.1, group-balanced conformal: run conformal separately per group, giving P(Y ∈ C(X) | group = g) ≥ 1−α "for all groups". This is Vovk's Mondrian construction and the template for per-class strata.
  - §4.6, weighted conformal under drift: coverage ≥ 1 − α − 2Σ w̃_i ε_i, where ε_i is the TV distance.
  - §5.5: selective accuracy needs LTT because "we are not guaranteed that model accuracy is monotone in the cutoff λ".
- **Evaluation:** worked examples.
- **WorkTrace must NOT claim:** group-conditional guarantees, or LTT-based selective accuracy.
- **Leaves open:** agents and the delegation semantics.
- **Differentiation:** methodological citation.
- **Cautions:** cite the FnT version and give its correct title.

#### Conformal Risk Control (CRC)
- **Bibliographic data:** Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, Tal Schuster. "Conformal Risk Control." *ICLR 2024* (spotlight). arXiv:2208.02814. [verified: arXiv API; ICLR 2024 proceedings page found via web search].
- **Problem & contribution:** extends split conformal to E[L_{n+1}(λ̂)] ≤ α for any bounded loss that is **monotone** in λ.
- **Method:** λ̂ = inf{λ : (n/(n+1)) R̂_n(λ) + B/(n+1) ≤ α} (eq. 4). Thm 1 is the guarantee in expectation; Thm 2 the lower bound α − 2B/(n+1). §2.4: for non-monotone losses, "this algorithm does not control the risk" (Prop. 1). §4.1: weighted CRC under covariate shift, and a TV bound E L ≤ α + B Σ TV (Prop. 3). §4.2: quantile risk control.
- **Evaluation:** FNR in tumour segmentation and multilabel classification, hierarchical classification, F1 in QA.
- **WorkTrace must NOT claim:** risk control for monotone losses, the TV degradation bound.
- **Leaves open:** high-probability control, non-monotone (selective) risks, agents.
- **Differentiation:** "Because WorkTrace certifies a non-monotone selective risk with high probability, it uses LTT/binomial certification rather than CRC; CRC-based agent safeguards (CORA, ToolChain-CRC) control an expected joint risk."
- **Cautions:** the guarantee is in expectation (see Hultberg et al.).

#### Learn then Test (LTT)
- **Bibliographic data:** Anastasios N. Angelopoulos, Stephen Bates, Emmanuel J. Candès, Michael I. Jordan, Lihua Lei. "Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control." arXiv:2110.01052 (2021). Published in *The Annals of Applied Statistics* (2025), doi:10.1214/24-AOAS1998. [verified, arXiv API + Crossref].
- **Problem & contribution:** control *any* risk (including non-monotone ones) with high probability by recasting threshold selection as multiple testing.
- **Method:**
  - Def. 1: an (α, δ)-RCP satisfies "P(R(T_λ̂) ≤ α) ≥ 1 − δ".
  - For each λ_j test H_j: R(λ_j) > α with a valid p-value (Hoeffding–Bentkus, Prop. 1; for binary losses the exact binomial tail, §3.2). Apply an FWER-controlling procedure (Bonferroni, fixed-sequence (Prop. 3), graph-based (Prop. 5)).
  - Thm 1: P(sup_{λ∈Λ̂} R(λ) ≤ α) ≥ 1−δ. Any λ ∈ Λ̂ may then be chosen "(even in a data-driven way)".
  - §3.2: selective classification with risk P(T(X) ≠ Y | T(X) ≠ ∅), computed on the accepted subsample, with the exact binomial bound.
- **Evaluation:** ImageNet selective classification (α = 0.15, δ = 0.1, 5k calibration points), detection, OOD and others.
- **WorkTrace must NOT claim:** high-probability selective-risk certification, multi-risk control, fixed-sequence testing.
- **Leaves open:** the definition of the loss for agents, per-class delegation, sequential revocation.
- **Differentiation:** "WorkTrace's grant rule is an LTT instance with one hypothesis family per decision class and a loss defined by evidence interventions."
- **Cautions:** cite the AoAS version.

#### Related risk-control items
- Bates, Angelopoulos, Lei, Malik, Jordan. "Distribution-free, Risk-controlling Prediction Sets." *Journal of the ACM* (2021). doi:10.1145/3478535. arXiv:2101.02703. [verified, Crossref] **[not read]**.
- Hultberg, Zachariah, Ribeiro. "Anytime-Valid Conformal Risk Control." arXiv:2602.04364 (2026). [verified arXiv]. Abstract and §1 read; the n = 500 / 48% observation is quoted above.
- Lekeufack, Angelopoulos, Bajcsy, Jordan, Malik. "Conformal Decision Theory: Safe Autonomous Decisions from Imperfect Predictions." arXiv:2310.05921. [verified arXiv; venue unverified] **[not read]**. An online long-run guarantee, used by CCO.
- Feldman, Ringel, Bates, Romano. "Achieving Risk Control in Online Learning Settings." arXiv:2205.09095. [verified arXiv; venue unverified] **[not read]**.
- Gibbs & Candès. "Adaptive Conformal Inference Under Distribution Shift." arXiv:2106.00170. [venue unverified] **[not read]**.
- Tibshirani, Barber, Candès, Ramdas. "Conformal Prediction Under Covariate Shift." arXiv:1904.06019. [venue unverified] **[not read]**.
- Barber, Candès, Ramdas, Tibshirani. "Conformal prediction beyond exchangeability." *Annals of Statistics* 51(2) (2023). doi:10.1214/23-AOS2276. [verified, Crossref] **[not read]**.
- Gibbs, Cherian, Candès. "Conformal prediction with conditional guarantees." *JRSS-B* (2025). doi:10.1093/jrsssb/qkaf008. [verified, Crossref] **[not read]**.
- Vovk, Gammerman, Shafer. *Algorithmic Learning in a Random World.* Springer 2005, doi:10.1007/b106715; 2nd ed. 2022, doi:10.1007/978-3-031-06649-8. [verified, Crossref] **[not read]**. The Mondrian (class-conditional) source.
- Angelopoulos, Bates, Fannjiang, Jordan, Zrnic. "Prediction-Powered Inference." arXiv:2301.09633. [verified arXiv; venue (Science 2023) unverified here] **[not read in depth]**. See A2 for why it does not solve the generator→real shift.

### 6.4 Sequential, anytime-valid monitoring (revocation)

#### Podkopaev & Ramdas (2022)
- **Bibliographic data:** Aleksandr Podkopaev, Aaditya Ramdas. "Tracking the risk of a deployed model and detecting harmful distribution shifts." ICLR 2022 [venue per arXiv comment]. arXiv:2110.06177. [verified arXiv].
- **Problem & contribution:** sequential tests that fire only on *harmful* shifts (a risk increase beyond a tolerance) and that are valid under continuous monitoring.
- **Method:** H0: R_T ≤ R_S + ε_tol (eq. 1); a running-risk version under independence only (eq. 2). Alg. 1 compares a time-uniform lower confidence sequence on the target risk with an upper bound on the source risk. Prop. 1 gives type-I control. Remark 3: "the probability of ever raising a false alarm is at most δ". §2.1: if a shift is benign, "with high probability, the test will never output a 1 and stop".
- **Evaluation:** simulated and real shifts. Numbers not extracted.
- **WorkTrace must NOT claim:** sequential, anytime-valid detection of risk increase.
- **Leaves open:** per-class autonomy status and re-grant; basis-level losses.
- **Differentiation:** "WorkTrace's revocation rule is a per-class instance of sequential harmful-shift testing, applied to audited unjustified-action indicators."
- **Cautions:** none.

#### Standard anytime-valid references
All **[not read]**; cited because Podkopaev & Ramdas and Conformal Selective Acting rely on them.
- Waudby-Smith & Ramdas. "Estimating means of bounded random variables by betting." *JRSS-B* (online 2023). doi:10.1093/jrsssb/qkad009. arXiv:2010.09686. [verified, Crossref].
- Howard, Ramdas, McAuliffe, Sekhon. "Time-uniform, nonparametric, nonasymptotic confidence sequences." *Annals of Statistics* 49(2) (2021). doi:10.1214/20-AOS1991. [verified].
- Ramdas, Grünwald, Vovk, Shafer. "Game-Theoretic Statistics and Safe Anytime-Valid Inference." *Statistical Science* (2023). doi:10.1214/23-STS894. [verified, Crossref].
- Vovk & Wang. "E-values: Calibration, combination, and applications." *Annals of Statistics* 49(3) (2021). doi:10.1214/20-AOS2020. [verified].
- Shafer. "Testing by Betting." *JRSS-A* (2021). doi:10.1111/rssa.12647. [verified, Crossref].
- Grünwald, de Heide, Koolen. "Safe Testing." arXiv:1906.07801 (JRSS-B discussion paper per arXiv comment). [venue unverified].
- Xu, Karampatziakis, Mineiro. "Active, anytime-valid risk controlling prediction sets." *NeurIPS 37* (2024). doi:10.52202/079017-1920. arXiv:2406.10490. [verified, Crossref + arXiv]. Controls marginal, not selective, risk (per Conformal Selective Acting §3.2).

### 6.5 Abstention and escalation for LLMs (2023–2025)

#### KnowNo: Ren et al. (2023)
- **Bibliographic data:** Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, Zhenjia Xu, Dorsa Sadigh, Andy Zeng, Anirudha Majumdar. "Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners." *CoRL 2023*, PMLR 229. arXiv:2307.01928. [verified, arXiv + PMLR page].
- **Problem & contribution:** an LLM planner asks a human for help when the conformal prediction set over candidate actions is not a singleton.
- **Method:** Prop. 1 (single step): "With probability 1−δ over the sampling of the calibration set, the task completion rate over new test scenarios drawn from D is at least 1−ϵ". It holds "under the assumption of accurate human help". Prop. 2 (multi-step): sequence-level calibration with a min-score and causal reconstruction.
- **Evaluation:** simulated and hardware tabletop tasks; human help rate vs success.
- **WorkTrace must NOT claim:** conformal "ask for help" for LLM planners with completion-rate guarantees.
- **Leaves open:** per-class autonomy, the basis of decisions, an imperfect human, revocation.
- **Differentiation:** "KnowNo decides per instance whether a planner's action is ambiguous enough to ask; WorkTrace decides per decision class whether the agent's tested evidence-handling licenses unsupervised action."
- **Cautions:** the perfect-human assumption.
- **Related:** Liang, Zhang, Fisac. "Introspective Planning." NeurIPS 2024 [venue per arXiv comment]. arXiv:2402.06529. [verified arXiv] **[not read]**.

#### Yadkori et al. (2024): conformal abstention
- **Bibliographic data:** Yasin Abbasi Yadkori, Ilja Kuzborskij, David Stutz, András György, Adam Fisch, Arnaud Doucet, Iuliya Beloshapka, Wei-Hung Weng, Yao-Yuan Yang, Csaba Szepesvári, Ali Taylan Cemgil, Nenad Tomasev. "Mitigating LLM Hallucinations via Conformal Abstention." arXiv:2405.01563. [verified arXiv; venue unverified].
- **Problem & contribution:** decide when an LLM should say "I don't know", using self-consistency scores and CRC.
- **Method:** E[R(λ̂_n)] ≤ α (Prop. 3.1 setting: a non-increasing loss), i.e. a CRC-type expectation guarantee.
- **Evaluation:** TriviaQA, Temporal Sequences.
- **Must NOT claim:** conformal abstention for LLMs.
- **Leaves open:** agents, classes, basis.
- **Cautions:** Trust or Escalate §2.1 notes it approximates rather than exactly bounds the selective risk.

#### Gui, Jin & Ren (2024): Conformal Alignment
- **Bibliographic data:** Yu Gui, Ying Jin, Zhimei Ren. "Conformal Alignment: Knowing When to Trust Foundation Models with Guarantees." *NeurIPS 37* (2024). doi:10.52202/079017-2350. arXiv:2405.10301. [verified, Crossref].
- **Problem & contribution (abstract only):** select the units whose outputs meet an alignment criterion, with an FDR-type guarantee ("on average, a prescribed fraction of selected units indeed meet the alignment criterion").
- **Must NOT claim:** certified selection of trustworthy outputs.
- **Leaves open:** agents, classes, the basis of decisions.
- **Differentiation:** conformal selection (Jin & Candès, arXiv:2210.01408 [verified]) is an alternative statistical frame when many test units are certified at once. WorkTrace certifies classes, not units.

#### Jung, Brahman & Choi (2025): Trust or Escalate
- **Bibliographic data:** Jaehun Jung, Faeze Brahman, Yejin Choi. "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement." *ICLR 2025* (oral). arXiv:2407.18370. [verified, OpenReview API + arXiv].
- **Problem & contribution:** an LLM judge abstains or escalates along a cascade of judges, guaranteeing P(f_LM(x) = y_human | c_LM(x) ≥ λ) ≥ 1 − α with probability ≥ 1 − δ (eq. 2).
- **Method:** empirical selective risk on calibration data, exact binomial upper bound (eq. 4), fixed-sequence testing over λ (eq. 5), Thm 1. It explicitly "resembles that of selection with guaranteed risk (Geifman & El-Yaniv, 2017)".
- **Evaluation:** human-preference benchmarks. Numbers not extracted.
- **WorkTrace must NOT claim:** an exact high-probability selective guarantee with escalation.
- **Leaves open:** agents acting in the world, decision classes, basis, revocation.
- **Differentiation:** the closest *procedural* template for §3.4. Cite it as such.
- **Cautions:** none.

### 6.6 LLM-agent works, 2026 (the novelty-threat set)

#### Role-Stratified CRC for LLM tool calls (arXiv:2607.24343): main technical threat
- **Bibliographic data:** Md Ashikur Rahman, Md Arifur Rahman, Niamul Hassan Samin, Khandaker Rifah Tasnia, Md Hasibul Amin, Sifat Rahman Ahona, Juena Ahmed Noshin. "Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls." arXiv:2607.24343, v2, 31 Jul 2026. [verified arXiv; preprint, no venue].
- **Problem & contribution:** whole-call certification averages away failures in rare high-risk argument fields. Each semantic role (target, credential, command, content, …) gets its own threshold and budget.
- **Method:**
  - Violation: "A field is violated when untrusted input changes its value against the user's intent". V(r) = P(violated ∧ allowed | role = r) (eq. 2): a joint rate per field.
  - Per-role CRC (eq. 5), with a floor of 1/(n_r+1).
  - Prop. 1: aggregate control implies only V(r) ≤ α_agg/p_r ("Aggregate certification dilutes rare-role failures … inflates a role-r violation rate by 1/p_r").
  - Prop. 2 and Thm 1 ("price of coarseness", via a Blackwell ordering).
  - Thm 2: simultaneous Clopper–Pearson + Bonferroni certificate across final strata, with pooling of rare roles.
  - Recalibration under shift; empirical compliance otherwise.
- **Evaluation:** AgentDojo, InjecAgent, six LLMs. At a 1% budget, per-field CRC has 0.0–0.3% target violation vs up to 21.2% for single-threshold baselines (Table 1). The credential role could not be certified individually (it needs ≈300 fields; the data support ≈3%).
- **WorkTrace must NOT claim:**
  - stratified / per-group certification for agents;
  - the argument that pooled guarantees fail rare high-stakes strata;
  - simultaneous Clopper–Pearson / Bonferroni certificates;
  - pooling rare strata.
- **Leaves open:**
  - the strata are argument roles of a single call, not decision classes;
  - the certified object is runtime field gating, not an agent-level delegation status;
  - the label is an attack-induced value change, not agent behaviour under systematic interventions on evidence (no "right action, wrong basis"; no redundancy handling);
  - no outcome-only vs evidence-based comparison;
  - no revocation (only recalibration).
- **Differentiation:** "Role-stratified CRC certifies, per argument role, that injected content rarely determines a tool-call field; WorkTrace certifies, per decision class, that an agent's autonomous actions are rarely unjustified under interventions on the evidence they rest on, and uses that certificate to grant and revoke autonomy."
- **Cautions:**
  - Preprint, no venue.
  - Its "certificate under exchangeability or after recalibration" is honestly scoped.
  - The headline V(r) depends on attack prevalence (85–94% in the benchmarks), as the paper itself notes.

#### CORA (arXiv:2604.09155)
- **Bibliographic data:** Yushi Feng, Junye Du, Qifan Wang, Zizhan Ma, Qian Niu, Yutaka Matsuo, Long Feng, Lequan Yu. "CORA: Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Automation." arXiv:2604.09155, Apr 2026. [verified arXiv; preprint].
- **Problem & contribution:** a post-policy, pre-action guard for mobile GUI agents. It casts safety "as selective action execution". A Guardian scores each action, CRC sets the execute/abstain threshold, and a Diagnostician recommends confirm, reflect or abort. A Goal-Lock defends against injection. It introduces the Phone-Harm benchmark.
- **Method:** loss L(Z;τ) = ℓ(Z)·1{s ≤ τ} (eq. 3), the joint harmful-and-executed rate. CRC threshold (eq. 5), "Under the assumption of exchangeability". Weighted calibration over a deployment descriptor (app, OS, device) for shift (§3.7). Blockwise splits for within-trajectory dependence.
- **Evaluation:** Phone-Harm (Harm-150 + Normal-150), MobileRisk, AndroidWorld. On Harm-150: HR 4.37%, GAR 79.80%, IF1 85.29%, OIR 19.23% (Table 1). They report safety–helpfulness–interruption Pareto frontiers.
- **WorkTrace must NOT claim:**
  - execute/abstain for agent actions with conformal risk control;
  - risk–coverage / interruption frontiers as the evaluation protocol for agent gating;
  - human confirmation as the escalation path.
- **Leaves open:**
  - per-class guarantees (harm types are categorised but not certified per type);
  - conditional risk;
  - basis or justification;
  - agent-level grants and revocation;
  - an outcome-only vs evidence comparison.
- **Differentiation:** "CORA gates each proposed GUI action against an expected joint harm budget; WorkTrace grants autonomy per decision class against a high-probability bound on the conditional rate of unjustified actions."
- **Cautions:**
  - "users can set α = 0.01 to ensure that, on average, no more than 1% of autonomous actions are harmful" (§3.4) misreads the joint loss as a conditional rate.
  - The step labels on the benchmark come partly from an LLM judge (validated against humans per the appendix, not checked here).

#### ToolChain-CRC (arXiv:2606.18467)
- **Bibliographic data:** Jeffery Opoku, David Banahene. "ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift." arXiv:2606.18467, Jun 2026. [verified arXiv; preprint].
- **Problem & contribution:** the calibrated object is the whole trajectory (retrieval, tool calls, intermediate checks, final answer), not the final answer.
- **Method:**
  - Step scores S_ij combined by noisy-or into a trajectory score. Audited step labels Y_ij ("from human audit, gold labels, deterministic validators, or a frozen verifier") give Y^traj. Accepted-trajectory loss R^traj(λ) = Y^traj·A(λ). CRC (Thm 1), exchangeability across whole trajectories.
  - Prop. 1: "controlling the final visible risk E[AV] does not by itself control the trajectory risk E[AR^traj]". Utility-aware selection within the feasible set (Prop. 2).
  - A drift extension and an anytime escalation alarm via a supermartingale (not read).
- **Evaluation:** synthetic drift, RAG/tool stress tests, SQuAD-derived tasks, a live RAG agent. Numbers not extracted.
- **WorkTrace must NOT claim:**
  - that outcome/final-answer calibration misses upstream unsupported grounds (formally shown here);
  - trajectory-level CRC;
  - anytime escalation within a run.
- **Leaves open:**
  - the upstream labels are audit or validator judgements of support, not interventions testing whether the *action depends on* the evidence (no remove / invert / redundancy tests);
  - no decision classes;
  - no autonomy status or revocation across runs.
- **Differentiation:** "ToolChain-CRC adds audited upstream failures to the controlled loss of a single run; WorkTrace measures whether the agent's action actually tracks its external evidence under interventions, and certifies autonomy per decision class across runs."
- **Cautions:** two authors, preprint; the paper's own novelty claim is narrow ("not that conformal risk control is new").

#### Conformal Selective Acting (arXiv:2605.20270)
- **Bibliographic data:** Hamed Khosravi, Xiaoming Huo. "Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs." arXiv:2605.20270, May 2026. [verified arXiv; preprint].
- **Problem & contribution:** per-deployment, anytime-pathwise control of *selective* risk (verifier failures among released outputs) on a non-exchangeable, online-updated stream.
- **Method:**
  - Increment X_t(q) = A_t(q)((1 − V_t) − α).
  - Per-threshold e-process E_{j,t}(q) = Π(1 − λ X_s(q)) with predictable plug-in bets (eq. 1–2).
  - Bonferroni over the grid with an epoch factor; deploy the maximum certified threshold.
  - Thm 5.1: R^act_T ≤ α + ν̄_T + O(N_T^{−1/2}) for all T with probability ≥ 1−2δ.
  - Thm 5.3: certification time ≲ 4(log(1/δ)+1)/margin².
- **Evaluation:** eight specialist benchmarks, 480 + 160 streams, live RLVR cells. Not read.
- **WorkTrace must NOT claim:**
  - anytime-valid certification and de-certification of a release (autonomy) decision on selective risk;
  - e-processes per threshold.
- **Leaves open:** decision classes, basis/intervention losses, delegation to humans, outcome vs evidence comparison.
- **Differentiation:** the methodological citation for §3.8. "We use per-class e-processes on audited unjustified-action indicators in the manner of conformal selective acting."
- **Cautions:** the "unique instantiation" and "empty cell" rhetoric is the authors' framing.

#### Shen (2026): "certified autonomy" by Clopper–Pearson (arXiv:2608.05064)
- **Bibliographic data:** Jianru Shen. "Provable Limits and Certified Deferral for Verbalized Uncertainty in Small Language Models." arXiv:2608.05064, Aug 2026. Accepted at MIWAI 2026 per arXiv comment [venue unverified].
- **Problem & contribution:** whether verbalized confidence supports risk-controlled deferral for small LLMs.
- **Method:** Prop. 3: Clopper–Pearson upper bound on selective risk, union-corrected over the threshold grid; the grid is fixed from unlabelled confidences (Remark 2).
- **Evaluation:** 11 models on ARC and TruthfulQA. "The Clopper–Pearson procedure of Prop. 3 grants autonomy sparingly": at r_max = 20% only three model–task pairs are certified; at 10% none (§4.4).
- **WorkTrace must NOT claim:** the phrase "certified autonomy", or granting autonomy per (model, task) via Clopper–Pearson on outcome correctness.
- **Leaves open:** agents, evidence/basis, decision classes defined by situation, revocation.
- **Differentiation:** this *is* the outcome-only baseline. "Outcome-only certification as in Shen (2026) …".
- **Cautions:** single author, workshop-level venue.

#### Strategic Decision Support for AI Agents (arXiv:2606.12587)
- **Bibliographic data:** Shayan Kiyani, Sima Noorani, George Pappas, Hamed Hassani. "Strategic Decision Support for AI Agents." arXiv:2606.12587, Jun 2026. [verified arXiv; preprint].
- **Problem & contribution:** "When should an AI agent act alone, and when must it seek support". Minimise the support rate subject to a missed-support error P(a = 0 | g = 1) ≤ ε, i.e. acting alone when support would have materially helped.
- **Method:** Thm 3.1: the optimal policy thresholds the value of support. Online algorithm (SOS) with adaptive thresholding and randomized exploration; distribution-free error control; calibration on the fly.
- **Evaluation:** DDXPlus, WikiSQL, VirtualHome, MATH, with LLM agents. Less support at matched error (Fig. 2).
- **WorkTrace must NOT claim:**
  - a formal "act alone vs seek support (incl. human)" decision with distribution-free control for LLM agents;
  - randomized exploration to observe counterfactual labels.
- **Leaves open:**
  - the error is the counterfactual *value of support* (an FNR-like conditional on g = 1), not the unjustified-action rate among autonomous actions;
  - no classes, no basis interventions, no grant/revoke status.
- **Differentiation:** "Strategic decision support controls how often an agent skips help that would have changed its output; WorkTrace controls how often an agent's autonomous actions are unjustified given its evidence, per decision class."
- **Cautions:** preprint.

#### Think Short, Defer Smart (arXiv:2607.26865)
- **Bibliographic data:** Amirmohammad Farzaneh, Osvaldo Simeone. "Think Short, Defer Smart, Act, and Repeat: Calibrated Reasoning and Uncertainty-Aware Deferral for Edge LLM Agents." arXiv:2607.26865 (v3, Sep 2026). [verified arXiv].
- **Contribution (abstract + Prop. 1):** multi-objective LTT on end-to-end episodes, giving "simultaneous finite-sample guarantees on expected episode reward and cloud-call rate". Deferral goes to a cloud model, not a human.
- **Must NOT claim:** LTT on agent episodes with joint reward/deferral guarantees.
- **Leaves open:** classes, basis, humans, revocation.
- **Differentiation:** "LTT has been applied to agent deferral budgets (Farzaneh & Simeone 2026); WorkTrace applies it per decision class to an interventional justification loss."

#### SafeCommit (arXiv:2608.04289)
- **Bibliographic data:** Mayur Akewar, Ravi Ranjan. "SafeCommit: Certifying When Memory-Grounded Agents May Safely Act." arXiv:2608.04289, Aug 2026. [verified arXiv; preprint, "target NeurIPS"].
- **Contribution:** commit an action only if it is safe in every world of a conformally calibrated set of plausible latent worlds. Otherwise probe or fall back (defer / escalate / abstain). P(unsafe commit) ≤ α + β, where β is the proposal-miss rate (eq. 7).
- **Evaluation:** "a dependency-free controlled simulator … intentionally a proof of concept".
- **Must NOT claim:** "deciding … when the available evidence is sufficient to safely" act, in the per-decision runtime sense.
- **Leaves open:** tested agent behaviour, classes, agent-level autonomy.
- **Differentiation:** "SafeCommit certifies a single commit against plausible world states; WorkTrace certifies an agent's track record of evidence-handling in a decision class."
- **Cautions:** simulator-only.

#### Calibration Is Not Control (arXiv:2606.21399)
- **Bibliographic data:** Chubin Zhang, Zhenglin Wan, Xingrui Yu, Jingxuan Wu, Qi Wen, Pengfei Zhou, Wangbo Zhao, Ivor Tsang. "Calibration Is Not Control: Intervention Value for LLM-Agent Oversight." NeurIPS 2026 per arXiv comment [venue unverified]. arXiv:2606.21399.
- **Contribution:** "states with the same failure risk can differ in whether intervention helps". Routing should use the intervention advantage τ_i(h) = Q_i − Q_continue, not p_fail (Def. 1, Prop. 1, Remark 1: recalibration preserves the threshold policy class). Learned from prefix branching in replayable environments.
- **Evaluation:** ALFWorld regret 0.51 → 0.09. Online: 35% vs 48% handoff, 45% vs 37% success.
- **Must NOT claim:** that calibrated failure scores are insufficient for intervention decisions.
- **Leaves open:** basis, classes, guarantees.
- **Relevance:** a parallel argument at the oversight level ("predictive quality ≠ decision value") that supports WorkTrace's outcome-only critique. It also warns that escalation value is heterogeneous (§3.6).

#### Oversight Has a Capacity (arXiv:2606.08919)
- **Bibliographic data:** Emre Turan. "Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human." arXiv:2606.08919, Jun 2026. [verified arXiv; single author].
- **Contribution:** an agent action guard framed as selective classification under asymmetric cost (Table 1 costs: 1 / 5 / 50). Reviewer agreement κ = 0.52 on 125 actions. A fatigue model gives an inverted-U of safety vs escalation rate. The paper itself claims none of the mechanisms are novel.
- **Relevance:** escalation cost is endogenous. Cite it with FALCON and DeCCaF.
- **Cautions:** the inverted-U is a "modeling result", not a human study. Small n.

#### CCO: Calibrating Conservatism for Scalable Oversight (arXiv:2605.28807)
- **Bibliographic data:** William Overman, Mohsen Bayati. arXiv:2605.28807, May 2026. [verified arXiv].
- **Contribution:** an online conformal (CDT) controller λ_{t+1} = λ_t + η(ℓ_t − α) over a penalty from auxiliary overseers. A long-run violation rate ≈ α holds for arbitrary sequences.
- **Relevance:** an alternative guarantee type (long-run average, adversarial) that does not need exchangeability. It is weaker per class and per time.

#### Minor / adjacent (abstract or first page only)
All [verified arXiv]; preprints unless stated.
- **ReDAct**, Piatrashyn et al., arXiv:2604.07036: defers single decisions from a small to a large LLM. The threshold is calibrated to a *budget of deferrals*, with no risk guarantee (§4.2).
- **Bayesian Self-Escalation**, Shaikh, arXiv:2608.24087: escalation as optimal stopping on a competence posterior, with a regret bound. Model-to-model.
- **G-CARB**, Yu, Gu, Partovi Nia, Asgharian, arXiv:2610.05563 (NeurIPS 2026 workshop per comment): CRC over a harm ledger for stopping SLM agents, on AgentDojo replay.
- **LLMCert-T**, Yeon, Chaudhary, Singh, arXiv:2510.03992: Clopper–Pearson certificates on the probability that tool selection satisfies a specification under a tool-insertion process. A precedent for CP certificates on agent behaviour.
- **Agent Behavioral Contracts II**, Bhardwaj et al., arXiv:2608.12895: a Bonferroni–Clopper–Pearson LP for compositional reliability, plus an anytime-valid certificate. Shows that same-model components co-fail on 90% of failures, a warning for independence assumptions.
- **E-valuator**, Sadhuka et al., arXiv:2512.03109: sequential tests on verifier scores within a trajectory.
- **PACE**, arXiv:2606.08106: an anytime-valid commit gate for self-modifications.
- **Ramaswamy**, "Intelligence as Managed Autonomy: Failure, Escalation, and Governance for Agentic AI Systems," arXiv:2605.27628, doi:10.1007/s10846-026-02413-w (journal DOI per arXiv; [venue unverified]): a Petri-net model of autonomy states with "Regulated/Revoked transitions". It mentions "persistent but unjustified action". Conceptual, with no statistical certification. **Worth a sentence in related work**, because it uses "revoked autonomy" language.
- **Advani**, "When Small Models Are Right for Wrong Reasons: Process Verification for Trustworthy Agents," arXiv:2601.00513 (AAAI 2026 TrustAgent workshop per comment): 50–69% of correct answers have flawed reasoning. This is evidence for "right action, wrong basis", measured on reasoning traces, not by evidence interventions.
- **PPRM**, Zhang, Cai, Yu, Simeone, ICML 2026 (OpenReview API record "ICML 2026 regular"), arXiv:2602.02229: risk monitoring with few labels plus prediction-powered imputation. Relevant if real-episode audits are scarce.
- **Fernandez P8**, arXiv:2610.00787: signed human re-authorization after persistent halts. Already on the positioning list. Complementary governance mechanism; no statistical grant rule.
- **Saban**, "Domain-Conditioned Safety in Frontier Computer-Using Agents," arXiv:2606.05233: 0/140 attack success, Clopper–Pearson 95% upper bound 2.60%, but up to 100% in the coding domain. **Direct empirical support for per-domain/per-class rather than global certification.**
- **Messoudi & Mansar**, arXiv:2610.19811: LTT thresholds for binary LLM workflow decisions. Naive threshold selection exceeds the target risk in about half the settings vs 7.8% for LTT.
- **CCPO**, Si, Jang, Lee, Bastani, arXiv:2511.11828: online conformal constraints for cost-effective LLM orchestration.
- **Anytime Contracts for AI Services**, Velasevic, Saig, Mazumdar, arXiv:2610.22781: e-value-based contracts with unknown exit rules. A possible bridge to the economics of delegation.
- **Levels of Autonomy for AI Agents**, Feng, McDonald, Zhang, arXiv:2506.12469 **[not read]**: an autonomy-level taxonomy, a possible framing citation.

---

## 7. (d) Novelty threat: precise characterisation

Feature matrix (✓ = present, ~ = partial, blank = absent). Columns:
- **Agent:** LLM agent acting in an environment.
- **Per-class:** separate guarantee per group/stratum.
- **Agent-level status:** grant/revoke autonomy over a scope, not per-instance gating.
- **Basis loss:** penalises a right action on a wrong basis.
- **Interventions:** loss measured by interventions on external evidence.
- **Cond. HP:** conditional selective risk with high probability (α, δ).
- **Seq. revoke:** anytime-valid de-certification.
- **Outcome baseline:** explicit comparison against outcome-only certification.
- **Escal. cost:** an explicit cost of escalation in the objective.

| Work | Agent | Per-class | Agent-level status | Basis loss | Interventions | Cond. HP | Seq. revoke | Outcome baseline | Escal. cost |
|---|---|---|---|---|---|---|---|---|---|
| Geifman & El-Yaniv 2017; LTT | | | | | | ✓ | | | |
| Trust or Escalate 2025 | | | | | | ✓ | | | ~ (cascade cost) |
| KnowNo 2023 | ✓ (robot) | | | | | ~ (completion rate) | | | ~ (help rate) |
| CORA 2026 | ✓ | | | | | (expectation, joint) | | | ✓ (interruption) |
| Role-Stratified CRC 2026 | ✓ | ✓ | | ~ (untrusted influence) | ~ (clean vs injected) | ✓ (Thm 2, joint) | | ~ (aggregate vs stratified) | ~ |
| ToolChain-CRC 2026 | ✓ | | | ✓ (audited upstream) | | (expectation) | ~ (within run) | ✓ (final-answer-only) | ✓ (η·intervention rate) |
| Conformal Selective Acting 2026 | ~ (LLM stream) | | ~ (release on/off) | | | ✓ (anytime) | ✓ | | |
| Shen 2026 | ~ (LLM QA) | ~ (model × task) | ✓ ("grants autonomy") | | | ✓ | | | |
| Strategic Decision Support 2026 | ✓ | | | | | (online, counterfactual FNR) | | | ✓ (support rate) |
| SafeCommit 2026 | ✓ (sim) | | | ~ (evidence sufficiency) | | ~ | | | ~ |
| Calibration Is Not Control 2026 | ✓ | | | | ~ (branching on actions) | | | ~ (failure score vs value) | ✓ |
| **WorkTrace (proposed)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Characterisation.** No single work combines more than three of the WorkTrace columns.
- **Role-Stratified CRC** comes closest on the *statistics + stratification + evidence provenance* axis. Its unit is the field and its object is runtime gating.
- **ToolChain-CRC** comes closest on the *basis-aware loss + outcome-only critique* axis. Its labels are audited, not interventional, and its unit is the run.
- **Conformal Selective Acting** and **Shen 2026** come closest on the *autonomy-as-certified-status* axis. Their loss is outcome-only.

What WorkTrace can defensibly claim as new is therefore the **combination**:
1. The unit is the decision class, with an operational, decision-time membership rule.
2. The loss is interventional and redundancy-robust, so it counts correct-but-unjustified actions.
3. A pre-registered empirical test of whether that loss predicts held-out outcome failures under evidence shift better than outcome-only certification at matched coverage.
4. A grant / escalate / refuse / revoke life cycle with stated guarantees.

**Residual risk.** These are fast-moving 2026 preprints (several from June to October 2026). A paper combining (1) with (4), i.e. stratified CRC plus anytime monitoring per tool class, is a plausible near-term competitor. Re-run the search before submission. Suggested queries: "stratified" + "anytime" + "agent"; "autonomy" + "Clopper"; "per-tool certification".

---

## 8. Implications for WorkTrace

**Design changes**
1. **Certify the conditional selective risk with high probability** (LTT/SGR with exact binomial p-values, fixed-sequence over thresholds, Bonferroni over classes), not CRC. Write the proposition of §3.4 and label it explicitly as an instance of LTT (Angelopoulos et al. 2025) and Geifman & El-Yaniv (2017).
2. **Define ℓ_WT as counterfactual correctness over a pre-registered intervention family**, using the generator's normative map A*(do_j(E)). This makes "right action on wrong basis" computable without an LLM judge and handles redundancy by construction.
3. **Run the outcome-only rule through the identical pipeline** (ℓ_out instead of ℓ_WT) and cite Shen 2026 as an instance of it. H3's primary endpoint should be *held-out outcome errors under evidence shift* at matched coverage. That avoids the circularity of scoring the WorkTrace rule on its own loss (§3.7).
4. **Decide what "refuse" means**: (a) a certified-unsafe class, via a lower-bound test, or (b) a normative action for out-of-permission requests. State it.
5. **Add revocation as a per-class e-process on randomly audited autonomous episodes**, with hysteresis (grant α, revoke α′ > α), a reset on agent change, and fresh-evidence re-grant. Report detection delays (§5.4). They are long at low audit rates.
6. **Use the independent template/seed as the sampling unit** to keep Clopper–Pearson valid (A3).
7. **Include escalation cost J with reviewer error and capacity**, and present cost-adjusted risk–coverage curves for several κ/L ratios. Do not claim system-level guarantees for escalated cases.
8. **Pilot targets:** α = 0.10, δ = 0.05, simultaneous across ~6 classes. That means ≥46 clean (≈100 for realistic power) autonomous calibration episodes per class per configuration, plus a held-out set of similar size. Report α = 0.05 only where achievable.

**Risks**
- The statistics are textbook. Reviewers will discount any framing that suggests otherwise. Put the novelty in the loss, the unit, the comparison and the evidence.
- The certificate does not transfer from generated to real episodes. Present real episodes as descriptive validation with wide intervals.
- The guarantee is only as good as 𝓘 (the intervention family). Pre-register it per class and report the battery's sensitivity on generated ground truth.
- Terminology collisions: "certified autonomy" (Shen 2026); "revoked transitions" (Ramaswamy 2026); "selective action execution" (CORA); "selective acting" (Khosravi & Huo). Avoid these exact phrases or cite them.

**Must cite** (all verified): Chow 1970; El-Yaniv & Wiener 2010; Geifman & El-Yaniv 2017; Madras et al. 2018; Mozannar & Sontag 2020; Angelopoulos & Bates 2023 (FnT); Angelopoulos et al. 2024 (CRC, ICLR); Angelopoulos et al. 2025 (LTT, AoAS); Clopper & Pearson 1934; Podkopaev & Ramdas 2022; Waudby-Smith & Ramdas; Ramdas et al. 2023 (SAVI); Ren et al. 2023 (KnowNo); Jung et al. 2025 (Trust or Escalate); Rahman et al. 2026 (Role-Stratified CRC); Feng et al. 2026 (CORA); Opoku & Banahene 2026 (ToolChain-CRC); Khosravi & Huo 2026 (CSA); Shen 2026; Kiyani et al. 2026 (SDS).

**Should cite:** Saban 2026 (domain-conditioned safety, supports per-class certification); Zhang et al. 2026 (Calibration Is Not Control); Turan 2026 with FALCON and DeCCaF (escalation capacity); Hultberg et al. 2026 (expectation vs high probability); Barber et al. 2023 and Tibshirani et al. 2019 (shift); Vovk et al. 2005 (Mondrian).

---

## 9. Bibliography and verification record

| # | Reference | ID | Verified via |
|---|---|---|---|
| 1 | Chow, C. K. (1970). On optimum recognition error and reject tradeoff. IEEE TIT 16(1):41–46 | doi:10.1109/TIT.1970.1054406 | Crossref |
| 2 | Clopper, C. J., Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4):404 | doi:10.1093/biomet/26.4.404 | Crossref |
| 3 | El-Yaniv, R., Wiener, Y. (2010). On the Foundations of Noise-free Selective Classification. JMLR 11:1605–1641 | jmlr.org/papers/v11/el-yaniv10a | JMLR page + PDF |
| 4 | Geifman, Y., El-Yaniv, R. (2017). Selective Classification for Deep Neural Networks. NIPS 30 | arXiv:1705.08500 | arXiv API + papers.nips.cc |
| 5 | Hendrickx, K., Perini, L., Van der Plas, D., Meert, W., Davis, J. (2024). Machine learning with a reject option: a survey. Machine Learning | doi:10.1007/s10994-024-06534-x; arXiv:2107.11277 | Crossref + arXiv |
| 6 | Madras, D., Pitassi, T., Zemel, R. (2018). Predict Responsibly: Improving Fairness and Accuracy by Learning to Defer. NeurIPS 31 | arXiv:1711.06664 | arXiv API + proceedings.neurips.cc |
| 7 | Mozannar, H., Sontag, D. (2020). Consistent Estimators for Learning to Defer to an Expert. ICML 2020, PMLR 119 | arXiv:2006.01862 | arXiv API + PMLR |
| 8 | Verma, R., Nalisnick, E. (2022). Calibrated Learning to Defer with One-vs-All Classifiers. ICML 2022 | arXiv:2202.03673 | arXiv (venue per comment) |
| 9 | Mozannar, H., Lang, H., Wei, D., Sattigeri, P., Das, S., Sontag, D. (2023). Who Should Predict? Exact Algorithms For Learning to Defer to Humans. AISTATS 2023 | arXiv:2301.06197 | arXiv (venue per comment) |
| 10 | Okati, N., De, A., Gomez-Rodriguez, M. Differentiable Learning Under Triage | arXiv:2103.08902 | arXiv (venue unverified) |
| 11 | Leitão, D., Saleiro, P., Figueiredo, M. A. T., Bizarro, P. (2022). Human-AI Collaboration in Decision-Making: Beyond Learning to Defer. ICML 2022 Workshop | arXiv:2206.13202 | arXiv |
| 12 | Alves, J. V., et al. Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints | arXiv:2403.06906 | arXiv (TMLR 2024 unverified) |
| 13 | Zhang, Z., Nguyen, C. C., Rosewarne, D., Wells, K., Carneiro, G. (2026). Fatigue-Aware Learning to Defer via Constrained Optimisation | arXiv:2604.00904 | arXiv |
| 14 | Lykouris, T., Weng, W. Learning to Defer in Congested Systems: The AI-Human Interplay | arXiv:2402.12237 | arXiv |
| 15 | Bary, T., Macq, B., Petit, L. (2025). No Need for Learning to Defer? … through Conformal Prediction | arXiv:2509.12573 | arXiv |
| 16 | Pugnana, A., De Toni, G., Barbera, C., Pellungrini, R., Lepri, B., Passerini, A. (2025). To Ask or Not to Ask: Learning to Require Human Feedback | arXiv:2510.08314 | arXiv |
| 17 | Bansal, G., et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. CHI'21 | arXiv:2006.14779 | arXiv (venue per comment) |
| 18 | Angelopoulos, A. N., Bates, S. (2023). Conformal Prediction: A Gentle Introduction. FnT in ML 16(4):494–591 (arXiv title: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification) | doi:10.1561/2200000101; arXiv:2107.07511 | Crossref + arXiv |
| 19 | Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., Schuster, T. (2024). Conformal Risk Control. ICLR 2024 | arXiv:2208.02814 | arXiv + ICLR proceedings (web) |
| 20 | Angelopoulos, A. N., Bates, S., Candès, E. J., Jordan, M. I., Lei, L. (2025). Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control. Ann. Appl. Stat. | doi:10.1214/24-AOAS1998; arXiv:2110.01052 | Crossref + arXiv |
| 21 | Bates, S., Angelopoulos, A., Lei, L., Malik, J., Jordan, M. I. (2021). Distribution-free, Risk-controlling Prediction Sets. JACM | doi:10.1145/3478535; arXiv:2101.02703 | Crossref |
| 22 | Hultberg, B., Zachariah, D., Ribeiro, A. H. (2026). Anytime-Valid Conformal Risk Control | arXiv:2602.04364 | arXiv |
| 23 | Lekeufack, J., Angelopoulos, A. N., Bajcsy, A., Jordan, M. I., Malik, J. Conformal Decision Theory: Safe Autonomous Decisions from Imperfect Predictions | arXiv:2310.05921 | arXiv |
| 24 | Feldman, S., Ringel, L., Bates, S., Romano, Y. Achieving Risk Control in Online Learning Settings | arXiv:2205.09095 | arXiv |
| 25 | Gibbs, I., Candès, E. Adaptive Conformal Inference Under Distribution Shift | arXiv:2106.00170 | arXiv |
| 26 | Tibshirani, R. J., Barber, R. F., Candès, E. J., Ramdas, A. Conformal Prediction Under Covariate Shift | arXiv:1904.06019 | arXiv |
| 27 | Barber, R. F., Candès, E. J., Ramdas, A., Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. Ann. Statist. 51(2) | doi:10.1214/23-AOS2276 | Crossref |
| 28 | Gibbs, I., Cherian, J. J., Candès, E. J. (2025). Conformal prediction with conditional guarantees. JRSS-B | doi:10.1093/jrsssb/qkaf008 | Crossref |
| 29 | Vovk, V., Gammerman, A., Shafer, G. (2005; 2nd ed. 2022). Algorithmic Learning in a Random World. Springer | doi:10.1007/b106715; doi:10.1007/978-3-031-06649-8 | Crossref |
| 30 | Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., Zrnic, T. Prediction-Powered Inference | arXiv:2301.09633 | arXiv (Science venue unverified) |
| 31 | Jin, Y., Candès, E. J. Selection by Prediction with Conformal p-values | arXiv:2210.01408 | arXiv (JMLR per comment) |
| 32 | Podkopaev, A., Ramdas, A. (2022). Tracking the risk of a deployed model and detecting harmful distribution shifts. ICLR 2022 | arXiv:2110.06177 | arXiv (venue per comment) |
| 33 | Waudby-Smith, I., Ramdas, A. Estimating means of bounded random variables by betting. JRSS-B | doi:10.1093/jrsssb/qkad009; arXiv:2010.09686 | Crossref |
| 34 | Howard, S. R., Ramdas, A., McAuliffe, J., Sekhon, J. (2021). Time-uniform, nonparametric, nonasymptotic confidence sequences. Ann. Statist. 49(2) | doi:10.1214/20-AOS1991 | arXiv journal ref |
| 35 | Ramdas, A., Grünwald, P., Vovk, V., Shafer, G. (2023). Game-Theoretic Statistics and Safe Anytime-Valid Inference. Statistical Science | doi:10.1214/23-STS894 | Crossref |
| 36 | Vovk, V., Wang, R. (2021). E-values: Calibration, combination, and applications. Ann. Statist. 49(3) | doi:10.1214/20-AOS2020 | arXiv journal ref |
| 37 | Shafer, G. (2021). Testing by Betting: A Strategy for Statistical and Scientific Communication. JRSS-A | doi:10.1111/rssa.12647 | Crossref |
| 38 | Grünwald, P., de Heide, R., Koolen, W. Safe Testing | arXiv:1906.07801 | arXiv |
| 39 | Xu, Z., Karampatziakis, N., Mineiro, P. (2024). Active, anytime-valid risk controlling prediction sets. NeurIPS 37 | doi:10.52202/079017-1920; arXiv:2406.10490 | Crossref + arXiv |
| 40 | Ren, A. Z., et al. (2023). Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners. CoRL 2023, PMLR 229 | arXiv:2307.01928 | arXiv + PMLR |
| 41 | Liang, K., Zhang, Z., Fisac, J. F. Introspective Planning: Aligning Robots' Uncertainty with Inherent Task Ambiguity. NeurIPS 2024 | arXiv:2402.06529 | arXiv (venue per comment) |
| 42 | Abbasi Yadkori, Y., et al. (2024). Mitigating LLM Hallucinations via Conformal Abstention | arXiv:2405.01563 | arXiv |
| 43 | Gui, Y., Jin, Y., Ren, Z. (2024). Conformal Alignment: Knowing When to Trust Foundation Models with Guarantees. NeurIPS 37 | doi:10.52202/079017-2350; arXiv:2405.10301 | Crossref |
| 44 | Jung, J., Brahman, F., Choi, Y. (2025). Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement. ICLR 2025 | arXiv:2407.18370 | OpenReview API + arXiv |
| 45 | Wen, B., et al. Know Your Limits: A Survey of Abstention in Large Language Models. TACL | arXiv:2407.18418 | arXiv (venue per comment) |
| 46 | Rahman, M. A., Rahman, M. A., Samin, N. H., Tasnia, K. R., Amin, M. H., Ahona, S. R., Noshin, J. A. (2026). Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls | arXiv:2607.24343 | arXiv |
| 47 | Feng, Y., Du, J., Wang, Q., Ma, Z., Niu, Q., Matsuo, Y., Feng, L., Yu, L. (2026). CORA: Conformal Risk-Controlled Agents for Safeguarded Mobile GUI Automation | arXiv:2604.09155 | arXiv |
| 48 | Opoku, J., Banahene, D. (2026). ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift | arXiv:2606.18467 | arXiv |
| 49 | Khosravi, H., Huo, X. (2026). Conformal Selective Acting: Anytime-Valid Risk Control for RLVR-Trained LLMs | arXiv:2605.20270 | arXiv |
| 50 | Shen, J. (2026). Provable Limits and Certified Deferral for Verbalized Uncertainty in Small Language Models | arXiv:2608.05064 | arXiv (MIWAI per comment) |
| 51 | Kiyani, S., Noorani, S., Pappas, G., Hassani, H. (2026). Strategic Decision Support for AI Agents | arXiv:2606.12587 | arXiv |
| 52 | Farzaneh, A., Simeone, O. (2026). Think Short, Defer Smart, Act, and Repeat … for Edge LLM Agents | arXiv:2607.26865 | arXiv |
| 53 | Akewar, M., Ranjan, R. (2026). SafeCommit: Certifying When Memory-Grounded Agents May Safely Act | arXiv:2608.04289 | arXiv |
| 54 | Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., Tsang, I. (2026). Calibration Is Not Control: Intervention Value for LLM-Agent Oversight | arXiv:2606.21399 | arXiv (NeurIPS 2026 per comment) |
| 55 | Turan, E. (2026). Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human | arXiv:2606.08919 | arXiv |
| 56 | Overman, W., Bayati, M. (2026). Calibrating Conservatism for Scalable Oversight | arXiv:2605.28807 | arXiv |
| 57 | Piatrashyn, D., et al. (2026). ReDAct: Uncertainty-Aware Deferral for LLM Agents | arXiv:2604.07036 | arXiv |
| 58 | Shaikh, N. (2026). Knowing When to Ask for Help: Bayesian Self-Escalation in Hierarchical LLM Agents | arXiv:2608.24087 | arXiv |
| 59 | Yu, Z., Gu, Y., Partovi Nia, V., Asgharian, M. (2026). G-CARB: Graph-Localized Conformal Agent Risk Budget for Compositional Harm | arXiv:2610.05563 | arXiv |
| 60 | Yeon, J., Chaudhary, I., Singh, G. Quantitative Certification of Agentic Tool Selection | arXiv:2510.03992 | arXiv |
| 61 | Bhardwaj, V. P., Singh, G., Bhardwaj, A. P. (2026). Agent Behavioral Contracts II: Certifying Compositional Reliability Without Assuming Independence | arXiv:2608.12895 | arXiv |
| 62 | Sadhuka, S., et al. E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing | arXiv:2512.03109 | arXiv |
| 63 | ZayxShawn (2026). PACE: Anytime-Valid Acceptance Tests for Self-Evolving Agents | arXiv:2606.08106 | arXiv |
| 64 | Ramaswamy, S. (2026). Intelligence as Managed Autonomy: Failure, Escalation, and Governance for Agentic AI Systems | arXiv:2605.27628; doi:10.1007/s10846-026-02413-w | arXiv (DOI from arXiv record, not resolved) |
| 65 | Advani, L. (2026). When Small Models Are Right for Wrong Reasons: Process Verification for Trustworthy Agents | arXiv:2601.00513 | arXiv |
| 66 | Zhang, G., Cai, Y., Yu, G., Simeone, O. (2026). Prediction-Powered Risk Monitoring of Deployed Models for Detecting Harmful Distribution Shifts. ICML 2026 | arXiv:2602.02229 | arXiv + OpenReview API |
| 67 | Fernandez, M. (2026). Identity-Bound Governance Under Execution Uncertainty … (Agent Governance Series P8) | arXiv:2610.00787 | arXiv |
| 68 | Saban, N. (2026). Domain-Conditioned Safety in Frontier Computer-Using Agents … | arXiv:2606.05233 | arXiv |
| 69 | Messoudi, S., Mansar, Y. (2026). Calibration and Risk-Budgeted Decisions with System One Models | arXiv:2610.19811 | arXiv |
| 70 | Si, W., Jang, S., Lee, I., Bastani, O. Conformal Constrained Policy Optimization for Cost-Effective LLM Agents | arXiv:2511.11828 | arXiv |
| 71 | Velasevic, B., Saig, E., Mazumdar, E. (2026). Anytime Contracts for AI Services | arXiv:2610.22781 | arXiv |
| 72 | Feng, K. J. K., McDonald, D. W., Zhang, A. X. (2025). Levels of Autonomy for AI Agents | arXiv:2506.12469 | arXiv **[not read]** |
| 73 | Wang, P., Li, Y., Tian, Y. (2026). Reframing LLM Agent Security as an Agent-Human Interaction Problem | arXiv:2605.24309 | arXiv **[not read]** |
| 74 | Doula, A., Mühlhäuser, M., Sanchez Guinea, A. SafePath: Conformal Prediction for Safe LLM-Based Autonomous Navigation | arXiv:2505.09427 | arXiv **[not read]** |

**Not verified / not included.** "Vasudev et al. 2026" (cited in Calibration Is Not Control as showing that accurate failure prediction can coexist with harmful intervention) was not looked up and is not listed.
