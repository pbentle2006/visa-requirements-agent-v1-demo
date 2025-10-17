import streamlit as st
import json
import os
from pathlib import Path
import sys
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from src.utils.output_formatter import OutputFormatter
from src.generators.mock_results_generator import MockResultsGenerator
from src.generators.policy_generator import PolicyGenerator
from src.ui.enhanced_file_upload import show_enhanced_file_upload, get_document_content, get_document_path
from src.ui.agent_dashboard import show_agent_performance_dashboard

def main():
    st.set_page_config(
        page_title="Visa Requirements Agent Demo",
        page_icon="🛂",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🛂 Visa Requirements Agent Demo")
    st.markdown("**AI-Powered Policy Analysis and Requirements Generation**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Mode selection
        mode = st.radio(
            "Select Mode:",
            ["Demo Mode (Mock Data)", "Live API Mode"],
            help="Demo mode uses pre-generated mock data for quick demonstration"
        )
        
        # File upload section
        st.subheader("📄 Document Upload")
        document_info = show_enhanced_file_upload()
        
        # Extract document content if available
        document_content = None
        if document_info:
            document_content = document_info.get('content', '')
        
        # Processing button
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if mode == "Demo Mode (Mock Data)":
                # Use mock data
                with st.spinner("Processing with mock data..."):
                    import time
                    time.sleep(2)  # Simulate processing time
                    
                    mock_generator = MockResultsGenerator()
                    results = mock_generator.generate_complete_workflow_results()
                    st.session_state.results = results
                    st.success("✅ Analysis completed!")
            else:
                # Live API mode
                if document_content:
                    with st.spinner("Processing document with live API..."):
                        try:
                            orchestrator = WorkflowOrchestrator()
                            results = orchestrator.process_document(document_content)
                            st.session_state.results = results
                            st.success("✅ Analysis completed!")
                        except Exception as e:
                            st.error(f"Error processing document: {str(e)}")
                            # Fallback to mock data
                            mock_generator = MockResultsGenerator()
                            results = mock_generator.generate_complete_workflow_results()
                            st.session_state.results = results
                            st.warning("⚠️ Fell back to mock data due to API error")
                else:
                    st.error("Please upload a document first")
    
    # Main content area
    if 'results' not in st.session_state:
        st.info("👈 Please configure settings and start analysis using the sidebar")
        return
    
    results = st.session_state.results
    
    # Create tabs for different views
    tabs = st.tabs([
        "📄 Policy Analysis",
        "📋 Requirements", 
        "❓ Questions",
        "✅ Validation",
        "📊 Statistics",
        "🤖 Agent Dashboard",
        "📊 Policy Comparison",
        "🔄 Synthetic Data"
    ])
    
    # Tab 1: Policy Analysis
    with tabs[0]:
        st.header("📄 Policy Structure Analysis")
        
        if results and 'outputs' in results:
            outputs = results['outputs']
            
            # Policy structure
            if 'policy_structure' in outputs:
                policy_structure = outputs['policy_structure']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Basic Information")
                    visa_type = policy_structure.get('visa_type', 'Unknown')
                    visa_code = policy_structure.get('visa_code', 'Unknown')
                    st.write(f"**Visa Type:** {visa_type}")
                    st.write(f"**Visa Code:** {visa_code}")
                
                with col2:
                    st.subheader("🎯 Objectives")
                    objectives = policy_structure.get('objectives', [])
                    if objectives:
                        for obj in objectives[:3]:
                            st.write(f"• {obj}")
            
            # Eligibility rules
            if 'eligibility_rules' in outputs:
                st.subheader("📜 Eligibility Rules")
                eligibility_rules = outputs['eligibility_rules']
                
                if isinstance(eligibility_rules, list):
                    for rule in eligibility_rules[:5]:
                        if isinstance(rule, dict):
                            description = rule.get('description', rule.get('requirement', str(rule)))
                            mandatory = rule.get('mandatory', True)
                            status_icon = "🔴" if mandatory else "🟡"
                            st.write(f"{status_icon} {description}")
                        else:
                            st.write(f"• {str(rule)}")
        else:
            st.info("No policy analysis data available")
    
    # Tab 2: Requirements
    with tabs[1]:
        st.header("📋 Requirements Analysis")
        
        if results and 'outputs' in results:
            outputs = results['outputs']
            
            # Create requirement sections
            requirement_types = [
                ('functional_requirements', 'Functional Requirements', '⚙️'),
                ('data_requirements', 'Data Requirements', '📊'),
                ('business_rules', 'Business Rules', '💼'),
                ('validation_rules', 'Validation Rules', '✅')
            ]
            
            for req_type, title, icon in requirement_types:
                if req_type in outputs:
                    requirements = outputs[req_type]
                    if requirements:
                        st.subheader(f"{icon} {title}")
                        
                        for req in requirements[:5]:
                            if isinstance(req, dict):
                                req_id = req.get('requirement_id', 'N/A')
                                description = req.get('description', str(req))
                                priority = req.get('priority', 'Unknown')
                                
                                with st.expander(f"{req_id}: {description[:50]}..."):
                                    st.write(f"**Description:** {description}")
                                    st.write(f"**Priority:** {priority}")
                                    if 'policy_reference' in req:
                                        st.write(f"**Reference:** {req['policy_reference']}")
                            else:
                                st.write(f"• {str(req)}")
        else:
            st.info("No requirements data available")
    
    # Tab 3: Questions
    with tabs[2]:
        st.header("❓ Application Questions")
        
        if results and 'outputs' in results and 'application_questions' in results['outputs']:
            questions = results['outputs']['application_questions']
            
            if questions:
                # Group questions by section
                sections = {}
                for q in questions:
                    if isinstance(q, dict):
                        section = q.get('section', 'General')
                        if section not in sections:
                            sections[section] = []
                        sections[section].append(q)
                    else:
                        if 'General' not in sections:
                            sections['General'] = []
                        sections['General'].append({'question': str(q), 'input_type': 'text'})
                
                # Display questions by section
                for section, section_questions in sections.items():
                    st.subheader(f"📝 {section}")
                    
                    for i, q in enumerate(section_questions, 1):
                        if isinstance(q, dict):
                            question_text = q.get('question', q.get('description', str(q)))
                            input_type = q.get('input_type', 'text')
                            required = q.get('required', False)
                            
                            req_indicator = " *" if required else ""
                            st.write(f"**{i}.** {question_text}{req_indicator}")
                            
                            # Show input type
                            if input_type == 'text':
                                st.text_input(f"Answer {i}", key=f"q_{section}_{i}", disabled=True)
                            elif input_type == 'number':
                                st.number_input(f"Answer {i}", key=f"q_{section}_{i}", disabled=True)
                            elif input_type == 'date':
                                st.date_input(f"Answer {i}", key=f"q_{section}_{i}", disabled=True)
                            elif input_type == 'boolean':
                                st.checkbox(f"Answer {i}", key=f"q_{section}_{i}", disabled=True)
                        else:
                            st.write(f"**{i}.** {str(q)}")
                            st.text_input(f"Answer {i}", key=f"q_general_{i}", disabled=True)
            else:
                st.info("No questions generated")
        else:
            st.info("No questions data available")
    
    # Tab 4: Validation
    with tabs[3]:
        st.header("✅ Validation Results")
        
        if results and 'outputs' in results and 'validation_report' in results['outputs']:
            validation = results['outputs']['validation_report']
            
            # Overall score
            overall_score = validation.get('overall_score', 0)
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
                validation_errors = validation.get('validation_errors', 0)
                st.metric("Validation Errors", validation_errors)
            
            # Detailed breakdown
            st.subheader("📊 Score Breakdown")
            
            if 'requirement_validation' in validation:
                req_val = validation['requirement_validation']
                st.write(f"**Requirements Validation:** {req_val.get('validation_rate', 0):.1f}%")
            
            if 'question_validation' in validation:
                q_val = validation['question_validation']
                st.write(f"**Questions Validation:** {q_val.get('validation_rate', 0):.1f}%")
            
            # Recommendations
            if 'recommendations' in validation:
                recommendations = validation['recommendations']
                if recommendations:
                    st.subheader("💡 Recommendations")
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
        st.header("📊 Processing Statistics")
        
        if results:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                duration = results.get('duration_seconds', 0)
                st.metric("Processing Time", f"{duration:.1f}s")
            
            with col2:
                status = results.get('status', 'Unknown')
                st.metric("Status", status)
            
            with col3:
                if 'outputs' in results:
                    total_reqs = (
                        len(results['outputs'].get('functional_requirements', [])) +
                        len(results['outputs'].get('data_requirements', [])) +
                        len(results['outputs'].get('business_rules', [])) +
                        len(results['outputs'].get('validation_rules', []))
                    )
                    st.metric("Total Requirements", total_reqs)
            
            with col4:
                if 'outputs' in results:
                    total_questions = len(results['outputs'].get('application_questions', []))
                    st.metric("Total Questions", total_questions)
            
            # Processing stages
            if 'stages' in results:
                st.subheader("🔄 Processing Stages")
                stages = results['stages']
                
                stages_completed = sum(1 for stage in stages.values() if stage.get('status') in ['completed', 'success'])
                total_stages = len(stages)
                
                progress = stages_completed / total_stages if total_stages > 0 else 0
                st.progress(progress)
                st.write(f"Completed: {stages_completed}/{total_stages} stages")
                
                # Stage details
                for stage_name, stage_info in stages.items():
                    status = stage_info.get('status', 'unknown')
                    duration = stage_info.get('duration_seconds', 0)
                    
                    status_icon = "✅" if status in ['completed', 'success'] else "❌" if status == 'failed' else "⏳"
                    st.write(f"{status_icon} **{stage_name}**: {status} ({duration:.1f}s)")
            
            # Create a simple chart if we have timing data
            if 'stages' in results:
                stage_data = []
                for stage_name, stage_info in results['stages'].items():
                    stage_data.append({
                        'Stage': stage_name,
                        'Duration': stage_info.get('duration_seconds', 0)
                    })
                
                if stage_data:
                    df_stages = pd.DataFrame(stage_data)
                    fig = px.bar(df_stages, x='Stage', y='Duration', title="Processing Time by Stage")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No statistics available")
    
    # Tab 6: Agent Dashboard
    with tabs[5]:
            comparison_data = []
            for policy in selected_policies:
                comparison_data.append({
                    'Policy': policy,
                    'Requirements': random.randint(15, 35),
                    'Questions': random.randint(8, 20),
                    'Validation Score': f"{random.randint(75, 95)}%"
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            fig = px.bar(df, x='Policy', y='Requirements', title="Requirements Comparison")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least 2 policies to compare.")
    
    # Tab 8: Synthetic Data Generator
    with tabs[7]:
        st.header("🤖 Synthetic Data Generator")
        st.markdown("Generate realistic policy documents and mock results.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Policy Generator")
            visa_name = st.text_input("Visa Name", value="Custom Visitor Visa")
            visa_category = st.selectbox("Category", ["visitor", "work", "student", "family"])
            
            if st.button("🚀 Generate Policy", type="primary"):
                policy_content = f"""# {visa_name}
Category: {visa_category.title()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Eligibility Criteria
- Valid passport required
- Proof of financial support
- Clean criminal record

## Application Process
1. Complete online form
2. Submit documents
3. Pay fees
4. Attend interview"""
                
                st.success("✅ Policy generated!")
                st.text_area("Generated Content", policy_content, height=200)
                
                st.download_button(
                    "📥 Download Policy",
                    policy_content,
                    file_name=f"{visa_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            st.subheader("🔄 Mock Results Generator")
            policy_name = st.text_input("Policy Name", value="Sample Policy")
            num_requirements = st.slider("Requirements", 10, 50, 25)
            validation_score = st.slider("Validation Score (%)", 70, 100, 85)
            
            if st.button("🚀 Generate Results", type="primary"):
                mock_results = {
                    'policy_name': policy_name,
                    'total_requirements': num_requirements,
                    'validation_score': validation_score,
                    'status': 'completed',
                    'generated_at': datetime.now().isoformat()
                }
                
                st.success("✅ Results generated!")
                st.json(mock_results)
                
                st.download_button(
                    "📥 Download Results",
                    json.dumps(mock_results, indent=2),
                    file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Download section
    st.divider()
    st.header("💾 Download Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json_str,
            file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


if __name__ == "__main__":
    main()
