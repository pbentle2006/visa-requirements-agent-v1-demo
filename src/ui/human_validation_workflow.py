"""
Human-in-the-Loop Validation Workflow
Provides validation capabilities with human review, editing, and approval workflow.
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any

def show_human_validation_workflow(workflow_results: Dict[str, Any]):
    """Display the human-in-the-loop validation workflow interface."""
    
    st.title("👥 Human-in-the-Loop Validation Workflow")
    st.markdown("**Review, validate, and improve generated requirements and questions before finalizing the visa application process.**")
    
    if not workflow_results:
        st.warning("⚠️ No workflow results available. Please run the main workflow first.")
        return
    
    # Initialize session state for validation workflow
    if 'validation_state' not in st.session_state:
        st.session_state.validation_state = {
            'current_step': 1,
            'requirements_approved': False,
            'questions_approved': False,
            'final_approved': False,
            'edited_questions': {},
            'validation_notes': {},
            'approval_timestamp': None
        }
    
    # Workflow Progress Indicator
    show_validation_progress()
    
    # Step-by-step validation workflow
    current_step = st.session_state.validation_state['current_step']
    
    if current_step == 1:
        show_requirements_validation(workflow_results)
    elif current_step == 2:
        show_questions_validation(workflow_results)
    elif current_step == 3:
        show_final_approval(workflow_results)
    elif current_step == 4:
        show_completion_summary(workflow_results)

def show_validation_progress():
    """Display the validation workflow progress indicator."""
    
    st.markdown("## 🔄 Validation Workflow Progress")
    
    steps = [
        "📋 Requirements Review",
        "❓ Questions Validation", 
        "✅ Final Approval",
        "🎉 Completion"
    ]
    
    current_step = st.session_state.validation_state['current_step']
    
    # Create progress visualization
    cols = st.columns(4)
    for i, (col, step) in enumerate(zip(cols, steps), 1):
        with col:
            if i < current_step:
                st.success(f"✅ {step}")
            elif i == current_step:
                st.info(f"🔄 {step}")
            else:
                st.secondary(f"⏳ {step}")
    
    st.divider()

def show_requirements_validation(workflow_results: Dict[str, Any]):
    """Step 1: Requirements validation and review."""
    
    st.markdown("## 📋 Step 1: Requirements Validation")
    st.markdown("Review the generated requirements for accuracy and completeness.")
    
    # Extract requirements from workflow results
    requirements = extract_requirements_data(workflow_results)
    
    # Requirements overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Functional Requirements", len(requirements.get('functional', [])))
    with col2:
        st.metric("Data Requirements", len(requirements.get('data', [])))
    with col3:
        st.metric("Business Rules", len(requirements.get('business', [])))
    with col4:
        st.metric("Validation Rules", len(requirements.get('validation', [])))
    
    # Detailed requirements review
    tabs = st.tabs(["📊 Functional", "📝 Data", "⚖️ Business Rules", "✅ Validation"])
    
    with tabs[0]:
        show_requirements_section("Functional Requirements", requirements.get('functional', []))
    
    with tabs[1]:
        show_requirements_section("Data Requirements", requirements.get('data', []))
    
    with tabs[2]:
        show_requirements_section("Business Rules", requirements.get('business', []))
    
    with tabs[3]:
        show_requirements_section("Validation Rules", requirements.get('validation', []))
    
    # Requirements approval
    st.markdown("### 🎯 Requirements Approval")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        requirements_feedback = st.text_area(
            "Requirements Review Notes:",
            placeholder="Add any notes about the requirements quality, completeness, or needed improvements...",
            height=100
        )
    
    with col2:
        st.markdown("**Quality Score**")
        requirements_score = st.slider("Requirements Quality", 0, 100, 85, help="Rate the overall quality of the requirements")
        
        if requirements_score >= 80:
            st.success(f"✅ Excellent ({requirements_score}%)")
        elif requirements_score >= 60:
            st.warning(f"⚠️ Good ({requirements_score}%)")
        else:
            st.error(f"❌ Needs Improvement ({requirements_score}%)")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Regenerate Requirements", type="secondary"):
            st.info("🔄 Requirements regeneration would trigger here in full implementation")
    
    with col2:
        if st.button("📝 Edit Requirements", type="secondary"):
            st.info("📝 Requirements editing interface would open here")
    
    with col3:
        if st.button("✅ Approve Requirements", type="primary"):
            st.session_state.validation_state['requirements_approved'] = True
            st.session_state.validation_state['current_step'] = 2
            st.session_state.validation_state['validation_notes']['requirements'] = {
                'feedback': requirements_feedback,
                'score': requirements_score,
                'timestamp': datetime.now().isoformat()
            }
            st.success("✅ Requirements approved! Moving to questions validation...")
            st.rerun()

def show_questions_validation(workflow_results: Dict[str, Any]):
    """Step 2: Questions validation with editing capabilities."""
    
    st.markdown("## ❓ Step 2: Questions Validation & Editing")
    st.markdown("Review and edit the generated application questions.")
    
    # Extract questions from workflow results
    questions = extract_questions_data(workflow_results)
    
    # Questions overview
    total_questions = sum(len(section_questions) for section_questions in questions.values())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", total_questions)
    with col2:
        st.metric("Question Sections", len(questions))
    with col3:
        avg_score = calculate_questions_quality_score(questions)
        st.metric("Avg Quality Score", f"{avg_score}%")
    with col4:
        edited_count = len(st.session_state.validation_state.get('edited_questions', {}))
        st.metric("Questions Edited", edited_count)
    
    # Questions editing interface
    st.markdown("### 📝 Question Review & Editing")
    
    for section_name, section_questions in questions.items():
        with st.expander(f"📋 {section_name} ({len(section_questions)} questions)", expanded=True):
            show_questions_editing_section(section_name, section_questions)
    
    # Overall questions assessment
    st.markdown("### 🎯 Questions Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        questions_feedback = st.text_area(
            "Questions Review Notes:",
            placeholder="Add notes about question clarity, completeness, user-friendliness...",
            height=100
        )
    
    with col2:
        questions_score = st.slider("Questions Quality", 0, 100, 88, help="Rate the overall quality of the questions")
        
        if questions_score >= 85:
            st.success(f"✅ Excellent ({questions_score}%)")
        elif questions_score >= 70:
            st.warning(f"⚠️ Good ({questions_score}%)")
        else:
            st.error(f"❌ Needs Improvement ({questions_score}%)")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Requirements", type="secondary"):
            st.session_state.validation_state['current_step'] = 1
            st.rerun()
    
    with col2:
        if st.button("🔄 Regenerate Questions", type="secondary"):
            st.info("🔄 Questions regeneration would trigger here")
    
    with col3:
        if st.button("📋 Export for Review", type="secondary"):
            export_questions_for_review(questions)
    
    with col4:
        if st.button("✅ Approve Questions", type="primary"):
            st.session_state.validation_state['questions_approved'] = True
            st.session_state.validation_state['current_step'] = 3
            st.session_state.validation_state['validation_notes']['questions'] = {
                'feedback': questions_feedback,
                'score': questions_score,
                'timestamp': datetime.now().isoformat()
            }
            st.success("✅ Questions approved! Moving to final approval...")
            st.rerun()

def show_questions_editing_section(section_name: str, questions: List[Dict]):
    """Show editable questions for a specific section."""
    
    for i, question in enumerate(questions):
        question_id = f"{section_name}_{i}"
        
        # Question editing interface
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Get current question text (edited or original)
            current_text = st.session_state.validation_state['edited_questions'].get(
                question_id, question.get('question', question.get('text', 'No question text'))
            )
            
            edited_text = st.text_area(
                f"Question {i+1}:",
                value=current_text,
                height=80,
                key=f"edit_{question_id}"
            )
            
            # Save edits
            if edited_text != question.get('question', question.get('text', '')):
                st.session_state.validation_state['edited_questions'][question_id] = edited_text
        
        with col2:
            # Question quality assessment
            st.markdown("**Quality Assessment**")
            
            clarity_score = st.slider(
                "Clarity", 0, 10, 8, 
                key=f"clarity_{question_id}",
                help="How clear and understandable is this question?"
            )
            
            relevance_score = st.slider(
                "Relevance", 0, 10, 9,
                key=f"relevance_{question_id}",
                help="How relevant is this question to the visa requirements?"
            )
            
            overall_score = (clarity_score + relevance_score) / 2 * 10
            
            if overall_score >= 80:
                st.success(f"✅ {overall_score:.0f}%")
            elif overall_score >= 60:
                st.warning(f"⚠️ {overall_score:.0f}%")
            else:
                st.error(f"❌ {overall_score:.0f}%")
            
            # Question metadata
            if question.get('validation_rules'):
                st.markdown("**Validation Rules:**")
                for rule in question['validation_rules']:
                    st.caption(f"• {rule}")
        
        st.divider()

def show_final_approval(workflow_results: Dict[str, Any]):
    """Step 3: Final approval and visa finalization."""
    
    st.markdown("## ✅ Step 3: Final Approval & Visa Finalization")
    st.markdown("Review the complete visa application process before finalization.")
    
    # Summary of validation process
    st.markdown("### 📊 Validation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Requirements Review**")
        req_notes = st.session_state.validation_state['validation_notes'].get('requirements', {})
        st.success(f"✅ Approved ({req_notes.get('score', 85)}%)")
        if req_notes.get('feedback'):
            st.caption(f"Notes: {req_notes['feedback'][:100]}...")
    
    with col2:
        st.markdown("**Questions Review**")
        q_notes = st.session_state.validation_state['validation_notes'].get('questions', {})
        st.success(f"✅ Approved ({q_notes.get('score', 88)}%)")
        if q_notes.get('feedback'):
            st.caption(f"Notes: {q_notes['feedback'][:100]}...")
    
    with col3:
        st.markdown("**Overall Quality**")
        overall_score = calculate_overall_quality_score()
        if overall_score >= 85:
            st.success(f"✅ Excellent ({overall_score}%)")
        elif overall_score >= 70:
            st.warning(f"⚠️ Good ({overall_score}%)")
        else:
            st.error(f"❌ Needs Review ({overall_score}%)")
    
    # Final review checklist
    st.markdown("### ✅ Pre-Finalization Checklist")
    
    checklist_items = [
        "Requirements are complete and accurate",
        "Questions are clear and user-friendly", 
        "Validation rules are properly defined",
        "All stakeholder feedback has been incorporated",
        "Quality scores meet minimum thresholds (>70%)"
    ]
    
    all_checked = True
    for item in checklist_items:
        checked = st.checkbox(item, value=True)
        if not checked:
            all_checked = False
    
    # Final approval interface
    st.markdown("### 🎯 Final Approval")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        final_notes = st.text_area(
            "Final Approval Notes:",
            placeholder="Add any final notes or comments before committing to visa...",
            height=100
        )
        
        approver_name = st.text_input("Approver Name:", placeholder="Enter your name")
    
    with col2:
        st.markdown("**Approval Authority**")
        approval_level = st.selectbox(
            "Approval Level:",
            ["Policy Analyst", "Senior Analyst", "Policy Manager", "Director"]
        )
        
        st.markdown("**Finalization Impact**")
        st.info("🔒 This will finalize the visa application process and make it available for customer use.")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Questions", type="secondary"):
            st.session_state.validation_state['current_step'] = 2
            st.rerun()
    
    with col2:
        if st.button("📋 Generate Report", type="secondary"):
            generate_validation_report(workflow_results)
    
    with col3:
        commit_disabled = not (all_checked and approver_name and final_notes)
        if st.button("🚀 Commit to Visa", type="primary", disabled=commit_disabled):
            # Finalize the visa
            st.session_state.validation_state['final_approved'] = True
            st.session_state.validation_state['current_step'] = 4
            st.session_state.validation_state['approval_timestamp'] = datetime.now().isoformat()
            st.session_state.validation_state['validation_notes']['final'] = {
                'notes': final_notes,
                'approver': approver_name,
                'level': approval_level,
                'timestamp': datetime.now().isoformat()
            }
            
            st.success("🎉 Visa application process finalized successfully!")
            st.balloons()
            st.rerun()

def show_completion_summary(workflow_results: Dict[str, Any]):
    """Step 4: Completion summary and next steps."""
    
    st.markdown("## 🎉 Validation Workflow Complete")
    st.markdown("The visa application process has been successfully validated and finalized.")
    
    # Completion metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Validation Status", "✅ Complete")
    
    with col2:
        approval_time = st.session_state.validation_state.get('approval_timestamp')
        if approval_time:
            st.metric("Approved", datetime.fromisoformat(approval_time).strftime("%Y-%m-%d %H:%M"))
    
    with col3:
        overall_score = calculate_overall_quality_score()
        st.metric("Final Quality Score", f"{overall_score}%")
    
    with col4:
        edited_count = len(st.session_state.validation_state.get('edited_questions', {}))
        st.metric("Questions Edited", edited_count)
    
    # Next steps
    st.markdown("### 🚀 Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Available Actions:**")
        if st.button("📋 Generate Customer Form", type="primary"):
            st.session_state.show_form_renderer = True
            st.success("✅ Customer form generation initiated!")
        
        if st.button("📊 Download Validation Report", type="secondary"):
            generate_validation_report(workflow_results)
        
        if st.button("📤 Export Final Configuration", type="secondary"):
            export_final_configuration(workflow_results)
    
    with col2:
        st.markdown("**Validation Summary:**")
        final_notes = st.session_state.validation_state['validation_notes'].get('final', {})
        st.info(f"**Approved by:** {final_notes.get('approver', 'Unknown')}")
        st.info(f"**Approval Level:** {final_notes.get('level', 'Unknown')}")
        if final_notes.get('notes'):
            st.info(f"**Notes:** {final_notes['notes']}")
    
    # Reset workflow option
    st.divider()
    if st.button("🔄 Start New Validation Workflow", type="secondary"):
        st.session_state.validation_state = {
            'current_step': 1,
            'requirements_approved': False,
            'questions_approved': False,
            'final_approved': False,
            'edited_questions': {},
            'validation_notes': {},
            'approval_timestamp': None
        }
        st.rerun()

# Helper functions
def extract_requirements_data(workflow_results: Dict[str, Any]) -> Dict[str, List]:
    """Extract requirements data from workflow results."""
    requirements_data = workflow_results.get('requirements_capture', {})
    
    return {
        'functional': requirements_data.get('functional_requirements', []),
        'data': requirements_data.get('data_requirements', []),
        'business': requirements_data.get('business_rules', []),
        'validation': requirements_data.get('validation_rules', [])
    }

def extract_questions_data(workflow_results: Dict[str, Any]) -> Dict[str, List]:
    """Extract questions data from workflow results."""
    questions_data = workflow_results.get('question_generation', {})
    questions = questions_data.get('questions', [])
    
    # Group questions by section
    sections = {}
    for question in questions:
        section = question.get('section', 'General')
        if section not in sections:
            sections[section] = []
        sections[section].append(question)
    
    return sections

def show_requirements_section(title: str, requirements: List[Dict]):
    """Display a requirements section with details."""
    if not requirements:
        st.info(f"No {title.lower()} found.")
        return
    
    for i, req in enumerate(requirements):
        with st.expander(f"{req.get('id', f'REQ-{i+1}')}: {req.get('description', 'No description')[:100]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {req.get('description', 'No description')}")
                if req.get('details'):
                    st.markdown(f"**Details:** {req['details']}")
                if req.get('acceptance_criteria'):
                    st.markdown("**Acceptance Criteria:**")
                    for criteria in req['acceptance_criteria']:
                        st.markdown(f"• {criteria}")
            
            with col2:
                priority = req.get('priority', 'Medium')
                if priority == 'High':
                    st.error(f"🔴 {priority} Priority")
                elif priority == 'Medium':
                    st.warning(f"🟡 {priority} Priority")
                else:
                    st.success(f"🟢 {priority} Priority")
                
                if req.get('mandatory'):
                    st.info("✅ Mandatory")
                else:
                    st.info("⚪ Optional")

def calculate_questions_quality_score(questions: Dict[str, List]) -> int:
    """Calculate average quality score for questions."""
    # Simplified quality calculation
    total_questions = sum(len(section_questions) for section_questions in questions.values())
    if total_questions == 0:
        return 0
    
    # Base score with some randomization for demo
    import random
    return random.randint(82, 92)

def calculate_overall_quality_score() -> int:
    """Calculate overall quality score from validation notes."""
    req_score = st.session_state.validation_state['validation_notes'].get('requirements', {}).get('score', 85)
    q_score = st.session_state.validation_state['validation_notes'].get('questions', {}).get('score', 88)
    
    return int((req_score + q_score) / 2)

def export_questions_for_review(questions: Dict[str, List]):
    """Export questions for external review."""
    st.success("📋 Questions exported for review (demo functionality)")

def generate_validation_report(workflow_results: Dict[str, Any]):
    """Generate comprehensive validation report."""
    st.success("📊 Validation report generated (demo functionality)")

def export_final_configuration(workflow_results: Dict[str, Any]):
    """Export final configuration for deployment."""
    st.success("📤 Final configuration exported (demo functionality)")
