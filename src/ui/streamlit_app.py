import streamlit as st
import json
import os
import tempfile
from pathlib import Path
import sys
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from src.utils.output_formatter import OutputFormatter
from src.generators.mock_results_generator import MockResultsGenerator
from src.generators.policy_generator import PolicyGenerator
from src.ui.enhanced_file_upload import show_enhanced_file_upload, get_document_content, get_document_path
from src.ui.agent_dashboard import show_agent_performance_dashboard
from src.ui.enhanced_policy_comparison import show_enhanced_policy_comparison
from src.ui.pages.agent_architecture import show_agent_architecture

# Page configuration
st.set_page_config(
    page_title="Visa Requirements Agent Demo",
    page_icon="🛂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .agent-status {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🛂 Visa Requirements Agent Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Requirements Capture for Immigration Policies</div>', unsafe_allow_html=True)

# Initialize session state
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'document_info' not in st.session_state:
    st.session_state.document_info = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Workflow Analysis"

# Sidebar navigation
with st.sidebar:
    st.header("🧭 Navigation")
    
    # Navigation options
    page_options = [
        "🚀 Workflow Analysis",
        "🏗️ Agent Architecture", 
        "📈 Agent Performance",
        "📊 Policy Comparison"
    ]
    
    # Determine current index
    current_index = 0
    if st.session_state.current_page == "Agent Architecture":
        current_index = 1
    elif st.session_state.current_page == "Agent Performance":
        current_index = 2
    elif st.session_state.current_page == "Policy Comparison":
        current_index = 3
    
    selected_page = st.radio(
        "Choose functionality:",
        page_options,
        index=current_index,
        key="navigation_radio"
    )
    
    # Update session state
    if "Workflow Analysis" in selected_page:
        st.session_state.current_page = "Workflow Analysis"
    elif "Agent Architecture" in selected_page:
        st.session_state.current_page = "Agent Architecture"
    elif "Agent Performance" in selected_page:
        st.session_state.current_page = "Agent Performance"
    elif "Policy Comparison" in selected_page:
        st.session_state.current_page = "Policy Comparison"
    
    st.divider()
    
    # Configuration section (only show for Workflow Analysis)
    if st.session_state.current_page == "Workflow Analysis":
        st.header("⚙️ Configuration")
        
        # Demo mode toggle
        demo_mode = st.toggle("Demo Mode", value=False, help="Use synthetic data for demonstration")
        
        if demo_mode:
            st.info("🎭 Demo Mode: Using mock results for fast demonstration")
        else:
            st.info("🔴 Live API Mode: Using real OpenAI API calls")
        
        st.divider()
        
        # API Configuration
        st.header("🔑 API Configuration")
        
        if not demo_mode:
            # Check for API key in environment
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key or api_key == 'your_openai_api_key_here':
                st.warning("⚠️ OpenAI API Key required")
                api_key_input = st.text_input("Enter OpenAI API Key", type="password")
                if api_key_input:
                    os.environ['OPENAI_API_KEY'] = api_key_input
                    st.success("✅ API Key configured")
            else:
                st.success("✅ API Key configured")
        else:
            st.info("🎭 Using mock data - no API key required")
    else:
        st.info("📊 Policy Comparison Mode")
        st.markdown("Compare visa requirements, questions, and validation across different policy documents.")

# Main content area based on selected page
if st.session_state.current_page == "Workflow Analysis":
    # Workflow Analysis Page
    if st.session_state.workflow_results is None:
        # Configuration and setup phase
        
        # Enhanced file upload
        document_info = show_enhanced_file_upload(demo_mode)
        st.session_state.document_info = document_info
        
        if document_info:
            # Show document preview
            from src.ui.enhanced_file_upload import show_document_preview
            show_document_preview(document_info)
        
        st.divider()
        
        # Execution controls
        st.header("▶️ Execution")
        
        # Check if we have required inputs
        has_api_key = demo_mode or (os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here')
        has_document = document_info is not None
        
        if st.button("🚀 Run Complete Workflow", type="primary", disabled=not has_api_key or not has_document):
            if demo_mode:
                with st.spinner("Running demo workflow... Processing through 5-stage AI pipeline..."):
                    try:
                        import time
                        
                        # Add realistic delay to simulate processing (2 seconds for demo presentation)
                        time.sleep(2)
                        
                        # Use mock results generator
                        generator = MockResultsGenerator()
                        
                        # Generate results based on selected policy
                        policy_name = document_info.get('original_name', 'Sample Policy')
                        if '(' in policy_name:
                            policy_name = policy_name.split(" (")[0]  # Remove (Original/Synthetic) suffix
                        
                        results = generator.generate_complete_workflow_results(policy_name)
                        
                        # Verify results structure
                        if not results or 'stages' not in results:
                            raise ValueError("Invalid results structure generated")
                        
                        st.session_state.workflow_results = results
                        
                        st.success("✅ Demo workflow completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Demo Error: {str(e)}")
                        # Show debug info
                        if st.checkbox("Show Debug Info"):
                            st.exception(e)
            else:
                with st.spinner("Running workflow... This may take a few minutes."):
                    try:
                        # FORCE COMPLETE SESSION STATE RESET
                        print(f"FORCING COMPLETE SESSION STATE RESET", flush=True)
                        
                        # Clear ALL session state to prevent any caching issues
                        keys_to_delete = list(st.session_state.keys())
                        for key in keys_to_delete:
                            if key != 'uploaded_files':  # Keep uploaded files
                                del st.session_state[key]
                        
                        print(f"Cleared {len(keys_to_delete)} session state keys", flush=True)
                        
                        # Initialize fresh orchestrator
                        print(f"Initializing WorkflowOrchestrator...", flush=True)
                        st.session_state.orchestrator = WorkflowOrchestrator()
                        print(f"WorkflowOrchestrator initialized successfully", flush=True)
                        
                        # Get document path for workflow
                        policy_path = get_document_path(document_info)
                        policy_content = get_document_content(document_info)
                        
                        # HYBRID APPROACH - Detect visa type but use real agents
                        detected_visa_type = None
                        detected_visa_code = None
                        
                        if policy_content:
                            print(f" HYBRID: Analyzing document content for visa type detection ", flush=True)
                            print(f" Document content length: {len(policy_content)} ", flush=True)
                            print(f" First 500 chars: {policy_content[:500]} ", flush=True)
                            
                            content_upper = policy_content.upper()
                            print(f" Checking for PARENT BOOST: {'PARENT BOOST' in content_upper} ", flush=True)
                            
                            if any(keyword in content_upper for keyword in ['PARENT BOOST VISITOR VISA', 'PARENT BOOST', 'V4']):
                                detected_visa_type = "Parent Boost Visitor Visa"
                                detected_visa_code = "V4"
                                print(f" HYBRID: DETECTED PARENT BOOST VISITOR VISA - PROCESSING WITH REAL AGENTS ", flush=True)
                            elif any(keyword in content_upper for keyword in ['SKILLED MIGRANT', 'SR1', 'SR3', 'SR4', 'SR5', 'SKILLED RESIDENCE']):
                                detected_visa_type = "Skilled Migrant Residence Visa"
                                detected_visa_code = "SR1"
                                print(f" HYBRID: DETECTED SKILLED MIGRANT RESIDENCE VISA - PROCESSING WITH REAL AGENTS ", flush=True)
                            elif any(keyword in content_upper for keyword in ['WORKING HOLIDAY', 'YOUTH', 'TEMPORARY WORK', 'WHV', 'WORKING HOLIDAY VISA']):
                                detected_visa_type = "Working Holiday Visa"
                                detected_visa_code = "WHV"
                                print(f" HYBRID: DETECTED WORKING HOLIDAY VISA - PROCESSING WITH REAL AGENTS ", flush=True)
                            else:
                                print(f" HYBRID: NO SPECIFIC VISA TYPE DETECTED - USING GENERIC PROCESSING ", flush=True)
                                print(f" Content sample for debugging: {content_upper[:200]} ", flush=True)
                        
                        print(f"🚀 HYBRID: CALLING ORCHESTRATOR WITH REAL AGENTS 🚀", flush=True)
                        
                        # Add timestamp to force fresh execution
                        import time
                        execution_timestamp = int(time.time() * 1000)
                        print(f"🚀 EXECUTION TIMESTAMP: {execution_timestamp} 🚀", flush=True)
                        
                        # Run workflow with real agents and detected visa type hints
                        results = st.session_state.orchestrator.run_workflow(
                            policy_path, 
                            policy_content,
                            detected_visa_type=detected_visa_type,
                            detected_visa_code=detected_visa_code,
                            force_visa_type=bool(detected_visa_type)
                        )
                        st.session_state.workflow_results = results
                        
                        st.success("✅ Workflow completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Workflow Error: {str(e)}")
                        # Show debug info
                        if st.checkbox("Show Debug Info"):
                            st.exception(e)
        
        # Show help text
        if not has_api_key:
            st.warning("⚠️ Please configure your OpenAI API key to run the workflow.")
        elif not has_document:
            st.info("📄 Please upload a policy document to begin analysis.")
    
    else:
        # Results display phase
        results = st.session_state.workflow_results
        
        # Workflow Summary
        st.header("📊 Workflow Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status = results.get('status', 'unknown')
            status_color = "🟢" if status == 'success' else "🔴" if status == 'failed' else "🟡"
            st.metric("Status", f"{status_color} {status.upper()}")
        
        with col2:
            duration = results.get('duration_seconds', 0)
            st.metric("Duration", f"{duration:.1f}s")
        
        with col3:
            stages = results.get('stages', [])
            completed_stages = len([s for s in stages if s.get('status') == 'success'])
            st.metric("Stages Completed", f"{completed_stages}/{len(stages)}")
        
        with col4:
            # Calculate validation score - use new structure first
            outputs = results.get('outputs', {})
            
            # Try new structure first
            validation_score = outputs.get('validation_score', 0)
            if validation_score:
                # Convert to percentage if needed (0.75 -> 75%)
                score_display = float(validation_score) * 100 if float(validation_score) <= 1 else float(validation_score)
            else:
                # Fall back to old structure
                validation_data = outputs.get('validation', {})
                validation_report = outputs.get('validation_report', {})
                score_display = validation_data.get('overall_score', 0) if isinstance(validation_data, dict) else validation_report.get('overall_score', 0)
            
            st.metric("Validation Score", f"{score_display:.1f}%")
        
        st.divider()
        
        # Create tabs for different views
        tabs = st.tabs([
            "📄 Policy Analysis",
            "📋 Requirements", 
            "❓ Questions",
            "✅ Validation",
            "📊 Statistics",
            "🤖 Agent Dashboard"
        ])
        
        # Tab 1: Policy Analysis
        with tabs[0]:
            st.header("Policy Structure")
            
            policy_structure = results['outputs'].get('policy_structure', {})
            if policy_structure:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    visa_type = policy_structure.get('visa_type', 'Not specified')
                    st.metric("Visa Type", visa_type)
                
                with col2:
                    visa_code = policy_structure.get('visa_code', 'Not specified')
                    st.metric("Visa Code", visa_code)
                
                with col3:
                    version = policy_structure.get('version', 'Not specified')
                    st.metric("Version", version)
                
                # Eligibility Rules
                st.subheader("Eligibility Rules")
                eligibility_rules = results['outputs'].get('eligibility_rules', {})
                
                if eligibility_rules:
                    # Display different types of requirements
                    rule_types = ['applicant_requirements', 'sponsor_requirements', 'dependent_requirements']
                    
                    for rule_type in rule_types:
                        if rule_type in eligibility_rules:
                            rules = eligibility_rules[rule_type]
                            if rules:
                                st.write(f"**{rule_type.replace('_', ' ').title()}:**")
                                for rule in rules:
                                    if isinstance(rule, dict):
                                        description = rule.get('description') or rule.get('requirement', 'No description')
                                        mandatory = rule.get('mandatory', True)
                                        status_icon = "🔴" if mandatory else "🟡"
                                        st.write(f"{status_icon} {description}")
                                    else:
                                        st.write(f"• {rule}")
            else:
                st.warning("No policy structure data available")
        
        # Tab 2: Requirements
        with tabs[1]:
            st.header("Requirements Analysis")
            
            outputs = results.get('outputs', {})
            
            # Display different types of requirements (they're stored directly in outputs)
            req_types = [
                ('functional_requirements', 'Functional Requirements'),
                ('data_requirements', 'Data Requirements'), 
                ('business_rules', 'Business Rules'),
                ('validation_rules', 'Validation Rules')
            ]
            
            has_requirements = False
            
            for req_key, req_title in req_types:
                reqs = outputs.get(req_key, [])
                if reqs:
                    has_requirements = True
                    st.subheader(req_title)
                    
                    for req in reqs:
                        if isinstance(req, dict):
                            # Handle different field name variations
                            req_id = req.get('requirement_id') or req.get('id') or req.get('rule_id', 'Unknown')
                            description = req.get('description') or req.get('requirement') or req.get('rule', 'No description')
                            
                            # Additional details
                            category = req.get('category', '')
                            priority = req.get('priority', '')
                            reference = req.get('policy_reference', '')
                            
                            # Format display
                            details = []
                            if category:
                                details.append(f"Category: {category}")
                            if priority:
                                priority_icon = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                                details.append(f"Priority: {priority_icon} {priority}")
                            if reference:
                                details.append(f"Reference: {reference}")
                            
                            st.write(f"**{req_id}**: {description}")
                            if details:
                                st.write(f"   _{' | '.join(details)}_")
                        else:
                            st.write(f"• {req}")
                    
                    st.divider()
            
            if not has_requirements:
                st.warning("No requirements data available")
        
        # Tab 3: Questions
        with tabs[2]:
            st.header("Generated Questions")
            
            # Debug: Show what's actually in outputs
            if st.checkbox("🔍 Show Debug Info", key="questions_debug"):
                st.subheader("Debug: Available Output Keys")
                output_keys = list(results.get('outputs', {}).keys())
                st.write(f"Available keys: {output_keys}")
                
                # Show questions-related keys
                questions_keys = [key for key in output_keys if 'question' in key.lower()]
                st.write(f"Question-related keys: {questions_keys}")
                
                # Show sample data for each questions key
                for key in questions_keys:
                    data = results['outputs'].get(key, [])
                    st.write(f"**{key}**: {type(data)} with {len(data) if isinstance(data, (list, dict)) else 'N/A'} items")
                    if data and isinstance(data, list) and len(data) > 0:
                        st.write(f"Sample item: {data[0]}")
                
                # Show workflow stages info
                st.subheader("Debug: Workflow Stages")
                stages = results.get('stages', [])
                for i, stage in enumerate(stages):
                    stage_name = stage.get('name', f'Stage {i}')
                    stage_status = stage.get('status', 'unknown')
                    stage_agent = stage.get('agent', 'unknown')
                    
                    # Color code status
                    status_color = "🟢" if stage_status == 'success' else "🔴" if stage_status == 'failed' else "🟡"
                    st.write(f"**{stage_name}**: {status_color} {stage_status} (agent: {stage_agent})")
                    
                    # Show error if failed
                    if stage_status == 'failed':
                        error_msg = stage.get('error', 'No error message available')
                        st.error(f"Error: {error_msg}")
                    
                    # Show stage outputs if available
                    stage_outputs = stage.get('outputs', {})
                    if stage_outputs:
                        st.write(f"  Stage output keys: {list(stage_outputs.keys())}")
                
                # Show debug info from agents
                st.subheader("Debug: Agent Debug Info")
                debug_info = results.get('outputs', {}).get('debug_info', 'No debug info available')
                st.write(debug_info)
                
                # Show execution verification
                execution_timestamp = results.get('outputs', {}).get('execution_timestamp')
                execution_mode = results.get('outputs', {}).get('execution_mode')
                if execution_timestamp:
                    st.success(f"✅ **VERIFIED REAL EXECUTION**: {execution_mode} at {execution_timestamp}")
                else:
                    st.warning("⚠️ **UNVERIFIED**: No execution timestamp found - may be cached/dummy data")
                
                # Show full results structure (truncated)
                st.subheader("Debug: Full Results Structure")
                st.json({k: f"{type(v)} ({len(v)} items)" if isinstance(v, (list, dict)) else str(v)[:100] for k, v in results.get('outputs', {}).items()})
            
            # Questions are stored as 'application_questions' in outputs
            application_questions = results['outputs'].get('application_questions', [])
            
            # Fallback: Check for alternative question structures from Live API mode
            if not application_questions:
                # Check for 'questions' key (from QuestionGenerator agent)
                questions_data = results['outputs'].get('questions', {})
                if isinstance(questions_data, dict):
                    # Convert dict structure to list structure
                    application_questions = []
                    for section, section_questions in questions_data.items():
                        if isinstance(section_questions, list):
                            for q in section_questions:
                                if isinstance(q, dict):
                                    q['section'] = section.replace('_', ' ').title()
                                    application_questions.append(q)
                                else:
                                    # Handle string questions
                                    application_questions.append({
                                        'section': section.replace('_', ' ').title(),
                                        'question_text': str(q),
                                        'input_type': 'text',
                                        'required': True
                                    })
            
            if application_questions:
                # Group questions by section
                sections = {}
                for question in application_questions:
                    if isinstance(question, dict):
                        section = question.get('section', 'Other')
                        if section not in sections:
                            sections[section] = []
                        sections[section].append(question)
                
                # Display questions by section
                for section, section_questions in sections.items():
                    st.subheader(section)
                    
                    for i, question in enumerate(section_questions, 1):
                        q_text = question.get('question_text', question.get('question', 'No question text'))
                        input_type = question.get('input_type', '')
                        required = question.get('required', False)
                        help_text = question.get('help_text', '')
                        
                        # Format display
                        required_icon = "🔴" if required else "🟡"
                        type_info = f"({input_type})" if input_type else ""
                        
                        st.write(f"{i}. **{q_text}** {type_info} {required_icon}")
                        if help_text:
                            st.write(f"   _{help_text}_")
                    
                    st.divider()
            else:
                st.warning("No questions data available")
        
        # Tab 4: Validation
        with tabs[3]:
            st.header("Validation Results")
            
            # Check for new validation structure first, then fall back to old structure
            outputs = results.get('outputs', {})
            validation_score = outputs.get('validation_score', 0)
            requirements_validation = outputs.get('requirements_validation', {})
            questions_validation = outputs.get('questions_validation', {})
            overall_quality = outputs.get('overall_quality', 'Unknown')
            
            # Fall back to old structure if new structure not found
            validation_report = outputs.get('validation_report', {})
            
            if validation_score or requirements_validation or questions_validation or validation_report:
                # Overall score - use new structure first
                if validation_score:
                    score_display = float(validation_score) * 100 if float(validation_score) <= 1 else float(validation_score)
                    st.metric("Overall Validation Score", f"{score_display:.1f}%")
                    if overall_quality != 'Unknown':
                        st.info(f"Quality Assessment: {overall_quality}")
                else:
                    overall_score = validation_report.get('overall_score', 0)
                    st.metric("Overall Validation Score", f"{overall_score:.1f}%")
                
                # Requirements validation - use new structure first
                req_val = None
                if requirements_validation:
                    st.subheader("Requirements Validation")
                    req_val = requirements_validation
                elif 'requirement_validation' in validation_report:
                    st.subheader("Requirements Validation")
                    req_val = validation_report['requirement_validation']
                
                if req_val:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_reqs = req_val.get('total_requirements', 0)
                        st.metric("Total Requirements", total_reqs)
                    
                    with col2:
                        valid_reqs = req_val.get('valid_requirements', 0)
                        st.metric("Valid Requirements", valid_reqs)
                    
                    with col3:
                        val_rate = req_val.get('validation_rate', 0)
                        st.metric("Validation Rate", f"{val_rate:.1f}%")
                    
                    # Show errors if any
                    errors = req_val.get('errors', [])
                    if errors:
                        st.subheader("Requirement Errors")
                        for error in errors:
                            req_id = error.get('requirement_id', 'Unknown')
                            error_msgs = error.get('errors', [])
                            st.write(f"🔴 **{req_id}**: {', '.join(error_msgs)}")
                
                # Questions validation
                if 'question_validation' in validation_report:
                    st.subheader("Questions Validation")
                    q_val = validation_report['question_validation']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_questions = q_val.get('total_questions', 0)
                        st.metric("Total Questions", total_questions)
                    
                    with col2:
                        valid_questions = q_val.get('valid_questions', 0)
                        st.metric("Valid Questions", valid_questions)
                    
                    with col3:
                        q_val_rate = q_val.get('validation_rate', 0)
                        st.metric("Validation Rate", f"{q_val_rate:.1f}%")
                    
                    # Show errors if any
                    q_errors = q_val.get('errors', [])
                    if q_errors:
                        st.subheader("Question Errors")
                        for error in q_errors:
                            q_id = error.get('question_id', 'Unknown')
                            error_msgs = error.get('errors', [])
                            st.write(f"🔴 **{q_id}**: {', '.join(error_msgs)}")
                
                # Recommendations from separate section
                recommendations = results['outputs'].get('recommendations', [])
                if recommendations:
                    st.subheader("Recommendations")
                    for rec in recommendations:
                        if isinstance(rec, dict):
                            priority = rec.get('priority', 'medium')
                            category = rec.get('category', '')
                            description = rec.get('description', 'No description')
                            action = rec.get('action', '')
                            
                            priority_icon = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                            category_text = f"[{category}] " if category else ""
                            
                            st.write(f"{priority_icon} **{category_text}{description}**")
                            if action:
                                st.write(f"   _Action: {action}_")
                        else:
                            st.write(f"• {rec}")
            else:
                st.warning("No validation data available")
        
        # Tab 5: Statistics
        with tabs[4]:
            st.header("Workflow Statistics")
            
            # Processing times by stage
            stages = results.get('stages', [])
            if stages:
                stage_data = []
                for stage in stages:
                    stage_data.append({
                        'Stage': stage.get('name', 'Unknown'),
                        'Duration (s)': stage.get('duration_seconds', 0),
                        'Status': stage.get('status', 'unknown')
                    })
                
                df = pd.DataFrame(stage_data)
                
                # Bar chart of processing times
                fig = px.bar(df, x='Stage', y='Duration (s)', color='Status',
                           title="Processing Time by Stage")
                st.plotly_chart(fig, use_container_width=True)
                
                # Stage details table
                st.subheader("Stage Details")
                st.dataframe(df, use_container_width=True)
        
        # Tab 6: Agent Dashboard
        with tabs[5]:
            show_agent_performance_dashboard(results)
        
        # Export options
        st.divider()
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export full results as JSON
            results_json = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="📄 Download Full Results (JSON)",
                data=results_json,
                file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Export questions as JSON
            questions_data = {
                'questions': results['outputs'].get('questions', {}),
                'generated_at': datetime.now().isoformat()
            }
            q_json = json.dumps(questions_data, indent=2, default=str)
            st.download_button(
                label="❓ Download Questions (JSON)",
                data=q_json,
                file_name=f"questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Reset button
        st.divider()
        if st.button("🔄 Reset Workflow", type="secondary"):
            st.session_state.workflow_results = None
            st.session_state.document_info = None
            st.rerun()

elif st.session_state.current_page == "Agent Architecture":
    # Agent Architecture Page
    show_agent_architecture()

elif st.session_state.current_page == "Agent Performance":
    # Agent Performance Dashboard
    if st.session_state.workflow_results:
        show_agent_performance_dashboard(st.session_state.workflow_results)
    else:
        st.info("🔄 Run a workflow first to see agent performance metrics")
        st.markdown("Navigate to **Workflow Analysis** and run the complete workflow to generate performance data.")

elif st.session_state.current_page == "Policy Comparison":
    # Policy Comparison Page
    show_enhanced_policy_comparison()


if __name__ == "__main__":
    pass
