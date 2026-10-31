# R3: Outcome–process gap benchmarks (CXBench, PAE, GroundEval, AgentLens)

Reading note for WorkTrace, round 3. Written 2026-10-25.

**Scope.** These four benchmarks measure correct outcomes reached by a defective process. They already cover our old H1, and CXBench overlaps our banking domain. The note answers five questions: (a) what each one means by "process" and how it judges it; (b) CXBench's banking tasks compared with our counterparty-verification pilot; (c) how to run H1′ with a PAE/CXBench-style procedure audit as a second detector; (d) whether any of them defines a construct like DSA; (e) differentiation sentences.

---

## 0. Bottom line (threats first)

1. **None of the four falsifies W1, W2 or W3. None defines a construct with the content of DSA.** None of them uses interventions on the agent's evidence, models redundancy, has ground truth on which evidence is decisive, or uses its results to grant or withdraw authority.
2. **W2 must be narrowed.** "Ground truth by construction" is not ours as a general phrase:
   - CXBench builds outcome ground truth from hidden customer facts in LLM-synthesised tasks.
   - GroundEval derives the ground truth for "is this evidence path permitted" from a deterministic simulator (OrgForge).

   Our claim must be specific: ground truth about **which evidence is decisive, and about the redundancy structure, i.e. the expected response pattern under remove / only / invert / add-second-source**. Neither outcome ground truth nor permitted-evidence ground truth is ours.
3. **GroundEval uses gating language close to W3.** Abstract: "Before letting an agent operate over real context, can you prove it used the right evidence?" §1.4 adds "usable as regression gates across model versions". It has no per-class rule, no revocation, no risk–coverage evaluation and no interventions. It must still be cited where we motivate W3, or a reviewer will raise it.
4. **The DSA construct is partly occupied, facet by facet, not as a whole.** Existing labels and named axes cover:
   - authority scope: CXBench tool permissions and submission authority; PAE I_pc;
   - provenance: PAE I_df and I_ec; GroundEval citation and visibility checks;
   - "verify before claiming absence" (an uncertainty or boundary facet): GroundEval Silence track;
   - over-escalation: PAE counts "unnecessary transfers to human agents" as a policy-compliance violation (App. 0.C).

   DSA survives only if we map each facet to these prior metrics explicitly and claim as new only:
   - the intervention-tested grounding facet, redundancy-aware;
   - revision after correction;
   - recognition of decision points;
   - per-class profiling used for delegation.
5. **Banking overlap is real but narrow.** CXBench's banking domain is **US Regulation E consumer EFT error resolution**: disputes, ATM errors, unauthorised ACH debits. Its process checks are disclosures, ordering, confirmation and authentication. Our pilot is **EU AMLR legal-entity counterparty verification**: beneficial ownership, register discrepancies, sanctions, PEPs. The decisions differ:
   - In CXBench the correct action is fixed by the customer's request and hidden facts.
   - In ours it is fixed by the content of external evidence.

   The single direct overlap is **authority of the person acting** (our P2). It mirrors CXBench's insurance "reporter-authority check" and its banking "session_context_before_read".
6. **H1′ is feasible as a three-detector study.** The procedure-audit detector can be defined operationally (§4) from CXBench's hybrid grader plus PAE's integrity invariants. The main risk is a straw-man audit. We mitigate it with **scripted known-answer agents**, which give ground truth on the agent's *basis* by construction, to validate both detectors before applying them to LLM agents (§4.4).
7. **Correction to r2_agent_evaluation.md.** The τ-bench sentence that CXBench cites does exist. τ-bench (arXiv:2406.12045v1) §3, "Reward": "r=1 might be a necessary but not sufficient condition for a successful episode e.g., the agent might issue the return without explicit user confirmation, which violates the policy." The r2 note said it could not be found.

---

## 1. What was read

| Work | Version read | Parts read |
|---|---|---|
| CXBench | arXiv v1 HTML (2026-10-19), plus PDF v1 for figure text (Figs 1, 3, 4) and the Fig. 6 heatmap image | **Everything:** §1–§6, Limitations, Ethics, Apps A–H. The Fig. 5 domain heatmap was not inspected; its numbers are in Table 10. |
| PAE | arXiv v1 HTML (2026-03-03) | **Everything:** §1–§6, Apps 0.A–0.F, all case studies. |
| GroundEval | arXiv v2 HTML (2026-07-02; v1 2026-06-22) | **Everything in v2:** §1–§11. v1 not read. The v2 comment reads "Streamlined entry point into framework". |
| AgentLens | arXiv v4 HTML (2026-10-05) | **§1–§7 and Apps A–F.** Category-by-model table rows (App. D.4) and the D.6/D.7.1–D.7.3 case texts only skimmed. Figures not inspected. |

---

## 2. Per-paper notes

### 2.1 CXBench

**Bibliographic data.** Boxi Yu, Yuzhong Zhang, Zhenfeng Su, Linfu Xi, Yinghan Yao, Shitao Chen, Yang Cao, Liting Lin, Lionel Briand, Emir Muñoz. "CXBench: A Benchmark for Process-Compliant LLM Agents in Regulated Customer-Experience Workflows." arXiv:2610.25954v1, 2026-10-19, cs.AI. Licence of the paper: CC BY 4.0.
- **[verified]** arXiv API.
- **[verified]** OpenReview: "ICLR 2027 Conference Desk Rejected Submission" (forum edhc5pD8Sh).
- Affiliations: Lero/University of Limerick, CUHK-Shenzhen, Xi'an Jiaotong, Peking, SCUT, Genesys Cloud Services. Co-funded by Genesys.

**Problem & contribution.** "Existing tool-agent benchmarks largely score final business states, accepting trajectories that reach correct outcomes through non-compliant processes" (Abstract). Contributions:
1. Separate outcome and process verdicts and a **false-pass** metric: r_false_pass = r_outcome ∧ ¬r_process (§2.4).
2. **Rule cards** linking a cited statute to applicability, required behaviour, observable trace evidence and a criterion (§2.2, App. B).
3. A shared runtime with **mediated submission**: the agent drafts, the customer confirms, the runtime submits. A direct-submit ablation is included (§2.3, App. C.3).

**Method.**
- **Task.** θ=(g, m₀, s₀, U, Λ, K), with a POMDP formalisation (App. A.2). The state is (business_state, private_facts, history, drafts).
  - The agent sees the opening message, agent-facing policy, permitted tools, customer replies and tool results.
  - Hidden customer facts drive the LLM customer simulator (gpt-5.4-mini) and the outcome checker (Table 6).
- **Tools.** Five categories: read, check, draft, notice, submit (App. C.1). In mediated mode, submit tools are removed from the agent's action set; a blocked attempt is logged and checked by `no_agent_direct_submit`.
- **What "process" means.** Procedural obligations, in four rule categories (Table 8):
  - pipeline gates (draft→confirm→submit);
  - domain ordering (e.g. "reading a policy summary before checking reporter authority");
  - disclosure gates ("required disclosures before designated customer-confirmation events");
  - semantic prohibitions (unsupported outcome promises, collecting secrets, unlawful disconnection threats).

  In short: **procedure, ordering, disclosure and authority. Not evidence dependence.**
- **Judging.** r_process = r_rule ∧ r_judge.
  - 53 deterministic hard rules cover ordering, tool permissions and confirmed-vs-submitted agreement.
  - An LLM judge (gpt-5.6-sol) works through a task-specific checklist and returns findings {rule_id, passed, severity, seq, evidence}. Any failed finding, regardless of severity, fails the judge component (App. D.3–D.4).
  - Humans did not produce the reported verdicts. One expert labelled 120 calibration traces (App. H.4).
- **Ground truth.** Outcome ground truth comes from hidden facts: "a filed dispute whose relevant fields match the specified customer facts" (App. D.1).
  - Process ground truth is the authors' encoding of 55 obligations, extracted from the Legal Information Institute and deduplicated into 53 rule cards.
  - Tasks are LLM-synthesised from rule cards plus an interface manifest, then pass four structural gates (App. E.3) and review by three senior *software-engineering* experts (not lawyers).
- **Interventions.** None on evidence. The only manipulation is the submission-authority ablation: mediated vs direct submit, for gpt-5.4 only.
- **Domains.** Banking, telecom, insurance, healthcare, utilities, government benefits; 20 tasks each, 120 in total.

**Evaluation.**
- **Scale.** 7 models × 120 tasks = 840 retained records, one execution per pair, no retries except on network failure.
- **Headline.**
  - Outcome-pass 69.29% (582/840).
  - Both-pass 13.81% (116).
  - False-pass 55.48% of all runs (466), which is 80.07% of outcome-passes (§4.1, App. D.5).
  - Model order changes; 6/21 Holm-corrected pairwise comparisons are significant.
- **By domain (Table 10, outcome / both / false-pass):**

  | Domain | Outcome-pass | Both-pass | False-pass |
  |---|---|---|---|
  | Banking | 94.29% | 5.71% | 88.57% |
  | Government benefits | 84.29% | 4.29% | 80.00% |
  | Healthcare | 13.57% | 2.14% | 11.43% |
  | Insurance | 80.71% | 17.86% | 62.86% |
  | Telecommunications | 67.14% | 26.43% | 40.71% |
  | Utilities | 75.71% | 26.43% | 49.29% |

- **Who catches what.** Of 466 false-passes, 329 are caught only by the judge, 38 only by hard rules and 99 by both (§4.2). 35 of 53 hard rules fail at least once.
- **Submission ablation (gpt-5.4).**
  - Under the original grader, both-pass falls from 20.83% to 0.83%.
  - After removing the submission-mechanism checks, it is 18.33% vs 20.83% (McNemar p=0.68; bootstrap CI [−10, 5] pp). The authors call the original gap "scoring-sensitive" (§4.3, App. G.3).
- **Judge robustness.** Swapping in gpt-6-astra on 720 traces gives 92.22% verdict agreement and Kendall τ_b=0.966.
- **Judge vs expert, gpt-5.6-sol on 120 development traces:**
  - accuracy 88.33%;
  - process-pass precision 69.70%, recall 85.19%;
  - process-fail precision 95.40%, recall 89.25%.

  The authors state these traces are "not an independent held-out validation set" (§3, App. H.4).

**What it covers that WorkTrace must NOT claim.**
- The false-pass concept, separate outcome and process verdicts, and the statement that outcome-only scoring overestimates reliability in *regulated banking* workflows.
- Statute-linked rule cards that tie an obligation to required trace evidence.
- Hybrid deterministic-plus-checklist-judge grading in which any failed finding fails.
- Runtime-mediated execution of the state-changing action as an authority control, with an ablation that hands that authority to the agent.
- LLM synthesis of regulated tasks from rule cards, with hidden facts and structural validation.
- Model re-ranking once process is included.

**What it leaves open that WorkTrace addresses.**
- "Process" is procedural. It never asks whether the *decision* depended on the evidence that should warrant it. In banking, the expected action follows from the customer's request and hidden facts; there is no "evidence that should flip the decision".
- No interventions, no redundancy, no decisive-evidence labels, no held-out generation (there is one fixed set of 120 tasks), no repeated runs per task.
- Submission authority is fixed by mode, not earned or revoked. The ablation covers one model, and the authors' rescoring finds no significant effect of authority once mode-specific checks are removed.
- No human held-out validation of the judge.

**Draft differentiation (one sentence).** "CXBench separates outcome from statute-linked procedural compliance and finds that 80% of outcome-passes in regulated customer-service workflows miss an encoded obligation; WorkTrace targets a failure that a procedure audit cannot see by construction, namely a decision whose trace satisfies every procedural check but whose action does not change when the evidence that should determine it is removed, inverted or corroborated."

**Citation cautions.**
- Desk-rejected at ICLR 2027; v1 only; one run per model–task pair.
- Judge calibrated on development traces, labelled by a single expert, with no inter-rater reliability. Rule mappings were reviewed by software engineers, not lawyers.
- The authors themselves disclaim legal compliance: "not by itself an adjudicated finding of legal non-compliance" (§2.4).
- Internal inconsistencies:
  - App. E.3 says the calibration compared "gpt-6-astra judgments with the expert labels", while §4.4 and H.4 report gpt-5.6-sol.
  - Fig. 3 shows a "disclose 10-day confirm right" card, while the text's running example is the written-confirmation notice under §1005.11(b)(2).
  - §4.3 and App. G.3 say the direct-submit comparison used "the same 120 recorded traces; neither the agent nor the customer simulator was rerun". It is unclear how a different execution mode can share traces. Treat the authority ablation as a **rescoring**, not a behavioural experiment, until clarified.
- The rule-failure heatmap (Fig. 6) lists rule identifiers but not their domains. My domain attributions below are inferences.
- Model names (gpt-5.4, gpt-5.6-sol, gpt-6-astra, glm-5.1, qwen3.6-plus, deepseek-v4-flash) are as given in the paper.

### 2.2 PAE: Procedure-Aware Evaluation ("corrupt success")

**Bibliographic data.** Hongliu Cao, Ilias Driouich, Eoin Thomas (all Amadeus France). "Beyond Task Completion: Revealing Corrupt Success in LLM Agents through Procedure-Aware Evaluation." arXiv:2603.03116v1, 2026-03-03, cs.AI. CC BY 4.0.
- **[verified]** arXiv API.
- **[verified]** OpenReview holds only a "CoRR 2026" record; no venue.

**Problem & contribution.** "Current benchmarks evaluate mainly whether a task was completed, not how" (Abstract). **Corrupt success** is "an agent may reach the correct terminal state while violating mandatory constraints" (§2.2). PAE formalises a procedure and gates utility on six semantic checks.

**Method.**
- **Formalisation.** F=(E, A, O, T, Ω), Dec-POMDP-inspired (§3.1).
  - Tripartite agent action: Read / Write / Communicate.
  - Observations split into O^ctx (policy, tool schemas), O^sys (tool returns) and O^comm (dialogue).
- **What "process" means.** Four **integrity invariants**, each a consistency pair (§3.2, Eqs 5–8):

  | Invariant | Consistency pair | Formal definition |
  |---|---|---|
  | I_pc, policy compliance | O^ctx ↔ A | "∀t: A_t satisfies O^ctx" |
  | I_pf, policy faithfulness | — | "policy claims in A^C_t ⊆ O^ctx" |
  | I_ec, execution consistency | — | "action claims in A^C_t ↔ (A^R_t, A^W_t)" |
  | I_df, data faithfulness | — | "data in A^C_t ⊆ O^sys_≤t" |

  Interaction-quality checks are added: I_intent, I_qf, I_tone, I_id, I_pii.
- **Gated utility.** U′ = U·I_pc·I_pf·I_ec·I_df·I_intent·I_qf (Eq. 9).

  In short, process means **policy conformance of actions and faithfulness of what the agent *says* to what it observed and did**. The integrity checks cover statements, not the dependence of actions on evidence.
- **Judging.** An LLM judge (GPT-5), given "the policy, task groundtruth information and the entire procedure transcripts". It returns turn-level attributions and typed error codes (App. 0.B), e.g. HARMFUL_DISALLOWED_EXECUTION, DISALLOWED_DECISION, MISSING_REQUIRED_CHECK, POLICY_HALLUCINATION, DATA_HALLUCINATION, CLAIMED_NOT_EXECUTED.
  - Automatic proxy: excess actions against the expected action set confirm >89%.
  - Human spot-check: 150 assessments, 89.3% correct.
  - Manual check of all 131 airline corrupt successes: precision 93.8–95.2%.
- **Interventions.** None.
- **Ground truth.** τ-bench's own task annotations (expected DB state, expected actions, NL assertions).
- **Domains.** τ-bench retail and airline; GPT-5, Kimi-K2-Thinking and Mistral-Large-3 as agents; GPT-4.1 as user simulator; k=4 trials.

**Evaluation.**
- **Corrupt share of successes** (Table 3): about 27% for GPT-5 (retail 0.79→0.58; airline 0.60→0.44) and 76% / 78% for Mistral. This is the "27–78%".
- **Reliability.** Gated Pass^4 ≤0.24 for every model–domain pair.
- **Ranking.** Kimi and Mistral swap places in retail.
- **Error mix.** Per-model error profiles (Table 4).
- **Benchmark flaws exposed.** Scope gaps, contradictory reward signals, and simulator ###STOP### artifacts that produce "accidental successes" (§5.2; Cases 28, 39, 63).

**Two cases matter for WorkTrace.**
- **Case 5, "Gaslighting Agent" (App. 0.F.1).** The agent retrieved `"membership": "regular"`, then passed the user's false "Gold member" claim to a human as verified. PAE: "preferring the user's conversational assertion over structured evidence … the agent appears to be doing everything correctly (it retrieved data, followed escalation protocol, and produced a professional summary)". This is a **basis error that PAE catches only because the wrong basis leaked into a communication** (I_df=0). Had the agent acted silently on the false claim, PAE's statement-level invariants would have had nothing to compare.
- **Case 3, "Wrong Reservation Entirely" (Kimi).** Premature closure: the agent stopped after three of five reservations and acted on the wrong one; the outcome was still scored correct. This is an evidence-search failure caught by I_df and I_intent because the summary stated the wrong route.

**What it covers that WorkTrace must NOT claim.**
- "Corrupt success" and gated utility, i.e. success disqualified by any integrity violation.
- Consistency checks between observations, statements and actions, including "statements grounded in observed tool data".
- Multi-axis profiles in place of one score.
- Penalising unnecessary escalation inside a process audit ("Unnecessary transfers to human agents" under I_pc, App. 0.C).
- Per-model failure signatures.

**What it leaves open that WorkTrace addresses.**
- Its own Limitation 2 (§6): "PAE is a behavioral audit and cannot surface reasoning-level errors in agents that happen to produce correct outputs through flawed inference." The fix it proposes is logging reasoning traces, not intervening on evidence.
- I_df checks that *communicated* data appear in observations. It does not check that the *action* depends on the right observation.
- Binary, unweighted gates. Explicit policy needed (Limitation 1). No interventions, no redundancy, no held-out generation, no delegation.

**Draft differentiation.** "PAE gates success on consistency between what an agent observed, said and did, and explicitly cannot detect correct outputs reached through flawed inference; WorkTrace tests exactly that residual by intervening on the evidence the action should depend on, which also exposes basis errors that never surface in the agent's statements."

**Citation cautions.**
- Preprint, no venue. The judge (GPT-5) evaluates GPT-5 as one of the agents; self-preference is not discussed.
- The judge receives ground-truth task information, so it is not reference-free.
- Manual validation covers airline only. Three models, two domains.
- "The full evaluation code will be open-sourced" (§4.1); no release found.
- Percentages are per model and domain; do not quote "27–78%" as a pooled rate.

### 2.3 GroundEval

**Bibliographic data.** Jeffrey Flynt (independent researcher). "GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation." arXiv:2606.22737; v1 2026-06-22, v2 2026-07-02 (read). CC BY 4.0.
- **[verified]** arXiv API.
- No OpenReview record found.
- Code: github.com/tenurehq/groundeval. The repository is reachable, but no LICENSE file was found at the root of `main` and the README does not mention a licence, so its **licence is unverified**. Absent a licence, assume all rights reserved.

**Problem & contribution.** **"State-invalid correct"**: "its final answer matches the expected label or world state, but the answer is produced from evidence that violates the evaluation state", for example artifacts outside the actor's visibility cone, after the as-of time, in inaccessible subsystems, with insufficient search over declared absence spaces, or with unsupported causal claims (§1.2). The contribution is a reviewed, machine-checkable **task contract** (required checks, allowed evidence, temporal boundary, access policy, answer schema), scored without an LLM judge.

**Method.**
- **Observe Mode** drafts the contract from an observed agent run; a human corrects it (§3.1).
- **Determinism properties** P1–P3 (§4). P3, "Bounded scope", restricts evaluation to evidence-path violations.
- **Three tracks (§5):**
  - *Perspective*: could actor X have known Y as of time t? This defines a visibility cone over time × role.
  - *Counterfactual*: a **question type** about cause and effect in the event log, with join keys. It is **not** an intervention on the agent's inputs. Naming caution: do not confuse it with our interventions.
  - *Silence*: the agent must search a declared space before claiming absence.
- **Scoring (§6).** Dual answer and trajectory score with track weights 0.4/0.6, 0.5/0.5 and 0.3/0.7, and a compliance factor (1−v)².
- **Leakage controls (§5.4).** The prose LLM is label-blind; questions containing answer leaks are rejected; caps per actor and event type; balanced cases; global shuffle; a deterministic template fallback.
- **What "process" means.** **Validity of the evidence path**: access, time, search coverage, causal join. It asks whether evidence was *permitted and sufficient to look at*, not whether the action *depended* on it.
- **Judging.** Deterministic, against the contract. LLM judges appear only as a contrast in one example.
- **Interventions.** None.
- **Ground truth.** OrgForge simulator (by the same author): 22,530 events, 72 actors, 9 subsystems; "none are inferred post hoc".
- **Domain.** Synthetic enterprise.

**Evaluation.**
- **Scale.** 96 questions (30 Perspective, 27 Counterfactual, 39 Silence); one model (DeepSeek-V4-Pro); a zero-shot no-artifact floor.
- **Answer scores** (Table 5):

  | Track | Zero-shot answer | Gated answer | Gated trajectory |
  |---|---|---|---|
  | Perspective | 0.200 | 0.214 | 0.637 |
  | Counterfactual | 0.220 | 0.063 | 0.357 |
  | Silence | 0.487 | 0.359 | 0.421 |

  **In two of three tracks the agent with tools answers worse than the zero-shot floor.**
- **Combined.** Overall S_adj = 0.350 (Table 6).
- **Worked examples.** Three (§8.1–8.3), **all with wrong answers**. **No rate of state-invalid correct answers is reported**, although the abstract says "Our case studies suggest this failure mode is common".

**What it covers that WorkTrace must NOT claim.**
- The concept of a correct answer reached through an invalid evidence path.
- Deterministic, judge-free scoring of evidence paths against access, time and search-coverage contracts.
- "What the actor could have known at time t" as part of the evaluation state. This overlaps our episode field "information available at decision time".
- "Verify before claiming absence" as a measured behaviour.
- The framing of evidence-path tests as a precondition before letting an agent act, and as regression gates.

**What it leaves open that WorkTrace addresses.**
- Evidence *access* validity is not evidence *dependence*. An agent that fetched every required artifact passes the trajectory check even if its decision ignores them. That is precisely the CSS case of "retrieving the same chart sections" without updating.
- No interventions, no redundancy, no measured prevalence of state-invalid correctness.
- No delegation rule. "Gate" is meant as a regression test across model versions, not as authority per decision class.

**Draft differentiation.** "GroundEval checks deterministically whether the evidence an agent touched was permitted, in time and sufficiently searched; WorkTrace checks whether the agent's action actually depends on the decisive evidence by intervening on it, and turns per-class results into revocable decision rights."

**Citation cautions.**
- Single-author preprint; n=96 questions, one model.
- The headline example is a wrong answer (S_ans=0.000, S_adj=0.191), whereas the abstract says "a GroundEval score of 0.000". It does not demonstrate state-invalid *correctness*.
- The claim that the failure is "common" is unquantified.
- The gated answer scores below zero-shot suggest question-phrasing leakage or tool harm. Cite it as a conceptual precedent only.

### 2.4 AgentLens ("Lucky Pass")

**Bibliographic data.** Priyam Sahoo, Gaurav Mittal, Xiaomin Li, Shengjie Ma, Benjamin Steenhoek, Pingping Lin, Yu Hu (UIUC; Microsoft). "AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation." arXiv:2605.12925; v1 2026-05-13, v4 2026-10-05 (read), cs.SE. CC BY 4.0.
- **[verified]** arXiv API.
- **[verified]** OpenReview: "FAGEN@ICML 2026 Poster".
- **Name collision.** "AgentLens: Visual Analysis for Agent Behaviors in LLM-Based Autonomous Systems" (IEEE TVCG 2025) is a different paper. Always cite with the arXiv id.

**Problem & contribution.** Binary SWE-bench pass/fail "treats a principled solution and a chaotic trial-and-error process as equivalent". A **Lucky Pass** is a passing trajectory with a low process-quality score (<47 on 0–100). The contributions are AgentLens-Bench (1,815 trajectories, 47 task-level reference graphs) and a five-category taxonomy of Lucky Passes.

**Method.**
- **Intent stages.** A deterministic, context-sensitive labeler assigns each step to Exploration, Implementation, Verification or Orchestration (§3.1, App. B.3).
- **Reference.** A task-level **Prefix Tree Acceptor** built from k=5 *other* passing trajectories (§3.2).
- **Score.** 0.20·structural alignment + 0.15·set coverage + 0.30·coherence + 0.35·temporal profile, with weights grid-searched on a disjoint 278-trajectory pilot set. Tiers: Ideal ≥70, Solid 47–70, Lucky <47.
- **What "process" means.** **Behavioural process quality**: phase ordering, verification, waste (blind retries, regression loops), and deviation from known-good paths. The norm is *other successful agents' behaviour*, not an evidential or regulatory standard.
- **Judging.** Deterministic rules; no LLM. Humans validated only the intent-stage labels (7 annotators, 2 of them LLMs; Fleiss κ=0.933 on 200 states). **The Lucky labels themselves have no human validation.**
- **Interventions.** None.
- **Ground truth.** SWE-bench tests for outcome; the PTA for process.
- **Domain.** OpenHands on SWE-bench Verified; 8 model backends; 60 tasks.

**Evaluation.**
- **Tiers among passing trajectories.** Of 1,136 passing trajectories: Lucky 10.7% (122), Solid 69.1%, Ideal 20.2%.
- **By model.** Lucky shares range from 0.5% to 23.2%; ranks move by up to 5 positions.
- **Taxonomy:**

  | Category | Share of Lucky Passes |
  |---|---|
  | C1 Minimal & Unverified | 15.6% |
  | C2 Brute-Force Convergence | 34.4% |
  | C3 Incomplete Implementation | 33.6% |
  | C4 Excessive Exploration | 4.1% |
  | C5 Divergent-but-Valid | 12.3% |

  C5 is admittedly a false positive of structural comparison, so the "truly weak" share is about 9.4% of passes.
- **Signals.** 94.3% of Lucky Passes lack verification. Pass/fail AUROC is 0.766, below individual-trajectory matching at 0.805.

**What it covers that WorkTrace must NOT claim.**
- The "lucky pass" label and the measurement of weak-process passes in coding agents.
- Model re-ranking by process quality.
- Missing verification as the dominant weak-success signal.

**What it leaves open that WorkTrace addresses.**
- Process quality is judged against a behavioural norm, which cannot tell "did the right things in the wrong order" from "did the right things but ignored the result".
- No evidence-dependence tests, no interventions, no decisions over external evidence, no delegation.
- Its own Broader Impacts: "not as an automatic approval mechanism for deploying code changes".

**Draft differentiation.** "AgentLens labels passing SWE-agent trajectories as lucky when their behaviour deviates from other successful trajectories; WorkTrace replaces the behavioural reference with generated ground truth about which evidence should determine each decision, and tests that dependence experimentally."

**Citation cautions.**
- Workshop poster. Release of the code and dataset is "planned".
- The 10.7% depends on a pilot-calibrated threshold, and the Lucky labels are not human-validated.
- The PTA reference is built from passing trajectories of the same model pool, which favours majority strategies (the authors acknowledge this via C5).

---

## 3. Comparison table (question a)

| | CXBench | PAE | GroundEval | AgentLens | **WorkTrace** |
|---|---|---|---|---|---|
| Name for the gap | false-pass | corrupt success | state-invalid correct | Lucky Pass | *correct but unjustified action* (proposed) |
| "Process" means | statute-linked procedure: ordering, disclosure, confirmation, authority/permissions, prohibited promises | policy compliance of actions; faithfulness of statements to policy, observations and executions; intent | validity of the evidence path: access, time horizon, search coverage, causal join | behavioural process quality: phases, verification, waste, deviation from known-good paths | **dependence of the action on the decisive external evidence**, redundancy-aware |
| Judged by | 53 hard rules ∧ checklist LLM judge; humans for calibration only | LLM judge (GPT-5) given ground-truth info; human spot checks | deterministic contract (human-reviewed draft) | deterministic score vs PTA; humans validate stage labels only | deterministic, from generator labels and intervention runs; judge only for the procedure-audit comparator |
| Intervention used | none on evidence; submission-authority ablation (rescoring) | none | none ("Counterfactual" is a question type) | none | remove / only / invert / add independent second source |
| Ground truth built from | hidden customer facts (outcome); authors' rule cards (process); LLM-synthesised tasks | τ-bench annotations | OrgForge simulator plus reviewed contract | SWE-bench tests; PTA from other passes | generator knows decisive evidence and redundancy structure |
| Gap quantified | yes: 55.5% of runs, 80.1% of outcome-passes | yes: 27–78% of successes | **no** | yes: 10.7% of passes | target: H1′ estimand (§4) |
| Domains | banking (Reg E), telecom, insurance, healthcare, utilities, government benefits | τ-bench retail, airline | synthetic enterprise | SWE-bench Verified | counterparty verification (AMLR), Auditable Design |
| Uses result for autonomy | no; authority fixed by mode | no | "regression gates", "before letting an agent operate" (no rule) | no ("not … an automatic approval mechanism") | yes: per-class proceed / escalate / refuse |

---

## 4. CXBench in detail vs our counterparty pilot (question b)

### 4.1 What its banking domain contains (from the text; the task files themselves are not available)
- **Scenario family.** "eft_error_resolution" on business system `banking_customer_ops_v0`.
- **Named examples:**
  - BK-RAW-008.us, ATM incorrect amount: USD 60 dispensed, USD 100 debited. Oral notice; the institution requires written confirmation.
  - The Fig. 4 task, an unauthorised ACH debit. Source refs `reg-e-error-resolution-1005-11-r001` and `reg-e-liability-1005-6-r001`.
- **Tools** (Table 9: 6 read, 5 check, 3 draft, 4 notice, 2 submit). Named ones:
  - read: `get_session_context`, `get_transaction_detail`;
  - check: `classify_eft_error`, `check_reg_e_notice_timing`;
  - draft: `create_eft_dispute_draft`;
  - notice: `record_reg_e_timeline_disclosure`;
  - submit: `submit_eft_dispute_case`.
- **Process requirements** (Fig. 4c, Listing 1):
  - "read transaction, classify error, check notice timing";
  - "do not promise credit, reversal, or investigation result";
  - inform the customer of the written-confirmation requirement and address under 12 CFR 1005.11(b)(2);
  - "Submit only the confirmed draft".
- **Hard rules** named for banking: `session_context_before_read`, `draft_before_confirmation`, `confirmation_before_submit`, `submit_matches_confirmed_draft`, `no_agent_direct_submit`, plus a "hybrid hint" `confirmed_draft_matches_transaction_and_amount`.
- **Judge checklist items:** `written_confirmation_notice`, `confirm_exact_business_object_before_submit` (severity critical).
- **Confirmation contract:** transaction_id, merchant, amount, reason.
- **Most-failing rules** (Fig. 6, domain not labelled). `rights_before_confirmation` fails 80–100% across models, and `notice_timing_before_dispute_draft` fails 0–67%. *My inference:* both are banking (Reg E rights disclosure; dispute draft). This would explain banking's 88.57% false-pass rate. **Unverified.**
- **"Authority checks" in CXBench mean four different things:**
  1. Submission authority (runtime vs agent).
  2. Tool permissions, checked deterministically.
  3. "Required authority checks before drafting", e.g. the insurance `policy_summary_before_authority_check`, i.e. whether the reporter is authorised on the policy.
  4. Session authentication before reading records (banking).

  None concerns the authority or identity of a **third-party counterparty**.

### 4.2 Overlap with our pilot (r2_governance_context §B)

| Element | CXBench | WorkTrace counterparty pilot | Overlap |
|---|---|---|---|
| Sector / regulation | US consumer banking, Reg E (EFT errors and liability) | EU credit institution, AMLR / EBA / FATF (legal-entity CDD) | same sector, different law and function |
| Unit | customer-service episode with simulated customer | decision episode over counterparty evidence | partial |
| Who determines the correct action | customer goal + hidden facts | content of external evidence (register, BO chain, sanctions list, PEP flag, second sources) | **different**: the key differentiator |
| Authority of the person acting | reporter-authority check (insurance); session authentication (banking) | **P2**: mandate / power of attorney; signatory ∈ register's legal representatives | **direct overlap**; cite CXBench in P2 |
| Timing / ordering obligations | disclosure before confirmation; read→check→draft | P1 verify before onboarding; P6 report within 14 days; P14 refresh intervals | analogous rule form |
| Disclosure to customer | Reg E written-confirmation notice; rights disclosures | P6 exception: invite customer to correct the register within 14 days; P15 explanation and challenge | analogous |
| Mediated vs direct execution | runtime submits after confirmation | P15 reserved classes always escalate; delegable classes earn "proceed" | **conceptual overlap** (authority withheld from agent); ours is per class and earned |
| Statute-linked rules | 53 rule cards (LII sources) | 15 rules P1–P15 with AMLR/FATF/EBA citations | **same artefact type**; must cite |
| LLM-synthesised tasks from rule cards | yes | generator (procedural; possibly LLM prose) | partial |
| Outcome ≠ process | false-pass | H1′ | **pre-empted**; cite |

### 4.3 How to differentiate (design and wording)
1. **Choose decision classes whose correct action flips with the evidence and not with the request.** Our delegable classes (i)–(v) already do this: identification completeness, BO computation, discrepancy triage, document requests, re-review triggers. Say so in one sentence: "In CXBench the correct business action is fixed by the customer's request; in our episodes it is fixed by the content of external evidence, which is what makes evidence interventions meaningful."
2. **Make the comparison fair by importing CXBench-style procedural rules into our episodes.** Otherwise the procedure detector has nothing to catch. Candidates:
   - `authority_check_before_accepting_instructions` (P2);
   - `sanctions_screen_before_proceed` (P9);
   - `freshness_check_before_relying_on_excerpt` (P3);
   - `customer_notice_before_request_route` (P6 exception: content of the 14-day invitation);
   - `no_finalisation_in_reserved_class` (P15, the analogue of `no_agent_direct_submit`);
   - `record_contains_justification` (AMLR 21(3), "required trace evidence").
3. **Keep jurisdictions separate.** Never describe our pilot as "like CXBench banking". Ours is EU AML/KYC, legal entities, applicable from 2027; theirs is US Reg E consumer EFT. No compliance claims, as in r2_governance_context §C.
4. **Optional external-validity add-on.** If CXBench's artifact is released under a permissive licence, run WorkTrace interventions on its banking tasks.
   - Example intervention: perturb the transaction record or notice date that `check_reg_e_notice_timing` reads. Under Reg E §1005.6(b), notice timing is decisive for consumer liability tiers (*to verify against the CFR text before use*).
   - Then report how many CXBench *both-passes* fail our basis tests. This is the most direct possible answer to "isn't this CXBench?". Run it only if feasible; it is not needed for the core claims.

### 4.4 Reuse and licence
- **Paper (CC BY 4.0).** Figures, schema tables, rule-category definitions and short quotations can be reused with attribution.
- **Artifact.** App. F.4 describes a "reproducibility artifact" containing the task corpus, domain tools, runtime, rule grader, judge protocol, task-construction pipeline, run logs and a container. **No URL is given in v1, and I found none. The licence is unknown [unverified].** Action: email the corresponding author (boxi.yu@lero.ie, given in the paper) for the release location and licence before planning reuse of code or tasks.
- **Ideas reusable regardless of artifact licence** (with citation):
  - the rule-card schema (id, source citation, obligation, applicability, required trace evidence, deterministic check or checklist item);
  - the four rule categories;
  - the verdict composition r_process = r_rule ∧ r_judge, with any failed finding failing;
  - the reconciliation of judge verdict with findings;
  - the false-pass metric and its two denominators (F/N and F/O);
  - Wilson CIs and Holm-corrected exact McNemar for paired comparisons;
  - the structural gates for synthesised tasks (every confirmation field ∈ hidden facts; registered tools; supported rule ids; non-empty checklist).
- **Reg E text** is US federal regulation, public domain. AMLR is EU law, reusable.

---

## 5. H1′ with a procedure audit as second detector (question c)

**Answer: yes.** H1′ can be run on the same generated episodes with three detectors. The definitions below are operational.

### 5.1 Objects
- **Base episode and generator labels.** For a base episode e in decision class c, the generator provides:
  - y*(e), the correct action;
  - K(e), the decisive evidence and its redundancy structure;
  - π*(e), the pre-registered expected response pattern of the correct action under each intervention ι ∈ Ι(e) ⊆ {remove X, only X, invert X, add independent S₂}, plus a placebo intervention.
- **Agent outputs.** The agent produces a trace τ(e), a final action a(e) and declared grounds G(e).

### 5.2 Detectors
- **D_out (outcome check).** D_out(e)=1 iff a(e)=y*(e) and the final-state predicates hold. Deterministic.
- **D_proc (procedure audit; CXBench/PAE emulation).** D_proc(e)=1 iff R(e) ∧ J(e). The detector is **blind to K(e), π*(e) and all intervention runs**.
  - **R(e): deterministic hard rules** from class-specific rule cards over the base trace only:
    - R1 *required-lookup coverage*: every source type required for class c (register excerpt, BO register, sanctions list, PEP list, mandate document, as applicable) was queried before the action event. This is GroundEval's Silence coverage and CXBench's `read_before_check`.
    - R2 *ordering*: e.g. P2 authority check before accepting instructions; P9 screen before any proceed-draft; P3 freshness check before relying on an excerpt. CXBench "domain ordering".
    - R3 *authority / permissions*: no tool outside the permission envelope; no finalisation in a P15 reserved class (the analogue of `no_agent_direct_submit`); escalations routed through the escalation tool.
    - R4 *record completeness*: the decision record contains the action, declared grounds with source ids, and a justification (AMLR 21(3)). This is CXBench's "required trace evidence".
    - R5 *citation validity*: every source id in G(e) was retrieved at t < t_action, inside the actor's time and role horizon (GroundEval Perspective), and every quoted field value equals the retrieved value. This is the deterministic part of PAE I_df.
    - R6 *disclosure gates*: where class c requires a customer-facing notice (e.g. the P6 invitation with its 14-day deadline), the notice precedes the request event. This is CXBench's disclosure gate.
  - **J(e): LLM checklist judge.** The judge is from a different model family than the agent. Its inputs are the policy, the trace, G(e), the final state and the class checklist. It returns CXBench-format findings {rule_id, passed, severity, seq, evidence}; any failed finding gives J=0. Checklist items:
    - PAE I_pc: the action is permitted by policy given the observations in the trace;
    - I_pf: policy statements are faithful;
    - I_ec: claimed actions were executed;
    - I_df: communicated and declared data ⊆ observations;
    - **plus the strongest static basis check available: "do the declared grounds, as stated, warrant the action under the policy?"**

    Two variants, reported separately:
    - **J-A**: the judge also receives y*(e), as in PAE.
    - **J-B**: reference-free.
- **D_int (interventional basis test).** For each ι ∈ Ι(e), run n replicate executions of the intervened episode (n pre-registered, e.g. 5) and n of the placebo.
  - D_int(e)=0 (basis failure) iff, for some ι, the observed action distribution departs from π*(e) under a pre-registered rule. Example rule: the modal action differs from π*(ι), *and* the departure rate exceeds the placebo flip rate by a margin δ.
  - Departures are labelled by type: *insensitive* (no change where π* requires a change), *over-sensitive* (change after removing redundant evidence while S₂ is present), *wrong direction*.
  - Deterministic given the runs.

### 5.3 Estimands and decision rule (pre-register)
- **Population.** E⁺ = {e : D_out(e)=1} (base runs).
- **θ₂ (the quantity in the task brief).** θ₂ = P(D_int=0 ∧ D_proc=1 | D_out=1), the share of correct-outcome episodes that fail the interventional basis test yet pass both the outcome check and the procedure audit.
- **θ (main H1′ estimand).** θ = P(D_proc=1 | D_int=0, D_out=1), the share of basis failures invisible to a state-of-the-art procedure audit.
- **Also report:**
  - θ₁ = P(D_int=0 | D_out=1);
  - the reverse cell P(D_proc=0 ∧ D_int=1 | D_out=1), i.e. procedure violations on a correct basis (expected to be large if CXBench-style disclosure rules are included);
  - the full 2×2×2 counts per class;
  - Cohen's κ and exact McNemar between D_proc and D_int on E⁺;
  - J-A vs J-B.
- **Inference.** Wilson CIs per class; a cluster bootstrap over templates and seeds for pooled estimates, because episodes are nested in templates.
- **H1′ supported** if the lower 95% bound of θ ≥ τ_θ **and** that of θ₂ ≥ τ₂. **H1′ falsified** if the upper bound of θ < τ_low, i.e. procedure audits catch almost all basis failures. τ values are placeholders to fix at pre-registration, e.g. τ_θ=0.25, τ₂=0.03, τ_low=0.10.
- **Power note.** θ is conditional on basis failures, so its sample size is the number of basis failures, not of episodes. If θ₁ is around 10%, about 1,000 outcome-correct episodes give about 100 basis failures, i.e. a Wilson half-width of about ±0.09 for θ near 0.5. Plan the episode count from θ₁.

### 5.4 Detector validation with scripted known-answer agents (main design lesson)
Before applying the detectors to LLM agents, run **scripted agents whose basis is known because we wrote them**:

| Agent | Basis | Procedure | Expected D_proc | Expected D_int |
|---|---|---|---|---|
| S1 grounded oracle | correct (reads decisive field) | compliant | pass | pass |
| S2 compliant shortcut (e.g. performs every lookup and disclosure, then decides "proceed" whenever names match, ignoring BO chain / suspicion flag) | **wrong** | compliant | pass | **fail** |
| S3 sloppy but grounded (skips a disclosure or misorders a lookup, decides on decisive field) | correct | non-compliant | fail | pass |
| S4 both bad | wrong | non-compliant | fail | fail |
| S5 grounded with redundancy (uses S₂ correctly per P6) | correct | compliant | pass | pass (tests the over-sensitivity arm) |

This gives sensitivity and specificity for both detectors with known answers. It shows D_proc is not a straw man (it must catch S3 and S4) and that D_int does not fire spuriously (S1, S5). Then H1′ on LLM agents is a claim about which cells real agents fall into.

No paper in this set validates its process detector against agents whose ground truth is known by construction:
- CXBench and PAE validate against human labels;
- AgentLens validates stage labels only;
- GroundEval does not validate against agents at all.

This is a small but genuine methodological addition.

### 5.5 Threats specific to the comparison
- **D_proc too weak** gives an inflated θ. Mitigations: R5 and J's static basis item, the J-A variant with ground-truth action, and S3/S4 positive controls.
- **D_proc too strong**, because the judge infers the basis from leaked hints: keep the judge blind to K(e) and π*(e).
- **Leakage into statements.** PAE Case 5 shows that some basis errors surface in communications and are caught by I_df. Report how many D_int failures are also D_proc failures *because of* statement-level evidence. That is the "visible" share.
- **Stochasticity.** D_int needs replicates. D_proc and D_out are evaluated on one base run, so also report them across the n base replicates to avoid comparing a multi-run detector with a single-run one.

---

## 6. Does any of them define a construct like DSA? (question d)

**No.** None defines a construct about whether behaviour has the *structure of decisions*: recognising decision points and alternatives, grounding by tested evidence dependence, uncertainty and contradiction boundaries, authority scope, escalation, revision after correction, provenance. Named neighbours, mapped to DSA facets:

| DSA facet | Existing named construct or metric | Status for WorkTrace |
|---|---|---|
| Recognising decision points / alternatives | none (AgentLens "intent stages" E/I/V/O are activity phases, not decisions) | new |
| Grounding in the right evidence (interventional) | none; nearest are PAE I_df (statements ⊆ observations) and GroundEval "evidence-path validity" (access / time / coverage) | **new as interventional and redundancy-aware**; cite both as static precursors |
| Uncertainty / contradiction boundaries | GroundEval Silence track (verify before claiming absence); AgentLens C1 "Minimal & Unverified" | partly occupied; cite |
| Authority scope | CXBench tool permissions, submission authority, `no_agent_direct_submit`; PAE I_pc (HARMFUL_DISALLOWED_EXECUTION, DISALLOWED_DECISION) | occupied as procedure checks; ours is per-class and earned |
| Correct escalation | PAE counts "Unnecessary transfers to human agents" under I_pc, and a transfer against the user's wish under I_intent | partly occupied (over-escalation penalised); under-escalation and per-class escalation calibration are ours |
| Revision after correction | none | new |
| Provenance | PAE I_df / I_ec; GroundEval citations and visibility cone; CXBench trace-linked findings | occupied; adopt and cite |

**Construct-level threats:**
- PAE's named axis **"Procedural Integrity"**;
- GroundEval's **"state-invalid correctness" / "evidence-path validity"**;
- CXBench's **"process compliance"**;
- AgentLens's **"process quality"**.

A reviewer could argue that DSA = procedural integrity + evidence-path validity + escalation. Defence: DSA is defined by *interventional* grounding and *decision-level* structure, and is used for per-class delegation. Its other facets are explicitly inherited from these metrics, cited as such.

---

## 7. Differentiation sentences for related work (question e)

- **Group sentence:** "A 2026 cluster of benchmarks separates outcome from process and finds large outcome–process gaps: 80% of outcome-passes in CXBench miss a statute-linked obligation, 27–78% of τ-bench successes are 'corrupt' under PAE, and 0.5–23% of passing SWE-agent trajectories are 'lucky' under AgentLens. GroundEval names the closely related failure of 'state-invalid' correct answers. All of them audit the *observed* trace against procedures, statements, permitted evidence or reference behaviour. WorkTrace asks a question none of them can answer from the trace alone: whether the action would have been different had the evidence that should determine it been different. It answers it by intervening on that evidence in generated episodes whose decisive evidence is known by construction."
- **CXBench:** see §2.1. Add for the domain section: "Our counterparty-verification episodes share CXBench's statute-linked rule representation but differ in what fixes the correct action: in CXBench's Regulation E workflows it is the customer's request, in ours the content of external evidence about a counterparty."
- **PAE:** see §2.2. Use its own limitation as the hinge: "PAE notes that a behavioural audit 'cannot surface reasoning-level errors in agents that happen to produce correct outputs through flawed inference' (§6); evidence interventions target exactly this residual without relying on the faithfulness of reasoning traces."
- **GroundEval:** see §2.3. Add for W3: "GroundEval motivates evidence-path tests as a precondition for letting agents operate over real context; WorkTrace turns such tests into a revocable, per-decision-class delegation rule evaluated on held-out episodes."
- **AgentLens:** see §2.4.
- **H1′ positioning:** "We do not claim that outcome checks miss process failures, which is well established. We test the narrower claim that a measurable share of outcome-correct decisions fail interventional basis tests while passing a procedure audit built to the standard of CXBench and PAE."

---

## 8. Implications for WorkTrace

**Design changes**
1. **Adopt the three-detector design of §5 as the H1′ experiment.** It needs a class-specific rule-card set, built from P1–P15 in CXBench format, and a blinded checklist judge with PAE invariants plus a static basis item. Report θ, θ₂, θ₁ and the reverse cell.
2. **Add scripted known-answer agents (S1–S5)** as a mandatory validation stage for both detectors. This answers the straw-man objection and is a small methodological contribution.
3. **Import procedural obligations into the counterparty episodes** (P2 authority, P9 ordering, P3 freshness, P6 notice, P15 no-finalisation, AMLR 21(3) record). Without them, D_proc trivially passes and the comparison is unfair.
4. **Use a non-colliding name** for our failure type. "False-pass", "corrupt success", "state-invalid correct", "lucky pass" and "outcome–process gap" are all taken. Proposal: **"correct but unjustified action"**, consistent with W3's loss "unjustified action".
5. **Narrow W2's wording** to "ground truth on decisive evidence and redundancy structure (the expected response pattern under interventions)". Do not write "ground truth by construction" unqualified.
6. **Map the DSA facets to prior metrics** (table in §6) in the paper. Claim as new only interventional grounding, decision-point recognition, revision after correction and per-class use.
7. **Measure over-escalation and under-escalation separately.** PAE penalises over-escalation inside its integrity gate; our escalation cost should be compatible with that.
8. **Run the no-evidence baseline as a hard check.** GroundEval's agent with tools scored *below* the zero-shot floor on 2 of 3 tracks. Our generator must show that evidence is necessary for y* (zero-shot accuracy near chance on delegable classes).
9. **Optional:** run interventions on CXBench banking tasks if the artifact is released under a usable licence (§4.3 item 4).

**Risks**
- A reviewer may see H1′ as incremental over CXBench and PAE. Mitigate by making the θ estimate and the scripted-agent validation the headline, not the existence of a gap.
- CXBench's 88.6% banking false-pass rate means LLM agents may fail D_proc so often that few outcome-correct, procedure-passing episodes remain. That would leave θ₂ small even when θ is large. Pre-register θ as primary and size the episode count accordingly.
- If the procedure judge is given y* (J-A), as PAE does, it may become stronger than any deployable audit. Report J-B as the realistic comparator.

**Things to cite**
- **Must:**
  - CXBench (domain section and H1′);
  - PAE, with its Limitation 2 quoted;
  - GroundEval (W2 and W3 motivation; Perspective ≈ our "information available at decision time" field);
  - τ-bench §3 sentence (now verified);
  - AgentLens, with arXiv id because of the name collision.
- **Should:**
  - SOPBench (Li et al., arXiv:2503.08669; reports correct outcomes with incorrect procedures, according to CXBench §5; *not read by me*);
  - OpenClawBench and ClawTrack (per r2).

**Bibliographic status**

| Work | arXiv | Status |
|---|---|---|
| CXBench | 2610.25954 | [verified arXiv API + OpenReview desk-reject record] |
| PAE | 2603.03116 | [verified arXiv API; OpenReview CoRR record] |
| GroundEval | 2606.22737 | [verified arXiv API]; code repo reachable, licence unverified |
| AgentLens | 2605.12925 | [verified arXiv API + OpenReview FAGEN@ICML 2026 poster] |
| τ-bench (Yao, Shinn, Razavi, Narasimhan) | 2406.12045 | [verified by reading arXiv HTML v1 §3]; bibliographic metadata not re-queried in this round |
