# Round 2: Learned, calibrated and adaptive permissions for LLM agents

Agent-Sentry, the two static-permission baselines (AgentSpec, AgentBound), and a search for 2025–2026 work that learns, calibrates or adapts an agent's permissions or autonomy from its history.

Date: 25.10.2026. Bibliographic data comes from the arXiv API (export.arxiv.org) and, where a DOI exists, from Crossref. **[verified]** means title, authors, id/DOI and dates were checked against one of these. Quotes are verbatim from the PDFs (extracted with pdftotext). "[my reading]" marks interpretation.

---

## 0. Bottom line (read first)

1. **Agent-Sentry does not threaten WorkTrace's core claim, but it does pre-empt two sub-claims.**
   - What it learns is a *per-action injection detector*. A classifier over provenance-graph features of each action tool call is trained on labelled benign **and** injected traces. A value allowlist and an LLM judge sit on top.
   - It does not learn or allocate any *standing right to decide*. It has no decision classes, no revocation, no human escalation, and no test of how the agent responds to evidence.
   - It *does* already record **agent-declared per-argument provenance** (source set + derivation type) and **cross-checks the declared sources against the raw retrieved text**. WorkTrace therefore must not claim to be first to record an agent's declared grounds at action level, or to check them against the observed record.
2. **The bigger threats come from the search, not from Agent-Sentry.**
   - *The Digital Apprentice* (arXiv:2606.04321) has per-skill autonomy tiers with evidence-gated promotion (correction rate + quality scorer + recorded human authorisation) and automatic demotion. This is "per class, conditional, revocable" in all but name, but the evidence is **outcome/correction-based**.
   - *Hedwig* (arXiv:2605.11495, ACM CAIS 2026) learns, per repository, an online check-in policy from approval/denial history. It has proceed/flag/check-in bands and per-topic revocation.
   - *Trust Before Autonomy* (arXiv:2610.18789) is a position paper. It argues "autonomy should be earned, not assumed" and proposes an autonomy ladder whose gates include abstention on **unanswerable variants**, risk–coverage, and "evidence validity" (re-executing cited evidence). It is the closest to *testing evidence handling*, but it runs no experiment of its own.
   - *Intelligent AI Delegation* (Google DeepMind, arXiv:2602.11865) **already cites Castelfranchi & Falcone (1998) and Falcone & Castelfranchi (2002)**. It proposes trust- and reputation-graduated authority with automated revocation for LLM agents. **WorkTrace's contribution (1), "bridge to classic MAS delegation theory", is no longer unclaimed at the conceptual level.**
3. **Still unoccupied (as far as this search reaches):** granting or withdrawing autonomy per decision class on the basis of **interventional tests of whether the agent's decisions track external evidence** (remove / only / invert / add-independent-source, with redundancy control), **evaluated empirically on held-out episodes against an outcome-only rule with an explicit escalation cost.**
   - Every adaptive system found learns from outcomes, corrections, human approvals, or the structural envelope of past behaviour.
   - None compares against an outcome-only rule with a risk–coverage curve.
4. **Naming risk.** "Earning autonomy" and "autonomy is earned, not assumed" are already used in 2606.04321 and 2610.18789. *Earned Authority* (arXiv:2607.23586) explicitly criticises "earned-autonomy ladders" in which agent-produced performance evidence raises the ceiling. WorkTrace should answer that critique explicitly (see §7).

---

## 1. Reading status (what was read, exactly)

| Work | What I read |
|---|---|
| Agent-Sentry (2603.22868) | **v2 in full** (15 pp.): §§1–9, App. A (A.1–A.5 incl. full judge prompt), B, C, D.1–D.5 text. Some appendix tables only partially parsed (pdftotext layout). **v1** (13 pp.) skimmed to identify differences |
| AgentSpec (2503.18666) | **v3 in full** (10 pp.): §§1–8; reference list skimmed. The camera-ready ICSE version was not compared |
| AgentBound (2510.21236) | **v3 in full** (main text §§1–7, 25 pp. with refs); reference list skimmed. v3 is the FSE'26 version per its own note |
| Digital Apprentice (2606.04321) | Full text (5 pp.) |
| Hedwig (2605.11495) | Main text §§1–5 in full; Appendices A–B (synthetic trace generation, eval details) **not read** |
| Earned Authority (2607.23586) | Main text §§I–VIII in full; proof appendices **not read** |
| Progressive Autonomy as Preference Learning (2605.19151) | Full text (9 pp.) |
| Aethelgard / AgentWarden (2604.11839) | Main text §§1–4.8 and part of §5; appendices **not read** |
| Minimal Oversight (2606.15563) | §1 (setup, MSO principle, Return Operator, masking), "Connections", Related Work, semi-real workflow, Limitations. Theorem sections (capacity, autonomy-time) **skimmed only** |
| Trust Before Autonomy (2610.18789) | §§1, 3–5 (ladder, readiness protocol) read; §2 meta-analysis **skimmed** |
| Oversight Has a Capacity (2606.08919) | §§1–4 and part of §5 |
| Intelligent AI Delegation (2602.11865, 42 pp.) | §§1, 2.1, parts of 2.2, 3, 4 intro, **4.6 Trust & Reputation, 4.7 Permission Handling**, 5.1. Rest **not read** |
| Separating Capability from Permission (2607.23438); Decentralized Granular Access Control (2607.22611) | Abstract + keyword-targeted reading of the relevant sections only |
| MiniScope, ConLeash, Progent, AgenTRIM, TBAC-LLM-judge, Task-Conditioned Least-Privilege Learning, Dynamic Capability Scoping, IntentCap, KYA, DynaTrust, SoK Trust-Authorization Mismatch, Levels of Autonomy for AI Agents, Fernandez P8 | **Abstract only** |

---

## 2. Agent-Sentry (the flagged competitor)

### 2.1 Bibliographic data

- **Title:** Agent-Sentry: Bounding LLM Agents via Execution Provenance
- **Authors:** Rohan Sequeira, Stavros Damianakis, Umar Iqbal, Konstantinos Psounis. Affiliations: USC (Sequeira, Damianakis, Psounis); Washington University in St. Louis (Iqbal).
- **Year / venue:** 2026. arXiv preprint, cs.CR. No journal-ref, no comment, no DOI.
- **arXiv:** 2603.22868. v1 24 Mar 2026; **v2 8 May 2026 (read)**. **[verified]**
- **Version warning:** v1 and v2 differ substantially.
  - v1 builds "functionality graphs from prior benign and adversarial executions", runs coverage experiments at 50/90/100% "functionality graph coverage", and reports different headline numbers ("over 90% of attacks … up to 98% of system utility").
  - v2 replaces this with the three-layer XGBoost/rule pipeline described below. Cite v2 explicitly.

### 2.2 Problem and contribution

Defence against **indirect prompt injection (IPI)** for tool-calling agents. Key idea (§1): deployed agents serve specific use cases, so their executions show regularities that "form an envelope of executions for behaviors". Out-of-envelope **action tool calls** are flagged.

Contributions (§1):
1. A per-argument provenance graph as a substrate for IPI detection.
2. A three-layer enforcement pipeline.
3. Agent-Sentry Bench (≈30× more scenarios than AgentDojo/AgentDyn).
4. A comparison with Progent and CaMeL.

Defence objective (§3.4): "block action tool calls that the current user prompt did not authorize, while preserving the agent's ability to complete legitimate tasks."

Explicitly **out of scope**:
- text-to-text attacks (e.g., a wrong summary, or a phishing URL in the answer);
- jailbreaks;
- **ambiguous prompts** ("pay the bill" when several invoices exist).

### 2.3 Method

**Unit of decision.** A single **action tool call** c_i. Only tools in T_A ("perform irreversible side effects") are evaluated. Retrievals are not gated.

**Recorded trace (§4.1.1).**
- τ = (u, c_1, …, c_n), where u is the prompt and each c_i = (t_i, A_i, r_i).
- Each argument is (a_k, v_k, s_k, d_k):
  - s_k ⊆ {c_1..c_{i−1}, u} is the **per-argument provenance source set**;
  - d_k ∈ {verbatim, derived, generated} is the **derivation type**.
- Crucially: "these are **self reported by the agent** and not fully trusted on their own". They are collected by prepending provenance-reporting instructions to the system prompt and adding required source/derivation fields to the tool schemas. The fields are stripped before execution.

**Provenance graph G_τ (§4.1.3, App. A.1).**
- A DAG whose vertices are the prompt and the tool calls. Edges carry argument-level data flow.
- Unresolvable source ids are labelled *unknown* and "treated as adversarial downstream".
- The "untrusted hop depth" (Eq. 6) captures laundering through several untrusted retrievals.

**Static tool roles (§3.1.1, §4.1.2).**
- Retrieval tools: trusted vs untrusted (T_U = content authored outside the user's trust boundary).
- Action tools.
- The classification is fixed per domain.

**Layer 1: structural classifier (§4.3).** Two variants.
- **XGBoost** over a 17-dim feature vector (Table 9). Feature families:
  - control flow (position, preceding retrievals/actions, retrieval gap, tool diversity);
  - data flow (untrusted-source fraction, prompt-anchor fraction, max untrusted hop depth, source breadth);
  - information flow over 21 "sensitive argument" names (recipient, iban, password, …);
  - one **value-tracing** feature f17, which checks whether an argument value appears verbatim in any preceding untrusted retrieval, "independent of what the agent reports as the source".
  - Output p(c_i) is thresholded at θ_L=0.33 and θ_H=0.66 into Allow / Ambiguous / Block (Eq. 2).
- **Rule-based:** 11 hand-defined detectors (Table 11). Eight "anomaly" detectors relative to benign traces, e.g.:
  - "CFG Action Action: the action that immediately precedes this action was never observed in benign traces";
  - "Source Integrity";
  - "DFG Argument Source";
  - "Transformation Type".
  Three "benign-confirming" detectors (User Prompt Anchor, Trusted Provenance, Recurring Benign Motif). Composite rules are mined by brute force over detector subsets from **labelled benign and malicious actions** (App. A.3.2) into benign / attack / warn composites (Eq. 3). If no rule fires, the default is **Allow**.

**Layer 2: provenance-aware allowlist (§4.4).**
- W = {(tool, argument, value)} for 16 "groundable" sensitive arguments, built from benign traces.
- An action is ambiguous if any value is not in W **and** is unverifiable (unknown source, untrusted source, or the declared source does not contain the value).
- Layer 2 returns only {Allow, Ambiguous}.

**Layer 3: LLM intent-alignment judge (§4.5, App. A.5).**
- Model: Qwen 3.5-35B-A3B, temperature 0.
- Inputs: the user prompt, the call, per-argument provenance, a short window of prior calls, and bounded excerpts of untrusted retrievals in `<retrieved_data>` tags.
- Rule: if a value comes from the *descriptive content* of the source → Allow. If it comes from an *imperative/authority passage* → Block.
- The authors call this "a structural heuristic rather than a formal guarantee". They concede it "won't reliably block attacks that embed the attacker's value inside legitimate-looking content".

**Final decision (Eq. 1).** Allow or Block per action. A trace counts as blocked at the first Block.

**Training data and labels (§4.1.4, App. B.1).**
- A trace is benign if no injection payload was present in any readable source. It is malicious if a payload was present **and** the injection's effect is realised.
- Each action is labelled by matching the injection task's ground-truth signature.
- **Traces are retained only if "the agent completed the user's task (benign) or realized the attacker's goal (attack)".**
- [my reading] The learned "benign envelope" is therefore the envelope of *outcome-successful* benign behaviour. Layer 1 is supervised on **both** classes, so the abstract's "learns a bound … from prior legitimate executions" understates the data requirement: XGBoost and rule mining need labelled *attack* traces. Only the Layer 2 allowlist uses benign traces alone.

### 2.4 Evaluation

**Data.**
- Seven agents/domains: AgentDojo (Banking, Slack, Travel, Workspace) and AgentDyn (GitHub, DailyLife, Shopping).
- **Agent-Sentry Bench:**
  - 757 LLM-generated user-task specs + 3,734 paraphrases;
  - injection tasks reused from AgentDojo/AgentDyn;
  - **5,380 traces (3,299 benign, 2,081 successful attacks)**;
  - driven by Qwen 3.5-35B, plus GPT-OSS-120B on Workspace and GitHub.
- **Native-Trace Bench:**
  - 146 user tasks and 63 injection tasks;
  - **670 traces (126 benign, 544 attack)**;
  - GPT-4o-mini primary, Qwen 3.5 supplementary.

**Protocol.**
- Replay of fixed traces (§5.4); no live re-runs.
- 5-fold CV with paraphrase-grouped folds (App. C.1).
- Metrics:
  - Utility = % of benign traces allowed;
  - ABR = % of malicious traces blocked at or before the injected action;
  - FPR, FNR;
  - L1/L2/L3 routing shares.

**Main numbers.**

| Setting | Utility | ABR | Notes |
|---|---|---|---|
| ASB, XGBoost full pipeline (5-fold) | 96.4 | 96.8 | L1 decides 96.1%, L2 0.8%, L3 3.1% (Table 2) |
| ASB, rule-based full pipeline | 89.3 | 95.3 | L1 54.0%, L2 15.0%, L3 31.0% |
| ASB, L1+L2 only, XGBoost | 93.7 | 96.3 | 3.1% traces left ambiguous (Table 3) |
| ASB, L3 alone (tuned prompt) | 98.0 | 95.4 | untuned prompt: 82.0/75.5 (35B), 70.5/81.6 (7B) (App. D.5) |
| Transfer ASB → Native, XGBoost / rules | 64.4 / 79.1 | 90.9 / 95.0 | Table 5 |
| Native 5-fold, XGBoost / rules | 69.1 / 87.1 | 91.2 / 93.2 | Table 6 |
| **Rules "full coverage"** (fit and tested on the same traces) | 99.8 (ASB); 95.1 (Native) | 94.4; 94.3 | Table 7 |
| Progent | 69.2 (ASB); 93.7 (Native) | 97.7; 88.4 | Table 7 |
| CaMeL (Native only) | 31.0 | 99.3 | 26.60 s/trace vs 4.30 s for Agent-Sentry |
| Delivery-mechanism invariance (Native) | – | 91.5 / 92.3 / 90.8 | ImportantInstructions / DirectAttack / InjecAgent (Table 8) |

Latency: L1+L2 add under 10 ms per trace. The full pipeline averages 0.073 s per trace (with 3.1% judge calls).

### 2.5 Answers to the key questions

**(a) What exactly does it learn, and what does it decide?**
- *Unit:* one action tool call in context (preceding call sequence + per-argument provenance).
- *Representation:* a provenance DAG summarised as 17 numeric features (XGBoost) or 11 binary detector verdicts combined into mined composite rules. Plus a (tool, argument, value) allowlist.
- *Data:* replayed traces of the *same deployed agent/domain*, labelled per action as benign or injected. Traces are filtered to those where the user task succeeded or the attack succeeded.
- *Decision:* **Allow / Block per action** (Ambiguous is internal routing only).
- *Revocability and decision classes:* nothing is revocable or graded. There is **no notion of decision class** and no standing permission. The bound is a deployment-wide model, periodically refit ("the system can be periodically updated with newly observed traces", §8).
- *Human escalation:* **none.** The residual goes to an LLM judge, not a human. "Ambiguous prompts" are explicitly out of scope.
- §8 lists, as future work, "privilege context (conditioning decisions on roles or permissions)" and "external policy and compliance signals".

**(b) Does it test the agent's handling of evidence?**
- **No, not in WorkTrace's sense.** It tests **policy and envelope conformance**: is this action's structural and provenance pattern one seen in benign rather than injected traces, and does a sensitive value come from a trusted source or the prompt?
- There are no interventions on evidence. Nothing checks whether the action would change if a source were removed, inverted or duplicated, and nothing judges whether the decision is *correct given* the evidence.
- The closest element: it **audits the provenance the agent declares** for each argument and cross-checks it against the raw retrieved text (value tracing f17, Source Integrity, Trusted Provenance). This is a *consistency check between declared grounds and the record*, at argument level. It is correlational, not interventional.
- The LLM judge classifies *what kind of passage* a value came from (descriptive vs imperative). That is a heuristic about evidence type, not about evidence sensitivity.

**(c) Evaluation.** See §2.4.
- Fully offline replay. No human-in-the-loop study and no escalation-cost model. No risk–coverage curve, only fixed thresholds; the "Ambig.%" column in Table 3 is the nearest analogue of coverage.
- Generalisation to the native prompt style is weak: utility drops to 64–79% when trained on ASB.

**(d) Differentiation from the WorkTrace delegation rule.**

| Dimension | Agent-Sentry | WorkTrace |
|---|---|---|
| Question answered | Is *this action* consistent with the learned benign envelope? (IPI detection) | May the agent *decide on its own* in this *decision class*? |
| Object of authorisation | Single action tool call | Decision class (standing, revocable right) |
| Evidence used | Structural/provenance pattern of past traces; labelled attacks | Interventional tests of evidence-sensitivity on decision episodes |
| Output | Allow / Block | Proceed / Escalate (to human) / Refuse per class, revocable |
| Role of history | Training data for the envelope | Basis for granting or withdrawing autonomy |
| Redundancy / over-determination | Not addressed | Explicit (remove X / only X / invert X / independent 2nd source) |
| Baseline | Progent, CaMeL (security defences) | Outcome-only rule; risk–coverage with escalation cost |

### 2.6 What WorkTrace must NOT claim (because of Agent-Sentry)

- That it is the first to **learn a permission/behaviour bound from an agent's own past traces**.
- That it is the first to record **agent-self-reported per-argument provenance** (source set + derivation type) as part of a trace, or to **check declared sources against the observed record**.
- That **provenance of action arguments** (trusted vs untrusted origin) has not been used to gate agent actions.

### 2.7 What it leaves open (WorkTrace's territory)

- Decision classes; standing, revocable autonomy; human escalation and its cost.
- Interventional tests of whether decisions track evidence, including redundancy control.
- A comparison against an outcome-only allocation rule.
- Correctness under legitimate-looking but wrong evidence, which the authors concede they do not catch (§4.5).

### 2.8 Draft differentiation sentence

> Agent-Sentry learns from labelled benign and injected traces of a deployed agent a classifier over the provenance-graph structure of individual tool calls, and allows or blocks each call as an indirect-prompt-injection defence; WorkTrace instead grants or withdraws the agent's standing right to decide within a decision class, on the basis of interventional tests of whether its decisions respond correctly to external evidence, and evaluates that rule on held-out episodes against an outcome-only rule with an explicit escalation cost.

### 2.9 Citation cautions

- **Preprint, not peer-reviewed.** v1 and v2 describe different systems and numbers; cite v2.
- **The abstract's headline "blocking 94.3% … allowing 95.1%"** is the *rule-based "full coverage"* configuration. In that configuration Layer 1 and the allowlist are "fit on every benign benchmark trace and evaluated on the same set" (App. B.2.2). It is in-sample, justified by the authors as "matching what Progent and CaMeL observe through their policies". The held-out (5-fold) Native numbers are 69.1/91.2 (XGBoost) and 87.1/93.2 (rules).
- **Internal inconsistencies:**
  - Intro says "allowing 95.4%" where the abstract says 95.1%.
  - The judge invocation rate is given as 3.1% (§6.2) and 3.0% (App. D.5).
  - The mining hyperparameters (κ_A, κ_B, ρ) are "reported in Section 5" (App. A.3.2) but do not appear there.
  - Refs [9] and [10] are the same entry (FIDES, arXiv:2505.23643).
- Layer 3 performance depends heavily on a tuned prompt and model size (App. D.5).

---

## 3. AgentSpec (static-permission baseline 1)

### Bibliographic data

- **Title:** AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents
- **Authors:** Haoyu Wang, Christopher M. Poskitt, Jun Sun (Singapore Management University)
- **Venue:** Proc. ICSE 2026 (48th IEEE/ACM Int. Conf. on Software Engineering, Rio de Janeiro, 12–18 Apr 2026), pp. 2938–2950. DOI 10.1145/3744916.3764546.
- **arXiv:** 2503.18666 (v1 24 Mar 2025; **v3 31 Jul 2025, read**). **[verified]** via arXiv API and Crossref.

### Problem and contribution

A lightweight DSL for **user-specified runtime constraints** on LLM agents. A rule is a tuple (trigger event, predicates, enforcements).
- Triggers: `before_action`, `state_change`, `agent_finish`, and domain events.
- Enforcements: `user_inspection` (pause and ask the human), `llm_self_examine`, `invoke_action`, `stop` (§3.1–3.3, Defs. 3.1–3.3).
- Implemented by intercepting LangChain's `iter_next_step` (AgentAction / AgentStep / AgentFinish). Predicates are hand-written Python or **LLM-generated** (o1).

### Method (units, rules)

- Unit: an event in the trajectory, typically a planned action a_i given the trajectory τ_i.
- A rule is violated if its trigger occurs and all predicates hold (Def. 3.2).
- Enforcement transforms the trajectory (Def. 3.3). `user_inspection` either continues or terminates depending on the human answer.
- Rules are **static and per deployment**. Nothing is learned from the agent's history.
- §6.3 names as *future work* "learning a Discrete-Time Markov Chain … from historical agent interactions" to compute probabilistic reachability of unsafe states.

### Evaluation

| Domain / benchmark | Result |
|---|---|
| Code agent, RedCode-Exec (25 categories × 30) | Risky executions intercepted in >90% of the cases where the agent attempted them (Table 3) |
| Embodied, SafeAgentBench | Hazardous instruction fulfilment 0% with AgentSpec, from 0–78.6% without. **Safe-task completion 58.62% → 54.26%** (Table 4) |
| AV, Apollo/FixDrive (8 law-violation scenarios) | 100% compliance |
| LLM-generated rules (o1) | 87.26% of risky code enforced; embodied precision 95.56% / recall 70.96%; AV 5/8 |
| Overhead | Parsing ≈1.42 ms; predicate evaluation 1.11–2.83 ms |

Rules were developed on 10% of the risky data and tested on the remaining 90% ("Threats to validity"). "User inspection" outcomes were judged by the authors.

### What it covers (WorkTrace must not claim)

- Per-action runtime gating with **escalation to the human** (`user_inspection`) as a first-class enforcement.
- Rule-based triggers conditioned on context predicates (e.g., amount > threshold, `!is_to_family_member`).
- LLM-generated guardrails.

### What it leaves open

- Rules are hand-specified or LLM-specified **before** deployment and never change with the agent's track record.
- No decision classes with earned or revoked autonomy, no tests of evidence handling, no allocation metric beyond safety vs task completion.

### Draft differentiation

> AgentSpec lets a user declare, before deployment, which triggered actions require human inspection, self-examination or termination; WorkTrace makes that allocation an empirical, revocable outcome of how the agent has been shown to handle evidence in each decision class.

### Citation cautions

- Peer-reviewed (ICSE 2026). I read arXiv v3, not the camera-ready version.
- "Prevents unsafe executions in over 90% of code agent cases" counts only cases where the agent attempted the risky code. In 2 of 25 categories the predicates never fired because the agent did not reproduce the risk.
- The safe-task utility cost (−4.4 pp) is small but real.

---

## 4. AgentBound (static-permission baseline 2)

### Bibliographic data

- **Title:** AgentBound: Securing Execution Boundaries of AI Agents
- **Authors:** Christoph Bühler, Matteo Biagiola, Luca Di Grazia, Guido Salvaneschi (University of St. Gallen; Biagiola also USI)
- **Venue:** Proc. ACM Softw. Eng. 3(FSE), Article FSE096 (FSE 2026, Montréal), July 2026. DOI 10.1145/3808103.
- **arXiv:** 2510.21236 (v1 24 Oct 2025; **v3 24 Apr 2026, read**). **[verified]** via arXiv API and Crossref (Crossref issued date 30 Jun 2026).

### Problem and contribution

"The first access control framework for MCP servers." Two components:
- **AgentManifest:** a declarative, Android-permission-inspired capability vocabulary (Table 2). It has 18 capabilities: filesystem read/write/delete, env read/write, exec, process, network client/server/bluetooth, peripherals, location, notifications, clipboard.
- **AgentBox:** Docker-based enforcement using mounts, iptables allow-rules and env whitelists. Servers start "with no privileges". Generic capabilities are instantiated as **runtime permissions via user consent dialogs**.
- **AgentManifestGen:** manifests are generated automatically by an LLM pipeline (gpt-5-mini drafts × 5 → gpt-5 consolidator).

### Method

- **Unit:** an MCP server process (not the agent's decision).
- Permissions are static per server, fixed by the manifest plus user consent at first run. "Highly volatile runtime permissions … must be consented on each execution."
- Default-deny. Nothing is learned from behaviour.

### Evaluation

- **RQ1 completeness:** 296 top MCP servers.
  - Prevalent capabilities: network.client 83.1%, env.read 79.6%, filesystem.read 74.1%.
  - 96 manifests submitted as GitHub issues: 74% no response; 17.7% accepted; 4.2% rejected. Overall "80.9% accurate", recall 100% among responses.
  - Manual comparison on 48 servers: 96.5% accuracy, precision 0.94, recall 0.96.
- **RQ2 security:** a hand-made SSH-exfiltration server plus 4 + 10 malicious/vulnerable servers.
  - All 9 system-resource-targeting attacks blocked.
  - Not blocked: the puppet attack (B.2), SQL injection (B.4), pure prompt injections (C.1, C.6), and C.7.
  - The authors: attacks "within the trusted boundaries of the enforced policies … cannot be blocked".
- **RQ3 overhead:** about 0.6 ms (macOS) and 0.29 ms (Debian) per operation; a few hundred ms container start-up.

### What it covers (WorkTrace must not claim)

- Least-privilege, default-deny capability manifests for agent tools, with human consent at instantiation and automatic manifest generation.

### What it leaves open

- Permissions are about **what a tool server may touch**, independent of how well the agent decides. There is no adaptation over time; the authors list "permissions dynamically inherited from those of the employee invoking it" only as future work.
- It cannot stop misuse inside permitted bounds (the "semantic gap", §2.3/§5). That gap is exactly where a decision-quality–based allocation like WorkTrace's operates.

### Draft differentiation

> AgentBound fixes, per tool server, a least-privilege capability set declared in a manifest and consented by the user; WorkTrace leaves such capability ceilings in place and decides, within them, which classes of decisions the agent may take without a human, revising that allocation as test evidence accumulates.

### Citation cautions

- Peer-reviewed (FSE 2026).
- "80.9% accuracy" rests on 22 of 96 maintainers responding.
- The security evaluation is small (≈15 attack servers).
- Cite the FSE version, as the arXiv note itself requests.

**Joint note on the baselines.** Both baselines are *static* in WorkTrace's sense: the permission set is written (by a human or an LLM) before execution and does not move with evidence about the agent. AgentSpec's `user_inspection` is the static ancestor of WorkTrace's "escalate". AgentBound's manifest is a natural instance of the immutable **ceiling** that Earned Authority (§5.5) argues any earned-autonomy scheme must keep.

---

## 5. Search: 2025–2026 work that learns, calibrates or adapts agent permissions or autonomy

**Search procedure.** arXiv API title/abstract queries, combined with WebSearch:
- least privilege × agent × learn/adaptive/dynamic;
- trust score × access control/permission/autonomy;
- progressive/graduated/earned autonomy;
- reputation × LLM agent × permission;
- behavioural trust/trust calibration;
- adjustable autonomy × LLM;
- approval history × permission;
- "earned" × autonomy/authority;
- learned policy/policy mining × tool call;
- runtime/dynamic trust × agentic.

Candidates were then followed through reference lists (Earned Authority → ConLeash, Progent, AgenTRIM; Digital Apprentice → Feng et al. 2025). The search is not exhaustive. Industry blogs and frameworks were not reviewed.

### 5.1 Tier A: closest to WorkTrace's delegation rule (characterised in detail)

#### A1. The Digital Apprentice

- **Bibliographic:** "The Digital Apprentice: A Framework for Human-Directed Agentic AI Development". Travis Weber, Rohit Taneja (Pheo Inc). arXiv:2606.04321, 3 Jun 2026. Comment: "Submitted to ACM AI Leadership Summit 2026, Visionary Papers Track. 5 pages". **[verified]** (arXiv API). Not peer-reviewed as far as is known.
- **Problem and contribution:** "autonomy is earned, not assumed". The stated contribution is "the machinery for moving between levels: what evidence justifies an increase in autonomy, who must authorize it, and how the system detects when autonomy should be withdrawn".
- **Method:**
  - **Per-skill** finite-state autonomy tiers Pre-L0 → L0 Sandbox → L1 Draft → L2 Autonomous (Table 1). "The agent cannot promote itself."
  - Promotion (Eq. 3) requires: (C1) correction rate in window W_t lower than k=3 windows earlier; (C2) ρ(W_t) ≤ τ_corr; (Q1, if available) a share p of outputs passing a quality scorer Q(x) ≥ τ; **and** an explicit human authorisation H_auth=1.
  - "Demotion is asymmetric: the system rolls a skill back automatically when quality degrades". Triggers are ρ > ρ_demote or OOD uncertainty > u_max.
  - It names the automation-complacency risk ("a low correction rate can indicate either genuine competence or a reviewer who has stopped checking carefully") and treats reviewer engagement as monitored.
- **Evaluation:** a 40–60-prompt pilot on one open corpus, with an LLM judge (Gemma) scoring a six-dimension rubric.
  - Reported means: 0.717 → 0.957 after onboarding; drift recovery 0.930 → 0.957.
  - **The graduation rule itself is not evaluated.** No CIs, no inter-rater agreement, no comparison of rules.
- **What WorkTrace must not claim:**
  - per-class (per-skill) autonomy tiers;
  - promotion gated by evidence plus human authorisation;
  - automatic demotion and revocability as such;
  - the phrase "autonomy is earned, not assumed".
- **What it leaves open:**
  - The evidence is **correction rate and output-quality scores, i.e., an outcome-only signal.** No test of whether outputs respond to the evidence, and no redundancy control.
  - No empirical evaluation of the promotion rule, no risk–coverage curve, no escalation cost.
- **Draft differentiation:**
  > The Digital Apprentice promotes and demotes per-skill autonomy from human correction rates and judge-scored output quality; WorkTrace replaces this outcome-based gate with interventional tests of evidence-sensitivity and evaluates the resulting rule against exactly such an outcome-only gate on held-out episodes.
- **Citation cautions:** a 5-page visionary-track submission from a company, illustrative pilot only. [my reading] Its gate is a concrete instance of the "outcome-only rule" WorkTrace uses as baseline. Cite it as such.

#### A2. Hedwig

- **Bibliographic:** "Hedwig: Dynamic Autonomy for Coding Agents Under Local Oversight". Tanjal Shukla, K. J. Kevin Feng, Leijie Wang, Mohammad Rostami, Amy X. Zhang (University of Washington; Rostami at Amazon). Proc. 1st ACM Conference on AI and Agentic Systems (CAIS '26), demo track, San Jose, 26 May 2026. DOI 10.1145/3786335.3813223; arXiv:2605.11495. **[verified]** (arXiv API + Crossref).
- **Problem and contribution:** static permission settings and instruction files "cannot account for how developers' preferences for agent autonomy can shift across tasks and over time". Hedwig "learns an evolving set of behavioral guidelines from developer decisions and feedback, reducing friction on work for which the agent has **earned trust**, while tightening oversight when the agent operates outside familiar territory".
- **Method:**
  - Two governance tiers: **hard constraints** (enforced by the CLI) and **behavioural guidance** (retrieved into prompts).
  - Policy path: an **online logistic regression** over a 13-dim action feature vector, updated by SGD after each developer decision. Features include diff size, blast radius, change-pattern risk, **prior approval/denial counts**, security sensitivity, **verification-failure history**, and model confidence. It is warm-started from engineering priors, with coefficients persisted **per repository**.
  - Three bands: >0.90 silent approve; 0.20–0.90 approve but flag; <0.20 live check-in.
  - **Revocation by topic:** `hw observe preferences-revoke --topic api` "removes the API topic from trusted scope without resetting accumulated states".
  - Workflow-phase gating.
- **Evaluation:**
  - Synthetic personas: 20 seeded decisions replayed 3×. Two backend tasks, 11 write operations, an LLM-judge oracle (Claude Opus 4.7).
  - Cautious persona: recall 1.00, precision 0.67. Permissive persona: 4 unnecessary check-ins. Compared against Claude Code + CLAUDE.md.
  - Formative survey with N=21. "No formal user study".
- **What WorkTrace must not claim:**
  - adaptive, history-learned, per-action autonomy with proceed / flag / ask bands;
  - "earned trust" language;
  - topic- or area-scoped revocation of autonomy;
  - separating policy-initiated from agent-initiated escalation.
- **What it leaves open:**
  - The learning signal is **human approval/denial and verification outcomes**: preference plus outcome, not evidence handling.
  - Classes are implicit (file area / change category), not defined decision classes.
  - No held-out evaluation, no escalation-cost model beyond the authors' remark that a missed check-in is costlier than an extra one.
- **Draft differentiation:**
  > Hedwig adapts when a coding agent must check in by learning a developer's approval history over action features; WorkTrace adapts what an agent may decide by testing whether its decisions track the evidence, independently of whether a particular human happened to approve them.
- **Citation cautions:** a demo-track paper with a proof-of-concept and synthetic evaluation. Peer-reviewed as a demo.

#### A3. Trust Before Autonomy (position paper)

- **Bibliographic:** "Trust Before Autonomy: Rethinking Agentic Remote Sensing for Crisis Response". Georgios Angelidis, Aggelos Psiris, Spyridon Evangelatos, Thomas Lagkas, Panagiotis Sarigiannidis, Iraklis Varlamis, Georgios Th. Papadopoulos. arXiv:2610.18789, 13 Oct 2026. **[verified]** (arXiv API). Venue not stated.
- **Problem and contribution:** "autonomy should be earned, not assumed: an Earth-Observation agent should be granted autonomy in proportion to demonstrated reliability, epistemic honesty and verifiability."
  - A meta-analysis of 12 agentic RS/EO/GIS benchmarks finds that "task success exceeds tool-call correctness by up to 54pp" and that "capability does not predict abstention".
  - It proposes an autonomy ladder L1–L5 (roles from Feng et al. 2025) and a staged readiness protocol R1–R5: benchmark → **replay of archived activations** → shadow → supervised → conditional. "Promoted one rung … only after passing the corresponding gate … and demoted on failure"; R5 is "revoked on any drift".
- **Relevant tests (proposed only):**
  - R1 adds **unanswerable variants** built from physical evidence absence (cloud or smoke cover, no post-event acquisition, coarse resolution), scored with **selective risk–coverage** and abstention F1.
  - P3 "evidence validity" is "the share of claims whose cited evidence, when re-executed, reproduces the claim".
- **Evaluation:** meta-analysis of published tables only; **no experiment with the proposed gates.** It concludes that current evidence supports L1–L2 only.
- **What WorkTrace must not claim:**
  - "earned autonomy" as a slogan or idea;
  - autonomy ladders with evidence gates and demotion;
  - using risk–coverage to score abstention;
  - "task success ≠ correctness" as a motivating observation;
  - checking claims by re-executing their cited evidence.
- **What it leaves open:**
  - It is domain-specific (EO) and a proposal only.
  - Its evidence tests are *unanswerable variants* (closest to WorkTrace's "remove X") without only-X / invert-X / independent-second-source and without redundancy control.
  - Gates are per autonomy rung, not per decision class learned from episodes. No delegation rule is estimated or compared with an outcome-only rule.
- **Draft differentiation:**
  > Angelidis et al. argue that EO agents should earn autonomy through benchmark, replay and shadow gates that include abstention on unanswerable variants; WorkTrace formalises and runs such evidence tests generally, as a family of redundancy-robust interventions on decision episodes, and estimates a per-class delegation rule from them.
- **Citation cautions:** a position paper, preprint, posted 12 days ago. Cite as concurrent.

#### A4. Intelligent AI Delegation (Google DeepMind)

- **Bibliographic:** "Intelligent AI Delegation". Nenad Tomašev, Matija Franklin, Simon Osindero (Google DeepMind). arXiv:2602.11865, 12 Feb 2026. **[verified]** (arXiv API). No venue.
- **Problem and contribution:** a conceptual framework for delegation among humans and AI agents. It covers task decomposition, assignment, monitoring, **trust and reputation (§4.6)**, **permission handling (§4.7)**, verifiable completion, security, ethics, and protocols.
- **Key points for WorkTrace:**
  - **It grounds itself in classic MAS delegation:** "Delegation (Castelfranchi and Falcone, 1998) is more than just task decomposition…". Degrees of autonomy are cited to Falcone & Castelfranchi (2002). It also cites MAS trust work (Ramchurn et al. 2004; Pinyol & Sabater-Mir 2013) and the contract net.
  - §4.6: trust is "the delegator's degree of belief in a delegatee's capability … dynamically formed and updated based on verifiable data streams". "Graduated authority results in low-trust agents facing strict constraints … while high-reputation agents operate with minimal intervention."
  - Table 3 names "Behavioral Metrics" reputation, which "evaluates how a task is performed rather than just the result".
  - §4.7: risk-adaptive, just-in-time permissions; privilege attenuation on sub-delegation; "continuous validation and automated revocation … algorithmic circuit breakers: if an agent's reputation score drops suddenly … active tokens should be immediately invalidated".
- **Evaluation:** none (conceptual).
- **What WorkTrace must not claim:**
  - that **no one bridges** Castelfranchi–Falcone delegation theory to LLM agents;
  - that trust-graduated, revocable authority for LLM agents is a new *idea*;
  - that "how, not just the result" as a basis for reputation is new.
- **What it leaves open:**
  - No operational definition of what to test.
  - No decision episodes, no interventions on evidence, no estimated delegation rule, no empirical evaluation.
  - It does not cite adjustable autonomy (Scerri et al.); a grep for "adjustable"/"Scerri" found nothing in the full text.
- **Draft differentiation:**
  > Tomašev et al. sketch, from Castelfranchi and Falcone's delegation theory, how trust and reputation should graduate and revoke an agent's authority; WorkTrace supplies an operational, testable instance of that idea, in which the trust signal is the agent's measured sensitivity to external evidence per decision class, and evaluates it empirically.
- **Citation cautions:** a preprint, but high-visibility (DeepMind) and likely to be known to reviewers. **Must be cited.** WorkTrace's contribution (1) should be reworded from "first bridge" to "first *operational, empirically evaluated* bridge, including adjustable autonomy".

#### A5. Are You Still the Agent I Authorized? (Earned Authority)

- **Bibliographic:** "Are You Still the Agent I Authorized? Earned Authority under a Fixed Ceiling for Evolving Agents". Zhaoxi Zhang (University of Technology Sydney), Xiaomei Zhang (Griffith University). arXiv:2607.23586, 26 Jul 2026. **[verified]** (arXiv API).
- **Problem and contribution:** "authorization continuity" for self-evolving agents. A grant fixes:
  - an **immutable effect ceiling B**;
  - an initial active authority P_0 ⊆ B;
  - a **transition envelope** of mutation classes the grant may survive.

  Active authority "may contract freely and expand only under specified evidence conditions". The clamp is P_t = P_t^prop ∩ B. Theorem 1 (non-amplification) holds under complete mediation, sound effect abstraction, attenuating delegation and monitor integrity. Six mutation classes are mapped (Table I).
- **Key argument for WorkTrace (§V-C, §VII-a):**
  - "A system may condition authority on demonstrated performance only if it also fixes a bound that no performance can move."
  - "Task outcomes, tests, error rates, and execution histories are often produced by the same session that benefits from an authority increase … treating them as the only security boundary gives the beneficiary partial control over its own privilege."
  - "A tighter security bound requires at least one premise that the session cannot realize under its current authority, such as an external attestation, an **independently controlled evaluator**, or a fresh human countersignature."
  - Table II lists the "Earned-autonomy ladder" as a policy where "performance evidence may raise the terminal boundary". It cites practitioner sources (AWS, KnowBe4, CSA 2026).
- **Evaluation:** **none.** "We therefore present it as a formalization rather than as an empirical claim". Proposed metrics: grant persistence, post-mutation unauthorized-effect rate, false invalidation, interaction cost.
- **What WorkTrace must not claim:**
  - that conditional, evidence-gated expansion beneath a fixed ceiling is new;
  - that history-based authority adaptation is unproblematic.
- **What it leaves open:**
  - It does not say *what* evidence should gate expansion, beyond requiring that it be external to the session.
  - It has no decision quality, no experiments, and no decision classes; its unit is effect sets and mutation classes.
- **Draft differentiation:**
  > Zhang and Zhang show that evidence produced by an agent may allocate authority only beneath a user-fixed ceiling and only via premises the agent cannot generate itself; WorkTrace's interventional evidence tests are such an externally controlled evaluator, and its delegation rule operates strictly inside the permissions recorded in each decision episode.
- **Citation cautions:** a theory preprint from two authors, no evaluation. Useful as **support** for WorkTrace's design, and as the strongest articulated **objection** to naive earned autonomy, which WorkTrace should pre-empt.

#### A6. Progressive Autonomy as Preference Learning

- **Bibliographic:** "Progressive Autonomy as Preference Learning: A Formalization of Trust Calibration for Agentic Tool Use". Changkun Ou. arXiv:2605.19151, 18 May 2026. **[verified]** (arXiv API). No venue.
- **Method:**
  - A policy gateway places a GP prior over a latent human risk-tolerance f(a, c). The probit likelihood is fitted on **binary approve/deny feedback**.
  - Decision rule (Eq. 8): allow if p̂ > τ_high, block if p̂ < τ_low, otherwise **ask**. The ask band is an acquisition region.
  - Product kernel over tool, context and time. A time-decay kernel models drift ("a principled analog of … 'agents earn trust over time'").
- **Evaluation:** synthetic oracle only.
  - 18 tools × 8 resource tiers × 7 contexts; N=1,500 prequential decision points; 6 seeds.
  - Validation: auto-decision accuracy 0.973 at 68% coverage, false-allow 2.4%.
  - About 1.8× fewer queries than always-escalate.
  - An honest negative result: ask-band querying does **not** beat random querying (76.5% vs 78.4%).
- **What WorkTrace must not claim:** that allow/block/ask with a learned boundary, a coverage/false-allow trade-off, and human-burden reduction are new for agent tool use.
- **What it leaves open:**
  - It learns the **human's** risk tolerance, not the **agent's** competence or evidence-sensitivity.
  - No real data and no decision classes beyond kernel similarity.
- **Draft differentiation:**
  > Ou learns where a supervising human would approve an agent's action; WorkTrace learns where the agent's own decision-making has been shown to respond correctly to evidence.
- **Citation cautions:** a single-author preprint with a simulation only.

#### A7. Minimal Oversight

- **Bibliographic:** "Minimal Oversight: Uncertainty-Aware Governance for Delegated AI Systems". Carlos R. B. Azevedo (independent). arXiv:2606.15563, 4 Jun 2026. Companion package `minimal-oversight`. **[verified]** (arXiv API).
- **Method:**
  - Per task class x, the authority ceiling is α_max(x) = G(σ_raw(x)), a monotone function of the **raw (uncorrected) success rate**.
  - Oversight is then allocated by a Fisher-metric variational principle (MSO) with a water-filling solution.
  - **"Masking":** corrected output quality σ_corr hides raw competence; "Authorization must be based on σ_raw — not on σ_corr". Masking index M* ≈ 1.35–1.45 in its examples.
  - Evidence decays toward a prior (a leaky integrator), i.e., revocation by forgetting.
- **Evaluation:** synthetic simulations and one "semi-real reconstructed workflow" (2,400 items). The author states that these are "internal model checks rather than external field validation" and that there is no comparison with strong baselines.
- **What WorkTrace must not claim:**
  - per-task-class autonomy allocation from accumulated evidence with decay;
  - that corrected outcomes mislead trust calibration (masking).
- **What it leaves open:** the signal is success rate, i.e., **outcome-only**.
- **Draft differentiation:**
  > Azevedo allocates delegated authority per task class from raw success rates; WorkTrace argues that even raw success is the wrong signal when decisions can succeed for the wrong reasons, and gates autonomy on tested evidence-sensitivity instead.
- **Citation cautions:** a single-author theory preprint, partly LLM-assisted (disclosed), with synthetic validation. Its "masking" result is still a useful, citable argument against corrected-outcome rules.

### 5.2 Tier B: adaptive or learned *permission scope* (security-oriented); characterised briefly

| Work (all **[verified]** via arXiv API unless noted) | What adapts / is learned | From which signal | Decision | Read |
|---|---|---|---|---|
| **Beyond Static Sandboxing: Learned Capability Governance for Autonomous AI Agents.** Bronislav Sidik, Lior Rokach (BGU). arXiv:2604.11839 v2, 3 May 2026; "Submitted to NeurIPS 2026 Agent Safety Workshop" | PPO policy outputs a per-session tool-exposure mask per **task type** (6 manual types). A "trust level" ∈[0,1] is a state input; exec requires trust ≥ 0.8 | Audit log: task success, Skill Economy Ratio, Safety-Router block counts | Tool exposure + allow/block per call | Main text |
| **MiniScope: Authorizing Agents with Least-Privilege Permissions.** Jinhao Zhu, Xiao Huang, Kevin Tseng, Gil Vernik, Shishir G. Patil, Vivian Fang, Raluca Ada Popa. arXiv:2512.11147 (v2 6 Oct 2026) | Task-centric hierarchical permissions; automated permission-hierarchy discovery | Tool-call relationships | Contextual least privilege; 43–89% fewer confirmations | Abstract |
| **Options, Not Clicks: Lattice Refinement for Consent-Driven MCP Authorization (Conleash).** Ying Li, Yanju Chen, Peiran Wang, Issac Khabra, Faysal Hossain Shezan, Yu Feng, Yuan Tian. arXiv:2605.11360 | "Refinement loop that converts user decisions into reusable rules"; risk lattice auto-permits within known boundaries | User consent decisions | Allow / escalate / deny; 984 real traces, user study N=16 | Abstract |
| **Progent: Securing AI Agents with Privilege Control.** Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, Dawn Song. arXiv:2504.11703 (v3 14 May 2026) | LLM-generated policy updated during execution; SMT-checked **narrowing is automatic, expansion requires approval** (monotonic confinement) | User task + execution state | Allow/block per call | Abstract (plus its use in Agent-Sentry and Earned Authority) |
| **AgenTRIM: Tool Risk Mitigation for Agentic AI.** Roy Betser, Amit Giloni, Shamik Bose, Sindhu Padakandla, Chiara Picardi, Lidor Erez, Roman Vainshtein. arXiv:2601.12449; comment "EMNLP 2026 Findings" | Offline reconstruction of the tool interface "from code and execution traces"; per-step least-privilege filtering | Code + traces | Tool filtering / call validation | Abstract |
| **Uncertainty-Aware, Risk-Adaptive Access Control for Agentic Systems using an LLM-Judged TBAC Model.** Charles Fleming, Ashish Kundu, Ramana Kompella. arXiv:2510.11414 | LLM judge synthesises just-in-time task policy with risk + self-uncertainty | Task intent, resource risk | High risk/uncertainty → human approval | Abstract |
| **Task-Conditioned Least-Privilege Learning for Executable Terminal and MCP Agents.** Alexander Tu, Michael Tu. arXiv:2608.18351 | **Post-trains the agent** (Qwen3.5-4B) toward restraint; predefined sufficient-authority envelopes | Deterministic verifiers incl. "evidence" dimension | Agent's own choice of authority; excess-authority events 4.56% → 0.79% | Abstract |
| **Dynamic Capability Scoping for Enterprise AI Agents** (arXiv:2607.22445, AIWILD@ICML 2026) and **Empirical Evaluation of Task-Based Permission Scoping Architecture** (arXiv:2609.15422). Halil Burak Noyan | Role ceiling + task-context classifier + prohibitions | Prompt classification | Credential exposure per task | Abstract |
| **LLM Agent Capabilities Should Follow Task Intent and Context Source (IntentCap).** Yusheng Zheng, Wenhui Zhang, Yu Mao. arXiv:2609.14631; "Accepted at AgenticOS 2026" | Short-lived task leases composed from four sources, monotonic narrowing | Context sources | Lease checked before side effects | Abstract |
| **Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human.** Emre Turan. arXiv:2606.08919 | Guard threshold chosen under **asymmetric cost** and an **endogenous, fatiguing reviewer**; risk–coverage and AURC | 125 hand-labelled actions | Auto-allow vs escalate; inverted-U safety vs escalation rate | §§1–4 read |
| **KYA: A Framework-Agnostic Trust Layer for Autonomous Systems…** Kolawole Quadri. arXiv:2605.25376 | Trust scoring across humans/agents; "runtime debit for actual delegate misbehavior" | Behaviour/misbehaviour events | Policy gates | Abstract |
| **DynaTrust: Defending Multi-Agent Systems Against Sleeper Agents via Dynamic Trust Graphs.** Yu Li, Qiang Hu, Yao Zhang, Lili Quan, Jiongchi Yu, Junjie Wang. arXiv:2603.15661 | Per-agent trust updated "based on its historical behaviors" | Behaviour history + expert agents | Graph restructuring/isolation in MAS | Abstract |
| **Separating Capability from Permission: A Governance Framework for Agentic AI Autonomy Levels.** Haining Zheng, Qian Dong, Rodolfo K. Depena, Jonathan D. Bhatia, Feng Xiao, Peng Xu. arXiv:2607.23438 | Allowed Autonomy Level assigned by a risk-aware **design-time** decision process; not learned | Risk, reversibility, readiness | Autonomy level per application | Targeted skim |
| **Decentralized Granular Access Control for Agentic AI Systems in Critical Infrastructure.** Arun Malik et al. (6 authors). arXiv:2607.22611 | "Progressive trust escalation" = authorisation tiers rising with **operation risk** (not earned); agents cannot self-authorise | Operation risk | Tiered approvals; 8 months in production | Targeted skim |
| **SoK: Trust-Authorization Mismatch in LLM Agent Interactions.** Guanquan Shi et al. (7 authors). arXiv:2512.06914 | Survey (200+ papers); calls for moving "from static RBAC to dynamic, risk-adaptive authorization" | – | – | Abstract |
| **Levels of Autonomy for AI Agents.** K. J. Kevin Feng, David W. McDonald, Amy X. Zhang. arXiv:2506.12469 (Knight First Amendment Institute essay) | Five autonomy levels by user role; proposes "AI autonomy certificates" | – | – | Abstract |
| **Identity-Bound Governance Under Execution Uncertainty… (P8).** Marcelo Fernandez. arXiv:2610.00787 | Human-signed re-authorisation after a persistent HALT; drift threshold T* calibrated per model | Drift detection | Resume/deny/recalibrate | Abstract (already flagged in positioning.md) |

[my reading] Tier B systems adapt **permission scope** (which tools, resources or credentials) to the *task*, *human consent history* or *risk*. None conditions authority on *how well the agent decides*. They are complementary ceilings, not competitors.

### 5.3 Comparison matrix (closest works)

Columns:
- **Hist** = learns or adapts from the agent's history.
- **Unit** = unit of authorisation.
- **Signal** = evidence that moves authority.
- **Class** = per decision/skill/task class.
- **Revoc** = revocation/demotion.
- **Human** = human escalation.
- **EvTest** = tests evidence handling by intervention.
- **Eval** = empirical evaluation of the allocation rule against an outcome-only baseline, with risk–coverage and escalation cost.

| Work | Hist | Unit | Signal | Class | Revoc | Human | EvTest | Eval |
|---|---|---|---|---|---|---|---|---|
| Agent-Sentry | ✓ | action | structural/provenance envelope; labelled attacks | ✗ | ✗ (refit) | ✗ (LLM judge) | ✗ (provenance audit only) | ✗ |
| AgentSpec | ✗ | triggered action | hand/LLM rules | ✗ | ✗ | ✓ | ✗ | ✗ |
| AgentBound | ✗ | MCP server capability | manifest + consent | ✗ | ✗ | ✓ (consent) | ✗ | ✗ |
| Digital Apprentice | ✓ | skill tier | correction rate, judge quality + human sign-off | ✓ | ✓ (auto) | ✓ | ✗ | ✗ |
| Hedwig | ✓ | action (file area / topic) | approvals/denials, verification failures | ~ | ✓ (topic) | ✓ | ✗ | ✗ (synthetic personas) |
| Trust Before Autonomy | (proposed) | autonomy rung | pass^k, abstention on unanswerable variants, evidence validity | ~ (EO task types) | ✓ | ✓ | **~ (proposed, remove-type only)** | ✗ |
| Intelligent AI Delegation | (proposed) | delegated task / token | trust & reputation (incl. behavioural metrics) | ~ | ✓ | ✓ | ✗ | ✗ |
| Earned Authority | (formal) | effect set under ceiling | "specified evidence conditions" (external) | ✗ | ✓ | ✓ (new grant) | ✗ | ✗ |
| Progressive Autonomy PL | ✓ | action-context | human approve/deny | ~ (kernel) | ✓ (decay) | ✓ | ✗ | simulation only |
| Minimal Oversight | ✓ | task class | raw success rate | ✓ | ✓ (decay) | ✓ (corrector) | ✗ | synthetic |
| Aethelgard/AgentWarden | ✓ | tool set per task type | task success, tool economy, blocks | ✓ (task type) | ~ | ✗ | ✗ | ✗ |
| **WorkTrace (planned)** | ✓ | **decision class** | **interventional evidence-sensitivity tests (redundancy-robust)** | ✓ | ✓ | ✓ (with cost) | **✓** | **✓** |

### 5.4 Answer to (d): is there any work that comes closer than Agent-Sentry?

Yes. Ranked by closeness to the **delegation rule**, not to the evidence tests:

1. **The Digital Apprentice.** It has the same *shape* as WorkTrace's rule: per-skill, evidence-gated promotion, human authorisation, automatic demotion. The basis differs: correction rate is outcome-only.
2. **Hedwig.** It learns from history when an agent may proceed per action area, with topic revocation. The basis is human approvals.
3. **Trust Before Autonomy.** Its *evidence-handling* tests are closest (abstention on unanswerable variants, evidence validity, risk–coverage), but it is only a proposal, domain-specific, and has no redundancy control.
4. **Intelligent AI Delegation.** It is closest on the *theory bridge* (Castelfranchi & Falcone, graduated authority, revocation), at the conceptual level only.

Agent-Sentry is closer than all of these on only one axis: it **actually learns from traces at scale with a held-out evaluation**. But what it learns is an injection detector, not a delegation rule.

**No work found combines** interventional tests of evidence-sensitivity, decision-class autonomy allocation, and an empirical comparison with an outcome-only rule.

---

## 6. Implications for WorkTrace

### 6.1 Claims to change

1. **Contribution (1), the MAS bridge.**
   - Reword "nobody cites classic delegation theory" (positioning.md §3.1) to: "Tomašev et al. (2026) invoke Castelfranchi & Falcone conceptually; we give the first operational, empirically evaluated instantiation, and connect it additionally to adjustable autonomy (Scerri et al. 2002), which they do not cite."
   - Cite Intelligent AI Delegation prominently.
2. **"Earned autonomy" is not new as an idea or slogan.**
   - Cite Digital Apprentice, Trust Before Autonomy, Hedwig, Feng et al. 2025 (levels), and the practitioner sources Earned Authority cites.
   - WorkTrace's novelty is the **basis** (tested evidence-sensitivity, redundancy-robust), the **unit** (decision episode → decision class), and the **empirical comparison** against outcome-only allocation.
   - Consider whether the working title "Earning Autonomy" should change, or whether to keep it and state the lineage explicitly.
3. **Per-class, revocable, evidence-gated autonomy is not new as a mechanism** (Digital Apprentice, Minimal Oversight, Trust Before Autonomy). Do not present revocability or per-class tiers as contributions in themselves.
4. **Declared-grounds recording.** Agent-Sentry already elicits per-argument self-reported provenance through schema fields and cross-checks it against the record. Cite it when introducing the "graph of declared grounds". Differentiate:
   - WorkTrace's grounds sit at *decision* level and are tested **interventionally**;
   - Agent-Sentry's are checked for *consistency* only.
5. **Allow/escalate/block bands with a learned boundary** (Hedwig, Ou 2026, Conleash, Agent-Sentry's internal Ambiguous) are prior art. WorkTrace's three-way rule must be framed as *per decision class* and *grounded in evidence tests*.

### 6.2 Design changes suggested

1. **Fixed ceiling.** Adopt Earned Authority's constraint explicitly: the delegation rule only allocates autonomy *within* the permissions recorded in the episode (the static ceiling, e.g. AgentBound/AgentSpec/Progent-style). Evidence can never raise it. This pre-empts the strongest published objection to earned autonomy.
2. **Externality of the evidence.**
   - State that WorkTrace's interventions are generated and scored by an evaluator outside the agent's session and authority. That is Zhang & Zhang's "independently controlled evaluator" premise.
   - So the agent cannot manufacture its own promotion evidence, unlike correction rates or task outcomes produced inside the session.
   - This is a crisp, citable distinction from Digital Apprentice, Hedwig and Minimal Oversight.
3. **Make the outcome-only baseline concrete and literature-anchored.** Instantiate it as:
   - (i) a correction/success-rate gate à la Digital Apprentice (C1 ∧ C2) or Minimal Oversight's α_max = G(σ_raw);
   - optionally (ii) an approval-history gate à la Hedwig/Ou.

   Reviewers then see that WorkTrace beats the *published* rules, not a straw man. Minimal Oversight's "masking" argument and Trust Before Autonomy's "completion is not correctness" (up to 54 pp gap) both motivate why outcome-only rules over-authorise.
4. **Escalation cost.** Model the cost of escalating with reference to Turan (2606.08919): asymmetric cost table, risk–coverage/AURC, and a reviewer whose reliability falls with load. Consider reporting WorkTrace's curve under a fatigue-aware cost as a robustness check. FALCON and DeCCaF are cited there and should be verified before citing (**[unverified]**, not checked here).
5. **Evidence-handling attacks as a test family.** Agent-Sentry's limitation, "attacks that embed the attacker's value inside legitimate-looking content" (§4.5), is exactly an *invert-X* intervention on external evidence. WorkTrace can include such episodes and show that envelope/provenance detectors cannot catch them while an evidence-sensitivity test can. [my reading] This would be a strong, concrete differentiation experiment.
6. **Abstention variants.** Trust Before Autonomy's unanswerable variants are a special case of "remove X" where the correct response is to refuse or escalate. Make sure WorkTrace's intervention set covers this case and cite it.

### 6.3 Things to cite (with role)

| Cite | Role in WorkTrace |
|---|---|
| Agent-Sentry (2603.22868 v2) | Learned behavioural envelope / provenance gating; declared per-argument provenance |
| AgentSpec (ICSE'26), AgentBound (FSE'26), Progent (2504.11703) | Static ceilings; human-inspection enforcement; narrowing-free / expansion-needs-approval |
| Intelligent AI Delegation (2602.11865) | Conceptual delegation/trust/reputation bridge; graduated authority + revocation |
| Digital Apprentice (2606.04321), Hedwig (CAIS'26), Minimal Oversight (2606.15563) | Prior adaptive-autonomy mechanisms based on outcomes/approvals; templates for the outcome-only baseline |
| Trust Before Autonomy (2610.18789) | Concurrent position: earned autonomy with abstention/evidence-validity gates |
| Earned Authority (2607.23586) | Fixed-ceiling requirement; critique of self-produced evidence |
| Progressive Autonomy PL (2605.19151), Conleash (2605.11360), MiniScope (2512.11147) | Learned allow/ask/block boundaries from human feedback; consent fatigue |
| Oversight Has a Capacity (2606.08919) | Escalation cost, risk–coverage for guards, reviewer fatigue |
| Levels of Autonomy for AI Agents (2506.12469) | Autonomy-level taxonomy used by several of the above |

### 6.4 Risks

- **Reviewer framing risk.** Reviewers may say "this is Digital Apprentice/Hedwig with a different trust signal". The answer must rest on the empirical claim that the evidence-sensitivity signal **beats outcome-based signals on held-out episodes at matched escalation cost**. Without that result, the paper's novelty narrows to the test design.
- **Concurrency risk.** Trust Before Autonomy (13 Oct 2026) and Earned Authority (26 Jul 2026) are recent. More concurrent work in this area is likely; re-run the search before submission.
- **Venue status.** Most adaptive-autonomy works are unrefereed preprints or demo/visionary papers. Only Hedwig (demo), AgentSpec, AgentBound, AgenTRIM (EMNLP Findings, per its arXiv comment) and IntentCap (workshop) carry venue information.
