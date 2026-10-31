# Round 3: the closest neighbours to W2 (interventions on an agent's external evidence)

Date: 2026-10-25. Scope: full reads of Liao (2607.20827), Turk "Causal Sensitivity Score" (2605.30590) and Yang et al. "Spurious Tool Use" (2609.16268); a design re-check of Pawar et al. (2609.05385); and a targeted 2026 search for "add a corroborating / independent source" and "source redundancy" interventions on LLM agents and RAG.

Prerequisites read first: `notes/positioning.md` (v2) and `notes/r2_faithfulness_interventions.md`.

---

## Headline: what threatens W2 (read this first)

1. **"Add an independent second source" is no longer unoccupied as an intervention.** Between July and October 2026, several preprints vary the number of *independent* sources while holding the evidence content fixed, and contrast that with adding *copies*:
   - **Gao et al., "Copies or Sources?" (arXiv:2610.06192, Oct 2026).** Message logs with an exact Bayesian oracle. Conditions: one reading stated once / stated three times / three independent readings, plus pointer, padding and placebo controls. Belief is converted into decisions under explicit costs ("early commitment"). Also includes web documents with appended copies and agent-written logs. This is the "copy vs independent second source" contrast, with a normative oracle.
   - **Wang et al., "GraphEcho" (arXiv:2609.17695, Sep 2026).** Graph agents with active exploration. Conditions: "1 source, 5 paths" vs "5 sources, 5 paths", with evidence wording held fixed.
   - **Pandey et al., "Certified Multi-Source Integrity for Structured Agent Actions" (arXiv:2609.34245, UKAI 2026).** Admits a *payment* action only when corruption-distinct sources corroborate it, and otherwise abstains and escalates to a human. Measured on **sanctions designations** (70,966 entities). This sits in WorkTrace's own counterparty / AML domain. It certifies the *action from the evidence structure*, not the *agent's behaviour*, but it occupies "corroboration as the gate for autonomous action".
   - **Several agent-memory papers** contrast copied or paraphrased claims with independent ones: MEchoBench 2610.17763, CPB 2609.30813, CAMA 2608.19701, GovMem 2607.02579, LQET 2610.13008.
   - **Liao 2607.20827** appends an exact duplicate of a supporting proposition under a trusted or untrusted source marker (the co-present check). It also restores removed valid evidence through an untrusted note ("rescue").

   → What remains new is narrower. Not "the second-source intervention", but **(i)** using it *inside a joint battery* (add independent Y, then remove X) to tell redundancy apart from non-use for one decision, scored against the agent's declared grounds; and **(ii)** using the result to grant or revoke autonomy per decision class.

2. **"Ground truth by construction" is not unique either.** Rule-derived or generator-derived ground truth about which evidence matters exists in:
   - **InterPact (arXiv:2609.39608):** decision-criticality of an evidence unit from complete rule-derived condition→decision mappings, in eligibility and contract decisions.
   - **DRNOISE (2607.17291):** gold answer entailed by *two corroborating* record chains by construction, i.e. designed redundancy, in multi-step deep-research agents.
   - **Copies or Sources (T1):** an exact oracle.
   - **GraphEcho-Syn:** provenance by construction.
   - **ACED-Bench (2610.14381, abstract only):** a hidden PGM.
   - **Liao:** authored tasks whose trusted evidence "determines a unique reference action", plus *annotated* per-target Valid/Invalid labels.

   → Defensible residue: **ground truth, generated per episode, about the *redundancy structure* of the evidence for an *agent's action*** (necessary / sufficient / redundant-with-independent-Y / irrelevant / should-trigger-escalation). Declared grounds *and* intervention responses are both scored against it. I found no paper that scores declared grounds against generator-known decisive evidence in multi-step agent episodes.

3. **Liao (2607.20827) is the closest single neighbour to W2's framing.** It has:
   - next-action agents (tool + argument targets);
   - interventions that change *only source authority*;
   - removal of valid evidence with and without unauthorised competitors (full/mixed/clean);
   - the explicit thesis that "a correct action need not be grounded only in permitted evidence" and that "Outcome benchmarks cannot distinguish a well-grounded decision from a brittle one that happens to be correct".

   It does **not** use declared grounds, does not do multi-step episodes ("no environment transition is simulated during scoring"), and has no delegation rule.

4. **Nautil (Bi, Wang, Ma, arXiv:2610.03190) is a new, directly relevant hit.** LLM "investigators" decide whether to *close a case or leave it open*, which is a proceed vs escalate decision. Its "evidence dependence" test removes the cited grounds against a matched-size control. It reports that a closure-only (outcome) RL reward raises accuracy "at some cost in evidence dependence". It must be cited for W2 (remove-grounds test on a proceed/hold decision) and as support for W3's thesis. It does not grant autonomy.

5. **CSS (2605.30590) supports H2 weakly.** The "nearly opposite" ranking is ρ = −0.49 with p = 0.36 at n = 6 models; the author calls it "underpowered". Cite it as descriptive only.

---

## 0. Coverage and verification

All arXiv metadata (title, authors, dates, comments) was verified with the arXiv API (export.arxiv.org) on 2026-10-25. The ACL Anthology item was verified on its Anthology page.

| Work | Verified | What I read |
|---|---|---|
| Liao 2607.20827 | arXiv API [verified] | **Full PDF text (v1):** main text, App. A–J (all tables 10–58), including references. Figures read only through captions. |
| Turk 2605.30590 (CSS) | arXiv API [verified] | **Full PDF text (v1):** main text §1–7, App. A–M. Figures read through captions; App. E is a figure only. |
| Yang et al. 2609.16268 (Spurious Tool Use) | arXiv API [verified] | **Full PDF text (v1):** §1–7, Ethics, Reproducibility, App. A.1–A.3 (incl. judge prompts). |
| Pawar et al. 2609.05385 (re-check) | arXiv API [verified] | **Full PDF text (v2):** §1–5, Limitations, App. A–D (incl. system prompts and perturbation design). Figures through captions. |
| Gao et al. 2610.06192 (Copies or Sources?) | arXiv API [verified] | §1–5 and Related Work (§6) of the PDF text. Tables 1–3 numbers partly garbled by extraction; I quote only numbers stated in prose. Supplementary material not read. |
| Pandey et al. 2609.34245 (Certified Multi-Source Integrity) | arXiv API [verified] | Full main text §1–8. Appendices A–B (proof, tables) not read. |
| Zhang et al. 2609.39608 (InterPact) | arXiv API [verified] | Abstract, §1–4, §5 setup and RQ1, Limitations, App. B (B.1–B.5) in full. Other appendices skimmed by grep only. |
| Du 2608.08944 (Pair-ID) | arXiv API [verified] | Abstract, §1–3 (design), Table 2. Results beyond Table 2 and the appendices not read. |
| Nie et al. 2607.17291 (DRNOISE) | arXiv API [verified] | Abstract, §1 (introduction, contributions), §2 (related work, first part). Method details and results tables not read. |
| Bi, Wang, Ma 2610.03190 (Nautil) | arXiv API [verified] | Abstract, evidence-dependence definition (§3), evidence-dependence results (§6.x), App. "Counterfactual versions". The rest not read. |
| Wang et al. 2609.17695 (GraphEcho) | arXiv API [verified] | Abstract, §1–3 (intervention definitions, synthetic design). Results not read. |
| Bara 2609.01873 (Epistemic Sybil Resistance) | arXiv API [verified] | Abstract plus a keyword pass over §8 (design). Not read in full. |
| Guo et al., EMNLP 2026 main, "Auditing RAG Necessity" (RAG-CF) | ACL Anthology page [verified]: 2026.emnlp-main.1820, pp. 41480–41503 | Anthology abstract only. |
| Ross et al. 2608.13956; Sato et al. 2609.01687; Bi et al. 2609.06027 (HAE-GEO); Aggarwal 2608.27167; Chen et al. 2610.14381 (ACED-Bench); Deng et al. 2609.08943 (FAE/REAL, CIKM'26); memory papers 2610.17763, 2609.30813, 2608.19701, 2607.02579, 2610.13008; Raja 2607.24117; Jin et al. 2609.01662; Shao 2605.23701 | arXiv API [verified] | **Abstract only.** |
| Xie et al., "Adaptive Chameleon or Stubborn Sloth", arXiv 2305.13300, ICLR 2024 (Spotlight) | arXiv API [verified] | **Not re-read in this round.** Mentioned only as older knowledge-conflict context; do not cite content without reading it. |

---

## 1. Liao (2026), "Auditing Provenance Sensitivity in LLM Agent Action Selection"

### Bibliographic data [verified: arXiv API]
- **Title:** Auditing Provenance Sensitivity in LLM Agent Action Selection
- **Author:** Junchi Liao (single author; no affiliation in the PDF text)
- **arXiv:** 2607.20827v1, 23 Jul 2026, cs.AI
- **Venue:** none stated (AAAI-style template). Treat as a preprint.

### Problem & contribution
- Thesis (Abstract): "Evidence can be relevant without being authorized to determine a decision, so a correct action need not be grounded only in permitted evidence."
- Intro: "Outcome benchmarks cannot distinguish a well-grounded decision from a brittle one that happens to be correct."
- **Contributions:**
  1. A "target-specific authorization audit" with factor labels per tool target and per argument target.
  2. "Matched source interventions with controlled evidence degradation to distinguish response to source authority from behavioral isolation".
  3. An exact Harsanyi/Shapley partial-evidence interaction diagnostic, with its boundaries stated.

### Method
- **Unit.**
  - A fixed next-action decision: one tool target and two argument (slot) targets per task.
  - Context is decomposed into **8 removable semantic factors**: current goal, trusted lookup or policy, memory, retrieved record, previous action, metadata, untrusted note.
  - The system prompt, tool schemas and output format are fixed and not audited.
- **Ground truth (annotated, not purely by construction).**
  - Tasks are authored or converted so that "trusted evidence … determines a unique reference action". Ambiguous goals, underspecified values and "multiple equally acceptable actions" are excluded.
  - An application rule says which sources may authorise each target ("current user goals, trusted observations, and applicable policies").
  - Each target–factor pair is labelled **Valid** (authorised and supports y), **Invalid** (unauthorised *and* supplies a concrete competing value, entity, action, directive or previous-action residue), **Neutral**, or **Excluded**.
  - Labels are by the author team (primary). Three external PhD annotators relabelled 300 targets (2,400 pairs): 4-label κ = 0.608; invalid vs non-invalid κ = 0.626 (agreement 0.854). Adjudicated consensus matches author labels on 78.9% (Table 3, App. D).
- **Intervention operators (exact list).**
  1. **Matched source-authority factorial** (primary). Authority {Trusted, Untrusted} × relation {Support, Compete}. One proposition is added to the same valid-and-neutral base. "Within relation, only the frame changes in the exact template `Source status: [frame]. Proposition: [text]`". The paper calls this textual marker "a controlled proxy for source authority, not an operational provenance channel such as retrieval or tool transport".
  2. **Same-proposition source-only control.** Changes only the source marker of an existing competing factor and measures its removal effect (Tables 4, 10).
  3. **Controlled valid-evidence degradation.** For each Valid factor x: *full* (all factors), *mixed* (remove only x), *clean* (remove x and all Invalid factors). Primary endpoint: mixed–clean discordance. The strict "retained-invalid" pattern is c_F = 1, c_M = 0, c_C = 1.
  4. **Exact subset enumeration** (all 2^8 = 256 subsets) for Harsanyi / Shapley interactions. This is a secondary diagnostic.
  5. **Authority-flip paired control.** Rewrites the invalid factor as trusted/current (Table 41).
  6. **Authority-by-relation supporting arm.** Removes one valid factor and restores it either as trusted or as an untrusted external note ("rescue"; Table 43).
  7. **Exact-text co-present duplicate check** (Qwen3-4B, score-only). The full trusted context stays intact and "an exact duplicate of one supporting proposition is appended with either a trusted or untrusted source marker". Score gains: 1.986 trusted vs 1.726 untrusted; the untrusted duplicate helps on 69.9% of 1,350 targets. **This is a duplicate-source addition, i.e. a redundancy probe, but only as a source-marker control.**
  8. **Explicit authority-policy guardrail** in the prompt (Table 9).
  9. **Robustness controls:** factor-order shuffle; placeholder masks instead of deletion; coarsening; source-preserving no-invalid rewrites; content-type-, salience-, value-bearing- and role-matched random-label nulls; score-field and elicitation variants.
- **Where it intervenes.** Text factors in a single prompt that represent tool outputs, retrieved records, memory and notes. It does **not** intervene in the tool transport. Tau2 states are "convert[ed] … into textual factors; no environment transition is simulated during scoring".
- **Redundancy handling.**
  - Explicit and central. Intro: "The trusted lookup can mask this influence; if that lookup is missing, the same context may determine the recipient."
  - Partial-evidence Shapley exists because "Full-context deletion can miss dependence that emerges after other evidence disappears".
  - The full-context transform is near its null (fractional excess −.004), while the Shapley average is positive (+.027). So unauthorised influence shows up mainly *when valid evidence is absent*, which is masking by redundancy.
  - Reported boundary: strict role-matched controls *reverse* the coalition result (−.018), so coalition involvement "does not by itself isolate authorization from their competing semantic role".
- **Single call vs multi-step.** Single next-action calls. App. A: "does not establish practical scaling to long trajectories with evolving memory, repeated tool calls, and noisy retrieval."
- **Stochasticity.**
  - Teacher-forced target-token log-odds (open-weight models only). Generated actions use deterministic decoding.
  - CIs come from a cluster bootstrap over source tasks.
  - Closed APIs only allow a weaker forced-choice logprob proxy (GPT-4o-mini / 4o, Table 55).

### Evaluation
- **Data.** 450 tasks: AgentAudit-250 (authored), Tau2Audit-100, BFCLAudit-100. That gives 1,350 targets and 10,800 target–factor labels.
- **Models.** Qwen3-4B, Qwen3-30B, Mistral-Small-3.2-24B, Llama-3.3-70B; plus DeepSeek-V2-Lite and Ministral-8B for some endpoints.
- **Key numbers.**
  - Matched factorial: support +0.448 (T) vs −0.052 (U); competition −2.079 (T) vs −1.098 (U); ΔΔ = +0.481 [0.413, 0.550].
  - Generated-action discordance: 1.7% (support) vs 5.4% (compete).
  - Degradation: mixed vs clean actions differ on 24.6% of 12,120 rows. The retained-invalid pattern occurs on 2.4% [2.1, 3.0] of rows (range 0.5–4.1% by model).
  - The explicit authority policy cuts untrusted-competition errors from 14.9% to 9.5%, but "without acting as an invariant provenance filter".
- **Baselines.** First-order and leave-one-out attribution; an absolute score-effect baseline (AUROC .849) beats aligned Shapley (.813) for predicting action change.

### What it covers that WorkTrace must NOT claim
- "Testing whether a correct agent action rests on the right (authorised) evidence rather than only whether it is correct".
- "Interventions that change only the provenance/authority of evidence".
- "Removing valid evidence with and without competing unauthorised evidence".
- "Benign residues (stale memory, wrong-entity records, previous-action residue) as non-adversarial wrong evidence".
- "Separate audit of tool choice vs argument values".
- That redundancy (a trusted lookup) can mask reliance on bad evidence.

### What it leaves open that WorkTrace addresses
- **No declared grounds.** No comparison of the agent's stated reasons with the measured dependence.
- **No multi-step episodes, permissions, consequences or escalation option.** The output is a tool or slot value only, and "escalate" is not an action.
- **No independent-second-source condition.** The duplicate check is an *exact duplicate* with a marker, not an independent corroborating source.
- **Provenance is a textual marker,** not an operational channel. WorkTrace can carry provenance through the tool transport itself.
- **No delegation rule.** "The audit is also an evaluation method, not a guardrail."

### Draft one-sentence differentiation
> Liao (2026) audits single next-action decisions of tool-using LLMs by changing only the textual source-authority marker of evidence and by removing authorised evidence with and without unauthorised competitors, showing that correct actions can retain dependence on unauthorised context. WorkTrace instead intervenes on the external evidence of multi-step decision episodes, scores the responses against the agent's own declared grounds and a generator-known evidence structure (including an independent second source), and uses the result to grant or revoke autonomy per decision class.

### Citation cautions
- Single-author preprint with no venue. The rates are "controlled stress-set rates, not deployment prevalence" (Abstract).
- Main labels are the author team's own (external consensus agrees on 78.9%).
- The coalition result is fragile under role-matched controls.
- The score audit needs open weights.

---

## 2. Turk (2026), "Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents" (Causal Sensitivity Score, CSS)

### Bibliographic data [verified: arXiv API]
- **Title:** Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents
- **Author:** Matt Turk (Protege Data Lab, New York)
- **arXiv:** 2605.30590v1, 28 May 2026, cs.LG
- **Venue (arXiv comment):** "Accepted to RLEval @ ACM CAIS 2026 (Workshop on Methods and RL Environments for Evaluating AI Agents) … 4-page short paper + appendix". A workshop short paper.

### Problem & contribution
- Coverage rubrics ask "does the output look right?". Neither asks "is the model updating its output for the right reasons?" (§1).
- CSS is "a pre-registered interventional metric". It scores {0, 0.5, 1.0} for whether recommendations update "in the pre-registered correct direction" after a mutation of the patient packet.

### Method
- **Pre-registered catalog (§2.1, App. A).** 12 interventions in 5 families. Each is a YAML entry with five fields "committed before any model is evaluated":
  1. applicability filter;
  2. mutation rule (regex replace / delete / insert);
  3. expected change (e.g. `must_drop: [trastuzumab, …]`; `timing_must_shift: adjuvant → primary`; `rationale_must_mention`);
  4. {0, 0.5, 1.0} scoring rule;
  5. family label.
- **Operators (exact families, Table 1).**
  - **A:** biomarker flip (replace HER2/ER/PD-L1 status), eligible n = 129.
  - **B:** prior treatment (inject prior-line progression), n = 269.
  - **C:** biomarker strip (delete biomarker mentions), n = 153 eligible / 80 scored.
  - **D:** surgery status (toggle resection history: delete or insert), n = 306.
  - **E:** stage perturbation, n = 5.
  - In WorkTrace terms: invert X (A, D-toggle), remove X (C, D1-delete), add a new fact (B, D2-insert). There is **no "only X" and no second-source condition.**
- **Ground truth.** The *expected direction of change* is authored and pre-registered by one person. App. M: "authored by the author and have not yet undergone independent clinical vetting". It is a normative expectation, not ground truth by construction of the case. Baseline correctness comes from a two-round oncologist consensus (for CMS, not CSS).
- **Where it intervenes.**
  - Single-shot: the patient packet (median ~80k characters) in the prompt.
  - Agent setting (§4.6): "interventions mutate the underlying packet so the change propagates through retrieval". The tool is `read_chart_section(section)` over 10 sections, in a ReAct loop with an 8-call cap.
- **Judge.** An LLM judge sees baseline and intervened recommendations, the expected change and the scoring rule. gpt-5.4 is the default judge, with Opus judging when gpt-5.4 is under test; uniform-Opus replication (§4.5) gives rank ρ = +1.00 and per-model κ 0.61–0.69.
- **Redundancy handling.** None by design. "Incomplete propagation" is named as a failure mode: "one chart section changed while other parts continue to imply the original fact (e.g., deleting a Procedure block while encounter notes still refer to 'post-op')" (App. M). This is the leakage / redundancy problem, unaddressed.
- **Multi-step.** One ReAct experiment on 100 Family-D tuples. All other results are single-shot.
- **Stochasticity.** Default temperature, apparently one sample per tuple. No CIs in this version; App. M lists "Bootstrap CIs over cases" as camera-ready work. A rerun of Opus judging moved gpt-5.4 by +0.5 pp ("stochastic rerun variability").

### Evaluation
- **Data and models.** 224 tumor-board cases; six models (gpt-5, gpt-5.4, gpt-5.4-mini, claude-opus-4-7, claude-sonnet-4-6, grok-4.20-reasoning).
- **Coverage vs interventional ranking.**
  - CMS ranges 0.480–0.610; CSS ranges 0.309–0.473.
  - **Spearman ρ = −0.49, "exact permutation p = 0.36 at n = 6, underpowered"**; all six models change rank (Table 2, Fig. 1).
- **Family D failure.** Every model scores ≤ 17.2% on surgery-status interventions.
- **Agent setting.** Tool use lifts Family-D CSS for 5 of 6 models (+2.5 to +20.3 pp). gpt-5.4 stays at 0.050 → 0.050 "despite retrieving the same chart sections as the responsive five" (§4.6, App. I). This is a *retrieval-without-update* pattern.
- **Human validation (100 tuples, 3 raters).** Human–human κ 0.40–0.72; LLM vs majority κ 0.46. Per family: A 0.67, C 0.07, D 0.16. Annotators flagged **37/100 rows as medically incoherent (29/49 in Family D)**.
- **No-ops.** "73 of 862 eligible (case, intervention) tuples produced no-op mutations … silently dropped from CSS scoring rather than scored as 0" (App. G). All of them are in Family C: 73/153 = 48% of that family.

### What it covers that WorkTrace must NOT claim
- A pre-registered intervention catalog with expected-change directions and graded scoring.
- That coverage/outcome-style metrics and interventional metrics can rank models very differently (descriptively).
- That interventional evaluation transfers to tool-using agents by mutating the data behind the tools.
- That an agent can retrieve the changed information and still not update.

### What it leaves open that WorkTrace addresses
- **Redundancy and leakage:** incomplete propagation is a named, unsolved failure mode.
- **No "only X", no second source, no declared grounds** (the judge only sees recommendations).
- **Escalation counts as a failure.** The authors propose a 0.5 "refusal-credit branch" only for camera-ready. In WorkTrace, escalate/refuse is a scored, often correct outcome.
- No per-class delegation rule. CSS is offered as "a candidate dense reward for future agentic RL".

### Draft one-sentence differentiation
> Turk (2026) pre-registers input mutations with expected update directions for clinical recommendations, including a tool-using agent whose chart data are mutated, and finds that coverage- and intervention-based metrics can order models very differently; WorkTrace generalises the pre-registered-expectation idea to a redundancy-aware battery (remove / only / invert / independent second source) whose expected responses—including escalation—are derived from a generator-known evidence structure and used for per-class delegation.

### Citation cautions
- Workshop short paper by a single author at a data company.
- The rank reversal is not statistically significant (n = 6, p = 0.36). Cite it as "descriptive", not as evidence for H2.
- The scoring rules were authored by one non-clinician-vetted author.
- 37% of human-audited rows were incoherent.
- The no-op handling (dropping) changes denominators per family.
- Model names (e.g. claude-opus-4-7, grok-4.20) should be reported exactly as given.

---

## 3. Yang et al. (2026), "Spurious Tool Use: When RL Agents Learn the Wrong Reason to Act"

### Bibliographic data [verified: arXiv API]
- **Title:** Spurious Tool Use: When RL Agents Learn the Wrong Reason to Act
- **Authors:** Yiwei Yang, Haoxiang Zhang, Bingbing Wen, Yao Lu, Yuchen Wu, Lei Zhang, Julian McAuley, Pan Lu, Bill Howe (U. Washington, UC San Diego, Stanford). Yang and Zhang contributed equally.
- **arXiv:** 2609.16268v1, 14 Sep 2026, cs.CL. Labelled "Preprint."; no venue.

### Problem & contribution
- RL-trained tool-using agents can learn "cue-driven spurious tool selection".
- Definition 1: π(T_s | x_c, a) ≫ π(T_s | x_c), while T_s gives no advantage.
- The paper stresses that spurious calls are invisible to outcome-only evaluation: "an agent may invoke search, ignore the result, and still produce a correct response" (§1).
- Mitigation: a dense LLM-judged "tool-necessity" reward.

### Method
- **Operator.** Plant a causally irrelevant **cue** in training for one task subset. Then evaluate on **cue-present (Y) vs cue-absent (N)** pairs of the same question where the cued tool is unnecessary: ΔTool_{Y−N} = π̂(T_s | x_c, a) − π̂(T_s | x_c) (§2.2, §3.3).
- **Cues (exact list, §3.2).**
  - **Search-semantic** (put into NQ): `Source: [WEB INDEX 742]`, which is "metadata mimicking a web index provenance marker"; `[REFERENCE]`; and an `<answer></answer>` format instruction (appended).
  - **Code-semantic** (put into DeepMath): `# Cell [1] | kernel: python3 | status: idle`; `#!/usr/bin/python3`; `[CODE]`.
- **Where it intervenes.** The user prompt (question text), not tool outputs.
- **Ground truth by construction.** The cue is "causally irrelevant to tool necessity" by design. Tool necessity follows from task type (math → Python; factual → search). For the reward, necessity is judged by GPT-5 Nano.
- **Redundancy handling.** Not applicable.
- **Multi-step.** Yes: multi-turn VerlTool trajectories with `<python>` and `<search>` tools, GRPO-trained Qwen2.5-7B-Instruct.
- **Stochasticity.** Rollouts at temperature 0.75 during training. **One seed per run** (Table 6). No CIs or significance tests. Held-out sets: GSM8K and 2Wiki.

### Evaluation (numbers)
- Spurious search on math rises by up to **+39.2 pp** (GSM8K, `[WEB INDEX 742]`), +21.7 (DeepMath, `<answer>`) (Table 1).
- Code cues give no comparable effect (ΔPy −0.3 to +5.2). The authors attribute this to the agent failing to learn the math task ("shortcuts form only for the well-learned tool", §5.3).
- Swapped-cue control: semantically misaligned cues give ΔSearch ≤ 3.5.
- Cue–task correlation threshold: the effect appears at ≥ 80% correlation and vanishes at ≤ 70% (Table 5).
- The tool-necessity reward drives ΔSearch to ~0 with accuracy preserved or improved.

### What it covers that WorkTrace must NOT claim
- Cue-present/absent counterfactual pairs to detect "right outcome, wrong reason to act" in tool-using agents.
- The observation that outcome-only rewards leave intermediate decisions unsupervised.
- That task competence enables shortcut formation.

### What it leaves open that WorkTrace addresses
- **No evidence interventions on tool outputs.**
- **No declared grounds, no redundancy, no second source.**
- **No delegation.** The spurious attribute is a training artefact, not decision-relevant evidence.

### Draft one-sentence differentiation
> Yang et al. (2026) plant causally irrelevant cues—one of them a fake provenance marker—during RL training and show with cue-present/absent pairs that tool-using agents learn to select tools for the wrong reason without losing accuracy; WorkTrace tests, at evaluation time and without retraining, whether an agent's actions depend on the decision-relevant external evidence they should depend on, and uses that to set per-class autonomy.

### Citation cautions
- Preprint. Single seed per condition, one 7B base model, synthetic 1,000-example training set, 30 training steps.
- The "competence → shortcut" link is correlational (based on two task types).

---

## 4. Pawar et al. (2026), "Necessary or Sufficient?": design re-check

### Bibliographic data [verified: arXiv API]
Urja Pawar, Rajitha Ramanayake, Nabeel Kemal, Ashwin Kandath, Owen O'Neill, Guillaume Bourgeon, Houssem Chatbri, Christopher Martin, Vadim Pertsovskiy (all BNY). arXiv:2609.05385v2 (v1 4 Sep 2026; v2 7 Sep 2026), cs.AI. Preprint, no venue.

### Design details (new relative to round 2)
- **Factor selection.**
  - Factors are **fixed, dataset-specific feature keys**: 18 client fields; 8 risk categories.
  - The model must cite exactly three keys from the list. This was chosen after comparing 13 prompt formats (App. A.1, Table 1). It lowered positional instability from .929 to .235 (advisor) and from .858 to .240 (monitoring).
  - Uncited "eligible" features (active and scorable) are compared with the lowest-scoring cited one.
- **Intervention construction (App. C).**
  - *Contrast substitution:*
    - ordinal → value at the opposite end of the ordered list;
    - binary → flip;
    - 1–10 scale → 11 − x;
    - categorical / free text → the valid alternative with the fewest shared tokens;
    - monitoring → a segment from a "predefined contrasting risk category".
  - *Blank removal:* advisor → `[UNKNOWN]`; monitoring → delete the segment.
  - *Similar-value substitution:* adjacent interval or ±1 point; most token overlap; same risk category, different expression.
  - *Sufficiency:* other 17 fields → `[UNKNOWN]` while **keeping the advisor pool**; monitoring keeps the base request plus the target segment. Sufficiency is therefore "relative to this fixed context".
- **Ground truth.** **None.** "The evaluation uses no reference explanation or human-authored feature ranking" (§3.2). The data were generated from predefined value pools; risk pools were written by Claude Opus 4.6. 30 samples were manually reviewed. The data are **not released** ("constructed from proprietary evaluation schemas", App. B).
- **Agent framing.** Motivation only: "LLM decision components that can operate within agent workflows" (Abstract). Both use cases are single calls with no tools or trajectories. The authors scope the work "to individual LLM decisions" and not "to establish end-to-end agent safety" (§5).
- **Possible confound worth citing.** The system prompt itself instructs: "Consider: if this feature were different, would the outcome change? If only this feature were known, would it alone determine the outcome?" (App. B). The model is primed with the very criteria being tested. WorkTrace should *not* prime declared grounds with the test criteria, or should run both conditions.
- **Stochasticity.** T = 0, three API trials per intervention, invalid responses excluded. PN/PS are rates over ≤ 3 trials, so each score is coarse (0, 1/3, 2/3, 1).
- **Redundancy.** None: single-feature interventions only. Necessity and sufficiency rankings of the cited features correlate only 0.18–0.35 (advisor) and 0.38–0.87 (monitoring) (App. D.2). That is consistent with redundancy, but the paper does not interpret it that way.

### Updated differentiation sentence
> Pawar et al. (2026) estimate black-box necessity and sufficiency for the top-three factors an LLM cites from a fixed feature list, motivated by monitoring and escalation in agent workflows but evaluated on single, tool-free decisions without ground truth; WorkTrace intervenes on source-level external evidence inside multi-step agent episodes whose decisive and redundant evidence is known by construction, adds an independent-second-source condition, and turns the joint response pattern into a per-class delegation decision.

---

## 5. Search: "add a corroborating / independent source" and source redundancy (2026)

Strategy: arXiv API abstract searches combining corroborat*, "independent sources", "second source", "source redundancy", "redundant evidence", "duplicate evidence", "evidence intervention(s)", overdetermination, restated, provenance AND corroboration, "independent evidence" AND agent, "evidence dependence", plus three web searches. Results are sorted by date, and only those since Oct 2025 were kept. All hits listed are [verified] on arXiv or the ACL Anthology.

### 5.1 Directly occupying "independent second source vs copy"

| Work | Setting | Intervention | Ground truth | Read |
|---|---|---|---|---|
| **Gao, Li, Yu, Ren, Chen, Wang, "Copies or Sources? Measuring How LLM Aggregators Count Restated Evidence in Multi-Agent Systems"**, arXiv:2610.06192 (5 Oct 2026) | LLM aggregators of multi-agent logs; web documents (ConflictingQA); agent-team logs under 4 protocols | Same reading stated once / 3× / up to 8× vs *m* independent readings; Pointers, Padding, Claims, Packed and prose controls; conflict probes; a "declaration" paragraph plus placebo paragraphs; a protocol "reference rule" | **Exact Bayesian oracle** in T1 (by construction) | §1–6 |
| **Wang, Zhou, Fan, Zhang, "GraphEcho: Structural Redundancy and Evidence Provenance in LLM Graph Agents"**, arXiv:2609.17695 | Graph agents with active exploration; 800 fictional claims; SciFact | "1 source × 5 paths" (redundant paths) vs "5 sources × 5 paths" (distinct origins), wording and path templates matched | Provenance by construction (source identifiers preserved by the generator) | Abstract, §1–3 |
| **Pandey, Jain, Chen, Maple, Panchev, "Certified Multi-Source Integrity for Structured Agent Actions"**, arXiv:2609.34245 (UKAI 2026, PMLR) | Payment actions; **sanctions designations (OpenSanctions, 70,966 entities)**; npm/PyPI provenance | Not an agent test. A certifier counts **corruption-distinct** sources by minimum hitting set ("re-publishing or laundered copies cannot manufacture a quorum") and **abstains, escalating to a human**, unless corroboration suffices; live-model loop with 5 models | Theorem plus synthetic worlds | Main text §1–8 |
| Bara, "Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence", arXiv:2609.01873 | Multi-agent report aggregation (Haiku-class extractors on synthetic memos) | Report multiplicity 1→32 with one evidence root vs root multiplicity 1→16 | Synthetic latent state | Abstract and design keyword pass |
| Memory papers: MEchoBench 2610.17763; CPB 2609.30813; CAMA 2608.19701; GovMem 2607.02579; LQET 2610.13008 (NeurIPS 2026 workshop oral) | Agent memory admission / arbitration | Copied or paraphrased claims vs independent evidence; same-source record accumulation | Scenario-defined lineage | Abstracts only |
| Ross, Koopman, van der Vegt, Zuccon, "How retriever redundancy and diversity impact RAG effectiveness", arXiv:2608.13956 | RAG on FictionalQA | Duplicate vs paraphrased vs diverse-genre documents | Fictional QA: answer must come from documents | Abstract only |
| Bi et al., HAE-GEO, arXiv:2609.06027 | Deep-search agents | Poisoning level "L3 apparent corroboration" | Controlled corpus | Abstract only |

**Key facts from the full or partial reads**

- **Copies or Sources.**
  - "a forwarded copy counts for 0.06 to 0.42 of a new reading".
  - Copies are "mostly all or nothing": 4–35% of reports count fully.
  - The same log answered three times is counted inconsistently in 16–42% of logs.
  - "On 5% to 40% of logs that state one reading three times, the reported belief implies an early commitment that the oracle never makes".
  - Three independent readings are reproduced at 2.83–2.96 readings, so the unit is validated.
  - Discrimination D_3 between copies and sources ranges from 0.53 to 0.92.
  - Fixes: a declaration brings w_3 ≤ 0.08; the reference rule cuts early commitment from 11.2% to 1.1% "and preserves genuine corroboration".
- **Certified Multi-Source Integrity.**
  - In sanctions data, at the control-domain level, about 15% of entities have ≥ 3 issuing domains and about three-quarters rest on a single domain.
  - On 450 npm packages, an apparent third witness collapses: none reach three corruption-distinct witnesses.
  - In the live loop, the injection fools every model except Claude Opus 4.8. The naive agent executes fraudulent payments on 72–100% of attacks; the certifier admits none.
  - Baselines: CaMeL/FIDES-style capability gating ("executes nothing") and a PCAS-style policy monitor (up to 18% unsafe, 0% utility on novel payees).

### 5.2 Other 2026 evidence-intervention neighbours found in the search

- **Zhang, Zhao, Hao, Wang, "Is This Evidence Decision-Critical? Learning to Verify Rule-Governed Decisions" (InterPact), arXiv:2609.39608.** [verified; read §1–5 and App. B]
  - **Operators.** Six target operations: removal, polarity reversal, alternative replacement, irrelevant replacement, weakening, strengthening. Two invariance controls: paraphrase and distractor insertion. Rewrites are by frozen GPT-5.4, holding the rule and non-target conditions fixed.
  - **Ground truth.**
    - Condition states are *annotated* (structured adaptations of ContractNLI and ShARC).
    - Decisions follow from an explicit three-valued AND/OR aggregation.
    - "complete state-to-decision mappings" give, by construction, whether any change of the target condition could change the decision.
    - 53% of target interventions that change the condition leave the decision unchanged ("absorbed" vs "propagated").
    - Redundancy is acknowledged: "Other evidence can preserve the target condition state after its designated evidence unit is removed" (App. B.3).
  - **Results and scope.** It is used to *train a criticality verifier* (68.28% accuracy on 207 roots). Single-call, not agentic.
  - **Human audit** of 400 pairs: intervention fidelity 389/400; target condition state 363/400; decision after intervention 385/400.
  - **Relevance.** This is the closest existing "ground truth about decisive evidence by construction". Cite it.
- **Du, "What Would Fix This RAG Failure? Auditing Counterfactual Response with Paired Evidence Interventions" (Pair-ID), arXiv:2608.08944.** [verified; read §1–3]
  - A 2×2 factorial: **add missing gold support × delete verified non-support**, for the same failed query, with a fixed reader and decoding.
  - Length- and position-matched shams.
  - A prospectively fixed SHA-256 sample (1,200 of 11,105 eligible failures).
  - Support addition repairs 0.328; deletion 0.136.
  - Exact response vectors agree across 4 readers on only 0.675–0.765.
  - Ground truth is HotpotQA / 2Wiki gold-support annotation. Single-call RAG.
  - **Precedent for a crossed (joint) reading of two evidence interventions.**
- **Bi, Wang, Ma, "Not Until the Evidence Says So: Teaching LLM Investigators When to Close a Case" (Nautil), arXiv:2610.03190.** [verified; read the evidence-dependence parts]
  - Investigators request evidence from case files and either *close* or *leave open and name what is missing*.
  - **Evidence-dependence test:** remove 40/75/100% of the conclusion's cited grounds vs a control that removes the same number of non-cited items, with a leak check for restated content.
  - Findings:
    - After SFT, removing the grounds lowers closure by 26 points vs the control.
    - The base model and Gemini still close 87% and 93% of cases whose grounds are gone.
    - "Reinforcement learning that rewards only the closure decision … at some cost in evidence dependence".
  - Grounds are *teacher-cited*, not by construction. The authors note "a model might close a reduced case on other sufficient evidence" (the redundancy caveat).
- **Nie et al., DRNOISE, arXiv:2607.17291.** [verified; read abstract, §1–2]
  - 100 tasks; each gold answer is "supported by two corroborating indirect record chains". Redundancy and ground truth are both by construction.
  - The noisy condition adds one plausible conflicting direct-answer document.
  - Results: 66–88 pp accuracy drops; "verification inertia".
  - **Precedent for designed redundancy plus a single added-document intervention in multi-step research agents.**
- **Guo, Liu, Wu, Yiu, "Auditing RAG Necessity: A Conformal Test for Source-Independent Answers" (RAG-CF).** EMNLP 2026 main, pp. 41480–41503, ACL Anthology 2026.emnlp-main.1820. [verified on Anthology; abstract only]
  - Four counterfactual document operators; a split-conformal p-value per query.
  - Flagged (source-independent) rate is 13–56% across 60 configurations.
- **Deng, Cao, Aletras, Wang, Stevenson, "Evaluating and Improving Evidence-Grounded Fact-Checking in LLMs via Multi-Round Evidence Ablation" (FAE / REAL).** arXiv:2609.08943, CIKM'26. [verified; abstract only]
  - Iteratively ablates cited evidence; finds that LLM fact-checkers "rely more on their parametric knowledge than on the evidence provided".
- **Sato et al., "Learning Evidence Sufficiency Boundaries for Selective Answering in Grounded Multi-Hop QA", arXiv:2609.01687.** [verified; abstract only]
  - Ordered evidence chains: abstain below sufficiency, answer at the boundary, and "keep the answer stable when redundant evidence is added". This is a training objective that includes a redundant-evidence addition.
- **Aggarwal, "Calibrated Enough to Know, Not Calibrated to Act", arXiv:2608.27167.** [verified; abstract only]
  - Fabricated, authoritative-looking evidence raises agents' commitment to unknowable questions as much as genuine data does: "What unlocks confident action is not information but the authority of its packaging".
  - Relevant to the act/don't-act gate.

### 5.3 Verdict on question (b): is "add an independent second source" still unoccupied?

**No, not as an intervention.** As of Oct 2026:
- the contrast between an independent second source and a copy is measured for LLM aggregators (Gao et al.), graph agents (GraphEcho), memory systems (several) and RAG (Ross et al.);
- corroboration by corruption-distinct sources is used to gate autonomous payment actions, with escalation otherwise (Pandey et al.), including on sanctions data.

**What I did not find anywhere:**
1. An *independent-second-source* condition combined with *removal of the original source* ("add Y, then remove X" vs "remove X alone" vs "remove X and Y") to classify *one decision's* null effect as redundancy vs non-use.
2. That classification scored against the agent's own **declared grounds**.
3. The second-source condition used as a test of whether the agent's *proceed/escalate* choice responds to corroboration where the domain requires it (e.g. AMLR art. 24(2)(b), "another reliable source").
4. Any of this feeding a **per-decision-class autonomy rule**.

Pandey et al. come closest to (3)–(4) in spirit, but they gate the *action by evidence structure*, independent of the agent's behaviour. They do not test or certify the agent.

### 5.4 Verdict on question (c): is "ground truth about the decisive evidence by construction" present anywhere?

**Yes, in several forms. W2 must narrow.**

| Work | What is known by construction | Annotated part | Agentic? |
|---|---|---|---|
| InterPact 2609.39608 | Whether a change in the target condition can change the decision (complete rule mapping) | Original condition states and evidence association (ContractNLI/ShARC); post-edit condition state (LLM plus review); some negative labels by reviewers | No |
| DRNOISE 2607.17291 | Gold answer and two sufficient, corroborating record routes | — (by construction) | Yes (deep research) |
| Copies or Sources 2610.06192 (T1) | Exact posterior given distinct readings | — | Aggregator only (T3 uses agent teams) |
| GraphEcho 2609.17695 | Number of distinct origins vs paths | — | Yes (graph agent) |
| Liao 2607.20827 | Unique reference action from trusted evidence (authored) | Valid/Invalid/Neutral labels (author team; external κ ≈ .61–.63) | Next-action only |
| Spurious Tool Use 2609.16268 | Cue is irrelevant; tool necessity follows from task type | Necessity reward via LLM judge | Yes (RL agent) |
| Pair-ID 2608.08944 | — | Gold support from HotpotQA/2Wiki annotations | No |
| CSS 2605.30590 | — | Expected update direction, pre-registered by one author | Partly (1 ReAct experiment) |
| Nautil 2610.03190 | — | Grounds = teacher-cited items | Investigator agent |
| Pawar 2609.05385 | **None** | — | No |

**Residual novelty claim (defensible).** WorkTrace generates *multi-step agent decision episodes* in which the generator plants the **full evidence-role structure for the action**: necessary, sufficient, redundant with an *independent* (ancestry-distinct) second source, decoy, and escalation-triggering. The **agent's declared grounds and its intervention responses are both scored against that structure**.

I found no work that combines generator-known *redundancy structure* with *declared-grounds scoring* in agent episodes. InterPact is the closest single precedent for "decisiveness by construction" and must be cited as such.

---

## 6. Cross-cutting comparison (question (a))

| | Liao 2607.20827 | CSS 2605.30590 | Spurious Tool Use 2609.16268 | Pawar 2609.05385 | WorkTrace (planned) |
|---|---|---|---|---|---|
| Operators | Source-marker flip T/U × support/compete; remove valid x (mixed); remove x + all invalid (clean); exact subsets; authority-flip rewrite; trusted vs untrusted restoration; exact-duplicate co-present; explicit policy | Replace (flip); delete (strip / remove surgery); insert (prior failure, resection, stage); 12 interventions, 5 families | Cue present vs absent (prompt tags) | Contrast substitution; blank removal; similar-value substitution; keep-only-f (sufficiency) | Remove X; only X; invert X; add independent Y (plus copy-of-X control) |
| Where | Text factors standing in for tool outputs, records, memory, notes; textual source marker | Patient packet; in the agent setting, data behind `read_chart_section` | User prompt | Profile fields / prompt segments | External evidence in tool returns and documents of multi-step episodes |
| Ground truth for what should matter | Authored unique reference action plus annotated authorisation labels | Pre-registered expected direction (one author) | Cue irrelevant by design | None | Generator-known evidence roles |
| Redundancy | Central (masking; partial-evidence Shapley; full/mixed/clean) | Named failure ("incomplete propagation"), unaddressed | n/a | None | Designed (second source; joint reading) |
| Declared grounds | No | No (judge sees recommendations; a rationale field appears in some scoring rules) | No | Yes (top-3 fixed keys) | Yes (grounds graph) |
| Multi-step | No | One ReAct experiment | Yes | No | Yes |
| Escalation as an outcome | No | Scored as failure (refusal credit planned) | No | No | Yes |
| Stochasticity | Teacher forcing; deterministic decoding; cluster bootstrap | Default temperature, one sample, no CIs | T = 0.75 training; 1 seed; no CIs | T = 0, 3 trials | Multiple runs per episode (see §7) |

---

## 7. Implications for WorkTrace

### 7.1 Claims to change (W2)
1. **Drop "the add-an-independent-second-source intervention was not found anywhere".**
   - Replace it with: "We use an independent-second-source condition—previously studied as copy-vs-source counting in LLM aggregation, graph agents and memory (Gao et al. 2026; Wang et al. 2026; Bara 2026) and as a corroboration gate on agent actions (Pandey et al. 2026)—as one cell of a joint battery that separates redundancy from non-use for an individual agent decision and is scored against the agent's declared grounds."
2. **Drop "nobody has ground truth by construction".**
   - Replace it with: "Unlike benchmarks that fix the correct answer or the decision rule by construction (Nie et al. 2026; Zhang et al. 2026), our generator fixes the *role* of each evidence item for the action, including redundancy across independent sources, so that both declared grounds and intervention responses can be scored."
3. **Keep, as W2's core:**
   - joint reading of the four conditions against declared grounds;
   - escalation as a scored response;
   - external evidence carried by the tool transport in multi-step episodes;
   - its use for per-class delegation.
4. **H2 citation.** Cite CSS only as "descriptive evidence that coverage- and intervention-based metrics can order models differently (ρ = −0.49, n = 6, not significant)". Cite Pawar, Liao and Nautil for the stronger statement that outcome-correct behaviour can coexist with wrong evidence dependence.

### 7.2 Design changes (concrete)
1. **Define "independent" operationally, as ancestry- or corruption-distinct (Pandey et al.).**
   - In counterparty verification, a national list that transposes a UN designation is *not* an independent second source.
   - The generator should label each source's control domain and provenance root.
   - Add a **copy-of-X control condition** (same content, same root, different outlet or format) next to the independent-Y condition. Following Gao et al., include **pointer** and **padding** (length-matched) controls. Expected responses:
     - copy-of-X: no change;
     - independent Y: corroboration;
     - padding / pointer: no change.
2. **Pre-register the intervention catalog in CSS format.**
   - Per entry: applicability filter, mutation rule, expected response, graded scoring rule, family.
   - Extend "expected response" to {proceed, escalate, refuse} plus grounds-update, and **give credit for correct escalation**. CSS scored correct refusals of incoherent inputs as 0 and had to add a refusal-credit branch later.
3. **Measure and report semantic validity per mutation (CSS App. M; Liao; InterPact App. B.5).**
   - Three failure modes to audit: **semantic no-ops**, **incomplete propagation / leakage**, and **incoherence**.
   - CSS benchmarks: 8.5% no-ops overall and 48% in one family; 59% incoherent in one family.
   - InterPact human audit: 97% intervention fidelity; 91% condition-state agreement.
   - Report no-op rates per family; do *not* silently drop no-ops without reporting denominators.
   - Run a leakage check on removed items, as Nautil flags "removed items whose content is likely restated elsewhere". A generator makes this checkable by construction.
4. **Matched controls for every intervention.**
   - Length- and position-matched shams for additions and deletions (Pair-ID).
   - Same-size removal of non-ground items (Nautil).
   - Invariance controls: paraphrase and distractor insertion (InterPact).
   - Placebo paragraphs (Gao et al.).
   - Random-label and role-matched nulls (Liao). Note that role-matched controls *reversed* Liao's coalition result, so test same-role decoys explicitly.
5. **Provenance must travel through the operational channel.** Liao's marker is "a controlled proxy … not an operational provenance channel such as retrieval or tool transport". WorkTrace should vary provenance in the tool-return metadata, and report a textual-marker variant only as a comparison.
6. **Target-specific labelling.** Label evidence roles per action component (tool choice vs argument values) as Liao does. The same record can be valid for the tool and invalid for a slot.
7. **Declared-grounds elicitation.**
   - Use enumerated evidence IDs, as with Pawar's fixed keys (instability .93 → .24).
   - Do **not** prime with the test criteria (Pawar's prompt literally asks "if this feature were different…" and "if only this feature were known…"). Run a primed vs unprimed ablation.
   - Score necessity and sufficiency separately, since they diverge (Pawar App. D.2).
8. **Stochasticity.**
   - Single replies are unreliable for this kind of test: 16–42% of logs were copy-counted inconsistently across three replies (Gao et al.), and exact response vectors agree on only 0.675–0.765 across readers (Pair-ID).
   - Use ≥ 3–5 samples per episode × condition, and report per-episode response distributions.
   - Certify per model as well as per class, because responses are reader-conditional.
9. **Add an irrelevant-cue placebo family.** Insert a provenance-looking but causally irrelevant marker (cf. `Source: [WEB INDEX 742]`, Yang et al.) and expect no change in action. This tests "wrong reason to act" at evaluation time.
10. **Baselines to add.**
    - The **Pandey et al. corroboration certifier** as an evidence-structure-only gate: autonomy is granted whenever corroboration exists, *regardless of the agent's behaviour*. It is a strong, obvious competitor to WorkTrace's rule in the counterparty domain. Report matched-coverage comparisons against it.
    - A **Nautil-style remove-grounds test** as a cheaper single-intervention baseline for the delegation rule.
11. **Escalation endpoint and "absorbed vs propagated".** Use InterPact's distinction: a correct agent should show no action change when a condition change is absorbed by the rule, and should change or escalate when it propagates. The generator knows which case applies.

### 7.3 Risks
- **Novelty (high):** reviewers who know Gao et al., GraphEcho or Pandey et al. will reject any "first independent-source intervention" claim. Mitigation: wording as in §7.1.
- **Novelty (medium):** Liao already tests whether correct actions rest on authorised evidence, with removal and authority interventions, in next-action agents. Mitigation: emphasise declared grounds, multi-step episodes with operational provenance, escalation as a response, independent-source redundancy, and delegation.
- **Domain overlap:** Pandey et al. use sanctions data and payment actions with abstain/escalate. Cite them in the counterparty-domain section and explain that WorkTrace certifies *agent behaviour per decision class* while they certify *individual actions from source structure*. The two are complementary. A reviewer may ask why not simply use their certifier.
- **Measurement:** CSS shows how much of an intervention catalog can turn out invalid (incoherence, no-ops) once humans look. Budget a human audit of ≥ 400 intervened episodes (InterPact's size).
- **Outcome-only training erodes evidence dependence:** evidence for this comes from Nautil (RL on closure lowers dependence), Yang et al. (task reward leaves tool choice unsupervised) and Khan & Bhuyan (round 2). Use it to motivate re-testing after model updates (the revocation part of W3).

### 7.4 Draft related-work sentences (ready to paste)
- **Liao:**
  > Liao (2026) audits next-action decisions of tool-using LLMs by changing only the textual authority marker of a proposition and by removing authorised evidence with and without unauthorised competitors, finding that correct actions can remain sensitive to stale or untrusted context; we go further by scoring an agent's declared grounds against generator-known evidence roles in multi-step episodes and by using the results to delegate autonomy.
- **CSS:**
  > Turk (2026) pre-registers clinically motivated input mutations with expected update directions and reports that coverage- and intervention-based metrics order six models differently, including a tool-using agent that retrieves the mutated chart section yet does not update; our catalog follows the pre-registration practice but adds redundancy-aware conditions and treats escalation as a scored response.
- **Spurious Tool Use:**
  > Yang et al. (2026) show with cue-present/absent pairs that RL-trained agents can learn to call tools for causally irrelevant reasons while preserving accuracy, illustrating why outcome-based signals cannot certify the basis of an agent's actions.
- **Pawar:**
  > Pawar et al. (2026) test the necessity and sufficiency of the factors an LLM decision component cites, motivated by escalation in agent workflows, but on single tool-free decisions without ground truth.
- **Copies vs sources:**
  > Recent work shows that LLM aggregators and agents partially count restated evidence as independent corroboration (Gao et al. 2026; Wang et al. 2026; Bara 2026), and that corroboration across corruption-distinct sources can gate high-stakes agent actions (Pandey et al. 2026); we use an independent-second-source condition not to measure counting per se but to disambiguate redundancy from non-use in an agent's individual decisions.
- **Ground truth:**
  > Benchmarks increasingly fix by construction the correct answer and its supporting record chains (Nie et al. 2026) or the rule-implied criticality of an evidence unit (Zhang et al. 2026); our generator additionally fixes the redundancy structure of the evidence for each action, which lets us score both declared grounds and intervention responses.
- **Nautil:**
  > Bi et al. (2026) test whether LLM investigators stop closing cases when the cited grounds are removed, and report that outcome-only reinforcement trades evidence dependence for accuracy—a finding that motivates basing delegation on evidence tests rather than outcomes.

### 7.5 Things to cite (all [verified] as above)
- **Must cite:**
  - Liao 2607.20827
  - Pawar et al. 2609.05385
  - Gao et al. 2610.06192
  - Pandey et al. 2609.34245
  - Zhang et al. (InterPact) 2609.39608
  - Bi, Wang, Ma (Nautil) 2610.03190
  - Nie et al. (DRNOISE) 2607.17291
  - Turk (CSS) 2605.30590
  - Yang et al. 2609.16268
- **Should cite:**
  - Wang et al. (GraphEcho) 2609.17695
  - Du (Pair-ID) 2608.08944
  - Bara 2609.01873
  - Guo et al. (RAG-CF), EMNLP 2026
  - Deng et al. (FAE / REAL), CIKM'26, 2609.08943
  - Aggarwal 2608.27167
- **Optional:**
  - Ross et al. 2608.13956
  - Sato et al. 2609.01687
  - HAE-GEO 2609.06027
  - Memory-echo / admission papers (2610.17763, 2609.30813, 2608.19701, 2607.02579, 2610.13008)
  - ACED-Bench 2610.14381
  - Xie et al. ICLR 2024 (only after reading it)
