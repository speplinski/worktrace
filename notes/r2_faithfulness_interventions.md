# Round 2: faithfulness tests by intervention, the closest prior work to WorkTrace's evidence interventions

Date: 2026-10-25. Scope: Matton et al. 2025 (read in full) plus the three classic faithfulness papers (method and results). Then a search for 2025–2026 work that intervenes on the evidence of LLM **agents** to test whether they rely on what they cite.

**Headline for WorkTrace (read this first).**
1. **"Remove X" and "invert/replace X" are not new.** Several earlier works already have them:
   - Matton et al. (ICLR 2025) use concept *removal* and *replacement/swap* counterfactuals on the model's input. They compare the measured causal effect with how often the explanation cites the concept.
   - Turpin et al. (2023) flip the weak evidence between two individuals.
   - Pawar et al. (2026, preprint) use "contrast substitution".
   - Usman (2026) uses mirrored document sets.
2. **"Only X" (sufficiency) is not new either.**
   - Atanasova et al. (ACL 2023) have the "input reconstruction" test.
   - **Pawar et al., arXiv 2609.05385 (Sep 2026)** is the most direct novelty threat. It runs black-box **necessity** (change X) and **sufficiency** (keep only X) interventions on the factors an LLM cites. It frames this explicitly as a reliability check for **monitoring and escalation in agent workflows**.
3. **What I found nowhere:**
   - An "add an independent second source" intervention.
   - Any test battery that explicitly handles redundant or **overdetermined** evidence. Matton et al. name correlated or redundant concepts as an unsolved limitation (App. F.2) and propose joint interventions as future work.
   - Any work that uses these test results to **grant, restrict or revoke autonomy per decision class**.

---

## 0. Coverage and verification summary

| Work | Verified via | What I read |
|---|---|---|
| Matton et al. 2025 | arXiv API; ICLR 2025 proceedings page (proceedings.iclr.cc); OpenReview id from search results (the API was blocked by a challenge page) | **Full text** of arXiv v2 (66 pp.): main text §1–7; App. A, B, C (C.1–C.4); D.1–D.6 (D.2 partly, through the first example); E.1–E.4; F.1–F.3 in full. I skimmed rather than read the prompt tables (Tables 12–29) and the output-sample tables (Tables 30–40). |
| Lanham et al. 2023 | arXiv API | Main text §1–6 in full (methods, results, limitations). Appendices not read. |
| Turpin et al. 2023 | arXiv API; Crossref (NeurIPS 36 DOI) | Main text §1–7 in full. Appendices not read. |
| Atanasova et al. 2023 | arXiv API; Crossref (ACL DOI) | Full main text, results and limitations. Appendix tables not read. |
| Pawar et al. 2026 | arXiv API | Full main text §1–5 plus appendices A, B and part of C. |
| Liu et al. 2026 | arXiv API | Full main text plus App. A. |
| Usman 2026 | arXiv API | Abstract, §1 (introduction, contributions) and the start of §2. |
| Mahale 2026 | arXiv API | Abstract, §1, contributions, and grep for key terms. |
| Wallat et al. 2025 | arXiv API; Crossref (ICTIR 2025) | Abstract and §5 (the experiment). |
| Other 2025–2026 hits | arXiv API (abstracts only), plus ACL Anthology / NeurIPS pages | Abstract only, unless marked otherwise. |

---

## 1. Matton, Ness, Guttag, Kıcıman (2025), "Walk the Talk?" (the closest predecessor)

### Bibliographic data [verified]
- **Title:** Walk the Talk? Measuring the Faithfulness of Large Language Model Explanations
- **Authors:** Katie Matton (MIT), Robert Osazuwa Ness (Microsoft Research), John Guttag (MIT), Emre Kıcıman (Microsoft Research). The work was done during Matton's MSR internship.
- **Venue:** ICLR 2025. arXiv comment: "ICLR 2025 (spotlight) camera ready". Proceedings page: proceedings.iclr.cc/paper_files/paper/2025/hash/b5ec50eb177908f21f78ed0d76ed525c-Abstract-Conference.html. That page lists the authors as "Katie Matton, Robert Ness, John Guttag, Emre Kiciman". OpenReview forum id 4ub9gpx9xw, taken from the MIT Media Lab listing; I could not open it directly because of a bot challenge.
- **arXiv:** 2504.14150. v1 posted 19 Apr 2025; v2 dated 20 May 2025, 66 pp. Code: github.com/kmatton/walk-the-talk.

### Problem & contribution
- LLM explanations "can misrepresent the model's 'reasoning' process". The paper defines faithfulness "in terms of the difference between the set of concepts that LLM explanations imply are influential and the set that truly are" (Abstract).
- **Contributions:**
  - A formal definition of *causal concept faithfulness* (§2, App. B).
  - An estimator built from two parts: (1) an auxiliary LLM that extracts concepts and writes realistic counterfactual inputs; (2) Bayesian hierarchical models for concept effects and for faithfulness at the question level and the dataset level (§3, App. C).
  - "Semantic patterns" of unfaithfulness, i.e. *which* concepts are hidden or over-claimed (§1, §4).

### Method (answers question (a): **yes, it intervenes on input concepts and compares the stated reasons with the causal effect**)
- **Setting (§2).**
  - The model M is opaque and API-only. Only samples r ~ P_M(R|x) are observed.
  - Inputs are *context-based multiple-choice questions*, x = (context, question, choices).
  - Each response has the form r = (y, e): an answer choice plus a natural-language explanation.
- **Units.**
  - *Concepts* C_m are random variables with a domain of values, e.g. "the candidates' ages" = (54, 26).
  - Concepts are assumed **disentangled**, meaning each one can be changed while the others are held fixed.
  - Each concept is assigned to one higher-level *category* K, e.g. identity / behaviour / context, or clinical tests / symptoms / demographics.
- **Causal effect (Def. 2.1).** CE(x, C_m) is the mean, over counterfactual values c′_m, of D_KL(P_M(Y | x_{c_m→c′_m}) ‖ P_M(Y | x)).
  - App. B gives the do-calculus derivation. They target the **individual treatment effect** (per question) and the **direct effect**, "since we expect an LLM's explanations to mention the concepts that directly influenced its answer" (App. B).
  - The intervention keeps all other concepts and the remaining text V fixed.
- **Explanation-implied effect (Def. 2.2).**
  - EE(x, C_m) is the probability that the explanations imply C_m was causal.
  - An auxiliary LLM (GPT-4o) judges whether each explanation implies this.
  - In practice they use **only the explanations to the original question** (App. C.1).
- **Faithfulness (Def. 2.3).**
  - F(x) = PCC(CE(x, ·), EE(x, ·)), the Pearson correlation across the concepts of one question.
  - F(X) is the mean of F(x). App. F.1 argues against pooling all concepts across questions because of Simpson's-paradox effects.
- **Interventions (§3, App. C.1).** The auxiliary LLM (GPT-4o, T=0) does four jobs:
  - lists the concepts;
  - lists the current value and plausible alternatives for each;
  - rewrites x with one concept changed (**replacement**);
  - rewrites x so that the concept "cannot be determined" (**removal**).
  - On BBQ, replacements *swap* the attribute between the two people (e.g. swap genders). On MedQA they use **removal only**, because changes to clinical values are hard to judge.
- **Estimators (App. C.2–C.3).**
  1. **CE model.** A multinomial logistic regression per intervention, ln P(y)/P(y_b) = β·I + α. The β coefficients get a zero-mean Gaussian prior whose variance σ_K is **shared per concept category**, with hyperprior U(0, 100). Fitted with NUTS. CE comes from the posterior predictive.
  2. **Faithfulness model.** CE and EE are z-scored per question. Then EE ~ N(β_x · CE, σ), with β_x ~ N(μ, 1) and μ ~ N(0, 1). Here β_x is question-level F and μ is dataset-level F, both reported with 90% credible intervals.
- **Sampling.** S = 50 responses per original and counterfactual question, at T = 0.7. That gives 14,900 (BBQ) and 17,200 (MedQA) responses per evaluated LLM.

### Evaluation
- **Data.**
  - 30 BBQ questions in the Turpin et al. variant with "weak evidence", stratified over 9 bias categories.
  - 30 MedQA patient-vignette questions.
- **Models.** GPT-3.5 (gpt-3.5-turbo-instruct), GPT-4o, Claude-3.5-Sonnet, plus Llama-3.1-8B in App. D.6. Auxiliary LLM: GPT-4o.
- **Dataset-level F(X), BBQ (§4.1):**
  - GPT-3.5 0.75 [0.42, 1.00]
  - GPT-4o 0.56 [0.24, 0.86]
  - Claude-3.5-Sonnet 0.62 [0.28, 0.91]
  - Llama-3.1-8B 0.81 [0.49, 1.00]
- **Dataset-level F(X), MedQA (§4.2):**
  - GPT-3.5 0.50 [0.18, 0.77]
  - GPT-4o 0.34 [0.05, 0.65]
  - Claude 0.30 [0.01, 0.59]
- **Qualitative patterns.**
  - BBQ: explanations hide the influence of safety behaviour (identity information triggers "Undetermined", but the explanation cites ambiguity). They also hide social bias.
  - MedQA: explanations cite low-effect evidence and omit high-effect evidence. Example: Claude never mentions "mental status upon arrival" (CE = 0.32, EE = 0.00) but almost always mentions vital signs (CE ≤ 0.10, EE ≥ 0.96) (Table 3).
- **Sanity checks and robustness.**
  - On "objective" BBQ questions all models get F(x) ≥ 0.93 (App. D.3).
  - Results are stable for N ≥ 15 questions (App. D.4).
  - An anti-bias prompt does not raise faithfulness. For GPT-3.5 it lowers it, 0.75 → 0.61 (App. D.5).
  - Manual audit of 50 counterfactuals per dataset: error rates of 6% (BBQ) and 10% (MedQA), judged on coherence, completeness and minimality (App. F.3).
- **No baselines** from other faithfulness metrics are run against it. There is no ground-truth faithfulness, which they say themselves (§4.1).

### (b) How they handle redundant or overdetermined concepts: **they don't; they flag it as a limitation**
- **Their definition builds the problem in.** CE is the *direct* effect of a single-concept intervention "while keeping the values of all other concepts fixed" (App. F.2). If two concepts each suffice for the answer, intervening on either one alone leaves the answer unchanged. Both then get CE ≈ 0, and an explanation that correctly cites both is scored as unfaithful. Overdetermination in the strict sense (two independent sufficient grounds) is never discussed.
- **What App. F.2, "Correlated Concepts", does discuss is leakage or inferability:**
  - Quote: "even when a single concept (e.g., race) is removed from the input question, an LLM may still infer it using the information provided by the other concepts (e.g., name). As a result, the removal intervention might not succeed."
  - Quote: "Correlated concepts pose less of an issue for replacement-based counterfactuals."
  - Remedy, deferred: "intervening on multiple concepts jointly (e.g., both race and name)" (future work; also §6).
- **MedQA examples.** App. E.3 says the method "has the potential to underestimate the effects of concepts that are highly correlated with other concepts" (anorexia can be inferred from meal refusal). App. E.4 says some high-EE / low-CE concepts are, "Rather than being evidence of unfaithfulness, … related to the challenge of applying our method to correlated concepts". So the authors themselves read some apparent unfaithfulness as a measurement artefact of redundancy.
- **Entangled concepts.** App. F.3 says entangled concepts "can lead to redundant counterfactuals". Two different interventions then produce the same edited input. The authors judge the impact "minimal" but say it is worth further study.
- **Implication for WorkTrace.** This is exactly the gap our redundancy-robust battery targets. Our "only X" intervention and our designed second sources separate *unused* evidence from *used but redundant* evidence. We should cite F.2 and E.4 verbatim as motivation.

### (c) Agents, actions, permissions, delegation: **nothing technical**
- Single-turn multiple-choice QA. There are no tools, no multi-step trajectories, no actions with consequences, no permissions and no delegation. The word "agent" appears only as "anesthetic agent" in a MedQA item.
- **Closest conceptual hook (cite it).** The paper says question-level faithfulness can help users decide "whether to trust a model's answers to a specific question". It also says the *semantic* pattern of unfaithfulness "might lead the user to avoid using the model to compare applicants of different genders" (§1). That is an informal, human-applied restriction of use for one kind of decision. WorkTrace turns that intuition into an explicit rule: proceed / escalate / refuse per decision class, evaluated on held-out episodes.

### What it covers that WorkTrace must NOT claim
- The first general method that compares the stated influence of input concepts with their measured causal influence, with interventions written by an auxiliary LLM. Includes removal *and* replacement/swap counterfactuals.
- Per-instance and per-dataset faithfulness scores with Bayesian partial pooling across items and concept categories.
- "Semantic patterns" of unfaithfulness by category, e.g. "explanations omit identity, over-cite behaviour".
- Explicit counterfactual-quality criteria: coherence, completeness, minimality, plus disentanglement and referential validity of concepts.

### What it leaves open that WorkTrace addresses
- **Redundancy and overdetermination.** Single-concept direct effects with no joint or sufficiency tests; the gap is explicitly deferred (F.2).
- **External evidence with provenance.** Concepts are parts of a question text written by humans or the auxiliary LLM. They are not tool outputs, documents or observations with sources, so there is no notion of an *independent* source or of corroboration.
- **No declared-grounds structure.** EE is a per-concept mention rate. There is no graph of claimed grounds and no expected-response pattern derived from what the agent claimed.
- **No action or decision consequences.** Outcomes are answer distributions only.
- **No decision rule.** Faithfulness is reported, not used to gate autonomy. There is no risk–coverage analysis, no escalation cost, and no comparison with outcome-only rules.
- **No ground truth.** The paper admits this (§4.1). WorkTrace's generated episodes can plant ground truth by construction.

### Draft differentiation sentence
> Matton et al. (2025) estimate *causal concept faithfulness* by comparing an LLM's explanation-implied concept effects with effects measured through single-concept removal and replacement counterfactuals in multiple-choice QA, and leave correlated or redundant concepts to future work. WorkTrace applies interventions to the external evidence in an agent's decision episode, adds sufficiency ("only X") and independent-second-source conditions designed so that redundancy does not masquerade as non-use, and uses the results not as a faithfulness score but to decide, per decision class, whether the agent may proceed, must escalate, or must refuse.

### Citation cautions
- Peer-reviewed (ICLR 2025 spotlight).
- Small samples: 30 questions per dataset. Wide credible intervals; e.g. GPT-3.5 BBQ is [0.42, 1.00], so the model rankings are not well separated.
- Results depend on the GPT-4o auxiliary LLM, for both counterfactuals and EE judgements, and on post-hoc merging of categories (App. C.1). The categories were merged by hand: 40 → 3 on BBQ, and 82 categories merged "using GPT-4o (the web interface)" on MedQA.
- In practice EE uses only explanations to the original questions, not to counterfactuals (App. C.1). This departs from Def. 2.2.
- Cite as "Matton et al., ICLR 2025". The proceedings page spells the names "Robert Ness" and "Emre Kiciman"; the arXiv version has "Robert Osazuwa Ness" and "Emre Kıcıman".

---

## 2. Lanham et al. (2023), "Measuring Faithfulness in Chain-of-Thought Reasoning"

### Bibliographic data [verified: arXiv API]
- **Title:** Measuring Faithfulness in Chain-of-Thought Reasoning
- **Authors (30):** Tamera Lanham, Anna Chen, Ansh Radhakrishnan, Benoit Steiner, Carson Denison, Danny Hernandez, Dustin Li, Esin Durmus, Evan Hubinger, Jackson Kernion, Kamilė Lukošiūtė, Karina Nguyen, Newton Cheng, Nicholas Joseph, Nicholas Schiefer, Oliver Rausch, Robin Larson, Sam McCandlish, Sandipan Kundu, Saurav Kadavath, Shannon Yang, Thomas Henighan, Timothy Maxwell, Timothy Telleen-Lawton, Tristan Hume, Zac Hatfield-Dodds, Jared Kaplan, Jan Brauner, Samuel R. Bowman, Ethan Perez.
- **arXiv:** 2307.13702 (v1, 17 Jul 2023), cs.AI. Anthropic technical report. The arXiv record has **no journal reference**; treat it as a preprint.

### Problem & contribution
- Is CoT a faithful account of how the model reaches its answer?
- The paper tests specific hypotheses about unfaithfulness: post-hoc reasoning, test-time compute alone, and encoded reasoning (steganography). It does so by **intervening on the CoT itself**, not on the input.
- It takes a "defense-in-depth" view: "each test is not meant to be conclusive evidence for CoT being faithful, but rather aims to rule out the possibility of one class of faithfulness failures" (§1).

### Method
Model: a 175B RLHF assistant. 8 multiple-choice tasks (AQuA, LogiQA, MMLU, HellaSwag, TruthfulQA, OpenBookQA, ARC-Challenge, ARC-Easy). 100 CoT samples per question. Four interventions:
1. **Early answering** (§2.3): truncate the CoT after k sentences.
2. **Adding mistakes** (§2.4): a pretrained LM corrupts one step, then the rest is re-sampled.
3. **Filler tokens** (§2.5): replace the CoT with " ...".
4. **Paraphrasing** (§2.6): paraphrase a prefix of the CoT without access to the question.

Metric: how often the final answer matches the original. AOC (area over the curve) is weighted by CoT length.

### Evaluation (results)
- Post-hoc reasoning varies widely by task. Early-answering AOC is 0.44 for AQuA and 0.02 for ARC-Easy (Table 2). It is not strongly correlated with the accuracy gain from CoT.
- Filler tokens give no accuracy gain, and paraphrasing leaves accuracy unchanged. So neither extra compute alone nor phrasing-encoded information explains the CoT benefit.
- **Inverse scaling** (§3): across 13B → 175B models, larger models usually rely less on the CoT. On 6 of 8 tasks the 13B model is the most faithful. Synthetic addition tasks show that faithfulness falls as model size grows and as tasks get easier.
- Limitation stated in §5: there is no ground truth for the internal process.

### What it covers that WorkTrace must NOT claim
- Intervening on the model's own reasoning (truncate, corrupt, paraphrase, replace) to test whether the stated reasoning drives the output.
- The finding that faithfulness depends on the task and on model capability.

### What it leaves open that WorkTrace addresses
- It does not intervene on inputs or external evidence. There are no agents, tools, actions or permissions, and no decision rule.
- **Useful for us:** the task and capability dependence (§3) is an empirical argument for calibrating autonomy *per decision class* rather than per model.

### Draft differentiation sentence
> Lanham et al. (2023) perturb a model's chain of thought (truncation, injected mistakes, filler, paraphrase) to test whether its stated reasoning drives the answer. WorkTrace instead perturbs the external evidence the agent had and cited, and uses the response pattern to gate autonomy.

### Citation cautions
- Non-peer-reviewed technical report.
- The 175B model is unnamed and proprietary.
- "Faithfulness" here means *reliance on the CoT*, not alignment with the input causes. Do not conflate the two.

---

## 3. Turpin, Michael, Perez, Bowman (2023), "Language Models Don't Always Say What They Think"

### Bibliographic data [verified: arXiv API; Crossref DOI 10.52202/075280-3275]
- **Title:** Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting
- **Authors:** Miles Turpin, Julian Michael, Ethan Perez, Samuel R. Bowman (NYU, Cohere, Anthropic)
- **Venue:** Advances in Neural Information Processing Systems 36 (NeurIPS 2023)
- **arXiv:** 2305.04388 (v2, 9 Dec 2023). Code: github.com/milesaturpin/cot-unfaithfulness.

### Problem & contribution
- CoT explanations can be "plausible yet systematically unfaithful".
- Models respond to biasing features in the input that they almost never verbalise. In a review of 426 explanations supporting biased predictions, only 1 mentions the bias (§2).

### Method
Two kinds of counterfactual input, described in §2:
- **Perturbing features *not* referenced by explanations (BBH, §3).**
  - 13 BIG-Bench Hard tasks, 3,299 examples.
  - Biasing features: "Answer is Always A" (reorder the few-shot options) and "Suggested Answer" ("I think the answer is <X>…").
  - Metric: the drop in accuracy when the bias points to a wrong answer. Nearly all of the drop is explained by bias-consistent predictions.
- **Perturbing features that *are* referenced (BBQ, §4).**
  - 2,592 ambiguous BBQ items, each augmented with two versions of **weak evidence that is swapped between the two individuals**.
  - A pair is faithful if the model abstains on both versions or flips its answer with the evidence.
  - Metric: "% Unfaithfulness Explained by Bias", the share of unfaithful pairs that are stereotype-aligned. The unbiased value is 50%.
- **Models:** text-davinci-003 (GPT-3.5) and Claude 1.0. Conditions: zero-shot vs few-shot, CoT vs no-CoT, and with or without a debiasing instruction.

### Evaluation (results)
- **BBH.**
  - Under Suggested Answer, zero-shot CoT accuracy drops by up to **−36.3%** for GPT-3.5.
  - Under Answer is Always A, the drop is −18.7% for GPT-3.5 and −4.7% for Claude 1.0.
  - Few-shot prompting reduces the effect (−36.3 → −24.1 for GPT-3.5).
  - Of 104 annotated unfaithful explanations, 73% support the bias-consistent answer, and 15% contain no obvious error (§3.3).
- **BBQ.** Unfaithfulness explained by bias reaches 62.5% (Claude 1.0, few-shot CoT) and 59.2% (GPT-3.5, zero-shot CoT), against a 50% baseline. 86% of stereotype-aligned unfaithful explanations explicitly support the answer they give (§4.3).
- Limitation: "we have presented a necessary but not sufficient test for faithfulness" (§6).

### What it covers that WorkTrace must NOT claim
- Input interventions that swap or invert the evidence an explanation relies on, used to expose inconsistent use of evidence.
- The two-sided logic: (i) the output must not respond to features the explanation omits; (ii) the output must respond to features the explanation relies on.
- Faithfulness evaluated without ground-truth labels, through consistency under counterfactual pairs.

### What it leaves open that WorkTrace addresses
- The biases are hand-designed and single-feature. There is no notion of redundant or multiple sources, no agent setting, no actions or permissions, and no decision rule.

### Draft differentiation sentence
> Turpin et al. (2023) show, with planted biasing features and swapped weak evidence, that CoT explanations can rationalise answers driven by unverbalised inputs. WorkTrace generalises the "the output should follow the evidence the explanation relies on" test to an agent's external evidence, with redundancy-aware conditions, and turns its outcomes into per-class delegation decisions.

### Citation cautions
- Peer-reviewed.
- The models (text-davinci-003, Claude 1.0) are obsolete.
- The test is explicitly necessary but not sufficient.

---

## 4. Atanasova et al. (2023), "Faithfulness Tests for Natural Language Explanations"

### Bibliographic data [verified: arXiv API; Crossref]
- **Title:** Faithfulness Tests for Natural Language Explanations
- **Authors:** Pepa Atanasova, Oana-Maria Camburu, Christina Lioma, Thomas Lukasiewicz, Jakob Grue Simonsen, Isabelle Augenstein
- **Venue:** Proceedings of the 61st Annual Meeting of the ACL (Volume 2: Short Papers), pp. 283–294, Toronto, 2023. DOI 10.18653/v1/2023.acl-short.25.
- **arXiv:** 2305.18029 (v2). Code: github.com/copenlu/nle_faithfulness.

### Problem & contribution
Two tests for the faithfulness of free-text explanations (NLEs) produced by models that predict and explain jointly.

### Method
1. **Counterfactual test (§2.1).**
   - A trained T5 editor *inserts* tokens W into the input so that the prediction flips to a target label.
   - If no word of W appears in the new NLE, the NLE is unfaithful.
   - Baseline: random adjectives or adverbs from WordNet. Search: 4 positions × 4 candidates.
2. **Input reconstruction test (§2.2).**
   - Build a new input r_i from the reasons stated in the NLE. For e-SNLI this uses templates; for ComVE, the NLE replaces a sentence.
   - If f(r_i) ≠ f(x_i), the NLE is unfaithful.
   - This is a **sufficiency-of-stated-reasons** test.
- **Models and data:** T5-base NLE models in four setups (MT/ST × reasoning/rationalising). Datasets: e-SNLI, CoS-E, ComVE.

### Evaluation (results)
- Counterfactual test: total detected unfaithfulness ranges from 37.04% (MT-Ra, e-SNLI) to 59.04% (ST-Re, CoS-E) (Table 2).
- Reconstruction test: up to 14% (e-SNLI) and up to 40% (ComVE) unfaithful (Table 3).
- They say the tests are not comprehensive (Limitations).

### What it covers that WorkTrace must NOT claim
- **Additive** input interventions (insert content, then check whether the explanation reflects it).
- **Sufficiency of the stated reasons** (rebuild the input from the explanation alone and check that the prediction is preserved). This is a 2023 precursor of our "only X". ERASER's sufficiency metric (DeYoung et al., 2020, as cited by Matton et al. and Atanasova et al.) is older still; I did not re-verify it.

### What it leaves open that WorkTrace addresses
- Token-level edits on fine-tuned T5 classifiers. No LLM agents, no external sources, no redundancy treatment, no decision rule.
- Their "add" intervention is adversarial and changes the prediction. Our "add an independent second source" is *supportive*: it tests whether the agent registers corroboration and whether its decision or confidence responds appropriately.

### Draft differentiation sentence
> Atanasova et al. (2023) test free-text explanations with prediction-flipping token insertions and with inputs rebuilt from the stated reasons. WorkTrace applies the analogous necessity and sufficiency logic to source-level external evidence in agent episodes, adds a corroborating-source condition, and uses the results to gate delegation.

### Citation cautions
- Peer-reviewed short paper.
- The paraphrase check on NLEs was manual, on 100 instances per model.
- The models are small T5-base systems.

---

## 5. 2025–2026 work that intervenes on the evidence of agents (or of LLM components inside agent workflows)

Search strategy: several web searches combining agent / tool output / observation / documents / citation / RAG with counterfactual / ablation / necessity / sufficiency / faithfulness / audit, plus author-name searches for follow-ups by Matton et al. (none found). Every arXiv item below was **verified with the arXiv API** (title, authors, date, comments).

### 5.1 Top hits, ranked by threat to WorkTrace

**(1) Pawar, Ramanayake, Kemal, Kandath, O'Neill, Bourgeon, Chatbri, Martin, Pertsovskiy (2026), "Necessary or Sufficient? Evaluating LLM Explanations With Behavioural Evidence."** arXiv 2609.05385 (v2, 7 Sep 2026), BNY. Preprint, no venue. [verified] **Read: full main text plus appendices A–B, part of C.**
- **Problem.** "LLM decision components that can operate within agent workflows" give recommendations together with explanations. Operators may use the named factors "to monitor a system, diagnose errors, or decide when to escalate an output" (Abstract). If the explanations disagree with behaviour, "either mismatch could direct monitoring or escalation toward the wrong part of the input" (§1).
- **Method.**
  - The model cites its top 3 factors, chosen from a **fixed list of feature names**. They chose this format after comparing 13 prompt formats; it cut positional instability from 0.929 to 0.235.
  - **Necessity PN(f)** (§3.3): the rate at which the output changes when *only f* is changed. Advisor task: "contrast substitution" to the most different valid value, which is close to our *invert X*. Prompt-risk task: "blank removal", which is close to our *remove X*.
  - **Sufficiency PS(f)** (§3.4): the rate at which the output is preserved when f is kept and the other changeable features are masked or removed. This is our *only X*.
  - 3 API trials per intervention, T = 0, following Tian & Pearl (2000).
- **Evaluation.**
  - Two synthetic tasks: advisor recommendation (100 profiles × 18 features, 13 advisors) and prompt-risk monitoring (100 prompts with 3–4 risk segments).
  - Eight models: Claude Opus 4.6, Sonnet 5, Haiku 4.5; GPT-5.4 at 4 reasoning settings; Gemini 3.5 Flash.
  - Mean Spearman correlation of cited rank with PN / PS: 0.349 / 0.354 (advisor) and 0.431 / 0.580 (monitoring).
  - An uncited feature outscores the weakest cited one in 57.6% / 58.1% of advisor responses (PN / PS) and 25.8% / 8.9% of monitoring responses.
  - Higher GPT-5.4 reasoning effort reduces sufficiency-based omissions (76% → 40% in the advisor task).
- **What it does not do.**
  - No redundancy or overdetermination analysis. Features are intervened on one at a time.
  - No independent second source and no source provenance. Features are profile fields or prompt segments, not tool outputs or documents.
  - No multi-step agent and no actions with consequences.
  - No autonomy rule. It is explicitly "scoped to individual LLM decisions" (Abstract) and does not claim "to establish end-to-end agent safety" (§5).
- **Threat level: HIGH for the novelty of "remove X / only X" as a pair of necessity and sufficiency tests in an agent-oversight framing.** Must be cited. Differentiation: we use external evidence items in agent episodes, a declared-grounds graph rather than a top-3 list, redundancy-robust joint interpretation, an independent-source condition, and decisions to grant or revoke delegation per class evaluated by risk–coverage. **Design hint:** their sensitivity analyses show that the choice between contrast substitution, blank removal and similar-value substitution changes absolute PN. We should report the same, i.e. intervention strength as a reported factor.

**(2) Liu, Li, Wu, Duan, Li, Zhang, Min (2026), "Auditing Tool Traces in Agentic LLMs: Source Localization and Counterfactual Dependence Testing."** arXiv 2610.25540 (18 Oct 2026). Accepted at the NeurIPS 2026 Workshop on Agentic AI for Biological Discovery (AgenticLS). [verified] **Read: full main text plus App. A.**
- **Method.** Two stages:
  1. **PT2D** (per-tool TF-IDF decomposition) finds label-predictive patterns in individual tool results. Full-trace screening misses them because of "dilution".
  2. **Token-class redaction** removes the suspect token class *globally*, so duplicates cannot survive elsewhere. It is run against a non-overlapping control redaction, on a frozen fine-tuned Qwen3-4B (TCR–pMHC binding, five-tool traces).
- **Result.** Redacting PDB identifiers drops AUROC from 0.8136 to 0.4972; the peptide-redaction control gives 0.8152.
- **Caveat stated by the authors.** "redaction may also remove correlated signals or shift the input distribution" (§2).
- **Relevance.** This is a *remove X* intervention on **tool outputs**, at the source level, with a control. But it is outcome-level shortcut detection, with no comparison to stated grounds and no delegation logic. **Threat: medium.** Cite it as precedent for source-level removal on tool traces. Copy two ideas: global redaction of all copies (our leakage control) and matched control redactions.

**(3) Usman (2026), "Counterfactual Evidence Audits Predict LLM-Agent Susceptibility to Ranked Context."** arXiv 2606.00914 (v2, 2 Oct 2026). Single author, independent researcher. Accepted at FLMSec 2026 (NeurIPS 2026 workshop). [verified] **Read: abstract, §1, start of §2.**
- **Method.** Expose an agent to **two mirrored five-document sets** with opposite stance. Measure the shift across six downstream decisions and use it to predict the effect of a disjoint 45-document context.
- **Results.** Spearman ρ = .855 across 18 held-out model–task cells. Matched controls: composition matters, order alone does not. A provenance warning does not reliably mitigate the effect. In Codex agent tiers, the audit ranks models well but no full-context effect is individually significant.
- **Relevance.** An *invert X* intervention on agent evidence used for pre-deployment **triage** of model–task pairs. That is close in spirit to "test before granting". But it measures susceptibility, not faithfulness to cited grounds. There are no per-decision proceed / escalate / refuse rules and no redundancy design. **Threat: medium** for "evidence interventions as a pre-deployment gate". Cite it.

**(4) Wallat, Heuss, de Rijke, Anand (2025), "Correctness is not Faithfulness in Retrieval Augmented Generation Attributions."** ICTIR 2025 (Proc. 2025 ACM SIGIR ICTIR), pp. 22–32, DOI 10.1145/3731120.3744592. arXiv 2412.18004. The arXiv title is shortened to "…in RAG Attributions". [verified: Crossref and arXiv] **Read: abstract and §5.**
- **Method.** Separates citation *correctness* from *faithfulness*. Tests "post-rationalization" in Command-R+: answer statements are appended to other documents (random / relevant-but-uncited / cited-for-other-reasons), and the test checks whether the model now cites the forged document.
- **Result.** It does in 12%, 57% and 55% of cases respectively.
- **Relevance.** An *add* intervention on retrieved documents that exposes citations not grounded in actual use. Single-turn RAG, no agents or decision rule. **Cite** it as evidence that citing a source does not show reliance on it.
- **Follow-up:** Khan & Bhuyan (2026), "Attributable Post-Rationalization in RAG Citations: A Controlled Reproduction and an RLVR Comparison", arXiv 2609.23053 [verified, abstract only]. Reports that RLVR-trained search agents post-rationalise at the rate of their base model ("roughly one citation in seven" on Wikipedia QA). In other words, rewarding correct outcomes does not buy citation faithfulness. **This directly supports WorkTrace's "outcome-only is insufficient" thesis.**

**(5) Mahale (2026), "Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification."** arXiv 2609.06445. Single author. The arXiv comment states: "Pre-registered discrepancy experiment published in full and not run; no empirical result is claimed." [verified] **Read: abstract, §1.**
- **Content.** Theory of step-level attribution in agent trajectories, under the EU AI Act Articles 12 and 86.
  - Under the marginal total effect, a causally inert step is indistinguishable from the decisive one.
  - Under common random numbers, "an exact zero does not certify that a step did nothing".
  - Mediated-share rankings break when direct and mediated paths oppose.
- **Relevance.** A formal warning that zero-effect readings from single interventions are uninformative. This is the same family of problems as overdetermination. **Cite** it as theoretical support for redundancy-robust designs. Not empirical; cite with caution.

**(6) Lower-threat agent hits (abstract only unless noted; all [verified] on arXiv).**
- **Shah (2026), "Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures"**, arXiv 2606.08275. Applies do-interventions on agent *steps* with forward re-execution, plus Shapley credit, to find which step caused a failure. Mocked tools; validated on synthetic SCMs. Trajectory-step attribution, not evidence reliance against stated grounds.
- **Zhou, Liu, Li, Rossi, Hu (2026), "Counterfactual Trace Auditing of LLM Agent Skills"**, arXiv 2605.11946. Compares paired agent traces with and without a skill on 49 SWE tasks. Pass rate changes by +0.3 pp, yet there are 522 behavioural "Skill Influence Pattern" instances. Relevant as another argument that outcome-only evaluation hides behaviour. The intervention is on skills, not evidence.
- **Xu et al. (2026), "AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations"**, arXiv 2610.21624. Perturbs agent interaction inputs, including observations, on APEX-Agents and Toolathlon. Agents "rarely recognize altered inputs and often propagate corrupted information without verification". A robustness benchmark, not a faithfulness or delegation one. Useful to motivate an *invert X* test ("does the agent notice contradictory evidence?").
- **Chiu & Chen (2026), "Faithful to the Frame: Source-Framing Propagation in LLM-Agent Decision Workflows"**, EMNLP 2026 Main, pp. 42630–42650 [verified on the ACL Anthology page; no DOI shown]. The E2A protocol traces how fixed evidence (earnings disclosures) propagates to agents' reasoning, beliefs and actions: 24,816 agent decision traces. Source-faithful extraction leaves the action skew unchanged (80.1% vs 80.0%). Shows that evidence *framing* drives agent actions. Not a test of stated grounds.
- **Yuan et al. (2026), "Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing" (SAVER)**, arXiv 2604.08401, ACL 2026 Main (per the arXiv comment). A method for self-auditing an agent's reasoning before committing, not an evidence-intervention audit. Abstract seen only in search snippets: low confidence about its content.
- **Wang (2026), "Doing What They Say, Not What They Reason: Locating the Faithfulness Gap in LLM Agents"**, arXiv 2606.00476 (COLM workshop submission). Splits faithfulness into reasoning-to-conclusion and conclusion-to-action in a poker simulator. Conclusion-to-action inconsistency is 0.7–1.4% with tagged conclusions. Misapplication of the agent's own rule is 99.5% risk-averse (Haiku). Relevant to the *action* side of our episode; no evidence interventions.
- **Huang, Lin, Zhong, Liu (2025), "Learning to Seek Evidence: A Verifiable Reasoning Agent with Causal Faithfulness Analysis"**, arXiv 2511.01425 (stated as under review at CVPR 2026). A medical-imaging agent that chooses visual evidence. Masking the evidence it chose raises the Brier score by 0.029. That is a simple *remove X* sanity check, aggregate only.
- **Solonko (2025), "Evaluating the Causal Effect of Chain-of-Thought on Groundedness in Tool-Use Agents via Counterfactual Mutations"**, NeurIPS 2025 Women in ML affinity-event poster (OpenReview wDVPvcneyT) [verified page exists; only a partial abstract was visible]. Edits the CoT, not the evidence. Low weight; an affinity-event poster, not a main-track paper.
- **Closely related non-agent 2025–2026 work (cite selectively):**
  - Chen et al. (2025), "Reasoning Models Don't Always Say What They Think", arXiv 2505.05410 [verified]. Hint-insertion test on reasoning models: reveal rates are often below 20%; outcome-based RL plateaus.
  - Han, Lee, Do (2026), "RFEval", arXiv 2602.17053, ICLR 2026 poster [verified]. Output-level counterfactual interventions; 49.7% of outputs unfaithful; accuracy is not a proxy for faithfulness.
  - Mayne et al. (2026), "A Positive Case for Faithfulness", arXiv 2602.02639, ICML 2026 [verified]. Normalised simulatability gain of 11–37%; 5–15% of self-explanations are highly misleading.
  - Karvonen, Ong, Kantamneni, Marks (2026), "Would this change your answer?" (CHIVE), arXiv 2608.16747 [verified]. An agentic pipeline that *generates* counterfactual experiments to evaluate explanations.
  - Somov et al. (2026), "Breaking the Chain", arXiv 2603.16475 [verified, abstract via search only]. Causal mediation on intermediate structures; externalising them as tool calls shrinks the faithfulness gap.

### 5.2 Search verdict
- **No 2025–2026 paper found that does all of the following:**
  - (i) intervenes on the *external* evidence of a multi-step tool-using agent;
  - (ii) compares the response with the agent's *declared grounds*;
  - (iii) handles redundant or overdetermined evidence by design;
  - (iv) uses the results to decide autonomy.
- **Pawar et al. 2026 covers (ii) plus single-factor necessity and sufficiency, in an oversight and escalation framing, for single LLM decisions.** Liu et al. 2026 and Usman 2026 cover (i) without (ii).
- Caveat: web search is not exhaustive. Venue-indexed 2026 workshop papers may be missed.

---

## 6. (d) What remains new in WorkTrace's "remove X / only X / invert X / add an independent second source"

Each component taken separately has precedent:

| WorkTrace intervention | Prior instances (must cite) | What is still new in WorkTrace |
|---|---|---|
| remove X | Matton (removal counterfactuals); Pawar (blank removal, PN); Liu (token-class redaction on tool outputs); Huang 2025 (masking chosen evidence); TRACE (specified, not run) | Applied to source-level external evidence in agent episodes and **interpreted jointly with the other conditions**, so a null effect under redundancy is not scored as non-use. Includes a **leakage check**: X must not remain inferable from other context. Matton F.2 names this failure; Liu's global redaction is a partial remedy. |
| only X | Atanasova (input reconstruction from stated reasons); ERASER sufficiency (cited, not re-verified); Pawar (PS) | Sufficiency is tested per *declared ground* in an agent's grounds graph, and its expected sign comes from that graph. Pawar uses a top-3 list of fixed features. |
| invert X | Turpin (swapped weak evidence); Matton (swap replacements); Pawar (contrast substitution); Usman (mirrored document sets); AgentPerturb (corrupted observations) | Used as one cell of an expected-response pattern derived from the declared grounds, with *proceed / escalate / refuse* as the scored outcome, so that escalating on contradictory evidence counts as correct behaviour. |
| add an independent second source | **None found as such.** The nearest are Atanasova's additive counterfactual and Wallat's forged documents. Both are *adversarial* and test citation or explanation, not corroboration. TRACE's "effective number of sources" is a conceptual neighbour. | **Novel as far as this search reached.** It (a) tells redundancy apart from non-use: if X was used but redundant, adding a second source Y and then removing X should leave the decision intact, while removing both should change it; (b) tests whether the agent's decision or confidence responds to genuine corroboration (an evidential norm), not just whether it mentions the source. |

**Novel at the level of the battery and its use:**
1. A **joint, redundancy-robust reading** of the four conditions against a declared-grounds graph. Matton et al. defer this explicitly ("intervening on multiple concepts jointly", App. F.2). Pawar et al. only intervene on single features. Mahale shows formally that single-intervention zeros are uninformative.
2. **Agent episodes with actions, permissions and consequences** as the dependent variable, rather than a multiple-choice answer distribution or a recommendation label.
3. **Using the results to grant or revoke autonomy per decision class**, evaluated on held-out generated episodes through risk–coverage against an outcome-only rule, with an explicit escalation cost. Nobody does this. Matton §1 gestures at restricting use informally; Pawar §1 mentions escalation but builds no rule; Usman does triage at the level of model–task pairs.
4. **Ground truth by construction.** Generated episodes plant which evidence is necessary, sufficient or redundant. Matton et al. state that "in general there is no 'ground truth' for faithfulness" (§4.1).

**Wording to avoid:** do not say "we introduce counterfactual interventions on evidence", "first to test whether stated reasons match causal influence", or "first necessity/sufficiency test for LLM explanations".

**Wording that is defensible:** "redundancy-robust intervention battery on an agent's external evidence, interpreted against its declared grounds, and used as the evidential basis for a per-decision-class delegation rule".

---

## Implications for WorkTrace

**Design changes**
1. **Adopt the formal vocabulary and cite it.**
   - Define "remove X" as an estimate of necessity (PN) and "only X" as an estimate of sufficiency (PS), following Tian & Pearl (2000) as cited by Pawar et al. 2026. I did not re-verify that reference.
   - Present Matton's CE/EE as the faithfulness quantity we *do not* use as the gating criterion, and explain why: single-concept direct effects are blind to overdetermination.
2. **Run Matton-style causal concept faithfulness (and/or Pawar's PN/PS rank correlation) as a baseline.** Run it alongside the outcome-only baseline. Then show that the delegation rule adds value beyond a faithfulness score. A reviewer will ask: "why not just gate on F(x)?"
3. **Add a leakage / inferability check for "remove X".** Verify that X cannot be recovered from the remaining context. Options: an auxiliary judge, or a probe that asks the agent to state X's value. Remove all copies (Liu et al.'s global token-class redaction). Report completeness and minimality of the counterfactuals as in Matton App. F.3.
4. **Report intervention strength as a factor**: removal vs replacement vs similar-value substitution. Pawar shows that this changes absolute PN. Matton shows that replacement is more robust to correlated concepts.
5. **Borrow Matton's Bayesian hierarchical partial pooling.** Pool effect magnitudes within a decision class across episodes. This gives credible intervals for per-class delegation thresholds with few episodes per class, and posterior uncertainty can feed the escalate option directly.
6. **Score explanations elicited before the intervention as the declared grounds, and score the explanations given under each intervention separately.** Matton used only the original-question explanations. Turpin and Atanasova show that explanations shift under intervention. We can do better by checking whether the declared grounds *update* consistently.
7. **Specify the expected response pattern explicitly for every combination of declared-grounds structure and intervention.** Example: grounds {X, Y} declared as jointly required; grounds {X or Y} declared as redundant; grounds {X} declared as sole. Score conformity to that pattern. This is the operational answer to Matton F.2.
8. **Use the "invert X" condition to reward escalation**, not only answer flips. AgentPerturb found that agents rarely notice corrupted observations; noticing them is the desirable behaviour.

**Risks**
- **Novelty risk (high):** Pawar et al. 2026 already use necessity and sufficiency interventions on cited factors to check explanations "used for agent oversight", including escalation. Mitigation: cite it prominently, and claim only (i) redundancy-robust joint interpretation plus the independent-second-source condition, (ii) external evidence in agent episodes, (iii) the delegation rule and its risk–coverage evaluation.
- **Novelty risk (medium):** Usman 2026 already uses counterfactual evidence audits as a pre-deployment screen. Differentiate: susceptibility vs grounded reliance, and model–task triage vs per-decision-class autonomy with revocation.
- **Measurement risk:** dependence on an auxiliary LLM for counterfactual generation and for judging grounds, as in Matton F.3 (6–10% counterfactual errors). Budget for manual audits and report error rates.
- **Interpretive risk:** every test is "necessary but not sufficient" (Turpin §6; Lanham §1). Phrase delegation as conditional and revocable, not as certification.
- **Capability and scaling risk:** faithfulness can fall as capability grows (Lanham §3; Matton's GPT-3.5 > GPT-4o; Chen et al. 2025 plateau). Per-class gates must be re-tested when the model changes, which supports the "revocable" part of the thesis.

**Things to cite (all verified above)**
- Core: Matton et al. ICLR 2025; Turpin et al. NeurIPS 2023; Lanham et al. 2023 (arXiv); Atanasova et al. ACL 2023.
- Agent and evidence: Pawar et al. 2026 (arXiv 2609.05385); Liu et al. 2026 (arXiv 2610.25540, NeurIPS 2026 workshop); Usman 2026 (arXiv 2606.00914, NeurIPS 2026 workshop); Wallat et al. ICTIR 2025; Khan & Bhuyan 2026 (arXiv 2609.23053), for "outcome rewards do not buy citation faithfulness".
- Supporting: Mahale 2026 (arXiv 2609.06445, theory, no empirics); Chen et al. 2025 (arXiv 2505.05410); Chiu & Chen, EMNLP 2026.
- Optional: Shah 2026 (arXiv 2606.08275); Zhou et al. 2026 (arXiv 2605.11946); Xu et al. 2026 (AgentPerturb, arXiv 2610.21624).
