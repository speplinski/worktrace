# 3. Decision-Structured Agency

## 3.1 Definition

Following the tracking condition of meaningful human control (Santoni de Sio & van den Hoven, 2018), itself a reworking of Fischer and Ravizza's (1998) reasons-responsiveness, and its first behavioural test for foundation models (Suryana et al., 2026), we define *decision-structured agency* (DSA) as the extent to which an agent's behaviour within a decision class regularly recognises and reacts to the evidence that ought to settle decisions in that class.[^fr] Concretely, the agent's action changes when, and only when, the decisive evidence changes; it escalates when that evidence is missing or contradictory, or when the action would exceed its authority; and it revises correctly after correction. DSA is a behavioural, counterfactual property of an agent configuration in a decision class: it is measured by interventions on the external evidence the agent consults, whose decisive role and redundancy are set by construction, and it implies nothing about intentionality or moral responsibility, which remain with the human principals (the tracing condition of meaningful human control).

[^fr]: We borrow the structure of moderate reasons-responsiveness (receptivity and reactivity, evaluated over counterfactual scenarios for a fixed mechanism), not its threshold. Fischer and Ravizza accept *weak* reactivity because their question is blame; delegation asks whether outcomes will be reliable when no human checks, so DSA requires *regular* receptivity and *regular* reactivity. "Ought to settle" marks the reasons as normative rather than merely motivating (Veluwenkamp, 2022).

Two consequences of the definition matter for what follows. First, DSA is indexed by an *agent configuration* $\pi$ (model version, prompt, tools) and a *decision class* $c$; it is not an intrinsic trait of a model, and a change of $\pi$ is a change of agent. Second, each dimension of DSA has named neighbours in recent work (Table 2). What is new is their integration into a per-class profile, their measurement by interventions on external evidence with a normative basis fixed by construction, relative to the oracles' reading of the policy (§6.1), and the use of that profile to allocate autonomy (§4).

## 3.2 Decision episodes

The unit of measurement is the *decision episode*
$$E = (C, I, P, G, A, O),$$
where $C$ is the context (task, principal, decision class), $I$ the information available to the agent at decision time (the evidence items it retrieved, with their sources), $P$ the permissions in force, $G$ the graph of *agent-declared grounds* (the evidence items and rules the agent states it relies on), $A$ the action taken, drawn from the domain actions together with *escalate* and *refuse*, and $O$ the observed consequences, including deferred ones. Most of these fields have counterparts in existing decision records: DEMM's authorisation envelope covers $I$ and $P$ (Solozobov, 2026), the audit verdict of Nian et al. (2026) covers $A$ and part of $O$, and TRACE records cover claims, evidence and verdicts (Chang & Chang, 2026). What the episode adds is $G$ as an object to be *tested* rather than stored, and its use as the unit of intervention.

We keep two notions of authority apart. $P$ is the authority the episode grants; it is fixed by the environment and is the reference for the scope dimension of DSA. The *autonomy* that our rule grants for class $c$ (§4) is an output of measurement. Conflating them would make the rule circular.

## 3.3 Decision classes

A decision class $c \in \mathcal{C}$ is a family of decision situations that share a goal and an admissible action set (including *escalate* and *refuse*). Class membership is given by a rule $\kappa(E) \in \mathcal{C}$ computable at decision time from $(C, I, P)$ alone, never from the outcome, and the partition is fixed before any calibration label is seen. Following the socio-cognitive theory of delegation, in which trust is a relation about a task in a context and delegation occurs when the degree of trust exceeds a threshold reflecting acceptance of risk (Castelfranchi & Falcone, 1998; 2000), each class carries two separate descriptors:

- **requirements** $Q_c$: the evidence-handling capacities a justified decision in $c$ demands (reading the decisive item, detecting stale or contradictory sources, responding to independent corroboration, respecting scope, recognising when to escalate); $Q_c$ determines which DSA dimensions bear on $c$ and whether evidence may be shared across classes (§4.5);
- **risk parameters** $K_c$: stakes, reversibility, escalation cost and legal reservation; $K_c$ sets the tolerated rate $\alpha_c$ and, for legally reserved classes, forces escalation regardless of measured DSA.

Classes that differ only in $K_c$ may share DSA estimates but not thresholds; classes that differ in $Q_c$ may not share estimates even when their stakes coincide. To ease alignment with deployment practice, each class is tagged with the reversibility-graded action classes of Agent Reliability Profiles (Hsu et al., 2026) and with the verifiability, reversibility and criticality axes of Tomašev et al. (2026).

## 3.4 Dimensions

Table 2 lists the dimensions of DSA, the operational test for each, and the prior metric each is aligned with. Dimensions 1–5 enter the delegation rule; dimension 6 is reported but not certified. In the pilot the certified loss is computed from the action alone, which exercises dimensions 2–4 through $A^*$; receptivity is read from the declared grounds (the declared-grounds test, §6.2) and dimension 5 is not exercised (§3.5). What the pilot certifies is therefore an action-based proxy of DSA; the construct as proposed, with receptivity, scope restraint and provenance, is not validated by it.

**Table 2.** Dimensions of decision-structured agency.

| # | Dimension | Operational test | Aligned prior metric |
|---|---|---|---|
| 1 | Receptivity to decisive evidence | The agent registers an intervention on the decisive item (in $G$ or in an escalation message) | Epistemic competence (Shao et al., 2025) |
| 2 | Reactivity to decisive evidence | The action changes as $A^*$ prescribes under *remove*, *only*, *invert* and composed interventions, and not under placebo interventions | Reason-responsiveness (Suryana et al., 2026); necessity/sufficiency tests (Pawar et al., 2026) |
| 3 | Scope restraint | $R(a)=\mathbb{1}[\mathrm{auth}(a)\subseteq P]$, scored on *attempted* and decision-scope over-reach | Restraint in action alignment (Li & Zhao, 2026) |
| 4 | Escalation calibration | Escalates iff decisive evidence is missing or contradictory, or the action exceeds $P$; over-escalation is an error | Selective escalation (Trinh et al., 2026); escalation thresholds (DosSantos DiSorbo & Ju, 2026) |
| 5 | Revision after correction | A principal's correction propagates to later decisions in the episode | Evidence uptake and revision (Ríos-García et al., 2026) |
| 6 | Decision-point recognition and provenance | Alternatives and grounds are recorded; the decision path can be reconstructed from $E$ | Grounding (Shao et al., 2025); evidence-path validity (Flynt, 2026) |

For scope restraint we score attempted over-reach (calls blocked by the ceiling, §4.4) and decision-scope over-reach (deciding a matter reserved for a human), because executed over-reach is blocked mechanically and would otherwise be invisible. Authority is ordered by a small per-domain lattice of actions, data scopes and thresholds.

## 3.5 Measurement by composed evidence interventions

For every episode the generator supplies a *normative action map* $A^*(E) \subseteq \mathcal{A}$, the set of correct actions; it may contain *escalate* (for example when the decisive evidence is missing) and *refuse* (an out-of-permission request). An intervention family $\mathcal{I}(E) = \{do_j\}$ acts on the external evidence in $I$:

- **remove $X$**: delete the evidence item $X$;
- **only $X$**: remove all evidence except $X$;
- **invert $X$**: replace $X$ by an item whose content points to a different correct action;
- **add independent $Y$**: add a source $Y$ that agrees or conflicts with $X$, where *independent* means that $Y$ shares no controlling authority with $X$, counted per authority rather than per record of origin (Pandey et al., 2026a).

Each operator exists in prior work (Turpin et al., 2023; Matton et al., 2025; Pawar et al., 2026; Liu et al., 2026; Gao et al., 2026b). We use them in *composition*: adding an independent $Y$ and then removing $X$ distinguishes redundancy (the action is unchanged because $Y$ suffices) from non-use (the action is unchanged although nothing else supports it). Because the generator also computes $A^*(do_j(E))$, the correct response to every variant is fixed by construction, relative to the oracles' reading of the policy (§6.1, §8). Every unchanged decision is classified as *redundancy*, *cancellation* (opposing effects offset) or *non-reaction*, since a null effect of a single intervention does not show that an item is inert (Du & Chen, 2026; Mahale, 2026).

Receptivity and reactivity can be scored jointly per run in a $2\times 2$ table: recognised and reacted; recognised but not reacted; not recognised but reacted (unfaithful grounds); neither. This is where the agent-declared grounds $G$ earn their place: they are read against the interventional effects, not trusted. The pilot does not report this table: grounds were judged for factual decisions only (§6.2), so receptivity under each intervention was not read; §6 reports reactivity (the non-reaction and escalation measures of Table 7) and a static check of the declared grounds. A second, separate family of *policy interventions* holds the evidence fixed and changes the principal's class policy or $P$; it tests tracking of distal reasons (Mecacci & Santoni de Sio, 2020) and is not run in the pilot.

Controls are mandatory: null arms, placebo interventions on non-decisive evidence, prompt-format placebos (the largest effect in CARE-Drive was a format parameter; Suryana et al., 2026), size-matched shams, copy, pointer and padding controls (Gao et al., 2026b), and a fake declared-grounds graph with the same number of grounds rewired to other items. Controls are reported as separate flip rates and do not enter the basis loss; responsiveness to them is read as noise or sensitivity to form, not as dependence on evidence. The pilot runs four of these controls (null, placebo, sham and copy; §5.2). Agent behaviour is stochastic, so conditions should be run several times and compared as distributions; in the pilot one configuration was run three times and the others once (§5.3). Coupled replays with common random numbers are used only on open-weight stacks (Mahale, 2026).

## 3.6 What DSA is not

DSA is not general capability: it is scored on episodes the agent solves under full information, and its discriminant validity is tested with agents that have planted deficits (§5.3). It is not a security property: adversarially corrupted sources are out of scope (§1.5). And it is not an intrinsic trait of a model: like READY's qualification (Chatrath et al., 2026), it attaches to a configuration and a workflow, here refined to a decision class.

---

## References

All entries are in `paper/references.bib` (verified 2026-10-26; see its `x-verified` fields). Keys cited in this section: `castelfranchi1998delegation`, `chang2026trace`, `chatrath2026ready`, `dossantos2026escalate`, `flynt2026groundeval`, `du2026audita`, `hsu2026arp`, `li2026actionalignment`, `liu2026agentabstain`, `mahale2026causal`, `matton2025walk`, `mecacci2020mhc`, `nian2026auditable`, `pawar2026necessary`, `riosgarcia2026scientists`, `santonidesio2018mhc`, `shao2025seekbench`, `solozobov2026demm`, `suryana2026caredrive`, `trinh2026hilbench`, `turpin2023unfaithful`, `veluwenkamp2022reasons`.
