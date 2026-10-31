# 4. From DSA to Delegation

This section turns per-class DSA measurements into decisions about autonomy. All statistical machinery is standard; we present it as an application of selective classification (El-Yaniv & Wiener, 2010; Geifman & El-Yaniv, 2017), Learn-then-Test (Angelopoulos et al., 2025) and anytime-valid testing (Waudby-Smith & Ramdas, 2024; Podkopaev & Ramdas, 2022). The contribution lies in the loss being certified and in the grant–revoke cycle around it.

## 4.1 Losses

For an episode $E$ with action $a(E)$ and normative action map $A^*(E)$ (§3.5), define

$$\ell_{\text{out}}(E) = \mathbb{1}[a(E) \notin A^*(E)],$$
$$\ell_{\text{basis}}(E) = \mathbb{1}\big[\exists\, do_j \in \mathcal{I}(E):\ a(do_j(E)) \notin A^*(do_j(E))\big],$$

and the *unjustified-action* loss $\ell_{\text{WT}}(E) = \max(\ell_{\text{out}}, \ell_{\text{basis}})$ (WT for WorkTrace, the name of the instrument), so that $\ell_{\text{WT}} \ge \ell_{\text{out}}$ pointwise. An action is unjustified if it is wrong, or right but on a basis that fails a pre-registered intervention, for example by ignoring an inversion or surviving the removal of its only support. Control arms (null, placebo, sham, copy) are reported separately and do not enter $\ell_{\text{basis}}$. Redundancy is handled by $A^*$: if a redundant source survives *remove $X$*, $A^*$ does not change and an agent that keeps its action is not penalised. The guarantee below always holds *relative to $\mathcal{I}$*; unjustified behaviour on features no intervention probes is invisible to it. In the theory only autonomous actions incur $\ell_{\text{WT}}$, and escalation and refusal are charged through cost (§4.7). In the pilot the agent proposes an action on every episode and every proposal is scored against the admissible set, so an escalation is unjustified when escalation is not admissible, and the loss is computed over all episodes of the class (§4.2).

The decomposition $\ell_{\text{WT}} = \ell_{\text{out}} + (1-\ell_{\text{out}})\,\ell_{\text{basis}}$ has the same shape as the trajectory loss of ToolChain-CRC, whose Proposition 1 shows that calibrating on final answers cannot control the second term (Opoku & Banahene, 2026). The difference is how the basis term is measured. ToolChain-CRC uses an audit label on the run's evidence; we use the counterfactual dependence of the agent's action. The two disagree in both directions: an agent that ignores valid supporting evidence passes their audit but fails ours, and an agent that correctly discounts a faulty tool output fails their audit but passes ours.

## 4.2 Per-class certification

Let $\varphi_c$ denote autonomous coverage in class $c$ and
$$R_c = \Pr\big(\ell_{\text{WT}}(E)=1 \mid \text{autonomous},\ \kappa(E)=c\big)$$
the *selective* risk (El-Yaniv & Wiener, 2010). We certify this conditional quantity, not the joint rate $\Pr(\ell_{\text{WT}}=1 \wedge \text{autonomous})$, which is smaller by a factor of $\varphi_c$ and does not bound the rate a delegator experiences (Khosravi & Huo, 2026). The pilot certifies a different quantity: the whole-class rate $U_c = \Pr(\ell_{\text{WT}}(E)=1 \mid \kappa(E)=c)$ of unjustified proposals, with escalations scored against the admissible set, because its agents propose an action on every episode and no deployed selector exists yet. A bound $U_c \le \alpha_c$ implies $R_c \le \alpha_c/\varphi_c$ for any selector that acts autonomously on a share $\varphi_c$ of the class, which is informative only when $\varphi_c$ is close to one; a certificate of $R_c$ itself needs a fixed selector and a denominator counted among the autonomous decisions, and the pilot's grants should not be read as one. For each class, calibration episodes $D_c$ are drawn from disjoint generator seeds. With $n_c$ decisions and $k_c$ unjustified ones among them, where for the selective guarantee $n_c$ counts the autonomous decisions of a selector fixed before calibration and for the pilot's whole-class rate it counts every episode of the class, the exact binomial p-value for $H_c: R_c > \alpha_c$ is $p_c = \Pr(\mathrm{Bin}(n_c, \alpha_c) \le k_c)$ (Clopper & Pearson, 1934). If a within-class readiness threshold is used, thresholds are tested in a pre-specified fixed sequence (Angelopoulos et al., 2025). Classes are combined by Bonferroni, $\delta_c = \delta/|\mathcal{C}|$, or by an allocation chosen on an independent split, as in Role-Stratified CRC (Rahman et al., 2026). The grant set is $\hat G = \{c : p_c \le \delta_c\}$.

**Proposition 1 (simultaneous per-class guarantee).** Suppose the episodes in each $D_c$ are i.i.d. draws from the generator's class-$c$ distribution, future class-$c$ episodes are drawn from the same distribution, and $\kappa$, the threshold sequence and $\pi$ are fixed in advance. Then
$$\Pr\big(\exists\, c \in \hat G : R_c > \alpha_c\big) \le \delta .$$

*Proof sketch.* Conditional on $n_c$, $p_c$ is super-uniform under $H_c$ (Geifman & El-Yaniv, 2017). Fixed-sequence testing controls the family-wise error within a class at $\delta_c$ (Angelopoulos et al., 2025), and a union bound across classes gives $\delta$. $\square$

With zero observed failures, certification at $\alpha_c = 0.10$ needs $n_c \ge 46$ for six classes at $\delta = 0.05$, and roughly 100 episodes per class give 80% power at a true rate of 2%. Pooled guarantees dilute rare classes: a pooled level $\alpha$ implies only $R_c \le \alpha / w_c$ for a class of prevalence $w_c$ (Rahman et al., 2026), which is why we certify per class.

## 4.3 Verdicts

Two one-sided tests per class yield four verdicts:

- **proceed:** $c \in \hat G$; the agent acts without review in $c$;
- **proceed-narrowed:** a preparatory sub-class of $c$ is in $\hat G$ but the binding step is not; the agent completes the preparatory determination and escalates the binding one;
- **refuse:** the lower Clopper–Pearson bound on $R_c$ exceeds a level $\beta_c > \alpha_c$ (p-value $\Pr(\mathrm{Bin}(n_c,\beta_c) \ge k_c)$, with its own $\delta$ budget). The class is certified bad and removed from the agent's permissions; the agent no longer drafts or proposes there. This verdict differs from the agent refusing an out-of-permission request, which is part of $A^*$ and is certified like any other action;
- **escalate:** otherwise, including whenever the evidence is insufficient either way.

Classes that the law subjects to meaningful human intervention, such as entering, refusing or maintaining a customer relationship under Art. 76(5)(b) of the EU Anti-Money Laundering Regulation (AMLR), and that the policy therefore reserves for human officers, receive *escalate* regardless of measured DSA; the rule then governs only their preparatory sub-classes.

## 4.4 Ceiling and certificate lifecycle

Following Zhang and Zhang (2026), autonomy is allocated beneath a fixed, human-set ceiling: the episode permissions $P$ bound what any grant may cover, and only a human can raise them. Widening a class from *escalate* to *proceed* is gated expansion beneath the ceiling, never above it. Grants are issued by an evaluator independent of the agent, so that evidence the agent produces about itself cannot raise its authority. Each certificate is bound to a fingerprint of $\pi$ (model, prompt, tools), is suspended on any change outside a declared set, and expires after a fixed period. We call this *reliability allocation beneath a fixed ceiling*; it is not a security guarantee.

## 4.5 Transfer across classes

A profile measured in a source class $s$ may inform a target class $t$ only if $Q_t \subseteq Q_s$ and the source tests were at least as demanding, reflecting the asymmetry of trust transfer in the delegation literature (Falcone & Castelfranchi, 2010; Soh et al., 2020). Transferred evidence is a prior that orders testing and supports conservative verdicts; it never certifies. A *proceed* verdict in $t$ requires class-specific episodes, or a stated exchangeability assumption together with a sentinel sample in $t$ that can falsify it. Escalation is tested separately in every class, since competence on a task does not imply competence in judging one's own competence on it.

## 4.6 Revocation and re-grant

After a grant, a random audit selects each autonomous episode with probability $r_c$, fixed before the episode is seen; audited episodes are replayed with interventions to obtain $X_t = \ell_{\text{WT}}$. Revocation tests $H_0: \mathbb{E}[X_t \mid \mathcal{F}_{t-1}] \le \alpha'_c$ with the betting e-process
$$\begin{aligned}M_t &= \prod_{s \le t} \big(1 + \lambda_s (X_s - \alpha'_c)\big),\\ \lambda_s &\in [0, 1/\alpha'_c) \text{ predictable},\end{aligned}$$
and revokes at the first $t$ with $M_t \ge 1/\delta_{\text{rev}}$; by Ville's inequality the probability of a false revocation is at most $\delta_{\text{rev}}$ under continuous monitoring (Waudby-Smith & Ramdas, 2024; Podkopaev & Ramdas, 2022). Hysteresis, $\alpha'_c > \alpha_c$ (e.g. 0.05 and 0.10), prevents a class whose true rate sits near $\alpha_c$ from flapping. A revoked class returns to *escalate*, and re-grant requires fresh evidence. Because failures are charged to the agent only when they are unjustified actions, not when the evidence could not have revealed the right action, revocation accumulates only agent-attributable failures (Castelfranchi & Falcone, 2000). A failure on a requirement triggers re-testing in every proceeding class that shares it.

Data-driven per-class withdrawal already exists for outcome signals, explicitly in Digital Apprentice and implicitly in Minimal Oversight (Azevedo, 2026). What we add is withdrawal triggered by failed intervention tests, with hysteresis and re-testing across shared requirements. Unlike scheduled certificate resets (Khosravi & Huo, 2026), revocation here is data-driven. Detection is slow: when the true rate doubles, the median delay is about 113 audited episodes at $\alpha'_c = 0.05$. This argues for higher audit rates in high-stakes classes and is reported as a limitation. The grant–audit–revoke cycle has a classical precedent in continuous sampling inspection (Dodge, 1943).

## 4.7 Cost and masking

Risk is the constraint; cost is the objective among certified options. With deployment class mix $w_c$, the agent's inference cost per episode $c^{\mathrm{inf}}_c$ (paid on every episode, because the agent proposes even where it will escalate), harm $L_c$ of an unjustified action, escalation cost $e_c$, reviewer error $h_c$, and the cost $C_c$ of certifying class $c$ spread over the $N$ episodes a certificate covers before it expires, the expected cost per episode is
$$\begin{aligned}\mathcal{J} = \sum_c w_c\Big[\,&c^{\mathrm{inf}}_c + \mathbb{1}[c\in\hat G]\big(\varphi_c L_c R_c + (1-\varphi_c)(e_c + h_c L_c)\big)\\ &+ \mathbb{1}[c\notin\hat G]\,(e_c + h_c L_c)\Big] + \frac{1}{N}\sum_{c\in\hat G} C_c,\end{aligned}$$
optionally subject to a review-capacity bound $\sum_c w_c\,(1 - \mathbb{1}[c\in\hat G]\varphi_c) \le B$, following the learning-to-defer formulation (Madras et al., 2018; Mozannar & Sontag, 2020). Reviewer error is not zero, so escalation is never free.

All rules, ours and the baselines, obey a *masking rule*: the agent is scored on its own proposal on every episode, including escalated ones, and an episode that was escalated and then corrected by a human never counts as an agent success. Without it, correction hides raw competence and inflates any track record (Azevedo, 2026).

---

## References

All entries are in `paper/references.bib` (verified 2026-10-26; see its `x-verified` fields). Keys cited in this section: `angelopoulos2025ltt`, `azevedo2026minimal`, `castelfranchi2000trust`, `clopper1934confidence`, `dodge1943sampling`, `elyaniv2010foundations`, `falcone2010transitivity`, `geifman2017selective`, `khosravi2026csa`, `madras2018predict`, `mozannar2020consistent`, `opoku2026toolchain`, `podkopaev2022tracking`, `rahman2026rolestratified`, `soh2020multitask`, `waudbysmith2024betting`.
