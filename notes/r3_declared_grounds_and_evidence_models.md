# Round 3: declared grounds, evidence models, authority gap, information states

Works covered:
1. **GRADE** (Zhao, arXiv:2606.22741v3): dependency edges graded *observed / declared / inferred*, with degree-matched counterfeit controls.
2. **An Evidence Model for Agentic Processes** (Brömme, arXiv:2609.08481v1): evidence claims, trust assumptions, policy assessment and decision sessions. New; not read in earlier rounds.
3. **Agent Safety Is Action Alignment** (Li & Zhao, arXiv:2606.28739v1): harm as the gap between the authority an action exercises and the authority that was granted.
4. **CatchBench** (Zhao et al., arXiv:2608.22808v4): auditing under PRE / LIVE / POST information states.

## Bottom line (read this first)

**None of the four falsifies W1, W2 or W3. None threatens DSA as a construct outright.** Five points need care in our writing:

1. **Terminology clash: "declared".** In GRADE, a *declared* edge is a read/write recorded by **added instrumentation (logging)**. It is **not** a reason the agent states. GRADE has no agent-stated grounds, no interventions on evidence, and no test of whether an edge is causally used.
   - GRADE says this itself: "An observed edge records shared access to a resource, not proven reliance" (§4.1).
   - It also says: "Empirical coverage of declared event-level reliance therefore remains open" (App. F).
   - Since Auditable Agents and the survey 2606.04990 cite GRADE, a reader may assume "declared dependency" is already handled. **We must write "agent-declared grounds" (or "stated grounds") every time and add a footnote that disambiguates it from GRADE's instrumentation-declared grade.**
2. **A named neighbouring construct: "action alignment"** (Li & Zhao), S★ = Competence ∧ Restraint ∧ Resistance.
   - It overlaps with one DSA dimension, "stay within authority scope", via R(a) = 1[auth(a) ⊆ A]. It partly overlaps with a second: resistance to injected control is related to, but different from, our "preserving provenance".
   - It has **no evidence-grounding coordinate**. A right action taken on the wrong basis is fully "aligned" under S★.
   - We should cite it, adopt R as the formal definition of our authority dimension, and present DSA as adding the coordinates action alignment lacks: grounding, uncertainty/contradiction boundaries, escalation, revision and provenance.
   - Their own "projection is provably blind" argument transfers directly to our critique of outcome-based delegation.
3. **Brömme's "agentic decision sessions" record** contains the fields "inputs considered, arguments, dissent, uncertainty, outcome", held "before high-impact or policy-sensitive actions".
   - This overlaps with our episode fields (information available + declared grounds) **at the level of record-keeping**.
   - It explicitly treats semantic validity as untested, and it does not grant authority ("does not create organizational authority by itself").
   - Its PDCA "Act" phase updates **tool permissions** after audit findings. This is a human-ratified, finding-driven permission loop with no decision-class unit and no behavioural test.
   - Add it to the list of works where "recording the grounds/permissions" is already present (alongside Solozobov DEMM, Graph of Trace, Audit Trails).
4. **CatchBench's "dropped grounding" and "stale-state read" fault injections** look like our "remove X" and stale-evidence interventions.
   - They edit **the recorded trace graph** to test **auditors**. The agent is never re-run, so nothing is learned about whether the agent depends on the evidence.
   - CatchBench's own admissibility bar fails or leaves undetermined both injected substrates (§4.3, App. G).
   - Main lesson: **construction-artifact leakage**. A position-only rule scores F1 = 1.000 on one source because the label follows declaration order. Our generator is exposed to exactly this risk.
5. **One research group is converging on our area.** Yue Zhao's USC group wrote Auditable Agents, GRADE, CatchBench, Action Alignment, FORTIS and The Autonomy Tax. Together these cover authority-gap formalisation, graded dependency, information-state auditing, over-privilege benchmarks, and allow/block/escalate enforcement.
   - They have **not** connected these to granting autonomy from tested evidence-handling.
   - **This is the most likely group to publish a competing piece next.** Re-check arXiv for "Zhao, Yue" before submission.

**Reading status.** All four were read in full text, extracted from the arXiv PDFs with `pdftotext`. Figures were read only through their extracted text labels and captions. Per-work details are under each entry.

---

## 1. GRADE (Zhao, 2026)

### Bibliographic data
- **Title:** *GRADE: Graph Representation of LLM Agent Dependency and Execution.* The PDF typesets it as "Grade".
- **Author:** Yue Zhao (University of Southern California). Single author.
- **arXiv:2606.22741**:
  - v1: 22 Jun 2026; v3: 6 Oct 2026; cs.LG.
  - Comment: "35 pages. Expanded analyses and revised figures."
  - Code: github.com/yzhao062/grade.
  - **[verified: arXiv API]**
- **Venue:** none found. The text mentions "anonymized supplementary material", which suggests a review submission. The OpenReview API2 search returned nothing, and DBLP blocked automated access. **Treat as a preprint.**
- **Read:**
  - v3 PDF in full: §§1–7, Limitations, Ethics, references.
  - Appendices A (formal tuple), B, C.1–C.8, D.1–D.2, D.5–D.10, E, F, G, H, I, J.
  - D.3–D.4 and the D.6–D.7 tables were skimmed (prose read, numbers spot-checked).
  - Figures 1–5 and A1–A4 were read via caption and extracted labels only.

### Problem & contribution
- **Problem.** Traces record what agents *did* but not what each step *relied on*.
- **Contributions:**
  1. A two-layer graph G = (V, E_X, E_D, τ, t, σ). E_X are free execution edges (emit, handoff). E_D are costly dependency edges ("step v used state produced or held by the earlier node u"). σ grades each dependency edge as **observed / declared / inferred**. Six published graph views (ReAct traces, MetaGPT, GPTSwarm, computation graphs, PROV/lineage, agent anomaly graphs) are shown to be projections of this graph.
  2. An evaluation protocol: grade each edge, keep a run-size baseline, and score **degree-matched counterfeit** dependency layers.
  3. Empirical findings on the failure-prediction gain over run size.

### Method
- **Unit:** an agent **run** (trajectory). Nodes are agents, decisions, tool calls and resources. There is no decision-episode unit, although "decision" is a node type.
- **The three grades (§2.1), verbatim:**
  - "An edge is **observed** when the trace shows the access it records".
  - "It is **declared** when added logging records the reads and writes a raw trace omits."
  - "Where no access is logged, an edge is **inferred** under a named assumption, the weakest being full history: each step used every earlier step."
  - So "declared" = **instrumentation-declared**, not agent-declared. App. G: "Logging each step's reads and writes … is what carries an edge from inferred to declared."
- **Provenance of the edges actually used:**
  - "Every dependency edge in the six corpora is observed" (§4.1).
  - The declared grade is **never tested at event level**. The only "declared" probe is App. F, on FLORA-Bench *workflow* graphs emitted by a planner or program, at agent granularity and sometimes cyclic.
  - Even observed edges come from **heuristic attachment rules**:
    - tau-bench: a write attaches to every prior DB read, as an upper bound;
    - file and web corpora: the most recent earlier access to the same resource;
    - tau2-bench: identifier-keyed.
  - §4.1: "An observed edge records shared access to a resource, not proven reliance."
  - App. H: "ground-truth reliance labels do not exist at scale for any agent corpus."
- **Mixed grades:** "We evaluate each grade only as a whole layer; mixed-grade graphs are untested" (§2.1).
- **"Interventions":** none on the agent or its evidence. The controls are **statistical null models on the graph**:
  - n0: a reading-free chain;
  - n1: uniform rewiring, edge count kept;
  - n2: **degree-matched**, which keeps each step's number of earlier sources and rewires which ones (following Maslov–Sneppen, Váša–Mišić and Hewitt–Liang control tasks);
  - n3: recency.
  - These test whether the *attachment* (which earlier step) carries predictive signal beyond the *degree sequence*.
- **Features:**
  - density |D|/n;
  - depth (longest chain / n);
  - blast (the largest share of the run that relies on one step);
  - audit (the largest share of the run that one step relies on).
  - Density and audit **cannot move** under n2 or n3. This limits what the counterfeit test can detect, as GRADE notes in §4.2.
- **Learner:** standardized logistic regression, ROC-AUC, 5-fold CV × 5 seeds; also spline, GBT, GIN, R-GCN and HGT.

### Evaluation
- **Corpora:** tau-bench (660 runs), SWE-agent (600), SWE-Gym (376), OpenHands (600), tau2-bench (278), AgentRewardBench web (600). Who&When (126 failed runs) is used for execution-layer localization only.
- **Within-corpus gain over the linear run-size baseline (Table 2):**

  | Corpus | Gain (Δ AUC) |
  |---|---|
  | tau-bench | +0.046 |
  | SWE-agent | +0.085 |
  | SWE-Gym | +0.142 |
  | OpenHands | −0.004 |
  | tau2-bench | −0.015 |
  | web | −0.009 |

  - Under task resampling, only SWE-Gym's gain keeps an interval above 0.
  - Under task-grouped folds, SWE-agent's gain becomes −0.011.
  - Under flexible size baselines (B1: 1/n, log n) only tau-bench survives. SWE-Gym's gain turns negative (App. C.6).
- **Preregistered counterfeit test (§4.2, Table 3, Fig. 3):** recovered layer minus degree-matched counterfeit, d.
  - Six-corpus mean **−0.0003**.
  - Best is tau-bench, +0.011 (p = 0.08; Holm-adjusted 0.54).
  - **Neither preregistered prediction held.**
  - A chain that reads nothing beats the recovered layer on 3 of 6 corpora.
- **Transfer (pooled leave-one-corpus-out, logistic):**
  - Dependency features stay above chance on all six held-out corpora; run size inverts on tau-bench (0.436) and SWE-Gym (0.359).
  - Against the counterfeit in transfer, there are nominal separations on 3 corpora, and only SWE-Gym survives Holm.
  - With the **whole task family withheld**, there is no positive separation on any new target, and SWE-Gym reverses (−0.036, surviving Holm) (App. D.7).
- **Full-history inferred layer:** it "restates run size" (|r| up to 0.99; 1.00 on Who&When). The saturation ratio ρ = |E_D| / C(n,2) flags this but "certifies nothing" when small (§5.1).
- **Execution-layer localization on Who&When:**
  - Top-3: 0.614 vs position prior 0.516.
  - Top-1: 0.211 vs 0.159; this gain does not survive a run-level bootstrap.

### What it covers that WorkTrace must NOT claim
- A typed two-layer graph of runs that separates execution from dependency, with a **per-edge epistemic grade** (how an edge is known: observed / instrumentation-declared / assumed).
- The warning that graph structure "can pass for signal it does not carry", including saturated inferred layers that encode run length.
- The **degree-matched counterfeit control** for dependency graphs in agent traces, and the protocol "grade each edge, keep a run-size baseline, score degree-matched attachment controls".
- The empirical finding that static dependency structure adds little and fragile failure-prediction signal beyond counts. This supports our H2 rather than threatening it.

### What it leaves open that WorkTrace addresses
1. **Agent-stated grounds:** GRADE has no notion of them at all.
2. **Causal use:** no test of whether any edge is causally *used*. The grade is about how an edge is known, not whether the decision depends on it. GRADE concedes that observed edges are not "proven reliance" and that ground-truth reliance labels do not exist. WorkTrace provides both:
   - ground truth by construction (the generator knows the decisive evidence);
   - interventions on external evidence with the agent held fixed and re-run.
3. **Unit:** the unit is the run and the target is run failure. There is no decision episode, no information-available-at-decision-time slot, no permissions slot, and no delegation.
4. **Redundancy:** not addressed. Edges are binary access relations.

### Draft differentiation sentence
> GRADE grades each dependency edge in an agent trace by how it is known (observed in the trace, declared by added logging, or inferred under an assumption) and tests whether such structure predicts run failure beyond run size against degree-matched counterfeit graphs; it does not test whether any edge is causally used, whereas WorkTrace treats the agent's own stated grounds as hypotheses and tests them by intervening on the external evidence available at a decision, with the decisive evidence known by construction.

### Citation cautions
- Single-author preprint (v3). Most headline results are **nulls or fragile gains**, and the author states this carefully. Do not cite it as showing "dependency structure predicts failure" without the caveats.
- **"declared" ≠ our "declared".** Quote §2.1 when we cite it.
- Its two-sentence related-work mention of EDGE (Hou et al., arXiv:2609.01360 **[verified arXiv]**) is relevant to us. EDGE "distinguishes observational propagation edges from intervention-validated edges", using counterfactual rollout and an edge-count-matched random control. That is intervention validation of *error* dependency edges for attribution, not of decision grounds.
  - **I read only EDGE's abstract** (via the arXiv API). Add it to the next reading list as a possible reviewer comparison for "intervention-validated vs. observational edges".
- It also cites Sun & Kazakov (arXiv:2605.25310 **[verified arXiv]**, abstract only). Tool-call dependency structure is linearly decodable from residual streams, **but activation patching does not move the realised tool call**. This is a useful citation for "representation ≠ behavioural dependence". Abstract only.

---

## 2. An Evidence Model for Agentic Processes (Brömme, 2026) — NEW

### Bibliographic data
- **Title:** *An Evidence Model for Agentic Processes: Evidence Claims, Trust Assumptions, and Policy Assessment.*
- **Author:** Arslan Brömme (Independent Researcher; aviomatik.de). The PDF lists certifications CISSP, CISM, CISA and CAISE.
- **arXiv:2609.08481v1** (8 Sep 2026, cs.CR). Comment: "7 pages, 1 table". The PDF header says "Draft v0.9.0.6 – 8 September 2026 … Preprint / working paper. This version is a work in progress". **[verified: arXiv API]**
- **Venue:** none. It is a working paper.
- **Companion (prior) paper:** Brömme, *A Black Box for Agentic Processes: Blockchain-Anchored Evidence for AI Agent Communication, Human Oversight, and GRC Audits*, arXiv:2609.04017v1 (3 Sep 2026, 5 pp.). **[verified: arXiv API; abstract only, not read]**
- **Read:** the full PDF, §§1–10, Table 1, the example records in §§5 and 8, the references, and the AI-use declaration. No figures.

### Problem & contribution
- **Problem:** logs, hashes, signatures and anchors are easily over-read. "a hash does not establish semantic truth, a signature does not establish authorization, and an external anchor does not establish capture completeness" (Abstract).
- **Contributions** (explicitly "conceptual"; "does not … automate legal compliance"):
  1. An **evidence claim** model, claim = (event, property, mechanism, assumptions, limitation, threat scope) (§5).
  2. **Table 1**, which maps 14 mechanisms to claims, trust assumptions and limitations.
  3. An **agent organization**: a CEO agent; executive agents; operational agents; Logger / Historian / Evidence Supervisor / Evidence Controller / Anchoring Service; and an Audit-agent. These are wrapped in a **PDCA management loop**.

### Method
- **Units:**
  - the *event* (agent message, human approval, tool call, policy exception, decision-session record, audit finding, risk-treatment record, mitigation record, management decision);
  - the *claim* about an event.
- **"Evidence" here is forensic/audit evidence about records, not epistemic evidence a decision should depend on.** This is the key distinction for us.
- **Decision sessions (§3, §7, §8):**
  - "Before high-impact or policy-sensitive actions, an agent organization may convene agentic decision sessions in which specialized agents discuss a decision" (§7).
  - The record holds "topic, participants, inputs considered, policy context, arguments, dissenting views, confidence levels, required approvals, and outcome".
  - Table 1 row "Decision session record": the claim is *deliberation traceability*; the trust assumption is "Required participants and decision rules are defined and enforced"; the limitation is "**Does not create organizational authority by itself.**"
  - §7: "An agentic decision session does not create organizational authority by itself. It creates a documented decision process … Legal, managerial, or policy authority remains with the responsible human role".
- **Authority and delegation:**
  - Executive agents "accept or reject risks within delegated authority" (§3).
  - "Binding legal authority remains with the responsible human officer or legal entity."
  - In the Act phase the CEO and executive agents "update policies, workflows, agent communication rules, **tool permissions**, or propose residual-risk acceptance for human ratification" (§7).
  - Approval evidence assumes "authorization scope, validity interval, delegation state … are separately verifiable" (Table 1).
- **Self-report:** "self-reporting by operational agents is useful, but insufficient. It creates a self-reporting claim, not a completeness guarantee" (§4.1). "An audit-agent finding is therefore a claim, not a ground truth" (§4.3).
- **Only quantitative element:** mandatory-event coverage C = M / N_expected, where N_expected must come from an independently defined expectation model (§4.3).
- **Policy assessment:** the audit-agent emits a "signed policy-assessment claim over selected records". Example: "a privileged tool call was preceded by a recorded human approval under policy AI-GOV-07". These are **structural/procedural checks**, like Auditable Agents' structural policies.
- **Semantic validity** is "a recurring limitation" throughout. There is no test of whether stated rationale is true or causally used.

### Evaluation
None. "This position and architecture paper does not present an empirical performance, security, or compliance evaluation" (§1). One illustrative remediation workflow is given (§8).

### What it covers that WorkTrace must NOT claim
- That records of decisions (inputs considered, rationale, dissent, uncertainty, approvals, policy version) should be kept for agentic decisions, especially before high-impact actions.
- A claim/assumption/limitation vocabulary for what agent records can and cannot support, with explicit separation of record integrity, provenance, approval and authorization.
- A management loop in which audit findings lead to changes in **tool permissions** (with human ratification).
- The point that recorded deliberation does not create authority, and that agent self-report is not completeness.

### What it leaves open that WorkTrace addresses
1. **Linking evidence to authority:** no evidence → autonomy link. Permission changes are driven by audit findings (policy deviations, missing approvals, prompt-injection exposure) and ratified by humans. They are not derived from tested behaviour or estimated per decision class.
2. **Unit:** no decision-class unit. The unit is an event or record class (approval, decision session, …). "High-impact" is mentioned but not operationalised.
3. **Construct:** no DSA-like construct. The organisation's roles are functional. There is no measure of whether an agent's decisions have decision structure.
4. **Semantic validity:** declared as out of reach. WorkTrace supplies a mechanism that supports exactly one of the claims the model marks as unsupported: that a recorded rationale corresponds to what the decision depends on. This is the intervention test. **This is a clean way to position WorkTrace inside this vocabulary**, as a new row of Brömme's Table 1:

  | Mechanism | Supported claim | Trust assumption | Limitation |
  |---|---|---|---|
  | Evidence interventions (remove / only / invert / second source) on a fixed decision point | Grounding claim: the decision's response to the evidence matches its declared grounds | The generator's ground truth is correct; the interventions are semantically valid | Holds for the tested distribution of episodes; does not establish legal sufficiency |

### Draft differentiation sentence
> Brömme's evidence model specifies which evidentiary claims an agentic "black box" can support (integrity, provenance, approval, deliberation traceability, policy assessment) and explicitly leaves semantic validity untested, noting that a recorded decision session "does not create organizational authority by itself"; WorkTrace adds a mechanism for the missing claim — that a decision's recorded grounds are the evidence it actually depends on — and uses that claim, per decision class, as the basis on which authority is granted or withdrawn.

### Citation cautions
- Single-author, independent, unreviewed working paper ("v0.9.0.6"), 7 pages, conceptual only. It declares that GPT-5.6 and Claude Sonnet 5 were used for "language drafting, critical review, source checking …".
- Cite it as a governance/evidence-semantics framing, not as evidence of anything.
- The decision session involves *multiple specialized agents plus humans*. Do not describe it as a single-agent decision record.

---

## 3. Agent Safety Is Action Alignment (Li & Zhao, 2026)

### Bibliographic data
- **Title:** *Agent Safety Is Action Alignment.*
- **Authors:** Shawn Li, Yue Zhao (University of Southern California).
- **arXiv:2606.28739v1** (27 Jun 2026, cs.AI). **[verified: arXiv API]** Only v1 exists.
- **Venue:** none. The PDF uses the unfilled ACM template placeholder "Conference'17, July 2017, Washington, DC, USA". **Preprint (position paper).**
- **Read:** the full PDF (9 pp. including references): §§1–7 and references. Figure 1 was read via its extracted labels and caption. The two-column extraction scrambled some ordering in §§4–5; I reconstructed it by section headings.

### Problem & contribution
- **Position:** importing refusal training (a content-safety primitive) into agent safety is a "category error". Agentic harm "lies not in any output but in the relation between the authority an action exercises and the authority the user granted, which is absent from the text the model sees" (Abstract).
- **Contributions:**
  1. Content vs. action safety, distinguished by where harm resides (§3.1).
  2. A **multi-coordinate formalisation** (§3.3).
  3. Three lines of evidence, organised as corollaries plus two falsifiable claims (§4).
  4. A programme: least privilege, external enforcement, relational evaluation (§5).

### Method (formalism)
- **Content harm vs. action harm:** content harm is h_c(out(a)). For actions, "the action is over-privileged when auth(a) ⊈ A" (§3.1). A second source of action harm is *provenance*: whether a realizes the user's intent or an injected instruction.
- **Action alignment (§3.3, Eqs. 1–3):**
  - C(a) = 1[a accomplishes intent i] — **competence**
  - R(a) = 1[auth(a) ⊆ A] — **restraint**
  - B(a) = 1[¬adv(a)] — **resistance** to adversarial or injected control
  - S★(a) = C ∧ R ∧ B.
- **Projection argument:** the prevailing metric S_field is a function only of (ref(a), y). Responses a and a′ can have identical (ref, y) but different R. So "the refuse–comply axis is provably blind to over-privilege". Table 1 summarises this as an auditor question per coordinate.
- **Least privilege (§5.1):** "a bound on [the action's] scope, with refusal the degenerate empty-scope case": "over-refusal is under-privilege, over-reach is over-privilege".
- **External enforcement (§5.2):** "an external reference monitor checks it against the grant and the provenance of the controlling instruction, then **permits, narrows, or escalates to a human**."
- **Open problems (§6):**
  - (1) "Specifying authority: how to express A for open-ended tasks, and how much can be inferred versus must be declared";
  - (2) "ground-truth least-privilege references";
  - (7) "Delegation: how the grant A propagates when an agent spawns sub-agents".
- **A is treated as given and static.** There is no mechanism for changing A over time or from evidence.

### Evaluation
- **No new experiments.** All numbers are re-read from the authors' earlier work:
  - [19] *Defenses Against Prompt Attacks Learn Surface Heuristics*, arXiv:2601.07185 **[verified arXiv]**; ACL 2026 per the authors' reference, venue **[unverified]**;
  - [20] *FORTIS: Benchmarking Over-Privilege in Agent Skills*, arXiv:2605.09163 **[verified arXiv]**;
  - [21] *The Autonomy Tax: Defense Training Breaks LLM Agents*, arXiv:2603.19423 **[verified arXiv]**.
- **Cited figures:**
  - a defense-trained model executes the injected deletion 78% of the time;
  - defended models fail at step 1 on 47–77% of benign tasks vs 3% for the base model;
  - timeouts rise from 13% to 99%;
  - a single trigger token raises false refusals by up to 50%;
  - undefended frontier models misroute more than 1 in 3 skill requests;
  - end-to-end least privilege holds for under 15% of requests;
  - models abstain on under 1.5% of cases and "err toward more authority".

### What it covers that WorkTrace must NOT claim
- The **authority-gap formalisation** R(a) = 1[auth(a) ⊆ A], and the framing of agent safety as relational (deployment-conditioned) rather than a property of outputs.
- A multi-coordinate safety construct ("action alignment") that explicitly separates task success from staying within authority.
- The argument that outcome success can coexist with violated restraint ("the task succeeding while quietly exercising more authority than granted").
- External enforcement with a **permit / narrow / escalate** decision at the action boundary. With Aegis (via Auditable Agents), this is the second source for a proceed/refuse/escalate-style gate.
- The empirical claim (via FORTIS) that over-privilege is the norm under ordinary use and that models rarely abstain.

### What it leaves open that WorkTrace addresses
1. **Where A comes from.** A is exogenous and static. How much authority to grant, per what unit, on what evidence, and when to withdraw it is not addressed. Open problem (7) concerns propagation to sub-agents, not earning or revoking.
2. **Grounding is not a coordinate.** S★ scores a correct, in-scope, non-injected action as aligned **even if it was taken on the wrong evidence**. Their own projection argument applies one level up: any delegation rule that is a function of (C, R, B), or of outcomes only, is blind to the basis of the decision. WorkTrace's loss ("right action on the wrong basis") is exactly the coordinate S★ drops.
3. **Escalation and uncertainty.** "Escalate" appears only as a reference-monitor action, not as a behaviour of the agent to be measured. Agent-initiated escalation and abstention appear only as a symptom ("abstaining on under 1.5% of cases").

### Can we adopt R for DSA's "stay within authority scope" dimension? Yes, with four refinements.
1. **Separate two A's.**
   - A_task is the authority the episode grants. It is an explicit field of E (permissions), fixed by the generator.
   - A_c is the autonomy our delegation rule grants for decision class c.
   - Restraint, as a DSA dimension, is measured against A_task and is an input to the rule. The rule's output is A_c. Mixing the two makes the rule circular.
2. **Separate explicit and implicit restraint.**
   - Explicit restraint: auth(a) ⊆ A_task when A_task is stated in the agent's input.
   - Implicit least privilege: the agent chooses the minimally sufficient authority when A is not stated, as in FORTIS.
   - Li & Zhao's thesis is that A "is absent from the text the model sees". In our episodes it is present, so we measure a different (easier) thing and must say so.
3. **Measure attempted over-reach, not only executed over-reach.** Their prescription is mechanical enforcement outside the model. Under our hard ceiling (Earned Authority 2607.23586), executed over-reach is blocked anyway.
   - The DSA signal should therefore be *attempted* over-reach (blocked calls), plus **decision-scope over-reach**: deciding a matter reserved for a human, such as AMLR art. 76(5)(b) classes, which a reference monitor can only block if the class is labelled.
   - We should answer the obvious reviewer objection ("why measure restraint if a monitor enforces A?") in these terms.
4. **Authority needs an order.** auth(a) ⊆ A requires an authority lattice (actions × data scope × thresholds). We need a small, explicit lattice per domain, e.g. counterparty verification: {request document, flag, approve ≤ threshold, approve > threshold, reject, escalate}. Their open problem (2), ground-truth least-privilege references, is something our generator can supply by construction.

**Design idea:** the "narrow" option. Their monitor can *narrow* an action rather than only permit or escalate. Our per-class rule could add "proceed with narrowed scope" (e.g. proceed for preparatory steps, escalate the binding step). This matches our existing plan to delegate preparatory steps of legally reserved classes.

### Draft differentiation sentence
> Li and Zhao formalise agentic harm as the gap between the authority an action exercises and the authority granted, R(a)=1[auth(a)⊆A], and define action alignment as competence, restraint and resistance to injected control, with A given and enforced outside the model; WorkTrace adopts R as one coordinate of decision-structured agency but adds the coordinate their construct omits — whether the action rests on the evidence that should determine it — and makes the granted authority itself a per-decision-class, revocable output of tests on that coordinate.

### Citation cautions
- Short position paper. It has no venue, no new data, and only self-citations for its evidence. Cite it for the formalism and framing, not for the numbers. For numbers, cite FORTIS and The Autonomy Tax directly, after reading them; I read only their abstracts.
- "Provable blindness" is a two-line argument (a metric that is not a function of X cannot distinguish values of X). Do not overstate it as a theorem.
- "Provenance" in their usage = the trust level of the channel an instruction came through. In DSA, "preserving provenance" = keeping track of evidence sources. Do not conflate the two.

---

## 4. CatchBench (Zhao et al., 2026)

### Bibliographic data
- **Title:** *CatchBench: When Can an Agent Failure Be Caught?*
- **Authors:** Yue Zhao, Mengyuan Li, Ruolin Li, Prince Zizhuang Wang, Shuli Jiang, Linsey Pang, Xiongye Xiao, Xiyang Hu.
  - Affiliations: USC, CMU, AWS Agentic AI, PayPal AI, U. Tennessee Knoxville, Arizona State.
- **arXiv:2608.22808**:
  - v1: 24 Aug 2026; v4: 17 Sep 2026; cs.LG.
  - Comment: "55 pages, 15 figures, 27 tables. Updated author list, analyses, and presentation."
  - Code: github.com/yzhao062/catchbench.
  - **[verified: arXiv API]**
- **Venue:** none found (OpenReview API2 search empty). The format looks like ICLR-style. **Preprint.**
- **Read:**
  - v4 main text in full: §§1–6, Reproducibility, Ethics, AI-use statement.
  - App. A (extended related work) in full; App. B introduction and Table 3; App. C (entrant adaptations).
  - App. E (PRE corpus, label processes, scanner diagnostics; partially); App. G (Gold admissibility bar and construction) in full.
- **Not read:**
  - the 138-row comparison table (Table 4);
  - App. D (full board values) beyond spot checks;
  - App. F (corpus composition) and App. H (artifact detail).
  - Figures read by caption only.

### Problem & contribution
- **Problem:** "A weak audit score alone cannot identify whether the record or the method is limiting."
- **Contributions:**
  1. An arena that scores one auditor's question at three **information states**:
     - **PRE**: the declared configuration (plan + harness) before a run;
     - **LIVE**: a growing trace prefix;
     - **POST**: the finished trace.
  2. Seven task contracts, nine scored boards, 72 entrants.
  3. A PRE corpus where every record carries its label-process tag.
  4. An **admissibility bar** for injected faults, which its own injected data did not clear.

### Method
- **Unit:** an auditor scored on a task contract. Subjects are configurations (PRE) or runs (LIVE/POST). The information state is the **auditor's** information budget, not the agent's.
- **Boards:**
  - **PRE over-privilege:** does a declared harness grant capabilities the task does not need? Threat model: OWASP LLM06:2025 Excessive Agency. 1,187 configs from six sources, four label processes: cross-vendor LLM judging; roster relabelling; declared-minus-used from paired SWE-agent traces; synthetic over-grant.
  - **LIVE early warning:** 25/50/75/100% prefixes on SWE-Gym and tau-bench.
  - **LIVE online stale-state detection:** Gold, diagnostic only.
  - **POST localization:** Who&When, 126 runs.
  - **POST detection:** SWE-Gym, tau-bench.
  - **POST Gold localization and cause attribution:** diagnostic only.
- **CatchBench-Gold injections (§4.3, App. G)** edit the *recorded* dependency graph or argument values:
  - **stale-state read**: redirect a dependency to an earlier, superseded event on the same resource;
  - **dropped grounding**: remove one required dependency.
  - Gold v2 mutates a real argument value from a same-key donor and rebuilds the edges.
  - **The agent is not re-executed.** The edited trace is a test item for auditors.
- **Admissibility bar, five items:**
  1. fault realism;
  2. no artifact leakage (no construction-only baseline wins);
  3. distributional validity;
  4. non-circular labels;
  5. human validation on an airtight substrate.
  - **Results:** File-level Gold **fails item 2**: a "broken-predecessor" rule ranks 82/82 stale and 106/106 dropped targets Top-1 and flags 0/188 clean runs. Gold v2 is undetermined on items 1–3, and neither substrate has met item 5. Both Gold boards therefore "carry no evidential weight".
- **Statistics:**
  - Every comparison is printed as a difference with a marginal 95% interval: paired DeLong, exact McNemar, a task-clustered bootstrap for tau-bench (165 tasks × 4 models).
  - No family-wise control is claimed, and "no board declares a winner it cannot show".

### Evaluation (key numbers)
- **PRE:**
  - flag-all F1 0.601; combined token scanner 0.654;
  - held-out LLM judge 0.695 vs scanner 0.648 on 1,182 shared configs (+0.048 [0.021, 0.074]);
  - **a position-only rule scores F1 = 1.000 on injecagent**, because "the capability a task needs is always declared first".
- **LIVE:**
  - On SWE-Gym at 25%, the dependency-aware model gets 0.742 vs linear size 0.629. Against a size-only spline (0.794 at 25%) the matched contrast is +0.005 [−0.010, +0.020], which is unresolved.
  - On tau-bench, no entrant reaches the 0.70 warning bar at any prefix.
- **POST localization:**
  - GPT-5.5 reaches 0.452 Top-1; the best structural method reaches 0.211.
  - The benchmark cannot order its top judges.
  - GRADE's execution ranker beats position on Top-3 (+0.098 [0.035, 0.167]) but not on Top-1.
- **POST detection:**
  - SWE-Gym dependency gain: +0.147 with a linear size control vs −0.005 [−0.026, +0.015] with a matched spline.
  - tau-bench: +0.046 vs +0.045.
  - G-Safeguard 0.824 ± 0.007 vs the full feature model 0.819 ± 0.005; the interval on the difference contains 0.
  - ECOD on flat features ≈ GUARDIAN adaptation.

### What it covers that WorkTrace must NOT claim
- Structuring audits of agents by **information available to the auditor** (before / during / after a run), with one task-method interface.
- PRE-state **over-privilege detection** on declared configurations against task-relative least-privilege labels. AuthBench, ToolPrivBench and FORTIS do the same from other angles.
- Injecting "stale-state read" and "dropped grounding" faults into real traces as known-label test items, together with an explicit admissibility bar for synthetic faults.
- The methodological warnings:
  - a declaration-order shortcut can make a score measure corpus construction;
  - structural gains must be checked against flexible size controls.

### What it leaves open that WorkTrace addresses
1. **Whose information is varied.** The information states are about **what the auditor sees**. None concerns **what the agent had at decision time**, or whether the agent's decision depends on it.
2. **What is evaluated.** Its interventions are edits to records for evaluating detectors, not interventions on the agent's evidence with the agent re-run. A "dropped grounding" here means the *trace* lacks an edge, not that the agent acted without the evidence.
3. **What audits are for.** Audits catch failures; nothing grants or withdraws autonomy. "A full excessive-autonomy check requires an approval-gate field, which the schema does not carry" (App. E.1). Autonomy is explicitly outside its PRE schema.
4. **Unit and grounding.** There is no decision-class unit and no notion of right-for-the-right-reasons.

### Mapping its information states to our episode E
- **Agent side.** Our "information available at decision time" I_t is the agent-side analogue of LIVE-at-t, restricted to the evidence the agent could read, not the auditor's view of the trace.
- **PRE.** CatchBench's PRE (declared plan + harness capabilities) corresponds to our **permissions** slot plus the task context.
- **POST.** POST corresponds to our "observed consequences" plus the full trace.
- **Where the delegation rule sits.** Granting autonomy for the next episode is a **PRE-state decision** about the agent (made before the run, from POST evidence on past episodes), and the runtime gate is a LIVE decision. **We should state explicitly which information state each WorkTrace component uses.** CatchBench gives us vocabulary and a citation for doing so.

### Draft differentiation sentence
> CatchBench scores auditors of agent runs at three information states (the declared configuration, a live prefix, the finished trace) and injects stale-state and dropped-grounding faults into recorded traces as known-label test items; WorkTrace instead varies the evidence available to the agent itself at a decision point and re-runs the agent, measuring whether its decision depends on that evidence, and uses the result to decide what the agent may do before its next run.

### Citation cautions
- Unreviewed preprint (v4). It is self-critical and statistically careful, but it covers many heterogeneous boards and has no family-wise control (by design).
- The Gold boards explicitly carry **no evidential weight**. Do not cite them as evidence that stale-state or grounding faults are detectable.
- The PRE labels are mostly LLM-judged (cross-vendor κ = 0.666 overall). "Unused in one observed run is only a proxy for unneeded."
- The text references model names (GPT-5.5, Claude Opus 4.8, GPT-6 Astra, Claude Opus 5). Those numbers are single-generation and seedless (App. B), so do not quote judge rankings.

---

## Answers to the key questions

**(a) GRADE: are declared edges tested for causal use, or only graded by provenance type? How close is it to us?**
- **Only graded by how they are known.**
- There is no intervention on evidence, no re-execution, and no test of causal use. The controls are graph null models (degree-matched rewiring) for a *prediction* task.
- "Declared" means instrumentation-logged reads and writes, and that grade is not even exercised at event level. All six corpora use observed edges.
- **Distance from WorkTrace: far in method, close in vocabulary.** It actually *supports* our premise and H2:
  - it concedes that observed edges are not proven reliance;
  - it concedes that no ground-truth reliance labels exist;
  - its preregistered tests find that static attachment adds nothing measurable within corpus beyond degree.

**(b) 2609.08481: does it link evidence to granting authority or autonomy? Any decision-class unit or DSA-like construct?**
- **No to all three.**
- Its "evidence" is evidentiary support for claims about records. Authority stays with humans and is not created by records. Permission updates happen in a PDCA loop from audit findings, with human ratification.
- There is no decision-class unit (only event and record classes, plus informal "high-impact" decisions) and no capability construct.
- The overlap is limited to *recording* deliberation (inputs considered, rationale, dissent, uncertainty) before high-impact actions, and to the principle that self-report is a claim, not proof.

**(c) Action Alignment: can we adopt the authority-gap formalism for the "stay within authority scope" DSA dimension?**
- **Yes.** Adopt R(a) = 1[auth(a) ⊆ A] as the definition, with four refinements:
  1. separate A_task (an input) from A_c (the rule's output);
  2. separate explicit restraint from implicit least privilege;
  3. measure attempted over-reach and decision-scope over-reach, because enforcement blocks executed over-reach;
  4. define an authority lattice per domain.
- Cite it as the source of the formalism, and note that S★ lacks a grounding coordinate.

**(d) CatchBench information states vs. our "information available at decision time".**
- **Different subject.**
- CatchBench varies the **auditor's** information (PRE / LIVE / POST). Our I_t is the **agent's** information at a decision point, and we intervene on it.
- The vocabulary is useful for stating where each WorkTrace component sits:
  - the delegation rule is a PRE decision informed by POST evidence on past episodes;
  - runtime gating is LIVE.
- Its strongest lessons are methodological: label-process tagging, the declaration-order shortcut, and the admissibility bar.

**(e) Differentiation sentences:** see each work. One line in common: GRADE grades *how a dependency is known*; Brömme specifies *what a record can prove*; Li & Zhao define *whether an action stays within granted authority*; CatchBench measures *when an auditor can catch a failure*. WorkTrace tests *whether a decision depends on the evidence it claims*, and sets per-class authority from that.

---

## Implications for WorkTrace

### Novelty status
- **No falsification of W1, W2 or W3.**
- **W2 (evidence-basis tests):** unaffected. None of the four intervenes on agent-side evidence with the agent re-run, and none has an "add an independent second source" design.
- **W3 (per-class delegation):** unaffected. None grants or revokes autonomy from tested behaviour. Brömme's tool-permission updates and Li & Zhao's permit/narrow/escalate monitor are the nearest, and both take authority as externally set.
- **DSA as a construct:** no existing named construct has the same content.
  - "Action alignment" (Li & Zhao) is a proper sub-construct on the authority/injection side.
  - "Deliberation traceability" (Brömme) is a record property, not a capability.
- **Watch item:** the Zhao group (Auditable Agents, GRADE, CatchBench, Action Alignment, FORTIS) is one step from "authority granted from audit evidence". Re-check their arXiv output before submission.

### Writing changes
1. **Terminology.**
   - Always write "agent-declared grounds" or "stated grounds". Add a footnote: "not GRADE's *declared* grade, which denotes dependency edges recorded by added instrumentation (Zhao, 2026, §2.1)".
   - Avoid "information state" for I_t, or cite CatchBench and say ours is agent-side. Suggested name: "decision-time information set".
2. **Related-work paragraph on authority:** cite Li & Zhao for R(a) and the projection argument. Then state that DSA = {grounding, uncertainty/contradiction boundary, restraint (R), escalation, revision, provenance}, and that outcome- or (C, R, B)-based delegation rules are provably blind to grounding by the same argument.
3. **Related-work paragraph on records and evidence:** Brömme, Audit Trails, Auditable Agents, Solozobov. Records support claims about *what was stated or approved*. WorkTrace adds the mechanism that supports a *grounding claim*. Optionally present it as an extra row in Brömme's claim table (see §2).
4. **H2 support:** cite GRADE's null against degree-matched counterfeits and its "not proven reliance" concession, alongside Causal Sensitivity Score, as evidence that static graph inspection is a weak substitute for intervention.

### Design changes
1. **Degree-matched counterfeit control for the declared-grounds graph (from GRADE).** When testing H3 (whether the DSA profile predicts held-out outcome errors), add a control profile computed from a counterfeit grounds graph. It keeps the *number* of declared grounds per decision and rewires *which* evidence items they point to. If the predictive validity of DSA survives this control, the signal comes from *which* evidence, not from how many grounds the agent lists. A reviewer from the GRADE line will ask for this.
2. **Flexible size controls (from GRADE and CatchBench).** Report DSA's predictive validity against outcome-only and history-counter rules *and* against a flexible (spline) function of episode size: number of evidence items, steps, tool calls. CatchBench shows that a +0.147 linear gain can become −0.005 under a spline.
3. **Construction-shortcut audit of the generator (from CatchBench).** Before any result:
   - run a "position-only / format-only" rule that reads the *position, order or formatting* of evidence items but not their content, and show that it cannot predict the decisive item or the correct action;
   - tag every episode with its label process.
   - The injecagent case (F1 = 1.000 from declaration order) is exactly the failure mode a template generator invites.
4. **Admissibility bar for our interventions (adapted from CatchBench §4.3).** Every intervention type should clear five checks:
   1. it maps to a documented real-world evidence failure (stale, contradictory, single-source, missing);
   2. no construction-only baseline detects the intervened episodes;
   3. intervened and clean episodes are distributionally comparable on surface statistics;
   4. labels are fixed by the generator, independent of any evaluator;
   5. a human-audited slice confirms semantic validity.
   - This fits our existing "pre-registered intervention catalogue with semantic validity control" and strengthens it with a named, citable precedent.
5. **Authority lattice and two A's (from Action Alignment).**
   - Define auth(·) over an explicit per-domain lattice.
   - Keep A_task (an episode input) separate from A_c (the rule's output).
   - Measure attempted and decision-scope over-reach.
   - Consider a fourth rule outcome, "proceed narrowed" (delegate the preparatory steps, escalate the binding step), which matches Li & Zhao's permit/narrow/escalate monitor.
6. **State the information state of each component (from CatchBench).**
   - The grant/revoke decision is PRE for the next episode.
   - Evidence for it is POST on held-out episodes.
   - Any runtime gate is LIVE.
7. **Emit grant/revoke decisions as evidence records with explicit claims and limitations (from Brömme).** For example, claim: "class c certified at α_c on n episodes"; assumption: "generator distribution matches deployment"; limitation: "does not establish legal sufficiency". This links us to the GRC audience.

### Risks
- **"Isn't this just action alignment plus a grounding check?"** Reply: the construct is the grounding/escalation/revision structure, and the contribution is using it to *set* A. Action alignment takes A as given.
- **"CatchBench already injects dropped-grounding faults."** Reply: those are trace edits for testing auditors, the agent is not re-run, and the substrate failed their own admissibility bar.
- **"GRADE already has declared dependency edges."** Reply: there, "declared" means instrumentation-logged, untested at event level, with no causal test.

### To cite (all verified via the arXiv API)
- **Read in full:**
  - Zhao 2026, GRADE, arXiv:2606.22741
  - Brömme 2026, arXiv:2609.08481
  - Li & Zhao 2026, arXiv:2606.28739
  - Zhao et al. 2026, CatchBench, arXiv:2608.22808
- **Abstract only:**
  - Li et al. 2026, FORTIS, arXiv:2605.09163
  - Li & Zhao 2026, The Autonomy Tax, arXiv:2603.19423
  - Li et al. 2026, Defenses Against Prompt Attacks Learn Surface Heuristics, arXiv:2601.07185
  - Brömme 2026, A Black Box for Agentic Processes, arXiv:2609.04017
  - Hou et al. 2026, EDGE, arXiv:2609.01360
  - Sun & Kazakov 2026, arXiv:2605.25310
  - Zhou et al. 2026, Counterfactual Trace Auditing of LLM Agent Skills, arXiv:2605.11946

### Next reading
1. **EDGE (2609.01360):** intervention-validated vs observational edges via counterfactual rollout, for multi-error attribution. It is the closest remaining "intervention validates a dependency edge" work; check whether any edge is an evidence → decision edge.
2. **FORTIS (2605.09163):** least-privilege ground truth and the skill-level authority lattice. Possibly reusable for our restraint dimension.
3. **Counterfactual Trace Auditing (2605.11946):** paired with-skill / without-skill traces; a counterfactual on context (the skill), not on evidence. Probably distant, but it uses the word "counterfactual" near "auditing".
