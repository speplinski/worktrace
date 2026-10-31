# R3: Trust across task classes. Scope, transfer, dynamics, and what they imply for WorkTrace "decision classes"

Round-3 reading note, 25 Oct 2026. Task: check the classic theory of trust across task classes (Castelfranchi & Falcone) and the computational MAS/HRI work on task- or category-based trust transfer, because WorkTrace's per-decision-class claims rest on it.

---

## 0. Read first: novelty threats and the main finding

**No novelty threat to W1–W3 or to DSA was found.** However, five ideas that WorkTrace might be tempted to present as its own are **already established**:

1. **Trust is always relative to a task and context.** C&F write it as Trust(X, Y, C, τ, g_X), with τ = (α, g).
2. **Trust can generalise from task to task and from agent to agent by reasoning over task requirements and agent features.** Sources: C&F 2008 chapter; Book §6.6; operationalised in Venanzi et al. IJCAI 2011.
3. **Category or stereotype priors that "yield to direct evidence".** Source: Burnett, Norman & Sycara 2010.
4. **Task-similarity-graded and asymmetric transfer of trust, with learned task spaces.** Source: Soh et al. IJRR 2019.
5. **Trust updates require causal attribution of outcomes (internal vs external), not reinforcement on success/failure.** Sources: C&F HICSS 2000; Falcone & Castelfranchi AAMAS 2004.

**Consequence.** WorkTrace must cite these and claim only the following:
- (i) the *competence belief* per decision class is **measured by interventions on evidence** rather than inferred from outcomes, features or categories;
- (ii) a **certification-constrained** transfer/pooling rule across classes;
- (iii) revocation that propagates along shared requirements.

**Key gap: §6.6 of the 2010 book could not be read.** I read its TOC titles, the 2008 chapter's abstract, and two closely related full texts by the same authors (WOA 2010 transitivity paper; IJCAI 2011). From these, the §6.6 mechanism is very probably **matching task properties to agent features**: the TOC has §6.6.2 "Matching Agents' Features and Tasks' Properties" and §6.6.3 "Formal Analysis". This is consistent with the "requirements-based class definition" proposed below. It is not verified. Someone must read §6.6 (pp. 174–184) and the LNCS chapter (pp. 65–80) from a library copy before submission. *Risk: low–medium.* If §6.6 already contains an explicit "transfer iff requirements of τ′ ⊆ qualities ascribed for τ" rule, we cite it as the origin of our dominance-transfer rule rather than presenting the rule as ours.

**Design finding (most useful output).** C&F separate two things:
- the **degree of trust** (DoT, built from beliefs about ability, willingness, opportunity);
- the **acceptance threshold** σ, which depends on stakes and the trustor.

WorkTrace should mirror this. A decision class has:
- **competence-relevant features**: what evidence handling the decision requires. These define where a DSA profile may be shared.
- **risk features**: stakes, reversibility, legal reservation. These set α_c (the threshold) and must *not* be used as grounds to pool or split DSA estimates.

Sections 3 and 5 give details.

---

## 1. What I could read (exact access status)

| # | Work | Verification | What I read |
|---|---|---|---|
| 1 | Castelfranchi, C., Falcone, R. (2010). *Trust Theory: A Socio-Cognitive and Computational Model*. Wiley Series in Agent Technology. doi:10.1002/9780470519851, ISBN 978-0-470-02875-9. **Note: author order is Castelfranchi & Falcone, not Falcone & Castelfranchi as in the brief.** | Crossref [verified] | **Full TOC** (ETH Zürich TOC PDF). **Publisher reading sample** (e-bookshelf.de, 30 pp.: front matter, Introduction, start of Ch. 1). **§6.6 NOT read.** Google Books has a "partial preview" (volume id m82ikYnRpEAC), but page text could not be retrieved (automated-query block). Springer/Wiley/ResearchGate/Soton/CORE all blocked or closed. |
| 2 | Falcone, R., Castelfranchi, C. (2008). Generalizing Trust: Inferencing Trustworthiness from Categories. In Falcone, Barber, Sabater-Mir, Singh (eds), *Trust in Agent Societies* (TRUST 2008, Estoril, at AAMAS 2008), LNCS/LNAI 5396, pp. 65–80. doi:10.1007/978-3-540-92803-4_4 | Crossref [verified]. Search snippets say pp. 66–80; Crossref says 65–80, use Crossref | **Abstract only** (read directly on CNR IRIS / explore.cnr.it record; no file attached there). Full text not accessible |
| 3 | Falcone, R., Castelfranchi, C. (2004). Trust Dynamics: How Trust Is Influenced by Direct Experiences and by Trust Itself. *Proc. AAMAS 2004*, pp. 740–747 (IEEE CS / ACM). ACM id 10.5555/1018410.1018824. A Crossref DOI 10.65109/spsj1758 also exists | Crossref [verified] | **Abstract only** (Crossref). ResearchGate/ACM blocked |
| 4 | Falcone, R., Castelfranchi, C. (2010). Transitivity in Trust: A Discussed Property. *Proc. WOA 2010* (11th Workshop "Dagli Oggetti agli Agenti", Rimini), CEUR-WS Vol-621, paper 22 | CEUR volume page [verified] | **Full text** (6 pp.) |
| 5 | Venanzi, M., Piunti, M., Falcone, R., Castelfranchi, C. (2011). Facing Openness with Socio-Cognitive Trust and Categories. *Proc. IJCAI 2011*, pp. 400–405. doi:10.5591/978-1-57735-516-8/IJCAI11-075 | IJCAI site [verified] | **Full text** |
| 6 | Falcone, R., Piunti, M., Venanzi, M., Castelfranchi, C. (2013). From Manifesta to Krypta: The Relevance of Categories for Trusting Others. *ACM TIST* 4(2), 1–24. doi:10.1145/2438653.2438662. **Often cited as 2011; Crossref says 2013** | Crossref [verified] | **Abstract only** (Crossref). Soton PDF behind a bot wall |
| 7 | Castelfranchi, C., Falcone, R. (2000). Trust is much more than subjective probability. *Proc. HICSS-33*. doi:10.1109/HICSS.2000.926815 | [verified in R2] | **Full text** (re-read §3.2 internal/external attribution, §3.5 over-/under-confidence) |
| 8 | Burnett, C., Norman, T. J., Sycara, K. (2010). Bootstrapping Trust Evaluations through Stereotypes. *Proc. AAMAS 2010*, pp. 241–248 | Crossref [verified]. Caution: the Crossref record 10.65109/usfa8078 wrongly labels the container as the *Third* AAMAS; cite as AAMAS 2010 (9th), Toronto, pp. 241–248, without that DOI | **Full text** (IFAAMAS PDF) |
| 9 | Burnett, C., Norman, T. J., Sycara, K. (2013). Stereotypical Trust and Bias in Dynamic Multiagent Systems. *ACM TIST* 4(2), 1–22. doi:10.1145/2438653.2438661 | Crossref [verified] | **Abstract only** |
| 10 | Rehák, M., Gregor, M., Pěchouček, M., Bradshaw, J. (2006). Representing Context for Multiagent Trust Modeling. *Proc. IEEE/WIC/ACM IAT 2006*, pp. 737–746. doi:10.1109/IAT.2006.107 | Crossref [verified] | **Not read.** Author PDF (jeffreymbradshaw.net) returns 404; Wayback not reachable. Content below is from a search-engine summary of the PDF, so treat it as [unverified content] |
| 11 | Rehák, M., Pěchouček, M. (2007). Trust Modeling with Context Representation and Generalized Identities. *CIA 2007*, LNCS 4676, pp. 298–312. doi:10.1007/978-3-540-75119-9_21 | Crossref [verified] | **Not read** |
| 12 | Soh, H., Xie, Y., Chen, M., Hsu, D. (2019). Multi-task trust transfer for human–robot interaction. *IJRR* 39(2–3), 233–249. doi:10.1177/0278364919866905; arXiv:1807.01866 (v3, 2021). Earlier version RSS 2018 | arXiv API + Crossref [verified] | **Full text** (arXiv v3) |
| 13 | Şensoy, M., Yilmaz, B., Norman, T. J. (2016). STAGE: Stereotypical Trust Assessment Through Graph Extraction. *Computational Intelligence* 32(1), 72–101. doi:10.1111/coin.12046 | Crossref [verified] | **Abstract only** |
| 14 | Şensoy, M., Zhang, J., Yolum, P., Cohen, R. (2009). POYRAZ: Context-aware service selection under deception. *Computational Intelligence* 25(4), 335–366. doi:10.1111/j.1467-8640.2009.00348.x | Crossref [verified] | **Not read** |
| 15 | Teacy, W. T. L., Luck, M., Rogers, A., Jennings, N. R. (2012). An efficient and versatile approach to trust and reputation using hierarchical Bayesian modelling (HABIT). *Artificial Intelligence* 193, 149–185. doi:10.1016/j.artint.2012.09.001 | Crossref [verified] | **Not read** (repository blocked). Cited only as the MAS precedent for hierarchical pooling |
| 16 | Hermoso, R., Billhardt, H., Ossowski, S. (2007). Integrating Trust in Virtual Organisations. *COIN II*, LNCS 4386, pp. 19–31. doi:10.1007/978-3-540-74459-7_2 | Crossref [verified] | **Not read**; described second-hand from Burnett et al. 2010 §5 |
| 17 | Tavakolifard, M., Knapskog, S. J., Herrmann, P. (2008). Trust transferability among similar contexts. *Proc. 4th ACM Q2SWinet*, pp. 91–97. doi:10.1145/1454586.1454603 | Crossref [verified] | **Not read** (cited by #5) |
| 18 | Falcone, R., Castelfranchi, C. (2001). The Socio-cognitive Dynamics of Trust: Does Trust Create Trust? In *Trust in Cyber-societies*, LNAI 2246, pp. 55–72. doi:10.1007/3-540-45547-7_4 | Crossref [verified] | **Not read** |
| 19 | Jonker, C. M., Treur, J. (1999). Formal Analysis of Models for the Dynamics of Trust Based on Experiences. *MAAMAW'99*, LNCS 1647, pp. 221–231. doi:10.1007/3-540-48437-X_18 | Crossref [verified] | **Not read** |
| 20 | Keller, D., Rice, S. (2010). System-Wide versus Component-Specific Trust Using Multiple Aids. *J. General Psychology* 137(1), 114–128. doi:10.1080/00221300903266713 (online 2009) | Crossref [verified] | **Not read.** Its "system-wide trust" (one unreliable aid lowers trust in others) is quoted from memory and must be checked before citing |
| 21 | Mohsin, A., Janicke, H., Ibrahim, A., Sarker, I. H., Camtepe, S. (2025). A Unified Framework for Human AI Collaboration in Security Operations Centers with Trusted Autonomy. arXiv:2505.23397 (v3) | arXiv API [verified] | **Abstract + equations and task-autonomy table skimmed** (found in the novelty check) |

---

## 2. Per-work notes

### 2.1 Castelfranchi & Falcone (2010), *Trust Theory*: TOC + sample only

**What the accessible parts establish.**
- The Introduction says the model is "multi-factor and multi-dimensional … and a recursive one", where "trust in agent Y is based on beliefs about its powers, qualities, capacities; which actually are the basis for the global trust in Y, but also are sub-forms of trust: trust in specific virtues of Y (like 'persistence', 'loyalty', 'expertise', etc.)". This is point 4 of "The Characteristics of Our Trust Model".
- Trust is "context dependent, reasoning dependent, self-feed; and also reactive and interactive" (point 5).
- Chapter 2 shows "how trust implies an 'internal' attribution to the trustee, based on external cues" ("The Structure of the Book").
- Chapter 6 covers "how trust changes on the basis of the trustor's experiences; how trust is influenced by trust; how diffuse trust diffuses trust; how trust can change using generalization reasoning".

**TOC of the relevant parts (page numbers from the ETH TOC; OCR errors corrected where obvious):**
- §2.10 "The Other Parts of the Relation: the Delegated Task and the Context" (p. 82)
  - §2.10.2 "The Role of the Context/Environment in Trust" (p. 83)
- §3.6 "Generalizing the Trust Decision to a Set of Agents" (p. 111)
- §6.2 "Experience as an Interpretation Process: Causal Attribution for Trust" (p. 150)
- §6.6 "Trust Through Transfer and Generalization" (p. 174)
  - §6.6.1 "Classes of Tasks and Classes of Agents" (p. 175)
  - §6.6.2 "Matching Agents' Features and Tasks' Properties" (p. 175)
  - §6.6.3 "Formal Analysis" (p. 177?; the OCR shows "111")
  - §6.6.4 "Generalizing to Different Tasks and Agents" (p. 178)
  - §6.6.5 "Classes of Agents and Tasks" (p. 182)
- §6.7 "The Relativity of Trust: Reasons for Trust Crisis" (p. 184)

**Covers (cannot be claimed by WorkTrace):** the idea that trust is task-relative, decomposable into "virtues", and transferable across classes of tasks and agents by reasoning over features and properties.

**Leaves open (from accessible parts):** how the features of tasks/agents are *measured*. Nothing in the accessible material suggests controlled testing.

**Citation caution:** cite §6.6 only as "C&F analyse transfer and generalisation of trust across classes of tasks and agents by matching agents' features to tasks' properties (2010, §6.6; 2008)". Do not attribute any formula until §6.6 is read.

### 2.2 Falcone & Castelfranchi (2008), "Generalizing Trust": abstract only

**Problem (verbatim abstract, CNR IRIS).**

> "starting from a socio-cognitive model of trust, we analyze how it is possible to predict how/when an agent who trusts something/someone will therefore trust something/someone else, before and without a direct experience … a) given X's evaluation about Y's trustworthiness on a specific task τ, what can we say on X's evaluation about Y's trustworthiness on a different but analogous task τ'? What would we intend for an analogous task? b) Given X's evaluation about Y's trustworthiness on a specific task τ, what can we say on X's evaluation about the trustworthiness of a different agent Z on the same task τ? In fact, in our view only a cognitive model of trust, with its analytical power, seems able to account for the inferential generalization of trustworthiness from task to task and from agent to agent not just based on specific experience and/or learning."

Keywords: "Trust; Class and Task Generalizations; Inference; Reasoning".

- **Method / evaluation:** unknown (not read). Probably conceptual and formal, with no empirical evaluation (the book's §6.6 has "Formal Analysis"). [unverified]
- **Covers:** the *question* WorkTrace faces when pooling rare classes (a). It also argues that the answer must come from an analytic model of *why* Y is trustworthy, not from frequencies.
- **Leaves open:** empirical validation, and any statistical guarantee.
- **Draft differentiation:** "Falcone and Castelfranchi ask when trust earned on task τ licenses trust on an analogous task τ′ and answer by reasoning over the qualities that τ′ requires; WorkTrace measures those qualities directly by evidence interventions per decision class and allows transfer only where a certified class dominates the target class in required qualities."
- **Citation caution:** full text unread. Paper metadata lists the second author as "Falcone, Rosario" (Rino = Rosario).

### 2.3 Falcone & Castelfranchi (2004), "Trust Dynamics" (AAMAS): abstract only

**Problem (verbatim abstract, Crossref).**

> "a) How direct experiences involving trust, with their successes or failures, influence the future trust of an agent about similar facts. We challenge the trivial idea that always success increases trust while failure decreases it. … We claim that a cognitive attribution process is needed in order to update trust on the basis of an 'interpretation' of the outcome of A's reliance on B and of B's performance (failure or success). b) How the fact that A trusts B and relies on it in situation Ω can actually (objectively) influence B's trustworthiness in the Ω situation. Either trust is a self-fulfilling prophecy … or it is a self-defeating strategy … We present a formal model of these dynamic nontrivial aspects."

- **Covers:** non-monotonic, attribution-mediated updating. The phrase "about similar facts" shows that updates are scoped to similar tasks/situations. It also covers the reflexive effect of delegation on trustworthiness.
- **Leaves open:** how to *observe* the internal-vs-external attribution of an outcome. In WorkTrace, ground truth by construction supplies exactly this for generated episodes.
- **Draft differentiation:** "Falcone and Castelfranchi argue that experience should update trust only through a causal attribution of each outcome to the trustee or to circumstances; WorkTrace's loss (unjustified action, detected by evidence interventions) is such an internal attribution made operational, and its revocation e-process accumulates only internally attributed failures."
- **Citation caution:** abstract only. The book §6.2 ("Experience as an Interpretation Process: Causal Attribution for Trust") presumably contains the mature version.

### 2.4 Falcone & Castelfranchi (2010), "Transitivity in Trust" (WOA, CEUR Vol-621): FULL TEXT

**Problem & contribution.** The paper analyses whether "X trusts Y" and "Y trusts Z" imply "X trusts Z". It argues that this depends on the *task*, on the competence/willingness split, and on trust dynamics.

**Method (conceptual + formal notation).**
- Trust is "a relational construct between the trustor (X), the trustee (Y), about a defined (more or less specialized) task (τ): Trust (X Y C τ g_X)", where C is "the context … in which the relationship is going to happen" (§II).
- Beliefs: Bel(X Can_Y(τ)), Bel(X Will_Y(τ)), Bel(X ExtFact_Y(τ)), and "DoT_XYτ = f(DoC_X(Opp_Y(τ)), DoC_X(Abil_Y(τ)), DoC_X(Will_Y(τ)))". "X will trust Y about the task τ if DoT_XYτ > σ" (§II).
- Threshold σ is treated as "dependent just from the specific intrinsic characteristics of the trustor (… prudent, reckless …) independently from the external circumstances (on the contrary, these factors affect the degree of trust …)" (§III). **σ (risk acceptance) is separate from DoT (beliefs about Y).**
- "X trusts Y on the basis of the evaluation of Y's 'virtues/qualities', not just on the basis of a statistical sampling, some probability. The evaluations about the needed 'qualities' of Y for τ are the mediator for the decision to trust Y" (§III).
- **Transfer across tasks (case C, τ ≠ τ′):** "the transitivity essentially depends from the implication … are there elements in the reasons (believed by X) for trusting Y on the task τ that (in X's view) are sufficient also for trusting Y on the different task τ′?" (§III).
- **Meta-task:** being trustworthy on τ does not entail being trustworthy on "the meta-task of evaluating τ": Bel(X Trustworthiness(τ) > σ) implies Bel(X Trustworthiness(eval(τ)) > σ) must be an explicit assumption (§III).
- **Subtasks:** trust in Y about τ does not transfer to the agents to whom Y delegates subtasks τ1, τ2 unless X knows how the subtask delegation is done and how the subtasks interact (§III.A).
- **Competence vs willingness:** "even assuming that the competence is rather stable … not necessarily Z's willingness is equally stable and transferable … This is a more relation-based dimension" (§III.B).
- **Dynamics:** "Trust 'dynamics' between Y and Z, is not automatically identical to trust 'dynamics' between X and Z" (§III.C).

**Evaluation:** none.

**Covers (do not claim):**
- task- and context-relativity of trust;
- transfer between tasks justified by shared *reasons/qualities*;
- the competence/willingness asymmetry in transfer;
- trust in the evaluator as a separate meta-task.

**Leaves open:** how the "reasons for trusting Y on τ" are established and checked. The paper assumes X *believes* them.

**Draft differentiation:** "Falcone and Castelfranchi make transfer of trust from τ to τ′ depend on whether the reasons for trusting Y on τ suffice for τ′; WorkTrace makes those reasons explicit and testable: a DSA profile per requirement, measured by evidence interventions, and a class's required profile, so that transfer is a checkable inclusion rather than a belief."

**Citation caution:** a workshop paper in Italian national workshop proceedings, and a short conceptual piece. Fine for a definitional citation; pair it with the book.

### 2.5 Venanzi, Piunti, Falcone & Castelfranchi (2011), IJCAI: FULL TEXT

**Problem & contribution.** Trust formation in open MAS via "categorial reasoning". Categorisation recognises "signs (Manifesta) through which hidden capabilities (Kripta) can be inferred". Learning refines "reasoning attitudes needed to ascribe tasks to categories" (Abstract).

**Method.**
- Trust(ag_i, ag_j, E, τ). Delegate if DoT > σ, and choose the trustee with the highest DoT (§2, Alg. 1).
- "We model a set of tasks τ ∈ T, each task being identified by a couple (action, goal) … Tasks are specified by a list of practical requirements that agents performing the related actions have to comply with in terms of categories" (§3).
- Categories are professional (abilities), dispositional (willingness) and crosscutting. Each is "specified by a record of features, shaped on concrete dimensions and range of values" (§3, Table 1).
- An `ascribe(Cat, τ)` matchmaking function rates how well a category fits a task (§4.3).
- Three trust-eval implementations:
  - a neural net on (τ, E, manifesta);
  - Stereotrust-style C4.5 data mining (after Burnett et al. 2010);
  - a learning Fuzzy Cognitive Map (UnFCM) whose nodes are C&F beliefs: Bel(Can), Bel(Will), Bel(ExtFact), plus an Experience node.
- "direct experience (when available) dominates the categorial reasoning" (§4.3).

**Evaluation.** Simulated medical domain:
- 100 trustees drawn from 2,500 profiles; 5 professional, 6 dispositional and 2 crosscutting categories; one task ("chickenpox");
- environmental noise ρ = 5, openness δ = 5, learning interval L = 10; 20 trials × 150 rounds.

Results:
- Neural reaches score ≈ .95 and error < .1 after ≈ 32 rounds.
- LFCM reaches ≈ .85 and error < .1 after 16 rounds ("20% more efficient than Neural", t-test p < .05).
- Informed LFCM (initialised with `ascribe`) learns in 6 rounds; Deceptive LFCM needs ≈ 50 rounds but converges.

**Covers (do not claim):**
- tasks defined by requirements;
- categories defined by feature ranges;
- matching requirements to categories for delegation;
- learning category–task fit;
- experience overriding category priors;
- an explicit split into competence vs disposition vs external-factor nodes.

**Leaves open:**
- Ground truth is simulated "krypta" compared to thresholds; trustworthiness is outcome score.
- No test of *how* a trustee decides.
- A single task, so no cross-task transfer is evaluated.

**Draft differentiation:** "Venanzi et al. infer hidden competences ('krypta') from observable signs ('manifesta') via categories; WorkTrace does not infer the competence from signs but elicits it by intervention, treating an agent's declared grounds as manifesta whose honesty is tested by removing, isolating, inverting or corroborating the evidence they cite."

**Citation caution:** a short paper with a toy domain, and a single task despite the framing.

### 2.6 Castelfranchi & Falcone (2000), HICSS: FULL TEXT (re-read for attribution)

- **Internal vs external attribution** (§3.2): the global probability of success "should be decomposed into the probability of y performing the action well (that derives from the probability of willingness, persistence, engagement, competence: internal attribution) and the probability of having the appropriate conditions (opportunities and resources: external attribution) … and of not having interferences and adversities (external attribution)".
- Why this matters: "a) the agent's trusting/delegating decision might be different with the same global probability or risk, depending on its composition; b) trust composition (internal versus external) produces completely different intervention strategies" (§3.2).
- Sources of trust beliefs go beyond experience: "the basis and the dynamics of trust cannot be reduced to reinforcement learning or probability updating on the basis of personal experience … Trust beliefs come also from other sources: from observations, reasoning, social stereotypes, communication, spreading of reputation, signs" (§1).
- **Over-confidence consequence** relevant to DSA (§3.5): "Too open delegation: in other words, a delegation that permits (obligates) the trustee to make chooses, plans, etc., and he is unable to realize such a kind of actions."
- **Under-confidence consequences** include "We make too many controls … We specify too much the task/role without exploiting trustee's competence, intelligence, or local information".

**Use for WorkTrace.**
- DSA is the competence that *open* delegation presupposes: making the choice well within discretion.
- C&F name both the risk of too-open delegation and the cost of over-control, but do not measure that competence.
- The internal/external split maps onto WorkTrace's separation between the agent's evidence handling (DSA, internal) and evidence availability or quality (generator-controlled Opp/ExtFact, external).

### 2.7 Burnett, Norman & Sycara (2010), AAMAS: FULL TEXT

**Problem & contribution.** Bootstrapping trust when direct and reputational evidence is absent (cold start, newcomers, short-lived ad-hoc groups). Agents learn stereotypes, i.e. a function from observable agent features to an initial trust estimate.

**Method.**
- Subjective Logic opinions ω^x_{y:t} = ⟨b, d, u, a⟩ are kept per trustee *and task t* (§3.1.1). Evidence counts r, s give b = r/(r+s+2), etc. (Eq. 3). Expected value P = b + a·u (Eq. 4).
- **The stereotype sets the base rate a = S(F_y)**, so "as more evidence is received, the value of u decreases, and so the effect of a also decreases. This satisfies our fundamental condition that a stereotype must yield to concrete evidence as it is obtained" (§3.1.5).
- S is learned with M5 model trees over binary agent features every L experiences (§3.2).
- Stereotypical reputation is weighted by model fit, c_ρ = 1 − RMSE (Eqs. 6–7).
- §2: "an agent may learn … that agents who have performed competently in one role can therefore be trusted in another".

**Evaluation.**
- Simulation: 500 trustees in 5 performance profiles, 20 trustors, 20 ad-hoc groups of size 10 with lifetime 5, 6 noise features, L = 100, 800 rounds.
- Stereotyping beats the non-stereotyping baseline in all six conditions after the first learning interval (t-test p < 0.05). Example: ad-hoc interaction with global reputation, ≈ 0.8 vs ≈ 0.6 mean outcome.
- Under high dynamism (replacement probability 0.5): ≈ 0.8 vs ≈ 0.5.
- With noise-only features: identical to baseline.
- With unreliable features (0.8/0.2): small gain.

**Covers (do not claim):**
- class-based (stereotype) priors that yield to individual evidence;
- learning which features predict trustworthiness;
- "no worse than baseline when features are uninformative".

**Leaves open:**
- Features are features of *agents*, not of *tasks*. The opinion is per task t, but stereotypes are not shared across tasks.
- Trust is outcome-based.
- Decisions use arg max, without risk; the authors flag this themselves: "the problem of trust evaluation … is distinct from the problem of deciding to trust" (§5).
- No guarantee.

**Related work they summarise (second-hand):** Hermoso et al. 2007 represent trust over triples ⟨B, R, I⟩ (agent, role, interaction). They generalise by wildcards: ⟨_, R, I⟩ means "any agent in role R performing interaction I"; ⟨B, _, I⟩ means "agent B performing interaction I in any role". Aggregation is by weighted mean (§5). **This is the closest MAS precedent for WorkTrace pooling a class across sub-contexts.**

**Draft differentiation:** "Stereotype-based trust bootstraps outcome-based estimates for unknown partners from agent features (Burnett et al., 2010); WorkTrace instead bootstraps the evidence-handling profile of a known agent across decision classes, and only through classes that dominate the target in required evidence competences."

**Citation caution:** do not use the Crossref DOI 10.65109/usfa8078 (wrong container metadata). The extended version is ACM TIST 2013.

### 2.8 Soh, Xie, Chen & Hsu (2019), IJRR: FULL TEXT (arXiv v3)

**Problem & contribution.** "how human trust in robot capabilities transfers across multiple tasks" (Abstract). The paper adopts C&F's view of trust as a psychological attitude and focuses on competence.

**Method.**
- Human-subjects study (n = 32), with a household domain (Fetch robot) and a driving domain (VR). Tasks fall into 2 categories × 2 difficulty levels.
- Participants saw two successes or two failures, then rated trust on tasks from three cells: same category and difficulty; same category, other difficulty; other category, same difficulty.
- Computational models treat trust as a latent function over task features, τ^a_t(x): R^d → [0, 1], updated by g(τ_{t−1}, o_{t−1}) (Eq. 1). Three variants:
  - a GP with a projection kernel over a learned low-dimensional "psychological task space" (Eqs. 4–13);
  - a GRU-based neural model (Eqs. 14–20);
  - a GP-neural hybrid (Eq. 21).
- Task features are 50-d GloVe averages of the task descriptions.

**Evaluation.**
- Same-category trust distance M = 0.28 vs different-category M = 1.78 (household; t(31) = −5.82, p < 1e−5).
- Trust change is larger for same-category tasks, but **non-zero across categories** ("trust transfers even between task categories, albeit to a lesser extent", §3.4).
- **Asymmetry:** "positive trust transfers more easily to simpler tasks than to more difficult tasks" (H3 supported). For failures, the reverse tendency (distrust transfers to harder tasks) is not significant at 1% (H4).
  - Caution: the M values printed for H3 in §3.4 look inconsistent with the stated direction; rely on the stated finding and Fig. 7.
- General (Muir) trust correlates with task-specific trust at ρ = 0.93–0.94 for same category and difficulty, but only 0.50–0.60 for different categories (Fig. 8).
- The models beat constant and linear-Gaussian (OPTIMo-like) baselines on held-out participants (E1) and held-out tasks (E2, leave-one-task-out). The GPNN is best overall.
- **Failure mode:** with surface-text features, "the same model predicts the human highly trusts the robot's capability to 'Navigate to the moon' (τ = 0.83)" (§5.3).

**Covers (do not claim):**
- empirical evidence that (human) trust is task-specific and transfers in a graded, similarity- and difficulty-dependent, asymmetric way;
- differentiable models of transfer over learned task spaces;
- leave-one-task-out evaluation.

**Leaves open:**
- It models *human trust*, not *trustworthiness*.
- Its ground truth is self-reported trust, not the robot's actual capability.
- Outcome-only observations; no test of the basis of the robot's decisions.

**Draft differentiation:** "Soh et al. model how human trust in a robot transfers across tasks as a function of task similarity and difficulty; WorkTrace instead asks when an agent's *measured* evidence-handling competence in one decision class may stand in for a test in another, and treats similarity as inclusion of required competences rather than closeness in a description space."

**Citation caution:** small n; self-report. Their own surface-similarity failure ("moon") supports defining similarity structurally.

### 2.9 Rehák, Gregor, Pěchouček & Bradshaw (2006), IAT: NOT READ (search summary only) [unverified content]

According to a search-engine summary of the PDF:
- the model places situations in a metric space;
- it keeps trust data at "reference contexts" found by Leader–Follower clustering;
- it updates and queries each reference context "with the weight that decreases with distance";
- it reports that context-aware models beat general ones when context matters and match them otherwise.

The CIA 2007 follow-up adds "generalized identities".

**Use:** cite only as the MAS precedent for *distance-weighted* sharing of trust across contexts, and only after reading it.

**Differentiation (tentative):** distance-weighted sharing assumes smoothness of trustworthiness in context space. WorkTrace instead requires dominance in required competences plus a class-specific check, because a small change in evidence structure (e.g., a second source becoming available) can change the right action discontinuously. The AMLR art. 24(2)(b) example shows this.

### 2.10 Şensoy et al.: abstract only / not read

- **STAGE (2016), abstract:** "malicious agents may share some common patterns or complex features in their descriptions … we propose the use of frequent subgraph mining … to estimate a priori trust for agents … the proposed approach significantly outperforms well-known trust approaches if trustworthiness of agents is correlated with patterns … at least as good … if such correlations do not exist."
  - Same family as Burnett: agent-feature priors for newcomers. Not task transfer.
- **POYRAZ (2009):** context-aware service selection under deception; not read.

**Use:** one clause in related work ("stereotype/feature-based a priori trust: Burnett et al. 2010; Şensoy et al. 2016").

### 2.11 Mohsin et al. (2025), arXiv:2505.23397: skimmed

- Five autonomy tiers mapped to SOC functions, with "task-specific trust thresholds".
- Trust T = α1·E + α2·P + α3·(1 − U), built from explainability, past performance and uncertainty.
- Autonomy A = 1 − (λ1·C + λ2·R)(1 − T), from complexity and risk.
- Illustrated by a simulated cyber range with an LLM assistant.

**Threat:** low. This is per-task autonomy with hand-set trust formulas; there are no tests of decision basis and no held-out evaluation. Add it to the list of "per-task autonomy without tested basis" baselines (with Feng et al., Tomašev et al.).

**Citation caution:** preprint; heuristic formulas.

### 2.12 Not read; to be checked before citing

- Jonker & Treur 1999: trust-evolution functions over experience sequences.
- Falcone & Castelfranchi 2001: "does trust create trust?".
- Keller & Rice 2010: system-wide trust (contagion of distrust across aids).
- HABIT (Teacy et al. 2012): hierarchical Bayesian pooling.
- Tavakolifard et al. 2008: trust transferability among similar contexts.

All five are bibliographically verified.

---

## 3. Answers to the key questions

### (a) How the classic theory scopes trust, and when it transfers

**Scope.** Trust is never "X trusts Y" simpliciter but Trust(X, Y, C, τ, g_X), with τ = (α, g) and C the context (WOA 2010 §II; IJCAI 2011 §2; C&F 1998 §2 in R2).

The degree of trust DoT_XYτ composes three credibilities: about Y's ability Abil_Y(τ), Y's willingness Will_Y(τ), and the external opportunities Opp/ExtFact_Y(τ). It is compared with a trustor-specific threshold σ. A task can be "more or less specialized", so granularity is a modelling choice, not given.

**Transfer between tasks.** Transfer is *inferential*, not statistical. X may trust Y on τ′ if "the reasons (believed by X) for trusting Y on the task τ … are sufficient also for trusting Y on the different task τ′" (WOA 2010 §III, case C).

The mediating objects are Y's "qualities/virtues" relevant to τ. The machinery (from the book TOC and the 2008 abstract; §6.6 not read) is matching **tasks' properties** (what τ′ requires) to **agents' features** (what Y has, believed from τ).

Additional constraints from the accessible texts:
1. **Competence transfers more readily than willingness.** "competence is rather stable"; willingness is "relation-based" (WOA §III.B).
2. **Doing τ ≠ evaluating τ.** Trust in the meta-task eval(τ) needs its own grounds (WOA §III).
3. **Subtasks do not inherit trust** without knowing how they are delegated and integrated (WOA §III.A).
4. **Direct experience dominates category-based inference when available** (IJCAI 2011 §4.3; Burnett 2010 §3.1.5).

**Empirically** (Soh et al.):
- transfer is graded by similarity;
- it is non-zero even across categories;
- positive trust transfers *down* in difficulty but not up.

### (b) What this implies for WorkTrace's decision classes and pooling

**Definition.** Define a decision class by *requirements*, not by surface topic. Following τ = (α, g) and the features/properties matching, a class c has two parts.

1. **Task core:** the goal g_c and the admissible action set A_c (incl. escalate/refuse).

2. **Evidence-competence requirements R_c:** which DSA dimensions a correct decision in c needs, for example:
   - whether a decisive item exists and must be read (remove/only tests);
   - whether sources can be stale or contradictory (invert test, contradiction boundary);
   - whether independent corroboration changes the right action (second-source test);
   - whether the authority scope binds;
   - whether escalation conditions exist.

   These are exactly the "tasks' properties" that agents' measured "features" (the DSA profile) must match.

3. **Context/risk parameters K_c:** stakes, reversibility, legal reservation, escalation cost.

**Separation (mirrors DoT vs σ).**
- R_c determines *which* DSA estimates are relevant to c.
- K_c determines *how strict* the acceptance is (α_c, refuse-regardless constraints).
- Two classes that differ only in K_c may **share** the DSA estimate but **not** the threshold.
- Two classes with the same stakes but different R_c must **not** share estimates.

This avoids a common confusion: pooling "high-risk" classes together because they are risky. Under C&F, risk lives in the threshold, not in the trust belief.

**Similarity.** Use **inclusion (dominance) of requirements**, not distance in a description space.
- Soh et al.'s "navigate to the moon" failure shows that surface similarity misleads.
- Rehák-style distance weighting assumes smoothness that evidence structure violates: adding one independent source can flip the correct action.

**Granularity.**
- Classes too fine → too few episodes per class (cold start, rare classes). Under zero-failure Clopper–Pearson, 29 (α = 0.10) to 59 (α = 0.05) episodes per class are needed just to certify, and ~100+ for power.
- Classes too coarse → heterogeneity hides a failing sub-class (Simpson-type masking).
- Rule: split a class when calibration data show heterogeneous unjustified-action rates across values of a requirement feature. Merge only when requirements are identical. Report the class partition as pre-registered.

**May a DSA profile earned in one class inform another (pooling rare classes)?** The theory says yes, *if and only if* the reasons that justified trust in the source class suffice for the target class. Made operational:

- **(P1) Dominance transfer only.** A profile from class s may inform class t only if R_t ⊆ R_s and the source passes those requirements at least as hard as t demands. Graded difficulty must not decrease from s to t, consistent with Soh's asymmetry: success transfers to easier tasks, not harder ones.
- **(P2) A transferred profile is a prior, not a certificate.** As in Burnett's base rate and Venanzi's "experience dominates", transferred information may:
  - order which classes to test first;
  - justify *escalate* (conservative) decisions;
  - shrink estimates via hierarchical pooling (HABIT-style).

  But a **proceed** grant in class t needs class-t-specific held-out evidence. Alternatively, an explicit, pre-registered exchangeability assumption plus a small "sentinel" sample in t that can falsify the transfer.

  Reason: borrowed strength breaks the finite-sample guarantee P(unjustified | autonomous, c) ≤ α_c unless the classes are exchangeable. That is an assumption, not a result.

- **(P3) Transfer competence, never willingness-type properties.** WorkTrace already leaves willingness unmeasured. Transfer only measured DSA dimensions, and only between classes under the same principal/permission regime. Under C&F, relation-dependent properties do not transfer.

- **(P4) Self-evaluation is a separate requirement.** "Escalates correctly" (the agent evaluating its own competence) is the meta-task eval(τ). It is not implied by doing τ well and must have its own test in each class.

### (c) Trust dynamics: direct experience and revocation

**Attribution before update** (C&F 2000 §3.2; F&C 2004). Outcomes should update trust only after being attributed to the trustee's internal powers or to external conditions; "success always increases / failure always decreases" is rejected.

WorkTrace's loss already *is* an internal attribution:
- a wrong action on correct, available evidence counts against the agent;
- a right action on the wrong basis counts against the agent, even though the outcome was good;
- a wrong outcome caused by misleading evidence that the episode design made undetectable is *external* (ExtFact). It should be charged to the evidence pipeline, not to the agent's DSA.

**Recommendation:** in the revocation e-process, accumulate only internally attributed failures. Track externally attributed failures as a separate signal that triggers review of the evidence environment and class definition, not revocation. In production, where ground truth is missing, make attribution conservative (count ambiguous cases as internal) and say so.

**Propagation across classes (asymmetric).**
- Positive evidence transfers only downward (P1).
- Negative evidence should propagate *more* readily, along shared requirements. An internally attributed failure on requirement r in class s should trigger re-testing (or temporary escalation) in every proceed class t with r ∈ R_t.
- Rationale: Soh's direction of distrust transfer (not significant); Keller & Rice's system-wide trust (not read); and C&F's "reasons for trust crisis" (§6.7, not read). This gives "grant locally, revoke along shared requirements".

**Reflexive effect** (F&C 2004 b; WOA §III.C). Delegation can change the trustee's trustworthiness. For LLM agents, the permission and autonomy regime is part of the episode (P), and behaviour can differ when the agent "knows" it is autonomous or supervised.

**Recommendation:** measure DSA under the same permission/delegation framing the grant would create (the proceed regime). After a grant, re-test the class in the granted regime before relying on it. This is a concrete, theory-grounded design control.

**Context shift.** Trust is relative to C. A DSA certificate is conditional on the evidence-environment distribution (Opp/ExtFact). WorkTrace's primary endpoint under *evidence shift* is the right test of whether the competence belief is internal (it should survive a change in C) rather than an artefact of C.

### (d) Constructs in this tradition that overlap DSA

| Construct | Source | Overlap with DSA | Threat? |
|---|---|---|---|
| Ability/competence belief Can_Y(τ), DoC(Abil_Y(τ)) | C&F 1998/2000; WOA 2010 | DSA is a *specific operationalisation* of the competence belief for *decision-making under evidence* (discretion within open delegation) | No. C&F name the belief but do not measure it. Position DSA as "a measured competence belief" |
| Internal trust / internal attribution ("trust 'in' y relative to its internal powers") | HICSS 2000 §3.2; Book Intro, Ch. 2 | DSA = internal component; generator controls the external component | No. Strengthens the framing |
| Competence required by open delegation; "too open delegation" as over-confidence | HICSS 2000 §3.5; C&F 1998 §2.7 | DSA is the competence open delegation presupposes | No. Good citation for *why* DSA matters |
| Krypta/manifesta (hidden qualities vs observable signs) | Bacharach & Gambetta 2001 via IJCAI 2011 | Declared grounds = manifesta; DSA tests whether they are honest signals of krypta | No. Useful vocabulary. Bacharach & Gambetta not verified here |
| Meta-task eval(τ) | WOA 2010 §III | DSA's "recognising boundaries / escalating correctly" | No |
| Delegee self-confidence in adjustable autonomy | F&C 2001 SMC-A (R2, abstract) | Agent-initiated escalation | No |
| "Task-dependent functional trust" | Soh et al. 2019 | Function over tasks, but of human *trust*, not measured trustworthiness | No |

**Conclusion.** No construct in this tradition has DSA's content (tested structure of decisions with respect to evidence, authority and revision). The tradition supplies the *slot* DSA fills: the competence/ability belief, internally attributed, per task, as the basis for open delegation. That is a strength for W1.

---

## 4. (e) Draft paragraphs for the paper: "Decision classes" (≈1 page)

> **Decision classes.** Following the socio-cognitive theory of delegation, trust is never a global attitude towards an agent but a relation about a task in a context: X trusts Y about τ = (α, g) in context C to the degree that X credits Y's ability and willingness and the external conditions for τ, and X delegates when that degree exceeds a threshold reflecting X's acceptance of risk (Castelfranchi & Falcone, 1998; 2000; 2010; Falcone & Castelfranchi, 2010). WorkTrace adopts this structure and makes the *decision class* its unit of delegation. A decision class c is a family of decision situations that share (i) a goal and an admissible action set, including *escalate* and *refuse*; (ii) a set of evidence-competence requirements R_c, the decision-structured capacities that a justified decision in c demands, such as reading the decisive item, detecting stale or contradictory sources, responding to independent corroboration, respecting the authority scope, and recognising when to escalate; and (iii) risk parameters K_c (stakes, reversibility, escalation cost, legal reservation).
>
> Requirements and risk play different roles, mirroring the theory's separation between the degree of trust and the acceptance threshold. R_c determines which components of an agent's decision-structured agency (DSA) profile bear on c; K_c sets the tolerated rate α_c of unjustified autonomous actions and, for legally reserved classes, forces escalation regardless of measured competence. Classes that differ only in K_c may share DSA estimates but not thresholds; classes that differ in R_c may not share estimates even if their stakes coincide.
>
> **Granularity.** The theory allows tasks to be "more or less specialized"; we fix granularity empirically. The class partition is pre-registered, and a class is split when calibration episodes show heterogeneous unjustified-action rates across a requirement feature, since a coarse class can hide a failing sub-class behind a good average.
>
> **Transfer across classes.** Castelfranchi and Falcone treat generalising trust from task to task as an inference: trust earned on τ licenses trust on τ′ only if the reasons for trusting the agent on τ suffice for τ′ (Falcone & Castelfranchi, 2008; 2010; Castelfranchi & Falcone, 2010, §6.6). Computational work operationalises such generalisation through categories, stereotypes and task similarity (Venanzi et al., 2011; Burnett et al., 2010; Soh et al., 2019). It finds that class-level information helps when direct evidence is scarce but must yield to it, and that transfer is asymmetric, flowing to easier rather than harder tasks. WorkTrace makes the "reasons" explicit and testable. Because a DSA profile is measured per requirement by interventions on evidence, transfer from a source class s to a target class t is admissible only when R_t ⊆ R_s and the source tests were at least as demanding. Even then, the transferred profile serves as a prior that orders testing and supports conservative decisions; it does not by itself certify autonomy. A *proceed* grant in t requires class-specific held-out episodes, or an explicitly stated exchangeability assumption together with a sentinel sample in t that can falsify it. We transfer only measured competences, never relation-dependent properties, and we test escalation, the agent's evaluation of its own competence, separately in every class, since competence on a task does not imply competence in evaluating it (Falcone & Castelfranchi, 2010).
>
> **Dynamics and revocation.** Experience should revise trust through a causal attribution of each outcome to the agent or to the circumstances, not through reinforcement on success and failure (Castelfranchi & Falcone, 2000; Falcone & Castelfranchi, 2004). WorkTrace's loss is such an attribution: an unjustified action (a wrong action, or a right action on the wrong basis) is charged to the agent, whereas a failure caused by evidence that could not have revealed the right action is charged to the evidence environment. The revocation process accumulates only the former. Positive evidence transfers between classes only by dominance, but an attributed failure on a requirement triggers re-testing or escalation in every proceeding class that shares that requirement. Because delegation can itself change the trustee's behaviour (Falcone & Castelfranchi, 2004), DSA is measured under the permission regime that the grant would create.

**Citations to verify before use:**
- Book §6.6 wording (unread).
- Falcone & Castelfranchi 2004 (abstract only).
- The 2008 chapter (abstract only).

All others in the paragraph were read in full.

---

## 5. Implications for WorkTrace

### Design changes

1. **Class schema.** Encode each class as (g_c, A_c, R_c, K_c). Publish R_c as a requirement vector over DSA dimensions and K_c separately. Pool DSA estimates only over classes with identical R_c; never pool by stakes.
2. **Transfer rule (dominance + sentinel).** Implement P1–P4 from §3(b). In the experiment, pre-register:
   - which source→target transfers are admissible;
   - the sentinel sample size per rare class (e.g., ~10–20 episodes as a falsification check, separate from the certificate).
3. **Add an ablation:** per-class certification vs dominance-transfer vs naive pooling (all classes) vs similarity-weighted pooling (embedding distance, Soh/Rehák-style). Compare at matched coverage under evidence shift. This directly tests whether requirement-based classes beat surface-similarity classes, and pre-empts the reviewer question "why these classes?".
4. **Attribution in the e-process.** Count only internally attributed unjustified actions. Log externally attributed failures separately. State the conservative rule for ambiguous production cases.
5. **Revocation propagation along shared requirements;** grants stay local. Measure how often propagation fires and what it costs in coverage.
6. **Measure under the granted regime.** Add a check that DSA measured in "supervised" framing equals DSA in "autonomous" framing. If not, that is itself a finding (reflexive trust effect).
7. **Class granularity check.** On calibration data, test heterogeneity across requirement features within each class. Split if significant. Report the final partition.

### Risks

- **Reviewer from MAS:** "decision classes are just C&F's τ; generalisation across classes is C&F 2008/2010 §6.6; stereotypes and category trust are Burnett/Venanzi." **Mitigation:** cite all of these and claim only measurement by intervention, the certification-constrained transfer rule, and the empirical comparison.
- **Pooling vs guarantee:** any borrowing across classes weakens the per-class finite-sample certificate. State this explicitly; never claim a per-class guarantee for a class certified by transfer.
- **Unread §6.6:** if it already contains a formal inclusion rule, cite it as the source of P1.
- **Surface similarity is tempting** (embedding LLM task descriptions) but is known to fail (Soh "moon" example). Do not use it as the class-similarity metric. Use it only as an ablation.

### Things to cite

**Must cite:**
- Castelfranchi & Falcone 2010 (book; §6.6 only as a pointer until read);
- Falcone & Castelfranchi 2008 (LNCS 5396);
- Falcone & Castelfranchi 2010 (WOA, CEUR Vol-621);
- Castelfranchi & Falcone 2000 (HICSS);
- Falcone & Castelfranchi 2004 (AAMAS);
- Venanzi et al. 2011 (IJCAI);
- Burnett, Norman & Sycara 2010 (AAMAS);
- Soh et al. 2019 (IJRR).

**Should cite:**
- Falcone et al. 2013 (TIST);
- Burnett et al. 2013 (TIST);
- Şensoy et al. 2016 (STAGE);
- Hermoso et al. 2007;
- Rehák et al. 2006 (after reading);
- Teacy et al. 2012 (HABIT) for hierarchical pooling (after reading);
- Mohsin et al. 2025 (per-task autonomy without tested basis).

**Optional (read first):** Jonker & Treur 1999; Keller & Rice 2010; Tavakolifard et al. 2008; Falcone & Castelfranchi 2001 (LNAI 2246).

### Still to read before submission

- Book §6.2, §6.6, §6.7 and §3.6 (library or Wiley access).
- LNCS 5396 chapter, pp. 65–80.
- AAMAS 2004 full text.
- Rehák et al. 2006.
- HABIT §3–4 (how pooling and its exchangeability assumptions are handled).
