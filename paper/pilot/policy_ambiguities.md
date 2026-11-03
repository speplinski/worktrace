# Policy ambiguities found during the pilot

Log of places where the synthetic policy (R1–R5, `worktrace/policy.py`) can be read in more than one way. The policy
text is frozen for the pilot (pre-registration §8); entries here are for the phase-2 revision and for reporting.

| # | Found | By | Rule | Ambiguity | How the generator and oracles read it | Affects the pilot? |
|---|---|---|---|---|---|---|
| 1 | 2026-10-26 | audit (A1); author's review (E22, E23) | R3, R5 | Whether a file must contain a register excerpt at all, i.e. whether a missing excerpt is missing evidence. If it is, R5 admits two actions (request or escalate), not one. Legal check (iv): no text requires an excerpt in the file of an existing customer | missing excerpt → request a fresh one | yes: contested c5 `remove_X` arms (A1). Author: both readings defensible; the oracle's single answer is incomplete under either (A13) |
| 2 | 2026-10-26 | audit (A1) | R2 | Inverted notarial deed contradicting the excerpt: escalate or report | escalate / request document | yes: contested c3 `invert_X` arms (A1). Author's blind answers in both reviewed cases (E10, E28) equal the oracle's: evidence against the A1 premise |
| 3 | 2026-10-29 | author (expert review template) | R1 | "The institution's own records" (tier 1): the bank's own records, or also a supervisor's? | the bank's internal records only (risk record, CDD review, screening, checklist); no supervisor exists in the world | no |
| 4 | 2026-10-29 | author | R1 | "Regulated professionals" (tier 2) is not defined | only notaries occur. A data vendor is coded tier 2 internally, but R1 makes an aggregation inherit the register as issuer; the oracles treat tiers 1 and 2 alike and the vendor as not independent of the register, so answers do not depend on this | no |
| 5 | 2026-10-29 | author | R1 | A tier 1/2 document supplied by the customer: tier 3 ("anything supplied by the customer") or the original's tier ("a copy inherits the issuer")? The two sentences conflict | never occurs: customers supply only self-declarations, e-mails and cover letters; copies come only from the data vendor | no (text ambiguous) |
| 6 | 2026-10-29 | author (review E05) | R4, R5 | "Request the missing document": from the customer only, or also from within the institution (e.g. a missing internal screening result)? | `request_document` is an action with no addressee | no (wording) |
| 7 | 2026-10-29 | author (review E02) | R1, R2(b) | Independence "by controlling authority" cannot be established from the documents, which name issuers but never their controlling authorities; differing jurisdictions are not proof. Legal check (i): AMLR Art. 24(2)(b) requires only "another reliable source" | the oracles decide it from a field the agents do not see (`Authority.controller`): court and notary independent of the registers, the data vendor not | yes: every c3 episode where A* rests on exception (b); A13: report only, withdrawn by the author on 2026-10-30 after his blind answer to E14 (same structure) in the oracles' sense (a register and a court are taken as independent); the reviewed key keeps the oracles' reading |
| 8 | 2026-10-29 | author (review E03) | R3 | Which filings count as a "change": the feed lists every entry under "change", annual accounts included. Legal check (iii): Art. 26(3) speaks of "relevant circumstances" | an "Annual accounts filed" entry is not a change (the shifted-split decoy) | yes: shifted c5 episodes with such an entry after the last review; A13: both readings |
| 9 | 2026-10-29 | model-written counterpoint supplied by the author (E02); not adopted | R2 | "Instead of reporting, you may request…": a permitted alternative, or the required action when the exception applies? Legal check (ii): Art. 24(2) is a permission ("may refrain … may instead") | when the exception applies, only `request_customer_correction` | possibly: c3 typo cases (exception (a)); not part of A13; changes no H3 number in the exploratory check |
| 10 | 2026-10-26 | LLM judge trial (A3) | R3 | Whether the review-interval obligations of R3 bind a register-discrepancy (c3) decision | no: in c3, R3 does not decide the action and reopening is not a permitted action | yes: judge-v1 failed 11 of 13 trial decisions on this ground; judge-v2 states the task scope (A3) |
| 11 | 2026-10-26 | LLM judge (interim observation 2) | R4 | Whether the "current register excerpt" of R4 is a business-register excerpt or an excerpt of the beneficial-ownership register | business register (generator, oracles and agents) | yes: the judge mostly reads it as the beneficial-ownership register; in about two thirds of the cells where DSA beats a judge-based rule, the difference is that DSA delegates c6 (§6.1) |
| 12 | 2026-10-30 | author (review E16) | R3, R5 | When several actions are admissible (e.g. reopen a file that is overdue for review, request a fresh excerpt that is missing, or escalate), the policy gives no order of precedence; the author reads this as a flow question (data first, then the review, escalation in doubt) that the text leaves open | A* is a set: any admissible action scores as correct, so no order is needed for scoring | no (scoring); yes for a deployed agent, which must pick one |

## Check against the public texts the policy paraphrases (2026-10-29)

Done after the author's review (A13), at his request, from the full texts (FATF paragraph numbers INR.10 ¶23 and INR.24 ¶9 re-checked by the author in the June 2026 PDF on 2026-10-31): the FATF Recommendations with interpretive
notes (version updated June 2026, supplied by the author), EBA/GL/2021/02 (final report of 1 March 2021, downloaded from
eba.europa.eu) and Regulation (EU) 2024/1624 (AMLR; OJ L of 19 June 2024, supplied by the author). The question was
whether any disputed reading is settled by these texts rather than by the policy. Quotations are verbatim. This is a
reading of the texts for the purpose of the pilot, not legal advice, and the pilot makes no claim of compliance.

**(i) Source independence in exception R2(b) (entry 7; E02).** The texts require reliability, and for identity
verification independence from the customer; none defines independence between two sources, and none makes the
discrepancy derogation depend on it.

- FATF R.10(a): verification "using reliable, independent source documents, data or information"; R.10(b):
  "reasonable measures to verify the identity of the beneficial owner, such that the financial institution is
  satisfied that it knows who the beneficial owner is". INR.24 §9: accurate beneficial-ownership information is
  verified "using reliable, independently sourced/obtained documents, data or information", and "Countries should
  consider complementary measures as necessary to support the accuracy of beneficial ownership information, e.g.
  discrepancy reporting."
- EBA GL 4.26: verify "on the basis of reliable and independent information and data". 4.27: "Firms should set out
  in their policies and procedures which information and data they will treat as reliable and independent"; degrees
  of independence depend on whether the issuer "is linked to the customer through direct personal, professional or
  family ties" or "could have been unduly influenced by the customer". So the EBA's independence is independence from
  the customer, not from another source. 4.13: using the beneficial-ownership register "does not, in itself, fulfil"
  the duty to verify.
- AMLR Art. 22(6)(a): "information from reliable and independent sources, whether accessed directly or provided by
  the customer"; Art. 22(7)(b): beneficial owners verified "from the customer or other reliable sources, including
  public registers other than the central registers"; Art. 28(1)(d): AMLA is to specify "the reliable and independent
  sources of information that may be used to verify the identification data" in technical standards (due 10 July
  2026). Art. 24(2)(b): the derogation applies where the discrepancies "are a result of outdated data, but the
  beneficial owners are known to the obliged entity from another reliable source and there are no grounds for
  suspicion that there is an intention to conceal any information".
- Finding: R1's test of independence ("issuers do not answer to the same controlling authority") and R2(b)'s
  condition that the other source be independent of the register's controlling authority are the policy's own.
  AMLR Art. 24(2)(b) requires "another reliable source" and nothing more. The dispute in E02 was therefore about a
  condition the legal text does not contain. The texts do not say how the policy's own condition should be read.

**(ii) "Instead of reporting, you may request …" (entry 9).** AMLR Art. 24(1): discrepancies "shall be reported
without undue delay and, in any case, within 14 calendar days". Art. 24(2): "By way of derogation from paragraph 1,
obliged entities may refrain from reporting discrepancies to the central register and may instead request additional
information from the customers"; second subparagraph: "Where an obliged entity concludes that the beneficial
ownership information in the central register is incorrect, it shall invite the customer to submit the correct
information to the central register … within 14 calendar days"; third subparagraph: "This paragraph shall not apply
to cases of higher risk". Art. 24(3): if the customer has not corrected the entry in time, the entity "shall report
the discrepancy". Recital 54: "it should be possible for obliged entities to allow the customer to report
discrepancies". Finding: the derogation is a permission, so reporting remains admissible when it applies; once an
entity uses it, inviting the customer is the required step and reporting follows if the customer fails. In E02 the
derogation would be available on the text (register outdated, court record names the current owners, no alert,
standard risk), so both actions would be admissible: the oracles' single answer (correction) and the author's first verdict (report,
withdrawn on 2026-10-30) are both narrower than the text. The policy's R2 uses the same word ("may"), so the reading in
entry 9 is the one closest to the text. In the exploratory check (reporting admitted in that entry's case) it changes no H3 number; reporting
admissible wherever the derogation applies has not been varied as a dimension of the multiverse.

**(iii) Filing of annual accounts as a "change" (entry 8; E03).** FATF INR.10 §23: CDD information "kept up-to-date
and relevant by undertaking reviews of existing records, particularly for higher-risk categories of customers";
INR.10 §13: existing customers "on the basis of materiality and risk". EBA GL 4.76: "Firms must keep CDD information
up to date"; 4.77 lists as examples "an apparent change in the source of the customer's funds, the customer's
ownership structure, or behaviour that is consistently out of line"; 4.78: "A change in the customer's circumstances
is likely to trigger a requirement to apply CDD measures". AMLR Art. 26(2): the period between updates "shall not in
any case exceed: (a) for higher risk customers …, 1 year; (b) for all other customers, 5 years" (R3's intervals);
Art. 26(3): review "where (a) there is a change in the relevant circumstances of a customer; … (c) they become aware
of a relevant fact which pertains to the customer"; recital 69: "material changes, such as a change in the
jurisdictions transacted with, in the value or volume of transactions, upon requests for new products or services
that are significantly different in terms of risk, or following changes in beneficial ownership". Finding: the texts
tie re-review to relevant or material changes and list none that resembles the filing of annual accounts. R3's "any
change recorded in an official filing" is stricter than the texts; the oracles' reading (not a change) is the closer
one, the literal reading of R3 the stricter. Not settled; both defensible under R3.

**(iv) A register excerpt in the file, and its age (entry 1; E22, E23).** AMLR Art. 23(4): "Whenever entering into a
new business relationship with a legal entity …, obliged entities shall collect valid proof of registration or a
recently issued excerpt of the register confirming validity of registration" (new relationships only; no number of
days). Art. 26(2): for existing customers "the relevant documents, data or information of the customer are kept up
to date" within the intervals above. FATF INR.10 §5(a)(i): proof of existence "could be obtained, for example,
through a certificate of incorporation, a certificate of good standing, … or other documentation from a reliable
independent source". The EBA guidelines say nothing about the age of a document. Finding: no text requires an
excerpt in the file of an existing customer or sets its maximum age. The 30-day window is a synthetic parameter
(§5.2); whether a file must hold an excerpt is the institution's choice. The oracles required one; the texts do not.

**(v) Reserved decisions (R4, c6).** AMLR Art. 76(5): decisions taken by "automated processes … or from processes
involving AI systems" are permitted provided that "(b) any decision to enter or refuse to enter into or maintain a
business relationship with a customer …, or to increase or decrease the extent of the customer due diligence
measures …, is subject to meaningful human intervention to ensure the accuracy and appropriateness of such a
decision; and (c) the customer may obtain an explanation of the decision reached by the obliged entity, and may
challenge that decision". Finding: R4 follows the text. Entry 11 (which register R4's "current register excerpt"
means) is not touched by it.

**Summary.** None of the disputed readings of the policy is settled by FATF or the EBA guidelines, which leave the
choices to the institution. The AMLR is more specific, and against it the policy is stricter in two places that the
review found contested: the independence condition in R2(b) (i) and "any change" in R3 (iii); in a third (ii) the
oracles turned a permission into a single required answer. Among the 60 keys of the exploratory multiverse
(`multiverse/multiverse.md`), the one closest to the texts (exception (b) available on another reliable source,
annual accounts not a change, no excerpt required in the file) is row 3 with the inverted deed scored as the oracles do and row 4
with reporting also admitted for the deed (entry 2), a reading this legal check does not settle: on the final data (14 configurations),
common core, row 3 gives DSA lower in 3 of 9 differing cells and higher in 4 (β_DSA = −0.01, one-sided p = 0.48; all data 3 : 4 of 8,
−0.00, 0.48) and row 4 gives 4 : 3 of 7 (−0.09, 0.19; all data 4 : 3 of 7, −0.08, 0.20). The "may" reading of (ii) (entry 9) changes
no number. Ten of the 60 keys give a nominal one-sided p < 0.05 in the common core (eleven on all data), without correction for
multiplicity: seven treat a missing excerpt as missing evidence and the other three count annual accounts as a change with reporting
admitted for the deed (rows 14, 18, 20; the literal-policy key, p = 0.011 on 7 cells). All 60 keys differ in at least one admissible set, and all keep the policy's condition that the other source be independent of the register's
controlling authority (independence = shown decides it from the hidden controller field; = not shown never applies the exception); none implements the
AMLR wording ("another reliable source"). Added 2026-11-03 after a review: a third independence reading, any reliable source, without the controller
condition (rows 61–90; `worktrace/answer_key.py`, `controller_required=False`): it changes the admissible set of 1,162 of 34,580 core records and
1,491 of 45,001 on all data; under none of the 30 keys does DSA reach p < 0.05 (deed as the oracles: p 0.13–0.99 core, 0.15–0.96 all data; reporting
admitted: 0.25–1.00, 0.27–0.99). Row 63 (any reliable source, not a change, optional, oracle), the key that drops the controller condition and takes the lenient reading on the other
three dimensions, gives 4 : 0 : 1 (β −0.09, p 0.14; all data 4 : 0 : 0, −0.08, 0.16). All 30 variants keep the oracles' single-action convention
where the exception applies; "also report" concerns only the contested inverted deed. For phase 2 the policy text is to be aligned with the legal texts before any test is run.
