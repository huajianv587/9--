# Strict SCIE/SSCI Q3 70-80% Feasibility Audit

Date: 2026-06-01
Project: Analyst coverage and future financial stress

Latest update: Round 16 current-source recheck on 2026-06-02 still did not verify a scope-fitting regular SSCI/SCIE Q3 single journal with credible 70-80% acceptance evidence. See `docs/regular_scie_ssci_q3_journal_screen_round16_20260602.md`.

## User Requirement

The required target is:

**SCIE or SSCI indexed journal, Q3 level, with a stable 70-80% acceptance likelihood.**

This is stricter than the previous project-level ladder target. It requires all three conditions at the same time:

1. SCIE/SSCI indexed, not merely ESCI or Scopus.
2. Q3, not Q1/Q2 unless the evaluation rule accepts higher quartiles as better than Q3.
3. Realistic acceptance likelihood near 70-80%, not just a multi-journal aspiration.

## Current Paper Status

The manuscript and package are technically ready for a conservative analyst-coverage route:

- Main result: analyst coverage odds ratio = 0.568, p < 0.001.
- Conservative label-component robustness: odds ratio = 0.564, p < 0.001.
- Trimmed propensity-score common-support robustness: odds ratio = 0.591, p < 0.001.
- IPTW propensity-score weighted robustness: odds ratio = 0.659, p < 0.001.
- Market-year size-decile fixed-effects robustness: odds ratio = 0.621, p < 0.001.
- Sample: 19,402 labelled firm-years, 12,303 stress events.
- Claim boundary: no causality, no strong prediction-performance claim, no disagreement-title overclaim.
- Submission package check: `scripts/check_ael_submission_package.py` passes.

This is sufficient for a serious SCIE/SSCI submission. It does **not** prove a 70-80% acceptance probability at a strict Q3 outlet.

## Current Verified Outlets

| Outlet | Index/quartile signal | Official/public acceptance signal | Fit | Strict 70-80 Q3 target? |
|---|---|---:|---|---|
| Applied Economics Letters | SSCI; public mirrors show Economics Q3 | 35% official T&F acceptance rate | Strong fit for short empirical letter | No |
| Applied Economics | SSCI; T&F displays Q2 best quartile | 40% official T&F acceptance rate | Strong transfer fit | No: not Q3 and not 70-80 |
| Emerging Markets Finance and Trade | SSCI; T&F displays Q1 best quartile | 33% official T&F acceptance rate | Weak fit for Singapore/Australia | No |
| Eastern European Economics | SSCI; public mirrors report Q3 | no useful official high acceptance signal | Poor geographic fit | No |
| Journal of Behavioral Finance | SSCI; behavioral finance scope | no official high acceptance signal; secondary sources suggest low selectivity historically | Weak fit because disagreement evidence is mixed | No |
| Emerald finance/econ candidates checked | mostly ESCI in public pages or low acceptance | 5-29% range in public snippets | mixed | No |
| South African Journal of Economic and Management Sciences | official page indicates WoS/SSCI-style status and broad economics/finance/management scope | no useful official high acceptance signal found | Weak regional fit for Singapore/Australia sample | No |
| Journal of Economics and Finance | Springer public page shows ESCI/Scopus-type status | no useful official high acceptance signal found | Scope partly related | No: not strict SSCI/SCIE |
| Quantitative Finance | reputable quantitative-finance scope | no useful official high acceptance signal found | Weaker fit than APJFS for this empirical panel paper | No |
| Cogent Economics & Finance | Taylor & Francis shows Q1 best quartile and ESCI indexing | 17% official T&F acceptance rate | Broad economics/finance fit but open-access/ESCI route | No |
| Cogent Business & Management | Taylor & Francis shows Q2 best quartile | 20% official T&F acceptance rate | Broad business fit but not finance-specific | No |
| Transnational Corporations Review | Taylor & Francis shows ESCI/Scopus and TNC/FDI scope | 32% official T&F acceptance rate | Wrong scope and not strict SSCI/SCIE in publisher-facing evidence | No |
| Transformations in Business & Economics | public profiles show SSCI/Q3-type business/economics signals | no current official high acceptance found; historical editorial says 10-12% | Broad business/economics, but not higher probability than APJFS | No |
| International Economic Journal | Taylor & Francis shows broad economics scope but ESCI-style indexing | 8% official T&F acceptance rate | Weak fit for this corporate finance panel | No |
| Economic Research-Ekonomska Istraživanja | Taylor & Francis shows broad economics scope and visible Scopus-style metrics | 22% official T&F acceptance rate | Broad but not strict verified Q3/SSCI in the current visible metrics | No |
| Quantitative Finance | Taylor & Francis shows Q2 Impact Factor best quartile | 23% official T&F acceptance rate | Reputable but poor fit for a compact listed-firm analyst-coverage panel | No |
| Managerial Finance | Emerald lists finance-relevant scope/indexing but publisher-facing WoS status is ESCI | 16.3% official Emerald acceptance rate | Scope is plausible, but strict index/probability fail | No |
| Journal of Financial Economic Policy | Emerald lists broad financial economics and policy scope | 13.5% official Emerald acceptance rate | Plausible finance scope but far below 70-80 | No |
| Journal of Financial Crime | Emerald lists economics/finance directories and Scopus | 18.5% official Emerald acceptance rate | Wrong-scope and far below target | No |
| Multinational Business Review | Emerald lists SSCI and 2024 Impact Factor 2.7 | 11.9% official Emerald acceptance rate | Reputable but wrong-scope and too selective | No |
| Baltic Journal of Management | Emerald lists JCR and Social Sciences Citation Index | 5.7% official Emerald acceptance rate | Strict-index business/management example, but wrong-scope and too selective | No |
| Singapore Economic Review | public JCR export lists Economics, SSCI, Q3 | no official high acceptance signal found | Better Asia/economics fit than many backups, but not finance-specific and probability unverified | No |
| Academia Revista Latinoamericana de Administracion | public JCR export lists Management and Business, SSCI, Q3 | 18.7% official Emerald acceptance rate | Some finance/capital-market scope, but Latin America orientation and low acceptance | No |
| Global Economic Review | Taylor & Francis lists SSCI and Asia/East Asia economics scope | 6% official T&F acceptance rate | Some Asia/economics fit but too selective and not Q3 in T&F best quartile | No |
| German Economic Review | public JCR export lists Economics, SSCI, Q3 | no official high acceptance signal found | Regular economics outlet but weaker manuscript fit and no 70-80 evidence | No |
| Amfiteatru Economic | public JCR export lists Economics SSCI Q2 and Management/Business SSCI Q3 | no official high acceptance signal found | Broad business/economics, not a clean finance fit and no 70-80 evidence | No |
| Australian Journal of Management | public JCR export lists Management and Business, SSCI, Q3 | 4.5% official SAGE acceptance rate | Reputable and regionally plausible, but far too selective and management-facing | No |
| International Finance | public JCR export lists Business, Finance, SSCI, Q3 and Economics, SSCI, Q2 | no official high acceptance signal found | Clean finance status but more international macro-finance/policy than firm-level analyst coverage | No |
| Accounting and Business Research | public JCR export lists Business, Finance, SSCI, Q3 | no official high acceptance signal found; accounting scope is restrictive | Reputable but the current paper is not primarily accounting | No |
| Journal of Post Keynesian Economics | public JCR export lists Economics, SSCI, Q3 | 21% official T&F acceptance rate | Poor scope fit for firm-level analyst coverage and financial stress | No |
| Review of Pacific Basin Financial Markets and Policies | public JCR export lists Business, Finance, ESCI, Q4 | no official high acceptance signal used | Pacific Basin fit but fails strict SSCI/SCIE Q3 | No |
| Quarterly Journal of Finance | public JCR export lists Business, Finance, ESCI, Q4 | no official high acceptance signal used | Finance journal but fails strict SSCI/SCIE Q3 | No |
| Journal of Pension Economics & Finance | public JCR evidence lists Business, Finance, SSCI, Q3 | no official high acceptance signal found | Wrong substantive scope: pensions and retirement income | No |
| International Journal of Auditing | public JCR evidence lists Business, Finance, SSCI, Q3 | no current official high acceptance signal found | Wrong substantive scope: auditing and assurance | No |
| International Journal of Health Economics and Management | public JCR evidence lists Business, Finance, SSCI, Q3 | no relevant high acceptance signal found | Wrong substantive scope: health-care systems and health economics | No |
| International Journal of Finance & Economics | public JCR evidence lists Business, Finance, SSCI, but current visible signal is Q2 rather than Q3 | no official high acceptance signal found | Plausible topic fit, but not strict Q3/70-80 | No |
| International Review of Finance | public JCR evidence lists Business, Finance, SSCI, but current visible JIF signal is Q2 | no official high acceptance signal found | Better finance fit, but not high-probability Q3 route | No |
| Forest Science and Technology | publisher page shows Impact Factor metrics and 60% acceptance | 60% official T&F acceptance rate | Wrong field: forestry/natural resources | No |
| Journal of Wine Research | publisher page shows 50% acceptance | 50% official T&F acceptance rate | Wrong field: wine/viticulture/oenology | No |
| Asian Journal of Sport History & Culture | publisher page shows 55% acceptance | 55% official T&F acceptance rate | Wrong field: sport history/culture | No |
| The Italianist | publisher page shows 70% acceptance | 70% official T&F acceptance rate | Wrong field: Italian studies | No |
| Substance Use & Misuse | publisher page shows 45% acceptance | 45% official T&F acceptance rate | Wrong field: substance-use/public-health | No |
| Business & Society | reputable SAGE business journal; not a Q3 stability target | less than 5% SAGE editorial acceptance-rate evidence | Wrong contribution level and too selective | No |
| Organizational Research Methods | reputable SAGE management-methods journal | around 15% SAGE editorial acceptance-rate evidence | Wrong field and too selective | No |
| Finance Research Letters | Elsevier page lists SSCI, Impact Factor 6.9, broad finance scope | 35% official Elsevier acceptance rate | Strong scope fit, but not Q3 and not 70-80 | No |
| Financial Innovation | Springer page lists SSCI and broad financial-innovation/fintech scope | no high acceptance-rate signal used | Wrong framing for an analyst-coverage stress paper | No |
| Asia-Pacific Financial Markets | Springer page shows regional finance scope and subscription/OA options | no official high acceptance-rate signal found | Scope-adjacent but not verified as strict current Q3/70-80 route | No |
| Round 16 recheck | public JCR 2024 export confirms APJFS, Economic Record, AEL, Asia-Pacific Journal of Accounting & Economics, JBEM, and International Finance index/quartile signals | no credible official 70-80 single-journal acceptance evidence found for a scope-fitting regular finance/economics outlet | Reinforces current APJFS-first ladder; rejects secondary/promotional 80% claims | No |

## Interpretation

Current evidence supports:

- **SCIE/SSCI submission-ready:** yes.
- **Q3-compatible paper:** yes, especially for Applied Economics Letters-type applied-economics outlets.
- **Single-journal 70-80% acceptance at a reputable SCIE/SSCI Q3 journal:** no evidence.
- **Project-level probability after a ladder:** roughly 65-75% only as a sequential portfolio estimate, using the current full-paper route first and AEL only as a compressed fallback.

The exact user target, "SCIE/SSCI Q3 with 70-80% stable acceptance," is therefore **not yet achieved**.

## Why It Is Not Yet Achieved

1. Reputable SCIE/SSCI economics and finance journals rarely publish official acceptance rates near 70-80%.
2. Publicly visible high-acceptance-rate journals found in broad web search are usually wrong-field, ESCI-only, non-SSCI, or not credible enough for this target.
3. The current paper is empirical finance/applied economics. It cannot be honestly redirected to a geology, medical, or unrelated high-acceptance SCIE journal.
4. Scope fit matters more than raw acceptance rate. A nominal high-acceptance journal outside scope increases desk-rejection risk.

## Practical Decision

The current paper should **not** be represented as already meeting a strict 70-80% Q3 acceptance target.

There are three honest options:

1. **Submit now to AEL:** good fit, but official acceptance is 35%; not the user's requested probability.
2. **Use a ladder:** AEL plus Applied Economics plus a verified Q3 backup; realistic project-level target around 65-75%, possibly near 70 if the Q3 backup is strong.
3. **Pause and search specifically for a true Q3 high-acceptance outlet:** required if the user will not accept anything below a credible 70-80% probability.

## Required Next Step to Meet the Exact Target

Run a dedicated current-JCR / Master Journal List screen for:

- SCIE or SSCI only;
- JCR Q3 or institutionally accepted Q3 equivalent;
- economics, finance, risk, business, decision sciences, data science, or applied statistics scope;
- official or credible acceptance signal above 50%, ideally 60-70%+;
- no predatory or warning-list concerns;
- clear acceptance of empirical company-level panel/logit papers;
- APC acceptable to the user.

Until such an outlet is found and the manuscript is remapped to its scope, the exact 70-80% Q3 target remains unproven.

## Sources Checked

- Applied Economics Letters official T&F page: https://www.tandfonline.com/journals/rael20/about-this-journal
- Applied Economics official T&F page: https://www.tandfonline.com/journals/raec20/about-this-journal
- Taylor & Francis Open Select page: https://authorservices.taylorandfrancis.com/choose-open/publishing-open-access/open-select/
- Round 5 additional screen: `docs/regular_scie_ssci_q3_journal_screen_round5_20260601.md`
- Round 6 broad-journal screen: `docs/regular_scie_ssci_q3_journal_screen_round6_20260601.md`
- Round 7 additional official-metrics screen: `docs/regular_scie_ssci_q3_journal_screen_round7_20260601.md`
- Round 8 Emerald official-metrics screen: `docs/regular_scie_ssci_q3_journal_screen_round8_20260601.md`
- Round 9 cross-publisher regional economics/business screen: `docs/regular_scie_ssci_q3_journal_screen_round9_20260601.md`
- Round 10 additional finance/accounting/management fit screen: `docs/regular_scie_ssci_q3_journal_screen_round10_20260601.md`
- Round 11 Business-Finance boundary screen: `docs/regular_scie_ssci_q3_journal_screen_round11_20260601.md`
- Round 12 official high-acceptance signal screen: `docs/regular_scie_ssci_q3_journal_screen_round12_20260601.md`
- Round 13 SAGE business/management acceptance-rate screen: `docs/regular_scie_ssci_q3_journal_screen_round13_20260601.md`
- Round 14 direct finance-journal screen: `docs/regular_scie_ssci_q3_journal_screen_round14_20260601.md`
- Round 16 current-source recheck: `docs/regular_scie_ssci_q3_journal_screen_round16_20260602.md`
