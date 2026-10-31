# Round 2: adversarial novelty sweep ("this has been done")

Date of sweep: 25 Oct 2026. Scope: 2024 to Oct 2026 work on earned, graduated, progressive or calibrated autonomy for LLM agents; autonomy levels assigned from evaluations; trust calibration from track record; agent certification and licensing; deployment gating from evaluations (safety cases, frontier safety frameworks); learned human-in-the-loop escalation policies; right-for-the-right-reasons and process-versus-outcome evaluation of agents; escalation and abstention benchmarks; and delegation in human–agent teams.

Verification convention:
- **[verified]**: title, authors and date checked against the arXiv API (export.arxiv.org), Crossref or the OpenReview API on 25 Oct 2026.
- **[unverified]**: anything I could not check that way.

Equations in the arXiv HTML were dropped by my HTML-to-text conversion. Where I describe a formula, I am working from the surrounding prose, and I say so.

---

## 0. Bottom line (read this first)

1. **Nothing found does all four of our core properties together.** The four properties are:
   - (a) autonomy assigned per decision class;
   - (b) autonomy earned from tested behaviour towards evidence;
   - (c) autonomy that can be revoked;
   - (d) evaluation on held-out data.

   The closest works cover three of the four, or cover all four only on paper:

   | Work | (a) per class | (b) earned from evidence tests | (c) revocable | (d) held-out | Gap |
   |---|---|---|---|---|---|
   | Digital Apprentice, 2606.04321 | yes (per skill) | no | yes (automatic demotion) | no | Promotion signal is the human correction rate, an outcome/approval signal; the promotion rule itself is never evaluated. |
   | Trust Before Autonomy, 2610.18789 | position only | position only | position only | position only | A position paper with a gated ladder and risk–coverage metrics, but nothing is run. |
   | Hedwig, 2605.11495 | per action area | no | yes | no | Earned from developer approvals; evaluated on 11 operations with an LLM judge. |
   | READY, ICLR 2027 submission (abstract only) | no | no | – | yes | Certifies accept-or-escalate oversight policies on held-out cases with finite-sample error control. The signals are outcomes and confidence, not evidence handling. |

   Section 4 states the check in full.

2. **Contribution (1), the "bridge to classic MAS delegation theory", is NOT novel as stated.** Tomašev, Franklin and Osindero (DeepMind), *Intelligent AI Delegation* (arXiv:2602.11865, Feb 2026), does three things we would otherwise claim:
   - It explicitly grounds LLM-agent delegation in Castelfranchi & Falcone (1998) and in Falcone & Castelfranchi (2002), "the theory of adjustable social autonomy".
   - It proposes "graduated authority" driven by trust and reputation, including process-level "behavioral metrics", plus "automated revocation" through "algorithmic circuit breakers".
   - The statement in positioning.md §1 that "nobody cites classic delegation theory" is true only of the six audit papers. It is false for the wider literature.
   - **Required change:** reframe contribution (1) as an *operational* bridge, meaning a mapping of delegation and adjustable-autonomy constructs onto measurable episode fields and a testable rule. We must not claim to be first to connect the two literatures.

3. **"Earned autonomy" as a slogan is crowded.** It appears in Digital Apprentice ("autonomy is earned, not assumed"), Trust Before Autonomy ("autonomy should be earned, not assumed"), Hedwig ("work for which the agent has earned trust"), Intelligent AI Delegation ("graduated authority") and practitioner material (AWS "graduated autonomy", Cloud Security Alliance, Anthropic's *Measuring AI agent autonomy in practice*).
   - Earned Authority (2607.23586) directly attacks "earned-autonomy ladders" in which performance evidence raises the authority ceiling.
   - **Our defensible novelty is the evidence base for earning:** interventional tests of how the agent handles external evidence, as opposed to outcomes, approvals or correction rates. Added to that are a held-out empirical comparison and the escalation-cost model.

4. **The risk–coverage-with-escalation-cost evaluation is partially preempted in method.** Three works overlap:
   - READY (held-out certification, autonomous coverage against human-review burden and cost);
   - *Oversight Has a Capacity* (2606.08919), which treats the guard as selective classification under asymmetric cost with a fatiguing reviewer;
   - Trust Before Autonomy, which prescribes selective risk–coverage for abstention.

   **Our claim must be the comparison itself:** an evidence-test-based rule against an outcome-only rule (and an approval-history rule), per decision class, on held-out generated episodes. We should not claim the metric.

5. **Contribution (2), interventions on external evidence that are robust to redundancy, survives.**
   - The nearest neighbour is AgentAbstain (2607.10059). It builds paired should-act and should-abstain tasks "through a controlled perturbation to the instruction, tool, or environment state". That is close to our "remove X" intervention. I read the abstract only.
   - Nobody found does only-X, invert-X or an independent second source, and nobody uses intervention results to allocate autonomy.

---

## 1. Queries run (≥25 required; 135 run)

### 1a. arXiv API (export.arxiv.org, relevance-sorted, filtered to 2024 or later): 105 queries

1. `all:"earned autonomy" AND all:agent`
2. `abs:"graduated autonomy" AND abs:agent`
3. `abs:"progressive autonomy" AND abs:agents`
4. `abs:"calibrated autonomy" AND abs:agent`
5. `abs:"levels of autonomy" AND abs:"LLM agents"`
6. `abs:"autonomy levels" AND abs:"AI agents"`
7. `abs:"adjustable autonomy" AND abs:LLM`
8. `abs:"trust calibration" AND abs:"LLM agent"`
9. `abs:"track record" AND abs:agent AND abs:autonomy`
10. `abs:"agent certification" AND abs:AI`
11. `abs:"licensing" AND abs:"AI agents" AND abs:evaluation`
12. `abs:"safety case" AND abs:agent`
13. `abs:"frontier safety framework" AND abs:evaluation`
14. `abs:"deployment decision" AND abs:"capability evaluation"`
15. `abs:"dynamic autonomy" AND abs:agent`
16. `abs:autonomy AND abs:"per-action" AND abs:"LLM agents"`
17. `abs:"when to ask for help" AND abs:agent`
18. `abs:abstention AND abs:"LLM agents" AND abs:benchmark`
19. `abs:escalation AND abs:"LLM agent" AND abs:human`
20. `abs:"ask for clarification" AND abs:"agents" AND abs:benchmark`
21. `abs:"defer to human" AND abs:"LLM"`
22. `abs:"learning to defer" AND abs:"LLM agent"`
23. `abs:"selective prediction" AND abs:agent AND abs:LLM`
24. `abs:"risk-coverage" AND abs:agent`
25. `abs:"process-based" AND abs:"outcome-based" AND abs:agent`
26. `abs:"right for the right reasons" AND abs:LLM`
27. `abs:"process reward" AND abs:"agent" AND abs:evaluation AND abs:trajectory`
28. `abs:delegation AND abs:"human-agent" AND abs:LLM`
29. `abs:"intelligent delegation"`
30. `abs:"bounded autonomy" AND abs:agent`
31. `ti:"levels of autonomy" AND ti:agents`
32. `abs:"autonomy certificate"`
33. `ti:delegation AND abs:"AI agents" AND abs:trust`
34. `abs:"permission" AND abs:"earned" AND abs:agent`
35. `abs:"privilege" AND abs:"least privilege" AND abs:"LLM agents" AND abs:learned`
36. `abs:"trust score" AND abs:"AI agents" AND abs:history`
37. `abs:reputation AND abs:"LLM agents" AND abs:autonomy`
38. `abs:"evidence-based" AND abs:autonomy AND abs:agents AND abs:revocable`
39. `abs:revocation AND abs:autonomy AND abs:agent`
40. `abs:"human oversight" AND abs:"when to escalate" AND abs:agent`
41. `abs:"conformal" AND abs:"ask for help" AND abs:agent`
42. `abs:"conformal" AND abs:"LLM agents" AND abs:"human intervention"`
43. `abs:"approval" AND abs:"auto-approve" AND abs:agent`
44. `abs:"human-in-the-loop" AND abs:"learned policy" AND abs:"LLM agent" AND abs:intervention`
45. `abs:"evaluation" AND abs:"deployment gating"`
46. `abs:"pre-deployment" AND abs:"agent" AND abs:certification`
47. `abs:"conditional autonomy" AND abs:agents AND abs:LLM`
48. `abs:"graded autonomy"`
49. `abs:"autonomy" AND abs:"earned" AND abs:"trust"`
50. `abs:"incremental trust" AND abs:agent`
51. `abs:"probation" AND abs:agent AND abs:LLM`
52. `abs:"trust" AND abs:"autonomy" AND abs:"decision class"`
53. `abs:"risk tier" AND abs:"AI agents" AND abs:autonomy AND abs:evaluation`
54. `abs:"counterfactual" AND abs:"evidence" AND abs:"agent" AND abs:"decision" AND abs:faithfulness`
55. `abs:"evidence sensitivity" AND abs:LLM`
56. `abs:"knowledge conflict" AND abs:"agent" AND abs:"tool"`
57. `abs:"oversight" AND abs:"autonomy" AND abs:"calibrat" AND abs:"agents"`
58. `abs:"selective autonomy"`
59. `abs:"autonomy allocation" OR abs:"allocation of autonomy"`
60. `abs:"human-AI delegation" AND abs:"learned"`
61. `abs:"mixed-initiative" AND abs:"LLM agent"`
62. `abs:"trust" AND abs:"capability" AND abs:"permission" AND abs:"separate" AND abs:agents`
63. `abs:"conformal" AND abs:"agent" AND abs:"escalat"`
64. `abs:"risk control" AND abs:"LLM agents" AND abs:"human"`
65. `abs:"Calibrate-Then-Act"`
66. `abs:"trust" AND abs:"delegation" AND abs:"Castelfranchi"`
67. `abs:"autonomy" AND abs:"revocable"`
68. `abs:"authority" AND abs:"evidence" AND abs:"agent" AND abs:"expand" AND abs:"contract"`
69. `abs:"responsible scaling" AND abs:"capability thresholds"`
70. `abs:"if-then commitments"`
71. `abs:"agent" AND abs:"permission" AND abs:"learned from" AND abs:"traces"`
72. `abs:"outcome-only" AND abs:"agent" AND abs:"evaluation" AND abs:"process"`
73. `abs:"lucky guess" AND abs:agent`
74. `abs:"faithful" AND abs:"tool output" AND abs:"agent" AND abs:"counterfactual"`
75. `abs:"context sensitivity" AND abs:"retrieved evidence" AND abs:"ignore"`
76. `abs:"trust" AND abs:"LLM agent" AND abs:"Bayesian" AND abs:"track record"`
77. `abs:"human-agent teaming" AND abs:"adjustable"`
78. `abs:"autonomy" AND abs:"coding agents" AND abs:"permission" AND abs:"trust"`
79. `abs:"autonomy ladder"`
80. `abs:"autonomy tiers"`
81. `abs:"autonomy" AND abs:"demonstrated reliability"`
82. `abs:"earned, not assumed"`
83. `abs:"authority" AND abs:"agent" AND abs:"evidence" AND abs:"escalat" AND abs:"holdout"`
84. `abs:"permission" AND abs:"agent" AND abs:"downgrade" AND abs:"trust"`
85. `abs:"autonomy" AND abs:"agent" AND abs:"risk-coverage"`
86. `abs:"autonomy" AND abs:"certificate" AND abs:"agent"`
87. `abs:"delegation" AND abs:"LLM" AND abs:"adjustable autonomy"`
88. `abs:"escalation policy" AND abs:"agent"`
89. `abs:"human review" AND abs:"budget" AND abs:"agent" AND abs:"deferral"`
90. `abs:"trust" AND abs:"agent" AND abs:"Beta reputation"`
91. `abs:"evidence" AND abs:"perturbation" AND abs:"agent" AND abs:"decision" AND abs:"tool outputs"`
92. `abs:"redundant evidence" AND abs:LLM`
93. `abs:"trust" AND abs:"agents" AND abs:"process" AND abs:"outcome" AND abs:"autonomy" AND abs:"grant"`
94. `abs:"deployment overhang"`
95. `ti:"trust calibration" AND abs:agent`
96. `abs:"human-AI teams" AND abs:"delegation" AND abs:"LLM" AND abs:"reliance"`
97. `abs:"progressive autonomy"`
98. `abs:"autonomy" AND abs:"preference learning" AND abs:"tool use" AND abs:"approval"`
99. `abs:"permission prompts" AND abs:agent`
100. `abs:"finite-sample" AND abs:"agent" AND abs:"escalat"`
101. `abs:"human review" AND abs:"coverage" AND abs:"agent" AND abs:"held-out" AND abs:"certif"`
102. `abs:"frontier AI safety frameworks"`
103. `abs:"capability thresholds" AND abs:"safeguards" AND abs:"deployment"`
104. `abs:"autonomy" AND abs:"agent" AND abs:"shadow mode"`
105. `abs:"trust" AND abs:"agent" AND abs:"promotion" AND abs:"demotion"`

Plus abstract-level checks for `abs:"CliniCARE-Bench"`, `abs:"accept-or-escalate"`, `abs:"deployment qualification" AND abs:agent` and `abs:"certified operating point"`. I ran these to find READY on arXiv. It is not there.

### 1b. Web search (Google-like): 9 queries

1. "earned autonomy" AI agents trust track record permissions paper 2026
2. measuring AI agent autonomy in practice auto-approve users grant more autonomy over time Claude Code study
3. openreview 2026 "autonomy" LLM agents "trust calibration" earned permissions evaluation held-out
4. arXiv 2026 agent "graduated autonomy" OR "progressive autonomy" trust earned from evaluation promotion demotion LLM agents framework
5. "trust" "autonomy" LLM agent per-task "track record" adaptive permission granting empirical evaluation arxiv
6. AAMAS 2026 adjustable autonomy LLM agents trust delegation paper
7. NeurIPS 2025 OR ICLR 2026 benchmark LLM agents "when to ask" human intervention escalation cost interactive ambiguity software engineering agents
8. conformal prediction LLM agent "ask for help" OR "defer" actions risk guarantee 2025 2026 arxiv tool-use agents human oversight budget
9. FAccT 2026 OR AIES 2025 AI agents autonomy delegation accountability "levels of autonomy" governance evaluation paper

### 1c. OpenReview API search (`api2.openreview.net/notes/search`, source=forum): 21 queries

"earned autonomy"; "adjustable autonomy"; "autonomy levels agents"; "when to ask for help agents"; "delegation LLM agents trust"; "graduated autonomy agents"; "agent escalation human oversight policy"; "trust calibration agent autonomy"; "autonomy certification agents evaluation"; "right for the right reasons agents"; "proofs of autonomy"; plus title look-ups for READY, LEASH, *Right for Wrong Reasons* and *Proofs of Autonomy*.

The OpenReview `notes?id=` endpoint returned a browser challenge (HTTP 403), so I could not open full PDFs of anonymous ICLR 2027 submissions.

Semantic Scholar's API returned HTTP 429 (rate limited) and was not used. AAMAS 2026, FAccT 2026 and AIES accepted-paper lists were not directly searchable through my tools. Web search did not surface a matching AAMAS 2026, FAccT 2026 or AIES 2025 paper. **This is a coverage gap:** someone should browse the AAMAS 2026 (Paphos) proceedings for "adjustable autonomy" and "delegation" by hand.

---

## 2. Ranked table of closest works

Threat targets:
- **C1** = MAS bridge;
- **C2** = decision episode plus redundancy-robust evidence interventions;
- **C3** = per-class delegation rule evaluated on held-out episodes with risk–coverage and escalation cost;
- **Thesis** = "autonomy per decision class, earned from tested behaviour towards evidence, revocable".

| # | Title | Authors | Year | Venue / id | Bib | What it does (one line) | Threatens | Threat | Justification |
|---|---|---|---|---|---|---|---|---|---|
| 1 | The Digital Apprentice: A Framework for Human-Directed Agentic AI Development | Travis Weber, Rohit Taneja | 2026 | arXiv:2606.04321 (submitted to ACM AI Leadership Summit 2026, visionary track) | [verified] | Per-skill autonomy state machine (Pre-L0, L0, L1, L2). Promotion requires correction-rate improvement, a low residual correction rate, a quality-scorer gate and explicit human authorization. Demotion is automatic. | Thesis, C3 | **High** | The closest conceptual match: per-skill, earned, revocable, with explicit transition conditions. Weaker than us in three ways: the evidence is the correction rate (outcome/approval), there are no evidence-handling tests, and the promotion rule is never evaluated. |
| 2 | Intelligent AI Delegation | Nenad Tomašev, Matija Franklin, Simon Osindero | 2026 | arXiv:2602.11865 | [verified] | Conceptual framework for delegation (AI or human). Grounded in Castelfranchi & Falcone 1998 and Falcone & Castelfranchi 2002 (adjustable social autonomy). Reputation and trust drive "graduated authority"; process-level monitoring; revocation through circuit breakers. | **C1**, Thesis | **High** | Preempts "first bridge to MAS delegation theory" and the "graduated, revocable authority" concept. No method, no evaluation. |
| 3 | Qualifying AI Agents Under Cost-Aware Human Oversight (framework "READY") | anonymous | 2026 | ICLR 2027 Conference Submission, OpenReview forum 3AR0RdXhpV | [verified: OpenReview record; authors anonymous] | Certifies accept-or-escalate oversight policies on held-out cases with finite-sample error control. Returns the lowest-cost certified policy, with a profile of autonomous coverage, human-review burden and cost. Data: CliniCARE-Bench (18 systems, 750 cases) and τ²-bench retail (17 systems, 114 tasks). | **C3** (evaluation methodology) | **High** | Held-out, coverage-versus-oversight-cost evaluation of escalation policies is exactly our evaluation frame. The difference is the signal: outcome success and self-reported confidence, per agent–workflow configuration, with no evidence handling and no decision classes. **Abstract only.** |
| 4 | Trust Before Autonomy: Rethinking Agentic Remote Sensing for Crisis Response | Georgios Angelidis, Aggelos Psiris, Spyridon Evangelatos, Thomas Lagkas, Panagiotis Sarigiannidis, Iraklis Varlamis, Georgios Th. Papadopoulos | 2026 | arXiv:2610.18789 | [verified] | Position paper: "autonomy should be earned, not assumed". Meta-analysis of 12 EO benchmarks. Per-task autonomy ladder; readiness gates R1–R5 (benchmark, replay, shadow, supervised, conditional); "demoted on failure"; risk–coverage for abstention; "evidence validity". | Thesis, C3 | **Medium-High** | Covers all four properties as prescription, including held-out events and risk–coverage, but runs nothing. Grants autonomy "by rung, not by leaderboard". |
| 5 | Hedwig: Dynamic Autonomy for Coding Agents Under Local Oversight | Tanjal Shukla, K. J. Kevin Feng, Leijie Wang, Mohammad Rostami, Amy X. Zhang | 2026 | Proc. ACM Conf. on AI and Agentic Systems (CAIS ’26), demo; doi:10.1145/3786335.3813223; arXiv:2605.11495 | [verified] | An online logistic-regression policy over 13 action features, trained on developer approvals and denials, sets per-action check-in thresholds. Trust can be revoked per topic. | Thesis, C3 | **Medium-High** | "Earned trust", revocable and fine-grained, which reviewers will raise. But the evidence is human approval history, and the evaluation is 11 operations, a single run and an LLM-judge oracle. |
| 6 | Trust Is Not a Score: Runtime Assurance Contracts for High-Risk AI Agents | Serhii Zabolotnii | 2026 | arXiv:2609.39717 (v2) | [verified] | Policy schema mapping observed evidence to authority transitions (retry, switch, escalate, defer, act, stop), with non-compensatory gates. Compared with a score-only rule and a protocol-only rule on 174 plus 124 synthetic coding cases, 18 traces and a 24-episode LLM-labelled holdout. | C3 (outcome/score baseline), Thesis | **Medium** | Same framing of an "assurance-transition gap" ("how observed evidence should change an agent's authority"), with a paired baseline comparison and a holdout. But the gates are within one task, per action. Authority is not earned across episodes, and the agent's evidence handling is not tested. |
| 7 | Are You Still the Agent I Authorized? Earned Authority under a Fixed Ceiling for Evolving Agents | Zhaoxi Zhang, Xiaomei Zhang | 2026 | arXiv:2607.23586 | [verified] | Formal model: an immutable effect ceiling plus a transition envelope. Authority contracts freely and expands only under evidence conditions. Argues that agent-produced performance evidence must never raise the ceiling. | Thesis (critique), C3 | **Medium** | Directly critiques "earned-autonomy ladders". We must answer this critique. No evaluation. |
| 8 | Agent Reliability Profiles in Financial Services | Mike Hsu, Medha Bankhwal, Béatrice Moissinac, Kevin Werbach, Lukasz Szpruch, Bennett Hillenbrand | 2026 | arXiv:2610.04123 (MLCommons working draft) | [verified] | Per-deployment "bounded claim" over autonomy tier T0–T4, operational design domain (ODD), 12 action classes and a control envelope. Three assurance levels (asserted, validated by tests, independently verified); floors; invalidation list. The tier is "defined by evidence" from approval logs. | Thesis, C3 | **Medium** | Test-validated autonomy tiers with action classes and invalidation, strong institutional backing. But the unit is the deployment, not the decision class; there are no evidence-handling tests and no data. |
| 9 | Levels of Autonomy for AI Agents | K. J. Kevin Feng, David W. McDonald, Amy X. Zhang | 2025 | arXiv:2506.12469; Knight First Amendment Institute essay series | [verified] | Five user-role levels; "autonomy certificates" issued by a third party after "private evaluations" against an "autonomy case"; "assisted evaluation". | Thesis (certification from tests) | **Medium** | Origin of "certify autonomy from evaluation" for LLM agents. Per agent and configuration, not per decision class; evaluates the amount of autonomy, not its warrant. |
| 10 | Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human | Emre Turan | 2026 | arXiv:2606.08919 | [verified] | Treats the action-gating guard as selective classification under asymmetric cost. Reviewer fatigue makes realized safety an inverted U over the escalation rate. 125 hand-labelled actions. | C3 (escalation cost, curve) | **Medium** | Preempts "explicit escalation cost plus curve" for agent gating. Endogenous reviewer cost is richer than ours. The unit is the action, not the agent's earned autonomy. **Abstract only.** |
| 11 | AgentAbstain: Do LLM Agents Know When Not to Act? | Xun Liu, Yi Evie Zhang, Vira Kasprova, Parisa Rabbani, Pardis Sadat Zahraei, Tianyu Zhang, Ali Ebrahimpour-Boroojeny, Varun Chandrasekaran | 2026 | arXiv:2607.10059 | [verified] | 263 paired should-act and should-abstain tasks built by "controlled perturbation to the instruction, tool, or environment state"; 17 LLMs; abstention is independent of task-solving ability. | C2 (paired perturbations), C3 | **Medium** | Its paired controlled perturbation is the closest analogue to our "remove X" intervention, and it shows outcome capability does not predict abstention. But it is a benchmark of agent self-abstention, with no autonomy allocation and no redundancy controls. **Abstract only.** |
| 12 | HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help? | Tu Trinh, Mohamed Elfeki, Guangze Luo, Kelvin Luu, Nathan Hunt, Ernesto Hernandez, Nandan Marwaha, Yannis Yiming He, Charles Wang, Fernando Carabedo, Alessa Castillo, Bing Liu | 2026 | arXiv:2604.09408 (v4); ICLR 2027 submission per OpenReview | [verified] | Hidden blockers; Ask-F1 metric; "an agent that makes a lucky guess ... will score identically to one that would have asked". | C3 (outcome-only critique) | **Low-Medium** | Same argument against outcome-only scoring, aimed at agent self-escalation, not a principal's delegation rule. **Abstract only.** |
| 13 | Progressive Autonomy as Preference Learning: A Formalization of Trust Calibration for Agentic Tool Use | Changkun Ou | 2026 | arXiv:2605.19151 | [verified] | A Gaussian-process posterior over human risk tolerance from approve/deny feedback partitions the action space into allow, block and ask regions; escalates where approval is most uncertain. | Thesis, C3 | **Low-Medium** | "Progressive autonomy" learned from human approvals, i.e. modelling human preference, not agent behaviour towards evidence. **Abstract only.** |
| 14 | Agents' Last Doubt: Knowing When to Act and When to Step Back in Tool-Using Agents | Qisai Liu, Qingyue Jiao, Bangwei Guo, Wenxi Dai, Changyi Yang, Jiahe Liu, Dimitris N. Metaxas, Yiyu Shi, Zhanhong Jiang, Minghao Guo | 2026 | arXiv:2610.24194 | [verified] | Counterfactual dataset (3,115 action outcomes at 1,036 decision points in ToolSandbox) covering act, gather information and escalate; trains the SURE-Act controller. | C3 | **Low-Medium** | Counterfactual decision points with an escalation option and explicit costs, but it is a per-step controller trained on outcomes. **Abstract only.** |
| 15 | Separating Capability from Permission: A Governance Framework for Agentic AI Autonomy Levels | Haining Zheng, Qian Dong, Rodolfo K. Depena, Jonathan D. Bhatia, Feng Xiao, Peng Xu | 2026 | arXiv:2607.23438 | [verified] | Allowed Autonomy Levels (AAL) against Autonomous Capability Levels (ACL); a risk-aware process for assigning allowed autonomy; one enterprise case. | Thesis | **Low-Medium** | Shares "permission ≠ capability", but allowed autonomy is set by risk assessment, not earned from tests. **Abstract only.** |
| 16 | Toward Pre-Deployment Assurance for Enterprise AI Agents: Ontology-Grounded Simulation and Trust Certification | Thanh Luong Tuan, Abhijit Sanyal | 2026 | arXiv:2606.04037 (v2) | [verified] | Agent Operational Envelope (permissions, autonomy levels); scenarios generated from an ontology; machine-verifiable "Trust Certificate with graduated deployment verdicts". | Thesis (certification from tests) | **Low-Medium** | Deployment gate from test evidence, but its evaluation measures scenario-generation coverage, not a delegation rule. **Abstract only.** |
| 17 | Evaluating Bounded Autonomy in Regulated Agentic AI: A Diagnostic Harness with Constitutional Rewards, Escalation Labels, and Runtime Governance (RegLLM) | Dipankar Sarkar | 2026 | arXiv:2609.37501 | [verified] | "should-escalate" labels make act-versus-defer measurable; escalation recall; a runtime supervisor forces escalation; n=8–12 smoke tests. | C3 | **Low** | Tiny; agent-level escalation labels. **Abstract only.** |
| 18 | A Unified Framework for Human AI Collaboration in Security Operations Centers with Trusted Autonomy | Ahmad Mohsin, Helge Janicke, Ahmed Ibrahim, Iqbal H. Sarker, Seyit Camtepe | 2025/2026 | arXiv:2505.23397; ACM Trans. Internet Technology (Jul 2026, per arXiv journal ref) | [verified arXiv; TOIT ref unverified] | Five-tier autonomy mapped to human-in-the-loop roles and "task-specific trust thresholds" across SOC functions. | Thesis (per-task tiers) | **Low** | Per-task tiers, but thresholds are set by design, not earned from tests. **Abstract only.** |
| 19 | AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation | Priyam Sahoo, Gaurav Mittal, Xiaomin Li, Shengjie Ma, Benjamin Steenhoek, Pingping Lin, Yu Hu | 2026 | arXiv:2605.12925 | [verified] | 10.7% of passing SWE-agent trajectories are "Lucky Passes"; model rankings change under a process-quality score. | Motivation for C3 (process vs outcome) | **Low** | Supports our premise; no delegation. **Abstract only.** |
| 20 | Towards a Science of AI Agent Reliability | Stephan Rabanser, Sayash Kapoor, Peter Kirgis, Kangheng Liu, Saiteja Utpala, Arvind Narayanan | 2026 | arXiv:2602.16666; ICML 2026 (per arXiv comment) | [verified] | Twelve reliability metrics (consistency, robustness, predictability, safety) beyond accuracy; 15 models. | Motivation | **Low** | Beyond-accuracy profile, but no autonomy allocation. **Abstract only.** |
| 21 | Safety Cases: How to Justify the Safety of Advanced AI Systems | Joshua Clymer, Nick Gabrieli, David Krueger, Thomas Larsen | 2024 | arXiv:2403.10462 | [verified] | Structured arguments (inability, control, trustworthiness, deference) to justify deployment. | Thesis (deployment gating from evidence) | **Low** | System-level, catastrophic-risk deployment decisions; no per-class operational autonomy. **Abstract only.** |
| 22 | Measuring AI agent autonomy in practice (Anthropic research post) | Miles McCain, Thomas Millar, Saffron Huang, Jake Eaton, Kunal Handa, Michael Stern, Alex Tamkin, Matt Kearney, Esin Durmus, Judy Shen, Jerry Hong, Brian Calvert, Jun Shern Chan, Francesco Mosconi, David Saunders, Tyler Neylon, Gabriel Nicholas, Sarah Pollack, Jack Clark, Deep Ganguli | 2026 | anthropic.com/research/measuring-agent-autonomy (18 Feb 2026), not peer-reviewed | [verified web page] | Field data: users' full auto-approve rises from about 20% (fewer than 50 sessions) to over 40% (750 sessions); Claude stops itself more often than humans interrupt; "deployment overhang". | Motivation (earned autonomy by users in practice) | **Low** | Descriptive evidence that humans already grant autonomy from experience, i.e. outcome familiarity. Useful motivation. |
| 23 | LOGOS: A Living Logic for AI Agent Teams That Evolve With Humans | Yuma Ichikawa, Yamato Arai, Kosaku Kimura, Akira Sakai, Hiromichi Kobashi | 2026 | arXiv:2607.10878 | [verified] | Learned prompts, skills and tools remain "untrusted release candidate[s] until held-out execution evidence, human-controlled policy, and explicit authorization permit its promotion". | Thesis (promotion on held-out evidence) | **Low** | Promotion of agent artifacts, not decision authority. **Abstract only.** |
| 24 | Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents | Wenxuan Ding, Nicholas Tomlin, Greg Durrett | 2026 | arXiv:2602.16699 | [verified] | Gives the agent priors to reason about cost-uncertainty trade-offs (explore or commit). | C3 (costs) | **Low** | The agent's own policy, not delegation. **Abstract only.** |
| 25 | Task-Aware Delegation Cues for LLM Agents | Xingrui Gu | 2026 | arXiv:2603.11011; CHI ’26 workshop | [verified] | Task-conditioned capability profiles (from Chatbot Arena win rates) drive delegation routing. | Thesis (per-task trust) | **Low** | Per-task reliability cues from preference data, not tests of evidence handling. **Abstract only.** |

Also seen; low threat, but worth citing or knowing:
- Kasirzadeh & Gabriel, *Characterizing AI Agents for Alignment and Governance*, arXiv:2504.21848 [verified].
- Mitchell, Ghosh, Luccioni & Pistilli, *Fully Autonomous AI Agents Should Not be Developed*, arXiv:2502.02649 [verified].
- Cihon, Stein, Bansal, Manning & Xu, *Measuring AI agent autonomy: Towards a scalable approach with code inspection*, arXiv:2502.15212 [verified]; NeurIPS 2024 SoLaR workshop.
- Vijayvargiya, Zhou, Yerukola, Sap & Neubig, *Ambig-SWE*, arXiv:2502.13069 [verified]; ICLR 2026 per arXiv comment.
- Wang et al., *Learning to Ask: When LLM Agents Meet Unclear Instruction*, arXiv:2409.00557 [verified]; EMNLP 2025.
- Kim et al., *Tiered Agentic Oversight*, arXiv:2506.12482 [verified].
- Yan et al., *Do Coding Agents Understand Least-Privilege Authorization?* (AuthBench), arXiv:2605.14859 [verified].
- Parisel, *A Theory of Least Autonomy in AI*, arXiv:2607.09744 [verified].
- Shi et al., *SoK: Trust-Authorization Mismatch in LLM Agent Interactions*, arXiv:2512.06914 [verified].
- Noyan, *Empirical Evaluation of Task-Based Permission Scoping Architecture for AI Agents*, arXiv:2609.15422 [verified].
- Advani, *When Small Models Are Right for Wrong Reasons: Process Verification for Trustworthy Agents*, AAAI 2026 TrustAgent workshop poster [verified: OpenReview nH5O0AI61S].
- LEASH, *Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer Use*, ICLR 2027 submission [verified: OpenReview kDGgGKWYBi; authors anonymous].
- Grigor, Schroeder de Witt & Martinovic, *Proofs of Autonomy*, ICML 2025 TAIG workshop [verified: OpenReview qxFgQHN69d].
- Satta Chiris & Mishra, *AURA: An Agent Autonomy Risk Assessment Framework*, arXiv:2510.15739 [verified].
- Sun, *Safe Bilevel Delegation*, arXiv:2604.27358 [verified; framework only, empirical results "planned"].
- Zabolotnii, *TRACE: A Metrologically-Grounded Engineering Framework…*, arXiv:2605.03838 [verified]. **Name collision** with Chang & Chang TRACE, arXiv:2607.12480.

---

## 3. Full notes on the top threats

### 3.1 The Digital Apprentice (Weber & Taneja, 2026)

**Bibliographic data.**
- Travis Weber, Rohit Taneja (Pheo Inc).
- *The Digital Apprentice: A Framework for Human-Directed Agentic AI Development*, with the in-paper subtitle "Earned Autonomy Through Observational Learning and Inference-Time Decision Memory".
- arXiv:2606.04321v1 (3 Jun 2026), cs.AI. Comment: "Submitted to ACM AI Leadership Summit 2026, Visionary Papers Track. 5 pages". [verified]
- **Read:** full HTML text (§§1–7, all tables, references). Equations (1)–(5) were not rendered in my extraction; their content is described in prose.

**Problem and contribution.**
- The problem is responsible delegation for professional AI agents.
- §1: "Taxonomies describe what autonomy looks like; our contribution is the machinery for moving between levels: what evidence justifies an increase in autonomy, who must authorize it, and how the system detects when autonomy should be withdrawn."
- Implemented as the ADAPT inference-time control plane.

**Method.**
- §2.1: autonomy is "a per-skill property ... represented as a finite state machine". The states are:
  - Pre-L0, observe only;
  - L0, sandbox (100% human review);
  - L1, draft (human endorses before effect);
  - L2, autonomous (intervention on exceptions).
- "The agent cannot promote itself. Promotion ... requires both empirical evidence of competence on that skill and a recorded human authorization. Demotion is asymmetric: the system rolls a skill back automatically when quality degrades."
- §2.2 graduation conditions, all computed over non-overlapping windows of outputs:
  - C1: the correction rate falls compared with an earlier window;
  - C2: the correction rate is low;
  - Q1: a share of outputs clears a validated quality-scorer threshold;
  - plus a human authorization event.
- Demotion triggers on a high correction rate or out-of-distribution uncertainty.
- It explicitly flags complacency: "a low correction rate can indicate either genuine competence or a reviewer who has stopped checking carefully". The proposed remedy is to monitor reviewer engagement and use "periodic seeded checks" (§6).
- The rest is preference-pair capture plus a multi-policy "radar" quality rubric with six dimensions, one of which is "Grounding".

**Evaluation.**
- A proof-of-concept on "an openly available professional-methodology corpus", n of about 30–60 prompts per arm (exact n not rendered). Qwen generator; Gemma as LLM judge.
- Reported means of judge rubric scores: 0.717 (RAG), 0.780 (best-of-n), 0.803 (fusion), 0.957 (after onboarding); under drift, 0.930 recovering to 0.957.
- No confidence intervals, inter-rater agreement or significance tests (their own admission in §5).
- **The graduation rule itself is never evaluated.** There is no risk–coverage analysis, no baseline rule and no held-out promotion test.

**What it covers that WorkTrace must NOT claim.**
- Per-skill (per-class) graduated autonomy as a finite state machine with explicit promotion and demotion conditions.
- Asymmetric demotion.
- Human authorization as a necessary condition for promotion.
- The automation-complacency caveat for approval-based promotion.

**What it leaves open that WorkTrace addresses.**
- The promotion signal is the human correction rate plus an LLM-judge quality score: outcome or approval evidence, contaminated by reviewer complacency (they say so).
- There are no tests of whether the agent's action responds correctly to the evidence available.
- There is no held-out evaluation of the rule, no escalation-cost model and no comparison with an outcome-only rule.
- Its rule is in fact an instance of the outcome/approval baseline we compare against.

**Draft differentiation sentence.** "The Digital Apprentice specifies per-skill autonomy tiers promoted on falling human-correction rates and judge scores with human sign-off; WorkTrace replaces that outcome/approval signal with interventional tests of the agent's behaviour towards external evidence, and evaluates the resulting per-class delegation rule on held-out episodes against exactly such an outcome-based rule."

**Citation cautions.** Five-page visionary submission from a company (Pheo Inc); not peer-reviewed; one corpus; judge-measured telemetry only. Cite for the concept and transition machinery, not for empirical claims.

### 3.2 Intelligent AI Delegation (Tomašev, Franklin & Osindero, 2026)

**Bibliographic data.**
- Nenad Tomašev, Matija Franklin, Simon Osindero.
- *Intelligent AI Delegation*. arXiv:2602.11865v1 (12 Feb 2026). [verified] Google DeepMind affiliation per the paper; I did not open the title page in detail.
- **Read:** §1, §2 (all), §3, §4 introduction and Table 1, §4.5 Monitoring, §4.6 Trust and Reputation, §4.7 Permission Handling, §4.8 Verifiable Task Completion, §5.1, §6, §7.
- **Not read:** §4.1–4.4, §4.9, §5.2–5.6, reference list (beyond grep).

**Problem and contribution.**
- An "adaptive framework for intelligent AI delegation". Delegation is defined as "a sequence of decisions involving task allocation, that also incorporates transfer of authority, responsibility, accountability ... and mechanisms for establishing trust" (§2.1).
- Five pillars: dynamic assessment, adaptive execution, structural transparency, scalable market and systemic resilience (Table 1).

**Method.** Conceptual only.
- §1 opens with "Delegation (Castelfranchi and Falcone, 1998)…".
- §3 cites Falcone & Castelfranchi (2002) for degrees of autonomy (their reference title: "The human in the loop of a delegated agent: the theory of adjustable social autonomy").
- §2.2 gives task axes, including criticality, uncertainty, verifiability and reversibility.
- §2.3 covers trust calibration, authority gradient and zone of indifference.
- §4.5 sets outcome-level against process-level monitoring.
- §4.6: reputation from an "immutable ledger", a "web of trust" or "behavioral metrics", where the last "evaluates how a task is performed rather than just the result". Quote: "trust informs the dynamic scoping of authority and autonomy. This mechanism of graduated authority results in low-trust agents facing strict constraints ... while high-reputation agents operate with minimal intervention."
- §4.7: "Access rights are not static endowments but dynamic states that persist only as long as the agent maintains the requisite trust metrics ... algorithmic circuit breakers". Also: standing permissions for low-stakes tasks when "a reputation score exceed[s] a trusted threshold".

**Evaluation.** None.

**What it covers that WorkTrace must NOT claim.**
- Connecting Castelfranchi–Falcone delegation and adjustable autonomy to LLM-agent ecosystems.
- Graduated, reputation-driven, revocable authority.
- Process-versus-outcome monitoring as a basis for trust.
- Task criticality, reversibility and verifiability as delegation axes.

**What it leaves open that WorkTrace addresses.**
- No operational unit of evidence: reputation is left as ledger entries, credentials or vague "transparency scores".
- No test design: nothing like interventions on evidence, and nothing on redundancy.
- No decision-class definition, no delegation rule with thresholds and no evaluation of any kind. It names the gaming risk ("only accepting simple, low-risk tasks") but does not solve it.

**Draft differentiation sentence.** "Tomašev et al. (2026) argue, building on Castelfranchi and Falcone, that authority over AI delegatees should be graduated and revoked according to trust and process-level evidence; WorkTrace operationalises that programme by defining the evidential unit (the decision episode), the test (redundancy-robust interventions on external evidence) and the rule (proceed/escalate/refuse per decision class), and evaluates it empirically."

**Citation cautions.** A preprint without empirical content, but high-profile; reviewers will know it. Cite prominently in the introduction and in the related-work treatment of C1.

### 3.3 READY: *Qualifying AI Agents Under Cost-Aware Human Oversight* (anonymous, ICLR 2027 submission)

**Bibliographic data.** Anonymous. ICLR 2027 Conference Submission, OpenReview forum id 3AR0RdXhpV, created 16 Sep 2026. [verified: OpenReview record via the search API] **Read: abstract only.** The PDF sits behind an OpenReview challenge (HTTP 403) and is not on arXiv; a title search for distinctive phrases found nothing. This note must be completed once the PDF is accessible.

**Problem and contribution (from the abstract).**
- "Deployment requires determining under what operating conditions a system can meet a specified reliability requirement at acceptable cost."
- READY "turns workflow-level evaluation evidence into a statistically supported deployment qualification. Given a prespecified class of oversight policies, it evaluates their reliability and operating cost, tests them on held-out cases with finite-sample error control, and returns the lowest-cost member of the certified set."
- Output: a "deployment profile [of] reliability, autonomous coverage, human-oversight burden, and cost".

**Method.**
- Setting: terminal accept-or-escalate; the escalation signal appears to be self-reported confidence ranking.
- The unit is the agent–workflow–oversight configuration.

**Evaluation.**
- CliniCARE-Bench clinical audit (18 systems, 750 cases) and τ²-bench retail (17 systems, 114 tasks).
- Autonomous accuracy does not correlate with confidence ranking quality (r = −0.07 and −0.13).
- Sonnet 5 and GPT-5.4 differ by 0.3 accuracy points, yet need 12.0% against 29.3% human review at the same target.

**What it covers that WorkTrace must NOT claim.**
- Held-out certification of escalation policies with finite-sample guarantees.
- Coverage-versus-human-review-cost trade-offs.
- The point that "deployability is not an intrinsic property of an agent or its benchmark score".

**What it leaves open that WorkTrace addresses.**
- No decision classes.
- The signal is confidence and outcomes, not the agent's tested behaviour towards evidence.
- No interventions and no revocation over time (as far as the abstract shows).

**Draft differentiation sentence.** "READY certifies the cheapest accept-or-escalate oversight policy for an agent–workflow configuration from outcome and confidence evidence on held-out cases; WorkTrace asks what evidence should license autonomy in the first place, and shows on held-out episodes whether evidence-handling tests yield a better per-class risk–coverage frontier than outcome-based licensing."

**Citation cautions.** Anonymous and under review. Cite as an "ICLR 2027 submission" only if the venue allows citing OpenReview submissions; otherwise wait for an arXiv version. **Consider adopting its finite-sample certification** (for example, an upper confidence bound on risk at the chosen coverage) for our rule. Reviewers who know READY will ask for it.

### 3.4 Trust Before Autonomy (Angelidis et al., 2026)

**Bibliographic data.**
- Georgios Angelidis, Aggelos Psiris, Spyridon Evangelatos, Thomas Lagkas, Panagiotis Sarigiannidis, Iraklis Varlamis, Georgios Th. Papadopoulos.
- *Trust Before Autonomy: Rethinking Agentic Remote Sensing for Crisis Response*. arXiv:2610.18789v1 (13 Oct 2026). [verified]
- **Read:** §§1–6 in full. Appendix A–D (meta-analysis details) only skimmed through headers.

**Problem and contribution.**
- Position: "autonomy should be earned, not assumed: An Earth-Observation (EO) agent should be granted autonomy in proportion to demonstrated reliability, epistemic honesty and verifiability."
- Contributions: a meta-analysis of 12 agentic remote-sensing, EO and GIS benchmarks; three trust properties; an autonomy ladder; a readiness protocol.

**Method.**
- Trust properties:
  - P1 reliability: pass^k, accuracy on held-out *events*;
  - P2 epistemic honesty: abstention scored "with selective risk–coverage" plus abstention F1 on unanswerable variants, and conformal uncertainty;
  - P3 verifiability: "evidence validity", the share of claims whose cited evidence reproduces the claim on re-execution.
- Ladder (§4): rungs adapted from Feng et al.'s user roles, each attached to an example task class (scene search, flood-mask draft, checkpointed workflow, release-ready map, cloud screening).
- Gates (§5, Table 2): R1 benchmark, R2 replay of archived activations, R3 shadow, R4 supervised, R5 conditional ("Revoked on any drift").
- "an agent is promoted one rung ... only after passing the corresponding gate ... and demoted on failure."

**Evaluation.**
- Only a meta-analysis of published tables. Completion exceeds tool-call correctness by up to 54 pp; capability does not predict abstention (Spearman between −0.25 and 0.50, not significant).
- No gate or ladder is executed.

**What it covers that WorkTrace must NOT claim.**
- The normative position that autonomy should be earned per task class through gated, revocable promotion, measured with risk–coverage and held-out events.
- Replay of archived decisions as a gate.
- "Completion ≠ correctness" as an argument against capability-based autonomy.

**What it leaves open that WorkTrace addresses.**
- It does not implement or evaluate any rule.
- Its "evidence validity" checks reproducibility of cited evidence, not whether the decision depends on that evidence (no interventions, no redundancy).
- Domain-specific (crisis EO).

**Draft differentiation sentence.** "Angelidis et al. (2026) argue that EO agents should climb an autonomy ladder only by passing replay and shadow gates; WorkTrace supplies a domain-general, executable version of such a gate, built on interventional tests of evidence handling, and measures its value on held-out episodes."

**Citation cautions.** A position paper. Its meta-analysis numbers were extracted with Claude's help (their own LLM-use statement). Good to cite as convergent motivation.

### 3.5 Hedwig (Shukla, Feng, Wang, Rostami & Zhang, 2026)

**Bibliographic data.**
- Tanjal Shukla, K. J. Kevin Feng, Leijie Wang, Mohammad Rostami, Amy X. Zhang.
- *Hedwig: Dynamic Autonomy for Coding Agents Under Local Oversight*. Proceedings of the 1st ACM Conference on AI and Agentic Systems (CAIS ’26), 26 May 2026, demo track; doi:10.1145/3786335.3813223 (Crossref verified); arXiv:2605.11495. [verified]
- **Read:** full text, including Appendices A and B. Table 2 coefficient values were not rendered.

**Problem and contribution.**
- Static permission settings and instruction files cannot follow evolving developer trust.
- Hedwig "learns an evolving set of behavioral guidelines from developer decisions and feedback, reducing friction on work for which the agent has earned trust, while tightening oversight when the agent operates outside familiar territory."

**Method.**
- Hard constraints are enforced by the command-line tool. Behavioural guidance is retrieved into the prompt.
- Policy path: "an online logistic regression classifier", warm-started from priors and updated by stochastic gradient descent per developer decision. It uses 13 features (diff size, blast radius, change-pattern risk, prior approvals and denials, security sensitivity, verification-failure history, model confidence and others), persisted per repository.
- Three bands decide the outcome: above 0.90, approve silently; 0.20 to 0.90, approve and flag; below 0.20, live check-in.
- Revocable per topic ("preferences-revoke --topic api").
- Phase-gated actions.

**Evaluation.**
- Two backend tasks with 11 write operations; personas seeded with 20 synthetic decisions replayed three times (60 updates).
- Compared with Claude Code plus CLAUDE.md; an LLM judge (Claude Opus 4.7) labels four required check-ins for the cautious persona.
- Hedwig recall 1.00 (precision 0.67) against CC-C recall 0.50; on the permissive persona, Hedwig makes 4 false positives.
- Single run, no variance, no user study (Appendix B.4).

**What it covers that WorkTrace must NOT claim.**
- Dynamic, fine-grained (per action type or code area) autonomy learned across sessions.
- Tightening and loosening, including per-topic revocation.
- Legibility of why a check-in fired.

**What it leaves open that WorkTrace addresses.**
- The signal is human approval history: what the developer tolerates, not whether the agent's decisions track evidence.
- No held-out evaluation of risk.
- Decision classes are implicit feature regions.

**Draft differentiation sentence.** "Hedwig adapts per-action check-in thresholds to a developer's approval history; WorkTrace grounds the same proceed/escalate decision in tested agent behaviour towards evidence rather than accumulated approvals, which an agent can earn while being right for the wrong reasons."

**Citation cautions.** A demo paper; very small, synthetic evaluation. Feng and Zhang are also the authors of *Levels of Autonomy for AI Agents* (2506.12469), so cite both together as a research line.

### 3.6 Runtime Assurance Contracts (Zabolotnii, 2026)

**Bibliographic data.**
- Serhii Zabolotnii (Cherkasy State Business College and others).
- *Trust Is Not a Score: Runtime Assurance Contracts for High-Risk AI Agents*. arXiv:2609.39717v2 (16 Oct 2026; v1 30 Sep 2026). [verified]
- **Read:** full text (§§1–9, references). Equations (1)–(5) were not rendered; definitions taken from prose.

**Problem and contribution.**
- The "assurance-transition gap": benchmarks and protocols do not say "how observed evidence should change an agent's authority during a consequential task".
- The Runtime Assurance Contract (RAC) binds six elements: autonomy boundary, component eligibility, a stateful transition policy, human authority and capacity, an evidence schema, and hard gates.

**Method.**
- Permission to act is a conjunction of hard gates (G_BOUNDS, G_CONTEXT, G_EVIDENCE, G_ELIGIBILITY, G_SUPERVISION, G_RESOLUTION) alongside a transition policy. It is contrasted with a compensatory weighted score rule.
- Five invariants: authority separation, fail-closed gates, confidence asymmetry, oversight viability, evidence continuity.
- Proposition 1: for binary signals, the score rule equals the conjunction if and only if the threshold does not exceed the smallest weight.

**Evaluation.**
- 174 constructed coding failure-injection cases (87 injections, 87 controls; v2 rebuilt after v1's "index clones").
- At vendor weights the score rule admits 56 of 63 block-required injections; tuned in hindsight, it matches RAC.
- A blind corpus of 124 cases written by OpenAI Codex: RAC admits 35 of 79 injections (16 of 62 within its detectors' contract).
- 18 hand-authored transition traces.
- A 24-episode "prospective synthetic holdout" labelled by two GPT-6 Sol judges: RAC and a stateful baseline both match all 72 labels.

**What it covers that WorkTrace must NOT claim.**
- The framing "evidence → authority transition" with escalate/defer/stop outcomes.
- Non-compensatory gating against score aggregation.
- Human-review capacity as an explicit admissibility condition.

**What it leaves open that WorkTrace addresses.**
- Authority is per action within a task. Nothing is earned across episodes, and there are no decision classes.
- "Evidence" means freshness and provenance of context, not whether the agent's decision depends on it.
- No interventions on the agent's inputs.
- The results are mechanism checks on synthetic cases; the author admits "establish neither deployed safety nor cross-domain effectiveness".

**Draft differentiation sentence.** "Runtime Assurance Contracts specify which gate failures must block or escalate an individual action; WorkTrace operates one level up, deciding from tested evidence-handling behaviour whether an agent may act without escalation in a whole class of decisions."

**Citation cautions.**
- A single author with a series of self-citing frameworks. v1 had duplicated cases.
- **Name collision:** his earlier TRACE (arXiv:2605.03838) differs from Chang & Chang's TRACE (arXiv:2607.12480), which we already cite. Disambiguate both in text and bibliography.
- Do not rely on its numbers. Its Proposition 1 is useful as an argument for why our outcome baseline must be tuned charitably.

### 3.7 Earned Authority under a Fixed Ceiling (Zhang & Zhang, 2026)

**Bibliographic data.**
- Zhaoxi Zhang (University of Technology Sydney), Xiaomei Zhang (Griffith University).
- *Are You Still the Agent I Authorized? Earned Authority under a Fixed Ceiling for Evolving Agents*. arXiv:2607.23586v1 (26 Jul 2026). [verified]
- **Read:** full main text (§§I–IX) and references [22]–[37]. Appendix proofs not read.

**Problem and contribution.**
- "Authorization continuity" for self-evolving agents: when does a grant survive mutation of memory, tools, delegation or task phase?
- A state-bound model: an immutable effect ceiling plus a transition envelope.

**Method.**
- Authority below the ceiling "may contract freely and expand only under specified evidence conditions". A monitor clamp keeps active authority within the ceiling.
- Theorem 1 (non-amplification) holds under complete mediation, sound effect abstraction, attenuating delegation and monitor integrity.
- Six mutation classes.
- §V-C: "If the agent can produce the qualifying evidence itself ... the security guarantee remains [the ceiling] ... A tighter security bound requires ... an independently controlled evaluator."
- §VII criticises the "Earned-autonomy ladder: Performance evidence may raise the terminal boundary ... No fixed ceiling remains."

**Evaluation.** None. §VIII proposes metrics: grant persistence, post-mutation unauthorized effects, false invalidation and interaction cost.

**What it covers that WorkTrace must NOT claim.**
- The formal separation between a fixed ceiling and earned active authority.
- The critique that agent-produced competence evidence is not a security boundary.
- Phase or context changes as triggers to re-evaluate a grant.

**What it leaves open that WorkTrace addresses.** It deliberately does not say *which* evidence should license expansion below the ceiling. That is exactly our contribution.

**Draft differentiation sentence.** "Zhang and Zhang (2026) show that earned authority must stay beneath a ceiling that no runtime evidence can move; WorkTrace adopts that ceiling and supplies what their model leaves abstract, namely an evaluator-controlled, interventional test that decides how much of the ceiling an agent may use per decision class."

**Citation cautions.** A two-author preprint; the theorem is close to definitional under its assumptions; no data.

### 3.8 Agent Reliability Profiles (Hsu et al., 2026): shorter note

**Bibliographic data.**
- Mike Hsu, Medha Bankhwal, Béatrice Moissinac, Kevin Werbach, Lukasz Szpruch, Bennett Hillenbrand.
- *Agent Reliability Profiles in Financial Services*. arXiv:2610.04123v1 (2 Oct 2026), "Working draft circulated for comment" (MLCommons Financial Services Working Group). [verified]
- **Read:** §§1–8.1 and §§9–12 in full. Not read: §8.2, §9.3, Appendices A–D.

**What it does.**
- A per-deployment bounded claim over four axes: autonomy tier T0–T4 plus residual status U; ODD; permitted and prohibited sets over 12 action classes ordered by reversibility; control envelope (55 controls).
- Floors that must pass, an invalidation list, and three assurance levels (asserted, validated by in-house tests, verified by an independent assessor).
- §4.1: "The tier is defined by evidence ... A deployment reaches T2 when the approval log shows that human approvals are substantive". Habituation testing: inject materially incorrect proposals and measure reviewer catch rates.

**Evaluation.** None; it is a programme of work (§11).

**Must not claim.** Action classes graded by reversibility as the axis of autonomy; test-validated autonomy tiers; invalidation on material change.

**Open for us.**
- Tiers attach to deployments and are set by the institution's choice of envelope. Tests check that the claimed boundary holds; they do not decide how much autonomy is warranted.
- No evidence-handling tests and no rule evaluation.

**Differentiation.** "Agent Reliability Profiles certify that a deployment stays within a declared autonomy tier and action set; WorkTrace decides, from tested evidence handling, which tier each decision class has earned."

**Cautions.** Working draft. Influential authors (former Acting Comptroller of the Currency, Wharton, Turing Institute), so financial-services reviewers may know it. We should align our "decision class" with their action classes (A1–A12) where possible.

---

## 4. Explicit check: does anything do ALL of (a)–(d)?

(a) per-decision-class autonomy; (b) earned from tested behaviour towards evidence; (c) revocable; (d) evaluated on held-out data.

| Work | (a) per class | (b) earned from evidence-handling tests | (c) revocable | (d) held-out evaluation of the rule |
|---|---|---|---|---|
| Digital Apprentice | ✔ per skill | ✘ correction rate and judge score | ✔ automatic demotion | ✘ |
| Intelligent AI Delegation | ~ per task/context | ✘ reputation; "behavioral metrics" unspecified | ✔ circuit breakers | ✘ no evaluation |
| READY (abstract only) | ✘ per configuration | ✘ outcomes and confidence | ? | ✔ held-out, finite-sample |
| Trust Before Autonomy | ✔ per task rung | ~ reliability, abstention, evidence validity, but not interventional | ✔ "demoted on failure" | ✘ prescribed, not run |
| Hedwig | ~ per action features or area | ✘ approval history | ✔ per topic | ✘ 11 operations, LLM judge |
| Runtime Assurance Contracts | ✘ per action in a task | ✘ context and provenance gates | ✔ within a task | ~ 24-episode synthetic holdout of a policy, not of earned autonomy |
| Earned Authority (fixed ceiling) | ~ per grant | ✘ evidence left abstract | ✔ | ✘ |
| Agent Reliability Profiles | ~ per deployment × action classes | ~ tests validate a declared tier | ✔ invalidation | ✘ |
| Feng et al., Levels of Autonomy | ✘ per agent | ~ third-party evaluations of autonomy level | ✔ renewal | ✘ |

**Answer: no.** No work found satisfies all four. None uses interventions on the external evidence available at decision time as the basis for granting autonomy. Only READY and RAC run any held-out evaluation of a delegation or oversight policy, and neither is per decision class or earned from evidence handling.

**Residual risk.**
1. I read READY only as an abstract.
2. AAMAS 2026 and FAccT 2026 proceedings were not browsable through my tools.
3. ICLR 2027 submissions are anonymous and growing. Others with abstract-level relevance are "When Agents Refuse to Ask for Help" and "BeaconAgent: Learning Capability-Aware Help-Seeking Policies" (both agent self-help-seeking).

---

## 5. Implications for WorkTrace

### 5.1 Changes to our claims

1. **C1 (MAS bridge): downgrade from "first bridge" to "operational bridge".** Tomašev et al. (2026) already ground LLM-agent delegation in Castelfranchi & Falcone (1998) and Falcone & Castelfranchi (2002). Suggested wording: "We make the delegation-theoretic programme (Castelfranchi & Falcone 1998; Falcone & Castelfranchi 2002; Scerri et al. 2002), recently revived for LLM agents by Tomašev et al. (2026), operational: …". Also cite Falcone & Castelfranchi (2002) on adjustable social autonomy (bibliographic data [unverified] here; verify via DOI) and Feng et al. (2025) for autonomy levels. Correct positioning.md §1 and §3.1 accordingly.
2. **Do not claim "earned autonomy", "graduated autonomy" or "revocable autonomy" as new concepts.** They belong to Digital Apprentice, Trust Before Autonomy, Hedwig, Intelligent AI Delegation, Feng et al. and practitioner frameworks. Claim instead: **the evidence that should license autonomy is tested behaviour towards external evidence, not outcomes, approvals or correction rates; we provide the test, the rule and a held-out comparison.**
3. **Do not claim risk–coverage, escalation cost or held-out certification as methodological novelty.** They belong to READY, *Oversight Has a Capacity*, Trust Before Autonomy and the selective-prediction literature. Claim the *comparison*: evidence-test rule against outcome-only and approval-history rules, per decision class, on held-out generated episodes.
4. **Keep C2** (redundancy-robust interventions on external evidence) as the most clearly novel element. Cite AgentAbstain's paired controlled perturbations and Matton et al. (handled elsewhere) as nearest neighbours.
5. **Reframe the thesis sentence** so that it contrasts with outcome-, approval- and confidence-based licensing. That contrast is what all the close works share and what we do not.

### 5.2 Design changes

1. **Add an approval-history baseline** next to the outcome-only rule. This makes the Digital Apprentice and Hedwig signals into concrete competitors: promote a class when the correction rate falls below a threshold over a window of n episodes, or a logistic policy on approvals. It pre-empts the reviewer question "why not just learn from approvals?".
2. **Adopt an explicit fixed ceiling**, following Zhang & Zhang. The rule can only allocate autonomy below a human-issued permission ceiling per class. Interventional tests are run by the evaluator, not produced by the agent; state this explicitly to answer their §V-C critique.
3. **Consider finite-sample certification** of the chosen operating point (an upper confidence bound on per-class risk at the chosen coverage, e.g. Clopper–Pearson or a Learn-then-Test style guarantee), so that we are not weaker than READY on statistics.
4. **Model the escalation cost** at least as a constant plus a sensitivity analysis. Discuss *Oversight Has a Capacity* (reviewer fatigue makes the cost endogenous) and Agent Reliability Profiles and Digital Apprentice (reviewer complacency) as threats to approval-based rules. This is a principled argument for evidence tests that do not depend on reviewer vigilance.
5. **Decision-class definition:** consider aligning it with the reversibility-ordered action classes of Agent Reliability Profiles (A1–A12) or the task axes of Tomašev et al. (criticality, reversibility, verifiability). That gives an external anchor and avoids looking ad hoc.
6. **Distinguish two kinds of escalation:** agent *self*-escalation (HiL-Bench, AgentAbstain, Ambig-SWE, SURE-Act, LEASH) and the *principal's* delegation rule (ours). These benchmarks could also serve as sources of decision episodes.

### 5.3 Things to cite (additions to related work)

- **Earned/graduated autonomy:** Weber & Taneja 2026; Shukla et al. 2026 (Hedwig); Angelidis et al. 2026; Ou 2026; Anthropic, *Measuring AI agent autonomy in practice* (2026).
- **Delegation theory revived for LLMs:** Tomašev, Franklin & Osindero 2026; Falcone & Castelfranchi 2002 (verify).
- **Autonomy levels and certification:** Feng, McDonald & Zhang 2025; Hsu et al. 2026; Zheng et al. 2026 (AAL/ACL); Luong Tuan & Sanyal 2026; Kasirzadeh & Gabriel 2025; Mitchell et al. 2025; Cihon et al. 2025.
- **Authority and gating:** Zabolotnii 2026 (RAC); Zhang & Zhang 2026; Shi et al. 2025 SoK; Progent (Shi et al., arXiv:2504.11703, cited via RAC, [unverified] by me); Parisel 2026.
- **Oversight cost and certification:** READY (ICLR 2027 submission); Turan 2026; Clymer et al. 2024 (safety cases).
- **Escalation and abstention benchmarks:** HiL-Bench; AgentAbstain; Ambig-SWE (ICLR 2026); Learning to Ask (EMNLP 2025); Agents' Last Doubt / SURE-Act; Calibrate-Then-Act; RegLLM.
- **Process versus outcome:** AgentLens (Lucky Pass); Advani (right for wrong reasons); Rabanser et al. (ICML 2026).

### 5.4 Risks

- A reviewer citing Tomašev et al. and Digital Apprentice could call C1 and the thesis "known". Mitigate by making the contrast with outcome, approval and correction signals explicit in the abstract and introduction.
- READY may appear on arXiv or be accepted at ICLR 2027 before our submission. Monitor it, and re-read the full PDF when accessible.
- The "TRACE" name collision (Chang & Chang against Zabolotnii) could confuse reviewers. Always give the arXiv id.
