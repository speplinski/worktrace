# R4 — Pandey et al., certified multi-source integrity, as baseline B-Pandey

Prepared 25 Oct 2026. This note covers the full paper, its code, and the same group's other paper. Read with `positioning.md` v3 (W1 = DSA construct; W2 = delegation rule based on DSA; W3 = predictive-validity test against 12 baselines), `r3_evidence_interventions.md` §5 and §7, and `r2_governance_context.md` §B (synthetic AMLR counterparty policy P1–P15, decision classes §B.3).

---

## 0. Headline (read first)

1. **Correction to how we have described it.** The certifier was **not run on sanctions-screening decisions.**
   - The sanctions data (OpenSanctions, 70,966 entities) is used *only* in §4, to measure how often the multi-source precondition holds. That is the distribution of the number of issuing domains per designated entity.
   - Every certifier experiment (§3, §5, §6, App. B) uses **synthetic accounts-payable payment episodes**: payee, account and amount, with GBP amounts and GB-style account numbers. No sanctions field appears in them.
   - In `positioning.md` §2 W3, "certyfikator wielodomenowy w domenie sankcji" should read "a multi-domain corroboration certifier for agent payment actions; corroboration prevalence measured on sanctions designations".
2. **It does not measure the agent's decision behaviour.**
   - The model is reduced to a **source-isolated field extractor**. The certifier votes over per-source extractions and "never consumes the holistic proposal" (App. B).
   - There are no decision classes, no per-agent or per-configuration certificate, no revocation, and no learned or earned autonomy. Escalation (⊥) is scored as *safe*, with only a "false-abstention" liveness cost.
   - **Threat to W1 is low. Threat to W2 is medium:** it occupies "evidence structure gates autonomous action and escalates otherwise" in our own domain, with a theorem.
3. **Strongest point against WorkTrace: their Theorem 1 binds us too.**
   - Under their adversary (k corrupted control domains), *any* decision procedure that sees the same observation must abstain when two actions are k-feasible. That includes a DSA-certified agent.
   - So WorkTrace **cannot claim** higher safe coverage than B-Pandey **under adversarial corruption**. Any coverage gain there is bought with unsafe executions in some within-budget world.
   - WorkTrace's claim must be scoped to **non-adversarial evidence shift** (missing, stale, inverted or redundant evidence), and to decisions that are **rule-governed functions of evidence**, not corroborated field values. For adversarial settings, recommend **composing** with a Pandey-style gate.
4. **Empirical risk to W3 is medium to high in two of our classes.** Our synthetic policy rule P12 ("≥1 tier-1 or ≥2 independent sources") is itself a Pandey-style quorum rule. In class (i), identification-evidence consistency, and class (iv), request-document actions, B-Pandey given true domain labels will be close to the policy-optimal rule. Expect to **tie or lose** there, and pre-register that expectation.
5. **Design change forced by their Prop. 3 / Table 5.** `positioning.md` §3 defines "independent" as "distinct provenance **or** control domain". That is **unsafe**. Counting provenance *roots* is defeated by one compromised domain that issues several distinct original records. Independence must be **disjoint dependency sets over control domains**, counted by minimum hitting set (their Defs 1–2).
6. **Same group, second paper (new, important): Pandey, Jain, Chen, Maple, "Local Allow, Global Deny", arXiv:2610.27620 (IEEE TPS 2026, accepted per arXiv comment).**
   - It proves that "disclosure depends on context the purpose does not authorize" is a **2-safety hyperproperty** (a property of *pairs* of executions, not of single runs). A false-alarm-free per-trace monitor detects none of these violations (Thm 3).
   - It also shows that no single-execution observable decides the distributional version (Thm 4). Even paired comparison gives only statistical detection (Thm 5).
   - This is **formal support** for WorkTrace's thesis: rules built only on single-run outcome or trace judgements (B-OO, B-trace-judge, B-READY-proc) are structurally blind to dependence on the wrong evidence, which interventions over paired episodes can reveal.
   - It is also a **mild W2 threat**: paired executions that hold the authorized view fixed and vary only the unauthorized context are an intervention design, and they ran an offline paired audit of a frontier model with a Clopper–Pearson upper bound. They do not use it for delegation.

---

## 1. Coverage and verification

| Item | Verified | What I read |
|---|---|---|
| Pandey, Jain, Chen, Maple, Panchev, "Certified Multi-Source Integrity for Structured Agent Actions", arXiv:2609.34245v1 | arXiv API [verified]; PMLR vol. 348 index page [verified] | **Full PDF v1, all 14 pages:** §1–8, App. A (proofs), App. B (protocol; Tables 2–7; hitting-set algorithm; dependency-set maintenance; per-source vs holistic gap; extractor-independence study; canonicalization gap). The HTML version was downloaded but not read separately. |
| Code: github.com/anmolpandey299/certified-multisource-integrity (fetched via raw.githubusercontent.com on 25 Oct 2026; commit hash unknown, since the GitHub API and the tarball were blocked by the proxy) | — | README, LICENSE, `corruption_distinct.py`, `sanctions_mincover.py`, `agent_certify_harness.py`, `mechanism_unit_eval.py`, `baseline_headtohead.py` in full; `adaptive_attack_harness.py` lines 1–520 of 807 (all certifier and baseline logic; not the frontier, CSV or CLI code). **Not read:** `results/`, `runs/` logs, `supply_chain_provenance_study.py`, `reputation_axis.py`, `byzantine_radius_sweep.py`, `vote_identity_experiment.py`, `audit_log.py`. |
| OpenSanctions licence | opensanctions.org/licensing [verified 25 Oct 2026] | Footer statement: data "licensed under the terms of Creative Commons 4.0 Attribution NonCommercial". Commercial use requires a licence. |
| Pandey, Jain, Chen, Maple, "Local Allow, Global Deny: Why Per-Action Authorization Does Not Compose in LLM Agents", arXiv:2610.27620v1 | arXiv API [verified]. IEEE TPS 2026 acceptance only from the arXiv comment and the PDF header [unverified in IEEE Xplore] | **Full PDF v1, 12 pages:** §I–XI, App. A–C. The artifact repo `al-synth` was not read. |
| Same-group search | arXiv API author queries: `au:"Anmol Pandey"`, `au:Panchev AND au:Maple`, `au:"Carsten Maple" AND abs:agent(s)`, `au:"Liang Chen" AND au:Maple`. A DBLP query returned non-JSON and failed. | Only 2609.34245 and 2610.27620 share the author group. Other Maple co-authored 2026 agent papers come from different Warwick teams; titles only, not read: Kumar & Maple 2607.03968; Tapwal, Kumar, Maple 2605.10614; Wang et al. 2606.00756; Radanliev et al. 2606.19390, 2603.10057, 2605.19755; Baldazzi et al. 2606.22485. None looks relevant to delegation. |

---

## 2. Pandey et al. (2026), "Certified Multi-Source Integrity for Structured Agent Actions"

### 2.1 Bibliographic data [verified]
- **Title:** Certified Multi-Source Integrity for Structured Agent Actions
- **Authors:** Anmol Pandey, Aditya Jain, Liang Chen, Carsten Maple, Christo Panchev. Pandey, Jain, Maple and Panchev are at the University of Warwick; Chen is at the University of Hertfordshire.
- **Venue:** *Proceedings of the Fourth UK AI Conference 2026* (UKAI 2026, Nottingham, 29–30 Sep 2026), **PMLR 348:134–147**, published 30 Sep 2026. Confirmed on the PMLR v348 index page. PMLR issues no DOI.
- **arXiv:** 2609.34245v1, 28 Sep 2026. Primary category cs.CR; also cs.AI and cs.LG.
- **Code and data:** github.com/anmolpandey299/certified-multisource-integrity. MIT licence, "Copyright (c) 2026 Anonymous Author(s)". Standard library only.

### 2.2 Problem and contribution
- **Problem.** An agent assembles a privileged structured action, a payment (payee, amount, account), from documents and tool outputs that an adversary can corrupt. Prompt injection can make the model itself extract attacker-chosen values. Existing defences "gate on a source's trust label or certify free-text answer quality" (Abstract).
- **Four contributions (§1):**
  1. A characterization of safe certifiability. "Execution is sound exactly when the budgeted feasible set is a singleton, and the certifier meeting this bound is maximally live."
  2. An ablation showing that each mechanism is necessary.
  3. A measurement of how often the multi-source precondition holds on sanctions designations and npm/PyPI provenance.
  4. A live-model evaluation over five models against capability-gating and policy-monitor baselines.

### 2.3 Method: the exact certifier rule (question a)

**Objects (§2).**
- **Action.** a = (a₁, …, a_d) is a tuple of action-critical fields. For a payment these are payee identity, payable amount and payee account.
- **Attestation.** A pair (v, c) in which an *evidence class* c asserts value v. Each attestation is "bound, by an unforgeable origin identifier, to the control domain that produced it, and carries a provenance root". "A copy inherits the root of its source."
- **Adversary.** Picks a set C of control domains with |C| ≤ k. Inside C it may set values arbitrarily and "emit arbitrarily many records, including several distinct original records as well as laundered copies". It knows the certifier, the corpus and the policy. Its goal is either a wrong execution or forced abstention.
- **Trusted obligation skeleton Γ.** Fixed "from trusted user intent alone, before any untrusted evidence is read". It pins down "the operation, transaction key, mandatory relations, eligible sources, allowed destinations, amount cap, and policy version". Untrusted evidence may only fill the values Γ leaves open. This closes the *selection attack*, in which a poisoned source steers the agent to a different transaction.

**What counts as a separate control domain (Defs 1–3).**
- **Def. 1, dependency set.** D(att) is "the set of control domains for which corrupting any single member removes att". An authority that designates an entity on its own has D = {that authority}. "A national listing that merely transposes a United Nations designation has D(att) = {the nation, the UN}."
- **Def. 2, corruption-distinct count.** m = min |X| such that X ∩ D(attᵢ) ≠ ∅ for all i. This is a **minimum hitting set**: the fewest domains an adversary must corrupt to erase every attestation. For a threshold predicate such as "entity is designated", the **presence-removal radius is m − 1**.
- **Def. 3, budgeted influence.** b_k is the largest number of attestations that any k domains can alter. If dependency sets are disjoint, b_k = k; otherwise replace k by b_k (exact-value condition N > 2b_k).
- **Practical rule (App. B).** Mapping datasets to domains is "a curation task, folding datasets that share a jurisdiction or body". "An attestation of unknown provenance should be assigned to an unknown domain shared with every other unknown." Missing metadata therefore "costs liveness and never safety".
- **Prop. 3, vote identity.** Votes must be counted "once per authenticated control domain". **Root-counting is not enough**, because one compromised domain can issue several distinct originals, each with its own root. Table 5 shows this: at N = 2, a domain issuing two originals gets a wrong value certified under per-root counting, while per-domain counting abstains.

**Field rules (§2, "Certifier rules").** Each field is decided by the rule its evidence structure supports. The action executes only if every field is admitted; otherwise the result is ⊥, "an abstention that escalates to a human".

| Field structure | Rule | Exact condition | Guarantee |
|---|---|---|---|
| Multi-source **identity** field (payee) | **Agreement or escalate** | Execute v when "a mandatory quorum of corruption-distinct classes is present and all of them agree on v after canonicalization"; otherwise ⊥ | (N−1)-safe with abstention if ≥1 class is honest (Prop. 1). Not maximally live. |
| Multi-source **value** field | **Unique-threshold admission** | Admit v iff at most k corruption-distinct classes dissent (support ≥ N − k) **and** v is the *only* value clearing that threshold | Any admitted value is correct. Exact certification iff N > 2k, radius ⌊(N−1)/2⌋ (Prop. 2). |
| **Complementary** field (amount) | **Reconciliation** | A deterministic constraint, e.g. "invoiced amount lying within the authorized order plus tolerance" | A bound, not a radius |
| **Single-sourced** field (account) | **Anchor gate** | Execute when the account "both matches the payee name at the bank and appears on the onboarding allowlist"; otherwise ⊥ | Rests on trusted anchors outside the budget. Thm 1: "the anchor is necessary". |

**Theorem 1 (singleton feasibility).** An action is *k-feasible* if it satisfies Γ and one corruption set of size ≤ k explains every disagreeing attestation across all fields. Write F_k for the set of k-feasible actions.
- A k-safe certifier may execute a iff F_k = {a}. When |F_k| ≠ 1, "every k-safe certifier must abstain".
- The unique-feasible certifier is maximally live.
- Proof (App. A): two feasible actions give the same observation in two within-budget worlds.
- **Prop. 4:** the implemented field-wise rule is sound but conservative. It can abstain where the joint rule would certify.

**Trusted computing base (§2, four assumptions):**
1. Authentication of origin identifiers.
2. Trusted anchors (onboarding allowlist, account-name registry).
3. A trusted join key.
4. **Sound extraction:** "The extractor is itself a shared control domain… a systematic parser fault or a malicious provider is a common-mode corruption that source isolation does not remove."

**What the paper says about our specific sub-questions:**
- **Conflicting sources.**
  - Under agreement: any dissent → ⊥.
  - Under threshold: admit only if dissent ≤ k and the value is unique.
  - At N ≤ 2k two values can be feasible → ⊥ ("Uniqueness is load-bearing").
- **Stale data.** **Not addressed.** There are no timestamps, validity windows or freshness rules anywhere in the paper or the code I read. Dependency-set curation is reviewed "quarterly" (App. B), but that concerns metadata, not evidence freshness.
- **Partial matches.**
  - Only **deterministic canonicalization** is used: amounts by numeric value, accounts by alphanumerics, payees by "normalized text" (casefold plus whitespace, from the code). There is no fuzzy matching.
  - A partial or variant match counts as disagreement and therefore as ⊥ under agreement.
  - App. B reports a **canonicalization gap**: a Cyrillic vendor name was transliterated by models at 0–7.5%, and "canonicalization should fold scripts as well as case". It never caused an unsafe action but cost liveness (Haiku 4.5 abstained 4%).
- **Human handoff.** ⊥ is the only handoff. The paper does not model what the human receives, a human error rate, or escalation cost. The code returns reason codes such as `skeleton_no_attestation_for_transaction`, `payee_no_value_clears_threshold`, `payee_ambiguous_two_values_clear_threshold`, `amount_reconciliation_failed`, `amount_missing_source`, `account_missing` and `account_anchor_mismatch`.

**Implementation details from the code that matter for a faithful B-Pandey** (code read 25 Oct 2026; these are *not* stated in the paper):
- **Live-model harness** (`agent_certify_harness.py`, `baseline_headtohead.py`):
  - The certifier **votes on all three fields**, account included, with agree or N−k rules.
  - It applies **no skeleton, reconciliation or anchor gate**, and each source is *assumed* to be its own control domain.
  - Unparsed extractions are **dropped before agreement** (`agree_or_escalate` filters `None`). Agreement among the parsed subset therefore suffices; no mandatory quorum is enforced.
  - This is why the head-to-head certifier "pays every novel payee": an anchor gate with an onboarding allowlist would have refused novel payees. The paper's anchor-gate description (§2) and its novel-payee utility claim (§6) therefore refer to *different* certifier configurations.
- **Model-free mechanism harness** (`mechanism_unit_eval.py`):
  - The mandatory-source rule counts **≥ 2 distinct roots** for the vendor field, not domains.
  - The amount check is reconciliation with a +50 tolerance; the account is checked against the name registry and the onboarding allowlist.
- **Adaptive harness** (`adaptive_attack_harness.py`, `full_certifier`):
  - Root-counted plurality uses **observed** N, so the threshold is n_roots − k.
  - If sources were omitted down to one root, the threshold would be 0 and a single value would be certified. The harness never tests omission; omission is covered only in `mechanism_unit_eval.py`.
  - B-Pandey must therefore **pin N and the mandatory domains from Γ**, not from what is observed.
- **Sanctions measurement** (`sanctions_mincover.py`):
  - The "control domain" is the **dataset-name prefix** (e.g. `eu_fsf` → EU), and every attestation has a **singleton** dependency set.
  - Def. 1's transposition structure (D = {nation, UN}) is **not applied**. The code comment calls it "the next step".
  - Consolidated or aggregator datasets are excluded (`us_trade_csl` is mentioned; denylist: wikidata, opencorporates, *_pep, everypolitician, interpol, ext_).

### 2.4 Implementable pseudocode for B-Pandey

Part A is faithful to the paper. Part B lists **our** adaptations for the counterparty pilot, each flagged so we never attribute it to them.

```python
# ===== Part A: B-Pandey core (Pandey et al. 2026, §2, Props 1-4, App. B) =====
# Γ: trusted obligation skeleton, fixed from the decision class + case BEFORE reading untrusted evidence.
Γ = dict(
    decision_class, operation, case_key,          # join key: attestations for other cases are ignored
    policy_version,
    field_rule = {f: "AGREE" | "THRESHOLD" | "RECONCILE" | "ANCHOR"},
    eligible_source_types,                        # e.g. {register_excerpt, gov_id_doc, lei_record, customer_doc}
    mandatory_domains = {f: set_of_domains},      # mandatory-source rule (Table 3, "no mandatory source")
    expected_domains  = {f: set_of_domains},      # pins N for THRESHOLD   [ours: code uses observed N]
    q_min = {f: int},                             # AGREE quorum, counted as min-hitting-set size
    k,                                            # corruption budget in control domains
    reconcile = {f: predicate_over_certified_fields},
    anchors   = {f: trusted_lookup},              # e.g. register-of-record, onboarding allowlist
)

@dataclass
class Att:
    field: str
    value: object
    source_id: str
    source_type: str
    case_key: str
    domain: str        # authenticated origin; unknown provenance -> "UNKNOWN" (one shared domain)
    root: str          # provenance root; copies inherit it (used only for diagnostics)
    D: frozenset       # dependency set, Def. 1 (e.g. {"NAT_X","EU"} for a transposition)

def extract(sources, model):                      # source-isolated reads: one call per source (§5)
    return [att for s in sources for att in parse(model(single_source_prompt(s)), s)]

def canon(f, v):                                  # deterministic canonicalization only (no fuzzy match)
    if type_of(f) == "amount": return round(float(digits(v)), 2)
    if type_of(f) == "id":     return alnum(v).upper()
    return " ".join(str(v).split()).casefold()    # paper does NOT fold script/transliteration (App. B)

def tau(atts):                                    # minimum hitting set over dependency sets (Def. 2)
    return min_hitting_set([a.D for a in atts])   # exact; greedy only if >22 domains, and greedy
                                                  # OVERstates m, so use an exact or lower bound (App. B)

def eligible(atts, f):
    return [a for a in atts if a.field == f and a.case_key == Γ.case_key
            and a.source_type in Γ.eligible_source_types]

def admit_field(f, atts):
    A = eligible(atts, f)
    present = {a.domain for a in A}
    if not Γ.mandatory_domains[f] <= present:
        return BOT(f, "mandatory_source_missing")
    rule = Γ.field_rule[f]
    if rule == "AGREE":                                      # Prop. 1
        if tau(A) < Γ.q_min[f]:
            return BOT(f, "quorum_not_met")
        vals = {canon(f, a.value) for a in A}
        return OK(vals.pop()) if len(vals) == 1 else BOT(f, "disagreement")
    if rule == "THRESHOLD":                                  # Prop. 2 / Prop. 4 general form
        # A missing expected domain counts as dissent from every value.
        missing = [Att(f, None, ..., D=frozenset({d}))
                   for d in Γ.expected_domains[f] - present]
        cands = {canon(f, a.value) for a in A}
        feasible = [v for v in cands
                    if tau([a for a in A if canon(f, a.value) != v] + missing) <= Γ.k]
        # A domain that emits two different values is automatically a dissenter for each of them.
        if len(feasible) == 1:
            return OK(feasible[0])
        return BOT(f, "no_value_clears_threshold" if not feasible else "ambiguous")
    if rule == "RECONCILE":                                  # deterministic check, not a vote
        return OK(value_of(f)) if Γ.reconcile[f](certified_so_far) else BOT(f, "reconciliation_failed")
    if rule == "ANCHOR":                                     # single-sourced field
        vals = {canon(f, a.value) for a in A}
        if len(vals) != 1:
            return BOT(f, "missing_or_conflicting")
        v = vals.pop()
        return OK(v) if Γ.anchors[f](v, certified_so_far) else BOT(f, "anchor_mismatch")

def b_pandey(case, sources, model):
    atts = extract(sources, model)
    results = {f: admit_field(f, atts) for f in fields_in_dependency_order(Γ)}  # RECONCILE/ANCHOR after AGREE/THRESHOLD
    if all(r.ok for r in results.values()) and instantiates(Γ, results):
        return PROCEED(action_from(results))                 # "Execute(a)"
    return ESCALATE(reasons=[r.reason for r in results.values() if not r.ok])   # "⊥ → human"
```

```python
# ===== Part B: OUR adaptations for the counterparty pilot (not in the paper) =====
# B1. Freshness (variant B-Pandey+T). The paper has no time dimension.
#     Before voting, drop attestations with as_of < decision_date - window(source_type)
#     (P3: register excerpt 30 d [synthetic parameter]; P14: 1 y / 5 y).
#     The faithful B-Pandey (variant F) skips B1. Run both: F shows the stale-corroboration
#     failure mode; +T shows the best case.
#
# B2. Sanctions clearance (class vi), derived from the paper's own logic:
#     "designated" is a presence predicate with removal radius m-1 (Def. 2). Clearing an entity
#     ("not designated") cannot be certified by counting: an entity on one list (m=1, ~75% of real
#     entities by Table 2) is erased by one corruption. By Thm 1 a single-sourced fact needs a trusted anchor.
def screen(entity):
    hits = [r for r in list_responses(entity) if r.match in {"exact", "partial"}]   # any eligible list
    if hits:
        return ESCALATE("possible_hit")              # partial matches go to a human, no fuzzy auto-clear
    if not anchor_fresh_no_match(BINDING_LIST, entity):
        return ESCALATE("anchor_missing")            # synthetic EU list = trusted anchor
    if ownership_by_designated_over_50pct(entity):   # P9 aggregate-stake test: a computed predicate,
        return ESCALATE("computed_predicate")        # outside B-Pandey-F; deterministic in B-Pandey-R
    return PROCEED("clear")
#
# B3. Non-field decisions (BO set, P6 route, P8 plausibility, P10 PEP consequences, P11 consistency):
#     B-Pandey-F: ESCALATE always (the certifier certifies field values, not decisions).
#     B-Pandey-R: certify input fields (ownership edges, dates, flags) with Part A, then compute the
#       policy predicate deterministically (as a RECONCILE rule). ESCALATE when the predicate is
#       open-textured ("grounds for suspicion", "legitimate economic reason"), which no rule can compute.
#
# B4. Domain labels come in two versions: ORACLE (generator's true dependency sets, incl. transpositions
#     and shared upstreams) and APPARENT (one domain per outlet/dataset, as a naive deployment would curate).
```

### 2.5 Data (question b)

| Dataset | Role in paper | Real or synthetic | Size | Licence | Reusable in our synthetic counterparty environment? |
|---|---|---|---|---|---|
| **OpenSanctions "Consolidated Sanctions" collection** (`sanctions/entities.ftm.json`, accessed 14 Sep 2026; "continuously updated") | §4 only: measures the distribution of mapped issuing domains m̂ per designated entity | Real | **70,966** entities with ≥1 designation authority, after OpenSanctions' entity resolution | Data **CC BY-NC 4.0** (commercial use needs an OpenSanctions licence) | **No, not as data.** Our policy forbids real sanctions lists and real names (`r2_governance_context.md` P9 note and §C.5), and CC BY-NC conflicts with any commercial follow-up. **Yes, as published marginals:** cite Table 2 and use it to set the domain-count distribution of our *synthetic* designations (see below). |
| npm dependency closure of 20 popular roots | §4: witnesses to "package P comes from repository R" (registry, SLSA provenance, repository back-reference) | Real, fetched live | 450 packages; 307 declared repositories for the reputation axis | npm metadata. The licence is not stated in the paper. | Not relevant to our domain. Cite only as the second example of "apparent witnesses collapse to fewer domains". |
| PyPI packages | §4: same analysis | Real | 300 packages | Not stated | Not relevant |
| **Synthetic AP payment episodes** (`agent_certify_harness.py`) | §5–6 live-model loop | Synthetic: 10 fictional vendors, 4 attacker vendors, 5 source kinds (purchase order, supplier invoice, bank verification record, ERP vendor-master export, AP ledger entry), injections appended as "PROCESSING NOTE" or "REMITTANCE UPDATE (verified)" | 80 episodes per model per run, about 4,000 calls in total | MIT (code) | **The template is reusable** (MIT, keep the copyright notice), but it is a toy: every source carries the same three fields in identical layout. It is useful as a format reference for our *adversarial arm*, not as episode content. |
| Model-free worlds (`mechanism_unit_eval.py`, `adaptive_attack_harness.py`) | §3, §6, App. B Tables 3–5, 7 | Synthetic | 3,000 worlds per cell (ablation); 2,000 worlds (adaptive); 4,000 configurations per cell (Byzantine sweep) | MIT | **`corruption_distinct.py` can be reused directly** for our hitting-set computation (MIT, with attribution). |

**Table 2 (App. B), the numbers to reuse as synthetic parameters.** Mapped issuing domains per designated entity, N = 70,966.

| | raw dataset | control domain |
|---|---|---|
| m̂ = 1 | 62.5% | **74.6%** |
| m̂ ≥ 2 | 37.5% | **25.4%** |
| m̂ ≥ 3 | 22.7% | **14.9%** |
| m̂ ≥ 4 | 14.5% | **11.7%** |

Both columns are upper bounds. The control-domain column folds by jurisdiction prefix only, and EU member-state and UN transpositions are not collapsed (code comment). For our generator, sample synthetic designations with m̂ from the control-domain column. Then **add explicit transposition dependency sets** (national list D = {NAT, EU} or {NAT, UN}), so that the generator's *true* m is lower than the apparent count, as their Def. 1 says it should be.

### 2.6 Evaluation: metrics and results (question c)

**Metrics:**
- injection-following rate on source-isolated reads of the corrupted source;
- naive-agent unsafe rate, from a holistic read of all N documents;
- certifier unsafe rate;
- certifier abstention on attacked episodes;
- false abstention on clean episodes (the liveness cost);
- utility = correct payments / all episodes (head-to-head);
- attacker success per attack family (ablation, adaptive);
- the m̂ distribution (prevalence).

**Results:**
- **Table 1** (five models via OpenRouter, N = 5, k = 1, threshold rule; 80 episodes each, 54 attacked and 26 clean):

  | Model | Injection-following | Naive unsafe | False-abstain | Certifier unsafe |
  |---|---|---|---|---|
  | Claude Opus 4.8 | 0% | 0% | 3.8% | 0% |
  | GPT-5.5 | 100% | 72% | 0% | 0% |
  | Gemini 3.1 Pro | 100% | 100% | 0% | 0% |
  | Gemini 3.5 Flash | 100% | 98% | 0% | 0% |
  | Claude Haiku 4.5 | 100% | 100% | 0% | 0% |

  Text (§5):
  - The agreement rule at N = 3 has 0–12% honest-world false abstention.
  - The threshold rule has ≤ 4% false abstention and abstains on 0–6% of attacked episodes.
- **Head-to-head** (Fig. 3, Haiku 4.5; separate run of 80 episodes, 44 attacked, 36 clean, 13 with a novel payee):

  | Defence | Unsafe | Utility |
  |---|---|---|
  | Certifier | 0% | 98% |
  | CaMeL/FIDES-style capability gating | 0% | 0% ("executes nothing") |
  | PCAS-style policy monitor | 18% | 29% (0% on novel payees) |
  | Naive agent | fully unsafe | ≈45% (bar label in extracted figure text; **uncertain**) |

  - Across models the certifier is "96 to 100% correct overall" and pays 100% of novel payees.
- **Adaptive model-free attacker** (2,000 worlds): never forces an unsafe certifier execution and breaks both proxy baselines in every world.
  - Table 7: action-gating is unsafe on 5 of 6 families (it blocks only the fresh mule account); provenance-only is unsafe on 5 of 6 (it blocks only the currency swap).
- **Ablation** (Table 3): each removed mechanism opens exactly one attack at 100%:
  - join key → amount splice;
  - account policy → mule account;
  - mandatory source → omission;
  - atomic-claim counting → laundering;
  - authentication → Sybil.
- **Byzantine sweep** (Table 4): no wrong certification when N > k. Exact certification at N > 2k (k = 1 → N ≥ 3; k = 2 → N ≥ 5; k = 3 → N ≥ 7).
- **Supply chain:** 16.4% of npm packages (32.3% of PyPI) appear to have three witnesses; none do after collapsing the shared GitHub root, and about 90% have exactly two. The certifier certifies 0/450 malicious sources under registry compromise; a registry-trusting baseline accepts every one.
- **Extractor independence** (App. B): 150 episodes (N = 5, k = 1), six extractor configurations, 654 honest reads each. No honest read yielded the attacker value, and no two honest reads agreed on a wrong value, giving a bound of < 2% per configuration.
- **Per-source vs holistic gap** (App. B): GPT-5.5 follows the injection in isolation on every attacked episode, but the holistic agent proposes the attacker value in only 85% (agreement run) or 72% (threshold run). Holistic reading sometimes uses cross-source contradiction. This is the paper's only observation about *agent* behaviour toward conflicting evidence, and it is not used for gating.
- **Statistical caveat (authors', App. B):** "a reported zero is an observed count rather than a proof, bounding the rate below roughly 3/n"; "errors are correlated by template and by model family".

### 2.7 Agent decision behaviour, decision classes, revocation (question d)
- **What is measured:** whether an *action* is safe to execute given the corroboration structure of its evidence. The model is a component inside the trusted computing base (assumption 4), not the object of certification.
- **Agent behaviour measured:** only (1) the injection-following rate on single isolated reads and (2) naive holistic unsafe execution. Both are *outcome* rates under one attack type. Neither is used to grant anything.
- **No dependence-on-evidence measurement.** There is no removal, inversion or redundancy test of the *agent's* decision and no declared grounds. Corroboration is checked by the certifier, never asked of the agent.
- **No decision classes.** There is one operation type (pay invoice). The only typology is a **field typology by evidence structure**: identity, value, complementary, single-sourced. Conceptually this is the nearest thing to our "classes by requirements R_c", but it is per field, not per decision.
- **No revocation, no learned or earned autonomy, no history.** The certificate is computed per action at runtime from the observation alone and is "model-agnostic" in the sense that "the guarantee holds whether or not the model resists" (§5).
- **No escalation cost model.** ⊥ is scored as safe. Liveness is reported only as false abstention.
- **Adversarial threat model** (bounded corruption of control domains). There is no non-adversarial shift (stale, missing or redundant evidence), except that omission is one ablation family.

### 2.8 What it covers that WorkTrace must NOT claim
- Gating an autonomous **payment or counterparty action** on corroboration by **independent sources**, with **escalation to a human** otherwise. That idea, in our domain, is theirs.
- The formal definition of independence under corruption (dependency set, minimum-hitting-set count, domain-not-root vote identity, the unknown-provenance convention).
- The claim that apparent multi-source evidence collapses to fewer independent sources in real data (sanctions: about three-quarters single-domain).
- A theorem-backed optimality result for evidence-only gates (Thm 1: maximal liveness among k-safe certifiers).
- "Copy vs independent source" as a safety-relevant distinction for agent actions. Gao et al. and GraphEcho also cover it, for aggregation and graph agents (r3 note).

### 2.9 What it leaves open that WorkTrace addresses
- **Agent-level, per-class certification.** Whether *this agent configuration* may act unreviewed on *this decision class*, granted and revoked from data. Pandey certifies each action anew and never learns anything about the agent.
- **Decisions that are rule-governed functions of evidence** rather than corroborated field values: BO computation, the P6 exception route with suspicion and high-risk conditions, freshness and re-review, PEP consequences. Their certifier can only abstain on these.
- **The "sound extraction" assumption** (TCB 4). Whether the agent's reading of evidence is reliable is exactly an evidence-handling *behaviour*. WorkTrace measures its decision-level analogue (dependence on decisive evidence under interventions) instead of assuming it.
- **Non-adversarial evidence shift and staleness.** There is no time dimension. Stale but agreeing sources are certified.
- **Escalation as a cost.** WorkTrace's risk–coverage analysis and reviewer load put a price on ⊥.
- **Predictive validity.** Whether an evidence-behaviour measure predicts outcome errors on held-out episodes better than track records. Pandey runs no such test.

### 2.10 Draft differentiation sentences
- **Main (related work):** "Pandey et al. (2026) certify each structured agent action from the corroboration structure of its evidence: the model serves as a source-isolated extractor, and the action is executed only when corruption-distinct control domains pin down a unique value, otherwise it escalates to a human. WorkTrace instead certifies an agent configuration per decision class from its tested dependence on evidence, and targets decisions whose correct action is a rule-governed function of evidence (exceptions, temporal validity, computed ownership) rather than a corroborated field value."
- **On the TCB:** "Their guarantee is explicitly conditional on sound extraction, which they treat as a trusted-computing-base assumption; WorkTrace measures the decision-level counterpart of that assumption, whether the agent's choices track the decisive evidence, and uses it to allocate autonomy."
- **On scope (honest):** "Under bounded adversarial corruption of sources, Pandey et al.'s Theorem 1 implies that no procedure, including one based on agent behaviour, can safely act where their certifier abstains; WorkTrace addresses non-adversarial evidence shift and is complementary to, not a replacement for, such a gate."
- **On independence (methods section):** "Following Pandey et al. (2026, Defs 1–2, Prop. 3), we call a second source independent when its dependency set over control domains is disjoint from the first's, and count independent support as a minimum hitting set over authenticated control domains rather than over provenance roots."

### 2.11 Citation cautions
- **Do not write "tested on sanctions data".** Write "corroboration prevalence measured on sanctions designations (OpenSanctions)". The certifier experiments are on synthetic payment episodes.
- The **15%** figure (≥ 3 domains) is an **upper-bound proxy**. Domains are folded by dataset prefix, transpositions are not collapsed, and dependency sets are singletons in the code. The authors say so: "an upper bound on candidate multi-witness coverage, not evidence that 15% of payment actions obtain an exact-value radius".
- **The live-model certifier is not the full certifier** of §2. In the code it votes on all three fields, has no skeleton, reconciliation or anchor, has no enforced quorum among parsed extractions, and assumes each source is its own domain. Cite the live results as "corroboration voting over source-isolated extractions", and the anchor and reconciliation results as model-free.
- The live adversary is **property-based, not optimizing** (§8 limits); the optimizing attacker is model-free. Zeros are counts on 44–54 attacked episodes (≈ 3/n bounds), and errors are correlated by template.
- Prop. 2's "maximally live" applies to the **joint** certifier of Thm 1. The implemented field-wise version is only "a sound specialization whose liveness we measure rather than derive" (App. A).
- It is a 14-page PMLR conference paper whose proofs are short indistinguishability arguments. The reasoning is sound, but the venue is a national conference.
- The MIT licence names "Anonymous Author(s)". Keep that notice verbatim if we reuse code.
- Model names as given: Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro, Gemini 3.5 Flash, Claude Haiku 4.5 (via OpenRouter).

---

## 3. Pandey, Jain, Chen, Maple (2026), "Local Allow, Global Deny" — same group

### 3.1 Bibliographic data
- **Title:** Local Allow, Global Deny: Why Per-Action Authorization Does Not Compose in LLM Agents
- **Authors:** Anmol Pandey, Aditya Jain, Carsten Maple (University of Warwick); Liang Chen (University of Hertfordshire).
- **arXiv:** 2610.27620v1, 20 Oct 2026 [verified]. Categories cs.CR, cs.AI, cs.LO.
- **Venue:** "Extended version of a paper accepted at the 8th IEEE International Conference on Trust, Privacy and Security in Intelligent Systems and Applications (IEEE TPS 2026)" (arXiv comment). **[unverified in IEEE Xplore.]**
- **Artifact:** github.com/anmolpandey299/al-synth (not read).

### 3.2 Problem and contribution
- Per-action guards (each tool call screened in isolation) do not compose into global authorization.
- A **compositional authorization failure (CAF)** is a locally authorized trace, or *pair* of traces, that violates a global policy Φ = C1 (intent) ∧ C2^D (purpose) ∧ C3 (provenance) ∧ C4 (consent) ∧ C5 (delegation).
- **Purpose conjunct, Eq. (1):** two runs that agree on low inputs and on the purpose-authorized view D(hi) must agree on the policy-relevant disclosure α(obs).
- **Theorems:**
  - Thm 1: C2^D is 2-safety, and not trace-induced iff (D, α) is "residual-nondegenerate".
  - Thm 3 ("Set Locus"): "A per-trace monitor that never raises a false alarm for C2^D detects no violation of C2^D."
  - Thm 4 ("Distributional Locus"): for stochastic agents, no monitor seeing one execution's observable can soundly and completely decide Y ⊥ H | low, D(hi).
  - Thm 5: a relational (P7) monitor crosses the expressiveness barrier but "not the statistical one".

### 3.3 Method and evaluation
- **AL-SYNTH:** an SMT/SAT (Z3) bounded model checker. Relational witnesses are built by self-composition, validated against a brute-force oracle (soundness, bounded completeness, minimality; all 72 cells of the coverage matrix agree).
- **Monitor ladder P0–P7.** Six surveyed guardrails (Task Shield, RTBAS, CaMeL, Fides, SAFEFLOW, per-tool approval) are placed by design, not run. All miss the relational purpose class.
- **Nine LLM judges** (Opus 4.8, GPT-5.5, Gemini 3.1 Pro, Grok 4.3, DeepSeek V4 Pro, Qwen3.7-max, Llama-4-Maverick, Kimi-K2.6, Qwen3-30B):
  - Per action, they block the relational witness 0/30 (Kimi 3/30, at its benign-control level).
  - All block an overt C1 step 30/30.
  - Shown both executions, they detect it 30/30 (Llama 17/30).
- **Live agents** on the cumulative-consent calendar task:
  - Qwen3-30B commits a consent-composition CAF in 22/60 rollouts unguarded and 20/60 under an intent guard (Fisher p = 0.85).
  - A composition-aware (P5+) guard brings this to 0/60, with 0/60 false blocks.
  - Gemma-4 commits 0/60 throughout.
- **Offline audit of Claude Sonnet 4.6** (Table IV): 0 CAFs. One-sided Clopper–Pearson 95% upper bounds: ≤ 26% at n = 10 (C1, C4); ≤ 3.7% at n = 80 for the **paired** scheduling audit.
- **An instructive false positive (§VIII.C.a):** an initial "significant covert signal" came from "a feature extractor counting a word whose phrasing happened to differ". Their conclusion: "a result is a security result only under an abstraction that tracks the policy, with raw-data inspection as a check that no statistical rigor replaces."
- **Discussion:** "The model, not the monitor, carries the safety… deployments rely on an unverifiable, model-specific property that may not survive the next model."

### 3.4 Relevance to WorkTrace
- **Formal backing for W2/W3 (useful).**
  - "Right action on the wrong basis" can be cast as a C2^D-type relational property. Let D be the projection onto the *decisive* evidence, and α the policy-relevant action. A decision that changes when only non-decisive evidence changes violates it.
  - Their Thm 3 and Thm 4 then say that **no single-episode monitor**, whether an outcome check or an LLM trace judge, can detect such dependence soundly without false alarms. Detection needs paired or intervened executions and is statistical.
  - This is the cleanest available **theoretical argument** for why B-OO, B-trace-judge and B-READY-proc should under-detect basis errors. It also supports reporting interventions as *statistical* certificates.
  - **Caution:** the mapping is ours, not theirs. Their D is a declassification (authorized) view and their α a disclosure. State the mapping explicitly and claim only the analogy plus the general indistinguishability argument.
  - The other direction of a basis error, *insensitivity* to decisive evidence, is also a relational property, but it is not their C2^D.
- **What they cover that WorkTrace must NOT claim:**
  - that dependence on unauthorized context is relational, is invisible per trace, and needs paired executions;
  - paired-world construction that holds the authorized view fixed (an intervention on hidden context);
  - an offline paired audit of a frontier model with a Clopper–Pearson bound.
- **What they leave open:** decision-evidence dependence (as opposed to disclosure purpose); multi-condition interventions (remove / only / invert / add independent source); declared grounds; per-class delegation, revocation, matched-coverage comparison.
- **Draft differentiation:** "Pandey et al. (2026b) prove that a purpose violation—disclosure depending on context the purpose does not authorize—is a 2-safety hyperproperty invisible to any false-alarm-free per-action monitor; we exploit the same observation for agent *decisions*, using evidence interventions as the paired executions, and turn the resulting statistical audit into a per-class, revocable delegation rule."
- **Citation cautions:** IEEE TPS acceptance is unverified. The guardrail matrix is "design-derived", not executed. The agent experiments cover two open model families plus one hosted model audited offline. The judge campaign used OpenRouter default routing, with no pinned provider.

---

## 4. Implications for WorkTrace

### 4.1 Question (e): what our pilot must do differently, and how B-Pandey fits W3

**Differences the pilot must keep, and state:**
1. **Object of certification.** WorkTrace certifies *(agent configuration × decision class)* ahead of time from intervention tests and revokes on data. B-Pandey certifies *each action at runtime* from evidence structure and is agnostic to the agent. Say this in one sentence in the method section.
2. **The agent is not just an extractor.** Our episodes are multi-step. The agent chooses which sources to query, requests documents, and decides routes (P6), so evidence acquisition and escalation are part of DSA. B-Pandey must be given **its own source-isolated extraction calls**, using the same model and configuration. Charge their cost of N + 1 calls per episode in any cost table.
3. **Two threat regimes, reported separately.**
   - (a) **Non-adversarial evidence shift**, WorkTrace's home ground: removal, inversion, an independent second source, staleness, copies.
   - (b) **An adversarial arm** (one corrupted control domain with an embedded injection, k = 1), B-Pandey's home ground.
   - Pre-register that in (b) WorkTrace is *not expected* to beat B-Pandey on safe coverage (Thm 1), and that the composed rule **WorkTrace ∧ B-Pandey** is the recommended configuration.
4. **Generator must label control domains with true dependency sets.**
   - Label for each attestation: domain, root, D. Include transposition (national list D = {NAT, EU}), a shared upstream (customer-supplied document and customer-influenced website → one domain), an unknown-provenance class (shared UNKNOWN domain), and **one domain emitting several distinct originals** (Prop. 3 case).
   - Provide two label sets: ORACLE and APPARENT.
5. **Independence definition (design change).** Replace "distinct provenance **or** control domain" (`positioning.md` §3) with **"disjoint dependency sets over authenticated control domains; support counted as a minimum hitting set over domains, not roots"**. The copy-of-X control stays. Add a **"same domain, new original"** control: the same control domain issues a second, distinct original record for the same fact. The correct response is no corroboration credit. This is the case root-counting gets wrong (Table 5).
6. **Sanctions (P9) stays synthetic.** Do not ingest OpenSanctions entities: our policy forbids real lists and names, and the data are CC BY-NC 4.0. Use Pandey's Table 2 control-domain marginals (74.6 / 25.4 / 14.9 / 11.7%) to parametrise synthetic designations, and add explicit transposition dependency sets so that true m < apparent m̂. Cite the source of the parameters.
7. **Escalation cost.** B-Pandey scores ⊥ as safe. In W3 every rule is charged the same escalation cost and reviewer load, so B-Pandey's coverage loss is visible.
8. **Pre-registered B-Pandey failure modes** (where W3 can discriminate). Make sure the generator produces each:
   - (i) **stale but agreeing** sources: an outdated register plus an equally old customer document, both honest, both distinct domains;
   - (ii) **common-mode extraction error**: the same misreading across sources from the same model, e.g. a transliterated name or a legal-form suffix;
   - (iii) **mislabelled independence** under APPARENT labels: a transposed list counted as a second domain;
   - (iv) **decisions that are not field values** (P4/P5/P6/P8/P10/P14);
   - (v) **partial-match names**, which trigger ⊥ and cost coverage.
9. **Open-textured predicates (design change).** In a fully formal synthetic policy, B-Pandey-R (certified inputs plus a deterministic rule engine) would trivially dominate any agent. A reviewer would then ask why an agent is needed at all. Ensure that some decisive predicates are **open-textured and carried by narrative evidence**: P6 "grounds for suspicion", P8 "legitimate legal or economic reason", P11 activity consistency from free text. B-Pandey-R must escalate on these. Report what share of episodes in each class depends on such predicates.

**Where B-Pandey applies, per decision class** (classes from `r2_governance_context.md` §B.3; (vi) proposed here):

| Class | B-Pandey-F (faithful) | B-Pandey-R (+ deterministic rules) | Expectation vs WorkTrace |
|---|---|---|---|
| (i) Identification evidence: completeness and consistency, P1–P3 | **Fully applicable.** Name, registration number, office: AGREE / THRESHOLD over register, government document, LEI record and customer document (customer-influenced sources share a domain). Registration validity: ANCHOR (register). P3 freshness: only in the +T variant. | Same | **Strong competitor.** Expect a tie on non-stale episodes. WorkTrace can win only on stale corroboration (F) and on common-mode extraction errors. |
| (ii) BO computation from the ownership graph, P4–P5 | Certifies individual ownership edges and percentages (THRESHOLD/AGREE). The BO set itself → ⊥. Control via side agreements is single-sourced → ⊥. | Computes the BO set from certified edges (multiply along chains, sum across chains). Control-without-ownership remains ⊥. | B-Pandey-F coverage is near zero. B-Pandey-R is strong where edges are corroborated, but most edges in realistic structures are single-sourced (cf. 75% single-domain), so ⊥. |
| (iii) Discrepancy triage, P6 | A discrepancy *is* a disagreement → ⊥ under AGREE. Under THRESHOLD a majority value may be certified, but the **route** (report within 14 days vs request from customer) is not a field. | The route predicate needs "no grounds for suspicion" (open-textured) → ⊥. Typo and outdated-data conditions are partly computable. | **WorkTrace's clearest advantage.** This is also our flagship intervention (add or remove the independent second source). B-Pandey's coverage here should be near zero. |
| (iv) Request-additional-document actions, P11–P12 | **Directly applicable.** ⊥ on the sufficiency check ⇒ "request document". P12 is itself a quorum rule. | Same | **B-Pandey with ORACLE labels is close to the policy-optimal rule. Expect a tie or loss**, and pre-register it. WorkTrace can win only under APPARENT labels or extraction faults. |
| (v) Freshness and re-review triggers, P14 | **Not applicable** (no time) → ⊥, or it certifies stale values if forced. | +T variant only | WorkTrace advantage, but only against F. |
| (vi) **Sanctions-screening clearance**, P9 (proposed new delegable class; P9 is not in the §B.3 list) | Part B2: any hit or partial match → ⊥. Clearance requires the binding-list anchor. The > 50% aggregate stake test is a computed predicate → ⊥ in F. | Computes the aggregate stake from certified edges | Competitive on direct hits. Weak on indirect ownership. Note that clearance can never be certified by corroboration for single-domain designations (their Def. 2). |
| Reserved (P15: onboard/refuse/maintain, risk tier, EDD, STR) | Not applicable: always escalate | Not applicable | Excluded from risk–coverage curves for every rule |

**Integrating B-Pandey into the W3 engine.** `positioning.md` says "the same certification engine for all". B-Pandey does not fit that engine as is, because it is a *runtime gate*, not a class-level grant.
- **Primary:** run B-Pandey as a runtime rule (an episode is autonomous iff B-Pandey proceeds). Its coverage per class is the share of the class's held-out episodes it executes.
- **Matched coverage:** B-Pandey offers only discrete operating points (mode ∈ {AGREE, THRESHOLD} × k ∈ {0, 1, 2} × q_min × {F, +T} × {ORACLE, APPARENT}). Read WorkTrace's risk at B-Pandey's coverage points from WorkTrace's continuous risk–coverage curve, and also report B-Pandey's risk at WorkTrace's α-certified coverage.
- **Secondary:** a class-level wrapper, granting class c to B-Pandey if its calibration-set unsafe rate is ≤ α_c (Clopper–Pearson). Expect it to be granted nearly everywhere, since unsafe executions are near 0 by construction; it adds little.
- **Composition arm:** WorkTrace ∧ B-Pandey. The agent acts autonomously only in DSA-certified classes **and** when the runtime corroboration gate passes. This shows complementarity and is the honest recommendation for the adversarial arm.
- **Endpoint comparability.** W3's primary endpoint (outcome errors of autonomous decisions on held-out shifted episodes) applies to B-Pandey unchanged. The "unjustified action" loss does not transfer cleanly, because B-Pandey's "basis" is the certifier's vote, not the agent's. Report B-Pandey on outcome errors plus escalation rate only.

### 4.2 Question (f): threat level and differentiation

| Claim | Threat | Why | Required wording or change |
|---|---|---|---|
| **W1: DSA construct** | **Low** | No construct and no measurement of the agent beyond the injection-following rate. The field typology by evidence structure resembles class requirements, but it is per field. | Cite as a system that *assumes* sound extraction (TCB 4) rather than measuring evidence-handling. Cite "Local Allow, Global Deny" Thm 3 and Thm 4 as formal support that dependence on evidence is relational and needs paired, intervened episodes. |
| **W2: DSA-based delegation rule** | **Medium** | Same domain; "corroboration gates autonomous action, otherwise a human". Thm 1 is an optimality result for evidence-only gates under adversarial corruption, and it also bounds what any agent-based rule can safely do there. A reviewer will ask "why certify the agent if you can certify the action?" | (1) Scope W2 to non-adversarial evidence shift and to rule-governed decisions; say explicitly that it is complementary to a Pandey-style gate, and recommend composition under adversarial threat. (2) Adopt their independence definition (§4.1 item 5). (3) Do not claim "independent source" as a novel concept. Our novelty is the *joint* intervention battery scored against declared grounds and its per-class use. |
| **W3: predictive-validity test** | **Medium to high (empirical), low (novelty)** | Not a novelty threat: they run no held-out predictive comparison of rules at matched coverage and do not measure agents. Empirically, B-Pandey may tie or beat WorkTrace in classes (i) and (iv) and in the adversarial arm. | Pre-register per-class expectations (table in §4.1). Make the main H3 claim class-conditional, e.g. "in classes whose correct action is a rule-governed function of evidence". Ensure open-textured predicates exist. Report APPARENT vs ORACLE domain labels. |

**Differentiation sentences:** see §2.10 (Pandey 2026a) and §3.4 (Pandey 2026b).

### 4.3 Other design lessons
- **Unknown provenance → one shared UNKNOWN domain** (App. B). Adopt this in the generator's ground truth for "independent second source". An unknown-provenance "second source" must *not* count as corroboration, so the correct agent response is no change or escalation.
- **Canonicalization must fold scripts and transliteration** in names (their App. B gap). Our synthetic legal-entity names should deliberately include transliteration and legal-form variants (e.g. "GmbH" vs "Gesellschaft mit beschränkter Haftung") as a *partial-match* family. Under B-Pandey these cost coverage; in WorkTrace they test whether the agent recognises the same entity.
- **Their per-source vs holistic gap** (GPT-5.5: 100% follows the injection in isolation, 72–85% holistically) is a small natural experiment on the *agent's* use of conflicting evidence. Cite it as a hint that holistic agents partly do corroborate. DSA measures that systematically.
- **"Local Allow, Global Deny" §VIII.C.a lesson:** a statistically significant signal was a feature-extractor artifact. Score intervention responses under the policy-relevant abstraction (the action and its legally relevant arguments), not surface text, and keep raw-output inspection in the audit protocol. This matches our CSS-style validity audit (r3 §7.2.3).
- **Reuse:** `corruption_distinct.py` (MIT) for exact minimum hitting set, with the forced-singleton pass and exact solve for ≤ 22 domains. **Never use the greedy fallback for certification**, because it overstates m (App. B).

### 4.4 Things to cite
- Pandey, Jain, Chen, Maple, Panchev (2026a), PMLR 348:134–147, arXiv:2609.34245:
  - Defs 1–2 (independence), Prop. 3 / Table 5 (count domains, not roots), Thm 1 (escalation is necessary when feasibility is not a singleton);
  - TCB assumption 4 (sound extraction);
  - Table 2 (sanctions domain marginals, as an upper bound);
  - Fig. 2 (apparent witnesses collapse).
- Pandey, Jain, Chen, Maple (2026b), arXiv:2610.27620 (IEEE TPS 2026 per the authors): Thm 3 and Thm 4 (per-trace blindness to relational dependence), Corollary 1 (compare executions or accept false alarms), the Table IV offline paired audit as a precedent.
- OpenSanctions "Consolidated Sanctions" dataset: cite only via Pandey's Table 2. Do not redistribute (CC BY-NC 4.0).

### 4.5 Edits to propose to `positioning.md` (not made; outside this note's remit)
- §2 W3, B-Pandey line: replace "certyfikator wielodomenowy w domenie sankcji" with "a multi-domain corroboration certifier for agent payment actions (corroboration prevalence measured on sanctions data); a runtime gate, not a class grant; variants F/R/+T × ORACLE/APPARENT; mandatory for classes (i), (iv), (vi) and the adversarial arm".
- §3, the "Niezależne" (independent) definition: switch to disjoint dependency sets over control domains, counted by minimum hitting set (Pandey Defs 1–2, Prop. 3).
- §6 Risks: add "Thm 1 (Pandey): under adversarial corruption no agent-based rule safely exceeds evidence-only coverage; scope W2/W3 to non-adversarial shift, and offer the composition".
- §7: add Pandey et al. 2610.27620 (relational dependence; per-trace blindness) to the reading for the DSA and W3 sections.
