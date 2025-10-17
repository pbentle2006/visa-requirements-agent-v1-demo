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
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
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

# Main navigation
main_tabs = st.tabs(["🚀 Workflow Analysis", "📊 Policy Comparison"])

# Initialize session state
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'document_info' not in st.session_state:
    st.session_state.document_info = None

# Sidebar configuration (outside tabs so it's always visible)
with st.sidebar:
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

# Tab 1: Workflow Analysis
with main_tabs[0]:
    # Main content area
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
                    print(f"🔥🔥🔥 FORCING COMPLETE SESSION STATE RESET 🔥🔥🔥", flush=True)
                    if 'workflow_results' in st.session_state:
                        del st.session_state.workflow_results
                    if 'orchestrator' in st.session_state:
                        del st.session_state.orchestrator
                    
                    # Initialize fresh orchestrator
                    st.session_state.orchestrator = WorkflowOrchestrator()
                    
                    # Get document path for workflow
                    policy_path = get_document_path(document_info)
                    policy_content = get_document_content(document_info)
                    
                    # HYBRID APPROACH - Detect visa type but use real agents
                    detected_visa_type = None
                    detected_visa_code = None
                    
                    if policy_content:
                        print(f"🔥 HYBRID: Analyzing document content for visa type detection 🔥", flush=True)
                        print(f"🔥 Document content length: {len(policy_content)} 🔥", flush=True)
                        print(f"🔥 First 500 chars: {policy_content[:500]} 🔥", flush=True)
                        
                        # Enhanced detection with more keywords
                        content_upper = policy_content.upper()
                        print(f"🔥 Checking for PARENT BOOST: {'PARENT BOOST' in content_upper} 🔥", flush=True)
                        print(f"🔥 Checking for V4: {'V4' in content_upper} 🔥", flush=True)
                        print(f"🔥 Checking for PARENT: {'PARENT' in content_upper} 🔥", flush=True)
                        print(f"🔥 Checking for BOOST: {'BOOST' in content_upper} 🔥", flush=True)
                        print(f"🔥 Checking for VISITOR: {'VISITOR' in content_upper} 🔥", flush=True)
                        
                        if any(keyword in content_upper for keyword in ['PARENT BOOST VISITOR VISA', 'PARENT BOOST', 'V4']):
                            detected_visa_type = "Parent Boost Visitor Visa"
                            detected_visa_code = "V4"
                            print(f"🔥 HYBRID: DETECTED PARENT BOOST VISA - PROCESSING WITH REAL AGENTS 🔥", flush=True)
                        elif any(keyword in content_upper for keyword in ['SKILLED MIGRANT', 'SR1', 'SR3', 'SR4', 'SR5', 'SKILLED RESIDENCE']):
                            detected_visa_type = "Skilled Migrant Residence Visa"
                            detected_visa_code = "SR1"
                            print(f"🔥 HYBRID: DETECTED SKILLED MIGRANT VISA - PROCESSING WITH REAL AGENTS 🔥", flush=True)
                        elif any(keyword in content_upper for keyword in ['WORKING HOLIDAY', 'YOUTH', 'TEMPORARY WORK', 'WHV', 'WORKING HOLIDAY VISA']):
                            detected_visa_type = "Working Holiday Visa"
                            detected_visa_code = "WHV"
                            print(f"🔥 HYBRID: DETECTED WORKING HOLIDAY VISA - PROCESSING WITH REAL AGENTS 🔥", flush=True)
                        else:
                            print(f"🔥 HYBRID: NO SPECIFIC VISA TYPE DETECTED - USING GENERIC PROCESSING 🔥", flush=True)
                            print(f"🔥 Content sample for debugging: {content_upper[:200]} 🔥", flush=True)
                    
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
                    if st.checkbox("Show Debug Info"):
                        st.exception(e)
    
    # Show architecture overview when no results
    if not has_document:
        st.info("👆 Please select or upload a policy document to begin")
    elif not has_api_key:
        st.info("👆 Please configure your OpenAI API key to run the workflow")
    
    # Architecture diagram
    st.header("🏗️ System Architecture")
    st.markdown("""
    The Visa Requirements Agent uses a sophisticated 5-stage AI pipeline:
    
    ```
    Policy Document → PolicyEvaluator → RequirementsCapture → QuestionGenerator
                                                                      ↓
                      ConsolidationAgent ← ValidationAgent ←──────────┘
    ```
    """)

else:
    # Results display
    results = st.session_state.workflow_results
    
    # Summary metrics
    st.header("📊 Workflow Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Status", results['status'].upper())
    
    with col2:
        st.metric("Duration", f"{results['duration_seconds']:.1f}s")
    
    with col3:
        stages_completed = sum(1 for s in results['stages'] if s['status'] in ['success', 'completed'])
        st.metric("Stages Completed", f"{stages_completed}/{len(results['stages'])}")
    
    with col4:
        validation_score = results['outputs'].get('validation_report', {}).get('overall_score', 0)
        st.metric("Validation Score", f"{validation_score:.1f}%")
    
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
            # Basic info
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
            
            # Sections
            sections = policy_structure.get('sections', {})
            if sections:
                st.subheader("Policy Sections")
                for section_id, section_data in sections.items():
                    with st.expander(f"Section {section_id}: {section_data.get('title', 'No title')}"):
                        st.write(section_data.get('content', 'No content available')[:500] + "...")
        else:
            st.info("No policy structure data available")
        
        # Eligibility Rules
        st.header("Eligibility Rules")
        eligibility_rules = results['outputs'].get('eligibility_rules', [])
        if eligibility_rules:
            for rule in eligibility_rules:
                # Handle both string and dictionary formats
                if isinstance(rule, str):
                    # If it's a string, display it directly
                    st.write(f"🟡 **General**: {rule}")
                elif isinstance(rule, dict):
                    # If it's a dictionary, extract fields
                    rule_type = rule.get('type', 'general')
                    description = rule.get('description') or rule.get('requirement', 'No description')
                    mandatory = rule.get('mandatory', False)
                    
                    status_icon = "🔴" if mandatory else "🟡"
                    st.write(f"{status_icon} **{rule_type.title()}**: {description}")
                else:
                    # Fallback for other types
                    st.write(f"🟡 **General**: {str(rule)}")
        else:
            st.info("No eligibility rules extracted")
    
    # Tab 2: Requirements
    with tabs[1]:
        st.header("Requirements by Type")
        
        # Get all requirement types
        req_types = ['functional_requirements', 'data_requirements', 'business_rules', 'validation_rules']
        
        for req_type in req_types:
            requirements = results['outputs'].get(req_type, [])
            if requirements:
                display_name = req_type.replace('_', ' ').title()
                
                with st.expander(f"{display_name} ({len(requirements)} items)", expanded=False):
                    for req in requirements:
                        # Handle both string and dictionary formats
                        if isinstance(req, str):
                            # If it's a string, display it directly
                            st.write(f"• {req}")
                        elif isinstance(req, dict):
                            # If it's a dictionary, extract fields
                            req_id = req.get('requirement_id', 'No ID')
                            description = req.get('description', 'No description')
                            priority = req.get('priority', 'unknown')
                            policy_ref = req.get('policy_reference', 'No reference')
                            
                            # Priority color coding
                            priority_colors = {
                                'must_have': '🔴',
                                'should_have': '🟡', 
                                'could_have': '🟢'
                            }
                            priority_icon = priority_colors.get(priority, '⚪')
                            
                            st.markdown(f"""
                            **{req_id}**: {description}
                            - Priority: {priority_icon} {priority.replace('_', ' ').title()}
                            - Policy: {policy_ref}
                            """)
                        else:
                            # Fallback for other types
                            st.write(f"• {str(req)}")
    
    # Tab 3: Questions
    with tabs[2]:
        st.header("Application Questions")
        
        questions = results['outputs'].get('application_questions', [])
        if questions:
            # Group by section
            sections = {}
            for q in questions:
                if isinstance(q, dict):
                    section = q.get('section', 'Other')
                    if section not in sections:
                        sections[section] = []
                    sections[section].append(q)
                else:
                    # Handle non-dict questions
                    if 'Other' not in sections:
                        sections['Other'] = []
                    sections['Other'].append(q)
            
            for section_name, section_questions in sections.items():
                with st.expander(f"{section_name} ({len(section_questions)} questions)", expanded=False):
                    for q in section_questions:
                        if isinstance(q, str):
                            # If it's a string, display it directly
                            st.write(f"• {q}")
                        elif isinstance(q, dict):
                            # If it's a dictionary, extract fields
                            question_id = q.get('question_id', 'No ID')
                            question_text = q.get('question_text', 'No question text')
                            input_type = q.get('input_type', 'text')
                            required = q.get('required', False)
                            help_text = q.get('help_text', '')
                            
                            required_icon = "🔴" if required else "⚪"
                            
                            st.markdown(f"""
                            **{question_id}**: {question_text}
                            - Type: {input_type} {required_icon}
                            - Help: {help_text}
                            """)
                        else:
                            # Fallback for other types
                            st.write(f"• {str(q)}")
        else:
            st.warning("No questions generated")
    
    # Tab 4: Validation
    with tabs[3]:
        st.header("Validation Results")
        
        validation_report = results['outputs'].get('validation_report', {})
        if validation_report:
            # Overall score
            overall_score = validation_report.get('overall_score', 0)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Overall Score", f"{overall_score:.1f}%")
            
            with col2:
                if overall_score >= 90:
                    st.success("Excellent Quality")
                elif overall_score >= 75:
                    st.info("Good Quality")
                elif overall_score >= 60:
                    st.warning("Fair Quality")
                else:
                    st.error("Needs Improvement")
            
            with col3:
                validation_errors = validation_report.get('validation_errors', 0)
                st.metric("Validation Errors", validation_errors)
            
            # Detailed breakdown
            st.subheader("Score Breakdown")
            
            if 'requirement_validation' in validation_report:
                req_val = validation_report['requirement_validation']
                st.write(f"**Requirements Validation:** {req_val.get('validation_rate', 0):.1f}%")
            
            if 'question_validation' in validation_report:
                q_val = validation_report['question_validation']
                st.write(f"**Questions Validation:** {q_val.get('validation_rate', 0):.1f}%")
            
            # Recommendations
            if 'recommendations' in validation_report:
                recommendations = validation_report['recommendations']
                if recommendations:
                    st.subheader("Recommendations")
                    for rec in recommendations[:5]:
                        if isinstance(rec, dict):
                            priority = rec.get('priority', 'medium')
                            description = rec.get('description', str(rec))
                            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                            st.write(f"{priority_icon} {description}")
                        else:
                            st.write(f"• {str(rec)}")
        else:
            st.info("No validation data available")
    
    # Tab 5: Statistics
    with tabs[4]:
        st.header("Workflow Statistics")
        
        summary_stats = results['outputs'].get('summary_statistics', {})
        if summary_stats:
            # Requirements breakdown
            req_by_type = summary_stats.get('requirements_by_type', {})
            if req_by_type:
                st.subheader("Requirements by Type")
                df_req = pd.DataFrame([
                    {'Type': k.replace('_', ' ').title(), 'Count': v}
                    for k, v in req_by_type.items()
                ])
                fig = px.pie(df_req, values='Count', names='Type', title="Requirements Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            # Questions breakdown
            q_by_section = summary_stats.get('questions_by_section', {})
            if q_by_section:
                st.subheader("Questions by Section")
                df_q = pd.DataFrame([
                    {'Section': k, 'Count': v}
                    for k, v in q_by_section.items()
                ])
                fig = px.bar(df_q, x='Section', y='Count', title="Questions by Section")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No statistics available")
    
    # Tab 6: Agent Dashboard
    with tabs[5]:
        show_agent_performance_dashboard(results)
    
    # Download section
    st.divider()
    st.header("💾 Download Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        # Full results download
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json_str,
            file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Requirements only
        requirements_data = {
            'functional_requirements': results['outputs'].get('functional_requirements', []),
            'data_requirements': results['outputs'].get('data_requirements', []),
            'business_rules': results['outputs'].get('business_rules', []),
            'validation_rules': results['outputs'].get('validation_rules', [])
        }
        req_json = json.dumps(requirements_data, indent=2, default=str)
        st.download_button(
            label="📋 Download Requirements (JSON)",
            data=req_json,
            file_name=f"requirements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        # Questions only
        questions_data = {
            'application_questions': results['outputs'].get('application_questions', []),
            'conditional_logic': results['outputs'].get('conditional_logic', {})
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

# Tab 2: Policy Comparison
with main_tabs[1]:
    show_enhanced_policy_comparison()


if __name__ == "__main__":
    pass
