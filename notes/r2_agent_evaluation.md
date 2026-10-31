# R2 — Agent-evaluation landscape for H1 and for the generative, held-out, anti-Goodhart evaluation design

Reading note for WorkTrace (round 2). Written 2026-10-25.

H1 under test: *"episode-level evaluation reveals errors invisible to outcome-only evaluation"*, in the WorkTrace sense of **"correct outcome on a wrong basis"**.

Also in scope: the design of the episode generator (procedural generation, hidden seeds, rotation) and the anti-Goodhart claims (multidimensional profile, generative variation, public method with protected instances).

---

## 0. Bottom line (novelty threats first)

1. **H1 in its generic form is not novel any more.** In 2026 at least six arXiv preprints measured the *outcome–process gap* in agent benchmarks directly, with numbers:
   - **CXBench** (2610.25954): "false-pass" = 55.5% of all runs, which is 80.1% of the runs that passed the outcome check.
   - **Procedure-Aware Evaluation / "corrupt success"** (2603.03116): 27–78% of τ-bench successes are corrupt.
   - **OpenClawBench** (2605.29253): coins the name "Outcome–Process Gap"; 9.33% of 31,135 oracle-passing runs are anomalous.
   - **AgentLens** (2605.12925): "Lucky Pass", 10.7% of passing SWE-bench trajectories.
   - **ClawTrack** (2607.28037): "lucky passes".
   - **GroundEval** (2606.22737): "state-invalid correct", i.e. a correct answer reached through an evidence path the task forbids. This is the closest concept to "wrong basis". It is defined there, but not quantified.

   A reviewer will say "H1 is known". **H1 must be re-scoped:** it becomes a replication or precondition, not a contribution, unless it is sharpened (see §D).
2. **Interventions on external inputs to agents also have precedents.**
   - **Causal Sensitivity Score** (Turk, 2605.30590): a pre-registered catalogue of mutations to case inputs (flip / remove / inject). It scores whether a recommendation updates in the pre-registered direction, and it also runs in a tool-using agent where the mutation propagates through tool returns. Its coverage metric and its interventional metric rank six models in nearly opposite orders.
   - **Spurious Tool Use** (2609.16268): planted, causally irrelevant cues plus counterfactual cue-present/absent groups. The authors state explicitly that answer-correctness checks miss these shortcuts.
   - **τ-bench's own ablation** (Yao et al. 2024, Table 3): removing the policy document barely changes retail success (gpt-4o 61.2→56.8). The authors' reading is that successes "may not actually be leveraging the policy documents".
   - These touch H2 more than H1, but they weaken any claim that "intervening on external evidence to test the basis of an agent's decision" is new in itself.
3. **What I found nowhere** (the search was broad but not exhaustive; see §D):
   - (a) a benchmark that holds ground truth about the *decisive evidence* of each episode **by construction** and classifies outcome-correct episodes as basis-correct or basis-wrong with **redundancy-controlled** interventions (remove X / only X / invert X / add an independent second source);
   - (b) a head-to-head comparison of *outcome-only*, *procedure-audit* (CXBench/PAE style) and *interventional-basis* detectors on the same episodes;
   - (c) any use of such results to **grant or revoke autonomy per decision class**.

   PAE states its own blind spot in its Limitations: it "cannot surface reasoning-level errors in agents that happen to produce correct outputs through flawed inference" (§6).
4. **Domain collision.** CXBench evaluates regulated customer-service workflows, including **banking under Regulation E**, with "rule cards" that link statutes to trace evidence. Our *counterparty verification (AML/KYC)* pilot sits right next to it. We must cite it and state the difference precisely: CXBench checks *procedure* (disclosure, ordering, authority); we check *evidence-dependence of the decision*.
5. **Generator best practice is well documented** and can be adopted without novelty claims:
   - Procgen-style seed splits;
   - τ²-bench compositional generation from atomic (init, solution, assertion) functions;
   - the Power Systems Agent Benchmark (2606.20950): *private seed, public generator, accept a draw only if the reference solver solves it, publish only aggregates*;
   - LiveBench rotation;
   - GSM1k withheld set with a pre-committed release;
   - Kapoor et al.'s rule that the holdout level must match the intended generality;
   - the ABC checklist (trivial-agent baselines, ground-truth isolation).

---

## 1. Reading coverage and verification

**Verification method:**
- All arXiv items were checked against the arXiv API (export.arxiv.org) on 2026-10-25: title, full author list, date.
- DOIs were checked on Crossref.
- Venues were checked against OpenReview records, which include the DBLP mirror.
- DBLP's own API was blocked by an anti-bot page, so DBLP was **not** queried directly.
- "[verified]" means the bibliographic data was confirmed by at least one of these sources.
- Venue claims that rest only on an arXiv comment or my memory are marked.

**How much of each text was read.** Full HTML texts were downloaded from arxiv.org/html (or PMC) and read as plain text. Figures were seen only through captions and alt text.

| Work | What I read |
|---|---|
| CXBench | §1–§6, Limitations, App. A (all). Apps. B–H not read. |
| PAE (corrupt success) | All of §1–§6, Apps. 0.A, 0.B, 0.C. Apps. 0.D–0.F only skimmed (headers). |
| GroundEval | Entire main text (§1–§11). |
| Kirgis et al., Log analysis | §1–§7. Appendices not read. |
| Causal Sensitivity Score (Turk) | Main text §1–§7 and Apps. A–C. |
| Manheim & Garrabrant | Full. |
| Thomas & Uminsky (PMC full text) | Full main text up to and including "Involve a range of stakeholders" (conclusion not read). |
| Geirhos et al. (arXiv version) | Abstract, §3, §4 intro, §6.1, §6.2 (partly), §7. |
| Zhu et al. (ABC) | Abstract, §1–§4, §5.1. §5.2–§5.3 and appendices not read. |
| τ-bench | Abstract, §1, task/reward design (§3), results incl. failure analysis and policy-removal ablation (§5), §6. |
| τ²-bench | Abstract, contributions, task-generator Stage 3, evaluation criteria. |
| Kapoor et al., AI Agents That Matter | Abstract and §5 (shortcuts/holdouts) in full. |
| HAL | Abstract, §1 opening, §4.2 log-analysis findings, Appendix table captions. |
| Uesato et al. | Abstract, §1 findings, metric definitions, key results paragraphs. |
| ProcessBench | §3.3 statistics (Table 2) only. |
| Power Systems Agent Benchmark | Requirements, §4.4, §8.1–§8.2. |
| Spurious Tool Use | Abstract, §1–§3.3. |
| ImpossibleBench | Abstract, §1 contributions, result paragraphs located by grep. |
| SOPBench | Abstract and "error cause analysis" paragraph. |
| LiveBench | Abstract and update-policy paragraph. |
| GSM1k | Abstract and release-policy paragraphs. |
| Procgen | Abstract and protocol paragraphs (§2–§3). |
| AgentLens, OpenClawBench, ClawTrack, EnvTrustBench, SeekBench | Abstract and Introduction. |
| Agent-as-a-Judge | Abstract and alignment-results paragraph. |
| WebArena, GAIA, AgentBench, SWE-bench, SWE-Bench+, Wang et al. (PatchDiff), SWE-Bench Illusion, HELM, Dynabench, GSM-Symbolic, Recht et al., AgentRewardBench, ST-WebAgentBench, Online-Mind2Web, Leaderboard Illusion, SWE-Bench Pro, Lightman et al., Skalse et al., Gao et al., AgentPRM, TRAIL, MAST, Who&When, LiveCodeBench, Reasoning Gym, Ethayarajh & Jurafsky, "Right Answer, Wrong Method", "Agents Catching Agents", "Shortcut Sensitivity…", "Don't Blindly Trust It", CHIVE, SABER | **Abstract only** (sometimes plus the opening of §1). |
| McCoy et al. 2019, Ross et al. 2017, Lapuschkin et al. 2019, Burnell et al. 2023, Strathern 1997 | **Not read.** Bibliographic data verified on Crossref only. |

---

## A. Strongest evidence that outcome-only agent evaluation misses wrong-basis successes (for the Introduction)

Ranked by fit to *our* H1 (an agent decision that is correct in outcome but rests on the wrong basis) and by strength of evidence.

1. **CXBench** (Yu et al., 2026, arXiv:2610.25954).
   - Setup: 7 models × 120 regulated customer-service tasks in 6 domains.
   - 69.29% of 840 runs pass the outcome check, but only 13.81% pass both outcome and process.
   - **False-passes are 55.48% of all runs and 80.07% of outcome-passes.** "Every model produces false-passes."
   - Model ordering changes: deepseek-v4-flash and glm-5.1 tie at 77.50% outcome, but reach 13.33% vs 21.67% both-pass (§4.1).
   - Caution: preprint; the OpenReview record is an ICLR 2027 *desk-rejected* submission. The judge was calibrated on development traces, with no held-out judge validation (§4.4).
2. **Procedure-Aware Evaluation** (Cao, Driouich, Thomas, 2026, arXiv:2603.03116).
   - On τ-bench (GPT-5, Kimi-K2-Thinking, Mistral-Large-3; k=4 trials), **27–78% of reported successes are "corrupt successes"**.
   - Gated success drops: Mistral retail 0.68→0.16; GPT-5 retail Pass^4 0.58→0.24.
   - Rankings reverse.
   - Manual check of all 131 Airline corrupt-success cases gives judge precision of 93.8–95.2% (§5).
3. **Uesato et al. 2022** (arXiv:2211.14275): the classic quantification of right-answer/wrong-reasoning.
   - Definition: "Trace error rate is the fraction of problems with correct final answers for which the method produces at least one incorrect reasoning step."
   - Prior state of the art had 14.0% trace error.
   - Outcome-based RL left 12.4% trace error vs 3.8% for process-based (19.8% vs 11.4% before reranking).
   - **ProcessBench** (Zheng et al., ACL 2025) adds that the process-error share among correct-answer solutions rises with difficulty: 3.5% GSM8K, 18.8% MATH, 32.2% OlympiadBench, **51.8% Omni-MATH** (Table 2).
   - These are not agents, but they are the cleanest prior on "correct outcome ≠ correct basis".
4. **SWE-bench validity cluster** (outcome = tests pass):
   - **SWE-Bench+** (Aleithan et al., arXiv:2410.06992): 32.67% of successful SWE-Agent+GPT-4 patches involved solution leakage (the fix was in the issue text or comments), and 31.08% passed only because of weak tests. Resolution falls 12.47%→3.97%.
   - **Wang, Pradel, Liu** (ICSE 2026, doi:10.1145/3744916.3764576): 7.8% of patches counted correct fail the developer test suite; 29.6% of plausible patches behave differently from the ground truth; inflation is +6.4 pp.
   - **Zhu et al. ABC** (NeurIPS 2025 D&B): an empty-response agent passes 38% of τ-bench-airline tasks; overall over/underestimation reaches 100% relative; "24% of the top 50 leaderboard positions are incorrect" on SWE-bench-Verified (citing Yu et al.).
5. **τ-bench's own policy-removal ablation** (Yao et al. 2024, arXiv:2406.12045, §5, Table 3). This is an *evidence-removal intervention* in a canonical agent benchmark.
   - Removing the policy from the system prompt changes gpt-4o retail pass^1 only from 61.2 to 56.8, and gpt-3.5 airline from 10.8 to 9.6.
   - Authors: successes "mostly stem from using tools in an intuitive and common sense way, and … they may not actually be leveraging the policy documents".
   - Airline gpt-4o drops 33.2→10.8.
   - This is our best precedent that **removing the declared basis exposes successes that did not depend on it**. It is aggregate-level, not per episode.
6. **ImpossibleBench** (Zhong, Raghunathan, Carlini, ICLR 2026, arXiv:2510.20270). Tasks are mutated so that the specification and the tests conflict, so *any* pass implies a specification-violating shortcut. **GPT-5 "cheats" on 76% of Oneoff-SWEbench tasks** (2.9% on Oneoff-LiveCodeBench). This is the "wrong basis by construction" design that we want to emulate.
7. **Geirhos et al. 2020** (Nature Machine Intelligence 2:665–673): conceptual anchor.
   - "Shortcuts are decision rules that perform well on standard benchmarks but fail to transfer to more challenging testing conditions."
   - i.i.d. testing "is insufficient to distinguish between intended and unintended (shortcut) solutions" (§7, recommendation 3).
   - "Morgan's Canon for ML": "Never attribute to high-level abilities that which can be adequately explained by shortcut learning" (§6.1).
8. Choose one of the following for the rank-reversal / quantified-lucky-success point:
   - **Causal Sensitivity Score** (Turk, 2026, arXiv:2605.30590): the coverage metric (CMS) and the interventional metric (CSS) rank 6 frontier models in nearly opposite orders (Spearman ρ=−0.49; all six change rank). In the ReAct agent, gpt-5.4 retrieves the same chart sections as the others but does not update (CSS 0.050→0.050). This is "retrieved the evidence, did not use it".
   - **AgentLens** (Sahoo et al., FAGEN@ICML 2026, arXiv:2605.12925): 10.7% of 1,136 passing SWE-bench-Verified trajectories are Lucky Passes (0.5–23.2% across models); ranks move by up to 5.

**Secondary supports** (abstract-level or position papers):
- **Kirgis et al. 2026** "Log analysis is necessary…" (FAGEN@ICML 2026; Kapoor, Narayanan, Steinhardt, Hobbhahn et al.). Taxonomy of internal-validity, external-validity and safety threats that outcome-only scoring hides. τ-bench Airline: errors in 25 of 50 tasks; pass^5 roughly doubles, 20.8%→40.0%, on the corrected subset.
- **HAL** (Kapoor et al., ICLR 2026): eight cases of agents finding gold answers on HuggingFace or arXiv; hard-coded "plausible" solutions on CORE-Bench and SciCode.
- **"Right Answer, Wrong Method"** (2608.02442, work in progress): 8.2–44.1% of answers credited as correct are "hacked solutions" (science QA, not agents).
- **OpenClawBench** (2605.29253): 9.33% of oracle-passing runs anomalous; 92.70% within the high-risk slice.

---

## B. Per-work notes

Format per work: Bibliographic data · Problem & contribution · Method · Evaluation · Must NOT claim · Leaves open · Differentiation sentence · Citation cautions. Entries for minor works are compressed.

### B1. Outcome-based agent benchmarks (what H1 is positioned against)

#### τ-bench
- **Bib:** Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan. "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains." arXiv:2406.12045 (2024). [verified arXiv]. Venue: not found in OpenReview search. My belief is ICLR 2025 [unverified].
- **Problem & contribution:** Agents must converse with an LLM-simulated user, call domain APIs and follow a policy document (retail, airline). The paper introduces pass^k as a reliability measure.
- **Method:**
  - Reward is r = r_action × r_output: the final database must equal the unique annotated goal state, and the response must contain the required information (§3).
  - User instructions are iterated until "only one possible outcome" exists.
  - Read actions are free; only database writes are compared.
- **Evaluation:**
  - gpt-4o function calling: ~61% retail, ~35% airline; pass^8 <25% retail.
  - Failure breakdown: "wrong decision-making" is 25% of failures.
  - Policy-removal ablation (Table 3): retail 61.2→56.8 (gpt-4o), 20.0→14.5 (gpt-3.5); airline 33.2→10.8 (gpt-4o), 10.8→9.6 (gpt-3.5).
- **Must NOT claim:** that we invented pass^k-style reliability over repeated trials, or the idea of state-based outcome checks with free conversational paths.
- **Leaves open:**
  - The outcome check is blind to *why* the database ended up correct.
  - The authors themselves suggest "LM checks that certain rules are followed" (§6).
  - Their own ablation is an aggregate evidence-removal test, never per-episode.
- **Differentiation:** "τ-bench scores agents by whether the final database matches a unique goal state; WorkTrace asks, per episode, whether the action would have changed had the decisive evidence been removed, inverted, or corroborated, and τ-bench's own policy-removal ablation (Yao et al., 2024, Table 3) shows why the two can diverge."
- **Cautions:**
  - CXBench (§1) says the τ-bench authors acknowledge that a correct final state may result from a policy violation, e.g. a return processed without explicit confirmation. **I could not find that sentence in the v1 HTML**, so I do not attribute it to τ-bench directly.
  - Later critiques found task errors in τ-bench Airline (Kirgis et al.: 25 of 50 tasks) and an empty-response exploit (ABC: 38%).

#### τ²-bench
- **Bib:** Victor Barres, Honghua Dong, Soham Ray, Xujie Si, Karthik Narasimhan. "τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment." arXiv:2506.07982 (2025). [verified arXiv]. OpenReview: ICML 2026 spotlight record [verified OpenReview]. An earlier ICLR 2026 submission was desk-rejected.
- **Problem & contribution:** Dual-control (Dec-POMDP) telecom domain in which the user also acts. **Compositional task generator** that "programmatically creates diverse, verifiable tasks from atomic components".
- **Method:**
  - Each atomic subtask is a triple ({f_init}, {f_sol}, {f_assert}).
  - Groups of mutually exclusive subtasks; a composite task takes at most one subtask per group; 15 groups.
  - Success criteria: DB check, status assertions, natural-language assertions, communication-info check, action matching.
- **Evaluation:** Large drops from no-user to dual-control mode. I did not read the result tables.
- **Must NOT claim:** programmatic compositional generation of verifiable agent tasks with "provable correctness" as our novelty.
- **Leaves open:** The generator produces tasks with known *outcomes*, not known *decisive evidence*. There are no interventions on the evidence for a decision.
- **Differentiation:** "Like τ²-bench we compose episodes programmatically from atomic, verifiable components, but our generator additionally fixes which external evidence is decisive for each decision, so that the basis of an agent's action, not only its outcome, has ground truth."
- **Cautions:** Desk-rejection history at ICLR 2026, later accepted at ICML 2026 per OpenReview.

#### WebArena / GAIA / AgentBench / SWE-bench (abstract-level; cite as the canonical outcome-only benchmarks)
- **WebArena:** Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, Graham Neubig. arXiv:2307.13854; ICLR 2024 [verified]. "Functional correctness of task completions"; best GPT-4 agent 14.41% vs human 78.24%.
  - Later critiques: Kapoor et al. (top agent STeP "hardcodes policies to solve the specific tasks"; no held-out tasks); ABC (string matching overestimates by 5.2%). A "WebArena Verified" revision exists on OpenReview [seen, not read].
- **GAIA:** Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, Thomas Scialom. arXiv:2311.12983; ICLR 2024 [verified]. 466 questions; humans 92% vs GPT-4+plugins 15%.
  - **Answers to 300 questions are withheld** to power the leaderboard. This is an example of the held-out practice.
  - Exact-answer scoring only.
- **AgentBench:** Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, Jie Tang. arXiv:2308.03688; ICLR 2024 [verified]. 8 environments, 29 LLMs, success-rate based.
- **SWE-bench:** Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan. arXiv:2310.06770; ICLR 2024 (oral) [verified]. 2,294 issues; success means the hidden tests pass; Claude 2 solved 1.96%.
- **Must NOT claim (all four):** that outcome-only scoring is our discovery; these benchmarks are well-known targets of validity critiques.
- **One sentence for all four:** "Canonical agent benchmarks (WebArena, GAIA, AgentBench, SWE-bench, τ-bench) score the end state or final answer; a growing validity literature shows that such scores admit successes reached through leakage, weak tests, hard-coded policies or shortcuts (§A), which is the gap WorkTrace's decision episodes are designed to expose at the level of the decision's evidential basis."

### B2. Validity critiques, shortcuts, reward hacking

#### Zhu et al. — Agentic Benchmark Checklist (ABC)
- **Bib:** Yuxuan Zhu, Tengjun Jin, Yada Pruksachatkun, Andy Zhang, Shu Liu, Sasha Cui, Sayash Kapoor, Shayne Longpre, Kevin Meng, Rebecca Weiss, Fazl Barez, Rahul Gupta, Jwala Dhamala, Jacob Merizian, Mario Giulianelli, Harry Coppock, Cozmin Ududec, Jasjeet Sekhon, Jacob Steinhardt, Antony Kellermann, Sarah Schwettmann, Matei Zaharia, Ion Stoica, Percy Liang, Daniel Kang. "Establishing Best Practices for Building Rigorous Agentic Benchmarks." arXiv:2507.02825 (2025). NeurIPS 2025 Datasets & Benchmarks track [verified OpenReview; the published title reads "…Best Practices **in** Building…"].
- **Problem & contribution:**
  - Two validity conditions: **task validity** ("a task should be solvable if and only if the agent possesses the target capability") and **outcome validity** ("the evaluation result … truly indicates task success").
  - A checklist with items T.x (task), O.x (outcome) and R.x (reporting).
- **Method:** The checklist is applied to 10 benchmarks, and the issues it identifies are confirmed experimentally.
- **Evaluation:**
  - 7/10 benchmarks have outcome-validity flaws, 7/10 have task-validity flaws, and 10/10 have reporting gaps.
  - τ-bench empty-response agent: 38%.
  - SWE-Lancer: 100% achievable without resolving tasks.
  - KernelBench: +31% absolute overestimation.
  - WebArena: +5.2%.
  - Applying ABC to CVE-Bench reduces overestimation by 33%.
- **Must NOT claim:** a general taxonomy of benchmark validity for agents.
- **Leaves open:** Outcome validity is about *whether the task was achieved*; the checklist has no item for *whether the agent's decision rested on the right evidence*.
- **Differentiation:** "ABC asks whether a passing evaluation implies task success (outcome validity); WorkTrace adds a third condition, basis validity: whether the success depended on the evidence that should have warranted it."
- **Use for us:** adopt T.5 (isolate ground truth from the agent), T.9 (oracle solver), T.10 (inspect outliers), O.g.2 (include irrelevant states), O.g.3 (state space complex enough that trivial changes don't pass), and R.10–R.13 (significance, baselines).
- **Cautions:** none major. Cite as the NeurIPS D&B version.

#### SWE-Bench+ (solution leakage, weak tests)
- **Bib:** Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom, Gias Uddin, Song Wang. "SWE-Bench+: Enhanced Coding Benchmark for LLMs." arXiv:2410.06992 (2024) [verified]. OpenReview: submitted to ICLR 2025 and ICLR 2026, then withdrawn; an "AIWare 2026 Benchmark and Dataset" record also exists [venue status: unverified final].
- **Content (abstract only):** Manual screening of SWE-Agent+GPT-4 successes.
  - 32.67% solution leakage; 31.08% weak tests; resolution drops 12.47%→3.97%.
  - Over 94% of issues predate the model's knowledge cutoff.
  - The post-cutoff set SWE-Bench+ gives 0.55%.
- **Must NOT claim / leaves open:** It shows that the outcome signal (tests) admits wrong-basis passes in coding. It has no decision-level evidence model.
- **Differentiation:** "Solution leakage in SWE-bench (Aleithan et al.) is the coding analogue of a wrong-basis success: the right patch, obtained from the wrong source."
- **Cautions:** Preprint; percentages come from one agent configuration.

#### Wang, Pradel, Liu — "Are 'Solved Issues' in SWE-bench Really Solved Correctly?"
- **Bib:** You Wang, Michael Pradel, Zhongxin Liu. ICSE 2026 (Proc. 48th IEEE/ACM ICSE, pp. 169–181). doi:10.1145/3744916.3764576; arXiv:2503.15223 [verified Crossref].
- **Content (abstract only):** PatchDiff (differential patch testing).
  - 7.8% of patches counted correct fail the developer test suite.
  - 29.6% of plausible patches are behaviourally divergent; 28.6% of those are certainly incorrect.
  - Reported resolution rates are inflated by 6.4 pp.
- **Differentiation:** It uses an *independent second check* (differential testing) to expose outcome-validity gaps. That is analogous in spirit to our "add an independent second source", but it is applied to the grader, not to the agent's evidence.

#### SWE-Bench Illusion
- **Bib:** Shanchao Liang, Spandan Garg, Roshanak Zilouchian Moghaddam. "The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason." arXiv:2506.12286 (2025) [verified]. Venue unknown.
- **Content (abstract):** Models identify buggy file paths from the issue text alone with up to 76% accuracy, vs ≤53% on repositories outside SWE-bench. Up to 35% consecutive 5-gram overlap. This is evidence of contamination or memorization.
- **Use:** motivates generated rather than harvested episodes.

#### ImpossibleBench
- **Bib:** Ziqian Zhong, Aditi Raghunathan, Nicholas Carlini. "ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases." arXiv:2510.20270 (2025). ICLR 2026 poster [verified OpenReview].
- **Problem & contribution:** Quantify how often agents exploit tests instead of solving tasks.
- **Method:** Create "impossible" variants (Oneoff, Conflicting) of LiveCodeBench and SWE-bench by mutating tests so they conflict with the spec. "Cheating rate" = pass rate on impossible tasks.
- **Evaluation:**
  - GPT-5 cheats on 76% of Oneoff-SWEbench tasks and 2.9% of Oneoff-LiveCodeBench tasks.
  - Prompts, test access and feedback loops change cheating rates.
  - An abort option ("flag_for_human_intervention") reduces cheating.
  - LLM monitors catch 86–89% of cheating on LiveCodeBench but much less on SWE-bench.
- **Must NOT claim:** "ground truth about illegitimate success by construction" as a new evaluation idea.
- **Leaves open:**
  - Coding only.
  - Binary impossibility; no graded evidence manipulation.
  - No link to delegation. Interestingly, though, the abort option is an *escalation* channel, and it reduces cheating, which supports our escalate option.
- **Differentiation:** "ImpossibleBench makes any success illegitimate by construction; WorkTrace generalises the idea to decision episodes whose decisive evidence is known by construction, so that both illegitimate proceeding and unwarranted refusal are measurable, and treats the escalation option as part of the policy being evaluated."
- **Cautions:** Exact percentages depend on scaffold and prompt; cite the scaffold.

#### Kapoor et al. — AI Agents That Matter
- **Bib:** Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan. arXiv:2407.01502 (2024). Accepted by TMLR [verified OpenReview; year of TMLR publication not checked].
- **Problem & contribution:** Agent benchmarking shortcomings, among them "many agent benchmarks have inadequate holdout sets, and sometimes none at all. This has led to agents that are fragile because they take shortcuts."
- **Method (§5):** Four levels of generality (distribution-specific, task-specific, domain-general, general-purpose) and the **principle "the more general the intended generality of the agent, the more the held-out set should differ from the training set"** (Table 1):
  - in-distribution samples;
  - OOD samples;
  - held-out tasks;
  - held-out domains.

  Of 17 benchmarks, only 1/8 domain-general benchmarks have an appropriate holdout; 7 have none. Case study: WebArena's STeP agent hard-codes URL suffix policies. "The held-out set would need to be kept secret."
- **Must NOT claim:** the holdout-generality principle.
- **Leaves open:** How to build holdouts for *decision classes*; held-out *evidence configurations*.
- **Differentiation:** "Following Kapoor et al.'s rule that holdouts must match the intended generality, our delegation rule is calibrated on one set of generated episodes and evaluated on episodes from unseen seeds and unseen surface templates within each decision class."
- **Cautions:** none.

#### HAL — Holistic Agent Leaderboard
- **Bib:** Sayash Kapoor, Benedikt Stroebl, Peter Kirgis, Nitya Nadgir, Zachary S Siegel, Boyi Wei, Tianci Xue, Ziru Chen, Felix Chen, Saiteja Utpala, Franck Ndzomga, Dheeraj Oruganty, Sophie Luskin, Kangheng Liu, Botao Yu, Amit Arora, Dongyoon Hahm, Harsh Trivedi, Huan Sun, Juyong Lee, Tengjun Jin, Yifan Mai, Yifei Zhou, Yuxuan Zhu, Rishi Bommasani, Daniel Kang, Dawn Song, Peter Henderson, Yu Su, Percy Liang, Arvind Narayanan. arXiv:2510.11977 (2025). ICLR 2026 poster [verified OpenReview].
- **Content (abstract + §4.2):**
  - 21,730 rollouts, 9 models, 9 benchmarks, about $40k.
  - LLM-aided log inspection with Docent finds shortcuts: in AssistantBench, "eight cases where agents found a gold answer" on HuggingFace or arXiv; hard-coded solutions on CORE-Bench and SciCode.
  - It also finds costly actions (wrong credit card).
  - "Agents with identical accuracy scores can exhibit vastly different behaviors."
- **Differentiation:** HAL discovers wrong-basis successes post hoc via rubric-driven log reading; WorkTrace designs episodes so that the basis can be tested by intervention rather than inferred from logs.
- **Cautions:** Shortcut counts are small and qualitative.

#### Kirgis et al. — Log analysis is necessary for credible evaluation of AI agents
- **Bib:** Peter Kirgis, Sayash Kapoor, Stephan Rabanser, Nitya Nadgir, Cozmin Ududec, Magda Dubois, JJ Allaire, Conrad Stosz, Marius Hobbhahn, Jacob Steinhardt, Arvind Narayanan. arXiv:2605.08545 (2026). FAGEN@ICML 2026 workshop poster [verified OpenReview].
- **Problem & contribution:** A position paper: outcome-only evaluation threatens internal validity (score→capability), external validity (capability→utility) and safety evaluation. Table 1 gives a taxonomy with documented cases:
  - "Agents access future codebase state through git logs";
  - "modify evaluation code to report success";
  - "Half of passing SWE-Bench solutions would not be merged by repo maintainers" (citing Whitfill et al. 2026 [secondary, unverified]).
- **Method:** Four principles:
  1. define a validity target;
  2. confirm the essential environment pieces are logged;
  3. human-validated labels on a held-out set;
  4. quantify the label↔outcome link ("compute prevalence by outcome first … avoid causal claims without an experimental or pseudo-experimental design").
- **Evaluation:** τ-bench Airline with 13 models.
  - Errors in 25/50 tasks: 9 policy inconsistencies, 8 ambiguous, 8 DB/grading.
  - Average pass^5 rises 20.8%→40.0% on the corrected subset.
  - Persuasion-induced policy violations vary roughly 4× between models with similar pass^5.
- **Must NOT claim:** that "outcomes alone cannot license capability or safety inferences" is our insight.
- **Leaves open:** Principle 4 explicitly calls for *experimental* designs for causal claims, and log analysis is observational. **WorkTrace's interventions are exactly the experimental design they call for.**
- **Differentiation:** "Kirgis et al. argue that only logs reveal how an outcome was reached and warn against causal claims without experimental designs; WorkTrace supplies such a design at the level of single decisions, by intervening on the external evidence available to the agent."
- **Cautions:** workshop position paper; the case study is small (50 tasks).

### B3. Process / trajectory-level evaluation of agents (the 2026 cluster = main H1 threat)

#### CXBench
- **Bib:** Boxi Yu, Yuzhong Zhang, Zhenfeng Su, Linfu Xi, Yinghan Yao, Shitao Chen, Yang Cao, Liting Lin, Lionel Briand, Emir Muñoz. "CXBench: A Benchmark for Process-Compliant LLM Agents in Regulated Customer-Experience Workflows." arXiv:2610.25954 (submitted 2026-10-19) [verified]. OpenReview: ICLR 2027 Conference **Desk Rejected** Submission [verified OpenReview].
- **Problem & contribution:** "Existing tool-agent benchmarks largely score final business states, accepting trajectories that reach correct outcomes through non-compliant processes." Separate outcome and process verdicts, with a **false-pass** metric defined as "an outcome-pass run that fails process checks".
- **Method:**
  - Task θ=(g, m₀, s₀, U, Λ, K); POMDP formalisation (App. A.2).
  - 53 "rule cards" (55 obligations from the Legal Information Institute) link a statute to applicability, required behaviour, **observable trace evidence** and a criterion.
  - Process verdict = r_rule ∧ r_judge, combining deterministic checks (ordering, tool permissions, confirmed-vs-submitted agreement) with a checklist LLM judge.
  - Mediated-submit mode: the runtime, not the agent, submits after customer confirmation. Direct-submit is an ablation.
  - Tasks are LLM-synthesised from rule cards and pass structural checks plus expert review.
  - Domains: banking, telecom, insurance, healthcare, utilities, government benefits; 20 tasks each.
- **Evaluation:**
  - 7 models × 120 tasks = 840 records.
  - Outcome-pass 69.29%; both-pass 13.81%; false-pass 55.48% (80.07% of outcome-passes).
  - Per-domain example: banking 94.29% outcome vs 5.71% both-pass.
  - Of 466 false-passes, 329 are caught only by the LLM judge, 38 only by hard rules, 99 by both.
  - Direct-submit: both-pass 0.83%. After rescoring without submission-specific checks, 18.33% vs 20.83%. The authors call the original gap "scoring-sensitive".
  - Judge accuracy is 88.33% on 120 development traces, which are explicitly "not an independent held-out validation set".
- **Must NOT claim:**
  - the false-pass concept;
  - separate outcome/process verdicts;
  - statute-linked trace evidence;
  - runtime-mediated submission as a control on authority;
  - that regulated banking workflows are an untested setting for this.
- **Leaves open:**
  - Process = *procedural obligations* (disclosure, ordering, confirmation, authority). It does not test whether the *decision* depended on the evidence that warranted it. An agent can disclose, confirm and still approve for the wrong reason.
  - No interventions.
  - No redundancy control.
  - No ground truth about the decisive evidence.
  - No held-out generation.
  - No delegation rule (submission authority is fixed by mode, not earned).
- **Differentiation:** "CXBench separates outcome from procedural compliance and reports that most outcome-passes violate an encoded obligation; WorkTrace targets a different failure, a compliant-looking decision whose action does not depend on the evidence that should warrant it, which no procedure check can detect without intervening on that evidence."
- **Cautions:**
  - Single round of results; judge calibrated on development traces.
  - The gap is partly scoring-sensitive (the authors' own §4.3).
  - Desk-rejected at ICLR 2027.
  - The model names (gpt-5.4, gpt-5.6-sol, gpt-6-astra) are current as of 2026.
  - **Domain overlap with our banking pilot: must be cited.**

#### Procedure-Aware Evaluation (PAE): "Beyond Task Completion: Revealing Corrupt Success…"
- **Bib:** Hongliu Cao, Ilias Driouich, Eoin Thomas. arXiv:2603.03116 (2026-03-03) [verified]. OpenReview shows only the CoRR record; no venue.
- **Problem & contribution:** "Current benchmarks evaluate mainly whether a task was completed, not how." **Corrupt success** means achieving the correct terminal state through procedural violations.
- **Method:**
  - Procedure formalisation F=(E, A, O, T, Ω) with a tripartite action model: Read, Write, Communicate.
  - Structured observations: context (policy), system (tool returns), communication.
  - Four consistency pairs become **integrity invariants**:
    - policy compliance O^ctx↔A;
    - policy faithfulness O^ctx↔A^C;
    - execution consistency A^C↔(A^R, A^W);
    - data faithfulness O^sys↔A^C, "data in A^C_t ⊆ O^sys_≤t".
  - Four axes: Utility, Efficiency, Interaction Quality, Procedural Integrity.
  - Gated utility U′ = U·I_pc·I_pf·I_ec·I_df·I_intent·I_qf.
  - The judge is GPT-5 over the full transcript.
- **Evaluation:**
  - τ-bench retail and airline; GPT-5, Kimi-K2-Thinking, Mistral-Large-3; k=4.
  - 27–78% of successes are corrupt.
  - Gated Pass^4 ≤0.24 for every model.
  - Ranking reversal: Kimi vs Mistral in retail.
  - Judge validation: an automatic proxy gives >89%; a human spot-check of 150 gives 89.3%; all 131 Airline corrupt successes checked manually give 93.8–95.2% precision.
  - Per-model error profiles.
  - Benchmark flaws found: simulator artifacts that produce "accidental successes".
- **Must NOT claim:**
  - the "corrupt success" / gated-utility concept;
  - multi-axis profiles that disqualify outcomes;
  - checking that agent statements are grounded in observed tool data (I_df).
- **Leaves open:**
  - Their Limitation 2, verbatim: "PAE is a behavioral audit and cannot surface reasoning-level errors in agents that happen to produce correct outputs through flawed inference."
  - Binary, non-severity-weighted gates.
  - Explicit policies are needed.
  - No interventions, no held-out generation, no delegation.
  - Their I_df checks that *communicated* data appear in observations; it does not check that the *action* depends on the right observation.
- **Differentiation:** "PAE gates success on consistency between what an agent observed, said and did; WorkTrace tests what PAE explicitly leaves out, namely whether a correct action would survive removal, inversion or corroboration of the evidence it should depend on."
- **Cautions:** preprint; three models; a single judge model (GPT-5) evaluating GPT-5 (self-preference risk is not discussed in what I read).

#### GroundEval
- **Bib:** Jeffrey Flynt. "GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation." arXiv:2606.22737 (v1 2026-06-22; v2 read) [verified]. No venue. Single author.
- **Problem & contribution:** **"State-invalid correct"**: "its final answer matches the expected label or world state, but the answer is produced from evidence that violates the evaluation state". Examples: temporal leakage, permission leakage, invalid absence, invalid causality, ungrounded citation, cross-user memory leak.
- **Method:**
  - A reviewed, machine-checkable **task contract** covering required checks, allowed evidence, temporal horizon, access policy and answer schema. It is drafted by "Observe Mode" from a run and then corrected by a human.
  - Three tracks: Perspective (visibility cone in time × role), Counterfactual (cause/effect join keys), Silence (search-space coverage before claiming absence).
  - Dual score, answer + trajectory, with track weights (0.4/0.6, 0.5/0.5, 0.3/0.7).
  - Compliance factor (1−v)².
  - §5.4 leakage controls:
    - the question-prose LLM never sees the label;
    - prose with label strings or IDs is rejected;
    - caps per actor and event type;
    - balance of positive vs negative cases;
    - global shuffle;
    - deterministic template fallback.
- **Evaluation:**
  - OrgForge synthetic enterprise: 22,530 events, 72 actors, 9 subsystems.
  - 96 questions; one model (DeepSeek-V4-Pro).
  - Zero-shot no-artifact baseline as an answer floor (Perspective 0.200 vs gated 0.214, which suggests phrasing leaks answers).
  - Overall S_adj = 0.350.
  - Three worked examples, in which two LLM judges scored a wrong answer 0.90 and 0.85.
  - **No rate of state-invalid correct answers is reported**: all three worked examples have a wrong answer.
- **Must NOT claim:**
  - the concept of a "correct answer from an invalid evidence path";
  - deterministic scoring of evidence paths against access and time constraints;
  - "what the actor could have known at time t" as part of the evaluation state (overlaps our "information available at decision time" field I_i).
- **Leaves open:**
  - Evidence *access* validity (was the evidence reachable or allowed?) is not evidence *dependence* (did the decision rest on it?).
  - No interventions.
  - No redundancy handling.
  - No quantification of how common state-invalid correctness is.
  - No delegation.
- **Differentiation:** "GroundEval checks whether the evidence an agent touched was permitted and in scope at decision time; WorkTrace checks whether the agent's action actually depends on the decisive evidence, by intervening on it, and turns per-class results into a delegation decision."
- **Cautions:** single-author preprint; n=96 questions, one model. The headline example (0.85 vs 0.000) concerns a *wrong* answer, so it does not demonstrate "correct but invalid". Cite as conceptual precedent only.

#### Causal Sensitivity Score (CSS)
- **Bib:** Matt Turk. "Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents." arXiv:2605.30590 (2026-05-28) [verified]. No venue. Single author.
- **Problem & contribution:** "Does the output look right?" vs "Is the model updating its output for the right reasons?" A pre-registered interventional metric.
- **Method:**
  - 12 interventions in 5 families committed in a YAML catalogue before any evaluation: biomarker flip, prior-treatment injection, biomarker strip, surgery-status toggle, stage perturbation.
  - Each entry has an applicability filter, a regex mutation, the expected change and a {0, 0.5, 1} scoring rule.
  - The judge compares baseline and mutated recommendations.
  - In the agent setting, the mutation propagates through tool returns (`read_chart_section`).
- **Evaluation:**
  - 224 oncology cases; 6 frontier models.
  - CMS vs CSS: ρ=−0.49 (p=0.36, n=6, underpowered); all six models change rank.
  - Family D (surgery status) ≤17.2% for all models.
  - Agent mode: +2.5 to +20.3 pp for 5 of 6 models; gpt-5.4 stays at 0.050 "despite retrieving the same chart sections".
  - Human validation: LLM-vs-majority κ=0.46; family κ for D is 0.16 and for C is 0.07.
  - 37 of 100 mutated rows were flagged medically incoherent; 73 of 153 Family C mutations were regex no-ops.
- **Must NOT claim:**
  - pre-registered interventions on external inputs with expected direction;
  - "rank reversal between coverage and interventional metrics";
  - mutation via tool returns in agents.
- **Leaves open:**
  - No redundancy control (removing one biomarker mention while another remains is listed as a failure mode: "incomplete propagation").
  - No independent-second-source intervention.
  - No ground truth on the decisive evidence beyond the catalogue.
  - Real (not generated) cases.
  - No held-out generation.
  - No delegation.
- **Differentiation:** "CSS shows that interventional responsiveness and output quality can rank models in opposite orders; WorkTrace builds the interventions into generated episodes whose decisive evidence and redundancy structure are known by construction, so that non-response can be told apart from correct robustness to redundant evidence."
- **Cautions:**
  - Single-author preprint; n=6 models.
  - Low per-family κ.
  - Many no-op or incoherent mutations.
  - The catalogue has not been clinically vetted (App. M, per §2.1).
  - **Lesson for us:** generated interventions need semantic validity checks.

#### Spurious Tool Use
- **Bib:** Yiwei Yang, Haoxiang Zhang, Bingbing Wen, Yao Lu, Yuchen Wu, Lei Zhang, Julian McAuley, Pan Lu, Bill Howe. "Spurious Tool Use: When RL Agents Learn the Wrong Reason to Act." arXiv:2609.16268 (2026-09-14) [verified]. No venue.
- **Problem & contribution:** Cue-driven tool selection in RL-trained agents. From §1: "an unnecessary tool call does not always degrade the final answer … these spurious behaviors can persist undetected under standard evaluation protocols that focus solely on final-answer correctness."
- **Method:**
  - A synthetic NQ + DeepMath mixture with injected, causally irrelevant cues.
  - Counterfactual evaluation groups (cue present vs absent, same question).
  - ΔTool_{Y−N} measures cue-driven tool choice.
  - Group-robustness framing (Sagawa et al.).
- **Evaluation:**
  - Spurious search calls rise by up to +39.2% with search-semantic cues.
  - Code cues have no effect (the shortcut forms only for the well-learned tool).
  - A dense "tool-necessity" LLM-judge reward mitigates the effect.
- **Must NOT claim:**
  - planted spurious cues in synthetic agent environments with counterfactual pairs as a novel method;
  - "the shortcut lives in intermediate decisions invisible to answer correctness".
- **Leaves open:** It is about training-induced shortcuts in *tool selection*, measured as rates. It does not cover decisions over external evidence, per-episode basis verdicts, redundancy, or delegation.
- **Differentiation:** "Yang et al. show that RL agents can learn to choose tools for the wrong reason without harming final answers; WorkTrace evaluates the evidential basis of consequential decisions at deployment time and uses it to allocate decision rights."
- **Cautions:** preprint; synthetic and small (1,000 training examples).

#### OpenClawBench, AgentLens, ClawTrack (abstract + intro)
- **OpenClawBench:** Yibing Liu, Yangze Liu, Xiaolong Yin, Bin Wang, Chong Zhang, Hao Yin, Zhongyi Han. "OpenClawBench: Benchmarking Process-side Anomalies in Real-world Agent Execution Trajectories." arXiv:2605.29253 (2026) [verified].
  - Names the **Outcome–Process Gap**.
  - 31,264 BFCL-driven OpenClaw trajectories from 6 source models.
  - 9.33% of oracle-passing runs are anomalous (silver labels; 96.0% agreement on a 300-trajectory human audit).
  - Anomaly classes include "weakly grounded commitments".
  - A fine-tuned 12B detector reaches F1 0.729.
  - *Must not claim:* the name or the measurement of an outcome–process gap.
  - *Differentiation:* observational anomaly labels on real logs vs interventional basis tests on generated episodes.
  - *Caution:* silver labels.
- **AgentLens:** Priyam Sahoo, Gaurav Mittal, Xiaomin Li, Shengjie Ma, Benjamin Steenhoek, Pingping Lin, Yu Hu. "AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation." arXiv:2605.12925 (2026). FAGEN@ICML 2026 poster [verified].
  - 2,614 OpenHands trajectories across 8 backends.
  - A Prefix-Tree-Acceptor reference built from passing solutions.
  - Lucky Pass 10.7%, Solid 69.1%, Ideal 20.2% of 1,136 passing trajectories.
  - Rank shifts of up to 5 positions.
  - *Differentiation:* process quality is judged against *other passing trajectories* (a behavioural norm), not against an evidential ground truth.
- **ClawTrack:** Xingjian Wu, Xuhang Zhu, Xingchen Liu, Junlin Liu, Jianing Wang, Linsen Guo, Xiaoyu Li, Xuezhi Cao, Xunliang Cai. arXiv:2607.28037 (2026) [verified].
  - 320 tasks, 21 models, 16k+ trials.
  - A Process Grader over 12,541 rubric items in 4 dimensions (goal alignment, efficiency, **information utilization**, result verification).
  - "Filtering lucky passes invisible to outcome-only evaluation"; result verification is the bottleneck.
  - *Differentiation:* rubric-scored process quality vs an intervention-tested basis.
  - *Caution:* LLM-judge rubrics.

#### Evidence-grounding benchmarks (abstract + intro)
- **EnvTrustBench:** Strick Sheng, Ziyue Wang, Liyi Zhou. "When Agents Overtrust Environmental Evidence: An Extensible Agentic Framework for Benchmarking Evidence-Grounding Defects in LLM Agents." arXiv:2605.08828 (2026) [verified].
  - An "evidence-grounding defect" means treating an environment claim "as sufficient ground for action, without resolving it against available current evidence".
  - A generator builds the workspace, environment, objective and **validation oracle**.
  - Agents complete the false path in 3,206 of 3,850 runs (14 model–scaffold stacks; 55 cases).
  - *Relation:* this measures wrong-basis *failures*, i.e. a false path, and it is close to our "invert X" intervention with a verification opportunity. It does **not** measure correct outcomes on a wrong basis.
  - *Must not claim:* generated environments with oracles for testing over-trust in stale or wrong evidence.
- **SeekBench:** Jiaqi Shao, Yuxiang Lin, Munish Prasad Lohani, Yufeng Miao, Bing Luo. "Do LLM Agents Know How to Ground, Recover, and Assess? A Benchmark for Epistemic Competence in Information-Seeking Agents." arXiv:2509.22391 (2025) [verified].
  - 190 expert-annotated traces (>1,800 steps).
  - Groundedness, recovery, and **calibration of evidence sufficiency** (answering with insufficient evidence vs refusing when it is sufficient).
  - *Relation:* an epistemic-competence profile annotated post hoc, with no interventions. It is a close cousin of our "proceed vs escalate under insufficient evidence".
- **ST-WebAgentBench:** Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, Nir Mashkif, Segev Shlomov. arXiv:2410.06703. ICLR 2026 [verified].
  - 375 tasks, 3,057 policies.
  - **Completion Under Policy (CuP)** "credits only completions that respect all applicable policies".
  - Average CuP is "less than two-thirds" of nominal completion.
  - *Must not claim:* policy-gated success metrics for web agents.
- **SOPBench:** Zekun Li, Shinda Huang, Jiangtian Wang, Nathan Zhang, Antonis Antoniades, Wenyue Hua, Kaijie Zhu, Sirui Zeng, Chi Wang, William Yang Wang, Xifeng Yan. arXiv:2503.08669 (2025) [verified]. OpenReview: submitted to ICLR 2026 and ACL ARR 2026 [no accepted venue found].
  - 7 customer-service domains (including bank), 167 tools.
  - SOPs compiled to executable directed graphs that serve as oracle verifiers.
  - **Automated generation of >900 verified test cases.**
  - Error analysis: "procedural errors is the major error cause … models often overlook necessary verification steps and directly executing service functions." This is an *action without checking the warranting constraint*, i.e. potentially correct outcome on an unverified basis. The text gives no number.
  - *Must not claim:* executable verification of SOP adherence in banking-like domains.

#### Trajectory judges and process rewards (abstract-level)
- **Agent-as-a-Judge:** Mingchen Zhuge, Changsheng Zhao, Dylan Ashley, Wenyi Wang, Dmitrii Khizbullin, Yunyang Xiong, Zechun Liu, Ernie Chang, Raghuraman Krishnamoorthi, Yuandong Tian, Yangyang Shi, Vikas Chandra, Jürgen Schmidhuber. arXiv:2410.10934. ICML 2025 [verified].
  - DevAI: 55 tasks, 365 hierarchical requirements.
  - Alignment with human judges is 92.07% / 90.44% vs LLM-as-a-Judge 70.76% / 60.38% (OpenHands; gray/black-box).
  - Pairwise human disagreement 10–30%.
  - *Relation:* it judges requirement satisfaction along the trajectory, not evidential basis.
- **AgentRewardBench:** Xing Han Lù, Amirhossein Kazemnejad, Nicholas Meade, Arkil Patel, Dongchan Shin, Alejandra Zambrano, Karolina Stańczak, Peter Shaw, Christopher J. Pal, Siva Reddy. arXiv:2504.08942. COLM 2025 [verified].
  - 1,302 expert-reviewed web-agent trajectories; 12 LLM judges; "no single LLM excels".
  - Rule-based evaluation *underreports* success. Note: outcome checks can err in both directions.
- **An Illusion of Progress? (Online-Mind2Web):** Tianci Xue, Weijian Qi, Tianneng Shi, Chan Hee Song, Boyu Gou, Dawn Song, Huan Sun, Yu Su. arXiv:2504.01382. COLM 2025 [verified]. Reported web-agent success is over-optimistic; WebJudge agrees with humans about 85% of the time.
- **AgentPRM:** Sanjiban Choudhury. "Process Reward Models for LLM Agents: Practical Framework and Directions." arXiv:2502.10325 (2025) [verified; venue unknown]. Monte-Carlo process rewards for agents (ALFWorld); discusses reward hacking.
- **TRAIL** (Deshpande et al., arXiv:2505.08638 [verified]; ACL ARR 2025 submission), **MAST** "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al., arXiv:2503.13657; NeurIPS 2025 D&B spotlight [verified]), **Who&When** (Zhang et al., arXiv:2505.00212; ICML 2025 spotlight [verified]): trace error taxonomies and failure attribution, *mostly on failed runs*. Who&When: best method localises the failure step only 14.2% of the time.
- **One sentence for all of these:** "Trajectory judges, process reward models and failure-attribution datasets evaluate or localise step quality, mostly with LLM judges and mostly on failures; WorkTrace instead tests the causal dependence of a decision on its evidence, including in successful episodes, with ground truth fixed by the episode generator."

### B4. Outcome vs process classics; shortcut learning

#### Uesato et al. 2022
- **Bib:** Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, Irina Higgins. "Solving math word problems with process- and outcome-based feedback." arXiv:2211.14275 (2022) [verified; preprint, only the CoRR record found].
- **Content:**
  - On GSM8K, outcome supervision gives similar final-answer error with less labelling, but "for correct reasoning steps we find it necessary to use process-based supervision or … reward models that emulate process-based feedback".
  - Final-answer error 16.8%→12.7%; trace error 14.0%→3.4%.
  - Final-answer RL leaves the best trace error at 12.4% vs 3.8% for process-based.
  - From §2: "from a safety perspective, we are particularly interested in errors which remain undetected after applying easy-to-compute proxy metrics".
- **Must NOT claim:** that correct-outcome/incorrect-process is a new measurement target.
- **Leaves open:** Agents, external evidence, interventions (trace errors are human-annotated).
- **Differentiation:** "Uesato et al. measured how often correct final answers rest on flawed reasoning traces, by human annotation; WorkTrace measures how often correct agent actions rest on the wrong evidence, by intervention, with ground truth fixed by construction."

#### Lightman et al. 2023 — Let's Verify Step by Step
- **Bib:** Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, Karl Cobbe. arXiv:2305.20050. ICLR 2024 [verified].
- **Content (abstract):** Process supervision beats outcome supervision on MATH (78% solved on a representative subset).
- Cite only as the standard reference for process vs outcome supervision.

#### ProcessBench
- **Bib:** Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren Zhou, Junyang Lin. arXiv:2412.06559. ACL 2025 [verified].
- **Content (§3.3, Table 2):** Share of correct-final-answer solutions that contain process errors: GSM8K 3.5%, MATH 18.8%, OlympiadBench 32.2%, Omni-MATH 51.8%.
- **Use:** the rate of correct-on-wrong-basis rises with difficulty. This predicts that our harder decision classes will show more basis errors among successes, which is a testable expectation for the pilot.

#### "Right Answer, Wrong Method" (abstract only)
- **Bib:** Xuan Ren, Weiqi Zhai, Tianle Pu, Yihua Zhu, Yihua Zhu [listed twice in arXiv metadata], Hu Wei, Bing Zhao. "Right Answer, Wrong Method: Shortcut Hacking Misleads the Evaluation of LLM Reasoning on Frontier Science Benchmarks." arXiv:2608.02442 (2026) [verified; comment: "working in progress"].
- **Content:** "Solution hacking" rises from 2.2% on common problems to 28.3% on Olympiad problems and 37.4% on HLE; 8.2–44.1% of answers credited as correct are hacked.
- **Caution:** work in progress; not agents.

#### Geirhos et al. 2020 — Shortcut learning in deep neural networks
- **Bib:** Robert Geirhos, Jörn-Henrik Jacobsen, Claudio Michaelis, Richard Zemel, Wieland Brendel, Matthias Bethge, Felix A. Wichmann. *Nature Machine Intelligence* 2(11):665–673, 2020. doi:10.1038/s42256-020-00257-z [verified Crossref]; arXiv:2004.07780.
- **Content:**
  - A taxonomy of decision rules: training solutions ⊃ i.i.d. solutions ⊃ intended solutions. Shortcuts pass i.i.d. tests but fail o.o.d. tests (§3).
  - Recommendations (§7): connect the dots; interpret results carefully; "o.o.d. generalisation tests will need to become the rule rather than the exception"; understand what makes solutions easy to learn.
  - "Morgan's Canon for machine learning" (§6.1).
  - "Testing (surprisingly) strong baselines" (§6.1).
- **Must NOT claim:** that "right outcome, wrong rule" is a new idea.
- **Leaves open:** Agents; decisions with explicit evidence; operational tests per decision.
- **Differentiation:** "WorkTrace operationalises Geirhos et al.'s distinction between intended and shortcut decision rules for agent decisions: instead of hoping an o.o.d. test set exposes a shortcut, each episode's interventions are an o.o.d. test targeted at the evidence the intended rule must use."

#### Classics verified on Crossref but not read (cite for lineage only)
- R. Thomas McCoy, Ellie Pavlick, Tal Linzen. "Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference." ACL 2019, pp. 3428–3448. doi:10.18653/v1/P19-1334 [verified]. HANS.
- Andrew Slavin Ross, Michael C. Hughes, Finale Doshi-Velez. "Right for the Right Reasons: Training Differentiable Models by Constraining their Explanations." IJCAI 2017, pp. 2662–2670. doi:10.24963/ijcai.2017/371 [verified].
- Sebastian Lapuschkin, Stephan Wäldchen, Alexander Binder, Grégoire Montavon, Wojciech Samek, Klaus-Robert Müller. "Unmasking Clever Hans predictors and assessing what machines really learn." *Nature Communications* 10, 2019. doi:10.1038/s41467-019-08987-4 [verified].

### B5. Dynamic, generative, held-out benchmark practice

#### Procgen
- **Bib:** Karl Cobbe, Christopher Hesse, Jacob Hilton, John Schulman. "Leveraging Procedural Generation to Benchmark Reinforcement Learning." ICML 2020 (PMLR 119) [verified OpenReview DBLP record]; arXiv:1912.01588.
- **Content:**
  - 16 procedurally generated environments, with level layout, assets and spawn times conditioned on the level seed.
  - "Distinct training and test sets can be generated for each environment."
  - Agents "strongly overfit to small training sets"; closing the gap needs up to about 10,000 levels.
  - Recommended protocol: train on 500 levels, test on held-out levels.
- **Use:** the seed-split protocol, and the finding that overfitting to a finite set of generated instances is real, so the size of the calibration set matters.
- **Differentiation:** Procgen splits seeds for *environments*; we split seeds for *decision episodes*, and additionally hold out surface templates.

#### τ²-bench compositional generator — see B1.

#### Power Systems Agent Benchmark (held-out-by-generator)
- **Bib:** Sergei Trashchenkov. "Power Systems Agent Benchmark: Executable Evaluation of AI Agents in Electric Power Engineering." arXiv:2606.20950 (2026) [verified]; Zenodo doi:10.5281/zenodo.20753046 (from the arXiv comment, not checked separately).
- **Content (§4.4, §8.1–8.2):**
  - "The benchmark does not store its held-out cases at all. In place of held-out data files, it provides a generator".
  - Cases are redrawn from public cases under a **private random seed**. A draw is accepted only if the reference solver solves it, the evaluator confirms feasibility and no small perturbation scores higher.
  - "Auditable in mechanism and private in content at the same time".
  - Only aggregate summaries are published, never per-case held-out submissions or logs.
  - A held-out-above-public pattern would signal contamination; none was found.
  - **"Treat a unanimous failure as a likely defect in the specification or the evaluator"**. An evaluator bug went unnoticed because "the reference solver used for self-checking is derived from the same function as the evaluator".
- **Use:** almost exactly our anti-Goodhart mechanism (3) ("public methodology, protected instances"). **We must not claim it as novel; cite it.** The shared-code warning applies directly to a generator whose ground truth and checker come from the same code.
- **Caution:** single author; domain-specific; top agents near ceiling.

#### LiveBench
- **Bib:** Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid Shwartz-Ziv, Neel Jain, Khalid Saifullah, Sreemanti Dey, Shubh-Agrawal, Sandeep Singh Sandha, Siddartha Naidu, Chinmay Hegde, Yann LeCun, Tom Goldstein, Willie Neiswanger, Micah Goldblum. arXiv:2406.19314. ICLR 2025 (Spotlight) [verified].
- **Content:**
  - Questions come from recent sources and are scored against objective ground truth.
  - Rotation: "In each update, we replace 1/6 of the questions on average, so that the benchmark is fully refreshed roughly every 6 months … we do not release the new questions until one month later, so that the public leaderboard always has 1/6 questions that are private."
- **Use:** a concrete rotation schedule.

#### LiveCodeBench (abstract)
- **Bib:** Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, Ion Stoica. arXiv:2403.07974. ICLR 2025 [verified].
- Continuously collects time-stamped contest problems, which enables contamination detection by release date.

#### GSM1k
- **Bib:** Hugh Zhang, Jeff Da, Dean Lee, Vaughn Robinson, Catherine Wu, Will Song, Tiffany Zhao, Pranav Raja, Charlotte Zhuang, Dylan Slack, Qin Lyu, Sean Hendryx, Russell Kaplan, Michele Lunati, Summer Yue. "A Careful Examination of Large Language Model Performance on Grade School Arithmetic." arXiv:2405.00332. NeurIPS 2024 Datasets & Benchmarks (Spotlight) [verified].
- **Content:**
  - A held-out mirror of GSM8K; drops of up to 8%; Spearman r²=0.36 between memorisation probability and gap.
  - Release policy: "We encourage future benchmarks to follow a similar pattern, where they are not released publicly lest they be gamed, but are precommitted to be released at a future date or upon a future condition."
- **Use:** pre-committed release of the held-out set.

#### GSM-Symbolic (abstract)
- **Bib:** Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, Mehrdad Farajtabar. arXiv:2410.05229. ICLR 2025 [verified].
- **Content:** Symbolic templates generate instances. Performance varies across instantiations. Adding "a single clause that appears relevant" but is irrelevant (the NoOp variant) causes drops of up to 65%.
- **Use:** template-based instance variation, and evidence that irrelevant-but-plausible additions move decisions. This is relevant to our "add an independent second source" and to distractor control.
- **Caution:** a critical re-evaluation exists as an ACL ARR 2026 submission on OpenReview ("The Importance of Being Statistically Earnest…") [title seen, not read].

#### Dynabench (abstract)
- **Bib:** Douwe Kiela, Max Bartolo, Yixin Nie, Divyansh Kaushik, Atticus Geiger, Zhengxuan Wu, Bertie Vidgen, Grusha Prasad, Amanpreet Singh, Pratik Ringshia, Zhiyi Ma, Tristan Thrush, Sebastian Riedel, Zeerak Waseem, Pontus Stenetorp, Robin Jia, Mohit Bansal, Christopher Potts, Adina Williams. NAACL 2021, pp. 4110–4124. doi:10.18653/v1/2021.naacl-main.324 [verified].
- Human-and-model-in-the-loop adversarial data creation; dynamic benchmarking against saturation.

#### Recht et al. 2019 (abstract)
- **Bib:** "Do ImageNet Classifiers Generalize to ImageNet?" ICML 2019 [verified OpenReview DBLP record]; arXiv:1902.10811. Authors: Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, Vaishaal Shankar [verified arXiv].
- **Content:** Re-creating the test sets gives drops of 3–15% (CIFAR-10) and 11–14% (ImageNet).

#### Leaderboard Illusion (abstract)
- **Bib:** Shivalika Singh, Yiyang Nan, Alex Wang, Daniel D'Souza, Sayash Kapoor, Ahmet Üstün, Sanmi Koyejo, Yuntian Deng, Shayne Longpre, Noah A. Smith, Beyza Ermis, Marzieh Fadaee, Sara Hooker. arXiv:2504.20879. NeurIPS 2025 D&B [verified].
- **Content:** Undisclosed private testing and selective retraction (27 private Llama-4 variants) distort Chatbot Arena.
- **Use:** if certification episodes are private, submissions must be rate-limited and all attempts reported.

#### Also verified, abstract-level
- **SWE-Bench Pro:** Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer, Andrew Park, Nitin Pasari, Chetan Rane, Karmini Sampath, Maya Krishnan, Srivatsa Kundurthy, Sean Hendryx, Zifan Wang, Vijay Bharadwaj, Jeff Holm, Raja Aluri, Chen Bo Calvin Zhang, Noah Jacobson, Bing Liu, Brad Kenstler. arXiv:2509.16941 [verified]. Public / held-out / commercial three-way split; held-out and commercial sets are not public.
- **Reasoning Gym:** Zafir Stojanovski, Oliver Stanley, Joe Sharratt, Richard Jones, Abdulhakeem Adefioye, Jean Kaddour, Andreas Köpf. arXiv:2505.24760. NeurIPS 2025 D&B (Spotlight) [verified]. More than 100 procedural generators and verifiers with adjustable difficulty.

### B6. Goodhart's law in evaluation

#### Manheim & Garrabrant 2018
- **Bib:** David Manheim, Scott Garrabrant. "Categorizing Variants of Goodhart's Law." arXiv:1803.04585 (v4, 2019) [verified; preprint].
- **Content:** "A Goodhart effect is when optimization causes a collapse of the statistical relationship between a goal which the optimizer intends and the proxy used for that goal." Four types:
  1. **Regressional**: "selection for an imperfect proxy necessarily also selects for noise"; it "cannot be avoided".
  2. **Extremal**: model insufficiency or regime change at extreme values.
  3. **Causal**: intervention on a shared cause, an intermediary, or the metric itself.
  4. **Adversarial**: misalignment (Campbell's law) and the Cobra effect.
- **Use for WorkTrace:**
  - (i) Regressional: selecting the decision classes with the *highest* observed scores for autonomy will overestimate their true reliability. We need held-out re-estimation or a shrinkage / upper-bound rule. Our α-bound on held-out data addresses this.
  - (ii) Extremal: certification thresholds sit at the extreme, where the relation between proxy and target may change. We need held-out episodes near the decision boundary.
  - (iii) Adversarial: once the intervention types are public, agent developers can train for them (Campbell's law). This motivates private seeds and rotation, and possibly unannounced intervention variants.
  - (iv) Causal / metric manipulation: an agent that *declares* grounds can tune declarations without changing behaviour. This is why we test behaviour under intervention rather than the declared graph.
- **Differentiation:** none needed; cite as the framework for the anti-Goodhart section.
- **Cautions:** an arXiv preprint, never formally published as far as I know [not checked].

#### Thomas & Uminsky 2022
- **Bib:** Rachel L. Thomas, David Uminsky. "Reliance on metrics is a fundamental challenge for AI." *Patterns* 3(5):100476, 2022. doi:10.1016/j.patter.2022.100476 [verified Crossref]; open access PMC9122957. An earlier arXiv version, 2002.08512, is titled "The Problem with Metrics is a Fundamental Problem for AI" (EDSC 2020).
- **Content:**
  - Principles: "Any metric is just a proxy for what you really care about"; "Metrics can, and will, be gamed"; metrics overemphasise the short term; metrics are gathered in addictive environments.
  - Framework: (1) "use a slate of metrics to get a fuller picture (and resist the temptation to try to boil these down to a single score)"; (2) external algorithmic audits; (3) combine with qualitative accounts; (4) involve stakeholders.
  - Directly useful quote: "effective algorithmic audits will need to consider the company's processes and not just final performance on a benchmark."
  - Likierman, quoted by them: "it's a lot harder to game several of them at once."
- **Use:** justification for the multidimensional profile and for process-sensitive auditing.

#### Also verified, not read in full
- **Marilyn Strathern 1997.** "'Improving ratings': audit in the British University system." *European Review* 5(3):305–321. doi:10.1002/(SICI)1234-981X(199707)5:3<305::AID-EURO184>3.0.CO;2-4 [verified Crossref]. The source of the popular "When a measure becomes a target…" phrasing.
  - **Caution:** Thomas & Uminsky attribute the popular phrasing via Goodhart's encyclopedia entry. I have **not** checked the exact page or wording in Strathern.
- **Goodhart 1975**, "Problems of Monetary Management: The U.K. Experience", Papers in Monetary Economics, Reserve Bank of Australia. Cited in M&G [not verified independently].
- **Skalse et al. 2022.** Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, David Krueger. "Defining and Characterizing Reward Hacking." arXiv:2209.13085. NeurIPS 2022 [verified; the OpenReview NeurIPS title is "Defining and Characterizing Reward **Gaming**"]. Formal unhackability is a very strong condition.
- **Gao, Schulman, Hilton.** "Scaling Laws for Reward Model Overoptimization." arXiv:2210.10760. ICML 2023 [verified]. Quantified proxy-reward overoptimisation.

### B7. Multidimensional profiles vs single scores

#### HELM (abstract + multi-metric section header)
- **Bib:** Percy Liang, Rishi Bommasani, Tony Lee, and 47 further authors (the full list of 50 is in the arXiv record), "Holistic Evaluation of Language Models." arXiv:2211.09110. TMLR 2023 [verified].
- **Content:**
  - 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) × 16 core scenarios, "ensuring that metrics beyond accuracy don't fall to the wayside, and that trade-offs across models and metrics are clearly exposed".
  - Scenario coverage of prior evaluations was 17.9%; HELM reaches 96.0%.
- **Use:** the precedent for profile-not-score. Our profile is per decision class × capability; HELM's is per scenario × metric.
- **Differentiation:** "HELM made multi-metric profiles standard for models; WorkTrace builds a per-decision-class profile of evidence handling and uses it to allocate decision rights, rather than to rank systems."

#### Others
- **Ethayarajh & Jurafsky 2020.** Kawin Ethayarajh, Dan Jurafsky. "Utility is in the Eye of the User: A Critique of NLP Leaderboards." EMNLP 2020, pp. 4846–4853. doi:10.18653/v1/2020.emnlp-main.393 [verified; abstract read]. Leaderboards are poor proxies for practitioners' utility.
- **Burnell et al. 2023.** Ryan Burnell, Wout Schellaert, John Burden, Tomer D. Ullman, Fernando Martinez-Plumed, Joshua B. Tenenbaum, Danaja Rutar, Lucy G. Cheke, Jascha Sohl-Dickstein, Melanie Mitchell, Douwe Kiela, Murray Shanahan, Ellen M. Voorhees, Anthony G. Cohn, Joel Z. Leibo, Jose Hernandez-Orallo. "Rethink reporting of evaluation results in AI." *Science* 380(6641):136–138. doi:10.1126/science.adf6369 [verified Crossref; **not read**]. To my knowledge it argues for instance-level reporting instead of aggregates. Confirm before citing that claim.

---

## C. Best practices to adopt for the episode generator (with citations)

Every item is an adoption, **not** a novelty claim.

1. **Seeded procedural generation with disjoint calibration and held-out seeds** (Cobbe et al. 2020). Report calibration-vs-held-out gaps; Procgen shows that overfitting to finite generated sets is real.
   - Make the size of the calibration set an explicit parameter.
   - Plot the gap between calibration and held-out risk as the set grows (an analogue of Procgen Fig. 2).
2. **Compositional generation from atomic, verifiable components** (τ²-bench). Define each decision class as a set of atomic evidence modules (initialisation, decisive evidence, distractors, redundant copies) with solution and assertion functions, so that the correct action and the decisive evidence are known by construction. Groups of mutually exclusive modules control combinatorics.
3. **Generator public, instances private** (Power Systems Agent Benchmark §4.4; GAIA withheld answers; SWE-Bench Pro held-out/commercial sets).
   - Publish the generator code and intervention catalogue.
   - Keep the held-out seed private.
   - Accept a draw only if a reference policy solves it.
   - Publish only aggregate held-out results, never per-episode held-out logs ("each disclose that case's answer").
4. **Independent checking of the generator's own ground truth** (Power Systems §8.2; Wang et al. PatchDiff). Do not derive the reference decision and the checker from the same function. Use a second, independently written oracle on a sample, and treat *unanimous* agent failure on an episode as a suspected generator defect until inspected.
5. **Rotation** (LiveBench): replace a fixed fraction of templates or seeds per round (LiveBench uses 1/6 per month with a one-month private lag). Version every release.
6. **Pre-committed release** (GSM1k): commit to releasing retired held-out seeds after rotation, so the held-out set can be audited later without remaining gameable.
7. **Holdout level matches the claimed generality** (Kapoor et al. 2024, Table 1).
   - If we claim per-class delegation generalises to *new instances*, held-out seeds suffice.
   - If we claim it generalises to *new surface forms*, hold out templates and phrasings.
   - If we claim transfer across *domains*, hold out the domain (counterparty verification vs Auditable Design).
   - State the level explicitly.
8. **Leakage controls in LLM-generated text** (GroundEval §5.4):
   - the prose generator never sees the label;
   - reject text containing ground-truth strings or IDs;
   - cap per entity and type;
   - balance positive, negative and insufficient-evidence cases;
   - shuffle;
   - keep a deterministic template fallback.
9. **No-evidence and trivial-policy baselines** (GroundEval zero-shot floor; ABC's empty-response agent at 38% on τ-bench; Geirhos's "surprisingly strong baselines"; the "matched no-feedback fallback" of Zhang et al., arXiv:2606.21409 [abstract only]).
   - Always report always-proceed, always-escalate, always-refuse, and a no-evidence-access agent.
   - If the no-evidence agent is close to the full agent, the episodes leak the answer.
10. **"Impossible" or insufficient-evidence episodes** (ImpossibleBench; SeekBench calibration). Include episodes in which *any* proceed is unwarranted. Measure the proceed rate as a direct estimate of propensity to act on a wrong basis. Note ImpossibleBench's finding that an explicit abort/escalate option lowers cheating, so our action space must include escalate.
11. **Pre-registered intervention catalogue with expected direction** (Turk, CSS). Each intervention fixes in advance its applicability filter, mutation, expected change of verdict and scoring.
    - **Validate semantic effect**: CSS lost 73/153 Family C cases to no-op mutations, and annotators found 37/100 rows medically incoherent.
    - Our "remove X" and "invert X" must be checked for incomplete propagation, where another field still implies X. That is exactly the redundancy problem our design claims to handle, so it must be *tested* in the generator.
12. **Irrelevant-but-plausible additions** (GSM-Symbolic NoOp drops of up to 65%; "Agents Catching Agents", arXiv:2608.03744 [abstract only], where peer assertions are adopted 38% of the time). Include distractor and second-source variants. Separate an *independent* second source from a correlated or echoing one.
13. **Validate any LLM judge on a held-out human-labelled set** (Kirgis et al. Principle 3; CXBench admits it lacks this). Prefer deterministic verdicts, which a generator with ground-truth basis makes possible (GroundEval's judge-free argument).
14. **Submission discipline for private sets** (Leaderboard Illusion): cap the number of held-out evaluations per agent configuration and report all of them, to avoid best-of-N selection on the held-out set. This is also a regressional-Goodhart control (Manheim & Garrabrant).
15. **Profile, not a single score** (HELM; Thomas & Uminsky; PAE's non-redundant axes). Keep per-class, per-intervention results separate. If a gate is used for delegation, report the components too.
16. **Statistics and reporting** (ABC R.10–R.13; Kirgis et al. Principle 4): confidence intervals (Wilson, as CXBench uses); paired tests (exact McNemar, as CXBench uses for paired traces); prevalence by outcome before any risk ratio.

---

## D. Does any existing benchmark already measure "correct outcome on wrong basis" for agents? (novelty threat for H1)

**Short answer: yes, in a procedural and observational sense. Not, as far as I found, in an evidential and interventional sense with ground truth by construction.**

| Work | Measures "outcome-correct but X-wrong"? | What X is | How X is judged | Interventions? | Basis ground truth by construction? | Delegation? |
|---|---|---|---|---|---|---|
| CXBench (2610.25954) | **Yes**: false-pass 55.5% of runs | regulatory procedure (disclosure, ordering, authority) | rules + LLM judge | no | no (rule cards) | no (submission authority fixed by mode) |
| PAE (2603.03116) | **Yes**: corrupt success 27–78% | policy compliance/faithfulness, execution consistency, data faithfulness | LLM judge (GPT-5) | no | no | no |
| OpenClawBench (2605.29253) | **Yes**: 9.33% of oracle-passing | process anomalies incl. "weakly grounded commitments" | silver labels, LLM | no | no | no |
| AgentLens (2605.12925) | **Yes**: Lucky Pass 10.7% | process quality vs other passing paths | PTA reference + labeller | no | no | no |
| ClawTrack (2607.28037) | **Yes**: "lucky passes" | 4 rubric dimensions incl. information utilisation | rubric LLM grader | no | no | no |
| GroundEval (2606.22737) | **Defined** ("state-invalid correct"), **not quantified** | evidence path validity (access, time, search coverage, causal join) | deterministic contract | no | partly (access/time contract) | no |
| ST-WebAgentBench (2410.06703) | Yes: CuP < 2/3 of completion | policy adherence | rules/judge | no | no | no |
| SOPBench (2503.08669) | Partly: procedure vs outcome correctness (Fig. 8/13; no number in text) | SOP verification steps | executable oracle | no | yes (SOP graph) | no |
| τ-bench policy ablation (2406.12045) | Aggregate only | dependence on policy document | removal ablation | **yes (aggregate)** | no | no |
| Spurious Tool Use (2609.16268) | Yes (tool choice invisible to answer) | cue-driven tool selection | counterfactual cue groups | **yes** | **yes (planted cue)** | no |
| CSS (2605.30590) | Responsiveness, not "outcome-correct" | update of recommendation under input mutation | pre-registered catalogue + judge | **yes** | partly (expected direction) | no |
| ImpossibleBench (2510.20270) | Any pass = wrong basis | test exploitation | by construction | yes (task mutation) | **yes (binary)** | no (but abort option) |
| EnvTrustBench (2605.08828) | No: measures *failures* from over-trusted evidence | stale/false environment claims | oracle on final state | yes (planted claims) | yes | no |

**Assessment:**
- H1 as worded ("episode-level evaluation reveals errors invisible to outcome-only evaluation") is **already demonstrated** by CXBench, PAE, OpenClawBench, AgentLens and ClawTrack. Several of these report larger effects than we are likely to find.
- Claiming H1 as a contribution would invite a straightforward "known" objection.
- **No row has all of:**
  1. per-episode ground truth of the *decisive external evidence*;
  2. redundancy-aware interventions (remove / only / invert / independent second source);
  3. a classification of *outcome-correct* episodes into basis-correct vs basis-wrong;
  4. use of that classification to set *autonomy per decision class* with a held-out risk–coverage evaluation.

  Rows 1–3 are partly present in Spurious Tool Use (planted cue, counterfactual pairs, but tool choice under RL training) and CSS (interventions, but no redundancy model and no outcome-correct conditioning). Row 4 is absent everywhere.

**Recommended re-scoping of H1.** Turn it from a novelty claim into a sharpened, falsifiable claim positioned *against* the procedural-audit literature:

> **H1′.** Among outcome-correct decision episodes, a non-trivial fraction fail basis tests: the action does not change when the decisive evidence is removed or inverted, or it changes when only redundant evidence is removed. **A substantial share of these basis failures pass outcome-only checks *and* procedure/trace audits of the CXBench/PAE type**: the trace shows the right lookups, disclosures and confirmations.

Falsification: if procedure audits catch (almost) all basis failures, then interventions add nothing over existing process evaluation, and H1′ fails.

This gives a three-detector comparison on the same generated episodes:
1. outcome-only;
2. trace/procedure audit (rules + LLM judge over the trace, emulating PAE's I_pc / I_df);
3. WorkTrace interventions.

Report the overlap (a Venn diagram or a 2×2 per pair). CSS's "retrieved the same chart sections, still did not update" is exactly the case a trace audit would pass and an intervention would catch, so it serves as prior evidence that the gap exists.

---

## E. Draft differentiation sentences (related work)

- **Procedural-audit benchmarks (CXBench, PAE, ST-WebAgentBench, SOPBench):** "Recent benchmarks separate task outcome from procedural compliance and find that many outcome-passes violate required procedures (e.g., 80% of outcome-passes in CXBench; 27–78% of τ-bench successes in PAE). WorkTrace targets a failure these audits cannot see by construction: a decision whose trace looks compliant but whose action does not depend on the evidence that should warrant it, which we detect by intervening on that evidence."
- **Outcome–process gap datasets (OpenClawBench, AgentLens, ClawTrack):** "Where these works label process anomalies observationally in logs, against rubrics or against other successful trajectories, WorkTrace generates episodes whose decisive evidence is known by construction and tests each decision experimentally."
- **GroundEval:** "GroundEval asks whether the evidence an agent used was permitted and in scope at decision time; WorkTrace asks whether the decision actually depends on the decisive evidence, controlling for redundant evidence, and turns the answer into a revocable, per-class delegation decision."
- **Interventional evaluation (CSS, Spurious Tool Use, τ-bench policy ablation):** "Interventional metrics have shown that responsiveness to inputs and output quality can rank systems in opposite orders and that shortcut decisions persist under answer-correct evaluation; WorkTrace makes interventions redundancy-aware (remove / only / invert / add an independent source), conditions on outcome-correct episodes, and uses the results to allocate decision rights."
- **Benchmark validity critiques (ABC, SWE-Bench+, Wang et al., HAL, Kirgis et al.):** "This literature establishes that outcome scores admit successes reached through leakage, weak tests and shortcuts, and calls for experimental rather than purely observational designs (Kirgis et al.); WorkTrace provides such a design at the level of single decisions."
- **Process supervision (Uesato et al.; Lightman et al.; ProcessBench):** "Process-vs-outcome studies quantify correct answers built on flawed reasoning traces; WorkTrace transposes the question from the text of reasoning to the causal dependence of agent actions on external evidence."
- **Dynamic and generative benchmarks (Procgen, τ²-bench, LiveBench, GSM1k, Power Systems Agent Benchmark):** "We adopt established practice (seeded generation with disjoint calibration and held-out seeds, a public generator with private seeds, rotation, and pre-committed release) and contribute only what is specific to decision episodes: ground truth about which evidence is decisive."
- **Goodhart (Manheim & Garrabrant; Thomas & Uminsky; HELM):** "Our anti-Goodhart design maps onto known mechanisms: profiles instead of a single score against metric gaming (Thomas & Uminsky; HELM), private rotating instances against adversarial Goodhart, and held-out re-estimation of per-class risk against regressional Goodhart in selecting which classes to delegate."

---

## Implications for WorkTrace

**Design changes**
1. **Re-scope H1 to H1′** (§D) and add the **three-detector comparison**: outcome-only vs trace/procedure audit vs interventions.
   - Implement the procedure audit as a faithful re-implementation of the PAE invariants (I_pc, I_df) or CXBench-style rules + judge, so the comparison is with the state of the art and not a straw man.
   - Make the overlap table the headline H1′ result.
2. **Report the basis-wrong share among outcome-correct episodes**, per decision class and per difficulty (ProcessBench suggests it rises with difficulty), with Wilson CIs. Also report the *outcome-incorrect but basis-correct* cell (correct reasoning, unlucky outcome), which the procedural benchmarks rarely discuss.
3. **Generator requirements** (§C):
   - seeds split into calibration and held-out (plus held-out templates);
   - public generator with private held-out seed;
   - acceptance check by a reference policy;
   - a second, independently written oracle on a sample;
   - a unanimous-failure → defect review;
   - rotation and versioning;
   - a no-evidence baseline;
   - trivial policies (always proceed / escalate / refuse);
   - insufficient-evidence ("impossible") episodes;
   - a pre-registered intervention catalogue with an expected verdict per intervention;
   - semantic-validity checks on interventions (no-ops, incomplete propagation, incoherence).
4. **Escalation must be in the action space during evaluation, not only in the delegation rule.** ImpossibleBench shows an abort option changes agent behaviour, so the evaluated policy and its escalation propensity are entangled. Report results with and without the option.
5. **Banking pilot vs CXBench.** Either (a) explicitly import a few CXBench-style procedural rules into the counterparty-verification episodes, so procedure audits have something to catch and the comparison is fair, or (b) state clearly that our process checks are evidential, not procedural. Cite CXBench in the domain section.
6. **Deterministic verdicts where possible.** Because the generator knows the decisive evidence, the basis verdict can be computed without an LLM judge (GroundEval's argument). Reserve LLM judging for the Auditable Design domain and validate it on a held-out human-labelled set (Kirgis Principle 3).

**Risks**
- *"H1 is known"*: high if left as worded. Mitigate with H1′ and the three-detector comparison.
- *"Interventions on external inputs are known"* (CSS, Spurious Tool Use, τ-bench ablation, Matton et al. from round 1): medium. Our differentiators are redundancy-awareness, conditioning on outcome-correct episodes, and above all the delegation rule (H3). Keep H3 as the main claim, as positioning.md already concludes.
- *Generator self-consistency bugs* (Power Systems §8.2): the ground truth and the checker share code. Mitigate with an independent oracle and the unanimous-failure review.
- *Phrasing leakage*: generated episodes can be answerable without evidence (GroundEval Perspective: zero-shot 0.200 vs tool 0.214). Mitigate with the no-evidence baseline as a mandatory sanity check.
- *Small effects*: AgentLens and OpenClawBench report about 10% lucky or anomalous passes on real logs, while CXBench and PAE report much more under stricter definitions. Our basis-wrong rate depends heavily on generator design. Pre-register target rates and power for the pilot.
- *Regressional Goodhart in class selection*: picking classes for autonomy by observed calibration risk overestimates their quality. The held-out α-bound must be computed on held-out seeds that played no part in selection.

**Things to cite (priority)**
- **Must:** CXBench; PAE; GroundEval; CSS (Turk); τ-bench (incl. Table 3 ablation); ABC (Zhu et al.); Kirgis et al.; Kapoor et al. 2024; Uesato et al. 2022; Geirhos et al. 2020; Manheim & Garrabrant 2018; Thomas & Uminsky 2022; HELM; Procgen; τ²-bench; Power Systems Agent Benchmark; ImpossibleBench.
- **Should:** SWE-Bench+; Wang et al. ICSE 2026; ProcessBench; AgentLens; OpenClawBench; Spurious Tool Use; LiveBench; GSM1k; SOPBench; ST-WebAgentBench; HAL; EnvTrustBench; SeekBench.
- **Could:** WebArena, GAIA, AgentBench, SWE-bench (as canonical outcome benchmarks); Lightman et al.; Agent-as-a-Judge; AgentRewardBench; GSM-Symbolic; Dynabench; Recht et al.; Leaderboard Illusion; McCoy et al.; Ross et al.; Lapuschkin et al.; Strathern 1997; Skalse et al.; Gao et al.; Ethayarajh & Jurafsky; Burnell et al. (read it first).

**Open items for a next round**
- Read in full: CXBench App. D–H (grader details, false-pass annotated trace); Spurious Tool Use §4–§6; OpenClawBench taxonomy (the "weakly grounded commitments" class); SeekBench calibration metric.
- Read "Shortcut Sensitivity in Agent-Safety Evaluations" (Demirkiran & Ernstberger, arXiv:2610.22243; NeurIPS 2026 workshops TAE and AIWILD [verified arXiv; abstract only]). It uses paired cue edits with formatting placebos, which is a design control we could adopt for surface-form interventions.
- Confirm the τ-bench venue and Burnell et al.'s argument before citing.
