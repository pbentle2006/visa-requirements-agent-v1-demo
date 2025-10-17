"""
Enhanced Side-by-Side Policy Comparison
Focused on Requirements / Questions / Validation structure with detailed similarity analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import sys
from typing import Dict, List, Any, Tuple
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from src.utils.enhanced_document_parser import EnhancedDocumentParser


def show_enhanced_policy_comparison():
    """Display enhanced side-by-side policy comparison."""
    
    st.header("📊 Side-by-Side Visa Policy Comparison")
    st.markdown("**Compare visa requirements, questions, and validation across different policy documents**")
    
    # Policy Selection Section
    st.subheader("🎯 Select Policies to Compare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Policy A**")
        policy_a_type = st.selectbox(
            "Choose first policy:",
            ["Parent Boost Visitor Visa", "Skilled Migrant Residence Visa", "Working Holiday Visa", "Student Visa", "Tourist Visa"],
            key="policy_a"
        )
        
        # Option to upload custom document for Policy A
        uploaded_file_a = st.file_uploader(
            "Or upload custom policy document:",
            type=['txt', 'docx', 'pdf'],
            key="upload_a",
            help="Upload a policy document to analyze"
        )
    
    with col2:
        st.markdown("**Policy B**")
        policy_b_type = st.selectbox(
            "Choose second policy:",
            ["Skilled Migrant Residence Visa", "Parent Boost Visitor Visa", "Working Holiday Visa", "Student Visa", "Tourist Visa"],
            key="policy_b"
        )
        
        # Option to upload custom document for Policy B
        uploaded_file_b = st.file_uploader(
            "Or upload custom policy document:",
            type=['txt', 'docx', 'pdf'],
            key="upload_b",
            help="Upload a policy document to analyze"
        )
    
    if st.button("🔍 Generate Comparison Analysis", type="primary"):
        with st.spinner("Analyzing policies and generating comparison..."):
            
            # Generate or load policy data
            policy_a_data = get_policy_data(policy_a_type, uploaded_file_a)
            policy_b_data = get_policy_data(policy_b_type, uploaded_file_b)
            
            if policy_a_data and policy_b_data:
                # Generate comparison analysis
                comparison_results = generate_detailed_comparison(policy_a_data, policy_b_data)
                
                # Display results
                display_comparison_results(comparison_results, policy_a_type, policy_b_type)
            else:
                st.error("Failed to analyze one or both policies. Please check your selections.")


def get_policy_data(policy_type: str, uploaded_file=None) -> Dict[str, Any]:
    """Get policy data either from uploaded file or predefined data."""
    
    if uploaded_file:
        # Process uploaded file
        try:
            parser = EnhancedDocumentParser()
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Parse document
            doc_result = parser.load_document(tmp_path)
            content = doc_result.get('content', '')
            
            # Run workflow analysis
            orchestrator = WorkflowOrchestrator()
            results = orchestrator.run_workflow(tmp_path, content)
            
            return {
                'type': f"Custom: {uploaded_file.name}",
                'results': results,
                'content': content
            }
            
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            return None
    
    else:
        # Use predefined policy data
        return get_predefined_policy_data(policy_type)


def get_predefined_policy_data(policy_type: str) -> Dict[str, Any]:
    """Get predefined policy data based on policy type."""
    
    # Predefined policy structures based on your requirements
    policy_data = {
        "Parent Boost Visitor Visa": {
            'type': 'Parent Boost Visitor Visa',
            'visa_code': 'V4',
            'requirements_count': 24,
            'questions_count': 15,
            'requirements': [
                # Applicant Requirements (8)
                "Must be outside New Zealand when applying",
                "Must hold valid passport",
                "Must be sponsored by eligible sponsor",
                "Must meet health requirements",
                "Must meet character requirements",
                "Must have genuine intention to visit",
                "Must not intend to work or study",
                "Must have sufficient funds for visit",
                
                # Sponsor Requirements (8)
                "Sponsor must be NZ citizen or resident",
                "Sponsor must be adult child of applicant",
                "Sponsor must complete sponsorship form",
                "Sponsor must meet income requirements",
                "Sponsor must provide accommodation details",
                "Sponsor must provide financial support evidence",
                "Maximum two sponsors per application",
                "Sponsor may sponsor maximum of parents",
                
                # Documentation Requirements (8)
                "Birth certificate showing relationship",
                "Sponsor's citizenship/residence evidence",
                "Medical examination certificates",
                "Police clearance certificates",
                "Financial evidence and bank statements",
                "Travel insurance documentation",
                "Accommodation booking confirmations",
                "Return travel arrangements proof"
            ],
            'questions': [
                "What is your relationship to the sponsor?",
                "What is the purpose of your visit to New Zealand?",
                "How long do you intend to stay?",
                "Who will provide accommodation during your stay?",
                "What is your sponsor's occupation and income?",
                "Have you visited New Zealand before?",
                "Do you have any health conditions?",
                "Have you been convicted of any crimes?",
                "What are your ties to your home country?",
                "How will your visit be funded?",
                "What activities do you plan during your visit?",
                "When do you plan to return home?",
                "Do you have travel insurance?",
                "What is your current employment status?",
                "Do you have any family in New Zealand?"
            ]
        },
        
        "Skilled Migrant Residence Visa": {
            'type': 'Skilled Migrant Residence Visa',
            'visa_code': 'SR1',
            'requirements_count': 28,
            'questions_count': 18,
            'requirements': [
                # Skills and Employment Requirements (10)
                "Must have skilled employment offer",
                "Must meet minimum salary threshold",
                "Must have relevant qualifications",
                "Must have minimum work experience",
                "Must meet English language requirements",
                "Employment must be genuine and sustainable",
                "Employer must be accredited",
                "Job must be on skilled occupation list",
                "Must have employment agreement",
                "Must meet skills assessment criteria",
                
                # Personal Requirements (9)
                "Must be aged 55 or under",
                "Must meet health requirements",
                "Must meet character requirements",
                "Must not have outstanding debts to INZ",
                "Must have genuine intention to reside",
                "Must meet points threshold",
                "Must have acceptable standard of living",
                "Must not be liable for deportation",
                "Must meet residence requirements",
                
                # Documentation Requirements (9)
                "Passport and identity documents",
                "Employment offer documentation",
                "Qualification recognition certificates",
                "English language test results",
                "Medical examination certificates",
                "Police clearance certificates",
                "Evidence of work experience",
                "Financial evidence and statements",
                "Skills assessment documentation"
            ],
            'questions': [
                "What is your occupation and job title?",
                "What is your annual salary offer?",
                "What are your educational qualifications?",
                "How many years of work experience do you have?",
                "What is your English language test score?",
                "Who is your prospective employer?",
                "What will be your main duties and responsibilities?",
                "Have you worked in New Zealand before?",
                "What skills do you bring to New Zealand?",
                "Do you have any health conditions?",
                "Have you been convicted of any crimes?",
                "What are your ties to your home country?",
                "Do you have family in New Zealand?",
                "How will you support yourself initially?",
                "What is your current employment status?",
                "Do you have any outstanding debts?",
                "What is your long-term career plan?",
                "Why do you want to live in New Zealand?"
            ]
        },
        
        "Working Holiday Visa": {
            'type': 'Working Holiday Visa',
            'visa_code': 'WHV',
            'requirements_count': 16,
            'questions_count': 12,
            'requirements': [
                # Age and Nationality Requirements (4)
                "Must be aged 18-30 (or 35 for some countries)",
                "Must hold passport from eligible country",
                "Must not have held WHV before",
                "Must be outside New Zealand when applying",
                
                # Financial Requirements (4)
                "Must have minimum funds (NZ$4,200)",
                "Must have return ticket or funds for one",
                "Must have travel insurance",
                "Must demonstrate access to additional funds",
                
                # Health and Character Requirements (4)
                "Must meet health requirements",
                "Must meet character requirements",
                "Must provide medical certificates if required",
                "Must provide police clearances if required",
                
                # Purpose and Conditions Requirements (4)
                "Primary purpose must be holiday",
                "Work must be incidental to holiday",
                "Must not work for same employer >12 months",
                "Must not study for more than 6 months"
            ],
            'questions': [
                "What is your age and nationality?",
                "What is the primary purpose of your visit?",
                "How much money do you have available?",
                "Do you have a return ticket?",
                "Do you have travel insurance?",
                "Have you held a Working Holiday Visa before?",
                "What type of work do you plan to do?",
                "How long do you intend to stay?",
                "Do you have any health conditions?",
                "Have you been convicted of any crimes?",
                "What are your travel plans in New Zealand?",
                "Do you have accommodation arranged?"
            ]
        }
    }
    
    return policy_data.get(policy_type, {})


def generate_detailed_comparison(policy_a: Dict[str, Any], policy_b: Dict[str, Any]) -> Dict[str, Any]:
    """Generate detailed comparison analysis between two policies."""
    
    # Extract requirements and questions
    reqs_a = set(policy_a.get('requirements', []))
    reqs_b = set(policy_b.get('requirements', []))
    questions_a = set(policy_a.get('questions', []))
    questions_b = set(policy_b.get('questions', []))
    
    # Calculate similarities and differences
    common_requirements = reqs_a.intersection(reqs_b)
    unique_to_a_reqs = reqs_a - reqs_b
    unique_to_b_reqs = reqs_b - reqs_a
    
    common_questions = questions_a.intersection(questions_b)
    unique_to_a_questions = questions_a - questions_b
    unique_to_b_questions = questions_b - questions_a
    
    # Calculate similarity scores
    req_similarity = len(common_requirements) / max(len(reqs_a), len(reqs_b)) * 100 if reqs_a or reqs_b else 0
    question_similarity = len(common_questions) / max(len(questions_a), len(questions_b)) * 100 if questions_a or questions_b else 0
    
    return {
        'policy_a': policy_a,
        'policy_b': policy_b,
        'requirements': {
            'total_a': len(reqs_a),
            'total_b': len(reqs_b),
            'common': list(common_requirements),
            'unique_to_a': list(unique_to_a_reqs),
            'unique_to_b': list(unique_to_b_reqs),
            'similarity_score': req_similarity
        },
        'questions': {
            'total_a': len(questions_a),
            'total_b': len(questions_b),
            'common': list(common_questions),
            'unique_to_a': list(unique_to_a_questions),
            'unique_to_b': list(unique_to_b_questions),
            'similarity_score': question_similarity
        },
        'overall_similarity': (req_similarity + question_similarity) / 2
    }


def display_comparison_results(comparison: Dict[str, Any], policy_a_name: str, policy_b_name: str):
    """Display the comparison results in a structured format."""
    
    # Summary Section
    st.subheader("📊 Comparison Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            f"{policy_a_name} Requirements",
            comparison['requirements']['total_a']
        )
    
    with col2:
        st.metric(
            f"{policy_b_name} Requirements", 
            comparison['requirements']['total_b']
        )
    
    with col3:
        st.metric(
            "Common Questions",
            len(comparison['questions']['common'])
        )
    
    with col4:
        st.metric(
            "Overall Similarity",
            f"{comparison['overall_similarity']:.1f}%"
        )
    
    # Detailed Comparison Tabs
    tabs = st.tabs(["📋 Requirements", "❓ Questions", "📈 Analytics", "🔍 Detailed Analysis"])
    
    # Requirements Tab
    with tabs[0]:
        display_requirements_comparison(comparison, policy_a_name, policy_b_name)
    
    # Questions Tab  
    with tabs[1]:
        display_questions_comparison(comparison, policy_a_name, policy_b_name)
    
    # Analytics Tab
    with tabs[2]:
        display_analytics_comparison(comparison, policy_a_name, policy_b_name)
    
    # Detailed Analysis Tab
    with tabs[3]:
        display_detailed_analysis(comparison, policy_a_name, policy_b_name)


def display_requirements_comparison(comparison: Dict[str, Any], policy_a_name: str, policy_b_name: str):
    """Display side-by-side requirements comparison."""
    
    st.subheader("📋 Requirements Comparison")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Common Requirements", len(comparison['requirements']['common']))
    
    with col2:
        st.metric(f"Unique to {policy_a_name}", len(comparison['requirements']['unique_to_a']))
    
    with col3:
        st.metric(f"Unique to {policy_b_name}", len(comparison['requirements']['unique_to_b']))
    
    # Side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {policy_a_name}")
        st.markdown(f"**Total Requirements: {comparison['requirements']['total_a']}**")
        
        # Common requirements
        if comparison['requirements']['common']:
            st.markdown("**✅ Common Requirements:**")
            for req in comparison['requirements']['common']:
                st.markdown(f"• {req}")
        
        # Unique requirements
        if comparison['requirements']['unique_to_a']:
            st.markdown(f"**🔸 Unique to {policy_a_name}:**")
            for req in comparison['requirements']['unique_to_a']:
                st.markdown(f"• {req}")
    
    with col2:
        st.markdown(f"### {policy_b_name}")
        st.markdown(f"**Total Requirements: {comparison['requirements']['total_b']}**")
        
        # Common requirements (same as left)
        if comparison['requirements']['common']:
            st.markdown("**✅ Common Requirements:**")
            for req in comparison['requirements']['common']:
                st.markdown(f"• {req}")
        
        # Unique requirements
        if comparison['requirements']['unique_to_b']:
            st.markdown(f"**🔹 Unique to {policy_b_name}:**")
            for req in comparison['requirements']['unique_to_b']:
                st.markdown(f"• {req}")


def display_questions_comparison(comparison: Dict[str, Any], policy_a_name: str, policy_b_name: str):
    """Display side-by-side questions comparison."""
    
    st.subheader("❓ Questions Comparison")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Common Questions", len(comparison['questions']['common']))
    
    with col2:
        st.metric(f"Unique to {policy_a_name}", len(comparison['questions']['unique_to_a']))
    
    with col3:
        st.metric(f"Unique to {policy_b_name}", len(comparison['questions']['unique_to_b']))
    
    # Side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {policy_a_name}")
        st.markdown(f"**Total Questions: {comparison['questions']['total_a']}**")
        
        # Common questions
        if comparison['questions']['common']:
            st.markdown("**✅ Common Questions:**")
            for i, question in enumerate(comparison['questions']['common'], 1):
                st.markdown(f"{i}. {question}")
        
        # Unique questions
        if comparison['questions']['unique_to_a']:
            st.markdown(f"**🔸 Unique to {policy_a_name}:**")
            for i, question in enumerate(comparison['questions']['unique_to_a'], 1):
                st.markdown(f"{i}. {question}")
    
    with col2:
        st.markdown(f"### {policy_b_name}")
        st.markdown(f"**Total Questions: {comparison['questions']['total_b']}**")
        
        # Common questions (same as left)
        if comparison['questions']['common']:
            st.markdown("**✅ Common Questions:**")
            for i, question in enumerate(comparison['questions']['common'], 1):
                st.markdown(f"{i}. {question}")
        
        # Unique questions
        if comparison['questions']['unique_to_b']:
            st.markdown(f"**🔹 Unique to {policy_b_name}:**")
            for i, question in enumerate(comparison['questions']['unique_to_b'], 1):
                st.markdown(f"{i}. {question}")


def display_analytics_comparison(comparison: Dict[str, Any], policy_a_name: str, policy_b_name: str):
    """Display analytics and visualizations."""
    
    st.subheader("📈 Comparison Analytics")
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Requirements comparison chart
        fig_req = go.Figure(data=[
            go.Bar(name='Common', x=['Requirements'], y=[len(comparison['requirements']['common'])], marker_color='green'),
            go.Bar(name=policy_a_name, x=['Requirements'], y=[len(comparison['requirements']['unique_to_a'])], marker_color='blue'),
            go.Bar(name=policy_b_name, x=['Requirements'], y=[len(comparison['requirements']['unique_to_b'])], marker_color='orange')
        ])
        fig_req.update_layout(
            title='Requirements Distribution',
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_req, use_container_width=True)
    
    with col2:
        # Questions comparison chart
        fig_q = go.Figure(data=[
            go.Bar(name='Common', x=['Questions'], y=[len(comparison['questions']['common'])], marker_color='green'),
            go.Bar(name=policy_a_name, x=['Questions'], y=[len(comparison['questions']['unique_to_a'])], marker_color='blue'),
            go.Bar(name=policy_b_name, x=['Questions'], y=[len(comparison['questions']['unique_to_b'])], marker_color='orange')
        ])
        fig_q.update_layout(
            title='Questions Distribution',
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_q, use_container_width=True)
    
    # Similarity scores
    st.subheader("🎯 Similarity Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Requirements Similarity",
            f"{comparison['requirements']['similarity_score']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Questions Similarity", 
            f"{comparison['questions']['similarity_score']:.1f}%"
        )
    
    with col3:
        st.metric(
            "Overall Similarity",
            f"{comparison['overall_similarity']:.1f}%"
        )


def display_detailed_analysis(comparison: Dict[str, Any], policy_a_name: str, policy_b_name: str):
    """Display detailed analysis and insights."""
    
    st.subheader("🔍 Detailed Analysis & Insights")
    
    # Key insights
    st.markdown("### 💡 Key Insights")
    
    insights = []
    
    # Requirements insights
    req_diff = abs(comparison['requirements']['total_a'] - comparison['requirements']['total_b'])
    if req_diff > 5:
        more_complex = policy_a_name if comparison['requirements']['total_a'] > comparison['requirements']['total_b'] else policy_b_name
        insights.append(f"**{more_complex}** is significantly more complex with {req_diff} additional requirements")
    
    # Common elements insight
    common_pct = len(comparison['requirements']['common']) / max(comparison['requirements']['total_a'], comparison['requirements']['total_b']) * 100
    if common_pct > 50:
        insights.append(f"**High overlap**: {common_pct:.1f}% of requirements are shared between policies")
    elif common_pct < 25:
        insights.append(f"**Low overlap**: Only {common_pct:.1f}% of requirements are shared - these are quite different visa types")
    
    # Questions insight
    if len(comparison['questions']['common']) >= 10:
        insights.append(f"**{len(comparison['questions']['common'])} questions are identical** - suggesting similar application processes")
    
    for insight in insights:
        st.markdown(f"• {insight}")
    
    # Recommendations
    st.markdown("### 🎯 Recommendations")
    
    recommendations = []
    
    if comparison['overall_similarity'] > 70:
        recommendations.append("Consider consolidating application processes due to high similarity")
        recommendations.append("Shared documentation requirements could be streamlined")
    elif comparison['overall_similarity'] < 30:
        recommendations.append("These visa types serve very different purposes and should maintain separate processes")
        recommendations.append("Consider different application channels for these distinct visa categories")
    
    if len(comparison['requirements']['common']) > 10:
        recommendations.append("Common requirements could be processed through shared assessment modules")
    
    for rec in recommendations:
        st.markdown(f"• {rec}")
    
    # Export options
    st.markdown("### 📥 Export Analysis")
    
    if st.button("📊 Export Comparison Report"):
        # Create downloadable report
        report_data = {
            'comparison_summary': {
                'policy_a': policy_a_name,
                'policy_b': policy_b_name,
                'requirements_a': comparison['requirements']['total_a'],
                'requirements_b': comparison['requirements']['total_b'],
                'questions_a': comparison['questions']['total_a'],
                'questions_b': comparison['questions']['total_b'],
                'common_requirements': len(comparison['requirements']['common']),
                'common_questions': len(comparison['questions']['common']),
                'overall_similarity': comparison['overall_similarity']
            },
            'detailed_comparison': comparison
        }
        
        st.download_button(
            label="📄 Download JSON Report",
            data=json.dumps(report_data, indent=2),
            file_name=f"policy_comparison_{policy_a_name.replace(' ', '_')}_vs_{policy_b_name.replace(' ', '_')}.json",
            mime="application/json"
        )


if __name__ == "__main__":
    show_enhanced_policy_comparison()
