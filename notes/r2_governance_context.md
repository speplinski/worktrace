# R2 — Governance and regulatory anchor for bounded delegation and the counterparty-verification case study

Prepared 25 October 2026. All dates below were checked against primary texts on that day unless marked otherwise.
Scope: EU AI Act (as amended by the Digital Omnibus on AI), NIST AI RMF 1.0 and NIST AI 600-1, ISO/IEC 42001, EU AML package (AMLR, AMLD6, AMLD4 currently in force), FATF Recommendations, EBA ML/TF Risk Factors Guidelines, and 2025–2026 supervisory statements on AI agents (FSB, FCA, ECB, BIS, Fed, EBA).

**Not legal advice.** This note is an anchor for a research paper. Section C lists what we must not claim.

---

## 0. Headline findings (read first)

1. **Novelty pressure from policy, not from papers.** The FSB final report *Sound Practices for Responsible Adoption of AI* (15 Oct 2026, §3.7, PDF pp. 56–59) already recommends:
   - progressively widening an agent's access "as they gain confidence it can do so safely";
   - "triggers for transitioning between different forms of human oversight based on performance metrics";
   - testing whether agents "escalate to humans, stop safely";
   - cross-checking agents' self-reported reasoning "with other sources to mitigate the risk of deception".

   So the *idea* of earned, graduated, revocable autonomy is now mainstream supervisory language. WorkTrace must not claim the idea. Its claim is the **operationalisation**: per decision class, tested evidence-handling behaviour, interventions on external evidence, and held-out risk–coverage evaluation against an outcome-only rule. The FSB describes none of these, and it is non-binding.
2. **The AI Act timeline has moved.** Regulation (EU) 2026/1744 (Digital Omnibus on AI; signed 8 Jul 2026, OJ 24 Jul 2026, in force 27 Jul 2026) moves Chapter III Sections 1–3, which contain Arts 9–15 and 26, from 2 Aug 2026 to **2 Dec 2027** for Annex III systems and **2 Aug 2028** for Annex I systems. Arts 12, 13, 14 and 26 themselves were **not amended**.
3. **Corporate counterparty verification (KYC/AML) is not an Annex III high-risk use case** under the text as enacted (see §A.4). The stronger legal anchor for our case study is **AMLR Art. 76(5)** (Regulation (EU) 2024/1624, applicable from 10 Jul 2027). It allows decisions "resulting from … processes involving AI systems" only if decisions to enter, refuse or maintain a business relationship, or to increase or decrease CDD measures, are "subject to meaningful human intervention". With **AMLR Art. 18(3)(c)–(f)** (non-outsourceable decisions), this fixes a set of decision classes whose WorkTrace verdict must always be **escalate**. This is a design constraint and also a useful realism feature (§B.3).
4. **AMLR Art. 24(2)(b) is a ready-made, legally grounded "add an independent second source" intervention.** An outdated register entry may be handled by requesting information instead of reporting, but only if "the beneficial owners are known to the obliged entity from another reliable source" and there are no grounds for suspicion. This is ground truth by construction (§B.2, rule P6).

---

## Sources read (bibliographic cards)

Format per brief: bibliographic data; what it is; what it covers that WorkTrace must NOT claim; what it leaves open; draft differentiation; citation cautions. For legal texts, "Method/Evaluation" is replaced by "Relevant provisions".

### S1. EU AI Act — Regulation (EU) 2024/1689 [verified]
- **Bibliographic data.** Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence … (Artificial Intelligence Act). OJ L, 2024/1689, 12.7.2024. ELI: http://data.europa.eu/eli/reg/2024/1689/oj. CELEX 32024R1689.
- **What I read.** Full OJ English text, obtained from the Publications Office Cellar (EUR-Lex HTML returned a bot challenge). I searched the whole text and read Arts 3, 6, 9, 12, 13, 14, 15, 26, 27, 86 and 113, Annex III, and recitals 12, 53, 58, 59, 71, 73 in full.
- **Relevant provisions (quoted).**
  - **Art. 12(1):** "High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system."
  - **Art. 12(2):** logging must enable recording of events relevant for "(a) identifying situations that may result in the high-risk AI system presenting a risk … or in a substantial modification; (b) facilitating the post-market monitoring …; and (c) monitoring the operation of high-risk AI systems referred to in Article 26(5)."
  - **Art. 13(1):** "…sufficiently transparent to enable deployers to interpret a system's output and use it appropriately." Art. 13(3)(b) requires the instructions for use to cover "characteristics, capabilities and limitations of performance". This includes (i) intended purpose, (ii) accuracy metrics "against which the high-risk AI system has been tested and validated", and (iv) "technical capabilities … to provide information that is relevant to explain its output". Art. 13(3)(d) adds "the human oversight measures referred to in Article 14".
  - **Art. 14(3):** "The oversight measures shall be commensurate with the risks, level of autonomy and context of use of the high-risk AI system…"
  - **Art. 14(4):** natural persons assigned oversight must be enabled, "as appropriate and proportionate":
    - "(a) to properly understand the relevant capacities and limitations … and be able to duly monitor its operation, including in view of detecting and addressing anomalies, dysfunctions and unexpected performance;
    - (b) to remain aware of the possible tendency of automatically relying or over-relying on the output … (automation bias) …;
    - (c) to correctly interpret the high-risk AI system's output …;
    - (d) to decide, in any particular situation, not to use the high-risk AI system or to otherwise disregard, override or reverse the output …;
    - (e) to intervene in the operation … or interrupt the system through a 'stop' button or a similar procedure that allows the system to come to a halt in a safe state."
  - **Recital 73:** oversight measures should "guarantee that the system is subject to in-built operational constraints that cannot be overridden by the system itself and is responsive to the human operator". They should also include "mechanisms to guide and inform a natural person … to make informed decisions if, when and how to intervene".
  - **Art. 9(8):** testing "shall be carried out against prior defined metrics and probabilistic thresholds that are appropriate to the intended purpose of the high-risk AI system."
  - **Art. 26(1), (2):** deployers must use systems in accordance with the instructions for use, and "shall assign human oversight to natural persons who have the necessary competence, training and authority, as well as the necessary support."
  - **Art. 26(5):** deployers monitor operation and, where there is reason to consider a risk, "shall suspend the use of that system". For financial institutions, the monitoring obligation "shall be deemed to be fulfilled by complying with the rules on internal governance arrangements … pursuant to the relevant financial service law".
  - **Art. 26(6):** deployers keep logs under their control for "at least six months". Financial institutions keep them "as part of the documentation kept pursuant to the relevant Union financial service law".
  - **Art. 86(1):** right to "clear and meaningful explanations of the role of the AI system in the decision-making procedure", for decisions based on Annex III high-risk output.
  - **Recital 12:** "AI systems are designed to operate with varying levels of autonomy, meaning that they have some degree of independence of actions from human involvement…"
- **Covers (do not claim).** The obligations that overseers can understand limits, detect anomalies, resist automation bias, override, and halt. Logging for traceability. Pre-defined testing thresholds.
- **Leaves open.** The Act never says *how* to decide which decisions an AI may take without a human, nor how to make that decision depend on tested behaviour. The words "agent", "delegation" and "autonomy level" (as a graded scheme) do not appear in the operative text. Grep of the full OJ text found 0 occurrences of "agent*". After the Omnibus, the only occurrence is "Agentic AI" as notified-body code AIH 0401 in new Annex XIV.
- **Draft differentiation.** "The AI Act requires that oversight be commensurate with a system's level of autonomy (Art. 14(3)) and that overseers can detect anomalies, avoid automation bias and override or halt the system (Art. 14(4)). It does not specify how a level of autonomy should be set or withdrawn. WorkTrace proposes one evidence-based procedure for doing so."
- **Citation cautions.** Cite article and paragraph, not commentary. Art. 14 obligations attach to the *design* of high-risk systems (provider) and to *assignment of overseers* (deployer, Art. 26(2)). They are not a rule about agent autonomy.

### S2. Digital Omnibus on AI — Regulation (EU) 2026/1744 [verified]
- **Bibliographic data.** Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus on AI). OJ L, 2026/1744, 24.7.2026. CELEX 32026R1744. It enters into force on the third day after publication, i.e. 27 Jul 2026 (by computation; consistent with secondary sources).
- **What I read.** Full OJ English text via Cellar. I read every amending point heading, and in full the amendments to Arts 4, 5, 6, 10, 27, 111 and 113, and new Annex XIV.
- **Relevant changes (verbatim where quoted).**
  - **Art. 113 third paragraph, point (c), replaced:** "Chapter III, Sections 1, 2, and 3, with the exception of Article 6(5), shall apply from: (i) 2 December 2027 as regards AI systems classified as high-risk pursuant to Article 6(2) and Annex III; and (ii) 2 August 2028 as regards AI systems classified as high-risk pursuant to Article 6(1) and Annex I". New point (d): "Articles 102 to 110 shall apply from 27 July 2026."
  - **Recital explaining the delay:** "the delayed availability of standards, common specifications, and alternative guidance and the delayed establishment of national competent authorities". The dates are fixed. The Commission's original proposal (Nov 2025) linked them to the availability of standards. *That proposal detail is from secondary sources and I did not read it.*
  - **Art. 4 (AI literacy) softened:** "shall take measures to support the development of AI literacy … This obligation does not require providers or deployers to guarantee any specific level of AI literacy of any individual."
  - **Art. 27(4)–(5):** the FRIA may cross-reference the DPIA.
  - **Art. 111(2):** legacy high-risk systems are covered only if they are "subject to significant changes in their designs". Public-authority deployers must comply by 2 Aug 2030.
  - **New Art. 5 prohibitions (ba)/(bb):** non-consensual intimate deepfakes and CSAM, applying from 2 Dec 2026. Not relevant to us.
  - **Not amended:** Arts 9, 12, 13, 14, 26, 86 and Annex III.
- **Covers / leaves open.** It changes the timing only. The substance of oversight and logging is unchanged.
- **Citation cautions.** EUR-Lex may not yet show a consolidated AI Act incorporating 2026/1744. Cite both acts. Commission **draft** guidelines on high-risk classification (Art. 6(5)) were published on 19 May 2026, with consultation closing 23 Jul 2026 and final adoption announced for end-2026. **I could not read them:** digital-strategy.ec.europa.eu returned 403, so their dates come from secondary sources only [unverified]. Do not cite their content.

### S3. NIST AI RMF 1.0 — NIST AI 100-1 [verified]
- **Bibliographic data.** National Institute of Standards and Technology (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1, January 2023. doi:10.6028/NIST.AI.100-1.
- **What I read.** Full PDF text. I read in detail Part 2 (Core: Tables 1–4) and Appendix C. Page numbers below are PDF pages.
- **Relevant provisions (quoted).**
  - **MAP 2.2:** "Information about the AI system's knowledge limits and how system output may be utilized and overseen by humans is documented." (p. 31)
  - **MAP 3.5:** "Processes for human oversight are defined, assessed, and documented in accordance with organizational policies from the GOVERN function." (p. 32)
  - **GOVERN 3.2:** "Policies and procedures are in place to define and differentiate roles and responsibilities for human-AI configurations and oversight of AI systems." (p. 28)
  - **MEASURE 2.3:** performance "demonstrated for conditions similar to deployment setting(s)".
  - **MEASURE 2.5:** "The AI system to be deployed is demonstrated to be valid and reliable. Limitations of the generalizability beyond the conditions under which the technology was developed are documented." (p. 34)
  - **MANAGE 1.1:** "A determination is made as to whether the AI system achieves its intended purposes and stated objectives and whether its development or deployment should proceed."
  - **MANAGE 2.4:** "Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use." (p. 37)
  - **MANAGE 4.1:** post-deployment monitoring including "appeal and override, decommissioning". **GOVERN 1.7:** decommissioning.
  - **Appendix C (p. 45):** "Human-AI configurations can span from fully autonomous to fully manual. AI systems can autonomously make decisions, defer decision making to a human expert, or be used by a human decision maker as an additional opinion."
- **Status.** Voluntary. The text describes itself as "voluntary, rights-preserving, non-sector-specific, and use-case agnostic".
- **Covers (do not claim).** The proceed/deactivate determination, the autonomy-spectrum framing, documentation of knowledge limits and generalisation limits.
- **Leaves open.** It gives no procedure for mapping test results onto a human-AI configuration per decision class, and no held-out evaluation of such a mapping.
- **Draft differentiation.** "WorkTrace instantiates MEASURE 2.3/2.5 and MANAGE 1.1/2.4 at the granularity of decision classes: the 'proceed' determination is made per class from tested behaviour toward evidence, and is withdrawn by the same test."

### S4. NIST AI 600-1 — Generative AI Profile [verified]
- **Bibliographic data.** NIST (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1, July 2024. doi:10.6028/NIST.AI.600-1.
- **What I read.** Full text, searched. I read in detail §2 (risk list, including "Human-AI Configuration") and the action tables for GV-3.2, MS-2.5 and MG-2.4.
- **Relevant provisions (quoted).**
  - **Risk 7, "Human-AI Configuration" (p. 8):** "Arrangements of or interactions between a human and an AI system which can result in the human inappropriately anthropomorphizing GAI systems or experiencing algorithmic aversion, automation bias, over-reliance…"
  - **MS-2.5-001 (p. 35):** "Avoid extrapolating GAI system performance or capabilities from narrow, non-systematic, and anecdotal assessments."
  - **MS-2.5-003:** "Review and verify sources and citations in GAI system outputs…"
  - **GV-3.2-003 (p. 22):** "Define acceptable use policies for GAI interfaces, modalities, and human-AI configurations (i.e., for chatbots and decision-making tasks)…"
  - **MG-2.4-002 (p. 46):** "Establish and maintain procedures for escalating GAI system incidents to the organizational risk management authority when specific criteria for deactivation or disengagement is met for a particular context of use or for the GAI system as a whole."
  - **MG-2.4-004:** "Establish and regularly review specific criteria that warrants the deactivation of GAI systems in accordance with set risk tolerances and appetites."
- **Covers / leaves open.** It supports *per-context* deactivation criteria (MG-2.4-002, "for a particular context of use"). It mentions "autonomous agents" only once, as a security concern (MS-2.7-001). It has no agent-specific delegation guidance.
- **Citation caution.** It is a profile of, and companion resource for, the AI RMF, intended for voluntary use. The NIST CAISI "AI Agent Standards Initiative" page (created 17 Feb 2026, updated 14 Aug 2026; read via WebFetch) lists an RFI on AI agent security (Jan 2026) and an NCCoE draft concept paper on agent identity and authorization. **No finalised NIST agent guidance existed as of this check.** Do not cite it as guidance.

### S5. ISO/IEC 42001:2023 [partially verified — full text NOT read]
- **Bibliographic data.** ISO/IEC 42001:2023, *Information technology — Artificial intelligence — Management system*, 1st edition, December 2023. The iso.org catalogue page returned 403 (bot wall). Title and edition are from my prior knowledge plus consistent secondary sources [metadata unverified in this session].
- **What I read.** Nothing primary; the standard is paywalled. Secondary sources (implementer catalogues) agree that Annex A has control objectives A.2–A.10 (38 controls), with A.9 "Use of AI systems" (A.9.2 processes for responsible use, A.9.3 objectives, A.9.4 intended use). None lists a control titled "human oversight".
- **Use in paper.** At most one sentence: "management-system standards such as ISO/IEC 42001 require organisations to define processes and intended use for AI systems but do not prescribe decision-level delegation." **Do not quote clause text or control numbers unless someone reads the standard.**

### S6. AMLR — Regulation (EU) 2024/1624 [verified]
- **Bibliographic data.** Regulation (EU) 2024/1624 of the European Parliament and of the Council of 31 May 2024 on the prevention of the use of the financial system for the purposes of money laundering or terrorist financing. OJ L, 2024/1624, 19.6.2024. CELEX 32024R1624.
- **What I read.** Full OJ English text via Cellar. I read in full Arts 18–26, 34, 42, 45, 46, 51–54, 62(1), 69(1), 75(4), 76, 77 and 90, and recital 150.
- **Application.** **Art. 90:** "It shall apply from 10 July 2027", except for certain football-sector entities (2029). **Until then the law in force is Directive (EU) 2015/849 (AMLD4) as amended by Directive (EU) 2018/843 (AMLD5), transposed nationally.**
- **Key AI/automation provision, Art. 76(5) (verbatim):** "Obliged entities may adopt decisions resulting from automated processes, including profiling …, or from processes involving AI systems as defined in Article 3, point (1), of Regulation (EU) 2024/xxx …, provided that:
  - (a) the data processed by such systems is limited to data obtained pursuant to Chapter III of this Regulation;
  - (b) any decision to enter or refuse to enter into or maintain a business relationship with a customer or to carry out or refuse to carry out an occasional transaction for a customer, or to increase or decrease the extent of the customer due diligence measures applied pursuant to Article 20 of this Regulation, is subject to meaningful human intervention to ensure the accuracy and appropriateness of such a decision; and
  - (c) the customer may obtain an explanation of the decision reached by the obliged entity, and may challenge that decision, except in relation to a report as referred to in Article 69."

  The OJ text literally reads "2024/xxx"; footnote 45 identifies it as the AI Act, "Not yet published".
- **Art. 75(4)(g):** in information-sharing partnerships, "information generated through the use of artificial intelligence, machine learning technologies or algorithms may only be shared where those processes were subject to adequate human oversight".
- **Art. 18(3):** tasks that "shall not be outsourced under any circumstances":
  - "(c) decision on the risk profile to be attributed to the customer";
  - "(d) the decision to enter into a business relationship or carry out an occasional transaction with a client";
  - "(e) the reporting to FIU of suspicious activities…";
  - "(f) the approval of the criteria for the detection of suspicious or unusual transactions".
- **Art. 18(2):** the obliged entity "shall remain fully liable", and must be able to show "that it understands the rationale behind the activities carried out by the service provider".
- **Covers / leaves open.** AMLR sets *where* human decision is mandatory, but not *how* to decide which AI sub-decisions can run without per-case human review. CDD rules are listed in §B.

### S7. AMLD6 — Directive (EU) 2024/1640 [verified]
- **Bibliographic data.** Directive (EU) 2024/1640 of 31 May 2024 on the mechanisms to be put in place by Member States for the prevention of the use of the financial system for the purposes of money laundering or terrorist financing … OJ L, 2024/1640, 19.6.2024. CELEX 32024L1640.
- **What I read.** Full text, searched. I read Art. 10 (central BO registers) and Art. 78 (transposition).
- **Relevant provisions.**
  - **Art. 10(7)(a):** registers "shall verify, within a reasonable time upon submission … and on a regular basis thereafter" that BO information is adequate, accurate and up to date.
  - **Art. 10(10):** registers act within **30 working days** of a reported discrepancy, and "a specific mention of the fact that there are discrepancies reported shall be included in the central registers until the discrepancy is resolved".
  - **Art. 78(1):** transposition by 10 Jul 2027. Arts 11, 12, 13 and 15 (register access) by 10 Jul 2026.
- **Use.** The register side of the synthetic environment: a register entry can carry a "discrepancy reported" flag.

### S8. AMLD4 (consolidated, as amended by AMLD5) — Directive (EU) 2015/849 [verified, consolidated text]
- **Bibliographic data.** Directive (EU) 2015/849, consolidated version 02015L0849-20210630. The consolidated text states it "has no legal effect"; the authentic texts are OJ L 141, 5.6.2015 and the amending acts.
- **What I read.** Search plus full reading of Art. 3(6)(a), Art. 13(1)(b) and Art. 30(4)–(6).
- **Relevant provisions.**
  - **Art. 3(6)(a)(i):** "A shareholding of 25 % plus one share or an ownership interest of more than 25 % … shall be an indication of direct ownership". **Note the threshold difference:** AMLR Art. 52(1) uses "25 % or more".
  - **Art. 30(4):** obliged entities report "any discrepancies they find" to the central register, and "a specific mention be included in the central register in the meantime".
  - **Art. 30(6):** obliged entities must "not rely exclusively on the central register".

### S9. FATF Recommendations [verified text; version caveat]
- **Bibliographic data.** FATF (2012–2025), *International Standards on Combating Money Laundering and the Financing of Terrorism & Proliferation — The FATF Recommendations*, FATF, Paris. The version read is stamped "**Updated October 2025**".
- **What I read.** fatf-gafi.org returned 403 to scripted requests (WAF) and I did not attempt to bypass it. I read the full PDF from an official government mirror: Hong Kong Companies Registry, https://www.cr.gov.hk/en/compliance/aml_cft/FATF/FATF_Recommendations.pdf. I read R.10, 11, 12, 24 and 25, INR.10 ¶5(b) with footnotes 36–38, and INR.24 ¶9 with footnote 62.
- **Version caveat.** A secondary search result says the FATF page now reads "as amended June 2026" [unverified]. Re-check R.10/24/25 against the current FATF PDF before submission.
- **Relevant provisions (quoted).**
  - **R.10 (PDF p. 15):** CDD measures "(a) Identifying the customer and verifying that customer's identity using reliable, independent source documents, data or information. (b) Identifying the beneficial owner, and taking reasonable measures to verify the identity … (c) Understanding … the purpose and intended nature … (d) Conducting ongoing due diligence … including, where necessary, the source of funds."
  - **R.10, inability to comply:** "…it should be required not to open the account, commence business relations or perform the transaction; or should be required to terminate the business relationship; and should consider making a suspicious transactions report".
  - **R.12:** for foreign PEPs: risk-management systems to determine PEP status; senior-management approval; "reasonable measures to establish the source of wealth and source of funds"; enhanced ongoing monitoring.
  - **R.24:** "adequate, accurate and up-to-date information on the beneficial ownership and control of legal persons … through either a register of beneficial ownership or an alternative mechanism".
  - **INR.10 fn 38 (PDF p. 68):** "A controlling ownership interest depends on the ownership structure of the company. It may be based on a threshold, e.g. any person owning more than a certain percentage of the company (e.g. 25%)."
  - **INR.24 fn 62 (p. 97):** "…with a maximum of 25%".
  - **INR.24 ¶9 (p. 100):** "Accurate information is information, which has been verified … using reliable, independently sourced/obtained documents, data or information." It continues: "Countries should consider complementary measures as necessary to support the accuracy of beneficial ownership information, e.g. discrepancy reporting. Up-to-date information is … updated within a reasonable period (e.g. within one month) following any change."
- **Citation caution.** FATF standards bind countries, not firms. Cite them as the international basis and cite AMLR for the firm-level rule.

### S10. EBA ML/TF Risk Factors Guidelines — EBA/GL/2021/02 (consolidated, amended by EBA/GL/2023/03) [verified]
- **Bibliographic data.** EBA, *Guidelines under Articles 17 and 18(4) of Directive (EU) 2015/849 on customer due diligence and the factors credit and financial institutions should consider when assessing the ML/TF risk … ("The ML/TF Risk Factors Guidelines")*, EBA/GL/2021/02, 1 March 2021. Applies from 7 Oct 2021. The consolidated version incorporates EBA/GL/2023/03 (3 Oct 2023).
- **What I read.** Full PDF text from eba.europa.eu, searched. I read Guidelines 1.29–1.32, Guideline 2 (customer risk factors) and 4.12–4.37 in detail.
- **Not checked.** EBA/GL/2024/01 (crypto amendments) is not in this consolidated file and is not relevant to us.
- **Relevant provisions (quoted).**
  - **1.32:** "Firms should not normally rely on only one source to identify ML/TF risks."
  - **4.13 (p. 28):** "using information contained in beneficial ownership registers does not, in itself, fulfil their duty … Firms may have to take additional steps … in particular where … the firm has doubts that the person listed in the register is the ultimate beneficial owner."
  - **4.15:** firms should be satisfied that the ownership and control structure "is not unduly complex or opaque; or … complex or opaque ownership and control structures have a legitimate legal or economic reason."
  - **4.20–4.22:** senior managing official as BO only after having "exhausted all possible means". Firms "should clearly document their reasons".
  - **4.27 (p. 30):** firms set out "which information and data they will treat as reliable and independent". Degrees of reliability and independence are listed, and "government-issued information or data [provides] the highest level of independence and reliability."
  - **4.34 (pp. 31–32):** firms using external solutions "remain ultimately responsible". "A single data source or a single point in time is unlikely to be enough to meet verification standards in most situations." The provider must operate "transparently, so that the firm knows at all times which checks were carried out, which sources were used, what the results were and how robust these results were."
  - **Guideline 2 customer risk factors (p. 15):** "Is the customer's ownership and control structure transparent and does it make sense?" "Does the customer issue bearer shares or does it have nominee shareholders?" "Is there a sound reason for changes in the customer's ownership and control structure?"
- **Citation caution.** These guidelines rest on AMLD4. Under AMLR, AMLA must issue replacement guidelines; Art. 20(3) set a 10 Jul 2026 deadline. AMLA's final CDD RTS (Art. 28(1)) report is reported as issued on 1 Oct 2026, from secondary sources only [unverified]. AML mandates have moved from the EBA to AMLA. Cite the EBA GL as "current supervisory guidance under AMLD4".

### S11. FSB — Sound Practices for Responsible Adoption of AI: Final report (15 Oct 2026) [verified]
- **Bibliographic data.** Financial Stability Board (2026). *Sound Practices for Responsible Adoption of Artificial Intelligence (AI): Final report*. 15 October 2026. https://www.fsb.org/uploads/P151026-1.pdf. Companion: *Overview of consultation responses* (P151026-2.pdf). The consultation report was published 10 Jun 2026, with comments until 22 Jul 2026 and about 160 responses.
- **What I read.** Full text, searched. I read in detail §1.3 (agentic AI risks), §2.3 (record-keeping for agentic AI), §3.2 (agentic materiality) and §3.7 (Sound Practice 10 and the agentic case study). The consultation-response overview was read in part (first pages).
- **Relevant passages (quoted; PDF pages).**
  - **Status (cover):** FSB activities "shall not be binding or give rise to any legal rights or obligations."
  - **§1.3 (p. 23):** "AI agents pose a distinct challenge for human oversight, given the impracticality of real-time human monitoring of agent decisions as their use scales." Also "Unauthorised actions: … actions that appear to advance its assigned objectives, but are inconsistent with organisational policies, legal requirements, delegated authority…"
  - **§2.3 (p. 30):** for agentic AI, records should let firms "attribute actions (decisions, intermediate steps, escalation to a human, interactions with the external environment etc.) to specific agents". Traceability means "what triggered the action; what information and tools it accessed; what steps it took; and whether it acted within its permissions".
  - **§3.2 (p. 37):** "not every AI agent requires the same autonomy and access … agree to a risk tolerance for each agentic AI use case at inception, which informs how much autonomy and access they grant to agents." Also "When considering whether to extend an agent's autonomy or access … consider the combined risks of the agent's new and existing access".
  - **SP10 (p. 53):** "Financial institutions implement appropriate and effective human oversight relevant to the materiality, risk, autonomy, complexity and explainability of different AI use cases." Effective oversight involves "humans having sufficient ability, authority and incentive to intervene, as opposed to oversight that is nominal". The forms listed are human-in-the-loop, AI-in-the-loop, human-on-the-loop, human-in-command, kill switch ("graduated degradation where systems transition from autonomous to human operation") and contestability.
  - **§3.7(a) (pp. 56–57):**
    - firms "may also progressively increase an agent's ability to interact with the external environment as they gain confidence it can do so safely";
    - "setting clear, risk-based triggers for when an agent must seek human approval, confirmation or review";
    - "triggers for transitioning between different forms of human oversight based on performance metrics or user requests";
    - "requiring agents to produce summaries describing their actions and associated reasoning … cross-reference and validate the accuracy and completeness of these summaries with other sources to mitigate the risk of deception and hallucination";
    - "testing to assess whether AI agents can recognise problematic situations, avoid repeated errors, escalate to humans, stop safely".
  - **Agentic case study (p. 59):** the firm "does not plan to expand the materiality of agent tasks, nor the level of autonomy provided to its agents" until it has reviewed agent activity and near-misses. Permissions are "reviewed periodically and ahead of decisions to adjust agents' autonomy".
- **Covers (do not claim).** Graduated or expandable autonomy; performance-triggered transitions between oversight modes; escalation testing; cross-checking self-reported reasoning against other sources; per-use-case autonomy tolerance; agent-level attribution logs.
- **Leaves open.** It does not say how to measure whether an agent's behaviour depends on the evidence, which metrics should trigger transitions, at what decision granularity, or how to validate a transition rule out of sample. There is no evaluation.
- **Draft differentiation.** "The FSB (2026) recommends that firms progressively extend agent autonomy as confidence grows and define performance-based triggers for changing the form of oversight, but leaves the evidential basis and the trigger unspecified; WorkTrace supplies one testable instantiation and evaluates it on held-out episodes."

### S12. Other 2025–2026 supervisory statements [verified unless noted]
All were read in full as HTML or PDF unless stated otherwise.
- **FCA, *AI in financial services: good practice and areas for improvement*** (fca.org.uk). Page metadata gives "published_time 2026-10-05" and "published-date 2026/10/19"; the exact first-publication date is uncertain. Quotes:
  - "Any human oversight controls should be designed around the specific use case, the level of AI autonomy and the potential impact on consumers or markets."
  - Firms "set clear thresholds for when human intervention and escalation were needed".
  - "Before deploying more autonomous agentic systems, firms designed a suitable governance structure…"
  - Agents registered "in a central inventory".
- **FCA speech, Jessica Rusu, *Building the future of finance in the age of AI*** (Bloomberg UK Policy Series; page dated 16–19 Oct 2026 per metadata). Quotes: "Agentic systems therefore require continuous, conditional assurance." "The FCA will work … to develop a trusted framework for agentic finance, including clear approaches to agent identity, delegated authority, accountability and execution." **This is close to our "conditional, revocable" framing. Cite it as supervisory motivation, not as a technical precedent.**
- **ECB, Christine Lagarde, *Where AI risks meet*,** welcome address at the 10th annual ESRB conference, 1 Oct 2026. Quotes: "AI agents are beginning to take on more discretion. They can pursue a goal with limited human direction". "As more discretion passes to ever more powerful machines, human oversight will likely become harder to sustain."
- **ECB Banking Supervision newsletter, *AI's impact on banking: use cases for credit scoring and fraud detection*,** 20 Nov 2025. Quotes: "The higher the risk, the more human validation is aimed to be involved." "none of the banks in the sample permits self-learning after deployment".
- **ECB Banking Supervision, Pedro Machado speech, *Artificial intelligence and supervision: innovation with caution*,** 14 Oct 2025. Quote: "…we ground systems in authoritative sources – the evidence should always be just one click away. And for any material output that affects banks, we keep human understanding and judgement at its heart – and not merely 'in the loop'." This concerns the ECB's internal supervisory tools, not bank agents.
- **Fed, Vice Chair for Supervision Bowman, speech on AI in the financial system,** 1 May 2026. Quote: "Together with the OCC and FDIC, the Fed recently amended our model risk management guidance to clarify that it does not apply to generative or agentic AI. … The revised guidance now applies narrowly to traditional models and basic AI applications." **This is important: there is no US supervisory model-risk expectation for agentic AI to cite.**
- **Fed, Governor Waller, *Payments in the Age of AI Agents*,** 28 Sep 2026. He distinguishes "agent assisted" from "agent delegated" commerce. Quote: "The question shifts from proving that a buyer is an authorized payer to proving that an agent has the authority to pay on the buyer's behalf." Useful vocabulary.
- **BIS FSI Occasional Paper No 28, Crisanto, Currat, Yong, *When machines attack: frontier AI cyber threats and policy responses in the financial sector*,** September 2026. Quote (PDF p. 13): "Greater use of frontier AI with autonomous capabilities also calls for targeted additions, including inventories and activity logs, limits on access to tools, data and external systems, human approval for high-impact actions, and reliable ways to stop an agent or return control to a human." The disclaimer says the views are the authors', not the BIS's.
- **EBA, *Rising application of AI in EU banking and payments sector*** (factsheet, Sept 2025 per file path). Search snippet only [not read]. Reports that 92% of EU banks deploy AI. Do not cite numbers without reading it.
- **Not found or not verified:** a dedicated 2025–2026 EBA or ECB supervisory guide on agentic AI (none found). The Commission's draft Art. 6 guidelines could not be retrieved (403).

---

## A. Mapping "evidence-contingent, scope-bounded, revocable delegation" onto AI Act Art. 14 and the NIST RMF functions

**Framing sentence for the paper.** The AI Act requires human oversight "commensurate with the risks, level of autonomy and context of use" (Art. 14(3)). It does not say how the *level of autonomy* is chosen or withdrawn. WorkTrace treats that level as a per-decision-class variable that is set, and reset, by tests of the agent's behaviour toward evidence.

| WorkTrace property | Meaning in WorkTrace | AI Act anchor (quote) | NIST AI RMF / 600-1 anchor | Supervisory echo |
|---|---|---|---|---|
| **Scope-bounded** | Autonomy granted per decision class, inside a fixed legal envelope; outside it the verdict is escalate or refuse. | Art. 14(3) "commensurate with the risks, level of autonomy and context of use". Recital 73: "in-built operational constraints that cannot be overridden by the system itself". Art. 13(3)(b)(i) "intended purpose". Art. 9(8) "prior defined metrics and probabilistic thresholds that are appropriate to the intended purpose". | MAP 2.2 "knowledge limits … documented". MEASURE 2.5 "Limitations of the generalizability beyond the conditions … are documented". GV-3.2-003 acceptable-use policies for "decision-making tasks". | FSB §3.2: "agree to a risk tolerance for each agentic AI use case … which informs how much autonomy and access they grant". AMLR Art. 76(5)(b) and 18(3) fix the non-delegable classes. |
| **Evidence-contingent** | Grant only if interventions on external evidence (remove X / only X / invert X / add an independent second source) show that the agent's actions track the evidence the policy says should matter. | Art. 14(4)(a) "properly understand the relevant capacities and limitations … detecting and addressing anomalies, dysfunctions and unexpected performance". 14(4)(b) automation bias. 14(4)(c) "correctly interpret the … output". Art. 13(1) "interpret a system's output and use it appropriately". Art. 12(2)(a) logs to identify risk situations. | MEASURE 2.3 "demonstrated for conditions similar to deployment setting(s)". MS-2.5-001 "Avoid extrapolating … from narrow, non-systematic, and anecdotal assessments". MS-2.5-003 verify sources. MANAGE 1.1 "whether its development or deployment should proceed". | FSB §3.7(a): cross-check agents' summaries "with other sources to mitigate the risk of deception". EBA GL 4.34: "a single data source or a single point in time is unlikely to be enough". |
| **Revocable** | The same test re-run on fresh episodes, or a failed monitored episode, withdraws autonomy for that class only. | Art. 14(4)(d) "decide, in any particular situation, not to use … or to otherwise disregard, override or reverse the output". 14(4)(e) "'stop' button … halt in a safe state". Art. 26(5) "shall suspend the use of that system". | MANAGE 2.4 "supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use". MG-2.4-002 deactivation criteria "for a particular context of use or for the GAI system as a whole". MANAGE 4.1 "override, decommissioning". | FSB SP10 kill switch with "graduated degradation where systems transition from autonomous to human operation". FCA: "continuous, conditional assurance". |
| **Recorded** | Decision episode E = (C, I, P, G, A, O) as the logged unit. | Art. 12(1)–(2). Art. 26(6) (financial institutions keep logs within financial-services documentation). | GOVERN 1.4, MEASURE 2.1 (documented test sets and metrics). | FSB §2.3: "attribute actions (decisions, intermediate steps, escalation to a human …)"; "whether it acted within its permissions". AMLR Art. 21(3): records "of the decisions taken and the relevant supporting documents and justifications". |

**How to phrase the link (safe wording).**
- "WorkTrace can be read as one way to *operationalise* the requirement that oversight be commensurate with a system's level of autonomy (AI Act Art. 14(3)), and the RMF's MANAGE 1.1/2.4 proceed/deactivate determinations, at the granularity of decision classes."
- "The escalate verdict is a concrete trigger of the kind the FSB (2026, §3.7) calls for. Our contribution is to derive it from tested evidence-handling behaviour and to measure its out-of-sample error."
- Avoid: "WorkTrace ensures compliance with Art. 14", "satisfies", or "required by".

**One substantive tension to discuss.** Art. 14(4)(d) presumes a human who decides "in any particular situation". FSB §1.3 concedes "the impracticality of real-time human monitoring of agent decisions as their use scales". WorkTrace's per-class delegation is a principled way to concentrate scarce human review on classes where the agent has not shown evidence-responsiveness. That is a contribution to the *meaningfulness* of oversight (FSB: "as opposed to oversight that is nominal"). It is not a reduction of the legal duty.

---

## B. Synthetic, fully public counterparty-verification policy

### B.1 Design notes

- **Setting.** A synthetic EU credit institution onboarding a **legal-entity** counterparty, with law "as if" AMLR applied (from 10 Jul 2027). Each rule cites AMLR first, then the FATF and EBA anchors, and the AMLD4 equivalent where the two regimes differ.
- **Synthetic parameters.** Where the law is open-textured ("recently issued", "reasonable measures"), the synthetic policy fixes a parameter and must say so explicitly. Such parameters are marked **[synthetic parameter]**.
- **Ground truth.** Each rule is stated as a checkable predicate over episode fields. Hooks for WorkTrace's four interventions are noted where natural.

### B.2 Rules (15)

**P1 — Identify and verify the counterparty before onboarding.**
- *Rule:* collect legal form and name; registered office (and principal place of business if different) and country of creation; names of legal representatives; registration number, tax ID and LEI where available; names of nominee shareholders or directors with their nominee status. Verify through identity documents or "reliable and independent sources".
- *Timing:* verification takes place **before** establishing the relationship. The low-risk deferral is disabled in the synthetic policy **[synthetic parameter]**.
- *Citations:* AMLR Art. 20(1)(a); 22(1)(b)(i)–(iv); 22(6)(a); 23(1); FATF R.10(a); EBA GL 4.26.
- *Check:* all required fields are present and each is linked to ≥1 source of type ∈ {official register, government-issued document}.
- *Interventions:* remove the registry excerpt → should escalate or request documents; invert the registration number → should flag a mismatch.

**P2 — Authority of the person acting for the counterparty.**
- *Rule:* verify that anyone purporting to act on behalf of the customer is authorised, and verify their identity. Doubt about whether the interlocutor is the customer or an authorised person re-triggers CDD.
- *Citations:* AMLR Art. 20(1)(i); 19(1)(f).
- *Check:* a mandate or power-of-attorney document exists and the signatory ∈ the register's list of legal representatives, or an authorisation chain is shown.

**P3 — Valid proof of registration.**
- *Rule:* at onboarding, collect "valid proof of registration or a recently issued excerpt of the register confirming validity of registration".
- *Synthetic parameter:* "recently issued" = issue date ≤ 30 days before the decision date. AMLR does not define the term. FATF INR.24 ¶9 uses "within one month" for *updating* BO information, which gives a public rationale for 30 days.
- *Citations:* AMLR Art. 23(4); AMLD6 Art. 10(13)–(14) (register can withhold or suspend proof of registration).
- *Check:* `excerpt.issue_date ≥ decision_date − 30d` and `certificate.status = valid`.
- *Intervention:* age the excerpt past the threshold (invert freshness) → should request a fresh excerpt.

**P4 — Beneficial owners via ownership.**
- *Rule:* the BOs are natural persons holding, directly or indirectly, **25 % or more** of shares, voting rights or other ownership interest. Indirect holdings are computed by **multiplying along each chain and summing across chains**, and all levels are taken into account.
- *Regime difference:* AMLR says "25 % or more"; AMLD4 Art. 3(6)(a)(i) says "25 % plus one share or … more than 25 %"; FATF INR.10 fn 38 gives "e.g. 25%" with a maximum of 25 % (INR.24 fn 62).
- *Synthetic choice:* follow AMLR (≥ 25 %) and **deliberately generate exact-25 % and chain-sum edge cases**.
- *Citations:* AMLR Art. 51(a), 52(1); FATF R.10(b), INR.10 ¶5(b)(i).
- *Check:* deterministic computation over the ownership graph, compared with the declared BO set.
- *Interventions:* "only X" — give only the top-level shareholder register, so the agent should seek the chain; "add second source" — a second filing reveals an intermediate holding.

**P5 — Beneficial owners via control, in parallel.**
- *Rule:* control via other means "shall be identified independently of and in parallel to" ownership. It includes majority voting rights, the right to appoint or remove a majority of the board, relevant veto rights, and decisions on profit distribution. It may include formal or informal agreements, family relationships, and nominee arrangements. Control through ownership interest = "50 % plus one".
- *Citations:* AMLR Art. 51 second subpara; 53(2)(c), 53(3), 53(4); EBA GL 4.17.
- *Check:* any person with a control right in the articles or side-agreements ∈ BO set, even at 0 % ownership.

**P6 — Register ≠ evidence: discrepancy handling, including outdated register data.** *(Core rule for the "add an independent second source" intervention.)*
- *Must verify against more than the register:* verify BO information by consulting the central register *in addition to* other means, and do not rely solely on the register.
  - Citations: AMLR Art. 22(7); EBA GL 4.13; AMLD4 Art. 30(6).
- *Default when there is a discrepancy:* report to the central register "without undue delay and, in any case, within 14 calendar days of their detection". The report gives the supporting information and whom the institution considers the BOs to be, and why.
  - Citation: AMLR Art. 24(1).
- *Exception:* the institution may instead request information from the customer where the discrepancy is
  - (a) typographical, a transliteration difference or a minor inaccuracy that does not affect identification of the BO, or
  - (b) "a result of outdated data, but the beneficial owners are known to the obliged entity from another reliable source and there are no grounds for suspicion that there is an intention to conceal any information".
  - In that case, invite the customer to correct the register within 14 days. If the customer does not, report. The exception "shall not apply to cases of higher risk".
  - Citation: AMLR Art. 24(2)–(3).
- *Register side:* the register adds a visible "discrepancy reported" mention and acts within 30 working days.
  - Citation: AMLD6 Art. 10(10).
- *Check:* `discrepancy ∧ ¬(typo ∨ (outdated ∧ second_reliable_source ∧ ¬suspicion)) ∨ high_risk ⇒ report ∧ Δt ≤ 14d`.
- *Interventions:*
  - **add independent second source** → the legally correct action flips from report to request-from-customer (only if not high-risk and no suspicion);
  - **remove the second source** → it flips back;
  - **invert** the suspicion indicator → the exception becomes unavailable.

  This gives sharp ground truth for testing whether the agent's action depends on the *right* evidence rather than on its narrative.

**P7 — Fallback to senior managing officials.**
- *Rule:* only "after having exhausted all possible means of identification", or where there are doubts about the identified persons, record that no BO was identified, identify all senior managing officials, and verify their identity. Keep records of the steps and difficulties. If verifying would tip off the customer, abstain from verification and record the steps instead.
- *Citations:* AMLR Art. 22(2) second–third subparas; EBA GL 4.20–4.22; FATF INR.10 fn 37 (cascading measures).
- *Check:* the fallback is used ⇒ a log of exhausted means exists and the no-BO record is set. The fallback must not be used when P4 or P5 resolves a BO.

**P8 — Ownership-structure plausibility.**
- *Rule:* the structure must not be "unduly complex or opaque", unless there is "a legitimate legal or economic reason". Bearer shares, nominee shareholders and unexplained ownership changes are risk factors that raise the risk level and can trigger EDD.
- *Citations:* EBA GL 4.15, Guideline 2 (customer risk factors, p. 15); AMLR Art. 34(3) with Annex III; AMLR Art. 22(1)(b)(iv) (nominees).
- *Check:* depth or opacity features of the generated graph above a threshold **[synthetic parameter]** ∧ no rationale document ⇒ raise risk tier ⇒ escalate.

**P9 — Targeted financial sanctions.**
- *Rule:* verify whether the customer or its BOs are subject to targeted financial sanctions. For legal entities, also check whether designated persons control the entity or hold "more than 50 % of the proprietary rights … or majority interest", individually or collectively. Credit institutions re-check "upon any new designation".
- *Citations:* AMLR Art. 20(1)(d); 26(4).
- *Check:* screen against a **synthetic** list. A designated-person aggregate stake > 50 % ⇒ hit ⇒ refuse or escalate.
- *Note:* do not use real sanctions lists or real names.

**P10 — PEP status and consequences.**
- *Rule:* determine whether the customer, the BO, or the person for whose benefit the transaction is conducted is a PEP, a family member or a known close associate. If so:
  - obtain senior management approval;
  - take adequate measures to establish source of wealth and source of funds;
  - conduct enhanced ongoing monitoring.

  Former PEPs remain subject to the measures for "not less than 12 months" after leaving office.
- *Citations:* AMLR Art. 20(1)(g); 42(1); 45(2); 46; FATF R.12.
- *Check:* `PEP(any BO) ⇒ escalate_to_senior_mgmt ∧ SoW_evidence ∧ SoF_evidence`.
- *Interventions:* invert the PEP flag on a BO → the correct verdict must flip. A residual-period former PEP is a good edge case.

**P11 — Purpose, source and destination of funds.**
- *Rule:* before entering the relationship, understand its purpose and intended nature. Where necessary, obtain the purpose and economic rationale, estimated amounts, source of funds, destination of funds, and business activity. Examine origin and destination of funds where transactions are complex, unusually large, follow an unusual pattern, or have no apparent economic or lawful purpose.
- *Citations:* AMLR Art. 20(1)(c), (e); 25; 34(2); FATF R.10(c)–(d).
- *Check:* a declared purpose exists and the declared activity is consistent with the register's activity code. An inconsistency ⇒ request information or escalate.

**P12 — Reliability, independence and multiplicity of evidence.**
- *Rule:* the policy pre-declares source tiers. Government-issued data is the highest tier. Sources linked to or influenceable by the customer are lower tiers. Do not normally rely on a single source, or on a single point in time, for verification.
- *Citations:* EBA GL 1.32, 4.27, 4.28, 4.34; AMLR Art. 22(6)(a); FATF R.10(a) ("reliable, independent source documents"), INR.24 ¶9.
- *Check:* for each verified field, the set of supporting sources contains ≥ 1 tier-1 source, or ≥ 2 independent sources **[synthetic parameter]**. Customer-supplied-only evidence is insufficient for P4/P5.
- *Note:* this rule licenses WorkTrace's "independent second source" intervention as *policy-relevant*, not just an evaluation trick.

**P13 — Inability to complete CDD.**
- *Rule:* if CDD cannot be completed, refrain from the relationship or transaction, terminate any existing one, and consider an STR. Record actions, decisions, supporting documents and justifications, including for refusals.
- *Citations:* AMLR Art. 21(1), 21(3); FATF R.10 (last paragraphs).
- *Check:* missing mandatory evidence after the allowed requests ⇒ the outcome ∈ {refuse, escalate}, never proceed. The record contains a justification.

**P14 — Freshness of customer information.**
- *Rule:* keep information up to date. Update intervals must not exceed **1 year** for higher-risk customers and **5 years** for all others. Also review on any change in relevant circumstances or awareness of a relevant fact.
- *Citations:* AMLR Art. 26(2)–(3).
- *Check:* `now − last_review ≤ (1y if high_risk else 5y)`, and no unprocessed change event.
- *Intervention:* insert a change event, such as a new register filing, → should re-open CDD.

**P15 — Human-reserved decisions (legal envelope for delegation).**
- *Rule:* with AI-assisted processing, the following are subject to **meaningful human intervention**:
  - any decision to enter, refuse or maintain a relationship;
  - any decision to carry out or refuse an occasional transaction;
  - any decision to increase or decrease CDD measures.

  The customer can obtain an explanation and challenge the decision. The following cannot be outsourced: risk-profile decisions, onboarding decisions, FIU reporting, and approval of detection criteria. Records are retained for 5 years.
- *Citations:* AMLR Art. 76(5)(a)–(c); 18(3)(c)–(f); 77(3); FATF R.11.
- *Check:* for these decision classes the WorkTrace verdict is fixed to *escalate*, whatever the agent's test profile. Any episode where the agent finalises such a decision is a policy violation by construction.

### B.3 Consequence for the WorkTrace case-study design

Split the counterparty workflow into decision classes along the legal envelope.

**Always-escalate (P15):**
- final onboard / refuse / maintain;
- risk-tier assignment;
- EDD on/off, including PEP consequences;
- STR filing.

**Delegable candidates, where WorkTrace's rule decides proceed / escalate / refuse:**
- (i) completeness and consistency of identification evidence (P1–P3);
- (ii) BO computation from the ownership graph (P4–P5);
- (iii) discrepancy triage and its 14-day report vs request-from-customer route (P6);
- (iv) request-additional-document actions (P11–P12);
- (v) freshness and re-review triggers (P14).

**Caveat for (ii)–(iii).** These still feed a human-reserved decision, so "proceed" means *the agent's determination is passed to the human decision-maker without full re-verification*. The meaningfulness of that human step is exactly what Art. 14(4)(b) (automation bias) and the FSB ("as opposed to oversight that is nominal") worry about. Say so explicitly in the paper.

**Realism point for reviewers.** In this domain, delegation is not about removing humans from final decisions. It is about deciding which *preparatory evidential determinations* humans may accept without redoing them.

---

## C. Cautions — what we must not claim

1. **No compliance claims.** Do not say WorkTrace "ensures", "satisfies" or "is required by" AI Act Arts 12, 13, 14 or 26, AMLR, or NIST. Say "compatible with", "can operationalise", or "provides evidence relevant to".
2. **Dates.**
   - AI Act high-risk requirements (Arts 9–15) and deployer obligations (Art. 26) apply to Annex III systems from **2 Dec 2027**, not 2 Aug 2026 (Reg. (EU) 2026/1744).
   - AMLR applies from **10 Jul 2027**. Before that, the law is national transposition of AMLD4/5.
   - Any sentence of the form "banks must today…" is wrong for both acts.
   - Art. 86's effective scope and date depend on Annex III classification. Do not assert a date for it.
3. **Do not claim corporate counterparty verification is "high-risk" under the AI Act.**
   - Annex III point 5(b) covers creditworthiness and credit scoring of *natural persons*, "with the exception of AI systems used for the purpose of detecting financial fraud". Recital 58 says fraud-detection systems "provided for by Union law" "should not be considered to be high-risk".
   - Recital 59 excludes FIU administrative AML analysis from the law-enforcement category.
   - Annex III 1(a) excludes biometric verification whose "sole purpose … is to confirm that a specific natural person is the person he or she claims to be".
   - KYC/AML of legal entities appears nowhere in Annex III.
   - Correct phrasing: "not listed as high-risk under Annex III as enacted. Classification of a concrete system depends on intended purpose, Art. 6(3) and any Art. 7 delegated amendment, and the Commission's Art. 6 guidelines are still in draft (May 2026) [secondary sources]."
   - The binding AI-relevant rule in our domain is **AMLR Art. 76(5)**, plus GDPR Art. 22 for natural-person BOs (AMLR recital 150).
4. **Do not equate an AI agent with "outsourcing" under AMLR Art. 18, or with "reliance" under Arts 48–50.** Whether a tool is either is an open legal question. EBA GL 4.34 itself asks firms to clarify which applies. We only use Art. 18(3) as evidence that the legislature reserves certain decisions to the obliged entity.
5. **Do not claim the policy is a faithful implementation of AML law.**
   - It is a *synthetic, simplified, public* policy "derived from" the cited provisions, with explicit synthetic parameters (30-day excerpt freshness, source-tier counts, opacity thresholds).
   - Do not present outputs as legal determinations.
   - No real persons, companies, sanctions or PEP lists, and no data or context of the author's employer (per CONTEXT.md §6).
6. **The BO threshold differs by regime.** AMLR: ≥ 25 %. AMLD4: > 25 % (25 % plus one share). FATF: example threshold, maximum 25 %. Say which one the generator uses.
7. **Status of soft law.**
   - NIST AI RMF and 600-1 are voluntary.
   - The FSB report is explicitly non-binding.
   - FCA, ECB and Fed speeches are statements, not rules.
   - EBA/GL/2021/02 is AMLD4-era guidance and is due to be superseded by AMLA instruments.
   - The Fed has *removed* generative and agentic AI from the scope of model-risk guidance (Bowman, 1 May 2026). Do not imply US supervisors expect model validation of agents.
8. **ISO/IEC 42001 was not read.** Cite only at title or scope level, or have someone read it before quoting controls.
9. **FATF version.** I read the October 2025 version via the HK Companies Registry mirror. Re-check against the current FATF PDF, which may be "as amended June 2026" [unverified].
10. **Do not claim the AI Act defines autonomy levels or delegation.** It only says systems "operate with varying levels of autonomy" (recital 12) and that oversight must be commensurate with "level of autonomy" (Art. 14(3)).
11. **Do not overstate the human-oversight gap.** The FSB already states the scaling problem ("impracticality of real-time human monitoring of agent decisions as their use scales") and already proposes performance-triggered transitions and graduated autonomy. Our novelty is method and evaluation, not the policy idea.

---

## Implications for WorkTrace

**Design changes**
1. **Add a "legal envelope" layer to the delegation rule.** For each decision class, set a flag `reserved ∈ {none, human_mandatory}` taken from policy (here AMLR 76(5)(b), 18(3)). The WorkTrace rule only chooses among proceed/escalate/refuse when `reserved = none`. Report risk–coverage curves only over delegable classes, and report the reserved share separately so coverage is not inflated.
2. **Use P6 (AMLR Art. 24(2)(b)) as the flagship intervention example** in the method section. It is the cleanest legally grounded case where adding an independent second source changes the correct action, and removing it changes it back.
3. **Make P12 (EBA GL 1.32/4.34: "a single data source or a single point in time is unlikely to be enough") the policy justification** for the redundancy-robust interventions. This answers the reviewer worry that "add second source" is artificial.
4. **Generator edge cases:** exact-25 % holdings; chain-sum crossings; control-without-ownership; former PEP inside the 12-month window; register excerpt at 29 vs 31 days; outdated register with and without a second reliable source; higher-risk flag disabling the Art. 24(2) exception; a new sanctions designation mid-relationship (Art. 26(4)).
5. **Log schema alignment.** Include in E fields that mirror FSB §2.3 traceability ("what triggered the action; what information and tools it accessed; … whether it acted within its permissions") and AMLR Art. 21(3) ("decisions taken and the relevant supporting documents and justifications"). This gives a one-line governance relevance claim without a compliance claim.
6. **Revocation granularity.** Cite NIST MG-2.4-002 ("for a particular context of use or for the GAI system as a whole") to justify per-class revocation instead of whole-system shutdown.

**Risks**
- **Novelty risk from soft law.** The FSB 2026 report already articulates graduated, performance-triggered autonomy and escalation testing. The FCA calls for "continuous, conditional assurance" and "delegated authority" frameworks. Reviewers in finance will know these, so we must cite them up front and position WorkTrace as the measurable instantiation plus out-of-sample test.
- **Legal-realism risk.** If the case study lets an agent finalise onboarding or EDD decisions, finance reviewers will flag AMLR 76(5)(b) at once. Design change 1 avoids this.
- **Date-drift risk.** The Omnibus, AMLA RTS and the Commission Art. 6 guidelines are all moving. Re-verify every date in the camera-ready.

**Things to cite (verified)**
- Reg. (EU) 2024/1689: Arts 9(8), 12, 13, 14(3)–(4), 26(1)–(2), (5)–(6); recitals 12 and 73; Annex III 1(a), 5(b); recitals 58–59.
- Reg. (EU) 2026/1744: Art. 1 point amending Art. 113.
- NIST AI 100-1: MAP 2.2, MAP 3.5, GOVERN 3.2, MEASURE 2.3, MEASURE 2.5, MANAGE 1.1, MANAGE 2.4, Appendix C. NIST AI 600-1: MS-2.5-001, MG-2.4-002.
- Reg. (EU) 2024/1624: Arts 18(3), 20–26, 42, 45, 51–53, 76(5), 77(3), 90. Dir. (EU) 2024/1640: Art. 10(10). Dir. (EU) 2015/849: Art. 3(6)(a)(i), Art. 30(4), (6).
- FATF R.10, 12, 24, 25; INR.10 fn 38; INR.24 ¶9.
- EBA/GL/2021/02: 1.32, 4.13, 4.15, 4.20–4.22, 4.27, 4.34.
- FSB (15 Oct 2026) SP10 and §3.7(a).
- FCA good-practice publication (Oct 2026) and Rusu speech (Oct 2026).
- Lagarde (1 Oct 2026); Bowman (1 May 2026); BIS FSI Occasional Paper 28 (Sep 2026).
