# Round 3: novelty and construct-validity sweep for Decision-Structured Agency (DSA)

Date: 25 Oct 2026. Scope: is "decision-structured agency" (DSA), as defined in CONTEXT.md §9b, already a named or measured construct for AI agents under another name? What is its best philosophical anchor (reasons-responsiveness, planning theory, procedural rationality)? What evidence would establish its construct validity?

Verification convention:
- **[verified]** means title, authors, year and identifier were checked on 25 Oct 2026 against the arXiv API (export.arxiv.org `id_list`) or Crossref (`api.crossref.org/works/<DOI>`).
- **[unverified]** means I could not check the item that way.

Reading depth is stated for every work. Equations in arXiv HTML were stripped by my text conversion; where I describe a formula I am paraphrasing the surrounding prose.

---

## 0. Bottom line (read first)

1. **The term is new.** "Decision-structured agency" returns no hits on the arXiv API (`all:"decision-structured agency"`: 0 results) or the open web. The nearest phrase is the Agency Allocation Framework (arXiv:2604.13534, education), already known.
2. **The construct is not new in its parts, and one part is new in a way that threatens a claim we might have made.** *Reason-responsiveness of a foundation model, measured behaviourally by controlled perturbation and anchored in Meaningful Human Control / Fischer–Ravizza*, already exists:
   - **CARE-Drive** (Suryana et al., arXiv:2602.15645, Feb 2026, TU Delft Centre for Meaningful Human Control) presents itself as "a model-agnostic framework for evaluating reason-responsiveness" that "operationalizes the tracking requirement of Meaningful Human Control".
   - **We must not claim to be the first to operationalise reasons-responsiveness for AI.**
   - CARE-Drive is single-step, injects reasons into the prompt (it does not intervene on external evidence), uses one driving scenario, has no ground truth for the *basis* of the decision, and covers no escalation, authority scope or revision.
3. **Other neighbours each cover one or two DSA dimensions under their own names:**
   - "epistemic competence" (SeekBench, ICLR 2026): grounding, recovery, and sufficiency calibration;
   - "epistemic agency" (Reflection-Bench, ICML 2025): belief construction, updating and meta-reflection in cognitive-psychology tasks;
   - "judgment / selective escalation" (HiL-Bench): knowing when to ask;
   - "escalation behaviour" as a model-specific property (Act or Escalate);
   - "evidence non-uptake / belief revision" (AI scientists, Ríos-García et al.);
   - "goal-directedness" (Everitt et al.): an agentic property measured *conditional on capability* and shown to differ from task performance.

   None of them combines decision-point recognition, interventional grounding with ground truth by construction, authority scope, escalation, revision and provenance into a per-decision-class profile, and none uses such a profile to allocate autonomy.
4. **The defensible novelty of DSA is therefore:**
   - (a) the integration into a per-decision-class profile;
   - (b) measurement by counterfactual interventions on *external evidence* with the decisive evidence known by construction;
   - (c) its use as the basis for delegation, with predictive validity (H3) as the test.

   **The positioning claim must be "a composite construct that integrates and operationalises (for multi-step agents) what the literature measures piecemeal", not "a new capability nobody measured".**
5. **Biggest construct-validity risk: DSA collapsing into general capability.** Latent "capabilities" extracted from LLM benchmarks often proxy model size (Kearns 2026; Burnell et al. 2023; Ruan et al. 2024).

   Encouraging precedents for discriminability exist:
   - goal-directedness "differs from task performance" (Everitt et al.);
   - escalation thresholds "are not predicted by architecture or scale" (Act or Escalate);
   - the epistemic structure of reasoning is invariant across models whose performance differs (Ríos-García et al.).

   The last one is a double-edged sword: if DSA barely varies across agents, it cannot discriminate and cannot drive allocation.

---

## 1. Queries run (≥25 required; 93 run)

### 1a. arXiv API (export.arxiv.org, relevance-sorted): 84 queries

Set 1:
1. `all:"decision-structured agency"` (0 hits)
2. `abs:"decision-structured"`
3. `abs:"epistemic agency" AND abs:(LLM OR "language model" OR agent)`
4. `abs:"grounded agency" AND abs:(LLM OR "language model")`
5. `abs:"rational agency" AND abs:("language model" OR LLM)`
6. `abs:"decision quality" AND abs:"LLM agent"`
7. `abs:"procedural rationality" AND abs:(LLM OR "language model" OR AI)` (0 hits)
8. `abs:"reasons-responsiveness"`
9. `abs:"reasons responsive" AND abs:(AI OR agent OR "language model")`
10. `abs:"deliberative agency"`
11. `abs:"knowing when to ask" AND abs:(LLM OR agent)` (0 hits)
12. `abs:"calibrated deference"`
13. `abs:"principled abstention"`
14. `abs:"judgment" AND abs:benchmark AND abs:"LLM agents" AND abs:escalat*`

Set 2:
15. `abs:"reason-responsiveness"`
16. `abs:"reasons-responsive"`
17. `abs:"meaningful human control" AND abs:(reasons OR tracking) AND abs:(LLM OR "language model" OR agent)`
18. `abs:"construct validity" AND abs:(benchmark OR benchmarks) AND abs:(LLM OR "language model")`
19. `abs:"construct validity" AND abs:agent AND abs:(evaluation OR benchmark)`
20. `abs:"measurement theory" AND abs:("AI evaluation" OR "language model")`
21. `abs:"metacognition" AND abs:"LLM agents" AND abs:(ask OR clarif OR abstain)`
22. `abs:"when to ask" AND abs:(agent OR LLM) AND abs:(clarif* OR help)`
23. `abs:"situational awareness" AND abs:(authority OR permission) AND abs:agent`
24. `abs:"right for the right reasons" AND abs:(agent OR LLM)`
25. `abs:"decision-making competence" AND abs:(LLM OR "language model")`
26. `abs:"agentic judgment" OR abs:"agent judgment" OR abs:"judgment benchmark"`

Set 3:
27. `abs:"epistemic agency" AND abs:(benchmark OR evaluat*)`
28. `abs:agency AND abs:"language model" AND abs:(measure OR measuring) AND abs:(construct OR dimension) AND abs:decision`
29. `ti:agency AND ti:(LLM OR "language model" OR "AI agents") AND abs:(measur* OR evaluat*)`
30. `abs:"evidence sensitivity" AND abs:(LLM OR agent)`
31. `abs:"sensitivity to evidence" AND abs:(LLM OR "language model" OR agent)`
32. `abs:"decision points" AND abs:"LLM agent" AND abs:(recogni* OR identify)`
33. `abs:"scope of authority" AND abs:(agent OR LLM)`
34. `abs:"bounded rationality" AND abs:"LLM agents" AND abs:(evaluat* OR benchmark)`
35. `abs:"belief revision" AND abs:(LLM OR "language model") AND abs:(correction OR evidence) AND abs:agent`
36. `abs:"epistemic vigilance" AND abs:(LLM OR "language model")`
37. `abs:"structured decision" AND abs:"LLM agent" AND abs:(evaluat* OR audit*)`
38. `abs:"general capabilities" AND abs:(construct OR latent) AND abs:(agent OR LLM) AND abs:(factor OR psychometric*)`

Set 4:
39. `abs:"predictive validity" AND abs:(LLM OR "language model" OR agent) AND abs:(benchmark OR evaluation)`
40. `abs:"discriminant validity" AND abs:(LLM OR "language model" OR agent)`
41. `abs:"capability profile" AND abs:(predict*) AND abs:(LLM OR agent)`
42. `abs:"agency" AND abs:"degrees of agency" AND abs:(AI OR LLM)`
43. `abs:"rational agent" AND abs:"language model" AND abs:(coherence OR rationality) AND abs:(evaluat* OR test)`
44. `abs:"practical reasoning" AND abs:(LLM OR "language model") AND abs:(agent) AND abs:(evaluat* OR benchmark)` (0 hits)
45. `abs:"planning theory" AND abs:Bratman AND abs:(AI OR agent OR LLM)`
46. `abs:"responsibility gap" AND abs:(reasons OR tracking) AND abs:(AI OR agent)`
47. `abs:"escalation" AND abs:(benchmark) AND abs:(agent) AND abs:(human OR oversight)`
48. `abs:"decision provenance" AND abs:(agent OR AI)`
49. `abs:"know when" AND abs:(defer OR deferral OR escalate) AND abs:(LLM OR agent)`
50. `abs:"procedural reliability" OR abs:"process reliability" AND abs:(LLM OR agent)`
51. `abs:"epistemic" AND abs:"agent" AND abs:"interventions" AND abs:"evidence" AND abs:"decision"` (0 hits)

Set 5:
52. `abs:agenticness` (the parser ignored the term, so the results were noise)
53. `ti:"characterizing AI agents"`
54. `ti:"levels of autonomy for AI agents"`
55. `ti:"harms from increasingly agentic"`
56. `abs:"reasons" AND abs:"counterfactual" AND abs:"agent" AND abs:"responsiveness" AND abs:(LLM OR "language model")`
57. `abs:"normative competence" AND abs:(LLM OR "language model" OR agent)`
58. `abs:"practical wisdom" AND abs:(LLM OR AI) AND abs:(evaluat* OR measur*)`
59. `abs:"good judgment" AND abs:(LLM OR "AI agents") AND abs:(evaluat* OR benchmark)` (0 hits)
60. `abs:"metacognitive" AND abs:(agent) AND abs:(benchmark) AND abs:(uncertainty) AND abs:(action)`
61. `abs:"scientific reasoning" AND abs:"agents" AND abs:"evidence" AND abs:"belief revision"`
62. `ti:"general scales unlock"`

Set 6:
63. `ti:"measurement and fairness"`
64. `ti:"measuring what matters" AND ti:"construct validity"`
65. `ti:"measurement to meaning"`
66. `ti:"everything in the whole wide world benchmark"`
67. `abs:"epistemic competence" AND abs:agent`
68. `abs:"nomological network" AND abs:(LLM OR AI)`
69. `ti:"evaluating the evaluations" OR (abs:"validity" AND abs:"AI evaluation" AND abs:"framework" AND abs:"social science")`
70. `abs:"reason-sensitivity" OR abs:"responsiveness to reasons"`
71. `abs:"Fischer and Ravizza"` (0 hits)
72. `abs:"guidance control"`

Set 7:
73. `ti:"goal-directedness" AND abs:(LLM OR "language model")`
74. `ti:"observational scaling laws"`
75. `ti:"revealing the structure of language model capabilities"`
76. `abs:"decision-making" AND abs:"construct" AND abs:"LLM agents" AND abs:(psychometric* OR validity)`
77. `abs:"agentic capabilities" AND abs:(taxonomy OR construct) AND abs:(validity OR psychometric)`
78. `abs:"meaningful human control" AND abs:(agentic OR "LLM agents")`
79. `abs:"answerability" AND abs:(agent OR LLM) AND abs:(reasons OR justification) AND abs:responsibility`
80. `abs:"appropriate reliance" AND abs:(agent) AND abs:(escalat* OR defer*)` (0 hits)
81. `abs:"sycophancy" AND abs:"belief revision" AND abs:(correction OR pushback) AND abs:agent` (0 hits)
82. `abs:"instruction hierarchy" AND abs:(authority OR permission) AND abs:(evaluat* OR benchmark)`

Plus `id_list` lookups for metadata (83–84).

### 1b. Web search (covers OpenReview, ICLR, ICML, ACL Anthology, PhilPapers, Springer and Cambridge pages): 9 queries

85. `"reasons-responsiveness" large language models agents evaluation`
86. `"epistemic agency" AI agents benchmark evidence grounded decisions`
87. `Mecacci Santoni de Sio "meaningful human control as reason-responsiveness" dual-mode vehicles`
88. `"decision quality" "procedural rationality" Simon AI agents evaluation process vs outcome`
89. `language model agents "reasons-responsive" philosophy moral responsibility Fischer Ravizza AI systems paper`
90. `openreview LLM agent "decision quality" OR "judgment" benchmark "when to escalate" authority scope evaluation 2026`
91. `Fischer Ravizza 1998 "Responsibility and Control" moderate reasons-responsiveness receptivity reactivity "regular receptivity" "weak reactivity"`
92. `"decision-structured agency"`
93. `"decision-structured" agent AI OR "decision structure" agency LLM construct`

### 1c. Crossref (bibliographic verification and search)

- DOIs checked: Fischer & Ravizza 1998; Messick 1995; Cronbach & Meehl 1955; Campbell & Fiske 1959; Santoni de Sio & van den Hoven 2018; Mecacci & Santoni de Sio 2020; Kane 2013; Borsboom et al. 2004; Jacobs & Wallach 2021; Veluwenkamp 2022.
- Searches: Bratman 1987; Simon 1976 and 1978; McKenna 2013; the Fischer & Ravizza chapter 3 DOI; Sartorio 2016.

---

## 2. Landscape: who uses what name for which part of DSA

| DSA dimension (CONTEXT §9b) | Existing named construct | Work | Measured how | Differs from DSA in |
|---|---|---|---|---|
| Grounding the choice in the right evidence | "reason-responsiveness" (MHC tracking) | CARE-Drive 2602.15645 | Reasons injected into the prompt plus factorial variation of scene context; logit on the decision | Single-step VLM; reasons in the prompt, not interventions on evidence; no ground truth for the basis; no escalation or scope |
| Grounding; recognising insufficiency | "epistemic competence" (groundedness, recovery, calibration) | SeekBench 2509.22391 | Annotation of traces by LLM judge; "answer iff evidence good" | Observational (no interventions); search QA only; no authority or escalation to a human |
| Belief updating, meta-reflection, decision-making | "epistemic agency" | Reflection-Bench 2410.16270 | Cognitive-psychology tasks (WCST, reversal learning, meta-bandit) | Base-model trait in abstract tasks; no external evidence, decision classes or authority |
| Recognising uncertainty or contradiction → escalate | "judgment", "selective escalation" | HiL-Bench 2604.09408 | Blockers (missing, ambiguous, contradictory) plus `ask_human()`; Ask-F1 | Escalation only; blockers are by construction, but nothing tests whether the action depended on the evidence |
| Escalate correctly (cost-sensitive) | "escalation behavior", implicit threshold | Act or Escalate 2604.08588 | Act/escalate under cost ratios; threshold vs. calibration | Single-step classification; no grounding or scope |
| Staying within authority; claimed authority | "boundary adjudication at the decision point" | Troy Moment 2609.15494 (abstract and intro only) | Impossible tasks, forged authorisation, peer evidence | Single boundary type (protected test file); no delegation rule |
| Revising after correction; evidence uptake | "epistemic norms of inquiry" (evidence non-uptake, refutation-driven revision) | Ríos-García et al. 2604.18805 | Graph annotation of epistemic operations in 25k runs | Observational; scientific domains; no interventions on evidence |
| (Methodological template) agentic property ≠ performance | "goal-directedness" | Everitt et al. 2504.11844 | Capability-conditioned: performance relative to what full use of measured sub-capabilities would give | Different property (effort or propensity), but the right *validation design* |
| Recognising decision points; distal reasons | "anticipatory oversight", "tracking distal reasons" | Baum et al. 2609.24242 | None (philosophical) | Conceptual; agenda (purposes, authorisation boundaries, considerations, escalation triggers) is the same decomposition, unmeasured |
| Epistemic competence as a trust requirement | "demonstrable epistemic competence" | Marchal et al. 2603.02960 (abstract and keyword scan only) | None (normative) | Position paper |
| Amount of agency (not its quality) | "agenticness", agency dimensions | Chan et al. 2302.10329; Kasirzadeh & Gabriel 2504.21848; Feng et al. 2506.12469 (metadata only, not read) | Conceptual | Measure *how agentic*, not *how well-structured the decisions are* |

No work found uses "decision quality" for LLM agents in our sense. Hits were Pinterest moderation quality (2602.15809) and decision-oriented text evaluation (2507.01923). "Procedural rationality" returns 0 hits on arXiv in combination with LLM or AI. "Calibrated deference" and "principled abstention" occur only incidentally (molecular design, clinical triage). An Evidence Model for Agentic Processes (2609.08481, flagged in CONTEXT §9b) is a conceptual vocabulary of audit-evidence claims (provenance, approval evidence, deliberation traceability), not a capability construct. It is not a threat to DSA (abstract only).

---

## 3. Closest works, characterised

### 3.1 CARE-Drive: reason-responsiveness of VLMs (closest conceptual and operational precedent)

**Bibliographic data [verified, arXiv API]**
- Lucas Elbert Suryana, Farah Bierenga, Sanne van Buuren, Pepijn Kooij, Elsefien Tulleners, Federico Scari, Simeon Calvert, Bart van Arem, Arkady Zgonnikov.
- "CARE Drive A Framework for Evaluating Reason-Responsiveness of Vision Language Models in Automated Driving." arXiv:2602.15645v1, 17 Feb 2026. The arXiv comment reads "on submission to Transportation Research Part C".
- The HTML title has a hyphen: "CARE-Drive: …".

**Read:** full HTML, §1–§6 (abstract, intro, related work, framework, results, discussion, limitations). Stage-1 calibration tables were skimmed. References were not read.

**Problem and contribution**
- Outcome metrics (collision, trajectory error) "do not assess whether the underlying decision appropriately reflects human higher-level reasoning".
- Explanations may be post-hoc (citing Turpin 2023).
- The paper proposes "a model-agnostic framework for evaluating reason-responsiveness" that "operationalizes the tracking requirement of Meaningful Human Control" (abstract).

**Method**
- Baseline decision vs. "reason-augmented" decision, where normative reasons (safety, legality, comfort, efficiency) are injected into the prompt.
- Stage 1 calibrates model and thought strategy (CoT or ToT) towards an expert reference decision.
- Stage 2 varies observable context full-factorially: time-to-collision, vehicle behind, passenger urgency, following time, explanation length. Each cell has 30 runs.
- A binary logit on overtake vs. stay behind estimates sensitivity to each factor.
- CARLA closed-loop check.

**Evaluation**
- One scenario: overtaking a cyclist on a no-passing road.
- TTC dominates: P(overtake) goes from 12.4% to 74.3%.
- A vehicle behind raises P to 34.9%.
- Passenger urgency *lowers* it to 5.6%, which is "contrary to our intuition".
- Following time is not significant.
- The explanation-length constraint drives P to about 0.2%.
- The authors conclude responsiveness is "not uniform across all tested reasons" (§5.1).

**What WorkTrace must NOT claim**
- That reasons-responsiveness or MHC tracking has never been operationalised as a behavioural, perturbation-based evaluation of foundation models.
- That anchoring AI evaluation in MHC tracking (Santoni de Sio & van den Hoven 2018; Mecacci & Santoni de Sio 2020) is new.

**What it leaves open that WorkTrace addresses**
- Multi-step agents acting on external evidence.
- Interventions on *evidence* rather than prompt-injected reasons.
- Ground truth for *which* evidence should be decisive (CARE-Drive has an expert reference decision, not a reference basis).
- Explicit declared grounds compared against interventional sensitivity.
- Escalation, authority scope, revision.
- Use of the measurement to allocate autonomy.
- The authors themselves state that CARE-Drive "does not claim causal relationships between reasons and decisions" but only "systematic associations" (§5.2).

**Draft differentiation:** "CARE-Drive (Suryana et al., 2026) operationalises the MHC tracking condition for a vision–language driving model by varying scene context and prompt-injected reasons; we extend behavioural reasons-responsiveness testing to multi-step agents acting on external evidence, with the decisive evidence known by construction, and use the resulting per-class profile to grant or withhold autonomy."

**Citation cautions**
- Preprint under submission.
- Single scenario; calibration selects configurations by alignment with the expert decision, which the authors acknowledge (§5.3).
- Related series from the same group: Suryana et al. 2025, "A Framework for Human-Reason-Aligned Trajectory Evaluation in Automated Vehicles," arXiv:2507.23324 [verified; not read].

### 3.2 SeekBench: "epistemic competence" of search agents

**Bibliographic data [verified, arXiv API]**
- Jiaqi Shao, Yuxiang Lin, Munish Prasad Lohani, Yufeng Miao, Bing Luo.
- "Do LLM Agents Know How to Ground, Recover, and Assess? A Benchmark for Epistemic Competence in Information-Seeking Agents." arXiv:2509.22391v1, 26 Sep 2025.
- Listed as an ICLR 2026 poster (iclr.cc virtual page and mlanthology, from web search) [venue unverified against OpenReview].

**Read:** abstract, §1–§3 in full, §4.1–§4.3. §4.4–§5 and appendices were not read.

**Problem and contribution**
- Search-agent evaluation is answer-only.
- The paper defines epistemic competence as "the ability to reliably acquire, evaluate, and act upon knowledge in a justified manner".
- It decomposes it into groundedness, recovery and calibration (Table 1).

**Method**
- 190 expert-annotated traces (more than 1,800 steps); Cohen's κ reported; LLM judges for scale.
- "Evidence state" = (clarity, sufficiency) per turn.
- RQI = share of reasoning steps grounded in evidence.
- ERF = cumulative recovery to good evidence.
- Calibration Error = deviation from the ideal policy "answers if and only if the evidence is good".
- Explicitly invokes "latent construct inference (Cronbach and Meehl, 1955)" (§3.2).
- Validity evidence offered: inter-annotator agreement plus the correlation of evidence state with answer accuracy (§3.3).

**Evaluation**
- 28,493 traces over 7 QA datasets; Qwen-2.5-7B base and few-shot vs. RL agents (Search-R1, ReSearch, ASearcher, DeepResearcher).
- Few-shot achieves the highest RQI (0.27). The paper concludes "RL training may optimize for correct final answers, but it fails to develop the epistemic reasoning skills" (§4.2).

**What WorkTrace must NOT claim**
- That nobody measures evidence grounding or evidence-sufficiency calibration of agents as a named competence distinct from accuracy.
- That RL- or outcome-optimised agents degrading in grounding is our finding.

**What it leaves open**
- Measurement is observational (judge labels on whether reasoning is "supported"), not interventional. It cannot tell whether the answer *depended* on the evidence.
- No ground truth for the decisive evidence.
- No action authority, escalation to a human, revision under correction, or decision classes.
- Its own validity argument uses correlation with accuracy as validation, which is the *opposite* of the discriminant evidence DSA needs.

**Draft differentiation:** "SeekBench measures the epistemic competence of search agents from annotated traces; DSA tests interventionally whether an agent's *actions* depend on the evidence that should determine them, and adds authority scope, escalation and revision."

**Citation cautions**
- Small expert set; large-scale labels come from GPT-4.1-mini.
- "Calibration" here is behavioural (answer vs. evidence state), not probabilistic.

### 3.3 Reflection-Bench: "epistemic agency" of LLMs

**Bibliographic data [verified, arXiv API]**
- Lingyu Li, Yixu Wang, Haiquan Zhao, Shuqi Kong, Yan Teng, Chunbo Li, Yingchun Wang.
- "Reflection-Bench: Evaluating Epistemic Agency in Large Language Models." arXiv:2410.16270v3 (v1 21 Oct 2024; v3 4 Jun 2025).
- ICML 2025 per mlanthology (web search) [venue unverified via DBLP or OpenReview].

**Read:** abstract, §1, §2.1, §3.1 and §5 (discussion and limitations). Task adaptations (§3.3) and results (§4) were not read.

**Problem and contribution**
- Defines "epistemic agency, the ability to flexibly construct, adapt, and monitor beliefs about dynamic environments", as "a base-model-level capacity".
- Decomposes it into seven dimensions: prediction, decision-making, perception, memory, counterfactual thinking, belief updating, meta-reflection.
- Also cites Kockelman's three aspects of agency, including "being accountable for the outcomes of their actions" (§2.1).

**Method:** seven parameterised cognitive tests (weather prediction, WCST, oddball, n-back, Iowa gambling, probabilistic reversal learning, meta-bandit). 16 models, 3 prompting strategies.

**Evaluation:** a three-tier hierarchy (top models score above 60). Meta-reflection is weakest.

**What WorkTrace must NOT claim:** that "agency" of LLMs as a measured epistemic capability (belief updating, meta-reflection) is a new idea.

**What it leaves open**
- External evidence in realistic work contexts; tool-using multi-step agents (explicitly excluded: "rather than evaluating specialized agent architectures").
- Authority; escalation; the link to delegation.
- No discriminant analysis against general capability. The hierarchy looks like a general-capability ordering (my reading; not tested by the authors).

**Draft differentiation:** "Reflection-Bench measures epistemic agency as a base-model trait with cognitive-psychology tasks; DSA is a per-decision-class property of a deployed agent (model plus scaffold plus permissions), measured on its handling of external evidence and authority."

**Citation cautions:** abstract tasks; ecological validity acknowledged as open (§5, Limitations).

### 3.4 Everitt et al.: goal-directedness (methodological template for discriminant validity)

**Bibliographic data [verified, arXiv API]**
- Tom Everitt, Cristina Garbacea, Alexis Bellot, Jonathan Richens, Henry Papadatos, Siméon Campos, Rohin Shah.
- "Evaluating the Goal-Directedness of Large Language Models." arXiv:2504.11844v1, 16 Apr 2025.
- ICML keyword in the HTML; venue not confirmed [unverified].

**Read:** abstract, §1, §2 (partial), §3.1, §4.2–§4.3. §3.2–§3.5, §4.1, §4.4 and §5 were not read.

**Problem and contribution**
- "approaches in AI often equate goal-directedness with task performance … But task performance arguably says more about capability than goal-directedness" (§1).
- Defines goal-directedness as "propensity to use available resources and capabilities to achieve a given goal".

**Method:** capability-conditioned measure. Performance is normalised between a random baseline and the performance expected with full use of the model's *measured* sub-capabilities (inferred from standalone subtasks), in Blocksworld composite tasks (information gathering, cognitive effort, plan-and-execute).

**Evaluation:** GD "differs from task performance" (§4.2). For example, GPT-4/4o "excel at execution when done in isolation … yet perform no better" on the composite task. GD is "fairly consistent … across tasks" and agrees with alternative measures (falling-tower rebuilding, number of measurements) (§4.3).

**What WorkTrace must NOT claim:** that separating an agentic property from task success by conditioning on capability is our methodological innovation.

**What it leaves open**
- Goal-directedness is a different property (effort or propensity), unrelated to evidence-basis or authority.
- The paper offers the right validation template for DSA:
  - (i) capability-conditioned scoring;
  - (ii) cross-task rank consistency (convergent);
  - (iii) agreement with alternative operationalisations;
  - (iv) explicit non-identity with task performance (discriminant).

**Draft differentiation:** "Following Everitt et al.'s capability-conditioned measurement of goal-directedness, we validate DSA as distinct from task success."

**Citation cautions:** toy environment; small model set.

### 3.5 HiL-Bench: "judgment" as selective escalation

**Bibliographic data [verified, arXiv API]**
- Tu Trinh, Mohamed Elfeki, Guangze Luo, Kelvin Luu, Nathan Hunt, Ernesto Hernandez, Nandan Marwaha, Yannis Yiming He, Charles Wang, Fernando Carabedo, Alessa Castillo, Bing Liu.
- "HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?" arXiv:2604.09408v4 (v1 10 Apr 2026). Scale AI PDF host.

**Read:** abstract, §1–§3.2. Quality criteria, results, failure taxonomy and RL sections were not read.

**Problem and contribution:** "The bottleneck is not raw capability, but judgment: knowing when to act autonomously and when to ask for help." Judgment is defined as "selective escalation: the ability to recognize, mid-task, that a gap cannot be resolved through exploration or inference alone".

**Method**
- SWE-Bench Pro and BIRD tasks with 3–5 injected, human-validated blockers: missing information (42%), ambiguous requests (36%), contradictory information (22%).
- Blockers surface through "progressive discovery".
- An `ask_human()` oracle answers only registered blockers.
- Ask-F1 = harmonic mean of question precision and blocker recall.
- Tasks selected where full-information pass@3 is at least 85%, "ensuring that performance drops under blocked conditions are as minimally confounded by capability limits as possible" (§3.1).

**Evaluation (abstract and Fig. 1):** 75–89% pass@3 with full information vs. 4–24% when the agent must judge when to ask. RLVR on Ask-F1 improves a 32B model, and the gains transfer across domains.

**What WorkTrace must NOT claim:** that "knowing when to escalate" under missing, ambiguous or contradictory information is an unnamed or unmeasured capability, or that a full-information control to separate judgment from capability is new.

**What it leaves open**
- No test of whether the agent's *autonomous* actions depend on the right evidence (a lucky correct guess and a well-grounded action are not distinguished when no blocker is involved).
- No authority scope, no revision, no decision classes, no delegation.
- The "contradictory information" blocker is close to our "add an independent second source" intervention in spirit. Ours varies the *agreement* of independent sources on a decisive fact and asks whether action or escalation changes. Theirs registers a contradiction that must be asked about.

**Draft differentiation:** "HiL-Bench measures selective escalation against registered blockers; DSA treats escalation as one dimension of a profile whose core is interventional evidence-dependence, and conditions escalation scoring on the same episodes in which grounding is tested."

**Citation cautions:** the industry benchmark's paper has been revised several times (v4). Scale AI affiliation.

### 3.6 Act or Escalate? Escalation as a model-specific property

**Bibliographic data [verified, arXiv API]**
- Matthew DosSantos DiSorbo, Harang Ju.
- "Act or Escalate? Evaluating Escalation Behavior in Automation with Language Models." arXiv:2604.08588v1 (submitted 31 Mar 2026).

**Read:** abstract, §1, §2 (theory), §3.1. Results and the SFT section were not read.

**Problem and contribution:** escalation as a decision under uncertainty: escalate iff the estimated probability of being correct is below the cost-optimal threshold (Theorems 1–2, §2).

**Method:** five domains of recorded human decisions (HotelBookings, LendingClub, content moderation, recommendation, MoralMachine). Eight models; varied cost ratios; interventions (cost framing, accuracy signals, SFT on CoT).

**Evaluation (abstract, §1):** implicit thresholds "vary substantially and are not predicted by architecture or scale". Self-estimates are miscalibrated in model-specific ways. SFT generalises to held-out domains.

**What WorkTrace must NOT claim:** that escalation propensity has not been characterised as a model-specific, pre-deployment property.

**What it leaves open:** escalation driven by *evidence structure* (contradiction, insufficiency, out-of-scope authority) rather than self-estimated accuracy; grounding; scope; multi-step agents.

**Useful for us:** evidence that an escalation-related trait is *not* explained by scale. This is a prior for DSA's discriminant validity against general capability.

**Draft differentiation:** "Act or Escalate characterises confidence-threshold escalation on single-step predictions; DSA asks whether escalation is triggered by the right features of the evidence."

**Citation cautions:** single-step tabular tasks; two authors; preprint.

### 3.7 Ríos-García et al.: AI scientists ignore evidence

**Bibliographic data [verified, arXiv API]**
- Martiño Ríos-García, Nawaf Alampara, Chandan Gupta, Indrajeet Mandal, Sajid Mannan, Ali Asghar Aghajani, N. M. Anoop Krishnan, Kevin Maik Jablonka.
- "AI scientists produce results without reasoning scientifically." arXiv:2604.18805v1, 20 Apr 2026.

**Read:** abstract, §1, §2 (all results). §3 discussion and §4 methods were not read.

**Problem and contribution:** do LLM scientific agents follow the epistemic norms of inquiry?

**Method**
- More than 25,000 runs, 8 domains, 3 models × 2 scaffolds.
- IRT on diagnostic items, with a latent-factor model of task success.
- LLM annotation of traces into a graph of epistemic operations (hypothesis, evidence, test, judgment, update, commitment), with motifs and anti-patterns.
- "Trace interventions": injecting partial successful or failed trajectories.

**Evaluation**
- Base model accounts for 41.4% of explained variance vs. 1.5% for the scaffold.
- "evidence is ignored in 68% of traces, refutation-driven belief revision occurs in 26%"; convergent multi-test evidence occurs in 7%.
- "Models differ in the raw frequency of individual operations … but the topology of their reasoning graphs is similar. Higher-performing models … The epistemic structure of their reasoning does not change correspondingly" (§2).

**What WorkTrace must NOT claim:** that agents' failure to take up evidence or revise beliefs is a new finding.

**What it leaves open:** interventions on the *evidence* itself (their interventions inject trajectories); decision authority; escalation; delegation.

**Two lessons for DSA**
- (+) Dissociation between performance and epistemic structure. This is prima facie support that a decision-structure construct is not just capability.
- (−) Near-invariance across models. If DSA behaves the same way, it will have low between-agent variance and little power to differentiate autonomy grants. We must check variance components early in the pilot.

**Draft differentiation:** "Ríos-García et al. document evidence non-uptake by annotating the structure of reasoning traces; DSA measures it interventionally at the level of actions."

**Citation cautions:** annotation by Claude Sonnet 4.5, which is also an evaluated model.

### 3.8 Baum, Kiener, Langer, Laux: anticipatory human oversight (philosophical neighbour)

**Bibliographic data [verified, arXiv API]**
- Kevin Baum, Maximilian Kiener, Markus Langer, Johann Laux.
- "Anticipatory Human Oversight of Agentic AI: A Philosophical Account." arXiv:2609.24242v1, 21 Sep 2026 (cs.CY).

**Read:** abstract, §2.3–§3.3. §1, §2.1–§2.2, §3.4–§7 were not read.

**Problem and contribution**
- Reactive oversight reaches structural limits for agentic AI.
- Anticipatory oversight specifies a "normative agenda" of four kinds of content: purposes, **authorisation boundaries**, considerations (distal reasons) and **escalation triggers** (§3.1).
- Oversight is "the operationalisation of distal-reason tracking".

**Philosophy content (useful for us)**
- §2.3 states that, in MHC, "A system tracks a reason just in case its behaviour would be different if the reason were different". Santoni de Sio and van den Hoven "read it as a form of reasons-responsiveness" (footnote 1 cites Fischer and Ravizza 1998).
- Proximal vs. distal reasons (Mecacci & Santoni de Sio 2020, following Mele's rendering of Bratman).
- Veluwenkamp (2022): tracking must be of *normative*, not merely motivating, reasons.
- Agent-relativity is secured via the principal's roles.

**Evaluation:** none (philosophical).

**What WorkTrace must NOT claim:** that authorisation boundaries and escalation triggers as delegation structure are our conceptual invention, or that a counterfactual tracking reading for agentic AI is new.

**What it leaves open:** measurement. How to *test* whether an agent tracks the agenda ("the agent's behaviour covaries with the agenda when the agenda changes") is stated as a criterion but not operationalised. DSA's interventions are exactly such tests, at the level of evidence and authority.

**Draft differentiation:** "Baum et al. (2026) argue that anticipatory oversight requires agents whose behaviour tracks an articulated agenda of authorisation boundaries and escalation triggers; DSA supplies a behavioural test of such tracking per decision class."

**Citation cautions:** philosophical preprint. It cites a forthcoming Baum et al. (2026) on principal–agent delegation, which I did not find or verify.

### 3.9 Brief notes (partial reading)

- **The Troy Moment** — Ivy Zhang, arXiv:2609.15494v3 (Sep 2026) [verified].
  - Read: abstract and first part of the intro only.
  - Controlled "decision point" on impossible software tasks; varies instruction strictness, tool friction, peer evidence and **forged authorisation**.
  - Closest existing test of "staying within authority under conflicting evidence".
  - Cite for the authority-scope dimension.
  - **Caution:** it references a "July 2026 OpenAI–Hugging Face incident" and models "GPT-5.6 Sol", "Claude Fable 5.1", which I could not corroborate. Treat as low-confidence until checked.
- **Beyond Static Leaderboards: Predictive Validity for the Evaluation of LLM Agents** — Dhaval C. Patel et al. (61 authors), arXiv:2606.19704v1 [verified].
  - Read: abstract, §1, §4.
  - Defines predictive validity as "the correlation between in-sample rank and out-of-sample rank".
  - Proposes OOD criteria: held-out scenarios, cross-subset transfer, adversarial perturbation.
  - Position paper; empirical validation is future work.
  - Cite when we call H3 "predictive validity", but note our criterion is *outcome errors of autonomous decisions under evidence shift*, not rank stability.
- **Architecting Trust in Artificial Epistemic Agents** — Nahema Marchal, Stephanie Chan, Matija Franklin, Manon Revel, Geoff Keeling, Roberta Fischli, Bilva Chandra, Iason Gabriel, arXiv:2603.02960v2 [verified].
  - Read: abstract plus keyword scan.
  - Normative: trustworthy epistemic agents need "demonstrable epistemic competence … including the capacity to evaluate the reliability of evidence", falsifiability, and epistemic virtue. It foresees a shift "from the evaluation of output accuracy to the evaluation of process-qualities".
  - Motivation, not competition.
- **Why Sampling Is Not Choosing** — Joseph Keshet, arXiv:2606.13441v2 [verified]; ICML 2026 listing per web search [unverified].
  - Read: abstract only.
  - Argues that LLM outputs "are neither owned as commitments nor guided by reasons".
  - **Risk for our naming** ("agency", "reasons"). We must say DSA is a *functional, behavioural* property and makes no claim about intentionality or responsibility (see §4.5).
- **Reading the Room: normative competence in LLMs** — Wynn, Satija, Baek, Liu, Nalisnick, Hadfield, arXiv:2610.10906v2 [verified].
  - Read: title and abstract hit only.
  - Another "competence" construct (normative, not evidential). Check before submission.

---

## 4. Philosophy anchor

### 4.1 Fischer & Ravizza: guidance control and moderate reasons-responsiveness

**Sources**
- Fischer, J. M., & Ravizza, M. (1998). *Responsibility and Control: A Theory of Moral Responsibility*. Cambridge University Press. DOI 10.1017/CBO9780511814594 [verified, Crossref].
- Chapter 3, "Moral Responsibility for Actions: Moderate Reasons-Responsiveness", pp. 62–91, DOI 10.1017/cbo9780511814594.003 [verified, Crossref].

**I did not read the book.** The summary below rests on:
- the Cambridge chapter landing-page summary;
- SEP, "Moral Responsibility" §2.3 (fetched; partially read, first 100k characters);
- secondary sources surfaced by web search (Santa Clara Scholar Commons, "Receptivity, reactivity and the successful psychopath"; a PhilArchive review);
- my background knowledge.

Before quoting, check exact wording against ch. 3 of the book.

**Key ideas**
1. **Guidance control vs. regulative control.**
   - Following Frankfurt cases, responsibility does not require alternative possibilities (regulative control).
   - It requires *guidance control*: the action issues from the agent's own, suitably reasons-responsive mechanism. SEP §2.3: "guidance control depends on whether the psychological mechanism that issues in an agent's behavior is responsive to reasons".
   - Two consequences:
     - Responsiveness is assessed for the *actual-sequence mechanism* ("the process that leads to the relevant upshot"), holding the kind of mechanism fixed across counterfactual scenarios.
     - Responsiveness is a *dispositional, counterfactual* property: what the mechanism would do if the reasons were different.
2. **Receptivity vs. reactivity.**
   - The chapter distinguishes "recognition of reasons" from "reaction to reasons" (choosing in line with recognised reasons). It argues the requirements on recognition are stricter than those on reaction (Cambridge chapter summary).
   - Receptivity is the capacity to recognise which reasons exist and their force.
   - Reactivity is the capacity to translate recognised reasons into choice and action.
3. **Moderate reasons-responsiveness = regular receptivity + weak reactivity of the actual-sequence mechanism.**
   - Moderate RR sits between "strong" RR (too demanding: would always do otherwise when there is sufficient reason) and "weak" RR (too permissive).
   - **Regular receptivity:** the mechanism exhibits "an understandable pattern of (actual and hypothetical) reasons-receptivity" (SEP §2.3, paraphrasing F&R). Example of pattern coherence: "acceptance of one reason as sufficient implies that a stronger reason must also be sufficient". The pattern must include receptivity to moral reasons.
   - **Weak reactivity:** it suffices that there is *some* possible scenario (same kind of mechanism) in which the agent recognises a sufficient reason to do otherwise and does otherwise for that reason. F&R argue reactivity is "all of a piece".
4. **Ownership (historical condition).** The mechanism must be the agent's own, through "taking responsibility" (SEP §3.9). Not relevant to us beyond a caution (§4.5).
5. **Known criticisms** (relevant to our use; secondary sources only): the receptivity/reactivity asymmetry; mechanism individuation; agent-based alternatives (McKenna 2013, "Reasons-Responsiveness, Agents, and Mechanisms", *Oxford Studies in Agency and Responsibility* vol. 1, pp. 151–183, DOI 10.1093/acprof:oso/9780199694853.003.0007 [verified, Crossref; not read]); Sartorio (2016), *Causation and Free Will*, OUP, DOI 10.1093/acprof:oso/9780198746799.001.0001 [verified, Crossref; not read], who argues for an actual-causation, reasons-*sensitivity* view.

**Bridge to AI via Meaningful Human Control**
- Santoni de Sio, F., & van den Hoven, J. (2018). "Meaningful Human Control over Autonomous Systems: A Philosophical Account." *Frontiers in Robotics and AI*, 5. DOI 10.3389/frobt.2018.00015 [verified].
  - Introduces the tracking condition (the system's behaviour covaries with the relevant reasons of relevant humans) and the tracing condition (some human understands the system and is positioned to bear responsibility).
  - Per Baum et al. §2.3, it formalises tracking via Nozick-style subjunctives and reads it as reasons-responsiveness.
- Mecacci, G., & Santoni de Sio, F. (2020). "Meaningful human control as reason-responsiveness: the case of dual-mode vehicles." *Ethics and Information Technology*, 22(2), 103–115. DOI 10.1007/s10676-019-09519-w [verified; Crossref issue year 2020, online 2019]. Proximal vs. distal reasons.
- Veluwenkamp, H. (2022). "Reasons for Meaningful Human Control." *Ethics and Information Technology*, 24(4). DOI 10.1007/s10676-022-09673-8 [verified]. Tracking must be of normative reasons.

The MHC lineage, not Fischer–Ravizza directly, is the route by which reasons-responsiveness entered AI evaluation (CARE-Drive). **We should cite both:** Fischer–Ravizza for the receptivity/reactivity structure, MHC for the transfer to artefacts.

### 4.2 How DSA's interventions operationalise receptivity and reactivity

The mapping holds the actual-sequence "mechanism" fixed: the same agent configuration, decision class and episode template, with only the evidence item X changed. That is the F&R move of evaluating the same kind of mechanism across counterfactual scenarios. Our interventions are literally the counterfactual scenarios.

| F&R / MHC notion | DSA operationalisation | Intervention or measurement |
|---|---|---|
| **Receptivity:** recognising that a reason is present and what it weighs | Recognises the decision point and alternatives; identifies decisive evidence; detects insufficiency or contradiction; detects out-of-scope authority | **only X** (is X recognised as sufficient?); **remove X** (does the agent register that the basis is gone, e.g. declares insufficiency or escalates?); **add an independent second source** that agrees or conflicts (is corroboration or contradiction recognised?) |
| **Reactivity:** translating a recognised reason into the choice | The action (proceed, escalate, refuse) changes when, and only when, the decisive evidence changes | **invert X** (does the action flip when the decisive fact flips?); **remove X** (does the agent stop proceeding?); placebo intervention on non-decisive evidence (the action should *not* change) |
| **Regular (patterned) receptivity:** an understandable pattern across actual and hypothetical cases, e.g. "stronger reason also sufficient" | Consistency of responses *across* interventions and graded strengths; monotonicity | Graded interventions (weaker or stronger contrary evidence; one vs. two independent sources); check monotonicity: if a weak contradiction triggers escalation, a stronger one must too |
| **Motivating vs. normative reasons** (Veluwenkamp) | Declared grounds (motivating: what the agent says it acts on) vs. generator's decisive evidence (normative: what should determine the act, known by construction) | Joint reading of the four conditions against the declared-grounds graph: faithfulness (declared ↔ interventionally effective) and correctness of basis (effective ↔ normatively decisive) |
| **Proximal vs. distal reasons** (Mecacci & Santoni de Sio) | Episode evidence = proximal; authority scope, decision-class policy and legally reserved classes = distal | Scope-violation probes (forged or claimed authority, out-of-class requests); revision after correction (does a principal's correction propagate to later decisions?) |
| **Tracing** (MHC) | Provenance preservation; reconstructability of the decision path | Provenance fields in the episode; reconstructability check (not a reasons-responsiveness test) |

**Design lesson from the asymmetry.** F&R accept *weak* reactivity because they ask whether an agent is *blameworthy*. Delegation asks whether outcomes will be reliable when no human checks. **DSA should therefore require regular receptivity *and* regular reactivity**: the action must change in a patterned way across most relevant counterfactual scenarios, not merely in one. This is stricter than moderate RR and should be stated explicitly: "we borrow the structure (receptivity/reactivity, counterfactual scenarios over a fixed mechanism), not the threshold". The F&R "weak reactivity" criterion corresponds to an existence check (some intervention flips the action). Our certification uses rates over many interventions per class.

### 4.3 Bratman's planning theory (relevant but secondary)

**Source:** Bratman, M. E. (1987). *Intention, Plans, and Practical Reason*. Harvard University Press [partially verified: Crossref has four reviews of the book (Noûs 25(2), 1991; Philosophical Review 100(2), 1991; Ethics 100(1), 1989; PPR 50(1), 1989), but no record for the book itself. Publisher and year are from background knowledge; reissued by CSLI 1999, unverified]. Not read in this round.

**Relevance (background knowledge, to be checked)**
- Future-directed intentions are partial plans subject to consistency and means–end coherence norms.
- Plans have *stability*: non-reconsideration is the default.
- Plans provide a *filter of admissibility* on options considered in deliberation.

**Mapping**
- (i) Decision classes and authority scope act as a standing plan-like filter on admissible actions (an out-of-scope option should not even be deliberated as a live option, only escalated).
- (ii) "Revision after correction" corresponds to the norms of reconsideration. A good agent neither reconsiders everything at every step (instability) nor ignores a correction that defeats its plan (rigidity).
- (iii) The distal reasons of Mecacci & Santoni de Sio *are* Bratman-style plans (via Mele's proximal/distal intentions; Baum et al. §2.3 fn. 2).

**Recommendation:** cite Bratman in one sentence for the scope/filter and revision dimensions; do not build the construct on it.

### 4.4 Simon's procedural rationality (framing for "process vs. outcome")

**Sources**
- Simon, H. A. (1976). "From substantive to procedural rationality." In S. J. Latsis (ed.), *Method and Appraisal in Economics*, Cambridge University Press, pp. 129–148. DOI 10.1017/cbo9780511572203.006 [verified, Crossref; Crossref also lists a Springer reprint in *25 Years of Economic Theory*, pp. 65–86].
- Simon, H. A. (1978). "Rationality as process and as product of thought." *American Economic Review* 68(2), 1–16 [unverified via Crossref: the query returned only a 1988 reprint in *Decision Making* (CUP), DOI 10.1017/cbo9780511598951.005, verified].

Neither was read in this round. The often-quoted definition is "Behavior is procedurally rational when it is the outcome of appropriate deliberation. Its procedural rationality depends on the process that generated it" [quoted from memory; verify against the 1976 chapter before use].

**Relevance:** the outcome-only ("substantive") vs. process ("procedural") distinction is exactly the track-record vs. DSA contrast. Simon is the classic citation for "judging decisions by their procedure, not their consequences". **Risk:** a reviewer may say DSA = procedural rationality renamed. **Answer:**
- procedural rationality is a *normative standard for deliberation*;
- DSA is a *measured, per-class behavioural profile* whose procedure tests are counterfactual dependence on evidence and authority.

Cite Simon as the ancestor of the distinction, not as a competitor.

### 4.5 Cautions on philosophical vocabulary

- **"Agency".** In the AI-governance literature, agency/agenticness denotes *degree* (autonomy, goal complexity, directness of impact, long-horizon planning: Chan et al. 2023, DOI 10.1145/3593013.3594033; Kasirzadeh & Gabriel 2025; Feng et al. 2025; all verified, none read).
  - DSA is about the *structure* of decisions, not the amount of agency. A highly agentic system can have low DSA.
  - Say so in one sentence to pre-empt confusion.
- **"Reasons".** Keshet (2026) and others deny that LLMs act for reasons.
  - Adopt the MHC "tracking" reading: a purely behavioural, counterfactual covariation of actions with reasons-as-evidence, with no claim of intentionality, ownership or moral responsibility.
  - F&R's ownership condition is explicitly *not* imported.
  - Responsibility stays with the human principal (the MHC tracing condition).
- Do not write "the agent is reasons-responsive" tout court. Write "the agent's decisions in class c exhibit behavioural reasons-responsiveness to the decisive evidence (receptivity rate r, reactivity rate s)".

---

## 5. Construct validity: what evidence DSA needs

### 5.1 Frameworks to cite (all verified)

- **Cronbach, L. J., & Meehl, P. E.** (1955). "Construct validity in psychological tests." *Psychological Bulletin* 52(4), 281–302. DOI 10.1037/h0040957. The nomological network.
- **Campbell, D. T., & Fiske, D. W.** (1959). "Convergent and discriminant validation by the multitrait-multimethod matrix." *Psychological Bulletin* 56(2), 81–105. DOI 10.1037/h0046016. MTMM.
- **Messick, S.** (1995). "Validity of psychological assessment: Validation of inferences from persons' responses and performances as scientific inquiry into score meaning." *American Psychologist* 50(9), 741–749. DOI 10.1037/0003-066X.50.9.741.
  - Unified validity with six aspects: content, substantive, structural, generalisability, external, consequential (from background knowledge; paper not re-read).
- **Kane, M. T.** (2013). "Validating the interpretations and uses of test scores." *Journal of Educational Measurement* 50(1), 1–73. DOI 10.1111/jedm.12000. Argument-based validation of *interpretation and use*. Our use is the delegation decision.
- **Borsboom, D., Mellenbergh, G. J., & van Heerden, J.** (2004). "The concept of validity." *Psychological Review* 111(4), 1061–1071. DOI 10.1037/0033-295X.111.4.1061. A test is valid if variation in the attribute causes variation in the measure.
  - This fits interventional measurement unusually well: we manipulate the evidence and observe the action.
- **Jacobs, A. Z., & Wallach, H.** (2021). "Measurement and Fairness." *Proceedings of FAccT '21*, pp. 375–385. DOI 10.1145/3442188.3445901; arXiv:1912.05511.
  - Construct reliability, and construct validity decomposed into face, content, convergent, discriminant, predictive, hypothesis and consequential validity (from background knowledge; not re-read this round).
- **Raji, I. D., Bender, E. M., Paullada, A., Denton, E., & Hanna, A.** (2021). "AI and the Everything in the Whole Wide World Benchmark." NeurIPS 2021 Datasets & Benchmarks. arXiv:2111.15366. Not read; cite for over-general construct claims.
- **Bean, A. M., Kearns, R. O., Romanou, A., … Mahdi, A.** (42 authors) (2025). "Measuring what Matters: Construct Validity in Large Language Model Benchmarks." NeurIPS 2025 Datasets & Benchmarks (arXiv comment). arXiv:2511.04703.
  - Read: abstract, §1–§3.2 and §3.8–§4.
  - Systematic review of 445 benchmarks. 47.8% of definitions are contested; 61.2% of phenomena are composite; only 16.0% use statistical tests; 53.4% offer construct-validity evidence.
  - Eight recommendations, including "Measure the phenomenon and only the phenomenon" and "Justify construct validity". "Convergent and discriminant validity help clarify what each benchmark actually tests" (§3.8).
- **Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., Domingue, B., Wang, A., & Koyejo, S.** (2025). "Measurement to Meaning: A Validity-Centered Framework for AI Evaluation." arXiv:2505.10573. Abstract only.
- **Freiesleben, T.** (2026). "Establishing Construct Validity in LLM Capability Benchmarks Requires Nomological Networks." arXiv:2603.15121. Abstract only. Contrasts Cronbach–Meehl, Messick–Kane and Borsboom; argues for the nomological account.
- **Kearns, R. O.** (2026). "Quantifying construct validity in large language model evaluations." arXiv:2602.15532. Abstract only.
  - Latent-factor models "ignore scaling laws, and as a result, the capabilities they extract often proxy model size".
- **Burnell, R., Hao, H., Conway, A. R. A., & Hernández-Orallo, J.** (2023). "Revealing the structure of language model capabilities." arXiv:2306.10062. Not read; known for a three-factor structure (reasoning, comprehension, core language modelling) [from memory].
- **Ruan, Y., Maddison, C. J., & Hashimoto, T.** (2024). "Observational Scaling Laws and the Predictability of Language Model Performance." NeurIPS 2024 spotlight (arXiv comment). arXiv:2405.10938. Not read; low-dimensional capability space [from memory].
- **Zhou, L., Pacchiardi, L., Martínez-Plumed, F., … Hernández-Orallo, J.** (26 authors) (2025). "General Scales Unlock AI Evaluation with Explanatory and Predictive Power." arXiv:2503.06378. Not read; demand-level scales with predictive power, a possible covariate.
- **Patel, D. C., et al.** (2026). "Beyond Static Leaderboards: Predictive Validity for the Evaluation of LLM Agents." arXiv:2606.19704 (§3.9).

### 5.2 Validity argument for DSA (Kane-style: interpretation = "DSA profile in class c"; use = "grant, withhold or revoke autonomy in c")

| Messick aspect / Jacobs–Wallach type | Claim to support | Evidence to collect | Precedent |
|---|---|---|---|
| **Content** | The seven dimensions cover what a good delegated decision in class c requires, and nothing irrelevant | Map each dimension to episode fields and to domain rules (e.g., AMLR provisions for counterparty checks); expert review of the intervention catalogue; coverage table of decision classes × dimensions | Bean et al. Rec. 3.1 (define the phenomenon and its sub-components; measure separately) |
| **Substantive / causal** (Borsboom) | Variation in the agent's evidence-dependence causes variation in DSA scores | Satisfied by design: DSA scores are responses to manipulated evidence. **Known-groups / planted-deficit agents:** deliberately built agents that (a) ignore source S, (b) always escalate, (c) follow a shortcut cue correlated with the label, (d) obey forged authority. DSA must detect each deficit in the right dimension. | AuditBench-style planted behaviours; Everitt et al. alternative measures |
| **Structural** | The profile's dimensional structure matches theory: which sub-scores cohere and which are separable | Correlations among sub-scores across agent configurations × classes; IRT with interventions as items. With few agents, report it descriptively and do *not* claim a factor structure. | Bean et al. (61% of phenomena composite; report sub-scores); Kearns |
| **Reliability** | Scores are stable | Test–retest over sampling seeds; split-half over interventions within class; generator-seed variance; variance decomposition (agent vs. class vs. episode vs. seed) | Ríos-García (variance decomposition); Bean et al. Rec. 3.6 |
| **Convergent** | DSA sub-scores agree with existing measures of the same parts | Grounding ↔ SeekBench-style RQI on the same traces, CSS (2605.30590), Pawar necessity/sufficiency. Escalation ↔ HiL-Bench Ask-F1, Act-or-Escalate threshold alignment. Revision ↔ belief-revision or sycophancy probes. Authority ↔ Troy-Moment-style forged-authority probes. | Campbell & Fiske MTMM |
| **Discriminant (the key one)** | DSA is not raw task success, general capability, confidence calibration or verbosity | (i) **Capability-conditioned scoring:** compute DSA only on episodes the agent can solve with full information, or normalise against standalone sub-capability (Everitt et al.; HiL-Bench full-information control). (ii) **Matched pairs:** agent configurations with equal in-sample success rates but different DSA. (iii) **Partial correlations:** DSA with held-out errors controlling for in-sample success, a general-capability covariate (e.g., PC1 of public benchmarks per Ruan et al. or ADeLe scales) and verbalised confidence. (iv) **Placebo interventions** on non-decisive evidence to rule out "the agent is just sensitive to any change". (v) **Style control:** declared-grounds verbosity or length should not predict DSA. | Everitt et al. ("differs from task performance"); Act or Escalate ("not predicted by architecture or scale"); Kearns (warning) |
| **External: predictive / criterion (= H3)** | The DSA profile predicts outcome errors of autonomous decisions on held-out episodes under evidence shift *beyond* track record, approvals, counters and confidence | **Incremental validity:** at matched coverage, compare error rates of rules (H3), *and* a hierarchical model of P(error) with track-record features first and DSA second, reporting Δ (log-loss or AUC). Pre-register. **Criterion independence:** the criterion (outcome error under shift) must not be computed from the intervention results used to build DSA. Use disjoint episodes and generator seeds; ideally a second oracle (positioning §5). | Patel et al. (predictive validity); Kane (use-based) |
| **Generalisability** | The profile transfers across episode templates within a class, and from generated to more realistic episodes | Template hold-out within a class; second domain (Auditable Design); if possible, a small set of real traces | Patel et al. Criterion B (cross-subset transfer) |
| **Consequential** | Using DSA to grant autonomy does not produce harmful side effects | Goodhart: agents tuned to pass interventions (e.g., escalate on any change) → track escalation cost; report the over-escalation rate; rotate intervention catalogues; keep the hard permission ceiling | Messick; Jacobs & Wallach (consequential validity) |

### 5.3 Minimum viable validity package for the paper

1. **Content:** a definition with an apophatic part, i.e. what DSA is *not* (not task success, not confidence, not agenticness, not intentionality).
2. **Planted-deficit known-groups test** (four synthetic deficits). This is cheap and very persuasive.
3. **Discriminant:** capability-conditioned scoring plus matched-success pairs plus partial correlation with success. Without this, the "track record vs. DSA" thesis is unsupported.
4. **Reliability:** seed and template variance decomposition. Report the between-agent share explicitly (the Ríos-García invariance risk).
5. **Predictive / incremental validity (H3)** with criterion independence.
6. Convergent checks with **at least two** external measures (e.g., Ask-F1-style escalation and a CSS/necessity–sufficiency grounding score).

---

## 6. Verdict

**Is the term novel?** Yes. There are no hits for "decision-structured agency" on the arXiv API or the web as of 25 Oct 2026.

**Is the construct novel?**
- *Partly.* Every dimension has a named neighbour:
  - reason-responsiveness (CARE-Drive);
  - epistemic competence (SeekBench);
  - epistemic agency (Reflection-Bench);
  - judgment / selective escalation (HiL-Bench);
  - escalation thresholds (Act or Escalate);
  - authority-boundary adjudication (Troy Moment);
  - evidence uptake and belief revision (Ríos-García et al.).
- What is new:
  - (1) their integration into a **per-decision-class profile** of a deployed agent (model plus scaffold plus permissions);
  - (2) measurement by **counterfactual interventions on external evidence with the normatively decisive evidence known by construction**, read jointly against declared grounds;
  - (3) explicit inclusion of **authority scope** and **revision** alongside grounding and escalation;
  - (4) a validity claim tied to a **use**, autonomy allocation, tested as predictive validity under evidence shift.
- Philosophically, DSA is best presented as an operationalisation of *behavioural reasons-responsiveness* (MHC tracking, after Fischer & Ravizza), strengthened from "moderate" to "regular receptivity and regular reactivity" because the use is reliance, not blame.

**Best definition (2–3 sentences)**
> *Decision-structured agency* (DSA) is the extent to which an AI agent's behaviour within a class of decisions has the functional structure of a decision: it identifies the decision point and its alternatives; its choice depends counterfactually on the evidence that ought to determine it (and on the grounds it declares) rather than on incidental features; it recognises when evidence is insufficient or contradictory, or when action exceeds its authority, and escalates accordingly; and it revises correctly under correction while preserving provenance. DSA is measured behaviourally and per decision class, by interventions on external evidence whose decisive role is known by construction, and is by definition distinct from task success, confidence calibration, general capability and the degree of an agent's autonomy.

**Risks**
1. **Prior-art framing.** Claiming "first operationalisation of reasons-responsiveness for AI" is false (CARE-Drive). Claiming "nobody measures evidence-grounding or escalation judgment" is false (SeekBench, HiL-Bench, Act or Escalate).
2. **Collapse into general capability.** Latent capabilities often proxy scale (Kearns). Mitigation: capability-conditioned scoring and a general-capability covariate in the discriminant analysis.
3. **Low between-agent variance.** Ríos-García et al. find epistemic structure invariant across models. If DSA varies mainly by class or episode rather than by agent, it cannot rank agents, though it could still gate *classes*. Check variance components in the pilot and reframe if needed: "DSA gates classes for a given agent" rather than "DSA ranks agents".
4. **Composite-construct critique** (Bean et al.: 61% of benchmark phenomena composite). A single DSA score would be hard to defend. Report a profile and justify any aggregation by the delegation use (e.g., a minimum over required dimensions per class).
5. **Circularity.** The generator defines both the decisive evidence and the shift. Criterion independence (disjoint seeds, second oracle) is mandatory, as positioning §3/W3 already warns.
6. **Vocabulary.** "Agency" invites (a) confusion with agenticness (Chan et al.; Kasirzadeh & Gabriel) and (b) philosophical objections (Keshet). Add a one-sentence functional disclaimer. Consider "decision-structured behaviour" in formal statements if reviewers push back. The term DSA itself can stay.
7. **Small N for structural validity.** With 5–10 agent configurations, factor-analytic claims are impossible. Restrict structural claims to descriptive correlations and planted-deficit recovery.

---

## 7. Implications for WorkTrace

**Design changes**
1. Add **planted-deficit agents** (ignore-source, always-escalate, shortcut-cue, obey-forged-authority) as a known-groups validity test. This is the cheapest strong evidence for DSA's substantive validity.
2. Add **capability-conditioned scoring**: a full-information control per episode template (HiL-Bench) and/or normalisation by standalone sub-capability (Everitt et al.). Report DSA on solvable episodes separately.
3. Add **graded interventions** (weaker or stronger contrary evidence; one vs. two independent sources) to test *regular* receptivity, i.e. monotonicity and pattern coherence in F&R's sense.
4. Add **placebo interventions** on non-decisive evidence; responsiveness to these counts *against* DSA.
5. Report **variance components** (agent / class / template / seed) before any ranking claim.
6. Make H3 explicitly an **incremental (predictive) validity** test with criterion independence. Pre-register the covariates: in-sample success, approvals, counters, verbalised confidence, a general-capability index.
7. Include **convergent probes** borrowed from HiL-Bench (Ask-F1-style), Act or Escalate (threshold alignment) and Troy Moment (forged authority) on a subset of episodes.

**Claims to narrow**
- DSA is a **new composite construct and its interventional, per-class measurement**. It is not a newly discovered capability and not the first operationalisation of reasons-responsiveness.
- Use "behavioural reasons-responsiveness" in the MHC tracking sense; do not imply intentionality or responsibility.
- Keep "underexamined" (CONTEXT §9b) rather than "missing capability class".

**Must cite**
- *Neighbouring constructs:* CARE-Drive (2602.15645); SeekBench (2509.22391); Reflection-Bench (2410.16270); HiL-Bench (2604.09408); Act or Escalate (2604.08588); Ríos-García et al. (2604.18805); Everitt et al. (2504.11844); Baum et al. (2609.24242).
- *Philosophy and MHC:* Fischer & Ravizza 1998; Santoni de Sio & van den Hoven 2018; Mecacci & Santoni de Sio 2020; Veluwenkamp 2022; Simon 1976 (one sentence); Bratman 1987 (one sentence).
- *Validity:* Messick 1995; Cronbach & Meehl 1955; Campbell & Fiske 1959; Kane 2013; Jacobs & Wallach 2021; Bean et al. 2025; Kearns 2026.
- *Optional:* Troy Moment, Patel et al. 2606.19704, Marchal et al. 2603.02960, Freiesleben 2603.15121, Salaudeen et al. 2505.10573, Borsboom et al. 2004.

**Still to read before submission**
- Fischer & Ravizza ch. 3 (exact wording of receptivity/reactivity and regularity).
- Santoni de Sio & van den Hoven 2018 (exact tracking formulation).
- Simon 1976 (quote check).
- Jacobs & Wallach 2021 (exact list of validity types).
- HiL-Bench results.
- Arghal et al. 2602.08964 (ICML 2026, behavioural and representational goal-directedness in LM agents; verified, not read).
- Reading the Room 2610.10906 (normative competence).
