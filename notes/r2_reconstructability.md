# Property-level reconstructability cluster (Solozobov, 2026): reading note for WorkTrace

**Round 2. Read on 2026-10-25.**

## Coverage

**Read in full (three papers).** For each paper the arXiv e-print is a PDF only, with no LaTeX source. I extracted the full text with `pdftotext -layout` and read every section, table, listing and reference list.
- None of the three papers contains figures. Paper 1 says "8 tables", and Paper 3's only non-table display is a JSON listing.
- Tables were read as layout-extracted text. I checked the cell values against the running text and they match.

| # | Paper | Coverage |
|---|---|---|
| P1 | DEMM, arXiv:2605.04093 | full text, §1–§7 and references |
| P2 | Anchor-level pilot, arXiv:2605.12078 | full text, §1–§7 and references |
| P3 | Load-bearing evidence, arXiv:2607.12469 | full text, §1–§9 and references |

**Other members of the series, read only in part.** The exact coverage is stated per item in §4: abstract only, the introduction only, a few named sections, or a keyword scan.

**Verification.**
- All arXiv items were checked against the arXiv API (export.arxiv.org) on 2026-10-25.
- Zenodo deposits were checked against the DataCite API.
- The SSRN item was checked against Crossref.
- None of the series items has a journal-ref or DOI other than arXiv's. All are single-author preprints with no peer review.

Section numbers (§x) below refer to each paper's own sections.

---

## 1. P1: Decision Evidence Maturity Model (DEMM)

### Bibliographic data [verified, arXiv API]
- **Title:** *Decision Evidence Maturity Model for Agentic AI: A Property-Level Method Specification*.
- **Author:** Oleg Solozobov, sole author. Affiliation is "Independent Researcher (Global)". ORCID 0009-0009-0105-7459.
- **arXiv:** 2605.04093, **v1 only**, submitted 29 Apr 2026. Category cs.CY. 41 pages, 8 tables.
- **Venue:** none. It is a preprint.
- **Companion artefacts** [verified, DataCite]:
  - Decision Trace Reconstructor (DTR) v0.1.0, Apache-2.0, doi:10.5281/zenodo.19851574.
  - Decision Event Schema (DES), MIT, doi:10.5281/zenodo.18923177.

### Problem and contribution
**The "container fallacy".** When "an external party asks a specific governance question about a specific decision", the assembled evidence is often insufficient even though every logging mechanism worked. The paper names the error behind this the **container fallacy**: "an inferential step that treats evidence-container presence as if it implied audit sufficiency, when sufficiency requires per-question per-property checking that container presence does not perform" (§1).

**Three contributions (§1.3):**
1. A per-question, per-property sufficiency relation.
2. A five-level maturity rubric with "level pattern borrowed" from CMM/CMMI, TMMi and DCAM.
3. The DTR reference implementation, with a feasibility run on 140 synthetic scenarios and 3 public incidents.

### Method

**Sufficiency relation (§3.1).** S ⊆ 𝒬 × 𝒫 × 2^ℰ, ranging over:
- governance questions 𝒬;
- decision-evidence properties 𝒫;
- sets of evidence regimes ℰ.

**Eight property classes (§3.1).** Actor identity, principal authority, action boundary, policy basis, decision basis, data and resource touch, lifecycle context, verification strength. The implementation collapses these to **seven rows**: inputs, policy basis, actor identity/principal authority, action boundary/configuration envelope, reasoning trace, output action, post-condition state (Table 7).

**Pipeline (§3.2, Table 1).**
- Stage 0 is a set of evidence-regime adapters: 10 executable adapter-fallback classes plus 8 regime classes that exist at protocol level only.
- Six further stages: fragment collection, temporal ordering, chain assembly, **decision-boundary detection**, schema mapping, feasibility report.
- Each stage has a feasibility gate and a typed failure verdict.

**Unit "decision".** The pipeline *infers* the decision from continuous flows. Four heuristics in §3.3 (state-change magnitude, tool-call boundary, human intervention, policy-constraint activation) produce a confidence score. The paper adds: "no ground truth exists for boundary location in continuous flows".

**"Authorisation envelope" (§3.4).** This replaces opaque reasoning. It is defined as "inputs available (prompt, tool outputs, retrieval), constraints active (policies, tool-permission scopes, model limits), and outputs possible (tool calls allowed, format constraints, terminal action set)".
- Reasoning is classified as *opaque* "uniformly" as a matter of principle. §6.2 calls this the "ML-opacity boundary": "post-hoc reconstruction of internal neural reasoning conflates governance with explainability. The right question — was the step inside its authorisation envelope? — is what DEMM answers."

**Categories (§3.5).**
- *fully fillable*, weight 1.0;
- *partially fillable*, a default weight of 0.5 that is "not independently calibrated";
- *structurally unfillable*, weight 0;
- *opaque*, **weight 1.0**, because the envelope is substituted for the reasoning;
- *conflicting*, which exists at protocol level only and is never exercised.

Completeness is the weighted mean over the 7 rows.

**Output (§3.6).** A tensor over architecture × stack × regime × property × category, plus an "instrumentation recommendation" that names the upstream regime which would close each gap.

**Five-level rubric (§3.7).**
1. *Ad-hoc*: reactive manual assembly, turnaround days to weeks.
2. *Process-attested*: model cards and committees, manual reconstruction.
3. *Property-instrumented*: the runtime captures schema-named properties.
4. *Sufficiency-tested*: the regime is "exercised against a question battery; per-question pass/fail under S(Q,P,E)".
5. *Continuously-attested*: "Sufficiency monitored as SLO; degradation triggers alarms; posture maintained across retraining/drift/handoff/migration".

Levels are assigned **per property class**. The aggregate level is "the minimum across the property classes the forum's governance questions actually test". Thresholds are "proposed design parameters". The unit of capability is explicitly "the evidence the deployment can produce, on demand, for a specific governance question about a specific decision".

**Non-goals (§3.1).** DEMM "is not a debugger, does not produce evidence…, does not enforce at runtime…, does not establish legal compliance". It works "strictly post-hoc".

### Evaluation
**Design (§4).** A 3 × 2 matrix of architecture (single-agent / multi-agent / HITL) by stack coverage (within-stack / cross-stack). Each cell holds **20 synthetic scenarios from the author's deterministic generator**. There is also a non-agentic baseline of 20 scenarios, giving 140 in total, plus 3 named incidents (Replit, Cursor, Claude Code/DataTalks.Club) reconstructed from public reports.

**Completeness (Table 3).**

| Architecture | Within-stack | Cross-stack |
|---|---|---|
| Single-agent | 85.0 | 71.1 |
| Multi-agent | 67.5 | 53.6 |
| HITL | 94.3 | 79.3 |

The non-agentic baseline scores 100.

**Other results.**
- Boundary-detection F1: 0.84/0.76 (single-agent), 0.13/0.46 (multi-agent), 0.73/0.74 (HITL) (Table 4).
- All three incidents score exactly 57.1%, which the paper calls the "instrumentation premium" of 14.0 pp (Table 6).
- A container-presence baseline (a container scores "sufficient when present") overclaims by +23.6 to +80.7 pp (Table 8).

**Status, stated by the author.** "Feasibility, not validation". T1 is called the "most serious threat": the generator and mapper "encode the hypothesised mechanisms", so the severity ordering is "hypothesis-consistent by construction". There are "no independent labels", and the categories are "mapper outputs".

### What WorkTrace must NOT claim
- **A per-decision evidence record** covering inputs available at decision time, authority/permissions/policy, action and post-condition state. DES (2604.09296) and DEMM already do this.
- **The idea that "presence of logs ≠ sufficiency to answer a question about a specific decision"**. This is the container fallacy, and LEDGER's "visibility is not auditability" makes the same point.
- **Treating "information available + constraints active + outputs possible" as the auditable substitute for an opaque decision basis.** This is DEMM's authorisation envelope (§3.4). It is very close to the *(information available, permissions)* part of our episode E.
- **Non-compensatory, per-property, minimum aggregation** as a design principle.
- **Explicit typed "insufficient/unfillable" verdicts** instead of synthesising a plausible chain.

### What it leaves open that WorkTrace addresses
- **It tests the record, never the agent.** DEMM asks whether the archive can answer a question. It never asks whether the agent's action *depended correctly* on the evidence it had.
- **Reasoning is "opaque" by principle.** WorkTrace treats the declared grounds as hypotheses and tests them *behaviourally*, through interventions on external evidence. That requires no access to model internals. In effect, WorkTrace turns DEMM's "opaque" decision-basis row into something that can be tested without explainability.
- **Nothing is prospective.** No autonomy, no delegation, no escalation and no decision classes. The rubric grades an evidence regime for post-hoc audit.
- **No real agents, no held-out evaluation and no outcome-only baseline** of the kind WorkTrace uses.

### Draft differentiation (one sentence)
DEMM grades whether the *records* a deployment keeps can answer a governance question about a past decision (post hoc, per property, with reasoning treated as opaque by principle); WorkTrace tests whether the *agent's* decisions actually respond to the external evidence it declares as grounds, and uses that behaviour to grant or withhold autonomy per decision class.

### Citation cautions
- Single-author preprint with no peer review and extremely dense self-citation.
- **The completeness numbers are circular.** The author's own generator and mapper produce them, and the mapper encodes the hypotheses (T1, acknowledged).
- **The bootstrap CIs over deterministic fixtures are mostly cosmetic.** For example, HITL within-stack gives [94.3, 94.3].
- **Opaque counts as 1.0.** That adds a fixed 14.3 pp to every cell.
- **The identical 57.1% for all three incidents is fixed by arithmetic.** It is (2 + 2·0.5 + 0 + 1)/7 with the default c = 0.5, so it measures nothing incident-specific.
- **The container baseline is a straw rule.** It scores 100% "sufficient" by construction.
- **L1 calls the author's synthesis paper (2604.19112) a "peer-reviewed anchor".** arXiv shows no journal-ref (v2, cs.CY). [unverified claim, likely inaccurate]
- **Cite only for:** the container-fallacy concept, the authorisation-envelope idea, and per-property minimum aggregation. Do not cite its numbers.

---

## 2. P2: Anchor-level pilot across vendor SDK regimes

### Bibliographic data [verified, arXiv API]
- **Title:** *Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes*.
- **Author:** Oleg Solozobov, sole author.
- **arXiv:** 2605.12078, **v1 only**, submitted 12 May 2026. Categories cs.SE, cs.AI. 23 pages, 3 tables.
- **Venue:** none. It is a preprint.
- **Reproducibility package:** doi:10.5281/zenodo.20077961 [verified, DataCite]; GitHub `agent-runtime-evidence/anchor-level-reconstructability-pilot`.

### Problem and contribution
**Question.** Is "runtime evidence regime choice … functionally interchangeable for downstream reconstruction"?

**What was run.** DTR v0.1.0, unmodified, on six vendor regimes: Bedrock, LangSmith, Anthropic tool use, OpenAI Agents, OTLP/Vertex, and MCP. There are also two comparator columns:
- the author's own Operational Evidence Plane (OEP), presented as a "ceiling";
- a Replit-incident manifest reconstructed from public reports.

**Contributions.**
1. A cross-regime matrix.
2. A diagnostic that sorts each property into a regime-independent gap, a regime-dependent gap or "Mixed".
3. A checksum-verifiable package.

### Method
- Seven DES properties: inputs, policy basis, operator identity, authorization envelope, reasoning trace, output action, post-condition state (§4.4).
- Four categories: F, P, S, O.
- **Strict score: F = 1, P = 0.5, S = 0, O = 0.** Note that O is scored 1.0 in P1.
- There is **one anchor per cell**. Each anchor is "an illustrative worked example designed by the upstream repository", with "placeholder UUIDs, timestamps, and tool-call payloads" (§3.3, §4.3).

### Evaluation
**Strict-governance completeness (Table 2).**

| Regime | Strict completeness |
|---|---|
| Bedrock | 85.7 |
| LangSmith | 71.4 |
| Anthropic | 71.4 |
| OpenAI | 85.7 |
| OTLP-Vertex | 42.9 |
| MCP | 42.9 |
| OEP (comparator) | 85.7 |
| Replit (comparator) | 42.9 |

**Property-level findings.**
- Reasoning trace reads O in every vendor regime.
- Output action reads F everywhere.
- Policy basis splits 3 F against 3 S (CV 1.00, Table 3).

**Scope.** Single annotator, descriptive. "No falsification of … interchangeability is claimed".

### What WorkTrace must NOT claim
- That reconstructability of agent decisions has not been measured across real agent SDK trace formats. It has, though only at pilot scale.
- That "reasoning/deliberation is not externally evidenced in any mainstream agent trace format" is our own finding. It is P2's E3 finding.

### What it leaves open
Everything behavioural. It is a schema-coverage exercise over hand-written examples. No agent ever ran.

### Draft differentiation
P2 checks which decision properties different agent SDK trace formats *can* carry, using hand-written examples; WorkTrace measures how a running agent's decisions depend on the evidence it had.

### Citation cautions
- **The cell differences largely reflect how the author wrote each worked example.** The paper concedes the F/S split is "a property of the joint runtime evidence regime — vendor SDK emission, adapter mapping, and worked-example construction" (§5.2).
- **n = 1 per cell.** The CV is computed over 6 single anchors.
- **The scoring of "opaque" contradicts P1** (0 here against 1.0 in P1).
- **It calls "container fallacy" "the present manuscript's coinage" (§6.2),** although P1, posted two weeks earlier, already named and defined it. This is a self-citation inconsistency.
- **It refers to itself as "Paper 27",** which suggests a large internal numbering of outputs.
- **Cite at most as** "cross-format pilot (Solozobov 2026b)".

---

## 3. P3: Agent-safety evaluations as load-bearing evidence (the closest of the three)

### Bibliographic data [verified, arXiv API]
- **Title:** *Agent-Safety Evaluations as Load-Bearing Evidence: A Vendor-Neutral, Cross-Harness Reconstructability Metric*.
- **Author:** Oleg Solozobov, sole author.
- **arXiv:** 2607.12469, **v1 only**, submitted 14 Jul 2026. Categories cs.SE, cs.AI. 36 pages, 3 tables.
- **Venue:** none. It is a preprint.
- **Package:** `inspect-evidence-sufficiency` v0.3.0, doi:10.5281/zenodo.21055696 [verified, DataCite].

### Problem and contribution
**Thesis.** "Identical nominal outcomes (task success, attack success, monitor scores) may sit atop materially different evidence regimes."

**Definition of load-bearing (§1).** "An evaluation result is called load-bearing evidence here when the evidence its harness retained suffices to reconstruct the decision the claim is about."

**Four contributions:**
1. **A property-level metric over eight classes.** The classes are action recoverability, permission recoverability, monitor visibility, policy-state visibility, responsibility attribution, counterfactual replayability, claim sufficiency, and evaluation-awareness confounding.
2. **A cross-harness adapter** for Inspect and ControlArena that emits per-decision **Evidence Sufficiency Cards**.
3. **A counterfactual-replay intervention protocol.** Only its *precondition probe* is implemented.
4. **A claim-evidence "overclaim gap" G.**

The same Card also backs a **per-run monitor-coverage release check**.

### Method

**Unit of analysis (§3).** "the evaluation claim — an assertion a safety evaluation makes about an agent decision on the strength of a recorded run". Note the move from P2: "the unit of analysis becomes the evaluation claim rather than the vendor" (§1).

**Scoring.**
- Per property: r_p = |present(p)| / |R_p| (Def. 2). R_p, the required-evidence sets, are "the author's design … asserted, not empirically validated" (Def. 6).
- Vector r, with headline **bottleneck R_min = min over the claim-required properties** (Def. 3).
- G(A, B) = |R(A) − R(B)| for two regimes that share a nominal outcome (Def. 4).

**Card schema (Def. 5).** It includes `permission_decision: allow | block | escalate | none`, `monitor_view`, `policy_version`, `replay_preconditions {possible | degraded | impossible}`, and `counterfactuals_run`, which is empty in this release.

**Replay protocol (§3.5).**
- What it would alter: "the monitor-visibility regime …, the permission outcome (granted versus denied), the policy or rollout state, and inserted or removed evaluation-awareness cues".
- What is measured is whether replay is *possible*. Six preconditions: model binding, decision context, determinism controls, monitor-view spec, permission and policy state, environment re-creation.
- The causal hypothesis H3 is "executed replay changes the **reconstructability verdict**". This is "the v2 protocol".

**The released v0 scorer is coarser than the design (Table 1).**
- 12 fields F01–F12, each three-valued.
- Per trace, not per decision.
- Responsibility attribution and evaluation-awareness are carried "only indirectly".
- G itself is not implemented, only a "field-level analogue".
- Of the six replay preconditions, only model binding (F03) and the policy half of the permission-and-policy precondition (F10) are actually read, plus a replay-handle presence check (F09) (§4.3).

**Verdicts and gates (§4.4–§4.5).**
- Verdict tiers: *insufficient / conditional / sufficient-for-named-decision*.
- **CLI gates block on exit code:** `--gate`, `--strict`, `--require-present F07`.
- **Monitor-coverage gate:** "For every risky tool-execution span in a run, an identified monitor must have actually scored that span; any uncovered risky span makes the eval's PASS unbacked and fails the release gate."

### Evaluation
**Inputs (§5–§6).** Four scored traces:
- two public traces (Trace Commons coding, Assayo web research);
- one bundled Inspect `mockllm` log;
- one synthetic fixture.

There are also two **synthetic** fixture pairs: monitor coverage, and a raw versus instrumented release gate. **No new model runs.**

**Results.**
- Sufficiency 0.458, 0.458, 0.667, 0.833. Two cards are insufficient and two conditional; **none reaches sufficient-for-named-decision** (Table 3).
- Synthetic release-gate pair: 0.542 against 0.667. The raw variant is blocked and the instrumented one passes (§6.2).
- Replay preconditions are unmet in every trace (§6.3).
- Monitor-coverage pair: coverage 1.0 passes, 0.333 blocks (§6.4).

**Stated limits.**
- T1: R_p are author-declared.
- T2: "scores recoverability, not correctness".
- T3: ControlArena is never demonstrated on a real export, and there is no real matched-outcome pair.
- T4: no replay was executed.

### Key question (c): does P3 link evaluation evidence to deployment or delegation decisions?

**Partly, at the level of *release* gating, but only for the evidential *completeness of an evaluation record*. It never links to the agent's behaviour, and it never links to autonomy or delegation.** Specifically:

1. **There is a gate.** F01 is "eval objective and release decision". The CLI exit code "can therefore halt a release exactly when the evidence behind it is not there" (§8). This is the nearest thing in the cluster to "evidence → deployment decision".

2. **But the gated object is the *evaluation's PASS*, not the agent's right to act.** The gate checks presence and coverage only. The paper disclaims more than once:
   - "coverage is not accuracy, covered is not safety or release approval" (§4.5);
   - the card's `not_sufficient_for` includes "no production release approval by itself" (§6.5);
   - "diagnostic, not normative … it sets no threshold above which an evaluation is sound" (§8).

3. **The unit is the evaluation claim or run.** There is no notion of decision class, no per-class grant, no revocation, no proceed/escalate/refuse policy for the agent, no escalation cost and no risk–coverage analysis. `permission_decision: allow|block|escalate` is a recorded harness fact to be *recovered*. It is not an output of any rule P3 proposes.

4. **The replay protocol is the closest point to our interventions, but it differs in three ways.**
   - (i) It alters the *conditions of oversight and authorisation*: monitor view, permission granted/denied, policy state, evaluation-awareness cues. It does not alter the *information content of external evidence*. There is no remove-X / only-X / invert-X / add-independent-source operation, and no treatment of redundancy.
   - (ii) Its dependent variable is the *reconstructability verdict*, not the agent's action or its correctness.
   - (iii) It is not executed. "where evidence fails the preconditions, executed replay is … undefined".

5. **ADAS is mentioned only as a contrast.** P3 cites ADAS (Saparning, arXiv:2601.08869) and contrasts its own gate with it. ADAS "authorises a model deployment under law" through an "Evidence Sufficiency Check" and a deployment certificate. P3 places itself *below* that layer. (I did not read ADAS; see §5.)

**Verdict on threat.** P3 shares WorkTrace's *critique*: outcome-only numbers are not enough. It also shares the *gate posture*: no credit without sufficient evidence. But it locates the problem in the **record** and stops at a blocking check on evidence presence. WorkTrace locates the problem in the **agent's evidence-handling** and turns tested behaviour into graded, revocable autonomy per decision class. The overlap is real at the level of framing and vocabulary (load-bearing, gate, counterfactual replay, permission field). It does not overlap our core contribution.

### What WorkTrace must NOT claim
- **That "task/attack success can hide differences that matter" is new.** P3 frames it for evaluations, and Rabanser et al. 2026 (arXiv:2602.16666, cited by P2 and P3) frame it for reliability.
- **That WorkTrace is the first to tie an evidence-sufficiency verdict to a blocking gate in a release pipeline.** Release gating on evidence presence exists in P3 (and EviBound and ADAS at other levels).
- **That a counterfactual *replay* protocol altering permissions or policy state of a recorded agent decision is new.** P3 specifies one; AgenTracer (arXiv:2509.03312) executes counterfactual replay for failure attribution.
- **That WorkTrace introduces evaluation-awareness as a confound for agent-decision evidence.** P3 makes it a scored property.
- **That a three-valued verdict with an explicit "insufficient evidence" outcome is new.** P3 has one (inheriting comply / violate / ⊥ from Auditable Agents).

### What it leaves open that WorkTrace addresses
- **Behaviour versus record.** P3 states outright that it "scores recoverability, not correctness … A claim can be reconstructable and false" (T2). WorkTrace measures correctness of evidence use.
- **Executed interventions.** P3's replay is unexecuted. WorkTrace runs interventions on held-out generated episodes.
- **Decision rule.** P3 offers a gate on evidence presence. WorkTrace offers a delegation rule (proceed / escalate / refuse per decision class), with escalation cost, a risk–coverage curve and an outcome-only baseline.
- **Redundancy-robust evidence perturbations.** Absent from P3.

### Draft differentiation
P3 asks whether an agent-safety evaluation *kept enough evidence* for its headline outcome to bear weight, and gates releases on the presence of that evidence; WorkTrace asks whether the *agent* handles evidence correctly under executed interventions, and turns that tested behaviour into conditional, revocable autonomy per decision class.

### Citation cautions
- **The empirical part is a tool demonstration.** Four traces, three of six inputs synthetic, no matched real pair, no positive control, no executed replay.
- **The headline 0.458–0.833 compares heterogeneous inputs.** The paper admits this is "outside Definition 4's domain".
- **Two of the twelve fields (F01, F12) are not trace-derived,** so scores "modestly overstate trace-earned sufficiency".
- **The design–release gap is large** (eight properties against 12 fields; G not implemented).
- **The paper is candid about all of this.** Cite it for the *construct* (the load-bearing framing, Evidence Sufficiency Card, monitor-coverage gate, evaluation-awareness confounding), not for numbers.
- **Terminology collision.** If WorkTrace uses "load-bearing", either cite P3 or pick another word.

---

## 4. Further items in the series (all by O. Solozobov)

### Papers on arXiv (8) [all verified, arXiv API]

| arXiv / DOI | Title | Date | My coverage |
|---|---|---|---|
| 2604.09296 | *Decision Trace Schema for Governance Evidence in Real-Time Risk Systems* | 10 Apr 2026 | abstract + keyword scan |
| 2604.15740 | *Evidence Sufficiency Under Delayed Ground Truth: Proxy Monitoring for Risk Decision Systems* | 17 Apr 2026 | abstract, §1, §2.3–§3.1, §5 "Decision-level validation", §6.1–6.1.1 |
| 2604.17836 | *Label-Free Detection of Governance Evidence Degradation in Risk Decision Systems* | 20 Apr 2026 | abstract + keyword scan |
| 2604.19112 (v2, 24 Apr) | *Governed Auditable Decisioning Under Uncertainty: Synthesis and Agentic Extension* | 21 Apr 2026 | abstract + keyword scan |
| 2605.04093 | DEMM (P1) | 29 Apr 2026 | full |
| 2605.12078 | Anchor-level pilot (P2) | 12 May 2026 | full |
| 2606.20634 | *DEMM-Bench: A Cross-Regime Benchmark for Agent-Runtime Governance-Evidence Sufficiency* | submitted 30 May 2026 | abstract, §1 (intro, contributions, motivation) + keyword scan |
| 2607.12469 | Load-bearing evidence (P3) | 14 Jul 2026 | full |

What each of the partly read papers contains:

- **2604.09296 (Decision Trace Schema).** Introduces the Decision Event Schema (DES), with the "Fragmented Trace Problem" and a tiered evidence strategy by risk.
- **2604.15740 (Evidence Sufficiency Under Delayed Ground Truth).** For ML fraud/credit models.
  - It has a sufficiency score S(t) with a multiplicative **"decision-readiness gate" A(t)** and thresholds at 0.8 and 0.5.
  - The response below threshold ("enhanced review, fallback, or escalation") "is not prescribed by the framework". The paper states: "It does not validate whether governance actions triggered by threshold crossings (continue, escalate, intervene) are operationally correct."
  - So it is about *model-monitoring* evidence under label delay, not agent behaviour.
- **2604.17836 (Label-Free Detection).** Governance Drift Toolkit, applied to Lending Club data.
- **2604.19112 (Synthesis).** The "three structural breaks": decision diffusion, evidence fragmentation, responsibility ambiguity. It also has propositions on "delegation-depth effects". From my keyword scan, "delegation" here means multi-agent sub-task delegation, which degrades evidence. It does not mean granting autonomy.
- **2606.20634 (DEMM-Bench).**
  - 64 synthetic cases, 8 regimes, 8 degradation conditions.
  - Results: Overclaim Rate 75% for trace- and schema-present baselines and 50% for ledger-present; the property-level scorer has 0% overclaim and 56.25% Property Sufficiency Accuracy.
  - Labels come from a "construction oracle", not from humans.

### Other items
- **SSRN** [verified, Crossref; not read]: *Distinguishing Governance from Compliance Evidence: A Framework for Post-Incident Reconstruction*, doi:10.2139/ssrn.6457861 (2026).
- **Zenodo software and datasets** [verified, DataCite; descriptions only]:
  - DES and DTR (v0.1.0 to v0.2.0);
  - Operational Evidence Plane (doi:10.5281/zenodo.20051037);
  - inspect-evidence-sufficiency;
  - Evidence Sufficiency Calculator, Governance Drift Toolkit, Governance Benchmark Dataset, Evidence Collector SDK.

**Two deposits worth watching:**
- **agent-payment-repro** (doi:10.5281/zenodo.21525919, issued 2026-07-24).
  - Its description says it "reconstructs a single AI-agent payment episode from its recorded evidence — the action mandate, the agent's tool trace, the policy, and any out-of-band approval receipt". It returns verdicts on mandate conformance, authorization-evidence requirements, and reconstructability.
  - It uses the word **"episode"** and works in the **payments/banking domain**, which is close to Decision-Native Banking Agents. It is still post-hoc conformance and reconstruction, not delegation. It is software, not a paper.
- **DTR v0.2.0 replication dataset** (doi:10.5281/zenodo.23301643, issued 2026-10-11).
  - Contents: "36 GPT-4.1-mini sandbox trajectories represented by 72 paired full and reduced evidence packets … refunds, procurement and configuration changes across three agent architectures", with "frozen V5 assessments produced with Claude Sonnet 4.6".
  - The DTR v0.2.0 record mentions "the separate live-model replication study". **A follow-up paper with live agents on business-decision tasks is therefore likely imminent.** It would still score evidence-packet sufficiency (full against reduced), not agent behaviour.

**Not part of the series but surfaced by P3, to be read in round 3:** Saparning, *AI Deployment Authorisation: A Global Standard for Machine-Readable Governance of High-Risk Artificial Intelligence*, arXiv:2601.08869 (11 Jan 2026) [verified, arXiv API; abstract only]. It compiles regulatory obligations into "machine-executable deployment gates" and a "deployment certificate … license to operate", scored on risk, alignment, externality, control and auditability. That is evidence → *deployment* authorisation, at the level of the whole system and jurisdiction rather than the agent's decision class.

---

## 5. Answers to the key questions

### (a) Unit of analysis: their decision, properties and anchors against our decision episode

**Their units differ across the series.**
- **P1:** "a specific governance question about a specific decision". The decision is a unit *inferred* heuristically from a continuous flow, with a confidence score.
- **P2:** per anchor and per regime, with one decision unit per tool call plus state mutation by default (§3.4).
- **P3:** the *evaluation claim* about a recorded decision. In v0 this is in practice per trace.

**Mapping onto our episode E = (context, information available at decision time, permissions, graph of declared grounds, action, observed consequences):**

| WorkTrace E | DEMM / DES (P1, P2) | P3 Card | Overlap |
|---|---|---|---|
| context | lifecycle context; architecture/stack cell | policy-state visibility (rollout/context state), F02 scope | partial |
| information available at decision time | **inputs** ("prompt, tool outputs, retrieval"), part of the authorisation envelope | F04 and F06 (prompt, messages, tool calls); "decision context reconstructable" precondition | **strong** |
| permissions | principal authority, action boundary, policy basis, **authorisation envelope** ("constraints active … outputs possible") | permission recoverability (verdict, rule, principal), `permission_decision` | **strong**, and theirs is richer on principal/authority |
| graph of declared grounds | decision basis → "reasoning trace", **opaque by principle**, replaced by the envelope | partly within evaluation-awareness ("reasoning record"); otherwise absent | **divergent**: they refuse to reconstruct it, we test it |
| action | output action | action recoverability | strong |
| observed consequences | post-condition state (immediate) | state mutation within action recoverability | partial: no deferred consequences |
| (no counterpart in E) | verification strength, actor identity | monitor visibility, responsibility attribution, claim sufficiency, evaluation-awareness | theirs only |

**Consequence.** Five of the six components of E have named counterparts in DES/DEMM, and DEMM's *authorisation envelope* almost literally equals our *(information available, permissions, possible actions)*.

What remains ours:
- the *graph of declared grounds* as a testable object;
- deferred consequences;
- above all, the use of the episode as a **unit of experimental intervention**, not a unit of archival completeness.

The related-work section must say this explicitly. Episode *fields* are not our novelty; the *tests run on episodes* and the *delegation rule* are.

### (b) Container fallacy and the five-level rubric: does any level tie evidence sufficiency to what an agent may do?

**No.** All five levels describe "the evidence regime the deployment carries into post-hoc audit". Even Level 5 ("Sufficiency monitored as SLO; degradation triggers alarms") triggers *alarms*, not restrictions on the agent.

The closest wordings concern **claims**, not actions:
- "a deployment cannot defensibly claim attestability for properties classified structurally_unfillable or conflicting until the recommended upstream regime is in place" (§3.6);
- "feasibility precedes enforcement" (§6.4);
- "withholding final deployment ratings until F7 calibration" (§5.8), where the "deployment ratings" are maturity ratings.

"Procurement-time sufficiency screening" is listed as a beneficial use (§7) but is not developed.

The precursor 2604.15740 maps sufficiency thresholds to "continue / escalate / intervene" for ML models, but explicitly does not prescribe or validate that mapping.

**Nothing in the cluster grants, narrows or revokes agent autonomy.**

### (c) P3 and deployment or delegation

See the boxed analysis in §3. In brief:
- P3 has a **release gate** on the *evidence presence/coverage of an evaluation record*.
- It explicitly disclaims release approval.
- It has no decision classes, no agent-level autonomy, no revocation and no behavioural testing.
- Its counterfactual replay, which would alter permission/policy/monitor-view/evaluation-awareness cues, is specified but not executed, and its target variable is reconstructability.

It is the **closest framing neighbour, not a competitor on the core claim**.

### (d) Evaluation quality

**Weak across the cluster. All of it is self-generated or illustrative.**
- **P1:** circular synthetic generator and mapper; no independent labels; incident scores fixed by arithmetic.
- **P2:** six hand-written examples, n = 1 per cell, single annotator.
- **P3:** four traces, three of six inputs synthetic, no executed replay, no positive control.

**Strengths.**
- Exemplary candour about limits, with long threats-to-validity lists.
- Byte-reproducible packages.
- Deterministic scoring with no LLM judge.

**Internal inconsistencies:**
- opaque is weighted 1.0 in P1 but 0 in P2 and P3;
- P2 claims to coin a term P1 already defined;
- P1 calls an arXiv-only preprint "peer-reviewed".

**Style.** Dense self-citation and coined jargon; there are more than ten artefacts, which the author numbers internally ("Paper 27").

### (e) Precise differentiation from WorkTrace

| Axis | Solozobov cluster | WorkTrace |
|---|---|---|
| Object measured | sufficiency of *records* (traces, cards) to answer governance questions | the *agent's* evidence-handling behaviour |
| Time direction | retrospective audit; release check on evaluation evidence | prospective: decides future autonomy |
| Decision basis / reasoning | opaque by principle, replaced by the authorisation envelope | declared grounds treated as hypotheses and tested behaviourally via external-evidence interventions (no internals needed) |
| Interventions | none executed; P3 specifies replay altering monitor view, permissions, policy, evaluation-awareness cues | executed: remove X / only X / invert X / add independent second source, with redundancy control |
| Dependent variable | fillability category / r_p / sufficiency score | change and correctness of the action under intervention |
| Output | per-property tensor, maturity level, insufficient / conditional / sufficient verdict, CI exit code | proceed / escalate / refuse per decision class, conditional and revocable |
| Granularity | per property per deployment (P1); per evaluation claim/run (P3) | per decision class per agent |
| Evaluation | synthetic fixtures and hand-built examples, no held-out set | held-out generated episodes, risk–coverage against an outcome-only rule, explicit escalation cost |
| Theory lineage | maturity models (CMMI), audit/forensics, EU AI Act Art. 12/14 | MAS delegation, trust, adjustable autonomy |

---

## 6. Implications for WorkTrace

### Design changes and risks

1. **Do not present the episode schema as the novelty.** DES/DEMM fields (inputs, authorisation envelope, policy basis, actor/principal authority, output action, post-condition state) cover most of E.
   - Cite DES and DEMM and frame E as *"a decision record in the sense of DES/DEMM, extended with a declared-grounds graph and deferred consequences, and used as a unit of intervention"*.
   - Consider providing a field crosswalk (E ↔ DES ↔ Evidence Sufficiency Card) in an appendix; it costs little and pre-empts reviewers.
2. **Turn their "opaque" stance into our selling point.** DEMM declares the decision basis unreconstructable "by principle" and P2 finds it O in every vendor format. WorkTrace's interventions on *external* evidence make the decision basis *behaviourally* testable without explainability or chain-of-thought access. One sentence in the introduction or related work can make this contrast.
3. **Add a reconstructability precondition to the delegation rule.** A decision class whose episodes lack sufficient records (for example, inputs or permissions not recoverable) cannot be tested, so it should default to *escalate*. This mirrors P3's "insufficient evidence" verdict and P1's min-aggregation. Cite both. It also gives the rule a principled "no evidence → no autonomy" floor.
4. **Treat evaluation-awareness as an explicit threat to validity.** Generated episodes are tests. If agents detect test framing, their tested behaviour may not transfer to deployment. Cite P3 (property viii), and Chaudhary 2026 and van der Weij et al. 2024 as P3 cites them [not verified by me]. Consider varying test-framing cues as a robustness check.
5. **Keep our interventions clearly distinct from "counterfactual replay".**
   - P3 specifies replay that alters *permission/policy/monitor view*; AgenTracer executes replay for blame attribution.
   - Ours alters the *content and redundancy of external evidence* and measures the *agent's action and its correctness*.
   - Name ours "evidence interventions", not "counterfactual replay", to avoid the collision.
6. **Expect a live-agent follow-up from this author.** The DTR v0.2.0 dataset (Oct 2026) already holds GPT-4.1-mini trajectories on refunds, procurement and configuration changes, and there is a payments "episode" tool. If a paper appears before our preprint, its likely content is evidence-packet sufficiency (full against reduced packets) on live agents. That still does not test behaviour or allocate autonomy, but the domain overlap with Decision-Native Banking Agents is real. Re-check arXiv for "Solozobov" before submission.
7. **"Load-bearing"** is now P3's term. Either avoid it or cite it.
8. **Shared critique.** Both P3 and WorkTrace argue that outcome-only numbers mislead. Frame WorkTrace's outcome-only baseline as the *agent-behaviour* counterpart of P3's *record* critique, and cite P3 and Rabanser et al. 2026.

### Things to cite (and how)

| Item | Cite for |
|---|---|
| Solozobov 2026, DEMM, arXiv:2605.04093 [verified] | container fallacy; authorisation envelope; per-property min aggregation. Not its numbers. |
| Solozobov 2026, P3, arXiv:2607.12469 [verified] | evaluation claims as load-bearing only when reconstructable; Evidence Sufficiency Card; monitor-coverage release gate; evaluation-awareness confounding; specified-but-unexecuted counterfactual replay. Closest framing neighbour. |
| Solozobov 2026, DES, arXiv:2604.09296 [verified; abstract only] | per-decision evidence schema, in the crosswalk only |
| Solozobov 2026, P2, arXiv:2605.12078 [verified] | optional, at most one clause (reasoning is not evidenced in any surveyed SDK format) |
| Solozobov 2026, DEMM-Bench, arXiv:2606.20634 [verified; partially read] | optional, for overclaim of container-presence baselines |

**Round-3 reading list:**
- Saparning, ADAS, arXiv:2601.08869 [verified; abstract only]: evidence → deployment authorisation.
- Auditable Agents, Nian et al., arXiv:2604.05485 [verified, v4]. The arXiv comment says a condensed version was accepted to ACM AI Summit 2026 (Visionary Papers); I did not verify that acceptance independently. It is the source of the comply / violate / ⊥ verdict and of the five auditability dimensions.
- Rabanser et al., *Towards a Science of AI Agent Reliability*, arXiv:2602.16666. [unverified by me; cited in P2 and P3]

### Bottom line for novelty
**No threat to the core claim.** No work in this cluster grants, narrows or revokes agent autonomy; tests the agent's dependence on evidence through executed interventions; or evaluates a delegation rule.

**Moderate threat to secondary claims:**
- the episode schema fields, which are largely pre-empted by DES/DEMM's authorisation envelope;
- "outcome-only is insufficient" framing, shared with P3;
- "gate on evidence sufficiency", shared with P3 at the release level.

The related-work paragraph must concede these explicitly and position WorkTrace as moving from **record sufficiency** to **behavioural evidence-dependence**, and from **audit** to **delegation**.
