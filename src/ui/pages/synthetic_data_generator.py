"""
Enhanced Synthetic Data Generator Page

Advanced synthetic data generation with AI-powered content, batch processing, and export capabilities.
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
from datetime import datetime
import random
import zipfile
import io
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.generators.policy_generator import PolicyGenerator
from src.generators.mock_results_generator import MockResultsGenerator


def show_synthetic_data_generator():
    """Display the enhanced synthetic data generator interface."""
    
    st.header("🤖 Advanced Synthetic Data Generator")
    st.markdown("Generate realistic policy documents, mock workflow results, and comprehensive test datasets for demonstrations and testing.")
    
    # Initialize generators
    if 'policy_generator' not in st.session_state:
        st.session_state.policy_generator = PolicyGenerator()
    if 'mock_generator' not in st.session_state:
        st.session_state.mock_generator = MockResultsGenerator()
    
    # Generation statistics
    show_generation_statistics()
    
    # Create tabs for different generation options
    tabs = st.tabs([
        "📄 Policy Generator",
        "🔄 Workflow Results", 
        "📊 Batch Generation",
        "🎯 Custom Templates",
        "📈 Analytics & Insights",
        "📥 Export & Download"
    ])
    
    # Tab 1: Enhanced Policy Generator
    with tabs[0]:
        show_enhanced_policy_generator()
    
    # Tab 2: Enhanced Mock Results Generator
    with tabs[1]:
        show_enhanced_mock_results_generator()
    
    # Tab 3: Batch Generation
    with tabs[2]:
        show_batch_generation()
    
    # Tab 4: Custom Templates
    with tabs[3]:
        show_custom_templates()
    
    # Tab 5: Analytics & Insights
    with tabs[4]:
        show_generation_analytics()
    
    # Tab 6: Export & Download
    with tabs[5]:
        show_export_options()


def show_generation_statistics():
    """Show generation statistics and metrics."""
    
    st.subheader("📊 Generation Statistics")
    
    # Mock statistics for demonstration
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Policies Generated", "47", delta="12")
    
    with col2:
        st.metric("Workflow Results", "156", delta="23")
    
    with col3:
        st.metric("Templates Created", "8", delta="2")
    
    with col4:
        st.metric("Export Downloads", "89", delta="15")


def show_enhanced_policy_generator():
    """Show enhanced policy document generator interface."""
    
    st.subheader("📄 Generate Synthetic Policy Documents")
    st.markdown("Create realistic immigration policy documents with advanced customization options.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Policy configuration
        st.markdown("#### Policy Configuration")
        
        visa_types = {
            "Tourist Visa": {"complexity": "Low", "sections": 6, "processing_days": 15},
            "Student Visa": {"complexity": "Medium", "sections": 9, "processing_days": 30},
            "Skilled Worker Visa": {"complexity": "High", "sections": 15, "processing_days": 60},
            "Family Reunion Visa": {"complexity": "Medium", "sections": 8, "processing_days": 35},
            "Business Investor Visa": {"complexity": "High", "sections": 14, "processing_days": 90},
            "Humanitarian Visa": {"complexity": "Medium", "sections": 10, "processing_days": 120}
        }
        
        selected_visa_type = st.selectbox(
            "Visa Type:",
            list(visa_types.keys()),
            help="Choose the type of visa policy to generate"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            complexity_level = st.select_slider(
                "Complexity Level:",
                options=["Simple", "Standard", "Complex", "Enterprise"],
                value="Standard"
            )
            
            include_sections = st.multiselect(
                "Include Sections:",
                ["Eligibility Criteria", "Application Process", "Required Documents", 
                 "Processing Times", "Fees", "Appeals Process", "Compliance Requirements"],
                default=["Eligibility Criteria", "Application Process", "Required Documents"]
            )
            
            language_style = st.selectbox(
                "Language Style:",
                ["Formal Legal", "Plain English", "Technical", "Conversational"]
            )
            
            include_examples = st.checkbox("Include Examples", value=True)
            include_references = st.checkbox("Include Policy References", value=True)
        
        # Generation button
        if st.button("🚀 Generate Policy Document", type="primary"):
            with st.spinner("Generating policy document..."):
                policy_doc = generate_enhanced_policy_document(
                    selected_visa_type,
                    complexity_level,
                    include_sections,
                    language_style,
                    include_examples,
                    include_references
                )
                
                st.session_state.generated_policy = policy_doc
                st.success("✅ Policy document generated successfully!")
    
    with col2:
        # Preview and metadata
        st.markdown("#### Document Preview")
        
        if hasattr(st.session_state, 'generated_policy') and st.session_state.generated_policy:
            policy = st.session_state.generated_policy
            
            # Metadata
            st.write("**Document Metadata:**")
            st.write(f"• **Type**: {policy.get('visa_type', 'Unknown')}")
            st.write(f"• **Sections**: {len(policy.get('sections', {}))}")
            st.write(f"• **Word Count**: {policy.get('word_count', 0):,}")
            st.write(f"• **Complexity**: {policy.get('complexity', 'Unknown')}")
            
            # Preview content
            st.markdown("**Content Preview:**")
            preview_text = policy.get('preview', 'No preview available')
            st.text_area("Preview", preview_text, height=200, disabled=True)
            
            # Download button
            policy_json = json.dumps(policy, indent=2)
            st.download_button(
                "📥 Download Policy JSON",
                policy_json,
                file_name=f"{policy.get('visa_type', 'policy').lower().replace(' ', '_')}.json",
                mime="application/json"
            )
        else:
            st.info("Generate a policy document to see preview")


def generate_enhanced_policy_document(visa_type, complexity, sections, style, examples, references):
    """Generate enhanced policy document with advanced options."""
    
    # Simulate document generation
    word_count = random.randint(800, 2500)
    
    policy_doc = {
        'visa_type': visa_type,
        'complexity': complexity,
        'language_style': style,
        'sections': {},
        'word_count': word_count,
        'generated_at': datetime.now().isoformat(),
        'preview': f"This is a {complexity.lower()} complexity {visa_type} policy document...\n\nEligibility Criteria:\n- Applicant must be at least 18 years old\n- Valid passport required\n- Proof of financial support\n\nApplication Process:\n1. Complete online application\n2. Submit required documents\n3. Pay application fee\n4. Attend interview (if required)"
    }
    
    # Generate sections based on selections
    for section in sections:
        policy_doc['sections'][section] = f"Detailed content for {section} section..."
    
    return policy_doc


def show_enhanced_mock_results_generator():
    """Show enhanced mock workflow results generator."""
    
    st.subheader("🔄 Generate Mock Workflow Results")
    st.markdown("Create realistic workflow results for testing and demonstrations.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Configuration options
        st.markdown("#### Workflow Configuration")
        
        policy_name = st.text_input("Policy Name", value="Sample Immigration Policy")
        
        # Result quality settings
        with st.expander("🎯 Quality Settings"):
            validation_score_range = st.slider(
                "Validation Score Range:",
                min_value=0,
                max_value=100,
                value=(75, 95),
                help="Range for generated validation scores"
            )
            
            processing_time_range = st.slider(
                "Processing Time Range (seconds):",
                min_value=30,
                max_value=300,
                value=(120, 240)
            )
            
            include_errors = st.checkbox("Include Validation Errors", value=False)
            include_warnings = st.checkbox("Include Warnings", value=True)
        
        # Content customization
        with st.expander("📋 Content Customization"):
            num_requirements = st.slider("Number of Requirements:", 10, 50, 25)
            num_questions = st.slider("Number of Questions:", 8, 30, 15)
            num_sections = st.slider("Number of Policy Sections:", 3, 15, 8)
        
        # Generate button
        if st.button("🚀 Generate Mock Results", type="primary"):
            with st.spinner("Generating mock workflow results..."):
                mock_results = generate_enhanced_mock_results(
                    policy_name,
                    validation_score_range,
                    processing_time_range,
                    num_requirements,
                    num_questions,
                    num_sections,
                    include_errors,
                    include_warnings
                )
                
                st.session_state.generated_mock_results = mock_results
                st.success("✅ Mock results generated successfully!")
    
    with col2:
        # Results preview
        st.markdown("#### Results Preview")
        
        if hasattr(st.session_state, 'generated_mock_results') and st.session_state.generated_mock_results:
            results = st.session_state.generated_mock_results
            
            # Key metrics
            st.write("**Generated Metrics:**")
            st.write(f"• **Status**: {results.get('status', 'Unknown')}")
            st.write(f"• **Duration**: {results.get('duration_seconds', 0):.1f}s")
            st.write(f"• **Validation Score**: {results.get('outputs', {}).get('validation_report', {}).get('overall_score', 0):.1f}%")
            st.write(f"• **Requirements**: {len(results.get('outputs', {}).get('functional_requirements', []))}")
            st.write(f"• **Questions**: {len(results.get('outputs', {}).get('application_questions', []))}")
            
            # Download button
            results_json = json.dumps(results, indent=2)
            st.download_button(
                "📥 Download Results JSON",
                results_json,
                file_name=f"mock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("Generate mock results to see preview")


def generate_enhanced_mock_results(policy_name, score_range, time_range, num_reqs, num_questions, num_sections, errors, warnings):
    """Generate enhanced mock workflow results."""
    
    mock_generator = MockResultsGenerator()
    base_results = mock_generator.generate_complete_workflow_results(policy_name)
    
    # Customize based on parameters
    validation_score = random.uniform(score_range[0], score_range[1])
    processing_time = random.uniform(time_range[0], time_range[1])
    
    # Update validation score
    if 'validation_report' in base_results['outputs']:
        base_results['outputs']['validation_report']['overall_score'] = validation_score
    
    # Update processing time
    base_results['duration_seconds'] = processing_time
    
    # Adjust content counts (simplified for demo)
    base_results['outputs']['functional_requirements'] = [f"FR-{i:03d}: Functional requirement {i}" for i in range(1, num_reqs//4 + 1)]
    base_results['outputs']['data_requirements'] = [f"DR-{i:03d}: Data requirement {i}" for i in range(1, num_reqs//4 + 1)]
    base_results['outputs']['business_rules'] = [f"BR-{i:03d}: Business rule {i}" for i in range(1, num_reqs//4 + 1)]
    base_results['outputs']['validation_rules'] = [f"VR-{i:03d}: Validation rule {i}" for i in range(1, num_reqs//4 + 1)]
    
    base_results['outputs']['application_questions'] = [f"Q-{i:03d}: Sample question {i}" for i in range(1, num_questions + 1)]
    
    return base_results


def show_batch_generation():
    """Show batch generation interface."""
    
    st.subheader("📊 Batch Generation")
    st.markdown("Generate multiple policies and results in batch for comprehensive testing.")
    
    # Batch configuration
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.slider("Batch Size:", 1, 20, 5)
        
        generation_types = st.multiselect(
            "Generation Types:",
            ["Policy Documents", "Workflow Results", "Comparison Data"],
            default=["Policy Documents", "Workflow Results"]
        )
    
    with col2:
        output_format = st.selectbox(
            "Output Format:",
            ["JSON", "CSV", "Excel", "ZIP Archive"]
        )
        
        include_metadata = st.checkbox("Include Metadata", value=True)
    
    # Advanced batch options
    with st.expander("🔧 Advanced Batch Options"):
        vary_complexity = st.checkbox("Vary Complexity Levels", value=True)
        vary_visa_types = st.checkbox("Vary Visa Types", value=True)
        include_analytics = st.checkbox("Include Analytics Summary", value=True)
    
    # Generate batch
    if st.button("🚀 Generate Batch", type="primary"):
        with st.spinner(f"Generating batch of {batch_size} items..."):
            batch_results = generate_batch_data(
                batch_size,
                generation_types,
                vary_complexity,
                vary_visa_types,
                include_metadata,
                include_analytics
            )
            
            st.session_state.batch_results = batch_results
            st.success(f"✅ Generated {batch_size} items successfully!")
            
            # Show summary
            show_batch_summary(batch_results)


def generate_batch_data(size, types, vary_complexity, vary_visa_types, metadata, analytics):
    """Generate batch data based on configuration."""
    
    batch_results = {
        'generated_at': datetime.now().isoformat(),
        'batch_size': size,
        'generation_types': types,
        'items': []
    }
    
    visa_types = ["Tourist Visa", "Student Visa", "Skilled Worker Visa", "Family Reunion Visa"]
    complexity_levels = ["Simple", "Standard", "Complex"]
    
    for i in range(size):
        item = {
            'id': f"batch_item_{i+1:03d}",
            'visa_type': random.choice(visa_types) if vary_visa_types else "Tourist Visa",
            'complexity': random.choice(complexity_levels) if vary_complexity else "Standard"
        }
        
        if "Policy Documents" in types:
            item['policy_document'] = f"Generated policy document for {item['visa_type']}"
        
        if "Workflow Results" in types:
            mock_generator = MockResultsGenerator()
            item['workflow_results'] = mock_generator.generate_complete_workflow_results(item['visa_type'])
        
        batch_results['items'].append(item)
    
    return batch_results


def show_batch_summary(batch_results):
    """Show summary of batch generation results."""
    
    st.subheader("📈 Batch Generation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Items Generated", len(batch_results['items']))
    
    with col2:
        visa_types = [item['visa_type'] for item in batch_results['items']]
        unique_types = len(set(visa_types))
        st.metric("Unique Visa Types", unique_types)
    
    with col3:
        complexities = [item['complexity'] for item in batch_results['items']]
        unique_complexities = len(set(complexities))
        st.metric("Complexity Levels", unique_complexities)
    
    # Download batch results
    batch_json = json.dumps(batch_results, indent=2)
    st.download_button(
        "📥 Download Batch Results",
        batch_json,
        file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )


def show_custom_templates():
    """Show custom template creation interface."""
    
    st.subheader("🎯 Custom Templates")
    st.markdown("Create and manage custom templates for policy generation.")
    
    # Template creation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        template_name = st.text_input("Template Name", placeholder="e.g., 'EU Student Visa Template'")
        
        template_description = st.text_area(
            "Template Description",
            placeholder="Describe the purpose and characteristics of this template..."
        )
        
        # Template structure
        st.markdown("#### Template Structure")
        
        template_sections = st.multiselect(
            "Required Sections:",
            ["Eligibility", "Application Process", "Documents", "Fees", "Processing", "Appeals"],
            default=["Eligibility", "Application Process", "Documents"]
        )
        
        # Template parameters
        with st.expander("🔧 Template Parameters"):
            default_complexity = st.selectbox("Default Complexity:", ["Simple", "Standard", "Complex"])
            default_processing_days = st.number_input("Default Processing Days:", 1, 365, 30)
            default_fee = st.number_input("Default Fee ($):", 0, 5000, 200)
        
        if st.button("💾 Save Template", type="primary"):
            template_data = {
                'name': template_name,
                'description': template_description,
                'sections': template_sections,
                'default_complexity': default_complexity,
                'default_processing_days': default_processing_days,
                'default_fee': default_fee,
                'created_at': datetime.now().isoformat()
            }
            
            # Save to session state (in real app, would save to database)
            if 'custom_templates' not in st.session_state:
                st.session_state.custom_templates = []
            
            st.session_state.custom_templates.append(template_data)
            st.success("✅ Template saved successfully!")
    
    with col2:
        # Template library
        st.markdown("#### Template Library")
        
        if hasattr(st.session_state, 'custom_templates') and st.session_state.custom_templates:
            for i, template in enumerate(st.session_state.custom_templates):
                with st.expander(f"📋 {template['name']}"):
                    st.write(f"**Description**: {template['description']}")
                    st.write(f"**Sections**: {len(template['sections'])}")
                    st.write(f"**Complexity**: {template['default_complexity']}")
                    
                    if st.button(f"Use Template", key=f"use_template_{i}"):
                        st.info(f"Using template: {template['name']}")
        else:
            st.info("No custom templates created yet")


def show_generation_analytics():
    """Show analytics and insights about generated data."""
    
    st.subheader("📈 Generation Analytics & Insights")
    st.markdown("Analyze patterns and quality metrics of generated synthetic data.")
    
    # Mock analytics data
    analytics_data = {
        'total_generated': 156,
        'avg_validation_score': 87.3,
        'most_common_visa_type': 'Tourist Visa',
        'avg_processing_time': 45.2,
        'quality_distribution': {
            'Excellent (90%+)': 45,
            'Good (75-89%)': 89,
            'Fair (60-74%)': 18,
            'Poor (<60%)': 4
        }
    }
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Generated", analytics_data['total_generated'])
    
    with col2:
        st.metric("Avg Validation Score", f"{analytics_data['avg_validation_score']:.1f}%")
    
    with col3:
        st.metric("Most Common Type", analytics_data['most_common_visa_type'])
    
    with col4:
        st.metric("Avg Processing Time", f"{analytics_data['avg_processing_time']:.1f}s")
    
    # Quality distribution chart
    st.subheader("📊 Quality Distribution")
    
    quality_df = pd.DataFrame(
        list(analytics_data['quality_distribution'].items()),
        columns=['Quality Level', 'Count']
    )
    
    fig = px.pie(
        quality_df,
        values='Count',
        names='Quality Level',
        title="Generated Data Quality Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Trends over time (mock data)
    st.subheader("📈 Generation Trends")
    
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Generated': [random.randint(3, 12) for _ in range(30)],
        'Avg Quality': [random.uniform(75, 95) for _ in range(30)]
    })
    
    fig = px.line(
        trend_data,
        x='Date',
        y=['Generated', 'Avg Quality'],
        title="Generation Activity Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_export_options():
    """Show export and download options."""
    
    st.subheader("📥 Export & Download Options")
    st.markdown("Export generated data in various formats for external use.")
    
    # Export configuration
    col1, col2 = st.columns(2)
    
    with col1:
        export_type = st.selectbox(
            "Export Type:",
            ["Single Document", "Batch Results", "Analytics Report", "Complete Dataset"]
        )
        
        export_format = st.selectbox(
            "Export Format:",
            ["JSON", "CSV", "Excel", "PDF Report", "ZIP Archive"]
        )
    
    with col2:
        include_metadata = st.checkbox("Include Metadata", value=True)
        include_timestamps = st.checkbox("Include Timestamps", value=True)
        compress_output = st.checkbox("Compress Output", value=False)
    
    # Export options based on type
    if export_type == "Analytics Report":
        st.markdown("#### Report Configuration")
        
        report_sections = st.multiselect(
            "Include Sections:",
            ["Executive Summary", "Quality Metrics", "Trend Analysis", "Recommendations"],
            default=["Executive Summary", "Quality Metrics"]
        )
    
    # Generate export
    if st.button("📦 Generate Export", type="primary"):
        with st.spinner("Preparing export..."):
            export_data = prepare_export_data(export_type, export_format, include_metadata)
            
            # Create download
            if export_format == "JSON":
                st.download_button(
                    "📥 Download Export",
                    json.dumps(export_data, indent=2),
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            elif export_format == "CSV":
                # Convert to CSV format
                csv_data = "Generated CSV data would be here..."
                st.download_button(
                    "📥 Download CSV",
                    csv_data,
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            st.success("✅ Export prepared successfully!")


def prepare_export_data(export_type, format_type, include_metadata):
    """Prepare data for export based on configuration."""
    
    export_data = {
        'export_type': export_type,
        'format': format_type,
        'generated_at': datetime.now().isoformat() if include_metadata else None,
        'data': {}
    }
    
    # Add relevant data based on export type
    if export_type == "Single Document":
        if hasattr(st.session_state, 'generated_policy'):
            export_data['data'] = st.session_state.generated_policy
    elif export_type == "Batch Results":
        if hasattr(st.session_state, 'batch_results'):
            export_data['data'] = st.session_state.batch_results
    
    return export_data
    
    with col2:
        # Results preview
        st.markdown("#### Results Preview")
        
        if hasattr(st.session_state, 'generated_results'):
            results_data = st.session_state.generated_results['results']
            outputs = results_data.get('outputs', {})
            
            # Calculate metrics from actual data
            total_reqs = (len(outputs.get('functional_requirements', [])) + 
                         len(outputs.get('data_requirements', [])) + 
                         len(outputs.get('business_rules', [])) + 
                         len(outputs.get('validation_rules', [])))
            total_questions = len(outputs.get('application_questions', []))
            validation_score = outputs.get('validation_report', {}).get('overall_score', 0)
            
            st.metric("Requirements", total_reqs)
            st.metric("Questions", total_questions)
            st.metric("Validation Score", f"{validation_score:.1f}%")
            
            # Status indicators
            if results_data['status'] == 'completed':
                st.success("✅ Completed")
            else:
                st.warning("⚠️ Partial")
        else:
            st.info("Generate results to see preview")
    
    # Display generated results
    if hasattr(st.session_state, 'generated_results'):
        st.divider()
        st.markdown("#### Generated Results Summary")
        
        results_info = st.session_state.generated_results
        results = results_info['results']
        
        # Results metadata
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.caption(f"**Policy:** {results_info['policy_name']}")
        with col_meta2:
            st.caption(f"**Generated:** {results_info['generated_at'].strftime('%Y-%m-%d %H:%M')}")
        
        # Quick stats
        stats = results['outputs']['summary_statistics']
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Requirements", stats['total_requirements'])
        with col_stat2:
            st.metric("Questions", stats['total_questions'])
        with col_stat3:
            st.metric("Validation", f"{stats['validation_score']:.1f}%")
        with col_stat4:
            st.metric("Duration", f"{results['duration_seconds']:.1f}s")
        
        # Detailed breakdown
        with st.expander("📊 View Detailed Breakdown", expanded=False):
            # Requirements by type
            req_by_type = stats['requirements_by_type']
            df_req = pd.DataFrame([
                {'Type': k.replace('_', ' ').title(), 'Count': v}
                for k, v in req_by_type.items()
            ])
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig = px.pie(df_req, values='Count', names='Type', title="Requirements by Type")
                st.plotly_chart(fig, use_container_width=True)
            
            # Questions by section
            q_by_section = stats['questions_by_section']
            df_q = pd.DataFrame([
                {'Section': k, 'Count': v}
                for k, v in q_by_section.items()
            ])
            
            with col_chart2:
                fig = px.bar(df_q, x='Section', y='Count', title="Questions by Section")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Save and download options
        col_save1, col_save2 = st.columns(2)
        with col_save1:
            if st.button("💾 Save Results"):
                try:
                    output_dir = Path("data/synthetic/results")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    filename = f"{results_info['policy_name'].lower().replace(' ', '_')}_results.json"
                    file_path = output_dir / filename
                    
                    with open(file_path, 'w') as f:
                        json.dump(results, f, indent=2, default=str)
                    
                    st.success(f"✅ Saved to: {file_path}")
                except Exception as e:
                    st.error(f"❌ Save error: {str(e)}")
        
        with col_save2:
            # Download button
            json_str = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="📥 Download Results",
                data=json_str,
                file_name=f"{results_info['policy_name'].lower().replace(' ', '_')}_results.json",
                mime="application/json"
            )


def show_batch_generator():
    """Show batch generation interface."""
    
    st.subheader("📊 Batch Generation")
    st.markdown("Generate multiple policies and results in one operation.")
    
    # Predefined batch options
    st.markdown("#### Quick Batch Generation")
    
    batch_options = {
        "Standard Visa Types": [
            {"name": "Tourist Visa", "category": "visitor", "complexity": "simple"},
            {"name": "Business Visa", "category": "business", "complexity": "medium"},
            {"name": "Student Visa", "category": "student", "complexity": "medium"},
            {"name": "Work Visa", "category": "work", "complexity": "complex"}
        ],
        "Family Visas": [
            {"name": "Spouse Visa", "category": "family", "complexity": "medium"},
            {"name": "Parent Visa", "category": "family", "complexity": "complex"},
            {"name": "Child Visa", "category": "family", "complexity": "simple"}
        ],
        "Comprehensive Set": [
            {"name": "Tourist Visa", "category": "visitor", "complexity": "simple"},
            {"name": "Business Visa", "category": "business", "complexity": "medium"},
            {"name": "Student Visa", "category": "student", "complexity": "medium"},
            {"name": "Skilled Worker Visa", "category": "work", "complexity": "complex"},
            {"name": "Family Reunion Visa", "category": "family", "complexity": "medium"},
            {"name": "Transit Visa", "category": "transit", "complexity": "simple"}
        ]
    }
    
    selected_batch = st.selectbox("Select Batch Type", list(batch_options.keys()))
    
    # Show what will be generated
    st.markdown("#### Batch Contents")
    batch_specs = batch_options[selected_batch]
    
    df_batch = pd.DataFrame(batch_specs)
    st.dataframe(df_batch, hide_index=True, use_container_width=True)
    
    # Generation options
    col1, col2 = st.columns(2)
    with col1:
        generate_policies = st.checkbox("Generate Policy Documents", value=True)
        generate_results = st.checkbox("Generate Mock Results", value=True)
    
    with col2:
        save_files = st.checkbox("Save to Files", value=True)
        create_comparison = st.checkbox("Create Comparison Report", value=True)
    
    # Generate batch
    if st.button("🚀 Generate Batch", type="primary"):
        with st.spinner(f"Generating batch of {len(batch_specs)} items..."):
            try:
                batch_data = {}
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, spec in enumerate(batch_specs):
                    status_text.text(f"Processing: {spec['name']}")
                    
                    item_data = {}
                    
                    # Generate policy if requested
                    if generate_policies:
                        policy_content = st.session_state.policy_generator.generate_policy(
                            visa_category=spec['category'],
                            visa_name=spec['name'],
                            complexity=spec['complexity']
                        )
                        item_data['policy'] = policy_content
                        
                        # Save policy if requested
                        if save_files:
                            filename = f"{spec['name'].lower().replace(' ', '_')}.txt"
                            st.session_state.policy_generator.save_policy(
                                policy_content, filename, "data/synthetic"
                            )
                    
                    # Generate results if requested
                    if generate_results:
                        results = st.session_state.mock_generator.generate_complete_workflow_results(
                            spec['name']
                        )
                        item_data['results'] = results
                        
                        # Save results if requested
                        if save_files:
                            output_dir = Path("data/synthetic/results")
                            output_dir.mkdir(parents=True, exist_ok=True)
                            
                            filename = f"{spec['name'].lower().replace(' ', '_')}_results.json"
                            file_path = output_dir / filename
                            
                            with open(file_path, 'w') as f:
                                json.dump(results, f, indent=2, default=str)
                    
                    batch_data[spec['name']] = item_data
                    progress_bar.progress((i + 1) / len(batch_specs))
                
                status_text.text("Batch generation complete!")
                st.session_state.batch_data = batch_data
                
                st.success(f"✅ Generated {len(batch_specs)} items successfully!")
                
                # Create comparison if requested
                if create_comparison and generate_results:
                    create_batch_comparison(batch_data)
                
            except Exception as e:
                st.error(f"❌ Batch generation error: {str(e)}")
    
    # Display batch results
    if hasattr(st.session_state, 'batch_data'):
        st.divider()
        st.markdown("#### Batch Results")
        
        batch_summary = []
        for name, data in st.session_state.batch_data.items():
            summary_item = {'Name': name}
            
            if 'policy' in data:
                summary_item['Policy Length'] = f"{len(data['policy'])} chars"
            
            if 'results' in data:
                stats = data['results']['outputs']['summary_statistics']
                summary_item['Requirements'] = stats['total_requirements']
                summary_item['Questions'] = stats['total_questions']
                summary_item['Validation'] = f"{stats['validation_score']:.1f}%"
            
            batch_summary.append(summary_item)
        
        df_summary = pd.DataFrame(batch_summary)
        st.dataframe(df_summary, hide_index=True, use_container_width=True)


def create_batch_comparison(batch_data):
    """Create comparison analysis for batch data."""
    
    st.markdown("#### Batch Comparison Analysis")
    
    # Extract comparison data
    comparison_data = {}
    for name, data in batch_data.items():
        if 'results' in data:
            comparison_data[name] = data['results']
    
    if comparison_data:
        # Create comparison charts
        col1, col2 = st.columns(2)
        
        # Requirements comparison
        with col1:
            req_data = []
            for name, results in comparison_data.items():
                stats = results['outputs']['summary_statistics']
                req_data.append({
                    'Policy': name,
                    'Requirements': stats['total_requirements']
                })
            
            df_req = pd.DataFrame(req_data)
            fig = px.bar(df_req, x='Policy', y='Requirements', title="Requirements Comparison")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Validation scores comparison
        with col2:
            val_data = []
            for name, results in comparison_data.items():
                stats = results['outputs']['summary_statistics']
                val_data.append({
                    'Policy': name,
                    'Validation Score': stats['validation_score']
                })
            
            df_val = pd.DataFrame(val_data)
            fig = px.bar(df_val, x='Policy', y='Validation Score', title="Validation Scores")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)


def show_export_options():
    """Show export and download options."""
    
    st.subheader("📥 Export & Download")
    st.markdown("Export generated data in various formats for external use.")
    
    # Check what data is available
    has_policy = hasattr(st.session_state, 'generated_policy')
    has_results = hasattr(st.session_state, 'generated_results')
    has_batch = hasattr(st.session_state, 'batch_data')
    
    if not (has_policy or has_results or has_batch):
        st.info("Generate some data first to see export options.")
        return
    
    # Export options
    st.markdown("#### Available Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if has_policy:
            st.success("✅ Generated Policy")
            policy = st.session_state.generated_policy
            
            # Use preview content for download since 'content' key doesn't exist
            policy_content = policy.get('preview', 'Generated policy content...')
            st.download_button(
                label="📄 Download Policy (TXT)",
                data=policy_content,
                file_name=f"{policy.get('visa_type', 'policy').lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.info("No policy generated")
    
    with col2:
        if has_results:
            st.success("✅ Generated Results")
            results_info = st.session_state.generated_results
            
            json_str = json.dumps(results_info['results'], indent=2, default=str)
            st.download_button(
                label="📊 Download Results (JSON)",
                data=json_str,
                file_name=f"{results_info['policy_name'].lower().replace(' ', '_')}_results.json",
                mime="application/json"
            )
        else:
            st.info("No results generated")
    
    with col3:
        if has_batch:
            st.success("✅ Batch Data")
            
            # Create combined export
            combined_data = {
                'generated_at': datetime.now().isoformat(),
                'batch_summary': {},
                'policies': {},
                'results': {}
            }
            
            for name, data in st.session_state.batch_data.items():
                if 'policy' in data:
                    combined_data['policies'][name] = data['policy']
                if 'results' in data:
                    combined_data['results'][name] = data['results']
            
            json_str = json.dumps(combined_data, indent=2, default=str)
            st.download_button(
                label="📦 Download Batch (JSON)",
                data=json_str,
                file_name=f"batch_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No batch data")
    
    # Bulk export options
    if has_batch:
        st.divider()
        st.markdown("#### Bulk Export Options")
        
        col_bulk1, col_bulk2 = st.columns(2)
        
        with col_bulk1:
            if st.button("📁 Export All Policies as ZIP"):
                st.info("ZIP export functionality would be implemented here")
        
        with col_bulk2:
            if st.button("📊 Create Excel Report"):
                st.info("Excel export functionality would be implemented here")


# Remove the direct call to avoid execution when imported
