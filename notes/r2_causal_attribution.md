# Round 2: counterfactual and causal-attribution approaches to agent decisions. Reading note for WorkTrace

Works covered:

1. Counterfactual Trace Auditing (CTA), Zhou et al., arXiv:2605.11946.
2. AUDITA, Du & Chen, arXiv:2608.22160.
3. Causal Attribution for Agentic Decisions, Mahale, arXiv:2609.06445.
4. Evidence-Ledger Adjudication, Chen, Yu & Wang, arXiv:2607.26512.

Date of reading: 2026-10-25.

## Coverage of this reading

For all four papers I downloaded the arXiv PDF (latest version) and the arXiv HTML. I read the full PDF text, extracted with `pdftotext -layout`, from start to finish. Figures were seen only as extracted text labels and captions, some of them garbled. Nothing was skipped.

| Work | Version | Pages | What I read |
|---|---|---|---|
| CTA | v2 | 18 | Main text §1–§8, App. A (five case-study trace diffs), references |
| AUDITA | v2 | 43 | Main text (Introduction, Methods, Results, Discussion), Extended Data Figs 1–2 and Tables 1–2, Supplementary Notes S1–S10 (including every proof and Extended Data Fig. S1), references |
| Mahale | v1, the only version | 23 | §1–§10, App. A (traceability spec R1–R12), App. B (coupling table), references |
| Evidence-Ledger | v1 | 10 | Everything |

**Other works mentioned below (not part of the assignment).** For these I read only the arXiv abstract or metadata, and say so each time they come up: Liao 2607.20827, HANSARD 2608.22512, Shah 2606.08275, CausalFlow 2605.25338, Mishra & Sharad 2606.09692.

**Verification.**
- All arXiv metadata was checked with the arXiv API on 2026-10-25.
- Classic references were checked with Crossref (DOIs given below).

---

## 1. AUDITA: Du & Chen, arXiv:2608.22160

### 1.1 Bibliographic data [verified: arXiv API]

- **Title.** *AUDITA: certified auditing and causal attribution of adverse outcomes in autonomous multi-agent systems.* The PDF typesets it as "Audita".
- **Authors.**
  - Zhixu Du, Duke University, Department of Electrical and Computer Engineering. Corresponding author.
  - Yiran Chen, Duke University, Department of Electrical and Computer Engineering.
- **Year and versions.** 2026. v1 23 Aug 2026; v2 29 Aug 2026. I read v2.
- **Category.** cs.AI.
- **Venue.** None stated; it is a preprint. The layout is Nature-style ("Methods", "Extended Data", "Data availability"), but no journal is named. Do not speculate about the venue.
- **Code and data.** github.com/ZhixuDu/audita (MIT licence). Not inspected.

### 1.2 Problem & contribution

**Problem.** When a multi-agent system made of LLM planners, tool agents, robot controllers and human supervisors causes harm, existing attribution has two flaws:
- it reads logs whose integrity cannot be verified;
- it names a single culprit.

The single-culprit answer is wrong when outcomes are "overdetermined (two commands, either sufficient), preempted (the blamed command's effect never arrived), or caused by omission (a supervisor who never issued the required halt), and responsibility is then a matter of degree, not a pointer" (Introduction).

**Contribution.** An audit layer with two parts:
1. **Evidence layer.** Signed, citation-carrying, Merkle-sealed messages.
2. **Causal layer.** "Gate, grade, certify":
   - production gate;
   - modified Halpern–Pearl actual causation with Chockler–Halpern degree of responsibility;
   - replay certification.

**Verdict format.** A four-part negligence verdict (duty / breach / causation / harm) per principal.

**Theorems.**
- Culpability groundedness (Thm 1).
- Blame-shift certificate (Thm 2).
- No silent exoneration (Thm 3).
- Completeness barrier (Thm 4).
- Grounded framing at every order (Thm 5).

**Benchmark.** CulpaBench, built from structures grounded in 42 public robot-accident records.

### 1.3 Method

**Unit of evidence.** The message m = (a, π, C, φ, σ): author, payload, citation set, committed effect predicate, signature (Definition 1). The authors stress:

> "Citation is an admission: by citing m′, the author of m attests that m was issued because of m′, making the edge an authored causal claim rather than an inferred correlation." (Methods, "The accountable command graph")

**Verification partition.** The record is split into G_cert, a suspect set and a missing set. All attribution runs on G_cert.

**Adverse outcome.** A declared predicate Y over world or work state. The incident slice is the causal past of Y in G_cert (Definition 2).

**Structural causal model (SCM).**
- One binary presence variable per certified message.
- One **duty-indexed absence variable** per required-but-unissued intervention. An omission is "a first-class variable, not a gap".
- Mechanisms are induced by the citation structure and the actuation semantics.

**Gate (factual production).** A candidate enters only if it has an intact production path to Y, meaning its committed effect φ "was realised and propagated into the state that made Y true". This "retires preempted candidates (commands whose effect never reached the outcome) before any counterfactual is computed" (Methods). Prop. 2 (preemption retirement): with no intact production path, ρ = 0 plus an exoneration note.

**Grade (counterfactual dependence).** Modified Halpern–Pearl:

> "X\* is an actual cause of Y if there is a witness set W\*, frozen at its actual values, such that setting X\* to its counterfactual values falsifies Y, with X\* minimal."

The grade is ρ(X\*, W\*) = 1/(|X\*| + |W\*|), Eq. (1). A principal's responsibility is ρ_p = max over minimal certified causes that contain one of its messages, Eq. (2). The authors also state:
- "These degrees are not a normalised allocation and need not sum to one across principals."
- "Redundancy (two independently sufficient commands) yields ρ = ½ each rather than an arbitrary single culprit."
- Faithful relays get a **conduit** flag.

**Certify (counterfactual replay).** Each reported cause is re-executed with X\* intervened on and W\* frozen. The risk of Y must fall by at least δ.
- **Pinned stack** (exact):
  - open weights, greedy decoding, fixed seed;
  - "serial replay protocol": one replay at a time on an idle server. The paper says concurrent batching "voids bitwise exactness even in batch-invariant serving modes".
- **Hosted stack** (statistical): n independent replays per arm. A cause is reported only if q̂₀ − q̂₁ ≥ δ + 2ε, with ε(n, α) = √(ln(4/α)/(2n)) from Hoeffding plus a union bound (proof of Prop. 1, Note S2). An **action-match score** is reported alongside: the fraction of aligned actuation events that agree in type, target and parameters (Note S7).
- Prop. 1: certified false positives are excluded on pinned stacks and bounded by α on hosted ones. "The engine's failure mode is abstention (a missed cause), not a false accusation."

**NESS correspondence** (Remark 1; Lemma S3, Prop. S1, Note S2):
- On monotone slice models every minimal cause–witness pair has W\* = ∅, so ρ = 1/|X\*|.
- The minimal causes are exactly the **minimal transversals of the satisfied prime implicants** of Y.
- A variable is in some minimal cause iff it is a NESS cause (Wright 1985), i.e. it belongs to some minimal sufficient set of actual conditions.
- The gate convention is what makes the models monotone: preemption is "resolved at the evidence layer" (Note S1).

**Dependence vs production.** The authors tie the gate/grade split to Hall's "two concepts of causation" (dependence vs production; Note S10).

**Verdict.** Per principal: (duty, breach under a specification standard and a reasonable-agent standard, [ρ_lower, ρ_upper] with receipts, conduit/exoneration flags).
- **Content-determined duties** (Definition 3): predicates over the principal's own certified messages and certified input frontier only. No ground-truth label, no third-party testimony.
- **Missing evidence** turns ρ into an interval over admissible completions (S2). Remark S1 is a worked redundancy example: after deleting a₂, a₁ is reported as [½, 1].

### 1.4 Evaluation

**Live LLM pipeline.**
- GSM8K, with roles: planner, 3 solvers, aggregator with a declared normative duty, verifier.
- Models: Qwen2.5-72B (primary), Qwen2.5-7B, Llama-3.1-8B. vLLM, temperature 0, 3 seeds.
- Corpora: 3 × 480 cases with disclosed, calibrated fault injection.

| Method | Responsibility error (ℓ1 vs duty-aware Chockler–Halpern ground truth) |
|---|---|
| LLM judge (Who&When all-at-once) | 0.589 |
| CAR/CausalFlow single-site | 0.408 |
| Shapley | 0.223 |
| AUDITA causal-only | 0.408 |
| AUDITA full (gold-informed) | 0.170 |
| AUDITA deployable (no answer key) | 0.159 |

Other findings on the live pipeline:
- 95–98% of adverse incidents are *joint* solver–aggregator incidents; none is a single-culprit structure.
- On Who&When, 58.7% of traces have a duty-bearing role that stayed silent.

**CulpaBench** (300 draws per structure; Table 2):

| Structure | AUDITA full | Single-site | Shapley | LLM judge |
|---|---|---|---|---|
| Redundancy | 0.000 | **1.000** | 0.833 | 0.500 |
| Inert twin | 0.000 | 0.667 | 0.667 | 0.017 |
| Preemption | 0.000 | 0.000 | 0.095 | 0.000 |
| Omission | 0.000 | 0.500 | 0.667 | 0.500 |
| Chain | 0.000 | 0.000 | 0.000 | 0.500 |

On redundancy, single-site scoring fails completely:

> "Single-site scoring cannot represent overdetermination (deleting either sufficient cause alone leaves the outcome standing)." (Results, CulpaBench)

**Inert twin.** This structure is *transcript-identical* to redundancy. It differs only in whether the second command's effect reached the world, so "every transcript-level method returns one verdict for both" (Results).

**Further results.**
- Sampled register: 1,002 incidents, error 0.000.
- No-cause control: AUDITA names nobody in 300/300 draws; judges name someone in 100% of runs.
- Held-out unexpected-startup structure: 74 incidents, exact.
- Forgery: verdict unchanged. Deletion: the interval widens and always contains the truth, with error ≤ 0.122.
- Conduct attacks by insiders: they raise a compliant victim's involvement to 1.0 in 600/600 incidents, but culpability stays 0 in 600/600.
- Compute: roughly doubles per added candidate; the limit is k ≈ 8 at a 1 s budget.
- Off-bus coordination: 0.157 of responsibility becomes invisible, with over-attribution 0.000.
- Varying only the duty standard flips culpability in 69.8% of cases.
- Who&When (static logs, degraded variant): agent accuracy 0.408 vs the judge band 0.41–0.51. AUDITA's advantage requires counterfactual access.

### 1.5 What it covers that WorkTrace must NOT claim

- **Formal handling of overdetermination, preemption and omission in LLM multi-agent attribution.** Modified HP plus Chockler–Halpern grades, ρ = 1/w for w-way redundancy, NESS equivalence on monotone models. We cannot claim to be first to bring actual-causation semantics or redundancy-aware attribution to agent systems.
- **The empirical demonstration that single-site deletion fails under redundancy** (error 1.000). Our "remove X is not enough" argument is already made there, for messages.
- **Production vs dependence (gate vs grade)** and the "inert twin" idea: a recorded cause that is transcript-identical to a real one but had no effect.
- **Conduct-vs-outcome (negligence) semantics.** Judge conduct against content-determined duties, not outcomes, including a proof that no record-confined, content-determined breach standard can be both sound and complete under honest fallibility (Thm 4 / S3).
- **A hosted-stack statistical replay certificate** (Hoeffding margin plus action-match score) and the pinned-stack serial replay protocol.
- **Duty-indexed absence variables** for omissions, including omitted halts by supervisors.

### 1.6 What it leaves open that WorkTrace addresses

- **No prospective allocation of autonomy.** AUDITA "audits the event, not the model". It is post-incident, triggered by an adverse predicate Y, and its output is "an input to human and legal judgment". Nothing grants, narrows or revokes decision rights, and there is no notion of decision classes.
- **Interventions are on presence/absence of inter-agent messages.** None are on external evidence given to an agent. Value changes such as our "invert X", or adding an independent corroborating source, are outside its monotone model class.
- **Citations are trusted as authored causal claims.** AUDITA never tests whether an agent's stated grounds actually drive its action. Attack I (Note S3) shows that an attacker's own citation creates the production path. WorkTrace's grounds-graph tests target exactly this assumption: whether declared grounds are behaviourally real.
- **Only adverse outcomes are analysed.** Correct-by-luck decisions are never examined, and there is no risk–coverage evaluation.

### 1.7 Draft differentiation sentence

> AUDITA attributes graded responsibility for a concrete adverse outcome among multiple principals post hoc, using modified Halpern–Pearl causation over signed inter-agent messages whose citations it trusts as causal admissions. WorkTrace instead tests, before granting autonomy, whether a single agent's decisions actually depend on the external evidence it declares as grounds. It borrows AUDITA's redundancy semantics (jointly necessary sets, ρ = 1/w) to design its evidence interventions, and turns the result into a per-decision-class proceed/escalate/refuse rule.

### 1.8 Citation cautions

- **Preprint, two authors, very recent** (v2, 29 Aug 2026).
- **Ground truth is partly defined by the method's own semantics.** The live-corpus target is "duty-aware graded ground truth", so a duty-aware method beating duty-blind baselines is partly by construction. The authors' own phrasing admits the "deployable beats gold-informed" result depends on adopting negligence semantics (Remark S8).
- **CulpaBench exactness (0.000 everywhere) is on planted monotone structures.** An analytic oracle computes the ground truth. The authors say it is code-independent, but it implements the same definitions.
- **Quantitative evidence is simulated.** The Discussion says so: "the quantitative evidence is simulated". There are no physical robots or production stacks.
- **The redundancy family has no empirical provenance.** It "is absent from the accident corpus: every multi-failure incident in it is conjunctive" (S5.1). It is included for doctrinal reasons. Useful to cite honestly: real incident data rarely shows true overdetermination, but designed evidence redundancy is under our control.
- **Some theorems are true by construction.** Remark S6 itself says Thm 1 "is sound by careful construction". Cite the guarantees as design properties, not deep results.
- **Tension with Mahale on replay.** AUDITA says batch-invariant serving is not enough for bitwise exactness and requires serial replay; Mahale (citing He & Thinking Machines Lab 2025) says batch-invariant kernels are the remedy. If we claim exact replay, we should state our protocol and avoid relying on either claim.
- **Cite as:** Du, Z. & Chen, Y. (2026). AUDITA: certified auditing and causal attribution of adverse outcomes in autonomous multi-agent systems. arXiv:2608.22160v2.

---

## 2. Mahale: Causal Attribution for Agentic Decisions, arXiv:2609.06445

### 2.1 Bibliographic data [verified: arXiv API]

- **Title.** *Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification.*
- **Author.** Ajay Pravin Mahale (sole author), Hochschule Trier.
- **Year.** 2026. v1 6 Sep 2026; the only version. Note: the PDF header says "Draft of September 9, 2026", a date after the arXiv submission. Minor inconsistency.
- **Category.** cs.AI. 23 pp.
- **arXiv comment:** "Pre-registered discrepancy experiment published in full and not run; no empirical result is claimed."
- **Companion paper:** arXiv:2608.13754, *Explanation Multiplicity: Circuit-Level Interpretability Evidence Does Not Survive Defensible Analytic Variation*, Mahale, 13 Aug 2026 [verified].
- **Code:** github.com/designer-coderajay/Causal-Attribution-for-Agentic-Decisions. Not inspected.
- **Venue:** none; preprint.

### 2.2 Problem & contribution

**Question.** What must a provider record so that post-hoc causal attribution over an agent trajectory is possible at all? The paper frames this against the EU AI Act calendar:
- Art. 86 (right to explanation) has applied since 2 Aug 2026;
- Art. 11/12 and Annex IV were deferred to 2 Dec 2027 by Regulation (EU) 2026/1744.

These legal facts are as reported by Mahale; I did not verify Regulation 2026/1744.

**Contributions.**
1. A separation result between two total effects (marginal vs common random numbers, CRN).
2. A natural direct effect (NDE) under a pinned downstream, with pin plausibility reported per arm.
3. A closed form for shared-randomness (quantile) coupling, compared with maximal coupling.
4. Inconsistent mediation: the proportion mediated is not a share.
5. A pre-registered discrepancy experiment (H1–H4), **not run**.
6. A traceability specification R1–R12 with conformance levels L0–L3.

**Closest prior work.** Shah's Causal Agent Replay (CAR; arXiv:2606.08275, abstract only read). Mahale adopts its five intervention operators "verbatim":
- resample a step's action;
- force an action;
- force an observation;
- alter the context;
- alter the policy.

### 2.3 Method

**Setting.** A trajectory τ = (v₁…v_T) ends in a decision Y. Step k draws action a_k from the policy given the prefix, using exogenous noise u_k. "Every effect below is a contrast against that run" (§2). The primary operator is resampling. Removal is deliberately **not** used:

> "taking a step out puts the system off-distribution in the same unprincipled way that mean ablation does for circuits" (§2)

**The three estimands.**
- **Definition 1, marginal total effect.**
  - TE_marg(k) = E_{a′k, u>k}[Y | do(a_k := a′_k)] − y_fact.
  - Every downstream step re-decides under *fresh* noise.
- **Definition 2, CRN total effect.**
  - TE_crn(k) = E_{a′k}[Y | do(a_k := a′_k), U>k = u^fact_>k] − y_fact.
  - Downstream steps re-decide under the *factual* noise. "a counterfactual in Pearl's sense: same unit, same exogenous noise, one variable changed."
- **Definition 3, natural direct effect with pinned downstream.**
  - DE(k) = E_{a′k}[Y | do(a_k := a′_k), a>k := a^fact_>k] − y_fact.
  - Mediated effect ME = TE_crn − DE, an identity (§4).
  - Priority for the estimand: Pearl 2001; Robins & Greenland 1992.

**Planted chain (Eq. 1).**
- a₀ is inert.
- a₁ is the decisive retrieval.
- a₂ is inert.
- a₃ is the executing tool call: it equals a₁ with probability q, otherwise 1 − a₁.
- y = w·a₁ + (1 − w)·a₃.

**Prop. 1 (marginal indistinguishability is an identity).** On every run, TE_marg(0) = TE_marg(1) = ½ − y_fact. An inert step and the decisive step carry the same marginal effect:

> "no threshold on magnitude can separate them." (§3.1)

**Prop. 2 (an exact zero does not certify inertness).** With w = ½, on the event u₃^fact ≥ q (probability 1 − q), TE_crn(1) = 0 exactly while DE(1) = 0.25. The cause is exact cancellation between a direct path and a mediated path that the factual noise inverted. Validation:
- 18 of 300 seeds (vs a nominal 10%), all with |TE_crn| < 10⁻¹²;
- in a sweep over w, the exact-zero rate is 0.133 at w = ½ and 0 elsewhere.

> "A causally inert step returns exactly zero under CRN on every run. A step that returns exactly zero under CRN is not thereby inert" (§3.1)

**Against Shah's point-of-commitment rule (§3.2).** On the chain, Shah's rule names the executing step 60/60 times; largest |TE_crn| names the retrieval 52/60 times. They disagree on 52/60. "The two rules answer different questions": where the outcome became inevitable vs which step's own action carried the difference.

**Resampling a collapsed policy (§3.2).** If a policy has collapsed to a point mass, resampling always returns the factual action:

> "A zero effect at a zero change rate is not a measurement of no influence, it is the absence of a measurement."

**Pin plausibility (§4.1).** The pooled pin-agreement rate is ½ for every q, so it is uninformative. Report it per arm: at q = 0.9, 0.899 on the unchanged arm vs 0.097 on the changed arm. Where the changed-arm figure is small, ME should be read as bounded rather than as a point estimate.

**Coupling (§5).**
- Shared-u inverse-transform ("quantile") coupling attains A_quant = Σᵢ max(0, min(Pᵢ, Qᵢ) − max(Pᵢ₋₁, Qᵢ₋₁)) ≤ 1 − TV.
- Maximal coupling attains 1 − TV, but it needs **both** branches' distributions at draw time: one extra forward pass per step.
- At TV = 0.18:
  - V = 32: maximal 0.82, quantile 0.41;
  - V = 10⁵: quantile 0.0044, while maximal stays 0.820.
- Requirements:
  - use maximal coupling;
  - "Keep the uniform draw a pure function of its key" (run id, step, replicate), never of call order or context;
  - any vocabulary order must be shared and independent of the branch.

**Replay (§5.2).**
- "Temperature zero with a fixed seed is not sufficient." The cited reason is batch non-invariance (He & Thinking Machines Lab 2025: 1000 greedy completions gave 80 unique outputs).
- A replay is valid only within one pinned inference stack.
- "no effect smaller than the measured null-replay floor may be reported as an effect."

**Inconsistent mediation (§6, Prop. 3).** If sign(DE) ≠ sign(TE_crn), then |ME|/|TE_crn| = 1 + |DE|/|TE_crn| > 1, so a suppressor outranks a pure mediator. The paper credits MacKinnon et al. for this. The operational example is directly relevant to us:

> "it is a retrieval that directly supports approval while causing a later verification step to raise a flag." (§6.2)

The prescribed fix is exclusion with a reported exclusion rate: compute a share only when signs agree and |DE| ≤ |TE_crn|.

**Pre-registration (§7, not run).**
- Hypotheses:
  - H1: low Kendall τ_b between observability attributors (span duration, token count, terminal-action indicator) and causal rank;
  - H2 (primary): recency and verbosity dependence in a Plackett–Luce model, decision-clustered;
  - H3: a non-trivial fraction of decisions contain a causally dominant step that the trace ranks negligible;
  - H4: the discrepancy concentrates in high-mediated, low-direct steps.
- Corpus size and exclusion are fixed as *rules* keyed to a null-replay measurement that has not been taken.

**Traceability specification (App. A).**

| Level | Name | Requirements |
|---|---|---|
| L1 | trajectory reconstructable | R1–R4 |
| L2 | counterfactually replayable | R5–R9 |
| L3 | attributable and contestable | R10–R12 |

Requirements:
- R1 trajectory identity and order.
- R2 step typing.
- R3 content commitment (hash).
- R4 outcome function: recorded, versioned, **with no model call**.
- R5 exogenous randomness as a keyed function.
- R6 sampling distribution at draw time.
- R7 serving-stack fingerprint.
- R8 declared purity class per tool.
- R9 environment binding (external state read, with time of reading).
- R10 retention parity.
- R11 cross-actor completeness.
- R12 signed effects and mandatory exclusion rates.

### 2.4 Evaluation

**No empirical result on any LLM.**
- Validation is of estimators against hand-derived closed forms on planted Bernoulli chains.
- The coupling results are on synthetic categorical distributions (V = 32 up to 10⁵).
- The author says so repeatedly: "It has not been run against a language model" (§5.2 Remark), and "we report no rank correlation in this paper as a finding".

### 2.5 What it covers that WorkTrace must NOT claim

- **The marginal / CRN / natural-direct-effect distinction** for agent trajectories, and the result that marginal per-step effects cannot separate inert from decisive steps.
- **"A zero effect is not evidence of no influence"**, via cancellation (Prop. 2) and via policy collapse at zero change rate.
- **Coupling requirements:** keyed randomness, maximal coupling, the null-replay floor, and the insufficiency of seed plus temperature 0.
- **Not computing proportion-mediated under sign disagreement** (credited to MacKinnon et al.).
- **A record specification for counterfactual replayability** (R1–R12).

### 2.6 What it leaves open that WorkTrace addresses

- **No treatment of redundancy.** Overdetermination, preemption, Halpern–Pearl and NESS do not occur in the text; I checked with a full-text search. Interactions between steps are cut explicitly: "Single-step interventions miss interactions … The Shapley value over agent steps is the principled treatment and it is prior art … so we cut it" (§9). So Mahale gives no redundancy criteria for us to reuse. Its zero-effect warnings are the closest it comes.
- **Interventions target the agent's own steps** (resample its action). The agent's *external evidence* is never varied in a designed way. "Forcing an observation" is adopted as an operator but never analysed.
- **No delegation or autonomy decision.** The consumer is a regulator or explanation-seeker. Mahale's related work separates ex-ante gatekeeping (CIVeX, AttriGuard, CausalArmor, explanation-bound tool execution) from post-hoc attribution; WorkTrace is a third object (see §5(d)).
- **No data.**

### 2.7 Draft differentiation sentence

> Mahale specifies which per-step causal estimands (marginal, CRN, natural direct effect) an agent trajectory record must support and shows where each fails. WorkTrace adopts those estimand distinctions and replay requirements to design paired interventions on the *external evidence* available at decision time, and uses the measured evidence-response, not an attribution ranking, as the basis for granting or revoking autonomy per decision class.

### 2.8 Citation cautions

- **No empirical evidence.** The paper is a single-author preprint whose experiment is pre-registered but unrun. Cite it for definitions and requirements, not findings.
- **Coupling magnitudes are not general.** The author himself says they depend on V, entropy and the perturbation model; "only maximal coupling's 1 − TV is invariant". Quote that invariance, not the numbers.
- **The paper corrects itself openly** (a withdrawn number, an amended pre-registration, a corrected table cell). That is good practice, but quote only the final statements.
- **Legal-calendar claims are unverified by me.** These are Reg. 2026/1744, the Art. 86 dates and M/613. Verify independently before reuse.
- **Cite as:** Mahale, A. P. (2026). Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification. arXiv:2609.06445v1.

---

## 3. Counterfactual Trace Auditing (CTA): Zhou et al., arXiv:2605.11946

### 3.1 Bibliographic data [verified: arXiv API]

- **Title.** *Counterfactual Trace Auditing of LLM Agent Skills.*
- **Authors and affiliations.**
  - Xiaolin Zhou, Arizona State University;
  - Jinbo Liu, Arizona State University;
  - Li Li, University of Southern California;
  - Ryan A. Rossi, Adobe Research;
  - Xiyang Hu, Arizona State University.
- **Year and versions.** 2026. v1 12 May 2026; v2 28 May 2026. I read v2.
- **Category.** cs.AI. 18 pp.
- **Code:** github.com/WillChow66/CTA.git. Not inspected.
- **Venue:** none. The footer says "Preprint." and the abstract says "anonymized for review", which suggests it was under submission.
- **Dataset used:** SWE-Skills-Bench, arXiv:2603.15401, Han et al. 2026 [verified].

### 3.2 Problem & contribution

**Problem.** Skill evaluation reports only the change in pass rate (ΔP) between with-skill and without-skill runs, which treats the skill as a black box.

**Contribution.** CTA pairs a with-skill trace and a without-skill trace (same task, same model) and:
- segments each into phases;
- aligns them;
- emits divergence records and Skill Influence Pattern (SIP) labels.

**Headline result.** On 49 SWE-Skills-Bench tasks with Claude Sonnet 4.5:
- mean ΔP = +0.3 pp;
- yet 696 divergences and 522 SIP instances.

### 3.3 Method

**Input bundle.** B_τ = (q_τ, T⁺, T⁻, S_τ, r⁺, r⁻): task, with-skill trace, without-skill trace, skill document, and the two pass rates.

**M1, parsing.** Each trace becomes typed events: READ / WRITE / EXECUTE / SEARCH / THINK.

**M2, phase segmentation.** A deterministic finite-state machine assigns five phases: ORIENTATION, IMPLEMENTATION, VALIDATION, DEBUGGING, FINALIZATION. If no phase is found, the whole trace becomes one IMPLEMENTATION phase; 16 tasks hit this fallback.

**M3, alignment.** Two levels:
- dynamic time warping over phases, with cost = 1 when phase types differ;
- intent windows aligned by TF-IDF cosine over the agent's reasoning text, threshold δ = 0.5.

A divergence record has one of four types:
- target_mismatch;
- content_mismatch;
- outcome_mismatch;
- unilateral_action, from a one-sided recovery pass that catches with-skill writes to targets the baseline never touched.

**M4, SIP detection.** Deterministic rule detectors with threshold θ = 0.5 assign five classes:
- Procedural Scaffolding (constructive);
- Edge-case Prompting (constructive);
- Redundant Exploration (neutral);
- Surface Anchoring (destructive);
- Concept Bleed (destructive).

**What "counterfactual" means here.** The authors are explicit:

> "We use the term counterfactual in an operational sense. … It is not a causal estimand in the Pearl or Rubin sense." (§3)

### 3.4 Evaluation

**Design.** r = 1 run per (task, condition). The authors chose to cover 49 tasks once rather than 17 tasks with 3 runs each (§4).

**Results.**
- **ΔP.** Mean +0.34 pp, median 0, SD 4.4 pp. 45 of 49 tasks have ΔP = 0. One task is hurt: −20 pp on prompt-engineering-patterns.
- **Ceiling tasks** (baseline ≥ 0.9, n = 37): 80% of SIPs, ΔP −0.5 pp.
- **Mid tasks** (n = 10): ΔP +3.6 pp at 2.77× tokens.
- **Phases.** 84% of divergences fall in ORIENTATION or IMPLEMENTATION.
- **Token overhead.** Mean 1.91×, median 1.09×.
- **Case studies.** Include "premature closure": the only negative-ΔP case fired no SIP.

**Baselines.** No baseline method; ΔP is the foil.

**Limitations the authors state.**
- single repetition;
- single model and benchmark;
- no human gold set for detectors;
- phase segmenter not validated.

### 3.5 Does CTA's paired-trace design give WorkTrace a baseline or method?

**Adopt (with credit):**
1. **The argument structure.** An outcome metric saturates (37/49 ceiling tasks) and offsetting effects cancel, while behaviour changes substantially underneath. This is direct empirical support for our critique of outcome-only delegation rules. Cite it alongside AUDITA's Thm 4.
2. **The unilateral-action recovery pass.** In our interventions, the informative behaviour is often an action present in only one arm, for example:
   - the agent fetches a second source only when X is inverted;
   - the agent escalates only under "only X".

   Symmetric alignment misses these; CTA's one-sided pass catches them (112/696 divergences in CTA).
3. **The divergence typology** (target / content / outcome / unilateral) as a *secondary, descriptive* layer explaining *how* an evidence intervention changed the trajectory, not *whether* it did.

**Do NOT adopt as-is:**
1. **No noise control.** r = 1 and no null pair (same condition vs same condition), so the 14.2 divergences/task cannot be separated from sampling noise. A with-skill vs with-skill pair with different seeds might well show a comparable count. Our design must include null pairs, which is exactly Mahale's null-replay floor.
2. **No decision estimand.** CTA measures trajectory differences, not a change in a decision variable. The SIP detectors are unvalidated rules, and TF-IDF over reasoning text aligns what the agent *says*, which is the faithfulness problem we are testing, not a tool for it.

**As a baseline.** CTA is not a competing delegation rule. A "trace-divergence count, not null-calibrated" signal could serve as a naive behavioural baseline or ablation against our intervention-response signal. This is optional.

### 3.6 What it covers that WorkTrace must NOT claim

- Paired with/without-condition trace comparison on the same task and model for LLM agents, including phase-level alignment and unilateral-action recovery.
- The observation that pass-rate deltas hide large behavioural changes.

### 3.7 What it leaves open that WorkTrace addresses

- The condition is a skill document, not decision-relevant evidence.
- No replicates, no null calibration, no causal estimand, no use of the audit for any decision about the agent.

### 3.8 Draft differentiation sentence

> CTA contrasts a single with-skill and a single without-skill trajectory per task to describe how a skill reshapes behaviour, and explicitly disclaims a causal estimand. WorkTrace runs replicated, null-calibrated paired interventions on the external evidence available at a decision, defines the effect on a deterministically parsed decision, and uses it to grant or revoke autonomy per decision class.

### 3.9 Citation cautions

- **Single run per condition and single model.** The model (Claude Sonnet 4.5) is evaluated on skills in the vendor's skill format. There is no human-validated detector.
- **Minor internal inconsistencies.**
  - §4.5 says Table 3 lists "the six tasks with the largest |ΔP|", but only four tasks have nonzero ΔP. The other two rows (ΔP = 0) are arbitrary.
  - Token ratios 0.01–0.11× in Table 3 are implausibly low for with-skill runs; possibly parse artefacts.
  - add-uint-support has baseline 0.50 but appears to be counted as "floor (< 0.5)".
- **Treat SIP counts as descriptive only.**
- **Cite as:** Zhou, X., Liu, J., Li, L., Rossi, R. A., & Hu, X. (2026). Counterfactual Trace Auditing of LLM Agent Skills. arXiv:2605.11946v2.

---

## 4. Evidence-Ledger Adjudication: Chen, Yu & Wang, arXiv:2607.26512

### 4.1 Bibliographic data [verified: arXiv API]

- **Title.** *Evidence-Ledger Adjudication for Claim-Evidence Traceability.*
- **Authors and affiliations.**
  - Gengyu Chen, Carnegie Mellon University;
  - Yongjie Yu, Carnegie Mellon University;
  - Weiling Wang, Syracuse University.
- **Year and versions.** 2026. v1 29 Jul 2026, the only version. The PDF is dated 26 June 2026.
- **Categories.** cs.AI, cs.CL. 10 pp.
- **Venue:** none. No code or data link in the paper.

### 4.2 Problem & contribution

**Workflow.** Each claim in AI-assisted writing gets:
- an evidence packet;
- one relation: supports / contradicts / missing evidence / mixed evidence;
- an author-review route flag;
- a confidence;
- a short rationale.

**Route rule.** Route the claim back to the author iff the relation is not "supports" (§3.2).

**Benchmark.** A blind benchmark of 2,335 rows from AVeriTeC (500), CLIMATE-FEVER (1,535) and SciFact (300). Gold labels are hidden at prediction time and joined only for scoring.

### 4.3 Method

The agent condition reads each packet and emits relation, route, confidence and rationale, in 47 batches. Prompt hashes and prediction hashes are validated.

**The paper never names the model or agent used.** I found no model name in the full text.

**Baselines:**
- always-supported;
- lexical overlap with contradiction cues;
- TF-IDF logistic regression, tuned on 3,877 external rows.

### 4.4 Evaluation

| Condition | Relation accuracy | Macro-F1 | Review-needed recall | Supported claims routed |
|---|---|---|---|---|
| Agent evidence ledger | 0.676 (1579/2335) | 0.601 | 0.885 (1270/1435) | 0.328 (295/900) |
| Best non-agent baseline | 0.383 | 0.303 | — | — |

By source:

| Source | Accuracy |
|---|---|
| AVeriTeC | 0.844 |
| CLIMATE-FEVER | 0.587 |
| SciFact | 0.853 |

The mixed-evidence relation is weak: F1 0.289, recall 0.229. I checked the arithmetic of the confusion matrix and it is internally consistent.

### 4.5 What it covers that WorkTrace must NOT claim

- A four-way support relation including "missing" and "mixed" evidence.
- A deterministic routing rule from relation to human review, evaluated on externally labelled data with blind joining.
- Reporting of both miss rate and false-routing burden.

### 4.6 What it leaves open that WorkTrace addresses

- **It classifies whether evidence supports a *claim*.** It does not test whether an agent's *actions* respond to evidence: there are no interventions and no decisions with consequences.
- **The route is per claim at a single operating point.** It has no per-agent or per-class autonomy, no revocation and no escalation-cost model. 32.8% of supported claims are routed anyway, which is exactly the kind of escalation cost our risk–coverage evaluation prices.
- **Its relation labels are useful for us** as labels for edges of our grounds graph, with "mixed" mapping to our conflict / second-source cases.

### 4.7 Draft differentiation sentence

> Evidence-ledger adjudication has an agent label whether an evidence packet supports, contradicts, fails to establish or mixes evidence for a written claim, and routes non-supported claims to the author at a single operating point. WorkTrace instead intervenes on the evidence behind an agent's operational decisions to test whether those decisions track it, and calibrates a per-class proceed/escalate/refuse rule along a full risk–coverage curve with an explicit escalation cost.

### 4.8 Citation cautions

- **The model behind the "agent evidence-ledger" condition is undisclosed**, and there is no code. That is a serious reproducibility gap.
- **Weak baselines.** There is no LLM-without-ledger baseline, so the ledger's contribution over a plain LLM classifier is not isolated.
- **Possible contamination.** The benchmarks are public, which the authors acknowledge (§4.2).
- **Review recall is not a separate capability.** The route is a deterministic function of the predicted relation, so review recall is just recall of non-"supports" predictions.
- **Cite only as an adjacent example** of evidence-relation-based routing. It is not a causal-attribution paper.
- **Cite as:** Chen, G., Yu, Y., & Wang, W. (2026). Evidence-Ledger Adjudication for Claim-Evidence Traceability. arXiv:2607.26512v1.

---

## 5. Answers to the key questions

### (a) Overdetermination, preemption and redundancy: definitions and formal criteria to reuse or cite

**AUDITA is the work to cite.** Mahale does not treat these topics; the closest it comes is the "zero ≠ inert" results.

**Definitions** (AUDITA, Introduction):
- **Overdetermined:** "two commands, either sufficient".
- **Preempted:** "the blamed command's effect never arrived".
- **Omission:** "a supervisor who never issued the required halt".

**Formal criteria AUDITA uses:**
1. **Modified Halpern–Pearl actual cause.** Halpern 2015; book: Halpern 2016, *Actual Causality*. X\* is a cause iff there is a witness W\* frozen at actual values such that setting X\* to counterfactual values falsifies Y, with X\* minimal.
2. **Chockler–Halpern degree of responsibility**, 1/(|X\*| + |W\*|) (Chockler & Halpern 2004). On monotone models this is 1/|X\*|, so w-way redundancy gives 1/w each. Grades are not shares and need not sum to one.
3. **NESS.** Wright 1985: a necessary element of a sufficient set of actual conditions. AUDITA proves (Prop. S1) that on monotone models, minimal modified-HP causes are the minimal transversals of the satisfied prime implicants, and that NESS membership equals membership in some minimal cause.
4. **Production vs dependence.** Hall 2004. AUDITA's production gate removes preempted candidates before counterfactual grading.
5. **Graded causation and defaults** for omissions: Halpern & Hitchcock 2015.

**How this maps onto our four interventions.** Let Y = [decision = d], with E the evidence available at decision time.
- **remove X** is the but-for test. Under redundancy it returns "no change" for each source alone. This is *correct* behaviour, and AUDITA shows that scoring it as "X unused" is the single-site error (1.000 on redundancy).
- **remove {X₁, X₂}** (all redundant sources jointly) is the minimal-transversal test. If it flips Y while no single removal does, then {X₁, X₂} is a minimal cause and each gets ρ = ½. That is evidence that the agent treats the sources as alternative sufficient grounds.
- **only X** is a sufficiency test: is {X} a sufficient set, i.e. a prime-implicant member? It needs a companion "no evidence" arm to show ∅ is insufficient. With it, NESS membership of X is established directly.
- **invert X** is a *value* intervention, not presence/absence, so it falls outside AUDITA's monotone class. It still fits general modified HP (setting X to a non-actual value). It tests direction-sensitivity: a "no change" under inversion of a declared decisive ground is a failure, not redundancy.
- **add an independent second source** (agreeing or conflicting) *constructs* overdetermination or conflict on purpose. It also connects to TRACE's argument about effective numbers of sources.
- **Preemption analogue.** Our episode field "information available at decision time" works like AUDITA's production gate. Evidence that arrived after commitment, or was never surfaced to the agent, cannot be a ground. It must be gated out before scoring, and is not an unfaithfulness signal.
- **Omission analogue.** AUDITA's duty-indexed absence variables correspond to a required-but-missing escalation or verification by our agent. "Did not escalate when the only ground was removed" can be encoded as an absence variable.

**What must be cited, or our claim narrowed.** AUDITA (with HANSARD, abstract only: "attribution laundering … spreading an act across redundant agents until none is a but-for cause") already brings redundancy-aware actual causation into agent attribution. Our novelty claim must therefore be:

> designed interventions on *external evidence* to a *single agent's decision*, made robust to redundancy, and used *prospectively* for autonomy allocation.

We cannot claim "first to handle overdetermination in agent causal analysis". The first-round map (positioning.md §3.3) said nobody deals with redundancy; that is **no longer true** at the level of post-hoc multi-agent attribution.

**Caveats for reuse:**
- Halpern–Pearl and NESS are defined for deterministic SCMs in a fixed context. LLM agents are stochastic, so we need probability-raising or probabilistic versions. A candidate formal basis is Mu & Najib 2026, arXiv:2605.13077 (IJCAI 2026, probabilistic multi-agent responsibility; [verified metadata, not read]).
- The NESS equivalence needs monotonicity. Inversion and conflicting-source arms are non-monotone, so we should state which arms the equivalence covers.
- Exact enumeration is exponential (AUDITA: compute doubles per candidate). Keep designed source sets small (m ≤ 3, i.e. ≤ 8 subsets plus the inversion arms).

### (b) Mahale's estimand distinction: concrete design implications for paired evidence interventions

Our intervention acts on an *observation or context* (Shah/Mahale operators "force an observation" / "alter the context"), not on the agent's own action. Everything downstream (reasoning tokens, further tool calls, the final decision) re-decides. Mahale's warnings translate as follows.

1. **Do not anchor contrasts on the single factual decision.** Mahale's TE_marg subtracts y_fact, and Prop. 1 shows that per-run contrasts against y_fact can make inert and decisive components identical (½ − y_fact). For us, compare two *sampled* arms:

   Δ_e(I) = P̂(D = d | E_e) − P̂(D = d | I(E_e)), or the total-variation distance over {proceed, escalate, refuse}.

   Each arm gets k replicates; the factual run is just one draw of the first arm.

2. **The marginal estimand is the one that answers our question.** Delegation is a policy-level property (does the agent's decision distribution track evidence?), so the marginal interventional contrast is appropriate. Mahale's objection to it concerns ranking *steps within a trajectory*, which we do not do.

   CRN is a *variance-reduction and per-unit* device. On evidence interventions it buys little: changing the evidence changes the prompt, so token distributions diverge from the first token, and shared-u quantile coupling collapses at realistic vocabularies (0.0044 at V = 10⁵, TV = 0.18). Maximal coupling needs both branches' logits at every step.

   - **Decision:** primary estimand = marginal, paired at the episode level (both arms on the same episode, independent noise).
   - Use CRN or maximal coupling only on self-hosted, open-weight, pinned stacks, and report coupling agreement.
   - For hosted APIs, state explicitly that CRN is unavailable. Mahale and AUDITA agree that seed plus temperature 0 is not replay.

3. **Keyed randomness wherever we control sampling** (R5). Seeds are a pure function of (episode id, arm-independent step index, replicate), never of call order. Otherwise "TE_crn silently becomes TE_marg".

4. **Null arm and replay floor (mandatory).**
   - Add a *null* arm: the unchanged evidence re-run with k fresh replicates. This measures the decision flip rate with no intervention.
   - Add a *placebo* arm: change irrelevant evidence, or paraphrase or reorder.
   - Effects below the null floor are not reportable.
   - Episodes whose null-replay agreement is below a pre-registered floor are excluded, with the exclusion rate reported (Mahale §5.2, §7.3).

   This is precisely the control CTA lacks.

5. **Deterministic outcome function** (R4). Parse the agent's action into proceed / escalate / refuse with a rule, not an LLM judge. Otherwise judge variance contaminates every effect.

6. **Reading the decision distribution directly.** Where the decision can be elicited as a constrained choice at a pinned prefix (open-weight models), record the logprobs over {proceed, escalate, refuse} (R6). This gives the exact P(D | context) at the decision step without sampling noise. TV between arms, and maximal-coupling agreement 1 − TV, then come for free.

7. **Natural-direct-effect arm, to separate "reads evidence" from "re-plans".**
   - Intervene on X, but pin the agent's intermediate actions and observations to the factual run. Only the final decision step re-decides with the new evidence in context.
   - DE answers "does the decision read X directly?".
   - TE − DE = mediated effect, for example: inverting X triggers a verification lookup, which then changes the decision. A mediated escalation via verification is *desirable* behaviour and must not be scored as a failure.
   - Following Mahale:
     - report **pin plausibility per arm**: the logprob or likelihood of the pinned continuation under the intervened context, since a pinned continuation that cites the old evidence may be implausible;
     - **never compute proportion-mediated when signs differ.** The canonical case is exactly ours: "a retrieval that directly supports approval while causing a later verification step to raise a flag."

8. **A zero effect is not "unused"** (Prop. 2 and the zero-change-rate remark). For every "decision unchanged" outcome, record which of the following applies:
   1. redundancy: resolved by the joint-removal and only-X arms;
   2. cancellation of direct and mediated paths: resolved by the DE arm;
   3. policy collapse: the decision is constant whatever the evidence; resolved by the invert-X arm and the null-arm change rate.

   Case (3) is a *failure* of evidence-sensitivity, not inertness of X.

9. **Sample size: certify per class, not per episode.** AUDITA's hosted-stack certificate needs q̂₀ − q̂₁ ≥ δ + 2ε with ε = √(ln(4/α)/(2n)). At α = 0.05:

   | n replicates per arm | 2ε |
   |---|---|
   | 50 | 0.42 |
   | 100 | 0.30 |
   | 200 | 0.21 |

   Per-episode certification is therefore prohibitively expensive. Our delegation rule is a *class-level* statement, so use few replicates per episode-arm (e.g. k = 5–10) across many episodes. Make inferences by episode-cluster bootstrap (as in Mahale's decision-clustered design) or a hierarchical model, and use Hoeffding or exact binomial bounds only for the class-level rate.

10. **Record schema for our episodes.** Mahale's L2 "counterfactually replayable" level gives a checklist. Add a replay block to the decision episode E:
    - keyed seeds (R5);
    - decision-step distribution (R6);
    - serving-stack fingerprint (R7);
    - tool purity class (R8);
    - external state with time of reading (R9), which is our "information available at decision time".

    Because our episodes are *generated*, with sandboxed or mocked tools and pinned evidence, R8 and R9 hold by construction. We should say so.

### (c) Does CTA's paired-trace design give us a baseline or methodology to adopt?

**Partly.**
- **Adopt:**
  - the outcome-saturation argument as supporting evidence against outcome-only rules;
  - the one-sided "unilateral action" pass, for actions present in only one arm;
  - the divergence typology as a descriptive secondary analysis.
- **Do not adopt:**
  - r = 1;
  - uncalibrated divergence counts;
  - TF-IDF alignment over reasoning text.
- **Required improvements:** replicates, null pairs, and a decision-level estimand.
- **As a baseline:** CTA is not a delegation baseline. At most, an uncalibrated "trace divergence" signal could be an ablation against our intervention signal.

### (d) Links to delegation and autonomy decisions

**AUDITA.**
- *Delegation chain* structure: but-for chains grade every relay ρ = 1; faithful relays get a conduit flag; breach localises to the originator.
- A "delegation & duty registry D".
- Authenticated-delegation tokens (South et al. 2025, arXiv:2501.09674, cited by AUDITA [not verified by me]) are consumed as primitives.
- **No autonomy adjustment.** But three results matter for our framing:
  1. Thm 4: judging conduct against content-determined duties cannot be complete with respect to outcome-guilt when honest errors exist. "Innocence is certifiable from the record alone; outcome-guilt-completeness is not." This is a formal reason why an evidence-conduct-based rule and an outcome-based rule will disagree. It supports making the risk–coverage comparison against an outcome-only rule a central experiment, and predicts honest-error cases where our rule grants autonomy yet outcomes fail.
  2. "A verdict must ship with its standard attached": varying only the standard flips culpability in 69.8% of cases. Our delegation rule must publish its evidence-handling standard per class.
  3. Verdict-guided repair averts 2.4× the harm of a random fix.

**Mahale.**
- Nothing on autonomy.
- Its distinction between *ex-ante gatekeeping per action* (CIVeX, AttriGuard, CausalArmor) and *post-hoc attribution* lets us position WorkTrace as a third object: **ex-ante allocation of decision rights per decision class from tested behaviour.** This is neither a per-action gate nor an incident attribution.
- It cites Mishra & Sharad 2026 (arXiv:2606.09692, abstract only): delegation-scoped execution "is not identifiable from standard observables". This is relevant to logging *which delegation* an action ran under, i.e. our permissions field.

**CTA.**
- Nothing on autonomy.
- **Implication for us:** attaching a skill reshapes behaviour even at ΔP ≈ 0. So any configuration change (skills, prompts, tools, model version) should trigger re-testing or suspension of earned autonomy. This gives a concrete *revocation trigger*.

**Evidence-Ledger.**
- A per-claim keep-vs-route rule driven by a support relation: a single-operating-point escalation gate with a measured false-routing burden (32.8%). It is the nearest analogue to our proceed/escalate, but it has no per-agent or per-class rights and no cost model.

### (e) Differentiation sentences

Collected from §§1.7, 2.7, 3.8 and 4.7 above:

- **AUDITA:** AUDITA attributes graded responsibility for a concrete adverse outcome among multiple principals post hoc, using modified Halpern–Pearl causation over signed messages whose citations it trusts as causal admissions. WorkTrace tests *before* granting autonomy whether one agent's decisions actually depend on the external evidence it declares, borrowing AUDITA's redundancy semantics to design interventions and turning the result into a per-class proceed/escalate/refuse rule.
- **Mahale:** Mahale specifies which per-step causal estimands an agent-trajectory record must support and where they fail. WorkTrace adopts those distinctions and replay requirements for paired interventions on decision-time evidence, and uses the measured evidence-response, not an attribution ranking, to allocate autonomy.
- **CTA:** CTA contrasts one with-skill and one without-skill trajectory per task to describe behaviour change and disclaims a causal estimand. WorkTrace runs replicated, null-calibrated evidence interventions with a decision-level estimand and uses them to grant or revoke autonomy.
- **Evidence-Ledger:** Evidence-ledger adjudication labels whether evidence supports a written claim and routes unsupported claims at one operating point. WorkTrace tests whether an agent's operational decisions track their evidence and calibrates a per-class delegation rule along a risk–coverage curve with explicit escalation cost.

---

## 6. Implications for WorkTrace

### 6.1 Novelty status

**Core claim not threatened.** None of the four works grants, narrows or revokes autonomy from tested evidence-handling behaviour.

**Claim (2) must be narrowed** (redundancy-robust interventions):
- AUDITA already does redundancy-aware actual causation, with ρ = 1/w and a NESS equivalence, for LLM multi-agent incident attribution.
- AUDITA shows that single-site deletion fails completely on redundancy.
- HANSARD (arXiv:2608.22512, abstract only) names "attribution laundering" across redundant agents and uses modified HP.

New wording:

> first redundancy-robust intervention design on *external evidence to a single agent's decision*, used *prospectively* to allocate autonomy

### 6.2 New must-read works found while checking (abstract only so far)

- **Liao 2026, *Auditing Provenance Sensitivity in LLM Agent Action Selection*, arXiv:2607.20827 [verified metadata, abstract only].**
  - Holds task, proposition, position and policy fixed while changing only the *source authority* of a piece of evidence.
  - Tests behaviour when valid evidence is weakened, with context-subset interactions as a diagnostic.
  - 450 next-action tasks, several open-weight model families.
  - **This is the closest prior work to our evidence interventions seen so far. Read in full next round.**
- **Shah 2026, *Causal Agent Replay*, arXiv:2606.08275 [verified metadata, abstract only].** The intervention algebra over agent steps (including forcing an observation), point-of-commitment rule and Monte-Carlo Shapley that Mahale builds on. Read in full.
- **HANSARD, Sardianos et al., arXiv:2608.22512 [verified metadata, abstract only].** Redundancy laundering, a synergy residual, and live indicators that "gate oversight without adjudicating". The last is possibly close to escalation gating. Read in full.
- **CausalFlow, Bonagiri et al., arXiv:2605.25338 [verified metadata, abstract only].** Single-site counterfactual responsibility scores. This is the baseline AUDITA beats; useful as a "remove-X-only" foil.

### 6.3 Design changes

1. **Arms per episode.** For a designed source set S (|S| ≤ 3), run:
   - full;
   - null (re-run of full);
   - placebo;
   - remove-X for each X;
   - remove-all-redundant;
   - only-X for each X;
   - none;
   - invert-X for each declared decisive ground;
   - add-independent-second-source, agreeing and conflicting.

   Score evidence-use by modified HP / NESS on the presence/absence arms and by direction-sensitivity on the inversion arms. Never count "remove X → unchanged" as unfaithfulness when a redundant source remains.
2. **Estimand.** A marginal, two-arm sampled contrast on a deterministically parsed decision. No contrasts against the single factual run. Use CRN or maximal coupling only on pinned open-weight stacks, and report coupling agreement.
3. **Null replay floor and exclusion rule**, pre-registered (Mahale §7.3). Report exclusion rates.
4. **Direct-effect arm with a pinned downstream** for multi-step agents, to separate "decision reads X" from "X triggers verification". Report pin plausibility per arm. Exclude sign-disagreeing cases from any proportion statistic and report the exclusion count (R12).
5. **Zero-effect triage.** Classify every unchanged decision as redundancy, cancellation or collapse before scoring.
6. **Episode schema.** Add a replay block (keyed seeds, decision-step distribution, serving fingerprint, tool purity) and a timestamp on evidence availability, which acts as the production gate and handles preemption.
7. **Statistics.**
   - Few replicates per episode-arm, many episodes per class.
   - Class-level estimates with an episode-cluster bootstrap.
   - Exact or Hoeffding bounds only at class level. Per-episode certification at α = 0.05 needs ≈ 100+ replicates per arm.
8. **Revocation trigger.** Any change of skill, prompt, tool or model invalidates earned autonomy until re-tested (CTA: behaviour changes at ΔP ≈ 0).
9. **Declared grounds.** Treat these as *claims under test*, explicitly contrasting AUDITA's "citation is an admission". AUDITA's "inert twin" gives the vocabulary: a declared but behaviourally inert ground is transcript-identical to a real one, and only intervention separates them.
10. **Publish the evidence-handling standard per decision class** with the rule (AUDITA: the standard flips 69.8% of verdicts).

### 6.4 Risks

- **Honest-error disagreement.** By AUDITA's Thm 4 analogue, an evidence-conduct rule will grant autonomy to agents that handle evidence properly yet err on outcomes. The risk–coverage comparison with the outcome-only rule must expect this and report where each rule fails.
- **Cost on hosted models.** CRN is unattainable on hosted APIs, and per-episode power is low. Budget replicates accordingly, and present results as class-level marginal effects.
- **Monotonicity.** The HP/NESS equivalence applies only to presence/absence arms under monotonicity. State the scope.
- **Replay exactness.** AUDITA and Mahale disagree on whether batch-invariant kernels suffice. Do not claim bitwise replay unless it is measured.

### 6.5 Things to cite

**From the four papers:**
- AUDITA (2608.22160): redundancy, preemption and omission semantics; single-site failure; Thm 4.
- Mahale (2609.06445): estimands, the zero-effect caveat, coupling and replay requirements.
- CTA (2605.11946): paired traces; outcome metrics blind to behaviour change.
- Evidence-Ledger (2607.26512): adjacent evidence-relation routing; cite lightly.

**Classics, verified via Crossref:**
- Halpern & Pearl 2005, *Causes and Explanations: A Structural-Model Approach. Part I: Causes*, BJPS 56(4), doi:10.1093/bjps/axi147.
- Chockler & Halpern 2004, *Responsibility and Blame: A Structural-Model Approach*, JAIR 22, doi:10.1613/jair.1391.
- Halpern 2016, *Actual Causality*, MIT Press, doi:10.7551/mitpress/10809.001.0001.
- Wright 1985, *Causation in Tort Law*, California Law Review 73(6), doi:10.2307/3480373.
- Halpern & Hitchcock 2015, *Graded Causation and Defaults*, BJPS 66(2), doi:10.1093/bjps/axt050.
- Robins & Greenland 1992, *Identifiability and Exchangeability for Direct and Indirect Effects*, Epidemiology 3(2), doi:10.1097/00001648-199203000-00013.
- MacKinnon, Krull & Lockwood 2000, *Equivalence of the Mediation, Confounding and Suppression Effect*, Prevention Science 1, doi:10.1023/A:1026595011371.
- MacKinnon, Warsi & Dwyer 1995, *A Simulation Study of Mediated Effect Measures*, Multivariate Behavioral Research 30(1), doi:10.1207/s15327906mbr3001_3.

**Classics, verified on arXiv:**
- Halpern 2015, *A Modification of the Halpern-Pearl Definition of Causality*, arXiv:1505.00162. The IJCAI 2015 venue is as given by AUDITA and was not independently verified.
- Pearl 2001, *Direct and Indirect Effects*, arXiv:1301.2300. The UAI 2001 venue is as given by Mahale; arXiv title verified.

**Not independently verified:**
- Hall 2004, "Two concepts of causation", in *Causation and Counterfactuals* (MIT Press) [unverified; as cited by AUDITA].
- He & Thinking Machines Lab 2025, "Defeating nondeterminism in LLM inference" (blog) [unverified; as cited by Mahale].

**Verified metadata, not read:**
- Mu & Najib 2026, arXiv:2605.13077.
- Zhang et al. 2025 (Who&When), arXiv:2505.00212, ICML 2025.
- SWE-Skills-Bench, arXiv:2603.15401.
- SkillTester, arXiv:2603.28815.
