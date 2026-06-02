# SSCI/JCR Q3 Target Route Refresh

Date: 2026-06-03

## Decision

Status: PRIMARY_ROUTE_SELECTED_AEL_STRICT_V2_NOT_FINAL_UPLOAD

The current strict-accounting-stress manuscript should not be positioned as a causal finance paper, a bankruptcy-prediction paper, or a machine-learning paper. It should be submitted as a narrow applied empirical economics/finance paper: analyst coverage as an information-environment marker associated with lower subsequent accounting-based stress in Singapore and Australia.

Primary route selected after this refresh: Applied Economics Letters strict v2 short article.

Current primary-route artifacts:

- `manuscript/ael_strict_accounting_stress_v2_letter.md`
- `manuscript/ael_strict_accounting_stress_v2_submission.docx`
- `outputs/ael_strict_v2_submission_audit_20260603.md`
- `scripts/check_ael_strict_v2_package.py`

The raw-data download gate is complete for this claim boundary. More blind downloading is not the right next step. Additional data downloads are only justified if the paper expands into one of these claims:

- direct-ID bankruptcy/default/Key Developments event outcomes;
- tone or text-quality measures;
- industry-based exclusions or industry fixed effects.

## Current Data Answer

If all required data equals raw Capital IQ downloads needed for the current strict-accounting-stress route: 100%.

If all required data equals a journal-facing data package with unified cleaning, leakage checks, sample freeze, labels, model tables, and audit trail: about 90-92%.

If all required work equals final portal-ready paper submission: about 60-65%.

The gap is no longer mainly raw download volume. The gap is journal fit, final formatting, final upload QA, and conservative language around event-ID and tone limitations.

## Evidence Refreshed Online

### Applied Economics

- Publisher page: https://www.tandfonline.com/journals/raec20/about-this-journal
- Public publisher metrics observed in search cache: 2024 Impact Factor 2.1, Q2 Impact Factor Best Quartile, 40% acceptance rate, 53 days average first decision.
- Indexing/scope note observed in the publisher cache: peer-reviewed applied-economics journal, SSCI-indexed.

Assessment:

- Strongest if the user accepts "JCR Q3 and above" as including Q2.
- Better for a full-length applied empirical paper than a letter journal.
- Official acceptance rate is 40%, not 70-80%; a 70-80% paper-level probability would be an internal target after fit polishing, not an official journal rate.

### Applied Economics Letters

- Publisher page: https://www.tandfonline.com/journals/rael20/about-this-journal
- Public publisher metrics observed in search cache: 2024 Impact Factor 1.3, 2024 5-year IF 1.3, 2024 CiteScore 3.2, Q2 CiteScore Best Quartile, 35% acceptance rate, 58 days average first decision.
- Public JCR/Q3 supporting pages:
  - https://journalsimpactfactors.com/journal.php?id=12088
  - https://jrank.net/journals/appl-econ-lett/metrics
  - https://scholar.pusan.ac.kr/journals/9148/

Assessment:

- Best fit if the manuscript is converted into a concise empirical letter.
- Current draft is close in length but has too many tables for a clean letter submission. Compress to 2 main tables plus appendix if choosing this route.
- Official acceptance rate is 35%; no credible basis to call the journal itself 70-80%.

### Asia-Pacific Journal of Financial Studies

- Journal homepage: https://onlinelibrary.wiley.com/journal/20416156
- Public WoS/JCR supporting pages:
  - https://wos-journal.info/journalid/20795
  - https://journalsearches.com/journal.php?title=asia-pacific+journal+of+financial+studies
  - https://library.utem.edu.my/phocadownload/Research-Resources/JCR2024%20Updated%20July2025.pdf

Assessment:

- Region and finance fit are attractive.
- Public sources conflict between Q2 and Q3 depending on year/metric; verify in the live JCR account before final submission.
- No official acceptance rate was found in public publisher snippets during this refresh.
- Higher review risk than Applied Economics Letters because the current identification is deliberately associative and not a strong finance-design contribution.

### Singapore Economic Review

- Journal homepage: https://www.worldscientific.com/worldscinet/ser
- Public WoS/JCR supporting pages:
  - https://wos-journal.info/journalid/20070
  - https://journalsearches.com/journal.php?title=singapore+economic+review
  - https://www.ablesci.com/journal/detail?id=po0O75

Assessment:

- Good regional fit because Singapore is a core sample market and the paper has an applied Asia-Pacific framing.
- Public sources show SSCI and Q3/Q2-type evidence depending on year/metric; verify in live JCR before final lock.
- No official acceptance rate was found in public publisher snippets during this refresh.
- The paper must be framed as applied economics, not corporate-finance causality.

### Economic Record

- Journal homepage: https://onlinelibrary.wiley.com/journal/14754932
- Public JCR/Q3 supporting pages:
  - https://journalsimpactfactors.com/journal.php?id=12654
  - https://journalmetrics.org/journal/economic-record
  - https://library.utem.edu.my/phocadownload/Research-Resources/JCR2024%20Updated%20July2025.pdf

Assessment:

- Strong Australia angle, established economics outlet, public Q3 evidence.
- Lower article volume and no official acceptance rate found; probably not the safest route for a fast 70-80% internal probability target.
- Use as backup if the narrative is rewritten toward Australia/Singapore applied economics rather than finance.

## Recommended Submission Sequence

1. Applied Economics Letters, using the strict v2 short draft.
2. Applied Economics, if Q2 is acceptable under "Q3 or above" and a full article is preferred.
3. Singapore Economic Review, if regional Asia/Singapore fit is prioritized.
4. Economic Record, if Australia/economics fit is prioritized and slower review risk is acceptable.
5. Asia-Pacific Journal of Financial Studies only after strengthening finance contribution language or obtaining cleaner event-ID evidence.

## Reviewer-Level Risk Calibration

The current package is not a "no-risk" 70-80% submission. The hard risks are:

- endogeneity: analyst coverage is not randomly assigned;
- label defensibility: strict accounting stress is defensible, but it is still broad relative to legal default/bankruptcy;
- event evidence: Key Developments labels are candidate-level without clean direct baseline Entity ID alignment;
- Altman evidence: full-component coverage is limited, so Altman must remain robustness-only;
- tone/text: no tone dataset is merged, so tone must not be claimed;
- journal fit: Applied Economics and Applied Economics Letters have official acceptance rates of only 40% and 35%.

## Next Actions

1. Verify Applied Economics Letters in live JCR or institutional WoS access immediately before submission.
2. Regenerate strict-route title page, declarations, cover letter, and portal fields.
3. Rerender the exact final DOCX/PDF after author/declaration formatting.
4. Keep the raw data frozen unless the selected journal route requires a direct-ID event outcome or text/tone extension.
