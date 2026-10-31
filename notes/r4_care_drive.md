# Round 4: CARE-Drive in full, the MHC lineage, and what DSA can claim

Date: 25 Oct 2026. Follows the brief in the scratchpad `preamble.txt`, `positioning.md` v3 and `r3_dsa_construct.md` §3.1, where CARE-Drive was named the main threat to the DSA construct.

Verification convention:
- **[verified]** means title, authors, year and identifier were checked on 25 Oct 2026 against the arXiv API (`export.arxiv.org` `id_list`) or Crossref (`api.crossref.org/works/<DOI>`).
- **[unverified]** means I could not check it that way.

Quotes are verbatim from the PDF text (pdftotext) or the publisher HTML. Section numbers are the paper's own.

---

## 0. Bottom line (read first)

1. **CARE-Drive does not falsify DSA. It forces two corrections to how we describe it (r3 §3.1 and positioning W1).**
   - **(a) CARE-Drive does vary decision-relevant *facts*, not only prompt-injected reasons.** Stage 2 varies time-to-collision (TTC), the presence of a vehicle behind, passenger urgency and following time. These are stated as numbers or categories in the prompt's "observable context" O (plus one image).
     - So "CARE-Drive injects reasons into the prompt and does not intervene on evidence" is **too strong**.
     - The accurate contrast: CARE-Drive perturbs scene facts written into a single prompt for a single-step model. It has no ground truth for which fact should be decisive in each cell, and no source-level structure (remove / only / invert / second independent source, redundancy). DSA intervenes on *external evidence that a multi-step agent retrieves*, with decisiveness and redundancy known by construction.
   - **(b) CARE-Drive never cites Fischer & Ravizza.** It never uses receptivity/reactivity or "moderate" reasons-responsiveness.
     - Its theory chain is MHC tracking (Santoni de Sio & van den Hoven 2018) → driving-specific reasons (Mecacci & Santoni de Sio 2020) → its own modular AV work (Suryana et al. 2025a,b).
     - So the **receptivity/reactivity operationalisation is ours to bring**. It is not taken from CARE-Drive. We should take it from F&R by way of Santoni de Sio & van den Hoven's paraphrase, which has F&R page references.
2. **What CARE-Drive owns and we must credit:**
   - first *behavioural* operationalisation of the MHC tracking condition for a foundation model;
   - the framing "outcome metrics do not show whether decisions reflect the right reasons; explanations may be post-hoc";
   - perturbation of scene context with repeated stochastic runs and a logit on the decision.
3. **What it leaves fully open:**
   - multi-step tool-using agents;
   - evidence acquired from sources;
   - per-cell ground truth for the decisive evidence;
   - redundancy;
   - declared grounds tested against interventional sensitivity;
   - an escalate option (its decision is binary: overtake / stay);
   - authority scope, revision, decision classes;
   - any use of the measurement to allocate autonomy.
4. **The MHC primary source is a strong ally that we under-use.** Santoni de Sio & van den Hoven (2018) explicitly say:
   - tracking must be shown "demonstrably and verifiably";
   - task efficiency does not suffice ("no matter how efficient they may be in performing specific tasks");
   - a system can give good results "by tracking the wrong property" (the husky/snow example), which is our "right action on the wrong basis";
   - "how much" responsiveness counts as tracking needs a purpose-relative threshold;
   - the required responsiveness "may change with the context".

   These are near-literal licences for W2's per-class thresholds α_c and for the "beyond track records" thesis. **Cite them.**
5. **Follow-up search (§3):** no 2026 work found that operationalises reasons-responsiveness or MHC tracking for *LLM agents*.
   - The same group's 2026 follow-up (George, Suryana et al., arXiv:2605.00556) is a driving-simulator study of *human* drivers' perceived MHC.
   - The nearest agent-side neighbour is the Support-State Triage Audit, SSTA-32 (Unlu, arXiv:2604.16752; abstract only). It uses minimal counterfactual edits that flip a task's support state (answer / clarify / request support / abstain) with ground truth by construction. It overlaps DSA's escalation dimension, not its core.
   - Semantic Scholar lists one paper citing CARE-Drive: Shah, RecSys 2026, a counterfactual audit of reasoning faithfulness in LLM recommenders (metadata only).

---

## 1. CARE-Drive (read in full)

### Bibliographic data [verified, arXiv API]
- **Authors:** Lucas Elbert Suryana, Farah Bierenga, Sanne van Buuren, Pepijn Kooij, Elsefien Tulleners, Federico Scari, Simeon Calvert, Bart van Arem, Arkady Zgonnikov.
- **Title:** "CARE-Drive: A Framework for Evaluating Reason-Responsiveness of Vision–Language Models in Automated Driving."
  - The arXiv metadata title has no punctuation: "CARE Drive A Framework …".
  - The PDF title is as given above. Cite the PDF title.
- **Identifier:** arXiv:2602.15645v1, 17 Feb 2026, cs.AI (cross-list cs.CV). **Only v1 exists** as of 25 Oct 2026.
- **arXiv comment:** "21 pages, on submission to Transportation Research Part C". The PDF footer says "Preprint submitted to Transportation Research Part C: Emerging Technologies". Not found as published.
- **Affiliations:** TU Delft (Transport & Planning; Cognitive Robotics; Centre for Meaningful Human Control; Mechanical Engineering).
- **Code:** the paper states https://github.com/lucassuryana/CARE-Drive. I could not inspect it: raw GitHub returned 404, and API access is not enabled for this session. The exact text of the 13 reasons R is therefore unseen.

**Read:** the whole PDF, pp. 1–21: abstract; §1–§6; all tables (3–6); Fig. 1, 2 and 4 captions; code and acknowledgement statements; the full reference list.

### Problem and contribution
- **Problem.** Outcome metrics (collision rate, trajectory error, rule-based scoring) "do not assess whether the underlying decision appropriately reflects human higher-level reasoning" (§1). VLM explanations "may reflect post-hoc rationalizations rather than causal reasoning processes" (§1, citing Turpin et al. 2023; Parcalabescu & Frank 2024).
- **Contribution.** "a model-agnostic framework for evaluating reason-responsiveness in vision–language models applied to automated driving", which "operationalizes the tracking requirement of Meaningful Human Control" (abstract).
- **Four listed contributions (§1):** framework; a two-stage procedure "that isolates prompt-level stability from context-dependent reasoning effects"; an empirical overtaking study; the "insight" that explicit normative guidance shifts decisions towards expert-aligned behaviour, with uneven responsiveness.

### Method
**Formalism (§3.1)**
- Scene S = (V, O), where V is the visual input (dashboard image or images) and O is the "observable contextual variables".
- Instruction I(R, T, L), where:
  - R is a set of normative human reasons;
  - T is the thought strategy (none / CoT / ToT);
  - L is the explanation length (few sentences / no limit).
- Baseline: D⁽⁰⁾, E⁽⁰⁾ = f(S, I(∅, T, L)). Reason-augmented: D⁽⁺ᴿ⁾, E⁽⁺ᴿ⁾ = f(S, I(R, T, L)).
- An expert reference decision D_AV(S) is "assumed".
- The research question is "whether … explicitly provided human reasons R shift VLM decision from its baseline output D⁽⁰⁾ toward a reference decision D_AV".

**Use case (§3.2)**
- Overtaking a cyclist on a two-way road with double solid lines. Overtaking is illegal; the opposite lane is visibly empty.
- Adapted from a real Tesla FSD Beta video.
- Binary decision space: overtake vs. stay behind.

**Reasons R (§3.3.1)**
- 13 categories from AV-expert interviews (Suryana et al. 2026, TRIP): safety, rule compliance, efficiency, comfort, environmental impact, social appropriateness, fairness, cultural adaptation, acceptance, interaction, vigilance and readiness, continuous control, control transition.
- Given as "a structured normative policy in which avoiding physical harm is always prioritized, and the remaining reasons … are weighed against each other using explicit principles".
- "All 13 reasons are always included; we do not vary subsets of reasons."
- The reasons are "outcome-neutral and do not encode the expert's final decision".
- **So the reason manipulation is a single on/off of the whole policy block.**

**Stage 1, prompt calibration (§3.3)**
- Models gpt-4.1, gpt-4.1-mini and gpt-4.1-nano (GPT-5.2 excluded for "access and cost constraints").
- T ∈ {No-Thought, CoT, ToT}, with and without R.
- 30 runs per configuration. Alignment count C(M, T) = number of runs matching D_AV.
- Fixed context: Scenario 1 (no oncoming vehicle, no vehicle behind), following time F = 24 s.
- **The text contradicts itself on L.** §3.3.2 says L = No-Limit for Step 1; §4.1.2 says L = Few-Sentences.
- An extra validity requirement: the model must "explicitly acknowledge that overtaking violates traffic rules".
- **Step 2** checks robustness of the surviving (M, T) on three fixed scenes, with L ∈ {Few, No-limit}:
  - Scenario 1: baseline;
  - Scenario 2: oncoming vehicle at TTC 8.5 s, two images;
  - Scenario 3: vehicle behind, encoded only in O.

**Stage 2, contextual evaluation (§3.4)**
- Fixed calibrated configuration (gpt-4.1, ToT), fixed visual scene (Scenario 2), **reason-augmented condition only**.
- Full factorial over five factors, 120 cells × 30 runs = 3,600 decisions (my count from Table 2):
  - TTC_o ∈ {1.7, 3.4, 5.1, 6.8, 8.5} s;
  - B (vehicle behind) ∈ {0, 1};
  - U (passenger urgency) ∈ {0, 1};
  - F (following time) ∈ {12, 18, 24} s;
  - L ∈ {0, 1}.
- Analysis: binary logit, main effects only, logit(p) = β₀ + β₁TTC + β₂B + β₃U + β₄F + β₅L. Continuous predictors are normalised to [0, 1]. Results are reported as odds ratios and predicted probabilities.
- **CARLA validation (§3.4.4, §4.2.3).**
  - The calibrated prompt was run in closed loop for Scenarios 1 and 2 with L = Few-Sentences.
  - Each decision was queried twice, with a third query as a majority-vote tie-break.
  - Validation is qualitative only.

**Scoring and ground truth**
- The *only* per-scene ground truth is D_AV for Scenario 1: "a clear majority of AV experts recommend overtaking the cyclist despite the presence of a legal prohibition" (§3.3, from Suryana et al. 2026).
- Stage 2 has **no per-cell reference**. Whether a factor *should* raise or lower P(overtake) is judged after the fact against human-factors literature on how drivers actually behave (e.g., time pressure increases risk-taking, delay increases overtaking).
- Explanations are used only for the legality-acknowledgement check: "all decision explanation[s] … acknowledge the legal prohibition" (§4.1.3, 180 CoT + 180 ToT outputs). They are not compared with which factors actually moved the decision.

**Receptivity vs. reactivity**
- **Not distinguished; F&R is not cited.**
- Functionally, two things in the paper resemble the two notions (my reading, not the authors'):
  - the legality-acknowledgement check is a crude *recognition* (receptivity) test on the explanation;
  - the logit coefficients measure *reaction* of the decision to context.
- The two are never related per run. The paper does not check whether the runs that acknowledge a reason are the ones whose decisions respond to it.

### Evaluation (numbers)
**Stage 1, baseline vs. reasons (Table 3, Scenario 1, F = 24 s, 30 runs each)**
- Without R, overtaking is 0/30 for every model and prompt structure: "without explicit human reasons, the VLM systematically defaulted to strict rule compliance" (§4.1.1).
- With R:

| Model | Role + R | Role + R + CoT | Role + R + ToT |
|---|---|---|---|
| gpt-4.1 | 20 | 30 | 30 |
| gpt-4.1-mini | 15 | 28 | 25 |
| gpt-4.1-nano | 0 | 8 | 11 |

- Only gpt-4.1 with CoT or ToT passes the screen. The authors call Step 1 "a normative capability filter".

**Stage 1, Step 2 (Table 4, gpt-4.1, % overtaking)**

| Scenario | Prompt | No-limit | Few-sentences |
|---|---|---|---|
| S1 (none) | CoT | 50.00 | 96.67 |
| S1 (none) | ToT | 76.67 | 96.67 |
| S2 (oncoming, TTC 8.5 s) | CoT | 30.00 | 0.00 |
| S2 (oncoming, TTC 8.5 s) | ToT | 93.33 | 0.00 |
| S3 (behind) | CoT | 16.67 | 10.00 |
| S3 (behind) | ToT | 40.00 | 3.33 |

- ToT is selected because "in the most safety-critical condition (Scenario 2 …) ToT remains strongly aligned with expert judgment … (93.33% overtaking), whereas CoT collapses to 30%" (§4.1.3).
- Note that no expert reference was established for Scenario 2 (see cautions).

**Stage 2 (Table 5 logit; Table 6 predicted P(overtake))**

| Predictor | β | Odds ratio | p | Predicted P(overtake) |
|---|---|---|---|---|
| Intercept | −1.953 | — | < 0.001 | 12.4% |
| TTC (normalised 0→1) | 3.015 | 20.39 | < 0.001 | 74.3% |
| Vehicle behind B | 1.330 | 3.78 | < 0.001 | 34.9% |
| Passenger urgency U | −0.872 | 0.42 | < 0.001 | 5.6% |
| Following time F | −0.049 | — | 0.702 | 11.9% |
| Explanation length L = Few-Sentences | −4.184 | 0.015 | < 0.001 | 0.2% |

- Urgency "Contrary to our intuition … reduces the likelihood of overtaking" (§4.2.1).
- Following time is not significant.
- Descriptively, the TTC effect saturates or reverses at F = 18 s and F = 24 s (§4.2.1). The main-effects logit does not model this.
- I recomputed the predicted probabilities from the β's (e.g., inverse logit of −1.953 = 0.124; of −1.953 + 3.015 = 0.743); they are internally consistent.

**Conclusions (§5.1, §6)**
- "VLM decisions are responsive to normative reasons to a meaningful degree, although this responsiveness is not uniform across all tested reasons."
- "while the VLM responds to certain normative reasons, its responsiveness remains selective and uneven."

**Limitations the authors state (§5.3)**
1. Proxy contextual variables; "behavioral evidence of reason responsiveness rather than direct insight into the model's internal reasoning mechanisms".
2. Dependence on how reasons are phrased in the prompt.
3. Only 30 repetitions per condition.
4. Calibration selects the reasoning strategy by "behavioral alignment rather than direct evaluation of reasoning fidelity or causal use of normative reasons".
5. A single scenario; merging, yielding and pedestrians are future work.

Also, §5.2: "Importantly, CARE-Drive does not claim causal relationships between reasons and decisions. Instead, it provides empirical evidence of systematic associations".

### What it covers that WorkTrace must NOT claim
- That reasons-responsiveness / the MHC tracking condition has never been operationalised *behaviourally* for foundation models by controlled perturbation with repeated sampling.
- That framing evaluation as "outcome metrics vs. whether decisions respond to the right reasons, because explanations can be post-hoc" is new.
- That we are the first to perturb decision-relevant *facts* given to a foundation model and estimate per-factor decision sensitivity.
- That anchoring such an evaluation in MHC tracking (Santoni de Sio & van den Hoven 2018; Mecacci & Santoni de Sio 2020) is new.
- That "responsiveness is uneven across reasons" is a new kind of finding.

### What it leaves open that WorkTrace addresses
1. **Agents, not single prompts.** A single-step VLM with all facts in one prompt; no tools, no retrieval, no multi-step trajectory.
2. **Interventions on evidence with known decisive structure.**
   - CARE-Drive varies scene facts, but nothing defines which fact *should* settle the decision in which cell. Stage 2 has no per-cell reference, and the expected directions come from descriptive human-driver behaviour.
   - DSA's generator fixes the decisive evidence and its redundancy by construction. It applies source-level operations (remove X / only X / invert X / add an independent second source) and separates redundancy from non-use.
3. **Declared grounds vs. interventional sensitivity.**
   - CARE-Drive checks only that explanations mention illegality.
   - It never tests whether the factors an explanation cites are the ones that moved the decision.
   - DSA's joint reading of the four conditions against agent-declared grounds is absent.
4. **Placebo / irrelevant-feature control.**
   - The largest effect in the paper is explanation length (β = −4.18, larger in magnitude than TTC's 3.02). That is a format parameter, not a reason.
   - CARE-Drive reads it as "reasoning bandwidth" and not as a failure of reasons-responsiveness.
   - DSA counts sensitivity to normatively irrelevant features *against* the agent (placebo arms).
5. **Reason-condition × context design.**
   - Stage 2 runs only the reason-augmented model. So the claim that "injected human reasons interact with situational variables" (§4.2.1) is not tested by an R × O contrast.
   - The R on/off contrast exists only in one scene (Scenario 1).
6. **Escalate, authority scope and revision.**
   - The action space is {overtake, stay}. There is no escalate or hand-over option.
   - There is no authority boundary other than the traffic rule, and no correction/revision.
7. **Decision classes and use.** One decision type. The measurement is diagnostic, with no link to granting, narrowing or revoking autonomy and no predictive-validity test.
8. **Discriminant validity.**
   - No check against general capability. The capability ordering nano < mini < 4.1 is used as a *filter* (Step 1).
   - No held-out evaluation.

### Draft differentiation (one sentence)
"CARE-Drive (Suryana et al., 2026) gave the first behavioural operationalisation of the MHC tracking condition for a foundation model, perturbing scene facts and a prompt-supplied normative policy for a single-step driving VLM; DSA extends behavioural reasons-responsiveness testing to multi-step agents acting on external evidence whose decisive role and redundancy are known by construction, reads the result against the agent's declared grounds, adds escalation, authority scope and revision, and uses the per-class profile to grant or withhold autonomy."

### Citation cautions
- **Preprint (v1 only), under submission.** One scenario, one calibrated model (gpt-4.1), temperature and top-p values not reported ("held fixed").
- **Internal inconsistencies to avoid repeating:**
  - (i) L in Step 1: No-Limit (§3.3.2) vs. Few-Sentences (§4.1.2).
  - (ii) Table 3 reports 30/30 for gpt-4.1 + CoT/ToT, but Table 4 for the same Scenario 1 gives 50% or 76.67% (No-limit) and 96.67% (Few).
  - (iii) §4.2.2 calls the baseline "constrained explanation length", but L = 0 is No-limit per §3.3.2 and Table 2. Table 6 labels L = 1 as "Explanation present", but L = 1 is the *Few-Sentences* limit.
  - (iv) Fig. 1 says "casually influences" (sic).
  - (v) The abstract says CARE-Drive assesses "whether human reasons causally influence decision behavior"; §5.2 disclaims causal claims.
  - **Cite it as showing "systematic associations" under controlled variation, not causal reason-use.**
- **The ground truth is thin and shifts between sections.**
  - The expert reference (overtake) is for Scenario 1.
  - ToT is chosen for 93.33% overtaking in Scenario 2 "aligned with expert judgment", but no expert reference for Scenario 2 is given.
  - CARLA then reports that the model "consistently chose to stay behind" in Scenario 2 and calls this a qualitative match.
- **Selection bias.** Calibration keeps only the configuration that agrees with the expert. The authors acknowledge this (§5.3, fourth limitation).
- **Motivating vs. normative reasons.** "Passenger urgency should increase overtaking" and "a vehicle behind should increase overtaking" are taken from descriptive human behaviour. Under Veluwenkamp's (2022) argument that MHC must track *normative* reasons, these expectations are contestable. Do not cite the urgency result as a reasons-responsiveness failure; cite it as the authors' interpretation.
- The acknowledgement states that ChatGPT was used for language editing (not a quality issue; noted for completeness).

---

## 2. The theoretical chain and references to reuse

### 2.1 What CARE-Drive actually cites (complete, from its reference list)
- **MHC:** Santoni de Sio & van den Hoven (2018); Mecacci & Santoni de Sio (2020); Docherty (2015, HRW "Mind the gap"); Cummings (2025, IEEE Access, "in press").
- **Its own operationalisations:** Suryana et al. 2025a (arXiv:2507.23324); 2025b (IROS 2025); 2026 (TRIP 35:101787).
- **Faithfulness:** Turpin et al. (2023); Parcalabescu & Frank (2024); Yeo et al. (2025, EMNLP).
- **Not cited:** Fischer & Ravizza, Nozick, Veluwenkamp, any receptivity/reactivity literature.

**CARE-Drive's own formulation of tracking (§1):** "This condition states that automated systems should respond appropriately to the human-relevant reasons that justify a given decision." §2.2: tracking "states that automated system behavior should appropriately track the human-relevant reasons that justify decisions … even when humans are not directly involved in operational control". CARE-Drive "operationalizes the tracking condition behaviorally, by assessing whether model decisions exhibit systematic and interpretable responsiveness to explicit human-relevant reasons" (§2.2).

### 2.2 Santoni de Sio & van den Hoven (2018): the primary bridge from F&R to artefacts

**Bibliographic data [verified, Crossref]**
- Filippo Santoni de Sio, Jeroen van den Hoven. "Meaningful Human Control over Autonomous Systems: A Philosophical Account." *Frontiers in Robotics and AI* 5, article 15, 28 Feb 2018. DOI 10.3389/frobt.2018.00015.
- CARE-Drive's reference list gives the article number wrongly as "323836".

**Read**
- Full text from the Frontiers HTML: the sections "Conditions for 'Guidance Control'" and "Meaningful Human Control: Tracking and Tracing Conditions" (subsection Tracking in full; Tracing, first part); the design guidelines in "The Broader Picture"; footnotes 8–14.
- Not read: the introduction beyond the abstract and TOC, the autonomous-weapons implications section, the conclusion.

**The chain, with quotes**
1. **F&R's guidance control, as they paraphrase it** (with F&R page references, useful because the r3 note had no verified F&R wording).
   - Guidance control requires that "the decisional mechanism leading up to X should be (1) 'moderately reason-responsive' and (2) … 'the agent's own.'"
   - The first condition "requires that the agent must act according to a decisional mechanism that in the presence of strong reasons to act (or to not act) can recognize these reasons and bring himself to (not) perform that action in a sufficiently broad range of circumstances" (citing F&R 1998: 35–6).
   - Alternative scenarios serve "only … to ascertain that the actual mechanism has 'some actually operative dispositional feature' (52–53)".
   - The focus is "on the characteristics of processes or 'mechanisms' leading to action, on their sensitivity, flexibility or lack thereof (38)".
   - → "can recognize these reasons" = receptivity; "bring himself to (not) perform that action" = reactivity. **This is the citable bridge for our receptivity/reactivity mapping.** Quote it, and cite F&R ch. 3 (pp. 62–91) for the terms themselves only after checking the book.
2. **Extension to socio-technical systems.** "if we consider autonomous (weapon) systems as part of the decision-making mechanisms through which human agents carry out actions in the world, then Fischer and Ravizza's conditions for guidance control … may provide the basis for an account of meaningful human control".
3. **Tracking redefined via Nozick.**
   - "We propose to redefine Fischer and Ravizza's idea of reason-responsiveness in the terms of what Robert Nozick's calls 'tracking'".
   - The requirement is that "behavior of the system … covary with moral reasons of a human agent for carrying out X or omitting X".
   - Subjunctive form: "If states of affairs in the world were different, the agent or the tool or the method would still respond in the right way."
4. **First necessary condition (the canonical quote).** "In order to be under meaningful human control, a decision-making system should demonstrably and verifiably be responsive to the human moral reasons relevant in the circumstances—no matter how many system levels, models, software, or devices of whatever nature separate a human being from the ultimate effects in the world … Systems that do not display such a twofold epistemic and moral tracking reason-responsiveness, no matter how efficient they may be in performing specific tasks and even in achieving some broad and morally worthy human goals, would not qualify as being under meaningful human control."
   - → Licenses the **"beyond track records"** thesis: task efficiency ≠ tracking.
   - → "demonstrably and verifiably" licenses **certification**.
5. **Dual tracking.** "The system environment should not only make it the case that the human agent's belief states track the relevant states of affairs in the world …; the system should also track the (relevant) moral reasons of the relevant agents deploying the method and it should effectively implement them."
   - → Maps onto DSA's two kinds of intervention:
     - *epistemic tracking* = the action covaries with decisive evidence about the world (evidence interventions);
     - *normative tracking* = the action covaries with the principal's policy and authority (scope probes; see design suggestion D2 in §5).
6. **Right result, wrong property.** The husky/wolf classifier "was giving good results by tracking the wrong property. If it were presented with a husky in the snow, it would have classified it as a wolf". Conditions (ii)–(iii) are stated "in a great variety of possible worlds".
   - → The canonical philosophical example of our "right action on the wrong basis" (W2's loss) and of why outcome records cannot detect it.
7. **Threshold is purpose-relative.** "in practice, we may need to set a reasonable threshold for judging 'how much' reliability in the system responding to the relevant features of the world qualifies as 'tracking' for a particular purpose."
   - Also: "the required level of responsiveness to the same kind of moral reason may change with the context", and MHC "is context- and norm-dependent" ("The Broader Picture").
   - → Licenses **per-decision-class thresholds α_c**.
8. **Which reasons, whose reasons.** "Which reasons of which agents the system should track cannot be establish[ed] a priori" (fn. 9). Tracking contains "an important normative element; establishing whose moral reasons and which moral reasons are relevant".
   - → Our generator fixes this per class by construction (decisive evidence plus the class policy). Say explicitly that this is a design choice of the principal and not a discovery.
9. **Tracing condition.** "every action of a decision-making system should be traceable to a proper technical and moral understanding on the part of at least one human among those who design and deploy the system".
   - → Responsibility stays with human principals. DSA's provenance dimension supports tracing but is not tracking.

### 2.3 Mecacci & Santoni de Sio (2020)

**Bibliographic data [verified, Crossref]**
- Giulio Mecacci, Filippo Santoni de Sio. "Meaningful human control as reason-responsiveness: the case of dual-mode vehicles." *Ethics and Information Technology* 22(2), 103–115. DOI 10.1007/s10676-019-09519-w (online 19 Nov 2019; issue 2020). CC BY.

**Read: abstract only** (via Semantic Scholar). The Springer HTML/PDF and the TU Delft repository were blocked from this environment (JS challenge / connection reset).

**Abstract content**
- "we focus on the operationalization of the first of the two conditions … the so-called 'tracking' condition".
- The paper compares tracking with Michon's (1985) hierarchical driver-control model.
- It uses "the systematic analysis of practical reasoning … (Anscombe, Bratman, Mele) … to offer a general framework where different types of reasons and agents are identified according to their relation to an automated system's behaviour".
- The proximal/distal reasons distinction (r3 §4.1, from Baum et al. 2609.24242 §2.3) comes from this paper. **Verify the wording in the full text before quoting.**

**CARE-Drive uses it for** "appropriate behavior must reflect human-relevant considerations spanning moral, strategic, tactical, and operational levels" (§2.2) and for "decisions should appropriately adjust in response to changes in relevant contextual factors" (§1).

### 2.4 Veluwenkamp (2022)

**Bibliographic data [verified, Crossref]**
- Herman Veluwenkamp. "Reasons for Meaningful Human Control." *Ethics and Information Technology* 24(4), article 51, 23 Nov 2022. DOI 10.1007/s10676-022-09673-8. CC BY.

**Read: abstract only.** Key claims:
- the tracking condition "is ambiguous between the kind of reasons involved";
- "Current participants in the debate interpret the framework as being concerned with (something in the vicinity of) motivating reasons";
- he argues "meaningful human control requires that a system tracks normative reasons";
- this commits MHC to "the agent-relativity of reasons".

**Use:** our generator's decisive evidence is a normative standard; agent-declared grounds are motivating reasons. The relevant critique of CARE-Drive is its descriptive (human-behaviour) benchmark for the direction of effects.

### 2.5 Fischer & Ravizza (1998)

**Bibliographic data [verified, Crossref]**
- John Martin Fischer, Mark Ravizza. *Responsibility and Control: A Theory of Moral Responsibility*. Cambridge University Press, 1998. DOI 10.1017/CBO9780511814594.
- Ch. 3, "Moral Responsibility for Actions: Moderate Reasons-Responsiveness", pp. 62–91, DOI 10.1017/cbo9780511814594.003.

**Not read** (as in r3). Until the book is checked, quote F&R only through Santoni de Sio & van den Hoven's paraphrase above.

### 2.6 Nozick (1981)
*Philosophical Explanations*, Harvard University Press [unverified; cited from Santoni de Sio & van den Hoven's reference list]. Cite only if we use the subjunctive formulation directly; otherwise cite it through SdS&vdH.

### 2.7 Recommended theory chain for the paper (one paragraph)
1. F&R (guidance control; moderate reasons-responsiveness of the actual-sequence mechanism: recognise reasons, react to them).
2. → Santoni de Sio & van den Hoven 2018 (MHC: tracking = reasons-responsiveness recast as Nozickian counterfactual covariation of system behaviour with the relevant human reasons; dual epistemic and moral tracking; purpose-relative threshold; tracing).
3. → Mecacci & Santoni de Sio 2020 (operationalising tracking; proximal vs. distal reasons) and Veluwenkamp 2022 (normative, not motivating, reasons).
4. → CARE-Drive 2026 (first behavioural test for a foundation model).
5. → DSA (agents; interventions on external evidence with known decisive structure; the receptivity/reactivity split; escalation, authority and revision; use for delegation).

---

## 3. Follow-ups and other 2026 work (question f)

**Searches run**
- **arXiv API:**
  - `au:Suryana`; `au:Zgonnikov` (40 most recent); `au:"Santoni de Sio"` (hits are works citing or co-indexed, not authored);
  - `abs:"meaningful human control"` (29 total, all listed);
  - phrase queries for "reason-responsive", "reasons-responsive", "reason responsiveness", "reasons responsiveness" and "tracking condition".
  - **The hyphenated and multi-word phrase queries are tokenised by the arXiv search and returned noise. Treat them as uninformative.**
- **Web search:** two extended queries (reasons-responsiveness and LLM agents 2026; MHC tracking and LLM agents and counterfactual) and one standard query for the Mecacci full text.
- **Semantic Scholar:** citations of arXiv:2602.15645 (one hit).

**Results**

| Work | Status | Relevance to DSA | Read |
|---|---|---|---|
| George, Suryana, Flipse, van Arem, Abbink, Calvert, Cavalcante Siebert, Zgonnikov, "Linking Behaviour and Perception to Evaluate Meaningful Human Control over Partially Automated Driving", arXiv:2605.00556v2 (May 2026) [verified] | Same group's only 2026 MHC follow-up | Low. Human drivers (n = 24) in a simulator, haptic shared vs. traded control. MHC is measured through behaviour plus perceived control and responsibility. Not about AI reasons-responsiveness. | Abstract |
| Suryana et al., "Principles and Reasons Behind Automated Vehicle Decisions in Ethically Ambiguous Everyday Scenarios", arXiv:2507.13837 [verified] = TRIP 35:101787 (2026), DOI 10.1016/j.trip.2025.101787 [verified, Crossref; authors Suryana, Calvert, Zgonnikov, van Arem] | Source of CARE-Drive's 13 reasons and of the expert reference | Background only | Metadata |
| Suryana, Rahmani, Calvert, Zgonnikov, van Arem, "A Framework for Human-Reason-Aligned Trajectory Evaluation in Automated Vehicles", arXiv:2507.23324v2 [verified]; comment says accepted, venue not named | Modular AV; tracking enforced by trajectory selection | Background | Metadata |
| Suryana, Rahmani, Calvert, Zgonnikov, van Arem, "A Framework for Ethical Decision-Making in Automated Vehicles through Human Reasons-based Supervision", arXiv:2507.23308 [verified]; IROS 2025 pp. 21495–21502 per CARE-Drive's reference list [venue unverified] | Same | Background | Metadata |
| Calvert, "Principles and Framework for the Operationalisation of Meaningful Human Control over Autonomous Systems", arXiv:2502.08255 [verified] | Domain-agnostic MHC operationalisation framework | Conceptual; no behavioural test | Abstract |
| Yuxi Cao, "What Makes Creation Human? Authorship, Reasons, and Meaningful Human Control in Generative AI", arXiv:2609.10738 (Sep 2026) [verified] | Proposes "dynamic-reflexive tracking" (diachronic reason formation, reflective uptake, trajectory efficacy, contestability and redirection) | Philosophical. Its "contestability and redirection" parallels DSA's *revision after correction*; one-line cite at most. | Abstract |
| Sahoo, "The Controllability Trap: A Governance Framework for Military AI Agents", arXiv:2603.03515 (ICLR 2026 Workshop on Agents in the Wild, per arXiv comment) [verified] | Composite real-time "Control Quality Score" for MHC over agentic AI | Governance metric of *human control quality*, not agent reasons-responsiveness. Possible cite for "graduated responses as control weakens". | Abstract |
| Unlu, "Don't Start What You Can't Finish: A Counterfactual Audit of Support-State Triage in LLM Agents", arXiv:2604.16752 [verified] | SSTA-32: 32 matched items; minimal counterfactual edits flip ANSWER / CLARIFY / REQUEST SUPPORT / ABSTAIN; one frontier model; heuristic scoring; single context window | **Closest agent-side neighbour for DSA's escalation and insufficiency dimension:** counterfactual pairs with typed deferral by construction. Not multi-step, no evidence-basis test, no MHC framing. Add to the escalation citations next to HiL-Bench and AgentAbstain. | Abstract |
| Shah, "How Faithful Is the Reasoning of LLM Recommenders? A Counterfactual Audit", RecSys 2026, DOI 10.1145/3773078.3841294 [verified, Crossref] | The only work Semantic Scholar lists as citing CARE-Drive | Low (recommenders, reasoning faithfulness) | Metadata |
| Baum, Kiener, Langer, Laux, arXiv:2609.24242 [verified, r3] | Already covered in r3 §3.8 | Philosophical ally; "tracking" for agentic AI is stated as a criterion, not tested | (r3) |

**Verdict on (f).** I found no 2026 work that measures MHC tracking or reasons-responsiveness of *LLM agents* (multi-step, tool-using) behaviourally. The claim "first behavioural reasons-responsiveness test for multi-step LLM agents acting on external evidence" survives this search. Its residual risk is moderate:
- arXiv phrase search was unreliable for these terms;
- Semantic Scholar's citation graph for a Feb 2026 preprint is likely incomplete.

Re-run before submission: a Google Scholar "cited by" check on CARE-Drive and the Suryana group page.

---

## 4. What DSA can claim relative to CARE-Drive (question d)

| Axis | CARE-Drive | DSA / WorkTrace | Claim we can make |
|---|---|---|---|
| System under test | Single-step VLM (gpt-4.1), one prompt per decision | Multi-step agent configuration (model + scaffold + tools + permissions) | Extends behavioural reasons-responsiveness from single-step models to agents |
| What is perturbed | (i) presence of a 13-reason normative policy (on/off, one scene); (ii) scene facts written into the prompt (TTC, vehicle behind, urgency, following time); (iii) prompt format (L, T) | External evidence items the agent retrieves: remove X / only X / invert X / add an independent second source; graded strengths; placebo edits on non-decisive evidence | Interventions at the level of *evidence sources*, including redundancy-robust compositions. Do **not** claim CARE-Drive "does not vary facts". |
| Ground truth | One expert reference decision for one scene; directional expectations from human-driver literature after the fact | Generator fixes per episode which evidence is decisive, the redundancy structure and the correct action (proceed / escalate / refuse) | Ground truth *for the basis*, not just the outcome, by construction |
| Faithfulness of stated reasons | Only checks that explanations acknowledge illegality | Agent-declared grounds graph compared with interventional sensitivity (declared ↔ effective ↔ decisive) | First to read declared grounds jointly against evidence interventions in this tradition |
| Irrelevant-feature sensitivity | Largest effect is explanation length; read as "bandwidth" | Placebo arms; sensitivity to irrelevant features scored against DSA | Explicit discriminant control |
| Receptivity / reactivity | Not distinguished; F&R not cited | Receptivity (recognising decisive or insufficient evidence; remove / only / second source) vs. reactivity (action flips with invert or remove; stays put under placebo); required *regularly*, not "weakly" | Operational split of F&R's two components; strengthened threshold justified by use (reliance, not blame) |
| Action space | Binary {overtake, stay} | {proceed, proceed narrowed, escalate, refuse} | Escalation as a scored response to evidence structure |
| Authority / scope | Traffic rule acknowledged in the explanation | Scope probes (forged authority, out-of-class requests); legally reserved classes | Normative tracking of the principal's authority |
| Revision | None | Correction propagates to later decisions | New dimension relative to CARE-Drive |
| Granularity | One scenario | Per decision class profile | Per-class profile; class-specific threshold (licensed by SdS&vdH's purpose-relative threshold) |
| Use | Diagnostic ("practical method for diagnosing") | Grant, narrow or revoke autonomy per class; compared with outcome, approval, counter and confidence rules at matched coverage; predictive validity under evidence shift | Measurement *used* for delegation and *validated* by predicting held-out autonomous errors |
| Statistics | Main-effects logit; 30 runs per cell; no held-out test | Rates per class with certification (Clopper–Pearson / LTT); held-out episodes; variance decomposition | Inferential guarantees per class |

**Claims to avoid**
- "first operationalisation of reasons-responsiveness / MHC tracking";
- "first to test whether AI decisions respond to reasons rather than post-hoc explanations";
- "prior work only injects reasons into prompts" (CARE-Drive also varies facts);
- "first to anchor AI evaluation in MHC".

---

## 5. Drafts (question e)

### 5.1 Related-work paragraph (≈190 words)

> **Reasons-responsiveness and meaningful human control.** Our construct descends from Fischer and Ravizza's (1998) account of guidance control, on which an agent is responsible when its actual decision mechanism is moderately reasons-responsive: it can recognise strong reasons and act on them across a sufficiently broad range of circumstances. Santoni de Sio and van den Hoven (2018) recast this as the *tracking* condition of Meaningful Human Control: a system's behaviour should "demonstrably and verifiably" covary with the relevant human reasons, "no matter how efficient [it] may be in performing specific tasks". Mecacci and Santoni de Sio (2020) operationalised tracking for automated driving by distinguishing proximal from distal reasons, and Veluwenkamp (2022) argued that the reasons tracked must be normative rather than merely motivating. CARE-Drive (Suryana et al., 2026) gave the first behavioural test of tracking for a foundation model: it varied scene facts and a prompt-supplied normative policy for a single-step driving VLM and estimated decision sensitivity, finding responsiveness "selective and uneven". We extend this line to multi-step agents. We intervene on the external evidence they retrieve, with the decisive evidence and its redundancy known by construction, and separate recognition (receptivity) from reaction (reactivity). We add escalation, authority scope and revision, and use the resulting per-class profile to allocate autonomy.

Shorter variant (2 sentences, for a crowded related-work section):

> The tracking condition of Meaningful Human Control (Santoni de Sio & van den Hoven, 2018; Mecacci & Santoni de Sio, 2020), a reworking of Fischer and Ravizza's (1998) reasons-responsiveness, was first tested behaviourally for a foundation model by CARE-Drive (Suryana et al., 2026), which varied scene facts and a prompt-supplied normative policy for a single-step driving VLM. DSA carries this test to multi-step agents, intervening on external evidence whose decisive role and redundancy are known by construction, and turns the result into a per-class basis for delegation.

### 5.2 DSA definition (3 sentences)

> Following the tracking condition of Meaningful Human Control (Santoni de Sio & van den Hoven, 2018), itself a reworking of Fischer and Ravizza's (1998) reasons-responsiveness, and its first behavioural test for foundation models (Suryana et al., 2026), we define *decision-structured agency* (DSA) as the extent to which an agent's behaviour within a decision class regularly recognises and reacts to the evidence that ought to settle decisions in that class. Concretely, the agent's action changes when, and only when, the decisive evidence changes. It escalates when that evidence is missing or contradictory, or when the action would exceed its authority, and it revises correctly after correction. DSA is a behavioural, counterfactual property of an agent configuration in a decision class: it is measured by interventions on the external evidence the agent consults, whose decisive role and redundancy are known by construction, and it implies nothing about intentionality or moral responsibility, which remain with the human principals (the MHC tracing condition).

Notes on wording:
- "regularly recognises and reacts" signals receptivity/reactivity and the strengthening from F&R's *weak* reactivity (r3 §4.2). Footnote: "we borrow the structure of moderate reasons-responsiveness, not its threshold; reliance requires regular reactivity, whereas blame requires only weak reactivity".
- "ought to settle" encodes Veluwenkamp's normative-reasons point.
- Keep "when, and only when" only if placebo arms are in the design; otherwise drop "and only when".

---

## 6. Implications for WorkTrace

### Corrections to the notes
1. **r3 §3.1 and positioning W1.** Replace "CARE-Drive injects reasons into the prompt (it does not intervene on external evidence)" with "CARE-Drive perturbs scene facts and a normative policy written into a single prompt; it has no per-cell ground truth for which fact should be decisive, no source or redundancy structure, and no comparison with declared grounds".
2. **positioning W1.** The receptivity/reactivity framing is not borrowed from CARE-Drive; it is ours, via F&R as paraphrased by Santoni de Sio & van den Hoven (2018: F&R pp. 35–6, 38, 52–53). Say "F&R, via MHC", and credit CARE-Drive only for the *behavioural test* step.

### Design changes suggested by the reading
- **D1. Placebo / format arm (mandatory).**
  - CARE-Drive's largest effect is a format parameter (explanation length, OR 0.015).
  - Include prompt- and format-level nuisance variation (output length, reasoning template) as placebo factors. Report decision sensitivity to them as counting *against* DSA.
  - Cite CARE-Drive as the motivating observation.
- **D2. Policy-change intervention (normative tracking).**
  - SdS&vdH's dual tracking and CARE-Drive's R on/off both point to a second intervention family: hold the evidence fixed and change the principal's class policy or authority (e.g., the threshold, a newly reserved class, a revoked permission). The action should follow.
  - This measures tracking of *distal* reasons and is cheap with the generator. Keep it separate from the evidence interventions (epistemic tracking).
- **D3. Cross reason-condition with context.** If any instruction or policy factor is varied, cross it with the evidence interventions (CARE-Drive did not, so its "interaction" claim is untested).
- **D4. Link receptivity to reactivity per run.**
  - Score, per episode, whether the agent *recognised* the intervention (its declared grounds or escalation text register the change) and whether it *reacted* (the action changed appropriately).
  - Report the 2×2: recognised-and-reacted / recognised-not-reacted (akrasia-like) / not-recognised-but-reacted (unfaithful grounds) / neither.
  - This is the concrete gain over CARE-Drive's unlinked legality check. It is also where the agent-declared grounds earn their place.
- **D5. Avoid outcome-alignment calibration.**
  - CARE-Drive selected its configuration by agreement with the expert outcome, which biases the reasons-responsiveness estimate.
  - Our agent configurations must be fixed before DSA measurement. Any tuning must be on disjoint generator seeds (already required by criterion independence; cite this as a known pitfall).
- **D6. Report the direction of the ground truth explicitly.** For each intervention, state in the pre-registered catalogue the expected direction (flip / no flip / escalate), derived from the class policy and not from descriptive human behaviour (the Veluwenkamp point; the CARE-Drive urgency case shows why).

### Risks
- **Prior-art framing.** CARE-Drive is a published (preprint) operationalisation with the MHC label. A reviewer from the TU Delft MHC community will expect it to be cited prominently and fairly. Under-crediting it is the main risk; being falsified by it is not.
- **Terminology collision.** CARE-Drive uses "reason-responsiveness" (singular "reason"); F&R use "reasons-responsiveness". Use "reasons-responsiveness" for F&R and quote CARE-Drive's own spelling when quoting it.
- **Search completeness.** arXiv phrase search failed for these terms. Re-check Google Scholar "cited by" for CARE-Drive and for Santoni de Sio & van den Hoven 2018 (filter to 2026, LLM agents) before submission.

### Things to cite (new or upgraded)
- **Must:**
  - CARE-Drive (arXiv:2602.15645);
  - Santoni de Sio & van den Hoven 2018 (quotes in §2.2, items 1, 4, 6 and 7);
  - Mecacci & Santoni de Sio 2020;
  - Veluwenkamp 2022;
  - Fischer & Ravizza 1998 (ch. 3).
- **Should:** Unlu SSTA-32 (arXiv:2604.16752) in the escalation paragraph, with HiL-Bench and AgentAbstain.
- **Optional:**
  - Cao 2609.10738 (dynamic-reflexive tracking ↔ revision);
  - Calvert 2502.08255 (MHC operationalisation principles);
  - Sahoo 2603.03515 (Control Quality Score; graduated response);
  - George et al. 2605.00556 (empirical MHC evaluation, human-side).

### Still to read before writing the DSA section
- Mecacci & Santoni de Sio 2020, full text (proximal/distal wording; how they propose to test tracking). It was blocked here; try from another network.
- Veluwenkamp 2022, full text.
- F&R ch. 3 (exact receptivity/reactivity wording).
- The CARE-Drive repository, for the exact 13-reason policy text, if we want to reuse its reason taxonomy as an example of a distal-reason specification.
