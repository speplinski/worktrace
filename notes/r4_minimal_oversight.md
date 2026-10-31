# R4 — Minimal Oversight (Azevedo, arXiv:2606.15563): full reading

Round-4 note. Written 2026-10-25. Single work, read in full, plus its companion code. It answers the open TODO in `r3_intelligent_delegation.md`: what "sensitivity-based intervention" and "masking" mean, and whether they come closer to WorkTrace than earlier notes assumed. It also checks the summaries of this paper in `r2_learned_permissions.md` §A7 and `r3_oversight_and_profiles.md` §B.2.

**Verification legend.**
- **[verified]**: title, all authors, date and identifier checked in this session against the arXiv API (export.arxiv.org) or PyPI JSON.
- **[unverified]**: not checked.
- **[my reading]**: my interpretation, not the author's words.

Quotes are verbatim from `pdftotext` output of arXiv v1. The paper numbers only its top-level sections (1 The Principle; 2 Connections to Existing Frameworks; 3 Numerical Validation; 4 Discussion). Subsections are cited by their run-in headings.

---

## 0. Bottom line (threats first)

1. **No novelty threat to W1, W2 or W3. "Sensitivity-based intervention" is not an intervention on the agent's evidence.**
   - It means choosing *where in the workflow DAG to invest extra correction or review*: the node v with the largest ∂T*_auto/∂c(v) or ∂C_op/∂c(v), the derivative of autonomy time or quality ceiling with respect to that node's **corrector catch rate**.
   - When those derivatives are unavailable, the paper uses a proxy score S(v) = DC(v) × M*(v) × κ(v).
   - It does not perturb an agent's inputs, test whether a decision depends on any piece of evidence, or contain decisions, evidence items or declared grounds.
   - The closest thing to an input intervention is a pipeline ablation in the simulator: "removing the reviewer's corrector" and "shared source A fails". Its effect is measured as a change in aggregate success rate, with simulator parameters as ground truth.
   - The guess in `r3_intelligent_delegation.md` ("where to intervene as overseer") is **confirmed**.
2. **"Masking" means human/model correction hiding agent errors.**
   - The record of corrected outcomes makes the agent look more competent than it is: σ_corr = σ_raw + (1 − σ_raw)·c and M* = σ_corr/σ_raw.
   - The prescription is to authorise on σ_raw, logged on a pre-correction "shadow channel".
   - For WorkTrace this is a **measurement-hygiene rule for every baseline, and a framing gift**. It does not compete with our signal (§8.2).
3. **The gate is under-specified.**
   - α(x,t) ≤ α_max(x,t) = G(σ_raw(x,t)), with G only "monotone non-decreasing".
   - There are **no thresholds, no confidence bounds, no explicit revocation rule and no hysteresis**. Revocation is implicit: σ_raw decays toward a prior σ₀, so α_max falls.
   - The companion package **does not implement G at all**. Its own equation-to-code map labels Eq. 1 "Governance functional (conceptual)".
   - B-MinimalOversight is therefore *our* operationalisation. Pseudocode is in §5.
   - In the static held-out evaluation with a shared certification engine, it **collapses into B-OO**. It differs only in windowing/decay, the masking guard and the feasibility check.
4. **Claim to narrow (W2).** `positioning.md` v3 §2 W2 says that per-class, data-driven withdrawal of autonomy has been reported by no one ("nie zgłoszone przez nikogo").
   - Azevedo already has it implicitly and continuously: monotone G applied to a decaying σ_raw per task class.
   - The Digital Apprentice has explicit automatic demotion (r2).
   - What stays ours is narrower: withdrawal **triggered by failed evidence-intervention tests before outcome failures accumulate**, with hysteresis, cross-class retesting on shared requirements R_c, and a certificate tied to the configuration fingerprint.
5. **Terminology collisions to avoid.**
   - Azevedo calls the success rate σ_raw "**evidential support**".
   - He calls α_max = G(σ_raw) an **authority ceiling** that is *derived from evidence*. That is the opposite of our *fixed*, human-set permission ceiling.
   - He also uses "drift", which is already on our avoid list.
6. **No DSA-overlapping construct.**
   - His competence construct is one Bernoulli parameter, σ_raw ("raw competence", "demonstrated competence").
   - "Process entropy" H(W) treats the agent's routing and tool choices as *noise that taxes quality*, not as decisions to be tested.

---

## 1. Reading coverage

| Source | What I read |
|---|---|
| arXiv:2606.15563**v1** (the only version), PDF, 26 pp. | **In full:** abstract; symbol and notation preamble; §1 (delegation setup, MSO, Fisher metric, Return Operator, corrector and masking, delegation graphs, Euler–Lagrange solution, asynchronous GSPN dynamics, topology Table 1, delegation capacity incl. Definition 1, Theorem 1 with proofs, Proposition 2 with proof, autonomy time Proposition 3); §2 (Tables 3–4, principal–agent theory, least privilege, boundary conditions, Related Work, Computational considerations, Identifiability and measurement); §3 (semi-real workflow, Table 5); §4 (Implementation, Limitations, Conclusion); AI-assistance disclosure; references. **Figure 1** read via its caption only; the image was not inspected. **"Box 1"** is referenced in §1 ("See Box 1 for a worked example") but **does not appear in the v1 PDF text**. |
| Companion package `minimal-oversight` **v0.1.2** (the version the paper cites), PyPI sdist | **In full:** `_formulae.py`, `allocation.py`, `estimation.py`, `intervention.py`, `simulation.py`, `CHANGELOG.md`, `docs/concepts/delegation.md`, `docs/concepts/masking.md`, `docs/paper/validation.md`. **Partly:** `topology.py` (`delegation_centrality`), `capacity.py` (`check_feasibility`), `notebooks/06_paper_validation.ipynb` (cells 0–8 = Experiments 1–3 setup). **Grep only:** rest of `docs/`, `README.md`. GitHub (`crbazevedo/delegation-lab`) returned HTTP 403 through the proxy, so the code was read from the PyPI sdist, not the repo. |
| Package v0.1.3 (16 Jun 2026) | `CHANGELOG.md`; `diff` of `src/` against 0.1.2. Only docstrings changed. It adds a browser companion (`web/`), not read beyond a grep. |

---

## 2. Bibliographic data

- **Carlos R. B. Azevedo** (Independent Researcher, São Paulo, Brazil). *Minimal Oversight: Uncertainty-Aware Governance for Delegated AI Systems.* arXiv:2606.15563v1, submitted 4 Jun 2026. Primary cs.AI; cross-listed cs.IT, cs.MA. Single author.
- arXiv comment: "Companion Python package: pip install minimal-oversight | Code: https://github.com/crbazevedo/delegation-lab | 26 pages, 1 figure, 5 tables".
- No journal reference, no DOI, no venue. **[verified]** (arXiv API).
- Companion package `minimal-oversight` on PyPI: 0.1.0 (31 Mar 2026), 0.1.1 and 0.1.2 (4 Jun 2026), 0.1.3 (17 Jun 2026). **[verified]** (PyPI JSON).
- **Earlier framing.** The package's notebook 6 calls the paper "*Minimal Oversight: A Theory of Principled Autonomy Delegation*", and the 0.1.2 changelog replaces "Axiom of Minimal Oversight" with "Minimum Sufficient Oversight Principle".
  - The package also cites "Section 4, Demonstration 1–7" and "Table 7", which do not exist in arXiv v1.
  - [my reading] So a longer, differently titled draft existed. Cite only arXiv v1.
- An arXiv author search (au:Azevedo with delegation/oversight/masking) found **no other paper by this author** on the topic.

---

## 3. Problem and contribution

Abstract: the problem is "how much autonomy to grant, which evidence should calibrate trust, what performance ceiling a delegated AI system can sustain, and when human intervention becomes necessary".

Contributions:
- the **Minimum Sufficient Oversight Principle (MSO)**, a variational problem on the Bernoulli Fisher manifold;
- a **water-filling** solution;
- a **delegation-capacity theorem**, Theorem 1, for a "revealed-action governed delegation channel" with stationary symbolwise review;
- a **local process-complexity sensitivity law**, Proposition 2: σ*_raw ≥ C_op − λH(W);
- a **drift-dominated autonomy-time law**, Proposition 3: T*_auto = B_eff/μ_eff with B_eff = C_op − p_min − λH(W);
- **masking**, presented as "the first pathology the theory exposes" (§1 intro): "It is not the main object of the theory".

The paper's stance is that its contribution is a *calculus for placing oversight in a pipeline*. It is not an evaluation of agents: "This is not a replacement for safety evaluation or deployment testing; it is a calculus for deciding where such evaluation and oversight are most valuable" (§4, Implementation).

---

## 4. Method, answering questions (a), (b) and (f)

### 4.1 Setup and units

> "A delegation consists of a principal A, an agent B, a scope S (the set of tasks B is authorized to perform), and a corrector C that observes B's outputs and applies corrections. At each point x ∈ S, the agent produces outcomes; the corrector reviews a subset." (§1, The delegation setup)

- **Authorisation unit:** the scope point or **task class x**. α(x,t) ∈ [0,1] is "the fraction or weight of task class x allowed to be handled by the delegated system during interval t under the available governance regime" (§1, MSO).
  - In the experiments, x is a synthetic grid cell, from 6×6 to 20×20, or N = 80–144 "scope points" indexed by a competence value.
  - Task classes are never given semantic content, and there is no account of how classes are formed.
- **Intervention unit:** a **node v of the workflow DAG**, i.e. a pipeline stage or role such as generator, reviewer, test, security or merge. The package computes everything per node.
- **There is no decision-level unit.** Outcomes are binary success/failure. Decisions, alternatives, evidence items and grounds do not exist in the model.

### 4.2 (a) What "sensitivity-based intervention" is

It is used in three places:

> "For delegation DAGs, the principled improvement target is the local sensitivity ∂T*_auto/∂c(v) or its finite-difference approximation; when exact sensitivities are not available, the proxy score S(v) = DC(v) × M*(v) × κ(v) remains computable after a single topological sort" (§2, Computational considerations)

> "The governance target should therefore be chosen by sensitivity—for example ∂T*_auto/∂c(v) or ∂C_op/∂c(v)—rather than by local error rate alone." (§4)

> "4. Allocate scarce human or model review to the node with the largest estimated gain in C_op or T*_auto." (§4, Implementation)

Table 1 says the same in its last row: "Invest where ∂C_op/∂c(v) or ∂T*_auto/∂c(v) is largest, not where local quality is merely lowest."

**What is perturbed.** The derivative is taken with respect to **c(v), the corrector's catch rate at node v**. That is the overseer's strength, not the agent's input or evidence.
- **DC(v)** ("delegation centrality") is never defined in the paper. In the package (`topology.py`) it is out-degree × (1 + Σ_descendants 1/distance).
- **κ(v)** is never defined in the paper. In the package (`_formulae.sota_priority_score`) it is κ = 1 − σ_skill(v), "task complexity".
- The package calls S(v) the "SOTA priority score (Heuristic)".

**Answers to the specific questions.**
- *Does it intervene on the agent's evidence and measure whether decisions depend on it?* **No.**
- *On what unit?* Pipeline **nodes**, not task classes and not actions.
- *With what ground truth?* None in an empirical sense. The quantities are closed-form functions of the simulator's own parameters (σ_skill, c, η, δ, K/N). Section 3 says: "they test whether the closed-form quantities and scaling laws match the simulator generated from the same assumptions."

**The closest analogues to an input intervention** (all in the mean-field simulator, all measured on aggregate success rates):
- **Eq. 7.** σ_skill,eff(v) = σ_skill(v) × AGG(σ_corr(u₁), …, σ_corr(u_k)). A node's effective success depends on the *quality* of its parents' outputs, combined by product, min or weighted mean.
  - This is a *modelled* dependence on input quality, assumed rather than tested.
  - There is no notion of *which* input a decision uses, or of redundancy between inputs.
- **Experiment 5 / Fig. 1C.** "Removing the reviewer's corrector cascades Δσ_raw to three downstream branches simultaneously"; the cascades total −0.087 (Table 5). This is an ablation of a corrector node, not of an evidence source.
- **Diamond motif.** "quality at D drops 29% when the shared source A fails" and "1.4× fragility ratio" (§1, Remark (DAGs); Table 5). This conditions on an upstream node failing.
  - [my reading] It is the nearest thing to our "shared-provenance/redundancy" concern: correlated parents through a shared source.
  - It is stated at the level of success rates, as a diagnostic ("diagnose by conditional failure, not averages", Table 1). It is not a test of the agent.
- **Experiment 1.** The corrector is removed at step 125 "to reveal the true competence" (notebook 6). This is an intervention on the *overseer*.

The word "sensitivity" also appears in Proposition 2, the "Local Process-Complexity Sensitivity Law": quality falls by λ ≈ 0.02 per bit of workflow entropy. That too is unrelated to evidence-sensitivity.

### 4.3 (b) What "masking" is

> "In delegated systems, the process that preserves output quality can also destroy the information needed to calibrate trust. When corrected performance is used as the basis for authority, oversight can hide deterioration in the producing agent. We call this masking." (§1 intro)

> "Authorization must be based on σ_raw—not on σ_corr, which conflates the agent's competence with the corrector's diligence." (§1, The delegation setup)

**Quantities.**
- σ_raw(x,t) is "the empirical success rate of B's uncorrected outcomes at x, computed as the running fraction of correct outputs in the accumulated records R(t)". The paper calls it **"Evidential support"**.
- σ_corr is the success rate after correction.
- Eq. 6: σ*_corr = σ*_raw + (1 − σ*_raw)·c.
- Masking index: M* = σ*_corr/σ*_raw = 1 + (1 − σ*_raw)c/σ*_raw. The worked example (σ*_raw = 0.667, c = 0.70) gives M* = 1.35.

**Masking compounds with depth.** Corrected outputs feed downstream layers, so per-layer M* grows (1.77 → 2.20 over five layers) and total masking is "super-multiplicative": 14.3 in Fig. 1 under one parameter set, 38.7 in Table 5 under another.

**The cure.** "Dual tracking": "log both pre-correction and post-correction outcomes at every delegation boundary and track M* = σ_corr/σ_raw" (§4).
- **Identifiability caveat (Table 4):** σ_raw is only "Partial[ly]" observable. It requires a "pre-correction slice / shadow channel / synthetic estimator", and its "main failure mode" is "Leakage between corrected and raw channels".
- **Diagnostic differential** (§2 mention; table in the package docs): the joint trend of (Δσ_raw, ΔM*) over two consecutive windows.
  - falling/rising = "agent degrading, masked";
  - stable/rising = "corrector coasting";
  - and so on.

**Headline number.** "single-σ governance over-authorizes by 36%" (Table 5, Experiment 1).
- **Caution:** the companion notebook does **not** compute the 36%. It prints the hard-coded string "Paper reports: single-σ governance over-authorizes by 36% (α inflation)".
- A comment in the notebook guesses at how it was measured.
- The over-authorisation metric is never defined in the paper.

### 4.4 The gate, the allocation and revocation, as specified

- **Authority ceiling (Eq. 1):** "A baseline trust policy may map evidential support to a maximum allowed intensity, α(x,t) ≤ α_max(x,t) = G(σ_raw(x,t)), where G is monotone non-decreasing."
  - **G is never given**: no functional form, no thresholds, no confidence bounds.
  - The package maps Eq. 1 to "Governance functional (conceptual)" (`docs/paper/references.md`). `alpha_max` is a scalar constant (default 1.0) in `solve_mso`.
- **MSO allocation under the ceiling (Eqs. 2, 8):** α*(x) = min(α_max(x), (λ/2)·σ_raw·√(σ_raw(1 − σ_raw))), with λ set by the delivery constraint ∫α σ_raw dx ≥ p_min|S|.
  - It "peaks at intermediate competence (σ ≈ 0.75)" and tapers for σ → 1, because "review rarely finds errors".
  - [my reading] This confirms that α is *governed (reviewed) workload intensity*, not autonomy in our sense. It cannot be used as a delegation rule: it would give a near-perfect agent less delegation.
- **Evidence dynamics (Eq. 4), the Return Operator:** ∂σ_raw/∂t = η(σ_skill − σ_raw) − δ(σ_raw − σ₀). Fixed point: σ* = (ησ_skill + δσ₀)/(η + δ).
  - The **learning target is the true σ_skill**: the ODE is mean-field, not a per-observation estimator.
  - With the paper's default "conservative" σ₀ = 0, the **raw support can never exceed η/(η + δ) = 0.833** for η = 10, δ = 2 (§1, Delegation capacity: "the raw-support ceiling is η/(η + δ)").
  - [my reading] A threshold above 0.833 is unreachable under that convention, so a faithful baseline must pick σ₀ deliberately (§5).
- **Feasibility before expansion:**
  - B_eff = C_op − p_min − λH(W) > 0 (Eq. 16).
  - Corrector capacity threshold: K/N ≥ max(0, (p_min − σ*_raw)/[(1 − σ*_raw)c]).
  - Implementation step 3: "Check feasibility using C_op and B_eff before expanding autonomy."
  - When infeasible, "the MSO does not prescribe 'more authority'—it prescribes no delegation under the current design" (§1).
- **Estimation:** "Estimate σ_raw, σ_corr, M*, H(W), and local drift over rolling windows" (§4, Implementation step 2).
  - The package's `estimate_sigma_raw(outcomes, window=None)` is a plain mean over the last `window` outcomes.
  - Drift μ_eff is the negative slope of a linear fit to rolling-window means (window 50, step 10).
  - Bootstrap CIs are optional and are never used in any gate.
- **Revocation:** there is **no explicit revocation rule**. Withdrawal happens implicitly in three ways:
  - (i) σ_raw falls with failures or decays toward σ₀ when evidence goes stale, so G lowers α_max;
  - (ii) a "minimum human intervention frequency" f(v) = 1/T*_auto(v), solved as an LP over nodes;
  - (iii) package alerts at M* > 1.5 (warning) / > 2.0 (critical) and B_eff < 0.05.
  - There is **no hysteresis** and no cross-class propagation.
- **Endogenous scope (§1, "Scope and geometry"):** with d(x) ∈ {0,1}, the optimiser "may delegate only a small high-competence subset" ("cherry-picking"). It needs a coverage constraint ∫d(x)w(x)dx ≥ W_min.
  - [my reading] This is the same coverage-matching concern our risk–coverage evaluation handles.
  - The package's `select_scope` is a greedy heuristic: it delegates by σ·√(σ(1 − σ)), then adds any task with σ ≥ 0.8·p_min.

### 4.5 (f) Constructs and whether any overlaps DSA

| Azevedo construct | Content | Overlap with DSA |
|---|---|---|
| σ_raw, "raw competence", "demonstrated competence", "evidential support" | Pre-correction Bernoulli success rate per scope point | **None** beyond "outcome history". This is exactly the track record DSA is meant to go beyond. |
| σ_corr, "delivered quality" | Post-correction success rate | None |
| Masking index M* | σ_corr/σ_raw | None (it is a measurement-bias diagnostic) |
| Process entropy H(W) | H(routing) + H(tool calls) + H(timing) of the workflow, "the number of decisions agents make, the stochasticity of routing" | **Superficial.** It mentions agents' decisions, but only as stochasticity that taxes quality. It does not test whether decisions are grounded or whether decision points are recognised. |
| Delegation centrality DC(v) | Structural leverage of a node | None |
| Autonomy time T*_auto, buffer B_eff | Survivability of quality margin under drift | None (system-level). The idea of a re-test cadence is relevant to our certificate expiry. |

**Verdict.** Nothing here names or measures receptivity or reactivity to evidence, authority scope, escalation correctness, revision after correction or provenance. Minimal Oversight poses **no construct threat** to DSA.

---

## 5. (c) B-MinimalOversight: implementable pseudocode

### 5.1 Design choices

The paper leaves G, the thresholds, the window and the revocation logic open, so every choice below is ours and must be reported as an operationalisation. **[my reading]** throughout.

- **Masking guard (faithful, central):** σ_raw is computed on the **agent's own proposal** in every episode, whether the verdict was proceed or escalate. In our generated episodes the ground truth is known, so the "shadow channel" of Table 4 is exact. Escalated, human-corrected episodes **never** count as agent successes.
- **G:** primary = **step function** G_τ(σ) = 1[σ ≥ τ], because our verdicts are per class (proceed/escalate). Sweep τ to trace the risk–coverage curve.
  - Variant = linear ramp G(σ) = clip((σ − σ_lo)/(σ_hi − σ_lo), 0, 1), applied as a *randomised* per-episode proceed probability. Report it only as a sensitivity check.
- **Estimator:** primary = **rolling-window mean**, W ∈ {25, 50, 100}. This matches §4 Implementation step 2 and `estimate_sigma_raw(window=…)`.
  - Variant = the per-observation discretisation of Eq. 4: σ ← σ + a(y − σ) − b(σ − σ₀), with a:b = η:δ = 5:1 (e.g. a = 0.05, b = 0.01) and σ₀ ∈ {0, 0.5}.
  - Note the reachable maximum a/(a + b) = 0.833 when σ₀ = 0.
- **Feasibility check (faithful to step 3):** expand only if the class's uncorrected autonomous quality meets the target (q* = σ_raw for an uncorrected output stage) **and** the escalation load of the non-autonomous classes fits reviewer capacity. The latter is the analogue of the K/N threshold.
- **No hysteresis and no confidence bound in the faithful version.** In the "engine-matched" version, the same Clopper–Pearson/LTT engine and the same hysteresis as WorkTrace are applied to σ_raw.
  - **That version is B-OO plus windowing.** See §5.3.

### 5.2 Pseudocode

```
# B-MinimalOversight (faithful operationalisation of Azevedo 2026, Eq. 1 + §4 Implementation)
# Inputs:
#   stream E of episodes in chronological order, each e with: class c(e), agent_proposal(e),
#     correct_action(e) [from generator], final_action(e) [after escalation, if any]
#   params: tau (gate threshold, swept), W (window) or (a, b, sigma0) for leaky variant,
#           p_min (per-class autonomous-quality target), K_max (escalations per review period),
#           review_every (episodes between gate re-evaluations), c_h (reviewer catch rate, for sigma_corr only)

init for every class c:
    buf[c]      = empty FIFO of max length W          # rolling-window variant
    sigma[c]    = sigma0                               # leaky variant
    verdict[c]  = ESCALATE                             # start with no autonomy

for t, e in enumerate(E):
    c = class(e)
    # --- act under current verdict ---
    if verdict[c] == PROCEED:  executed = agent_proposal(e)
    else:                      executed = human_decision(e)      # simulated reviewer, catch rate c_h
    # --- record (MASKING GUARD) ---
    y_raw  = 1[agent_proposal(e) == correct_action(e)]          # always logged: shadow channel
    y_corr = 1[executed == correct_action(e)]                   # logged for diagnostics only
    buf[c].push(y_raw)                                          # rolling-window variant
    sigma[c] = sigma[c] + a*(y_raw - sigma[c]) - b*(sigma[c] - sigma0)   # leaky variant
    # --- periodic gate re-evaluation (implicit revocation) ---
    if t % review_every == 0:
        for each class k:
            s = mean(buf[k]) if len(buf[k]) >= n_min else sigma0       # or sigma[k]
            alpha_max = G_tau(s)                                        # 1[s >= tau]
            feasible  = (s >= p_min)                                    # q* = sigma_raw for uncorrected output
            verdict[k] = PROCEED if (alpha_max == 1 and feasible) else ESCALATE
        # capacity feasibility (analogue of K/N >= (p_min - sigma)/((1 - sigma) c)):
        load = expected escalations next period = sum over k with verdict ESCALATE of rate(k)
        if load > K_max:
            report INFEASIBLE   # Azevedo: "no delegation under the current design"; do NOT relax tau
        # optional diagnostics (not used for gating): M*(k) = mean(y_corr)/mean(y_raw);
        # differential (Δsigma_raw, ΔM*) between consecutive windows; T*_auto = B_eff / mu_eff

Ablation B-MO-corr ("single-σ", the masked rule): identical, but buf[c].push(y_corr).
  Expected behaviour: escalated classes look near-perfect (y_corr ≈ c_h-corrected), get promoted,
  then fail -> oscillation. This reproduces Azevedo's masking claim inside our harness.
```

**Static held-out evaluation (the W3 primary endpoint).**
- Run the stream on the calibration split.
- Freeze the verdicts and apply them to the held-out, evidence-shifted episodes.
- Sweep τ to obtain the risk–coverage curve.
- The **online variant** keeps updating on the held-out stream. Report **errors committed between the evidence shift and the first revocation**. This is the only place where B-MO's windowing and decay behave differently from B-OO.

### 5.3 Relation to B-OO

With one certification engine for all rules (`positioning.md` §2 W3), "B-MO-certified" applies the Clopper–Pearson lower bound to σ_raw per class. **That is B-OO**, except for the rolling window or decay and the p_min feasibility check.

Recommendations:
- **(i)** In the static held-out comparison, report **B-OO as "per-class raw-success gate (Azevedo 2026; masking-guarded)"** rather than as a separate B-MO row. This avoids two near-identical baselines.
- **(ii)** Keep B-MO as a separate rule only in the **online/sequential** experiment, where windowing and decay matter.
- **(iii)** Add **B-MO-corr**, the masked single-σ rule, as a sanity ablation. It shows that our harness reproduces masking and that every other baseline is masking-guarded.

---

## 6. (d) Evaluation details

- **Type:** "internal model checks rather than external field validation" (§3). Simulator: "a mean-field ODE model with Bernoulli outcome noise over N = 80–144 scope points"; "200–400 steps over n = 20–30 independent seeds".
- **Default parameters:** η = 10, δ = 2, σ_skill = 0.55–0.80, c = 0.65–0.70, K/N = 0.50.
- **Corrector model:** "σ_corr = σ_raw + (1 − σ_raw) c (K/N)". The paper adds: "This is not a holdout measurement protocol".
- **Noise:** in the package, the noise is Gaussian with sd 0.01/√n_scope added to the ODE state, not per-item Bernoulli draws.
- **Eight experiments (Table 5; `docs/paper/validation.md`):**
  1. masking (M* ≈ 1.4; "single-σ governance over-authorizes by 36%");
  2. communication/routing (σ* 0.545 → 0.579, +6.1%; routing ≈ 53% of the gain);
  3. bottlenecks (capacity loss −0.106 > adversarial drift −0.035 > correlations −0.008 > heterogeneity −0.002);
  4. linked chains (per-layer M* 1.77 → 2.20; total 38.7);
  5. DAG motifs (cascade −0.087; diamond fragility 1.4×);
  6. capacity (theory–simulation gap ≤ 0.002 over 28 conditions);
  7. process entropy (λ ≈ 0.02/bit);
  8. autonomy time (log–log slope −0.99).
  - Robustness: grid 6×6–20×20, catch rate 0.30–0.90, skill distributions uniform/Gaussian/bimodal: "the qualitative results persist".
- **Semi-real reconstructed workflow:** 2,400 items over four windows; generator → reviewer → {test, requirements, security} → merge.
  - Results: reviewer σ_raw = 0.62, σ_corr = 0.90, M* = 1.45; H(W) = 2.3 bits; C_op ≈ 0.86; p_min = 0.75; B_eff ≈ 0.064; μ_eff ≈ 0.012; T*_auto ≈ 5.3 time units.
  - The data source and the reconstruction procedure are **not described**.
- **Baselines:** none. The paper itself says: "the main experiments do not compare against strong baselines such as bandit allocation, queue-aware control, active learning, or software-testing heuristics. These are not small caveats." (§4, Limitations)
- **No LLM agents, no real outcomes, no held-out split.** Limitations also states: "The agents do not strategically adapt to the corrector; the corrector catch rate is fixed; the outcomes are binary; the nodes are conditionally independent".

---

## 7. (e) Threat assessment and differentiation

### 7.1 What Minimal Oversight covers that WorkTrace must NOT claim

- Per-task-class authority computed from accumulated, decaying behavioural evidence (Eq. 1 + Eq. 4).
- That corrected or delivered outcomes mislead authorisation, and that the rule must use pre-correction outcomes logged on a shadow channel (masking, M*).
- A feasibility check before autonomy is expanded; reviewer-capacity thresholds; "no delegation under the current design" when the target is infeasible.
- Continuous, data-driven withdrawal per class as a consequence of falling evidence (implicit, via G and decay).
- A re-review cadence derived from a quality buffer and drift (T*_auto).
- That endogenous scope selection cherry-picks easy classes without a coverage constraint.
- Information-theoretic or variational framing of oversight allocation in delegation pipelines.

### 7.2 What it leaves open that WorkTrace addresses

- **The signal.** σ_raw is an outcome rate. It cannot separate right-for-the-right-reason from right-for-the-wrong-reason, because both give y_raw = 1. Azevedo's question "which evidence should calibrate trust" is answered with *which outcome stream*; ours is answered with *how the agent's decisions respond to the evidence it was given*.
- **Decision structure.** It has no decisions, evidence, grounds, escalation correctness or authority-scope adherence.
- **The unit.** Task classes are unstructured grid cells; it has no notion of requirements R_c or transfer between classes.
- **Statistical guarantees.** G is unspecified and there are no confidence bounds or per-class risk certificates.
- **Empirical comparison.** There are no agents, no held-out data and no baselines.
- **The fixed permission ceiling.** Azevedo's "ceiling" is itself evidence-derived; nothing caps it from above with a human-set limit.

### 7.3 Per-claim verdicts and differentiation sentences

**W1 (DSA construct): no threat.**
> Azevedo (2026) models delegated competence as a single Bernoulli success rate per task class and shows that it must be measured before correction; DSA instead measures whether an agent's decisions have the structure of decisions—grounded in the decisive evidence, bounded by authority, escalated when warranted—which a success rate, raw or corrected, cannot reveal.

**W2 (DSA-based delegation rule): no method threat; narrow one sub-claim.**
> Minimal Oversight caps each task class's delegated share by a monotone function of its decaying raw success rate, leaving the function, thresholds and revocation rule unspecified; WorkTrace issues per-decision-class certificates whose loss counts right actions on the wrong basis, detects that basis by evidence interventions rather than outcomes, keeps autonomy beneath a fixed human-set permission ceiling, and withdraws it when intervention tests fail—before outcome failures accumulate.

**Narrowing required:** data-driven per-class withdrawal is not new (Azevedo implicitly; Digital Apprentice explicitly). Claim only the trigger (intervention tests), hysteresis, cross-class retesting on shared R_c, and fingerprint-bound expiry.

**W3 (predictive-validity test): no threat.** It strengthens the motivation and supplies a baseline.
> Azevedo validates his allocation rule only against a simulator built on the same assumptions and reports no baselines; we test, on held-out generated episodes under evidence shift, whether a DSA-based gate predicts autonomous errors better than his masking-guarded raw-success gate at matched coverage.

**Framing sentence for the introduction** (it credits Azevedo and sets up our step):
> Azevedo (2026) shows that corrected outcomes mask an agent's raw competence and that authorisation must use pre-correction outcomes; we argue that raw outcomes mask something further—whether a correct action was taken for the right reason—and that this second layer is exposed only by intervening on the evidence.

---

## 8. Implications for WorkTrace

### 8.1 Claim changes

1. **`positioning.md` §2 W2, revocation bullet.** Replace "Odebranie na podstawie danych, per klasa, z histerezą: nie zgłoszone przez nikogo" with the narrower claim: withdrawal per class **triggered by failed evidence-intervention tests** (before outcome failures), with hysteresis and cross-class retesting on shared R_c. Cite Azevedo (implicit decay-based withdrawal) and the Digital Apprentice (explicit demotion) as prior data-driven withdrawal.
2. **Terminology.**
   - Never use "evidential support" for anything of ours; Azevedo uses it for the success rate.
   - When citing him, write "his authority cap α_max = G(σ_raw)", and reserve "ceiling" for our fixed, human-set permission ceiling. Say explicitly that the two point in opposite directions: his is derived from evidence, ours can never be raised by evidence.
   - Do not adopt "Return Operator", "governed delegation" or "drift" (the last is already on the avoid list).
3. **"Which evidence should calibrate trust."** This phrase is in Azevedo's abstract. If we use similar wording ("what evidence should autonomy rest on"), cite him and state the difference: outcome *streams* vs *the agent's evidence-handling*.

### 8.2 Design changes

1. **Masking guard for all rules (confirms r3 §C.2).**
   - Every rule's statistics use the agent's *pre-escalation proposal* scored against generator ground truth, in all episodes including escalated ones.
   - The decision-episode record must store the **agent's pre-correction action and declared grounds** separately from the human's final action. This is Azevedo's "dual tracking" applied to E.
   - Note it in the episode definition.
2. **Avoid absorbing revocation.** If a rule stopped observing a class after revocation (no shadow channel), the window would freeze or σ would decay to σ₀ = 0, and the class could never be re-promoted.
   - Our harness always has the agent's proposal, so this is moot for evaluation.
   - For deployment, say that re-promotion requires either shadow-mode proposals or scheduled re-testing. WorkTrace has the second by design: interventions are run by the external evaluator.
3. **Escalation as a corrector.**
   - [my reading] Agent-initiated escalation is itself a correction channel. An agent that escalates whenever unsure has high delivered quality and unknown raw competence.
   - DSA already scores *whether escalation was warranted* against generator ground truth. Make explicit that this is what prevents escalation-induced masking from inflating the profile.
   - Count agent-initiated escalations as decisions (scored), not as successes.
4. **Add B-MO-corr as a sanity ablation** (§5.2), and the "errors before first revocation after shift" endpoint in the online variant (§5.2), where B-MO is the natural comparator.
5. **Cost model.**
   - Keep Azevedo's corrector-capacity feasibility (already in r3 §C.2) and his "infeasible → no delegation, do not relax τ" rule for all baselines.
   - Do **not** adopt his α²√g cost: it gives near-perfect agents less delegation (Eq. 8) and models review intensity, not autonomy.
   - The reviewer catch rate c in his Eq. 6 corresponds to our reviewer reliability r(ℓ). Cite it there.
6. **Expository parallel.**
   - Azevedo's Experiment 1 removes the corrector "to reveal the true competence".
   - Our evidence-shift split removes redundant or shortcut evidence to reveal the true basis.
   - [my reading] This makes a clean two-layer story for the introduction: correction masks raw competence (Azevedo); outcome success masks decision basis (us). It decomposes σ_raw = P(correct ∧ right basis) + P(correct ∧ wrong basis). The second term is what our loss counts as unjustified, and what turns into errors under evidence shift.
   - **Use "basis masking" only as an explicitly credited analogy, not as a new term.**
7. **Diamond / shared-source fragility.** Azevedo's diamond result (correlated parents through a shared source) is a system-level counterpart of our provenance-independence requirement for the "add an independent second source" intervention. Optionally cite it in the paragraph defining "independent = distinct provenance or control domain".

### 8.3 Things to cite (with role)

| Cite | Role |
|---|---|
| Azevedo 2026, arXiv:2606.15563 **[verified]** | (i) Masking: why delegation statistics must use pre-correction agent behaviour. (ii) Prior per-class gating on outcomes with decay and a feasibility check; template for the raw-success baseline. (iii) Oversight-capacity feasibility. |
| Fudenberg & Liang, "Friend or Foe: Delegating to an AI Whose Alignment is Unknown", arXiv:2509.14396 (Drew Fudenberg, Annie Liang; 2025) **[verified: arXiv API, abstract not read]** | Optional. Economics of delegating to an AI of uncertain alignment; cited by Azevedo. Read before citing. |
| Engels, Baek, Kantamneni, Tegmark, "Scaling Laws For Scalable Oversight", arXiv:2504.18530 (2025) **[verified: arXiv API, not read]** | Optional, for an oversight-capability-gap remark. |

### 8.4 Risks

- **Reviewer objection: "Just use σ_raw with dual tracking."** Answer with W3: B-OO/B-MO is masking-guarded in our harness, and the claim is that it still over-authorises under evidence shift, because σ_raw counts right-for-wrong-reason successes. If B-OO matches WorkTrace at matched coverage, H3 fails for this baseline and must be reported.
- **Straw-man risk.** G is unspecified, so any B-MO is our construction. Pre-register τ grid, W, a/b, σ₀ and p_min, and report sensitivity across them.

### 8.5 Citation cautions

- Single-author, unrefereed preprint with LLM-assisted drafting disclosed: "Claude Code and Codex, using models identified by the author as Claude Opus 4.7 and GPT-5.5".
- Validation is internal only (the simulator is built from the same equations). No baselines. The semi-real workflow's provenance is not described.
- **Internal inconsistencies:**
  - M* "≈ 1.8 in the standard single-layer delegation" (§1) vs "≈ 1.4" (Table 5). The package footnote explains this: c vs c·K/N as the effective catch rate.
  - Total masking 14.3 (Fig. 1) vs 38.7 (Table 5).
  - "Box 1" is referenced but absent.
  - DC(v) and κ(v) are used but not defined in the paper (only in the code).
  - The package cites "Section 4, Demonstration 1–7" and "Table 7", which are not in v1.
- **The "36% over-authorization" figure is not reproduced by the companion notebook** (hard-coded print), and its metric is undefined. Do not cite the number. Cite the qualitative masking argument only.
- **α semantics are muddled.** α is "governed delegation intensity"; the water-filling solution tapers to 0 as σ → 1. Do not describe α* as "autonomy granted" when citing.
- **Corrections to earlier notes:**
  - `r2_learned_permissions.md` §A7 says "evidence decays toward a prior … i.e., revocation by forgetting". That is right, but the ODE's learning target is the *true* σ_skill (mean-field), and there is no explicit revocation rule.
  - `r3_oversight_and_profiles.md` §B.2 is otherwise accurate. "G is never specified" is confirmed, and the package does not implement it either.
