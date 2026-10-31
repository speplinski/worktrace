# DNative-Twin (Pang et al., arXiv:2609.03787) — reading note for WorkTrace

**Coverage:** I read the whole paper: the arXiv HTML v1 (abstract, §I–VIII, all tables I–IX, Algorithm 1, the Fig. 1 caption, and references [1]–[22]). I also checked it against the v1 PDF (pdftotext), which has the same content and the text inside the Fig. 1 image. There are no appendices or supplementary material, and the paper gives no code or artifact link. Table V only *specifies* a "minimal artifact package". Quotes below are verbatim from v1.

---

## 1. Bibliographic data

- **Title:** DNative-Twin: Decision Graphs and Digital Twins for Reconstructable Agentic Decisions
- **Authors and affiliations (as printed):**
  - Junjie Pang: Qingdao University, Qingdao, China
  - Zhenzhen Xie: Shandong University, Qingdao, China
  - Haoke Han: Qingdao University, Qingdao, China (the submitter on arXiv)
  - Ying He: Hangzhou Shujiao Technology Partnership (Limited Partnership), Hangzhou, China
  - Jing Wang: Changchun University of Technology, Changchun, China
  - Gang Liu (corresponding author, lg@ccut.edu.cn): Changchun University of Technology, Changchun, China
- **arXiv:** 2609.03787v1 [cs.AI]. Submitted Thu, 3 Sep 2026 12:59:34 UTC. Only v1 existed as of 2026-10-25. License: arXiv perpetual non-exclusive.
- **Venue:** arXiv preprint only. No journal-ref and no comments field. The formatting is IEEE-style ("Index Terms", Roman-numeral sections, IEEEtran look), which suggests an IEEE submission, but the paper does not say so. *Uncertain.*
- **Index Terms:** AI agents, agentic decisions, decision reconstructability, digital twin, heterogeneous graph, agent governance.
- **Suggested BibTeX key:** `pang2026dnativetwin`. Cite as: J. Pang, Z. Xie, H. Han, Y. He, J. Wang, G. Liu, "DNative-Twin: Decision Graphs and Digital Twins for Reconstructable Agentic Decisions," arXiv:2609.03787, Sep. 2026.

## 2. Problem & motivation

A final agent output cannot show *which evidence, tool state, rule, authorization, or action path produced it*. The motivating example (§I) has two procurement runs that both return APPROVE:
1. Current supplier alert, valid policy, successful budget call, authorized manager.
2. Stale alert, budget-call timeout, informal override.

The outputs agree but the "decision mechanisms" differ. The authors call the ability to recover this path **decision reconstructability**. Their diagnosis is that existing operational and provenance records "leave three parts disconnected: what the agent observed, how it acted, and what authorized the resulting action."

→ This is the "same output, different mechanism ⇒ output-only assessment is insufficient" argument. **They already make it.** We cannot present the argument itself as new. We can only present our use of it (tested evidence-sensitivity → autonomy) as new.

## 3. Core contributions (their list, §I)

1. A dynamic heterogeneous decision graph that connects what an agent observed, how it acted, and how the resulting action was authorized and committed.
2. Decision trajectories defined as decision-bounded subgraphs, plus a formal definition of reconstructability for "human–AI and delegated automated decisions".
3. DNative-Twin itself: it replays a decision mechanism in synchronized state and compares its trajectory under controlled changes.
4. An executable specification (invariants I1–I7, a graph-algorithm interface, a minimal artifact package) and an enterprise evaluation on public process logs plus controlled replay suites.

Other notable pieces:
- **Governance equivalence** of trajectories.
- **Four-way rule-based adjudication** of GraphDiffs: benign / material / critical / unresolved.
- A **ReleaseReady** gate plus an independent **GovApproves** step for revised mechanisms.
- A **traceability vs validity vs contextual applicability** distinction (`App(v,S_t)`).

## 4. What does "DNative" mean? Name-collision check

- **The paper never expands "DNative".** It does not appear as an acronym or in any definition. The only "-native" words are "DNative-Twin" itself and **"graph-native"**, which appears twice:
  - Abstract: *"We present DNative-Twin, a **graph-native** digital twin that records a committed agentic decision as a typed trajectory and re-executes its decision mechanism under declared conditions."*
  - §I: *"We implement this model in DNative-Twin, a **graph-native** digital twin for reconstructing and testing agentic decision mechanisms (Fig. 1)."*
- **"decision-native" does not occur** in the HTML or the PDF (grep-checked both).
- Reading "D" as "Decision" is plausible, given the title "Decision Graphs…" and the stress on "decision trajectory". That is **my inference only**; the paper does not state it.
- **Collision implications:**
  - "DNative" is a visible brand-like prefix in a 2026 cs.AI paper about agent decisions, authority and enterprise processes. A reader may well read "Decision-Native Banking Agents" as related to, or derived from, DNative-Twin.
  - The paper does not claim the term "decision-native", so there is **no prior-definition conflict**.
  - Recommendation: never abbreviate our track as "DNative" or "DN-…". If "Decision-Native" stays, add one footnote: "unrelated to DNative-Twin [Pang et al. 2026], which uses 'graph-native' and does not define 'decision-native'".

## 5. Representation: the committed agentic decision as a typed trajectory

**State tuple (Eq. 1):** S_t = (B_t, K_t, P_t, T_t, H_t, A_t, O_t)

| Symbol | Contents |
|---|---|
| B | decision objects |
| K | versioned knowledge |
| P | policies, constraints, **authority grants** |
| T | tools and their observable states |
| H | authorized human or machine actors and roles |
| A | agents and bounded skills |
| O | outcome signals |

The text adds: *"S_t is the state relevant to one class of decisions."* (They use "class of decisions" too; see §14.)

**Graph (Eq. 2):** G_t = (V_t, E_t, X_t, φ, ψ, ρ), a temporal attributed heterogeneous multigraph. The metadata map ρ gives each element an environment label, source time, ingestion time, validity interval, version, provenance reference, and confidence when applicable. It also carries machine-readable *scope* and *precondition* fields for state-sensitive items.

**Table I (exact): minimum node and relation types**

| Category | Minimum node types | Representative edge types |
|---|---|---|
| Decision context | DecisionObject, EvidenceArtifact, KnowledgeUnit, PolicyRule | about, supports, contradicts, version_of, governs |
| Execution | Agent, Skill, ToolCall, DecisionEvent | performed, invokes, uses, acts_on, produces |
| Authorization | AuthorizedActor, DecisionRole, ReviewEvent, AuthorityGrant | holds_role, authorizes, commits, reviews, delegates_to |
| Decision | Recommendation, CommitmentEvent, OutcomeSignal | recommends, committed_as, modified_as, results_in, responds_to |
| Twin operation | ScenarioPerturbation, GraphDiff, CandidateRevision | perturbs, replayed_from, diverges_from, motivates |

Totals are 18 node types and 25 representative edge types. The edge list is "representative", not closed. Domains may add or refine types.

**Mechanism (Eq. 3):** M = (Q, π, Γ, Λ). These are the typed decision states, the action policy of agents and actors, the constraints, and the commitment/escalation/release rules (Λ). Γ = Γ_path ∪ Γ_temporal ∪ Γ_version ∪ Γ_app. M is kept separate from G so that the mechanism can be replayed against different states.

**Trajectory (Eq. 6):** T(b,z;[t0,t1]) is the induced subgraph on the decision object b, a terminal node z ∈ {DecisionEvent, CommitmentEvent, ReviewEvent}, z's admissible decision ancestors, and the outcome nodes attributed to z. Admissibility uses relations such as uses, supports, invokes, produces, reviews, authorizes, commits, committed_as, results_in. A boundary rule excludes records that merely share a case ID.

**How authority is represented:**
- **Recommendation and commitment are separate nodes** (invariant I1).
- `Committed(T,a)=1` (Eq. 8) holds iff all of the following:
  - there is a recommendation r with (r, committed_as | modified_as, a);
  - there is an AuthorityGrant g with (g, authorizes, h) and an AuthorizedActor h with (h, commits, a);
  - Valid(g, a.time)=1 and App(g, S_{a.time})=1.
- A rejection is a ReviewEvent with no commitment.
- *"In automated operation, an authorized machine actor may commit the output within authority granted in advance."*
- Authority grants are attribute-style (they cite NIST ABAC [1]) and carry scope and preconditions.
- `delegates_to` exists as an edge type but is never formalized further. In the case study, a missing delegation (alternate approver) is the defect that gets repaired.

**Reconstructability (Eq. 10):**
- Every required antecedent type group R_j has some ancestor of the matching type. Minimal groups: {DecisionObject}, {EvidenceArtifact}, {KnowledgeUnit, PolicyRule}, {Agent, ToolCall}, {AuthorizedActor}, {AuthorityGrant}.
- Outcome is covered: an OutcomeSignal descendant exists, or the outcome is PendingOutcome.
- All constraints in C(a) hold.

Three failure types are distinguished: **capture failure** (something missing), **mechanism failure** (constraint violated) and **divergence** (valid trajectories differ across environments).

## 6. The digital twin & replay

- **Synchronization contract (Eq. 11):** a typed mapping σ: ΔG_real(t) → ΔG_twin(t′). It "need not preserve identity": IDs are tokenized, sensitive evidence becomes governed references, and unavailable tools get "consequence-preserving stubs". The contract states what is synchronized, how fresh, which transformations apply, and how failed updates are represented.
- **Shadow replay (Eq. 15):** T_shadow = Execute(M, S^twin_t, C_R). *"The real trajectory T_real is an attributable comparison reference rather than executable ground truth."*
- **Replay contract (Eq. 16):** C_R = (b, t_cut, K, P, A, T, H, Θ, Ω), grouped into four parts:
  1. decision identity and cutoff (b, t_cut);
  2. governed state (K, P, H);
  3. execution configuration (A, T, Θ);
  4. environment Ω.

  "Each unbound or substituted field is recorded as a possible source of divergence."
- **Tool replay modes (Table III):**

  | Mode | Question it answers |
  |---|---|
  | Response injection | Is downstream behaviour reproducible under the historical observation? |
  | Executable replay (read-only copy) | How does the mechanism behave under the currently synchronized tool state? |
  | Consequence-preserving stub | How does the mechanism handle a declared result or failure, with no production side effects? |

- **Isolation:** the twin has no authority to commit external actions (I4). Side-effecting calls become read-only or simulated, labelled environment=twin.
- **Declared conditions / controlled changes:**
  - A scenario operator W_δ(G_twin, M, b) applies a typed perturbation δ, recorded as a ScenarioPerturbation node linked to the baseline. "Perturbation then tests **one declared dependency** of that baseline."
  - Examples: replace a successful budget check with a timeout; add a supplier-risk alert K-supplier-alert-v13; remove the primary manager's authority; near-threshold value changes (50,000 → 50,001); evidence availability; regional shipping constraints.
  - The evaluation has "material" and "null" interventions, plus seven drift types.
- **Alignment and diff:**
  - Terminal nodes are aligned when they share the decision object, replay lineage, mechanism version and observation window.
  - GraphDiff D = (ΔV, ΔE, ΔX, ΔP) covers nodes, edges, attributes and paths (they cite graph edit distance [2]).
  - Source labels Src ⊆ {state, config, tool, stoch, mechanism} are not mutually exclusive.
- **Governance equivalence (∼_I):** equal required-evidence coverage, applicable-policy set, authority path, critical-invariant vector, commitment class and outcome constraints. Structural differences within the class are "benign".
- **Classify (Eq. 14):** returns the first label that applies, in priority order:
  1. **unresolved**: *"It returns unresolved when the available evidence cannot support a governed classification."*
  2. **critical**: a mandatory authority, isolation, evidence or review violation;
  3. **material**: another governance-relevant change;
  4. **benign**: the trajectories stay governance-equivalent.

  *"Frequency does not override a mandatory constraint."*
- **What "unresolved divergence" means:** a difference whose governance effect cannot be decided from the evidence available. The canonical case is an **unobserved tool state (tool timeout)**: the graph has no structural trace of the timeout's consequence. A graph-only detector therefore calls it benign. Replay-contract state (the tool mode and expected behaviour) and verification results (whether the condition held) are needed to recover it.
- **Revision loop:** Algorithm 1, "Synchronize–Replay–Stress–Diff–Revise". A CandidateRevision M′ is linked to the divergence that motivated it.
  - ReleaseReady(M′) (Eq. 17) requires C_inv=1, C_scn=1, r_mat ≤ ε_mat, r_eq ≥ τ_eq, f_twin ≥ τ_fresh and N_crit,unres = 0.
  - Release also requires an independent GovApproves.
  - Drift, a policy or tool change, a new incident or a new critical scenario reopens the cycle. An iteration cap and a replay budget stop it.

## 7. Evaluation

**Evidence layers.** Every field is labelled *source-observed, derived, overlaid, injected,* or *model-annotated*. The public logs do not contain LLM prompts, replay modes, authority grants or applicability rules. These appear "only in the declared overlay or injected layers".

**Three public process logs (Table VI):**

| Log | Cases/objects | Events | Nodes | Edges | Node types | Edge types |
|---|---|---|---|---|---|---|
| OCEL 2.0 Procure-to-Pay [4,5] | 9,543 | 14,671 | 30,956 | 81,132 | 6 | 5 |
| BPI Challenge 2020 PermitLog (travel permit) [6] | 5,000 | 61,408 | 225,290 | 349,116 | 10 | 9 |
| BPI Challenge 2019 (seed-42 reservoir sample of 5,000 from 251,734 traces / 1,595,923 events) [7] | 5,000 | 30,428 | 103,283 | 164,272 | 11 | 9 |

An independent operator re-ran the BPI 2019 pipeline and reproduced all 18 declared checks, with byte-identical case-ID files.

**Research questions:** RQ1 graph dependency retrieval; RQ2 replay stability; RQ3 material vs null interventions; RQ4 value of replay-contract and verification information for adjudication; RQ5 revision gate.

**Information baselines:** B0 final output only → B1 ordered trace → B2 structural GraphDiff → B3 full graph and queries.

**Results:**

*Graph construction and queries*
- **OCEL:** all 3,371 evaluable commitments passed I1/I2. All 1,598 purchase orders have a Create–Approve–Pay trajectory.
- **BPI 2020 mapping ablations:**
  - Removing the overlay policy layer drops knowledge-policy traceability from 1.0 to 0.
  - Unresolved resource identity drops the human-approval-path pass rate from 1.0 to 0.
  - Base 225,290 nodes; strict 188,093; broad 228,761.
- **Dependency queries** (7 constructed cases, 5 questions): accuracy B0 0.06, B1 0.14, B2 0.20, B3 1.00. Caveat: B3 had access to overlay ground truth that B0–B2 lacked.
- **LLM annotation probe** (20 BPI 2020 cases, two prompt-separated LLM annotators): raw agreement 0.55, κ = 0.5175.

*Replay stability*
- 50 BPI 2020 carriers × 30 runs at temperature 0: exact trajectory match = governance-equivalent rate = 1.0.
- Injected-noise flip rate 0.098 ± 0.014, with governance equivalence preserved.
- 38/50 carriers passed I5 (knowledge-version traceability).

*Perturbation suite*
- 7 constructed cases, 42 material and 27 null interventions.
- Detected 36/42 (PS = 0.8571, F1 = 0.9231). NPS = 1.0 (27/27 stable).
- The 6 misses were near-threshold changes: ground-truth threshold 50,000 vs a detector alert band of 55,000.

*Drift injection*
- 7 drift types × 40 held-out BPI 2020 carriers = 280 instances.
- Sensitivity, benign stability and source localization were all 1.0.
- The graph-only detector labelled **all 40 unresolved tool-timeout cases benign** (unresolved recall 0, macro-F1 0.6667).

*Three-condition experiment (Table VIII)*
- 30 held-out BPI 2020 carriers × 11 scenarios = **300 instances: 180 benign, 30 material, 90 unresolved, 0 critical**. The critical-timeout scenario needed requests above 50,000, and none of the carriers had one.

| Metric | A: Graph | B: +Contract | C: +Verification |
|---|---|---|---|
| Macro-F1 (over benign/material/unresolved) | 0.600 | 0.908 | 1.000 |
| Unresolved recall | **0.000** | **0.667** (60/90) | **1.000** (90/90) |
| Unresolved→benign FN | 1.000 | 0.333 | 0.000 |
| Critical support | 0 | 0 | 0 |

- Condition C uses *injected* signature-verification results. The authors say it "measures the value of making those outcomes available".

*Tool replay modes*
- With no drift, the three modes agree.
- Under drift, injection keeps the historical observation, executable replay exposes the change, and the stub preserves the consequence.

*Revision gate*
- M0 (budget timeout with no fallback) vs M1 (bounded escalation added):
  - critical-invariant pass rate 0.7143 → 1.0;
  - material-divergence rate 0.3333 → 0;
  - governance-equivalent rate 0.7143 → 1.0;
  - unresolved critical cases 6 → 0.
- M0 fails and M1 passes under the 4 thresholds evaluated, out of 8 conditions.

*Scalability (BPI 2020, 5 reps)*
- Median end-to-end time: 0.794 s (500 cases), 1.682 s (1,000), 4.335 s (2,500), 8.889 s (5,000).
- At 5,000 cases, graph construction takes 1.797 s and invariant checking 3.846 s.
- Platform: Python 3.11.15, NetworkX 3.6.1, Apple M5 Pro, 64 GB RAM.

*External-model noise probes (Table IX; 5 calls per case)*

| Probe | Valid calls | Exact repeat | Baseline agreement |
|---|---|---|---|
| DeepSeek-20 | 100/100 | 0.700 | 0.820 |
| DeepSeek-100 | 500/500 | 0.870 | 0.932 |
| Kimi-100 | 496/500 | 0.960 | 0.982 |

**My read of the evaluation:** almost everything beyond graph construction is *constructed* or *injected* (overlay authority, injected drift, injected verification results). Positives are recovered by design: B3 has the ground-truth overlay, and C has the injected verification fields. The critical class is never exercised on held-out data. No real LLM agent's decisions are reconstructed end to end. The external probes measure only output repeatability.

**Uncertainty:** the paper does not say clearly what executes M in the replay experiments. It mentions "carriers" and a "temperature-zero contract", and there are separate LLM probes. The mechanism may be rule-based or an LLM, and I could not determine which.

## 8. Faithfulness of stated reasons?

**No.** The paper reconstructs *mechanisms and dependencies* (which evidence, policy, tool call and authority are graph ancestors of a commitment). It never tests whether the agent's *stated reasons* are faithful to what actually drove the action.

- There is no model-declared "grounds" object. The agent's rationale is not a node type. The `supports`/`contradicts` edges link evidence to decision objects, but nothing says who declares them.
- The Fig. 1 legend separates **"Observed Relation (Recorded Link)"** from **"Derived Relation (Inferred Link)"**. The field-level labels are source-observed / derived / overlaid / injected / model-annotated. These are **data-provenance labels, not a declared-vs-actual-reason separation**.
- Interventions test whether the **trajectory/governed path** changes as it should (material vs null). They do not test whether the agent's account of *why* matches its sensitivity to evidence. "Null intervention stays stable" and "material intervention is detected" concern detector or mechanism behaviour, not reason faithfulness.
- They explicitly defer causal and correctness claims: *"The resulting record supports later analysis of correctness, fairness, and causality, each of which requires its own evidence."* (§II-B)
- No CoT-faithfulness literature is cited.

## 9. Authority, permissions, delegation, autonomy scope, escalation

**What they do with "the authority behind the resulting action":**
- They *record* it (AuthorityGrant → authorizes → AuthorizedActor → commits → CommitmentEvent).
- They *check* it: it must be valid at commit time and contextually applicable (`App(g,S)`); required review must not be bypassed (I3); the twin has no grant (I4).
- They *perturb* it (removing the manager's authority) to expose missing alternate paths.
- They *repair* the mechanism, e.g. by adding a "bounded alternate-approver rule" or "bounded escalation".

Escalation appears as a rule within Λ ("commitment, escalation, and release rules") and as an expected replay outcome (APPROVE → ESCALATE when an alert activates a mandatory fallback).

**What they do *not* do:** they never decide or learn what an agent *may* do autonomously. Authority is an **exogenous input** ("authority delegated in advance", "a grant issued in advance"). There is no:
- mechanism for granting, scoping, widening or revoking autonomy per decision class from evidence of behaviour;
- risk–coverage analysis;
- escalation-cost model.

The closest analogue is the **ReleaseReady + GovApproves gate**. It gates the *release of a revised decision mechanism* against a critical scenario suite and thresholds. It is not an autonomy grant to an agent for a decision class, and approval remains an external governance act.

Quotes:
- §I: *"Some decisions remain under direct human review; others operate under authority delegated in advance. In both settings, a consequential action must be connected to what the system observed, how it acted, and the authority under which the action was taken."*
- §II-A: *"In an automated setting, the same authority path can end at a machine actor operating within a grant issued in advance."*
- §II-A: *"one authority grant can cover a bounded class of commitments."*
- §III-C: *"Passing these criteria makes the mechanism eligible for authorization under the declared scenario suite and thresholds. The subsequent GovApproves step records the independent authorization decision; release requires both results."*
- §VI: they note that the Agentic BPM manifesto [18] "emphasizes bounded autonomy and explainability". This is the only time "autonomy" appears in the paper.

## 10. Redundancy / overdetermination

**Not addressed as a causal problem.** Three related points:
- **Disjunctive requirement groups:** each R_j "contains acceptable alternatives for one requirement", e.g. {KnowledgeUnit, PolicyRule}. Reconstructability needs ∃ one ancestor of each group. This is redundancy-tolerant *coverage checking*, not a test of which source actually drove the decision.
- **Governance equivalence handles reordering:** *"Two executions may retrieve independent evidence in different orders while preserving the same decision dependencies."* That covers order, not redundant or duplicated grounds.
- **Interventions are single-dependency** ("tests one declared dependency of that baseline"). They are add or change state, or remove authority. There is no "only X", no "invert X", and no "add a second corroborating source". There is no discussion of the case where removing one of two sufficient grounds leaves the action unchanged (the masking or overdetermination problem). A "null intervention" in their sense is an *irrelevant* change, not a *redundant* one.

→ Our redundancy-robust intervention set (remove X / only X / invert X / add second source) is **not covered** by this paper.

## 11. Limitations

**Acknowledged by the authors (§VII):**
- Applies only when there is an identifiable decision object and a bounded trajectory with recordable dependencies, constraints, authority and outcome. "Generation without a committed action falls outside this scope."
- Evaluated only on enterprise processes. Other domains need their own evidence, authority rules, constraints and outcomes.
- Schema design and event-to-graph extraction bound what can be reconstructed, and some queries depend on derived or overlay fields.
- The BPI 2019 results describe the sample only.
- Replay stability was measured under one fixed configuration. The external probes cover two provider-specific models.
- Adjudication covers injected benign, material and unresolved cases only, with **no held-out critical instance**.
- The release demonstration evaluates **4 of 8** declared conditions (freshness, the full critical suite, iteration limits and replay budget are not evaluated).
- Privacy: deployment needs access control, retention limits and privacy-preserving references.
- Graph structure alone cannot see unobserved tool state; replay context and verification are needed.

**Limitations I see:**
- **Circularity of the strong results.**
  - B3's 1.00 query accuracy uses overlay ground truth that B0–B2 lack.
  - Condition C's 1.0 recall uses *injected* verification fields that directly encode the answer.
  - Authority grants, applicability rules and prompts are overlays, not observed data.
- **Small constructed suites:** 7 cases for queries and perturbations, and the near-threshold misses came from a pre-set alert band.
- **No real LLM agent decisions are reconstructed.** The LLMs appear only as annotators (κ ≈ 0.52) and in repeatability probes. It is unclear whether M in replay is an LLM.
- **No faithfulness test** of agent-stated reasons. Reconstructability is graph-ancestor *presence*, not evidence that a dependency was *used* or causally *sufficient*. The authors themselves defer causality.
- **Authority is assumed, not earned.** There is no feedback from replay results to the scope of autonomy. Escalation cost and human workload are not measured.
- **Classification is rule-based** with hand-declared invariants and thresholds. There is no learning or generalization test across decision classes.
- **No comparison** to existing agent-tracing or provenance tooling beyond the conceptual Table II.
- **Released code is not present.** Table V specifies an artifact package but gives no link. *Uncertain whether one exists elsewhere.*
- **The MAS delegation and adjustable-autonomy literature is absent** (Castelfranchi & Falcone, Bradshaw, Scerri et al.), as are selective prediction and risk–coverage work.

## 12. Related work they cite that is relevant to us (full references as printed)

- [1] D. Ferraiolo, R. Kuhn, A. Schnitzer, A. Sandlin, K. Miller, K. Scarfone, "Guide to attribute based access control (ABAC) definition and considerations," NIST, 2014, pp. 1–47. *(authority-grant scope and preconditions)*
- [3] I. D. Raji, A. Smart, R. N. White, M. Mitchell, T. Gebru, B. Hutchinson, J. Smith-Loud, D. Theron, P. Barnes, "Closing the AI accountability gap: defining an end-to-end framework for internal algorithmic auditing," FAT* '20, pp. 33–44, 2020.
- [9] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, Y. Cao, "ReAct: synergizing reasoning and acting in language models," ICLR 2023.
- [10] Y. Ruan, H. Dong, A. Wang, S. Pitis, Y. Zhou, J. Ba, Y. Dubois, C. J. Maddison, T. Hashimoto, "Identifying the risks of LM agents with an LM-emulated sandbox," arXiv:2309.15817, 2023. *(ToolEmu)*
- [11] Z. Zhang, S. Cui, Y. Lu, J. Zhou, J. Yang, H. Wang, M. Huang, "Agent-SafetyBench: evaluating the safety of LLM agents," arXiv:2412.14470, 2024.
- [12] NIST, "Artificial intelligence risk management framework: generative artificial intelligence profile," NIST AI 600-1, 2024.
- [13] L. Moreau, P. Missier, "PROV-DM: the PROV data model," W3C Recommendation, 2013.
- [14] OpenTelemetry Authors, "OpenTelemetry specification: tracing API and trace semantic conventions," 2026 (accessed 2026-08-14).
- [15] A. AlSayyad, K. Y. Huang, R. Pal, "AgentTrace: a structured logging framework for agent system observability," arXiv:2602.10133, 2026.
- [16] W. M. P. van der Aalst, A. Adriansyah, A. K. A. de Medeiros, et al., "Process mining manifesto," BPM Workshops, LNBIP 99, pp. 169–194, 2012.
- [17] M. Dumas, F. Milani, D. Chapela-Campa, "Agentic business process management systems," BPM Workshops, LNBIP 569, pp. 3–14, 2026.
- [18] D. Calvanese, A. Casciani, G. De Giacomo, M. Dumas, F. Fournier, T. Kampik, E. La Malfa, L. Limonad, A. Marrella, A. Metzger, M. Montali, et al., "Agentic business process management: a research manifesto," arXiv:2603.18916, 2026. *(**bounded autonomy**; probably worth checking for our bridge contribution)*
- [19] G. Park, W. M. P. van der Aalst, "Realizing a digital twin of an organization using action-oriented process mining," ICPM 2021, pp. 104–111.
- [20] K. Lyytinen, B. Weber, M. C. Becker, B. T. Pentland, "Digital twins of organization: implications for organization design," Journal of Organization Design 13, pp. 77–93, 2024.
- Lower relevance: [2] Gao et al. 2010 graph edit distance survey; [4] Park & Unterberg 2023, OCEL 2.0 P2P log (Zenodo); [5] Berti et al. 2024, OCEL 2.0 spec, arXiv:2403.01975; [6] van Dongen 2020, BPI Challenge 2020; [7] van Dongen 2019, BPI Challenge 2019; [8] NetworkX; [21] Ji et al. 2022, KG survey, IEEE TNNLS; [22] Cai et al. 2022, temporal KG completion survey, arXiv:2201.08236.

Note that author names in [4] are garbled in the HTML ("G. Park and g. U. Leah Tacke"); they are probably G. Park and L. Tacke genannt Unterberg. In [18] the HTML prints "G. D. Giacomo" and "E. L. Malfa"; I normalized these to De Giacomo and La Malfa.

## 13. Short verbatim quotes useful for our related work

1. §I: *"Consider two procurement runs that both return APPROVE. … The outputs agree, but the decision mechanisms differ. These differences determine whether the committed action can be explained, reproduced, and safely revised. We call the ability to recover this path decision reconstructability."*
2. §I: *"Existing operational and provenance records rarely preserve this path as one connected record. They often leave three parts disconnected: what the agent observed, how it acted, and what authorized the resulting action."*
3. §III-A: *"DNative-Twin joins these records around a decision trajectory, which becomes the unit of replay and comparison."*
4. §III-B: *"Replay establishes a baseline; perturbation then tests one declared dependency of that baseline."*
5. §II-B: *"The resulting record supports later analysis of correctness, fairness, and causality, each of which requires its own evidence."*
6. §VII: *"A graph can localize a represented change, but an unobserved tool state leaves no structural evidence of its consequence."*

## 14. Positioning for WorkTrace

**What they cover. We must not claim these as novel:**
- **The decision as the unit of analysis, replay and comparison.** Their "committed agentic decision" / decision trajectory is a decision-bounded subgraph with context (evidence, knowledge, policy), execution (agent, tool calls), authority (grant, actor, role, review) and outcome. This substantially overlaps our E = (context, information, permissions, …, action, consequences), except for the *declared grounds* part.
- **Replay under controlled, declared changes** in an isolated twin: typed single-dependency perturbations, material vs null interventions, a replay contract and tool replay modes.
- **The argument that the final output is insufficient**, with the same-label/different-mechanism example and an output-only baseline (B0).
- **Representing authority and permissions inside the decision record:** AuthorityGrant validity and applicability, recommendation vs commitment, required-review non-bypass, `delegates_to`.
- **A gate before releasing a revised mechanism**, based on a critical scenario suite and thresholds, plus independent governance approval.
- The phrase "class of decisions" appears ("S_t is the state relevant to one class of decisions"; "an authority grant can cover a bounded class of commitments"). We should not imply that we coined decision classes. We can claim **per-class autonomy calibration**.

**What they leave open, where WorkTrace adds something:**
- **Declared grounds vs behaviour.** They have no graph of the agent's *declared* grounds and no test of whether those reasons are faithful. Their perturbations test governance-path change, not whether the agent's sensitivity to evidence matches its stated reasons.
- **Redundancy and overdetermination.** Interventions are single-dependency, with no only-X / invert-X / add-second-source. Disjunctive requirement groups check coverage, not reliance.
- **Earning autonomy.** Authority is exogenous ("granted in advance"). Nothing decides per decision class, conditionally and revocably, what an agent may do autonomously from tested behaviour.
- **Evaluating a delegation rule.** They have no held-out generated-episode evaluation, risk–coverage curve against an outcome-only rule, or escalation cost.
- **Classic MAS delegation and adjustable-autonomy theory.** They do not cite it. Their only autonomy reference is the Agentic BPM manifesto ("bounded autonomy").
- **LLM-agent decisions.** Their evaluated decisions are mostly process-log carriers with overlays and injections, not LLM agents' reasoning.

**One-sentence differentiation:** DNative-Twin reconstructs and replays *how* a committed decision was produced and *whether its authority path was valid*, taking the agent's authority as given. WorkTrace instead uses redundancy-robust evidence interventions to test *whether the agent's declared grounds actually govern its behaviour*, and turns that tested behaviour into a per-decision-class, revocable delegation rule evaluated by risk–coverage against outcome-only delegation.

**Suggested citation framing:** "Pang et al. [DNative-Twin] make the committed decision the unit of replay and comparison, recording evidence, tool state and authority grants in a typed graph and replaying it under declared perturbations in an isolated twin. We build on this decision-centred view but address a question it leaves open: given such episodes, when should an agent be *granted* authority for a decision class? We answer it by testing whether its declared grounds survive evidence interventions."
