# Final Submission Readiness Status

Date: 2026-06-03
Project: Analyst Coverage and Subsequent Accounting-Based Financial Stress
Target: Applied Economics Letters

---

## Overall Progress: 80-85%

### ✅ Completed (100%)

1. **Raw Data Download**
   - All Capital IQ data downloaded and audited
   - Company master data ✓
   - Financial statements (including current assets/liabilities, retained earnings) ✓
   - Market data (including market cap, returns, volatility) ✓
   - Analyst estimates ✓
   - Key Developments events ✓
   - Status: 3,005 companies including non-operating status

2. **Data Processing and Cleaning**
   - V2 panel constructed: 21,737 firm-years, 2,335 companies
   - Main estimation sample: 19,322 firm-years after timing audit
   - Strict accounting stress label built: 40.8% event rate
   - Winsorization and standardization complete
   - Analyst timing violations removed

3. **Statistical Analysis**
   - Main logit model: OR = 0.711, p < 0.001 ✓
   - Market split: ASX and Singapore both negative ✓
   - Robustness checks: 11 specifications ✓
   - Prediction performance: AUC and Brier documented ✓
   - Altman and event validation: completed ✓

4. **Manuscript Writing**
   - Strict v2 manuscript complete
   - Conservative framing: information environment marker, not causal
   - Word count appropriate for AEL letter format
   - References complete and formatted
   - Data availability statement: conservative Capital IQ wording

5. **Submission Package**
   - Anonymous manuscript DOCX ✓
   - Title page and declarations DOCX ✓
   - With-author template DOCX ✓
   - Cover letter MD ✓
   - Portal fields ready-to-paste MD ✓
   - Final checklist ✓
   - PDF preview generated ✓
   - Automated checks: PASSED ✓

6. **Version Control**
   - All artifacts committed to GitHub
   - Latest commit: e1b9ccf Record AEL strict v2 local package QA
   - Working tree clean
   - Local data files properly gitignored

---

## ⚠️ Remaining Tasks (15-20%)

### Critical (Must Complete Before Upload)

1. **JCR/Web of Science Real-Time Verification**
   - **Action Required**: Log into institutional JCR/Web of Science account
   - **Verify**: Applied Economics Letters is currently SSCI-indexed and Q3 (or acceptable Q2)
   - **Timeline**: Do this immediately before submission (within 24 hours of upload)
   - **Why**: JCR categories can change between editions

2. **Author Information Confirmation**
   - **Action Required**: Fill in TEMPLATE fields in:
     - `Title_page_and_declarations_strict_v2.docx`
     - `Manuscript_AEL_strict_v2_with_author_details_TEMPLATE.docx` (if using this route)
   - **Details Needed**:
     - Author name
     - Affiliation
     - Email
     - ORCID (if available)
     - Funding statement
     - Conflict of interest statement
     - Ethics approval (if required)

3. **Capital IQ Data License Confirmation**
   - **Action Required**: Confirm current wording is acceptable:
     > "The data used in this study were obtained from S&P Capital IQ under institutional database access and are subject to database licensing and redistribution restrictions."
   - **Check**: Does your institutional license allow this type of academic publication?
   - **Alternative**: If uncertain, contact your library's Capital IQ license administrator

4. **Final Visual QA**
   - **Action Required**: Open `Manuscript_AEL_strict_v2_preview.pdf`
   - **Check**:
     - All tables render correctly
     - No text overflow or cutoff
     - Equations formatted properly
     - Page breaks acceptable
     - References formatted consistently

---

## 📋 Upload Procedure (When Ready)

### Step 1: Pre-Upload Checks
- [ ] JCR verification completed (within 24h)
- [ ] Author details filled in TEMPLATE files
- [ ] Capital IQ license wording approved
- [ ] Final PDF visual QA passed
- [ ] Automated check passed: `python3 scripts/check_ael_strict_v2_package.py`

### Step 2: Go to Taylor & Francis Submission Portal
- URL: https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=rael20
- Log in with your account (or create one)

### Step 3: Upload Files

**Route A (Recommended): Separate Title Page**
1. Main manuscript: `Manuscript_AEL_strict_v2_draft.docx`
2. Title page: `Title_page_and_declarations_strict_v2.docx`
3. Cover letter: Copy text from `Cover_letter_strict_v2.md` and paste into portal
4. Metadata: Use `Portal_fields_ready_to_paste_strict_v2.md` for title, abstract, keywords

**Route B (Alternative): Manuscript with Author Details**
1. Main manuscript: `Manuscript_AEL_strict_v2_with_author_details_TEMPLATE.docx` (after filling TEMPLATE)
2. Cover letter: Copy text from `Cover_letter_strict_v2.md`
3. Metadata: Use `Portal_fields_ready_to_paste_strict_v2.md`

### Step 4: Complete Portal Form
- Article type: Original Research / Empirical Letter
- Subject categories: Finance, Applied Economics
- Suggested reviewers: (Optional, add 2-3 if desired)
- Exclude reviewers: (Optional)
- Open access: Select "No" unless you have APC funding

### Step 5: Review and Submit
- Preview final PDF in portal
- Confirm all fields complete
- Check for any warning messages
- Click "Submit"

---

## 💬 Important Reminders

### Acceptance Rate Reality Check
- **Applied Economics Letters official acceptance rate: 35%**
- This is a Taylor & Francis publicly displayed metric
- Your "70-80%" target is an **internal quality goal**, not the journal's rate
- With thorough preparation, your paper's individual probability could reach 50-60%
- First decision timeline: Average 58 days

### Conservative Positioning
This paper is framed as:
- ✅ Information environment marker
- ✅ Conditional association (not causal)
- ✅ Narrow empirical contribution
- ✅ Two-market evidence (Singapore + Australia)

It explicitly **does NOT claim**:
- ❌ Causal effect of analyst coverage
- ❌ Bankruptcy/default prediction model
- ❌ Machine learning contribution
- ❌ Broad Asia-Pacific generalization
- ❌ Tone or sentiment analysis

### Data Sharing Limitations
- **Do not upload**: Raw Capital IQ exports
- **Do not upload**: Firm-level derived panels with Capital IQ data
- **Can upload**: Aggregate tables, summary statistics, code (without data)
- **Can upload**: Audit reports, variable definitions

---

## 📊 Progress Breakdown

| Component | Status | Completion |
|-----------|--------|------------|
| Raw data download | Complete | 100% |
| Data cleaning and processing | Complete | 100% |
| Statistical analysis | Complete | 100% |
| Manuscript writing | Complete | 100% |
| Submission package | Complete | 100% |
| Automated checks | Passed | 100% |
| **JCR verification** | **Pending** | **0%** |
| **Author details** | **Pending** | **0%** |
| **License confirmation** | **Pending** | **0%** |
| **Final visual QA** | **Pending** | **0%** |
| **Portal upload** | **Not started** | **0%** |

**Overall: 80-85% complete**

---

## 🎯 Next Immediate Actions

1. **JCR Verification** (15 minutes)
   - Log into Web of Science / JCR
   - Search "Applied Economics Letters"
   - Confirm SSCI + Q3 status
   - Screenshot for record

2. **Author Details** (30 minutes)
   - Fill in all TEMPLATE fields
   - Save final versions
   - Run automated check again

3. **Visual QA** (15 minutes)
   - Open PDF preview
   - Check all tables and formatting
   - Confirm acceptable

4. **Upload** (30 minutes)
   - Go to T&F portal
   - Follow Step 3-5 above
   - Submit!

**Total estimated time to complete: ~90 minutes**

---

## 📁 File Locations

All submission files are in:
```
/Users/guohuiwen/华健 论文/9- 金融/submission_package/ael_strict_v2_20260603/
```

Key files:
- `Manuscript_AEL_strict_v2_draft.docx` ← Main upload file
- `Title_page_and_declarations_strict_v2.docx` ← Complete TEMPLATE
- `Cover_letter_strict_v2.md` ← Copy to portal
- `Portal_fields_ready_to_paste_strict_v2.md` ← Metadata
- `Final_upload_checklist_strict_v2.md` ← Step-by-step guide

---

## ✅ Sign-Off

This paper is ready for submission pending the 4 remaining tasks above.

Data work is complete. Analysis is complete. Writing is complete. Package is built and verified.

**The paper is now in your hands for final author confirmation and upload.**

Good luck! 🚀
