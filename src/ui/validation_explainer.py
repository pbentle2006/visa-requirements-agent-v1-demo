import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List


def create_validation_dashboard(validation_report: Dict[str, Any]) -> None:
    """
    Create comprehensive validation dashboard with detailed explanations.
    
    Args:
        validation_report: Validation report from ValidationAgent
    """
    
    if not validation_report:
        st.info("No validation report available")
        return
    
    # Create tabs for different aspects of validation
    val_tabs = st.tabs([
        "📊 Score Breakdown",
        "📋 Methodology", 
        "🔍 Detailed Results",
        "💡 Recommendations"
    ])
    
    # Tab 1: Score Breakdown
    with val_tabs[0]:
        show_score_breakdown(validation_report)
    
    # Tab 2: Methodology
    with val_tabs[1]:
        show_validation_methodology()
    
    # Tab 3: Detailed Results
    with val_tabs[2]:
        show_detailed_results(validation_report)
    
    # Tab 4: Recommendations
    with val_tabs[3]:
        show_recommendations(validation_report)


def show_score_breakdown(validation_report: Dict[str, Any]) -> None:
    """Show detailed score breakdown with visualizations."""
    
    st.subheader("🔍 Validation Score Composition")
    
    overall_score = validation_report.get('overall_score', 0)
    
    # Extract component scores
    req_validation = validation_report.get('requirement_validation', {})
    q_validation = validation_report.get('question_validation', {})
    coverage_analysis = validation_report.get('coverage_analysis', {})
    
    req_score = req_validation.get('validation_rate', 0)
    q_score = q_validation.get('validation_rate', 0)
    cov_score = coverage_analysis.get('requirement_coverage', {}).get('coverage_percentage', 0)
    
    # Overall score display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Score", f"{overall_score:.1f}%", 
                 help="Weighted average of all validation components")
    
    with col2:
        quality_tier = get_quality_tier(overall_score)
        st.metric("Quality Tier", quality_tier['name'], 
                 help=quality_tier['description'])
    
    with col3:
        validation_errors = validation_report.get('validation_errors', 0)
        st.metric("Validation Errors", validation_errors,
                 help="Number of validation issues identified")
    
    # Component breakdown with weights
    st.subheader("📊 Component Analysis")
    
    # Weighted scoring formula (Requirements: 30%, Questions: 30%, Coverage: 40%)
    weights = {'Requirements': 0.30, 'Questions': 0.30, 'Coverage': 0.40}
    components = {
        'Requirements': req_score,
        'Questions': q_score, 
        'Coverage': cov_score
    }
    
    # Calculate weighted contributions
    contributions = {}
    for component, score in components.items():
        contributions[component] = score * weights[component]
    
    # Create visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Component scores chart
        fig_scores = go.Figure(data=[
            go.Bar(
                x=list(components.keys()),
                y=list(components.values()),
                text=[f"{v:.1f}%" for v in components.values()],
                textposition='auto',
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
            )
        ])
        fig_scores.update_layout(
            title="Component Scores",
            yaxis_title="Score (%)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_scores, use_container_width=True)
    
    with col2:
        # Weighted contributions pie chart
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=list(contributions.keys()),
                values=list(contributions.values()),
                hole=0.4,
                textinfo='label+percent',
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
            )
        ])
        fig_pie.update_layout(
            title="Weighted Contributions to Overall Score",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed component analysis
    st.subheader("🔍 Component Details")
    
    for component, score in components.items():
        weight = weights[component]
        contribution = contributions[component]
        
        with st.expander(f"{component}: {score:.1f}% (Weight: {weight*100:.0f}%)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Raw Score", f"{score:.1f}%")
            with col2:
                st.metric("Weight", f"{weight*100:.0f}%")
            with col3:
                st.metric("Contribution", f"{contribution:.1f}%")
            
            # Component-specific details
            if component == 'Requirements':
                show_requirements_details(req_validation)
            elif component == 'Questions':
                show_questions_details(q_validation)
            elif component == 'Coverage':
                show_coverage_details(coverage_analysis)


def show_validation_methodology() -> None:
    """Explain the validation methodology and scoring approach."""
    
    st.subheader("📋 Validation Methodology")
    
    st.markdown("""
    ### 🎯 Scoring Formula
    
    The overall validation score is calculated using a **weighted average** of three key components:
    
    ```
    Overall Score = (Requirements × 30%) + (Questions × 30%) + (Coverage × 40%)
    ```
    
    ### 📊 Component Breakdown
    """)
    
    # Component explanations
    components_info = [
        {
            "name": "Requirements Validation (30%)",
            "description": "Evaluates the quality and completeness of extracted requirements",
            "criteria": [
                "Requirement clarity and specificity",
                "Policy reference accuracy", 
                "Priority classification correctness",
                "Completeness of requirement capture"
            ]
        },
        {
            "name": "Questions Validation (30%)",
            "description": "Assesses the generated application questions",
            "criteria": [
                "Question relevance to policy requirements",
                "Input type appropriateness",
                "Question clarity and understandability",
                "Coverage of all policy aspects"
            ]
        },
        {
            "name": "Coverage Analysis (40%)",
            "description": "Measures how well the extraction covers the source policy",
            "criteria": [
                "Policy section coverage percentage",
                "Requirement extraction completeness",
                "Key policy element identification",
                "Gap analysis accuracy"
            ]
        }
    ]
    
    for component in components_info:
        with st.expander(f"🔍 {component['name']}"):
            st.write(component['description'])
            st.write("**Evaluation Criteria:**")
            for criterion in component['criteria']:
                st.write(f"• {criterion}")
    
    # Quality tiers
    st.subheader("🏆 Quality Tiers")
    
    tiers = [
        {"range": "90-100%", "tier": "Excellent", "color": "#28a745", "description": "Outstanding quality with minimal issues"},
        {"range": "75-89%", "tier": "Good", "color": "#17a2b8", "description": "High quality with minor improvements needed"},
        {"range": "60-74%", "tier": "Fair", "color": "#ffc107", "description": "Acceptable quality with some issues to address"},
        {"range": "0-59%", "tier": "Poor", "color": "#dc3545", "description": "Significant issues requiring attention"}
    ]
    
    for tier in tiers:
        st.markdown(f"""
        <div style="padding: 10px; margin: 5px 0; border-left: 4px solid {tier['color']}; background-color: rgba(0,0,0,0.05);">
            <strong>{tier['range']}: {tier['tier']}</strong><br>
            {tier['description']}
        </div>
        """, unsafe_allow_html=True)


def show_detailed_results(validation_report: Dict[str, Any]) -> None:
    """Show detailed validation results and error analysis."""
    
    st.subheader("🔍 Detailed Validation Results")
    
    # Error analysis
    validation_errors = validation_report.get('validation_errors', [])
    if validation_errors:
        st.subheader("⚠️ Validation Issues")
        
        for i, error in enumerate(validation_errors[:10], 1):  # Show top 10 errors
            severity = error.get('severity', 'medium') if isinstance(error, dict) else 'medium'
            message = error.get('message', str(error)) if isinstance(error, dict) else str(error)
            
            severity_colors = {
                'high': '🔴',
                'medium': '🟡', 
                'low': '🟢'
            }
            
            icon = severity_colors.get(severity, '🟡')
            st.write(f"{icon} **Issue {i}**: {message}")
    else:
        st.success("✅ No validation issues identified")
    
    # Coverage details
    coverage_analysis = validation_report.get('coverage_analysis', {})
    if coverage_analysis:
        st.subheader("📊 Coverage Analysis")
        
        req_coverage = coverage_analysis.get('requirement_coverage', {})
        if req_coverage:
            coverage_pct = req_coverage.get('coverage_percentage', 0)
            total_sections = req_coverage.get('total_sections', 0)
            covered_sections = req_coverage.get('covered_sections', 0)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Coverage Percentage", f"{coverage_pct:.1f}%")
            with col2:
                st.metric("Covered Sections", f"{covered_sections}/{total_sections}")
            with col3:
                missing_sections = total_sections - covered_sections
                st.metric("Missing Sections", missing_sections)
    
    # Gap analysis
    gap_analysis = validation_report.get('gap_analysis', {})
    if gap_analysis:
        st.subheader("🔍 Gap Analysis")
        
        missing_reqs = gap_analysis.get('missing_requirements', [])
        if missing_reqs:
            st.write("**Missing Requirements:**")
            for req in missing_reqs[:5]:  # Show top 5
                st.write(f"• {req}")
        
        incomplete_sections = gap_analysis.get('incomplete_sections', [])
        if incomplete_sections:
            st.write("**Incomplete Sections:**")
            for section in incomplete_sections[:5]:  # Show top 5
                st.write(f"• {section}")


def show_recommendations(validation_report: Dict[str, Any]) -> None:
    """Show actionable recommendations based on validation results."""
    
    st.subheader("💡 Actionable Recommendations")
    
    overall_score = validation_report.get('overall_score', 0)
    recommendations = validation_report.get('recommendations', [])
    
    # Generate recommendations based on score
    generated_recommendations = generate_recommendations(validation_report)
    all_recommendations = recommendations + generated_recommendations
    
    if not all_recommendations:
        st.success("🎉 Excellent work! No specific recommendations at this time.")
        return
    
    # Group recommendations by priority
    priority_groups = {'high': [], 'medium': [], 'low': []}
    
    for rec in all_recommendations:
        if isinstance(rec, dict):
            priority = rec.get('priority', 'medium')
            priority_groups[priority].append(rec)
        else:
            priority_groups['medium'].append({'description': str(rec), 'priority': 'medium'})
    
    # Display recommendations by priority
    priority_info = {
        'high': {'icon': '🔴', 'title': 'High Priority', 'color': '#dc3545'},
        'medium': {'icon': '🟡', 'title': 'Medium Priority', 'color': '#ffc107'},
        'low': {'icon': '🟢', 'title': 'Low Priority', 'color': '#28a745'}
    }
    
    for priority, recs in priority_groups.items():
        if not recs:
            continue
            
        info = priority_info[priority]
        st.markdown(f"### {info['icon']} {info['title']}")
        
        for i, rec in enumerate(recs, 1):
            description = rec.get('description', str(rec))
            action = rec.get('action', 'Review and address this issue')
            impact = rec.get('impact', 'Improves overall quality')
            
            with st.expander(f"{info['icon']} Recommendation {i}: {description[:50]}..."):
                st.write(f"**Issue:** {description}")
                st.write(f"**Recommended Action:** {action}")
                st.write(f"**Expected Impact:** {impact}")


def get_quality_tier(score: float) -> Dict[str, str]:
    """Get quality tier information based on score."""
    
    if score >= 90:
        return {
            'name': 'Excellent',
            'description': 'Outstanding quality with minimal issues'
        }
    elif score >= 75:
        return {
            'name': 'Good', 
            'description': 'High quality with minor improvements needed'
        }
    elif score >= 60:
        return {
            'name': 'Fair',
            'description': 'Acceptable quality with some issues to address'
        }
    else:
        return {
            'name': 'Poor',
            'description': 'Significant issues requiring attention'
        }


def generate_recommendations(validation_report: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate recommendations based on validation results."""
    
    recommendations = []
    overall_score = validation_report.get('overall_score', 0)
    
    # Score-based recommendations
    if overall_score < 60:
        recommendations.append({
            'priority': 'high',
            'description': 'Overall validation score is below acceptable threshold',
            'action': 'Review policy document quality and re-run extraction process',
            'impact': 'Significantly improves extraction accuracy and completeness'
        })
    
    # Component-specific recommendations
    req_validation = validation_report.get('requirement_validation', {})
    if req_validation.get('validation_rate', 0) < 70:
        recommendations.append({
            'priority': 'high',
            'description': 'Requirements validation score is low',
            'action': 'Review extracted requirements for clarity and policy alignment',
            'impact': 'Improves requirement quality and traceability'
        })
    
    q_validation = validation_report.get('question_validation', {})
    if q_validation.get('validation_rate', 0) < 70:
        recommendations.append({
            'priority': 'medium',
            'description': 'Question validation score needs improvement',
            'action': 'Review generated questions for relevance and clarity',
            'impact': 'Enhances application form quality and user experience'
        })
    
    coverage_analysis = validation_report.get('coverage_analysis', {})
    coverage_pct = coverage_analysis.get('requirement_coverage', {}).get('coverage_percentage', 0)
    if coverage_pct < 80:
        recommendations.append({
            'priority': 'high',
            'description': 'Policy coverage is incomplete',
            'action': 'Review policy document for missing sections or unclear content',
            'impact': 'Ensures comprehensive requirement capture'
        })
    
    return recommendations


def show_requirements_details(req_validation: Dict[str, Any]) -> None:
    """Show detailed requirements validation information."""
    
    validation_rate = req_validation.get('validation_rate', 0)
    total_reqs = req_validation.get('total_requirements', 0)
    valid_reqs = req_validation.get('valid_requirements', 0)
    
    st.write(f"**Validation Rate:** {validation_rate:.1f}%")
    st.write(f"**Valid Requirements:** {valid_reqs}/{total_reqs}")
    
    issues = req_validation.get('issues', [])
    if issues:
        st.write("**Common Issues:**")
        for issue in issues[:3]:
            st.write(f"• {issue}")


def show_questions_details(q_validation: Dict[str, Any]) -> None:
    """Show detailed questions validation information."""
    
    validation_rate = q_validation.get('validation_rate', 0)
    total_questions = q_validation.get('total_questions', 0)
    valid_questions = q_validation.get('valid_questions', 0)
    
    st.write(f"**Validation Rate:** {validation_rate:.1f}%")
    st.write(f"**Valid Questions:** {valid_questions}/{total_questions}")
    
    sections = q_validation.get('sections_covered', [])
    if sections:
        st.write(f"**Sections Covered:** {', '.join(sections)}")


def show_coverage_details(coverage_analysis: Dict[str, Any]) -> None:
    """Show detailed coverage analysis information."""
    
    req_coverage = coverage_analysis.get('requirement_coverage', {})
    coverage_pct = req_coverage.get('coverage_percentage', 0)
    
    st.write(f"**Coverage Percentage:** {coverage_pct:.1f}%")
    
    covered_sections = req_coverage.get('covered_sections', 0)
    total_sections = req_coverage.get('total_sections', 0)
    st.write(f"**Section Coverage:** {covered_sections}/{total_sections}")
    
    policy_sections = coverage_analysis.get('policy_sections', [])
    if policy_sections:
        st.write(f"**Policy Sections:** {len(policy_sections)} identified")
