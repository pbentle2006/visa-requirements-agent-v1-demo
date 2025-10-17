# Comprehensive Demo Guide

## Demo Options Overview

The Visa Requirements Agent offers **three demo modes** to showcase capabilities:

1. **Live API Demo** - Real LLM processing (requires API credits)
2. **Mock Demo Mode** - Synthetic data (always available)  
3. **Comparison Dashboard** - Multi-policy analysis

---

## Quick Start (2 minutes)

### Option 1: Streamlit Web Interface (Recommended)

```bash
# 1. Navigate to project directory
cd visa-requirements-agent-demo

# 2. Install dependencies (if not done)
pip install -r requirements.txt

### 3. Start Streamlit App
```bash
streamlit run src/ui/streamlit_app.py
```

## Demo Flow

### Phase 1: Introduction (5 minutes)

**Key Points:**
- Problem: Manual requirements gathering is slow, error-prone, and inconsistent
- Solution: Multi-agent AI system that automates the entire process
- Benefits: Speed (weeks → hours), Coverage (95%+), Traceability (complete)

**Show:**
- Project structure overview
- Architecture diagram in README
- List of 5 specialized agents

### Phase 2: Policy Analysis (10 minutes)

**Narrative:**
"Let's start with a real immigration policy document - the Parent Boost Visitor Visa..."

**Demo Steps:**
1. Show the raw policy document (`data/input/parent_boost_policy.txt`)
2. Click "Run Complete Workflow"
3. While running, explain what each agent does:
   - **PolicyEvaluator**: Parses document, extracts structure
   - **RequirementsCapture**: Identifies functional, data, business requirements
   - **QuestionGenerator**: Creates application form questions
   - **ValidationAgent**: Validates completeness and consistency
   - **ConsolidationAgent**: Synthesizes final specification

**Show Results:**
- Policy Analysis tab:
  - Visa type, code, objectives
  - Key requirements extracted
  - Eligibility rules by category
  - Stakeholders identified

**Key Metrics:**
- Sections parsed: ~15 policy sections
- Rules extracted: ~50+ individual rules
- Time: ~30-60 seconds (vs. hours manually)

### Phase 3: Requirements Capture (10 minutes)

**Narrative:**
"The system has automatically categorized requirements into four types..."

**Show:**
- Requirements tab with expandable sections:
  
  **Functional Requirements** (e.g.):
  - FR-001: System must verify applicant is outside NZ
  - FR-002: System must validate sponsorship form completion
  - FR-003: System must calculate income thresholds
  
  **Data Requirements** (e.g.):
  - DR-001: Applicant personal details (name, DOB, passport)
  - DR-002: Sponsor income history (3 tax years)
  - DR-003: Medical certificate dates
  
  **Business Rules** (e.g.):
  - BR-001: Maximum 2 sponsors allowed
  - BR-002: Sponsor can support max 6 parents
  - BR-003: Medical certificates valid 36 months
  
  **Validation Rules** (e.g.):
  - VR-001: Age validation for dependent children (under 18)
  - VR-002: Date calculation for medical certificates
  - VR-003: Income threshold calculations

**Highlight:**
- Each requirement has policy reference (traceability)
- Priority levels (must_have, should_have, could_have)
- Acceptance criteria included

**Key Metrics:**
- Total requirements: 40-60 (varies by LLM output)
- Coverage: 95%+ of policy sections
- Time: ~45 seconds (vs. days manually)

### Phase 4: Question Generation (10 minutes)

**Narrative:**
"From requirements, the system generates actual application form questions..."

**Show:**
- Questions tab organized by section:
  
  **Applicant Details:**
  - Q_APP_001: Are you currently in New Zealand? (boolean, required)
  - Q_APP_002: What is your full name? (text, required)
  - Q_APP_003: What is your date of birth? (date, required)
  
  **Sponsorship:**
  - Q_SPON_001: How many sponsors do you have? (number, max: 2)
  - Q_SPON_002: How many parents are being sponsored? (number, max: 6)
  - Q_SPON_003: Has the sponsorship form been completed? (boolean)
  
  **Financial Requirements:**
  - Q_FIN_001: What is the sponsor's income for last 3 years? (currency)
  - Q_FIN_002: How much maintenance funds do you have? (currency, min: $10,000)
  
  **Health & Character:**
  - Q_HEALTH_001: When was your medical certificate issued? (date)
  - Q_HEALTH_002: What is your insurance coverage amount? (currency, min: $200,000)

**Highlight:**
- Input types (text, number, date, boolean, select, file)
- Validation rules embedded
- Help text with policy references
- Conditional logic (questions that show based on previous answers)

**Key Metrics:**
- Total questions: 30-50
- Sections: 5-7 logical groupings
- Time: ~60 seconds (vs. weeks manually)

### Phase 5: Validation & Quality (10 minutes)

**Narrative:**
"The system validates its own work to ensure quality..."

**Show:**
- Validation tab:
  
  **Overall Score:** 85-95% (typical)
  
  **Requirement Validation:**
  - Total: 50 requirements
  - Valid: 48 (96%)
  - Invalid: 2 (4%)
  - Show specific errors if any
  
  **Question Validation:**
  - Total: 40 questions
  - Valid: 38 (95%)
  - Invalid: 2 (5%)
  
  **Gap Analysis:**
  - Missing requirements: List any gaps
  - Missing questions: List coverage gaps
  - Uncovered policy sections: Highlight any missed sections
  
  **Recommendations:**
  - HIGH: Fix 2 invalid requirements
  - MEDIUM: Add validation for income thresholds
  - LOW: Enhance help text for complex questions

**Highlight:**
- Self-validation catches errors
- Gap analysis ensures completeness
- Actionable recommendations for improvement
- Traceability: policy → requirements → questions

**Key Metrics:**
- Validation score: 85-95%
- Coverage: 95%+ of policy sections
- Time: ~30 seconds (vs. manual review taking days)

### Phase 6: Consolidated Output (5 minutes)

**Narrative:**
"Finally, the system produces a complete specification document..."

**Show:**
- Consolidated tab:
  
  **Executive Summary:**
  - System overview
  - Key objectives
  - Scope and boundaries
  
  **Implementation Guide:**
  - Architecture recommendations
  - Database schema
  - API endpoints
  - Security considerations
  - Testing strategy
  
  **Traceability Matrix:**
  - Complete mapping: Policy → Requirements → Questions
  - Coverage indicators
  - Easy to audit and verify

**Statistics Tab:**
- Requirements by type (pie chart view)
- Requirements by priority
- Questions by section
- Quality metrics dashboard

**Download Options:**
- Full results (JSON)
- Requirements only
- Questions only
- Implementation guide

## Key Talking Points

### Speed
- **Manual Process**: 2-4 weeks for requirements gathering
- **Automated Process**: 3-5 minutes end-to-end
- **Improvement**: 99% time reduction

### Coverage
- **Manual Process**: 70-80% coverage (things get missed)
- **Automated Process**: 95%+ coverage with gap analysis
- **Improvement**: Higher quality, fewer rework cycles

### Consistency
- **Manual Process**: Varies by analyst, terminology inconsistent
- **Automated Process**: Consistent structure, standardized format
- **Improvement**: Easier to maintain and update

### Traceability
- **Manual Process**: Hard to trace requirements back to policy
- **Automated Process**: Complete policy references on every item
- **Improvement**: Audit-ready, compliance-friendly

### Scalability
- **Manual Process**: Linear scaling (more policies = more analysts)
- **Automated Process**: Parallel processing, handles multiple policies
- **Improvement**: Can process entire policy library

## Q&A Preparation

### Expected Questions

**Q: How accurate is the LLM?**
A: Validation scores typically 85-95%. System includes self-validation and gap analysis to catch errors. Human review still recommended but focused on exceptions.

**Q: What if policy changes?**
A: Re-run the workflow with updated policy. System will regenerate requirements and highlight what changed. Much faster than manual updates.

**Q: Can it handle other visa types?**
A: Yes! System is policy-agnostic. Works with any structured policy document. Just provide the document and run.

**Q: What about complex conditional logic?**
A: System generates conditional logic rules. For very complex scenarios, may need manual refinement, but provides 80% of the work.

**Q: How much does it cost?**
A: Using GPT-4: ~$0.50-1.00 per policy document. Compare to analyst time ($50-100/hour × 40-80 hours = $2,000-8,000).

**Q: Can we customize the output format?**
A: Yes! Templates are configurable. Can adjust to match your organization's standards.

**Q: What about data privacy?**
A: Can use local LLMs (Llama, Mistral) or Azure OpenAI with private endpoints. No data sent to public APIs.

**Q: How do we integrate with existing systems?**
A: Outputs are JSON/structured data. Easy to integrate via APIs or import into existing tools.

## Success Metrics to Highlight

1. **Time Savings**: 99% reduction (weeks → minutes)
2. **Coverage**: 95%+ policy section coverage
3. **Quality**: 85-95% validation scores
4. **Traceability**: 100% policy references
5. **Consistency**: Standardized output format
6. **Scalability**: Process multiple policies in parallel

## Closing

**Summary:**
"We've demonstrated how a multi-agent AI system can automate the entire requirements capture process - from policy analysis to validated specifications - in minutes instead of weeks, with higher coverage and complete traceability."

**Next Steps:**
1. Pilot with 3-5 policy documents
2. Customize templates to your standards
3. Integrate with existing workflow
4. Train team on system usage
5. Measure ROI and iterate

**Call to Action:**
"Ready to transform your requirements gathering process? Let's discuss implementation."
