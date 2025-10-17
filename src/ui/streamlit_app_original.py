import streamlit as st
import json
import os
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None

# Navigation
page = st.sidebar.selectbox(
    "🧭 Navigation",
    ["🏠 Main Demo", "📊 Policy Comparison", "🔧 Synthetic Data Generator"],
    index=0
)

# Header
if page == "🏠 Main Demo":
    st.markdown('<div class="main-header">🛂 Visa Requirements Agent Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated Requirements Capture for Immigration Policies</div>', unsafe_allow_html=True)
elif page == "📊 Policy Comparison":
    st.markdown('<div class="main-header">📊 Policy Comparison Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Compare Multiple Visa Policies Side-by-Side</div>', unsafe_allow_html=True)
elif page == "🔧 Synthetic Data Generator":
    st.markdown('<div class="main-header">🔧 Synthetic Data Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate Realistic Policy Documents and Test Data</div>', unsafe_allow_html=True)

# Handle page routing
if page == "📊 Policy Comparison":
    from pages.policy_comparison import show_policy_comparison
    show_policy_comparison()
elif page == "🔧 Synthetic Data Generator":
    from pages.synthetic_data_generator import show_synthetic_data_generator
    show_synthetic_data_generator()
else:
    # Main Demo page content
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Demo mode toggle
        demo_mode = st.toggle("🎭 Demo Mode (No API calls)", value=False, help="Use mock data for demonstrations")
        
        if demo_mode:
            st.info("🎭 Demo mode enabled - using synthetic data")
            api_key = "demo_mode"
        else:
            # Check for API key
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                st.error("⚠️ OPENAI_API_KEY not found in .env file")
                st.info("Please create a .env file with your OpenAI API key")
                api_key_input = st.text_input("Or enter API key here:", type="password")
                if api_key_input:
                    os.environ['OPENAI_API_KEY'] = api_key_input
                    api_key = api_key_input
            else:
                st.success("✅ API Key configured")
        
        st.divider()
        
        # File upload
        st.header("📄 Policy Document")
        
        if demo_mode:
            # Synthetic policy options
            policy_options = {
                "Parent Boost Visitor Visa (Original)": "parent_boost_policy.txt",
                "Tourist Visa (Synthetic)": "tourist_visa.txt", 
                "Skilled Worker Visa (Synthetic)": "skilled_worker_visa.txt",
                "Student Visa (Synthetic)": "student_visa.txt",
                "Family Reunion Visa (Synthetic)": "family_reunion_visa.txt"
            }
            
            selected_policy = st.selectbox("Select Policy Document", list(policy_options.keys()))
            policy_filename = policy_options[selected_policy]
            
            project_root = Path(__file__).parent.parent.parent
            if "Synthetic" in selected_policy:
                policy_path = project_root / 'data' / 'synthetic' / policy_filename
            else:
                policy_path = project_root / 'data' / 'input' / policy_filename
            
            st.info(f"Using: {selected_policy}")
            
        else:
            use_sample = st.checkbox("Use sample Parent Boost policy", value=True)
            
            if use_sample:
                project_root = Path(__file__).parent.parent.parent
                policy_path = project_root / 'data' / 'input' / 'parent_boost_policy.txt'
                st.info(f"Using: {policy_path.name}")
            else:
                uploaded_file = st.file_uploader("Upload Policy Document", type=['txt', 'docx', 'pdf'])
                if uploaded_file:
                    # Save uploaded file
                    project_root = Path(__file__).parent.parent.parent
                    policy_path = project_root / 'data' / 'input' / uploaded_file.name
                    with open(policy_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"Uploaded: {uploaded_file.name}")
                else:
                    policy_path = None
        
        st.divider()
        
        # Execution controls
        st.header("▶️ Execution")
        
        if st.button("🚀 Run Complete Workflow", type="primary", disabled=not api_key or not policy_path):
            if demo_mode:
                with st.spinner("Running demo workflow... Processing through 5-stage AI pipeline..."):
                    try:
                        import time
                        
                        # Add realistic delay to simulate processing (15 seconds for demo presentation)
                        time.sleep(15)
                        
                        # Use mock results generator
                        generator = MockResultsGenerator()
                        
                        # Generate results based on selected policy
                        policy_name = selected_policy.split(" (")[0]  # Remove (Original/Synthetic) suffix
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
                        # Initialize orchestrator
                        st.session_state.orchestrator = WorkflowOrchestrator()
                        
                        # Run workflow
                        results = st.session_state.orchestrator.run_workflow(str(policy_path))
                        st.session_state.workflow_results = results
                        
                        st.success("✅ Workflow completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.workflow_results:
            if st.button("🔄 Reset"):
                st.session_state.workflow_results = None
                st.session_state.orchestrator = None
                st.rerun()

# Main content
if st.session_state.workflow_results is None:
    # Welcome screen
    st.info("👈 Configure settings and click 'Run Complete Workflow' to start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What This Demo Does")
        st.markdown("""
        This multi-agent system automates the process of:
        
        1. **Policy Analysis** - Parse and understand immigration policy documents
        2. **Requirements Capture** - Extract business and technical requirements
        3. **Question Generation** - Generate application form questions
        4. **Validation** - Validate requirements against policy
        5. **Consolidation** - Synthesize into cohesive specification
        """)
    
    with col2:
        st.subheader("📊 Expected Benefits")
        st.markdown("""
        - **Speed**: Reduce requirements gathering from weeks to hours
        - **Coverage**: 95%+ policy requirement capture
        - **Accuracy**: High validation scores
        - **Traceability**: Complete policy-to-question mapping
        - **Automation**: Eliminate manual steps
        """)
    
    st.divider()
    
    st.subheader("🏗️ System Architecture")
    st.markdown("""
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
    
    # Tabs for different views
    tabs = st.tabs([
        "📋 Policy Analysis",
        "📝 Requirements",
        "❓ Questions",
        "✅ Validation",
        "📦 Consolidated",
        "📈 Statistics"
    ])
    
    # Tab 1: Policy Analysis
    with tabs[0]:
        st.subheader("Policy Structure")
        
        policy_structure = results['outputs'].get('policy_structure', {})
        
        if policy_structure:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Visa Information**")
                visa_info = {}
                if policy_structure.get('visa_type'):
                    visa_info['Visa Type'] = policy_structure['visa_type']
                if policy_structure.get('visa_code'):
                    visa_info['Code'] = policy_structure['visa_code']
                if policy_structure.get('version'):
                    visa_info['Version'] = policy_structure['version']
                if policy_structure.get('effective_date'):
                    visa_info['Effective Date'] = policy_structure['effective_date']
                
                if visa_info:
                    st.json(visa_info)
                else:
                    st.info("No visa information available")
                
                st.markdown("**Key Requirements**")
                st.json(policy_structure.get('key_requirements', {}))
            
            with col2:
                st.markdown("**Objectives**")
                st.json(policy_structure.get('objective', {}))
                
                st.markdown("**Stakeholders**")
                stakeholders = policy_structure.get('stakeholders', [])
                for s in stakeholders:
                    st.markdown(f"- {s}")
        
        st.divider()
        
        st.subheader("Eligibility Rules")
        eligibility_rules = results['outputs'].get('eligibility_rules', {})
        
        if eligibility_rules:
            for category, rules in eligibility_rules.items():
                with st.expander(f"**{category.replace('_', ' ').title()}**"):
                    if isinstance(rules, list):
                        for rule in rules:
                            # Handle different data structures
                            description = rule.get('description') or rule.get('requirement', 'No description available')
                            st.markdown(f"- {description}")
                            
                            # Show policy reference if available
                            policy_ref = rule.get('policy_reference') or rule.get('reference')
                            if policy_ref:
                                st.caption(f"Policy Ref: {policy_ref}")
                            
                            # Show mandatory status if available
                            if 'mandatory' in rule:
                                mandatory_text = "✅ Mandatory" if rule['mandatory'] else "⚪ Optional"
                                st.caption(mandatory_text)
    
    # Tab 2: Requirements
    with tabs[1]:
        st.subheader("Requirements by Type")
        
        req_types = {
            'Functional Requirements': results['outputs'].get('functional_requirements', []),
            'Data Requirements': results['outputs'].get('data_requirements', []),
            'Business Rules': results['outputs'].get('business_rules', []),
            'Validation Rules': results['outputs'].get('validation_rules', [])
        }
        
        for req_type, requirements in req_types.items():
            with st.expander(f"**{req_type}** ({len(requirements)} items)"):
                if requirements:
                    for req in requirements[:10]:  # Show first 10
                        # Get requirement ID and description
                        req_id = req.get('requirement_id') or req.get('rule_id') or req.get('validation_id', 'Unknown ID')
                        description = req.get('description') or req.get('rule', 'No description available')
                        st.markdown(f"**{req_id}**: {description}")
                        
                        cols = st.columns([1, 1, 2])
                        with cols[0]:
                            priority = req.get('priority', '')
                            if priority:
                                st.caption(f"Priority: {priority}")
                        with cols[1]:
                            req_type = req.get('type') or req.get('rule_type') or req.get('validation_type') or req.get('category', '')
                            if req_type:
                                st.caption(f"Type: {req_type}")
                        with cols[2]:
                            policy_ref = req.get('policy_reference', '')
                            if policy_ref:
                                st.caption(f"Policy: {policy_ref}")
                        
                        st.divider()
                    
                    if len(requirements) > 10:
                        st.info(f"Showing 10 of {len(requirements)} requirements")
    
    # Tab 3: Questions
    with tabs[2]:
        st.subheader("Application Questions")
        
        questions = results['outputs'].get('application_questions', [])
        
        if questions:
            # Group by section
            sections = {}
            for q in questions:
                section = q.get('section', 'General')
                if section not in sections:
                    sections[section] = []
                sections[section].append(q)
            
            for section, section_questions in sections.items():
                with st.expander(f"**{section}** ({len(section_questions)} questions)"):
                    for q in section_questions:
                        st.markdown(f"**{q.get('question_id', 'N/A')}**: {q.get('question_text', 'N/A')}")
                        
                        cols = st.columns([1, 1, 1, 2])
                        with cols[0]:
                            st.caption(f"Type: {q.get('input_type', 'N/A')}")
                        with cols[1]:
                            st.caption(f"Required: {q.get('required', False)}")
                        with cols[2]:
                            st.caption(f"Policy: {q.get('policy_reference', 'N/A')}")
                        with cols[3]:
                            if q.get('help_text'):
                                st.caption(f"Help: {q['help_text'][:100]}...")
                        
                        st.divider()
        else:
            st.warning("No questions generated")
    
    # Tab 4: Validation
    with tabs[3]:
        st.subheader("Validation Report")
        
        validation_report = results['outputs'].get('validation_report', {})
        
        if validation_report:
            # Overall score
            score = validation_report.get('overall_score', 0)
            st.metric("Overall Validation Score", f"{score:.1f}%")
            
            if score >= 90:
                st.success("✅ Excellent quality!")
            elif score >= 70:
                st.warning("⚠️ Good quality, some improvements needed")
            else:
                st.error("❌ Quality needs improvement")
            
            st.divider()
            
            # Requirement validation
            req_val = validation_report.get('requirement_validation', {})
            if req_val:
                st.markdown("**Requirement Validation**")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Total", req_val.get('total_requirements', 0))
                with cols[1]:
                    st.metric("Valid", req_val.get('valid_requirements', 0))
                with cols[2]:
                    st.metric("Invalid", req_val.get('invalid_requirements', 0))
                
                if req_val.get('errors'):
                    with st.expander("View Errors"):
                        for error in req_val['errors'][:5]:
                            st.error(f"{error.get('requirement_id')}: {error.get('errors')}")
            
            st.divider()
            
            # Question validation
            q_val = validation_report.get('question_validation', {})
            if q_val:
                st.markdown("**Question Validation**")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Total", q_val.get('total_questions', 0))
                with cols[1]:
                    st.metric("Valid", q_val.get('valid_questions', 0))
                with cols[2]:
                    st.metric("Invalid", q_val.get('invalid_questions', 0))
        
        st.divider()
        
        # Gap analysis
        st.subheader("Gap Analysis")
        gap_analysis = results['outputs'].get('gap_analysis', {})
        
        if gap_analysis:
            for gap_type, gaps in gap_analysis.items():
                if isinstance(gaps, list) and gaps:
                    with st.expander(f"**{gap_type.replace('_', ' ').title()}** ({len(gaps)} items)"):
                        for gap in gaps:
                            if isinstance(gap, dict):
                                st.markdown(f"- {gap.get('description', gap)}")
                            else:
                                st.markdown(f"- {gap}")
        
        st.divider()
        
        # Recommendations
        st.subheader("Recommendations")
        recommendations = results['outputs'].get('recommendations', [])
        
        if recommendations:
            for rec in recommendations:
                priority = rec.get('priority', 'medium')
                if priority == 'high':
                    st.error(f"**{rec.get('category', 'N/A').upper()}**: {rec.get('description', 'N/A')}")
                elif priority == 'medium':
                    st.warning(f"**{rec.get('category', 'N/A').upper()}**: {rec.get('description', 'N/A')}")
                else:
                    st.info(f"**{rec.get('category', 'N/A').upper()}**: {rec.get('description', 'N/A')}")
                
                st.caption(f"Action: {rec.get('action', 'N/A')}")
    
    # Tab 5: Consolidated
    with tabs[4]:
        st.subheader("Consolidated Specification")
        
        consolidated_spec = results['outputs'].get('consolidated_spec', {})
        
        if consolidated_spec:
            # Executive summary
            if consolidated_spec.get('executive_summary'):
                st.markdown("### Executive Summary")
                st.write(consolidated_spec['executive_summary'])
            
            # Other sections
            for section_name, section_content in consolidated_spec.items():
                if section_name != 'executive_summary' and section_content:
                    with st.expander(f"**{section_name.replace('_', ' ').title()}**"):
                        if isinstance(section_content, dict):
                            st.json(section_content)
                        elif isinstance(section_content, list):
                            for item in section_content:
                                st.markdown(f"- {item}")
                        else:
                            st.write(section_content)
        
        st.divider()
        
        # Implementation guide
        st.subheader("Implementation Guide")
        impl_guide = results['outputs'].get('implementation_guide', {})
        
        if impl_guide:
            for section_name, section_content in impl_guide.items():
                with st.expander(f"**{section_name.replace('_', ' ').title()}**"):
                    if isinstance(section_content, dict):
                        st.json(section_content)
                    elif isinstance(section_content, list):
                        for item in section_content:
                            if isinstance(item, dict):
                                st.json(item)
                            else:
                                st.markdown(f"- {item}")
                    else:
                        st.write(section_content)
    
    # Tab 6: Statistics
    with tabs[5]:
        st.subheader("Summary Statistics")
        
        summary_stats = results['outputs'].get('summary_statistics', {})
        
        if summary_stats:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Requirements")
                st.metric("Total Requirements", summary_stats.get('total_requirements', 0))
                
                req_by_type = summary_stats.get('requirements_by_type', {})
                if req_by_type:
                    df = pd.DataFrame([
                        {'Type': k.replace('_', ' ').title(), 'Count': v}
                        for k, v in req_by_type.items()
                    ])
                    st.dataframe(df, hide_index=True)
                
                st.markdown("### By Priority")
                req_by_priority = summary_stats.get('requirements_by_priority', {})
                if req_by_priority:
                    df = pd.DataFrame([
                        {'Priority': k.replace('_', ' ').title(), 'Count': v}
                        for k, v in req_by_priority.items()
                    ])
                    st.dataframe(df, hide_index=True)
            
            with col2:
                st.markdown("### Questions")
                st.metric("Total Questions", summary_stats.get('total_questions', 0))
                
                q_by_section = summary_stats.get('questions_by_section', {})
                if q_by_section:
                    df = pd.DataFrame([
                        {'Section': k, 'Count': v}
                        for k, v in q_by_section.items()
                    ])
                    st.dataframe(df, hide_index=True)
                
                st.markdown("### Quality Metrics")
                quality = summary_stats.get('quality_metrics', {})
                if quality:
                    st.metric("Requirement Validation", f"{quality.get('requirement_validation_rate', 0):.1f}%")
                    st.metric("Question Validation", f"{quality.get('question_validation_rate', 0):.1f}%")
        
        st.divider()
        
        # Traceability matrix
        st.subheader("Traceability Matrix")
        traceability = results['outputs'].get('traceability_matrix', [])
        
        if traceability:
            df = pd.DataFrame(traceability)
            st.dataframe(df, hide_index=True)
    
    # Download section
    st.divider()
    st.header("💾 Download Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download full results as JSON
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json_str,
            file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Download requirements
        requirements_data = {
            'functional': results['outputs'].get('functional_requirements', []),
            'data': results['outputs'].get('data_requirements', []),
            'business_rules': results['outputs'].get('business_rules', [])
        }
        req_json = json.dumps(requirements_data, indent=2)
        st.download_button(
            label="📥 Download Requirements (JSON)",
            data=req_json,
            file_name=f"requirements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        # Download questions
        questions_data = results['outputs'].get('application_questions', [])
        q_json = json.dumps(questions_data, indent=2)
        st.download_button(
            label="📥 Download Questions (JSON)",
            data=q_json,
            file_name=f"questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
