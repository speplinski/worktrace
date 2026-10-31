# Round 2: agent tracing and provenance systems closest to LEDGER

Works covered: (1) Graph of Trace (Gao et al., ACL 2026 Demos); (2) AgenTracer (arXiv:2509.03312); (3) Auditable Agents (arXiv:2604.05485); (4) Audit Trails for Accountability in LLMs (arXiv:2601.20727).

**Bottom line.** None of the four grants or revokes agent autonomy from tested behaviour towards evidence. None tests an agent's stated reasons by intervention. AgenTracer comes closest to our machinery. It intervenes on **agent actions** with LLM-generated oracle corrections or injected faults, replays the run, and labels the earliest step whose correction flips the **task outcome**. That makes it an outcome-flip, single-step-sufficiency design: it is outcome-based, and it is not built to cope with redundancy. Two narrower overlaps need care in our writing:
- Graph of Trace already records **agent-declared dependency lists** whose edges mean "logical research justification" rather than time order.
- The runtime layer in Auditable Agents (Aegis) already uses an **allow / block / pending-for-human** triad per tool call.

We must not present "recording declared grounds" or "a proceed/refuse/escalate triad" as new in themselves. The new part is testing those declared grounds by intervening on evidence, and deriving the triad per decision class from those tests.

**Reading status.** All four were read in full (main text, appendices, prompts and references). The figures in all four are images, and I read only their captions. Details are given per work below.

---

## 1. Graph of Trace (Gao et al., ACL 2026 System Demonstrations)

### Bibliographic data
- **Title (ACL Anthology / Crossref):** *Graph of Trace: Visualizing Execution Traces of Scientific Agents.*
- **arXiv title:** *Graph of Trace: Visualizing Execution Traces of Scientific Agent* (singular "Agent").
- **Authors:** Tianci Gao\*, Haoxuan Li\*, Jianhe Li, Tianxiang Zhao, Runze Shi, Weiran Wang, Zezhao Wu, Lu Mi† (\* equal contribution; † corresponding author). Affiliations: Shanghai Qi Zhi Institute, Tsinghua, Renmin, Beihang, Georgia Tech, Fudan.
  - Crossref metadata garbles two names, as "Jian He Li" and given/family "Shi Runze". The PDF reads "Jianhe Li" and "Runze Shi".
- **Venue:** Proceedings of the 64th Annual Meeting of the ACL (Volume 3: System Demonstrations), pp. 297–306, July 2–7, 2026.
  - DOI **10.18653/v1/2026.acl-demo.29**; Anthology ID 2026.acl-demo.29. **[verified: Crossref DOI record]**
  - Also on **arXiv:2606.15116v1** (13 Jun 2026, cs.HC). **[verified: arXiv API]**
- **Code/demo:** github.com/NeuroAIHub/Graph-of-Trace-Visualizing-Execution-Trace-of-Scientific-Agents
- **Read:** the full ACL PDF (10 pp.): §§1–8, Appendix A (Monitor prompt and MCP description excerpts) and Appendix B (questionnaire). Figs. 1–3 were read by caption only. A word-level diff against the arXiv v1 text shows only layout and header differences; I saw no substantive change.

### Problem and contribution
Scientific agents (OpenHands in their setup) run long research workflows, and scientists cannot follow or review the intermediate steps. The paper contributes:
1. "structured execution traces as an abstraction";
2. a four-module architecture: Scientific Agent → Monitor Agent → Parser & Structure → Frontend;
3. a three-panel React UI (chat, graph, node detail).

### Method
- **Unit of analysis:** the *atomic subtask*. "each node represents a single atomic subtask and contains structured metadata, including a textual description, references to artifacts, and identifiers of the parent nodes" (§3.4).
- **Node/edge vocabulary:**
  - There is one node type: a subtask with title, description, artifacts and parent ids.
  - There is one edge type: a dependency. "Directed edges capture dependencies between nodes, representing causal or logical progression rather than mere temporal order" (§3.4).
  - The Monitor prompt says: "Parents represent logical research justification, NOT chronological execution order" (App. A).
  - The Parser enforces a DAG. Parents must exist, and cycles and orphans are rejected. Storage is an append-only JSON ledger.
- **Provenance of the structure:** this is **self-report plus LLM interpretation**.
  - The Scientific Agent calls an MCP tool after each subtask. It supplies a title, a description and "a dependence list to describe those dependencies" (App. A).
  - The Monitor LLM converts these reports into nodes and chooses parents.
  - The MCP description explicitly excludes reasoning: "It is NOT for chain-of-thought, progress logs, explanations, or exploratory work" (App. A).
- **Are stated reasons tested?** No. The declared dependencies are *recorded* and rendered. They are checked only by experts, who judged whether nodes and edges were "correct" (Table 1). Nothing is perturbed.
- **Interventions or counterfactuals:** none. "Node-level backtracking" so that experts can intervene is listed as **future work** (§7).
- **Authority, permissions, delegation:** none. The human role is monitoring and review.

### Evaluation
- **Setup:** 5 domain experts (AI, neuroscience, biology) ran 7 replication case studies, with graphs of 5 to more than 20 nodes.
- **Fidelity:** overall node correctness 0.98 (101/103) and edge correctness 0.96 (120/125). Mean per-expert accuracy was 0.96 for nodes and 0.94 for edges.
- **Latency:** average 1.6 s, computed from interval midpoints.
- **Likert ratings (1–5):** interpretability 4.43, aesthetics 4.14, usability 4.29. The "baseline" is the same experts rating usability with raw logs only: 2.51.
- **Failure modes they report (§5):**
  - delayed MCP reporting;
  - missing parent links, e.g. environment setup not linked to experiments;
  - in long contexts, new branches wrongly attached to the last node, which makes parallel work look sequential.

### What it covers that WorkTrace must NOT claim
- Recording **agent-declared dependency lists** and storing them as a justification DAG ("logical research justification"), with edges distinct from temporal order.
- An append-only, schema-validated trace ledger and real-time graph visualisation for human review.

### What it leaves open that WorkTrace addresses
- The declared dependencies are never tested; a declared parent may play no causal role.
- Its own Limitations (§8) say it relies on "Agent Compliance" with the tracing protocol, and that the Monitor may "introduce hallucinated structure".
- There is no decision-level unit, no notion of the information available at decision time, no permissions, and no use of the trace to set autonomy.

### Draft differentiation sentence
> Graph of Trace renders agent-reported subtasks and their declared dependencies as a live DAG for expert review; WorkTrace treats declared grounds as hypotheses to be tested by intervening on the external evidence available at decision time, and uses the results to set per-decision-class autonomy.

### Citation cautions
- This is a demo paper. The "evaluation" is 5 experts and 7 cases, with no inter-rater agreement and no statistical test, yet the conclusion says it "significantly enhances" understanding.
- The baseline is a self-rated condition without randomisation or counterbalancing.
- Title differs between the arXiv and ACL versions: cite the ACL version.
- LEDGER calls it "closest to our setting". It is close to LEDGER, but far from WorkTrace.

---

## 2. AgenTracer (Zhang et al., 2025; ICLR 2026)

### Bibliographic data
- **Title:** *AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?*
- **Authors:** Guibin Zhang, Junhao Wang, Junjie Chen, Wangchunshu Zhou, Kun Wang, Shuicheng Yan. The PDF lists NUS, CUHK, OPPO and NTU and gives no per-author mapping.
- **arXiv:2509.03312**: v1 3 Sep 2025, v2 4 Sep 2025. **[verified: arXiv API]**
- **Venue:** OpenReview lists it as **ICLR 2026 Poster** (forum id l05DseqvuD). **[verified: OpenReview API search]**
- **Read:** the arXiv **v2** PDF in full (18 pp.): §§1–6, Algorithm 1, Tables 1–3 and Appendix B prompts (analyzer, attack). Figs. 1–4 were read by caption and surrounding text.
- **Not read:** the ICLR camera-ready. The OpenReview PDF download returned HTML, not a PDF. Numbers may differ in the camera-ready.

### Problem and contribution
The task is failure attribution in multi-agent LLM systems: identifying the failure-responsible agent *i\** and the decisive error step *t\**. The contributions are:
1. an automated annotation pipeline that uses **counterfactual replay** and **programmatic fault injection**, producing TracerTraj (≈2.5K annotated trajectories);
2. **AgenTracer-8B** (Qwen3-8B fine-tuned with GRPO and a "multi-granular" reward), which predicts ⟨agent, step⟩ from a failed log.

### Method
- **Unit of analysis:** a whole multi-agent **trajectory** τ = (s₀, a₀, …, s_T) under a turn-based protocol, where one agent µ(t) acts per step.
  - The output is a single ⟨agent, step⟩ pair.
- **Node/edge vocabulary:** none as a graph. The trace is a linear sequence of (state, action) pairs with an acting-agent label. The history H_t is "implementation-dependent".
- **Decisive error (§3):** "the earliest action in the trajectory whose correction is sufficient to steer the system from failure to success."
  - Formally, R(τ, t, a′_t) replaces a_t by an oracle action a′_t and "all subsequent steps are re-simulated". The decisive step t\* is the earliest t at which the outcome flips.
  - *Caution:* Eq. (4) as printed has the condition reversed ("Ω(τ)=1 ∧ Ω(R(·))=0"). Algorithm 1 implements the intended direction: the run failed, and the corrected run succeeds.
- **Counterfactual replay, in practice (§4.1, Alg. 1, lines 2–8):**
  - An analyzer agent (DeepSeek-R1) receives the trajectory, environment feedback F, and **the ground-truth solution G**. It proposes "a minimally invasive, corrected action a′_t … without revealing the complete solution".
  - The steps are tried in order t = 0…T, and the first t whose replay succeeds is labelled.
- **Fault injection (Alg. 1, lines 9–17):**
  - On *successful* runs, sample K steps and corrupt the action, ã_t = Π(a_t), using a DeepSeek-R1 "attack expert" prompt that asks for "SPECIFIC, IMPLEMENTABLE" code changes.
  - Replay; if the run now fails, ⟨µ(t), t⟩ is the label by construction. Stop after the first successful injection.
- **What is intervened on:** **the agent's own action at one step**, not the external evidence. In a multi-agent run, an upstream corrupted action *does* change what downstream agents see. Figure 4's case study is exactly that: a Web Surfer fetched a stale file. But the measured quantity is the **system outcome Ω ∈ {0, 1}**, not whether any downstream decision tracked that information.
- **Are stated reasons tested?** No.
  - The tracer *produces* reasons inside ⟨think⟩. These are used as feedback text, not checked.
  - The analyzer's JSON contains a "reason" field. It is not tested either.
- **Authority, permissions, delegation:** none. "Responsibility" means which agent acted at the decisive step, and µ(t) is a scheduler, not an authority relation.
- **Use of the output:**
  - accuracy of attribution;
  - injecting the tracer's ⟨think⟩ text as feedback into the next attempt ("self-correcting and self-evolving agentic AI").
  - **There is no gating or autonomy decision.**

### Evaluation
- **Data:**
  - TracerTraj comes from 6 MAS frameworks: MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow and OWL-Workforce.
  - It covers coding (MBPP+, KodCode, Blackjack), math (MATH, GSM8K) and agentic tasks (GAIA, HotpotQA).
  - Annotated counts are 1288, 630 and 558, which sum to 2476. A 9:1 test split gives test sets of 147, 63 and 56.
  - The external benchmark is **Who&When** (Zhang et al. 2025, arXiv:2505.00212 **[verified arXiv]**), with hand-crafted and automated subsets.
- **Metrics:** agent-level and step-level accuracy, with and without G.
- **Who&When hand-crafted (Table 1):**
  - AgenTracer-8B: agent 69.10/63.82, step 20.68/20.68 (w/ G / w/o G).
  - Best baselines: Claude-4-Sonnet 56.90/50.00 (agent) and 17.24/18.97 (step); DeepSeek-R1 56.90/53.44.
- **Who&When automated:** AgenTracer agent 69.62/63.73, step 42.86/37.30.
- **TracerTraj step-level (w/ G):** Code 18.85, Math 57.63, Agentic 36.17.
  - On Agentic agent-level, Claude-4-Sonnet w/ G (55.20) **beats** AgenTracer (53.28).
- **Downstream improvement (Fig. 3):** gains of +4.8% (OWL on GAIA) to +14.21% (MaAS on MATH-500) over 3 feedback rounds, compared with Self-Refine and CRITIC (both using GPT-4.1).
- **What we learn:** step-level attribution from logs stays low (≈20% on hand-crafted Who&When even for the best model). Reading blame off a trace is hard, and this supports WorkTrace's choice to *test* by intervention rather than *infer* from logs.

### What it covers that WorkTrace must NOT claim
- **Counterfactual replay on agent trajectories as a labelling device**, i.e. replace a step, re-simulate, observe the outcome. It is also the source of the decisive-error formalism, inherited from Who&When.
- **Programmatic fault injection into successful runs to get labels by construction.** This is close to our "generated episodes with known ground truth".
- Training a small attributor on synthetic interventional labels.

### What it leaves open that WorkTrace addresses
1. **Target of intervention.** AgenTracer intervenes on actions. WorkTrace intervenes on *external evidence* at a fixed decision point (remove X / only X / invert X / add an independent second source) and holds the agent fixed.
2. **Measured quantity.** AgenTracer measures outcome flips. WorkTrace measures whether the *decision* responds to evidence as its declared grounds say it should.
   - AgenTracer is outcome-only by design, which is the very comparator our delegation rule is evaluated against.
3. **Redundancy.** The decisive-error definition is single-step sufficiency ("earliest action whose correction is sufficient").
   - If a failure is over-determined (two independent errors, each sufficient), no single correction flips the outcome. The trajectory then gets no label, and Alg. 1 just exits the loop without recording anything.
   - Likewise, an injection that does not flip the outcome is discarded. So the dataset is **selected for non-redundant causal structure**. This is exactly the case our redundancy-robust interventions are designed for.
4. **Oracle dependence.** The counterfactual a′_t is generated by an LLM that sees the ground truth G. It is not a controlled manipulation, and the replay is stochastic. The paper reports **no repeated replays** and no variance, so a flip can be noise. WorkTrace should state its replay count and its stochasticity controls explicitly.
5. **No delegation.** The output is blame and feedback. Nothing decides what the agent may do next without supervision.

### Draft differentiation sentence
> AgenTracer uses counterfactual replay of agent actions with oracle corrections and fault injection to localise the earliest outcome-flipping step for failure attribution; WorkTrace instead holds the agent fixed, intervenes on the external evidence available at a decision with redundancy-robust designs, measures whether the decision tracks that evidence as its declared grounds claim, and turns the result into a per-decision-class proceed/escalate/refuse rule rather than a blame label.

### Citation cautions
- Cite as ICLR 2026, with arXiv:2509.03312.
- Several errors in v2:
  - Eq. (4) has the outcome condition reversed.
  - "Detailed statistics … are placed in ??" (broken reference).
  - "Observation ❶" is used twice.
  - The dataset is described both as "over 2,000" and as "2.5K".
- **I could not reproduce the abstract's "up to 18.18%" margin over Gemini-2.5-Pro from Table 1.** The agent-level gap on hand-crafted w/ G is 17.38 points. Do not quote 18.18% without checking the camera-ready.
- G helps baselines inconsistently, and the authors acknowledge this.

---

## 3. Auditable Agents (Nian et al., 2026)

### Bibliographic data
- **Title:** *Auditable Agents.*
- **Authors:** Yi Nian\*, Aojie Yuan\*, Haiyue Zhang\*, Jiate Li\*, Li Li, Xiyang Hu, Hua Wei, Xiongye Xiao, Chaowei Xiao, Yue Zhao (\* equal contribution). Affiliations: USC, Arizona State, U. Tennessee Knoxville, Johns Hopkins.
- **arXiv:2604.05485v4** (v1 7 Apr 2026; v4 dated 27 Sep 2026, cs.AI). **[verified: arXiv API]**
- **Venue:** the arXiv comment says "A condensed 5-page version was accepted to ACM AI Summit 2026 (Visionary Papers track)". The PDF footnote says "Proceedings of the ACM AI Leadership Summit 2026".
  - The condensed version and its DOI are **[unverified]**; I did not find or read it.
  - Cite the arXiv extended version.
- **Read:** v4 PDF in full (25 pp.): §§1–6, Limitations, Conclusion, references, and Appendices A–C. Figures read by caption and in-text description.

### Problem and contribution
This is a **position paper**: "no agent system can be accountable without auditability." It separates three levels:
- **accountability** (the goal);
- **auditability** (the system property);
- **auditing** (the process).

It defines five dimensions, three mechanism classes, "layered evidence", an **Auditability Card**, and six open problems.

### Method
- **Unit of analysis:** the **audit verdict** V = (s, c, ν, r, σ) for a *policy-relevant action*:
  - s: the action;
  - c: its execution context;
  - ν ∈ {comply, violate} under a stated policy π, or ⊥ if undecidable;
  - r: the responsibility chain;
  - σ: the integrity guarantee (Eq. 1).
- **Formal model (App. B):**
  - An execution is X = (A, S, ψ, ρ), with steps sᵢ = (type, in, out, t, ctx). ψ maps steps to lifecycle phases, and ρ maps each step to its responsibility chain.
  - A record is L = (R, σ), where entries are partial observations of steps.
- **Five dimensions and metrics:**
  - Action Recoverability: ACR (coverage) and RF (record fidelity).
  - Lifecycle Coverage: LPC and GB (gap burden).
  - Policy Checkability: SPDR (share of decidable policies) and ADL (detection latency).
  - Responsibility Attribution: AC (chain completeness) and ACD (chain depth).
  - Evidence Integrity: IS (an ordinal scale: none / append-only / hash-chained / signed) and VC (verification cost).
- **Definition 2:** auditability is a threshold predicate on the existence metrics.
- **Proposition 1:** if a field a policy needs is missing from every relevant record entry, then π(L) = ⊥. The authors call this "not a deep result".
- **Node/edge vocabulary:**
  - Records are events, not a graph. Responsibility is a chain user → agent → skill → tool → service.
  - It "generalizes from chain recovery to subgraph recovery" over an interaction topology G = (A, E), where an edge means "component a_u's output influenced component a_v's action" (App. B.5).
  - It explicitly notes: "A trace records what each step did, but not what it relied on, so the dependency structure of a run has to be inferred rather than read off the record" (§2.2, citing GRADE, Zhao 2026).
- **Are stated reasons tested?** No. Rationale is not a field.
  - Only **structural** policies are considered, e.g. "tool X requires prior user approval".
  - Semantic policies are open problem OP4.
- **Interventions or counterfactuals:** none on agent behaviour. The "recover" class (IET) is watermark-style attribution, not counterfactual.
- **Authority, permissions, delegation:** this is where the paper is strongest.
  - Delegation events count as policy-relevant actions, and approvals and retries count as lifecycle phases.
  - It distinguishes "authenticated delegation addresses who is permitted to act" (South et al., ICML 2025) from "tracing who actually caused a given outcome" (§2.4).
  - It cites Li & Zhao: "agentic harm lies in the gap between the authority an action exercises and the authority the user granted" (§5).
  - The **enforce** mechanism (their Aegis firewall) gives each tool call one of "**allow, block, or pending (escalated to a human reviewer)**" (§4.2), based on content risk scanning plus configured policies.

### Evaluation (all from the authors' own tools, which they acknowledge in Limitations)
- **Detect:** an agent-audit v0.15.1 scan of 6 open-source agent projects found 617 security findings: 269 critical, 134 in the highest confidence tier, and 64% tool misuse.
- **Enforce (Aegis):**
  - 48/48 curated attacks blocked;
  - 1.2% false positives on 500 benign calls;
  - 8.3 ms median overhead (P95 14.7 ms, P99 23.1 ms);
  - Ed25519-signed, hash-chained records.
- **Recover (IET):** on 4–6-agent chain, star and tree setups:
  - token attribution 0.818–0.867;
  - IoU 0.814–0.843;
  - EdgeSim 0.912–0.949;
  - under identity removal 21.51–24.45%, against baselines at 0–4.17%.
- **Not done:** an end-to-end audit ("No end-to-end audit", Limitations). Thresholds θ are not calibrated.

### What it covers that WorkTrace must NOT claim
- The accountability / auditability / auditing distinction, and a five-dimension, metricised notion of record sufficiency.
- The idea that a missing field makes a policy undecidable.
- The **allow / block / pending-to-human** runtime triad, i.e. a per-call proceed/refuse/escalate gate. We must cite it.
- The authority-gap framing (via Li & Zhao 2026, arXiv:2606.28739).
- The Auditability-Card reporting idea.

### What it leaves open that WorkTrace addresses
- The gate's inputs are **static policy plus content scanning of the call's arguments**. It does not use any record of the agent's past behaviour, any test of how the agent handles evidence, or any per-class history. Its auditability thresholds apply to the *record*, not the *agent*.
- There is no information-at-decision-time slot and no declared-grounds slot in V. Compliance is decided against a policy, not against the evidence.
- **Earned and revocable autonomy is not discussed.** The six open problems do not include it.
- OP4 (semantic decidability) and OP3 (full-chain attribution) are adjacent to, but not the same as, our question.

### Draft differentiation sentence
> Auditable Agents specifies when an agent's record suffices to decide policy compliance and assign responsibility, and demonstrates a per-call allow/block/escalate gate driven by static policies; WorkTrace asks a different question — whether the agent's decisions in a class respond correctly to evidence — and derives a revocable per-class proceed/escalate/refuse rule from intervention tests rather than from policy rules on single calls.

### Citation cautions
- This is a position paper. The evidence is heterogeneous and comes entirely from the authors' own tools (agent-audit, Aegis, IET). Security findings are used as a *proxy* for auditability.
- The "Aegis" here (Yuan et al., arXiv:2603.12621, pre-execution firewall) **[verified arXiv]** is a different system from "Aegis" (Kong et al., arXiv:2509.14295, error generation and attribution) listed in our survey note. Do not conflate them.
- Its Table 4 positions Ojewale et al. (Audit Trails). It is useful for related work, but the cell-level ratings are the authors' own judgement.

---

## 4. Audit Trails for Accountability in Large Language Models (Ojewale, Suresh, Venkatasubramanian, 2026)

### Bibliographic data
- **Title:** *Audit Trails for Accountability in Large Language Models.*
- **Authors:** Victor Ojewale, Harini Suresh, Suresh Venkatasubramanian (Brown University).
- **arXiv:2601.20727v1** (28 Jan 2026, cs.CY). **[verified: arXiv API]** Only v1 exists.
- **Venue:** none. The PDF footer says "Manuscript submitted to ACM", and a Crossref search found no published version. Treat it as a **preprint**.
- **Read:** the full PDF (§§1–9, references, Appendix A). Figs. 2–4 are code screenshots and were not read; Fig. 1 (architecture) was read via its text labels.
- **Code:** github.com/victorojewale/audit-trail-PoC

### Problem and contribution
Organisations often cannot reconstruct which model version was live, which data shaped it, or who approved a change. The proposal is an **LLM audit trail**: "a chronological, tamper-evident, context-rich ledger of lifecycle events and decisions that links technical provenance … with governance records (approvals, waivers, and attestations)". The contributions are:
1. a lifecycle framework covering pretraining, base model selection, adaptation/evaluation/release, deployment, and monitoring/incident response;
2. a Capture / Store / Use reference architecture;
3. the `llm-audit-trail` Python proof of concept.

### Method
- **Unit of analysis:** a **lifecycle event** of the *model or system*, not an agent decision. Examples are FineTuneStart, EpochEnd, Evaluation, DeploymentCompleted, RolloutChanged, ServingConfigChanged, InferenceRequestMetadata, GuardrailTriggered, DriftDetected and IncidentOpened.
- **Governance events:**
  - Approval, RiskWaiver and Attestation are human-authored, via a CLI.
  - Each carries the decision owner, rationale or statement, scoped identifiers, constraints (e.g. jurisdictions, user groups) and references.
- **Vocabulary:**
  - Core schema: {event_id, timestamp, system, actor, event_type, model_id, dataset_id, deployment_id, details, prev_hash, curr_hash, sig?} (§5.4).
  - Links are by shared identifiers and the hash chain. **There is no causal or dependency edge.**
- **Are stated reasons tested?** No. Human *rationales* for approvals are recorded verbatim and never checked. The authors are explicit: "Audit trails provide chronological and structural traceability but not causal explanation. They verify that events occurred in a verifiable sequence without showing that one directly caused another" (§8, "Epistemic limits").
- **Interventions:** none.
- **Authority, permissions, delegation:** recorded *about humans and organisations*:
  - who authorised deployment, and for what scope;
  - rollout scope expansions, as "conditional approvals tied to user groups or geographies";
  - who holds modify and rollback authority;
  - cross-organisation signed pointers.
  - Sector profiles can require "an Approval event in scope before any DeploymentCompleted event" (§5.4).
  - In the bank scenario, "human loan officers retain formal authority over lending decisions."
  - The *agent's* own autonomy is not modelled.

### Evaluation
None beyond the proof of concept. The paper revisits its two scenarios (bank chatbot, clinical note assistant) qualitatively. There are no user studies, no overhead numbers and no data.

### What it covers that WorkTrace must NOT claim
- Tamper-evident, hash-chained logging of **governance decisions** (approvals, waivers, scope constraints) next to technical telemetry. Recording *who authorised what scope* is not new.
- Staged and conditional rollout scope as a recorded governance object. This is the organisational analogue of "bounded autonomy", but it is decided by humans.

### What it leaves open that WorkTrace addresses
- The analysis covers the model lifecycle, not runtime agent decisions. This is the same critique made in Auditable Agents §5.
- By its own statement there is no causal claim, and nothing tests whether the system's behaviour depends on its evidence.
- Scope decisions are human inputs that the trail *records*. WorkTrace *computes* a scope recommendation (per decision class) from tested behaviour. The decision itself could be logged as an Approval/RiskWaiver-style event.

### Draft differentiation sentence
> LLM audit trails make lifecycle provenance and human governance decisions (approvals, waivers, scope conditions) reconstructible and tamper-evident but explicitly disclaim causal explanation; WorkTrace supplies the missing causal test at the level of individual agent decisions and produces the evidence on which such scope approvals could be granted or withdrawn.

### Citation cautions
- This is an unreviewed preprint with a proof of concept only. The headline claim, that audit trails "transform accountability from an aspirational goal into a continuous, operational capability", is not evaluated.

---

## Answers to the key questions

**(a) Does any of these do counterfactual replay on EVIDENCE in a way close to our interventions?**

Only AgenTracer does counterfactual replay at all, and it is **not on evidence**. It replaces or corrupts an agent's **action** at one step, using an LLM that sees the ground truth, re-runs the rest, and records whether the **task outcome** flips. The earliest flipping step is the label.

Its overlap with us is real at the level of machinery: replay, injection, and labels known by construction. It differs on four points:
1. the intervention target (action vs. external evidence, with the agent held fixed);
2. the response variable (outcome vs. decision–evidence dependence);
3. redundancy (single-step sufficiency, which silently drops over-determined cases, vs. our remove / only / invert / add-second-source designs);
4. purpose (blame and feedback vs. delegation).

Indirectly, its upstream fault injection *does* change the information later agents receive. A reviewer could say "AgenTracer already perturbs what downstream agents see", so we should pre-empt that point.

**(b) Does any use trace analysis to decide what the agent may do autonomously?**

No.
- **Auditable Agents / Aegis** is the nearest. It makes a per-call allow / block / pending-to-human decision from static policy and content risk scanning, with no learning from tested behaviour and no per-class or revocable scope.
- **Audit Trails** records human scope and rollout approvals but does not derive them.
- **AgenTracer** feeds diagnoses back for self-improvement.
- **Graph of Trace** supports human monitoring and leaves intervention as future work.

**(c) Differentiation:** see the draft sentence under each work. In one line: these works *record* (Graph of Trace, Audit Trails), *specify record sufficiency* (Auditable Agents), or *blame by outcome* (AgenTracer). WorkTrace *tests decision–evidence dependence and grants scope from the result*.

---

## Implications for WorkTrace

1. **Do not claim novelty for:**
   - counterfactual replay or fault injection in agent traces (cite AgenTracer and Who&When);
   - recording agent-declared dependencies or justification edges (cite Graph of Trace; LEDGER's edges are tracer-inferred);
   - a proceed/refuse/escalate-style gate (cite Aegis, via Auditable Agents §4.2 and arXiv:2603.12621);
   - tamper-evident logging of authority and approval decisions (cite Audit Trails, Auditable Agents).
2. **Claim precisely:**
   - interventions on **external evidence at a fixed decision point, with the agent held fixed**;
   - a response variable defined on **the decision relative to declared grounds**, not on outcome;
   - **redundancy-robust** intervention designs;
   - **per-class, revocable** gating evaluated with risk–coverage and escalation cost against an **outcome-only rule**. AgenTracer is the natural exemplar of an outcome-only attribution, so we can name it as the type of baseline we beat.
3. **Design changes suggested:**
   - **Report replay stochasticity.** Use multiple samples per intervention, plus a flip-rate threshold. AgenTracer reports neither, which is a weakness we can avoid visibly.
   - **Report dropped or unlabelled cases.** AgenTracer silently drops non-flipping cases. We should report how many episodes are over-determined and how our redundancy designs label them.
   - **Avoid ground-truth leakage into interventions.** AgenTracer's oracle sees G. Our evidence manipulations should be specified without access to the right answer, or the leakage should be stated.
   - Consider emitting each grant or revocation as an **Approval/RiskWaiver-style event** (Audit Trails schema). Our episode records could then satisfy Auditable Agents' five dimensions; at minimum we can fill in an Auditability Card in an appendix. This is cheap and connects us to the accountability literature.
   - Our episode E maps partly onto Auditable Agents' V = (s, c, ν, r, σ):
     - action and context map directly;
     - permissions correspond to the policy and authority chain;
     - the **information-at-decision-time** and **declared-grounds** slots have no counterpart there.
     
     A small mapping table in the paper would make the contribution legible to that community.
4. **New leads, not yet read in full** (abstract only, via arXiv API; all **[verified arXiv]**). They should be read in the next round:
   - **GRADE: Graph Representation of LLM Agent Dependency and Execution** (Yue Zhao, arXiv:2606.22741, v3).
     - Dependency edges are "graded as observed in the trace, declared by added logging, or inferred under an assumption, a schema we test one grade at a time".
     - It uses degree-matched "counterfeit" dependency controls and finds that inferred structure can "restate run size".
     - **This is potentially the closest threat to our declared-grounds graph and to our methodology**, and it is cited by Auditable Agents §2.2.
   - **CatchBench: When Can an Agent Failure Be Caught?** (Zhao et al., arXiv:2608.22808, v4). It covers PRE / LIVE / POST information states for auditing, with 1187 configurations and 1162 runs. It is relevant to our "information available at decision time" framing and to our evaluation hygiene (label-shortcut tests).
   - **Agent Safety Is Action Alignment** (Shawn Li, Yue Zhao, arXiv:2606.28739). Harm is located in "the relation between the authority an action exercises and the authority the user granted", and safety is framed as least privilege enforced outside the model. It is relevant to the permissions slot of E and to the delegation framing.
5. **Risks:**
   - A reviewer from the failure-attribution community may read WorkTrace as "AgenTracer with different perturbations". The four-point distinction in (a) should appear explicitly in related work, ideally with a worked example of an over-determined episode that AgenTracer cannot label and our designs can.
   - A reviewer from the governance community may read the delegation rule as "Aegis with a learned policy". We need to stress that the rule is per decision class, is derived from evidence-handling tests (not content risk), is revocable, and comes with an explicit escalation cost.
