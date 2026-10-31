# Survey note: "From Agent Traces to Trust" (arXiv:2606.04990)

Read in full: **v6** (latest, PDF + HTML, 55 pp. incl. appendices A–E). I also grepped v4 and v5 to see what changed between versions (§1 below).
Page/section numbers refer to v6. Quotes are verbatim from the v6 PDF text. "[my reading]" marks my interpretation; everything else is what the survey says.

---

## 1. Bibliographic data

- **Title:** From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents
- **Authors (11):** Yiqi Wang¹\*, Jiaqi Zhang², Zhangkai Wu³, Taotao Cai¹\*, Zirui Liu⁴, Zequn Sun⁵, Mingkai Zheng⁶, Manqing Dong⁷, Yu-Xuan Qiu⁸, Xuefei Yin⁹, Yanming Zhu⁹ (\* corresponding: yiqi.wang.jennie@gmail.com, taotao.cai@unisq.edu.au)
- **Affiliations:** ¹University of Southern Queensland (AU); ²Jiangsu University (CN); ³The University of Sydney (AU); ⁴Peking University (CN); ⁵Nanjing University (CN); ⁶Southern University of Science and Technology (CN); ⁷UNSW (AU); ⁸Beijing Institute of Technology, Zhuhai (CN); ⁹Griffith University (AU)
- **arXiv:** 2606.04990 [cs.CR; cross-list cs.AI]. DOI 10.48550/arXiv.2606.04990
- **Versions:** v1 3 Jun 2026; v2 14 Jun; v3 16 Jun; v4 28 Jun; v5 10 Sep 2026; **v6 15 Oct 2026 (latest, read)**.
  - v1–v4 were 17–18 MB with heavy figures; v6 is 810 KB. v6 adds a lot of formal material: the corpus protocol (§1.1), "Two Decisions the Taxonomy Changes" (§2.3), the provenance-origin/assurance attributes, §7.6 trace assurance, and appendices B–D (operational semantics, projection π, coding protocol). The set of cited arXiv ids is effectively the same across v4–v6. The only differences are Aegis and MemoryArena, which are now cited by venue (ICLR 2026, ICML 2026) instead of by arXiv id.
- **Venue:** none. It is an arXiv preprint: there is no journal-ref or comments field on the abs page, and the PDF names no venue. It calls itself "a structured curated review rather than an exhaustive systematic review" (§1.1).
- **Resources:** https://github.com/xiaoqi-7/Agent-Tracing-Survey ("continuously updated")
- **Corpus:** 71 works, built by seeded snowballing from 15 listed seeds. 13 are from 2023, 16 from 2024, 13 from 2025, 24 from 2026, plus 5 classic foundations. 51 are peer-reviewed, 17 are preprints, 3 are standards. **None of our nine known competitors is cited** in v4, v5 or v6 (I checked by grepping for their arXiv ids and names).

## 2. Taxonomy (structure)

**Core definitions (§1).**
- **Execution provenance:** a typed graph of an agent run made of *evidence units* (artifacts: queries, documents, observations, tool outputs, memory items, generated tool parameters, intermediate claims, inter-agent messages, final outputs), *execution units* (occurrences: reasoning steps, retrieval calls, tool invocations, memory accesses, environment actions, **delegation steps**), and the semantic, derivational, causal and procedural relations among them.
- **Evidence tracing:** a projection π of that graph that keeps support, contradiction, invalidation and content derivation, drops causal and procedural edges, and adds *Support-candidate* links for content-flow paths that nobody has adjudicated (formalized in App. C, with properties P1–P4: non-injective, grounded, "not all influence is evidence", idempotent).

**Six dimensions (§2.1, Table 1, Fig. 2):**

| Dimension | Categories |
|---|---|
| 1. Trace sources | instructions/inputs, reasoning, retrieval, tool use (incl. MCP server/host boundaries), memory, environment, multi-agent communication |
| 2. Evidence & execution units | evidence units = artifacts with comparable content ρ(v); execution units = occurrences with actor + time interval (the PROV entity/activity split); actors are a third node class (App. B.1) |
| 3. Provenance relations | 9 relations in 4 families (see §3 below) |
| 4. Granularity & timing | granularity: run, step, tool-call, parameter, claim, token/span. Timing: pre-execution, runtime, post-hoc, continuous. Coverage/scope: nodes only, edges only, nodes + edges, cross-session, cross-agent |
| 5. Representation forms | structured logs, execution graphs, evidence/claim-support graphs, provenance graphs, static schemas, runtime state/provenance (Table 4) |
| 6. Trust functions | verification, attribution, debugging, safety enforcement, audit, recovery (Fig. 2 groups them as Correctness / Engineering / Governance) |

**Two cross-cutting attributes (§2.1, Table 2):**
- **Provenance origin** of an edge: *Instrumented* (emitted by the harness), *Inferred* (assigned post hoc by a model or human), *Declared* (self-reported by the agent, the weakest kind), *Derived* (computed from the graph; used only by π).
- **Trace assurance:** *logged*, *tamper-evident*, *attested*. The survey says none of the reviewed systems establishes tamper-evident or attested traces.

**Other structural elements:**
- Four design tensions (§2.2): log vs. semantic provenance; component vs. end-to-end accountability; static schema vs. runtime enforcement; completeness vs. deployability.
- Table 3 groups 27 systems by their primary trust function: Substrate / Attribution-Verification / Safety / Safety (eval) / Recovery / Debugging-Audit.
- Three threads get dedicated review: §3 representation and attribution, §4 tool-use provenance (information flow, access control, guardrails), §5 memory as provenance-bearing evidence (Table 6 scores Write/Retr./Conf./Stale/Verify).
- §6 covers benchmarks: 6 families × 7 capabilities heatmap (Fig. 5), a 25-entry catalogue (Table 8) and metric dimensions (Table 7).

## 3. Typed relations, provenance concepts, evaluation dimensions

**Nine relations in four families (Tables 1, 11, 12; App. B):**

| Family | Relation | Operational test (paraphrase) | Origin |
|---|---|---|---|
| Semantic support | **Support** E→C∪X | Taking ρ(s) as given raises the warrant for ρ(t) (or for a step's *precondition*) above a threshold θ fixed in advance. Agent-independent; "Not necessary: that the agent read s. Not sufficient: that the agent cited s, that s was in context, or that s changed the output." | Inferred / Declared |
| | **Contradict** E↔E | The two contents cannot both hold at the same time index. Symmetric. | Inferred / Declared |
| | **Invalidate** E→C∪mem∪X | s contradicts t or defeats its precondition, s is at least as authoritative as t and later than it, and t may no longer be used as a warrant. The record persists. | Inferred / Declared |
| Content derivation | **Derive** E→E | ρ(t) is a transformation of ρ(s). This shows lineage, not correctness. Derive without Support is the "attributable hallucination". | Inferred / Declared |
| Causal dependence | **Depend-on** X→E∪X | "Had t been absent or different, step s would have been issued with different arguments…" Established by **replay, ablation, fault injection**. | Inferred only |
| | **Trigger** E∪X→X | The occurrence of s caused t to be scheduled at all (*whether* t happens, as opposed to *how*). | Instrumented / Inferred |
| Procedural | **Use** X→E | The harness supplied t to s. Over-approximates Depend-on. | Instrumented |
| | **Generate** X→E | The activity produced the artifact. | Instrumented |
| | **Update** E→E | The same identified location is superseded. | Instrumented / Inferred |

**Other concepts:**
- **Derived predicates** (App. B.5), defined with the origin attribute: *Cited* (a Declared Support edge) vs. *Supported* (an Inferred Support edge). Then *citation error* = Cited ∧ ¬Supported, *attribution gap* = Supported ∧ ¬Cited, and *Omitted* = available but supporting no claim.
- **Relation admission tests** (App. B.6): *necessity* (some trust-function query becomes unanswerable without the relation) and *distinctness* (it has its own decision test).
  - Rejected candidates: Follows, Cited, Omitted, Retrieved-from.
  - **Open candidates: Authorized-by and Responsible-for.** They "fail necessity only under the current corpus, in which delegation and policy are expressed indirectly".
- **Temporal succession is deliberately not a relation**: adjacency in a log establishes no dependence.
- **Two boundary cases** (App. B.3): a tool output that changes a decision without justifying it is annotated {Use, Depend-on} with no Derive and no Support; an incorrect memory item that triggers an action is annotated Trigger with no Support, plus Contradict and Invalidate later.

**Evaluation dimensions (Table 7, §6.4):**
1. *Evidence attribution* (✓ established): evidence recall, citation precision, source supportiveness, faithfulness, claim support accuracy.
2. *Execution provenance* (★ proposed, not operationalized): **trace completeness, provenance accuracy, dependency coverage, temporal consistency**.
3. *Safety and robustness* (✓): unsafe influence detection, attack success rate, policy violation rate, false-positive rate.
4. *Debugging and recovery* (• partly established): failure localization accuracy, diagnosis correctness, auditability, recovery success.

Benchmark capability columns (Fig. 5 / Table 8): evidence labels, tool calls, memory, multi-agent, safety attacks, provenance relations, recovery (plus trace availability). No family reaches S on provenance relations or on recovery.

## 4. Open problems and future directions

The three headline gaps (abstract, §1, §8):
- (G1) "limited integration of fine-grained provenance with multiple trust functions"
- (G2) "no benchmark in our catalog that evaluates the complete provenance chain"
- (G3) "little reporting of tamper-evident or attested traces"

Flag legend: **[DEL]** delegation · **[SCOPE]** autonomy scope · **[AUTH]** authorization · **[CAL]** trust calibration · **[ESC]** escalation/human approval · **[FAITH]** faithfulness of stated reasons · **[CF]** counterfactual/interventional testing · **[RED]** redundancy · **[HO]** held-out evaluation · **[GH]** Goodhart/gaming

| § | Open problem (near-verbatim) | Flags |
|---|---|---|
| 7.1 Unified and interoperable trace schemas | "few schemas jointly represent reasoning steps, retrieval, tool calls and outputs, memory reads and writes, inter-agent messages, intermediate claims, final responses, and external state changes." Future schemas should "connect these operational trace structures with semantic evidence relations" (Support, Contradict, Depend-on, Update, Invalidate) so traces are easier "to compare, replay, annotate, audit, and exchange". | (none directly; replay → weak [CF]) |
| 7.2 Claim-level and semantic provenance | "the harder problem is semantic provenance across transformations… String-level matching and citation presence are therefore insufficient… robust claim-level provenance for long agent executions remains open." | **[FAITH]** (citation ≠ support) |
| 7.3 Memory and multi-agent provenance | Memory items should carry source attribution, write time, update history, conflict status and invalidation events. For multi-agent systems: "agents may communicate, **delegate tasks**, verify one another's outputs… Future provenance models should therefore track… which agent introduced a claim… and **where responsibility lies**. The remaining challenge is to integrate responsibility attribution with claim-level evidence provenance, memory lineage, and recovery actions." It also cites "labeled, **counterfactual**, or contrastive multi-agent trajectories". | **[DEL]** (task delegation among agents, *not* autonomy granting) **[CF]** |
| 7.4 Runtime safety, enforcement, and recovery | Danger arises "when an agent invokes a tool **outside its intended boundary**." "The remaining challenge is recovery… Future systems should use provenance to invalidate stale memory, quarantine contaminated evidence, retry tool calls…, **request human approval**, roll back unsafe state changes, or replay execution from safe checkpoints. This requires provenance representations that support **intervention** and recovery, not only explanation." | **[SCOPE]** (weak) **[ESC]** **[AUTH]** (weak) |
| 7.5 Realistic benchmarks, privacy, and governance | Benchmarks should "move from isolated answer-, task-, or attack-level evaluation toward trace-level evaluation… annotate the provenance relations needed to evaluate evidence support, unsafe influence, responsibility attribution, and recovery." Plus privacy: minimization, access control, anonymization, retention, encryption, selective disclosure. | (benchmark design; no [HO] or [GH] wording) |
| 7.6 Trace assurance and attested provenance | "whether a trace can be trusted by a party other than the one that produced it." Three questions: what to attest; how assurance interacts with privacy; how it interacts with origin. "attestation should not be read as evidence of correctness." | (adjacent to [GH]: an attested trace can still contain wrong inferred edges) |
| 6.4 Research agenda for provenance metrics | Trace completeness, **dependency coverage** ("obtainable by ablation and replay: perturb each candidate dependency and observe whether the dependent step changes… one replay per candidate edge"), temporal consistency, provenance accuracy. **"Why provenance accuracy resists a single gold graph"** gives three options: an admissible set, edge-level scoring weighted by annotators, or the "**minimal sufficient graph**… under replay. This sidesteps disagreement about **redundant edges** at the cost of discarding genuine **over-determination**." "which one the field should adopt remains open." | **[CF] [RED]** ← the closest hook to our C2 |
| 6.5 Limitations of evaluation protocols | None of the benchmarks "scores whether provenance can help the system repair execution, such as by… **requesting human approval**, or rolling back an unsafe state change." "What the field lacks is therefore not more agent tasks but released relation annotations and replayable executions." | **[ESC] [CF]** |
| 2.1 Origin attribute (framed as a caveat, functionally an open issue) | "a reasoning trace is an artifact the model emitted, not an observation of the computation… an edge read off a stated rationale is **Declared** and does not, by itself, establish faithful dependence… [such claims should be] validated by replay or annotation rather than by pointing at the log." | **[FAITH] [CF]** |
| 2.3 Decision 1 / Decision 2 | D1: "Depend-on is Inferred only, so no logging granularity yields it… spend the budget on **replay hooks** and an annotation protocol." D2: "task success and defense quality can come apart… **answer accuracy is not a reliable proxy** for defense quality." | **[CF]**; D2 is related in spirit to **[GH]** (outcome as proxy), though the survey never says "Goodhart" |
| App. B.6 Open relations | "Two candidates we regard as open are an explicit **authorization relation linking an action to the policy that permitted it**, and a **responsibility relation for multi-agent delegation**; both are currently expressed indirectly, and Section 7 treats them as such." (Note: §7 does *not* actually take them up explicitly; I found no mention of Authorized-by in §7.) Also: "A different set of trust functions would admit a different set" of relations. | **[AUTH] [DEL]** |
| App. E.1, Table 17 | Trust metadata should include "Source trust, **permission scope**…, actor identity, and policy constraints". Replay/recovery fields should include "**human approvals**". | **[SCOPE] [ESC]** (schema-level only) |
| App. E.4, Table 19 | Recovery is listed as an "Open problem": "Invalidate stale memory… request approval, roll back…". | **[ESC]** |

**Flags that never occur:** **[CAL] trust calibration**, **[HO] held-out evaluation**, **[GH] Goodhart/gaming**. The words *calibration, escalation, held-out, Goodhart, gaming, adjustable autonomy* do not appear in v6. *Autonomy* appears only inside reference titles; v4/v5 had one passing use in the abstract ("expand agent autonomy"). **[RED]** appears only in the single §6.4 passage above.

## 5. KEY QUESTION: does the survey mention delegating autonomy based on trace evidence?

**No.** No version of the survey (v4–v6) discusses granting, scoping, conditioning, revoking or earning autonomy on the basis of trace or provenance evidence. Specifically:

- **"Trust" means something else here.** It is operationalized as six *trust functions*: verification, attribution, debugging, safety enforcement, audit, recovery. **Delegation, authorization and autonomy allocation are not among them.** The survey itself says the relation set "is minimal only relative to the six trust functions… A different set of trust functions would admit a different set" (§2.1/App. B.6). [my reading] This is an explicit opening for adding a seventh function, *delegation/authorization*.
- **"Delegation" means an execution unit**: "delegation steps" (§1, §2.1, Table 10) and multi-agent task hand-off (§7.3, E.3: "which agent introduced the unsupported claim, which agent failed to verify it"). It never means a principal granting decision rights to an agent.
- **Authorization is an open relation, not a decision rule:** "Responsible-for and Authorized-by fail necessity only under the current corpus, in which delegation and policy are expressed indirectly; they are the two candidates we regard as open" (App. B.6). The authorization relation they have in mind links "an action to the policy that permitted it". That is a *record* of a static permission, not a *policy for granting* permission from evidence.
- **The nearest passages are about per-action gating, not per-decision-class earned autonomy:**
  - §4.4: "capability policies delimit the tools and resources available to an agent (Bühler et al., 2026), while provenance and runtime rules determine whether a particular action should proceed, be restricted, require confirmation, or be blocked (Wang et al., 2026; Sequeira et al., 2026)."
  - §4.4: "A read-only search tool may be permitted to consume untrusted web content, whereas an email, database-update, or code-execution tool may require arguments derived from authorized user intent, verified tool outputs, or explicit approval."
  - §2.1 timing: "The appropriate choice depends on the risk and persistence of the workflow: low-risk RAG may require claim-level post-hoc attribution, whereas high-impact tool use may require runtime parameter-level provenance." This is risk-proportional *tracing*, not risk-proportional *autonomy*.
  - Agent-Sentry (via §4.4) "uses execution provenance… to bound tool calls according to learned behavior and user intent". Its own abstract says it "learns a bound on an agent's benign execution from prior legitimate executions". [my reading] This is the only surveyed work that *learns* a permission boundary from past traces. Its target is injection/out-of-bounds detection, though, not evidence-sensitivity per decision class. There is no revocability, no risk–coverage analysis and no escalation-cost accounting.
- **Escalation** appears only as a recovery option ("request human approval"), and the survey notes that no benchmark scores it (§6.5).

**Bottom line for us:** the survey maps *how to record and judge* agent behaviour. It does not map *what a principal should then do with that judgement*. The step from trace evidence to a bounded, revocable delegation decision is absent. So is any classic MAS delegation or adjustable-autonomy literature (§7 below).

## 6. Most relevant surveyed works for WorkTrace

Contributions: **C1** = MAS delegation ↔ LLM-agent auditing bridge; **C2** = decision episode + redundancy-robust evidence interventions; **C3** = held-out delegation rule (risk–coverage vs. outcome-only, escalation cost).
IDs and venues are given exactly as the survey's v6 reference list states them. † = the survey marks the work as unrefereed.

| # | Work (short title) | Authors | Year | Venue / id as listed | What it does (per survey) | Touches |
|---|---|---|---|---|---|---|
| 1 | **Agent-Sentry: Bounding LLM agents via execution provenance** † | Sequeira, Damianakis, Iqbal, Psounis | 2026 | arXiv:2603.22868 | Builds an execution-provenance graph and per-argument data flow, learns a bound on benign behaviour from prior executions, and flags or blocks out-of-bounds tool calls | C3 (learned permission bound), C1 |
| 2 | **AgenTracer: Who is inducing failure in the LLM agentic systems?** | G. Zhang, J. Wang, J. Chen, W. Zhou, K. Wang, S. Yan | 2026 | ICLR 2026, arXiv:2509.03312 | Counterfactual replay + fault injection to attribute failures to responsible agents/steps (TracerTraj) | C2 (interventional testing) |
| 3 | **Aegis: Automated error generation and attribution for multi-agent systems** | Kong et al. | 2026 | ICLR 2026 (v5 listed arXiv:2509.14295) | Positive–negative trajectory pairs with injected errors labelled by faulty agent and error mode | C2 (generated episodes) |
| 4 | **TRAIL: Trace reasoning and agentic issue localization** † | Deshpande, Gangal, Mehta, Krishnan, Kannappan, Qian | 2025 | arXiv:2505.08638 | Human-annotated traces for step-level failure localization | C2 |
| 5 | **Why do multi-agent LLM systems fail? (MAST)** | Cemri et al. | 2025 | NeurIPS 2025 D&B, doi:10.52202/085713-4082 | Multi-agent failure taxonomy (specification, misalignment, weak verification) | C1 (responsibility) |
| 6 | **Auditable agents** † | Nian, Yuan, Zhang, Li, Li, Hu, Wei, Xiao, Xiao, Zhao | 2026 | arXiv:2604.05485 | Argues for auditable agent design (cited for trace assurance). Its own abstract: 5 auditability dimensions, including *responsibility attribution* and *policy checkability*, plus an "Auditability Card" | C1 (accountability framing) |
| 7 | **Audit trails for accountability in large language models** † | Ojewale, Suresh, Venkatasubramanian | 2026 | arXiv:2601.20727 | Tamper-evident lifecycle audit trails. Its own abstract: links technical provenance with governance records ("approvals, waivers, attestations… who authorized it") | C1 (authorization records) |
| 8 | **ACRFence: Preventing semantic rollback attacks in agent checkpoint-restore** † | Zheng, Yang, Zhang, Quinn | 2026 | arXiv:2603.20625 | Shows agent checkpoint state can be attacked (trace assurance) | (peripheral; integrity of episodes) |
| 9 | **PROV-AGENT: Unified provenance for tracking AI agent interactions in agentic workflows** | Souza et al. | 2025 | IEEE eScience 2025, pp. 467–473 | Extends W3C PROV to prompts, responses, **decisions**, tool interactions | C2 (schema baseline) |
| 10 | **AgentTrace: A structured logging framework for agent system observability** † | AlSayyad, Huang, Pal | 2026 | arXiv:2602.10133 (AAAI 2026 TrustAgent WS poster, non-archival) | Operational / cognitive / contextual logs | C2 (trace substrate) |
| 11 | **AgentOps: Enabling observability of LLM agents** † | Dong, Lu, Zhu | 2024 | arXiv:2411.05285 | Artifact lifecycle observability | C2 (substrate) |
| 12 | **AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents** | H. Wang, Poskitt, J. Sun | 2026 | ICSE 2026, arXiv:2503.18666 | User-defined runtime constraints over agent actions | C1/C3 (static permission rules, the baseline to contrast with earned autonomy) |
| 13 | **AgentBound: Securing execution boundaries of AI agents** | Bühler, Biagiola, Di Grazia, Salvaneschi | 2026 | FSE 2026, doi:10.1145/3808103, arXiv:2510.21236 | Capability-based access control for MCP servers | C1 (permission scope) |
| 14 | **Defeating prompt injections by design (CaMeL)** | Debenedetti et al. | 2026 | SaTML 2026, arXiv:2503.18813 | Control-flow/data-flow separation; restricts external data influence | C2 (external evidence ↔ action influence) |
| 15 | **Securing AI agents with information-flow control (Fides)** † | Costa et al. | 2025 | arXiv:2505.23643 | Confidentiality/integrity labels enforced at runtime | C2 |
| 16 | **Ghost in the agent: Redefining information flow tracking for LLM agents (NeuroTaint / TaintBench)** † | Cai, Tang, Wen, Qin | 2026 | arXiv:2604.23374 | Semantic taint across neural/symbolic steps; source-to-sink influence labels (evidence for Depend-on) | C2 (influence of external evidence under transformation) |
| 17 | **An automated framework for assessing how well LLMs cite relevant medical references (SourceCheckup)** | K. Wu et al. | 2025 | Nature Communications 16:3615 (earlier arXiv:2402.02008) | Shows that cited ≠ supporting; motivates the Declared vs. Inferred split | C2 (faithfulness of declared grounds) |
| 18 | **PaperTrail: A claim-evidence interface for grounding provenance in LLM-based scholarly Q&A** | Martin-Boyle, Leckey, Brown, Kaur | 2026 | CHI 2026 | Claim–evidence mapping: supported, unsupported, omitted | C2 (graph of declared grounds) |
| 19 | **Enabling LLMs to generate text with citations (ALCE)** | Gao, Yen, Yu, Chen | 2023 | EMNLP 2023, doi:10.18653/v1/2023.emnlp-main.398 | Citation support evaluation | C2 (background) |
| 20 | **τ-bench** | Yao, Shinn, Razavi, Narasimhan | 2025 | ICLR 2025 | Tool-agent-user tasks graded on policy following + final DB state | C3 (outcome/state-based scoring; candidate episode source) |
| 21 | **OpenAgentSafety** | Vijayvargiya et al. | 2026 | ICLR 2026 | Real-tool, multi-turn safety evaluation | C3 (risk side) |
| 22 | **MCP-SafetyBench** | Zong, Shen, Wang, Lan, Yang | 2026 | ICLR 2026, arXiv:2512.15163 | Safety on real MCP servers / multi-server workflows | C3 |
| 23 | **Identifying the risks of LM agents with an LM-emulated sandbox (ToolEmu)** | Ruan et al. | 2024 | ICLR 2024 | Risky tool execution in an emulator | C3 (generated risky episodes) |
| 24 | **AgentDojo** | Debenedetti, J. Zhang, Balunovic, Beurer-Kellner, Fischer, Tramèr | 2024 | NeurIPS 2024 | Prompt-injection attacks/defences in realistic tasks | C2 (adversarial external evidence) |
| 25 | **A-MemGuard: A proactive defense framework for LLM-based agent memory** | Wei et al. | 2026 | ICML 2026, arXiv:2510.02373 | Memory checking/correction; cited as Invalidate in practice | C2 (invalidate X) |
| 26 | **Attribution, citation, and quotation: A survey of evidence-based text generation with LLMs** | Schreieder, Schopf, Färber | 2026 | ACL 2026 (long), arXiv:2508.15396 | The closest prior survey by subject | related-work positioning |
| 27 | **The protection of information in computer systems** | Saltzer, Schroeder | 1975 | Proc. IEEE 63(9), doi:10.1109/PROC.1975.9939 | Least privilege / complete mediation, the only "classic" authorization source cited | C1 (classic security baseline, *not* MAS) |

Also cited and possibly useful as a single line in related work: Instruction Hierarchy (arXiv:2404.13208); StruQ (USENIX Sec 2025); LADYBUG (EDBT 2025); RAGChecker (NeurIPS 2024); FActScore (EMNLP 2023); FEVER (NAACL 2018, doi:10.18653/v1/N18-1074); Lin et al. agent-hallucination survey (arXiv:2509.18970).

## 7. Classic MAS trust/delegation and adjustable-autonomy literature

**None cited.** The v6 reference list contains no Castelfranchi & Falcone, Scerri/Pynadath/Tambe, Sierra & Debenham, Ramchurn et al., Jøsang, Sabater & Sierra, Bradshaw, Horvitz (mixed initiative), Parasuraman/Sheridan levels of automation, Lee & See (trust in automation), or any other adjustable-autonomy, MAS trust or reputation work. I grepped for these names and for "adjustable", "calibrat" and "escalat": all returned 0 hits.

The only "classic" foundations it uses are from **security and provenance**:
- W3C PROV-DM (2013)
- Saltzer & Schroeder (1975)
- Denning, lattice model of secure information flow (1976, doi:10.1145/360051.360056)
- Sabelfeld & Myers, language-based IFC (2003, doi:10.1109/JSAC.2002.806121)
- FEVER (2018)

Multi-agent content is limited to LLM frameworks (AutoGen, CAMEL) and failure attribution (MAST, AgenTracer, Aegis). → Our C1 bridge has **no counterpart** in this survey.

## 8. W3C PROV

- It cites **W3C PROV-DM** ("PROV-DM: The PROV data model", W3C Recommendation, 2013), **not PROV-O**: "PROV-O", "ontology" and "OWL" do not appear.
- PROV-DM is one of the 15 seeds and a "foundation" (§1.1). Footnote 1 lists it next to OpenTelemetry as an inspiration.
- **How the survey positions it:**
  1. The evidence/execution unit split "follow[s] the entity/activity split of W3C PROV-DM" (§2.1, App. B.1). PROV Agent maps to "Agent: LLM, tool/API, user, or sub-agent; multi-agent roles and **delegation become first-class**" (Table 9).
  2. **App. A, Table 9 sorts relations into three tiers:**
     - *Inherited*: used→Use, wasGeneratedBy→Generate, wasDerivedFrom→Derive.
     - *Specialized*: used (strengthened)→Depend-on, made counterfactual; wasInformedBy→Trigger; wasInvalidatedBy→Invalidate, which marks something "epistemically invalid while the record persists"; wasRevisionOf→Update.
     - *Novel* (no PROV counterpart): **Support, Contradict**, and semantic units (claims, tool-call rationales, NL observations, messages, trust labels).
  3. "agent provenance **extends, rather than merely instantiates**, classical provenance models" (App. A.1).
  4. "W3C PROV-DM unextended" is a rejected alternative because "Support and Contradict have no counterpart at all" (App. B.6).
  5. §7.1/E.1: PROV-DM, OpenTelemetry, OpenLineage and PROV-AGENT are "useful building blocks but do not fully solve the agent-provenance problem".
- [my reading, worth exploiting] **The survey never maps PROV-DM's own responsibility relations**: `wasAttributedTo`, `wasAssociatedWith`, and especially **`actedOnBehalfOf` (PROV's Delegation)**. At the same time it lists "Responsible-for" and "Authorized-by" as open relations. A WorkTrace schema built on PROV-O could reuse `actedOnBehalfOf` (with `prov:hadPlan` for the permission or plan) as the anchor for a delegation relation, and say that the survey leaves this unaddressed. (The PROV-DM relation names here come from my own knowledge of the standard, not from the survey.)

## 9. Short verbatim quotes for the intro / related work

1. **Abstract:** "These findings highlight why final-answer correctness alone is insufficient to establish process-level trust and motivate research on unified trace schemas, semantic provenance, memory and multi-agent lineage, provenance-aware safety and recovery, realistic benchmarks, trace assurance, and privacy-aware auditing."
2. **§2.1 (Provenance origin and assurance):** "a reasoning trace is an artifact the model emitted, not an observation of the computation that produced the output, so an edge read off a stated rationale is Declared and does not, by itself, establish faithful dependence"
3. **§2.1:** "Declared edges are agent self-reports, such as a generated citation, and are the weakest: a declared citation need not support the claim it annotates"
4. **§2.3 (Decision 2):** "answer accuracy is not a reliable proxy for defense quality, so dependency coverage should be reported separately from answer accuracy" (useful against outcome-only delegation)
5. **§6.4 (Why provenance accuracy resists a single gold graph):** "the minimal sufficient graph, a subgraph in which every edge is necessary to explain the observed outputs under replay. This sidesteps disagreement about redundant edges at the cost of discarding genuine over-determination." (our redundancy-robust interventions address exactly this)
6. **App. B.6:** "Two candidates we regard as open are an explicit authorization relation linking an action to the policy that permitted it, and a responsibility relation for multi-agent delegation; both are currently expressed indirectly"

Spares: §2.3: "And Support is never observable at any granularity, so claim-level audit requires an annotation protocol with a fixed warrant threshold and reported agreement, not a finer trace." §4.4: "provenance and runtime rules determine whether a particular action should proceed, be restricted, require confirmation, or be blocked". §6.5: "What the field lacks is therefore not more agent tasks but released relation annotations and replayable executions".

## 10. Assessment: where WorkTrace sits, and close competitors

**Position and gap.** In the survey's map, a WorkTrace decision episode is an execution-provenance subgraph rooted at an action (execution unit). It has:
- a **Declared** support layer: the agent's graph of stated grounds;
- **Inferred** Depend-on/Trigger edges established by our interventions (remove X / only X / invert X / add a second source);
- a permissions node that the survey lacks (Authorized-by is "open");
- observed consequences, which the survey treats only as "external state changes" or recovery.

Our interventions are exactly the replay/ablation route the survey prescribes for Depend-on and dependency coverage (§2.3 D1, §6.4). Our redundancy-robust variants ("only X", "add second source") answer the over-determination problem the survey leaves open in §6.4.

The real gap we fill sits **downstream of all six trust functions**. The survey stops at *judging* a trace (verification, attribution, debugging, safety, audit, recovery). It never asks how a principal should *allocate decision rights* from accumulated trace evidence. That question has several parts, all of which the survey lacks: delegation per decision class; conditional and revocable grants; held-out validation; risk–coverage against an outcome-only baseline; escalation cost. The survey does not draw on MAS delegation or adjustable-autonomy theory at all. Its own B.6 rule ("a different set of trust functions would admit a different set" of relations) gives us a clean framing: WorkTrace adds **delegation** as a seventh trust function, which in turn makes Authorized-by/Responsible-for necessary relations. The headline gap G2 (no benchmark evaluates the full chain) and the absence of [HO] and [GH] further support C3's generated held-out episodes.

**Close competitors inside the survey that are not on our list** (none of the nine known ones is cited by the survey):
1. **Agent-Sentry (arXiv:2603.22868)** is the most dangerous. It *learns a permission bound from prior legitimate execution traces* and uses argument provenance plus a residual LLM judge to allow or flag each action. Reviewers may read it as "autonomy bounded from trace evidence". Differences to state: it learns *where an agent normally acts* (an injection defence), not *whether the agent responds correctly to evidence*. Its gating is per action, not per decision class with revocation. It has no counterfactual evidence interventions and no risk–coverage or escalation-cost analysis.
2. **AgenTracer (arXiv:2509.03312, ICLR 2026)**: counterfactual replay + fault injection over agent trajectories, close to C2's intervention machinery. Its purpose is failure blame, not delegation.
3. **Auditable Agents (arXiv:2604.05485)**: position paper with "responsibility attribution" and "policy checkability" dimensions and an Auditability Card. Close to C1's accountability framing. It has no delegation rule. (I read only the abstract, not the full paper.)
4. **Audit Trails for Accountability in LLMs (arXiv:2601.20727)**: links provenance to governance records ("approvals, waivers… who authorized it"). It concerns authorization *records* at lifecycle level, not earned agent autonomy. (Abstract only.)
5. **AgentSpec (ICSE 2026) and AgentBound (FSE 2026)** are not competitors but are the *static-permission baselines* our "earned, revocable" autonomy should be contrasted with.

Uncertainty: the claims about #3 and #4 rest on their arXiv abstracts plus the survey's one-line citations; I have not read their full texts. Agent-Sentry was checked against its abstract.
