"""
Enhanced Policy Comparison Page

Advanced policy comparison with detailed analytics, visual diffs, and compliance analysis.
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import sys
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.generators.mock_results_generator import MockResultsGenerator
from src.generators.policy_generator import PolicyGenerator


def show_policy_comparison():
    """Display the enhanced policy comparison interface."""
    
    st.header("📊 Advanced Policy Comparison Dashboard")
    st.markdown("Compare multiple visa policies with detailed analytics, visual diffs, and compliance analysis.")
    
    # Initialize generators
    if 'mock_generator' not in st.session_state:
        st.session_state.mock_generator = MockResultsGenerator()
    if 'policy_generator' not in st.session_state:
        st.session_state.policy_generator = PolicyGenerator()
    
    # Enhanced policy selection with metadata
    st.subheader("🎯 Policy Selection & Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        available_policies = {
            "Parent Boost Visitor Visa": {"complexity": "High", "sections": 12, "type": "Family", "processing_days": 45},
            "Tourist Visa": {"complexity": "Low", "sections": 6, "type": "Temporary", "processing_days": 15},
            "Skilled Worker Visa": {"complexity": "High", "sections": 15, "type": "Work", "processing_days": 60},
            "International Student Visa": {"complexity": "Medium", "sections": 9, "type": "Study", "processing_days": 30},
            "Family Reunion Visa": {"complexity": "Medium", "sections": 8, "type": "Family", "processing_days": 35},
            "Business Investor Visa": {"complexity": "High", "sections": 14, "type": "Investment", "processing_days": 90},
            "Humanitarian Visa": {"complexity": "Medium", "sections": 10, "type": "Protection", "processing_days": 120}
        }
        
        selected_policies = st.multiselect(
            "Choose 2-5 policies to compare:",
            list(available_policies.keys()),
            default=["Parent Boost Visitor Visa", "Tourist Visa", "Skilled Worker Visa"],
            max_selections=5,
            help="Select policies for detailed comparison analysis"
        )
    
    with col2:
        if selected_policies:
            st.write("**Selected Policies:**")
            for policy in selected_policies:
                metadata = available_policies[policy]
                st.write(f"• **{policy}**")
                st.write(f"  - Type: {metadata['type']}")
                st.write(f"  - Complexity: {metadata['complexity']}")
                st.write(f"  - Sections: {metadata['sections']}")
                st.write(f"  - Processing: {metadata['processing_days']} days")
    
    if len(selected_policies) < 2:
        st.warning("Please select at least 2 policies to compare.")
        return
    
    # Generate comparison data
    with st.spinner("Generating comparison analysis..."):
        comparison_data = generate_comparison_data(selected_policies, available_policies)
    
    # Comparison tabs
    comparison_tabs = st.tabs([
        "📊 Overview",
        "📋 Requirements Analysis",
        "❓ Questions Comparison", 
        "🎯 Validation Metrics",
        "📈 Visual Analytics",
        "🔍 Detailed Diff"
    ])
    
    # Tab 1: Overview
    with comparison_tabs[0]:
        show_comparison_overview(comparison_data)
    
    # Tab 2: Requirements Analysis
    with comparison_tabs[1]:
        show_requirements_comparison(comparison_data)
    
    # Tab 3: Questions Comparison
    with comparison_tabs[2]:
        show_questions_comparison(comparison_data)
    
    # Tab 4: Validation Metrics
    with comparison_tabs[3]:
        show_validation_comparison(comparison_data)
    
    # Tab 5: Visual Analytics
    with comparison_tabs[4]:
        show_visual_analytics(comparison_data)
    
    # Tab 6: Detailed Diff
    with comparison_tabs[5]:
        show_detailed_diff(comparison_data)


def generate_comparison_data(selected_policies: List[str], policy_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive comparison data for selected policies."""
    
    mock_generator = MockResultsGenerator()
    comparison_data = {
        'policies': {},
        'summary': {},
        'analytics': {}
    }
    
    for policy in selected_policies:
        # Generate workflow results for each policy
        results = mock_generator.generate_complete_workflow_results(policy)
        
        comparison_data['policies'][policy] = {
            'results': results,
            'metadata': {**policy_metadata[policy], **extract_policy_metadata(results)},
            'metrics': calculate_policy_metrics(results)
        }
    
    # Generate cross-policy analytics
    comparison_data['analytics'] = generate_cross_policy_analytics(comparison_data['policies'])
    comparison_data['summary'] = generate_comparison_summary(comparison_data['policies'])
    
    return comparison_data


def extract_policy_metadata(results: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key metadata from policy results."""
    
    outputs = results.get('outputs', {})
    
    return {
        'visa_type': outputs.get('policy_structure', {}).get('visa_type', 'Unknown'),
        'visa_code': outputs.get('policy_structure', {}).get('visa_code', 'Unknown'),
        'total_requirements': len(outputs.get('functional_requirements', [])) + 
                           len(outputs.get('data_requirements', [])) + 
                           len(outputs.get('business_rules', [])) + 
                           len(outputs.get('validation_rules', [])),
        'total_questions': len(outputs.get('application_questions', [])),
        'validation_score': outputs.get('validation_report', {}).get('overall_score', 0),
        'processing_time': results.get('duration_seconds', 0),
        'complexity_score': calculate_complexity_score(outputs)
    }


def calculate_complexity_score(outputs: Dict[str, Any]) -> float:
    """Calculate policy complexity score based on various factors."""
    
    # Factors contributing to complexity
    sections = len(outputs.get('policy_structure', {}).get('sections', {}))
    rules = len(outputs.get('eligibility_rules', []))
    conditions = len(outputs.get('conditions', []))
    requirements = len(outputs.get('functional_requirements', [])) + len(outputs.get('data_requirements', []))
    questions = len(outputs.get('application_questions', []))
    
    # Weighted complexity calculation
    complexity = (sections * 2) + (rules * 1.5) + (conditions * 1.2) + (requirements * 0.8) + (questions * 0.5)
    
    # Normalize to 0-100 scale
    return min(100, complexity * 2)


def calculate_policy_metrics(results: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate comprehensive metrics for a policy."""
    
    outputs = results.get('outputs', {})
    
    return {
        'requirement_distribution': {
            'functional': len(outputs.get('functional_requirements', [])),
            'data': len(outputs.get('data_requirements', [])),
            'business': len(outputs.get('business_rules', [])),
            'validation': len(outputs.get('validation_rules', []))
        },
        'question_sections': count_question_sections(outputs.get('application_questions', [])),
        'validation_breakdown': extract_validation_breakdown(outputs.get('validation_report', {})),
        'coverage_analysis': analyze_policy_coverage(outputs)
    }


def count_question_sections(questions: List[Dict]) -> Dict[str, int]:
    """Count questions by section."""
    
    sections = {}
    for q in questions:
        if isinstance(q, dict):
            section = q.get('section', 'Other')
            sections[section] = sections.get(section, 0) + 1
        else:
            sections['Other'] = sections.get('Other', 0) + 1
    
    return sections


def extract_validation_breakdown(validation_report: Dict[str, Any]) -> Dict[str, float]:
    """Extract validation score breakdown."""
    
    if not validation_report:
        return {'overall': 0, 'requirements': 0, 'questions': 0, 'coverage': 0}
    
    req_val = validation_report.get('requirement_validation', {})
    q_val = validation_report.get('question_validation', {})
    cov_val = validation_report.get('coverage_analysis', {}).get('requirement_coverage', {})
    
    return {
        'overall': validation_report.get('overall_score', 0),
        'requirements': req_val.get('validation_rate', 0) if isinstance(req_val, dict) else 0,
        'questions': q_val.get('validation_rate', 0) if isinstance(q_val, dict) else 0,
        'coverage': cov_val.get('coverage_percentage', 0) if isinstance(cov_val, dict) else 0
    }


def analyze_policy_coverage(outputs: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze policy coverage comprehensiveness."""
    
    policy_structure = outputs.get('policy_structure', {})
    sections = policy_structure.get('sections', {}) if isinstance(policy_structure, dict) else {}
    
    return {
        'total_sections': len(sections),
        'covered_areas': list(sections.keys()) if sections else [],
        'coverage_depth': calculate_coverage_depth(sections)
    }


def calculate_coverage_depth(sections: Dict[str, Any]) -> float:
    """Calculate depth of policy coverage."""
    
    if not sections:
        return 0
    
    total_content = sum(len(str(content)) for content in sections.values())
    avg_content_length = total_content / len(sections)
    
    # Normalize to 0-100 scale (assuming 500 chars is good depth)
    return min(100, (avg_content_length / 500) * 100)


def generate_cross_policy_analytics(policies: Dict[str, Any]) -> Dict[str, Any]:
    """Generate analytics across all policies."""
    
    analytics = {
        'complexity_comparison': {},
        'requirement_patterns': {},
        'validation_trends': {},
        'processing_efficiency': {}
    }
    
    for policy_name, policy_data in policies.items():
        metadata = policy_data['metadata']
        metrics = policy_data['metrics']
        
        analytics['complexity_comparison'][policy_name] = metadata.get('complexity_score', 0)
        analytics['requirement_patterns'][policy_name] = metrics['requirement_distribution']
        analytics['validation_trends'][policy_name] = metrics['validation_breakdown']
        analytics['processing_efficiency'][policy_name] = {
            'processing_time': metadata.get('processing_time', 0),
            'validation_score': metadata.get('validation_score', 0),
            'efficiency_ratio': metadata.get('validation_score', 0) / max(metadata.get('processing_time', 1), 1)
        }
    
    return analytics


def generate_comparison_summary(policies: Dict[str, Any]) -> Dict[str, Any]:
    """Generate high-level comparison summary."""
    
    summary = {
        'total_policies': len(policies),
        'avg_complexity': 0,
        'avg_validation_score': 0,
        'most_complex': '',
        'highest_validation': '',
        'fastest_processing': ''
    }
    
    if not policies:
        return summary
    
    complexities = []
    validation_scores = []
    processing_times = []
    
    for policy_name, policy_data in policies.items():
        metadata = policy_data['metadata']
        
        complexity = metadata.get('complexity_score', 0)
        validation = metadata.get('validation_score', 0)
        processing = metadata.get('processing_time', 0)
        
        complexities.append((policy_name, complexity))
        validation_scores.append((policy_name, validation))
        processing_times.append((policy_name, processing))
    
    # Calculate averages
    summary['avg_complexity'] = sum(c[1] for c in complexities) / len(complexities)
    summary['avg_validation_score'] = sum(v[1] for v in validation_scores) / len(validation_scores)
    
    # Find extremes
    summary['most_complex'] = max(complexities, key=lambda x: x[1])[0]
    summary['highest_validation'] = max(validation_scores, key=lambda x: x[1])[0]
    summary['fastest_processing'] = min(processing_times, key=lambda x: x[1])[0]
    
    return summary


def show_comparison_overview(comparison_data: Dict[str, Any]):
    """Show high-level comparison overview."""
    
    st.subheader("📊 Comparison Overview")
    
    summary = comparison_data['summary']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Policies Compared", summary['total_policies'])
    
    with col2:
        st.metric("Avg Complexity", f"{summary['avg_complexity']:.1f}")
    
    with col3:
        st.metric("Avg Validation", f"{summary['avg_validation_score']:.1f}%")
    
    with col4:
        st.metric("Most Complex", summary['most_complex'])
    
    # Policy comparison table
    st.subheader("📋 Policy Comparison Table")
    
    table_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        metadata = policy_data['metadata']
        table_data.append({
            'Policy': policy_name,
            'Type': metadata.get('type', 'Unknown'),
            'Complexity': metadata.get('complexity', 'Unknown'),
            'Requirements': metadata.get('total_requirements', 0),
            'Questions': metadata.get('total_questions', 0),
            'Validation Score': f"{metadata.get('validation_score', 0):.1f}%",
            'Processing Days': metadata.get('processing_days', 0)
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)


def show_requirements_comparison(comparison_data: Dict[str, Any]):
    """Show detailed requirements comparison."""
    
    st.subheader("📋 Requirements Analysis")
    
    # Requirements distribution chart
    req_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        req_dist = policy_data['metrics']['requirement_distribution']
        for req_type, count in req_dist.items():
            req_data.append({
                'Policy': policy_name,
                'Requirement Type': req_type.title(),
                'Count': count
            })
    
    if req_data:
        df_req = pd.DataFrame(req_data)
        
        fig = px.bar(
            df_req, 
            x='Policy', 
            y='Count', 
            color='Requirement Type',
            title="Requirements Distribution by Policy",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Requirements heatmap
        pivot_df = df_req.pivot(index='Policy', columns='Requirement Type', values='Count').fillna(0)
        
        fig_heatmap = px.imshow(
            pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            title="Requirements Heatmap",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)


def show_questions_comparison(comparison_data: Dict[str, Any]):
    """Show questions comparison analysis."""
    
    st.subheader("❓ Questions Comparison")
    
    # Questions by section
    questions_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        question_sections = policy_data['metrics']['question_sections']
        for section, count in question_sections.items():
            questions_data.append({
                'Policy': policy_name,
                'Section': section,
                'Questions': count
            })
    
    if questions_data:
        df_questions = pd.DataFrame(questions_data)
        
        fig = px.sunburst(
            df_questions,
            path=['Policy', 'Section'],
            values='Questions',
            title="Questions Distribution by Policy and Section"
        )
        st.plotly_chart(fig, use_container_width=True)


def show_validation_comparison(comparison_data: Dict[str, Any]):
    """Show validation metrics comparison."""
    
    st.subheader("🎯 Validation Metrics Comparison")
    
    # Validation scores comparison
    validation_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        val_breakdown = policy_data['metrics']['validation_breakdown']
        for metric, score in val_breakdown.items():
            validation_data.append({
                'Policy': policy_name,
                'Metric': metric.title(),
                'Score': score
            })
    
    if validation_data:
        df_val = pd.DataFrame(validation_data)
        
        fig = px.line_polar(
            df_val,
            r='Score',
            theta='Metric',
            color='Policy',
            line_close=True,
            title="Validation Scores Radar Chart"
        )
        st.plotly_chart(fig, use_container_width=True)


def show_visual_analytics(comparison_data: Dict[str, Any]):
    """Show advanced visual analytics."""
    
    st.subheader("📈 Visual Analytics")
    
    analytics = comparison_data['analytics']
    
    # Complexity vs Validation scatter plot
    scatter_data = []
    for policy_name in comparison_data['policies'].keys():
        complexity = analytics['complexity_comparison'][policy_name]
        validation = analytics['validation_trends'][policy_name]['overall']
        processing = analytics['processing_efficiency'][policy_name]['processing_time']
        
        scatter_data.append({
            'Policy': policy_name,
            'Complexity': complexity,
            'Validation Score': validation,
            'Processing Time': processing
        })
    
    if scatter_data:
        df_scatter = pd.DataFrame(scatter_data)
        
        fig = px.scatter(
            df_scatter,
            x='Complexity',
            y='Validation Score',
            size='Processing Time',
            color='Policy',
            title="Complexity vs Validation Score (Size = Processing Time)",
            hover_data=['Processing Time']
        )
        st.plotly_chart(fig, use_container_width=True)


def show_detailed_diff(comparison_data: Dict[str, Any]):
    """Show detailed policy differences."""
    
    st.subheader("🔍 Detailed Policy Differences")
    
    if len(comparison_data['policies']) < 2:
        st.warning("Need at least 2 policies for detailed comparison.")
        return
    
    # Select two policies for detailed diff
    policy_names = list(comparison_data['policies'].keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        policy1 = st.selectbox("Select first policy:", policy_names, key="diff_policy1")
    
    with col2:
        policy2 = st.selectbox("Select second policy:", policy_names, index=1 if len(policy_names) > 1 else 0, key="diff_policy2")
    
    if policy1 == policy2:
        st.warning("Please select two different policies.")
        return
    
    # Show detailed comparison
    show_policy_diff(comparison_data['policies'][policy1], comparison_data['policies'][policy2], policy1, policy2)


def show_policy_diff(policy1_data: Dict[str, Any], policy2_data: Dict[str, Any], name1: str, name2: str):
    """Show detailed differences between two policies."""
    
    st.write(f"### Comparing **{name1}** vs **{name2}**")
    
    # Metadata comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"#### {name1}")
        metadata1 = policy1_data['metadata']
        st.write(f"- **Type**: {metadata1.get('type', 'Unknown')}")
        st.write(f"- **Complexity**: {metadata1.get('complexity_score', 0):.1f}")
        st.write(f"- **Requirements**: {metadata1.get('total_requirements', 0)}")
        st.write(f"- **Questions**: {metadata1.get('total_questions', 0)}")
        st.write(f"- **Validation**: {metadata1.get('validation_score', 0):.1f}%")
    
    with col2:
        st.write(f"#### {name2}")
        metadata2 = policy2_data['metadata']
        st.write(f"- **Type**: {metadata2.get('type', 'Unknown')}")
        st.write(f"- **Complexity**: {metadata2.get('complexity_score', 0):.1f}")
        st.write(f"- **Requirements**: {metadata2.get('total_requirements', 0)}")
        st.write(f"- **Questions**: {metadata2.get('total_questions', 0)}")
        st.write(f"- **Validation**: {metadata2.get('validation_score', 0):.1f}%")
    
    # Key differences
    st.write("#### Key Differences")
    
    req_diff = metadata1.get('total_requirements', 0) - metadata2.get('total_requirements', 0)
    q_diff = metadata1.get('total_questions', 0) - metadata2.get('total_questions', 0)
    val_diff = metadata1.get('validation_score', 0) - metadata2.get('validation_score', 0)
    
    if req_diff != 0:
        direction = "more" if req_diff > 0 else "fewer"
        st.write(f"• **{name1}** has {abs(req_diff)} {direction} requirements than **{name2}**")
    
    if q_diff != 0:
        direction = "more" if q_diff > 0 else "fewer"
        st.write(f"• **{name1}** has {abs(q_diff)} {direction} questions than **{name2}**")
    
    if abs(val_diff) > 1:
        direction = "higher" if val_diff > 0 else "lower"
        st.write(f"• **{name1}** has {abs(val_diff):.1f}% {direction} validation score than **{name2}**")


def show_overview_comparison(comparison_data):
    """Show high-level overview comparison."""
    
    st.markdown("### 📊 High-Level Metrics")
    
    # Create summary table
    summary_data = []
    for policy_name, results in comparison_data.items():
        stats = results['outputs']['summary_statistics']
        validation = results['outputs']['validation_report']
        
        summary_data.append({
            'Policy': policy_name,
            'Total Requirements': stats['total_requirements'],
            'Total Questions': stats['total_questions'],
            'Validation Score': f"{validation['overall_score']:.1f}%",
            'Policy Coverage': f"{stats['policy_coverage']:.1f}%",
            'Processing Time': f"{results['duration_seconds']:.1f}s"
        })
    
    df = pd.DataFrame(summary_data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Visual comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Requirements by Policy")
        fig = px.bar(
            df, 
            x='Policy', 
            y='Total Requirements',
            title="Total Requirements Comparison",
            color='Policy'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Questions by Policy")
        fig = px.bar(
            df,
            x='Policy',
            y='Total Questions', 
            title="Total Questions Comparison",
            color='Policy'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Validation scores radar chart
    st.markdown("#### Quality Metrics Comparison")
    
    # Prepare data for radar chart
    policies = list(comparison_data.keys())
    validation_scores = []
    coverage_scores = []
    
    for policy_name, results in comparison_data.items():
        validation = results['outputs']['validation_report']
        stats = results['outputs']['summary_statistics']
        validation_scores.append(validation['overall_score'])
        coverage_scores.append(stats['policy_coverage'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=validation_scores,
        theta=policies,
        fill='toself',
        name='Validation Score',
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=coverage_scores,
        theta=policies,
        fill='toself',
        name='Policy Coverage',
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Quality Metrics Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_requirements_comparison(comparison_data):
    """Show requirements comparison."""
    
    st.markdown("### 📋 Requirements Analysis")
    
    # Requirements by type comparison
    req_type_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        # Use the metrics we calculated in generate_comparison_data
        req_dist = policy_data['metrics']['requirement_distribution']
        
        for req_type, count in req_dist.items():
            req_type_data.append({
                'Policy': policy_name,
                'Requirement Type': req_type.replace('_', ' ').title(),
                'Count': count
            })
    
    df_req = pd.DataFrame(req_type_data)
    
    # Stacked bar chart
    fig = px.bar(
        df_req,
        x='Policy',
        y='Count',
        color='Requirement Type',
        title="Requirements by Type and Policy",
        barmode='stack'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Requirements breakdown table
    st.markdown("#### Detailed Requirements Breakdown")
    
    breakdown_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        req_dist = policy_data['metrics']['requirement_distribution']
        
        breakdown_data.append({
            'Policy': policy_name,
            'Functional': req_dist.get('functional', 0),
            'Data': req_dist.get('data', 0),
            'Business Rules': req_dist.get('business', 0),
            'Validation': req_dist.get('validation', 0)
        })
    
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, hide_index=True, use_container_width=True)
    
    # Sample requirements comparison
    st.markdown("#### Sample Requirements Comparison")
    
    for policy_name, policy_data in comparison_data['policies'].items():
        with st.expander(f"**{policy_name}** - Sample Requirements"):
            # Get functional requirements from the results
            results = policy_data['results']
            functional_reqs = results.get('outputs', {}).get('functional_requirements', [])[:3]
            
            if functional_reqs:
                for req in functional_reqs:
                    if isinstance(req, dict):
                        req_id = req.get('requirement_id', 'N/A')
                        description = req.get('description', str(req))
                        priority = req.get('priority', 'Unknown')
                        reference = req.get('policy_reference', 'N/A')
                        st.markdown(f"- **{req_id}**: {description}")
                        st.caption(f"Priority: {priority} | Ref: {reference}")
                    else:
                        st.markdown(f"- {str(req)}")
            else:
                st.info("No functional requirements available")


def show_questions_comparison(comparison_data):
    """Show questions comparison."""
    
    st.markdown("### ❓ Questions Analysis")
    
    # Questions by section comparison
    section_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        question_sections = policy_data['metrics']['question_sections']
        
        for section, count in question_sections.items():
            section_data.append({
                'Policy': policy_name,
                'Section': section,
                'Count': count
            })
    
    df_sections = pd.DataFrame(section_data)
    
    # Grouped bar chart
    fig = px.bar(
        df_sections,
        x='Section',
        y='Count',
        color='Policy',
        title="Questions by Section and Policy",
        barmode='group'
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Questions summary table
    st.markdown("#### Questions Summary")
    
    questions_summary = []
    for policy_name, policy_data in comparison_data['policies'].items():
        results = policy_data['results']
        questions = results.get('outputs', {}).get('application_questions', [])
        
        # Count by input type
        input_types = {}
        required_count = 0
        
        for q in questions:
            if isinstance(q, dict):
                input_type = q.get('input_type', 'unknown')
                input_types[input_type] = input_types.get(input_type, 0) + 1
                if q.get('required', False):
                    required_count += 1
            else:
                input_types['text'] = input_types.get('text', 0) + 1
        
        questions_summary.append({
            'Policy': policy_name,
            'Total Questions': len(questions),
            'Required Questions': required_count,
            'Optional Questions': len(questions) - required_count,
            'Text Fields': input_types.get('text', 0),
            'Number Fields': input_types.get('number', 0),
            'Date Fields': input_types.get('date', 0),
            'Boolean Fields': input_types.get('boolean', 0)
        })
    
    df_q_summary = pd.DataFrame(questions_summary)
    st.dataframe(df_q_summary, hide_index=True, use_container_width=True)


def show_quality_comparison(comparison_data):
    """Show quality metrics comparison."""
    
    st.markdown("### ✅ Quality Metrics Analysis")
    
    # Quality metrics table using the correct data structure
    quality_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        validation_breakdown = policy_data['metrics']['validation_breakdown']
        
        quality_data.append({
            'Policy': policy_name,
            'Overall Score': f"{validation_breakdown['overall']:.1f}%",
            'Requirements': f"{validation_breakdown['requirements']:.1f}%",
            'Questions': f"{validation_breakdown['questions']:.1f}%",
            'Coverage': f"{validation_breakdown['coverage']:.1f}%"
        })
    
    df_quality = pd.DataFrame(quality_data)
    st.dataframe(df_quality, hide_index=True, use_container_width=True)
    
    # Quality trends chart
    st.markdown("#### Quality Score Comparison")
    
    # Create a simple bar chart for quality comparison
    quality_chart_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        validation_breakdown = policy_data['metrics']['validation_breakdown']
        quality_chart_data.append({
            'Policy': policy_name,
            'Overall Score': validation_breakdown['overall']
        })
    
    if quality_chart_data:
        df_quality_chart = pd.DataFrame(quality_chart_data)
        fig = px.bar(
            df_quality_chart,
            x='Policy',
            y='Overall Score',
            title="Overall Quality Score Comparison",
            color='Overall Score',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)


def show_analytics_comparison(comparison_data):
    """Show advanced analytics comparison."""
    
    st.markdown("### 📈 Advanced Analytics")
    
    # Simple analytics using the correct data structure
    st.markdown("#### Policy Complexity Analysis")
    
    complexity_data = []
    for policy_name, policy_data in comparison_data['policies'].items():
        metadata = policy_data['metadata']
        complexity_data.append({
            'Policy': policy_name,
            'Complexity Score': metadata.get('complexity_score', 0),
            'Total Requirements': metadata.get('total_requirements', 0),
            'Total Questions': metadata.get('total_questions', 0),
            'Validation Score': metadata.get('validation_score', 0)
        })
    
    if complexity_data:
        df_complexity = pd.DataFrame(complexity_data)
        st.dataframe(df_complexity, hide_index=True, use_container_width=True)
        
        # Simple scatter plot
        fig = px.scatter(
            df_complexity,
            x='Total Requirements',
            y='Total Questions',
            size='Complexity Score',
            color='Validation Score',
            hover_name='Policy',
            title="Policy Complexity Analysis"
        )
        st.plotly_chart(fig, use_container_width=True)


# Remove the direct call to avoid execution when imported
