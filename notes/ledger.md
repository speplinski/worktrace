# LEDGER — Claim-to-Evidence Trace Graphs for Auditing LLM Agents (reading note)

**What I read:** the whole paper, v1. Sources: arXiv HTML (https://arxiv.org/html/2608.18398), which redirects to v1 and was fetched 2026-10-25, plus the PDF (https://arxiv.org/pdf/2608.18398), used only to get page numbers. That covers the abstract, §§1–6, the acknowledgments, all 26 references, Appendix A (both prompts) and Appendix B. **Not read:** the figures (Figs. 1–8) are images. I read only their captions, so I did not inspect the node and edge layouts inside the full trace graphs in Appendix B (Figs. 7–8).
Page numbers below refer to the arXiv PDF v1 (15 pages including references and appendices).

---

## 1. Bibliographic data

- **Title:** *LEDGER: Claim-to-Evidence Trace Graphs for Auditing LLM Agents*
- **Acronym (expanded in the paper):** LEDGER = "Layered Evidence and Decision Graphs for Execution Review"
- **Authors and affiliations:**
  - Daehong Kim, Carnegie Mellon University, Pittsburgh, PA (daehongk@andrew.cmu.edu)
  - Haichao Miao, Lawrence Livermore National Laboratory, Livermore, CA (miao1@llnl.gov)
  - Shusen Liu, Lawrence Livermore National Laboratory, Livermore, CA (liu42@llnl.gov). Shusen Liu is the submitter on arXiv.
- **arXiv:** 2608.18398**v1**, submitted Wed 19 Aug 2026 00:10:04 UTC. This is the only version. Primary category cs.HC, cross-listed to cs.AI. DOI 10.48550/arXiv.2608.18398. License CC BY 4.0.
- **Venue:** none stated. The first-page footer reads "Preprint." The heading "Acknowledgments and Disclosure of Funding" looks like the NeurIPS LaTeX style, but that is *my inference*; the paper does not say this. It carries the LLNL release number "LLNL-CONF-2022801", and the "CONF" suggests the authors intend a conference or workshop submission (*uncertain*). Funding: U.S. DOE, LLNL Contract DE-AC52-07NA27344, DOE ECRP 51917/SCW1885.
- **Suggested BibTeX:**
  ```bibtex
  @misc{kim2026ledger,
    title  = {{LEDGER}: Claim-to-Evidence Trace Graphs for Auditing {LLM} Agents},
    author = {Kim, Daehong and Miao, Haichao and Liu, Shusen},
    year   = {2026},
    eprint = {2608.18398}, archivePrefix = {arXiv}, primaryClass = {cs.HC},
    note   = {v1, 19 Aug 2026}
  }
  ```

## 2. Problem and motivation (as the authors frame it)

- LLM agents now run long technical workflows with planning, tool calls, code execution, file edits and generated artifacts. "As agents do more work faster, the productivity bottleneck shifts from producing outputs to auditing whether those outputs are correct and trustworthy" (Abstract).
- To accept a result, the user must know "which inputs were inspected, which hypotheses or implementation choices were explored, which files were changed, which artifacts were produced, which checks were run, and which pieces of evidence support the final claim" (§1, p.1).
- Observability tools such as LangSmith make event-level records visible. However, "Visibility, however, is not the same as auditability" (§1, p.2). Human review is described as *evidence-centered*: start from a claim, then ask what supports it, which artifact holds the evidence, which action produced it, and which check validated it. Rebuilding this from a flat log is manual work, and its cost grows with session length.
- The paper's framing is therefore **human review support (HCI/visualization)**. It is not about evaluation scores, safety monitoring or governance.

## 3. Core contributions (their words)

The paper lists two contributions (§1, p.2):

1. **"A claim-to-evidence trace graph construction method.** We introduce a sidecar tracer that runs alongside an unmodified interactive agent session, parses captured messages, tool calls, outputs, file interactions, and artifacts into Trace Records, and organizes them into a layered semantic trace graph. Artifact nodes represent inspectable evidence objects, while typed edges connect claims to supporting work and validation steps."
2. **"An interface for evidence-centered agent review.** The interface exposes Workflow Nodes, Evidence Nodes, Trace Records, graph updates, artifacts, and tracer-agent call records in one dashboard. This lets reviewers move between graph-level audit paths and the source records behind them, including the records used to construct the graph itself."

Positioning claim: "LEDGER does not replace observability; it builds on observed records and reorganizes them around audit needs" (§1, p.2). They call it "the review layer above" provenance and observability capture (§2.1, p.2).

## 4. Representation

**Unit of analysis.** One **observed agent session** (a Codex session, possibly with several turns). The graph is built per session. No smaller unit such as a decision or choice point is defined. A "claim" is a Workflow-Node category, not a separate formal object.

**Three layers (§3.2, p.4), plus artifacts and edges:**

| Layer | What it is | How it is built |
|---|---|---|
| **Trace Records** | "preserved observations of what happened during the session" (§3.1, p.3): message content, tool calls and results, lifecycle boundaries, artifact references, timing, links back to the transcript | **Deterministic** transcript parsing |
| **Evidence Nodes** | "concrete, inspectable work units" that group Trace Records (e.g., a tool-call request and its result that share a group id) | **LLM "tracer agent"** |
| **Workflow Nodes** | groups of Evidence Nodes into "workflow phases" | **LLM "tracer agent"** |

**Evidence-node types and action categories (Table 1, p.5), exactly as listed:**

| Type | Category | Definition |
|---|---|---|
| action | `control` | Session, turn, or task lifecycle record. |
| action | `user_message` | User request, correction, approval, or clarification. |
| action | `assistant_message` | Assistant plan, update, reasoning note, or answer. |
| action | `tool_call` | One tool invocation and its result, grouped by a shared id. |
| artifact | n/a | Inspectable object used, produced, or referenced by the agent. |

**Workflow-node categories (Table 2, p.5), exactly as listed:**

| Category | Definition |
|---|---|
| `context` | Frames the task, user goal, constraints, or session setting. |
| `plan` | Records the approach, scope, procedure, or tradeoff before work. |
| `inspect` | Gathers evidence by reading, searching, listing, previewing, or probing. |
| `execute` | Performs task-directed work such as editing, computation, analysis, or generation. |
| `validate` | Checks correctness or readiness through tests, builds, screenshots, or review. |
| `claim` | Records a final answer, explicit finding, status handoff, or user-facing conclusion. |

**Edge types (Table 3, p.6), exactly as listed.** "Edges are directed in trace order, and each type names the semantic relation that makes the source and target relevant to each other."

| Type | Relation definition |
|---|---|
| `frames` | The source requirement, constraint, or plan sets context for the target. |
| `uses` | A work unit uses an artifact or resource as input. |
| `produces` | A work unit creates or changes an artifact, output, or state. |
| `informs` | The source evidence or result shapes the target analysis, plan, or action. |
| `checked_by` | The source change or result is checked by the target validation step. |
| `supports` | The source evidence or finding justifies the target claim or committed choice. |

Edges exist at two levels:
- Evidence-layer edges connect action and artifact Evidence Nodes, e.g., a command uses a file, a command produces output, a test checks a changed file.
- Workflow-level edges hold when one phase "frames, informs, checks, or supports another phase or claim".

There are also **cross-layer edges** that link each Workflow Node back to its Evidence Nodes and Trace Records. "Edges follow trace order, but they are added only when there is a semantic relation" (§3.3, p.6).

**How claims link to evidence.** A claim is a Workflow Node of category `claim`. It reaches evidence through `supports` (and `checked_by`) edges to artifact and action Evidence Nodes, and from there through cross-layer pointers to raw Trace Records. Artifact nodes act as "evidence anchors". Under hook tracing, "artifact nodes are recovered from tool-call Trace Records and their results. The command, its arguments, and its output carry the file path and the kind of interaction, and the tracer reads them from that text" (§3.3, p.6).

**Schema details.** No formal schema, JSON spec or grammar is given. Node attributes appear only in the UI description: "category, status, description, evidence links, Trace Record links, and related artifacts" (§4, p.6). Edges have no weights, confidence or uncertainty scores. The paper lists uncertainty encoding as future work.

## 5. Method / system: capture, and declared vs observed

- **Sidecar tracer** next to an *unmodified* interactive agent. The prototype targets **OpenAI Codex**, through lifecycle hooks plus transcript reconstruction. They say the approach generalizes to "Any coding agent … if it exposes similar hooks, session transcripts and records" (§3.1, p.3).
- **Hooks recorded:** `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`. Each hook appends its JSON payload to a hook-event log and refreshes a per-session transcript dump. The dump is a "live snapshot" during a turn and becomes the "final snapshot" after `Stop`. The copied transcript is "the source of truth for complete reconstruction because hooks may not intercept every tool pathway or every non-shell event" (§3.1, p.3).
- **Two evidence levels are preserved:**
  1. the Codex transcript JSONL, copied unchanged;
  2. `trace.json`, which normalizes the rows into record families: session/turn context, visible messages, tool calls and results, lifecycle events, reasoning summaries when present, parse errors, and **coverage records**. Coverage records "make missing or unfamiliar transcript rows explicit rather than silently dropping them" (§3.1, p.4).
- Everything is stored per session (hook payloads, transcript, trace summary), and graph elements keep source pointers so the graph can be rebuilt post hoc.

**Is model-declared content separated from environment-observed content?** Partly, but along a different axis.
- **What they separate explicitly** is *captured* (deterministic Trace Records) versus *inferred* (the Evidence and Workflow structure built by an LLM tracer agent): "This separation matters because reviewers need to distinguish evidence that was captured from structure that was inferred during graph construction" (§3.1, p.3). And: "The Trace Records therefore stand on their own, while the structure built over them is an interpretation" (§3.2, p.4).
- **Agent-declared versus environment-observed:** this is only *implicit*, through the action categories. `assistant_message` covers the agent's "plan, update, reasoning note, or answer", while `tool_call` and artifact nodes carry tool results and files. The paper does **not** treat the agent's declared reasons or grounds as a separate object to be checked against observed evidence. The `supports` edges are inferred **by the tracer LLM**, not declared by the working agent. LEDGER therefore has no "declared grounds" layer; the evidential relations are the tracer's interpretation.
- In its contrast with Graph of Trace, the paper stresses that LEDGER "reads records emitted by an unmodified interactive session rather than relying on the working agent to self-report" (§2.3, p.3).
- **The tracer model is not specified.** The paper says "tracer agent" and "model-call records" but never names the model or its prompt (*not stated*). The working agent in the case studies is "Codex using GPT-5.5" (§5, p.7).
- **Trace-construction audit:** the UI also shows graph updates, tracer events, model-call records and trace errors. This lets the reviewer "distinguish an agent error from a tracing error" (§4, p.6).

## 6. Evaluation

- **Type:** two **qualitative case studies** (demonstrations). Each is one session, as far as the text says. Both ran "in Codex using GPT-5.5 with live tracing enabled, then reviewed through the dashboard" (§5, p.7). The text does not say who did the review; it appears to be the authors (*inference*).
  1. **Tabular data analysis.** UCI hourly air-quality CSV (`data/airqualityuci.csv`). Tasks: clean the data (timestamps, numeric conversion, the documented missing-value convention), compute hourly means, find the peak hour per pollutant, and write a report, a missingness table, an hourly table and a plot (prompt in App. A.1). Observations:
     - the plan came after file inspection;
     - the first script failed on an unavailable optional dependency (a Markdown-table call), followed by patches, a rerun and validation;
     - the final claim linked back to the report, tables and plot.
  2. **Feature addition in NetworkX.** Add an ordered-waypoint shortest-path utility (prompt in App. A.2). Observations:
     - the first implementation passed its tests;
     - the agent then checked how existing functions handle missing nodes, followed by a guard patch, a regression test and a second test run;
     - the trace separates "which behavior came from the design and which came from an edge case the agent raised after the fact" (§5.2, p.9);
     - "the trace records which check covered which behavior. A reviewer can therefore read the extent of the support behind the claim rather than only that support exists" (§5.2, p.9–10).
- **Number of cases:** 2 sessions.
- **Metrics:** **none.**
- **Baselines:** **none.** Raw transcripts and LangSmith are discussed conceptually but not compared.
- **Quantitative results:** **none.** There is no user study, no inter-run stability measure and no graph-accuracy measure. Repeated-run stability is listed as future work (§6, p.10).

## 7. Intervention / perturbation / counterfactual testing of evidence?

**No.** The paper has no evidence ablation, removal, inversion, injection or counterfactual replay, and no test of whether a claim *depends* on the evidence linked to it. `supports` edges are asserted by the tracer from the trace and never tested causally. The only perturbation-like idea is future work on **reconstruction stability**: "Repeated-run studies should also measure whether the same session produces stable nodes, edges, and claim-support paths under reconstruction" (§6, p.10). That tests the stability of the *tracer*, not the agent's sensitivity to evidence.

## 8. Authority, permissions, delegation, autonomy scope, escalation?

**Essentially absent.** The paper never discusses delegation, autonomy levels, scoping what an agent may do, escalation policy, or turning audit results into permissions. The words "delegat-", "escalat-" and "authori-" do not occur. "Autonom-" appears only in the titles of references [1] and [2]. The only touch points are:
- Capture includes the Codex `PermissionRequest` hook: "the hook configuration records SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest, and Stop events" (§3.1, p.3). Permission requests are captured as records, but the graph has no permission node or edge type and they play no further part in the analysis.
- The `user_message` category includes "approval": "User request, correction, approval, or clarification." (Table 1, p.5).
- The broadest framing is that productive use "depends not only on generation speed, but also on the user's ability to audit the recorded work" (§1, p.1). Audit serves *accepting outputs*, not *granting autonomy*.

## 9. Redundancy / overdetermination (several sources supporting the same claim)?

**Not addressed as a concept.** The graph can contain several `supports` edges into one claim. In Case 2, "The final claim traversed back to this evidence through its supports edges, which reached the changed files, the documentation update, the focused test run, the import check, and the final diff review" (§5.2, p.10). But LEDGER does not:
- separate necessary from sufficient support;
- detect redundant or overdetermined support;
- weigh sources.

The closest idea is **coverage**: which check covered which behaviour, and "the extent of the support behind the claim rather than only that support exists" (§5.2, p.10). In Discussion they ask for future graphs to "encode uncertainty or missing support directly in the graph" and to "emphasize unsupported claims and unchecked artifacts" (§6, p.10). Missing support is in scope as future work. Redundant support is not mentioned.

## 10. Limitations

**Acknowledged by the authors (§6, p.10):**
- "The main limitation is that the current graph above the Trace Record layer is not fully deterministic … the tracer still interprets which records belong together, which Workflow Node they express, and which semantic edge best describes a relation. These choices can be incomplete, unstable, or wrong." Hence: "LEDGER therefore treats the graph as an audit aid rather than a source of truth."
- Future work: deterministic or verifiable structure through stronger instrumentation or provenance backends (DFTracer [26]); table-, column- and transformation-level dependencies for data workflows; repeated-run stability.
- The edge vocabulary blurs: "Edge types such as uses, informs, supports, and checked_by are useful for review, but their boundaries can blur in long sessions." They propose separating "temporal, dataflow, validation, and evidential relations more explicitly", exposing how each edge was produced, encoding uncertainty, and visually separating deterministic from inferred structure.
- Hooks "may not intercept every tool pathway or every non-shell event" (§3.1).

**Limitations I see:**
- **No empirical evaluation:** n=2 demos, no metrics, no baselines, no user study, no accuracy check of tracer-inferred edges against ground truth.
- **`supports` is correlational/annotative, not tested.** An LLM labels an edge "supports" from text, so the graph cannot show whether the agent's conclusion actually *depended* on that evidence. This is the same faithfulness gap they cite ([4], [16]), moved from the agent to the tracer.
- **The unit is a session, and the focus is outcome claims** (final answer, completion status). Intermediate *decisions*, with their alternatives, the information available and permissions at the time, are not first-class objects. The NetworkX design choice is reconstructed narratively in §5.2, not represented as a decision object.
- **Permissions and authority are ignored** beyond logging the `PermissionRequest` hook. There is no link between audit outcome and what the agent may do next.
- **Consequences are limited** to artifacts produced within the session. Deferred or real-world consequences are not modelled.
- **No generalization or prediction:** traces are not used to predict future behaviour on new episodes, and there is no held-out evaluation.
- **Single agent platform** (Codex with GPT-5.5) and a single coding/data-analysis domain.
- The tracer model, its prompts and its cost are not reported, which hurts reproducibility.

## 11. Related work they cite that matters for us (full references as printed)

Provenance / observability:
- [8] LangChain. *LangSmith: AI agent & LLM observability platform*, 2026. https://www.langchain.com/langsmith/observability
- [9] Susan B. Davidson and Juliana Freire. *Provenance and scientific workflows: Challenges and opportunities.* In Proc. 2008 ACM SIGMOD International Conference on Management of Data, pp. 1345–1350, 2008.
- [10] Paolo Missier, Khalid Belhajjame, and James Cheney. *The W3C PROV family of specifications for modelling provenance metadata.* In Proc. 16th International Conference on Extending Database Technology (EDBT), pp. 773–776, 2013.
- [11] Gabriele Padovani, Valentine Anantharaj, and Sandro Fiore. *Provenance tracking in large-scale machine learning systems.* In Workshop Proc. 54th International Conference on Parallel Processing, pp. 167–174, 2025.
- [12] Renan Souza, Amal Gueroudji, Stephen DeWitt, Daniel Rosendo, Tirthankar Ghosal, Robert Ross, Prasanna Balaprakash, and Rafael Ferreira da Silva. *PROV-AGENT: Unified provenance for tracking AI agent interactions in agentic workflows.* In 2025 IEEE International Conference on eScience, pp. 467–473, 2025.
- [26] Hariharan Devarajan, Loïc Pottier, Kaushik Velusamy, Huihuo Zheng, Izzet Yildirim, Olga Kogiou, Weikuan Yu, Anthony Kougkas, Xian-He Sun, Jae Seung Yeom, et al. *DFTracer: An analysis-friendly data flow tracer for AI-driven workflows.* In SC24: International Conference for High Performance Computing, Networking, Storage and Analysis, pp. 1–24. IEEE, 2024.

CoT faithfulness / monitorability:
- [4] Yanda Chen, Joe Benton, Ansh Radhakrishnan, Jonathan Uesato, Carson Denison, John Schulman, Arushi Somani, Peter Hase, Misha Wagner, Fabien Roger, Vlad Mikulik, Samuel R. Bowman, Jan Leike, Jared Kaplan, and Ethan Perez. *Reasoning models don't always say what they think.* arXiv:2505.05410, 2025.
- [5] Melody Y. Guan, Miles Wang, Micah Carroll, Zehao Dou, Annie Y. Wei, Marcus Williams, Benjamin Arnav, Joost Huizinga, Ian Kivlichan, Amelia Glaese, Jakub Pachocki, and Bowen Baker. *Monitoring monitorability.* In Proc. 43rd International Conference on Machine Learning (ICML), PMLR vol. 306, 2026.
- [16] Miles Turpin, Julian Michael, Ethan Perez, and Samuel Bowman. *Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting.* Advances in Neural Information Processing Systems 36:74952–74965, 2023.
- [17] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. *ReAct: Synergizing reasoning and acting in language models.* ICLR 2023.

Agent evaluation / trajectory auditing (close to our "beyond task success" argument):
- [3] Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, and Michal Shmueli-Scheuer. *A survey on evaluation of LLM-based agents.* In Findings of ACL 2026, pp. 26690–26714, 2026.
- [6] Minxing Wang, Xiaofei Xie, and Yintong Huo. *TrajAudit: Automated failure diagnosis for agentic coding systems.* arXiv:2605.26563, 2026.
- [7] Han Li, Yifan Yao, Letian Zhu, Rili Feng, Hongyi Ye, Jiaming Wang, Yancheng He, Pengyu Zou, Lehan Zhang, Xinping Lei, et al. *CodeTracer: Towards traceable agent states.* arXiv:2604.11641, 2026.
- [13] Ziru Chen, Shijie Chen, Yuting Ning, et al. (incl. Yu Su, Huan Sun). *ScienceAgentBench: Toward rigorous assessment of language agents for data-driven scientific discovery.* ICLR 2025.
- [14] Shuyang Liu, Yang Chen, Rahul Krishna, Saurabh Sinha, Jatin Ganhotra, and Reyhaneh Jabbarvand. *Process-centric analysis of agentic software systems* (Graphectory). Proc. ACM Program. Lang. 10(OOPSLA1):1961–1988, 2026.
- [15] Hanjun Luo, Shenyu Dai, Chiming Ni, Xinfeng Li, Guibin Zhang, Kun Wang, Tongliang Liu, and Hanan Salam. *AgentAuditor: Human-level safety and security evaluation for LLM agents.* NeurIPS 2025.

Trace visualization (closest system):
- [24] Tianci Gao, Haoxuan Li, Jianhe Li, Tianxiang Zhao, Runze Shi, Weiran Wang, Zezhao Wu, and Lu Mi. *Graph of Trace: Visualizing execution traces of scientific agents.* In Proc. 64th Annual Meeting of the ACL (Vol. 3: System Demonstrations), pp. 297–306, 2026. **The paper calls this "closest to our setting".** It relies on agent self-report; we should probably read it too.
- [19] ReasonGraph (Li et al., ACL 2025 Demos, pp. 140–147); [20] Chen et al., *When the chain breaks: Interactive diagnosis of LLM chain-of-thought reasoning errors*, Computer Graphics Forum, e70439, 2026; [21] InteractiveKG (Kim et al., Information Visualization 25(3):310–332, 2026); [22] DeepVIS (Shuai et al., IEEE TVCG 32(1):868–878, 2026); [23] Kulesza, Burnett, Wong, Stumpf, *Principles of explanatory debugging to personalize interactive machine learning*, IUI 2015, pp. 126–137.

Other: [1] Ferrag, Tihanyi, Debbah, *From LLM reasoning to autonomous AI agents: A comprehensive review*, IEEE Access 14:84237–84285, 2026; [2] Shin et al., *The (r)evolution of scientific workflows in the agentic AI era: Towards autonomous science*, SC '25 Workshops, pp. 2305–2316, 2025; [18] Wang & Duan, *Agent AI with LangGraph…*, arXiv:2412.03801, 2024; [25] Hagberg, Schult, Swart, NetworkX, SciPy 2008, pp. 11–15.

**Not cited at all:** classic MAS delegation, adjustable autonomy or trust (Castelfranchi & Falcone, Scerri/Tambe, Bradshaw et al., Parasuraman/Sheridan levels of automation), selective prediction or risk–coverage, and causal or counterfactual explanation. This is a clear gap that our contribution (1) fills.

## 12. Verbatim quotes for our related work

1. "Visibility, however, is not the same as auditability. An event trace can show what happened without showing which events matter for checking a particular conclusion." (§1, p.2)
2. "These systems provide the capture layer, whereas our focus is the review layer above it, i.e., arranging captured records around claims, artifacts, actions, and checks so a reviewer can traverse from a reported result to supporting evidence." (§2.1, p.2)
3. "The Trace Records therefore stand on their own, while the structure built over them is an interpretation." (§3.2, p.4)
4. "These approaches motivate using intermediate actions as evidence, but they typically produce scores, metrics, monitor judgments, or failure labels. Our goal is instead focusing on supporting human review of agent output claim and the work / evidence behind it." (§2.2, p.2) — the grammar is the original's.
5. "LEDGER therefore treats the graph as an audit aid rather than a source of truth" (§6, p.10)
6. "Future systems should distinguish temporal, dataflow, validation, and evidential relations more explicitly, expose how each edge was produced, and encode uncertainty or missing support directly in the graph." (§6, p.10)

## 13. Positioning for WorkTrace

**What LEDGER already covers (we must not claim these as new):**
- Turning flat agent logs into a **typed, layered claim→evidence graph** with artifact anchors (`frames / uses / produces / informs / checked_by / supports`) for coding and data-analysis agents.
- Explicitly **separating deterministic captured records from LLM-inferred structure**, and keeping pointers back to raw transcripts. They also audit the trace-construction process itself.
- The argument that **observability ≠ auditability**, and that a run should be judged by the actions behind a claim, not only by its output.
- Capture from an **unmodified agent through lifecycle hooks**, including `PermissionRequest` events. We cannot claim "hook-based, non-self-report capture" as novel.
- The idea of **validation coverage**: which check covered which behaviour, and the "extent of support".

**What LEDGER leaves open and WorkTrace addresses:**
- **Unit of analysis.** LEDGER's unit is a *session* and its *final claims*. WorkTrace's unit is a **decision episode**: context, information *available*, **permissions**, a **graph of declared grounds**, action, and observed consequences. Alternatives, the information state and the authority in force at decision time are not first-class in LEDGER.
- **Declared vs. tested grounds.** LEDGER's `supports` edges are *asserted by a tracer LLM* and never tested. WorkTrace tests **behaviour towards evidence** with **interventions** (remove X / only X / invert X / add a second source). That is causal and counterfactual dependence, not annotation. LEDGER has no interventions at all (§7 above).
- **Redundancy/overdetermination.** LEDGER does not address it. A simple `supports` graph cannot tell redundant from necessary support, and our intervention design targets exactly that.
- **Authority and delegation.** LEDGER contains no delegation, autonomy scope, escalation or revocability. Its audit serves *human acceptance of an output*. WorkTrace turns evidence behaviour into a **per-decision-class, conditional, revocable delegation rule**, and bridges to MAS adjustable-autonomy theory, which LEDGER does not cite.
- **Evaluation.** LEDGER has two qualitative demos, no metrics and no baselines. WorkTrace evaluates on **held-out generated episodes** with risk–coverage curves against an outcome-only rule and with escalation cost.

**One-sentence differentiation for our related work:**
> LEDGER [Kim et al., 2026] reorganizes observed agent sessions into layered claim-to-evidence graphs whose `supports` edges are inferred post hoc to aid human review; WorkTrace instead takes the individual decision episode, with its available information, permissions and declared grounds, as the unit, *tests* the agent's dependence on evidence through redundancy-robust interventions, and uses the result to grant or revoke autonomy per decision class rather than to annotate a finished session.
