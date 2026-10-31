# R3 — READY / "Qualifying AI Agents Under Cost-Aware Human Oversight": full reading and threat to W3

Round-3 reading note. Written 2026-10-25. The task was to read the full READY paper (the round-2 notes had only the OpenReview abstract), answer key questions (a)–(h), and decide what remains of W3.

## 0. Bottom line (threats first)

1. **The full text is available.** The anonymous ICLR 2027 submission is the extended version of a public, attributed arXiv preprint: **Chatrath et al., "READY or Not: Reliable Enterprise Agent Deployment", arXiv:2609.02095v1 (2 Sep 2026), Scale AI.** I read the arXiv v1 in full. The ICLR version itself (new title, 18 systems instead of 16, an added τ²-bench retail workflow, changed headline numbers) could not be read beyond its OpenReview metadata, because the PDF is behind a browser challenge.
2. **READY already owns the "held-out qualification of an oversight policy" frame.** That covers:
   - a development/qualification split;
   - a frozen policy that is certified with a one-sided exact Clopper–Pearson bound;
   - the minimum-cost policy subject to a reliability target;
   - an explicit human-review cost, C = k_m + k_h·(review rate);
   - risk–coverage, AURC and AUROC of the routing signal;
   - the thesis "**autonomous accuracy does not determine deployability**".

   WorkTrace must claim none of these.
3. **READY also already contains a "right verdict, wrong basis" loss.** App. B.3 replaces the success predicate with u_df = "verdict correct ∧ no disqualifying process defect". The defect is an LLM-judged MUST-NOT "prohibited shortcut" rubric, taken from CliniCARE-Bench. 21.9% of runs carry a defect. The process-aware predicate moves mean review burden from 53.0% to 69.8%, and makes two systems undeployable. So **putting the wrong basis into the loss is not new.** What is new in WorkTrace is **how the wrong basis is detected**: interventions on external evidence with ground truth by construction, rather than an LLM judge reading the trajectory.
4. **What READY does NOT do, so W3 survives in narrowed form:**
   - **Unit.** It never grants autonomy per decision class. Its unit is one agent–workflow–policy configuration with one global threshold. Its claims are explicitly pointwise, and it does no simultaneous inference across classes.
   - **Signal.** Its routing signal is the agent's self-reported confidence. It runs no evidence tests or interventions.
   - **Shift and revocation.** Distribution shift and post-deployment monitoring/revocation are explicitly "beyond the scope" (§7). Its only form of revocation is lineage-triggered requalification.
   - **Construct.** It defines no agent capability construct, and explicitly denies that deployability is an intrinsic property of an agent.
5. **READY must become a baseline (two variants), and our claims must be re-worded** (§9).

---

## 1. Bibliographic data

| Item | Data | Status |
|---|---|---|
| **arXiv preprint (read in full)** | Veronica Chatrath*, Bryan Zhu*, Jingxuan Fan*, George Pu, Soham Dinesh Tiwari, Soham Dan, Ryan Young, Yuan (Christy) Li, Yuang Yao, Apaar Shanker, Minglai Yang, Daniel Yue Zhang, Yunzhong He, Ying Liu, Chenguang Wang, Zhijun Yin, Yuan (Emily) Xue (*co-first). "READY or Not: Reliable Enterprise Agent Deployment." arXiv:2609.02095v1 [cs.AI], submitted 2 Sep 2026. Affiliations: Scale AI; UC Santa Cruz; Vanderbilt University Medical Center. | **[verified: arXiv API + PDF]**. The arXiv API splits "Yuan (Christy) Li" into two author entries (" Yuan", " Li"); the PDF gives the correct form. Only v1 exists (v2 returns 404 as of 2026-10-25). |
| **OpenReview submission (metadata only)** | Anonymous. "Qualifying AI Agents Under Cost-Aware Human Oversight." ICLR 2027 Conference Submission #26877. Forum 3AR0RdXhpV. Primary area: datasets and benchmarks. Licence CC BY 4.0. Created 2026-09-16; public since 2026-10-03; last modified 2026-10-05. | **[verified: api2.openreview.net `notes/search` record]**. Authors are anonymous on OpenReview. |
| Identity of the two | Same framework name and acronym ("Reliable Enterprise Agent Deployment (READY)"), same CliniCARE-Bench 750 cases, same Sonnet 5 vs GPT-5.4 "0.3 points" example. | **Same work: near-certain inference, not an author statement.** |
| Companion benchmark (partly read) | Chatrath, Zhu, Pu, Fan, Shanker, Ursekar, Sharma, Qin, Han, Tiwari, Dan, Kalmath, Li, Zhang, Wang, Doctor, Yin, Shah, Xue. "CliniCARE-Bench: Clinical Calibrated Audit of Medical Reasoning in EHR." arXiv:2608.07796v1, 7 Aug 2026. | [verified: arXiv API + PDF] |
| Scale web pages | labs.scale.com/papers/reliable-enterprise-agent-deployment (dated 9/4/2026) links a PDF on static.remotasks.com; its text is identical to arXiv v1 (diff checked). labs.scale.com/blog/ready says READY launched with CliniCARE-Bench and PSEBench, and that "financial services" is "coming soon". | Fetched |

### Differences between the ICLR version and arXiv v1 (from the OpenReview abstract and TL;DR only)

- **Workflows:** CliniCARE-Bench with **18** systems and 750 cases, **plus τ²-bench retail** (17 systems, 114 tasks).
- **Guarantee wording:** "tests them on held-out cases with finite-sample error control, and returns the lowest-cost member of the **certified set**". This suggests the ICLR version tests the whole policy class on held-out data (Learn-then-Test-style multiple testing) instead of v1's select-on-dev-then-qualify-one-policy. **This is my inference and is unconfirmed.**
- **Headline numbers changed:** Sonnet 5 vs GPT-5.4 now need "**12.0% versus 29.3%** human review" (v1: 29.6% vs 39.2%). The accuracy-vs-ranking correlation is now "Pearson r = −0.07 and −0.13" across the two workflows (v1: ρ = −0.12).
- **New claim:** "Accounting for agent and review costs can further change which certified configuration is preferred."
- **Keywords:** LLM agents, agent evaluation, deployment, human oversight, calibration, reliability, cost-aware evaluation, enterprise AI, benchmarking.
- **TL;DR (verbatim):** "READY turns agent-evaluation evidence into a deployment qualification: it picks the cheapest human-oversight policy meeting a reliability target and qualifies it on held-out cases, showing autonomous accuracy alone fails to predict deployability."

## 2. Reading coverage (exactly what was read)

- **arXiv v1, read in full:** Abstract; §1–§8 (Intro; Design overview §2.1–2.3; §3.1–3.7 qualification method; §4.1–4.6 runtime and testbed; §5.1–5.7 CliniCARE experiments; §6.1–6.7 related work with Table 4; §7 limitations; §8 conclusion); App. A.1–A.2; App. B.1–B.5 prose.
  - Tables 2, 3, 5 and 6 were read; Tables 7–9 only partly, because pdftotext garbled their columns.
  - References were skimmed.
- **OpenReview ICLR version, metadata only:** title, TL;DR, abstract, keywords, primary area, venue, PDF hash, dates.
  - Retrieved from `https://api2.openreview.net/notes/search?term=...&source=forum`.
  - Every PDF route returned HTTP 403 "ChallengeRequiredError": `openreview.net/pdf?id=3AR0RdXhpV`, `/pdf/f49039d5….pdf` on openreview.net, api and api2, `attachment?id=…&name=pdf`, and the supplementary attachment. So did `api/api2 notes?id=` and `notes?forum=`.
  - I did not try to bypass the browser challenge.
- **Reviews:** none found. The search API returned no Official_Review or Comment notes for Submission26877; ICLR 2027 reviews are probably not yet released. **Not confirmed**, because the forum endpoint was blocked.
- **Code:** no public repository was found (arXiv text, Scale pages, web search). READY is "built on Inspect AI"; the Scale blog says the testbed is open, but gives no link.
- **CliniCARE-Bench:** abstract and §5.5 "Process Adherence" (definition of process defect and defect-free accuracy); judge-reliability passages located but only skimmed.

---

## 3. Problem and contribution

- **Problem:** benchmarks measure autonomous capability, but deployment needs to know whether the *human–AI system* under some oversight policy meets a reliability target at acceptable cost.
- **Contributions:**
  1. A "deployment-centered evaluation objective": reliability and cost of the human–AI system under policy π.
  2. Selecting the minimum-cost policy subject to R(π) ≥ Y, then statistically qualifying the frozen policy on held-out cases, giving a "deployment profile" (reliability, autonomous coverage, review burden, cost, workflow risk).
  3. An open, Inspect-based testbed that separates workflow evaluation from qualification, instantiated on CliniCARE-Bench (16 systems × 750 cases = 12,000 runs).
- **Central hypothesis (§5.6, verbatim):** "The central READY hypothesis is that autonomous benchmark performance alone does not determine deployment value."

## 4. Method: answers to the key questions

### (a) Unit of certification

- **Unit:** one agent system m (model + harness, e.g. "Claude Code / Opus 5") × one workflow w × one oversight policy π. The deployment profile is "conditional on the workflow, evaluated system, oversight policy, and declared deployment assumptions, rather than a context-free model score" (§4.5).
- **Not per action class, and not per decision class.** The empirical policy is one global threshold per system and workflow. It is "deliberately agnostic to what the classes mean: class semantics enter only through the success predicate φ_w, never through the escalation rule" (§5.2). The "classes" here are the four verdict labels, not decision types.
- **Routing is per case at run time:** each completed case is accepted or escalated by its signal.
- **Qualification is aggregate:** "Deployment qualification is an aggregate statistical claim about the human–AI system induced by π, not a property assigned to any individual task instance" (§3.1).
- **Simultaneity is out of scope:** "Unless otherwise stated, READY qualification claims are pointwise for a pre-specified deployment target and frozen policy. Simultaneous statistical claims across multiple targets, policies, or operating points require an appropriate simultaneous-inference procedure" (§3.5). They do not provide one.

### (b) What decides accept vs escalate

- **Framework level:** any "observable routing signal s_i". "READY does not prescribe a signal" (§6.4).
- **Empirical instantiation:** the **self-reported (verbalized) confidence** in the agent's final report, rescaled to [0, 1]. Policy (Eq. 44): accept if s_i ≥ τ, else review.
- **Negative control (App. B.5):** escalate every *predicted* indeterminate verdict regardless of confidence.
  - It turned out *not* more expensive: mean review 48.9% vs 53.0%.
  - The authors keep the signal-only rule on structural grounds, and state that "A deployment free to use both would do better than either."
- **Class-agnostic justification (App. B.4):** the routing signal keeps within-class ranking power (within-class AUROC 0.61–0.67), "the empirical basis for keeping class semantics inside φ_w and out of the escalation policy".
- **Success** is defined separately by the workflow evaluator g_w and predicate φ_w. These "may require a conjunction of outcome correctness with selected process, grounding, or policy requirements" (§2.1). Process requirements must rest on "observable execution evidence, such as retrieved sources, tool calls, or state changes, not unrecorded model reasoning" (§6.2).
- **No evidence tests, no interventions, no counterfactual reruns.**

### (c) Guarantee form

- **Target:** system reliability R(π) = E[u^π], where the terminal reliability is R(τ) = c(τ)·a(τ) + (1 − c(τ))·a_h (Eq. 17–18). Here:
  - c(τ) is autonomous coverage;
  - a(τ) is success among accepted cases;
  - a_h is the success rate of the human-review path.
- **Important:** this is reliability of the *mixture*, not the selective risk P(error | autonomous) that WorkTrace certifies.
- **Procedure (v1):**
  - Random 375/375 split of the 750 cases into development and qualification sets.
  - On the development set, pick the highest-coverage τ with estimated R ≥ Y + δ, where **δ = 0.05 is a selection margin, not a confidence level**. Without the margin only 46% of policies qualify; with it, 95%.
  - Freeze τ.
  - On the qualification set, compute the one-sided **95% exact Clopper–Pearson** lower bound on accepted-case success.
  - Combine: LCB = (n_acc/N)·p̲_acc + ((N − n_acc)/N)·a_h. "No statistical confidence is attributed to the assumed term" (§3.5).
  - Qualify iff LCB ≥ Y.
- **Break-even review assumption:** a_h^min = the weakest review success under which the policy still qualifies (Eq. 35).
- **Optional tail-risk constraint:** CVaR upper confidence bound by bootstrap (App. A.2). Not used in the experiments.
- **Sampling unit:** "repeated runs ... carried together at the task-instance level"; clustering by patient, customer and similar units must be preserved (§3.5).
- **Possible inconsistency (citation caution):**
  - §3.5 says READY bounds the mean of y_i(a_h) "rather than treating the observed routing fraction as fixed".
  - App. B.1 computes the bound with the observed fraction n_acc/N held fixed.
- **ICLR version:** "finite-sample error control" over a "certified set". The method may differ (§1).

### (d) Cost model for human oversight

- C(π) = C_agent + C_human (Eq. 13). Under constant costs, C(τ) = k_m + k_h·e(τ), where e(τ) = 1 − c(τ) is the review rate (Eq. 19). So minimizing cost equals minimizing review burden.
- Case-level costs are allowed (§3.3).
- **The human path's quality a_h is a declared assumption.** The primary value is a_h = 0.9, with sensitivity runs over 0.80–1.00 (App. B.2).
- Consequences:
  - No policy can exceed a_h; reliability tops out at the reviewer's accuracy.
  - At a_h = 0.80, 311 of 496 policies qualify only by routing 100% to review.
- The ICLR abstract adds cost-based comparison across configurations.

### (e) Held-out evaluation and distribution shift

- **Held-out:** yes, a random split of the same cohort, with the verdict mix preserved without stratification.
- **No distribution shift.** §7 (verbatim): "It does not guarantee the same reliability under arbitrary distribution shift, changes in workflow composition, environment changes, or materially different agent behavior."

### (f) "Right outcome on wrong basis", interventions, evidence sensitivity

- **Right outcome on wrong basis: present, through a judged predicate.** The process-aware variant u_i,df = 1{ŷ_i = y_i* ∧ no disqualifying process defect} (Eq. 42; App. B.3).
  - **Where the defect comes from:** CliniCARE-Bench §5.5. MUST-NOT criteria list "prohibited shortcuts and unsupported inferences", for example "inferring an endpoint from an administrative code alone, treating an order time as a performed-procedure time". They are graded by an **LLM judge (GPT-5.5, itself an evaluated system)** against the report plus the logged trajectory, and validated with a five-judge panel.
  - **How common:** a defect appears in 21.9% of runs (12.7–30.0% by system). Using u_df lowers autonomous success by 4.5–13.1 points.
  - **Routing quality is stable:** Spearman 0.87 for AUROC under u vs u_df.
  - **The frontier is not stable:** mean review burden goes from 53.0% to 69.8%, and both Gemini Flash systems become undeployable at Y = 0.76.
  - Verbatim (B.3): "The conclusions of Section 5.3 survive the substitution; the frontier of Section 5.4 does not."
- **Interventions on evidence: none.** There is no remove-X, only-X, invert-X or second-source condition, and no test of whether the verdict depends on the evidence that should determine it.
- READY cites faithfulness work (Lanham 2023; Turpin 2023) only as motivation (§6.2).

### (g) Revocation and sequential monitoring

- **None statistically.** Monitoring is "important for detecting performance degradation and determining when requalification is needed, but designing such monitoring and requalification triggers is beyond the scope of this work" (§7).
- **What exists:** discrete **lineage-based requalification rules** (§4.6):
  - assumptions change → recompute;
  - evaluator changes → re-score saved trajectories if they hold enough information;
  - agent, harness, environment or population changes → re-execute.
- Stated stance: qualification is "not ... a permanent property of an agent but ... an evidence-backed claim attached to a specific lineage and deployment context."

### (h) A capability construct comparable to DSA?

- **No.** The only agent-side quantity is **routing quality**: AUROC and AURC of the self-reported confidence for predicting success. This is a metacognitive-discrimination measure.
- The finding: base accuracy and AUROC are essentially uncorrelated (v1: ρ = −0.12; ICLR: r = −0.07, −0.13). The Scale blog puts it as "Accuracy, and knowing when to escalate, are different skills."
- READY **explicitly rejects** agent-intrinsic deployability. ICLR abstract: "deployability is not an intrinsic property of an agent or its benchmark score, but of an agent-workflow-policy configuration". §6.6: "rather than certifying the agent in isolation".
- **Overlap with DSA:** only DSA's "recognising uncertainty boundaries / escalating correctly" component, operationalised as confidence ranking. READY separates **task-level abstention** (a correct "Indeterminate" verdict is a *success*) from **deployment-level escalation** (§6.3, B.5). WorkTrace needs the same distinction.

### Other useful features

- **Trajectory-invariant vs trajectory-dependent oversight (§3.7).** Terminal accept/escalate can be evaluated by replaying saved runs. Intervention mid-run "changes what happens next" and needs policy-in-the-loop execution or simulation. This is formalised, but only the terminal case is evaluated.
- **Reachable operating points depend on signal granularity.** Gemini-3.1-Pro has only 5 distinct confidence values, so it qualifies only at 100% review.
- **Single-target comparisons are noisy because of threshold overshoot.** The authors recommend comparing on the whole frontier.

## 5. Evaluation

- **Data:** CliniCARE-Bench retrospective clinical audit over MIMIC-IV: 25 scenarios, 750 cases, four-way verdicts (Yes / No / Indeterminate: Lack of Data / Indeterminate: Medically Ambiguous).
- **Systems:** 16 agent systems across the Claude Code, Codex, Gemini CLI and opencode harnesses.
- **Metrics:** a0 (autonomous accuracy), AURC, AUROC, Succ@50%, review %, R̂, 95% LCB, a_h^min, qualified status.
- **Headline numbers (v1):**
  - At Y = 0.76 and a_h = 0.9, Sonnet 5 (a0 = 72.5) qualifies with 29.6% review (LCB 0.826); GPT-5.4 (a0 = 72.8) needs 39.2% (LCB 0.797).
  - GLM-5.2 needs the least review (10.9%) and its point estimate clears the target, but it fails qualification: its LCB is 0.725.
  - 15 of 16 systems qualify at Y = 0.76.
- **Baselines:** no external baselines. Comparisons are across systems, plus the class-based negative control (B.5) and a sensitivity analysis over a_h and the success predicate.
- **Not evaluated:** trajectory-dependent oversight, distribution shift, monitoring.

## 6. What READY covers that WorkTrace must NOT claim

1. Held-out qualification of a frozen escalation policy with an exact binomial (Clopper–Pearson) lower bound, after development-set selection with a margin.
2. Choosing the minimum-cost (maximum-coverage) policy subject to a reliability target, with an **explicit human-review cost**. This is the reliability–oversight–cost frontier.
3. Risk–coverage curve, AURC and AUROC as diagnostics of a routing signal for agents on held-out cases.
4. The thesis that **autonomous accuracy (track record) does not determine deployability**. That is READY's central hypothesis. Our "Beyond Track Records" framing must cite it.
5. Folding a "**correct outcome via a prohibited shortcut**" condition into the deployment success predicate, and showing that this changes the oversight frontier. That is u_df, App. B.3 (also CliniCARE's "defect-free accuracy"; compare ToolChain-CRC in r2_defer).
6. Separating task-level abstention from deployment-level escalation.
7. Version- and lineage-pinned requalification triggers.
8. The trajectory-invariant vs trajectory-dependent distinction for oversight evaluation.

## 7. What READY leaves open that WorkTrace addresses

1. **Per-decision-class grants with a simultaneous certificate across classes.** READY: one global threshold, pointwise claims, simultaneity left to "an appropriate procedure".
2. **The grant rests on tested evidence-handling, not self-reported confidence.** WorkTrace uses interventions on external evidence (remove / only / invert / independent second source) with **ground truth by construction**.
3. **How the wrong basis is detected.** READY uses an LLM-judged rubric on the report plus trajectory, with the judge being one of the evaluated models. WorkTrace uses an interventional test whose answer key comes from the generator. This is the precise W2/W3 seam.
4. **Revocation through anytime-valid sequential monitoring, and re-grant.** READY puts monitoring out of scope.
5. **Evaluation under distribution shift in the evidence** (stale or contradictory sources). READY's guarantee is explicitly in-distribution.
6. **A capability construct (DSA)** that predicts where autonomy is safe. READY declines any agent-level construct.

## 8. Draft related-work text

**One sentence (preferred):**

> READY (Chatrath et al., 2026) qualifies an agent–workflow–oversight configuration by selecting on development cases the lowest-cost accept-or-escalate policy that meets a reliability target and certifying it on held-out cases with an exact binomial bound, routing on the agent's self-reported confidence and, optionally, penalising LLM-judged process shortcuts; WorkTrace adopts this held-out qualification logic but changes what autonomy is granted over and on what grounds — per decision class, from interventions on external evidence whose correct effect is known by construction — and adds anytime-valid revocation and evaluation under evidence shift, both of which READY leaves out of scope.

**Short variant:**

> Unlike READY (Chatrath et al., 2026), which certifies a single confidence-threshold escalation policy per agent and workflow in distribution, WorkTrace certifies autonomy per decision class from intervention tests of evidence use, revokes it sequentially, and evaluates it under evidence shift.

**Supporting sentence for the introduction:**

> Chatrath et al. (2026) show that agents with near-identical autonomous accuracy can require very different human-review burdens to reach the same reliability, because accuracy and the ability to rank one's own failures are nearly uncorrelated; we argue the same holds one level deeper — neither accuracy nor confidence reveals whether an agent's decisions depend on the evidence that should determine them.

## 9. Required changes to claims and baselines

### Claims (W3)

- **Remove from the list of novelties:**
  - held-out qualification;
  - an explicit escalation cost;
  - the risk–coverage or reliability–oversight curve;
  - "loss includes right action on wrong basis" as such.
- **Restate W3 as:** "per-decision-class autonomy certified jointly across classes, where the loss is unjustified action *detected by evidence interventions with constructed ground truth*, revocable by anytime-valid monitoring, and evaluated under evidence shift against outcome-, approval-, counter-, confidence- (READY) and judge-based process-audit (READY-u_df / CliniCARE) rules."
- **Primary endpoint unchanged:** outcome errors of autonomous decisions on held-out episodes under evidence shift. This endpoint is not READY's quantity: READY certifies mixture reliability under an assumed a_h. **State the difference explicitly.** We certify selective risk among autonomous decisions, which does not depend on an assumed review accuracy.
- **Secondary outcome to add:** a READY-style frontier (review burden needed to reach target Y), plus the break-even a_h^min, so results are commensurable with READY.

### Baselines (READY becomes two or three of them)

1. **B-READY-conf:**
   - global threshold on the agent's self-reported confidence;
   - selected on calibration seeds at target + margin (δ = 0.05, as READY does);
   - frozen;
   - Clopper–Pearson qualification on held-out seeds.

   This replaces the vaguer "confidence (CORA/READY)" baseline.
2. **B-READY-proc:** the same machinery with READY's process-aware predicate. The loss is an outcome error OR an **LLM-judged** MUST-NOT shortcut on our episodes' trajectories (judge rubric pre-registered, judge model not among the tested agents). This is the **key ablation**: it isolates *how the wrong basis is detected* (judge vs interventions) and is the strongest reviewer objection ("READY with φ_w = correct ∧ grounded already does this").
3. **(Optional) B-hybrid:** WorkTrace per-class grant ∧ confidence ≥ τ within granted classes. READY itself predicts that combining class and signal information beats either alone (App. B.5).

### Matching and reporting

- Compare at matched autonomous coverage (our plan) **and** at a matched certified target (READY's frontier).
- Report the whole frontier, not single points, because of step-function overshoot with coarse signals.
- A class-level grant is coarse, so coverage moves in jumps. Report reachable operating points.

## 10. Implications for WorkTrace

### Design lessons to adopt (with citation)

- **Disjoint calibration and held-out seeds; freeze the rule before looking.** Use a pre-registered selection margin; READY shows that without it only 46% of selected policies qualify, against 95% with it. Never retune on held-out data; a change requires a new held-out set.
- **Sampling unit.** Multiple stochastic runs of one episode are carried together. Cluster by generator template/seed family, mirroring READY's clustering by patient.
- **Trajectory-dependence.** If escalation happens mid-episode (a decision point inside a multi-step run), evaluation needs policy-in-the-loop simulation of the human resolution, not replay. Declare which regime each decision class is in (cite READY §3.7).
- **Two meanings of "escalate".** Distinguish the agent's own escalation, which is a DSA component and a task-level outcome that can be correct, from the delegation rule's escalation, which is deployment-level. Score them separately (cite READY §6.3).
- **Requalification triggers.** Adopt READY's lineage-pinned triggers (model, harness, tools, population change → re-test) *in addition to* statistical revocation.

### Construct (DSA)

- READY gives no competing construct, but it argues that deployability is a property of the configuration, not of the agent.
- **Define DSA as a profile of an agent configuration (model + harness + tools) per decision class**, not an intrinsic trait.
- Cite READY's routing-quality finding (accuracy ⟂ confidence ranking) as evidence that delegation-relevant capability is separable from the track record. That supports H3's motivation.

### Risks

1. **Reviewer framing.** "WorkTrace = READY with a different φ_w and a per-class policy." Counter with the B-READY-proc ablation and the shift endpoint.
2. **Confidence may beat us in distribution.** READY shows confidence keeps ranking power within classes. Our advantage is predicted mainly *under evidence shift*. Pre-register both regimes and report honestly if we lose in distribution.
3. **Version drift.** The ICLR version may add τ²-bench retail, a certified-set (multiple-testing) procedure and cost comparisons. **Re-read the OpenReview PDF once it is reachable** (log in, or wait for camera-ready/arXiv v2) before final submission. Check especially whether it adds per-class policies or shift experiments.
4. **Terminology.** "Qualification", "deployment profile", "certified set", "routing quality" and "reliability–oversight frontier" are READY's. Use our own terms or cite READY.

### Things to cite

- READY arXiv:2609.02095 (cite the arXiv version with authors; mention the ICLR 2027 submission only as "under review" if needed).
- CliniCARE-Bench arXiv:2608.07796, for defect-free accuracy as an LLM-judged right-outcome/wrong-process measure.
- Inspect AI, as the harness READY builds on, if we use it too.

### Citation cautions

- Both READY versions are preprints; the ICLR version is under review.
- The empirical evidence is a single workflow in v1 (CliniCARE only); the second workflow exists only in the ICLR version, which I have not read.
- Both a_h and every qualification result are conditional on an *assumed* review accuracy (0.9).
- The CliniCARE process-defect labels come from an LLM judge that is also an evaluated system.
- Possible inconsistency between §3.5 and App. B.1 in how the routing fraction is treated (§4(c)).
- The ICLR headline numbers differ from v1 (12.0% vs 29.3% against 29.6% vs 39.2%). **Do not mix numbers across versions.**
