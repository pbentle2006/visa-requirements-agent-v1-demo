"""
Customer Form Renderer
Generates interactive customer-facing visa application forms with validation and guidance.
"""

import streamlit as st
import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import re

def show_customer_form_renderer(workflow_results: Dict[str, Any]):
    """Display the customer form renderer interface."""
    
    st.title("📋 Customer Visa Application Form")
    st.markdown("**Interactive visa application form with real-time validation and guidance.**")
    
    if not workflow_results:
        st.warning("⚠️ No workflow results available. Please complete the validation workflow first.")
        return
    
    # Check if validation workflow is complete
    if not st.session_state.get('validation_state', {}).get('final_approved', False):
        st.warning("⚠️ Please complete the Human Validation Workflow before generating customer forms.")
        if st.button("🔄 Go to Validation Workflow"):
            st.session_state.current_page = "Human Validation"
            st.rerun()
        return
    
    # Initialize form state
    if 'customer_form_data' not in st.session_state:
        st.session_state.customer_form_data = {}
    
    if 'form_validation_errors' not in st.session_state:
        st.session_state.form_validation_errors = {}
    
    # Form header with visa information
    show_form_header(workflow_results)
    
    # Progress indicator
    show_form_progress()
    
    # Main form sections
    questions = extract_questions_for_form(workflow_results)
    requirements = extract_requirements_for_validation(workflow_results)
    
    # Render form sections
    form_sections = organize_questions_by_section(questions)
    
    for section_name, section_questions in form_sections.items():
        show_form_section(section_name, section_questions, requirements)
    
    # Form validation and submission
    show_form_validation_summary()
    show_form_submission()

def show_form_header(workflow_results: Dict[str, Any]):
    """Display form header with visa information."""
    
    # Extract visa information
    policy_data = workflow_results.get('policy_evaluation', {})
    visa_type = policy_data.get('policy_structure', {}).get('visa_type', 'Visa Application')
    visa_code = policy_data.get('policy_structure', {}).get('visa_code', 'N/A')
    
    # Header styling
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f77b4, #17a2b8); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">🛂 {}</h2>
        <p style="color: #e8f4f8; margin: 0.5rem 0 0 0;">Visa Code: {} | Application Form</p>
    </div>
    """.format(visa_type, visa_code), unsafe_allow_html=True)
    
    # Important information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📋 **Complete all required fields**\nFields marked with * are mandatory")
    
    with col2:
        st.info("💡 **Hover for guidance**\nTooltips provide helpful information")
    
    with col3:
        st.info("✅ **Real-time validation**\nErrors are highlighted immediately")

def show_form_progress():
    """Display form completion progress."""
    
    questions = extract_questions_for_form(st.session_state.get('workflow_results', {}))
    total_questions = len(questions)
    completed_questions = len([q for q in questions if get_form_field_value(q.get('id', '')) is not None])
    
    if total_questions > 0:
        progress = completed_questions / total_questions
        st.progress(progress, text=f"Form Progress: {completed_questions}/{total_questions} questions completed ({progress:.0%})")
    
    st.divider()

def show_form_section(section_name: str, questions: List[Dict], requirements: Dict[str, Any]):
    """Display a form section with questions and validation."""
    
    with st.expander(f"📋 {section_name}", expanded=True):
        st.markdown(f"### {section_name}")
        
        for question in questions:
            render_form_question(question, requirements)
        
        # Section completion indicator
        section_complete = all(get_form_field_value(q.get('id', '')) is not None for q in questions)
        if section_complete:
            st.success(f"✅ {section_name} section completed")
        else:
            remaining = len([q for q in questions if get_form_field_value(q.get('id', '')) is None])
            st.info(f"📝 {remaining} questions remaining in this section")

def render_form_question(question: Dict[str, Any], requirements: Dict[str, Any]):
    """Render an individual form question with validation."""
    
    question_id = question.get('id', f"q_{hash(question.get('question', ''))}")
    question_text = question.get('question', question.get('text', 'No question text'))
    question_type = question.get('type', 'text')
    is_required = question.get('required', question.get('mandatory', True))
    help_text = question.get('help_text', question.get('guidance', ''))
    validation_rules = question.get('validation_rules', [])
    
    # Question label with required indicator
    label = f"{question_text}{'*' if is_required else ''}"
    
    # Render question based on type
    current_value = get_form_field_value(question_id)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if question_type == 'text':
            value = st.text_input(label, value=current_value or '', help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'textarea':
            value = st.text_area(label, value=current_value or '', help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'number':
            value = st.number_input(label, value=current_value or 0, help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'date':
            value = st.date_input(label, value=current_value or date.today(), help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'select':
            options = question.get('options', ['Option 1', 'Option 2', 'Option 3'])
            value = st.selectbox(label, options, index=0 if current_value is None else options.index(current_value) if current_value in options else 0, help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'multiselect':
            options = question.get('options', ['Option 1', 'Option 2', 'Option 3'])
            value = st.multiselect(label, options, default=current_value or [], help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'radio':
            options = question.get('options', ['Yes', 'No'])
            value = st.radio(label, options, index=0 if current_value is None else options.index(current_value) if current_value in options else 0, help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'checkbox':
            value = st.checkbox(label, value=current_value or False, help=help_text, key=f"form_{question_id}")
        
        elif question_type == 'file':
            value = st.file_uploader(label, help=help_text, key=f"form_{question_id}")
        
        else:
            value = st.text_input(label, value=current_value or '', help=help_text, key=f"form_{question_id}")
        
        # Store form data
        st.session_state.customer_form_data[question_id] = value
    
    with col2:
        # Real-time validation
        validation_result = validate_form_field(question_id, value, validation_rules, is_required)
        show_field_validation_status(validation_result)
        
        # Show guidance tooltip
        if help_text:
            with st.popover("💡 Guidance"):
                st.markdown(help_text)
        
        # Show validation rules
        if validation_rules:
            with st.popover("📋 Requirements"):
                st.markdown("**Field Requirements:**")
                for rule in validation_rules:
                    st.markdown(f"• {rule}")
    
    # Show validation errors
    if question_id in st.session_state.form_validation_errors:
        st.error(f"❌ {st.session_state.form_validation_errors[question_id]}")
    
    st.divider()

def show_field_validation_status(validation_result: Dict[str, Any]):
    """Show validation status for a field."""
    
    if validation_result['is_valid']:
        st.success("✅ Valid")
    elif validation_result['value'] is None or validation_result['value'] == '':
        st.info("⏳ Pending")
    else:
        st.error("❌ Invalid")
        if validation_result.get('errors'):
            for error in validation_result['errors']:
                st.caption(f"• {error}")

def validate_form_field(field_id: str, value: Any, validation_rules: List[str], is_required: bool) -> Dict[str, Any]:
    """Validate a form field against its rules."""
    
    errors = []
    
    # Required field validation
    if is_required and (value is None or value == '' or (isinstance(value, list) and len(value) == 0)):
        errors.append("This field is required")
        return {'is_valid': False, 'errors': errors, 'value': value}
    
    # Skip other validations if field is empty and not required
    if not is_required and (value is None or value == ''):
        return {'is_valid': True, 'errors': [], 'value': value}
    
    # Apply validation rules
    for rule in validation_rules:
        rule_lower = rule.lower()
        
        if 'email' in rule_lower and value:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)):
                errors.append("Please enter a valid email address")
        
        elif 'phone' in rule_lower and value:
            if not re.match(r'^[\+]?[1-9][\d]{0,15}$', str(value).replace(' ', '').replace('-', '')):
                errors.append("Please enter a valid phone number")
        
        elif 'minimum length' in rule_lower and value:
            try:
                min_length = int(re.search(r'\d+', rule).group())
                if len(str(value)) < min_length:
                    errors.append(f"Minimum length is {min_length} characters")
            except:
                pass
        
        elif 'maximum length' in rule_lower and value:
            try:
                max_length = int(re.search(r'\d+', rule).group())
                if len(str(value)) > max_length:
                    errors.append(f"Maximum length is {max_length} characters")
            except:
                pass
        
        elif 'numeric' in rule_lower and value:
            try:
                float(value)
            except:
                errors.append("Please enter a numeric value")
        
        elif 'date' in rule_lower and 'future' in rule_lower and value:
            if isinstance(value, date) and value <= date.today():
                errors.append("Date must be in the future")
        
        elif 'date' in rule_lower and 'past' in rule_lower and value:
            if isinstance(value, date) and value >= date.today():
                errors.append("Date must be in the past")
    
    # Update session state errors
    if errors:
        st.session_state.form_validation_errors[field_id] = '; '.join(errors)
    else:
        st.session_state.form_validation_errors.pop(field_id, None)
    
    return {'is_valid': len(errors) == 0, 'errors': errors, 'value': value}

def show_form_validation_summary():
    """Display overall form validation summary."""
    
    st.markdown("## 📊 Application Summary")
    
    questions = extract_questions_for_form(st.session_state.get('workflow_results', {}))
    total_questions = len(questions)
    completed_questions = len([q for q in questions if get_form_field_value(q.get('id', '')) is not None])
    error_count = len(st.session_state.form_validation_errors)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Questions", total_questions)
    
    with col2:
        st.metric("Completed", completed_questions)
    
    with col3:
        st.metric("Remaining", total_questions - completed_questions)
    
    with col4:
        if error_count == 0:
            st.metric("Validation Errors", "✅ None")
        else:
            st.metric("Validation Errors", f"❌ {error_count}")
    
    # Progress bar
    if total_questions > 0:
        progress = completed_questions / total_questions
        st.progress(progress, text=f"Application Progress: {progress:.0%} complete")
    
    # Show validation errors summary
    if st.session_state.form_validation_errors:
        st.markdown("### ❌ Validation Errors")
        with st.expander("View all errors", expanded=False):
            for field_id, error in st.session_state.form_validation_errors.items():
                st.error(f"**{field_id}**: {error}")

def show_form_submission():
    """Display form submission interface."""
    
    st.markdown("## 🚀 Submit Application")
    
    questions = extract_questions_for_form(st.session_state.get('workflow_results', {}))
    total_questions = len(questions)
    completed_questions = len([q for q in questions if get_form_field_value(q.get('id', '')) is not None])
    has_errors = len(st.session_state.form_validation_errors) > 0
    
    # Submission requirements
    can_submit = completed_questions == total_questions and not has_errors
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if can_submit:
            st.success("✅ Application is ready for submission!")
            st.markdown("All required fields have been completed and validated.")
        else:
            st.warning("⚠️ Application is not ready for submission")
            if completed_questions < total_questions:
                st.markdown(f"• Complete {total_questions - completed_questions} remaining questions")
            if has_errors:
                st.markdown(f"• Fix {len(st.session_state.form_validation_errors)} validation errors")
    
    with col2:
        # Submission buttons
        if st.button("💾 Save Draft", type="secondary"):
            save_form_draft()
        
        if st.button("📋 Preview Application", type="secondary"):
            show_application_preview()
        
        submit_disabled = not can_submit
        if st.button("🚀 Submit Application", type="primary", disabled=submit_disabled):
            submit_application()

def save_form_draft():
    """Save form as draft."""
    st.success("💾 Application draft saved successfully!")
    st.info("You can return to complete your application later.")

def show_application_preview():
    """Show application preview."""
    st.info("📋 Application preview would be displayed here (demo functionality)")

def submit_application():
    """Submit the completed application."""
    st.success("🎉 Application submitted successfully!")
    st.balloons()
    st.info("**Application Reference:** VA-2024-" + str(hash(str(st.session_state.customer_form_data)))[-6:])
    st.info("You will receive a confirmation email shortly with next steps.")

# Helper functions
def extract_questions_for_form(workflow_results: Dict[str, Any]) -> List[Dict]:
    """Extract questions from workflow results for form rendering."""
    questions_data = workflow_results.get('question_generation', {})
    questions = questions_data.get('questions', [])
    
    # Add IDs and enhance questions for form rendering
    enhanced_questions = []
    for i, question in enumerate(questions):
        enhanced_question = question.copy()
        enhanced_question['id'] = enhanced_question.get('id', f"q_{i}")
        
        # Infer question type from text
        question_text = question.get('question', question.get('text', '')).lower()
        if 'email' in question_text:
            enhanced_question['type'] = 'text'
            enhanced_question['validation_rules'] = enhanced_question.get('validation_rules', []) + ['Valid email format required']
        elif 'phone' in question_text:
            enhanced_question['type'] = 'text'
            enhanced_question['validation_rules'] = enhanced_question.get('validation_rules', []) + ['Valid phone number required']
        elif 'date' in question_text or 'birth' in question_text:
            enhanced_question['type'] = 'date'
        elif 'age' in question_text or 'number' in question_text:
            enhanced_question['type'] = 'number'
        elif 'yes' in question_text and 'no' in question_text:
            enhanced_question['type'] = 'radio'
            enhanced_question['options'] = ['Yes', 'No']
        elif 'select' in question_text or 'choose' in question_text:
            enhanced_question['type'] = 'select'
            enhanced_question['options'] = ['Option 1', 'Option 2', 'Option 3']
        else:
            enhanced_question['type'] = 'text'
        
        enhanced_questions.append(enhanced_question)
    
    return enhanced_questions

def extract_requirements_for_validation(workflow_results: Dict[str, Any]) -> Dict[str, Any]:
    """Extract requirements for form validation."""
    return workflow_results.get('requirements_capture', {})

def organize_questions_by_section(questions: List[Dict]) -> Dict[str, List[Dict]]:
    """Organize questions by section."""
    sections = {}
    for question in questions:
        section = question.get('section', 'General Information')
        if section not in sections:
            sections[section] = []
        sections[section].append(question)
    
    return sections

def get_form_field_value(field_id: str) -> Any:
    """Get the current value of a form field."""
    return st.session_state.customer_form_data.get(field_id)
