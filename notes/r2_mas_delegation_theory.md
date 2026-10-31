# R2 — Classic MAS delegation, trust and adjustable autonomy: the theory bridge (contribution 1)

Round-2 reading note, 2026-10-25. Scope: the classic MAS and human-factors literature that WorkTrace's contribution 1 ("a bridge between classic MAS delegation/trust/adjustable-autonomy theory and modern LLM-agent auditing") must build on, plus the 2025–2026 works on levels of autonomy, framed autonomy and AI delegation found while doing that.

---

## 0. Read first: threats to novelty

1. **Tomašev, Franklin & Osindero (Google DeepMind), "Intelligent AI Delegation", arXiv:2602.11865 (Feb 2026). This already makes the bridge, at the level of concepts.** It cites Castelfranchi & Falcone 1998, Falcone & Castelfranchi's adjustable social autonomy, Ramchurn et al. 2004 and Pinyol & Sabater-Mir 2013. It also uses trust calibration in the Lee & See sense. On top of these it proposes several mechanisms:
   - "graduated authority": autonomy scoped by trust;
   - reputation from "behavioral metrics" that look at *how* a task was done, not only the outcome;
   - permissions as "dynamic states that persist only as long as the agent maintains the requisite trust metrics", with "algorithmic circuit breakers" for automatic revocation.

   The paper is a position paper. It has no evaluation and does not operationalise trust by tests. **WorkTrace can no longer present itself as the first to link classic delegation theory with LLM agents.** It can claim the first *operationalisation* of the socio-cognitive decomposition of trust: interventional tests on external evidence, per decision class, with held-out validation against an outcome-only rule.
2. **"Earned autonomy" is already in use as a term and as a mechanism.** Yuan, Zhang, Wang & Zhao, *Sovereign-OS*, arXiv:2603.14011 (Mar 2026), implements "earned-autonomy permissions governed by a dynamic TrustScore":
   - asymmetric updates on audit success or failure (+5/−15);
   - tiered capability thresholds;
   - revocation when the score drops.

   That is exactly an **outcome-only, revocable, tiered** delegation rule. It is the natural concrete baseline for H3, and a name collision with our working title "Earning Autonomy". A second paper also uses the phrase "earned autonomy", with a different meaning: Wang & Wang, arXiv:2603.26942, where the agent builds up its own function library.
3. **Feng, McDonald & Zhang 2025** propose third-party *autonomy certificates* backed by an *autonomy case*. The level is set by "assisted evaluation": the minimum user involvement needed to exceed an accuracy threshold T. This is a certification-of-autonomy mechanism, but it works per agent, not per decision class, and it is outcome-based. WorkTrace's "narrowed certification" must be positioned against it.
4. **Nothing found grants or revokes autonomy from *interventional tests of how the agent handles evidence*.** This holds for all of the classic works (C&F, Scerri, Ramchurn, Lee & See), and none of them validates a delegation rule on held-out episodes. Classic theory derives the beliefs that support delegation from:
   - past outcomes;
   - reputation;
   - the agent's declarations;
   - its category or role;
   - for automation: displayed performance, process and purpose.

   The core of WorkTrace survives, but contribution 1 must be reworded from "bridge" to "bridge + operationalisation + test".

---

## 1. Reading status and bibliographic verification

| # | Work | Verified via | Status | What I actually read |
|---|---|---|---|---|
| 1 | Castelfranchi, C., Falcone, R. (1998). Towards a theory of delegation for agent-based systems. *Robotics and Autonomous Systems* 24(3–4):141–157. doi:10.1016/S0921-8890(98)00028-1 | Crossref | [verified] | **Full text** (publisher PDF via a third-party SciSpace copy, 17 pp.) |
| 2 | Falcone, R., Castelfranchi, C. (1999). Levels of Delegation and Levels of Help for Agents with Adjustable Autonomy. AAAI Spring Symposium on Agents with Adjustable Autonomy, Tech. Rep. SS-99-06, pp. 25–32 | AAAI PDF header (cdn.aaai.org); no DOI | [verified from AAAI PDF; not in Crossref] | **Full text** |
| 3 | Castelfranchi, C., Falcone, R. (2000). Trust is much more than subjective probability: mental components and sources of trust. *Proc. 33rd HICSS*, 10 pp. doi:10.1109/HICSS.2000.926815 | Crossref | [verified] | **Full text** (author-hosted copy, U. Delaware course page) |
| 4 | Castelfranchi, C., Falcone, R. (1998). Principles of trust for MAS: cognitive anatomy, social importance, and quantification. *Proc. ICMAS'98*, pp. 72–79. doi:10.1109/ICMAS.1998.699034 | Crossref, OpenAlex | [verified] | **Abstract only** |
| 5 | Falcone, R., Castelfranchi, C. (2001). Social Trust: A Cognitive Approach. In Castelfranchi, C., Tan, Y.-H. (eds), *Trust and Deception in Virtual Societies*, Springer (Kluwer), pp. 55–90. doi:10.1007/978-94-017-3614-5_3 | Crossref | [verified] | **Not accessed** (closed). Its content overlaps #3 and #4, which I did read |
| 6 | Castelfranchi, C., Falcone, R. (2010). *Trust Theory: A Socio-Cognitive and Computational Model*. Wiley (Wiley Series in Agent Technology). doi:10.1002/9780470519851, ISBN 9780470028759 | Crossref | [verified] | **Front matter, full table of contents, Introduction, first pages of Ch. 1 only** (publisher excerpt). Chapters 2, 3, 6 and 7 not read |
| 7 | Falcone, R., Castelfranchi, C. (2001). The human in the loop of a delegated agent: the theory of adjustable social autonomy. *IEEE Trans. SMC-A* 31(5):406–418. doi:10.1109/3468.952715 | Crossref, OpenAlex | [verified] | **Abstract only** |
| 8 | Scerri, P., Pynadath, D. V., Tambe, M. (2002). Towards Adjustable Autonomy for the Real World. *JAIR* 17:171–228. doi:10.1613/jair.1037 | Crossref | [verified] | **Full text read: §§1–4, 5.1–5.3, 6, 7, 8.** Skimmed: §5.4 (MDP experiments) and Appendices I–II (algorithm, proof) |
| 9 | Mostafa, S. A., Ahmad, M. S., Mustapha, A. (2019). Adjustable autonomy: a systematic literature review. *Artificial Intelligence Review* 51(2):149–186. doi:10.1007/s10462-017-9560-8 (online 2017) | Crossref, Semantic Scholar, UNITEN repository | [verified] | **Abstract only** (paraphrase via the repository; publisher closed) |
| 10 | Ramchurn, S. D., Huynh, D., Jennings, N. R. (2004). Trust in multi-agent systems. *Knowledge Engineering Review* 19(1):1–25. doi:10.1017/S0269888904000116 | Crossref | [verified] | **Partial**: §1, §2 intro, §2.1 intro, §2.1.2, §2.3, §4 (incl. 4.1, 4.2) in full. §2.2 and §3 headings only |
| 11 | Sabater, J., Sierra, C. (2005). Review on Computational Trust and Reputation Models. *Artificial Intelligence Review* 24(1):33–60. doi:10.1007/s10462-004-0041-5 | Crossref | [verified] | **Not accessed**: the author-hosted IIIA link returned 404/503 and the publisher is closed |
| 12 | Pinyol, I., Sabater-Mir, J. (2013). Computational trust and reputation models for open multi-agent systems: a review. *Artificial Intelligence Review* 40(1):1–25. doi:10.1007/s10462-011-9277-z (online 2011) | Crossref, DBLP id journals/air/PinyolS13 | [verified] | **Not accessed** (IIIA server returned 503; publisher closed). Only a search-engine paraphrase of the abstract was seen; no quotes taken |
| 13 | Parasuraman, R., Sheridan, T. B., Wickens, C. D. (2000). A model for types and levels of human interaction with automation. *IEEE Trans. SMC-A* 30(3):286–297. doi:10.1109/3468.844354 | Crossref, OpenAlex | [verified] | **Abstract plus the start of §I only.** The 10-level table was **not** read, so it is not quoted |
| 14 | Lee, J. D., See, K. A. (2004). Trust in Automation: Designing for Appropriate Reliance. *Human Factors* 46(1):50–80. doi:10.1518/hfes.46.1.50_30392 | Crossref | [verified] | **Substantial**: Introduction, Definition of trust, Calibration/Resolution/Specificity, Bases of trust, Implications, Conclusion. The middle sections (affect, the dynamic model) only skimmed |
| 15 | W3C (2013). PROV-DM: The PROV Data Model, W3C Recommendation, 30 April 2013 (eds. L. Moreau, P. Missier), §5.3.4 *Delegation*; and PROV-O: The PROV Ontology, W3C Recommendation, 30 April 2013 (eds. T. Lebo, S. Sahoo, D. McGuinness), terms `prov:actedOnBehalfOf`, `prov:Delegation`, `prov:qualifiedDelegation` | w3.org/TR | [verified] | **Full relevant sections** |
| 16 | Feng, K. J. K., McDonald, D. W., Zhang, A. X. (2025). Levels of Autonomy for AI Agents. arXiv:2506.12469 (v2, 28 Jul 2025); essay in the Knight First Amendment Institute "AI and Democratic Freedoms" series | arXiv API | [verified] | **Full text** (Table 1 skimmed) |
| 17 | Calvanese, D., Casciani, A., De Giacomo, G., Dumas, M., Fournier, F., Kampik, T., La Malfa, E., Limonad, L., Marrella, A., Metzger, A., Montali, M., Amyot, D., Fettke, P., Polyvyanyy, A., Rinderle-Ma, S., Sardiña, S., Tax, N., Weber, B. (2026). Agentic Business Process Management: A Research Manifesto. arXiv:2603.18916 (v3, 12 Apr 2026) | arXiv API | [verified] | **Most of it**: §1, §2, §3.1–3.3, §4.1–4.3, the M1 and C4 parts of §4.4–4.5, §5. Not read: §3.4, rest of §4.4–4.5 |
| 18 | Tomašev, N., Franklin, M., Osindero, S. (2026). Intelligent AI Delegation. arXiv:2602.11865 (v1, 12 Feb 2026) | arXiv API | [verified] | **Full text** |
| 19 | Yuan, A., Zhang, H., Wang, Z., Zhao, Y. (2026). Sovereign-OS: A Charter-Governed Operating System for Autonomous AI Agents with Verifiable Fiscal Discipline. arXiv:2603.14011 | arXiv API | [verified] | **Partial**: abstract, contributions list, §3.1 TrustScore |
| 20 | Ferreira, J. D. (2026). When Intelligence Becomes Agency: A Theory of Governed, Proactive Agency for Symbiotic AI Systems. arXiv:2609.07741 | arXiv API | [verified] | **Partial**: abstract, first page of §1, related-work passages on delegation |
| — | Wang, Y., Wang, C. (2026). The Observability Gap: Why Output-Level Human Feedback Fails for LLM Coding Agents. arXiv:2603.26942 | arXiv API | [verified] | Abstract only (relevant only for the "earned autonomy" name collision) |

**Correction to the brief.** The Calvanese et al. manifesto does **not** use the term "bounded autonomy". The term does not occur in the text; the only "bounded" hits are about memory and context. Its term is **"framed autonomy"** (Def. 2.4, §3.1, §4.1). Cite it as "framed autonomy".

**Correction found in the literature.** Tomašev et al. cite Falcone & Castelfranchi's IEEE SMC-A paper as 2002. Crossref gives 31(5):406–418, **2001**. Do not copy their reference.

---

## 2. Per-work notes

### 2.1 Castelfranchi & Falcone (1998), "Towards a theory of delegation for agent-based systems" — FULL TEXT

**Problem & contribution.** The paper builds a plan-based theory of delegation and adoption that grounds the notions of "agent", "on behalf of" and autonomy. The abstract gives three motivations: "First, one of the most relevant notions of 'agent' is based on the notion of 'task' and of 'on behalf of.' … Second, the notion of autonomy should be based on different kinds and levels of delegation. Third, … cooperation and collaboration requires … goal delegation and adoption."

**Method: concepts to reuse.**
- *Object of delegation.* "We consider the action/goal pair τ = (α, g) as the real object of delegation, and we will call it 'task'" (§2). Operator: `Delegates(A, B, τ, d)` with a deadline d (§2.2).
- *Delegation is mental, possibly unilateral.* "a delegation (or an adoption) is a set of agent's (agents') beliefs, goals, intentions, commitments, etc.: externally there may be no interaction between the agents" (§2).
- *Rationality of delegation is reduced to trust.* "It is rational for the client to delegate a task to the contractor iff the client's trust in the contractor's action … is greater than its trust in the alternatives. So the rationality of delegation is reduced to the level of trust the agent requires for delegating. … delegation is in fact a risk, a bet on the contractor" (§2). Delegation costs include communication and influence, the contractor's conditions, and "the cost of possible delegation conflicts" (§2).
- *Types of delegation by interaction* (§2.3, Table 1):
  - **Weak delegation**: "based on exploitation, on the passive achievement by A of the task. In it there is no agreement, no request or even influence: A is just exploiting in its plan a fully autonomous action of B."
  - **Mild delegation**: "based on induction, on the active indirect achievement by A of the task. In it there is no agreement, no request, but A is itself eliciting, inducing in B the desired behaviour in order to exploit it."
  - **Strict delegation**: "based on explicit agreement, on the active achievement by A of the task through an agreement with B. It is based on B's adopting A's task in response to A's request/order." Strict delegation ⇔ strict adoption ⇔ "contract"; after agreement, "(h) B is socially committed to A to achieve τ for A" (§2.6).
  - The paper says "strict", not "strong". Later works (the 2010 book ToC: "The Case of Strong Delegation") use "strong".
- *Trust as the belief component; delegation as the decision component.* For weak delegation, conditions (a)–(d) are "what the agent A views as a 'Potential for relying on' the agent B, its trust; and (e)–(f) what A views as the 'Decision to rely on' B" (§2.3).
- *Open vs close delegation* (§2.7): "The object of delegation (τ) can be minimally specified (open delegation), completely specified (close delegation) or specified at any intermediate level." On open delegation, the delegate "can (or must) realize the delegated (adopted) task by exerting its autonomy". "When A is open delegating … it is necessarily also delegating to B some meta-action … We call B's discretion concerning τ the fact that some decision about τ is delegated to B."
- *When close delegation is rational* (§2.7): "It is rational to closely delegate when … we do not trust the ability/willingness of the contractor to find or developing a plan for the goal … So, rationality in the level of delegation strictly depends on the client's model of the contractor."
- *Delegation of control* (§2.9). Four options: "(i) A delegates the control to B … (ii) A delegates the control to a third agent … (iii) A gives up the control … (iv) A maintains the control for itself."
- *Levels of adoption* (§2.10): literal help, overhelp, critical help ("achieves the relevant results of the requested plan/action, but modifies the plan/action"), critical overhelp, hyper-critical help.
- *Autonomy defined by delegation* (§2.11): "The autonomy of the contractor vis-a-vis the client increases along various dimensions: the more open the delegation …, the more control actions given up or delegated to B by A, … the more delegated decisions (discretion)." Kinds: executive, planning and goal autonomy.
- *Sources of the client's model of the contractor* (§3): "(a) previous experience of the other's behaviour …; (b) an explicit declaration of the agent …; (c) an implicit communication of the agent …; (d) attributions to the category or role the agent belongs to". There are also "class competence" and "personal competence".
- *Trust = model of competence and willingness* (§3.2): "The client's model of the contractor has mainly to do with the contractor's competence and willingness … the model of the willingness is related to goals, commitments, and reliability." Beliefs (b), (c), (c-bis), (h) "represent the client's trust in the contractor".
- *Non-transitivity* (§2.8): from Delegate(A,B,τ) and Delegate(B,C,τ) "it does not follow that Delegate(A,C,τ)".

**Evaluation.** None (theoretical, formal).

**What WorkTrace must NOT claim.**
- That it introduces delegation types, levels, open-vs-closed delegation, delegated discretion, or delegation of control.
- That trust is the belief component behind a decision to delegate.
- That autonomy is defined by delegation openness, control and discretion.
- That delegation is a risky bet whose rationality depends on trust *relative to alternatives*.

**What it leaves open (WorkTrace addresses).**
- *How* the client obtains warranted beliefs about the contractor's competence. §3 lists only experience, declaration, implicit communication and category ascription; no controlled testing.
- No empirical evaluation of whether delegation decisions are correct.
- No notion of the information available at decision time or of evidence handling.

**Draft differentiation.** "Castelfranchi and Falcone define delegation as a decision to rely, grounded in beliefs about a delegate's competence and willingness that come from experience, declarations or category membership; WorkTrace adds a fifth, experimental source of those beliefs (controlled interventions on the external evidence of decision episodes) and turns it into a revocable open-delegation rule per decision class whose predictive validity is tested on held-out episodes."

**Citation cautions.** The full text came from a third-party (SciSpace) copy of the publisher PDF; cite the DOI. Use "strict" for the 1998 term and note that later works say "strong".

---

### 2.2 Falcone & Castelfranchi (1999), AAAI SS-99-06, "Levels of Delegation and Levels of Help for Agents with Adjustable Autonomy" — FULL TEXT

**Problem & contribution.** Links the delegation theory to *adjustable autonomy* (the AAAI 1999 symposium framing): the client adjusts the level of delegation, and the contractor adjusts its own autonomy by "restricting or by expanding the received delegation" (Abstract).

**Concepts to reuse (quotes).**
- "it could be useful an explicit theory of delegation (and of trust) able to specify different levels, and able to link to these the notion and the levels of autonomy" (Introduction).
- Dynamic programme, left as future work: "how the levels delegation or help can vary over time and in a reactive way (depending on the intermediate results of co-operation); how the levels of delegation, of trust, and of autonomy can be different for different aspects and dimensions of the same task" (Introduction).
- **Key for WorkTrace** (Concluding Remarks): "trust is not only the global final result of the evaluation, that determines if one delegates or not that task to that agent. It should be articulated along several dimensions. Our claim is that it is precisely an articulated trust which determines the level and kind of delegation … He has different degree of trust relative to different aspects of the complex task, and he delegates more or less on one aspect or on the other depending on this differential reliance. To model this process – that we believe to be the basis of Adjustable Autonomy – we claim that it is necessary to merge the theory of levels of delegation with the theory of the degrees of trust."
- Delegation of control and of initiative ("motu proprio", "spontaneous interaction or pro-active help"). Defined as in #1.

**Evaluation.** None.

**Must NOT claim:** that differential, per-aspect trust determining per-aspect delegation is a new idea. This is the classic statement of our "per decision class" thesis.

**Leaves open:** how per-aspect trust is measured; the dynamics are announced but not given.

**Differentiation.** "Falcone and Castelfranchi called for merging levels of delegation with degrees of trust that differ across aspects of a task; WorkTrace supplies an operational, test-based estimate of one such aspect (evidence handling) per decision class and evaluates the resulting delegation rule."

**Cautions.** Symposium tech report, not peer-reviewed in the journal sense; cite as AAAI Technical Report SS-99-06.

---

### 2.3 Castelfranchi & Falcone (2000), HICSS, "Trust is much more than subjective probability" — FULL TEXT

This is the most quotable open-access statement of the socio-cognitive trust model; it substitutes for #5, which I could not access.

**Concepts to reuse (quotes).**
- Abstract: trust is "a complex structure of beliefs and goals … Such a structure of beliefs determines a 'degree of trust' and an estimation of risk, and then a decision to rely or not on the other, which is also based on a personal threshold of risk acceptance/avoidance."
- Trust and delegation (§3.1): "Trust is the mental counter-part of delegation."
- Belief components (§3.1):
  1. Competence;
  2. Disposition ("y will actually do what x needs. With cognitive agents this will be a belief with respect to their willingness");
  3. Dependence;
  4. Fulfilment;
  5. Willingness;
  6. Persistence;
  7. Self-confidence ("It is difficult to trust someone who does not trust himself!").
- Internal vs external attribution (§3.2). The global probability "should be decomposed into the probability of y performing the action well … (internal attribution) and the probability of having the appropriate conditions (opportunities and resources: external attribution)". This matters because "(a) the agent's trusting/delegating decision might be different with the same global probability or risk, depending on its composition; (b) trust composition (internal versus external) produces completely different intervention strategies".
- Degree of trust (§3.3): `DoT_XYτ = DoC_X[Opp_Y(α,g)] * DoC_X[Ability_Y(α)] * DoC_X[WillDo_Y(α,g)]`, with `DoC_X[WillDo] = DoC_X[Intend] * DoC_X[Persist]`. "the degree of trust is a function of the subjective certainty of the pertinent beliefs."
- The decision is discrete (§2.1): "Trust … is a continuous [quantity] … Only the decision to trust (or better to delegate a task …) is discrete: either trust is sufficient or it is not".
- Risk threshold independent of expected value (§3.4): "it is possible that the value of the damage per se (in case of failure) is too high to choose a given decision branch, and this is independently from the probability of the failure … (for example, in our model we introduce an 'acceptable damage' threshold)."
- Rational vs unwarranted trust (§3.4–3.5): "those beliefs can also be not really warranted, not based on evidences … We call this part of the trust in y: 'faith'." "To trust is indeed irrational either when the accepted risk is too high … or when trust is not based on good evidences".
- Over-confidence and over-diffidence (§3.5.1). One consequence of over-confidence is "Too open delegation". Consequences of over-diffidence include "We search and wait for too many evidences and proofs; We make too many controls". On the right degree: "The right level of positive trust in the trustee (esteem) is when the marginal utility of the additional evidence on him … seems inferior to the cost for acquiring it".
- Against reduction to a number (§4): "The reduction of these articulated aspects of trust to a probability measure, reduces the explanatory and predictive power of the theory."

**Evaluation.** None.

**Must NOT claim:**
- trust decomposed into competence/willingness/opportunity;
- a trust threshold for delegation;
- a damage threshold independent of probability (our "refuse");
- that over-trust and over-control are both costly;
- the idea of warranted, evidence-based trust.

**Leaves open:**
- How to *obtain* the DoC values for an artificial delegate.
- How to test them.
- How to validate the resulting decisions.

**Differentiation.** "Castelfranchi and Falcone's degree of trust multiplies the credibility of beliefs about a delegate's opportunity, ability and willingness; WorkTrace estimates one ability-like component (responsiveness to decision-time evidence) by intervention, keeps it separate from the external conditions it controls in the generator, and leaves willingness explicitly unmeasured."

**Cautions.** HICSS proceedings have no volume numbers; cite the DOI.

---

### 2.4 Castelfranchi & Falcone (1998), ICMAS, "Principles of trust for MAS" — ABSTRACT ONLY

Abstract (OpenAlex): "we present a principled quantification of trust, based on its cognitive ingredients. And use this 'degree of trust' as the basis for a rational decision to delegate or not to another agent." Cite this as the original source of "degree of trust → decision to delegate". Quote the HICSS paper (§2.3) for details.

### 2.5 Falcone & Castelfranchi (2001), "Social trust: a cognitive approach" — NOT ACCESSED

Bibliographic data verified only. Cite only as a general reference for the socio-cognitive model, not for specific claims.

### 2.6 Castelfranchi & Falcone (2010), *Trust Theory* (Wiley) — FRONT MATTER, TOC, INTRODUCTION, START OF CH. 1

**Useful from what was read.** The Introduction says the model presents trust as "not only a disposition or a set of beliefs (evaluation or prediction), but also a decision to rely on, and the following 'act' of, and the consequential social relation", and "not only about 'reliability' but also about 'competence'" (Introduction, "The Structure of the Book").

The table of contents points to sections that bear directly on WorkTrace; **none of them was read**, so cite them as pointers only:
- §2.9.2 "Trust in Open Delegation Versus Trust in Closed Delegation"
- §3 "To Trust or Not to Trust: Degrees of Trust and Decision to Trust"
- §6.3.1–6.3.2 "The Case of Weak Delegation / Strong Delegation"
- **§6.6 "Trust Through Transfer and Generalization — Classes of Tasks and Classes of Agents"**: a direct precedent for *per decision class* trust and its generalisation
- §6.7 "The Relativity of Trust: Reasons for Trust Crisis"
- §7.1.10 "Control Kills Trust"
- §7.2 "Adjusting Autonomy and Delegation on the Basis of Trust in Y" (incl. §7.2.9 "When to Adjust the Autonomy of the Agents")
- §11 a fuzzy implementation

**Action.** Before submission, someone must read §6.6 and §7.2. They may already formalise trust generalisation across task classes, which our per-class rule relies on. *Risk: medium.*

### 2.7 Falcone & Castelfranchi (2001), IEEE SMC-A, "The human in the loop of a delegated agent: the theory of adjustable social autonomy" — ABSTRACT ONLY

Abstract (OpenAlex): autonomy depends on "1) the degree of 'openness' of delegation; 2) the allowed initiative in (re)starting negotiation; 3) the degree and kind of control; and 4) the strength of delegation". Adjustment is "'bilateral'", "'bidirectional' and multidimensional". The delegator adjusts on a "'crisis of trust'". The delegee's adjustment "depends on some disagreement about the trust received from the delegator, and, in particular, either a higher or lower confidence in itself or in external circumstances."

**Relevance.** This is the classic source for *revocation* ("crisis of trust") and for *delegee-side* self-restriction. WorkTrace's rule is principal-side only (§4).

---

### 2.8 Scerri, Pynadath & Tambe (2002), "Towards adjustable autonomy for the real world" (JAIR 17) — FULL TEXT (§5.4 and appendices skimmed)

**Problem & contribution.** Adjustable autonomy (AA) is framed as deciding "whether and when such transfers-of-control should occur", which is "arguably the fundamental research problem in adjustable autonomy" (Abstract). Previous approaches "use rigid one-shot transfers of control that can result in unacceptable coordination failures" and "ignore costs (e.g., in terms of time delays …)" (Abstract).

**Method: concepts to reuse.**
- Problem instance ⟨A, α, ρ, ζ, d, E⟩: agent, joint activity, role, coordination constraints, decision, candidate decision-makers (§2).
- "Definition 3.1 A transfer-of-control strategy is a pre-defined, conditional sequence of two types of actions: (i) actions to transfer decision-making control … and (ii) actions to change an agent's pre-specified coordination constraints with team members, aimed at minimizing miscoordination costs." Strategies are written e.g. H(5)A, ADH, H DA; the strategy space is a regular expression.
- **Cost model** (§3.1). The EU of a strategy combines four elements:
  - the expected decision quality of each entity, EQ^d_e(t) ("reflects both the probability that the entity will make an 'appropriate' decision and the costs incurred if the decision is wrong");
  - the response-time distribution P_>(t);
  - a non-decreasing wait cost W(t) up to a deadline;
  - coordination-change actions D with D_value and D_cost.

  EU_s = ∫ P_>(t) EU^d_e(t) dt, where EU^d_e(t) = EQ^d_e(t) − W(t).
- **Lemma 1** (§3.2): the agent should eventually take back control iff for some t, ∫_t^Γ P_>(t′)W(t′)dt′ − W(t) > EQ^d_U(t) − EQ^d_A(t). In words: "if … the expected cost of indefinitely leaving control in the hands of the user exceeds the difference in quality between the agent's and user's decisions, then strategies which ultimately give the agent control dominate".
- "no particular transfer-of-control strategy dominates all others across all domains" (§3.2).
- MDP operationalisation (§4). Reward Table 3: wait cost for transfer-without-response and wait; D_cost; EQ for a response. Plus q(e), "the cost of transferring control to a particular entity, e.g., the cost of a WAP phone message" (Eq. 11).
- **User-specified constraints** (§4.4): forbidden-action and forbidden-state constraints (and required ones). "a forbidden-action constraint that prevents the agent from taking autonomous action in a particular state is equivalent to the user specifying that the agent must transfer control to the user in that state."
- Footnote 7: "We consider choosing not to act an autonomous decision".
- Future work (§8): "transferring control of many decisions to a user, reduces the probability of getting a prompt response to any of them"; "if actions were reversible, the agent could make the decision but allow the user to reverse it."

**Evaluation.**
- E-Elves deployment, June–Dec 2000, ~10 users. Nearly 700 meetings monitored; "usually 50% or more of delayed meetings were autonomously delayed" (§5.1, Fig. 8).
- Auctions: 5 of 7 presenter auctions decided autonomously (Table 4).
- Model-vs-MDP agreement on strategy choice (Table 5).
- The failed C4.5 baseline: "Tambe's … Friday incorrectly cancelled a meeting with the division director because Friday over-generalized from training examples" (§2.2).
- Qualitative behavioural side-effects: "some users preferring to be a minute or two early for a meeting lest their agent decide they were late" (§5.2).

**What WorkTrace must NOT claim.**
- That escalation has a cost that must be traded against decision quality.
- That neither "always escalate" nor "never escalate" dominates.
- That users need hard constraints over the learned AA policy.
- That an agent learning *when to transfer control* from user feedback is new: the C4.5 baseline learned a second decision tree for exactly that.

**What it leaves open (WorkTrace addresses).**
- **EQ^d_A(t), the agent's expected decision quality, is assumed or hand-estimated.** In E-Elves it is crudely set ("EQ_U ≈ EQ_A" or "EQ_U ≈ 10·EQ_A", §3.3); for the auction it is "a function of the number of bids" (§4.3).
- The paper never tests whether the agent's decision quality is warranted by the information it used.

WorkTrace can be presented as *a method to estimate EQ^d_A per decision class from tested evidence handling*, feeding a Scerri-style choice between A (proceed) and H (escalate).

**Draft differentiation.** "Scerri et al. choose transfer-of-control strategies that trade the agent's expected decision quality against waiting and interruption costs, but take that quality as given; WorkTrace estimates it per decision class from interventional tests on decision episodes and evaluates the resulting proceed/escalate/refuse rule on held-out episodes with an explicit escalation cost."

**Citation cautions.** The domain is 2000-era, with timing-centred coordination costs. Our episodes are one-shot: say explicitly that we model only single-shot strategies (A, H, and "no action") and ignore D-actions and response latency. That is precisely the simplification Scerri et al. warn against for team settings.

---

### 2.9 Mostafa, Ahmad & Mustapha (2019), "Adjustable autonomy: a systematic literature review" — ABSTRACT ONLY

According to the repository abstract (paraphrased), it is a systematic review of adjustable autonomy in multi-agent systems that screened 171 papers and examined 78 in detail. It covers approaches and their utility, requirements for formulating AA, assessment techniques, and research gaps.

Use: a single citation for "adjustable autonomy has a large MAS literature". Do not attribute specific claims. *Caution*: online-first 2017, issue 2019; cite as 2019, AIR 51(2):149–186.

---

### 2.10 Ramchurn, Huynh & Jennings (2004), "Trust in multi-agent systems" (KER) — PARTIAL

**Concepts to reuse (quotes).**
- Adopted definition (§1): "Trust is a belief an agent has that the other party will do what it says it will (being honest and reliable) or reciprocate (being reciprocative for the common good of both), given an opportunity to defect to get higher payoffs (adapted from (Dasgupta, 1998))."
- Two levels (§1): "individual-level trust, whereby an agent has some beliefs about the honesty or reciprocative nature of its interaction partners; system-level trust, whereby the actors in the system are forced to be trustworthy by the rules of encounter (i.e. protocols and mechanisms)". This is a useful framing: WorkTrace = individual-level evidence used for a *system-level* rule (the delegation policy).
- Individual-level models are "learning (and evolution) based, reputation based, or socio-cognitive based" (§2). All the learning and reputation models "are all based on an assessment of the outcomes of interactions" (§2.3).
- On Castelfranchi & Falcone (§2.3): it lists the competence, willingness, persistence and motivation beliefs, then criticises: "it lacks the rational grounding … In effect, the socio-cognitive approach could exploit the assessment performed by these models to form the core beliefs illustrated above."
  - **This is the gap WorkTrace fills**: a measurable, non-outcome-only basis for the competence belief.
- Open issues (§4.2):
  - "Strategic lying: … Strategic lies aim to trick agents into believing the liars are trustworthy".
  - "Context: most trust models do not take into account the fact that interactions take place within a particular organisational and environmental context … If an agent has performed poorly due to changes in their environment, they should not be taken to be dishonest";
  - "if rules prevent lying, there is no need to increase trust in interaction partners if they interact well since there is no guarantee they would still do so if the rules were not present (Molm et al., 2000)". This bears on testing under guardrails versus deployment without them.
- Performance ratings beyond a binary outcome (REGRET's multi-facet ratings, §2.1.2). Outcome-based trust can be exploited "so long as the opponent is not 'completely defecting'" (footnote 6).

**Evaluation.** None (survey).

**Must NOT claim:**
- that outcome-based trust is the default in computational trust;
- that socio-cognitive trust lacks operational grounding (they said it in 2004);
- that context-dependence of trust is new.

**Leaves open:** grounding the cognitive beliefs; context handling.

**Differentiation.** "Computational trust models in MAS estimate trustworthiness from interaction outcomes and reputation (Ramchurn et al., 2004); WorkTrace instead grounds the competence belief of the socio-cognitive model in counterfactual tests of how the agent's actions depend on the evidence it had, which Ramchurn et al. identified as the missing rational grounding of that model."

**Cautions.** A 2004 survey of a pre-LLM field. Fine for framing, not for state-of-the-art claims.

### 2.11 Sabater & Sierra (2005) and 2.12 Pinyol & Sabater-Mir (2013) — NOT ACCESSED

Bibliographic data verified (Crossref; DBLP id for Pinyol). Content was not read: the IIIA server returned 503 and the publisher is closed.
- Cite only as "further surveys of computational trust and reputation models" together with Ramchurn et al.
- Do **not** attribute specific definitions to them until read. A search snippet suggests Pinyol & Sabater-Mir offer a definition of trust in the Castelfranchi "decision to rely" line; that is unverified.

**TODO:** retry https://www.iiia.csic.es/~jsabater/Publications/2011-AIR.pdf.

---

### 2.13 Parasuraman, Sheridan & Wickens (2000), "A model for types and levels of human interaction with automation" — ABSTRACT + START OF §I ONLY

**Concepts to reuse (abstract, verbatim).**
- "automation can be applied to four broad classes of functions: 1) information acquisition; 2) information analysis; 3) decision and action selection; and 4) action implementation. Within each of these types, automation can be applied across a continuum of levels from low to high, i.e., from fully manual to fully automatic. A particular system can involve automation of all four types at different levels."
- "The human performance consequences of particular types and levels of automation constitute primary evaluative criteria … Secondary evaluative criteria include automation reliability and the costs of decision/action consequences".

**Not read:** the 10-level scale (after Sheridan & Verplanck) and any recommended upper bounds. **Do not quote the table or attribute level numbers until the full text is checked.**

**Use for WorkTrace.**
- Our decision classes live in stage 3 (decision and action selection).
- Our interventions perturb the inputs of stages 1–2 (what evidence is acquired or available).
- "Different levels for different functions" is the human-factors precedent for per-class autonomy.
- PSW's secondary criteria ("automation reliability and the costs of decision/action consequences") are exactly the two quantities in our rule: the unjustified-action bound α, and the escalation and error costs.

**Must NOT claim** that function- or class-specific levels of automation are new.

**Differentiation.** "Parasuraman et al. choose a level of automation per function from human-performance, reliability and consequence criteria; WorkTrace sets the delegation level per decision class from measured evidence handling and checks the choice on held-out episodes."

---

### 2.14 Lee & See (2004), "Trust in automation: designing for appropriate reliance" — SUBSTANTIAL

**Concepts to reuse (quotes).**
- Definition (Introduction, p. 51): "Trust can be defined as the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability."
- Trust vs reliance (pp. 53–54): "In the context of trust and reliance, trust is an attitude and reliance is a behavior … Trust stands between beliefs about the characteristics of the automation and the intention to rely on the automation."
- Conclusion: "Trust influences reliance on automation; however, it does not determine reliance."
- Misuse and disuse (Introduction, after Parasuraman & Riley 1997): "Misuse refers to the failures that occur when people inadvertently violate critical assumptions and rely on automation inappropriately, whereas disuse signifies failures that occur when people reject the capabilities of automation."
- **Calibration, resolution, specificity** (pp. 55–56):
  - "Calibration refers to the correspondence between a person's trust in the automation and the automation's capabilities … Overtrust is poor calibration in which trust exceeds system capabilities; with distrust, trust falls short".
  - "Resolution refers to how precisely a judgment of trust differentiates levels of automation capability … With low resolution, large changes in automation capability are reflected in small changes in trust."
  - "Specificity refers to the degree to which trust is associated with a particular component or aspect of the trustee. Functional specificity describes the differentiation of functions, subfunctions, and modes of automation … High temporal specificity means that a person's trust reflects moment-to-moment fluctuations in automation capability".
  - "Good calibration, high resolution, and high specificity of trust can mitigate misuse and disuse of automation".
- **Bases of trust** (pp. 58–59, after Lee & Moray 1992):
  - "Performance refers to the current and historical operation of the automation and includes characteristics such as reliability, predictability, and ability. Performance information describes what the automation does."
  - "Process is the degree to which the automation's algorithms are appropriate for the situation and able to achieve the operator's goals. Process information describes how the automation operates."
  - "Purpose refers to the degree to which the automation is being used within the realm of the designer's intent."
- Design guidance ("Implications"):
  - "Design for appropriate trust, not greater trust."
  - "Show the past performance of the automation."
  - "Show the process and algorithms of the automation by revealing intermediate results in a way that is comprehensible to the operators."
  - "Show how past performance depends on situations."
  - "Evaluate the appropriateness of trust according to calibration, resolution, and specificity. Specificity and resolution are particularly critical when the performance of the automation is highly context dependent."
  - The trade-off between "trustworthy automation and trustable automation".
  - "meta trust" in other people's trust.

**Evaluation.** None (integrative review).

**Must NOT claim:**
- "appropriate, calibrated trust" or "per-function trust";
- misuse/disuse as the two failure modes (they correspond to our two error types: unjustified autonomous action vs unnecessary escalation);
- that process-based trust beats performance-only trust *as a concept*.

**What it leaves open (WorkTrace addresses).**
- The process basis is conveyed by displays and training. Nobody *tests* that the process is appropriate, so calibration is not validated against held-out capability.
- An artificial principal (a delegation rule rather than a human) can be evaluated directly for calibration, resolution and specificity.

**Draft differentiation.** "Lee and See distinguish trust based on performance (what automation does) from trust based on process (how it operates) and ask for calibrated, high-resolution, function-specific trust; WorkTrace makes the process basis testable for LLM agents and evaluates whether a process-based delegation rule is better calibrated and has higher resolution than a performance-only (outcome-only) rule."

**Cautions.** A human-factors construct (an attitude of a human). Applying "calibration" to an algorithmic delegation rule is an analogy; say so.

---

### 2.15 W3C PROV — delegation (PROV-DM §5.3.4; PROV-O) — FULL RELEVANT SECTIONS

**Definition** (identical in PROV-DM §5.3.4 and PROV-O): "Delegation is the assignment of authority and responsibility to an agent (by itself or by another agent) to carry out a specific activity as a delegate or representative, while the agent it acts on behalf of retains some responsibility for the outcome of the delegated work. For example, a student acted on behalf of his or her supervisor … all those agents are responsible in some way for the activity that took place but we do not say explicitly who bears responsibility and to what degree."

**Structure.**
- PROV-N: `actedOnBehalfOf(id; ag2, ag1, a, attrs)`, with delegate ag2, responsible ag1, an OPTIONAL activity a, and OPTIONAL attributes.
- "If an activity is not specified, then the subordinate agent is considered to act on behalf of the responsible agent, in all the activities the subordinate agent is associated with."
- PROV-O: `prov:actedOnBehalfOf` (domain and range `prov:Agent`; "An object property to express the accountability of an agent towards another agent. The subordinate agent acted on behalf of the responsible agent in an actual activity"). It is qualified by `prov:Delegation` (a subclass of `prov:AgentInfluence`) via `prov:qualifiedDelegation`, with `prov:agent` and `prov:hadActivity`.
- Related: `wasAssociatedWith(id; a, ag, pl, attrs)` with an optional `prov:Plan`.
- Software agents are first-class (`prov:SoftwareAgent`).

**Use for WorkTrace.**
- Encode each executed decision episode as `wasAssociatedWith(decision_activity, agent)` plus `actedOnBehalfOf(agent, principal, decision_activity, [wt:decisionClass=…, wt:delegationRule=…, wt:ruleVersion=…, wt:verdict="proceed"])`.
- An escalation becomes an association with the human, with the agent's recommendation as an entity.

**What PROV does NOT give.** It is a *record of delegation that occurred* ("in an actual activity"), not a standing, conditional or revocable *permission*. It deliberately does not say "who bears responsibility and to what degree". WorkTrace needs an extension (a policy entity derived from test results, with validity and revocation) and should not overclaim that PROV "models" the delegation rule.

**Cautions.** PROV-DM/PROV-O are W3C Recommendations (2013); cite the TR URLs with dates. PROV-O editors: Lebo, Sahoo, McGuinness. PROV-DM editors: Moreau, Missier.

---

### 2.16 Feng, McDonald & Zhang (2025), "Levels of Autonomy for AI Agents" — FULL TEXT

**Problem & contribution.** Treat autonomy "as a deliberate design decision, separate from its capability and operational environment" (Abstract). Five levels by user role: L1 operator, L2 collaborator, L3 consultant, L4 approver ("Agent engages user only in risky or pre-specified scenarios"), L5 observer (Fig. 1). Autonomy is "the extent to which an AI agent is designed to operate without user involvement" (§2.2).

**Mechanisms.**
- **Autonomy certificates** (§4): "a digital document that prescribes the maximum level of autonomy at which an agent can operate given 1) some set of technical specifications … and 2) its operational environment", issued by a third party after reviewing an **autonomy case**, "analogous to safety cases". Renewal is needed on changes to specifications or environment.
- **Assisted evaluation** (§5): "designed to surface the minimum level of user involvement needed for the agent to exceed a certain accuracy or pass rate threshold, and then assign an autonomy level". The procedure iterates from no involvement (L5) towards more involvement until threshold T is reached.
- L4 open questions (§3.4): "How can users be engaged in agent activities to avoid meaningless rubber stamping?"; "How can misaligned agents leverage user disengagement to gain more autonomy?"; "How can the agent reliably know when to seek approval?"

**Evaluation.** None (essay; evaluation proposed only).

**Must NOT claim:**
- levels of autonomy for LLM agents;
- autonomy as separable from capability;
- third-party certification of a maximum autonomy level with renewal on change.

**What it leaves open.**
- Its certificates are per agent and per environment, not per decision class.
- Its evaluation is accuracy/pass-rate based (outcome-only) and measures *how much help the agent needs*, not *whether its unassisted decisions are warranted by evidence*.
- No held-out validation; no cost of escalation.

**Draft differentiation.** "Feng et al. certify a maximum autonomy level per agent from the least user involvement needed to reach a task-accuracy threshold; WorkTrace grants or withholds autonomy per decision class from tested evidence handling and shows on held-out episodes that this does better than an accuracy-based (outcome-only) rule at the same autonomy coverage."

**Cautions.** A non-peer-reviewed essay (Knight Institute series; arXiv cs.HC). Cite for the framework and the certificate idea only.

---

### 2.17 Calvanese et al. (2026), "Agentic Business Process Management: A Research Manifesto" — MOST OF THE TEXT

**Concepts.**
- **Framed autonomy, not "bounded autonomy".** "Definition 2.4. Framing is a primary mechanism for ensuring process-awareness and goal alignment in an APM system, imposing restrictions on the autonomy of agents through their knowledge and goals."
- "Frames establish boundaries within which one or several agents in an APM system may operate with maximal flexibility, making autonomous decisions" (§3.1).
- Normative vs operational frames: "the operational frame requires finding a strategy to satisfy the objective, whereas the normative frame requires choosing a strategy that remains within what is allowed" (§3.1).
- Autonomy vs automation: "automation follows fixed rules, whereas autonomy in APM allows agents to make context-sensitive decisions while still respecting process awareness and constraints" (§2.1).
- Research challenges:
  - **A4**: "How to balance autonomy, delegation, and control? … how to achieve the best trade-off between delegation (improving performance) and control (mitigating undesired outcomes and retaining human responsibility)" (§4.3).
  - **M1**: "A key question is when to refrain from autonomy and return control to a human agent, e.g., in scenarios where the autonomous agent has insufficient confidence … Research in AI planning, runtime monitoring may help establish thresholds or confidence bounds beyond which a process must escalate to human decision-makers. Techniques from the ML literature on prediction with reject option (sometimes called 'learning to defer') can be explored" (§4.4).
  - **C4**: calls for "defining the boundaries of delegation and the precise conditions under which human intervention is legally and operationally mandatory" (§4.5).
- Frames can be mined: "rule mining approaches can be applied to infer normative constraints from the traces of well-behaved agents" (F2, §4.1).

**Evaluation.** None (manifesto).

**Must NOT claim:**
- that BPM/MAS lacks the idea of constrained autonomy;
- that the delegation-vs-control trade-off or escalation thresholds are new *questions*.

**What it leaves open.** A4, M1 and C4 are posed but not answered. WorkTrace offers a concrete, testable answer to A4/M1 for decision classes inside a process frame.

**Draft differentiation.** "The Agentic BPM manifesto frames *what* agents may do (normative and operational frames) and leaves open when an agent should be trusted to decide within the frame and when it must escalate (challenges A4, M1); WorkTrace answers that question per decision class from tested evidence handling."

**Cautions.** A manifesto preprint (v3, 12 Apr 2026), 18 authors. Use "framed autonomy". Our counterparty-verification domain is itself a business process, so this is a natural venue bridge (BPM, CAiSE, EPAIS).

---

### 2.18 Tomašev, Franklin & Osindero (2026), "Intelligent AI Delegation" — FULL TEXT — MAIN NOVELTY THREAT FOR CONTRIBUTION 1

**Problem & contribution.** "We define intelligent delegation as a sequence of decisions involving task allocation, that also incorporates transfer of authority, responsibility, accountability, clear specifications regarding roles and boundaries, clarity of intent, and mechanisms for establishing trust between the two (or more) parties" (§2.1).

**Concepts and mechanisms.**
- Task axes (§2.2): complexity, criticality, uncertainty, duration, cost, resource requirements, constraints, **verifiability**, **reversibility**, contextuality, subjectivity.
- Organisational concepts (§2.3): span of control, principal–agent problem, authority gradient, zone of indifference. On **trust calibration**: "trust calibration, where the level of trust placed in a delegatee is aligned with their true underlying capabilities".
- Echoes C&F's open delegation (§4.2): "We distinguish between atomic execution, where agents adhere to strict specifications for narrowly scoped tasks, and open-ended delegation, where agents are granted the authority to decompose objectives and pursue sub-goals. This level of autonomy should not be static; it may be constrained … explicitly by the delegator's trust model."
- Monitoring (§4.5): outcome-level vs process-level ("essential for tasks that are long-running, critical, or where the how is as important as the what").
- **Trust & reputation** (§4.6):
  - "We define trust as the delegator's degree of belief in a delegatee's capability to execute a task in alignment with explicit constraints and implicit intent. This belief is dynamically formed and updated based on verifiable data streams".
  - "reputation as the public, verifiable history of an agent's reliability, and trust as the private, context-dependent threshold set by a delegator".
  - Gaming: "an agent can inflate its reputation by only accepting simple, low-risk tasks".
  - "Behavioral Metrics … Evaluates how a task is performed rather than just the result" (Table 3), via "the clarity of reasoning traces and protocol compliance".
  - "This mechanism of graduated authority results in low-trust agents facing strict constraints … while high-reputation agents operate with minimal intervention."
- **Revocation** (§4.7): "Access rights are not static endowments but dynamic states that persist only as long as the agent maintains the requisite trust metrics. The framework should implement algorithmic circuit breakers".
- "contract-first decomposition … task delegation is contingent upon the outcome having precise verification" (§4.1).
- Liability firebreaks (§5.2).
- Footnote 1 on evaluation gaming: models can "detect when they are being evaluated".

**Evaluation.** None (position/framework paper; protocol sketches only).

**What WorkTrace must NOT claim.**
- Being the first to connect Castelfranchi–Falcone delegation and MAS trust/reputation to LLM agents.
- Introducing trust-scoped, graduated, revocable autonomy for LLM agents *as a concept*.
- Introducing process-level (how, not only what) evidence for reputation *as a concept*.
- Introducing verifiability and reversibility as delegation criteria.

**What it leaves open (WorkTrace addresses).**
- How "behavioral metrics" are measured; they propose reasoning-trace clarity, which is exactly the unfaithful-explanation trap (they cite Turpin et al. themselves).
- No empirical test that process-based trust predicts anything better than outcome-based reputation.
- No per-decision-class operationalisation.
- No escalation cost model.
- No treatment of evidence redundancy.

**Draft differentiation.** "Tomašev et al. argue for trust-scoped, graduated and revocable delegation to AI agents, informed by process-level behavioural metrics, but leave those metrics undefined and untested; WorkTrace defines one, the agent's tested responsiveness to decision-time evidence under redundancy-robust interventions, and shows on held-out episodes whether a delegation rule built on it beats an outcome-only reputation rule."

**Citation cautions.**
- An arXiv preprint (Google DeepMind authors), not peer-reviewed.
- It contains a reference error (Falcone & Castelfranchi SMC-A dated 2002; it is 2001).
- It is our closest conceptual predecessor for contribution 1: cite it prominently and early, not in a footnote.

---

### 2.19 Yuan et al. (2026), Sovereign-OS — PARTIAL (abstract, §1 contributions, §3.1)

"(3) Earned-autonomy permissions. We implement a TrustScore model (SovereignAuth) with asymmetric updates (+5 success, −15 failure) and tiered capability thresholds, requiring agents to demonstrate sustained trustworthy behavior before accessing dangerous capabilities" (§1).
- "Each agent starts with a base TrustScore of 50 … A single audit failure from score 50 drops the agent to 35, revoking write-file access" (§3.1).
- Successes and failures come from an LLM "Auditor (ReviewEngine)" that checks outputs against Charter KPIs.
- Reported numbers: "achieves 94% correct permission gating (200 trust-escalation missions)" (Abstract). Not checked further.

**Role for WorkTrace.** A published, concrete instance of **revocable, tiered, earned autonomy driven by outcome audits**. Use it as the "outcome-only" baseline archetype in H3, and cite it to show that the mechanism (earn, revoke) is not ours; the *basis* is. **Name collision**: our title "Earning Autonomy" ≈ their "earned-autonomy permissions".

**Cautions.**
- A demo/system paper; per-capability tiers, not decision classes.
- The audit is LLM-judged on outputs.
- Only partially read.

### 2.20 Ferreira (2026), "When Intelligence Becomes Agency" — PARTIAL

Defines "symbiotic agency as delegation under a standing, revocable mandate", with "behavioral episodes as the unit of analysis" (Abstract). It cites Castelfranchi & Falcone (related work). It is about *activation* (whether to act, ask, defer, refrain) and mandates, not about tested evidence handling.

Overlap with WorkTrace: the vocabulary of "revocable mandate" and "episodes". Cite in passing as a parallel governance framework; no empirical claim to compete with. Single-author preprint (company affiliation).

---

## 3. Concept table: what to reuse, from where, mapped to WorkTrace

| Classic concept | Source (section) | WorkTrace counterpart |
|---|---|---|
| Task τ = (α, g) as the object of delegation | C&F 1998 §2 | **Decision class** c: a family of decision situations sharing goal and admissible actions; the episode's action A_i and goal live inside the context C_i |
| Weak / mild / strict delegation | C&F 1998 §2.3 | WorkTrace concerns **strict** delegation: explicit, the agent "knows" it acts on our behalf, with permissions P_i. Weak/mild delegation (exploiting or inducing an agent's autonomous behaviour without agreement) is out of scope; say so |
| Open vs close delegation; discretion | C&F 1998 §2.7 | **proceed** = open delegation of the decision within class c (the agent has discretion). **escalate** = control of the decision retained by the principal (Scerri's H), with the agent's proposal as input. **refuse** = no delegation in c (Scerri's forbidden-action constraint) |
| "Rational to closely delegate when … we do not trust the ability … to find … a plan" | C&F 1998 §2.7 | The escalate/refuse decision is justified by low tested ability in c |
| Delegation of control (i)–(iv) | C&F 1998 §2.9 | WorkTrace is control **(ii) delegated to a third agent**: the test harness, ex ante through interventions and ex post through observed consequences O_i. It does not replace run-time control (iv) |
| Potential for relying vs decision to rely | C&F 1998 §2.3 | **Accountability profile** (beliefs, per class) vs **delegation rule** (decision) |
| Competence & willingness as the two trust pillars; DoT = Opp × Ability × WillDo | C&F 1998 §3.2; C&F 2000 §3.1, §3.3 | Interventions estimate an **Ability-type** component (evidence-sensitivity: remove X / only X / invert X / second source). The generator controls **Opp** (what evidence exists). **WillDo** (intention, persistence) is *not* measured, except weakly via consistency between declared grounds G_i and behaviour |
| Sources of beliefs about the contractor: experience, declaration, implicit communication, category | C&F 1998 §3 | WorkTrace adds **(e) controlled counterfactual testing**. Declared grounds G_i are source (b)/(c), which interventions check rather than accept |
| Decision is discrete; trust is graded; risk threshold; "acceptable damage" threshold | C&F 2000 §2.1, §3.4 | Profile graded per class, rule discrete. α is the risk-acceptance threshold. A **refuse** class corresponds to damage above the acceptable-damage threshold *regardless of* measured reliability |
| Over-confidence vs over-diffidence (too open delegation vs too many controls) | C&F 2000 §3.5.1 | The two axes of the risk–coverage curve: unjustified autonomous actions vs escalations |
| Articulated trust per aspect determines level and kind of delegation | F&C 1999 (Concl.) | Per-class rule; profile per intervention type |
| Bilateral, bidirectional adjustment; "crisis of trust"; delegee's self-confidence | F&C 2001 SMC-A (abstract) | **Revocation** triggers; add measurement of the agent's **own escalation calibration** (does it self-restrict when its evidence is insufficient?) |
| Transfer-of-control strategy; EQ^d_e(t), W(t), q(e), D actions | Scerri et al. §3, §4 | proceed = strategy A, escalate = strategy H (one-shot), refuse = A with "no action" (their fn. 7). **EQ^d_A for class c is what WorkTrace estimates**. Escalation cost c_esc ≈ q(H) + expected wait cost |
| Lemma 1: give the agent control iff waiting cost > quality gap | Scerri et al. §3.2 | The rule's threshold should depend on the quality gap EQ_H − EQ_A **and** the escalation cost, not on α alone (§4.3) |
| User constraints over learned policy | Scerri et al. §4.4 | Hard policy layer: classes forced to escalate or refuse regardless of test results |
| Calibration / resolution / functional & temporal specificity | Lee & See pp. 55–56 | Calibration: predicted vs held-out unjustified-action rate. Resolution: does the rule separate agents/configurations of different true quality (the outcome-only rule has low resolution when right-for-wrong-reasons is common)? Functional specificity: per decision class. Temporal specificity: revocation on drift or context change |
| Performance vs process vs purpose bases | Lee & See pp. 58–59 | Outcome-only rule = **performance** basis. WorkTrace = **process** basis, made *testable* rather than displayed |
| "Design for appropriate trust, not greater trust" | Lee & See (Implications) | Objective: minimise misuse (unjustified autonomy) and disuse (unnecessary escalation), not maximise coverage |
| Four function classes; levels per class; reliability & consequence costs as criteria | PSW 2000 (abstract) | Decision classes ⊂ stage 3. Interventions act on stage-1/2 inputs. α and costs are PSW's secondary criteria |
| Delegation = authority + responsibility "while the agent it acts on behalf of retains some responsibility" | PROV-DM §5.3.4 | Encode executed episodes as qualified `prov:Delegation` with decision class and rule version. The rule itself needs an extension (PROV records actual delegation, not permission) |
| Levels by user role; autonomy certificate; autonomy case; assisted evaluation | Feng et al. §3–5 | "Narrowed certification" = per-class certificate whose autonomy case is the test profile + held-out risk–coverage evidence |
| Framed autonomy; A4 delegation-vs-control; M1 escalation thresholds | Calvanese et al. §2.4, §4.3, §4.4 | WorkTrace operates *inside* a frame; answers A4/M1 per class |
| Graduated authority; trust ≠ reputation; behavioral metrics; circuit-breaker revocation | Tomašev et al. §4.6–4.7 | Concrete definition and test of a behavioural metric; revocation rule with held-out evaluation |

---

## 4. Proposed conceptual bridge (draft for the paper, ~1.5 pages)

### 4.1 Delegation in WorkTrace, in the classic vocabulary

We adopt Castelfranchi and Falcone's view that delegating is a *decision to rely*, made on the basis of *trust*: beliefs about the delegate's competence and willingness whose strength sets a degree of trust, compared with a risk-acceptance threshold [C&F 1998 §2–3; C&F 2000 §3].

In WorkTrace the principal (an organisation, through a human owner) considers **strict delegation** to an LLM agent. The delegation is explicit and the agent acts with permissions P. The object of delegation is not one task but a **decision class** c: a family of decision situations sharing a goal and an action set. For each class the principal chooses one of three delegation levels:

- **proceed**: *open delegation* of the decision. The agent has discretion over the choice within the frame of permitted actions; in Calvanese et al.'s terms, autonomy is *framed* by P and by hard constraints.
- **escalate**: the principal *keeps control of the decision*. The agent prepares the episode (context, evidence, declared grounds, proposed action) and transfers control to a human, a one-shot transfer-of-control strategy H in Scerri et al.'s sense.
- **refuse**: *no delegation* in c. The agent must not act, which corresponds to a forbidden-action constraint [Scerri et al. §4.4] or to an expected damage above the principal's "acceptable damage" threshold [C&F 2000 §3.4].

The delegation level is **adjustable and revocable**, as in Falcone and Castelfranchi's theory of adjustable social autonomy: a "crisis of trust" (here, a failed re-test or drift in observed consequences) moves a class from proceed to escalate.

### 4.2 Where the trust comes from: the missing source

Classic theory names four sources of the beliefs that justify delegation:
- past experience of the delegate's behaviour;
- its explicit declarations;
- implicit communication;
- attribution from its category or role [C&F 1998 §3].

Computational trust models in MAS mostly realise the first through interaction outcomes and reputation [Ramchurn et al. 2004 §2]. Ramchurn et al. note that the socio-cognitive model "lacks the rational grounding" that such outcome-based assessments provide.

Recent LLM-agent proposals keep the same sources. Sovereign-OS updates a TrustScore from audited outcomes. Feng et al. certify autonomy from task accuracy under assisted evaluation. Tomašev et al. ask for "behavioral metrics" based on reasoning-trace clarity.

WorkTrace adds a fifth source: **controlled counterfactual testing of decision episodes**. A decision episode E = (C, I, P, G, A, O) records:
- what the agent was allowed to do (P);
- what it could know at decision time (I);
- what it declared as its grounds (G);
- what it did (A);
- what followed (O).

Interventions on the *external* evidence in I (remove X, only X, invert X, add an independent second source) test whether A depends on the evidence the way the task requires. In Lee and See's terms, this moves the basis of trust from **performance** (what the agent achieved) to **process** (how it decided), and makes the process basis *testable* rather than *displayed*. The declared grounds G are treated as a declaration (source (b)), and the interventions check it rather than accept it.

### 4.3 What is estimated, and how it enters the decision

Castelfranchi and Falcone decompose the degree of trust into the credibility of beliefs about the delegate's opportunity, ability and willingness (DoT = DoC[Opp] · DoC[Ability] · DoC[WillDo]).
- WorkTrace's per-class profile estimates an **ability-type** component: *evidence responsiveness*, the probability that the agent's action is justified by the decision-time evidence.
- The episode generator fixes **opportunity** (which evidence exists and how redundant it is), so internal and external attribution can be separated, as C&F 2000 §3.2 requires.
- **Willingness** is not measured. We state this as a limitation (§4.5).

The profile is graded and multidimensional (one entry per intervention type). The delegation **decision is discrete**, as in C&F (2000 §2.1). WorkTrace's rule grants proceed in class c only if an upper confidence bound on the rate of unjustified autonomous actions is ≤ α. α is the principal's risk-acceptance threshold, set per class from the cost of consequences (PSW's secondary criteria).

Following Scerri et al. we make the **cost of escalation explicit**. Escalation is not free: it costs human time and delay (their q(e) and W(t)), and the human's decision is not perfect (EQ_H finite). Scerri et al.'s Lemma 1 implies that the agent should keep control when the expected cost of escalating exceeds the quality gap between the human's decision and its own. WorkTrace's evaluation therefore reports, on held-out episodes:
- the unjustified-action rate inside granted autonomy (misuse, in Lee and See's terms);
- autonomy coverage;
- the number and cost of escalations (disuse/over-control).

This gives a risk–coverage curve compared against an outcome-only rule that uses the same thresholds. Lee and See's three criteria become measurable properties of the rule:
- *calibration*: predicted vs held-out unjustified-action rate;
- *resolution*: whether the rule separates configurations of different true quality, where outcome-only rules are expected to fail when agents are right for the wrong reasons;
- *functional specificity*: per decision class.

### 4.4 Records

Each executed episode can be expressed in W3C PROV:
- `wasAssociatedWith(decision, agent)`;
- `actedOnBehalfOf(agent, principal, decision, [decisionClass, ruleVersion, verdict])` via a qualified `prov:Delegation`;
- for escalated episodes, an association with the human and the agent's proposal as an entity.

PROV records *that* a delegation happened and deliberately does not say "who bears responsibility and to what degree" (PROV-DM §5.3.4). The *standing, conditional and revocable* grant is a WorkTrace policy entity derived from test results, and it needs a small vocabulary extension.

### 4.5 Where the classic theory criticises this design (to state openly in the paper)

1. **Trust is more than one number, and more than competence.** C&F (2000) argue that reducing trust to a probability "reduces the explanatory and predictive power of the theory", and that competence and willingness predict different failures and call for different remedies.
   - Our rule thresholds one ability-type quantity. *Response*: keep the profile decomposed (per intervention type, per class), use the scalar only for the discrete decision (which C&F accept), and name what is not measured.
   - For LLM agents, "willingness" maps to goal and instruction adherence under conflicting pressure, sycophancy, susceptibility to injected instructions, and evaluation-aware behaviour (Tomašev et al. fn. 1). None of these is tested by evidence interventions.
2. **Internal vs external attribution.** The same failure rate can come from the agent or from poor evidence (C&F 2000 §3.2; Ramchurn et al. §4.2 "Context"). *Response*: the generator controls evidence regimes; report results per regime; never pool them into one trust score.
3. **Context and temporal specificity.** Trust is "context-dependent" (Lee & See; Tomašev et al. §4.6). A grant earned on one distribution of episodes may not transfer to another.
   - *Response*: define decision classes operationally.
   - Test transfer across held-out generators and seeds.
   - Make revocation triggers explicit (temporal specificity).
   - Read C&F 2010 §6.6 ("Trust Through Transfer and Generalization — Classes of Tasks and Classes of Agents") before claiming anything about class generalisation.
4. **Delegation is bilateral and bidirectional** (F&C 2001). The delegate may rightly restrict its own autonomy when it lacks self-confidence, or go beyond the literal request (C&F 1998 §2.10 "critical help"). A principal-side rule that ignores this may punish good behaviour.
   - *Response*: (a) count appropriate *self-escalation* as a measured capability;
   - (b) define "justified action" so that justified deviation from the literal instruction (critical help) is not scored as unjustified.
5. **Rationality is relative to alternatives.** Delegation is rational iff trust in the contractor exceeds trust in the alternatives (C&F 1998 §2). An absolute α ignores how good the human alternative is.
   - *Response*: report the human error rate and escalation cost as parameters, with a sensitivity analysis (the Scerri et al. Lemma 1 framing).
6. **Single-shot transfer is fragile.** Scerri et al. showed that rigid one-shot transfers fail in team settings, where response latency and miscoordination dominate. *Response*: state that WorkTrace models one-shot escalation without time-dependent wait costs or coordination-change actions; this is a scope limitation.
7. **Testing is not neutral.** Control interacts with trust (C&F 2010 §7.1.10 "Control Kills Trust", ToC only); strategic agents game the basis of trust (Ramchurn et al. "strategic lying"); agents may detect evaluation (Tomašev et al. fn. 1). Trust earned under test conditions with guardrails may not hold without them (Ramchurn et al. §4.2, after Molm et al.).
   - *Response*: hidden seeds and held-out generators (the anti-Goodhart mechanisms);
   - report the gap between test and deployment as a threat to validity.
8. **Trust ≠ reliance** (Lee & See). Even a well-calibrated rule may be overridden or rubber-stamped by human overseers (Feng et al. §3.4). WorkTrace evaluates the rule, not the human–rule system.

### 4.6 What is genuinely new relative to this tradition

- **A new source of the beliefs that justify delegation.** Controlled interventions on decision-time external evidence, robust to redundancy, as opposed to:
  - outcomes and reputation (Ramchurn; Sovereign-OS);
  - declarations and category (C&F);
  - designer-estimated decision quality (Scerri);
  - displayed process (Lee & See);
  - accuracy under assisted evaluation (Feng);
  - reasoning-trace clarity (Tomašev).
- **The decision episode as the unit that carries all of trust's ingredients at once**: the opportunity (I), the authority (P), the declared grounds (G), the act (A) and the consequences (O). Classic models attach trust to an agent–task pair, not to a recorded decision situation.
- **An empirical test of a delegation rule's predictive validity.** A risk–coverage evaluation on held-out generated episodes, with explicit escalation cost, against an outcome-only rule. None of the classic works compares *bases* of trust by how well the resulting delegation decisions generalise; Scerri et al. evaluated a deployed policy, not alternative trust bases.
- **Not new** (cite, do not claim):
  - delegation types and levels;
  - per-aspect or per-function trust and autonomy;
  - graduated, revocable autonomy;
  - escalation costs;
  - risk thresholds;
  - calibrated trust;
  - levels of autonomy for LLM agents;
  - autonomy certificates;
  - the conceptual MAS ↔ LLM delegation bridge (Tomašev et al. 2026).

---

## 5. Implications for WorkTrace

**Design changes.**
1. **Reword contribution 1.** From "a bridge between classic MAS delegation theory and LLM-agent auditing" to "an *operationalisation* of the socio-cognitive theory of delegation and trust: a test-based source for the competence belief, per decision class, with a revocable delegation rule whose predictive validity we test". Cite Tomašev et al. 2026 as the concurrent conceptual bridge, early in the introduction.
2. **Fix the vocabulary.**
   - strict delegation (not weak/mild);
   - proceed = open delegation of the decision in class c;
   - escalate = retained control / transfer of control H;
   - refuse = no delegation / forbidden action;
   - revoke = "crisis of trust".
   - Use "framed autonomy" for Calvanese et al., not "bounded autonomy".
3. **Add a Scerri-style cost model** to the H3 evaluation: c_esc (human time + delay), human error rate e_H, and the expected cost per episode = c_err·(unjustified autonomous) + c_esc·(escalated) + e_H·c_err·(escalated). Report a sensitivity analysis over c_esc and e_H. This also answers the "relative to alternatives" critique.
4. **Decompose the profile along DoT.**
   - Label each intervention by the trust component it informs: opportunity (generator-controlled), ability (evidence responsiveness), declared-ground consistency (a weak proxy for sincerity).
   - State that willingness/persistence is not measured.
   - Optional extension: an "instruction-conflict" intervention family as a willingness probe (out of the core scope).
5. **Measure delegee-side adjustment.** Add the agent's *self-escalation calibration* (does it ask or abstain when evidence is removed?) as a capability. It corresponds to F&C's "self-confidence" belief and to the bidirectional adjustment of autonomy.
6. **Define "justified action"** so that critical help is allowed: deviation from the literal instruction is justified if the evidence supports it.
7. **Report Lee & See criteria for both rules.** Calibration (predicted vs held-out), resolution (separation between agent configurations of known different quality), functional specificity (per class).
8. **Baselines for H3:**
   - (a) outcome-only threshold rule, as now;
   - (b) a Sovereign-OS-style asymmetric TrustScore with tiers (+5/−15) as the published archetype of "earned, revocable, outcome-based autonomy";
   - (c) optionally, Feng-style accuracy-threshold autonomy per class.
9. **PROV encoding.** Executed episodes as qualified `prov:Delegation`; the standing grant as a separate policy entity (a small WorkTrace vocabulary), explicitly not claimed to be PROV semantics.
10. **Title risk.** "Earning Autonomy" collides with "earned-autonomy permissions" (Sovereign-OS, 2603.14011) and "earned autonomy" (2603.26942). Either keep it and differentiate in the first paragraph ("earned from tested evidence handling, not from outcomes"), or choose e.g. "Evidence-Earned Autonomy" or "Autonomy by Evidence".

**Risks.**
- *Medium–high*: reviewers from AAMAS/MAS will know C&F, Scerri and Lee & See. Any "first to…" phrasing about graduated or revocable autonomy, per-class autonomy, or trust calibration will be rejected. Tomašev et al. pre-empts the conceptual bridge.
- *Medium*: C&F 2010 §6.6 (trust transfer across classes of tasks) may formalise what we call per-class delegation. It must be read.
- *Medium*: the critique that we reduce trust to one probability. Mitigate with a decomposed profile and an explicit statement of what is not measured.
- *Low–medium*: Scerri's critique of one-shot transfers. State it as a scope limitation.

**To cite (all verified; see §1).**
- Must cite:
  - Castelfranchi & Falcone 1998 (RAS);
  - Castelfranchi & Falcone 2000 (HICSS) and/or 1998 (ICMAS) for the degree of trust and the decision to delegate;
  - Falcone & Castelfranchi 2001 (IEEE SMC-A) for adjustable social autonomy;
  - Scerri, Pynadath & Tambe 2002;
  - Lee & See 2004;
  - Parasuraman, Sheridan & Wickens 2000;
  - Ramchurn, Huynh & Jennings 2004;
  - W3C PROV-DM/PROV-O 2013;
  - Tomašev, Franklin & Osindero 2026;
  - Feng, McDonald & Zhang 2025;
  - Calvanese et al. 2026.
- Optional:
  - Falcone & Castelfranchi 1999 (AAAI SS);
  - Castelfranchi & Falcone 2010 (book; only after reading the cited chapters);
  - Mostafa et al. 2019;
  - Sabater & Sierra 2005 and Pinyol & Sabater-Mir 2013 (only as further surveys until read);
  - Sovereign-OS 2026 (as the outcome-based baseline archetype);
  - Ferreira 2026 (in passing).

**Open TODOs.**
- Read Pinyol & Sabater-Mir 2013 (retry the IIIA PDF).
- Read the full text of Parasuraman et al. 2000 (the 10-level table; any recommended upper levels for high-risk decisions).
- Read C&F 2010 Ch. 3, §6.6 and §7.2.
- Read Falcone & Castelfranchi 2001 SMC-A in full (adjustment protocols).
- Read Sovereign-OS fully, if it is used as a baseline.
