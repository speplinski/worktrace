# Project Ariadne (Khanzadeh, 2026), reading note for WorkTrace

**Coverage:** I read the **full text** of v1 (7 pages including references) from the arXiv PDF (`arxiv.org/pdf/2601.02314`, extracted with pdftotext). I also checked the abstract page and the HTML rendering; they match the PDF. The paper has no appendix, no supplementary material and no code link. Figure 2 (a distribution plot) is an image, so I have only its caption.

---

## 1. Bibliographic data

- **Title:** Project Ariadne: A Structural Causal Framework for Auditing Faithfulness in LLM Agents
- **Author:** Sourena Khanzadeh (single author)
- **Affiliation:** **none given** in the PDF, the HTML or the arXiv metadata.
- **arXiv:** 2601.02314, **v1** (the only version as of 2026-10-25), submitted Mon 5 Jan 2026, 18:05 UTC, primary class cs.AI. The PDF is dated "January 2026".
- **Venue:** none listed. There is no journal reference or comments field. Treat it as a non-peer-reviewed preprint.
- **Suggested BibTeX key:** `khanzadeh2026ariadne`. `@misc{..., eprint={2601.02314}, archivePrefix={arXiv}, primaryClass={cs.AI}, year={2026}}`

## 2. Problem & motivation

- LLM "agents" are used for "high-stakes autonomous decision-making" (finance, scientific discovery). Their CoT traces may be **post-hoc rationalisations** rather than **faithful generative drivers** of the final answer. The paper calls this the "Faithfulness Gap".
- Existing evaluation is criticised as relying on "surface-level textual similarity or static benchmarks". Ariadne proposes an interventionist, SCM-based audit instead.
- The failure mode it names is **Causal Decoupling**: the answer stays the same when the reasoning is contradicted. It also calls this "Reasoning Theater" or the "Hallucinated Explanation".

## 3. Core contributions (as claimed)

1. A formalisation of an agent's CoT generation as an SCM, M = ⟨U, V, F⟩, over the reasoning steps and the answer.
2. Hard interventions `do(s_k = s'_k)` on a single intermediate reasoning step. The counterfactual step is written by a "critic" model using one of four contradiction types. The agent is then re-run from the intervention point.
3. Metrics: a per-intervention **Causal Sensitivity / Faithfulness score φ = 1 − S(a, a\*)**, a binary **violation indicator** V, **Expected Faithfulness** EF, and **Violation Density** ρ.
4. An empirical "Faithfulness Gap": high ρ on General Knowledge and Science, much lower on Math.
5. A proposal (abstract only) of the "Ariadne Score" as a benchmark. It is never defined separately (see §4).

## 4. Method

**SCM (Sec. 4.1).**
- Exogenous variables: U = {q, θ}, the query and the model parameters.
- Endogenous variables: V = {s₁,…,s_n, a}, the reasoning steps (the trace T) and the final answer.
- Structural equations F.
- Step equation (Eq. 1): `s_i = f_i(q, s_<i; θ) + ε_i`. Here ε_i is the noise of autoregressive sampling.
- Answer equation (Eq. 2): `a = f_a(q, T(q); θ)`.
- Sec. 2.2 also writes `s_i = f_step(q, s_<i, θ)`. That sentence ends in a broken citation, "[?]".

**Intervened nodes.** The interventions target **one intermediate reasoning step s_k at a time**, i.e. a step of the model's own generated CoT text. The intervention is `do(s_k = s'_k)`, "where s'_k is a counterfactual thought generated to contradict the original reasoning".
- **Re-execution (Eq. 3):** `a* = f_a(q, {s₁,…, ι(s_k),…, s*_n}; θ)`. The steps after k "are re-sampled and may deviate from the original trace", so the agent can repair the injected step in later steps.

**Intervention operator (Eq. 4).** `ι_τ(s_k) = f_critic(s_k, τ, θ_critic)`, i.e. an LLM critic rewrites the step. There are exactly four types:
`τ ∈ {LogicFlip, FactReversal, PremiseNegation, CausalInversion}`.
- In the abstract and introduction these appear as "inverting logic, negating premises, and reversing factual claims" and "flipping logical operators, negating factual premises, or inverting causal directions".
- **In the experiments only LogicFlip (τ_flip) was used, and only at the first reasoning step s₀** (Sec. 5.1). The critic model is not named.

**Scores.**
- **Causal Sensitivity Score / Faithfulness Score (Eq. 5):** `φ(q, k, ι) = 1 − S(a, a*)`. S is a semantic-similarity function in [0, 1]. In the experiments S is an LLM judge (Claude 3.7 Sonnet). The same quantity is written `φ = 1 − S(a, a_ι)` in Sec. 2.3 and is called the "Faithfulness Score" there.
- **Violation / Causal Decoupling (Eq. 6):** `V(q,k,ι) = 1 if S(a,a*) > τ_sim and Strength(ι, s_k) > λ; 0 otherwise`.
  - τ_sim is a similarity threshold.
  - λ is the "minimum intervention strength required to expect a change in a".
  - **Neither the value of τ_sim nor λ, nor how `Strength(·)` is computed, is reported.**
- **Expected Faithfulness (Eq. 7):** `EF(θ) = E_{q∼D}[1 − S(a, a*)]`.
- **Violation Density (Eq. 8):** `ρ = (1/m) Σ_i V(q_i, k_i, ι_i)`.
- Sec. 2.4 also mentions a "Violation Rate V_rate" and an "Average Faithfulness φ̄". These seem to be the same as ρ and EF; the paper does not say so explicitly.
- **"Ariadne Score":** it appears **only in the abstract** ("we propose the Ariadne Score as a new benchmark for aligning stated logic with model action"). It has no formula. Presumably it means φ, EF or ρ, but the paper does not say which (*uncertain*).

**Definition of faithfulness (Sec. 2.2).** Faithfulness is defined as causal consistency: "a change in reasoning ι(s_k) ≠ s_k must necessitate a change in the final answer a(q) ≠ a_ι(q, k)". This is a **necessity** criterion and it is central to §7 below.

## 5. Internal reasoning vs. external evidence — EXACT answer

**Ariadne intervenes only on the agent's internal reasoning text**, i.e. the generated CoT steps s_k. These are modelled as endogenous nodes. It does **not** intervene on external inputs or evidence.
- The query q is exogenous and held fixed.
- There are no tool calls, retrieved documents, environment observations, permissions or actions anywhere in the method or the experiments.
- "Agent" means a "GPT-4o-based agent" that produces a CoT and an answer to a QA-style query. The "action" is the textual answer.
- Removing, isolating, inverting or adding a second source of evidence is **not** done.
- The closest operations are "PremiseNegation" and "FactReversal". These rewrite a *reasoning step* (e.g. forcing the agent to "accept an initial premise negating human-induced climate change"); they do not change what the environment provides.
- The authors' own future work also stays inside the trace: multi-node "path-specific" perturbations, and saliency via attention or gradients to find "load-bearing" steps.

## 6. Evaluation

**Setup.**
- **Agent model:** one model only, "a GPT-4o-based agent". This is despite the claims about "state-of-the-art models" (plural).
- **Judge:** a secondary **Claude 3.7 Sonnet** instance computes S(a, a\*).
- **Data:** "a dataset of **500 queries**" in three categories. The source is not given; it may be self-constructed (*uncertain*).
  - General Knowledge (geography, history)
  - Scientific Reasoning (climate science, biology)
  - Mathematical Logic (arithmetic, symbolic logic)
- **Intervention:** LogicFlip at s₀ only.
- **Not reported:** number of seeds or samples per query, confidence intervals, statistical tests, a baseline (e.g. a no-intervention resampling control or a random-edit control), and a human validation of the judge.

**Table 1** (verbatim numbers):

| Category | Mean φ̄ | Similarity S | Violation Rate ρ |
|---|---|---|---|
| General Knowledge | 0.062 | 0.938 | 92% |
| Scientific Reasoning | 0.030 | 0.970 | 96% |
| Mathematical Logic | 0.329 | 0.671 | 20% |

**Other numbers.**
- Headline: **ρ = 0.767**, from "our audit of **30 distinct reasoning traces**" (Sec. 5.5 and the Conclusion: "thirty distinct audits").
- The abstract says "violation density (ρ) of **up to 0.77** in factual and scientific domains".
- **These numbers are internally inconsistent:**
  - Table 1 reports 0.92 and 0.96 for the factual and science categories, which is above "up to 0.77".
  - The unweighted mean of the three Table 1 rows is ≈ 0.69, not 0.767.
  - The sample size is given as 500 queries in one place and 30 traces in another.
  - The text says the Table 1 values are "Violation Density (ρ)", but the column is labelled "Violation Rate".
- Case study "audit 7152213f (Global Warming)": S = 0.9698 after a premise negating human-induced climate change was injected.
- Trace length (Sec. 5.4), qualitative only: for General Knowledge, longer traces correlated positively with S, i.e. more reversion to the prior. No coefficient is given.

## 7. Redundancy / overdetermination

**The paper does not discuss redundancy or overdetermination as a legitimate reason for an unchanged answer.** There is no notion of another sufficient support: a second source, a different reasoning path, or correct world knowledge that also entails the answer.

- It does observe self-correction. Sec. 5.5 says: "the agent often identifies the contradiction in subsequent steps (s\*_{k+1}) and reverts to its high-probability parametric prior". It says this behaviour is "beneficial for accuracy" but still "catastrophic for faithfulness", and counts it as a violation.
- The definition in Sec. 2.2 is explicitly necessity-based: "a change in reasoning ι(s_k) ≠ s_k must necessitate a change in the final answer".
- The only hedge is the strength gate in Eq. 6, "λ is the minimum intervention strength required to expect a change in a". It is not operationalised and is not tied to whether the step was load-bearing.
- Sec. 7 admits as future work the need to find "load-bearing" steps via saliency. That implies, without saying it, that some steps are not necessary. But the reported results do not condition on this.

## 8. Authority, delegation, autonomy, escalation, deployment

**There is nothing substantive.** Autonomy appears only as motivation:
- "high-stakes autonomous decision-making" (Abstract)
- "As agentic systems take on more autonomous roles in society, ensuring that their stated logic is the true cause of their actions is a fundamental requirement for AI safety" (Sec. 6)

There are no permissions, no decision classes, no delegation or authorisation rule, no escalation or human-in-the-loop policy, no deployment gate, no risk–coverage analysis and no link to task outcomes in the world. The only downstream use proposed is **φ as a training reward (RLHF/DPO)** and benchmarking "System 2" models such as o1 (Sec. 7).

## 9. Limitations

**Acknowledged by the author.** The paper has no explicit limitations section. Implicitly, Future Work (Sec. 7) concedes:
- only single-node interventions;
- no automatic identification of load-bearing steps;
- no evaluation of reasoning or test-time-compute models.

**Limitations I see:**
1. **Construct validity.** Injecting a false step and observing that the model repairs it and gives the correct answer measures *robustness to injected errors* or *prior strength* as much as unfaithfulness. A good reasoner should often ignore a wrong premise it can check (e.g. that climate change is not human-induced). Treating every invariance as a violation conflates faithfulness with correctness and with redundancy (§7).
2. **Intervening on generated text is off-policy.** The critic-written s'_k is a string the model would not itself produce. Re-sampling after s_k lets the model "notice" the edit. So the experiment tests the response to *tampered context*, not the causal role of the model's own computation. Lanham et al. (2023) discussed similar caveats; Ariadne does not cite them.
3. **Minimal experiment.** One agent model, one intervention type, one position (s₀), and no controls such as resampling noise or a neutral or paraphrase edit. This matters because Eq. 1 includes sampling noise ε, so the baseline S between two unperturbed runs is unknown.
4. **The LLM judge is a black box.** τ_sim, λ and Strength() are unspecified, so V cannot be reproduced. No judge agreement or human check is reported.
5. **Reporting inconsistencies.** The 500 vs. 30 sample sizes, "up to 0.77" vs. 0.92/0.96, and the ρ vs. "Violation Rate" labels (§6). The "Ariadne Score" is undefined.
6. **"Agent" in name only.** There are no tools, environment or actions. The "agentic" framing does not reach multi-step tool-using behaviour.
7. **Citation quality.**
   - Ref [3] gives arXiv:2102.12451, which is an unrelated statistics paper. The intended Wiegreffe & Marasović paper is arXiv:2102.12060, "Teach Me to Explain: A Review of Datasets for Explainable NLP", NeurIPS 2021 Datasets & Benchmarks.
   - Ref [8] (Pelosi et al. 2025, a review of drift explainability) is cited for "interventional faithfulness … when intermediate steps are mutated", which it does not appear to be about.
   - Ref [6] has no authors.
   - There is an unresolved "[?]" in Sec. 2.2.
   - The closest prior work, Lanham et al. 2023, is not cited.
8. **No uncertainty.** No CIs, no significance tests, and an over-strong claim ("proving") from n = 30.

## 10. Related work

### 10a. References Ariadne cites (complete list, as printed, with corrections)

- [1] J. Pearl. *Causality: Models, Reasoning, and Inference*, 2nd ed. Cambridge University Press, 2009.
- [2] A. Jacovi, Y. Goldberg. "Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness?" ACL 2020. The paper prints a truncated title.
- [3] S. Wiegreffe, A. Marasović. Printed as "Explainability for Natural Language Processing: A Survey", arXiv:2102.12451, 2021. **That id and title are wrong.** The correct reference is "Teach Me to Explain: A Review of Datasets for Explainable Natural Language Processing", NeurIPS 2021 (Datasets & Benchmarks), arXiv:2102.12060, which I verified via the arXiv API.
- [4] M. Turpin, J. Michael, E. Perez, S. R. Bowman. "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023. arXiv:2305.04388 (verified).
- [5] K. Meng, D. Bau, A. Andonian, Y. Belinkov. "Locating and Editing Factual Associations in GPT." NeurIPS 2022 (ROME). The paper prints "K. Meng et al."
- [6] "TIR-Bench: A Comprehensive Benchmark for Agentic Thinking," ICLR 2026. No authors are given; I have not verified it.
- [7] A. Geiger, D. Ibeling, A. Zur, M. Chaudhary, S. Chauhan, J. Huang, … T. Icard. "Causal abstraction: A theoretical foundation for mechanistic interpretability." JMLR 26(83):1–64, 2025.
- [8] D. Pelosi, D. Cacciagrano, M. Piangerelli. "Explainability and interpretability in concept and data drift: a systematic literature review." *Algorithms* 18(7):443, 2025. As noted in §9, this looks miscited.

### 10b. Key CoT-faithfulness work Ariadne does NOT cite

We should cite these. All arXiv metadata below was verified via the arXiv API on 2026-10-25.

- **T. Lanham, A. Chen, A. Radhakrishnan, B. Steiner, C. Denison, D. Hernandez, D. Li, E. Durmus, … E. Perez. "Measuring Faithfulness in Chain-of-Thought Reasoning." arXiv:2307.13702, 2023.** This is the direct precedent for Ariadne's method: early answering, adding mistakes to CoT steps and regenerating, paraphrasing, and filler tokens. It already reports task-dependent faithfulness. Ariadne's LogicFlip-at-a-step-then-resample is essentially Lanham's "adding mistakes" test.
- M. Turpin, J. Michael, E. Perez, S. R. Bowman. "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023. arXiv:2305.04388. This one is cited. Note that it intervenes on *inputs* (biasing features such as reordered few-shot answers or a suggested answer), not on the CoT.
- P. Atanasova, O.-M. Camburu, C. Lioma, T. Lukasiewicz, J. G. Simonsen, I. Augenstein. "Faithfulness Tests for Natural Language Explanations." ACL 2023 (short). arXiv:2305.18029. Introduces a counterfactual input editor and reconstruction of inputs from explanations.
- D. Paul, R. West, A. Bosselut, B. Faltings. "Making Reasoning Matter: Measuring and Improving Faithfulness of Chain-of-Thought Reasoning." Findings of EMNLP 2024. arXiv:2402.13950. Uses causal mediation analysis of reasoning steps and introduces the FRODO method.
- Q. Lyu, S. Havaldar, A. Stein, L. Zhang, D. Rao, E. Wong, M. Apidianaki, C. Callison-Burch. "Faithful Chain-of-Thought Reasoning." IJCNLP-AACL 2023. arXiv:2301.13379.
- Y. Chen, J. Benton, A. Radhakrishnan, J. Uesato, C. Denison, J. Schulman, A. Somani, P. Hase, … E. Perez. "Reasoning Models Don't Always Say What They Think." arXiv:2505.05410, 2025. Uses hints in inputs and checks whether the CoT verbalises them.
- K. Matton, R. O. Ness, J. Guttag, E. Kıcıman. "Walk the Talk? Measuring the Faithfulness of Large Language Model Explanations." ICLR 2025 (spotlight). arXiv:2504.14150. Uses counterfactual interventions on **input concepts** and compares the concepts an explanation implies with the concepts that actually have a causal effect. **This is the closest in spirit to WorkTrace's input-side interventions.**
- M. Tutek, F. Hashemi Chaleshtori, A. Marasović, Y. Belinkov. "Measuring Chain of Thought Faithfulness by Unlearning Reasoning Steps." EMNLP 2025 (Outstanding paper). arXiv:2502.14829. A parametric intervention as an alternative to editing text.
- I. Arcuschin, J. Janiak, R. Krzyzanowski, S. Rajamanoharan, N. Nanda, A. Conmy. "Chain-of-Thought Reasoning In The Wild Is Not Always Faithful." ICML 2026. arXiv:2503.08679.

## 11. Verbatim quotes for related work

1. Abstract: "Project Ariadne performs hard interventions (do-calculus) on intermediate reasoning nodes—systematically inverting logic, negating premises, and reversing factual claims—to measure the Causal Sensitivity (ϕ) of the terminal answer."
2. Sec. 2.2: "we can rigorously define faithfulness as causal consistency: a change in reasoning ι(s_k) ≠ s_k must necessitate a change in the final answer a(q) ≠ a_ι(q, k)."
3. Sec. 4.3.2: "An agent exhibits Causal Decoupling—a faithfulness violation—if the answer remains invariant (S → 1) despite a substantive contradiction in the reasoning chain."
4. Sec. 5.5: "When a counterfactual logic node is introduced via Project Ariadne, the agent often identifies the contradiction in subsequent steps (s\*_{k+1}) and reverts to its high-probability parametric prior."
5. Sec. 5.5 (continued): "This behavior, while beneficial for accuracy, is catastrophic for faithfulness. It confirms that the reasoning trace is not a generative constraint but a fluid narrative layer."
6. Sec. 6: "As agentic systems take on more autonomous roles in society, ensuring that their stated logic is the true cause of their actions is a fundamental requirement for AI safety, reliability, and alignment."

## 12. Positioning for WorkTrace

**What Ariadne covers, which we must not claim as new:**
- Framing an LLM's reasoning trace as an SCM with Pearl-style `do()` interventions on reasoning steps.
- Typed contradiction interventions on CoT steps: LogicFlip, FactReversal, PremiseNegation, CausalInversion.
- An answer-invariance metric based on semantic similarity, φ = 1 − S(a, a\*), plus a violation density ρ.
- The empirical observation that answer invariance under CoT perturbation depends strongly on the domain (high for factual and science, low for math).

None of this originates with Ariadne; Lanham et al. 2023 did the substantive version earlier. But we must not present "do-interventions on reasoning to test faithfulness" or "domain-dependent decoupling" as our contribution.

**What Ariadne leaves open:**
1. **Interventions on external evidence.** These include tool outputs, documents and observations, i.e. what the agent was given, rather than what it wrote. Ariadne never touches the environment.
2. **Redundancy and overdetermination.** Ariadne treats any invariance as a violation and explicitly calls correct self-repair "catastrophic for faithfulness". WorkTrace's remove-X / only-X / invert-X / add-second-source design is exactly what is needed to separate a legitimate unchanged answer (another sufficient ground exists) from decoupling.
3. **Declared grounds as a graph, checked against the evidence actually available.** Ariadne has a linear chain of text steps, with no notion of the information available, permissions or consequences.
4. **Anything about authority.** Ariadne has no decision classes, delegation rule, escalation cost, risk–coverage analysis, held-out test of a policy, or comparison with outcome-only rules. Its only downstream use is a training reward.
5. **Rigour.** One model, one intervention type at one position, n = 30 or 500 with inconsistent reporting, no controls and an unspecified judge thresholding. Re-running with proper controls is a real gap. We can cite it carefully as preliminary.

**One-sentence differentiation:** Ariadne asks whether an LLM's *self-generated reasoning text* causally drives its answer, by editing that text. WorkTrace instead asks whether an agent's *action* responds correctly to the *external evidence* it was given, using redundancy-aware interventions on that evidence. It turns this into revocable, per-decision-class grants of autonomy validated on held-out episodes.
